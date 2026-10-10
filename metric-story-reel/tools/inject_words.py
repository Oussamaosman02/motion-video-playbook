#!/usr/bin/env python3
"""Swap the VO word timings embedded in index.html (the `const W = [...]` line).

Usage: python3 tools/inject_words.py words.json index.html
words.json = [[word, start, end], ...] (ElevenLabs alignment) or a hyperframes `transcribe` transcript.json
({"words":[{"text","start","end"}]} or a list of such dicts). Every scene time is t(i) = W[i][1] + VO, so after
swapping the voice, re-check the word INDEXES used in the script block (T2..C9, t(28), t(55)...) against the new
print-out this tool gives (index:word@start), then re-run `npx hyperframes@0.8.137 check` and snapshots.
"""
import json, re, sys

src, html = sys.argv[1], sys.argv[2]
w = json.load(open(src))
if isinstance(w, dict):
    w = w.get("words", w.get("segments", []))
rows = []
for x in w:
    if isinstance(x, list):
        rows.append([x[0], round(float(x[1]), 3), round(float(x[2]), 3)])
    else:
        rows.append([x.get("text", x.get("word", "")).strip(), round(float(x["start"]), 3), round(float(x["end"]), 3)])
s = open(html, encoding="utf-8").read()
new, n = re.subn(r"const W = \[.*?\];", "const W = " + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";", s, count=1, flags=re.S)
if n != 1:
    sys.exit("no `const W = [...];` line found")
open(html, "w", encoding="utf-8").write(new)
print(" ".join(f"{i}:{r[0]}@{r[1]:.2f}" for i, r in enumerate(rows)))
print(f"{len(rows)} words written to {html}")
