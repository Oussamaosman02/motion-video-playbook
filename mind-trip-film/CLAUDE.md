# Agent instructions: Mind-trip film

Wordless (music-only) vertical film: a hand-drawn block mascot walks on paper, the camera dives through its eye into a starry inner world, a montage of procedural "wonders" (orbits, neuron, DNA, prism, sunflower, black hole, countdown rings, light beam, earthrise) carries one script beat each as handwritten on-screen text, then an iris opens back onto the paper with the mascot happy and the brand.

1. Read `PLAYBOOK.md` in this folder fully before doing anything (recipe, beat map, gotchas).
2. Start from a copy of `template/` (HyperFrames 0.8.137 project, everything is SVG + GSAP in `index.html`; no images, no TTS).
3. Keep everything deterministic (seeded `rnd()`, no `Math.random`/`Date.now`); one paused timeline in `window.__timelines["main"]`.
4. Invented numbers keep an `EJEMPLO` tag; never present anyone as a real customer.
5. Audio is reused (see PLAYBOOK §4). If you generate new music, use `../tools/el_audio.sh` (sequential, 429 backoff; key is shared).
6. QA the final mp4: ffprobe 1080x1920, volumedetect, extract 8+ frames and look at them.
