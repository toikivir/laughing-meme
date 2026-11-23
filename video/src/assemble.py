"""Assemble the EverFunded comparison video.

Pipeline:
  1. build a timeline from the narration chunks (intro -> chunk blocks)
  2. render each slide still as a Ken-Burns clip with faded edges + burned captions
  3. concatenate video, synthesise a music bed + SFX, mix with narration
  4. mux to video/out/everfunded_account_comparison.mp4

Run:  python3 video/src/assemble.py
"""
from __future__ import annotations

import math
import os
import re
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "video", "src"))
from narration import CHUNKS  # noqa: E402

WORK = "/tmp/vid"
FONT_DIR = os.path.join(ROOT, "video", "assets", "fonts")
SLIDES = os.path.join(WORK, "slides")
AUD = os.path.join(ROOT, "video", "audio", "narration")
INTRO = os.path.join(ROOT, "video", "assets", "Intro.mp4")
OUTDIR = os.path.join(ROOT, "video", "out")
OUT = os.path.join(OUTDIR, "everfunded_account_comparison.mp4")

FPS = 30
PAD = 0.55          # visual hold after each narration block
FADE = 0.35         # edge fade between slides
CRF = int(os.environ.get("CRF", "28"))
MAXRATE = os.environ.get("MAXRATE", "2600k")
SR = 44100


def sh(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        raise SystemExit(f"FAILED: {' '.join(map(str, args))}\n{r.stderr[-2000:]}")
    return r


def dur(path):
    o = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=nw=1:nk=1", str(path)]).stdout.strip()
    return float(o)


# ------------------------------------------------------------------ audio ---
def synth_music(total, sr=SR):
    """Slow lo-fi pad bed: Am - F - C - G, sub root, sparse pluck."""
    n = int(total * sr)
    t = np.arange(n) / sr
    out = np.zeros(n, dtype=np.float64)
    roots = [110.00, 87.31, 130.81, 98.00]          # A2 F2 C3 G2
    bar = 4.0
    for i, root in enumerate(roots):
        start = i * bar
        seg = int(bar * sr)
        idx = np.arange(seg)
        tt = idx / sr
        env = np.minimum(1.0, tt / 1.2) * np.minimum(1.0, (bar - tt) / 1.2)
        env = np.clip(env, 0, 1) ** 1.5
        chord = np.zeros(seg)
        for mult, amp in [(1.0, 0.30), (1.1892, 0.20), (1.4983, 0.22), (2.0, 0.12)]:
            det = 1.0 + 0.0015 * np.sin(2 * np.pi * 0.11 * tt + i)
            chord += amp * np.sin(2 * np.pi * root * mult * det * tt)
        pos = int(start * sr)
        out[pos:pos + seg] += chord * env * 0.35
        sub = 0.22 * np.sin(2 * np.pi * (root / 2) * tt)
        out[pos:pos + seg] += sub * env
    # sparse pluck melody (A minor pentatonic), one note per 2 bars
    notes = [440.0, 523.25, 587.33, 659.25, 783.99, 880.0]
    rng = np.random.default_rng(7)
    step = 2.0
    k = 0
    while k * step < total - 1:
        f = notes[int(rng.integers(0, len(notes)))]
        st = int(k * step * sr)
        ln = int(1.1 * sr)
        tt = np.arange(ln) / sr
        env = np.exp(-tt * 3.0)
        tone = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2 * tt)
        out[st:st + ln] += tone * env * 0.10
        k += 1
    # gentle limiter
    peak = np.max(np.abs(out)) or 1.0
    out = out / peak * 0.72
    return np.stack([out, out], axis=1)


def _noise(n, sr):
    return np.random.default_rng(3).standard_normal(n)


def synth_sfx(total, events, sr=SR):
    """events: list of (time, kind)."""
    n = int(total * sr)
    out = np.zeros(n)
    for t0, kind in events:
        st = int(t0 * sr)
        if kind == "whoosh":
            ln = int(0.55 * sr)
            tt = np.arange(ln) / sr
            nz = _noise(ln, sr)
            # simple swept bandpass via cumulative smoothing
            k = np.linspace(0.02, 0.35, ln)
            sm = np.cumsum(nz * k) / np.maximum(np.cumsum(k), 1e-6)
            sig = (nz - sm) * np.sin(np.pi * tt / 0.55) ** 2
            out[st:st + ln] += sig * 0.9
        elif kind == "pop":
            ln = int(0.14 * sr)
            tt = np.arange(ln) / sr
            f = 520 + 420 * (tt / 0.14)
            env = np.exp(-tt * 22)
            out[st:st + ln] += np.sin(2 * np.pi * f * tt) * env * 0.7
        elif kind == "ding":
            ln = int(0.7 * sr)
            tt = np.arange(ln) / sr
            env = np.exp(-tt * 6.0)
            sig = np.sin(2 * np.pi * 1174.7 * tt) + 0.4 * np.sin(2 * np.pi * 1760 * tt)
            out[st:st + ln] += sig * env * 0.45
        elif kind == "riser":
            ln = int(1.1 * sr)
            tt = np.arange(ln) / sr
            f = 200 + 900 * (tt / 1.1) ** 2
            env = np.sin(np.pi * tt / 1.1) ** 2
            out[st:st + ln] += np.sin(2 * np.pi * f * tt) * env * 0.25
    peak = np.max(np.abs(out)) or 1.0
    return np.stack([out / peak * 0.8, out / peak * 0.8], axis=1)


def wav_write(path, data, sr=SR):
    import wave
    import struct
    x = np.clip(data, -1.0, 1.0)
    pcm = (x * 32767).astype("<i2").tobytes()
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm)


# ------------------------------------------------------------- captions -----
def caption_units(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    units, cur = [], ""
    for p in parts:
        if len(cur) + len(p) + 1 <= 100:
            cur = (cur + " " + p).strip()
        else:
            if cur:
                units.append(cur)
            cur = p
    if cur:
        units.append(cur)
    return units


def ass_time(sec):
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_escape(s):
    return s.replace("{", "(").replace("}", ")").replace("\n", "\\N")


def build_ass(events, path, playres=(1920, 1080)):
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {playres[0]}", f"PlayResY: {playres[1]}",
        "WrapStyle: 2", "", "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, "
        "BorderStyle, Outline, Shadow, MarginL, MarginR, MarginV, Alignment",
        "Style: Default,Inter,42,&H00FFFFFF,&H00000000,&H96000000,-1,1,3,1,80,80,48,2",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for st, en, txt in events:
        words = txt.split(" ")
        lines_out = []
        cur = ""
        for w in words:
            if len(cur) + len(w) + 1 <= 46:
                cur = (cur + " " + w).strip()
            else:
                lines_out.append(cur)
                cur = w
        lines_out.append(cur)
        txt = ass_escape("\\N".join(lines_out))
        lines.append(f"Dialogue: 0,{ass_time(st)},{ass_time(en)},Default,,0,0,0,,{txt}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ------------------------------------------------------------------- main ---
def main():
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)

    intro_dur = dur(INTRO)
    timeline = []
    t = intro_dur
    for c in CHUNKS:
        d = dur(os.path.join(AUD, f"{c['id']}.mp3"))
        timeline.append(dict(c, audio=d, start=t, seg=d + PAD))
        t += d + PAD
    total = t + 1.2
    print(f"intro {intro_dur:.2f}s | narration {sum(x['audio'] for x in timeline):.1f}s | total {total:.1f}s")

    # caption events per chunk
    for blk in timeline:
        units = caption_units(blk["text"])
        weights = [len(u) for u in units]
        sw = sum(weights) or 1
        st = blk["start"]
        for u, w in zip(units, weights):
            d = blk["audio"] * (w / sw)
            blk.setdefault("caps", []).append([st, st + d, u])
            st += d

    # ---- render state clips -------------------------------------------------
    seg_files = []
    idx = 0
    for blk in timeline:
        weights = [w for _, w in blk["slides"]]
        sw = sum(weights)
        t0 = blk["start"]
        for name, w in blk["slides"]:
            sd = blk["seg"] * (w / sw)
            s0, s1 = t0, t0 + sd
            img = os.path.join(SLIDES, name)
            seg_path = os.path.join(WORK, f"seg_{idx:03d}.mp4")
            ev = [(max(a, s0) - s0, min(b, s1) - s0, tx)
                  for a, b, tx in blk.get("caps", []) if b > s0 and a < s1]
            ass_p = os.path.join(WORK, f"cap_{idx:03d}.ass")
            build_ass(ev, ass_p)
            vf = (f"zoompan=z='min(zoom+0.0009,1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                  f":d=1:s=1920x1080:fps={FPS},format=yuv420p"
                  f",ass={ass_p}:fontsdir={FONT_DIR}")
            if not (os.path.exists(seg_path) and os.path.getsize(seg_path) > 10000):
                sh(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", img, "-t", f"{sd:.3f}",
                    "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", str(CRF),
                    "-maxrate", MAXRATE, "-bufsize", "5200k", "-pix_fmt", "yuv420p",
                    "-r", str(FPS), "-an", seg_path])
            seg_files.append(seg_path)
            t0 = s1
            idx += 1
    print(f"rendered {len(seg_files)} clips")

    # ---- concat video -------------------------------------------------------
    import json as _json
    with open(os.path.join(WORK, "concat.txt"), "w") as f:
        f.write(f"file '{INTRO}'\n")
        for p in seg_files:
            f.write(f"file '{p}'\n")
    raw = os.path.join(WORK, "video_raw.mp4")
    if not (os.path.exists(raw) and os.path.getsize(raw) > 100000):
        sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
            "-i", os.path.join(WORK, "concat.txt"), "-c:v", "libx264", "-preset", "veryfast",
            "-crf", str(CRF), "-maxrate", MAXRATE, "-bufsize", "5200k", "-pix_fmt", "yuv420p",
            "-an", raw])

    # ---- audio: narration track --------------------------------------------
    sil = os.path.join(WORK, "silence.wav")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
        "-i", "anullsrc=r=44100:cl=stereo", "-t", "900", sil])
    inputs, labels = [], []
    idx = 0
    inputs += ["-t", f"{intro_dur:.3f}", "-i", sil]
    labels.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo[s{idx}]")
    idx += 1
    for i, blk in enumerate(timeline):
        inputs += ["-i", os.path.join(AUD, f"{blk['id']}.mp3")]
        labels.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo[s{idx}]")
        idx += 1
        if i < len(timeline) - 1:
            inputs += ["-t", f"{PAD:.3f}", "-i", sil]
            labels.append(f"[{idx}:a]aformat=sample_rates=44100:channel_layouts=stereo[s{idx}]")
            idx += 1
    n = idx
    fc = (";".join(labels) + ";" + "".join(f"[s{i}]" for i in range(n)) +
           f"concat=n={n}:v=0:a=1[raw];[raw]loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    narr = os.path.join(WORK, "narration.wav")
    if not (os.path.exists(narr) and os.path.getsize(narr) > 100000):
        cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs +
               ["-filter_complex", fc, "-map", "[out]", "-ar", "44100", narr])
        sh(cmd)

    # ---- audio: music + sfx -------------------------------------------------
    music = synth_music(total)
    wav_write(os.path.join(WORK, "music.wav"), music)
    events = []
    for blk in timeline:
        events.append((blk["start"], "whoosh"))
        if len(blk["slides"]) > 1:
            wsum = 0.0
            for nm, w in blk["slides"][:-1]:
                wsum += w
                events.append((blk["start"] + blk["seg"] * (wsum / sum(x[1] for x in blk["slides"])), "pop"))
    events.append((timeline[-1]["start"], "riser"))
    sfx = synth_sfx(total, events)
    wav_write(os.path.join(WORK, "sfx.wav"), sfx)

    # ---- mix + mux ----------------------------------------------------------
    sh(["ffmpeg", "-y", "-loglevel", "error",
        "-i", raw, "-i", narr, "-i", os.path.join(WORK, "music.wav"),
        "-i", os.path.join(WORK, "sfx.wav"),
        "-filter_complex",
        # Measured on this ffmpeg build: amix divides by ~3.6 for 3 inputs (no
        # `normalize` option exists here). Pre-gaining by 3.6 lands the voice at unity.
        # music and sfx sit well under the voice. This build's `alimiter` amplifies
        # rather than limits, so no limiter is used -- a linear trim sets level while
        # keeping peaks safely below 0 dBFS. Final: ~-16 LUFS, ~-1.5 dBFS peaks.
        "[2:a]volume=0.15[m2];"
        "[3:a]volume=0.75[s2];"
        "[1:a]volume=3.6[v2];"
        "[v2][m2][s2]amix=inputs=3:duration=first[mixA];"
        "[mixA]volume=0.8[out]",
        "-map", "0:v", "-map", "[out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", OUT])

    size = os.path.getsize(OUT) / 1048576
    print(f"WROTE {OUT}  {size:.1f} MB  duration {dur(OUT):.1f}s")


if __name__ == "__main__":
    main()
