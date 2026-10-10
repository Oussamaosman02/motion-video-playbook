# Prompts used (feijen-whiteboard)

## Finished board — gen_image_916.py (9:16), style ref = tweet thumbnail
Photorealistic vertical phone photo (9:16) of a clean white dry-erase whiteboard that fills the ENTIRE frame edge to edge (no frame, no wall visible), shot straight on, soft natural daylight with a gentle brighter glare at the top and slight grey falloff toward the bottom corners, like the reference. On the board, neat hand-written uppercase text in thin black dry-erase marker, casual hand-lettered style like the reference (not a font), plenty of white space, everything left-aligned starting about 15% from the left edge. Exact content top to bottom, Spanish, spelled exactly:
Row 1 (top, around 9% height, largest letters): "QUIZ FUNNEL" with one straight underline below it.
Row 2: the word "DEMO" with a single horizontal line striking through it, then an arrow "→", then a small simple funnel icon.
Row 3: a small speech bubble icon with a question mark inside, then "→ 5-8 PREGUNTAS".
Row 4 (smaller letters, indented under row 3 text): "¿QUIÉN ES? ¿QUÉ QUIERE?".
Row 5: a small icon of two stacked cards, then "→ CASOS Y DATOS".
Row 6: a small target / bullseye icon, then "→ RESULTADO A MEDIDA".
Row 7: a small alarm clock icon, then "→ OFERTA + CONTADOR".
Row 8 (around 85% height): "SEGMENTA → EDUCA → VENDE" with a hand-drawn oval circled around the word "VENDE".
Icons are simple black line drawings, same marker. Rows evenly spaced. No hand, no marker, no person, no watermark, no logo, no other text.
Style ref: https://pbs.twimg.com/ext_tw_video_thumb/2083148272097447936/pu/img/uasngR1nLNYclMyq.jpg

## Writing hand — IMG_SIZE=2:3
Photorealistic photo of a real man's right hand writing with a black dry-erase marker (Sharpie-style black marker with white label), seen from behind/above as if writing on a whiteboard facing the camera. The marker points to the upper-left, its black felt tip at the top-left of the hand. The hand comes from the lower right: wrist and a long forearm covered by a dark charcoal-grey cotton sweatshirt sleeve that continues diagonally all the way to the bottom-right corner of the image and is cut off by the image edge. Natural skin, soft daylight. Isolated on a perfectly flat solid magenta (#FF00FF) background, no shadow on the background, no board, nothing else.

## Phone hand — IMG_SIZE=2:3
Photorealistic photo of a real man's left hand holding up a modern black smartphone (thin bezels, rounded corners) perfectly upright and facing the camera straight on, the screen is a perfectly flat uniform pure green (#00FF00) with no reflections, no notch content, no UI. The hand grips the phone from the lower-left side, thumb on the left edge, like showing a product to the camera. The wrist and forearm, in a dark charcoal-grey cotton sweatshirt sleeve, continue diagonally down to the bottom-left corner and are cut off by the image edge. The phone is in the upper-center of the image and occupies about 45% of the image width. Soft daylight. Isolated on a perfectly flat solid magenta (#FF00FF) background, no shadow on the background, nothing else.

## ElevenLabs
- Voice: Bruno Torres SKjgN71N3MeGl4r2JbRt, speed 1.1 (eleven_multilingual_v2 via ../tools/tts_with_timestamps.py)
- /v1/music (38000 ms): "light upbeat background music for a casual social media ad, warm lo-fi hip hop beat with soft keys and a gentle bass, positive and modern, steady tempo, no vocals"
  The track has its own outro from ~31s, so build the bed: music[0:28] crossfaded (1.5s) into music[14:28] → music_bed.mp3:
  ffmpeg -i music.mp3 -filter_complex "[0:a]atrim=0:28,asetpts=PTS-STARTPTS[a];[0:a]atrim=14:28,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=1.5[m]" -map "[m]" music_bed.mp3
- /v1/sound-generation 10s, influence 0.6: "close-up sound of someone writing quickly with a dry-erase marker on a whiteboard, continuous soft felt-tip squeaks and strokes, no voices, no music"
- /v1/sound-generation 1s, influence 0.5: "soft quick whoosh of a phone being raised into view, subtle, short"
