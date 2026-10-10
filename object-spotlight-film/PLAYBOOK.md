# Playbook: Object spotlight film (voice, zero images)

- **Reference:** part 3 (100–156 s) of @_mexicat's Opus-made motion-graphics lyric film, reposted by @minchoi: https://x.com/minchoi/status/2104227722377757031. This part is the "cinematic object chapter": a field of repeated 3D objects, a glowing screen in the dark, a spotlight cone on a stage, giant type slams with cropped letters, and a big counter that multiplies and then collapses into one serif-italic statement. Contact sheet of the part: `original-contact-sheet-100-156.jpg`. We copy the techniques only, never the lyrics, characters, mask, product names or on-screen text.
- **First use:** SaaS in House Quiz Funnel, `x-batch/minchoi-c/` (1080x1920, 57 s).
- **Cost:** $0 for images (everything is drawn in code), 2 ElevenLabs SFX (spot clunk, screen-off). The VO, music and other SFX are reused.

## How it differs from `kinetic-hud-film` (same reference, whole film)
`kinetic-hud-film` is **type as the visual**: a HUD stage (crop marks, timecode strip, transcript line), wireframe canvas scenes, one accent colour, ghost/echo type. This format is **objects and light as the visual**: physical-looking things (monuments, slabs, a laptop, a stage, a result card) lit by a single warm light source in a dark room. There is no HUD chrome. Every scene answers "what is lit, and what is in the dark". Type only *slams* over objects (cropped by the frame) or settles as a quiet serif statement. Palette: tungsten warm `#ffd2a1` + hot orange `#ff5a2b` + brand red `#e8382d` on near-black, one paper-white contrast beat. The ending is a counter → statement collapse, not a logo orbit.

## 1. What makes it distinctive
- **Repetition, then selection.** Open on a field of many identical objects (a crowd = "everyone gets the same thing"), then kill the light on all but one, which gets a spotlight. That cut is the message: segment, pick one.
- **One light source per scene:** the spot cone (canvas or CSS `clip-path` + `mix-blend-mode: screen`), the screen glow (`box-shadow` + a floor pool), and the burst. Darkness does the framing.
- **Cropped slams:** Archivo 900 at `font-stretch: 62%`, set bigger than the frame (`width > 1080`, negative left), entering with scale 1.3–2.2 → 1 + blur → 0 in ~0.3 s on the spoken word. One word or half-word in hot orange, sometimes outline (`-webkit-text-stroke`).
- **Paper flash:** one white beat with black type cropped at the bottom and outline echoes stacked below (QUIZ / FUNNEL).
- **Depth descent:** 3D CSS slabs (`preserve-3d`, `translateZ(-i·330px)`), the camera "descends" by tweening the parent's `z` one stop per spoken item. The past slab dims and the one two back vanishes.
- **Type wall:** a dense, tilted wall of a repeated word. Rows drift in opposite directions, and one row lights up white + orange on the word.
- **Screen-off:** the glowing screen flashes, collapses to a horizontal line (`scaleY .012`), then to a spark.
- **Counter chapter:** a mono label `NAME(args)`, a huge light-weight mono number and an orange slider with ticks. The number changes meaning per sentence (card n/8 → fit 0.12→0.97 → −30 % → a countdown). On "limitado" it **multiplies** into a grid of timers, which collapses (scaleY then scaleX) into a single glowing "1 lead". That resolves into a serif-italic statement `Lead → compra (1)` with a footnote.
- **CTA as a UI button in the dark:** a spark, one pill button, a cursor clicks it, the button fills red, then the chime and the lockup.
- Phrase captions in mono under every scene (the spoken word in warm orange; dark on the paper beat).

## 2. Beats (Quiz Funnel script, Gabriel VO, `t(i)` = word start + 0.3 s)
| Scene | Words | What you see | Technique |
|---|---|---|---|
| s1 field | 0–13 | Dolly over ~390 identical landing "monuments", slams TODO EL MUNDO → A LA MISMA / LANDING | canvas `field()`, `panel()` |
| s2 spot | 14–15 | All dark but one, spot flickers on, serif *Haz esto.* | same canvas, sightline cleared |
| s3 demo | 16–22 | Push-in on the chosen one, DEMO slam, red strike + demote on "directamente" | slam + strike bar |
| s3b paper | 23–26 | QUIZ / FUNNEL, letters drop, echoes | paper flash |
| s4 depth | 27–48 | 8 question slabs, a stop per item, `PROFUNDIDAD · P.0n / 08`, 5–8, ¿QUIÉN? / ¿QUÉ QUIERE? / ¿SU PROBLEMA? | CSS 3D descent |
| s5 wall | 49–53 | PREGUNTAS? wall, SOLO PREGUNTAS lights, "+ algo más" box | type wall |
| s6 screen | 54–73 | Laptop glowing in the dark, 4 cards pop on their words (ejemplo), «Vale, esto tiene sentido.» | CSS 3D laptop + glow |
| s7 stage | 74–82 | Screen-off → curtain stage, spot, TU RESULTADO card drops, PERSONALIZADO stamp | screen-off, CSS cone |
| s8 burst | 83–87 | Converging streaks, then burst + flash + IMPORTANTE (music drop) | canvas `burst()` |
| s9 counter | 88–119 | CARD 06→08/08 · ENCAJE 0.12→0.97 · −30 % · countdown → timer grid → collapse | `TXT(t)` pure counter |
| s10 statement | 120–136 | 1 lead → "No solo captas el lead." / *lo segmentas, lo educas…* → *Lead → compra* (1) | serif collapse |
| s11 CTA | (after the VO) | Spark, ↻ Comenta QUIZ button clicked, SaaS IN House | cursor click + chime |

## 3. Recipe
1. Copy `template/`. Put your VO in `assets/vo.mp3` and run `npx --yes hyperframes@0.8.137 transcribe assets/vo.mp3 -m small -l es` (**`-l es` + the multilingual `small` model**: an old English transcript of this VO was a translation). Fix spellings in `FIX` in `tools/build.py`.
2. Edit `tools/index.src.html` (never `index.html`): scene windows `T`, caption chunks `CH`, the cues per scene. Edit the SFX list `CUES` in `tools/build.py` (`"w87"` = word 87; `"w79+0.3"` = with an offset). Then run `python3 tools/build.py`.
3. Music: `fit_music.sh` with a splice so the track's drop lands on your "importante" word. Here it was `XF=1.0 FADE=1.6 fit_music.sh x-batch/aiandesign/assets/music.mp3 music.mp3 57 4-30 10-16.2 28-end` (drop at 33.0 s). Then an ffmpeg `volume='if(lt(t,51.7),1,…)':eval=frame` envelope lifts the bed after the VO, so the CTA isn't quiet. The bed sits at 0.2 under the VO.
4. `npx --yes hyperframes@0.8.137 check` → 0 errors. `snapshot --at … --describe false --no-end --timeout 15000`, then look.
5. Render one at a time: see `template/RENDER.md`.

## 4. Gotchas
- **`fromTo` renders its FROM at t=0** (immediateRender). A `fromTo("#flash",{opacity:.9},…)` at 33 s covered the whole film. For anything whose "from" differs from its resting CSS, use `tl.set(from, at)` + `tl.to(...)`.
- `check` errors on tweened `letterSpacing` (it snaps). Use `scaleX` for the "tracking in" feel.
- A second root HTML (`index.src.html`) makes `check` fail with `multiple_root_compositions`, so keep the source in `tools/`.
- Canvas monuments in front of the chosen one hide the spotlight: skip the rows in front (`z < CHOSEN.z`, `|x| < 4`) once the field goes dark.
- Mono numbers at 250 px: an `hh:mm:ss` overflows 1080. `TXT()` drops to 180 px when the string is longer than 5 chars.
- Counters, depth labels and the timer grid are written by `TXT(t)` inside the canvas clock's `onUpdate`, so they are a pure function of time (safe for seeking). Never update text from separate tween `onUpdate`s.
- The rotated slams crop by design, but keep the key word readable (¿SU PROBLEMA? needed 186 px, not 230).
- Example numbers (3× demos, 7 de 10, +42 %, −30 %, 0.97, 23:59:59) are placeholders marked **ejemplo**.
