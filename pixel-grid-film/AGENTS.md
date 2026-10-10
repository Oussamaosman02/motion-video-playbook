# Agent instructions

Pixel-grid film (voice): a Swiss-minimal launch film on an off-white grid with one red accent. Pixel squares assemble into UI, with mosaic wipes, stacked dark cards, node lines, a giant countdown and a pixel staircase. It uses zero images; everything is code.
Read `PLAYBOOK.md` fully, then start from a copy of `template/` (HyperFrames 0.8.137, 1080x1920).
- Word times: `npx --yes hyperframes@0.8.137 transcribe vo.mp3 -l es -m small` → `work/words.json`. Then run `python3 work/inject.py`, which injects the words and the SFX cues into `index.html`.
- Helpers in `index.html`: `sq()`, `glyph(map)`, `mosaic(cut, palette)`, `popIn/fadeUp/draw`, a seeded `rnd()`. Motion is transforms only (never left/top).
- Shared tools are in `../tools/` (`fit_music.sh`, `sfx_normalize.sh`, `el_audio.sh`, `audio_check.sh`). Reuse the VO and music; ElevenLabs is only for a few SFX, one call at a time.
- Check: `npx --yes hyperframes@0.8.137 check` must report 0 errors. Then take snapshots at 10+ beats, look at them and fix what you see. Render with `-w 2`, one render at a time on this machine.
