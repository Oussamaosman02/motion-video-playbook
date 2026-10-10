#!/usr/bin/env python3
"""Embed a words.json ([[word, start, end], ...] from tts_with_timestamps.py) into index.html.

Canonical copy of ui-launch-film/tools/embed_words.py (/*W*/ markers) and
benchmark-film/tools/inject_words.py (`const W = ...; // from assets/words.json`). Both marker
styles are supported, so it works on either template; re-run it after every new voiceover.

Usage (from the project folder):
  python3 embed_words.py [index.html] [assets/words.json] [--full]
  --full keeps [word, start, end]; the default for the /*W*/ style is [word, start] (what ui-launch-film reads).
"""
import json
import re
import sys

args = [a for a in sys.argv[1:] if a != "--full"]
full = "--full" in sys.argv
html = args[0] if len(args) > 0 else "index.html"
words_path = args[1] if len(args) > 1 else "assets/words.json"
words = json.load(open(words_path, encoding="utf-8"))
s = open(html, encoding="utf-8").read()

if "/*W*/" in s:  # ui-launch-film style: /*W*/[...]/*W*/
    data = words if full else [[w[0], w[1]] for w in words]
    arr = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    s, n = re.subn(r"/\*W\*/.*?/\*W\*/", lambda m: f"/*W*/{arr}/*W*/", s, count=1, flags=re.S)
else:  # benchmark-film style: const W = [...]; // from assets/words.json
    line = "const W = " + json.dumps(words, ensure_ascii=False) + "; // from assets/words.json"
    s, n = re.subn(r"const W = .*?; // from assets/words\.json", lambda m: line, s, count=1)
if not n:
    sys.exit("no marker found: add /*W*/[]/*W*/ or `const W = []; // from assets/words.json` to the script")
open(html, "w", encoding="utf-8").write(s)
print(f"embedded {len(words)} words into {html}")
