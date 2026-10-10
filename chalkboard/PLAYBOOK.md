# Playbook B: Chalkboard explainer

A real-looking hand writes an infographic on a green chalkboard while a voice explains it. The drawing is rendered from code (`../tools/render_chalk.py`) from two generated images: the finished board and the same board empty. Example: `../../chalk-quiz-funnel.mp4`. Project files: `template/`.

This playbook is for **any coding agent (Claude Code, Codex, …) or a human**. Commands assume you are in the folder that contains `playbook/`; shared scripts live in `playbook/tools/`.

---

## 1. Prerequisites

- `ffmpeg`, Python 3 with `numpy pillow scipy`.
- `ELEVENLABS_API_KEY` (`source <(grep ELEVENLABS_API_KEY ~/.zshrc)`).
- `treg` CLI for image generation (`../tools/gen_image.py`, ~$0.03 per image).
- No HyperFrames needed: `render_chalk.py` writes frames straight into ffmpeg.

![chalk reference](reference-frame.jpg)

Inspired by the "Chalkboard Explainer" ad format (reference: https://x.com/spwfeijen/status/2107023055532810720, a 23.6s AI video of a hand drawing a "BELLY FAT?" infographic). The original is made with AI video, which costs ~$1–5 per attempt and garbles text. **We fake it with code instead**: generate the *finished* board as one image, generate the same board *empty*, and reveal the chalk stroke by stroke under a real-looking hand. Cost ≈ $0.10 per video; re-renders are free.

## 2. What the format is

| Element | Spec |
|---|---|
| Frame | 1080×1920, 30 fps, ~20–30s. A green chalkboard with an aluminium frame on a light wall fills the frame, shot straight on |
| Board content | A title with quote marks (`¿QUIZ FUNNEL?`), a simple chalk drawing column (left), a numbered list with one small icon per item (right), a short "don't" note with a crossed-out sketch, and a bottom takeaway underlined twice |
| Motion | Elements appear in narration order. Text is written letter by letter, left to right; drawings are traced around their outline. A hand holding chalk follows the drawing point and rests off to the side during pauses, then leaves at the end |
| Audio | Casual, friendly voice (no captions, like the original), a quiet upbeat music bed, and soft chalk scratching only while writing |
| Length rule | One idea per list item, 5 items max. The voice reads the board in drawing order |

## 3. Recipe

All commands run from a copy of `template/` (`cp -R playbook/chalkboard/template my-chalk && cd my-chalk`). `T=../playbook/tools`.

**1) Script**: write `script.txt` in the same order the board will be drawn: hook → title, then the idea → drawing, then items 1–5, then the "don't", then the takeaway. Write the numbers as "Uno, … Dos, …" with **commas, not colons** (colons cause long pauses). ~70 words ≈ 27s.

**2) Voice + word timings** (we used "Sara Martin 3", Spain Spanish, upbeat female, `gD1IexrzCvsXPHUuT0s3`, at speed 1.2; at 1.05 it ran 33s):
```bash
source <(grep ELEVENLABS_API_KEY ~/.zshrc)
python3 $T/tts_with_timestamps.py script.txt . gD1IexrzCvsXPHUuT0s3 1.2      # → vo.mp3, words.json
python3 -c "import json;w=json.load(open('words.json'));print(' '.join(f'{i}:{x[0]}@{x[1]}' for i,x in enumerate(w)))"
```

**3) Finished board** (~$0.03). Spell out every word, the layout and the icons. Passing the reference video's thumbnail as a style reference gives a realistic photo look:
```bash
python3 $T/gen_image.py board_final.png 'Photorealistic vertical photo (9:16) of a real green school chalkboard filling the frame, with a thin aluminium frame and a light wall around it, shot straight on with a phone. On the board, neat hand-drawn white chalk in a clean uppercase handwritten style, like a teacher infographic. Exact text and layout, in Spanish, spelled exactly as written: Title at top in large letters with quote marks: "¿QUIZ FUNNEL?". Left column: <drawing>; below it the words "<DON'T NOTE>" and a small crossed-out <sketch>. Right column, a numbered list, each item with a small chalk icon on its right: "1. …" (<icon>), "2. …" (<icon>), "3. …" (<icon>), "4. …" (<icon>), "5. …" (<icon>). Bottom, centered and underlined twice: "<TAKEAWAY>". Realistic chalk texture, slight chalk dust, no hand, no person, no other text.' \
  "https://pbs.twimg.com/amplify_video_thumb/2107022904181346304/img/MfLC6-lZaFV-5JRr.jpg"
```
**Read the image and check every word** (accents, ¿?, numbers). Regenerate if anything is wrong; it's $0.03.

**4) Empty board** (~$0.03), as an edit of the finished one so it lines up to the pixel. Pass the URL printed in step 3:
```bash
python3 $T/gen_image.py board_empty.png "Edit this image: completely erase ALL chalk writing and drawings from the chalkboard so it is a clean, empty green chalkboard with only very faint old chalk smudges. Keep EVERYTHING else pixel-identical: same board, same aluminium frame, same wall, same camera framing, same lighting, same size and position. No text." "<board_final URL>"
```
Verify the alignment: the mean absolute difference of the outer 70–90px strips should be about 2–3 (ours: 2.3–2.8). If it isn't, erase the chalk yourself with `cv2.inpaint` on the dilated chalk mask instead.

**5) Hand** (reuse `template/hand_long_cut.png`, or make a new one for ~$0.06). It needs a **long** arm; a short one ends mid-frame. Two steps: a hand holding chalk on magenta, then an edit that makes "the forearm continue long and diagonally to the bottom-right corner, cut off by the image edges". Then:
```bash
python3 $T/cutout_poses.py . 1600 hand_long_cut=hand_long.png
```

**6) Element boxes + timing** in `config.json`. Each element is `{name, box:[x0,y0,x1,y1] in board_final px, kind:"text"|"drawing", lines, start, dur}`:
```bash
python3 $T/chalk_boxes.py board_final.png board_empty.png suggest boxes.jpg        # candidate boxes per word/icon/drawing
# … write config.json elements …
python3 $T/chalk_boxes.py board_final.png board_empty.png check config.json check.jpg  # verify every mark is covered
```
- `kind:"text"` writes letter by letter in reading order; set `lines` to the number of text lines in the box. `kind:"drawing"` traces each stroke around its center (good for icons, funnels, stick figures, underlines).
- **List icons first** in `elements`: a box earlier in the list claims overlapping pixels. That keeps an icon out of its item's text box, and the icon is drawn right after the text.
- `start` = the start of the word that introduces the element (from `words.json`), `dur` = writing time. Rules of thumb: ~0.12–0.15s per character for text, 0.4–0.9s per icon or drawing part, and never longer than the gap to the next cue. Split big drawings into parts (people → funnel → stick figure) to keep the hand moving.
- `duration` = last word end + ~1.5s.
- `geometry` maps board px to the 1080×1920 frame: `scale` = 1040 / board width in px, `ox` = 540 − board center x × scale, `oy` = (1920 − image height × scale) / 2. The wall around the board is edge-padded.
- Hand: `hand_scale` 0.58, `arm_angle_deg` 24 (the arm's tilt in the source image, used to extend it), `sprite_rotate_deg` 30 (+ makes the arm more horizontal, so it leaves through the right edge like the original).

**7) Preview, render, sound**:
```bash
python3 $T/render_chalk.py config.json prev --preview 0.4,3,8,15,22,26   # stills: prev_XX.XX.jpg
python3 $T/render_chalk.py config.json silent.mp4                         # ~75s for 28s of video
# music + chalk SFX from ElevenLabs (reuse the template's, or regenerate):
curl -s -o music.mp3 https://api.elevenlabs.io/v1/music -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"prompt":"light upbeat background music for a short social media explainer video, playful plucked acoustic guitar and soft claps, positive and calm, steady tempo, no vocals","music_length_ms":30000}'
curl -s -o chalk_sfx.mp3 https://api.elevenlabs.io/v1/sound-generation -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"close-up sound of someone writing quickly with chalk on a chalkboard, continuous light chalk scratching and tapping, no voices, no music","duration_seconds":10,"prompt_influence":0.6}'
python3 $T/mix_chalk_audio.py config.json silent.mp4 vo.mp3 music.mp3 chalk_sfx.mp3 ../my-chalk.mp4
ffmpeg -v error -i ../my-chalk.mp4 -vf "fps=1/1.2,scale=216:-1,tile=8x3" -frames:v 1 sheet.jpg   # look at it
```

## 4. How `render_chalk.py` works

1. **Chalk alpha**: `A = clip((L_final − L_empty − 18) / 45, 0, 1)`, the per-pixel strength of chalk on the finished board. A frame is `empty + (final − empty) × A × reveal(t)`, so the unrevealed board is exactly the empty board, with no seams.
2. **Draw-time map `T[y,x]`**: each element's chalk pixels are split into connected components (letters, strokes).
   - Components are ordered by reading order (text: line band, then x) or top-to-bottom (drawings).
   - Each component gets time in proportion to its ink, with a ~12% pen-lift gap.
   - Inside a component, text uses a diagonal sweep (65% top→bottom, 35% left→right), which reads as handwriting. Drawings sweep by angle around the centroid starting at 12 o'clock, which reads as tracing an outline; thin strokes use their long axis.
   - Each pixel then fades in over 60ms after its time.
3. **Pen path**: while revealing, it samples the centroid of the ink front 2× per frame. Between samples less than 0.5s apart, the hand moves linearly with a ±1.5px tremor. In longer pauses it lifts down-right (+60, +90px), rests, then eases to the next start. It enters from the right before the first stroke and exits bottom-right after the last.
4. **Hand sprite**:
   - The forearm is extended along its axis: rotate the arm vertical, repeat the widest clean row, add the real skin texture from the 120 rows above (opaque pixels only, mirrored tiles), rotate back.
   - The sprite is then rotated `sprite_rotate_deg` and scaled.
   - The chalk tip is found automatically as the top-left-most bright pixel, and the sprite is placed so the tip sits on the pen point.
   - A soft 25% shadow is offset (18, 14)px.
5. Frames are piped as raw RGB into `ffmpeg libx264 crf 17`.

## 5. Gotchas

- **Short arm**: an arm that ends mid-frame kills the illusion. Use a long-arm image, plus the extension, plus the sprite rotation.
- **Texture seams**: repeating one row looks airbrushed, and copying texture that includes edge pixels gives a sawtooth edge. Use the opaque-only, mirrored texture (already in the script).
- **Rotation sign**: PIL's `rotate(+θ)` is counter-clockwise. To make a down-right arm vertical, rotate by −θ, then rotate back by +θ.
- **NumPy 2** removed `ndarray.ptp()`; use `np.ptp(arr)`.
- Specks on the board frame show up in `suggest`. Leave them out of every box and they're never drawn.
- If a letter looks "wiped" rather than written, the `dur` is too short for that much ink; give it more time, or split the box.
- The voice should not run ahead of the board: start every element on its word, and make the title or hook element finish before the second sentence.

## 6. Cost (chalk Quiz Funnel video)

- Images: board $0.03 + empty $0.03 + hand 2 × $0.03 ≈ $0.12.
- ElevenLabs credits: ~400 characters of TTS, a 30s music bed, a 10s SFX.
- Render: ~75s on an M-series Mac.
- **Vs AI video: ~$1–5 per attempt, usually several attempts, plus garbled text.**
