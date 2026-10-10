#!/usr/bin/env python3
"""Mix voiceover + music bed + chalk-scratch SFX (only while writing) onto the silent render.

Usage:
  python3 mix_chalk_audio.py config.json silent.mp4 vo.mp3 music.mp3 chalk_sfx.mp3 out.mp4

The chalk SFX is looped and gated by the elements' [start, start+dur] windows in config.json.
Levels: voice 1.0, music 0.13 (fades in 0.8s, out over the last 1.8s), chalk 0.32 high-passed.
"""
import json
import subprocess
import sys

cfg_path, silent, vo, music, sfx, out = sys.argv[1:7]
c = json.load(open(cfg_path))
D = c["duration"]
gate = "+".join(f"between(t,{e['start']:.2f},{e['start'] + e['dur']:.2f})" for e in c["elements"])
fc = (f"[1:a]volume=1.0,apad[vo];"
      f"[2:a]volume=0.13,afade=t=in:d=0.8,afade=t=out:st={D - 1.8}:d=1.8[mu];"
      f"[3:a]volume='0.32*gt({gate},0)':eval=frame,highpass=f=1200[ch];"
      f"[vo][mu][ch]amix=inputs=3:normalize=0:duration=first,atrim=0:{D}[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", vo, "-i", music, "-stream_loop", "-1", "-i", sfx,
                "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-t", str(D), out], check=True)
print("->", out)
