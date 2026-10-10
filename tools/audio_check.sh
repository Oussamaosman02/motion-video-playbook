#!/bin/bash
# Final-mp4 audio check: whole-file loudness plus the first and last N seconds on their own.
# Canonical copy (2026-10-07, batch 2). Workers ran these volumedetect checks by hand on robj3d3, jahooma, boxd,
# elevenlabs and feijen-whiteboard: whole-file numbers looked fine while the ending (lockup + CTA) was almost silent.
# Usage: audio_check.sh video.mp4 [N=3]
# Warns when the tail or head mean is under −35 dB. Local ffmpeg only.
set -uo pipefail
f=${1:?video or audio file}; N=${2:-3}
m() { ffmpeg -hide_banner "$@" -af volumedetect -f null - 2>&1 | sed -n 's/.*mean_volume: \(-*[0-9.]*\) dB/\1/p'; }
x() { ffmpeg -hide_banner "$@" -af volumedetect -f null - 2>&1 | sed -n 's/.*max_volume: \(-*[0-9.]*\) dB/\1/p'; }
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
all=$(m -i "$f"); mx=$(x -i "$f"); head=$(m -t "$N" -i "$f"); tail=$(m -sseof "-$N" -i "$f")
echo "$f  ${d}s  whole mean ${all} dB / max ${mx} dB  first ${N}s ${head} dB  last ${N}s ${tail} dB"
python3 - "$head" "$tail" "$mx" <<'P'
import sys
h, t, mx = (float(v) if v else -99 for v in sys.argv[1:])
if t < -35: print("WARNING: the ending is near-silent (music tail?): splice a loud section with fit_music.sh or add a chime")
if h < -35: print("WARNING: the opening is near-silent: the hook needs sound (SFX or a punchier music start)")
if mx > -0.5: print("WARNING: peaks near 0 dB: lower the mix or add alimiter")
P
