#!/bin/bash
# Measure SFX loudness and boost the near-silent ones (with a limiter so nothing clips).
# Canonical copy (2026-10-07, batch 2). Workers rewrote "volumedetect, then volume=NdB,alimiter" by hand in
# motion-showreel (pop −47 dB), paper-desk-film (stamp −62.9, drop −52.5), search-bar-film (blip −39),
# halftone-mascot-film (click/type −34), airy-launch-chapters (tick −50, pop −36) and el_audio.sh's tip.
#
# Usage:
#   sfx_normalize.sh assets/*.mp3                 # report only: mean/max dB per file, flags quiet ones
#   FIX=1 sfx_normalize.sh assets/*.mp3           # write <name>_n.mp3 next to each quiet file
#   FIX=1 INPLACE=1 sfx_normalize.sh assets/x.mp3 # replace the file (only on YOUR copy, never on a shared/reused source)
# Env: TARGET=mean dB to aim for (default −22), QUIET=threshold under which a file is "quiet" (default −30).
# Local ffmpeg only, no API calls.
set -uo pipefail
TARGET=${TARGET:--22}; QUIET=${QUIET:--30}; FIX=${FIX:-0}; INPLACE=${INPLACE:-0}
[ $# -gt 0 ] || { sed -n '2,13p' "$0"; exit 1; }
for f in "$@"; do
  out=$(ffmpeg -hide_banner -i "$f" -af volumedetect -f null - 2>&1)
  mean=$(sed -n 's/.*mean_volume: \(-*[0-9.]*\) dB/\1/p' <<<"$out"); max=$(sed -n 's/.*max_volume: \(-*[0-9.]*\) dB/\1/p' <<<"$out")
  [ -n "$mean" ] || { echo "?? $f (could not measure)"; continue; }
  quiet=$(python3 -c "print(int($mean < $QUIET))")
  if [ "$quiet" = 1 ]; then
    gain=$(python3 -c "print(round($TARGET - ($mean), 1))")
    echo "QUIET $f  mean $mean dB  max $max dB  -> +$gain dB"
    if [ "$FIX" = 1 ]; then
      dst="${f%.*}_n.${f##*.}"
      ffmpeg -v error -y -i "$f" -af "volume=${gain}dB,alimiter=limit=0.9" "$dst"
      if [ "$INPLACE" = 1 ]; then mv "$dst" "$f"; dst=$f; fi
      new=$(ffmpeg -hide_banner -i "$dst" -af volumedetect -f null - 2>&1 | sed -n 's/.*mean_volume: //p')
      echo "      wrote $dst  mean $new"
    fi
  else
    echo "ok    $f  mean $mean dB  max $max dB"
  fi
done
