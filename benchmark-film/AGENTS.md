# Agent instructions: benchmark-film

This folder is a reproducible recipe for a near-black, AI-lab-style **benchmark / launch-announcement film** (9:16, narrated, bottom captions). It includes a prompt box, a report-card table, a terminal, a rotating dot sphere, a tilted UI collage, an A/B comparison with a cursor click, a step chip row, a line chart and a logo lockup. It is adapted from the HyperFrames Code2Video benchmark launch.

- Read `PLAYBOOK.md` fully before doing anything.
- Start from a copy of `template/` (HyperFrames 0.8.137). Never edit the template in place.
- Shared scripts are in `../tools/` (TTS with timestamps, gen_image, cutout_grid). This format's own script is in `tools/` (`inject_words.py`).
- Cues are word indexes: `t(i)` = `words.json[i].start + 0.3`. After a new voiceover, run `tools/inject_words.py` and re-index the cues.
- No AI video. Images only via Gemini (treg), on flat magenta, with no text in them. Make ElevenLabs calls one at a time and retry on 429.
- QA the final mp4 (ffprobe 1080x1920, volumedetect, 10+ extracted frames) before calling it done.
