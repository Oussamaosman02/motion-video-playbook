#!/usr/bin/env python3
"""Build index.html from tools/src.html.tpl: inject the VO word times and the SFX <audio> tags.

Every cue is a word index into assets/words.json (reused Bruno Torres VO, see RENDER.md),
so swapping the voice = new words.json + rerun this script. Local only, no API calls.
Usage: python3 tools/build.py
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
VO = 0.3      # VO offset on the film clock
END = 38.5    # film length (CTA + lockup after the VO ends at ~32.9 s)
W = json.loads((HERE / "assets/words.json").read_text())
t = lambda i: round(W[i][1] + VO, 3)

# (time, file, volume)  -- times come from word indexes, CTA times are absolute
SFX = [
    (0.05, "whoosh", 0.30),
    *[(t(1) + k * 0.28, "tick", 0.40) for k in range(6)],   # visitor pills arrive
    (t(12) - 0.1, "whoosh", 0.40),                           # all collapse into the same landing
    (t(13) + 0.25, "alert", 0.30),
    (t(14), "pop", 0.38),                                    # "Haz esto." cap pops
    (t(15) + 0.05, "blip", 0.35),
    (t(16), "tick", 0.40),
    (t(21), "alert", 0.42),                                  # demo crossed out
    (t(22), "impact", 0.45),                                 # quiz_funnel block lands
    (t(27), "blip", 0.30), (t(30), "blip", 0.30),
    (t(34), "key", 0.45), (t(37), "key", 0.45), (t(42), "key", 0.45),
    (t(47), "pop", 0.32), (t(50), "pop", 0.32), (t(54), "pop", 0.32),
    (t(55), "blip", 0.38), (t(58), "chime", 0.30),
    (t(59), "whoosh", 0.38), (t(62), "glitch", 0.30), (t(65), "blip", 0.38),
    (t(66), "impact", 0.50),                                 # "Y lo importante" floor
    (t(69), "whoosh", 0.35),
    (t(76), "key", 0.45), (t(79), "key", 0.45), (t(83), "key", 0.45),
    (t(87), "whoosh", 0.30), (t(90), "blip", 0.40), (t(94), "blip", 0.40), (t(96), "blip", 0.40),
    (t(103), "chime", 0.45),                                 # compra ✓
    (33.35, "whoosh", 0.35),
    *[(33.9 + k * 0.09, "key", 0.22) for k in range(0, 13, 2)],  # "$ comenta QUIZ" typing
    (36.2, "pop", 0.40),                                     # lockup
    (36.6, "chime", 0.45),                                   # ending is never silent
]
DUR = {"whoosh": 1.0, "tick": 0.5, "alert": 0.6, "pop": 0.5, "blip": 0.5, "impact": 2.0,
       "key": 0.5, "glitch": 1.2, "chime": 1.0}

audio = [
    f'<audio id="vo" src="assets/vo.mp3" data-start="{VO}" data-duration="32.6" data-track-index="10" data-volume="1"></audio>',
    f'<audio id="mus" src="assets/music.mp3" data-start="0" data-duration="{END}" data-track-index="11" data-volume="0.26"></audio>',
]
for k, (at, f, v) in enumerate(sorted(SFX)):
    audio.append(f'<audio id="a{k}" src="assets/{f}.mp3" data-start="{at:.3f}" data-duration="{DUR[f]}" '
                 f'data-track-index="{12 + k}" data-volume="{v}"></audio>')

src = (HERE / "tools/src.html.tpl").read_text()
out = (src.replace("<!--AUDIO-->", "\n      ".join(audio))
          .replace("/*WORDS*/[]", json.dumps([[w[0], round(w[1], 3), round(w[2], 3)] for w in W], ensure_ascii=False))
          .replace("/*VO*/0", str(VO)).replace("/*END*/0", str(END)).replace('data-duration="END"', f'data-duration="{END}"'))
(HERE / "index.html").write_text(out)
print(f"index.html: {len(W)} words, {len(SFX)} sfx, END {END}s")
for i in (0, 14, 16, 26, 43, 59, 66, 69, 87, 93, 103):
    print(f"  w{i} {W[i][0]} @ {t(i)}")
