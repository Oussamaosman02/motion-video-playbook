# Agent instructions: Glow signal film

A dark, music-only product teaser: word-by-word headline, a glowing dot whose line bursts into lead nodes, a live feed panel with a camera push, an interleaved question/value-card stack, Pendiente → Cumplido gate panels with striped bars, and a wordmark end card. Built with HyperFrames (HTML + SVG + GSAP), 1 Gemini image (6 avatars) and ElevenLabs music/SFX. No AI video, no voice.

1. Read `PLAYBOOK.md` in this folder fully before doing anything.
2. Start from a copy of `template/` (`cp -R playbook/glow-signal-film/template my-film`).
3. Make ElevenLabs calls one at a time with `tools/el_post.sh`, which retries HTTP 429 with backoff. Generate images only through `playbook/tools/gen_image.py` (Gemini via treg), on flat magenta, then run `cutout_grid.py`.
4. Edit copy and data in `index.html`: `words(...)` tokens, captions `#c*`, `NODES`, `LEADS`, `#stack`, `GATES`, end card.
5. Run `npm run check` (0 errors), take snapshots, and render. Then QA the **final mp4**: ffprobe 1080x1920, volumedetect, and 6+ frames you actually look at.
6. Numbers labelled "ejemplo" are illustrative. Replace them before posting.

Example output: `../../x-batch/trenchers.mp4` (38s). Reference: https://x.com/TrenchersAI/status/2107010967393673449
