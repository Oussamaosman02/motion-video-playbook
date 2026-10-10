# aura-kinetic-film · agent notes

Narrated SaaS film on an airy off-white ground with a rising colour aura; every sentence is a small UI moment (pill rolodex, prompt box + cursor click, Thinking→Ready cards, avatar ring, phone with offer + countdown, coin sweep), plus colour-flood and deep-slam beats. Read `PLAYBOOK.md` first.

- Project: `template/` (HyperFrames 0.8.137, single `index.html`). **Edit `template/work/index.src.html`, not `index.html`**; rebuild with `python3 work/build.py` (words from `work/transcript.json`, SFX cue list in `build.py`, VO offset `VO = 0.3`).
- New VO: copy it to `assets/vo.mp3`, `npx --yes hyperframes@0.8.137 transcribe assets/vo.mp3` → `work/transcript.json`, then remap every word index in the scene code (`C`, `kin`, `QS`, `CARDS`, `HDR`, `VAT`, captions `CH`).
- Re-skin: `.aura`, `.flood`, `.deep`, `.acc`, `.salary` gradients + `--red` tokens.
- Loop: `npm run check` (0 errors) → `npx --yes hyperframes@0.8.137 snapshot --at … --describe false` → look → fix. Render one at a time: `npx --yes hyperframes@0.8.137 render -o out.mp4 -w 2 --quiet`.
- Rules: children toggled with opacity (never visibility) inside scenes; animate transforms only; keep everything original (CSS initials avatars, own coins, no third-party logos/faces).
- `tools/build.py` = the generator (same as `template/work/build.py`).
- Reference frames: `frames/`.
