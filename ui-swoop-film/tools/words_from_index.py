#!/usr/bin/env python3
"""Print the word table embedded in a HyperFrames index.html (`const W = [[word,start,end],...]`)
as `index:word@filmTime`, so cues written as t(i) can be checked or re-mapped after swapping the VO.
Usage: python3 -I words_from_index.py path/to/index.html [VO_OFFSET=0.3]
Local only, no API."""
import json, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
off = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
m = re.search(r"const W = (\[\[.*?\]\]);", src, re.S)
if not m:
    sys.exit("no `const W = [[...]]` array found")
W = json.loads(m.group(1))
print("  ".join(f"{i}:{w}@{s + off:.2f}" for i, (w, s, e) in enumerate(W)))
