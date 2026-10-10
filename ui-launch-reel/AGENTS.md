# Agent instructions: UI launch reel

This folder is a self-contained recipe for a light, pixel-mono "product launch" reel. It has typed Geist Pixel headlines with one accent phrase, UI-mock proof cards, a VS split, and a comparison table with a GANADOR badge and confetti. There is no voiceover: music + UI SFX only. Built in HyperFrames, with 1 Gemini image and no AI video.

1. Read `PLAYBOOK.md` fully before doing anything.
2. Start from a copy of `template/` (HyperFrames 0.8.137 project; the on-screen copy is in `template/script.txt`).
3. Shared scripts live in `../tools/` (`gen_image.py`, `cutout_grid.py`). Do not edit them.
4. ElevenLabs calls one at a time, with a 20–60s backoff on HTTP 429.
5. Verify the final mp4 (ffprobe, volumedetect, extracted frames), not only snapshots.
