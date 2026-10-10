# Agent instructions: form dossier film (`form-dossier-film/`)

Music-only, zero-image vertical film told as a stack of official paperwork (forms, stamps, diagram plates, a crossed-out appendix, a cage-bar wipe into a dark terminal page, a milestone schedule with an odometer). Cream paper, black condensed type, one red ink.

1. Read `PLAYBOOK.md` in this folder fully (beats, recipe, gotchas, how it differs from `../kinetic-hud-film/`).
2. Copy `template/` into your project folder. Edit `T`, the scene sections and their cue blocks in `index.html`; every cue is an absolute time (no VO).
3. Reuse a music bed not used elsewhere in the batch and fit it with `tools/fit_bed.sh` (wraps `../tools/fit_music.sh`). No TTS. ElevenLabs only for SFX the format really needs, sequential, via `../tools/el_audio.sh`.
4. `npm run check` must report 0 errors; snapshot every stamp and scene change and look at the PNGs.
5. Render one project at a time: `npx --yes hyperframes@0.8.137 render -o ../<slug>.mp4 -w 2 --quiet`, then `../tools/audio_check.sh`.
6. Illustrative numbers (probability table, −30%) are labelled `ejemplo`; replace them with real ones before posting. Never copy text, characters or logos from a reference; copy only its techniques.
