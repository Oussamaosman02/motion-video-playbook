# minchoi-a: render (coordinator only, one render at a time)

From this folder (`x-batch/minchoi-a/`):

```sh
npx --yes hyperframes@0.8.137 render -o ../minchoi-a.mp4 -w 2 --quiet
bash ../../playbook/tools/audio_check.sh ../minchoi-a.mp4
```

- Expected: 1080x1920, **31.5 s**, 30 fps. `npx --yes hyperframes@0.8.137 check` = 0 errors (3 lint warnings: file size / nested sections, intentional).
- Audio is fully in the composition (no premix step): `assets/vo.mp3` (Sara, reused from `chalk-quiz-funnel/vo.mp3`) at 0.4 s; `assets/music_mix.mp3` = sih-trace-film bed fitted with `fit_music.sh` (source 0.7–35 s, so its drop lands on the black hole at ~17 s) and a volume lift to 0.54 after the VO ends (27.3 s). Opening: impact + whoosh at 0 s. Ending: chimes at 27.7 s and 30.2 s over the loud part of the bed (fades over the last 1.8 s).
- The canvas engine is heavy-ish (grid + 7.7k-vertex sculpt in 10.8–14.2 s). If the render is slow there, `-w 1` is fine.

## Timestamps to check in the mp4
| t (s) | Should show |
|---|---|
| 1.0 | Flat dune grid, "¿vendes un SaaS?" being written along a red ridge with a spark; white dots streaming in; caption bottom |
| 2.9 | Red box on the ground with "LA MISMA LANDING" lying flat inside, dots piled in it |
| 4.15 | Big red standing ERROR with glitch slices, "conversión 0,8 % · ejemplo" |
| 6.3 | Grid sunk into a swirled gravity well, "QUIZ" (far rim) and red "FUNNEL" (near rim) glued on the surface |
| 9.95 | Topo rings P1–P8 lit red, spark spiralling, "¿quién es?" and "¿qué necesita?" on the funnel, "5–8 PREGUNTAS" standing behind |
| 13.4 | Hatched sculpt rising from the well with 4 red HUD callouts: CASO REAL / DATO / RESULTADO / CONSEJO (all numbers "ejemplo"), "CARDS" headline |
| 16.3 | Top-down oscilloscope: clean red wave, "tu resultado personalizado" riding it, RESULTADO box |
| 18.3 | Black hole with accretion streaks, "OFERTA" / "A MEDIDA" ring type, "04" |
| 20.3 | Countdown ring "QUEDAN 00:14:58 · CANJÉALA YA" around the hole + big 14:58 (red after 21.34) |
| 23.4 | Tunnel, "LA MISMA LANDING" on the floor struck through in red (breaks into dots at ~24) |
| 26.95 | Red "VENDES" orbiting the hole (SEGMENTAS faded behind) |
| 30.8 | SaaS IN House lockup, red pill "COMENTA «QUIZ»", "y te enseño cómo montarlo" — audible chime, not silent |
