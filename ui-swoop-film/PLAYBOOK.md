# UI swoop film (`ui-swoop-film`)

A fast, light **SaaS product-promo reel built only from UI pieces**: a URL card typing on a dark stage, a camera push into its send button, tilted 3D cards, outline type columns, a pan across a grid of pills, blob-mask reveals with gold feature tags, a "word [phone] word" sandwich, floating cards, a button that becomes a "done" pill, and a list of toggles switching on. Every beat is a UI micro-interaction, and every cut is a **whip with motion blur**. It's voiced here (a reused 26 s VO) with a dark pill caption. It's 100% HTML + GSAP: **0 images, 0 ElevenLabs calls, no AI video.**

Project: `x-batch/chhddavid/` (28.0 s, 1080x1920, Spanish). Template: `template/`.

## Source
Reverse-engineered from David Ch's quote-tweet "IT'S SO OVER!! Motion designs are cooked. This AI agent one-shot this video in 13 mins" (https://x.com/chhddavid/status/2102063344765264348). It is a 20 s, 16:9, music-only launch reel for an AI short-clip tool, with 63k views and 694 bookmarks. The author posted no making-of (the replies only debate whether it was really AI). The motion language was copied, never the content: the original's brand, logo, platform logos and the real person in its clips were all replaced by coded quiz-funnel UI.

## What makes it distinctive
1. **UI is the actor.** There are no characters and no photos. Cards, pills, buttons, bars and toggles carry the story, each doing one micro-interaction (type, click, check, toggle).
2. **Camera moves through the UI**: a 3D-tilted card, then a `scale ×5.5` push toward its send button, then the next scene opens on that button, huge and blurred, settling in (match cut).
3. **Light / dark alternation**: dark stage with scallop circles → cream → white with black blobs → black sandwich → gold gradient → white end card.
4. **Sandwich typography**: one word left of a phone, one right (and the punch word huge below it in portrait), revealed word by word on the VO.
5. **Accent system**: brand red for the hero (QUIZ pill, strike, "sentido."), gold for tags/badges/toggles and the highlighted caption word, ink for "done" pills.

## Beat table (ref → ours, film times)
| t | Reference | Ours | Technique |
|---|---|---|---|
| 0–2.9 | "COPY & PASTE", green circles, URL card, cursor clicks | Dark stage, red scallop circles, "Tu próximo cliente / no llega por la landing", card types `tusaas.com/landing`, click, red strike + "0 leads" | circles `fromTo` y/x; `textContent` set per char; cursor tween + yoyo click |
| 2.5–2.95 | 3D swoop into the send arrow | card `rotationX/Y + scale 5.5 + x/y` in 0.42 s `power3.in` | scene `perspective: 1600px` |
| 2.9–4.5 | big round arrow button | button lands huge + blurred → morphs into red **QUIZ** pill on "quiz." | circle squashes/fades + pill `scaleX .63→1` `back.out` (never tween width/left: the linter rejects it) |
| 4.5–8.7 | "ANALYZING" outline columns, tilted clip, yellow/purple bars + playhead | "PREGUNTAS" outline columns, tilted quiz card cycling 3 questions on "quién / qué quiere / qué le duele", "5–8" chip, bars + playhead | `-webkit-text-stroke` + `writing-mode: vertical-rl` (mark `data-layout-ignore`) |
| 8.7–10.1 | grid of grey pills, dark "Clipped ✓" | pan across a pill grid, dark "Pregunta 2 ✓" → "Pregunta 3 ✓" | grid container x/y pan + blur yoyo; check `strokeDashoffset` |
| 10.1–12.6 | black circle masks, "Auto …" yellow tags orbit a clip, green glitch | black blobs, case card "4→19 demos al mes", gold tags Casos reales / Datos / Resultados / Consejos, red-gold glitch out | tags `back.out(2.6)` pops + sine drift; glitch = gradient overlay + skew yoyo |
| 12.6–13.7 | "Built to [phone] go viral" + hearts | "Esto [phone] tiene / **sentido.**" + check-mark burst | words timed to `t(i)`; radial burst from the phone corner |
| 13.7–16.2 | clip + track editor rows | result phone "Perfil: Escalando" + 4 answer tracks + playhead, "Hecho para ti ✓" | bars `scaleX` from 0 |
| 16.2–17.5 | black "Every [phone] Time" | black "una oferta [phone −30%] a su medida" + gold sparkles | same sandwich on night bg |
| 17.5–19.3 | floating 3D clip cards, "Generate multiple clips" | floating mini quiz cards fly in with blur, countdown card 14:59 → 14:57 | per-card blur by fake depth |
| 19.3–23.6 | "Publish" yellow button → click → "Completed", platform toggles | gold "Captar lead" → click → dark "Lead captado ✓", toggles Segmentado / Educado / Listo para comprar | `.hl` gradient `scaleX`, knob `x: 54` |
| 23.6–28 | logo end card | "Comenta QUIZ" + sub + SaaS IN House lockup, red scallops callback, fade to white | |

## Recipe
1. Copy `template/` to `x-batch/<slug>/`.
2. Audio first. Voice: reuse a VO (`AUDIO-REUSE.md`) and paste its word array into `const W`. `python3 -I tools/words_from_index.py index.html` prints `index:word@time`. Every cue is `t(i)` and every scene boundary is `t(i) - 0.05`. For a music-only cut, drop `#vo`, keep the caption pill as the on-screen script, and time scenes to bars (`playbook/tools/music_rms.py`).
3. Music: `playbook/tools/fit_music.sh SRC assets/music.mp3 28 0-22 31.5-39.5` (keeps the source's outro, so the lockup is not silent). Bed volume is 0.3 under the VO.
4. SFX: library only (andres-clips `click/ding/swoosh_in/swoosh_up/stamp/thump/riser`, airy `chime`, jordan `key`, plus whoosh/pop/impact). One `<audio>` per cue, on its own track index.
5. Edit the `SC` windows, captions `CAP` (index ranges) and `capEnd` (hide the pill before scenes that carry their own big type).
6. `npm run check` → `snapshot --at …` at every scene → look → fix.

## Cost
0 images ($0), 0 ElevenLabs calls, 0 TTS. Reused: VO `sih-quiz-film/assets/vo.mp3`, bed `playbook/ui-launch-reel/template/assets/music.mp3`.

## Gotchas
- **Never tween `width/left/top`** for the morph (`gsap_non_transform_motion` is a hard error). Cross-fade two elements with scale instead.
- Outline text (`color: transparent` + stroke) trips `text_not_painted`, so add `data-layout-ignore`.
- Caption groups switch `position: relative/absolute` so the pill hugs the active phrase. When a scene hides the pill (`capEnd`), the next group must re-show the box (`[12,26,30,41,54,59]` list). Forgetting this dropped the S5 caption in the first pass.
- Portrait sandwich: "word [phone] word" only fits with short words (≤ 6 letters at 92px). Put the long punch word big under the phone.
- The −30% inside a 290px phone needs ≤ 84px.
- Overlapping tweens on the swoop card: end the drift tween before the swoop starts (lint warning).
- Muted grey on paper fails contrast at #8d8a96. Use #6b6976.
- Copy the motion language, never the content: no platform logos in the toggle list (generic numbered icons) and no people in the cards.
