# Agent instructions: device mockup film

This folder is one format of the low-cost vertical video playbook: CSS 3D phones / laptops / tablets showing your product UI over dreamy Gemini photo backdrops, dot-matrix LED statements on brand-colour REC slides, dark HUD scenes with a giant grey word, and an inflated-surface logo outro. Music only, no AI video.

1. Read `PLAYBOOK.md` fully before doing anything.
2. Start from a copy of `template/` (HyperFrames 0.8.137 project). Never edit the template in place.
3. Format-specific scripts are in `tools/` (`gen_backdrops.sh`, `prep_images.py`, `el_audio.sh`); shared ones are in `../tools/`.
4. ElevenLabs calls must stay sequential (429 backoff is built in). Keep image spend ≈ $0.20.
5. QA the final mp4 (ffprobe 1080x1920, volumedetect, frames pulled from the mp4) before calling it done.
