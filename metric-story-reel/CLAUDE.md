# Agent instructions: metric-story reel

A dark, fast SaaS launch reel where one product object travels through every beat. A long URL collapses into a pill, the pill drives an odometer over a planet, then come a 3D tabbed dashboard card with toasts and a network around the brand mark. A burst of one-word colour-block cards follows, and a brand-colour iris lands on the logo end card. It is voiced (reused VO) with captions, uses a reused music bed, and needs **zero generated images** and no AI video. Example: `../../x-batch/steventey.mp4` (35.5 s, Spanish, Quiz Funnel).

1. Read `PLAYBOOK.md` in this folder fully (beat map, recipe, gotchas).
2. Start from a copy of `template/` (HyperFrames 0.8.137, single `index.html`, assets included: VO, spliced bed, pad, SFX, fonts).
3. Swap the voice with `tools/inject_words.py <words.json> index.html`, then fix the word indexes listed in the recipe. Check transcript times against `silencedetect` (whisper was ~0.4 s early on this take).
4. Every cue is `t(wordIndex)`. Scene windows are in the `SC` array, and the card words are in the `<section class="card">` blocks.
5. `npx --yes hyperframes@0.8.137 check` (0 errors) → `snapshot --at …` at 10+ beats → look at them → fix. Render one film at a time with `-w 2`.
6. Keep invented numbers labelled `EJEMPLO`. No third-party logos, faces or marks: the avatars are abstract silhouettes.
Shared helpers: `../tools/` (`fit_music.sh`, `sfx_normalize.sh`, `el_audio.sh`, `music_rms.py`). Do not edit them from a format folder.
