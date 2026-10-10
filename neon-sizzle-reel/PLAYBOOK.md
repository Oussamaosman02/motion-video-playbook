# Playbook: Neon sizzle reel (dark space + one neon colour, music only)

Reverse-engineered from **@AIandDesign "Opus 5.5 is killing motion graphics"** (https://x.com/AIandDesign/status/2104285967251378494): a 66 s, 16:9 brand sizzle reel for an AI studio, all code ("one HTML file"), music only (local whisper returns only noise). Contact sheet of the original: `reference-original-sheet.jpg`. Our version: `x-batch/aiandesign/` (55 s, 1080x1920, Spanish, SaaS in House red instead of the original's acid green).

## What makes it distinctive
- **One neon accent on near-black space.** Starfield everywhere, one glow colour (theirs green, ours brand red `#ff4134`) for wireframes, lasers, the second headline line and chips. Everything else is white/grey.
- **Section grammar:** small mono `01 Label` tag → two-line grotesk headline (line 1 white, line 2 neon) → one grey sub-line. Left-aligned at x=96 in vertical.
- **A procedural "hero" per section**, all drawn on one canvas as a pure function of time: wireframe polyhedron on a hex grid → particle burst/cloud → 3D glass emblem → orbiting cards with constellation lines → particle galaxy with laser beams → perspective grid floor + wireframe UI → wall of tiles → speed streaks → wireframe funnel → particle stream into the wordmark.
- **Typewriter mono lines** for the "thinking" beats, and a **black breath** with a blinking cursor (placed on the music's silent gap).
- **Inverted slab:** one full-colour (neon) frame with a huge black question, right before the lockup.
- Hard cuts between sections, flashes on the burst and on the music drop.

## Beat table (ours, 55 s, music cuts from `assets/music.mp3`)
| t | Section | What you see | Technique |
|---|---|---|---|
| 0–5.6 | S1 hook | stars, mono typed "Mandar a todos a la misma landing es fácil." → red "Venderles con ella, no." | `typeOn` proxy tween, `rise` (blur/opacity/y) |
| 5.6–9.6 | S2 | neon icosahedron draws on, rotates over a hex grid, bursts into a particle cloud | canvas `drawPoly` (3-pass neon line), seeded `BURST` particles |
| 9.6–14.2 | S3 hero | flash → glass "?" emblem + "Menos demos a ciegas. / Más Quiz Funnel." | Gemini emblem on black → `glow_to_alpha.py` |
| 14.2–19.4 | 01 Preguntas | 16 grey question cards orbit the emblem in 3D, constellation lines | card transforms set from `drawFX(T)` (seek-safe) |
| 19.4–24.4 | 02 Cards de valor | 1,500-point red galaxy, 3 lasers draw out to 3 chips (Caso real / Dato / Consejo) | canvas spiral arms, `neonLine` |
| 24.4–29.0 | 03 Resultado | red perspective grid floor, wireframe dashboard counts up, phone with result | DOM `.wire` boxes + SVG line draw |
| 29.0–31.0 | breath | black, typed "Y aquí viene lo importante." + cursor | sits on the music's silent gap |
| 31.0–37.0 | 04 Oferta (drop) | planet-horizon image, hexagon wire, 4 photo panels in 3D, countdown pill | `bg-space` under the canvas |
| 37.0–39.6 | wall | tilted wall of photo/UI tiles scrolling, "Un formulario capta un lead." | DOM grid in `rotateX/rotateZ` |
| 39.6–42.6 | streaks | red/grey speed streaks, "lo segmenta, lo educa / y lo lleva a la compra." | canvas, seeded per frame |
| 42.6–46.0 | funnel | rotating neon wireframe funnel with leads dropping through | canvas ellipses + meridians |
| 46.0–50.4 | red slab | huge black typed "¿Y si cada lead viera la oferta que necesita?" | `#bg-red` under the canvas |
| 50.4–55.0 | lockup | particle stream collapses to a line → SaaS IN House + "Comenta QUIZ" | `STREAM` particles, chime |

## Recipe
```bash
cp -r playbook/neon-sizzle-reel/template x-batch/<slug> && cd x-batch/<slug>
# 1) music: a bed with a slow build, a short silent gap and a drop works best (ours: hero-object-film bed from 3 s)
FADE=1.2 FADEIN=0.05 GAIN=2 bash ../../playbook/tools/fit_music.sh <bed.mp3> work/m.mp3 55 3-end
ffmpeg -i work/m.mp3 -af "alimiter=limit=0.89:level=false" -b:a 192k assets/music.mp3
python3 ../../playbook/tools/music_rms.py assets/music.mp3 1   # put B.s8 on the drop, B.s7 on the gap
# 2) images (4 × ~$0.03): glowing emblem ON BLACK (not magenta), 9:16 planet horizon, 2 square photos for panels/tiles
python3 ../../playbook/tools/gen_image_ar.py work/emblem.png "<object> made of glossy translucent <colour> glass, inner neon glow, pure solid black background, no text" --ar 1:1
python3 tools/glow_to_alpha.py work/emblem.png assets/emblem.png 900
# 3) edit copy + B (scene starts) in index.html, then
npx --yes hyperframes@0.8.137 check
npx --yes hyperframes@0.8.137 snapshot --at 4.5,7,9.3,12.8,17,22,27.6,30,34.5,38.6,41.8,45,49.6,54.2 --describe false
```
Retheme: change `--neon`/`--red` and every `rgba(255,65,52,…)` in the canvas code (one search/replace).

## Cost
4 Gemini images = **$0.12**. No TTS, no ElevenLabs (music + 13 SFX reused from the library). No AI video.

## Gotchas
- **`mix-blend-mode: screen` on the emblem showed a black square** inside a `perspective` wrapper (the wrapper isolates the blend). Convert glow-on-black renders to real alpha with `tools/glow_to_alpha.py` (alpha = brightness, colour un-premultiplied) and drop the blend mode.
- **First polyhedron was cropped**: with perspective (`f=1100`) the near vertices grow ~25 %; keep scale ≤ ~210 px for a centred 1080-wide frame.
- **Lint vs. intentional 3D swarms**: overlapping orbit cards / the tile wall / photo panels trip `content_overlap` and contrast (blurred far cards). Mark their containers (and the canvas) `data-layout-ignore`.
- **`gsap_fullscreen_overlay_starts_visible`** fired on `#bg-space` even with inline `opacity: 0` (inline `url('…')` in the same style). Add `gsap.set(["#bg-space","#bg-red"], {opacity: 0})` outside the timeline.
- Two `<img>` with the same src trigger `duplicate_media_discovery_risk`: the second emblem is a `background-image` div.
- Music-only: give each headline ≥ 3 s on screen; the first S5 draft revealed it 2 s before the cut.
- Canvas is redrawn every frame (stars + up to 1,500 points); no `shadowBlur`, the glow is a 3-pass stroke (wide transparent, mid, thin white core).

## Placeholders / example data
"4 → 19 demos/mes", "7 de cada 10 lo terminan", dashboard 412/268/19, "SaaS B2B con leads fríos", "Plan Growth −30 %", countdown 14:59 — all invented, labelled DATOS/OFERTA DE EJEMPLO.

## Files
`template/` (project, assets, `tools/glow_to_alpha.py`), `tools/glow_to_alpha.py`, `reference-frames/` (7 s polyhedron, 12.8 s hero, 34.5 s offer, 54.2 s lockup), `reference-original-sheet.jpg`.
