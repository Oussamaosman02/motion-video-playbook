#!/usr/bin/env python3
"""Make the EMPTY whiteboard from the finished one, in code (free, pixel-aligned).

Usage: python3 erase_board.py board_final.png board_empty.png [thresh=28]

Dark ink = pixels darker than the local background (a 61px median) by > thresh. The ink mask is
dilated and filled with a normalized-convolution blur of the surrounding clean board, so the
glare/vignette gradients survive. A little grain is added back so the fill isn't airbrushed.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

src, dst = sys.argv[1], sys.argv[2]
TH = float(sys.argv[3]) if len(sys.argv) > 3 else 28
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
L = im.mean(-1)
small = L[::4, ::4]
bg = ndimage.zoom(ndimage.median_filter(small, 31), 4, order=1)[: L.shape[0], : L.shape[1]]
ink = (bg - L) > TH
ink = ndimage.binary_dilation(ink, iterations=7)
keep = (~ink).astype(np.float32)
out = im.copy()
for s in (6, 18, 50):  # fill progressively from fine to coarse
    num = ndimage.gaussian_filter(im * keep[..., None], (s, s, 0))
    den = ndimage.gaussian_filter(keep, s)[..., None]
    fill = num / np.maximum(den, 1e-4)
    ok = (den[..., 0] > 0.05) & ink
    out[ok] = fill[ok]
    im = np.where(ink[..., None] & ok[..., None], fill, im)
    keep = np.maximum(keep, ok.astype(np.float32))
rng = np.random.default_rng(1)
grain = rng.normal(0, 1.6, L.shape)[..., None]
out[ink] += grain[ink]
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(dst)
print(f"ink px {ink.mean() * 100:.1f}% -> {dst}")
