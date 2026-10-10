# Agent instructions: iso data-twin film

Narrated isometric data-cartography film (navy/paper scenes, octagon iris wipes, plates, exploded layers, iso tiles, a recoloured hex city, a traceability tree), 1080x1920, zero images.
Read `PLAYBOOK.md` in this folder fully before doing anything. The example is `../../x-batch/humbertblanco/`.

1. Copy `template/` to your project folder. Never edit `template/` in place.
2. `index.html` is generated: edit `work/index.src.html` and `work/build.py`, then run `python3 work/build.py`.
3. Audio: reuse a VO with word times (`work/words.json`), fit and bake the music (see the recipe). ElevenLabs only for SFX, sequential, via `../tools/el_audio.sh`.
4. `npx --yes hyperframes@0.8.137 check` (0 errors), snapshots at every beat, look, fix. Then render.
5. Remember: `svgOrigin` goes in BOTH the from- and to-vars of every `fromTo`.
Reusable helpers: `tools/iso_helpers.js` (projection, prism extruder, recolour, octagon iris, typewriter) and `tools/build.py`.
