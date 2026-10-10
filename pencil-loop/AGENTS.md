# Pencil loop format: agent instructions

You are making a **pencil-loop** video: a wordless coloured-pencil storybook in which one small character travels through one hand-drawn world, the camera follows it, and the last frame equals the first frame, so it loops. The script appears as handwritten paper slips over soft music.

1. Read `PLAYBOOK.md` in this folder (the recipe, helpers and gotchas).
2. Start from `template/` (a HyperFrames 0.8.137 project). Copy it; never edit it in place.
3. Rules:
   - No AI video. Only Gemini images via treg: plates in the pencil style with the reference image, plus one magenta sprite sheet cut with `../tools/cutout_grid.py`.
   - Make ElevenLabs calls one at a time; on HTTP 429, wait 20–60s and retry.
   - Take path coordinates from a grid overlay of each plate.
   - Keep cards and labels in screen space (`note("ui", …)`).
   - End on the opening view, with all text faded out.
4. Before you finish: `npm run check` (0 errors) → snapshots → render → crf-19 re-encode → ffprobe 1080x1920 + volumedetect + look at 6+ frames from the final mp4, first and last frame included.
