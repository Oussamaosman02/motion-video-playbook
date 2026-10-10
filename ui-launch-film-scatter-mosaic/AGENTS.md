# Agent instructions: UI launch film, scatter variant, mosaic look (voice)

This folder is a **variant of `../ui-launch-film-scatter/`**, which is a variant of `../ui-launch-film/` (F1). Read those two `PLAYBOOK.md` files first, then `PLAYBOOK.md` here, which documents only the differences: photoreal product cut-outs on grey grid squares, pixel-mosaic tile transitions, a code-made halftone sky with a glass "incoming" pill, a warm circle → orb, frosted transcript bubbles over a blurred gradient, gradient agent cards and a wordmark rising over a glowing horizon.

- Start from a copy of `template/` (HyperFrames 0.8.137). **Edit `index.tpl`, never `index.html`**: run `python3 <this folder>/tools/build.py` in the project to regenerate `index.html` (scene times come from `assets/words.json`), then `npm run check` and `npx --yes hyperframes@0.8.137 render -o out.mp4 .`.
- Folder tools: `tools/build.py` (word-time templating), `tools/make_plates.py` (halftone/paper/blur backgrounds, free), `tools/cut_cells.py` (grid-split magenta sheets with gutters + strong despill).
- Shared scripts live in `../tools/` (`gen_image_ar.py`, `tts_with_timestamps.py`, `el_audio.sh`). Do not copy or edit them.
- ElevenLabs key is shared: one call at a time, back off on 429. If credits are out, reuse an existing base-script VO + words.json (same word indices).
- No AI video. Images only via treg Gemini (this format: 2 object sheets, ~$0.06).
- Keep "EJEMPLO" tags on every invented number; never present generated people as real customers.
- Example output: `../../x-batch/elevenlabs.mp4`.
