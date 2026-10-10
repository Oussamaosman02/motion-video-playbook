# Agent notes: motion showreel (format L)

You are making a **music-only "motion designer showreel"**: a dark red/black film inside a camera-viewfinder HUD (brackets, ● REC, running timecode, `30 FPS / 128 BPM`, numbered chapter label), where every 2-bar chapter shows off one motion technique while carrying one beat of the script as on-screen text. Read `PLAYBOOK.md` first (beat map, recipe, gotchas).

- Start from `template/` (HyperFrames 0.8.137, single `index.html`). No AI video. Images only via treg Gemini (`playbook/tools/gen_image_ar.py`): a 9:16 smoke plate and one 3D brand emblem on magenta (`playbook/tools/cutout_grid.py`), ~$0.06 total.
- **Music first**: ask ElevenLabs for an exact BPM (128) with drops every 8 bars and a final hit; read the loudness curve with `tools/music_rms.py`; cut every scene on a bar line (`BAR = 1.875`). Quiet "proof" beats go in breaks, the lockup on the final hit. Run ElevenLabs calls **sequentially** with `playbook/tools/el_audio.sh` (shared key, 429 backoff).
- One idea + one technique per chapter, nothing repeated: RGB-split collapse, 3D tunnel fly-through, spring physics, card + heart burst, bars → dots → line morph, 8-tile kinetic grid, beat-pulsing countdown ring, rolling counters, lockup with sparks.
- Chapter labels (`CH` array) name the funnel step, so the HUD also tells the story.
- Use the helpers: `sparks()`, `shake()` (on each scene's `.cam`), `glitchIn()`, `words()`, `.rgb` ghosts, `.roller` letters, proxy-driven timecode/countdown (seek-safe).
- Keep big type ≤ ~116px for 15-char lines and ≤ 150px for 10-char words; check frame edges.
- Mark invented numbers and offers with the `.ex` "ejemplo" chip. Never present generated people as customers (this format uses none).
- `npm run check`: ~8 `content_overlap` errors from tight sans/serif line stacks are expected; verify them visually. Always QA frames from the **final mp4**, including mid-spring moments and the gold flash frame.
