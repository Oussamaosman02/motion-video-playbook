#!/usr/bin/env python3
"""Print a music track's loudness every STEP seconds, to find drops, breaks and the final hit.

Usage: python3 music_rms.py assets/music.mp3 [STEP=0.25]
Look for: a jump up (drop: land a big reveal there), a sustained dip of 5+ dB (break: use it for a
quieter "proof" beat and a riser), the last loud value before the tail (final hit: land the lockup there).
At 128 BPM a bar is 1.875 s, so cut on 1.875*k.
"""
import subprocess, sys
import numpy as np

path = sys.argv[1]; step = float(sys.argv[2]) if len(sys.argv) > 2 else 0.25
sr = 22050
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True, check=True).stdout
a = np.frombuffer(raw, dtype=np.int16).astype(float) / 32768
h = int(sr * step)
print(" ".join(f"{i*step:.2f}:{20*np.log10(np.sqrt(np.mean(a[j:j+h]**2))+1e-9):.0f}" for i, j in enumerate(range(0, len(a) - h, h))))
