# Agent notes: notch-teaser format

Read `PLAYBOOK.md` in this folder first. In short:
- Format: a Mac-style launch teaser over an impressionist painting. Blur-in white text, a slot-machine roll list with icons, a chaotic desktop, then the notch grows into a product pill and drops into the product UI, ending on a checklist and the wordmark. Music + SFX only, no voiceover, no AI video.
- Start from `template/` (HyperFrames 0.8.137). Tools: `tools/gen_image.py` (Gemini via treg, `SIZE` env, default 9:16) and `tools/el_audio.sh` (sequential ElevenLabs music/SFX with 429 backoff).
- Keep image spend ≤ ~$0.40 (this format needs 2 images ≈ $0.06).
- Never tween `top/left/margin/fontSize` (the linter rejects them): use `x/y/scale/xPercent`. Set initial `scaleX` with `tl.set` rather than CSS `transform`.
- Pre-blur the backgrounds in PIL (`*_blur.jpg`). Do not use a CSS blur on full-frame images.
- QA the final mp4: ffprobe 1080x1920, volumedetect on the mp4 and on every SFX, and look at 6+ extracted frames.
- Do not edit `../tools/` or `../PLAYBOOK.md` from a format task.
