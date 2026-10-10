#!/usr/bin/env python3
"""Shorten long pauses in a timestamped voiceover and shift the word timings to match.

Usage: python3 tighten_gaps.py vo.mp3 words.json out.mp3 out_words.json [max_gap=0.42] [keep=0.32]

Any silence between two words longer than max_gap is cut down to `keep` seconds
(the cut is taken from the middle of the gap, with 15ms crossfades).
"""
import json
import subprocess
import sys

vo, wj, out, owj = sys.argv[1:5]
MAX = float(sys.argv[5]) if len(sys.argv) > 5 else 0.42
KEEP = float(sys.argv[6]) if len(sys.argv) > 6 else 0.32
w = json.load(open(wj))
cuts = []  # (cut_start, cut_end) in source time
for a, b in zip(w, w[1:]):
    gap = b[1] - a[2]
    if gap > MAX:
        mid = (a[2] + b[1]) / 2
        cuts.append((mid - (gap - KEEP) / 2, mid + (gap - KEEP) / 2))
segs, t = [], 0.0
for c0, c1 in cuts:
    segs.append((t, c0)); t = c1
segs.append((t, None))
parts, labels = [], []
for i, (s, e) in enumerate(segs):
    trim = f"atrim=start={s:.3f}" + (f":end={e:.3f}" if e else "")
    parts.append(f"[0:a]{trim},asetpts=PTS-STARTPTS,afade=t=in:d=0.015[s{i}]")
    labels.append(f"[s{i}]")
fc = ";".join(parts) + ";" + "".join(labels) + f"concat=n={len(segs)}:v=0:a=1[a]"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", vo, "-filter_complex", fc, "-map", "[a]", "-b:a", "192k", out], check=True)


def shift(x):
    return round(x - sum(min(c1, max(x, c0)) - c0 for c0, c1 in cuts if x > c0), 3)


json.dump([[x[0], shift(x[1]), shift(x[2])] + x[3:] for x in w], open(owj, "w"), ensure_ascii=False)
print(f"{len(cuts)} gaps cut, saved {sum(c1 - c0 for c0, c1 in cuts):.2f}s -> {out}")
