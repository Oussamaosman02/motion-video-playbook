# sim-timeline-film · agent notes

Format: **Sim-timeline film (voice)**. A light, dotted canvas with gradient "operation pills" (badge + mono label + red cap), branching spines, a futures micro-grid, a 3D pill floor, green check chips and a dark terminal CTA. Motion language from @workersio's launch film; content is our Quiz Funnel script. Read `PLAYBOOK.md` first.

- Template: `template/` (HyperFrames 0.8.137). Edit `template/tools/src.html.tpl` + the `SFX` list in `template/tools/build.py`, then run `python3 tools/build.py` from `template/` to regenerate `index.html`. Never put `src.html` in the project root.
- Every cue is a VO word index (`t(i)`). New voice → replace `assets/vo.mp3` + `assets/words.json`, re-check the indexes.
- Reuse audio (no TTS): VO = `playbook/whiteboard-ad/template/vo.mp3` (Bruno Torres); bed = liu8in piano refit with `../tools/fit_music.sh`; SFX from the library.
- Seek-safety: no `className`/`textContent` sets in the timeline; use fading overlays and `onUpdate` proxies; canvas hashes must be unsigned (`>>> 0`).
- QA: `npm run check` → `snapshot --at …` → look at the frames → render `-w 2`. Reference frames: `reference-frame-*.png`. Original contact sheet (logo row cropped): `original-contact-sheet.jpg`.
- `tools/build.py` is a copy of the build script (word times + SFX → index.html).
