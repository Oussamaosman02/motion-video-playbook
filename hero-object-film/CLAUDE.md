# Agent instructions: hero-object film (voice)

Format: one white 3D object (the idea) + calm narrator + an isometric cube field on a dark navy/maroon glow, product-film HUD, bottom-left word-by-word captions with underlined keywords, one light blueprint interlude. Reference: @boxd_sh "boxd in 60 seconds". Example: `../../x-batch/boxd.mp4`.

1. Read `PLAYBOOK.md` in this folder fully (anatomy, beat map, recipe, gotchas). The general rules (HyperFrames, voices, costs) are in `../PLAYBOOK.md`.
2. Start from a copy of `template/` (HyperFrames 0.8.137). Shared scripts: `../tools/` (`el_audio.sh`, `gen_image_ar.py`, `embed_words.py`); TTS with 429 backoff: `../founder-depth-type/tools/tts_retry.py`; this format's helper: `tools/key_neutral.py`.
3. ElevenLabs key is shared: one call at a time. Images only via treg Gemini (this format needs 1, ~$0.03). No AI video.
4. After a new voice: re-embed words, recompute `B`, `END`, section `data-start/duration` and audio durations; check the music still covers the ending.
5. QA: `npm run check` (0 errors), snapshots, render, ffprobe 1080×1920, volumedetect on the whole file AND on the last 3s, look at 6+ frames of the final mp4.
6. Keep `EJEMPLO` on invented numbers; generated objects only, no people.
