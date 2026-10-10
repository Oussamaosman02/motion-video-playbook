# Neon sizzle reel: agent notes

Format: dark starfield + ONE neon accent, a procedural hero per section (polyhedron, particle burst, glass emblem, orbiting cards, galaxy + lasers, grid floor + wireframe UI, tile wall, streaks, wireframe funnel, particle stream → wordmark), `01 Label` tag + two-line headline (white / neon), music only. Read `PLAYBOOK.md` first.

- Start from `template/` (HyperFrames 0.8.137). Scene starts live in `B` at the top of the script; every canvas motion is in `drawFX(T)` and is a pure function of `T` (seek-safe). Never store state between frames.
- Put `B.s7` (black breath) on the music's silent gap and `B.s8` on the drop (`playbook/tools/music_rms.py`).
- Emblem: generate on **black**, convert with `tools/glow_to_alpha.py`; no `mix-blend-mode`.
- Keep `data-layout-ignore` on `#fx`, `#s4-cards`, `#s9-wall`, `#s8-panels`.
- `npx --yes hyperframes@0.8.137 check` must be 0 errors; snapshot 12+ beats and look at them.
- Don't render in parallel with other renders (RAM). Check the ending with `playbook/tools/audio_check.sh`.
- Numbers are example data; keep the EJEMPLO labels unless real figures are provided.
