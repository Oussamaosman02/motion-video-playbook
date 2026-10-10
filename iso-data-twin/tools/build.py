#!/usr/bin/env python3
"""Build index.html from work/index.src.html: embeds the VO word times and writes the SFX <audio> cues.

Every cue is a word index (start of that word on the film clock) plus an offset, so a new VO only needs a new
work/words.json ([[word, start, end], ...]) and a re-run. Usage (from the project folder): python3 work/build.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
VO = 0.4      # VO offset on the film clock
END = 58.5    # film length (VO ends ~54.3 s, end card after)
W = json.loads((ROOT / "work/words.json").read_text())
t = lambda i: W[i][1] + VO

# (file, start, duration, volume)
CUES = [
    ("datarain", 0.15, 2.5, 0.55),
    ("whoosh", t(12), 1.2, 0.4),
    ("pop", t(12) + 0.55, 0.5, 0.35),
    ("type", t(14), 0.6, 0.4),
    ("iris", t(14) + 0.55, 1.2, 0.55),
    ("pop", t(19), 0.5, 0.3),
    ("click", t(22) + 0.2, 0.5, 0.55),
    ("pop", t(23), 0.5, 0.35),
    ("chime", t(25) + 0.1, 1.5, 0.35),
    ("tick", t(30), 0.5, 0.6),
    ("tick", t(32), 0.5, 0.6),
    ("blips", t(36), 0.8, 0.5),
    ("blips", t(40), 0.8, 0.5),
    ("blips", t(44), 0.8, 0.5),
    ("whoosh", t(51), 1.2, 0.35),
    ("iris", t(54) - 0.62, 1.2, 0.5),
    ("blips", t(60), 0.8, 0.45),
    ("blips", t(62), 0.8, 0.45),
    ("blips", t(63), 0.8, 0.45),
    ("blips", t(64), 0.8, 0.45),
    ("chime", t(70), 1.5, 0.4),
    ("iris", t(74) - 0.58, 1.2, 0.5),
    ("whoosh", t(76), 1.2, 0.35),
    ("whoosh", t(78) + 0.2, 1.2, 0.3),
    ("pop", t(80), 0.5, 0.4),
    ("iris", t(83), 1.2, 0.55),
    ("impact", t(88), 1.5, 0.35),
    ("iris", t(89) - 0.48, 1.2, 0.45),
    ("pop", t(95), 0.5, 0.3),
    ("click", t(100), 0.5, 0.5),
    ("click", t(108), 0.5, 0.5),
    ("click", t(115), 0.5, 0.5),
    ("tick", t(115) + 1.0, 0.5, 0.5),
    ("tick", t(115) + 2.0, 0.5, 0.5),
    ("pop", t(120), 0.5, 0.35),
    ("iris", t(121) - 0.5, 1.2, 0.45),
    ("pop", t(124), 0.5, 0.3),
    ("pop", t(128), 0.5, 0.3),
    ("pop", t(130), 0.5, 0.3),
    ("pop", t(132), 0.5, 0.3),
    ("chime", t(137), 1.5, 0.4),
    ("whoosh", 54.5, 1.2, 0.35),
    ("click", 55.9, 0.5, 0.55),
]

import subprocess
vo_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ROOT / "assets/vo.mp3")]).decode()) - 0.02
lines = [
    f'<audio id="vo" src="assets/vo.mp3" data-start="{VO}" data-duration="{vo_dur:.2f}" data-track-index="10" data-volume="1"></audio>',
    f'<audio id="mus" src="assets/music_mix.mp3" data-start="0" data-duration="{END}" data-track-index="11" data-volume="1"></audio>',
]
for k, (f, s, d, v) in enumerate(CUES):
    lines.append(f'<audio id="a{k}" src="assets/{f}.mp3" data-start="{s:.2f}" data-duration="{d}" data-track-index="{12 + k}" data-volume="{v}"></audio>')

src = (ROOT / "work/index.src.html").read_text()
src = src.replace("/*WORDS*/[]", json.dumps(W, ensure_ascii=False)).replace("<!--AUDIO-->", "\n      ".join(lines))
src = src.replace("/*VO*/0", str(VO)).replace("/*END*/0", str(END)).replace('data-duration="END"', f'data-duration="{END}"')
(ROOT / "index.html").write_text(src)
print(f"index.html written: {len(W)} words, {len(CUES)} SFX cues, END={END}s, VO ends {VO + vo_dur:.2f}s")
