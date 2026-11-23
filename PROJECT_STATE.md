# PROJECT_STATE

> Checkpoint ledger. Update after every milestone. Sandbox refreshes wipe this file
> and all untracked files — **commit to git after each milestone**.

## Current branch

`arena/54aa1182-laughing-meme` (base `main`). HEAD at last write: see `git log -1`.

## Active task

**EverFunded YouTube review video — v2 DELIVERED (real screen captures).**

- Deliverable: `video/out/everfunded_account_comparison.mp4`
  - 1920x1080, 30 fps, H.264 + AAC stereo
  - 539.9 s (**9:00**, inside the requested 8–10 min)
  - Captions burned in (`ass=`), motion-graphics slides, TTS narration, synth music + SFX
  - Integrated loudness **-16.4 LUFS**, true peak **-1.27 dBTP**, 17.2 MB
  - **Real captures (user correction "You have to screen capture"):**
    - c02 overview slide = real everfunded.com "Choose Your EverFunded Challenge"
      comparison table (`video/assets/captures/comparison_table.png`, from
      Walkthrough-Final 562 s)
    - c08 dashboard segment = 27 s of genuine `app.everfunded.com` dashboard footage
      (`video/assets/captures/dashboard_demo.mp4`, from Walkthrough-Final 505–535 s)
    - c10 CTA slide = real checkout capture with GEOID applied
      (`video/assets/captures/checkout_panel.png`)
    - slide 12 objectives = faithful reproduction of real dashboard labels/values
- Uploaded to Google Drive folder **`Agent Everfunded`**
  - folder id `13w8UZ7P1nS0JNT9XKt6oYUwmMxh4iuzk`
  - v2 file id `1uoBHjJSyp8EalAfZ7wF5UObdDfRweWqg`
  - https://drive.google.com/file/d/1uoBHjJSyp8EalAfZ7wF5UObdDfRweWqg/view
  - v1 (mockups) file id `1PrQA8haR1xgYcS_QSNpFJ0VBOeVY-0Qm` — superseded

## Video structure (15 slides -> 10 narration chunks)

| chunk | topic | slides |
|---|---|---|
| c01 hook | intro + agenda (opens "Hey what's up guys, it's Geoid...") | 01,02 |
| c02 overview | three routes side by side | 03 |
| c03 twostep | 2-Step rules + $100K math | 04,05 |
| c04 tradeoff | time/room vs discipline framing | 06 |
| c05 onestep | 1-Step spec | 07 |
| c06 instant | Instant + trailing-limit diagram | 08,09 |
| c07 sizes | six sizes, fees, leverage, platforms | 10 |
| c08 dashboard | home tab + objectives tabs | 11,12 |
| c09 pick | reviewer's pick (2-Step) and why | 13 |
| c10 cta | GEOID code, referral CTA, recap | 14,15 |

Narration total 539.5 s; intro clip 1.44 s; 10 x 0.55 s pads -> 545.5 s.

## How to rebuild

```bash
bash tools/setup_media.sh                       # ffmpeg/ffprobe/pillow/numpy/fonts (idempotent)
python3 video/src/build.py /tmp/vid/slides      # renders 15 PNGs
python3 video/src/assemble.py                   # -> video/out/*.mp4 (uses /tmp/vid cache)
```

Env knobs: `CRF`, `MAXRATE`, `FPS`, `SR`. Defaults CRF=28 / MAXRATE=2600k;
the delivered render used `CRF=20 MAXRATE=8000k`.

## ffmpeg build quirks (important — this sandbox's static build)

Verified empirically, do not "fix" these blindly:

- `amix` has **no `normalize` option** and **divides by ~3.6** for 3 inputs
  (not by input count). Every branch is pre-gained to cancel the division.
- `alimiter` **amplifies instead of limiting** (`limit=0.95` -> -1.1 dB but
  `limit=0.70` clips at 0 dB). Do not use it; use a linear `volume` trim.
- `sidechaincompress` fails with "Input/output error". Avoid.
- `volume` accepts linear factors and normal dB strings; `+2.9dB` scaled oddly,
  so prefer linear factors.

## Environment / prior work

- 15 GitHub skills under `.claude/skills/` (see `SKILLS_INDEX.md`), commit `5673c5d`.
- Snapshot tarballs go to Drive and are deleted locally afterwards.
- Network egress is allowlisted: `everfunded.com` is NOT reachable from bash or
  Chromium, so no live screen capture was possible. All visuals are designed
  locally from facts gathered via `fetch_page`.
- Demo credentials were supplied by the user for a walkthrough; the site could
  not be reached, so the dashboard section is an illustrative mock labelled as such
  rather than recorded footage.
- Drive ids: `Arena_Workspace_Sync` `1tEpJ57vzSklFaO4mhP7PUcDbAVWst0yM`;
  `Arrox` `14tcnfy7ppSgjjzlc5-Lohyr9F0vInya2`; `Intro.mp4` `13GOkFusvedXh0hLRzIxlLLQLN45c2yQG`.
