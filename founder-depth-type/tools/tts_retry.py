#!/usr/bin/env python3
"""ElevenLabs TTS with timestamps + 429/5xx backoff (the key is shared, never call in parallel).

Usage: python3 tts_retry.py "text" out.mp3 out_words.json voice_id [speed] [stability]
"""
import base64, json, os, sys, time, urllib.request, urllib.error

text, mp3, wj, voice = sys.argv[1:5]
speed = float(sys.argv[5]) if len(sys.argv) > 5 else 1.05
stab = float(sys.argv[6]) if len(sys.argv) > 6 else 0.45
body = json.dumps({"text": text, "model_id": "eleven_multilingual_v2", "language_code": "es",
                   "voice_settings": {"stability": stab, "similarity_boost": 0.8, "style": 0.35,
                                      "use_speaker_boost": True, "speed": speed}}).encode()
for attempt in range(8):
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=180)); break
    except urllib.error.HTTPError as e:
        if e.code in (429, 500, 502, 503):
            w = 20 + attempt * 10; print(f"HTTP {e.code}, retry in {w}s", file=sys.stderr); time.sleep(w); continue
        raise SystemExit(f"HTTP {e.code}: {e.read()[:300]}")
else:
    raise SystemExit("gave up")
open(mp3, "wb").write(base64.b64decode(d["audio_base64"]))
a = d["alignment"]; words, cur, s, e = [], "", None, None
for c, b, f in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
    if c.isspace():
        if cur: words.append([cur, round(s, 3), round(e, 3)]); cur = ""
        continue
    if not cur: s = b
    cur += c; e = f
if cur: words.append([cur, round(s, 3), round(e, 3)])
json.dump(words, open(wj, "w"), ensure_ascii=False)
print(f"{len(words)} words, {words[-1][2]}s -> {mp3}")
