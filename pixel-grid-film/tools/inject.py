#!/usr/bin/env python3
"""Inject word times and the SFX cue list into index.html (re-runnable: rewrites between markers).

Usage: python3 work/inject.py            (run from the project folder)
- words: work/words.json  ([[text, start, end], ...] from `hyperframes transcribe -l es`, times relative to vo.mp3)
- SFX cues below: (file, at_seconds_on_film_clock_or_word_index, volume). An int `at` = word index -> W[i].start + VO.
"""
import json, re, pathlib

VO = 0.4
ROOT = pathlib.Path(__file__).resolve().parent.parent
W = json.loads((ROOT / "work/words.json").read_text())
DUR = {"tick": .52, "pop": .52, "whoosh": 1.23, "chime": 1.23, "blip": .52, "glitch": .63, "impact": 2.04,
       "type": 1.5, "ding": 1.04, "pixels": 1.2, "build": 1.0}

def T(i, d=0.0):
    return round(W[i][1] + VO + d, 3)

CUES = [
    ("build", 0.1, .35), ("blip", 1.0, .3), ("whoosh", T(7), .35), ("build", T(12), .45),
    ("pixels", T(14) - 0.36, .5), ("impact", T(14), .35), ("pixels", T(16) - 0.3, .4),
    ("pop", T(19), .35), ("tick", T(22, .1), .5), ("glitch", T(22, .5), .3), ("pixels", T(23), .55),
    ("build", T(25, -.3), .4), ("tick", T(25, -.18), .3), ("tick", T(25, -.06), .3), ("pop", T(25), .35), ("pop", T(26), .35),
    ("tick", T(27, .1), .35), ("blip", T(30), .35), ("blip", T(32), .35),
    ("whoosh", T(33, .05), .3), ("pop", T(39), .3), ("whoosh", T(40, -.25), .3), ("pop", T(43, -.1), .3), ("whoosh", T(44, -.25), .3), ("pop", T(48), .4),
    ("pixels", T(49), .4), ("glitch", T(52), .25), ("build", T(53), .45),
    ("whoosh", T(55, -.1), .3), ("tick", T(56, .1), .3), ("pop", T(60), .32), ("pop", T(62), .32), ("pop", T(63, .3), .32), ("pop", T(65), .32),
    ("whoosh", T(70, -.15), .3), ("chime", T(73, .1), .35),
    ("tick", T(75), .35), ("tick", T(76, .1), .35), ("tick", T(77), .35), ("blip", T(78, .2), .3), ("build", T(81), .45), ("impact", T(82), .3),
    ("pixels", T(83) - 0.3, .45), ("whoosh", T(83, .1), .3), ("impact", T(87), .4),
    ("whoosh", T(88), .3), ("tick", T(89), .3), ("tick", T(90), .3), ("whoosh", T(97, -.05), .4),
    ("pop", T(99, -.05), .3), ("pop", T(102, -.05), .3), ("pop", T(105, -.05), .3), ("whoosh", T(107, -.1), .3), ("ding", T(110, .1), .35),
    ("blip", T(114), .35), ("tick", T(114, .3), .45), ("tick", T(114, 1.3), .45), ("tick", T(114, 2.3), .45), ("glitch", T(116), .2),
    ("pop", T(119), .35), ("tick", T(119, .58), .5),
    ("pop", T(123, -.1), .35), ("blip", T(125), .3), ("pop", T(127, -.1), .35), ("pop", T(129, -.1), .35), ("pixels", T(132), .5), ("ding", T(136), .4),
    ("pixels", 54.0, .45), ("build", 54.75, .45), ("chime", 56.5, .35),
]

lines = []
for k, (name, at, vol) in enumerate(CUES):
    lines.append(f'      <audio id="sx{k}" src="assets/{name}.mp3" data-start="{at:.3f}" data-duration="{DUR[name]}" data-track-index="{20 + k}" data-volume="{vol}"></audio>')

p = ROOT / "index.html"
s = p.read_text()
s = re.sub(r"<!--SFX-->.*?<!--/SFX-->", "<!--SFX-->\n" + "\n".join(lines) + "\n      <!--/SFX-->", s, flags=re.S)
s = re.sub(r"/\*WORDS\*/.*?/\*/WORDS\*/", "/*WORDS*/" + json.dumps(W, ensure_ascii=False, separators=(",", ":")) + "/*/WORDS*/", s, flags=re.S)
p.write_text(s)
print(f"injected {len(W)} words, {len(CUES)} sfx cues")
