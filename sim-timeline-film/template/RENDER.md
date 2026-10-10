# workersio · render instructions (NOT rendered by the worker)

```sh
cd /Users/amalio/Downloads/insta/x-batch/workersio
python3 tools/build.py        # only if you changed tools/src.html.tpl or assets/words.json (index.html is already built)
npx --yes hyperframes@0.8.137 render -o ../workersio.mp4 -w 2 --quiet
```

- Expected: **1080x1920, 38.5 s**. Light DOM + 2 canvases (one redraws per frame during 18.1–21.4 s only), no video, no images except fonts, so it should be a light render.
- Audio: VO (Bruno Torres, reused `playbook/whiteboard-ad/template/vo.mp3`) at 0.3 s → 32.9 s; music bed (reused liu8in piano/pads, refit) 0 → 38.5 s at 0.26; 45 library SFX; end chime at 36.6 s.
- Quick checks: `ffprobe` duration ≈ 38.5; `ffmpeg -ss 36 -t 2.5 -i ../workersio.mp4 -af volumedetect -f null -` should be above ≈ −40 dB mean (music tail + chime; a pre-mix measured −27 dB at 35.5 s).

## Timestamps to verify in the mp4

| t (s) | Should show |
|---|---|
| 2.4 | Headline "¿Quieres vender tu SaaS sin mandar a todo el mundo" typing; 6 gradient pills (founder, cto, marketing, agencia, freelance, curioso) staggered on the left |
| 3.4 | All pills gone into one grey "# /landing" block + red tag "6 visitas · 1 mensaje"; "misma landing?" in red |
| 7.1 | "En vez de pedir una demo, crea un Quiz Funnel." · greyed "✕ pedir_demo" pill · big orange "⚡ quiz_funnel" block + "nuevo" tag |
| 11.9 | Spine with p1–p8 (p6–p8 ghosted) + 3 question pills ¿quién eres? / ¿qué quieres? / ¿tu problema? |
| 17.2 | Orange cards (caso real, dato 4→19, consejo) between the questions + green "✓ tiene_sentido" chip |
| 19.6 | "65.536 caminos posibles", dimmed micro-grid with ONE red outlined cell |
| 22.3 | "Y lo importante:" over a 3D perspective floor of pills moving toward camera |
| 27.6 | Staircase: últimas cards → tu producto → oferta −30% → 14:5x countdown, readout "tiempo limitado 00:14:5x" ticking |
| 32.8 | Four chips all green ✓ (lead_captado, segmentado, educado, compra; compra enlarged) |
| 37.6 | "Comenta QUIZ" + dark terminal "$ comenta QUIZ" with 3 lines + SAAS [IN] HOUSE lockup; fades to white in the last 0.5 s |

Also watch: words in the headline appear on the spoken word (captions = what Bruno says); the top-right `t+00:xx.xx` clock runs the whole film.
