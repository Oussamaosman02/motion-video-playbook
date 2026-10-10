# Agent instructions

This folder is a self-contained recipe for one video format: the frosted-glass launch film (monochrome glass UI on a window-lit grey wall, blur-in words, vertical word ticker, prompt box that types, tilted 3D tile wall, Sí/No zoom, white end card; music only). Read `PLAYBOOK.md` here fully before doing anything.
Start from a copy of `template/`. Format-specific scripts are in `tools/` (`el_audio.sh`, `splice_music.sh`, `wall_grade.py`); shared scripts are in `../tools/`. The overview of all formats is `../PLAYBOOK.md`.
Rules: images only via treg Gemini (this format needs 1); ElevenLabs calls one at a time with 429 backoff; never AI video; QA the rendered mp4 (frames + black-band scan), not only snapshots.
