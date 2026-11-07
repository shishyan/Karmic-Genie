# Storage policy

**Google Drive (nagaraj957@gmail.com) is the central repository** for all videos, audio, renders, clips,
thumbnails, bundles and episode build artifacts. GitHub is only for code sync (pipeline scripts, SKILL.md, docs).

- Drive project folder: `Karmic_Genie_Show_S01E01` (Colab/remote agents read from here)
- Dated sync drops: `remote_agent_sync_YYYYMMDD/` inside that folder
- Git LFS is not used. Do not add `filter=lfs` rules.
- Never commit OAuth tokens, `.env`, or media; `.gitignore` enforces this.
