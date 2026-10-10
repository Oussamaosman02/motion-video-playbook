# Format: Pixel-grid film (voice)

A Swiss-minimal launch film in the style of the 66s narrated launch video in @Miguel07Code's tweet (https://x.com/Miguel07Code/status/2095931337811042640, 16:9, 139K views, 1.3K bookmarks). He posted it as "one-shotted with HyperFrames from a reference video". It is pure HTML motion: an off-white grid, one orange-red accent, and pixel squares that assemble into UI. We kept that motion language and rebuilt everything else: the quiz-funnel script, original UI, 9:16, our brand red. **No images at all**: every visual is a div, an SVG or a pixel map in code.

Example: `../../x-batch/miguel07code.mp4` (59s, 1080x1920, rendered by the coordinator). Project: `../../x-batch/miguel07code/`.

## What makes it distinctive
| Element | Reference | Our build |
|---|---|---|
| Canvas | Light grey paper, a faint large grid, "+" crosshairs at intersections, a soft white centre glow | `#bg` with two `linear-gradient` line layers (135px cells = 1080/8), `#cross` SVG plus marks at every 3rd intersection, `#bgglow` radial gradient |
| One accent | Everything greyscale except a single orange-red | Brand red `#e8382d` on greys `#e2e2df / #cfcfcc / #a9a9a5 / #5d5d59`, dark cards `#1b1b1d` |
| Pixels assemble | Squares pop into diamond/ring formations, fly together into UI, break apart again | `sq()` helper; `glyph(parent, map, x, y, cell, colors)` draws any string map as squares (funnel, checks, avatar, icons, the CTA word) |
| Mosaic wipe | A full-screen grid of dark/grey/red tiles flips in, the scene changes under it | `mosaic(cut, palette)`: 8x15 tiles of 135px, diagonal order + seeded jitter, scale in → hard cut → scale out. Used 4 times |
| Stacked dark cards | Research cards stack and slide up, the front one in focus | `#s4-stack`: each new card enters from below; older cards go `y -100·lvl`, `scale 1-0.07·lvl`, darker bg, text faded (only their top strip peeks out) |
| Node lines + travelling dot | Orthogonal lines between price nodes, a red dot rides them | S6 question spine (P1–P5 spread apart to make room for cards); S7 three answer chips → orthogonal SVG paths → result card |
| Wireframe → content | A grey skeleton page turns into the real one | `#s7-skel` → `#s7-real` crossfade on "resultado" |
| Page grid + zoom | A grid of page thumbnails pans, then the camera dives into one | S9: 3x6 mini quiz cards pan up, the last two rows light red ("las últimas cards"), `scale 3.4` into one card → white → product card |
| Big counter | "1,000,000" in giant type | Giant GeistMono countdown `15:00.00` updated every 1/24 s with `tl.set(textContent)`, plus a 20-square pixel bar that drains |
| Pixel staircase | Red stepped bars fan out of the logo node | S11: 12 red bars whose widths step by 30px, `scaleX` from the centre, grey edge pixels flicker |
| Round icon tiles | White round tiles with a soft halo ring | `boxShadow: 0 0 0 14px rgba(255,255,255,.6), 0 18px 40px …` plus a pixel glyph inside |
| Chapter HUD (ours) | A small "\| SCRAPE \|" label | Mono `[01] una landing` … `[10] comenta` top-left; a red block wipes across on each chapter change |
| Captions (ours) | none | Chunks of ≤4 words at y 1560, upcoming words light grey, spoken word red, then ink. Hidden where the big type already says it (S2, S8, CTA). A fading bg band (`#capbg`) behind them over the page grid |

## Beat table (59s, VO at +0.4s)
| # | Window | VO | Visual |
|---|---|---|---|
| S1 | 0–4.7 | ¿Quieres vender tu SaaS sin mandar a todo el mundo a la misma landing? | Red square + grey ring → scatter into "visitors" → red square becomes the card CTA → every pixel streams into ONE landing card, visit counter 0→1.284, red "la misma landing" tag |
| S2 | 4.7–5.7 | Haz esto. | Dark mosaic, big cream "Haz esto." with a red dot |
| S3 | 5.7–10.5 | En lugar de pedir una demo… crea un quiz funnel. | "Pedir una demo" button, cursor click, it greys out and gets struck through ("conversión 1,2 %"), shatters into 48 pixels → stepped funnel with stage labels → "QUIZ FUNNEL" |
| S4 | 10.5–18.1 | Primero haces entre cinco y ocho preguntas… | "5–8" + 8-square bar; three dark question cards stack; a chip selected on each |
| S5 | 18.1–20.3 | pero no hagas solo preguntas. | 3x3 "?" tiles shake, the centre one flips red "+" |
| S6 | 20.3–29.9 | Entre medias añade pequeñas cards… Vale, esto tiene sentido. | Spine nodes spread, dashed ghosts, 4 cards slot in (caso real / dato / resultado / consejo), a red dot travels down; then a dark thought-bubble card with a pixel check |
| S7 | 29.9–34.3 | Después, según sus respuestas… resultado personalizado. | Answer chips → lines → skeleton → result card (pixel avatar, 87 %), "PERSONALIZADO" stamp |
| S8 | 34.3–36.1 | Y aquí viene la parte importante. | Mosaic → isometric red SVG cube with orbiting pixels, "LA PARTE / IMPORTANTE." |
| S9 | 36.1–44.6 | Las últimas cards… producto. Le explicas por qué encaja… oferta específica | Card grid pans, last rows light, zoom; "Por qué encaja contigo" card with 3 pixel checks; dark offer card, 149 € struck → 99 €/mes |
| S10 | 44.6–48.0 | y añades un contador con tiempo limitado para canjearla. | Giant countdown, draining bar, "Canjear oferta" button + cursor click |
| S11 | 48.0–54.3 | Así no solo captas el lead, lo segmentas, lo educas y lo llevas… a la compra. | Three round pixel-icon nodes (captas / segmentas / educas, "+1 lead"), red staircase, dark "COMPRA." card |
| S12 | 54.3–59 | (music) | Mosaic → "Comenta" + red pixel-built QUIZ (squares fly in, one wave pulse) + "y te enseño cómo montarlo" + SaaS IN House lockup |

## Recipe (≈ $0 images, 2 SFX calls, VO and music reused)
1. **VO:** reuse a base-script VO. Here that's `playbook/ui-launch-film/template/assets/vo.mp3` (Guillermo, 53.9s). Transcribe locally **with `-l es -m small`**: without the flags, whisper `small.en` *translated* the Spanish into English nonsense. Fix the mis-hearings by ear in `FIX` (SA → SaaS, haga → hagas, Yaquí → Y aquí). Save `[[text, start, end]]` to `work/words.json`.
2. **Music:** reuse a calm tech-launch bed. Here that's `benchmark-film/template/assets/music.mp3` (60s, final hit at ≈50–54s). Splice it so the hit lands on the CTA: `FADE=1.0 ../tools/fit_music.sh in.mp3 assets/music.mp3 59 0-46 41-end`. Check the last 3s are not silent (−18 dB here).
3. **SFX:** library tick/pop/whoosh/chime/blip/glitch/impact/ding, plus 2 ElevenLabs calls: `pixels.mp3` "cascade of tiny soft digital pixel tiles flipping…" 1.2s and `build.mp3` "short soft digital shimmer as small squares snap together…" 1.0s. `build` came back at −56 dB, so run `FIX=1 INPLACE=1 ../tools/sfx_normalize.sh`.
4. **Build** from `template/`: edit the copy and the beat code in `index.html`, then set the SFX cue list in `work/inject.py` (word index or seconds) and run `python3 work/inject.py` from the project folder. It injects `work/words.json` and the `<audio>` cues between the `/*WORDS*/` and `<!--SFX-->` markers. `tools/inject.py` is the same script, for reference.
5. `npx --yes hyperframes@0.8.137 check` (0 errors) → `snapshot --at …` at 10+ beats → look → fix → render `-w 2`.

## Gotchas
- **Lint `gsap_non_transform_motion`:** never tween `left/top`. Positions are set in CSS, and motion is `x/y` deltas (e.g. `x: target - parseFloat(e.style.left)`).
- **Stacked cards and dimmed backgrounds trigger `content_overlap`.** That is intentional, so mark the container `data-layout-ignore` (`#s4-stack`, `#s6-cards`). Still fade the text of back cards: semi-transparent dark cards on light paper read as washed-out grey with ghost text. Keep them opaque and darken the bg instead.
- **Reusing tiles across several mosaics:** use `tl.set(backgroundColor)` + `tl.to(scale)` only. A second `fromTo` on the same element snaps it back.
- **Text over stripes is unreadable** (the staircase). Put the payoff word on a solid dark card.
- **The page-grid pan slides under the HUD and the captions.** Keep the pan small (60 → −120) and fade in `#capbg` during that scene.
- The Write tool turns a ` ` escape into a literal nbsp. Group thousands with a regex instead of `toLocaleString`, which doesn't group 4-digit numbers in es-ES anyway ("1284").
- Empty openings: when a scene starts before its key word, show the frame (empty node circles, the timer at 15:00.00) right away and fill it on the word.
- Example data is placeholder (Clínica dental +38 %, 7/10, ×2,4, 149 € → 99 €, 87 %, "Founder en tracción"). Replace it with true client facts before publishing.
- Originality: the reference has a third-party brand's logo and partner icons. We use none of them. The avatar, icons and checks are our own pixel maps.
