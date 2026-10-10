# Agent instructions: Whiteboard ad

This folder is a self-contained recipe for one video format: a hand writes an icon list on a white board in marker, then a second hand holds up a phone with live SaaS in House UI (ticking countdown). Read `PLAYBOOK.md` here fully before doing anything.

- Start from a copy of `template/` (config, images, audio, fonts, `prompts.md`).
- Format-specific scripts are in `tools/` (`render_whiteboard.py`, `phone_ui.py`, `key_sprite.py`, `erase_board.py`, `tighten_gaps.py`, `whiteboard_boxes.py`, `gen_image_916.py`, `mix_whiteboard_audio.py`). The shared `../tools/tts_with_timestamps.py` makes the voice.
- No AI video. Images only via treg Gemini (~$0.03 each; this format needs 3, or 0 if you reuse the template hands and only regenerate the board).
- Make ElevenLabs calls one at a time with a 429 retry loop.
- QA the final mp4: 1080×1920, volumedetect on the whole file and on the reveal hold, and look at ≥6 frames.
- The overview of all formats is `../PLAYBOOK.md`.
