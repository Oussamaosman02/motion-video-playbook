# Format: Sim-timeline film (voice)

A clean, light "systems diagram in motion" short in the motion language of @workersio's launch film "Introducing Workers IO" (https://x.com/workersio/status/2107923334134710653, 45.4s, 16:9 4K, music only, ~25K views / 386 bookmarks on day 1). That film shows a distributed-systems simulator: operation pills (`1 put x`, `2 get x`) on a dotted white canvas, a run branching into millions of futures, faults injected into timelines, and a bug found and replayed. We kept the **visual grammar** and rebuilt everything else: our Quiz Funnel script, our labels, brand red instead of their orange, 9:16, a voice.

Example: `../../x-batch/workersio.mp4` (38.5s, 1080x1920, rendered by the coordinator). Project: `../../x-batch/workersio/`.

Use it when the message is a **process or pipeline** (steps, branches, "what happens next"), and you want it to look like a calm, precise dev-tool. It's the light, engineering-flavoured cousin of the UI launch films (Part F) and the terminal teaser (N).

## What makes it distinctive
| Element | Original | Our build |
|---|---|---|
| Canvas | Off-white, faint dot grid, no chrome | `#dots` radial-gradient dots 54px; `--bg #fbfbfc` |
| Operation pill | `[number badge | mono label on a light→saturated gradient] + small orange square cap`, soft drop shadow; blue/purple/green | `pill()` factory + `.blue/.purple/.green/.grey/.orange` colour vars; the cap is brand red `#e8382d` |
| Pill entrance | Cap appears first, body unrolls out of it | `grow(id, at)`: cap `scale 0→1` (back.out), then `.body` `clip-path inset(0 0 0 100%) → 0` |
| Fault / special block | Big orange "⚡ partition" block that pushes into a timeline | `.pill.big.orange` "⚡ quiz_funnel", "⚡ tu producto", dropped in from above |
| Headline | Top-left, medium-weight grotesk, typed word by word, one or two accent words in orange | `typed(host, from, to, accentIdx)` on the VO word times, Archivo 600 64px, accent = brand red |
| Branching | Vertical spine with `#hash` rows, fault pills attached to rows | S4/S5: spine + `# p1…p8` (p6–p8 ghosted = "5 to 8"), question pills on even rows, orange cards injected on odd rows |
| Futures | "64 futures" → "2,097,152 futures", grid of micro-pills densifies, one red cell | `<canvas>` redrawn from a tween proxy `{k, dim}` (seek-safe), 8→64 columns, counter in powers of 4 up to 65.536, then dim + red outlined cell + zoom ×9 into it → "★ tu resultado" |
| 3D floor | A perspective plane of pill rows racing toward camera | `#s7-floor` `rotateX(66deg)` with a canvas drawn once at load, translateY tween; white fog gradient on top |
| Virtual time | Mono readout `virtual time 00:00:10.982` | Top-right `t+00:xx.xx` clock over the whole film + "tiempo limitado 00:14:59.00" countdown in S8 |
| Checks | Row of `● name` chips turning green ✓ (and one red ✗) | S9: 4 big chips (lead_captado, segmentado, educado, compra) go green on the VO words |
| Issue terminal | Dark card with `$` command + numbered lines, one highlighted red | CTA: `$ comenta QUIZ` typed char by char + 3 lines, last one highlighted |
| End | Orange square → logo lockup | Red cap pops over the IN badge → SAAS [IN] HOUSE lockup |

## Beat table (Bruno Torres VO, 32.7s, cut hard on the first word of each sentence)
| Film t | Words | Visual |
|---|---|---|
| 0–3.7 | ¿Quieres vender… misma landing? | 6 audience pills arrive, then all collapse into one grey `# /landing` + red tag |
| 3.7–4.7 | Haz esto. | One big orange pill grows out of its cap |
| 4.7–7.4 | En vez de pedir una demo, crea un Quiz Funnel. | `pedir_demo` gets a red ✕ and greys out; `⚡ quiz_funnel` drops in |
| 7.4–12.5 | Primero, entre cinco y ocho preguntas… | spine p1–p8, 3 question pills on quién / quiere / problema |
| 12.5–18.1 | Entre medias, cards… esto tiene sentido. | orange cards injected between the questions; green ✓ `tiene_sentido` |
| 18.1–21.4 | Después, un resultado personalizado… | futures grid → one red cell → zoom → `★ tu resultado` |
| 21.4–22.7 | Y lo importante: | 3D pill floor + `! importante` |
| 22.7–28.0 | las últimas cards… tiempo limitado. | staircase: últimas cards → producto → oferta −30% → countdown |
| 28.0–33.1 | Así no solo captas el lead. Lo segmentas… compra. | 4 chips turn green one by one |
| 33.1–38.5 | (CTA, no VO) | "Comenta QUIZ" + terminal + lockup + chime |

## Recipe (≈ $0 images, 0 ElevenLabs calls)
1. **Audio (all reused):** VO `playbook/whiteboard-ad/template/vo.mp3` (Bruno Torres) with its own `words.json` (ElevenLabs alignment; it matches the file length, 32.68s). Music: `x-batch/liu8in/project/assets/music.mp3` (piano/pads) refit with `../tools/fit_music.sh in out 38.5 3.0-36.0 24.0-36.5` (`XF=1.0 FADE=2.5`); this skips the 3.5s quiet intro and keeps the bed alive under the CTA (the source dies at 38s). SFX copied from `sih-trace-film/assets` (blip, chime, whoosh, alert) and `x-batch/jordan/assets` (tick, key, pop, glitch, impact), normalised with `FIX=1 INPLACE=1 ../tools/sfx_normalize.sh` (alert and tick were −34 dB).
2. **No images.** Everything is DOM + 2 canvases. The only brand asset is the text lockup.
3. **Build:** edit `template/tools/src.html.tpl` (scenes, labels) and the `SFX` list in `template/tools/build.py` (word-index cues), then `python3 tools/build.py` → `index.html`. A new voice = new `assets/vo.mp3` + `assets/words.json` (`[[word, start, end], …]`) + re-check the word indexes used in `C`, `typed()` ranges and `SFX`.
4. `npm run check` (0 errors; the overlap infos in S1 are the intentional collapse) → `npx --yes hyperframes@0.8.137 snapshot --at … --describe false` → render with `-w 2`.

## Gotchas
- **`src.html` must not sit in the project root**: `check` sees two `data-composition-id` roots ("multiple_root_compositions", duplicate audio). Keep the template at `tools/src.html.tpl`.
- **Don't tween `className` or `textContent` with `tl.set`** (GSAP 3 dropped className tweens; text sets are not reliably seek-safe). Use overlay elements that fade (the red ✕ badge, the green chip background `.okbg`, the ✓ `.tick`) and `onUpdate` proxies for counters.
- **Canvas hash must be unsigned**: `(x ^ (x >>> 16)) / 2**32` can go negative → `COLS[-1]` is undefined → `fillStyle` silently keeps the previous colour (the grid came out half red). Use `>>> 0`.
- At 64×64 the micro-grid cell is 14px: the "found" cell is invisible unless you add an outline box + solid fill once the grid dims.
- At first the 84px pills looked lost in the 1080×1920 frame (lower half empty). Use 106px pills / 176px big blocks, and spread rows to y≈1650.
- The IN badge failed contrast at 2.71:1 with cream text mid-animation; white text passes.
- Don't copy the original's brand: no logo, no hash strings, no "partition/put/get" labels. Our labels are about the funnel.

## Cost
Images $0 (0 calls). ElevenLabs 0 calls (VO, music and SFX all reused). Render: light (no video layers).
