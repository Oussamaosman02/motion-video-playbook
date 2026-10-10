#!/usr/bin/env python3
"""Rewrite the <!--AUDIO--> ... <!--/AUDIO--> block of index.html from word-indexed SFX cues.

Usage (from the project folder):  python3 tools/build_audio.py [index.html]
Reads the word array `const W = [...]` and `const VO = ...` from index.html, so swapping the voice
(new W + VO) and re-running this script re-times every SFX. Local only, no API.
Cue = (file, word index or None, offset s, volume, duration s). With word index None, offset is absolute.
"""
import json, re, sys
path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
src = open(path, encoding="utf-8").read()
W = json.loads(re.search(r"const W = (\[\[.*?\]\]);", src, re.S).group(1))
VO = float(re.search(r"const VO = ([0-9.]+)", src).group(1))
END = 28
t = lambda i: W[i][1] + VO

CUES = [
    ("whoosh", None, 0.0, 0.35, 0.8), ("click", None, 0.45, 0.18, 0.5), ("click", None, 0.95, 0.15, 0.5),
    ("pop", 3, 0.0, 0.9, 0.5), ("tick", 7, 0.35, 0.35, 0.5),
    ("whoosh", 8, -0.1, 0.35, 0.8), ("pop", 10, -0.05, 0.8, 0.5), ("click", 11, 0.0, 0.5, 0.5), ("sparks", 11, 0.03, 0.4, 1.2),
    ("whoosh", 12, -0.08, 0.4, 0.8), ("tick", 18, 0.0, 0.3, 0.5), ("tick", 20, 0.0, 0.3, 0.5), ("tick", 23, 0.0, 0.3, 0.5),
    ("whoosh", 25, -0.1, 0.3, 0.8), ("click", 25, 0.55, 0.45, 0.5),
    ("whoosh", 26, -0.08, 0.35, 0.8), ("pop", 26, 0.15, 0.7, 0.5), ("pop", 26, 0.45, 0.6, 0.5), ("pop", 26, 0.75, 0.6, 0.5),
    ("tick", 30, 0.2, 0.2, 0.5), ("tick", 30, 0.45, 0.2, 0.5), ("tick", 30, 0.75, 0.2, 0.5), ("pop", 33, 0.0, 0.8, 0.5),
    ("pop", 37, 0.0, 0.8, 0.5), ("riser", 38, -0.6, 0.25, 1.5), ("pop", 38, 0.05, 0.9, 0.5), ("chime", 40, 0.0, 0.25, 1.5),
    ("impact", 41, 0.0, 0.35, 2.0), ("tick", 42, 0.65, 0.3, 0.5), ("tick", 42, 1.1, 0.3, 0.5), ("chime", 45, 0.0, 0.3, 1.5),
    ("whoosh", 48, -0.08, 0.35, 0.8), ("pop", 48, 0.15, 0.7, 0.5), ("whoosh", 54, -0.05, 0.4, 0.8), ("pop", 54, 0.25, 0.8, 0.5),
    ("tick", 56, 0.6, 0.35, 0.5), ("tick", 56, 1.6, 0.35, 0.5),
    ("impact", 59, -0.05, 0.4, 2.0), ("whoosh", 59, 0.0, 0.3, 0.8), ("pop", 62, 0.0, 0.7, 0.5), ("pop", 65, 0.0, 0.8, 0.5),
    ("pop", 67, 0.0, 0.8, 0.5), ("pop", 73, 0.0, 0.8, 0.5), ("chime", 73, 0.05, 0.3, 1.5),
    ("whoosh", 74, -0.1, 0.35, 0.8), ("sparks", 75, 0.1, 0.4, 1.2), ("whoosh", 76, 0.0, 0.25, 0.8), ("chime", 80, 0.45, 0.35, 1.5),
]
lines = ['<audio id="vo" src="assets/vo.mp3" data-start="%.2f" data-duration="26.1" data-track-index="10" data-volume="1"></audio>' % VO,
         '<audio id="mus" src="assets/music.mp3" data-start="0" data-duration="%d" data-track-index="11" data-volume="0.2"></audio>' % END]
for n, (f, wi, off, vol, dur) in enumerate(CUES):
    at = max(0.0, (t(wi) if wi is not None else 0.0) + off)
    dur = min(dur, END - at)
    lines.append('<audio id="a%02d" src="assets/%s.mp3" data-start="%.2f" data-duration="%.2f" data-track-index="%d" data-volume="%.2f"></audio>' % (n, f, at, dur, 12 + n, vol))
block = "<!--AUDIO-->\n      " + "\n      ".join(lines) + "\n      <!--/AUDIO-->"
src = re.sub(r"<!--AUDIO-->.*?<!--/AUDIO-->", lambda m: block, src, flags=re.S)
open(path, "w", encoding="utf-8").write(src)
print(f"{len(CUES)} sfx cues written")
