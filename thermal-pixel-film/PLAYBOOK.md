# Format U: Thermal pixel film (voice)

An art-film short in the style of @jordanarchivess's "how do you communicate that you're going through a change?" (https://x.com/jordanarchivess/status/2107536262894915762, 20.4s, 4:3, 428K views). We kept its motion language and rebuilt everything else: our quiz-funnel script, original assets, 9:16.

Example: `../../x-batch/jordan.mp4` (28s, 1080x1920). Project: `../../x-batch/jordan/`.

## What makes it distinctive
| Element | Original | Our build |
|---|---|---|
| Paper | Off-white paper, heavy film grain, a vignette that breathes from white to pink-dark | `.paper` radial gradient; 3 grain PNGs swapped and shifted every 1/12 s (`mix-blend-mode: overlay`); `#s1-vig` closes in |
| Type | Tiny lowercase geometric sans, typed word by word; one huge word slides past on a dashed line; a white bar cursor after single words ("action. \|") | Archivo 700, 44–66px, blur-in on each VO word; `typed()` + `blink()` helpers |
| Hand marks | Grey and red scribbles draw over the text, ink comet streaks | SVG paths with `pathLength=1` and stroke-dashoffset; blurred thick dash for comets |
| Flare | A cyan → blue concave 4-point star sweeps in from the left edge | One SVG path + radial gradient + drop-shadow |
| Thermal | A profile and a hand in false-colour heat (orange/yellow core, red edge) on black | Gemini photo → `npx hyperframes remove-background` → `tools/thermal.py` (alpha mask, blurred core + luminance → 5-stop heat ramp) plus a flat shadow version for paper scenes |
| Pixel objects | A ring of 16-bit objects rotates, flattens into a row, breaks apart; ink blots swallow most of them | 11 original pixel icons from ONE magenta sheet (`cutout_grid.py`); a ring counter-rotated so icons stay upright; fixed scatter spots; `brightness(0)` + blurred blobs = ink |
| Close-ups | Black or white card: one big object + red star + one word + cursor | `c1`/`c2`/`c3` scenes, cut on the VO word |
| Letters | L O V E scattered around a hero object, colour flashes (black, red, paper); red scribble circles around letters at the end | L E A D around heart → target → mail → coin; Q U I Z with red circles as the CTA |

## Recipe (≈ $0.09 images, 6 SFX calls, VO reused)
1. Script: reuse an existing VO (here `sih-quiz-film/assets/vo.mp3`, 26s) and get word times with local `npx hyperframes transcribe` (whisper). Map **one beat per sentence** and cut hard on the first word of each sentence.
2. Images (`../tools/gen_image_ar.py`):
   - icon sheet `--ar 4:3`: "4×3 grid of 12 separate chunky retro pixel-art icons … flat pure magenta … no text, no logos, no brands" → `cutout_grid.py sheet.png assets 420 names…`. **Drop anything that copies a famous game item** (we dropped a "?" block);
   - profile photo and hand photo `--ar 3:4` on pure black → `remove-background` → `tools/thermal.py cut.png thermal.png shadow.png`.
3. SFX (ElevenLabs, sequential): ink splat, flare shimmer, soft key press, pencil scribble, sub boom, 8-bit blip. Then run `../tools/sfx_normalize.sh` with `FIX=1 INPLACE=1`: the ink splat came back at −57 dB.
4. Build from `template/`: replace `__WORDS__`-style data (`words_inline.txt` → `const W`), retime the `SC` scene table by word index, and swap the copy.
5. `npm run check` → `snapshot --at …` → render with `-w 2`. Then check frames from the mp4.

## Gotchas
- A container with an inline `opacity: 0` hides `typed()` words forever (the CTA subtitle went missing this way). Only the spans animate.
- The big slide-by word and the small sentence overlap: show the sentence only after the slide (`#s1-line` fades in at 0.72s).
- A highlighted word in white disappears on paper. Use red, or darken the vignette first.
- Random scatter clumps icons and drops blots on the heroes and the countdown. Use fixed spots that avoid the hero zone and the caption band, and shrink the inked icons before the counter shows.
- The thermal threshold on a "black" Gemini background leaks (the background is ~5–8% grey). Always mask with `remove-background`.
