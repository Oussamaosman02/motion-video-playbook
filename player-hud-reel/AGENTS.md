# Agent instructions

Player-HUD reel with voice (`player-hud-reel/`, example `../../x-batch/nateherk/`). Read `PLAYBOOK.md` fully, then start from a copy of `template/` (index.html + assets; `data/` holds the word times, particle points, the pre-injection template and the prompts).
Make particle targets with `tools/glyph_points.py`. `tools/inject_cues.py` is the one-off builder kept as the SFX cue-list pattern; don't re-run it over a finished index.html. Shared helpers are in `../tools/` (fit_music.sh, cutout_grid.py, gen_image_ar.py, el_audio.sh).
Rules: everything original (no platform logos, play buttons or third-party UI); reuse a VO and a bed; `npx --yes hyperframes@0.8.137 check` must show 0 errors before rendering; look at snapshots of every shot.
