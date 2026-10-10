#!/usr/bin/env python3
"""Turn a Gemini 'window light on a grey wall' image into the neutral 1188x2112 background.

Usage: python3 wall_grade.py wall.png assets/wall.jpg
Crops to 9:16 by WIDTH (the 2:3 Gemini image is too wide, not too tall: cropping by height
pads black bands top and bottom, a bug we shipped once), strips the blue cast, stretches contrast
and maps shadows→176 grey, light→252 so the glass cards still read on it. The 10% oversize
leaves room for the slow drift/scale in the template.
"""
import sys
from PIL import Image, ImageOps

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("L")
w, h = im.size
nw = min(w, int(h * 9 / 16)); nh = int(nw * 16 / 9)
l, t = (w - nw) // 2, (h - nh) // 2
im = ImageOps.autocontrast(im.crop((l, t, l + nw, t + nh)), cutoff=0.5)
im = ImageOps.colorize(im, (176, 176, 180), (252, 252, 253), mid=(222, 222, 225)).resize((1188, 2112))
im.save(out, quality=90)
print(out, im.size, im.convert("L").getextrema())
