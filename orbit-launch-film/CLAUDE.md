# Agent instructions · orbit-launch-film

Light "integration launch" film: cream bg, brand red pills on kinetic sans type, a clicked "+" that becomes a blue core with an orbit of icon bubbles, a feature wheel with tag pills, a red card shrinking into a tile grid, a ring of tiles around one word, a red blob behind the closing lines, and a two-shape logo merge. Voiced (reused VO) or music-only.

1. Read `PLAYBOOK.md` here fully (beat table, recipe, gotchas). Reference frames: `frames/`.
2. Copy `template/` to your project. Edit only `src/index.tpl.html` and `src/build.py`; `python3 src/build.py` regenerates `index.html` (word times + every `<audio>` tag).
3. Every cue is `t(wordIndex)` on the VO's word array: re-count indexes whenever the voice changes.
4. Icons are original 24×24 line paths in code. Never paste third-party logos, mascots or brand marks.
5. `npm run check` → 0 errors; `snapshot --at …` at 9+ beats and look at them before rendering.
6. Shared helpers: `../tools/fit_music.sh`, `../tools/music_rms.py`, `../tools/sfx_normalize.sh`. This format's own copy of the builder: `tools/build.py`.
Example: `../../x-batch/adishj/` (28.5s). Cost: $0 images, 0 ElevenLabs calls.
