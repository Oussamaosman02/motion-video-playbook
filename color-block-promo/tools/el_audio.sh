#!/bin/bash
# Sequential ElevenLabs music/SFX with 429 backoff. Usage:
#   el_audio.sh music OUT.mp3 "prompt" LENGTH_MS
#   el_audio.sh sfx   OUT.mp3 "prompt" SECONDS
source <(grep ELEVENLABS_API_KEY ~/.zshrc)
kind=$1; out=$2; prompt=$3; len=$4
for try in 1 2 3 4 5 6; do
  if [ "$kind" = music ]; then
    code=$(curl -s -o "$out" -w "%{http_code}" https://api.elevenlabs.io/v1/music -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
      -d "$(python3 -c 'import json,sys;print(json.dumps({"prompt":sys.argv[1],"music_length_ms":int(sys.argv[2])}))' "$prompt" "$len")")
  else
    code=$(curl -s -o "$out" -w "%{http_code}" https://api.elevenlabs.io/v1/sound-generation -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
      -d "$(python3 -c 'import json,sys;print(json.dumps({"text":sys.argv[1],"duration_seconds":float(sys.argv[2]),"prompt_influence":0.7}))' "$prompt" "$len")")
  fi
  echo "$out $code"
  [ "$code" = 200 ] && exit 0
  [ "$code" = 429 ] && { sleep $((20 + try*10)); continue; }
  head -c 300 "$out"; exit 1
done
exit 1
