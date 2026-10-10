# Orbit launch film (`orbit-launch-film`) — format letter to be assigned by the coordinator (proposed: V)

A light, fast **"integration launch" film**: cream background, one brand red, one electric blue, and kinetic sans type where the key words land as **red pills**. A **"+" button** is clicked by a cursor, turns blue and sinks to become a **glowing core at the bottom of the frame**, with an **orbit of icon bubbles** around it and a rolling counter on top. Then a **feature wheel** (rows scroll through a highlighted centre line with an icon ring + tag pill), a **full-screen red card that shrinks into a tile grid**, a **ring of tiles around one big word**, a **soft red gradient blob** behind the closing line, and a **logo built from two shapes** that merge.

- **Reference:** https://x.com/_adishj/status/2102520354069729456 (26.3s, 16:9, music only; an app-integrations launch film made with Opus 5.5 in a motion tool). The original is full of third-party app logos: **we copy only the motion language** and draw our own line icons in code.
- **Our example:** `../../x-batch/adishj/` → `x-batch/adishj.mp4` (28.5s, 1080x1920, SaaS in House, Quiz Funnel script, reused Spanish VO).
- **Closest formats:** F1 `ui-launch-film/` (UI vocabulary), F6 `airy-launch/` (light palette), U `thermal-pixel-film/` (same reused VO + word-times approach). New here: the ticker of pills, the button→core→orbit transition, the feature wheel and the card→grid shrink.

## What makes it distinctive
1. **Pills, not captions.** Every sentence is plain sans (Archivo 500) with 1–2 words boxed in a red rounded pill that pops in with `back.out` + a −8° twist. Negative words get a **grey pill with a strike-through** ("landing").
2. **Right-anchored ticker.** Line 1 grows from the right: each item is an `inline-flex` box whose `max-width` animates 0 → est. width, so earlier words slide left on their own (no measuring). The row starts at scale 1.25 and pulls back.
3. **One object carries over the cut.** The "+" that ends the ticker is a global element: it flies to centre, the cursor clicks it (scale yoyo), it turns blue with a glow, then sinks and scales ×7 to become the hemisphere at the bottom of the orbit scene.
4. **Orbit:** 4 dashed concentric arcs around (540, 1900); bubbles (white or red, 112px) pop in staggered and the arcs rotate at different speeds (glyphs counter-rotate to stay upright); camera push-in 1→1.12; bubbles scatter outward on exit. Counter rolls 1→8 with a tick per number, red → ink, then shrinks to the top.
5. **Feature wheel:** 12 rows, 110px apart, right-aligned; the list `y` steps one row per cue word; opacity falls off 1 / .5 / .26 / .1 with blur on far rows; a ring (red outline) with the row's icon and a red **tag pill** swap at each step (`autoAlpha`, scaleX from the left).
6. **Card → grid:** a full-bleed red card ("Al final,") animates width/height/radius to a 560px tile while a grid of white icon tiles behind it zooms out 1.9 → 0.92.
7. **Ring around a word:** 16 small icon tiles on r=400, rotating; centre word swaps (−30% offer → countdown with a draining red arc).
8. **Blob + stack:** a radial-gradient red blob (no SVG filter) drifts while lines stack with pills; older lines dim.
9. **Logo merge:** rounded square + circle slide together, the circle disappears into the square, the square becomes the brand mark ("S" on red), slides left and the wordmark types in letter by letter; CTA "Comenta [QUIZ]" under it.

## Beat table (our 28.5s film; VO = `sih-quiz-film/assets/vo.mp3` at +0.3s)
| t (s) | VO | Visual | Technique |
|---|---|---|---|
| 0–1.0 | "Tu próximo" | "Tu próximo" tracking-in, dark brown | per-glyph `x` spread → 0 (letterSpacing is banned by `check`) |
| 1.0–4.6 | "cliente no llega por la landing, llega por un quiz" | ticker: [cliente] pill + user chip, [landing] grey struck, [quiz] pill, red + | right-anchored row, `max-width` growth |
| 4.1–4.9 | "Cinco" | + to centre, cursor click, turns blue | global `#btn`, cursor SVG |
| 4.6–8.7 | "…preguntas para saber quién es, qué quiere y qué le duele" | blue core + orbit, "1→8 preguntas", 3 red question pills | polar layout, rotating hosts |
| 8.7–13.7 | "Entre pregunta y pregunta, casos reales y datos… Esto tiene sentido." | wheel: Pregunta 1/2, Caso real, Dato, Consejo, ✓ | `STEPS` = [row, word index] |
| 13.7–16.4 | "Al final, un resultado hecho para él" | red card → "Tu resultado · Founder SaaS" tile in a grid | card size tween + grid zoom (music drop on the cut) |
| 16.4–19.3 | "una oferta a su medida, con un contador para canjearla" | ring of tiles, −30% → 15:00 countdown + red arc | `textContent` sets per 0.5s |
| 19.3–23.6 | "No solo captas el lead, lo segmentas, lo educas y lo llevas a la compra" | blob, "No solo" → 4 stacked lines with pills | |
| 23.6–28.5 | "Comenta quiz y te enseño cómo montarlo" | shapes merge → S mark + "SaaS in House", "Comenta [QUIZ]" | letter-by-letter wordmark |

## Recipe
1. Copy `template/` to your project. Assets: `vo.mp3`, `music.mp3`, SFX (`whoosh pop key tick impact boom type`), `Archivo.ttf`.
2. **Voice:** reuse a base-script VO (see `x-batch/AUDIO-REUSE.md`); paste its word array into `WORDS` in `src/build.py` *and* `__WORDS__` is filled from it automatically. Every cue in the template is `t(wordIndex)` — **re-check the indexes** when the voice changes (count words; this build first had the wheel steps one word early, which made two tag pills overlap and `check` flagged it).
3. **Music:** `bash playbook/tools/fit_music.sh <bed> assets/music.mp3 28.5 <offset>-end` with the offset chosen so the bed's drop lands on the red-card cut (`python3 playbook/tools/music_rms.py` prints the drop). Volume 0.2 under VO.
4. `python3 src/build.py` → writes `index.html` (audio tags + word times). Edit only `src/index.tpl.html` and `src/build.py`.
5. `npm run check` (0 errors), then `npx --yes hyperframes@0.8.137 snapshot --at 1.2,4.8,7.9,12.9,14,16,19,23.5,28 --describe false`, look, fix.
6. Render: `npx --yes hyperframes@0.8.137 render -o out.mp4 -w 2 --quiet`.

Music-only variant: keep the same scenes, drop the VO, put the beats on the bed's bar lines (the reference is music-only).

## Cost
0 images ($0.00), 0 ElevenLabs calls (VO, music and SFX all reused), no AI video. Everything is HTML/CSS/SVG + GSAP. Build ≈ 1 h.

## Gotchas
- **Never copy the reference's app logos.** The icons here are 21 hand-written 24×24 line paths (`P` in the template). The brand mark is SaaS in House's own favicon ("S" on red).
- **Icon picking stride must be coprime with the icon count** (21): `NAMES[(i*7+3)%21]` gave only 3 distinct icons; use 4 or 5.
- `letterSpacing`/`width` tweens: `check` errors on `letterSpacing`; animate per-glyph `x` instead. The ticker's `max-width` tween passes (it reflows but the row is right-anchored, so it reads as a slide).
- Keep the top of the outer orbit arcs empty (the template skips angles −128°…−52° on rings 3–4) or bubbles sit behind the question pills.
- Use `autoAlpha` (not `opacity`) for swapped tag pills: `check` counts opacity-0 boxes as overlapping text.
- Wheel steps closer than ~0.4 s apart: shorten the tag pop (0.3 s) or the previous tag's hide is overwritten by its own `fromTo`.
- Wordmark grey letters need ≥ 3:1 contrast on cream (`#8a847b` passes; `#9b958c` fails).

## Placeholders (replace before posting)
"Founder SaaS · B2B · 2–10 personas" result tile, **−30% offer** and the **15:00 countdown** (both labelled EJEMPLO), wheel row copy ("Un caso como el tuyo", "Un dato que sorprende") — no invented statistics.
