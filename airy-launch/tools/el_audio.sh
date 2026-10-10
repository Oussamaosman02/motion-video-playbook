#!/bin/bash
# Sequential ElevenLabs music + SFX with 429 backoff (the key is shared with parallel workers).
# Usage: bash el_audio.sh OUT_DIR   (template: bash ../playbook/airy-launch/tools/el_audio.sh assets)
set -u
OUT=${1:-assets}; source <(grep ELEVENLABS_API_KEY ~/.zshrc)
call(){ # url outfile json
  for i in 1 2 3 4 5 6; do
    code=$(curl -s -o "$2" -w "%{http_code}" "$1" -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" -d "$3")
    echo "$(basename $2) $code"; [ "$code" = 200 ] && return 0
    [ "$code" = 429 ] && sleep $((20 + i*10)) || { cat "$2"; return 1; }
  done; return 1; }
[ -s "$OUT/music.mp3" ] || call https://api.elevenlabs.io/v1/music "$OUT/music.mp3" '{"prompt":"airy uplifting modern tech brand film music, soft warm felt piano and gentle plucked synths, light airy pads like flying above clouds, calm optimistic intro, a soft kick enters around 8 seconds and the track builds gently with light percussion, warm and confident, a small lift around 30 seconds, then resolves into a short bright bell-like outro jingle around 41 seconds and ends cleanly, no vocals, premium startup launch video","music_length_ms":45000}'
sfx(){ [ -s "$OUT/$1" ] || call https://api.elevenlabs.io/v1/sound-generation "$OUT/$1" "{\"text\":\"$2\",\"duration_seconds\":$3,\"prompt_influence\":0.7}"; }
sfx whoosh.mp3 "soft airy wind whoosh transition, gentle, clean" 1.2
sfx pop.mp3 "soft cute bubble pop, light UI appear sound" 0.5
sfx tick.mp3 "single soft UI click tick, clean digital" 0.5
sfx chime.mp3 "gentle bright notification chime, two soft bell notes" 1.2
