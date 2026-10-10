#!/usr/bin/env python3
"""Turn a glowing object rendered on pure black into an RGBA PNG (alpha = brightness), so it composites
anywhere without mix-blend-mode (screen blend breaks inside perspective/filter stacking contexts).
Usage: python3 glow_to_alpha.py in.png out.png [size] [black_floor=8]"""
import sys
import numpy as np
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else 0
floor = float(sys.argv[4]) if len(sys.argv) > 4 else 8
im = Image.open(src).convert("RGB")
if size: im = im.resize((size, size), Image.LANCZOS)
a = np.asarray(im).astype(np.float32)
m = a.max(axis=2)
alpha = np.clip((m - floor) / (255 - floor), 0, 1)
rgb = np.where(alpha[..., None] > 0.004, np.clip(a / np.maximum(m[..., None], 1) * 255, 0, 255), 0)
out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
Image.fromarray(out, "RGBA").save(dst, optimize=True)
