# Format: aura-kinetic-film (narrated SaaS film on an airy glow, every phrase is a UI moment)

Reference: https://x.com/RoundtableSpace/status/2080967546266902913 (repost of a 49.8 s 16:9 narrated launch film for an "AI employees" builder,
"one-shotted by Claude Opus 5 in 19 minutes"). First built as `x-batch/roundtable/` (55.6 s, Spanish, SaaS in House, Quiz Funnel script).

## What makes it distinctive
- **Three grounds only**: airy off-white with a big soft **colour aura rising from the bottom** (most beats), a **full colour flood**
  (opening + bookend), and a **deep slam** (dark radial with a hot glow at the bottom) for one-word punches.
- **Every word lands with blur → sharp + a small rise** (no typewriter for headlines). Key word in an accent gradient. A giant ghost
  word sits blurred behind the flood beats.
- **Each sentence becomes a tiny product moment**: pill rolodex ("Meet your [Engineer/Copywriter…]"), prompt box + tabs + cursor
  click with a glow ring, stacked message cards with "Thinking… → Ready" badges, avatar ring, app/phone UI, floating salary chips and
  3D coins, a giant-shape sweep as transition, end card = logo + prompt input + cursor click.
- Hard cuts on word onsets; the narration drives everything. Music is a light bed.

## Beat table (reference → ours)
| Ref beat | Technique | Ours (word cue) |
|---|---|---|
| "Meet your AI employees" pill rolodex on green flood | pills column shifting y, active pill filled white | audience pills → collapse into "la misma landing" (t(4)…t(12)) |
| "RESEARCH" on dark green | scanline gradient text, scale 1.35→1 blur slam | "HAZ ESTO." (t(14), t(15)) |
| prompt box "Create an online store…" + cursor + glowing send | per-char typewriter, tabs, click + ring | "Reservar una demo" struck → "Crea un quiz funnel", click on "funnel" |
| skeleton list → items | odometer + 8 step dots | "entre 5 y 8 preguntas" |
| agent message cards Thinking/Ready | cards blur-in on word, badge swap | 3 question cards (chip auto-selected), then 4 insight cards (caso/dato/resultado/consejo) |
| tilted "DESIGN" selection frame | rotated frame with handles + cursor drag | "SOLO PREGUNTAS" + strike |
| giant star sweep | 1400 px PNG flying diagonally across the cut | giant brand "?" coin |
| avatar ring + red counter | 12 avatars on a circle, highlight groups | CSS initials ring + "Tu resultado: Founder/Marketing/Agencia" |
| "You" / "free" giant words | giant black word on white, then deep slam | "Y aquí" → "IMPORTANTE" |
| app dashboard + salary chips + coins | phone UI with screens swapped on words, coral chips, coins | product → por qué encaja → oferta 99€→69€ → contador 14:59 |
| logo + "What will you build first?" input + click | wordmark + prompt pill + cursor click | "SaaS IN House" + "Comenta QUIZ" |

## Recipe
1. Audio first: reuse a VO, `npx hyperframes transcribe` → `work/transcript.json`. `work/build.py` injects the words and the SFX cue list (word-indexed) into `work/index.src.html` → `index.html`.
2. Scene windows `C = {…}` are word onsets minus ~0.1 s. Every headline = `kin(host, from, to, {acc, map})`.
3. Colours are two CSS tokens away from any brand: `.aura`, `.flood`, `.deep`, `.acc` gradients (ref = mint; ours = SaaS in House red).
4. `npm run check` → `snapshot --at …` → look → fix.

## Cost
$0 images (reused brand coins from `sih-quiz-film`), 0 ElevenLabs calls (VO `quiz-funnel-es` Gabriel Blanco, bed `ui-launch-film`, SFX from earlier projects). Fonts: Geist (OFL), Silkscreen for the IN chip.

## Gotchas
- **`visibility: visible` on a child overrides a hidden scene** → typewriter chars/countdown digits leaked into every later scene. Toggle children with `opacity`, scenes with `visibility`.
- `check` rejects tweening `left/top/letterSpacing` and `width`: cursors use x/y deltas from the authored left/top, rolodex uses `y`, progress bar uses `scaleX`.
- `check` rejects `querySelector` with a template literal; keep a JS reference to created nodes.
- Kinetic lines reserve the width of not-yet-visible words (opacity 0) → the line "grows" off-centre; that is the reference's look, but long lines must fit 1080 at full length (split into two `.k` hosts).
- A flex container drops whitespace-only spans ("ComentaQUIZ"): don't use `display:flex` on typewriter hosts; `.w` margin must be global, not only `.k .w`.
- Light text on the flood needs the darker flood stops (contrast check); ghost word warning (1.2:1) is decorative and expected.
