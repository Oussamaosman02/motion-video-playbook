# Agent instructions: mascot-cast-film

You are making a **Mascot cast film**: a music-only 9:16 launch film where code-built SVG mascots (flat shapes + googly eyes) and two-line masked captions (ink + brand-red accent) tell the story over phone/card UI and two Gemini photo backdrops.

1. Read `PLAYBOOK.md` in this folder (and `../ui-launch-film/PLAYBOOK.md` for the UI parts).
2. `cp -R playbook/mascot-cast-film/template my-film`, edit captions (`cap(...)`), UI copy and the `DESK` array in `index.html`; cues are absolute seconds.
3. Images only via `../tools/gen_image_ar.py` (Gemini, ~$0.03 each). No AI video. ElevenLabs only via `../tools/el_audio.sh` (sequential, 429 backoff), or reuse existing music/SFX.
4. `npm run check` (0 errors), snapshots, render, then extract frames from the final mp4 and look at them.
5. Keep "ejemplo" on invented numbers; mascots are lead types, never presented as real customers.
