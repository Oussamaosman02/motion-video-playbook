# Agent notes: brand-identity film (music only)

You are making a **"brand guidelines come to life"** launch film: logo built from pixel blocks, palette swatches with names + hex, a cropped type specimen whose line swaps sans → italic serif, a card that opens onto a flat-vector illustrated world, a mosaic wall of cards, a mascot drawn as line art then in colour (beaming results down), an icon grid, a laptop over the landscape, a studio triptych, product lockups over each landscape and an end lockup. Read `PLAYBOOK.md` first (anatomy table, recipe, gotchas).

- Start from `template/` (HyperFrames 0.8.137, single `index.html`). No AI video. Images only via treg Gemini (`playbook/tools/gen_image_ar.py`, sequential): 3 landscapes + 1 "inside" scene with one shared STYLE string (`template/prompts.md`) + 1 mascot on magenta. ≈ $0.18.
- Translucent mascot (glass, bubble): cut it out with `tools/fix_glass_cutout.py`, not `cutout_grid.py` (that leaves grey holes inside the glass).
- Music only, script as on-screen "brand copy" (≤ 6 words per line). Reused bed: `playbook/airy-launch/template/assets/music.mp3` (lift at 19.25s, fade from 40s). If you call ElevenLabs, use `playbook/tools/el_audio.sh` sequentially (shared key, 429 backoff).
- Signature moves to keep: the sans → serif swap (two stacked copies, blur crossfade), spec labels in Silkscreen (`ARCHIVO HEAVY 100% / −4%`), palette swatches that carry content (here: the quiz questions), the card that shrinks into the centre tile of the mosaic (`tiles[12]` must match it), the beam that drops result cards.
- Keep specimen drift offsets small (≤ 220px) so the hook reads; serif lines ≤ ~126px for 20 characters.
- Mark every invented number/offer with the `.ex` "ejemplo" chip. No generated people; never present anyone as a real customer.
- `npm run check`: `content_overlap` on intentional layers (mosaic dim + quote, sans/serif stacks) is expected; verify visually. Always QA frames from the **final mp4**.
