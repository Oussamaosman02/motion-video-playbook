# Agent instructions: paper-desk film (format L, music only)

Read `PLAYBOOK.md` in this folder fully before doing anything.
Start from a copy of `template/` (HyperFrames 0.8.137 project: `index.html`, `script.txt`, `assets/` = desk plate, prop cut-outs, Fraunces + JetBrains Mono, music, SFX; `src/props.png` = the uncut prop sheet).
Shared scripts are in `../tools/`: `gen_image_ar.py` (Gemini via treg, 9:16 default), `cutout_grid.py` (magenta sheet → props), `el_audio.sh` (ElevenLabs music/SFX, sequential, 429 backoff; the key is shared, never call it in parallel).
Rules: no AI video; ≤ ~$0.40 of images; keep `ejemplo` labels on invented numbers; never present generated people as real customers; check every SFX with volumedetect; QA frames from the final mp4.
Key helpers in `index.html`: `proj()` (plane → screen), `stamp()`, `land()`, `pan()`, `cap()`.
