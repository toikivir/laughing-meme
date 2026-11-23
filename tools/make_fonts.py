"""Install display fonts from npm (@fontsource) and convert woff2 -> ttf into the repo."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "video", "assets", "fonts")
TMP = "/tmp/fontsrc"

WANT = {
    "inter": [400, 500, 600, 700, 800],
    "space-grotesk": [500, 700],
    "oswald": [500, 600, 700],
    "jetbrains-mono": [400, 700],
}


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
    subprocess.run(["npm", "init", "-y"], cwd=TMP, capture_output=True)
    pkgs = [f"@fontsource/{p}" for p in WANT]
    r = subprocess.run(["npm", "install", "--silent", *pkgs], cwd=TMP, capture_output=True, text=True)
    if r.returncode != 0:
        print("npm font install failed:", r.stderr[-500:])
        return 1
    from fontTools.ttLib import woff2
    for pkg, weights in WANT.items():
        for w in weights:
            src = os.path.join(TMP, "node_modules", "@fontsource", pkg, "files",
                               f"{pkg}-latin-{w}-normal.woff2")
            dst = os.path.join(OUT, f"{pkg}-{w}.ttf")
            if not os.path.exists(src):
                print("MISSING", src)
                continue
            woff2.decompress(src, dst)
            print("ok", os.path.basename(dst))
    return 0


if __name__ == "__main__":
    sys.exit(main())
