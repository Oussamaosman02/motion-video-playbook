#!/usr/bin/env python3
"""Cut a NEUTRAL (white/grey) object off a magenta background and remove the pink spill.

Gemini's magenta bounces onto white plastic (the cube came back pink). For a neutral object the
green channel is spill-free, so the output colour is rebuilt from G (optionally lifted), and alpha
comes from how "magenta" a pixel is (R and B above G). Then the largest component is kept.

Usage: python3 key_neutral.py in.png out.png [size=900] [lift=1.06]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, dst = sys.argv[1], sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else 900
lift = float(sys.argv[4]) if len(sys.argv) > 4 else 1.06
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mag = np.minimum(r, b) - g                      # background ~ 165 (255,85,255); white ~ 0
bg_lvl = np.median(mag[:40, :40])
alpha = np.clip(1 - (mag - 18) / (bg_lvl * 0.75 - 18), 0, 1)
lab, n = ndimage.label(alpha > 0.5)
if n:
    big = 1 + np.argmax(ndimage.sum(np.ones_like(lab), lab, range(1, n + 1)))
    keep = ndimage.binary_dilation(lab == big, iterations=3)
    alpha *= keep
grey = np.clip(g * lift, 0, 255)
# a hint of cool tint in the shadows so it doesn't look flat grey
out = np.dstack([grey * 0.99, grey, np.clip(grey * 1.015, 0, 255), alpha * 255]).astype(np.uint8)
im = Image.fromarray(out, "RGBA")
im = im.crop(im.getbbox())
im.thumbnail((size, size), Image.LANCZOS)
im.save(dst)
print(dst, im.size)
