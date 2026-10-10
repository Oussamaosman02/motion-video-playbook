#!/usr/bin/env python3
"""Embed assets/words.json into index.html (`const W = ...; // from assets/words.json`) and inject the SFX
<audio> tags between <!--SFX--> markers from sfx.json (cues keyed to word indices, so a new VO re-syncs them).
Usage (from the project folder): python3 build.py"""
import json, re, subprocess
OFF = 0.6
W = json.load(open("assets/words.json", encoding="utf-8"))
s = open("index.html", encoding="utf-8").read()
s = re.sub(r"const W = .*?; // from assets/words\.json", lambda m: "const W = " + json.dumps(W, ensure_ascii=False) + "; // from assets/words.json", s, count=1)
dur = {}
tags = []
for k, (f, i, off, vol) in enumerate(json.load(open("sfx.json"))["cues"]):
    if f not in dur:
        dur[f] = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"assets/{f}.mp3"]))
    t = (W[i][1] + OFF + off) if i is not None else off
    tags.append(f'<audio id="sfx{k}" src="assets/{f}.mp3" data-start="{max(t, 0):.2f}" data-duration="{dur[f]:.2f}" data-track-index="{10 + k}" data-volume="{vol}"></audio>')
s = re.sub(r"<!--SFX-->.*?<!--/SFX-->", lambda m: "<!--SFX-->\n      " + "\n      ".join(tags) + "\n      <!--/SFX-->", s, count=1, flags=re.S)
open("index.html", "w", encoding="utf-8").write(s)
print(f"embedded {len(W)} words, {len(tags)} sfx")
