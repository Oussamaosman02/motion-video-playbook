#!/usr/bin/env python3
"""Crop the 2:3 Gemini backdrops to 1080x1920 (by width) and split the 3x3 faces sheet.

Usage: python3 prep_images.py GEN_DIR ASSETS_DIR
Reads GEN_DIR/{flowers,desert,hill,peach,puffer}.png and faces.png;
writes ASSETS_DIR/<name>.jpg and face0..face8.jpg (360x360, cropped towards the top of each tile).
"""
import sys
import numpy as np
from PIL import Image

gen, out = sys.argv[1], sys.argv[2]
for n in ["flowers", "desert", "hill", "peach", "puffer"]:
    im = Image.open(f"{gen}/{n}.png").convert("RGB"); w, h = im.size; nw = int(h * 9 / 16); l = (w - nw) // 2
    im.crop((l, 0, l + nw, h)).resize((1080, 1920), Image.LANCZOS).save(f"{out}/{n}.jpg", quality=88)

im = Image.open(f"{gen}/faces.png").convert("RGB"); a = np.asarray(im).astype(int)
white = a.min(axis=2) > 235


def spans(m):
    res, s = [], None
    for i, v in enumerate(m):
        if not v and s is None: s = i
        if v and s is not None: res.append((s, i)); s = None
    if s is not None: res.append((s, len(m)))
    return [x for x in res if x[1] - x[0] > 100]


cs, rs = spans(white.mean(axis=0) > 0.9), spans(white.mean(axis=1) > 0.9)
k = 0
for y0, y1 in rs:
    for x0, x1 in cs:
        t = im.crop((x0 + 6, y0 + 6, x1 - 6, y1 - 6)); s = min(t.size)
        ox, oy = (t.size[0] - s) // 2, (t.size[1] - s) // 4
        t.crop((ox, oy, ox + s, oy + s)).resize((360, 360), Image.LANCZOS).save(f"{out}/face{k}.jpg", quality=88); k += 1
print(f"{k} faces (expect 9; if not, the sheet's white gaps were not clean: regenerate)")
