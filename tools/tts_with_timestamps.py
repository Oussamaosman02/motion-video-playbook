#!/usr/bin/env python3
"""Generate a voiceover with ElevenLabs and word-level timings in one call.

Usage:
  export ELEVENLABS_API_KEY=...            # e.g. `source <(grep ELEVENLABS_API_KEY ~/.zshrc)`
  python3 tts_with_timestamps.py script.txt out_dir [voice_id] [speed]

Writes out_dir/vo.mp3 and out_dir/words.json ([[word, start, end], ...]).
Default voice: Gabriel Blanco (Spain Spanish, energetic) RwzBDEn5f6FIgpAjH9YN.
List voices:  curl -s "https://api.elevenlabs.io/v2/voices?page_size=100" -H "xi-api-key: $ELEVENLABS_API_KEY"
"""
import base64
import json
import os
import sys
import urllib.request

script, out = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else "RwzBDEn5f6FIgpAjH9YN"
speed = float(sys.argv[4]) if len(sys.argv) > 4 else 1.08
os.makedirs(out, exist_ok=True)

body = json.dumps({
    "text": open(script, encoding="utf-8").read().strip(),
    "model_id": "eleven_multilingual_v2",
    "language_code": "es",
    "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35,
                       "use_speaker_boost": True, "speed": speed},
}).encode()
req = urllib.request.Request(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
    data=body,
    headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"},
)
d = json.load(urllib.request.urlopen(req))
open(f"{out}/vo.mp3", "wb").write(base64.b64decode(d["audio_base64"]))

# character alignment -> words
a = d["alignment"]
words, cur, s, e = [], "", None, None
for c, b, f in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
    if c.isspace():
        if cur:
            words.append([cur, round(s, 3), round(e, 3)])
            cur = ""
        continue
    if not cur:
        s = b
    cur += c
    e = f
if cur:
    words.append([cur, round(s, 3), round(e, 3)])
json.dump(words, open(f"{out}/words.json", "w"), ensure_ascii=False)
print(f"{len(words)} words, ends at {words[-1][2]}s -> {out}/vo.mp3, {out}/words.json")
