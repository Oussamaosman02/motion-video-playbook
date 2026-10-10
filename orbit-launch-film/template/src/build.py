#!/usr/bin/env python3
"""Build index.html from src/index.tpl.html: injects the VO word times, the film length and every <audio> tag.

Every SFX time is derived from a word index of the VO (t(i) = word start + VO offset), so swapping the voice
means: replace assets/vo.mp3, paste its words into WORDS (from `npx hyperframes transcribe` or an embedded array),
run `python3 src/build.py`, then `npm run check`.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
VO = 0.3
END = 28.5
# sih-quiz-film/assets/vo.mp3 (26.15s), words as embedded in sih-quiz-film / x-batch/jordan: [word, start, end]
WORDS = [["Tu",0.09,0.13],["próximo",0.13,0.67],["cliente",0.67,1.13],["no",1.13,1.26],["llega",1.26,1.59],["por",1.59,1.79],["la",1.79,1.91],["landing,",1.91,2.45],["llega",2.63,3],["por",3,3.32],["un",3.32,3.45],["quiz.",3.45,4.12],["Cinco",4.21,4.4],["a",4.4,4.45],["ocho",4.45,4.67],["preguntas",4.7,5.19],["para",5.19,5.42],["saber",5.42,5.7],["quién",5.7,6.03],["es,",6.03,6.24],["qué",6.31,6.33],["quiere",6.75,6.88],["y",6.88,7],["qué",7,7.48],["le",7.48,7.57],["duele.",7.57,8.34],["Entre",8.43,8.64],["pregunta",8.66,9.17],["y",9.17,9.23],["pregunta,",9.23,9.86],["casos",9.86,10.18],["reales",10.18,10.47],["y",10.47,10.72],["datos",10.72,10.97],["que",10.97,11.13],["le",11.13,11.26],["hacen",11.26,11.57],["pensar.",11.57,12.06],["Esto",12.33,12.48],["tiene",12.48,12.79],["sentido.",12.82,13.42],["Al",13.42,13.56],["final,",13.56,14.1],["un",14.1,14.25],["resultado",14.25,14.93],["hecho",14.93,15.31],["para",15.31,15.61],["él",15.61,15.69],["y",15.69,15.95],["una",15.95,16.03],["oferta",16.1,16.48],["a",16.53,16.55],["su",16.55,16.7],["medida,",16.7,17.21],["con",17.22,17.32],["un",17.41,17.45],["contador",17.45,17.97],["para",17.97,18.23],["canjearla.",18.23,19.04],["No",19.04,19.19],["solo",19.19,19.43],["captas",19.79,19.94],["el",19.95,20.09],["lead,",20.09,20.55],["lo",20.55,20.69],["segmentas,",20.69,21.44],["lo",21.44,21.61],["educas",21.61,22.14],["y",22.18,22.2],["lo",22.2,22.28],["llevas",22.28,22.59],["a",22.59,22.69],["la",22.69,22.78],["compra.",22.8,23.37],["Comenta",23.37,23.82],["quiz",23.82,24.04],["y",24.09,24.14],["te",24.14,24.27],["enseño",24.27,24.71],["cómo",24.71,24.74],["montarlo.",25.23,25.8]]
t = lambda i: WORDS[i][1] + VO
C1, C2, C3, C4, C5, C6 = t(12) + 0.05, t(26) - 0.05, t(41), t(50) - 0.05, t(59), t(74) - 0.05

# (file, start, volume) — all library SFX, 0 ElevenLabs calls
SFX = [
    ("whoosh", 0.05, 0.25),
    ("pop", t(2), 0.32), ("key", t(2) + 0.16, 0.4),
    ("pop", t(7), 0.28), ("tick", t(7) + 0.42, 0.5),
    ("pop", t(11), 0.34), ("pop", t(11) + 0.38, 0.28),
    ("whoosh", t(12) - 0.42, 0.35), ("key", t(12) + 0.12, 0.7),
    ("whoosh", t(12) + 0.3, 0.3), ("impact", C1 + 0.75, 0.3),
] + [("tick", C1 + 0.4 + (n - 1) * 0.11, 0.42) for n in range(1, 9)] + [
    ("pop", t(18), 0.3), ("pop", t(20) + 0.1, 0.3), ("pop", t(23), 0.32),
    ("whoosh", C2 - 0.4, 0.3),
] + [("tick", a, 0.5) for a in (C2, t(29), t(30), t(31), t(33), t(35), t(37), t(38))] + [
    ("pop", t(40), 0.35),
    ("boom", C3, 0.45), ("whoosh", t(44) - 0.15, 0.35),
    ("whoosh", C4, 0.3), ("pop", C4 + 0.05, 0.3),
] + [("tick", t(56) + 0.5 * k, 0.55) for k in range(0, 4)] + [
    ("impact", C5, 0.3), ("whoosh", t(61) - 0.25, 0.25),
    ("pop", t(63), 0.28), ("pop", t(65), 0.32), ("pop", t(67), 0.32), ("pop", t(73), 0.36),
    ("whoosh", C6, 0.3), ("impact", C6 + 0.7, 0.35), ("type", C6 + 1.2, 0.35),
    ("pop", t(75), 0.38),
]
DUR = {"whoosh": 1.2, "pop": 0.5, "key": 0.5, "tick": 0.5, "impact": 2.0, "boom": 1.5, "type": 1.5}

lines = [
    f'      <audio id="vo" src="assets/vo.mp3" data-start="{VO}" data-duration="26.1" data-track-index="10" data-volume="1"></audio>',
    f'      <audio id="mus" src="assets/music.mp3" data-start="0" data-duration="{END}" data-track-index="11" data-volume="0.2"></audio>',
]
for k, (name, at, vol) in enumerate(SFX):
    d = min(DUR[name], END - at)
    lines.append(f'      <audio id="a{k}-{name}" src="assets/{name}.mp3" data-start="{at:.2f}" data-duration="{d:.2f}" data-track-index="{12 + k}" data-volume="{vol}"></audio>')

tpl = (ROOT / "src/index.tpl.html").read_text()
html = (tpl.replace("__AUDIO__", "\n".join(lines))
           .replace("__WORDS__", json.dumps(WORDS, ensure_ascii=False, separators=(",", ":")))
           .replace("__VO__", str(VO)).replace("__END__", str(END)))
(ROOT / "index.html").write_text(html)
print(f"index.html: {len(SFX)} SFX, END={END}s, cuts {[round(c, 2) for c in (C1, C2, C3, C4, C5, C6)]}")
