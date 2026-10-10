#!/bin/bash
# Sequential ElevenLabs music + SFX with 429 backoff (the key is shared with parallel workers).
# Usage: bash el_audio.sh OUT_DIR   (music 47s: build, drop ~13.5s, breakdown ~39s; check with the loudness one-liner in PLAYBOOK.md)
set -u
OUT=${1:-assets}; source <(grep ELEVENLABS_API_KEY ~/.zshrc)
call(){ # url outfile json
  for i in 1 2 3 4 5 6; do
    code=$(curl -s -o "$2" -w "%{http_code}" "$1" -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" -d "$3")
    echo "$(basename $2) $code"; [ "$code" = 200 ] && return 0
    [ "$code" = 429 ] && sleep $((20 + i*10)) || { cat "$2"; rm -f "$2"; return 1; }
  done; return 1; }
[ -s "$OUT/music.mp3" ] || call https://api.elevenlabs.io/v1/music "$OUT/music.mp3" '{"prompt":"modern confident tech product launch film music, crisp electronic beat with deep sub bass, glossy synth plucks and airy pads, short tense riser intro, a punchy drop at 7.5 seconds with driving four-on-the-floor groove, energy keeps building, a short breakdown with filtered synths at 32 seconds, a riser and a big final hit at 43 seconds, then a short bright outro jingle that ends cleanly at 47 seconds, no vocals, premium Apple-style launch video","music_length_ms":47000}'
sfx(){ [ -s "$OUT/$1" ] || call https://api.elevenlabs.io/v1/sound-generation "$OUT/$1" "{\"text\":\"$2\",\"duration_seconds\":$3,\"prompt_influence\":0.7}"; }
sfx whoosh.mp3 "fast clean cinematic camera whoosh transition" 1.0
sfx scramble.mp3 "short digital data scramble, retro computer text decoding chirps" 1.0
sfx tick.mp3 "single soft UI click tick, clean digital" 0.5
sfx hit.mp3 "deep punchy cinematic bass impact hit, clean" 1.2
sfx chime.mp3 "bright modern app notification chime, two soft notes" 1.0
