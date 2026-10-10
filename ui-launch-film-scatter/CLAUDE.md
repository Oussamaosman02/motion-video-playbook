# Agent instructions: UI launch film, scatter variant (F1 variant, voice)

This folder is a **variant of `../ui-launch-film/`** (F1). Read `../ui-launch-film/PLAYBOOK.md` first (recipe, `w(i)` cues, helpers, rules), then `PLAYBOOK.md` here, which documents only the differences: scatter words placed one by one on a white canvas with floating UI chips, slanted sky sweeps into tilted 3D glass screens, the circle → glass orb statement device, a typed iPhone chat, and a dark glow act with price-style cards and a glowing wordmark.

- Start from a copy of `template/` (HyperFrames 0.8.137 project; `npm run check`, then `npx --yes hyperframes@0.8.137 render -f 30 -o out.mp4 .`).
- Shared scripts live in `../tools/` (`tts_with_timestamps.py`, `embed_words.py`, `el_audio.sh`, `gen_image_ar.py`, `cutout_grid.py`). Do not copy or edit them.
- ElevenLabs key is shared: one call at a time, back off on 429.
- No AI video. Images only via treg Gemini (this format needs 1 image, ~$0.03).
- Keep "EJEMPLO" tags on every invented number; never present generated people as real customers.
- Example output: `../../x-batch/notdwd.mp4`.
