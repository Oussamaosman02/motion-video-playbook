#!/bin/bash
# tts_with_timestamps.py with 429/5xx backoff (shared ElevenLabs key)
source <(grep ELEVENLABS_API_KEY ~/.zshrc)
for i in 1 2 3 4 5 6; do
  out=$(python3 /Users/amalio/Downloads/insta/playbook/tools/tts_with_timestamps.py "$@" 2>&1) && { echo "$out"; exit 0; }
  echo "$out" | tail -2
  echo "$out" | grep -qE "429|50[023]" || exit 1
  sleep $((20+10*i))
done; exit 1
