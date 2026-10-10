# Player-HUD reel (voice): format V candidate, `player-hud-reel/`

Example: `x-batch/nateherk/` (36.0 s, 1080x1920, Spanish, SaaS in House Quiz Funnel). Reference: https://x.com/nateherk/status/2103611727661482117 is a 15 s, 16:9, 60 fps "motion reel" for a video platform, music only at 129 BPM, one-shot by Opus 5.5 in HyperFrames. We copy its motion language, never its content (no platform logos, play buttons or UI).

## What makes it distinctive
- **A persistent player HUD over every shot**: corner brackets, a breadcrumb top-left (`■ BRAND / QUIZ REEL`), a spec badge top-right (`● 1080P60 · 117 BPM`), a live timecode bottom-left (`0:07 / 0:36`), a **chapter-segmented progress bar with a glowing red playhead**, and the chapter name bottom-right (`03 · PREGUNTAS ›`). The HUD recolours with each shot (cream on dark or red, ink on white). This is what makes 15 different shots feel like one film.
- **Hard cuts on the beat or word, with backgrounds cycling dark / white / red** (only the brand red, cream and ink). There's a 0.4 s `scale 1.06 → 1` punch-in on every cut and a white flash at section changes.
- **The product's own UI primitives are the heroes**, shown huge and clicked by a cursor: a search bar that types, a pill button with a counter, a subscribe-style black button, a countdown. In our version these are a quiz funnel's primitives: search, answer chips, a "tiene sentido" pill, a result card, an offer button and a countdown.
- **Debug/inspector annotations** in tiny mono with leader lines (`POS 431.9 1002.0 / SCL 108% / VEL 1058 PX/S`, `OBJECT RESULT_BADGE / MATCH 97%`). They sell the "made in a motion tool" look.
- **Showpiece techniques, one per beat**: a dot on a timeline that splits into a crowd; a giant word over **diagonal tiled repeating words** (rows scrolling in opposite directions, every 4th row in red); **particle dust assembling a number**; a red tile grid that becomes a wall of cards on a tilted perspective plane; a **glossy 3D object** (red, then a chrome swap with a brightness flash); a "LIVE"-style slam on red; and an end lockup with a rule and small text left and right.

## Beat table (nateherk, VO offset 0.4 s, `t(i)` = word i)
| t (s) | VO | shot (bg) | technique |
|---|---|---|---|
| 0–3.8 | ¿Quieres vender… misma landing? | dark | red playhead dot moves along a segmented line with a debug callout; on "todo el mundo" it splits into 46 dots, which all dive into one outlined LANDING box on "misma", and the box shakes red |
| 3.8–4.8 | Haz esto. | white | HAZ / ESTO. slams (270 px Archivo 900), white flash |
| 4.8–6.4 | En vez de pedir una demo, crea un… | white | search bar types "pedir una demo" in time with the VO, red strike, then retypes "quiz funnel", dropdown, cursor click |
| 6.4–7.5 | Quiz Funnel. | white → dark | QUIZ on white; on "Funnel" the bg turns dark with 16 tiled rows of "QUIZ FUNNEL ·" (−14°) and FUNNEL lands |
| 7.5–9.6 | Primero, entre cinco y ocho preguntas | dark | 597 red particles assemble "5–8", left to right ("5" on cinco, "8" on ocho), then PREGUNTAS |
| 9.6–12.5 | para saber quién es, qué quiere… problema | dark | 4×8 red tile grid sweeps in from the centre; 3 white question cards pop on quién / qué / cuál |
| 12.5–16.4 | Entre medias, cards… pensar | dark | tilted card wall (perspective 1600, rotateX 18, rotateZ −9) whose tiles flip from red to cards; a hero "caso real" card on casos, a red "×3" card on datos |
| 16.4–18.2 | vale, esto tiene sentido | dark | ring draws in, the "Tiene sentido" pill is clicked on "esto": the check fills red, a 14-dot burst, the counter ticks 2.4K→3.1K |
| 18.2–21.5 | Después, un resultado personalizado según sus respuestas | dark | 3D red "?" badge flies in with an inspector note; result card with bars; chrome swap on "personalizado"; answer chips on "según" |
| 21.5–22.8 | Y lo importante: | red | ● AHORA blink, LO / IMPORTANTE slam + 4-frame shake |
| 22.8–26.3 | las últimas cards… oferta específica | white | 3 small cards fly into "Tu producto"; the black "Activar oferta −30%" button is clicked → red "✓ Oferta activada" + mono state line |
| 26.3–28.1 | y un contador de tiempo limitado | red | 300 px countdown 14:59→14:56, draining bar |
| 28.1–29.9 | Así no solo captas el lead | dark | NO SOLO struck through, target brackets close on a lead dot, "✓ CAPTADO" |
| 29.9–33.0 | Lo segmentas, lo educas y lo llevas… compra | white / dark / red | three hard cuts: dots sort into 3 columns; cards over EDUCAS; COMPRA + "Pagar ✓" |
| 33.0–36.0 | (music) | dark | S logo pops, wordmark clip-wipe, rule, "Comenta QUIZ" + "y te enseño cómo montarlo", HUD fades, then black |

## Recipe
1. Copy `template/` and swap `assets/vo.mp3` and the `W` array (words `[word, start, end]`). Every cue is `t(i)`. Keep `VO`, `END` and `S15` in sync with your VO length.
2. Set the `SC` scene table (`[id, start, end, theme]`). The loop shows/hides scenes, recolours the HUD and caption, and adds the punch-in. `CH` is the chapter table that drives the progress-bar segments (flex = chapter length) and the chapter label.
3. Captions: `CHUNKS` lists phrase ranges of word indexes. Each chunk shows on its first word, and each word goes from 0.32 → 1 opacity on its own start (karaoke). They always match the VO.
4. Particles: `python3 tools/glyph_points.py data/pts.json "5–8" assets/Archivo.ttf`, then paste the result as `PTS`. The reveal order is driven by x (`(px/1080)*1.05 s`).
5. Images: one Gemini sheet (16:9, magenta, two objects not touching), cut out with `../tools/cutout_grid.py sheet.png assets 900 badge_red badge_chrome`. Prompt: `template/data/prompts.md` (sheet kept as `data/badges_sheet.png`).
6. Audio: reuse a bed with `../tools/fit_music.sh` (≈115–130 BPM; 117 BPM ui-launch-reel bed here), library SFX, and at most 2 new ElevenLabs SFX (`shimmer` for particles/chrome, `stutter` for cuts). SFX cues are plain `<audio>` elements on their own track indexes (`tools/inject_cues.py` shows the cue-list pattern).
7. `npm run check` → 0 errors, then snapshots at every shot (≥ 20 for a 36 s reel).

## Cost
1 Gemini image (~$0.03), 2 ElevenLabs SFX (~2 calls), VO and bed reused, no AI video.

## Gotchas
- **`fromTo` renders immediately.** A flash done as `fromTo({opacity:.55},{opacity:0})` at t=3.7 leaves the flash at 0.55 *before* t=3.7 (check flagged it as low contrast on the HUD). For later effects on an element that already has a tween, use `tl.set(...)` + `tl.to(...)` instead (the flash and the badge brightness).
- An SVG `transform="rotate(-90)"` on a circle is wiped as soon as GSAP scales it. Put the rotation on a wrapping `<g>`.
- Elements with a CSS `transform: scaleX(0)` must be animated with `fromTo` (lint `gsap_css_transform_conflict`). Don't tween `letterSpacing` (lint `gsap_non_transform_motion`).
- Tiled words, the tile grid, the card wall and rotated mini cards trip `content_overlap` by design, so mark them `data-layout-ignore`.
- Huge single words: 9–10 letters at Archivo 900 need ≤ 150 px (SEGMENTAS 150, IMPORTANTE 128, COMPRA 186) or they cross the 1080 frame.
- Particle dots: generate points offline (a runtime canvas sample races the font load). ~600 dots is the sweet spot.
- Debug annotations are decorative (19–22 px). Keep real information in the 44 px caption and the big type.
- Keep HUD text off the bottom ~1500–1780 band: that's where the caption lives (top 1548 px), clear of the Reels UI.
- `npx hyperframes transcribe` auto-detected English on this Spanish VO (garbled words, correct timing). Use it only to verify the timing of an existing `words.json`, or pass a language.
