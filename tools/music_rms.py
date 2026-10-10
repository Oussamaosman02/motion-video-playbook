#!/usr/bin/env python3
"""Loudness map of a music track: find the drop, the breaks and where it dies, to place scene cuts.

Canonical copy (2026-10-07, batch 2). The same scan was rewritten by 5 workers: motion-showreel/tools/music_rms.py,
the inline "drop finder" snippets in search-bar-film, airy-launch and terminal-teaser, and hero-object-film's probe.

Usage:
  python3 music_rms.py assets/music.mp3            # 0.5 s windows + a summary
  python3 music_rms.py assets/music.mp3 0.25       # finer windows (e.g. to cut on 128 BPM bars, bar = 1.875 s)
  python3 music_rms.py assets/music.mp3 1 --quiet  # summary only

Prints "t:dB" per window, then a summary:
  drops   = a window >= 6 dB louder than the 2 s before it (land a big reveal there)
  breaks  = 2+ s stretches >= 5 dB under the track median (quiet proof beat / riser)
  dies at = start of the final stretch under median-12 dB (the outro tail; put the lockup before it,
            or splice a loud section on the end with fit_music.sh)
Needs ffmpeg + numpy. Local, free, no API.
"""
import subprocess, sys
import numpy as np

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    sys.exit(__doc__)
path = args[0]
step = float(args[1]) if len(args) > 1 else 0.5
quiet = "--quiet" in sys.argv

sr = 16000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
a = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
h = max(1, int(sr * step))
db = np.array([20 * np.log10(np.sqrt(np.mean(a[j:j + h] ** 2)) + 1e-9) for j in range(0, len(a) - h + 1, h)])
t = np.arange(len(db)) * step
if not quiet:
    print(" ".join(f"{x:.2f}:{v:.0f}" for x, v in zip(t, db)))

med = float(np.median(db))
back = max(1, int(round(2 / step)))
drops = [t[i] for i in range(back, len(db)) if db[i] - db[i - back:i].mean() >= 6 and db[i] > med - 3]
# keep the first window of each cluster
drops = [d for k, d in enumerate(drops) if k == 0 or d - drops[k - 1] > 2]

breaks, start = [], None
for i, v in enumerate(db):
    low = v < med - 5
    if low and start is None:
        start = i
    if (not low or i == len(db) - 1) and start is not None:
        end = i if not low else i + 1
        if (end - start) * step >= 2:
            breaks.append((t[start], t[start] + (end - start) * step))
        start = None

dies = None
for i in range(len(db) - 1, -1, -1):
    if db[i] >= med - 12:
        dies = t[i] + step if i < len(db) - 1 else None
        break

dur = len(a) / sr
print(f"\nduration {dur:.2f}s  median {med:.1f} dB")
print("drops   " + (", ".join(f"{d:.2f}s" for d in drops) or "none found"))
print("breaks  " + (", ".join(f"{s:.1f}-{e:.1f}s" for s, e in breaks) or "none"))
print("dies at " + (f"{dies:.2f}s (tail under median-12 dB)" if dies else "never (loud to the end)"))
