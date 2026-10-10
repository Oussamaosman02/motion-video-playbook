#!/usr/bin/env python3
"""Turn a local `hyperframes transcribe` transcript.json into (a) an index:word@time list for
planning cuts and (b) the `const W = [...]` array the template's script expects.

usage: python3 -I words_to_js.py path/to/transcript.json [--offset 0.3]
Whisper sometimes emits a junk first token for music-only intros; tokens with no letters/digits are dropped.
"""
import json, re, sys

def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    off = 0.0
    if "--offset" in args:
        i = args.index("--offset"); off = float(args[i + 1]); del args[i:i + 2]
    words = json.load(open(args[0]))
    if isinstance(words, dict):
        words = words.get("words") or words.get("segments") or []
    keep = [w for w in words if re.search(r"\w", w.get("text", ""))]
    for i, w in enumerate(keep):
        print(f"{i:3d}:{w['text'].strip()}@{w['start'] + off:.2f}")
    arr = ",".join(json.dumps([w["text"].strip(), round(w["start"], 2), round(w["end"], 2)], ensure_ascii=False) for w in keep)
    print(f"\nconst W = [{arr}];")

if __name__ == "__main__":
    main()
