#!/bin/bash
# Sequential ElevenLabs music + SFX with 429 backoff (the key is shared with parallel workers).
# Usage: bash el_audio.sh OUT_DIR   (template: bash ../playbook/frosted-glass-film/tools/el_audio.sh assets; then splice music with splice_music.sh)
set -u
OUT=${1:-assets}; source <(grep ELEVENLABS_API_KEY ~/.zshrc)
call(){ # url outfile json
  for i in 1 2 3 4 5 6; do
    code=$(curl -s -o "$2" -w "%{http_code}" "$1" -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" -d "$3")
    echo "$(basename $2) $code"; [ "$code" = 200 ] && return 0
    rm -f "$2"; [ "$code" = 429 ] && sleep $((20 + i*10)) || return 1
  done; return 1; }
[ -s "$OUT/music.mp3" ] || call https://api.elevenlabs.io/v1/music "$OUT/music.mp3" '{"prompt":"minimal elegant premium product launch film music, clean soft felt piano motif with delicate glassy plucks and airy pads, subtle ticking hi-hat pulse, calm and confident, sophisticated Scandinavian design feel, gentle build with soft sub bass from 10 seconds, fuller and brighter from 26 seconds, a short quiet breath at 32 seconds, final lift at 34 seconds, then resolves into a soft warm outro chord at 44 seconds and ends cleanly at 48 seconds, no vocals","music_length_ms":48000}'
sfx(){ [ -s "$OUT/$1" ] || call https://api.elevenlabs.io/v1/sound-generation "$OUT/$1" "{\"text\":\"$2\",\"duration_seconds\":$3,\"prompt_influence\":0.7}"; }
sfx whoosh.mp3 "soft airy glass whoosh transition, gentle, clean, subtle" 1.2
sfx glass.mp3 "soft glass tap, delicate crystal UI tick, clean" 0.5
sfx key.mp3 "soft quiet laptop keyboard typing, a few keystrokes, clean" 1.5
sfx click.mp3 "single soft mouse click, clean UI" 0.5
sfx chime.mp3 "gentle bright notification chime, two soft glassy bell notes" 1.2
