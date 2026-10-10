#!/usr/bin/env python3
"""Cut several separate objects (e.g. 6 coins) out of ONE magenta-background image.

Usage:
  python3 cutout_grid.py sheet.png OUT_DIR MAX_SIDE name1 name2 ...
  e.g. python3 cutout_grid.py coins.png assets 360 coin_q coin_target coin_bolt coin_clock coin_euro coin_rocket

Objects are found as separate blobs and named in reading order (rows top→bottom, then left→right),
so prompt for "a grid of N objects with lots of space between them, not touching".
One image for many objects costs one generation (~$0.03 with Gemini via gen_image.py).
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sheet, out_dir, max_side, names = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:]
a = np.asarray(Image.open(sheet).convert("RGB")).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
alpha = 1 - np.clip(((np.minimum(r, b) - g) - 60) / 80, 0, 1)
lim = np.minimum(np.minimum(r, b), g + 20)  # despill the pink fringe
o = a.copy()
o[..., 0] = np.where(alpha < 1, np.minimum(r, np.maximum(g, lim)), r)
o[..., 2] = np.where(alpha < 1, np.minimum(b, np.maximum(g, lim)), b)
rgba = np.dstack([o, alpha * 255]).astype(np.uint8)

lab, n = ndimage.label(alpha > 0.2)
objs = ndimage.find_objects(lab)
sizes = ndimage.sum(alpha > 0.2, lab, range(1, n + 1))
big = [(i, s) for i, (s, z) in enumerate(zip(objs, sizes)) if z > sizes.max() * 0.04]
row_h = np.median([s[0].stop - s[0].start for _, s in big])
big.sort(key=lambda t: (round(t[1][0].start / row_h), t[1][1].start))
if len(big) != len(names):
    print(f"warning: found {len(big)} objects but got {len(names)} names")
for (i, s), name in zip(big, names):
    y0, y1 = max(0, s[0].start - 6), s[0].stop + 6
    x0, x1 = max(0, s[1].start - 6), s[1].stop + 6
    crop = rgba[y0:y1, x0:x1].copy()
    crop[..., 3] = np.where(lab[y0:y1, x0:x1] == i + 1, crop[..., 3], 0)
    im = Image.fromarray(crop)
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(f"{out_dir}/{name}.png")
    print(name, im.size)
