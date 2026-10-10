#!/usr/bin/env python3
"""Help define the element boxes for render_whiteboard.py (dark-ink fork of ../../tools/chalk_boxes.py).

Usage:
  python3 whiteboard_boxes.py board_final.png board_empty.png suggest out.jpg
      -> prints candidate boxes (source-image px) for each blob of chalk and saves an overlay
  python3 whiteboard_boxes.py board_final.png board_empty.png check config.json out.jpg
      -> draws the config's boxes + names + start times on the board so you can verify them

Suggested boxes group nearby chalk (a word line, an icon, a drawing). Merge or split them by
hand when writing config.json; boxes earlier in the list win overlapping pixels.
"""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

final_p, empty_p, mode = sys.argv[1:4]
fin = Image.open(final_p).convert("RGB")
Lf = np.asarray(fin.convert("L")).astype(np.float32)
Le = np.asarray(Image.open(empty_p).convert("L")).astype(np.float32)
chalk = (Le - Lf) > 30  # dark marker ink: finished board is DARKER than the empty one
img = fin.copy()
d = ImageDraw.Draw(img)

if mode == "suggest":
    out = sys.argv[4]
    blobs = ndimage.binary_dilation(chalk, iterations=14)  # join letters of a line
    lab, n = ndimage.label(blobs)
    boxes = []
    for sl in ndimage.find_objects(lab):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        if (x1 - x0) * (y1 - y0) < 2500:
            continue
        boxes.append([x0, y0, x1, y1])
    boxes.sort(key=lambda b: (round(b[1] / 60), b[0]))
    for i, b in enumerate(boxes):
        d.rectangle(b, outline=(255, 60, 60), width=5)
        d.text((b[0] + 6, b[1] + 4), str(i), fill=(255, 220, 0))
        print(i, b)
else:
    cfg, out = json.load(open(sys.argv[4])), sys.argv[5]
    for e in cfg["elements"]:
        b = e["box"]
        col = (255, 200, 0) if e.get("kind") == "text" else (80, 200, 255)
        d.rectangle(b, outline=col, width=5)
        d.text((b[0] + 6, b[1] + 4), f"{e['name']} @{e['start']}s", fill=col)
img.save(out, quality=85)
print("->", out)
