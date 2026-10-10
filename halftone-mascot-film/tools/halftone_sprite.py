#!/usr/bin/env python3
"""Key flat-background 3D renders (mascot poses, objects) and turn them into crisp
1-bit "halftone print" sprites: paper-white inside the silhouette, ink dots for the shading.

Usage:
  python3 halftone_sprite.py OUT_DIR WIDTH CELL name1=img1.png name2=img2.png ...
    WIDTH  output width in px (all poses share ONE crop box, so swapping them never jitters)
    CELL   dot cell in px (5-7 reads like the Pocketsflow mascot at 1080 wide)
  env: INK=#0b0b10 PAPER=#ffffff GAMMA=0.85 SPLIT=1 (SPLIT=1: 2x2 object sheet -> 4 sprites; HUEKEY=1 keys on magenta hue so cast shadows drop out)

The background colour is sampled from the image corners (Gemini's "magenta" comes back as
a muted pink, so a fixed key colour would fail). Tones are stretched inside the silhouette
(2nd..98th percentile) before an 8x8 Bayer ordered dither, so skin/beige reads as light
dots and eyes/hair shadows go solid ink.
Needs numpy, pillow, scipy.
"""
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

out_dir, W, CELL = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
items = [a.split("=", 1) for a in sys.argv[4:]]
hexrgb = lambda h: tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
INK, PAPER = hexrgb(os.environ.get("INK", "#0b0b10")), hexrgb(os.environ.get("PAPER", "#ffffff"))
GAMMA = float(os.environ.get("GAMMA", "0.85"))
SPLIT = os.environ.get("SPLIT") == "1"
os.makedirs(out_dir, exist_ok=True)


def key(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    h, w = a.shape[:2]
    k = 24
    corners = np.concatenate([a[:k, :k], a[:k, -k:], a[-k:, :k], a[-k:, -k:]]).reshape(-1, 3)
    bg = np.median(corners, axis=0)
    d = np.sqrt(((a - bg) ** 2).sum(-1))
    solid = d > 57
    if os.environ.get("HUEKEY") == "1":  # cast shadows on magenta stay magenta-hued: key on b/g ratio
        solid = a[..., 2] < 1.3 * a[..., 1] + 4
    solid = ndimage.binary_fill_holes(ndimage.binary_opening(solid, iterations=2))
    lab, n = ndimage.label(solid)
    if n:
        sizes = ndimage.sum(solid, lab, range(1, n + 1))
        solid = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s >= sizes.max() * 0.02])
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]) / 255
    return lum, solid


B8 = np.array([[0, 32, 8, 40, 2, 34, 10, 42], [48, 16, 56, 24, 50, 18, 58, 26],
               [12, 44, 4, 36, 14, 46, 6, 38], [60, 28, 52, 20, 62, 30, 54, 22],
               [3, 35, 11, 43, 1, 33, 9, 41], [51, 19, 59, 27, 49, 17, 57, 25],
               [15, 47, 7, 39, 13, 45, 5, 37], [63, 31, 55, 23, 61, 29, 53, 21]])
B8 = (B8 + 0.5) / 64


def halftone(lum, solid, box, name):
    y0, y1, x0, x1 = box
    lum, solid = lum[y0:y1, x0:x1], solid[y0:y1, x0:x1]
    H = round(lum.shape[0] * W / lum.shape[1])
    gw, gh = W // CELL, H // CELL
    L = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).resize((gw, gh), Image.BOX)) / 255
    M = np.asarray(Image.fromarray(solid.astype(np.uint8) * 255).resize((gw, gh), Image.BOX)) > 127
    lo, hi = np.percentile(L[M], float(os.environ.get("LO", "2"))), np.percentile(L[M], float(os.environ.get("HI", "98")))
    L = np.clip((L - lo) / (hi - lo + 1e-6), 0, 1) ** GAMMA
    th = np.tile(B8, (gh // 8 + 1, gw // 8 + 1))[:gh, :gw]
    ink = (L < th) & M
    rgba = np.zeros((gh, gw, 4), np.uint8)
    rgba[M] = (*PAPER, 255)
    rgba[ink] = (*INK, 255)
    out = Image.fromarray(rgba).resize((gw * CELL, gh * CELL), Image.NEAREST)
    out.save(f"{out_dir}/{name}.png")
    print(f"{out_dir}/{name}.png", out.size)


keyed = [(name, *key(p)) for name, p in items]
if SPLIT:  # 2x2 object sheet: one sprite per quadrant (name1..name4, row by row)
    for name, lum, solid in keyed:
        h, w = solid.shape
        for i, (qy, qx) in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
            q = np.zeros_like(solid)
            q[qy * h // 2:(qy + 1) * h // 2, qx * w // 2:(qx + 1) * w // 2] = True
            ys, xs = np.where(solid & q)
            box = (ys.min(), ys.max() + 1, xs.min(), xs.max() + 1)
            halftone(lum, solid & q, box, f"{name}{i + 1}")
else:
    union = np.any([s for _, _, s in keyed], axis=0)
    ys, xs = np.where(union)
    m = 8
    box = (max(ys.min() - m, 0), ys.max() + m, max(xs.min() - m, 0), xs.max() + m)
    for name, lum, solid in keyed:
        halftone(lum, solid, box, name)
