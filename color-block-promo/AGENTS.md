# Agent notes: colour-block promo

You are making a **music-only, kinetic-text promo**: one flat colour per beat, a heavy grotesk label, and one small code-built UI vignette per beat. Transitions are iris, diagonal wipe and whip-slide, cut on the music. It ends with a card collage and a logo end card with a cursor click. Read `PLAYBOOK.md` first.

- Start from `template/` (HyperFrames 0.8.137, a single `index.html`). Don't add AI video or generated images unless a beat really needs an illustration.
- Audio: generate the music first (ask for bpm + "brief stop" breaks), find its drop/breaks with an RMS print, and put the big reveals there. Trim and fade it with ffmpeg; never tween `<audio>` volume. Run ElevenLabs calls **sequentially** with `tools/el_audio.sh` (it retries on 429).
- No narration: the script is on-screen text. Keep labels to ≤ 6 words per line and give each line ≥ 1s on screen.
- Scenes overlap by ~0.5s on alternating tracks 1/2, with later sections on top. Use `enter()`/`leave()`/`words()`/`drift()`/`click()` from the template.
- Name fonts distinctly (never `"Serif"`). Check the **rendered mp4** frames, not only snapshots.
- The `content_overlap` errors from `npm run check` on stacked cards and swaps are expected. Verify them visually.
- Mark invented stats and offers as "ejemplo".
