#!/usr/bin/env python3
"""Turn a photo into a transparent halftone/dither PNG (the Laminar "pixel clouds" look).

Usage:
  python3 dither_image.py in.jpg out.png [width=1080] [cell=3] [floor=0.16]

- Ordered 4x4 Bayer dither on a grid of `cell`-px squares, kept crisp (nearest-neighbour upscale).
- Brightness becomes dot density AND opacity, so black areas turn fully transparent
  and the PNG sits on any dark background.
- `floor` clips dark tones first; raise it if the sky shows speckle.
Prompt idea for the source: "dramatic soft cumulus clouds in a pure black night sky,
high contrast black and white photo, separate cloud puffs with lots of black space, no text".
Use CSS `image-rendering: pixelated` when scaling it in the page.
"""
import sys

import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1080
cell = int(sys.argv[4]) if len(sys.argv) > 4 else 3
floor = float(sys.argv[5]) if len(sys.argv) > 5 else 0.16

im = Image.open(src).convert("L")
H = round(im.size[1] * W / im.size[0])
small = im.resize((W // cell, H // cell), Image.BOX)
s = np.asarray(small).astype(np.float32) / 255
s = np.clip((s - floor) / (1 - floor), 0, 1)
bayer = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16
th = np.tile(bayer, (s.shape[0] // 4 + 1, s.shape[1] // 4 + 1))[: s.shape[0], : s.shape[1]]
on = (s ** 1.2) > th
rgba = np.zeros((s.shape[0], s.shape[1], 4), np.uint8)
rgba[..., :3] = (150 + 70 * s[..., None]).astype(np.uint8)  # grey dots, brighter in highlights
rgba[..., 3] = np.where(on, (90 + 110 * s).astype(np.uint8), 0)
out = Image.fromarray(rgba).resize((s.shape[1] * cell, s.shape[0] * cell), Image.NEAREST)
out.save(dst)
print(dst, out.size)
