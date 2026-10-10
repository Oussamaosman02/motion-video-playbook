# Format · Kinetic launch trailer (`kinetic-launch-trailer`)

Source: https://x.com/javiiarchive/status/2107474804496351557 ("one shotted this launch video in 1 prompt"). The original is a 32.5 s 16:9 product trailer for a Claude Code MCP, made in one prompt. It's music-only apart from one sampled line at 20 s. See `original-contact-sheet.jpg` (one frame every 0.5 s).
Our version: `x-batch/javiiarchive/` (1080x1920, 28 s, Spanish, narrated Quiz Funnel script).

## What makes it distinctive
- **Light-grey canvas (#f2f2f4), huge heavy sans, two accents.** The original uses purple + lime. We use brand red #e8382d + highlighter yellow #f7d33c, with ink #131316.
- **The film opens with a 3D "puck" that stretches into a prompt pill** and types the first words (dark pill, hard 10 px drop shadow, red caret).
- **Word-by-word kinetic type.** Each word pops from a blur on its own beat. One accent word per line: red text, a yellow marker swipe, or a red strike/scribble.
- **Floating chips burst out of the centre** (dark, white, red, yellow pills with small dots), slightly rotated and drifting.
- **Hard-cut card montage with a dark label pill above each card**, e.g. "Pregunta 2 de 8", "Caso real", "Dato", "Consejo", "Oferta para ti". Cards pop in with back.out.
- **A product UI moment.** In the original it's an editor timeline; ours is a browser window with a result plus a funnel timeline whose playhead sweeps the tracks.
- **A full-bleed colour slab.** One red full screen ("una oferta a su medida.") and one red diagonal slab wipe ("a la compra.").
- **An original mascot as the brand mark.** It's a red quiz bubble with two eyes that blink and look around; it replaces the original's eyes logo. Its CTA is a prompt pill: "› comenta QUIZ" with a red send button.

## Beat table (film clock; VO starts at 0.3 s; `t(i)` = word i start + 0.3)
| t | VO | what you see | technique |
|---|---|---|---|
| 0–1.4 | tu próximo cliente | puck → pill, typed text, caret blinks | caps translate + middle scaleX (no width tweens), per-char `tl.set` |
| 1.4–2.9 | no llega por la landing | pill lifts and shrinks; big 2-line type; red strike, "landing." goes grey | `words()`, SVG path dashoffset |
| 2.9–4.5 | llega por un quiz | 7 chips burst from centre + drift; mascot pops; "quiz." red | seeded rnd drift, `mascot()`, `look()`, `blinkM()` |
| 4.5–6.0 | 5 a 8 preguntas para saber | label pill, giant "5 a 8", progress bar 5/8 → 8/8 | scaleX bar |
| 6.0–8.7 | quién es / qué quiere / qué le duele | 3 stacked questions, marker on "quiere?", scribble under "duele?", mascot peeks | `marker()` (CSS var `--m` → background-size) |
| 8.7–12.6 | entre pregunta y pregunta, casos reales y datos… | 4 hard-cut cards with label pills; radio pick, +38 % counter, 7/10 counter, tips | `counter()`, caption swaps per phrase |
| 12.6–13.7 | esto tiene sentido | 2-line type, yellow marker on "sentido." | slight zoom-out |
| 13.7–16.0 | un resultado hecho para él | browser window: spinner → "Plan Growth", ticks, CTA button | |
| 16.0–17.5 | una oferta a su medida | red full bleed, white type, yellow underline | |
| 17.5–19.3 | con un contador para canjearla | offer card, 15:00 → 14:57 on SFX ticks, button pulse | `steps(3)` tween |
| 19.3–22.9 | no solo captas el lead, lo segmentas, lo educas, y lo llevas | one line per beat over a funnel timeline; playhead sweeps; matching clip pulses | |
| 22.9–23.7 | a la compra | red diagonal slab slams in from the right | power4.out, rotate(-9deg) |
| 23.7–28 | comenta quiz y te enseño cómo montarlo | mascot, "› comenta QUIZ" pill, sub line, SaaS IN House lockup, fade | |

## Recipe
1. Copy `template/` and pick a VO (reuse it; no TTS). Get word times with `npx --yes hyperframes@0.8.137 transcribe <vo> -l es -m large-v3`, then run `python3 -I tools/words_to_js.py transcript.json --offset 0.3`. This prints `index:word@time` and the `const W = [...]` array. **Check the transcript is Spanish:** `sih-quiz-film/assets/transcript.json` is a bad English transcript, so use the W array embedded in `template/index.html` / `x-batch/jordan/index.html` for that VO.
2. Rewrite the `SC` scene windows in word indexes (hard cuts on words) and each `words(host, from, to, {map, cls})` call. `map` replaces the displayed text, which keeps captions = spoken words (e.g. "Cinco" → "5"). `cls` adds `red`/`hl` to the accent word.
3. Swap the card copy (label pill + card). Anything numeric that isn't real gets an `ejemplo` / `dato ilustrativo` tag.
4. Put SFX `<audio>` on the cut times: whoosh on scene cuts, pop on chips/cards, key on typing, tick on countdown seconds, impact on the slabs.
5. Run `npm run check` (0 errors), then `npx --yes hyperframes@0.8.137 snapshot --at … --describe false --no-end` at every beat. Look at the frames and fix.

## Cost
$0 of images: everything is HTML/CSS (cards, chips, UI, mascot), and no ElevenLabs calls. The VO, music and SFX are reused from `sih-quiz-film` and `x-batch/jordan`.

## Gotchas
- **Don't tween `width`/`left`.** Check fails with `gsap_non_transform_motion`. The pill stretch is built from two round caps translating plus a middle rect `scaleX` inside a `drop-shadow` wrapper.
- **The highlighter uses `background-size: calc(var(--m)*100%)`.** A `::before` with `z-index:-1` gets a negative_z_index warning, and an opaque scene background hides it.
- **Hidden cards inside a later scene still trip layout overlap checks.** Give every card layer an explicit `visibility: hidden` and set it visible on its cut.
- **Typed text in a flex row drops trailing spaces.** Use `margin-right` between word spans.
- **Small grey labels on white fail contrast (need 3:1).** Ruler numbers use #6e6e78, and clip colours are darkened (#b8352c, #2f5fd0, #1b8a4b).
- **Centred lines are pre-laid out.** All words exist from the start at opacity 0, so the line never re-centres while it builds.
- **Readability.** The original crams many things at once, and a reply on the tweet criticised it for "not communicating what the app does". Keep one idea per beat, and let the spoken words drive what is on screen.
