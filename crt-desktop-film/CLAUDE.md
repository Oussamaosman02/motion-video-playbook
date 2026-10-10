# Agent instructions: CRT desktop film

A dark, music-only retro-computer launch film shot "inside" a CRT: phosphor UI with scanlines and a rounded bezel, a pixel menu bar, a big pixel cursor that right-clicks / installs / picks answers, paper dialog windows that snap open like a CRT line, an NLE-style editor (BIN / PREVIEW / TIMELINE) driven by an `@SaaSinHouse` agent prompt, one hero object (chrome funnel) re-rendered in 8 styles with scan-wipes plus a 4x4 variant wall, offer windows with a countdown, and an end card on a photo of a real CRT on a desk. Built with HyperFrames (HTML + GSAP). **2 Gemini images**, no voice, no AI video.

1. Read `PLAYBOOK.md` in this folder fully before doing anything (closest older formats: `../terminal-teaser/`, `../hero-object-film/`).
2. Start from a copy of `template/` (`cp -R playbook/crt-desktop-film/template my-crt`). `template/script.txt` maps every beat to the on-screen copy and the music cues.
3. Images: one symmetric hero object on pure black (1:1) and one CRT-on-desk photo with a flat-colour screen (9:16), via `../tools/gen_image_ar.py`. Then `python3 tools/style_variants.py hero.png template/assets 1024` makes the 9 render styles + `grid.png`. Re-measure the CRT screen rectangle and update `#scr` / `#photo`.
4. Music: reuse a bed with a clear drop (or `../tools/el_audio.sh`, sequential, 429 backoff; the key is shared). Put the drop on "Pero no hagas solo preguntas", the break on "la parte importante".
5. Edit copy in the `<section>`s and timings under each `/* ==== Sn ==== */` block. Open windows with `winOpen()` (a `tl.set` + `to`), never a bare `fromTo`, or later windows show as thin bars early.
6. `npm run check` (only the intentional contrast warnings on dimmed background windows may remain), draft render, look at 8+ frames, final render. QA the **final mp4**: ffprobe 1080x1920, volumedetect, frames you actually look at.
7. Numbers with `ejemplo` chips (2%→6%, –30%, 14:59, the "tu situación" card) are illustrative. Replace them before posting. No people appear in this format.

Example output: `../../x-batch/trymirage.mp4` (45.5s). Reference: https://x.com/trymirage/status/2107504042205139269
