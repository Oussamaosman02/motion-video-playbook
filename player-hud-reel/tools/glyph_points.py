#!/usr/bin/env python3
"""Sample a word/number into particle target points (for the 'particle dust forms a number' beat).

Usage:
  python3 glyph_points.py OUT.json "5–8" [FONT.ttf] [SIZE=520] [STEP=17] [BOX_W=1000] [BOX_H=560] [X_OFF=40]
Writes [[x,y],...] in a BOX_W x BOX_H box (x shifted by X_OFF), jittered ±3 px, one point per STEP px of ink.
Paste the array as `const PTS = [...]` in index.html; each point becomes one .dot div tweened from a random cloud.
Done offline on purpose: sampling a canvas at runtime races the @font-face load and is not deterministic.
~600 points (STEP 17 for a 520 px glyph) render fine; 1000+ makes snapshots slow.
"""
import json, random, sys
from PIL import Image, ImageDraw, ImageFont

a = sys.argv[1:]
out, txt = a[0], a[1]
font = a[2] if len(a) > 2 else "assets/Archivo.ttf"
size, step, W, H, xo = [int(v) for v in (a[3:8] + ["520", "17", "1000", "560", "40"][len(a[3:8]):])]
im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
f = ImageFont.truetype(font, size)
try: f.set_variation_by_axes([900, 100])  # Archivo variable: weight 900, width 100
except Exception: pass
bb = d.textbbox((0, 0), txt, font=f)
d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], (H - (bb[3] - bb[1])) / 2 - bb[1]), txt, font=f, fill=255)
px = im.load(); random.seed(7); pts = []
for y in range(0, H, step):
    for x in range(0, W, step):
        jx = min(W - 1, max(0, x + random.randint(-3, 3))); jy = min(H - 1, max(0, y + random.randint(-3, 3)))
        if px[jx, jy] > 128: pts.append([jx + xo, jy])
json.dump(pts, open(out, "w"), separators=(",", ":"))
print(len(pts), "points →", out)
