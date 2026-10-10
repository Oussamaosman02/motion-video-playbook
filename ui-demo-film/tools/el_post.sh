#!/bin/bash
# el_post.sh OUT ENDPOINT JSON  — ElevenLabs POST with 429 backoff (shared key, sequential only)
source <(grep ELEVENLABS_API_KEY ~/.zshrc)
out=$1; ep=$2; data=$3
for i in 1 2 3 4 5 6; do
  code=$(curl -s -o "$out" -w "%{http_code}" "https://api.elevenlabs.io$ep" -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" -d "$data")
  echo "$out $code"; [ "$code" = 200 ] && exit 0
  [ "$code" = 429 ] && { sleep $((20 + i*8)); continue; }
  head -c 300 "$out"; exit 1
done; exit 1
