#!/bin/bash
# Canonical ElevenLabs music / SFX / raw-POST helper with 429 (and 5xx) backoff.
# The API key is shared by every agent on this machine: run calls ONE AT A TIME, never in parallel.
# Promoted from the per-format copies (airy-launch, notch-teaser, serif-launch-film, color-block-promo,
# frosted-glass-film, device-mockup-film el_audio.sh; ui-demo-film, glow-signal-film el_post.sh).
#
# Usage:
#   el_audio.sh music OUT.mp3 "prompt" LENGTH_MS          # POST /v1/music
#   el_audio.sh sfx   OUT.mp3 "text"   SECONDS            # POST /v1/sound-generation (SECONDS >= 0.5, else HTTP 400)
#   el_audio.sh post  OUT     /v1/endpoint 'JSON body'    # any other ElevenLabs POST (same as el_post.sh)
#
# Skips the call when OUT already exists and is non-empty (re-runs are free); set FORCE=1 to regenerate.
# Retries up to 6 times on 429/500/502/503, waiting 20+10*n seconds. A failed call deletes OUT and exits 1.
# Example (sequential block):
#   T=playbook/tools
#   bash $T/el_audio.sh music assets/music.mp3 "calm minimal launch music, no vocals" 45000
#   bash $T/el_audio.sh sfx assets/whoosh.mp3 "soft airy whoosh transition" 1.2
#   bash $T/el_audio.sh sfx assets/tick.mp3  "single soft UI click tick, clean digital" 0.5
# Tip: an SFX can come back near-silent (one tick was -41 dB). Check with
#   ffmpeg -i tick.mp3 -af volumedetect -f null - 2>&1 | grep mean_volume
# and normalise: ffmpeg -i tick.mp3 -af "volume=34dB,alimiter=limit=0.9" tick_n.mp3
set -u
[ -n "${ELEVENLABS_API_KEY:-}" ] || source <(grep ELEVENLABS_API_KEY ~/.zshrc)
kind=${1:?kind: music|sfx|post}; out=${2:?OUT path}; a=${3:?prompt/text/endpoint}; b=${4:?length/seconds/json}

case "$kind" in
  music) url=https://api.elevenlabs.io/v1/music
         body=$(python3 -c 'import json,sys;print(json.dumps({"prompt":sys.argv[1],"music_length_ms":int(sys.argv[2])}))' "$a" "$b") ;;
  sfx)   url=https://api.elevenlabs.io/v1/sound-generation
         body=$(python3 -c 'import json,sys;print(json.dumps({"text":sys.argv[1],"duration_seconds":float(sys.argv[2]),"prompt_influence":0.7}))' "$a" "$b") ;;
  post)  url="https://api.elevenlabs.io$a"; body=$b ;;
  *)     echo "unknown kind: $kind (music|sfx|post)" >&2; exit 2 ;;
esac

if [ -s "$out" ] && [ "${FORCE:-0}" != 1 ]; then echo "$out exists, skipped (FORCE=1 to redo)"; exit 0; fi
mkdir -p "$(dirname "$out")"
for i in 1 2 3 4 5 6; do
  code=$(curl -s -o "$out" -w "%{http_code}" "$url" -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" -d "$body")
  echo "$out $code"
  [ "$code" = 200 ] && exit 0
  case "$code" in
    429|500|502|503) sleep $((20 + i*10)); continue ;;
  esac
  head -c 300 "$out"; echo; rm -f "$out"; exit 1
done
rm -f "$out"; exit 1
