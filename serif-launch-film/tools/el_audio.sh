#!/bin/bash
# Sequential ElevenLabs music/SFX calls with 429 backoff (key shared with other workers).
# usage: el_audio.sh music OUT "prompt" LENGTH_MS   |   el_audio.sh sfx OUT "text" SECONDS
source <(grep ELEVENLABS_API_KEY ~/.zshrc)
kind=$1; out=$2; text=$3; len=$4
if [ "$kind" = music ]; then url=https://api.elevenlabs.io/v1/music; body=$(python3 -c 'import json,sys;print(json.dumps({"prompt":sys.argv[1],"music_length_ms":int(sys.argv[2])}))' "$text" "$len")
else url=https://api.elevenlabs.io/v1/sound-generation; body=$(python3 -c 'import json,sys;print(json.dumps({"text":sys.argv[1],"duration_seconds":float(sys.argv[2]),"prompt_influence":0.7}))' "$text" "$len"); fi
for i in 1 2 3 4 5 6; do
  code=$(curl -s -o "$out" -w "%{http_code}" "$url" -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" -d "$body")
  echo "$out $code"; [ "$code" = 200 ] && exit 0
  [ "$code" = 429 ] && { sleep $((20 + i*10)); continue; }; head -c 300 "$out"; exit 1
done; exit 1
