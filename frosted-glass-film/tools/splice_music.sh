#!/bin/bash
# Cut a long ElevenLabs music track down to the film length, keeping its real ending.
# Usage: bash splice_music.sh IN.mp3 OUT.mp3 CUT_A CUT_B LEN
#   keeps IN[0:CUT_A] + IN[CUT_B:end] with a 1s crossfade, fades out the last 1.4s, trims to LEN.
#   template: bash splice_music.sh music.mp3 music50.mp3 40.5 51.5 50   (final hit of the outro lands at 44s)
# Find CUT_B with the per-second loudness print in PLAYBOOK.md (the breath before the outro).
set -eu
IN=$1; OUT=$2; A=$3; B=$4; LEN=$5
ffmpeg -v error -y -i "$IN" -filter_complex "[0]atrim=0:$A,asetpts=N/SR/TB[a];[0]atrim=$B,asetpts=N/SR/TB[b];[a][b]acrossfade=d=1:c1=tri:c2=tri,afade=t=out:st=$(echo "$LEN-1.4" | bc):d=1.4[o]" -map "[o]" -t "$LEN" "$OUT"
ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"
