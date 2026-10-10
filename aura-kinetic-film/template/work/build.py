# Builds ../index.html from index.src.html: injects the word array (work/transcript.json) and the audio tags (cue list below).
import json, os
H = os.path.dirname(os.path.abspath(__file__))
w = json.load(open(f"{H}/transcript.json")); w = w if isinstance(w, list) else w["words"]
W = [[x.get("text", x.get("word")).strip(), round(x["start"], 2), round(x["end"], 2)] for x in w]
W[83][0] = "Y aquí"   # whisper merged "Y aquí" into one token
VO = 0.3
t = lambda i: round(W[i][1] + VO, 2)
te = lambda i: round(W[i][2] + VO, 2)
END = 55.6
# (file, start, volume)
S = [("whoosh", 0.0, 0.35),
     ("tick", t(5), 0.3), ("tick", t(7), 0.3), ("tick", t(9), 0.3), ("pop", t(12), 0.4),
     ("impact", t(14) - 0.02, 0.55), ("glitch", t(15), 0.35),
     ("type", t(19), 0.3), ("tick", t(22) + 0.15, 0.35), ("type", t(23), 0.3), ("click", t(26) + 0.12, 0.6), ("ding", t(26) + 0.18, 0.3),
     ("whoosh", t(27) - 0.12, 0.3), ("pop", t(30), 0.45), ("tick", t(32), 0.35), ("tick", t(32) + 0.12, 0.3), ("tick", t(32) + 0.24, 0.3),
     ("whoosh", t(36) - 0.22, 0.3), ("pop", t(36), 0.35), ("click", t(36) + 0.6, 0.4), ("pop", t(41), 0.35), ("click", t(41) + 0.6, 0.4), ("pop", t(44), 0.35), ("click", t(44) + 0.6, 0.4),
     ("whoosh", t(49) - 0.14, 0.3), ("tick", t(52), 0.35), ("glitch", te(53) + 0.05, 0.35),
     ("whoosh", t(54) - 0.14, 0.25), ("pop", t(60), 0.35), ("pop", t(62), 0.35), ("pop", t(63), 0.35), ("pop", t(65), 0.35),
     ("pop", t(70) - 0.25, 0.4), ("chime", te(73) - 0.1, 0.35), ("whoosh", t(74) - 0.9, 0.5),
     ("pop", t(76), 0.35), ("tick", t(81) - 0.1, 0.35), ("tick", t(82) - 0.05, 0.35), ("tick", t(82) + 0.45, 0.35),
     ("impact", t(83), 0.45), ("impact", t(87), 0.6),
     ("whoosh", t(88) - 0.12, 0.35), ("whoosh", t(98) - 0.1, 0.25), ("click", t(102), 0.35), ("click", t(104), 0.35), ("click", t(105), 0.35),
     ("whoosh", t(106) - 0.1, 0.25), ("pop", t(109), 0.4), ("glitch", t(110), 0.3), ("whoosh", t(111) - 0.1, 0.25),
     ("tick", t(114), 0.3), ("tick", t(114) + 1, 0.3), ("tick", t(114) + 2, 0.3), ("tick", t(114) + 3, 0.3), ("click", t(119) - 0.05, 0.55),
     ("whoosh", t(120) - 0.18, 0.35), ("tick", t(123), 0.3), ("tick", t(127) - 0.05, 0.3), ("tick", t(129) - 0.05, 0.3), ("tick", t(132) - 0.05, 0.3),
     ("impact", t(135), 0.4), ("chime", t(136) - 0.1, 0.4),
     ("whoosh", te(136) + 0.15, 0.3), ("type", te(136) + 0.75, 0.3), ("click", te(136) + 2.1, 0.6), ("ding", te(136) + 2.15, 0.4)]
D = {"whoosh": 0.83, "tick": 0.52, "pop": 0.52, "impact": 2.0, "glitch": 0.62, "type": 1.5, "click": 0.52, "ding": 1.04, "chime": 2.0}
tags = [f'      <audio id="vo" src="assets/vo.mp3" data-start="{VO}" data-duration="51.35" data-track-index="10" data-volume="1"></audio>',
        f'      <audio id="mus" src="assets/music.mp3" data-start="0" data-duration="{END}" data-track-index="11" data-volume="0.2"></audio>']
for n, (f, a, v) in enumerate(S):
    d = min(D[f], END - a)
    tags.append(f'      <audio id="a{n}" src="assets/{f}.mp3" data-start="{a:.2f}" data-duration="{d:.2f}" data-track-index="{12 + n}" data-volume="{v}"></audio>')
src = open(f"{H}/index.src.html").read()
out = src.replace("<!--AUDIO-->", "\n".join(tags)).replace("/*WORDS*/", json.dumps(W, ensure_ascii=False, separators=(",", ":")))
open(f"{H}/../index.html", "w").write(out)
print("ok", len(S), "sfx")
