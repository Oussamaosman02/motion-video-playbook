# Agent instructions: UI launch film

This folder is a self-contained recipe for one video format: a light-canvas SaaS launch film where product UI builds itself under word-by-word captions (after the Retti V2 launch).
Read `PLAYBOOK.md` here fully before doing anything.

- Start from a copy of `template/` (HyperFrames 0.8.137 project). Shared scripts are in `../tools/`. The format-specific `tools/embed_words.py` is also in `template/tools/`.
- Audio first: TTS with timestamps → `python3 tools/embed_words.py` → re-map the word indices in the `caption(...)` groups and the `w(i)` cues.
- ElevenLabs calls one at a time, retrying on 429. Images only via treg Gemini (2 images ≈ $0.06). No AI video.
- `npm run check` must reach 0 errors. Then look at the snapshots and at frames from the final mp4 before calling it done.
- Mark invented stats/offers as "ejemplo". The overview of all formats is `../PLAYBOOK.md`.
