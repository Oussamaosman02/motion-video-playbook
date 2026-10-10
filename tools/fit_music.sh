#!/bin/bash
# Fit a music bed (fresh or reused) to the film length: trim + fade, or splice sections with crossfades.
# Canonical copy (2026-10-07, batch 2). Unifies the trim/fade and splice commands that workers rewrote by hand:
# frosted-glass-film/tools/splice_music.sh, terminal-teaser (atrim+acrossfade), hero-object-film (WAV splice),
# ui-launch-film-scatter-mosaic (3-part splice), and the trim+fade lines in halftone-mascot-film, mascot-cast-film,
# crt-desktop-film and every reused bed in batch 2.
#
# Usage:
#   fit_music.sh IN OUT LEN                       # trim to LEN s, 0.3 s fade-in, fade-out over the last FADE s
#   fit_music.sh IN OUT LEN 0-40 32-45 46.5-54.5  # keep these source ranges in order, crossfaded, then trim/fade to LEN
#   fit_music.sh IN OUT LEN 9.6-47.1 55.6-end     # "end" = end of the source (keep the track's real outro)
# Env: XF=crossfade seconds between ranges (default 1.0), FADE=fade-out seconds (default 2.0), FADEIN (default 0.3),
#      GAIN=extra dB on the result (e.g. GAIN=4 for a quiet reused bed).
# Works through WAV files: a single asplit/atrim filtergraph on an mp3 returned the wrong section twice (hero-object-film).
# Prints the result's duration and the loudness of its last 3 s (a music tail can make the lockup silent).
# Local ffmpeg only, never calls an API. Never edits IN: copy reused beds into your own project first (x-batch/AUDIO-REUSE.md).
set -euo pipefail
IN=${1:?IN}; OUT=${2:?OUT}; LEN=${3:?LEN seconds}; shift 3
XF=${XF:-1.0}; FADE=${FADE:-2.0}; FADEIN=${FADEIN:-0.3}; GAIN=${GAIN:-0}
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
ffmpeg -v error -y -i "$IN" -ac 2 -ar 44100 "$tmp/src.wav"
if [ $# -eq 0 ]; then
  cp "$tmp/src.wav" "$tmp/joined.wav"
else
  n=0
  for r in "$@"; do
    s=${r%-*}; e=${r#*-}
    if [ "$e" = "end" ]; then ffmpeg -v error -y -ss "$s" -i "$tmp/src.wav" "$tmp/p$n.wav"
    else ffmpeg -v error -y -ss "$s" -to "$e" -i "$tmp/src.wav" "$tmp/p$n.wav"; fi
    n=$((n+1))
  done
  cp "$tmp/p0.wav" "$tmp/joined.wav"
  for ((i=1; i<n; i++)); do
    ffmpeg -v error -y -i "$tmp/joined.wav" -i "$tmp/p$i.wav" -filter_complex "[0][1]acrossfade=d=$XF:c1=tri:c2=tri" "$tmp/j.wav"
    mv "$tmp/j.wav" "$tmp/joined.wav"
  done
fi
st=$(python3 -c "print(max(0, $LEN - $FADE))")
ffmpeg -v error -y -i "$tmp/joined.wav" -t "$LEN" \
  -af "afade=t=in:d=$FADEIN,afade=t=out:st=$st:d=$FADE,volume=${GAIN}dB,alimiter=limit=0.95" -c:a libmp3lame -q:a 2 "$OUT"
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
tail=$(ffmpeg -v error -sseof -3 -i "$OUT" -af volumedetect -f null - 2>&1 | sed -n 's/.*mean_volume: //p')
[ -n "$tail" ] || tail=$(ffmpeg -hide_banner -sseof -3 -i "$OUT" -af volumedetect -f null - 2>&1 | sed -n 's/.*mean_volume: //p')
echo "$OUT  duration ${d}s  last-3s mean ${tail}"
python3 - "$d" "$LEN" <<'P'
import sys
d, want = float(sys.argv[1]), float(sys.argv[2])
if d < want - 0.05:
    print(f"WARNING: result is {d:.2f}s, shorter than LEN {want:.2f}s: add a range or loop a section")
P
