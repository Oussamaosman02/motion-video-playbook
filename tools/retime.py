#!/usr/bin/env python3
"""Retarget an existing composition to a NEW narration of the SAME script.

Usage:
  python3 retime.py template/index.html new_words.json new_project/index.html AUDIO_DURATION

How it works:
  * Both narrations have the same word count, so word i in the old read maps to word i in
    the new one. Any authored time t is mapped piecewise-linearly between word starts.
  * Captions and character cues are built from WORDS / word indices, so swapping WORDS is
    enough for them. Scene cues (hard-coded seconds after the "// ---- scene cues ----"
    marker) are remapped at runtime through a proxy timeline `mapped`.
  * Scene <section data-start/data-duration> attributes are rewritten with the same map.
Template contract: `const WORDS = [...]`, `const END = ...;`, root data-duration, the
<audio id="vo"> data-duration, one `const tl = gsap.timeline({ paused: true });`, and the
marker line `      // ---- scene cues ----`.
"""
import json
import re
import sys

src, words_path, dst, audio_dur = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
s = open(src, encoding="utf-8").read()
old = json.loads(re.search(r"const WORDS = (\[.*?\]\]);", s).group(1))
new = [w[:3] for w in json.load(open(words_path))]
assert len(old) == len(new), f"word count differs: {len(old)} vs {len(new)} - same script required"
for o, n in zip(old, new):  # keep the template's caption spelling (e.g. "5" for "cinco")
    n[0] = o[0]
OA, NA = [w[1] for w in old], [w[1] for w in new]


def M(t):
    if t <= OA[0]:
        return t
    for i in range(len(OA) - 1):
        if OA[i] <= t <= OA[i + 1]:
            f = (t - OA[i]) / (OA[i + 1] - OA[i]) if OA[i + 1] > OA[i] else 0
            return NA[i] + f * (NA[i + 1] - NA[i])
    return NA[-1] + (t - OA[-1])


old_end = float(re.search(r"const END = ([\d.]+);", s).group(1))
END = round(new[-1][2] + 1.3, 2)
s = s.replace(re.search(r"const WORDS = (\[.*?\]\]);", s).group(1), json.dumps(new, ensure_ascii=False))
s = re.sub(r"const END = [\d.]+;", f"const END = {END};", s)
s = s.replace(f'data-duration="{old_end:g}"', f'data-duration="{END}"', 1)
s = re.sub(r'(<audio id="vo"[^>]*data-duration=")[\d.]+', rf"\g<1>{audio_dur}", s)


def sec(m):
    st, du = float(m.group(2)), float(m.group(3))
    ns = round(M(st), 2)
    ne = END if abs(st + du - old_end) < 0.01 else round(M(st + du), 2)
    return f'id="{m.group(1)}" class="scene clip" data-start="{ns}" data-duration="{round(ne - ns, 2)}"'


s = re.sub(r'id="(s\d+)" class="scene clip" data-start="([\d.]+)" data-duration="([\d.]+)"', sec, s)
mapjs = f"""      const OA = {json.dumps(OA)};
      const NA = {json.dumps(NA)};
      const M = (t) => {{
        if (typeof t !== "number" || t <= OA[0]) return t;
        for (let i = 0; i < OA.length - 1; i++) if (t >= OA[i] && t <= OA[i + 1]) {{
          const f = OA[i + 1] > OA[i] ? (t - OA[i]) / (OA[i + 1] - OA[i]) : 0;
          return NA[i] + f * (NA[i + 1] - NA[i]);
        }}
        return NA[NA.length - 1] + (t - OA[OA.length - 1]);
      }};
      // scene cues below were authored against the template narration; remap their positions
      const mapped = {{
        to: (a, b, t) => raw.to(a, b, M(t)),
        set: (a, b, t) => raw.set(a, b, M(t)),
        fromTo: (a, b, c, t) => raw.fromTo(a, b, c, M(t)),
      }};
"""
assert s.count("const tl = gsap.timeline({ paused: true });") == 1
assert s.count("      // ---- scene cues ----\n") == 1
s = s.replace("const tl = gsap.timeline({ paused: true });",
              "const raw = gsap.timeline({ paused: true });\n      let tl = raw;\n" + mapjs)
s = s.replace("      // ---- scene cues ----\n", "      // ---- scene cues ----\n      tl = mapped;\n")
s = s.replace('window.__timelines["main"] = tl;', 'window.__timelines["main"] = raw;')
open(dst, "w", encoding="utf-8").write(s)
print(f"END={END}s  -> {dst}")
