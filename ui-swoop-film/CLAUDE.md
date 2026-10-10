# Agent instructions · UI swoop film (`ui-swoop-film`)

A fast, light SaaS promo reel made only of UI micro-interactions: a URL card, a camera push into a button, tilted 3D cards, outline type columns, a pill-grid pan, blob masks with gold tags, a "word [phone] word" sandwich, floating cards, a button that turns into a "done" pill, and toggles. Every cut is a motion-blur whip. HTML + GSAP only: 0 images, 0 ElevenLabs calls, no AI video.

1. Read `PLAYBOOK.md` in this folder fully (beat table, recipe, gotchas). The reference frames are in `reference/`.
2. Copy `template/` to your project folder (`x-batch/<slug>/`). It is a working 28 s project: reused VO `assets/vo.mp3` (word array `const W` in `index.html`), fitted bed `assets/music.mp3`, library SFX.
3. Audio first. To swap the voice, paste the new word array into `W` and re-check the cues with `python3 -I tools/words_from_index.py index.html` (prints `index:word@time`). Every cue is `t(i)`.
4. Edit the scene windows `SC`, the caption ranges `CAP`/`capEnd` and the scene copy. Never tween width/left/top, only transforms.
5. Run `npm run check` (0 errors), then `npx --yes hyperframes@0.8.137 snapshot --at … --describe false`, look at every scene and fix.
6. Render: `npx --yes hyperframes@0.8.137 render -o ../<slug>.mp4 -w 2 --quiet` (one render at a time on this Mac).

Shared helpers are in `../tools/` (`fit_music.sh`, `sfx_normalize.sh`, `audio_check.sh`, `music_rms.py`). Do not edit them from a format folder.
Everything must be original: no third-party logos (the toggle list uses numbered icons, not platform logos) and no real people.
