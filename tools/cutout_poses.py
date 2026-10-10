#!/usr/bin/env python3
"""Turn magenta-background character images into aligned transparent PNG poses.

Usage:
  python3 cutout_poses.py OUT_DIR HEIGHT name1=img1.png name2=img2.png ...
  e.g. python3 cutout_poses.py assets 720 jake_idle=jake_base.png jake_talk=jake_talk.png jake_point=jake_point.png

All poses of ONE character must be passed together: they are cropped with the same box,
so swapping poses in the video never makes the character jump. Generate them as edits of
the same base image ("keep everything else identical") so the body stays put.
Needs: numpy, pillow, scipy.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

out_dir, H = sys.argv[1], int(sys.argv[2])
items = [a.split("=", 1) for a in sys.argv[3:]]


def key(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bg = np.clip(((np.minimum(r, b) - g) - 60) / 80, 0, 1)  # 1 = pure magenta
    alpha = 1 - bg
    lim = np.minimum(np.minimum(r, b), g + 20)  # despill pink fringe on soft edges
    out = a.copy()
    out[..., 0] = np.where(alpha < 1, np.minimum(r, np.maximum(g, lim)), r)
    out[..., 2] = np.where(alpha < 1, np.minimum(b, np.maximum(g, lim)), b)
    rgba = np.dstack([out, alpha * 255]).astype(np.uint8)
    # drop stray specks: keep blobs >= 2% of the largest
    solid = rgba[..., 3] > 40
    lab, n = ndimage.label(solid)
    sizes = ndimage.sum(solid, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= sizes.max() * 0.02])
    keep = keep | (ndimage.binary_dilation(keep, iterations=3) & (rgba[..., 3] > 0))
    rgba[..., 3] = np.where(keep, rgba[..., 3], 0)
    return rgba


keyed = {name: key(p) for name, p in items}
boxes = []
for k in keyed.values():
    ys, xs = np.where(k[..., 3] > 40)
    boxes.append((xs.min(), ys.min(), xs.max(), ys.max()))
box = (min(b[0] for b in boxes) - 6, min(b[1] for b in boxes) - 6,
       max(b[2] for b in boxes) + 6, max(b[3] for b in boxes) + 4)
for name, k in keyed.items():
    im = Image.fromarray(k).crop(box)
    W = round(im.size[0] * H / im.size[1])
    im.resize((W, H), Image.LANCZOS).save(f"{out_dir}/{name}.png")
    print(name, (W, H))
