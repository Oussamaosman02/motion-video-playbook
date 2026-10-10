#!/usr/bin/env python3
"""Mix voiceover + music bed + marker SFX (only while writing) + a whoosh on the phone reveal.

Usage:
  python3 mix_whiteboard_audio.py config.json silent.mp4 vo.mp3 music.mp3 marker_sfx.mp3 whoosh.mp3 out.mp4

Fork of ../../tools/mix_chalk_audio.py. Marker SFX is looped and gated by the elements'
[start, start+dur] windows. Levels: voice 1.0, music 0.14 (lifts to 0.30 after the voice for the
reveal hold, fades out over the last 1.5s), marker 0.45 high-passed at 900 Hz, whoosh 0.5.
"""
import json
import subprocess
import sys

cfg_path, silent, vo, music, sfx, whoosh, out = sys.argv[1:8]
c = json.load(open(cfg_path))
D = c["duration"]
R = c.get("reveal", {}).get("start", D)
gate = "+".join(f"between(t,{e['start']:.2f},{e['start'] + e['dur']:.2f})" for e in c["elements"])
fc = (f"[1:a]volume=1.0,apad[vo];"
      f"[2:a]volume='0.14+0.16*min(1,max(0,(t-{R - 0.3:.2f})/0.6))':eval=frame,afade=t=in:d=0.6,afade=t=out:st={D - 1.5}:d=1.5[mu];"
      f"[3:a]volume='0.45*gt({gate},0)':eval=frame,highpass=f=900[mk];"
      f"[4:a]volume=0.5,adelay={int(R * 1000)}|{int(R * 1000)}[wh];"
      f"[vo][mu][mk][wh]amix=inputs=4:normalize=0:duration=first,atrim=0:{D}[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", vo, "-i", music, "-stream_loop", "-1", "-i", sfx,
                "-i", whoosh, "-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
                "-b:a", "192k", "-t", str(D), out], check=True)
print("->", out)
