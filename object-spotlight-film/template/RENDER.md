# minchoi-c: render notes (do NOT render in parallel)

```sh
cd /Users/amalio/Downloads/insta/x-batch/minchoi-c
python3 tools/build.py            # only if tools/index.src.html changed (index.html is already built)
npx --yes hyperframes@0.8.137 render -o ../minchoi-c.mp4 -w 2 --quiet
```

- Expected: 1080x1920, **57.0 s**, VO from 0.3 s to ~51.6 s, then music + click/chime CTA to the end (music is lifted after the VO, so the last 3 s are not silent).
- `check`: 0 errors. 1 warning (file length) is expected. Canvas + 3D CSS + grain makes the first frame slow ("render-ready within 3000ms" warning in check). It is harmless.

## Timestamps to verify in the mp4
| t (s) | Should show |
|---|---|
| 1.2 | Field of identical "landing" monuments on a warm-horizon floor; mono caption "¿Quieres vender tu SaaS sin mandar"; VO audible from 0.3 s |
| 3.4 | Giant cropped slam "A LA **MISMA** / LANDIN(G)" over the field |
| 4.6 | Field dark, ONE monument under a spotlight cone, serif "Haz esto." (spot clunk at 3.83) |
| 8.8 | Paper flash: black "**Q**UIZ / FUNNEL" with outline echoes cropped below |
| 13.2 | 3D question blocks descending, "¿QUIÉN?" slam, "PROFUNDIDAD · P.05 / 08", "5–8" |
| 23.8 | Laptop glowing in the dark, 4 cards on screen (CASO REAL / DATO / RESULTADO / CONSEJO, all "ejemplo") |
| 28.3 | Screen collapsed to a line/spark (screen-off sfx) |
| 31.7 | Red-curtain stage, spotlight on "TU RESULTADO" card + red PERSONALIZADO stamp |
| 33.8 | Light burst + cropped "IMPORTANTE" slam (music drop + boom) |
| 44.6 | Grid of countdown timers (the counter multiplies) |
| 51.6 | Serif statement "*Lead* → *compra*" (1) with footnote |
| 55.5 | Red "↻ Comenta QUIZ" button clicked, SaaS IN House lockup, chime audible |
