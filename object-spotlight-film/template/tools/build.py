#!/usr/bin/env python3
"""Build index.html from index.src.html: inject the word array (__W__) and the SFX <audio> tags (<!--SFX-->).

Usage: python3 tools/build.py            (run from the project folder)
- Words: assets/transcript.json (local `npx hyperframes transcribe assets/vo.mp3 -m small -l es`), FIX below
  corrects whisper spellings so captions match what is said.
- SFX cues: CUES below = (file stem, film time or "w<idx>" word cue [+offset], volume). Word cue time = word start + VO.
Every <audio> gets its own track index (HyperFrames needs one per overlapping clip). Local only, no API.
"""
import json, re, subprocess, pathlib
VO = 0.3
FIX = {13: "landing?", 25: "Quiz", 26: "Funnel.", 40: "qué", 83: "Y aquí", 30: "5", 32: "8"}
CUES = [
    ("whoosh", 0.02, 0.45), ("thump", "w7", 0.55), ("impact", "w12", 0.5), ("spot", "w14", 0.75),
    ("thump", "w21", 0.55), ("glitch", "w22", 0.4), ("whoosh", "w23-0.1", 0.4), ("impact", "w25", 0.55), ("tick", "w26", 0.4),
    ("whoosh", "w27", 0.35), ("tick", "w30", 0.45), ("tick", "w32", 0.45), ("tick", "w33", 0.4), ("tick", "w36", 0.4),
    ("thump", "w36", 0.45), ("thump", "w41", 0.45), ("tick", "w44", 0.4), ("thump", "w47", 0.5),
    ("boom", "w49", 0.45), ("thump", "w53", 0.5), ("whoosh", "w54", 0.3),
    ("click", "w60", 0.5), ("click", "w62", 0.5), ("click", "w63", 0.5), ("click", "w65", 0.5), ("sparks", "w70", 0.3),
    ("crtoff", "w74", 0.6), ("spot", "w75", 0.75), ("thump", "w79+0.3", 0.5), ("impact", "w82+0.15", 0.45),
    ("riser", "w83", 0.5), ("boom", "w87", 0.75), ("impact", "w87", 0.5),
    ("whoosh", "w88", 0.3), ("tick", "w90", 0.45), ("tick", "w94", 0.45), ("click", "w97", 0.5),
    ("odometer", "w102", 0.5), ("thump", "w109", 0.55), ("tick", "w114", 0.45), ("glitch", "w117", 0.35), ("whoosh", "w119+0.2", 0.4),
    ("impact", "w120", 0.4), ("click", "w127", 0.45), ("click", "w129", 0.45), ("thump", "w136", 0.5),
    ("sparks", 52.0, 0.3), ("click", 53.7, 0.7), ("chime", 53.78, 0.75),
]
root = pathlib.Path(__file__).resolve().parent.parent
words = json.load(open(root / "assets/transcript.json"))
W = [[FIX.get(i, w["text"]), round(w["start"], 2), round(w["end"], 2)] for i, w in enumerate(words)]
def at(c):
    if isinstance(c, (int, float)): return float(c)
    m = re.match(r"w(\d+)([+-][\d.]+)?$", c); return W[int(m.group(1))][1] + VO + float(m.group(2) or 0)
dur = {}
def d(stem):
    if stem not in dur:
        dur[stem] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(root / f"assets/{stem}.mp3")]))
    return dur[stem]
tags = []
for k, (stem, c, vol) in enumerate(CUES):
    tags.append(f'      <audio id="sx{k}" src="assets/{stem}.mp3" data-start="{at(c):.2f}" data-duration="{d(stem):.2f}" data-track-index="{20 + k}" data-volume="{vol}"></audio>')
src = (root / "tools/index.src.html").read_text()
out = src.replace("<!--SFX-->", "\n".join(tags)).replace("__W__", json.dumps(W, ensure_ascii=False))
(root / "index.html").write_text(out)
print(f"index.html: {len(W)} words, {len(tags)} sfx")
