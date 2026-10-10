#!/usr/bin/env python3
"""Embed assets/words.json into index.html between the /*W*/ ... /*W*/ markers.

Usage (from the project folder):  python3 tools/embed_words.py
Run it again whenever you regenerate the voiceover; every cue in index.html is written as w(i) = word i start.
"""
import json
import re

words = json.load(open("assets/words.json"))
html = open("index.html", encoding="utf-8").read()
arr = json.dumps([[w[0], w[1]] for w in words], ensure_ascii=False, separators=(",", ":"))
html = re.sub(r"/\*W\*/.*?/\*W\*/", lambda m: f"/*W*/{arr}/*W*/", html, flags=re.S)
open("index.html", "w", encoding="utf-8").write(html)
print(f"embedded {len(words)} words")
