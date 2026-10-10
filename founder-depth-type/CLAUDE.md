# Agent instructions

This folder is a self-contained recipe for one video format: a founder talking-head made from ONE generated photo (no filming, no AI video), with depth type (words behind the head via a local background-removal cutout), Figma-style red selection highlights, a cheap lip-flap (mouth patch driven by the voice envelope), paper UI inserts, a desk + curved card wall, and a brace end card.
Read `PLAYBOOK.md` here fully before doing anything.
Start from a copy of `template/` (edit `index.tpl`, then run `python3 build.py` to produce `index.html`). Format-specific scripts are in `tools/` (`gen_image_ar.py`, `mouth_patch.py`, `tts_retry.py`); shared scripts are in `../tools/`. The overview of all formats is `../PLAYBOOK.md`.
ElevenLabs keys may be shared with other agents: never call it in parallel; `tools/tts_retry.py` backs off on HTTP 429.
