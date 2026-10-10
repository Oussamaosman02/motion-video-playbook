# Format V: Neon orbit launch film (voice)

A fast product-launch film in the style of @heylaxxy's 25s piece (https://x.com/heylaxxy/status/2100641829561741628, 16:9, 1280x720 best variant, music + SFX, made by hand by an agency for a voice-AI product). We kept its motion language and rebuilt everything else: our quiz-funnel script, the reused quiz VO, original assets, 9:16.

Example: `../../x-batch/heylaxxy.mp4` (28.0s, 1080x1920). Project: `../../x-batch/heylaxxy/`.

## What makes it distinctive
A chain of **one-idea micro-scenes (1–4 s each), each one a different "UI toy"**, cut hard with a short blur-in. Every scene changes background family (black → grey glow → black neon → pastel → navy → slate-purple → sky blue → deep navy), so the cut itself is the rhythm.

| Beat (ours) | Original | Technique |
|---|---|---|
| 0–2.9 s glow type → neon pill → strike | Glowing gradient text types out, morphs into a pill with a magenta/violet halo | Per-char spans with interpolated **solid** colours (gradient look, passes `text_not_painted`), drop-shadow glow; pill = black fill + white border + 3 stacked box-shadows; red strike bar `scaleX` |
| 2.9–4.5 s "Haz un quiz ✦" button | Purple "Generate ✦" button, cursor click, 4-point sparkles | Gradient pill, SVG cursor `<symbol>`, press = scale .92 → 1.06, shock ring, `sparkle()` helper |
| 4.5–8.7 s neon quiz window | Dark app window with a magenta→orange→yellow neon edge; camera dives into the corner where "Generate" is clicked | Two copies of the gradient (blurred glow + 6px edge), `backgroundPosition` drift; questions cycle on VO words; `#s3-cam` scale 1.75 + x/y onto "Siguiente →" + cursor click |
| 8.7–12.6 s pastel proof wall | Pastel gradient, testimonial cards with avatars and stars, huge blurred counter "Trusted by 895,799" | 6 white cards drifting up (generated illustrated avatars), `count()` = discrete `tl.set(innerHTML)` steps with a blur that clears (seek-safe) |
| 12.6–13.7 s face ring | Emoji ring around "Responds to emotional cues" | 8 **original** SVG faces drawn in `face(kind)` (no emoji font, no platform emoji art) |
| 13.7–16.0 s orbital dial | Concentric rings, white pause button, glowing satellite orbs with labels, a needle sweeps between them, then a waveform | Camera zoom-out 2.1 → 1, needle rotations to each orb (Perfil / Objetivo / Problema), pause → check, 15 bars with random heights set every 0.1 s |
| 16.0–19.3 s avatar ring → one lead | Ring of portrait cards "Access the library", then one portrait pushed in | 9 avatar cards counter-rotating in a rotating ring; on "contador" the others blow out (scale + blur) and one comes forward; offer pill + countdown in a **text-selection box** (blue frame + round handles) |
| 19.3–23.7 s sky + globe | Glossy globe rises into a cloudy sky, flags pop on its rim, big counter "36+ → 70+", white chips | Gemini glossy globe cut-out, CSS clouds, 8 abstract 3-stripe **segment tags** (not flags), headline swaps on VO words, chips Segmentado / Educado / Listo para comprar |
| 23.7–28 s navy end | "with 8840" in a selection box with handles, "every Month", grid lines, "Try now for free", logo | "comenta" + **QUIZ** in the selection box + wink face, 4 grid lines drawn with scaleX/Y, subline on VO words, SaaS IN House lockup, fade |

## Recipe (≈ $0.06 images, 0 ElevenLabs calls)
1. Audio: reuse `sih-quiz-film/assets/vo.mp3` (26.1 s, word array already in `template/index.html` as `const W`) and a music bed (`playbook/motion-showreel/template/assets/music.mp3` fitted with `../tools/fit_music.sh … 28`). SFX are the motion-showreel set (whoosh, click, pop, tick, chime, sparks, riser, impact).
2. Images (`../tools/gen_image_ar.py --ar 1:1`, 2 calls):
   - "3x3 grid of nine friendly flat-illustrated avatar head-and-shoulders portraits of fictional diverse business people … each on its own pastel rounded tile, wide gaps, not touching, flat magenta, no text, not photorealistic" → `cutout_grid.py sheet.png assets 300 av1 … av9`;
   - "single glossy stylised 3D toy planet globe … flat magenta" → `cutout_grid.py globe.png assets 1200 globe`.
3. Build from `template/`: retime the `SC` scene table (word indexes), change copy, then `python3 tools/build_audio.py` rewrites the `<!--AUDIO-->` block (VO, bed, 48 SFX cues by word index). New voice = paste the new `W` + `VO` and rerun.
4. `npx --yes hyperframes@0.8.137 check` (0 errors) → `snapshot --at …` → look → render with `-w 2`.

## Gotchas
- Gradient text on per-char spans fails `text_not_painted` (the spans inherit `color: transparent`). Give each char an interpolated solid colour instead.
- Don't tween `left/top` (lint error `gsap_non_transform_motion`); move cards with x/y. For a card inside a rotated ring, also tween the ring rotation back to 0, or the card lands tilted and off-centre.
- A GSAP `scale` tween overwrites a CSS `transform: translateX(-50%)`: centre pills with `xPercent: -50` inside the tween.
- The proof progress bar collides with the 3rd option if the window is < ~980 px tall.
- White small text on the sky fails contrast; use navy (#0a1f5c) for small lines, keep white only for 130 px+ headlines.
- Clouds, the globe and the rim tags overflow on purpose: mark them `data-layout-allow-overflow`.
- Keep it original: the reference's photoreal portraits, real flags, platform emoji and the brand's logo are replaced by illustrated avatars, abstract stripe tags, hand-drawn SVG faces and our lockup.

## Placeholders
"Caso real: de 4 a 19 demos al mes", "Plan Growth −30%", the 15:00 countdown and the testimonial names/quotes are `EJEMPLO` data. Replace with real numbers or drop them before posting.
