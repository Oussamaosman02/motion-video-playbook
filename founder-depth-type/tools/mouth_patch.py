#!/usr/bin/env python3
"""Cheap lip-flap for a still talking-head: cut a feathered mouth patch from a
'mouth open' Gemini edit and align + colour-match it onto the closed base image.

Usage: python3 mouth_patch.py base.png open.png out_patch.png cx cy [rx ry]
cx,cy = mouth centre in base pixels. Output = RGBA same size as base, opaque only
around the mouth; overlay it on the base and toggle its opacity from the VO envelope.
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

base, opn, out = sys.argv[1:4]
cx, cy = int(sys.argv[4]), int(sys.argv[5])
rx = int(sys.argv[6]) if len(sys.argv) > 6 else 150
ry = int(sys.argv[7]) if len(sys.argv) > 7 else 95
A = Image.open(base).convert("RGB"); O = Image.open(opn).convert("RGB").resize(A.size)
a = np.asarray(A).astype(float)
best = None
for s in np.linspace(0.96, 1.04, 9):           # scale + shift search around the mouth
    W, H = A.size
    Os = O.resize((round(W * s), round(H * s)), Image.LANCZOS)
    o = np.asarray(Os).astype(float)
    ocx, ocy = cx * s, cy * s
    for dy in range(-24, 25, 3):
        for dx in range(-24, 25, 3):
            ys, xs = int(ocy + dy) - ry - 60, int(ocx + dx) - rx - 40
            ref = a[cy - ry - 60:cy - ry + 10, cx - rx - 40:cx + rx + 40]   # nose/moustache band
            cand = o[ys:ys + ref.shape[0], xs:xs + ref.shape[1]]
            if cand.shape != ref.shape:
                continue
            e = np.abs(ref - cand).mean()
            if best is None or e < best[0]:
                best = (e, s, dx, dy)
e, s, dx, dy = best
print(f"align err={e:.1f} scale={s:.3f} dx={dx} dy={dy}")
W, H = A.size
Os = np.asarray(O.resize((round(W * s), round(H * s)), Image.LANCZOS)).astype(float)
ox, oy = int(cx * s + dx) - cx, int(cy * s + dy) - cy
patch = np.zeros_like(a)
y0, y1, x0, x1 = cy - 2 * ry, cy + 2 * ry, cx - 2 * rx, cx + 2 * rx
patch[y0:y1, x0:x1] = Os[y0 + oy:y1 + oy, x0 + ox:x1 + ox]
yy, xx = np.mgrid[0:H, 0:W]
d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
ring = (d > 1.0) & (d < 1.8)
gain = a[ring].mean(0) / np.maximum(patch[ring].mean(0), 1)   # colour-match on a ring
patch = np.clip(patch * gain, 0, 255)
mask = Image.fromarray((np.clip(1.6 - d, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
rgba = np.dstack([patch, np.asarray(mask)]).astype(np.uint8)
Image.fromarray(rgba, "RGBA").save(out)
print("->", out)
