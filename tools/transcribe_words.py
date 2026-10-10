#!/usr/bin/env python3
"""Word timings for an EXISTING audio file (ElevenLabs Scribe), optionally with speakers.

Usage:
  python3 transcribe_words.py audio.mp3 words.json [--diarize]

Copy files with odd names (commas, semicolons, ".mp3.mpeg") to a clean path first:
curl -F breaks on those and returns an empty body.
"""
import json
import os
import subprocess
import sys

audio, out = sys.argv[1], sys.argv[2]
cmd = ["curl", "-s", "https://api.elevenlabs.io/v1/speech-to-text",
       "-H", f"xi-api-key: {os.environ['ELEVENLABS_API_KEY']}",
       "-F", "model_id=scribe_v1", "-F", "language_code=es", "-F", f"file=@{audio}"]
if "--diarize" in sys.argv:
    cmd += ["-F", "diarize=true"]
d = json.loads(subprocess.run(cmd, capture_output=True, text=True, check=True).stdout)
words = [[w["text"], round(w["start"], 3), round(w["end"], 3)] + ([w.get("speaker_id")] if "--diarize" in sys.argv else [])
         for w in d["words"] if w["type"] == "word"]
json.dump(words, open(out, "w"), ensure_ascii=False)
print(d["text"])
print(f"{len(words)} words -> {out}")
