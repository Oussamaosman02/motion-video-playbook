#!/bin/bash
# Fit a reused music bed to a form-dossier film and report the opening/ending loudness.
# Usage: tools/fit_bed.sh SRC.mp3 OUT.mp3 LEN [ranges...]   (ranges as in playbook/tools/fit_music.sh)
# Example (minchoi-b, saivion bed → 46 s, keeps the 8.5 s drop for the APROBADO stamp):
#   tools/fit_bed.sh work/music_src_saivion.mp3 assets/music.mp3 46 0-38.5 30-end
# Local ffmpeg only. Never edits SRC.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
FIT="$HERE/../../tools/fit_music.sh"
SRC=${1:?SRC}; OUT=${2:?OUT}; LEN=${3:?LEN}; shift 3
FADE=${FADE:-2.5} bash "$FIT" "$SRC" "$OUT" "$LEN" "$@"
first=$(ffmpeg -t 3 -i "$OUT" -af volumedetect -f null - 2>&1 | awk '/mean_volume/{print $5}')
echo "first-3s mean ${first} dB (want > -30: the hook stamp needs an audible bed)"
