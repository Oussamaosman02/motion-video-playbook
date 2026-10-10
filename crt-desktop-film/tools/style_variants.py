#!/usr/bin/env python3
"""One hero image on black -> N "render style" variants (transparent PNGs) + a 4x4 colour grid.

Usage: python3 style_variants.py hero.png out_dir [size]
Writes out_dir/{chrome,dither,ascii,halftone,contour,thermal,points,xray,red}.png and grid.png.
The hero must sit on a (near) black background; the mask is luminance-based.
"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

src, out = sys.argv[1], sys.argv[2]
S = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert("RGB").resize((S, S), Image.LANCZOS)
rgb = np.asarray(im).astype(np.float32) / 255
L = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
mask = np.clip((L - 0.04) / 0.08, 0, 1)
mask = np.asarray(Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1))) / 255.0
MINT = np.array([160, 236, 210], np.float32)
RED = np.array([232, 56, 45], np.float32)


def save(name, rgbf, alpha):
    a = np.dstack([np.clip(rgbf, 0, 255), np.clip(alpha, 0, 1) * 255]).astype(np.uint8)
    Image.fromarray(a).save(f"{out}/{name}.png")
    return a


def cells(px):
    """per-cell mean luminance and mask on a px grid"""
    n = S // px
    l = L[: n * px, : n * px].reshape(n, px, n, px).mean((1, 3))
    m = mask[: n * px, : n * px].reshape(n, px, n, px).mean((1, 3))
    return n, l, m


res = {}
# chrome: the original, black keyed out
res["chrome"] = save("chrome", rgb * 255, mask)

# dither: 1-bit ordered Bayer 8x8, chunky pixels
B = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26], [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
              [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25], [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]]) / 64
px = 6; n, l, m = cells(px)
th = np.tile(B, (n // 8 + 1, n // 8 + 1))[:n, :n]
on = ((np.clip(l * 1.6, 0, 1) > th) & (m > 0.5)).astype(np.float32)
on = np.kron(on, np.ones((px, px)))
full = np.zeros((S, S)); full[: on.shape[0], : on.shape[1]] = on
res["dither"] = save("dither", np.broadcast_to(MINT, (S, S, 3)), full)

# ascii
px = 14; n, l, m = cells(px)
ramp = " .:-=+*#%@"
font = ImageFont.load_default(size=px)
img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
for y in range(n):
    for x in range(n):
        if m[y, x] > 0.4:
            c = ramp[min(len(ramp) - 1, int(np.clip(l[y, x] * 1.5, 0, 0.999) * len(ramp)))]
            d.text((x * px + 2, y * px - 2), c, fill=(160, 236, 210, 255), font=font)
img.save(f"{out}/ascii.png"); res["ascii"] = np.asarray(img)

# halftone dots (white)
px = 16; n, l, m = cells(px)
img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
for y in range(n):
    for x in range(n):
        if m[y, x] > 0.4:
            r = px * 0.55 * np.sqrt(np.clip(l[y, x] * 1.4, 0.05, 1))
            cx, cy = x * px + px / 2, y * px + px / 2
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(235, 240, 238, 255))
img.save(f"{out}/halftone.png"); res["halftone"] = np.asarray(img)

# contour "wireframe": a few iso-luminance lines + a masked mesh + the outline
Lb = np.asarray(Image.fromarray((L * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))) / 255
q = np.floor(Lb * 6)
edge = (q != np.roll(q, 1, 0)) | (q != np.roll(q, 1, 1))
mm = mask > 0.5
yy, xx = np.mgrid[0:S, 0:S]
mesh = ((yy % 32) < 2) | ((xx % 32) < 2)
outline = mm ^ (np.asarray(Image.fromarray((mm * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))) > 0)
lines = ((edge | mesh) & mm) | outline
res["contour"] = save("contour", np.broadcast_to(MINT, (S, S, 3)), lines * 1.0)

# thermal colormap
def thermal(v):
    stops = np.array([[10, 10, 80], [40, 40, 220], [0, 200, 220], [60, 220, 60], [250, 230, 40], [250, 120, 20], [230, 30, 30], [255, 255, 255]], np.float32)
    v = np.clip(v, 0, 1) * (len(stops) - 1); i = np.floor(v).astype(int).clip(0, len(stops) - 2); f = (v - i)[..., None]
    return stops[i] * (1 - f) + stops[i + 1] * f
res["thermal"] = save("thermal", thermal(L * 1.3), mask)

# points (sparse cloud)
px = 10; n, l, m = cells(px)
img = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
for y in range(n):
    for x in range(n):
        if m[y, x] > 0.4 and ((x * 7 + y * 13) % 3 == 0 or l[y, x] > 0.55):
            cx, cy = x * px + (x * 37 % 5), y * px + (y * 53 % 5)
            r = 1.5 + 2.5 * l[y, x]
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 245, 230, 255))
img.save(f"{out}/points.png"); res["points"] = np.asarray(img)

# xray: inverted luminance in cold blue
inv = (1 - L) * mask
res["xray"] = save("xray", np.dstack([inv * 120 + 60, inv * 180 + 70, 255 * np.ones_like(inv)]), mask * (0.35 + inv))

# red brand duotone
res["red"] = save("red", RED[None, None] * (0.35 + 0.9 * L[..., None]) + 255 * np.clip(L - 0.75, 0, 1)[..., None] * 3, mask)

# 4x4 colour grid of variants on coloured tiles
T = S // 4
bgs = [(12, 22, 28), (150, 30, 25), (20, 20, 70), (40, 10, 50), (10, 10, 10), (10, 40, 35), (120, 20, 20), (30, 30, 30)]
order = ["chrome", "red", "thermal", "xray", "contour", "thermal", "dither", "red", "halftone", "ascii", "red", "points", "thermal", "chrome", "xray", "dither"]
grid = Image.new("RGB", (S, S))
for k, name in enumerate(order):
    tile = Image.new("RGB", (T, T), bgs[(k * 3) % len(bgs)])
    v = Image.fromarray(res[name]).resize((T, T), Image.LANCZOS)
    tile.paste(v, (0, 0), v)
    grid.paste(tile, ((k % 4) * T, (k // 4) * T))
grid.save(f"{out}/grid.png")
print("ok", sorted(res))
