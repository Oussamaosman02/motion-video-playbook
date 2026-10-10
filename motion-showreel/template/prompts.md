# Generation prompts (Gemini 3 Pro Image via treg, ~$0.03 each; playbook/tools/gen_image_ar.py)

smoke.jpg (--ar 9:16, then ffmpeg scale/crop to 1080x1920):
Dark cinematic background plate for a motion-design showreel: soft wisps of deep crimson red smoke and haze slowly drifting over an almost black background (#0b0b10). Mostly dark, the smoke is subtle, concentrated in the upper-left and lower-right areas, faint warm ember glow in the smoke, fine film grain. Vertical. No text, no objects, no people, no logos.

emblem.png (--ar 1:1, then playbook/tools/cutout_grid.py gen/emblem.png assets 620 emblem):
A single glossy 3D app-icon style emblem: a thick rounded-square tile made of glossy red enamel (#e8382d) with a bold cream-white pixel-art question mark embossed on its face, warm orange rim light and a soft inner glow, slight three-quarter tilt, premium photoreal 3D render. Centered with a lot of empty margin around it. Background: perfectly flat solid pure magenta #FF00FF. No shadow, no text, no other objects.

Audio (playbook/tools/el_audio.sh, sequential):
music  assets/music.mp3  "punchy modern motion-design showreel track at exactly 128 BPM, dark cinematic electronic, tight four-on-the-floor kick, sharp claps, deep sub bass, glitchy risers into drops every 8 bars, energetic and confident from the first beat, a big impact hit and short glowing synth tail ending at 32 seconds, no vocals"  33000
sfx    assets/sparks.mp3 "bright crackling fire sparks burst, short ember sizzle" 1.2
sfx    assets/riser.mp3  "short fast tension riser swell into a hit, cinematic" 1.5
Reused (copied from earlier templates): whoosh, tick, pop (+24 dB), click, chime (color-block-promo), glitch, impact (brand-film).
