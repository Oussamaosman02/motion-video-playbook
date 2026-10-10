#!/bin/bash
# Analyse ONE time range of a long reference (when a film is split across workers).
# Usage: ref_range.sh ref.mp4 START END OUTDIR [STEP=2] "t1 t2 ..."
# Writes OUTDIR/sheet.jpg (one tile every STEP s, 5 columns) and OUTDIR/keys.jpg (2-column grid of the key times, 640 px each).
set -euo pipefail
IN=${1:?ref}; S=${2:?start}; E=${3:?end}; OUT=${4:?outdir}; STEP=${5:-2}; KEYS=${6:-}
mkdir -p "$OUT/frames"
ffmpeg -v error -y -ss "$S" -t "$(python3 -c "print($E-$S)")" -i "$IN" -vf "fps=1/$STEP,scale=320:-1,tile=5x$(python3 -c "import math;print(math.ceil(($E-$S)/$STEP/5))")" -frames:v 1 "$OUT/sheet.jpg"
[ -z "$KEYS" ] && exit 0
args=(); n=0
for t in $KEYS; do ffmpeg -v error -y -ss "$t" -i "$IN" -frames:v 1 -vf scale=640:-1 "$OUT/frames/f$t.jpg"; args+=(-i "$OUT/frames/f$t.jpg"); n=$((n+1)); done
python3 - "$OUT" "$n" "${args[@]}" <<'P'
import sys,subprocess
out,n=sys.argv[1],int(sys.argv[2]); ins=sys.argv[3:]
lay=[]
for i in range(n):
    x="0" if i%2==0 else "w0"; y="+".join(["h0"]*(i//2)) or "0"; lay.append(f"{x}_{y}")
if n%2: ins+=["-f","lavfi","-i","color=black:s=640x360:d=0.04"]; lay.append("w0_"+("+".join(["h0"]*(n//2)) or "0")); n+=1
subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex","".join(f"[{i}]" for i in range(n))+f"xstack=inputs={n}:layout="+"|".join(lay),"-frames:v","1",out+"/keys.jpg"],check=True)
P
