#!/usr/bin/env python3
"""Split an R x C photo grid with dark gutters (Gemini "2x2 grid of portraits") into separate square JPGs.
usage: split_grid.py sheet.png ROWS COLS out_prefix [size]
Finds the gutters as the darkest columns/rows near each expected split line."""
import sys
from PIL import Image
import numpy as np
src, R, C, pre = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
size = int(sys.argv[5]) if len(sys.argv) > 5 else 512
im = Image.open(src).convert("RGB"); a = np.asarray(im).astype(float).mean(axis=2)
H, W = a.shape
def edges(prof, n, L):
    cuts = [0]
    for k in range(1, n):
        c = int(L * k / n); w = int(L * 0.06)
        seg = prof[c - w:c + w]; dark = np.where(seg < seg.min() + 12)[0] + c - w
        cuts += [int(dark.min()), int(dark.max()) + 1]
    cuts.append(L)
    # trim the outer dark border too
    return [(cuts[2*i], cuts[2*i+1]) for i in range(n)]
cols = edges(a.mean(axis=0), C, W); rows = edges(a.mean(axis=1), R, H)
i = 0
for (y0, y1) in rows:
    for (x0, x1) in cols:
        tile = im.crop((x0, y0, x1, y1)); t = np.asarray(tile).astype(float).mean(axis=2)
        ys = np.where(t.mean(axis=1) > 25)[0]; xs = np.where(t.mean(axis=0) > 25)[0]
        tile = tile.crop((xs.min() + 4, ys.min() + 4, xs.max() - 4, ys.max() - 4))
        s = min(tile.size); tile = tile.crop(((tile.width - s)//2, 0, (tile.width - s)//2 + s, s)).resize((size, size), Image.LANCZOS)
        i += 1; tile.save(f"{pre}{i}.jpg", quality=92); print(f"{pre}{i}.jpg", (x0, y0, x1, y1))
