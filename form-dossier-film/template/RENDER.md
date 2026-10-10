# minchoi-b · Form dossier film — render notes

**Do not render in parallel with other projects.** From this folder:

```sh
npx --yes hyperframes@0.8.137 render -o ../<slug>.mp4 -w 2 --quiet
```

- Expected: **1080x1920, 46.0 s**, music-only (script as on-screen text), no VO.
- Audio: `assets/music.mp3` = saivion bed (`x-batch/saivion/project/assets/music.mp3`), fitted with
  `FADE=2.5 playbook/tools/fit_music.sh work/music_src_saivion.mp3 assets/music.mp3 46 0-38.5 30-end` (last 3 s −17.9 dB).
  SFX reused (stamp/paper/ding from dzhng, scribble/key from jordan, type/thump/whoosh/click/blip/glitch from kinetic-hud-film). 0 ElevenLabs calls.
- After the render: `bash ../../playbook/tools/audio_check.sh ../<slug>.mp4` (opening + ending must not be silent; ding at 44.65 s).

## Timestamps to check in the mp4

| t (s) | Should show |
|---|---|
| 0.5 | Cream FORM L-01 sheet, "¿LA MISMA / LANDING PARA / TODOS?" slamming in; music + thump audible from the first frame |
| 3.6 | Question typed on ruled lines, 4 checkboxes ticked with X |
| 4.6 | Red "SIN SEGMENTAR" rubber stamp on the form, then FORM Q-01 feeds in from below (previous sheet dims, not black) |
| 8.8 | "HAZ ESTO.", "pedir una demo directamente" struck in red, red ✓ "UN QUIZ FUNNEL", "APROBADO" stamp fully inside frame |
| 15.6 | Network diagram lit red layer by layer, 3 outputs (¿quién es? / ¿qué quiere? / ¿su problema?), "SEGMENTA" flipping from mirrored to readable |
| 22.6 | Crossed-out P1→P4 chain + "aburrido…", new flow with red cards, handwritten «vale, esto tiene sentido» |
| 23.3 | Black vertical cage bars dropping over the paper |
| 26.4 | Dark terminal: probability table (founder-b2b 0.64 … ejemplo), prompt typing "founder B2B" with red caret |
| 35.4 | FORM C-04 milestone schedule: ENCAJE, OFERTA −30% filled red diamonds, CONTADOR odometer 14:59 |
| 41.6 | "ASÍ NO SOLO CAPTAS EL LEAD." checklist ×3, "SaaS in House" signature, "LISTO PARA COMPRAR" stamp, ARCHIVADO tab |
| 45.6 | End card: COMENTA / QUIZ (red), "y te enseño cómo montarlo.", "POR DM" stamp, SaaS in House; music + ding audible to the end |
