# Agent instructions: Search-bar launch film

This folder is a self-contained recipe for a clean fintech-style launch film (light grey canvas, white UI cards, black tiles, one accent colour). A **search bar types one query per beat** and the scene under it answers the query. There is no voiceover: music + UI SFX, with the script as on-screen text. Built in HyperFrames 0.8.137 with 1 Gemini image and no AI video. Reference: @FacundoMarino1's Wallbit promo (made with Claude). Closest siblings: `../ui-launch-reel/` (F2) and `../color-block-promo/` (G4).

1. Read `PLAYBOOK.md` fully before doing anything.
2. Start from a copy of `template/` (the on-screen copy and the beat timings are in `template/script.txt`).
3. Shared scripts live in `../tools/` (`el_audio.sh`, `gen_image_ar.py`, `cutout_grid.py`). Do not edit them.
4. ElevenLabs calls one at a time (the key is shared); `el_audio.sh` backs off on HTTP 429.
5. Keep the "ejemplo" chips on invented numbers; never present generated people as real customers.
6. Verify the final mp4 (ffprobe, volumedetect, extracted frames), not only snapshots.
