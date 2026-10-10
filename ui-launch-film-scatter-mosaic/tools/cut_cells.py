#!/usr/bin/env python3
"""Cut a COLS x ROWS magenta product sheet into transparent PNGs, cell by cell.

Gemini often draws white gutter lines between the cells of a "grid of objects" sheet; the shared
tools/cutout_grid.py then sees one giant blob. This splits by the grid first, insets each cell
past the gutter, keys the magenta (same despill as cutout_grid.py) and trims to the object.

Usage: python3 tools/cut_cells.py sheet.png OUT_DIR COLS ROWS MAX_SIDE name1 name2 ...   (reading order)
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sheet, out_dir, cols, rows, max_side, names = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6:]
im = Image.open(sheet).convert("RGB")
W, H = im.size
cw, ch = W / cols, H / rows
for k, name in enumerate(names):
    cx, cy = k % cols, k // cols
    ins = int(min(cw, ch) * 0.04)
    cell = im.crop((int(cx * cw) + ins, int(cy * ch) + ins, int((cx + 1) * cw) - ins, int((cy + 1) * ch) - ins))
    a = np.asarray(cell).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    alpha = 1 - np.clip(((np.minimum(r, b) - g) - 60) / 80, 0, 1)
    lim = np.minimum(np.minimum(r, b), g + 20)
    o = a.copy()
    o[..., 0] = np.where(alpha < 1, np.minimum(r, np.maximum(g, lim)), r)
    o[..., 2] = np.where(alpha < 1, np.minimum(b, np.maximum(g, lim)), b)
    # global despill: any pixel where both R and B sit above G is magenta light bouncing off a
    # reflective/white object (chrome, glass, white plastic); pull R and B down to G (+6)
    spill = np.clip(np.minimum(o[..., 0], o[..., 2]) - o[..., 1] - 6, 0, None)
    o[..., 0] -= spill
    o[..., 2] -= spill
    # keep only the largest blob (drops stray gutter slivers)
    lab, n = ndimage.label(alpha > 0.5)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(alpha), lab, range(1, n + 1))
        keep = ndimage.binary_dilation(lab == (1 + int(np.argmax(sizes))), iterations=4)
        alpha = alpha * keep
    rgba = np.dstack([o, alpha * 255]).clip(0, 255).astype(np.uint8)
    obj = Image.fromarray(rgba)
    obj = obj.crop(obj.getbbox())
    obj.thumbnail((max_side, max_side), Image.LANCZOS)
    obj.save(f"{out_dir}/{name}.png")
    print(name, obj.size)
