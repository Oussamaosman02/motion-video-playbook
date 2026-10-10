#!/usr/bin/env python3
"""Cut N separate objects out of one sheet whose background is ANY flat colour
(Gemini often returns a dull magenta like #c84f9f instead of #FF00FF, which cutout_grid.py misses).
The key colour is sampled from the image corners; alpha = distance from it.

Usage: python3 cutout_keyed.py sheet.png OUT_DIR MAX_SIDE name1 name2 ...
Names follow reading order (rows top->bottom, then left->right).
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

sheet, out_dir, max_side, names = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4:]
a = np.asarray(Image.open(sheet).convert("RGB")).astype(np.float32)
h, w, _ = a.shape
corners = np.concatenate([a[:20, :20].reshape(-1, 3), a[:20, -20:].reshape(-1, 3), a[-20:, :20].reshape(-1, 3), a[-20:, -20:].reshape(-1, 3)])
key = np.median(corners, axis=0)
d = np.sqrt(((a - key) ** 2).sum(-1))
alpha = np.clip((d - 40) / 50, 0, 1)
# fill holes inside objects (eyes etc. are never key-coloured, but be safe) and smooth edges
solid = ndimage.binary_fill_holes(alpha > 0.5)
alpha = np.where(solid, np.maximum(alpha, ndimage.binary_erosion(solid, iterations=3).astype(np.float32)), alpha)
# despill: pull key tint out of semi-transparent edge pixels
o = a.copy()
edge = (alpha > 0) & (alpha < 1)
o[edge] = np.clip((a[edge] - (1 - alpha[edge, None]) * key) / np.maximum(alpha[edge, None], 0.25), 0, 255)
rgba = np.dstack([o, alpha * 255]).astype(np.uint8)
lab, n = ndimage.label(alpha > 0.5)
objs = ndimage.find_objects(lab)
sizes = ndimage.sum(alpha > 0.5, lab, range(1, n + 1))
big = [(i, s) for i, (s, z) in enumerate(zip(objs, sizes)) if z > sizes.max() * 0.04]
row_h = np.median([s[0].stop - s[0].start for _, s in big])
big.sort(key=lambda t: (round(t[1][0].start / row_h), t[1][1].start))
print(f"key={key.astype(int)} objects={len(big)}")
for (i, s), name in zip(big, names):
    y0, y1 = max(0, s[0].start - 6), min(h, s[0].stop + 6)
    x0, x1 = max(0, s[1].start - 6), min(w, s[1].stop + 6)
    crop = rgba[y0:y1, x0:x1].copy()
    crop[..., 3] = np.where(lab[y0:y1, x0:x1] == i + 1, crop[..., 3], 0)
    im = Image.fromarray(crop)
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(f"{out_dir}/{name}.png")
    print(name, im.size)
