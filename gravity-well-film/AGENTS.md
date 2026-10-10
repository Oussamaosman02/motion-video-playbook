# Playbook: Gravity-well film (one deformable 3D wireframe world, type glued into it; voice, zero images)

- **Reference:** the first 60 s (the dark 3D chapter) of the Opus-made motion-graphics lyric film by @_mexicat, reposted by @minchoi: https://x.com/minchoi/status/2104227722377757031. It is 157 s, 16:9 and set to a song. The film was split in three: 60–100 s (paper forms) and 100–156 s (object field) belong to sibling formats. Contact sheet of this part: `original-contact-sheet-0-60s.jpg` (one tile every 2 s).
- **First use:** SaaS in House Quiz Funnel, `x-batch/minchoi-a/` → `x-batch/minchoi-a.mp4` (1080x1920, 31.5 s, Spanish).
- **Cost: $0 of images, 2 ElevenLabs SFX calls** (`rumble.mp3`, `vortex.mp3`). The VO (Sara, `chalk-quiz-funnel/vo.mp3`), the music (sih-trace-film bed) and the other SFX are reused. No AI video.

## 1. What makes it distinctive (we keep the techniques, never the lyrics, creature, mask or logos)
What we take from that 0–60 s part: loss-landscape topo surfaces in perspective, a spark sliding into a "sharp minimum", type riding curved 3D paths, a hatched sculpted object with HUD callout boxes, an oscilloscope grid with type on the sine, a spacetime-warp grid around a black hole with ring type, and type sweeping around the vortex.
- **One world, no cuts.** Everything happens on ONE wireframe surface `surf(x, z)` whose shape is keyframed on word times: flat dunes (the "landing") → swirled gravity well (the funnel) → topo rings → flattened graph paper (oscilloscope, camera straight down) → deep black hole → a rolled-up tunnel → the well again → a faint grid under the lockup. Scene changes are **morphs of the surface plus a camera move**, never hard cuts.
- **Type lives inside the 3D scene.** `text3()` places each glyph with its own affine transform built from 3 projected points (position, +tangent, −up). The same function does:
  - *glued type*: lies flat on the surface and bends with it, so when the plane sinks into the well, "LA MISMA LANDING" and ERROR are swallowed for free;
  - *ring type*: arcs on the far rim (reads left→right, up = outward) and the near rim (up = inward), e.g. QUIZ / FUNNEL, OFERTA / A MEDIDA;
  - *standing ring*: upright glyphs on a rotating circle, with the back half mirrored at 22 % alpha (the countdown, the 3 orbit words);
  - *riding type*: along a sine (oscilloscope) or a spiral, revealed by a spark that leads it.
- **Hatched sculpt with tracking callouts.** An original lumpy "lead core" (displaced sphere) drawn as ~70 latitude hatch lines, back-face culled, shaded by Lambert buckets, over a dark body fill. Four red HUD boxes track points on the turning surface, with leader lines to big labels (CASO REAL / DATO / RESULTADO / CONSEJO).
- **Physics HUD:** mono strip (brand · section · timecode), corner crop marks, and a live readout `prof / giro / tubo` printed from the surface parameters (depth, swirl, tunnel). Single accent: SaaS in House red `#e8382d` on near-black, cream type.

### How it differs from `kinetic-hud-film` (same reference, whole film)
| kinetic-hud-film | gravity-well-film |
|---|---|
| Type-first: one huge flat hero word per sentence (ghost/echo stacks) | The 3D surface is the protagonist; the words are objects in it |
| Separate canvas scenes (floor, topo funnel, city, orb) behind DOM type, hard cuts on every sentence | One continuous surface `surf(x,z)` that morphs; no hard cuts |
| Text on paths is 2D (`textPath` on an SVG line/circle) | Per-glyph 3D affine: type glued to the deforming mesh, ring type in perspective, mirrored back halves |
| A paper insert for contrast | Hatched sculpt with tracking HUD callouts, oscilloscope, black hole, tunnel |
| Green, LPDA brand | Red, SaaS in House brand |

## 2. Beats (Sara VO, `w(i)` = word start + 0.4 s)
| t (s) | Words | Surface / camera | What you see |
|---|---|---|---|
| 0–4.0 | ¿Vendes un SaaS… misma landing? | flat dunes, low dolly | "¿vendes un SaaS?" standing on a red ridge line with a spark; 54 lead dots stream to ONE red box; "LA MISMA LANDING" glued flat inside it |
| 4.0–5.4 | Error. | shake + glitch slices | standing red ERROR, "conversión 0,8 % · ejemplo" |
| 4.7–6.6 | Haz un quiz funnel. | plane sinks into a swirled well (rumble, vortex SFX) | box, dots and ERROR are sucked in; QUIZ (far rim) / FUNNEL (near rim) |
| 6.6–10.8 | Uno, 5–8 preguntas… quién es y qué necesita | orbiting camera over the funnel | 8 topo rings P1–P8 (3 dim until "ocho"), spark spirals down lighting them, "5–8 PREGUNTAS" standing behind, "¿quién es?" / "¿qué necesita?" glued to the walls |
| 10.8–14.0 | Dos, entre medias, cards con casos reales | camera level, sculpt rises from the throat | hatched sculpt + 4 tracking callouts (numbers marked *ejemplo*), "CARDS" |
| 14.0–17.0 | Tres, … resultado personalizado | well flattens, camera straight down = graph paper | noisy trace resolves into a clean red sine on "personalizado"; type rides it; RESULTADO box |
| 17.0–18.8 | Cuatro, una oferta a medida | deep black hole, swirl + spin | accretion streaks (front/back split around the horizon), OFERTA / A MEDIDA ring type, "04" |
| 18.8–22.4 | Y cinco, un contador… canjee ya | low orbit | standing ring "QUEDAN 00:14:58 · CANJÉALA YA" ticking every 0.5 s, big mm:ss; red + flash on "ya", ring shrinks into the hole |
| 22.4–24.7 | Nada de mandar a todos a la misma landing | plane rolls into a tunnel, fly-through | "LA MISMA LANDING" on the floor, red strike on "todos", breaks into dots on "landing" |
| 24.7–27.5 | Así segmentas, educas y vendes | the well again | SEGMENTAS / EDUCAS / VENDES on 3 orbits (each dims when the next lands), collapse + flash |
| 27.5–31.5 | (no VO) | faint grid | SaaS IN House lockup, red pill "comenta «QUIZ»", "y te enseño cómo montarlo", 2 chimes |

## 3. Recipe
1. Copy `template/`. Replace `assets/vo.mp3` and the `W` array (`[[word, start], …]`) with your word timings (local `npx --yes hyperframes@0.8.137 transcribe`, or the TTS alignment if the project has one; check they agree). Set `VO` (offset), `VO_END`, `END`, and the caption phrases `PH`.
2. Retime the world: `KD` (well depth), `KS` (swirl), `KR0` (throat radius), `KT` (tunnel), `KC` (camera eye + target). They are smooth keyframes; put the surface change ~0.3–1 s before the word that needs it.
3. Rewrite the scene functions (`landing`, `errorWord`, `funnelRing`, `topo`, `blob`, `scope`, `blackHole`, `tunnel`). Each one draws only inside its time window and fades with `sm()`.
4. Music: `fit_music.sh IN assets/music.mp3 LEN a-b` choosing a range so the bed's drop lands on the black hole, then a volume lift after the VO (`volume='if(lt(t,27.3),0.24,…)':eval=frame` → `music_mix.mp3`). SFX are `<audio>` tags. The voice is never processed.
5. `npx --yes hyperframes@0.8.137 check` → 0 errors. Then `snapshot --at … --describe false --no-end` at every beat and LOOK. Most bugs are type direction/length (see Gotchas).
6. Hand `RENDER.md` to whoever renders (`render -o ../x.mp4 -w 2 --quiet`, one at a time).
- To study one slice of a long reference: `tools/ref_range.sh ref.mp4 0 60 outdir 2 "12 15 35 41 45"` writes a contact sheet of that range plus a 2-column key-frame grid.

## 4. Gotchas
- **`F(t)` must be pure:** the engine is `tl.to(CLK, {v: END, onUpdate: () => F(CLK.v)})`; snapshots/renders seek randomly. Use `hash(n)` for randomness, no state carried between frames (the HUD `textContent` writes are fine because they are recomputed each frame).
- **Text longer than its path silently drops the end letters** ("FUNNE", "ISMA LAND", the countdown). Make the path longer than chars × size × ~0.75 × track; spaces are widened ×1.9 in `text3` because Archivo 900 spaces vanish in perspective.
- **Direction decides readability:** on the near side of a ring the angle must increase (left→right); on the far side it must decrease. `autoFlip` only fixes mirroring, not 180° rotation, so an upside-down word means the path runs the wrong way, or the word sits on the far side of a spiral. Put important words on the camera's side (`Math.atan2(S.e[2], S.e[0])` is the camera azimuth).
- **The swirl rotates everything glued to the surface,** ring type included. Use `arcS()` (swirl-compensated arc) for rings that must stay in front.
- Red type on red lit rings disappears: make the type cream with a red glow.
- Words on concentric orbits overlap in screen space: dim the previous word when the next one lands.
- A standing glyph close to the camera stretches badly at the frame edge; keep radii ≤ ~1.5 when the camera is at ~4 units.
- The sculpt is about 7.7k vertices per frame; it's fine for `-w 2` but don't add a second one.
- Brand/originality: the callout numbers are all marked *ejemplo*; the sculpt is an abstract displaced sphere (no eyes, tentacles or faces); no third-party names or logos; never reuse the reference lyrics or on-screen text.
