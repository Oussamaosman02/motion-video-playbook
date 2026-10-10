#!/usr/bin/env python3
"""Advance width (in em) of strings in a font, for the cursive() helper's EM table.
The pen dot and the clip reveal end exactly where the ink ends: width_px = em * font_size.
Usage: python3 text_em.py assets/PinyonScript.ttf "quiz funnel" "tu resultado" ...
Needs fontTools (pip install fonttools). Ignores kerning (good to ~2%)."""
import sys
from fontTools.ttLib import TTFont

font = TTFont(sys.argv[1])
cmap, hmtx, upm = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
for s in sys.argv[2:]:
    em = sum(hmtx[cmap[ord(c)]][0] for c in s if ord(c) in cmap) / upm
    print(f'"{s}": {em:.3f},')
