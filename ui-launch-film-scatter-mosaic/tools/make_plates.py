#!/usr/bin/env python3
"""Render the code-made backgrounds of the mosaic variant (free, no Gemini).

Usage:  python3 tools/make_plates.py assets
Writes:
  halftone.png   1080x2200  wavy blue/teal/green gradient covered by a dot/dash halftone (the "incoming call" sky)
  paper.png      1080x1920  warm off-white paper with a faint square grid (the scatter scenes)
  blurA/B/C.png  1080x1920  soft blurred green/blue/yellow gradients (frosted chat + agent cards + warm circle)
Tweak PALETTE / seeds to restyle; everything is deterministic.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

out = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(out, exist_ok=True)


def ramp(t, stops):
    """t in [0,1] (HxW) -> RGB via colour stops [(pos, (r,g,b)), ...]"""
    t = np.clip(t, 0, 1)
    res = np.zeros(t.shape + (3,), np.float32)
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        m = (t >= p0) & (t <= p1)
        k = ((t - p0) / max(p1 - p0, 1e-6))[..., None]
        res[m] = (np.array(c0) * (1 - k) + np.array(c1) * k)[m]
    return res


# ---------- halftone sky ----------
W, H = 1080, 2200
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
f = (np.sin(y / 230 + np.sin(x / 310) * 1.6) * 0.5 + np.sin((x + y * 0.4) / 420) * 0.35 + np.sin(y / 97 + x / 520) * 0.15)
f = (f - f.min()) / (f.max() - f.min())
g = (np.sin(x / 260 - y / 700) + 1) / 2  # second field: hue drift blue -> green/olive
blue = ramp(f, [(0, (38, 92, 140)), (0.45, (78, 140, 186)), (0.75, (120, 172, 206)), (1, (150, 190, 214))])
green = ramp(f, [(0, (52, 98, 96)), (0.5, (96, 142, 120)), (1, (160, 176, 120))])
base = blue * (1 - g[..., None] * 0.55) + green * (g[..., None] * 0.55)
img = Image.fromarray(base.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
d = ImageDraw.Draw(img, "RGBA")
step = 9
for yy in range(0, H, step):
    for xx in range(0, W, step):
        v = f[yy, xx]
        h = (0.78 - v) * 13  # dashes only in the darker bands, longer where darker
        if h < 0.9:
            continue
        c = base[yy, xx] * 0.55
        d.rectangle([xx + 3, yy + 4 - h / 2, xx + 5, yy + 4 + h / 2], fill=(int(c[0]), int(c[1]), int(c[2]), 200))
img.save(os.path.join(out, "halftone.png"))

# ---------- paper with square grid ----------
W, H = 1080, 1920
p = Image.new("RGB", (W, H), (241, 240, 236))
d = ImageDraw.Draw(p)
for k in range(-1, W // 135 + 2):
    d.line([(k * 135 + 67, 0), (k * 135 + 67, H)], fill=(228, 227, 222), width=2)
for k in range(0, H // 135 + 2):
    d.line([(0, k * 135 + 25), (W, k * 135 + 25)], fill=(228, 227, 222), width=2)
p.save(os.path.join(out, "paper.png"))


# ---------- soft blurred gradients ----------
def blobs(spec, seed_bg, name):
    im = Image.new("RGB", (W // 4, H // 4), seed_bg)
    d = ImageDraw.Draw(im)
    for (cx, cy, r, col) in spec:
        d.ellipse([cx / 4 - r / 4, cy / 4 - r / 4, cx / 4 + r / 4, cy / 4 + r / 4], fill=col)
    im = im.filter(ImageFilter.GaussianBlur(55)).resize((W, H), Image.BICUBIC)
    a = np.asarray(im).astype(np.float32)
    a += np.random.default_rng(3).normal(0, 3.2, a.shape)  # film grain, kills banding
    Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(os.path.join(out, name))


# A: green forest with yellow + sky-blue corners (frosted chat, like the reference's call screen)
blobs([(150, 250, 700, (214, 176, 52)), (900, 300, 760, (150, 196, 222)), (540, 900, 900, (34, 74, 30)),
       (120, 1500, 800, (170, 206, 228)), (950, 1600, 760, (88, 150, 70)), (540, 1950, 700, (40, 90, 40))], (52, 100, 44), "blurA.png")
# B: teal / green (agent cards)
blobs([(200, 300, 800, (64, 128, 128)), (900, 900, 900, (98, 156, 84)), (300, 1500, 900, (150, 190, 120)), (900, 1800, 700, (40, 90, 70))], (60, 120, 90), "blurB.png")
# C: warm brand circle (red / orange / yellow) for the "Haz esto." beat
blobs([(300, 500, 900, (232, 56, 45)), (850, 900, 800, (246, 140, 50)), (400, 1400, 900, (250, 200, 90)), (900, 1700, 700, (200, 40, 40))], (230, 90, 50), "blurC.png")
print("plates ->", out)
