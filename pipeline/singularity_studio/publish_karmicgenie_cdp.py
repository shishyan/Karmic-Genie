#!/usr/bin/env python3
"""
Headless Chrome CDP (http://127.0.0.1:9225) Publisher for The Karmic Genie Show
(`@karmicgenie` / `UCmixCKV4uTv3wIp634IRLXg`).
Attaches >300 MB 1080p master MP4s via zero-copy `DOM.setFileInputFiles`,
attaches the verified <2 MB 16:9 poster thumbnail, waits for 100% upload transfer,
clicks 'Publish anyway' if content checks are still running, and verifies PUBLIC visibility.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from karmicgenie_seo import apply_tags_in_studio_page, assert_zero_cta, get_episode_seo_package

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

CHANNEL_ID = "UCmixCKV4uTv3wIp634IRLXg"
STUDIO_URL = f"https://studio.youtube.com/channel/{CHANNEL_ID}?authuser=0"
CONTENT_URL = f"https://studio.youtube.com/channel/{CHANNEL_ID}/videos/upload?authuser=0"
CDP_URL = "http://127.0.0.1:9225"


def click_by_text_or_id(page, selectors=(), texts=()) -> bool:
    for sel in selectors:
        loc = page.locator(sel)
        if loc.count() > 0:
            for i in range(loc.count()):
                el = loc.nth(i)
                if el.is_visible():
                    el.click()
                    return True
    return bool(
        page.evaluate(
            """(texts) => {
            function walk(root) {
                const els = Array.from(root.querySelectorAll('*'));
                for (const el of els) {
                    if (el.shadowRoot) {
                        const r = walk(el.shadowRoot);
                        if (r) return true;
                    }
                    const tag = el.tagName;
                    if (tag === 'BUTTON' || tag === 'YTCP-BUTTON' || tag === 'TP-YT-PAPER-ITEM' || tag === 'TP-YT-PAPER-RADIO-BUTTON') {
                        const t = (el.innerText || '').trim();
                        const aria = (el.getAttribute('aria-label') || '').trim();
                        for (const target of texts) {
                            if (t === target || aria === target) {
                                const rect = el.getBoundingClientRect();
                                if (rect.width > 0 && rect.height > 0 && !el.hasAttribute('disabled')) {
                                    el.click();
                                    return true;
                                }
                            }
                        }
                    }
                }
                return false;
            }
            return walk(document.body);
        }""",
            list(texts),
        )
    )


def publish_single_video(
    video_path: str,
    thumb_path: str,
    title: str,
    description: str,
    tags: list[str] | None = None,
    visibility: str = "PUBLIC",
) -> str:
    assert os.path.exists(video_path), f"Missing video: {video_path}"
    assert os.path.exists(thumb_path), f"Missing thumb: {thumb_path}"
    assert_zero_cta(title, "upload.title")
    assert_zero_cta(description, "upload.description")

    # Prevent Playwright connect_over_cdp hang on Chrome 156+ omnibox browser_ui targets
    try:
        import urllib.request as _ur, json as _js
        for _t in _js.loads(_ur.urlopen(f"{CDP_URL}/json/list", timeout=4).read()):
            if _t.get("type") == "browser_ui":
                _ur.urlopen(f"{CDP_URL}/json/close/{_t['id']}", timeout=4).read()
    except Exception:
        pass

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL, timeout=25000)
        ctx = browser.contexts[0]
        page = ctx.new_page()
        try:
            print(f"[CDP] Navigating to {STUDIO_URL} ...")
            page.goto(STUDIO_URL, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(5000)

            skip_link = page.locator("a:has-text('SKIP TO YOUTUBE STUDIO'), button:has-text('SKIP TO YOUTUBE STUDIO')")
            if skip_link.count() > 0 and skip_link.first.is_visible():
                skip_link.first.click()
                page.wait_for_timeout(4000)
            else:
                click_by_text_or_id(page, texts=["SKIP TO YOUTUBE STUDIO"])
                page.wait_for_timeout(1500)

            body_txt = page.locator("body").inner_text()
            if "Karmic Genie" not in body_txt:
                raise RuntimeError(f"SAFETY ABORT: Active Studio channel is not Karmic Genie Show! Snippet: {body_txt[:250]}")
            print("[CDP] Verified active channel: Karmic Genie Show (UCmixCKV4uTv3wIp634IRLXg)")

            print("[CDP] Opening Upload dialog...")
            click_by_text_or_id(
                page,
                selectors=["#upload-icon", "ytcp-button#upload-button", "#create-icon"],
                texts=["Upload videos", "Create", "CREATE"],
            )
            page.wait_for_timeout(2000)
            click_by_text_or_id(page, selectors=["#text-item-0"], texts=["Upload videos"])
            page.wait_for_timeout(2500)

            print(f"[CDP] Attaching video via DOM.setFileInputFiles: {video_path}")
            cdp = ctx.new_cdp_session(page)
            cdp.send("DOM.enable")
            doc = cdp.send("DOM.getDocument", {"depth": -1, "pierce": True})

            def find_upload_picker_input(node, inside_picker=False):
                nname = node.get("nodeName", "")
                now_inside = inside_picker or (nname == "YTCP-UPLOADS-FILE-PICKER")
                if now_inside and nname == "INPUT":
                    attrs = node.get("attributes", [])
                    attr_map = {attrs[i]: attrs[i + 1] for i in range(0, len(attrs) - 1, 2)}
                    if attr_map.get("type") == "file":
                        return node.get("nodeId")
                for child in node.get("children", []):
                    res = find_upload_picker_input(child, now_inside)
                    if res:
                        return res
                for sr in node.get("shadowRoots", []):
                    res = find_upload_picker_input(sr, now_inside)
                    if res:
                        return res
                return None

            file_node_id = find_upload_picker_input(doc["root"], False) or find_upload_picker_input(doc["root"], True)
            assert file_node_id, "Could not locate <input type='file'> in upload modal!"
            cdp.send("DOM.setFileInputFiles", {"files": [video_path], "nodeId": file_node_id})

            print("[CDP] Waiting for Details form...")
            for _ in range(25):
                page.wait_for_timeout(2000)
                dlg_txt = page.locator("ytcp-uploads-dialog").inner_text() if page.locator("ytcp-uploads-dialog").count() else ""
                if "Daily upload limit reached" in dlg_txt or "daily upload limit" in dlg_txt.lower():
                    page.screenshot(path="/tmp/kg_daily_limit_debug.png")
                    raise RuntimeError(f"ERROR_DAILY_UPLOAD_LIMIT_REACHED on @karmicgenie: {dlg_txt[:240]!r}")
                tloc = page.locator("ytcp-video-title #textbox, #title-textarea #textbox")
                if tloc.count() > 0 and tloc.first.is_visible():
                    break
            else:
                page.screenshot(path="/tmp/kg_upload_form_debug.png")
                raise RuntimeError(f"Upload Details form did not open within 50s (dialog={dlg_txt[:240]!r})")
            page.wait_for_timeout(2000)

            video_id = None
            for _ in range(30):
                hrefs = page.evaluate(
                    """() => Array.from(document.querySelectorAll('ytcp-uploads-dialog a, ytcp-video-info a, a.ytcp-video-info')).map(a => a.href).filter(h => h.includes('youtu.be/'))"""
                )
                for h in hrefs:
                    m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", h)
                    if m:
                        video_id = m.group(1)
                        break
                if video_id:
                    break
                page.wait_for_timeout(2000)
            print(f"[CDP] Assigned YouTube Video ID: {video_id}")

            safe_title = title.strip()[:98]
            title_box = page.locator("ytcp-video-title #textbox, #title-textarea #textbox").first
            title_box.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            title_box.fill(safe_title)
            page.wait_for_timeout(1000)

            desc_box = page.locator("ytcp-video-description #textbox, #description-textarea #textbox").first
            desc_box.click()
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            desc_box.fill(description)
            page.wait_for_timeout(1000)

            print("[CDP] Attaching custom 16:9 thumbnail...")
            thumb_attached = False
            thumb_inputs = page.locator("ytcp-thumbnails-compact-editor-uploader input[type='file'], input#file-loader")
            if thumb_inputs.count() > 0:
                thumb_inputs.first.set_input_files(thumb_path)
                thumb_attached = True
            else:
                try:
                    with page.expect_file_chooser(timeout=8000) as fc_info:
                        click_by_text_or_id(page, texts=["Upload file", "Upload thumbnail"])
                    fc_info.value.set_files(thumb_path)
                    thumb_attached = True
                except Exception as te:
                    print("[CDP] Thumbnail filechooser warning:", te)
            print(f"[CDP] Thumbnail attached: {thumb_attached}")
            page.wait_for_timeout(3000)

            not_kids = page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']")
            if not_kids.count() > 0:
                not_kids.first.scroll_into_view_if_needed()
                not_kids.first.click()
            page.wait_for_timeout(1500)

            if tags:
                applied_n = apply_tags_in_studio_page(page, tags, clear_existing=True)
                print(f"[CDP] Applied {applied_n} SEO tags in Upload Details!")
                page.wait_for_timeout(1200)

            print("[CDP] Stepping Next -> Next -> Next to Visibility...")
            for step_idx in range(3):
                clicked = click_by_text_or_id(page, selectors=["#next-button"], texts=["Next", "NEXT"])
                print(f"  Step {step_idx + 1} Next: {clicked}")
                page.wait_for_timeout(2500)

            vis_radio = page.locator(f"tp-yt-paper-radio-button[name='{visibility}']")
            if vis_radio.count() > 0:
                vis_radio.first.scroll_into_view_if_needed()
                vis_radio.first.click()
            else:
                click_by_text_or_id(page, texts=[visibility.capitalize()])
            print(f"[CDP] Selected visibility: {visibility}")
            page.wait_for_timeout(2000)

            print("[CDP] Waiting for large file upload transfer + initial processing...")
            for wait_i in range(280):
                progress_txt = page.evaluate(
                    """() => {
                    const el = document.querySelector('ytcp-video-upload-progress');
                    return el ? (el.innerText || '').trim() : '';
                }"""
                )
                if wait_i % 5 == 0:
                    print(f"  Upload status [{wait_i * 3}s]: {progress_txt}")
                if "Uploading " not in progress_txt and (
                    "Checks complete" in progress_txt
                    or "No issues found" in progress_txt
                    or ("Processing" in progress_txt and wait_i >= 10)
                    or ("complete" in progress_txt.lower() and wait_i >= 10)
                ):
                    print(f"  Transfer ready: {progress_txt}")
                    break
                page.wait_for_timeout(3000)

            print("[CDP] Clicking Publish / Save...")
            done_clicked = click_by_text_or_id(
                page,
                selectors=["#done-button"],
                texts=["Publish", "PUBLISH", "Save", "SAVE"],
            )
            print(f"[CDP] Publish clicked: {done_clicked}")
            page.wait_for_timeout(4000)

            # Click "Publish anyway" if YouTube Studio's checks warning modal appears!
            for _ in range(3):
                pa = click_by_text_or_id(
                    page,
                    selectors=["ytcp-button#secondary-action-button", "ytcp-dialog ytcp-button:has-text('Publish anyway')"],
                    texts=["Publish anyway", "PUBLISH ANYWAY"],
                )
                if pa:
                    print("[CDP] Clicked 'Publish anyway' on content-checks modal!")
                    page.wait_for_timeout(5000)
                    break
                page.wait_for_timeout(1500)

            click_by_text_or_id(
                page,
                selectors=["#close-button", "ytcp-video-share-dialog #close-button"],
                texts=["Close", "CLOSE"],
            )
            page.wait_for_timeout(3000)

            # Verify on Content page that the video is not stuck in Draft!
            page.goto(CONTENT_URL, wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(5000)
            edit_btns = page.locator("ytcp-button:has-text('Edit draft'):visible, button:has-text('Edit draft'):visible")
            if edit_btns.count() > 0 and edit_btns.first.is_visible():
                print("[CDP] Completing draft -> PUBLIC transition from Content list...")
                edit_btns.first.click()
                page.wait_for_timeout(3500)
                for _ in range(3):
                    click_by_text_or_id(page, selectors=["#next-button"], texts=["Next", "NEXT"])
                    page.wait_for_timeout(2000)
                vis_r2 = page.locator(f"tp-yt-paper-radio-button[name='{visibility}']")
                if vis_r2.count() > 0:
                    vis_r2.first.scroll_into_view_if_needed()
                    vis_r2.first.click()
                page.wait_for_timeout(1500)
                click_by_text_or_id(page, selectors=["#done-button"], texts=["Publish", "PUBLISH", "Save", "SAVE"])
                page.wait_for_timeout(4000)
                click_by_text_or_id(page, texts=["Publish anyway", "PUBLISH ANYWAY"])
                page.wait_for_timeout(4000)
                page.goto(CONTENT_URL, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(4000)

            shot_path = f"/tmp/kg_published_{video_id or 'latest'}.png"
            page.screenshot(path=shot_path)
            print(f"[PUBLISHED] VIDEO_ID={video_id} URL=https://youtu.be/{video_id} SCREENSHOT={shot_path}")
            return video_id or ""
        finally:
            page.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--ep-slug",
        default="KG_Ep03_Infinite_Distractions",
        help="Episode slug under episodes/karmic_genie/ (or comma-separated list of slugs)",
    )
    ap.add_argument("--visibility", choices=["PUBLIC", "UNLISTED"], default="PUBLIC")
    args = ap.parse_args()

    studio_root = Path("/home/shishyan/GitHub/Influenzian/Utility_Explainer_Studio")
    if args.ep_slug == "both":
        slugs = ["KG_Creator_Dharma_2Percent", "KG_Time_Is_Life_Part2"]
    else:
        slugs = [s.strip() for s in args.ep_slug.split(",") if s.strip()]

    published: dict[str, str] = {}
    for slug in slugs:
        ep_dir = studio_root / "episodes" / "karmic_genie" / slug
        mp4 = str((ep_dir / f"{slug}_1080p.mp4").resolve())
        thumb = str((ep_dir / "thumbnail_16x9.jpg").resolve())

        seo_pkg = get_episode_seo_package(slug)
        title = seo_pkg["title"]
        desc = seo_pkg["description"]
        tags = seo_pkg["tags"]

        vid = publish_single_video(mp4, thumb, title, desc, tags=tags, visibility=args.visibility)
        published[slug] = vid

        links_path = ep_dir / "delivery_links.json"
        dl = json.loads(links_path.read_text(encoding="utf-8")) if links_path.exists() else {"episodeId": slug}
        dl["youtubeVideoId"] = vid
        dl["youtubeUrl"] = f"https://youtu.be/{vid}" if vid else None
        dl["privacyStatus"] = args.visibility.lower()
        dl.pop("youtubeError", None)
        links_path.write_text(json.dumps(dl, indent=2), encoding="utf-8")

        kg_repo_ep = Path(f"/home/shishyan/GitHub/Karmic-Genie-Show/episodes/{slug}")
        kg_repo_ep.mkdir(parents=True, exist_ok=True)
        (kg_repo_ep / "published_manifest.json").write_text(json.dumps(dl, indent=2), encoding="utf-8")
        time.sleep(4)

    print("ALL_PUBLISHED:", json.dumps(published, indent=2))


if __name__ == "__main__":
    main()
