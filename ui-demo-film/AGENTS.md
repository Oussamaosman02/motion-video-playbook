# AGENTS: ui-demo-film

You are reproducing the **UI demo film** format (phone walkthrough + cursor + chapter captions, music only). Read `PLAYBOOK.md` in this folder first.

- Start from `template/` (HyperFrames 0.8.137). Never edit `../tools/` or `../PLAYBOOK.md`; format-specific helpers live in `tools/` here (`el_post.sh` = ElevenLabs POST with 429 backoff).
- Code builds everything: UI, phones, cursor, grid. The only generated images are optional avatars (Gemini via treg, magenta background → `cutout_grid.py`). No AI video.
- ElevenLabs calls run one at a time; the key is shared.
- Loop: `npm run check` (0 errors) → `snapshot` → look → `render` → ffprobe + volumedetect + look at 6+ frames from the mp4.
- Cursor/click coordinates are canvas pixels; phone screen origin = (256, 576).
- Keep illustrative numbers labelled "ejemplo".
