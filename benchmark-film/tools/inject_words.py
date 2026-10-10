#!/usr/bin/env python3
"""Paste assets/words.json into index.html as the inline `const W = [...]` array.

Usage (from the project folder):  python3 tools/inject_words.py [index.html] [assets/words.json]

The composition reads cue times as t(i) = W[i][1] + VO (word index i), and builds the
bottom captions from W, so re-run this after every new voiceover, then re-check the
word indexes used in the timeline (print them with the one-liner in PLAYBOOK.md).
"""
import json
import re
import sys

html = sys.argv[1] if len(sys.argv) > 1 else "index.html"
words = sys.argv[2] if len(sys.argv) > 2 else "assets/words.json"
s = open(html, encoding="utf-8").read()
w = json.load(open(words, encoding="utf-8"))
line = "const W = " + json.dumps(w, ensure_ascii=False) + "; // from assets/words.json"
s, n = re.subn(r"const W = .*?; // from assets/words\.json", lambda m: line, s, count=1)
if not n:
    sys.exit("marker `const W = ...; // from assets/words.json` not found")
open(html, "w", encoding="utf-8").write(s)
print(f"{len(w)} words injected into {html}")
