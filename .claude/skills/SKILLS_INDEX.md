# VidzEditor — Installed Video Skills Index

Installed 2026-11-23 from the user's list. Each entry below is a cloned GitHub repo
(trimmed of heavy media/demos/tests/generated docs to respect the 128 MB workspace cap —
re-clone the URL if the full repo is needed).

| # | Skill / Tool | Source | Local path | SKILL.md |
|---|--------------|--------|------------|----------|
| 1 | yt-dlp | github.com/yt-dlp/yt-dlp | *installed via pip* (`yt-dlp 2026.10.26`) | — |
| 2 | Whisper | github.com/openai/whisper | `whisper/` | — (Python lib) |
| 3 | FFmpeg Skill | github.com/kajisho5/ffmpeg-skill | `ffmpeg-skill-kajisho5/` | 19 |
| 4 | FFmpeg Skill | github.com/ychoi-kr/claude-ffmpeg-skill | `claude-ffmpeg-skill/` | 1 |
| 5 | Ghost Editor | github.com/kurbaitaev/ghost-editor | `ghost-editor/` | 1 |
| 6 | Claude Shorts | github.com/agricidaniel/claude-shorts | `claude-shorts/` | 1 |
| 7 | Three.js Skills | github.com/cloudai-x/threejs-skills | `threejs-skills/` | 13 |
| 8 | Three.js Skills | github.com/Impertio-Studio/Three.js-Claude-Skill-Package | `threejs-skill-package/` | 24 |
| 9 | Motion Skills | github.com/iart-ai/motion-skills | `motion-skills/` | 0 (docs/scripts) |
| 10 | Motion Skills | github.com/Barty-Bart/motion-graphics | `motion-graphics/` | 6 |
| 11 | Motion Skills | github.com/mattypark/Motion-graphics-skill | `motion-graphics-skill/` | 1 |
| 12 | MotionClone | github.com/LPengYang/MotionClone | `MotionClone-LPengYang/` | 0 (ML model code) |
| 13 | MotionClone | github.com/Bujiazi/MotionClone | `MotionClone-Bujiazi/` | 0 (ML model code) |
| 14 | HyperFrames | github.com/heygen-com/hyperframes | `hyperframes/` | 22 |
| 15 | Awesome Skills | github.com/zhuyansen/awesome-claude-video-skills | `awesome-claude-video-skills/` | 0 (curated list) |

## Runtime tools installed

- **ffmpeg** + **ffprobe** — static builds on `PATH` (`/usr/local/bin`), from
  `@ffmpeg-installer/linux-x64` / `@ffprobe-installer/linux-x64` (npm registry).
- **yt-dlp** — `pip3 install yt-dlp` → `2026.10.26`.
- **openai-whisper** — `pip3 install openai-whisper` → `20250625`, torch `2.15.0`.
  ⚠️ Whisper model weights download from `openaipublic.azureedge.net`, which is blocked in
  this sandbox. Models must be supplied locally (or use `faster-whisper`) for transcription.

## Trimmed to stay under 128 MB (re-clone URLs above to restore)

- All `.git/` directories removed.
- Demos, sample footage, showcase reels, docs sites, test fixtures, model checkpoints
  (e.g. `face_landmarker.task`), and generated registries dropped from the heavier repos
  (hyperframes, ghost-editor, ffmpeg-skill, MotionClone, motion-graphics, awesome list).
- Current footprint: ~87 MB.

## Notes

- `ffmpeg-skill-kajisho5` ships extra generic Claude Code skills under its nested
  `.claude/skills/` (code-review, git-hygiene, CI, release, etc.).
- `hyperframes` is a HeyGen video-generation framework; its `skills/` + core packages are
  kept, the web studio frontend and block registry were dropped.
- Two MotionClone repos are separate implementations of the same paper — both kept.
