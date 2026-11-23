#!/usr/bin/env bash
# VidzEditor media toolchain bootstrap.
# The Arena sandbox only reliably persists git-committed files inside the repo, and
# system installs (/usr/local, site-packages) vanish between sessions — so re-run this
# after any sandbox refresh:  bash tools/setup_media.sh
set -e
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "[1/4] ffmpeg + ffprobe (static, via npm)"
mkdir -p /tmp/ffbin && cd /tmp/ffbin
npm init -y >/dev/null 2>&1 || true
npm install --silent @ffmpeg-installer/linux-x64 @ffprobe-installer/linux-x64 >/dev/null 2>&1
cp node_modules/@ffmpeg-installer/linux-x64/ffmpeg /usr/local/bin/ffmpeg
cp node_modules/@ffprobe-installer/linux-x64/ffprobe /usr/local/bin/ffprobe
chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe
cd /
echo "[2/4] python deps"
pip3 install --quiet --break-system-packages pillow numpy fonttools brotli >/dev/null 2>&1
echo "[3/4] fonts (woff2 -> ttf)"
python3 "$REPO/tools/make_fonts.py"
echo "[4/4] verify"
ffmpeg -version 2>/dev/null | head -1
ffprobe -version 2>/dev/null | head -1
python3 -c "import PIL, numpy, fontTools; print('pillow', PIL.__version__, 'numpy', numpy.__version__)"
