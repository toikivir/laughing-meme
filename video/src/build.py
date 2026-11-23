"""EverFunded comparison video — design system + slide renderer + narration data.

Run:  python3 video/src/build.py [slides_out_dir]
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ tokens --
W, H = 1920, 1080
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "fonts")
CAP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "captures")
_F: dict = {}


def font(name, size):
    key = (name, size)
    if key not in _F:
        _F[key] = ImageFont.truetype(os.path.join(FONT_DIR, f"{name}.ttf"), size)
    return _F[key]


BG, BG_TOP = (7, 11, 22), (10, 16, 32)
PANEL, PANEL_HI, STROKE = (14, 21, 38), (19, 28, 49), (30, 42, 68)
TEXT, MUTED, FAINT = (242, 246, 255), (147, 161, 189), (94, 108, 138)
GREEN, GREEN_HI, TEAL = (34, 197, 94), (74, 222, 128), (56, 189, 248)
GOLD, RED, PURPLE = (245, 181, 68), (240, 82, 82), (139, 124, 250)
MARGIN, CONTENT_W = 120, 1920 - 240


def _lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def canvas(top=BG_TOP, bottom=BG):
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        c = _lerp(top, bottom, y / (H - 1))
        for x in range(W):
            px[x, y] = c
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 80):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 6))
    for y in range(0, H, 80):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 6))
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-W * .35, -H * .35, W * 1.35, H * 1.35], fill=90)
    return Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, vig)


def rr(d, box, r=18, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def measure(d, s, f):
    b = d.multiline_textbbox((0, 0), s, font=f)
    return b[2] - b[0], b[3] - b[1]


def wrap(d, s, f, max_w):
    out = []
    for raw in s.split("\n"):
        cur = ""
        for word in raw.split(" "):
            trial = (cur + " " + word).strip()
            if d.textlength(trial, font=f) <= max_w or not cur:
                cur = trial
            else:
                out.append(cur)
                cur = word
        out.append(cur)
    return "\n".join(out)


def para(d, xy, s, f, fill=TEXT, max_w=CONTENT_W, leading=10, align="left"):
    s = wrap(d, s, f, max_w)
    d.multiline_text(xy, s, font=f, fill=fill, spacing=leading, align=align)
    return measure(d, s, f)


def chip(d, xy, label, f, fg=TEXT, bg=PANEL_HI, px=18, py=10):
    tw, th = measure(d, label, f)
    box = [xy[0], xy[1], xy[0] + tw + 2 * px, xy[1] + th + 2 * py]
    rr(d, box, 999, fill=bg)
    d.text((xy[0] + px, xy[1] + py - 2), label, font=f, fill=fg)
    return box


def card(d, box, r=22, fill=PANEL, outline=STROKE, width=2, glow=None):
    if glow:
        d.rounded_rectangle([box[0] - 3, box[1] - 3, box[2] + 3, box[3] + 3],
                            radius=r + 3, outline=glow, width=3)
    rr(d, box, r, fill=fill, outline=outline, width=width)


def hline(d, x0, x1, y, fill=STROKE, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def header(d, kicker, title, accent=GREEN, y=84):
    chip(d, (MARGIN, y), kicker.upper(), font("oswald-600", 26), fg=accent,
         bg=(accent[0] // 8, accent[1] // 8, accent[2] // 8))
    d.text((MARGIN, y + 52), title, font=font("space-grotesk-700", 60), fill=TEXT)
    hline(d, MARGIN, MARGIN + 90, y + 130, fill=accent, width=4)
    return y + 156


def lower_third(d):
    """Compact channel badge, top-right — keeps the caption zone clear."""
    label = "GEOID"
    f = font("oswald-700", 26)
    tw, th = measure(d, label, f)
    w = tw + 56
    x1 = W - MARGIN
    rr(d, [x1 - w, 40, x1, 40 + th + 26], 12, fill=(10, 14, 26, 215), outline=GREEN, width=2)
    d.text((x1 - w + 28, 40 + 13), label, font=f, fill=GREEN_HI)


def blobs(d, specs):
    for cx, cy, r, col in specs:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


# ------------------------------------------------------------- slide builds --
def s_hero():
    img = canvas(top=(16, 26, 54)); d = ImageDraw.Draw(img, "RGBA")
    blobs(d, [(1520, 180, 520, (34, 197, 94, 26)), (240, 900, 560, (56, 189, 248, 18)),
              (1700, 950, 420, (139, 124, 250, 20))])
    chip(d, (MARGIN, 250), "EVERFUNDED · ACCOUNT COMPARISON", font("oswald-600", 30),
         fg=GREEN_HI, bg=(20, 60, 40))
    d.text((MARGIN - 4, 300), "EVERFUNDED", font=font("space-grotesk-700", 148), fill=TEXT)
    d.text((MARGIN, 468), "2-Step  vs  1-Step  vs  Instant", font=font("oswald-500", 60), fill=GREEN_HI)
    para(d, (MARGIN, 586), "Which funded-account route actually fits the way you trade? We break down "
                           "the real numbers — targets, loss limits, fees and the dashboard.",
         font("inter-400", 33), fill=MUTED, max_w=1180)
    x = MARGIN; y = 800
    for big, small in [("Up to $200,000", "simulated funded capital"),
                       ("Payouts in 24h", "bank transfer or crypto"),
                       ("Profit split up to 100%", "you keep the upside")]:
        card(d, [x, y, x + 520, y + 150])
        d.text((x + 30, y + 26), big, font=font("space-grotesk-700", 38), fill=TEXT)
        d.text((x + 30, y + 88), small, font=font("inter-400", 24), fill=MUTED)
        x += 560
    return img


def s_agenda():
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    top = header(d, "Today's breakdown", "What we're covering, in order")
    items = [("01", "The three accounts side by side", "structure at a glance"),
             ("02", "2-Step deep dive", "our main example, with a $100K walkthrough"),
             ("03", "The trade-off, then 1-Step and Instant", "wider room vs. one shot vs. no evaluation"),
             ("04", "Sizes, fees, platforms", "five thousand to two hundred thousand"),
             ("05", "The dashboard, my pick, and the offer", "what you track, and how to claim 50% off")]
    y = top + 22
    for num, head, sub in items:
        card(d, [MARGIN, y, W - MARGIN, y + 116])
        d.ellipse([MARGIN + 28, y + 28, MARGIN + 92, y + 88], fill=PANEL_HI, outline=STROKE, width=2)
        d.text((MARGIN + 60, y + 58), num, font=font("oswald-600", 34), fill=GREEN_HI, anchor="mm")
        d.text((MARGIN + 122, y + 22), head, font=font("space-grotesk-700", 37), fill=TEXT)
        d.text((MARGIN + 122, y + 74), sub, font=font("inter-400", 25), fill=MUTED)
        y += 138
    return img


def s_overview():
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "The three routes", "The real comparison, straight from everfunded.com")
    box = [MARGIN, 256, W - MARGIN, 936]
    browser_frame(d, box, "everfunded.com — choose your challenge")
    cap = Image.open(os.path.join(CAP_DIR, "comparison_table.png")).convert("RGB")
    ix0, iy0, ix1, iy1 = box[0] + 14, box[1] + 60, box[2] - 14, box[3] - 14
    iw, ih = ix1 - ix0, iy1 - iy0
    scale = min(iw / cap.width, ih / cap.height)
    nw, nh = int(cap.width * scale), int(cap.height * scale)
    cap = cap.resize((nw, nh), Image.LANCZOS)
    img.paste(cap, (ix0 + (iw - nw) // 2, iy0 + (ih - nh) // 2))
    d.text((MARGIN, 952), "Real capture of EverFunded's published comparison table — 2-Step phases shown.",
           font=font("inter-400", 22), fill=FAINT)
    lower_third(d)
    return img


def spec_slide(fname, name, color, tag, rows, note_title, note_body, extra=None):
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "Deep dive", f"The {name}", accent=color)
    lw = 620
    card(d, [MARGIN, 296, MARGIN + lw, 856], outline=color, width=3)
    d.text((MARGIN + 40, 332), name, font=font("space-grotesk-700", 60), fill=color)
    d.text((MARGIN + 40, 414), tag, font=font("inter-500", 28), fill=TEXT)
    hline(d, MARGIN + 40, MARGIN + lw - 40, 478)
    yy = 506
    for k, v in rows:
        d.text((MARGIN + 40, yy), k, font=font("inter-400", 25), fill=MUTED)
        vw, _ = measure(d, v, font("jetbrains-mono-700", 29))
        d.text((MARGIN + lw - 40 - vw, yy - 4), v, font=font("jetbrains-mono-700", 29), fill=TEXT)
        yy += 60
    rx = MARGIN + lw + 60; rw = W - MARGIN - rx
    d.text((rx, 322), note_title, font=font("space-grotesk-700", 40), fill=TEXT)
    para(d, (rx, 392), note_body, font("inter-400", 29), fill=MUTED, max_w=rw, leading=12)
    if extra:
        extra(d, rx, 636, rw)
    lower_third(d)
    return img


def two_step_extra(d, x, y, w):
    card(d, [x, y, x + w, y + 176], fill=PANEL_HI, outline=GREEN, width=2)
    d.text((x + 28, y + 22), "ON A $100,000 ACCOUNT", font=font("oswald-600", 27), fill=GREEN_HI)
    d.text((x + 28, y + 74), "Phase 1 target  $8,000      Phase 2 target  $5,000",
           font=font("jetbrains-mono-700", 29), fill=TEXT)
    d.text((x + 28, y + 122), "Overall loss floor  $90,000", font=font("jetbrains-mono-400", 25), fill=MUTED)


def s_twostep_math():
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "2-Step · concrete math", "$100,000 evaluation, step by step")
    cw = (CONTENT_W - 60) // 2; x = MARGIN
    for nm, pct, amt, col in [("PHASE 1", "8%", "$8,000", GREEN), ("PHASE 2", "5%", "$5,000", TEAL)]:
        card(d, [x, 316, x + cw, 612], outline=col, width=3)
        d.text((x + 36, 348), nm, font=font("oswald-600", 29), fill=col)
        d.text((x + 36, 398), pct, font=font("oswald-700", 106), fill=TEXT)
        d.text((x + 36, 530), amt, font=font("jetbrains-mono-700", 43), fill=col)
        d.text((x + 252, 546), "profit target", font=font("inter-400", 25), fill=MUTED)
        x += cw + 60
    d.line([(MARGIN + cw + 8, 466), (MARGIN + cw + 52, 466)], fill=GREEN, width=6)
    d.polygon([(MARGIN + cw + 52, 454), (MARGIN + cw + 52, 478), (MARGIN + cw + 72, 466)], fill=GREEN)
    card(d, [MARGIN, 656, W - MARGIN, 792], fill=PANEL_HI, outline=STROKE, width=2)
    d.text((MARGIN + 32, 680), "Overall loss floor during each phase", font=font("inter-500", 26), fill=MUTED)
    d.text((MARGIN + 32, 718), "$90,000", font=font("jetbrains-mono-700", 50), fill=GOLD)
    d.text((MARGIN + 320, 736), "10% below the starting balance", font=font("inter-400", 25), fill=MUTED)
    para(d, (MARGIN, 836), "Each phase starts again at $100,000 — evaluation profits don't carry over "
                           "into the next account.", font("inter-400", 29), fill=TEXT)
    lower_third(d)
    return img


def s_tradeoff():
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "The useful comparison", "It's a trade-off, not a 'best account'")
    cw = (CONTENT_W - 80) // 2; x = MARGIN
    for nm, col, rows in [("2-STEP", GREEN, ["Two evaluation phases", "5% max daily loss",
                                             "10% static overall loss", "More room, longer path"]),
                          ("1-STEP", TEAL, ["One evaluation phase", "3% max daily loss",
                                            "6% static overall loss", "Shorter path, tighter room"])]:
        card(d, [x, 296, x + cw, 756], outline=col, width=3)
        d.text((x + 34, 326), nm, font=font("space-grotesk-700", 52), fill=col)
        hline(d, x + 34, x + cw - 34, 402)
        yy = 440
        for r in rows:
            d.ellipse([x + 40, yy + 6, x + 52, yy + 18], fill=col)
            d.text((x + 74, yy - 4), r, font=font("inter-500", 30), fill=TEXT)
            yy += 64
        x += cw + 80
    para(d, (MARGIN, 796), "Neither is objectively better. The question is which constraint you'd rather live "
                           "with: more time and more room, or one shot with tighter discipline.",
         font("inter-400", 31), fill=MUTED)
    lower_third(d)
    return img


def s_trailing():
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "Instant · how trailing works", "The limit follows your closed-balance highs", accent=PURPLE)
    import math
    cx0, cy0, cx1, cy1 = MARGIN, 316, W - MARGIN, 796
    card(d, [cx0, cy0, cx1, cy1])
    d.line([(cx0 + 80, cy1 - 60), (cx0 + 80, cy0 + 40)], fill=STROKE, width=3)
    d.line([(cx0 + 80, cy1 - 60), (cx1 - 40, cy1 - 60)], fill=STROKE, width=3)
    eq, lim = [], []
    for i in range(121):
        t = i / 120
        x = cx0 + 80 + t * (cx1 - cx0 - 120)

        def y_of(tt):
            v = 560 - 90 * math.sin(tt * 5.2) * (0.35 + 0.65 * tt) - 40 * tt
            return cy0 + 40 + max(0, min(1, (v - 380) / 200)) * (cy1 - cy0 - 120)
        eq.append((x, y_of(t)))
        lim.append((x, min(y_of(max(0.0, t - 0.06)), cy0 + 40 + (560 - 380) / 200 * (cy1 - cy0 - 120))))
    lock_y = cy0 + 40 + (560 - 380) / 200 * (cy1 - cy0 - 120)
    d.line([(cx0 + 80, lock_y), (cx1 - 40, lock_y)], fill=GOLD, width=3)
    d.line(eq, fill=GREEN, width=6)
    d.line(lim, fill=RED, width=5)
    d.text((cx1 - 40, lock_y - 34), "locks at starting balance", font=font("inter-500", 23), fill=GOLD, anchor="ra")
    d.line([(cx0 + 100, cy1 - 26), (cx0 + 150, cy1 - 26)], fill=GREEN, width=6)
    d.text((cx0 + 162, cy1 - 40), "closed-balance high", font=font("inter-400", 23), fill=TEXT)
    d.line([(cx0 + 500, cy1 - 26), (cx0 + 550, cy1 - 26)], fill=RED, width=5)
    d.text((cx0 + 562, cy1 - 40), "6% trailing overall limit", font=font("inter-400", 23), fill=TEXT)
    para(d, (MARGIN, 836), "A funded payout resets the balance and re-arms the trailing limit for the next cycle.",
         font("inter-400", 29), fill=MUTED)
    lower_third(d)
    return img


def s_sizes():
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "Account sizes & fees", "Six sizes, from $5K to $200K")
    data = [("$5,000", "$43.75", "$21.88"), ("$10,000", "$87.50", "$43.75"), ("$25,000", "$200", "$100"),
            ("$50,000", "$312.50", "$156.25"), ("$100,000", "$562.50", "$281.25"), ("$200,000", "$1,250", "$625")]
    x0, y0, rh, tw = MARGIN, 296, 72, CONTENT_W
    d.rectangle([x0, y0, x0 + tw, y0 + rh], fill=PANEL_HI)
    for tx, htext in zip([x0 + 40, x0 + 420, x0 + 880, x0 + 1340],
                         ["ACCOUNT", "LIST FEE", "WITH CODE GEOID", ""]):
        d.text((tx, y0 + 22), htext, font=font("oswald-600", 27), fill=MUTED)
    y = y0 + rh
    for i, (sz, listf, disc) in enumerate(data):
        hi = sz == "$100,000"
        if hi:
            d.rectangle([x0, y, x0 + tw, y + rh], fill=(24, 52, 40), outline=GREEN, width=3)
        elif i % 2 == 0:
            d.rectangle([x0, y, x0 + tw, y + rh], fill=PANEL)
        d.text((x0 + 40, y + 19), sz, font=font("jetbrains-mono-700", 31), fill=TEXT)
        d.text((x0 + 420, y + 21), listf, font=font("jetbrains-mono-400", 29), fill=MUTED)
        d.text((x0 + 880, y + 19), disc, font=font("jetbrains-mono-700", 31), fill=GREEN_HI)
        if hi:
            chip(d, (x0 + 1300, y + 16), "BEST VALUE", font("oswald-600", 23), fg=GREEN_HI, bg=(20, 60, 40))
        y += rh
    card(d, [MARGIN, 760, W - MARGIN, 876], fill=PANEL_HI)
    d.text((MARGIN + 32, 782), "Leverage", font=font("oswald-600", 27), fill=GOLD)
    d.text((MARGIN + 32, 820), "1:100 in 2-Step evaluation · 1:50 once funded · 1:30 other products · "
                               "gold/indices/oil 1:10 · crypto 1:2", font=font("inter-400", 25), fill=TEXT)
    para(d, (MARGIN, 906), "Platforms: Match-Trader and MetaTrader 5 · first payout after 14 days · "
                           "minimum payout $100.", font("inter-400", 27), fill=MUTED)
    lower_third(d)
    return img


def browser_frame(d, box, url):
    card(d, box, 16, fill=(9, 13, 24))
    d.rectangle([box[0], box[1], box[2], box[1] + 46], fill=PANEL_HI)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([box[0] + 20 + i * 26, box[1] + 16, box[0] + 34 + i * 26, box[1] + 30], fill=c)
    rr(d, [box[0] + 120, box[1] + 10, box[2] - 30, box[1] + 36], 10, fill=(6, 9, 17))
    d.text((box[0] + 140, box[1] + 16), url, font=font("jetbrains-mono-400", 19), fill=MUTED)


def s_dashboard(home=True):
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "Inside the dashboard", "What you actually see when you start", accent=TEAL)
    box = [MARGIN, 276, W - MARGIN, 900]
    browser_frame(d, box, "app.everfunded.com/dashboard")
    ix0, iy0, ix1, iy1 = box[0] + 14, box[1] + 60, box[2] - 14, box[3] - 14
    sw = 300
    d.rectangle([ix0, iy0, ix0 + sw, iy1], fill=(10, 15, 27))
    # account card from the real dashboard
    card(d, [ix0 + 18, iy0 + 18, ix0 + sw - 18, iy0 + 190], r=16, fill=PANEL_HI)
    d.text((ix0 + 36, iy0 + 34), "EverFunded 2-Step", font=font("inter-600", 23), fill=TEXT)
    d.text((ix0 + 36, iy0 + 66), "#30005", font=font("jetbrains-mono-400", 21), fill=MUTED)
    chip(d, (ix0 + 36, iy0 + 100), "MAX LOSS", font("oswald-600", 17), fg=RED, bg=(60, 22, 22))
    chip(d, (ix0 + 160, iy0 + 100), "DAILY LOSS", font("oswald-600", 17), fg=GOLD, bg=(58, 42, 16))
    d.text((ix0 + 36, iy0 + 140), "2-STEP · PHASE 1 · $100K", font=font("jetbrains-mono-700", 18), fill=GREEN_HI)
    my = iy0 + 210
    for i, m in enumerate(["Dashboard", "Accounts", "Payouts", "Rewards",
                           "Certificates", "Contracts", "Billing", "Settings"]):
        act = (i == 0) if home else (i == 1)
        if act:
            d.rectangle([ix0 + 14, my - 6, ix0 + sw - 14, my + 38], fill=(24, 52, 40))
        d.text((ix0 + 34, my), m, font=font("inter-500", 22), fill=GREEN_HI if act else MUTED)
        my += 42
    cx = ix0 + sw + 30
    if home:
        cw = (ix1 - cx - 48) // 3
        for i, (lab, val, col) in enumerate([("Balance", "$100,000.00", GREEN),
                                             ("Equity", "$101,240.50", GREEN_HI),
                                             ("Open P&L", "+$1,240.50", TEAL)]):
            x = cx + i * (cw + 24)
            card(d, [x, iy0, x + cw, iy0 + 148])
            d.text((x + 26, iy0 + 20), lab.upper(), font=font("oswald-600", 23), fill=MUTED)
            d.text((x + 26, iy0 + 66), val, font=font("jetbrains-mono-700", 38), fill=col)
        py = iy0 + 186
        card(d, [cx, py, ix1, py + 116], fill=(40, 26, 26), outline=RED, width=2)
        d.text((cx + 26, py + 18), "PERMITTED LOSS", font=font("oswald-600", 23), fill=RED)
        d.text((cx + 26, py + 58), "Max  $90,000", font=font("jetbrains-mono-700", 33), fill=TEXT)
        d.text((cx + 330, py + 58), "Daily floor  $95,000", font=font("jetbrains-mono-700", 30), fill=GOLD)
        oy = py + 146
        ow = (ix1 - cx - 48) // 4
        for i, (lab, tgt, res) in enumerate([("Min trading days", "3", "0 / 3"),
                                             ("Profit target", "$8,000", "$1,240"),
                                             ("Daily drawdown", "$95,000 floor", "safe"),
                                             ("Max drawdown", "$90,000 floor", "safe")]):
            x = cx + i * (ow + 16)
            card(d, [x, oy, x + ow, oy + 168])
            d.text((x + 20, oy + 16), lab.upper(), font=font("oswald-600", 21), fill=MUTED)
            d.text((x + 20, oy + 52), tgt, font=font("jetbrains-mono-700", 30), fill=TEXT)
            d.text((x + 20, oy + 108), res, font=font("jetbrains-mono-400", 23), fill=GREEN_HI)
    else:
        # faithful reproduction of the labels and values on the real dashboard
        pw = (ix1 - cx - 24) // 2
        card(d, [cx, iy0, cx + pw, iy0 + 158], fill=(40, 26, 26), outline=RED, width=2)
        d.text((cx + 24, iy0 + 16), "RISK FLOORS", font=font("oswald-600", 22), fill=RED)
        d.text((cx + 24, iy0 + 56), "Static max loss", font=font("inter-400", 21), fill=MUTED)
        d.text((cx + 24, iy0 + 84), "$0 / $10,000", font=font("jetbrains-mono-700", 28), fill=TEXT)
        d.text((cx + 250, iy0 + 92), "($90,000 floor)", font=font("inter-400", 21), fill=GOLD)
        d.text((cx + 24, iy0 + 124), "Daily loss  $0 / $5,000", font=font("jetbrains-mono-400", 21), fill=MUTED)
        px2 = cx + pw + 24
        card(d, [px2, iy0, ix1, iy0 + 158])
        d.text((px2 + 24, iy0 + 16), "PROGRESS & TIMELIMITS", font=font("oswald-600", 22), fill=GREEN_HI)
        d.text((px2 + 24, iy0 + 56), "Profit target", font=font("inter-400", 21), fill=MUTED)
        d.text((px2 + 24, iy0 + 84), "$0 / $8,000", font=font("jetbrains-mono-700", 28), fill=TEXT)
        d.text((px2 + 250, iy0 + 92), "NOT REACHED", font=font("inter-500", 20), fill=RED)
        d.text((px2 + 24, iy0 + 124), "Min days  0 / 3   (≥ $500 / day)", font=font("jetbrains-mono-400", 21), fill=MUTED)
        sy = iy0 + 176
        card(d, [cx, sy, ix1, sy + 96])
        stats = [("INITIAL BALANCE", "$100,000", TEXT), ("PROFIT TARGET", "$8,000", GREEN_HI),
                 ("MIN TRADING DAYS", "3", TEXT), ("PEAK EQUITY", "$100,000", TEAL),
                 ("TROUGH", "$100,000", MUTED)]
        sw2 = (ix1 - cx - 4 * 18) // 5
        for i, (lab, val, col) in enumerate(stats):
            x = cx + i * (sw2 + 18)
            d.text((x, sy + 16), lab, font=font("oswald-600", 17), fill=MUTED)
            d.text((x, sy + 46), val, font=font("jetbrains-mono-700", 24), fill=col)
        ty = sy + 114
        card(d, [cx, ty, ix1, ty + 96])
        tl = [("BALANCE", "$100,000"), ("EQUITY", "$100,000"), ("TODAY'S P&L", "$0"),
              ("DAILY LOSS RESET", "10h 48m 53s"), ("INACTIVITY", "0 / 30 days")]
        tw2 = (ix1 - cx - 4 * 18) // 5
        for i, (lab, val) in enumerate(tl):
            x = cx + i * (tw2 + 18)
            d.text((x, ty + 16), lab, font=font("oswald-600", 17), fill=MUTED)
            d.text((x, ty + 46), val, font=font("jetbrains-mono-700", 22), fill=TEXT)
        d.text((cx, 756), "Labels and values reproduced from EverFunded's published trader dashboard.",
               font=font("inter-400", 20), fill=FAINT)
    lower_third(d)
    return img


def s_pick():
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "My take", "Which one I'd pick, and why", accent=GOLD)
    rows = [("2-STEP", GREEN, "MY PICK", "Room to have a bad day without ending the account, and no "
                                        "deadline breathing down your neck."),
            ("1-STEP", TEAL, "IF YOU'RE CONFIDENT", "Cleanest route to funded — but 3% daily and 6% "
                                                       "overall are unforgiving."),
            ("INSTANT", PURPLE, "IF YOU HATE EVALUATIONS", "Trading immediately, as long as you respect "
                                                             "the 6% trailing limit.")]
    y = 296
    for nm, col, tag, txt in rows:
        hot = nm == "2-STEP"
        card(d, [MARGIN, y, W - MARGIN, y + 148], outline=col if hot else STROKE, width=3 if hot else 2)
        d.rectangle([MARGIN, y, MARGIN + 10, y + 148], fill=col)
        d.text((MARGIN + 40, y + 26), nm, font=font("space-grotesk-700", 42), fill=col)
        chip(d, (MARGIN + 40, y + 90), tag, font("oswald-600", 23), fg=col,
             bg=(col[0] // 8, col[1] // 8, col[2] // 8))
        para(d, (MARGIN + 540, y + 36), txt, font("inter-400", 29), fill=TEXT,
             max_w=CONTENT_W - 660, leading=8)
        y += 174
    para(d, (MARGIN, 838), "Honestly: the 2-Step on a size you can trade well. The wider loss limits are "
                           "worth more than the extra phase.", font("inter-500", 30), fill=GOLD)
    lower_third(d)
    return img


def s_cta():
    img = canvas(top=(14, 34, 26)); d = ImageDraw.Draw(img, "RGBA")
    blobs(d, [(1500, 200, 520, (34, 197, 94, 30)), (300, 900, 520, (34, 197, 94, 16))])
    chip(d, (MARGIN, 176), "LAUNCH OFFER", font("oswald-600", 29), fg=GREEN_HI, bg=(20, 60, 40))
    d.text((MARGIN, 232), "50% OFF your first eligible purchase", font=font("space-grotesk-700", 66), fill=TEXT)
    card(d, [MARGIN, 376, 900, 552], outline=GREEN, width=4, glow=(34, 197, 94, 70))
    d.text((MARGIN + 40, 404), "USE CODE AT CHECKOUT", font=font("oswald-600", 25), fill=MUTED)
    d.text((MARGIN + 40, 444), "GEOID", font=font("oswald-700", 92), fill=GREEN_HI)
    # real checkout capture (code already applied)
    cap = Image.open(os.path.join(CAP_DIR, "checkout_panel.png")).convert("RGB")
    cw_, ch_ = 850, int(850 * cap.height / cap.width)
    cap = cap.resize((cw_, ch_), Image.LANCZOS)
    cbox = [950, 252, 950 + cw_, 252 + ch_]
    card(d, cbox, r=14, fill=(9, 13, 24))
    img.paste(cap, (cbox[0] + 8, cbox[1] + 8))
    chip(d, (950, 214), "REAL CHECKOUT — CODE APPLIED", font("oswald-600", 21), fg=GREEN_HI,
         bg=(20, 60, 40))
    d.text((950, cbox[3] + 18), "List price $562.50  →  total to pay $281.25",
           font=font("jetbrains-mono-400", 25), fill=MUTED)
    d.text((950, cbox[3] + 54), "everfunded.com/checkout", font=font("jetbrains-mono-700", 30), fill=TEAL)
    x = MARGIN; y = 700; cw = (CONTENT_W - 80) // 3
    for n, t in [("1", "Open the link in the description"),
                 ("2", "Compare 2-Step, 1-Step and Instant"),
                 ("3", "Apply GEOID at checkout — 50% off")]:
        card(d, [x, y, x + cw, y + 158])
        d.ellipse([x + 26, y + 26, x + 86, y + 86], fill=PANEL_HI, outline=GREEN, width=3)
        d.text((x + 56, y + 56), n, font=font("oswald-700", 37), fill=GREEN_HI, anchor="mm")
        para(d, (x + 104, y + 32), t, font("inter-500", 26), fill=TEXT, max_w=cw - 132, leading=6)
        x += cw + 40
    lower_third(d)
    return img


def s_recap():
    img = canvas(); d = ImageDraw.Draw(img, "RGBA")
    header(d, "Recap", "Three routes, one decision")
    y = 296
    for nm, col, txt in [("2-STEP", GREEN, "2 phases · 8% + 5% targets · 5% daily · 10% static overall"),
                         ("1-STEP", TEAL, "1 phase · 10% target · 3% daily · 6% static overall"),
                         ("INSTANT", PURPLE, "no evaluation · 3% daily · 6% trailing overall")]:
        card(d, [MARGIN, y, W - MARGIN, y + 108])
        d.rectangle([MARGIN, y, MARGIN + 10, y + 108], fill=col)
        d.text((MARGIN + 40, y + 22), nm, font=font("space-grotesk-700", 39), fill=col)
        d.text((MARGIN + 330, y + 33), txt, font=font("jetbrains-mono-400", 29), fill=TEXT)
        y += 130
    card(d, [MARGIN, 700, W - MARGIN, 796], fill=PANEL_HI)
    d.text((MARGIN + 32, 722), "Six sizes up to $200,000  ·  payouts in 24h  ·  profit split up to 100%  ·  "
                               "code GEOID for 50% off", font=font("inter-500", 27), fill=TEXT)
    para(d, (MARGIN, 846), "If this was useful — like, subscribe with notifications on, and comment which "
                           "account you'd pick. Trade safe, I'll see you in the next one.",
         font("inter-500", 31), fill=GREEN_HI)
    lower_third(d)
    return img


SLIDES = {
    "01_hero.png": s_hero,
    "02_agenda.png": s_agenda,
    "03_overview.png": s_overview,
    "04_two_step.png": lambda: spec_slide("04", "2-Step", GREEN, "A structured evaluation with wider loss limits",
        [("Profit target", "8% then 5%"), ("Max daily loss", "5%"), ("Max overall loss", "10% static"),
         ("Qualifying days", "3 per phase"), ("Min qualifying day", "0.5% net"), ("Deadline", "None")],
        "Two evaluation phases, wider limits.",
        "Two phases with profit targets of eight and five percent, a five percent maximum daily loss and a "
        "ten percent static maximum overall loss. No deadline, subject to inactivity rules — and at least "
        "three qualifying days per phase.", two_step_extra),
    "05_two_step_math.png": s_twostep_math,
    "06_tradeoff.png": s_tradeoff,
    "07_one_step.png": lambda: spec_slide("07", "1-Step", TEAL, "One evaluation phase, tighter limits",
        [("Profit target", "10%"), ("Max daily loss", "3%"), ("Max overall loss", "6% static"),
         ("Qualifying days", "3 total"), ("Min qualifying day", "0.5% net"), ("Deadline", "None")],
        "One phase. Ten percent. Tighter limits.",
        "A single evaluation phase with a ten percent profit target, a three percent maximum daily loss and "
        "a six percent static maximum overall loss. No deadline, subject to inactivity rules, with the same "
        "three qualifying-day requirement."),
    "08_instant.png": lambda: spec_slide("08", "Instant", PURPLE, "No evaluation — funded from day one",
        [("Evaluation", "None"), ("Max daily loss", "3%"), ("Max overall loss", "6% trailing"),
         ("Drawdown type", "Trailing"), ("Payout eligibility", "Applies"), ("Deadline", "None")],
        "Start directly as a simulated funded account.",
        "There's no evaluation phase. You begin as a simulated funded account with a three percent maximum "
        "daily loss and a six percent trailing overall limit that follows closed-balance highs and "
        "eventually locks at the starting balance."),
    "09_trailing.png": s_trailing,
    "10_sizes.png": s_sizes,
    "11_dashboard_home.png": lambda: s_dashboard(True),
    "12_objectives.png": lambda: s_dashboard(False),
    "13_pick.png": s_pick,
    "14_cta.png": s_cta,
    "15_recap.png": s_recap,
}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/vid/slides"
    os.makedirs(out, exist_ok=True)
    for name, fn in SLIDES.items():
        img = fn()
        img.save(os.path.join(out, name))
        print("rendered", name)
    print("slides ->", out)


if __name__ == "__main__":
    main()
