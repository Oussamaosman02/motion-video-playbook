# Agent instructions: Halftone mascot film

This folder is a self-contained recipe for a punchy voiced product film: a 3D clay mascot printed as a 1-bit halftone "talks" (pose swaps per word) while the spoken words appear as the headline one by one, with red italic-serif accent words. Scenes hard-cut between white, full-bleed brand red, black and a grid "bento" of product tiles, under a mono HUD with a live timecode. Built in HyperFrames, with 5 Gemini images and no AI video.

1. Read `PLAYBOOK.md` fully before doing anything.
2. Start from a copy of `template/` (HyperFrames 0.8.137 project; narration in `template/script.txt`; source renders in `template/sources/`).
3. Format helpers are in `tools/` (`halftone_sprite.py`, `tts_retry.sh`); `template/build.py` embeds words + word-indexed SFX. Shared scripts live in `../tools/` (`gen_image_ar.py`, `el_audio.sh`, `tts_with_timestamps.py`). Do not edit `../tools/`.
4. ElevenLabs calls one at a time, with a 20–60s backoff on HTTP 429 (the key is shared).
5. Keep `ejemplo` chips on invented numbers; the mascot is a toy, never present it as a real person.
6. Verify the final mp4 (ffprobe, volumedetect, extracted frames), not only snapshots: fonts can differ between snapshot and render.
