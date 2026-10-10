# Agent instructions: Terminal teaser

A dark, music-only CLI launch teaser: an accelerating stack of red `×` errors, a typed command that bursts into pixel particles which assemble into a pixel wordmark, a terminal window where a quiz is answered at the prompt and value cards stream like an agent thinking, a full-bleed red card with a slot-roll word, a pixel-block dissolve, a giant pixel number that assembles / scatters / re-forms into a countdown, a `✓` list, and a wordmark typed with a ghost cursor over `$ comenta QUIZ`. Built with HyperFrames (HTML + GSAP + one canvas). **Zero images**, no voice, no AI video.

1. Read `PLAYBOOK.md` in this folder fully before doing anything (closest older formats: `../glow-signal-film/`, `../ui-launch-reel/`).
2. Start from a copy of `template/` (`cp -R playbook/terminal-teaser/template my-teaser`). `template/script.txt` maps every beat to the on-screen copy.
3. ElevenLabs music/SFX one call at a time with `../tools/el_audio.sh` (429 backoff; the key is shared). Splice the music so its drop lands on the swarm (~6.3s) and its real outro ends the film.
4. Edit copy in the HTML sections and `ERR[]`; edit timings under each `/* ==== Sn ==== */` block; edit canvas beats in `paint(t)` (keep it a pure function of `t`).
5. `npm run check` (only the known canvas `text_occluded` false positives may remain), snapshots, render. QA the **final mp4**: ffprobe 1080x1920, volumedetect (also the first 3s), and 6+ frames you actually look at.
6. Figures with `EJEMPLO` chips and the plan names are illustrative. Replace them before posting.

Example output: `../../x-batch/jahooma.mp4` (42.3s). Reference: https://x.com/jahooma/status/2104619086579990583
