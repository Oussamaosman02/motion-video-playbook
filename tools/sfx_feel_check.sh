#!/bin/bash
# Does this SFX *feel* made with AI? (model trained on the client's blind ratings, ~80% agreement)
# Usage: playbook/tools/sfx_feel_check.sh sound.mp3 [more.mp3 ...]
#   -> "FEELS AI 0.91 riser.mp3 <reasons>" or "clean 0.03 pop.mp3". >= 0.5 = do not use.
# Details, patterns and the approved list: ../../sfx-forensics/README.md, ../../sfx-forensics/approved_sounds.txt
HERE="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$HERE/../../sfx-forensics/feel_ai.py" "$@" 2> >(grep -v -i warn >&2)
