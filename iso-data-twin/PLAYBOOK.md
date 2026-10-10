# Iso data-twin film (`iso-data-twin/`)

A calm, narrated **isometric data-cartography film**. It is built like a product tour of an "urban digital twin": navy and paper scenes alternate under **octagon iris wipes**, and every idea becomes an isometric object. A plate of map data, exploded layers, floating data tiles, a hex-block city recoloured by data, and a detail card with a traceability tree. 100% code (SVG + GSAP), **zero images**.

- **Reference:** https://x.com/humbertblanco/status/2107872497345630406. "Xamfrà", a 70s Catalan beta teaser (1920x1080, ElevenLabs narration + soft bed) for a digital twin of 36 municipalities. The author says it was made with Opus 5.5, "a good design system" and ElevenLabs, for about 50€ of tokens. Their contact sheet is in `frames/ref-contact-sheet.jpg`.
- **Our film:** `x-batch/humbertblanco/` (1080x1920, 58.5s, Spanish, Quiz Funnel base script, SaaS in House end card). Reference frames: `frames/01…05`.

## What makes it distinctive
1. **Isometric everything.** A single projection `P(x,y,z)` and one `prism()` extruder (any polygon → shaded visible sides + top) build plates, layers, tiles, 3D bars and hex blocks. It feels like a data tool, not a motion template.
2. **Two-tone rhythm.** Dark navy scenes (with a faint dot pattern) alternate with warm paper scenes (with a faint grid), always through an **octagon iris** that grows from the centre and covers the frame exactly at the cut. Gold is the only accent; red is kept for "problem" and the countdown.
3. **Typewriter headlines, top-left.** A small grey lead-in line, then bold lines typed per character with a block cursor. The previous list lines **dim** as the next one types (the ref's "Repartida en / sistemes, / formats / i organismes").
4. **Data changes colour, not the camera.** The hex city recolours in waves (stagger by x+y). Two "filter chips" toggle gold, and each toggle is followed by a choropleth wave. One block is then lifted and pinned.
5. **Product-UI epilogue.** A white detail card with a big counter and bars, then a **traceability tree** (spine plus elbow connectors) whose nodes slide in on their words.
6. **Close on a bullet list** with a gold active bullet and underline, previous bullets dimmed, while the map below fills gold. Then a centred logo card.

## Beat table (our 58.5s cut; word index → `t(i)`)
| # | t | VO | Visual | Technique |
|---|---|---|---|---|
| 1 | 0–4.5 | ¿Quieres vender… misma landing? | 230 streaks rain onto a navy iso plate, VISITAS counts to 2.151, then all the dots converge into one gold `/landing` bar | SVG `<line>` attr tweens (y1/y2 fall, then x/y converge); bar `scaleY` from its base |
| 2 | 4.5–5.7 | Haz esto. | big "Haz esto.", scene dims, white octagon iris | `iris()` |
| 3 | 5.7–10.3 | En lugar de pedir una demo… crea un Quiz Funnel | "Pedir una demo" pill struck in red and dropped; octagon mark + gold dot + typed wordmark + gold rule | logo build like the ref's lock-up (original mark) |
| 4 | 10.3–18.3 | 5 y 8 preguntas… persona / conseguir / problema | "5–8 preguntas" counter; 4 exploded octagon layers (Lead, Perfil dots, Objetivo routes, Problema heat) drop in with a legend | `prism()` slabs + textures projected on their top faces |
| 5 | 18.3–20.2 | Pero no hagas solo preguntas | layers collapse into a thin stack and recentre; dark iris | group `y` tweens |
| 6 | 20.2–29.9 | cards con casos, datos, resultados, consejos… "vale, esto tiene sentido" | 12 navy tiles rise; 4 light up gold with mono tags and content (avatar, 3D bars, stripe, checklist); gold line links them, checks pop; gold quote | ref's floating "systems" tiles |
| 7 | 29.9–34.3 | según sus respuestas… resultado personalizado | ~100 hex blocks rise, 2 recolour waves (gold→red, then green→gold), all dim but one gold block lifted with a LEAD #257 pin; result card counts to 87% | `recolor()` waves |
| 8 | 34.3–36.1 | Y aquí viene la parte importante | gold frame, dark octagon, white ring and dot; the dot grows into the next paper scene | ref's gold/dark octagon transition |
| 9 | 36.1–48.0 | últimas cards → producto, encaja, oferta, contador | gold hex + "Tu producto encaja 87%" card with bars; tree: Por qué encaja (3 ticks), Oferta 99€→69€, Tiempo limitado 15:00 counting in real seconds | HTML cards + SVG spine/elbows |
| 10 | 48.0–54.6 | captas, segmentas, educas, compra | bullet list; hex plate tints into 3 segments, little cards pop up, then everything fills gold from the centre | stagger by distance |
| 11 | 54.6–58.5 | (music) | SaaS in House mark, "Comenta QUIZ" pill, "y te enseño cómo montarlo" | end card |

## Recipe
1. Copy `template/` to `x-batch/<slug>/`. `index.html` is **generated**: edit `work/index.src.html` (scenes + timeline) and `work/build.py` (VO offset, END, SFX cue list by word index), then `python3 work/build.py`.
2. VO: put `assets/vo.mp3` and `work/words.json` (`[[word,start,end],…]`) in place. Reused takes already have word times (`ui-launch-film/template/assets/words.json`); otherwise run `npx --yes hyperframes@0.8.137 transcribe` locally and convert. Scene starts are word indices in the `S` object; re-check them if the wording changes.
3. Music: `playbook/tools/fit_music.sh` (this film spliced `sih-fila-film` 0–42 + 30.5–49.8 because the bed dies at 50s). Then bake the duck/raise into one file with ffmpeg `volume='if(lt(t,54.2),0.22,…)':eval=frame` (HyperFrames audio has no volume automation).
4. `npx --yes hyperframes@0.8.137 check` → 0 errors, then `snapshot --at …` at every beat and LOOK.
5. Render from the project folder: `npx --yes hyperframes@0.8.137 render -o ../<slug>.mp4 -w 2 --quiet`.

Helpers (also in `tools/iso_helpers.js`): `P`, `prism`, `recolor`, `isoPoly`, `isoLine`, `polyN`, `iris`, `typeLine`, `dim`, `counter`. `tools/build.py` is the generator.

## Cost
Images $0 (none). ElevenLabs: 3 SFX calls (`datarain`, `iris`, `blips`). VO and music reused. No AI video.

## Gotchas
- **GSAP `svgOrigin` must be in BOTH the from- and to-vars of `fromTo`.** With it only in the to-vars, the first render used a different origin. The logo octagon and dot drifted off-centre, the S8 octagon never appeared and the landing bar was invisible. Fixed by repeating `svgOrigin` in the from-vars.
- Typewriter: per-character `<span>`s toggled with `tl.set(display)`. The cursor then sits at the real end of the typed text, and seeking backwards reverts cleanly.
- Painter's order: sort prisms (and side faces) by `x+y` ascending before appending. To lift one block above its neighbours, re-append its `<g>` to the end of the SVG.
- Iso tags on the dark tiles overlap if wider than ~270px at s=74. Keep the sub-labels short.
- Light-scene greys must be ≥ #686e7d on #f3f1ec, or `check` flags contrast.
- Music beds that fade early (`sih-fila-film` dies at 50s): check with `music_rms.py` before fitting.
- The countdown runs in real seconds from "contador" (it only reaches 14:58 before the cut). Shorten the format by tying it to a longer beat, or accept it as the other films do.

## Placeholders (replace before posting)
87% encaje, Lead #257, "SaaS B2B", bars 92/85/81, 99€→69€ −30% (labelled EJEMPLO), 15:00 countdown, VISITAS 2.151. The CTA deliverable for "Comenta QUIZ" must exist.
