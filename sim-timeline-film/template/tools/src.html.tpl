<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Archivo"; src: url("assets/Archivo.ttf") format("truetype"); font-weight: 100 900; font-stretch: 62% 125%; }
      @font-face { font-family: "JBM"; src: url("assets/JetBrainsMono.ttf") format("truetype"); font-weight: 100 800; }
      :root {
        --bg: #fbfbfc; --dot: #d5d7dd; --ink: #121216; --mute: #8b8f99; --red: #e8382d; --red-deep: #a8231b; --cream: #f2efe6;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--bg); font-family: "Archivo", sans-serif; color: var(--ink); }
      #dots { position: absolute; inset: 0; background-image: radial-gradient(circle, var(--dot) 1.6px, transparent 2px); background-size: 54px 54px; background-position: 13px 13px; opacity: 0.8; }
      .scene { position: absolute; inset: 0; overflow: hidden; visibility: hidden; }
      .hl { position: absolute; left: 80px; top: 196px; width: 930px; font-weight: 600; font-size: 64px; line-height: 1.12; letter-spacing: -0.03em; }
      .hl .w { display: inline-block; margin-right: 0.22em; }
      .hl .acc { color: var(--red); }
      .mono { font-family: "JBM", monospace; }
      #meta { position: absolute; left: 80px; right: 80px; top: 112px; display: flex; justify-content: space-between; font-size: 26px; color: var(--mute); letter-spacing: 0.01em; }
      #meta b { color: var(--ink); font-weight: 600; }
      /* operation pill: [badge | gradient label] + red cap */
      .pill { position: absolute; height: 106px; display: flex; font-family: "JBM", monospace; font-size: 37px; font-weight: 500; color: var(--ink); filter: drop-shadow(0 10px 14px rgba(30, 34, 60, 0.13)); }
      .pill .body { display: flex; height: 100%; }
      .pill .n { width: 106px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 40px; background: var(--c2); }
      .pill .l { display: flex; align-items: center; gap: 14px; padding: 0 52px 0 30px; background: linear-gradient(90deg, var(--c0), var(--c1)); white-space: nowrap; }
      .pill .cap { position: absolute; right: -24px; top: 50%; width: 52px; height: 52px; margin-top: -26px; background: var(--red); border-radius: 7px; box-shadow: 0 4px 8px rgba(168, 35, 27, 0.35); }
      .pill.big { height: 176px; font-size: 50px; }
      .pill.big .n { width: 150px; font-size: 56px; }
      .pill.big .l { padding: 0 70px 0 36px; }
      .pill.big .cap { width: 66px; height: 66px; margin-top: -33px; right: -32px; }
      .blue { --c0: #dcefff; --c1: #74bff5; --c2: #56aaea; }
      .purple { --c0: #eee3ff; --c1: #ae90f8; --c2: #9677ef; }
      .green { --c0: #d2f8e4; --c1: #55dd98; --c2: #3cca82; }
      .grey { --c0: #f1f2f5; --c1: #d4d8df; --c2: #c6cbd3; }
      .orange { --c0: #fde0c8; --c1: #f39150; --c2: #ee7a2e; }
      .yellow { --c2: #f5c51b; }
      .bad .n { background: var(--red) !important; color: #fff; }
      .rail { position: absolute; height: 92px; border-radius: 4px; background: linear-gradient(90deg, #e6e8ec, #dfe2e7); box-shadow: 0 8px 16px rgba(30, 34, 60, 0.08); }
      .spine { position: absolute; width: 14px; background: #dfe2e7; border-radius: 7px; }
      .chip { position: absolute; left: 130px; height: 132px; display: flex; align-items: center; gap: 30px; padding: 0 52px 0 28px; background: #f0f1f4; font-family: "JBM", monospace; font-size: 44px; border-radius: 6px; box-shadow: 0 10px 18px rgba(30, 34, 60, 0.1); }
      .chip .dot { width: 76px; height: 76px; border-radius: 50%; background: var(--ink); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 42px; font-weight: 800; }
      .chip.ok { background: linear-gradient(90deg, #d2f8e4, #55dd98); }
      .chip.ok .dot { background: #1f9e5f; }
      .chip .okbg { position: absolute; inset: 0; border-radius: 6px; background: linear-gradient(90deg, #d2f8e4, #55dd98); opacity: 0; }
      .chip .dot, .chip .lab { position: relative; }
      .chip .tick { position: absolute; inset: 0; border-radius: 50%; background: #1f9e5f; display: flex; align-items: center; justify-content: center; opacity: 0; }
      .tag { position: absolute; font-family: "JBM", monospace; font-size: 26px; padding: 8px 14px; border-radius: 6px; background: var(--red); color: #fff; font-weight: 700; }
      .readout { position: absolute; font-family: "JBM", monospace; font-size: 44px; color: var(--mute); }
      .readout b { color: var(--red); font-weight: 600; }
      #s7-wrap { position: absolute; left: -700px; right: -700px; top: 760px; height: 2400px; perspective: 900px; perspective-origin: 50% 0%; }
      #s7-floor { position: absolute; left: 0; right: 0; top: 0; height: 2400px; transform-origin: 50% 0%; transform: rotateX(66deg); }
      .term { position: absolute; left: 70px; width: 940px; background: #111216; border-radius: 18px; padding: 48px 48px; color: #e9e9ee; font-family: "JBM", monospace; font-size: 38px; line-height: 1.6; box-shadow: 0 30px 60px rgba(10, 10, 20, 0.28); }
      .term .pr { color: var(--red); }
      .term .ln { color: #7b7f8c; margin-right: 22px; }
      .term .hi { background: rgba(232, 56, 45, 0.35); }
      .lock { position: absolute; left: 0; right: 0; display: flex; justify-content: center; align-items: center; gap: 18px; color: var(--ink); }
      .lock .wm { font-weight: 860; font-stretch: 118%; font-size: 76px; letter-spacing: -0.02em; text-transform: uppercase; }
      .lock .in { font-family: "JBM", monospace; font-weight: 800; font-size: 44px; background: var(--red); color: #fff; padding: 6px 16px; border-radius: 10px; box-shadow: 5px 5px 0 var(--red-deep); }
      #fade { position: absolute; inset: 0; background: var(--bg); opacity: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="END" data-width="1080" data-height="1920">
      <!-- audio: reused Bruno Torres VO (whiteboard-ad), reused piano bed (liu8in) refit, library SFX -->
      <!--AUDIO-->

      <div id="dots" data-layout-ignore></div>
      <div id="meta" class="mono"><span><b>quiz_funnel</b>.sim</span><span id="clock">t+00:00.00</span></div>

      <!-- S1 · everyone to the same landing -->
      <section id="s1" class="scene"><div id="s1-hl" class="hl"></div><div id="s1-v"></div></section>
      <!-- S2 · Haz esto -->
      <section id="s2" class="scene"><div id="s2-hl" class="hl"></div><div id="s2-v"></div></section>
      <!-- S3 · demo ✕ → quiz funnel -->
      <section id="s3" class="scene"><div id="s3-hl" class="hl"></div><div id="s3-v"></div></section>
      <!-- S4+S5 · question tree + injected cards -->
      <section id="s4" class="scene"><div id="s4-hl" class="hl"></div><div id="s5-hl" class="hl"></div><div id="s4-v"></div></section>
      <!-- S6 · all answer paths → one personalised result -->
      <section id="s6" class="scene">
        <div id="s6-hl" class="hl"></div>
        <div id="s6-count" class="readout" style="left: 80px; top: 560px;"><b id="s6-n">64</b> caminos posibles</div>
        <div id="s6-zoom" style="position: absolute; left: 80px; top: 660px; width: 920px; height: 860px; transform-origin: 50% 50%;">
          <canvas id="s6-cv" width="920" height="860" style="width: 920px; height: 860px;"></canvas>
        </div>
        <div id="s6-v"></div>
      </section>
      <!-- S7 · Y lo importante: perspective floor -->
      <section id="s7" class="scene">
        <div id="s7-wrap" data-layout-ignore><div id="s7-floor"><canvas id="s7-cv" width="2480" height="2400" style="width: 2480px; height: 2400px;"></canvas></div></div>
        <div id="s7-fog" data-layout-ignore style="position: absolute; left: 0; right: 0; top: 700px; height: 420px; background: linear-gradient(var(--bg), rgba(251,251,252,0));"></div>
        <div id="s7-hl" class="hl"></div>
        <div id="s7-v"></div>
      </section>
      <!-- S8 · last cards: product, offer, countdown -->
      <section id="s8" class="scene"><div id="s8-hl" class="hl"></div><div id="s8-v"></div></section>
      <!-- S9 · checks -->
      <section id="s9" class="scene"><div id="s9-hl" class="hl"></div><div id="s10-hl" class="hl"></div><div id="s9-v"></div></section>
      <!-- S11 · CTA -->
      <section id="s11" class="scene">
        <div id="s11-hl" class="hl"><span class="w">Comenta</span> <span class="w acc">QUIZ</span></div>
        <div id="s11-sub" class="readout" style="left: 80px; top: 300px; font-size: 38px;">y te paso el funnel completo</div>
        <div id="s11-term" class="term" style="top: 620px;">
          <div><span class="pr">$</span> <span id="s11-cmd"></span><span id="s11-cur">▍</span></div>
          <div id="s11-l1" style="opacity: 0;"><span class="ln">1</span>5–8 preguntas de diagnóstico</div>
          <div id="s11-l2" style="opacity: 0;"><span class="ln">2</span>cards con casos reales y datos</div>
          <div id="s11-l3" style="opacity: 0;"><span class="ln">3</span><span class="hi">resultado + oferta + contador</span></div>
        </div>
        <div id="s11-v"></div>
        <div id="s11-lock" class="lock" style="top: 1380px; opacity: 0;"><div class="wm">SaaS</div><div class="in" id="s11-in">IN</div><div class="wm">House</div></div>
      </section>

      <div id="fade" data-layout-ignore></div>
    </div>

    <script>
      const VO = /*VO*/0;   // VO offset; word times are relative to assets/vo.mp3 (assets/words.json)
      const W = /*WORDS*/[];
      const END = /*END*/0;
      const t = (i) => W[i][1] + VO;
      const tl = gsap.timeline({ paused: true });
      let seed = 7;
      const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
      const $ = (id) => document.getElementById(id);

      // hard cuts, like the reference
      const C = { s2: t(14), s3: t(16), s4: t(26), s6: t(59), s7: t(66), s8: t(69), s9: t(87), s11: t(103) + 0.75 };
      const SC = [["s1", 0, C.s2], ["s2", C.s2, C.s3], ["s3", C.s3, C.s4], ["s4", C.s4, C.s6], ["s6", C.s6, C.s7],
                  ["s7", C.s7, C.s8], ["s8", C.s8, C.s9], ["s9", C.s9, C.s11], ["s11", C.s11, END + 1]];
      SC.forEach(([id, a, b]) => { tl.set("#" + id, { visibility: "visible" }, a); tl.set("#" + id, { visibility: "hidden" }, b); });

      // headline typed word by word on the VO; acc = word indexes in the red accent
      function typed(host, from, to, acc = []) {
        const el = $(host);
        for (let i = from; i <= to; i++) {
          const s = document.createElement("span");
          s.className = "w" + (acc.includes(i) ? " acc" : ""); s.id = `${host}-w${i}`;
          s.textContent = W[i][0].replace(/^¿/, "¿");
          el.appendChild(s);
          tl.fromTo(s, { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 0.16, ease: "power2.out", immediateRender: false }, t(i));
          tl.set(s, { opacity: 0 }, 0);
        }
      }

      // operation pill factory
      function pill(host, o) {
        const p = document.createElement("div");
        p.id = o.id; p.className = `pill ${o.kind || "blue"} ${o.cls || ""}`;
        p.style.left = o.x + "px"; p.style.top = o.y + "px";
        p.innerHTML = `<div class="body">${o.n !== undefined ? `<div class="n">${o.n}</div>` : ""}<div class="l"${o.w ? ` style="min-width:${o.w}px"` : ""}>${o.label}</div></div>${o.cap === false ? "" : '<div class="cap"></div>'}`;
        $(host).appendChild(p);
        return p;
      }
      // pop a pill in: cap first, then the body unrolls leftwards out of it
      function grow(id, at, d = 0.32) {
        tl.set("#" + id, { opacity: 1 }, at);
        tl.fromTo(`#${id} .cap`, { scale: 0 }, { scale: 1, duration: 0.16, ease: "back.out(3)", immediateRender: false }, at);
        tl.fromTo(`#${id} .body`, { clipPath: "inset(0 0 0 100%)" }, { clipPath: "inset(0 0 0 0%)", duration: d, ease: "power3.out", immediateRender: false }, at + 0.06);
        tl.set(`#${id} .body`, { clipPath: "inset(0 0 0 100%)" }, 0);
        tl.set("#" + id, { opacity: 0 }, 0);
      }
      const show = (sel, at, from = { opacity: 0, y: 24 }, d = 0.3) => {
        tl.fromTo(sel, from, { opacity: 1, y: 0, x: 0, scale: 1, duration: d, ease: "power3.out", immediateRender: false }, at);
        tl.set(sel, from, 0);
      };

      /* ---------- top readout: virtual clock ---------- */
      const clk = { v: 0 };
      tl.to(clk, { v: END, duration: END, ease: "none", onUpdate: () => {
        const s = clk.v; $("clock").textContent = `t+${String(Math.floor(s / 60)).padStart(2, "0")}:${(s % 60).toFixed(2).padStart(5, "0")}`;
      } }, 0);

      /* ---------- S1 · ¿Quieres vender tu SaaS sin mandar a todo el mundo a la misma landing? ---------- */
      typed("s1-hl", 0, 13, [12, 13]);
      const who = [["founder", "blue"], ["cto", "purple"], ["marketing", "green"], ["agencia", "blue"], ["freelance", "purple"], ["curioso", "green"]];
      who.forEach(([lab, k], i) => {
        const y = 640 + i * 134, x = 90 + (i % 2) * 210;
        pill("s1-v", { id: "s1-p" + i, x, y, kind: k, n: i + 1, label: lab, w: 270 });
        tl.fromTo("#s1-p" + i, { x: -700, opacity: 1 }, { x: 0, duration: 0.45, ease: "power3.out", immediateRender: false }, t(1) + i * 0.28);
        tl.set("#s1-p" + i, { x: -700 }, 0);
        // everyone collapses into the same landing
        tl.to("#s1-p" + i, { x: 330 - x + (i - 2.5) * 6, y: 1520 - y, scale: 0.45, opacity: 0, duration: 0.42, ease: "power2.in" }, t(12) - 0.1 + i * 0.04);
      });
      pill("s1-v", { id: "s1-land", x: 200, y: 1480, kind: "grey", n: "#", label: "/landing", w: 380, cls: "big" });
      show("#s1-land", t(10), { opacity: 0, y: 40 });
      tl.to("#s1-land", { scale: 1.06, duration: 0.12, yoyo: true, repeat: 1 }, t(13) + 0.15);
      const tag1 = document.createElement("div"); tag1.id = "s1-tag"; tag1.className = "tag"; tag1.textContent = "6 visitas · 1 mensaje";
      Object.assign(tag1.style, { left: "600px", top: "1430px" }); $("s1-v").appendChild(tag1);
      show("#s1-tag", t(13) + 0.25, { opacity: 0, y: 14, scale: 0.8 }, 0.22);

      /* ---------- S2 · Haz esto. ---------- */
      typed("s2-hl", 14, 15, [15]);
      pill("s2-v", { id: "s2-p", x: 170, y: 900, kind: "orange", n: "1", label: "empieza aquí", cls: "big" });
      grow("s2-p", t(14) + 0.02, 0.4);

      /* ---------- S3 · En vez de pedir una demo, crea un Quiz Funnel. ---------- */
      typed("s3-hl", 16, 25, [24, 25]);
      [[600, 600], [1400, 680]].forEach(([y, w], i) => {
        const r = document.createElement("div"); r.className = "rail"; r.id = "s3-r" + i;
        Object.assign(r.style, { left: "-40px", top: y + "px", width: w + "px" }); $("s3-v").appendChild(r);
        show("#s3-r" + i, t(16), { opacity: 0, x: -200 }, 0.4);
      });
      pill("s3-v", { id: "s3-demo", x: 120, y: 800, kind: "blue", n: "1", label: "pedir_demo", w: 300 });
      grow("s3-demo", t(16) + 0.1);
      const x3 = document.createElement("div"); x3.id = "s3-x"; x3.textContent = "✕";
      Object.assign(x3.style, { position: "absolute", left: 0, top: 0, width: "84px", height: "84px", background: "var(--red)", color: "#fff", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: "36px", opacity: 0 });
      $("s3-demo").appendChild(x3);
      tl.fromTo("#s3-x", { opacity: 0, scale: 1.6 }, { opacity: 1, scale: 1, duration: 0.18, ease: "power3.out", immediateRender: false }, t(21));
      tl.to("#s3-demo", { opacity: 0.45, filter: "grayscale(1)", duration: 0.25 }, t(21) + 0.15);
      pill("s3-v", { id: "s3-qf", x: 150, y: 1040, kind: "orange", n: "⚡", label: "quiz_funnel", w: 480, cls: "big" });
      show("#s3-qf", t(22), { opacity: 0, y: -260, scale: 1.15 }, 0.36);
      tl.to("#s3-demo", { y: -46, duration: 0.3, ease: "power2.out" }, t(22) + 0.2);
      tl.to("#s3-qf", { scale: 1.07, duration: 0.14, yoyo: true, repeat: 1, ease: "power2.out" }, t(24));
      const tag3 = document.createElement("div"); tag3.id = "s3-tag"; tag3.className = "tag"; tag3.textContent = "nuevo";
      Object.assign(tag3.style, { left: "830px", top: "1000px" }); $("s3-v").appendChild(tag3);
      show("#s3-tag", t(25), { opacity: 0, y: 12, scale: 0.7 }, 0.2);

      /* ---------- S4 · Primero, entre cinco y ocho preguntas… / S5 · Entre medias, cards… ---------- */
      typed("s4-hl", 26, 42, [28, 29, 30, 31]);
      typed("s5-hl", 43, 58, [45, 55, 56, 57, 58]);
      tl.set("#s4-hl", { opacity: 0 }, t(43) - 0.02);
      const spine = document.createElement("div"); spine.className = "spine"; spine.id = "s4-sp";
      Object.assign(spine.style, { left: "86px", top: "630px", height: "1000px" }); $("s4-v").appendChild(spine);
      tl.fromTo("#s4-sp", { scaleY: 0, transformOrigin: "50% 0%" }, { scaleY: 1, duration: 0.5, ease: "power2.out", immediateRender: false }, t(26) + 0.1);
      tl.set("#s4-sp", { scaleY: 0, transformOrigin: "50% 0%" }, 0);
      const ROW = (i) => 640 + i * 124;
      for (let i = 0; i < 8; i++) {
        const ghost = i >= 5;
        pill("s4-v", { id: "s4-h" + i, x: 120, y: ROW(i), kind: "grey", n: "#", label: "p" + (i + 1), w: 96, cap: false });
        const at = ghost ? t(30) + (i - 5) * 0.1 : t(27) + i * 0.1;
        show("#s4-h" + i, at, { opacity: 0, x: -40 }, 0.25);
        if (ghost) tl.to("#s4-h" + i, { opacity: 0.4, duration: 0.01 }, at + 0.26);
      }
      const Q = [[34, "¿quién eres?", "blue"], [37, "¿qué quieres?", "purple"], [42, "¿tu problema?", "green"]];
      Q.forEach(([wi, lab, k], i) => {
        pill("s4-v", { id: "s4-q" + i, x: 380, y: ROW(i * 2), kind: k, n: i + 1, label: lab });
        grow("s4-q" + i, t(wi));
      });
      [[3, "pregunta 4"], [5, "pregunta 5"]].forEach(([r, lab], i) => {
        pill("s4-v", { id: "s4-f" + i, x: 380, y: ROW(r), kind: "grey", n: r === 3 ? 4 : 5, label: lab, cap: false });
        grow("s4-f" + i, t(42) + 0.25 + i * 0.12, 0.25);
      });
      // S5: cards injected between the questions (orange, like faults injected into a run)
      const K = [[47, 1, "★ caso real"], [50, 3, "▲ dato 4→19"], [54, 5, "✦ consejo"]];
      K.forEach(([wi, r, lab], i) => {
        pill("s4-v", { id: "s5-c" + i, x: 380, y: ROW(r), kind: "orange", label: lab });
        tl.set("#s5-c" + i + " .l", { paddingLeft: 30 }, 0);
        grow("s5-c" + i, t(wi));
      });
      tl.to(["#s4-f0", "#s4-f1"], { x: -200, opacity: 0, duration: 0.3, ease: "power2.in" }, t(46));
      const ch5 = document.createElement("div"); ch5.className = "chip ok"; ch5.id = "s5-ok"; ch5.innerHTML = '<div class="dot">✓</div>tiene_sentido';
      Object.assign(ch5.style, { left: "380px", top: "1660px" }); $("s4-v").appendChild(ch5);
      show("#s5-ok", t(55), { opacity: 0, y: 30, scale: 0.85 }, 0.3);
      tl.to("#s5-ok", { scale: 1.06, duration: 0.14, yoyo: true, repeat: 1 }, t(58));

      /* ---------- S6 · Después, un resultado personalizado según sus respuestas. ---------- */
      typed("s6-hl", 59, 65, [62]);
      const cv = $("s6-cv"), cx = cv.getContext("2d");
      const hash = (n) => { let x = (n * 2654435761) >>> 0; x ^= x >>> 13; x = (x * 1274126177) >>> 0; return ((x ^ (x >>> 16)) >>> 0) / 4294967296; };
      const COLS = ["#74bff5", "#ae90f8", "#55dd98"];
      const HI = [41, 27];   // the one path that matches this lead
      const g = { k: 3, dim: 0 };
      function drawGrid() {
        const side = Math.pow(2, Math.round(g.k));        // 8, 16, 32, 64 columns
        const cw = 920 / side, chh = 860 / side;
        cx.clearRect(0, 0, 920, 860);
        for (let r = 0; r < side; r++) for (let c = 0; c < side; c++) {
          const h = hash(r * 977 + c * 131 + side);
          const isHi = Math.round(g.k) === 6 && c === HI[0] && r === HI[1];
          const x = c * cw + cw * 0.12, y = r * chh + chh * 0.3, w = cw * (0.55 + 0.33 * h), hh = Math.max(2, chh * 0.4);
          cx.globalAlpha = isHi ? 1 : 1 - 0.78 * g.dim;
          cx.fillStyle = isHi && g.dim > 0 ? "#e8382d" : COLS[Math.floor(h * 3)];
          cx.fillRect(x, y, w * 0.72, hh);
          cx.fillStyle = isHi && g.dim > 0 ? "#e8382d" : COLS[Math.floor(hash(h * 1e6) * 3)];
          cx.fillRect(x + w * 0.72, y, w * 0.28, hh);
          if (!isHi) { cx.globalAlpha *= 0.6; cx.fillStyle = "#e8382d"; cx.fillRect(x + w, y, Math.max(1.5, cw * 0.08), hh); }
        }
        cx.globalAlpha = 1;
        if (g.dim > 0) {
          const cw2 = 920 / 64, ch2 = 860 / 64, pad = 10 + 26 * (1 - g.dim);
          cx.strokeStyle = "#e8382d"; cx.lineWidth = 4; cx.globalAlpha = g.dim;
          cx.strokeRect(HI[0] * cw2 - pad, HI[1] * ch2 - pad, cw2 + 2 * pad, ch2 + 2 * pad);
          cx.fillStyle = "#e8382d"; cx.fillRect(HI[0] * cw2 - 3, HI[1] * ch2 + 1, cw2 + 6, ch2 - 2);
          cx.globalAlpha = 1;
        }
        const n = Math.pow(4, Math.round(3 + (Math.min(g.k, 6) - 3) * (5 / 3)));
        $("s6-n").textContent = Math.min(65536, n).toLocaleString("es-ES");
      }
      drawGrid();
      tl.fromTo(g, { k: 3 }, { k: 6, duration: t(62) - t(59) - 0.2, ease: "power1.in", onUpdate: drawGrid, immediateRender: false }, t(59) + 0.1);
      tl.to(g, { k: 6.6, duration: 0.3, onUpdate: drawGrid }, t(62) - 0.1);
      tl.to(g, { dim: 1, duration: 0.3, onUpdate: drawGrid }, t(62));
      // zoom into the matching path, then it becomes the result card
      const hx = (HI[0] + 0.5) / 64 * 920, hy = (HI[1] + 0.5) / 64 * 860;
      tl.set("#s6-zoom", { transformOrigin: `${hx}px ${hy}px` }, 0);
      tl.to("#s6-zoom", { scale: 9, duration: 0.6, ease: "power3.in" }, t(64) - 0.1);
      tl.to("#s6-zoom", { opacity: 0, duration: 0.15 }, t(65) - 0.05);
      pill("s6-v", { id: "s6-res", x: 110, y: 1000, kind: "orange", n: "★", label: "tu resultado", cls: "big" });
      show("#s6-res", t(65) - 0.05, { opacity: 0, scale: 0.4 }, 0.32);
      const sub6 = document.createElement("div"); sub6.className = "readout"; sub6.id = "s6-sub"; sub6.innerHTML = "según <b>tus</b> respuestas";
      Object.assign(sub6.style, { left: "120px", top: "1230px" }); $("s6-v").appendChild(sub6);
      show("#s6-sub", t(65) + 0.15, { opacity: 0, y: 14 }, 0.25);

      /* ---------- S7 · Y lo importante: ---------- */
      typed("s7-hl", 66, 68, [68]);
      (function floor() {
        const c = $("s7-cv").getContext("2d"); let s = 3;
        const r = () => ((s = (s * 16807) % 2147483647) / 2147483647);
        for (let y = 20; y < 2400; y += 46) for (let x = 0; x < 2480; ) {
          const w = 60 + r() * 150;
          c.fillStyle = COLS[Math.floor(r() * 3)]; c.globalAlpha = 0.85; c.fillRect(x, y, w * 0.7, 18);
          c.fillStyle = COLS[Math.floor(r() * 3)]; c.fillRect(x + w * 0.7, y, w * 0.3, 18);
          c.fillStyle = "#e8382d"; c.fillRect(x + w, y, 8, 18); x += w + 30 + r() * 60;
        }
      })();
      tl.fromTo("#s7-floor", { y: -900 }, { y: 0, duration: t(69) - t(66), ease: "power1.out", immediateRender: false }, t(66));
      tl.set("#s7-floor", { y: -900 }, 0);
      pill("s7-v", { id: "s7-p", x: 280, y: 560, kind: "orange", n: "!", label: "importante" });
      grow("s7-p", t(68));

      /* ---------- S8 · las últimas cards lo llevan a tu producto, con una oferta específica y un contador… ---------- */
      typed("s8-hl", 69, 86, [76, 79, 80, 83, 84, 85, 86]);
      const ST = [[69, 70, 620, "grey", "#", "últimas cards"], [76, 170, 830, "orange", "⚡", "tu producto"], [79, 270, 1040, "purple", "%", "oferta −30%"], [83, 370, 1250, "green", "⏱", "14:59"]];
      ST.forEach(([wi, x, y, k, n, lab], i) => {
        pill("s8-v", { id: "s8-p" + i, x, y, kind: k, n, label: lab, w: i === 3 ? 200 : 0 });
        grow("s8-p" + i, t(wi) + (i === 0 ? 0.15 : 0));
        if (i > 0) {   // elbow connector from the previous step
          const e = document.createElement("div"); e.id = "s8-e" + i;
          Object.assign(e.style, { position: "absolute", left: ST[i - 1][1] + 50 + "px", top: ST[i - 1][2] + 106 + "px", width: "5px", height: "104px", background: "#c6cbd3" });
          $("s8-v").appendChild(e);
          tl.fromTo(e, { scaleY: 0, transformOrigin: "50% 0%" }, { scaleY: 1, duration: 0.2, immediateRender: false }, t(wi) - 0.15);
          tl.set(e, { scaleY: 0, transformOrigin: "50% 0%" }, 0);
        }
      });
      const ro8 = document.createElement("div"); ro8.className = "readout"; ro8.id = "s8-ro";
      ro8.innerHTML = 'tiempo limitado <b id="s8-time">00:14:59.00</b>';
      Object.assign(ro8.style, { left: "80px", top: "1510px" }); $("s8-v").appendChild(ro8);
      show("#s8-ro", t(84), { opacity: 0, y: 14 }, 0.25);
      const cd = { v: 899 };
      tl.fromTo(cd, { v: 899 }, { v: 899 - (t(87) - t(84)), duration: t(87) - t(84), ease: "none", immediateRender: false, onUpdate: () => {
        const s = cd.v; $("s8-time").textContent = `00:${String(Math.floor(s / 60)).padStart(2, "0")}:${(s % 60).toFixed(2).padStart(5, "0")}`;
        $("s8-p3").querySelector(".l").textContent = `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
      } }, t(84));
      // the offer pulses on "específica"
      tl.to("#s8-p2", { scale: 1.06, duration: 0.14, yoyo: true, repeat: 1 }, t(80));

      /* ---------- S9 · Así no solo captas el lead. / S10 · Lo segmentas, lo educas y lo llevas directo a la compra. ---------- */
      typed("s9-hl", 87, 92, [90, 91, 92]);
      typed("s10-hl", 93, 103, [94, 96, 103]);
      tl.set("#s9-hl", { opacity: 0 }, t(93) - 0.02);
      const CH = [[90, "lead_captado"], [94, "segmentado"], [96, "educado"], [103, "compra"]];
      CH.forEach(([wi, lab], i) => {
        const c = document.createElement("div"); c.className = "chip"; c.id = "s9-c" + i;
        c.innerHTML = `<div class="okbg" id="s9-g${i}"></div><div class="dot"><div class="tick" id="s9-k${i}">✓</div></div><span class="lab">${lab}</span>`;
        c.style.top = 660 + i * 200 + "px";
        $("s9-v").appendChild(c);
        show("#s9-c" + i, t(87) + 0.1 + i * 0.1, { opacity: 0, x: -60 }, 0.3);
        tl.fromTo("#s9-g" + i, { opacity: 0 }, { opacity: 1, duration: 0.2, immediateRender: false }, t(wi));
        tl.fromTo("#s9-k" + i, { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)", immediateRender: false }, t(wi));
      });
      tl.to("#s9-c3", { scale: 1.12, x: 40, duration: 0.35, ease: "back.out(2)" }, t(103) + 0.05);

      /* ---------- S11 · CTA: Comenta QUIZ ---------- */
      const S11 = C.s11;
      show("#s11-hl", S11 + 0.05, { opacity: 0, y: 20 }, 0.3);
      show("#s11-sub", S11 + 0.35, { opacity: 0, y: 14 }, 0.3);
      show("#s11-term", S11 + 0.2, { opacity: 0, y: 60 }, 0.35);
      const cmd = "comenta QUIZ";
      for (let k = 0; k <= cmd.length; k++) tl.set("#s11-cmd", { textContent: cmd.slice(0, k) }, S11 + 0.55 + k * 0.09);
      tl.set("#s11-cmd", { textContent: "" }, 0);
      for (let k = S11 + 0.3; k < END; k += 0.5) tl.set("#s11-cur", { opacity: 0 }, k).set("#s11-cur", { opacity: 1 }, k + 0.25);
      ["#s11-l1", "#s11-l2", "#s11-l3"].forEach((id, i) => show(id, S11 + 1.9 + i * 0.35, { opacity: 0, x: -20 }, 0.25));
      pill("s11-v", { id: "s11-cap", x: 478, y: 1395, kind: "orange", label: "", cap: true });
      $("s11-cap").querySelector(".body").style.display = "none";
      tl.set("#s11-cap", { opacity: 0 }, 0);
      tl.set("#s11-cap", { opacity: 1 }, 36.0);
      tl.fromTo("#s11-cap .cap", { scale: 0 }, { scale: 1.6, duration: 0.2, ease: "back.out(3)", immediateRender: false }, 36.0);
      tl.to("#s11-cap", { opacity: 0, duration: 0.12 }, 36.22);
      show("#s11-lock", 36.2, { opacity: 0, y: 30 }, 0.45);
      tl.fromTo("#s11-in", { scale: 0.3, rotation: -12 }, { scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2.5)", immediateRender: false }, 36.2);
      tl.to("#fade", { opacity: 1, duration: 0.5 }, END - 0.5);

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
