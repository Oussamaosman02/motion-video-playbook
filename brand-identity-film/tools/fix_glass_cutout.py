#!/usr/bin/env python3
"""Cut a TRANSLUCENT object (glass pod, bubble) out of a magenta background without grey holes.

cutout_grid.py keys every magenta-ish pixel; inside glass the background shows through, so it leaves
grey/see-through specks. Here: key only the outside (fill holes of the object mask), and inside the
object replace magenta-tinted pixels with a tint colour.
Usage: python3 fix_glass_cutout.py in_magenta.png out.png [max_side=600] [tint=238,172,192]
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

src, out = sys.argv[1], sys.argv[2]
max_side = int(sys.argv[3]) if len(sys.argv) > 3 else 600
tint = np.array([float(v) for v in (sys.argv[4] if len(sys.argv) > 4 else "238,172,192").split(",")])
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mag = np.clip(((np.minimum(r, b) - g) - 60) / 80, 0, 1)  # 1 = pure magenta
obj = ndimage.binary_fill_holes(ndimage.binary_opening(mag < 0.5, iterations=2))
lab, n = ndimage.label(obj)
sizes = ndimage.sum(obj, lab, range(1, n + 1))
obj = lab == (1 + int(np.argmax(sizes)))
inner = ndimage.binary_erosion(obj, iterations=3)
o = a.copy()
k = (mag * inner)[..., None]
o = o * (1 - k) + tint * k  # magenta seen through the glass -> tint
alpha = np.where(inner, 1.0, np.where(obj, 1 - mag, 0.0))
alpha = ndimage.gaussian_filter(alpha, 0.8)
rgba = np.dstack([np.clip(o, 0, 255), alpha * 255]).astype(np.uint8)
ys, xs = np.where(alpha > 0.05)
im = Image.fromarray(rgba).crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
im.thumbnail((max_side, max_side), Image.LANCZOS)
im.save(out)
print(out, im.size)
