#!/usr/bin/env python3
"""Key a magenta-background photo into a tight RGBA sprite; optionally find a green phone screen.

Usage: python3 key_sprite.py in.png out.png [--screen screen.json]

Magenta key with despill (soft edge from the magenta distance). With --screen, pure-green
pixels become a separate mask: the sprite gets them as transparent and screen.json stores the
screen box + a mask PNG (out_screen.png) in sprite px, so the renderer can draw live UI there.
"""
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

src, dst = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
# magenta-ness: high R and B, low G
mag = np.clip(((r + b) / 2 - g - 60) / 60, 0, 1)
alpha = 1 - mag
alpha = ndimage.binary_opening(alpha > 0.5, iterations=2) * alpha
lab, n = ndimage.label(alpha > 0.5)
if n > 1:  # keep the biggest blob only (drop specks)
    big = np.argmax(ndimage.sum(np.ones_like(alpha), lab, range(1, n + 1))) + 1
    alpha *= ndimage.binary_dilation(lab == big, iterations=3)
# despill: pull magenta fringe toward neutral
rgb = a.copy()
m = np.minimum(r, b)
spill = np.clip(m - g, 0, None)  # only magenta-tinted pixels have both R and B above G
rgb[..., 0] -= spill
rgb[..., 2] -= spill
alpha = ndimage.minimum_filter(alpha, 3)  # eat the 1px fringe
alpha = ndimage.gaussian_filter(alpha, 0.7)
screen = None
if "--screen" in sys.argv:
    gm = (g > 180) & (r < 120) & (b < 120)
    lab, n = ndimage.label(gm)
    big = np.argmax(ndimage.sum(gm, lab, range(1, n + 1))) + 1
    gm = ndimage.binary_fill_holes(lab == big)
    screen = ndimage.binary_dilation(gm, iterations=2)
    alpha = np.where(screen, 0, alpha)
ys, xs = np.where(alpha > 0.02)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
if screen is not None:
    sy, sx = np.where(screen)
    y0, y1, x0, x1 = min(y0, sy.min()), max(y1, sy.max() + 1), min(x0, sx.min()), max(x1, sx.max() + 1)
out = np.dstack([np.clip(rgb, 0, 255), alpha * 255])[y0:y1, x0:x1].astype(np.uint8)
Image.fromarray(out).save(dst)
print(f"sprite {out.shape[1]}x{out.shape[0]} -> {dst}")
if screen is not None:
    sm = screen[y0:y1, x0:x1]
    Image.fromarray((sm * 255).astype(np.uint8)).save(dst.replace(".png", "_screen.png"))
    sy, sx = np.where(sm)
    box = [int(sx.min()), int(sy.min()), int(sx.max() + 1), int(sy.max() + 1)]
    json.dump({"box": box, "mask": dst.replace(".png", "_screen.png")}, open(sys.argv[sys.argv.index("--screen") + 1], "w"))
    print("screen box", box)
