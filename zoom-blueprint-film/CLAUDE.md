# Agent instructions: zoom-blueprint film

Narrated vertical film (1080x1920, Spanish) in which one unbroken camera zooms through nested chalk-line drawings on indigo, each drawing hiding the next inside a small red "door"; it ends with a pull-back through every layer and a film strip of live thumbnails, then the CTA.

1. Read `PLAYBOOK.md` in this folder fully (it explains the camera maths, the doors, and the `non-scaling-stroke` gotcha).
2. Copy `template/` to a new project folder. Everything is in `template/index.html`: word times `W`, `LINKS` (focus P, anchor C, ratio k), one block per drawing, the film strip and the CTA.
3. Audio is reused (no ElevenLabs): `assets/vo.mp3` = `chalk-quiz-funnel/vo.mp3`, `assets/music.mp3` = `x-batch/dzhng/assets/music.mp3` fitted with `../tools/fit_music.sh`. For a new VO transcribe locally with `npx --yes hyperframes@0.8.137 transcribe`.
4. `npx --yes hyperframes@0.8.137 check` (0 errors), snapshots at 10+ beats including mid-zoom times, look at them, fix. Render one at a time: `npx --yes hyperframes@0.8.137 render -o ../out.mp4 -w 2 --quiet`, then `../tools/audio_check.sh`.
5. New cursive words: `python3 tools/text_em.py template/assets/PinyonScript.ttf "palabra"` and add the value to `EM`.
Zero images, zero AI video. Keep every number labelled EJEMPLO until it is real.
