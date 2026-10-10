<!doctype html>
<html lang="es" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      @font-face { font-family: "Archivo"; src: url("assets/Archivo.ttf") format("truetype"); font-weight: 100 900; font-stretch: 62% 125%; }
      @font-face { font-family: "Silkscreen"; src: url("assets/Silkscreen-400.woff2") format("woff2"); font-weight: 400; }
      @font-face { font-family: "Silkscreen"; src: url("assets/Silkscreen-700.woff2") format("woff2"); font-weight: 700; }
      :root {
        --bg: #0b0b10; --red: #e8382d; --red-deep: #7e140d; --cream: #f2efe6; --paper: #f7f5f0; --ink: #141217; --muted: #8b8790;
      }
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: var(--bg); }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--bg); color: #fff; font-family: "Archivo", sans-serif; }
      .scene { position: absolute; inset: 0; overflow: hidden; }
      .full { position: absolute; inset: 0; }
      .px { font-family: "Silkscreen", monospace; letter-spacing: 0.12em; text-transform: uppercase; }
      /* talking-head layers: plate (cam) < text behind < cutout (camfg) < text front */
      .cam, .camfg { position: absolute; inset: 0; transform-origin: 50% 50%; }
      .cam img, .camfg img.cut { position: absolute; left: 0; top: -7px; width: 1080px; height: 1935px; }
      .mouth { position: absolute; left: 404px; top: 906px; width: 303px; height: 207px; opacity: 0; }
      .grade { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 45%, transparent 55%, rgba(0,0,0,0.45)); }
      .t { position: absolute; color: #fff; font-weight: 560; letter-spacing: -0.01em; line-height: 1.02; text-shadow: 0 4px 24px rgba(0,0,0,0.35); white-space: nowrap; }
      .big { font-weight: 640; font-stretch: 88%; letter-spacing: -0.035em; line-height: 0.9; }
      .w { display: inline-block; }
      /* Figma-style selection highlight: red box + corner handles */
      .sel { position: relative; display: inline-block; isolation: isolate; padding: 0 0.12em 0.04em; }
      .sel > .bx { position: absolute; inset: 0; background: var(--red); transform-origin: left center; z-index: -1; }
      .sel > .h { position: absolute; width: 14px; height: 14px; background: #fff; border: 2px solid var(--red); }
      .sel > .h.a { left: -7px; top: -7px; } .sel > .h.b { right: -7px; top: -7px; } .sel > .h.c { left: -7px; bottom: -7px; } .sel > .h.d { right: -7px; bottom: -7px; }
      .strike { position: absolute; height: 18px; background: var(--red); border-radius: 9px; transform-origin: left center; }
      .guide { position: absolute; border-top: 2px dashed rgba(255,255,255,0.45); }
      .vguide { position: absolute; border-left: 2px dashed rgba(255,255,255,0.45); }
      /* cream inserts */
      .paper { background: var(--paper); color: var(--ink); }
      .lbl { position: absolute; font-size: 34px; font-weight: 520; color: var(--ink); display: flex; align-items: center; gap: 14px; white-space: nowrap; }
      .dot { width: 22px; height: 22px; border-radius: 50%; background: var(--red); display: inline-block; }
      .card { position: absolute; background: #fff; border-radius: 30px; box-shadow: 0 30px 70px rgba(30,20,20,0.12), 0 1px 0 rgba(0,0,0,0.05); padding: 34px 38px; color: var(--ink); }
      .tag { display: inline-block; font-size: 24px; font-weight: 700; color: var(--red); background: rgba(232,56,45,0.1); padding: 8px 16px; border-radius: 999px; }
      .card .k { font-size: 30px; color: var(--muted); margin-top: 18px; }
      .card .v { font-size: 66px; font-weight: 760; letter-spacing: -0.03em; margin-top: 6px; }
      .ex { font-size: 22px; color: #6f6a73; margin-top: 10px; letter-spacing: 0.08em; text-transform: uppercase; }
      .pill { position: absolute; border: 3px solid var(--ink); border-radius: 999px; display: flex; align-items: center; justify-content: center; }
      .ring { position: absolute; border: 2px dashed rgba(20,18,23,0.18); border-radius: 50%; }
      .q { position: absolute; font-size: 36px; font-weight: 600; background: #fff; color: var(--ink); padding: 18px 28px; border-radius: 999px; box-shadow: 0 16px 40px rgba(30,20,20,0.12); white-space: nowrap; }
      .q b { color: var(--red); }
      .bar { position: absolute; left: 70px; right: 70px; height: 150px; background: #fff; border: 2px solid #e7e2ea; border-radius: 80px; box-shadow: 0 20px 50px rgba(30,20,20,0.1); display: flex; align-items: center; padding: 0 40px 0 56px; }
      .send { position: absolute; right: 22px; top: 22px; width: 106px; height: 106px; border-radius: 50%; background: var(--red); display: flex; align-items: center; justify-content: center; }
      .caret { display: inline-block; width: 4px; height: 52px; background: var(--red); margin-left: 4px; vertical-align: middle; }
      /* desk wall */
      .wall { position: absolute; top: 680px; width: 470px; height: 960px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
      .tile { background: #f4efe7; border-radius: 16px; position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: center; align-items: center; color: var(--ink); font-weight: 700; text-align: center; }
      .tile.d { background: #1d1b22; color: var(--cream); }
      .tile.r { background: var(--red); color: #fff; }
      .tile .s { font-size: 20px; font-weight: 500; opacity: 0.6; margin-top: 6px; }
      .tile .n { font-size: 54px; letter-spacing: -0.03em; }
      .tile .hl { position: absolute; inset: 0; border: 6px solid var(--red); border-radius: 16px; opacity: 0; }
      .toplabel { position: absolute; top: 210px; left: 0; right: 0; display: flex; justify-content: center; }
      .toplabel .p { background: var(--red); color: #fff; font-size: 40px; font-weight: 700; padding: 14px 34px; border-radius: 14px; }
      .feat { position: absolute; left: 90px; right: 90px; top: 330px; height: 300px; }
      .feat > div { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: #fff; }
      .disp { font-weight: 860; font-stretch: 118%; text-transform: uppercase; line-height: 0.94; letter-spacing: -0.015em; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="57.5" data-width="1080" data-height="1920">
      <!-- audio: vo.mp3 already contains both voices at their absolute times -->
      <audio id="vo" src="assets/vo.mp3" data-start="0" data-duration="53.53" data-track-index="10" data-volume="1"></audio>
      <audio id="mus" src="assets/music.mp3" data-start="0" data-duration="57.5" data-track-index="11" data-volume="0.2"></audio>
      <audio id="sfx-wh1" src="assets/whoosh.mp3" data-start="4.62" data-duration="0.8" data-track-index="12" data-volume="0.45"></audio>
      <audio id="sfx-ty1" src="assets/type.mp3" data-start="6.35" data-duration="1.5" data-track-index="13" data-volume="0.3"></audio>
      <audio id="sfx-pop1" src="assets/pop.mp3" data-start="7.92" data-duration="0.5" data-track-index="14" data-volume="0.6"></audio>
      <audio id="sfx-pop2" src="assets/pop.mp3" data-start="11.03" data-duration="0.5" data-track-index="15" data-volume="0.6"></audio>
      <audio id="sfx-wh2" src="assets/whoosh.mp3" data-start="12.3" data-duration="0.8" data-track-index="16" data-volume="0.5"></audio>
      <audio id="sfx-t1" src="assets/tick.mp3" data-start="15.22" data-duration="0.5" data-track-index="17" data-volume="0.6"></audio>
      <audio id="sfx-t2" src="assets/tick.mp3" data-start="15.83" data-duration="0.5" data-track-index="18" data-volume="0.6"></audio>
      <audio id="sfx-t3" src="assets/tick.mp3" data-start="17.15" data-duration="0.5" data-track-index="19" data-volume="0.6"></audio>
      <audio id="sfx-wh3" src="assets/whoosh.mp3" data-start="21.6" data-duration="0.8" data-track-index="20" data-volume="0.5"></audio>
      <audio id="sfx-c1" src="assets/pop.mp3" data-start="24.23" data-duration="0.5" data-track-index="21" data-volume="0.5"></audio>
      <audio id="sfx-c2" src="assets/pop.mp3" data-start="25.13" data-duration="0.5" data-track-index="22" data-volume="0.5"></audio>
      <audio id="sfx-c3" src="assets/pop.mp3" data-start="25.69" data-duration="0.5" data-track-index="23" data-volume="0.5"></audio>
      <audio id="sfx-c4" src="assets/pop.mp3" data-start="26.38" data-duration="0.5" data-track-index="24" data-volume="0.5"></audio>
      <audio id="sfx-ty2" src="assets/type.mp3" data-start="28.55" data-duration="1.5" data-track-index="25" data-volume="0.3"></audio>
      <audio id="sfx-ding1" src="assets/ding.mp3" data-start="30.2" data-duration="1" data-track-index="26" data-volume="0.45"></audio>
      <audio id="sfx-wh4" src="assets/whoosh.mp3" data-start="30.55" data-duration="0.8" data-track-index="27" data-volume="0.5"></audio>
      <audio id="sfx-wh5" src="assets/whoosh.mp3" data-start="37.4" data-duration="0.8" data-track-index="28" data-volume="0.5"></audio>
      <audio id="sfx-t4" src="assets/tick.mp3" data-start="40.8" data-duration="0.5" data-track-index="29" data-volume="0.6"></audio>
      <audio id="sfx-t5" src="assets/tick.mp3" data-start="42.75" data-duration="0.5" data-track-index="30" data-volume="0.6"></audio>
      <audio id="sfx-t6" src="assets/tick.mp3" data-start="44.14" data-duration="0.5" data-track-index="31" data-volume="0.6"></audio>
      <audio id="sfx-pop3" src="assets/pop.mp3" data-start="48.75" data-duration="0.5" data-track-index="32" data-volume="0.6"></audio>
      <audio id="sfx-pop4" src="assets/pop.mp3" data-start="52.3" data-duration="0.5" data-track-index="33" data-volume="0.6"></audio>
      <audio id="sfx-ty3" src="assets/type.mp3" data-start="53.8" data-duration="1.5" data-track-index="34" data-volume="0.3"></audio>
      <audio id="sfx-ding2" src="assets/ding.mp3" data-start="55.3" data-duration="1" data-track-index="35" data-volume="0.5"></audio>

      <!-- ============ S1 · host A, hook ============ -->
      <section id="s1" class="scene clip" data-start="0" data-duration="4.75" data-track-index="1">
        <div class="cam"><img src="assets/hostA.jpg" alt="" /></div>
        <div class="t big" id="s1-land" style="left: 60px; top: 520px; font-size: 270px;">landing</div>
        <div class="strike" id="s1-strike" style="left: 40px; top: 640px; width: 1000px; transform: rotate(-6deg);"></div>
        <div class="camfg"><img class="cut" src="assets/hostA_cut.png" alt="" /><img id="s1-mouth" class="mouth" src="assets/hostA_mouth.png" alt="" /></div>
        <div class="grade"></div>
        <div class="t" id="s1-a" style="left: 80px; top: 300px; font-size: 64px;"><span class="w" id="s1-w0">¿Quieres</span> <span class="w" id="s1-w1">vender</span></div>
        <div class="t" id="s1-b" style="left: 80px; top: 380px; font-size: 64px;"><span class="w" id="s1-w2">tu SaaS</span> <span class="w" id="s1-w3">sin mandar</span></div>
        <div class="t" id="s1-c" style="left: 560px; top: 470px; font-size: 54px;"><span class="w" id="s1-w4">a todos</span> <span class="w" id="s1-w5">a la misma</span></div>
        <div class="t big" id="s1-haz" style="left: 0; right: 0; top: 270px; font-size: 190px; display: flex; justify-content: center;"><span class="sel"><span class="bx"></span><span class="h a"></span><span class="h b"></span><span class="h c"></span><span class="h d"></span>Haz esto.</span></div>
      </section>

      <!-- ============ S2 · host B listening, off-camera question ============ -->
      <section id="s2" class="scene clip" data-start="4.75" data-duration="4.6" data-track-index="2">
        <div class="cam"><img src="assets/hostB.jpg" alt="" /></div>
        <div class="camfg"><img class="cut" src="assets/hostB_cut.png" alt="" /></div>
        <div class="grade"></div>
        <div class="guide" id="s2-g1" style="left: 40px; right: 40px; top: 560px;"></div>
        <div class="vguide" id="s2-g2" style="left: 640px; top: 120px; height: 520px;"></div>
        <div class="t" id="s2-esp" style="left: 80px; top: 230px; font-size: 46px; opacity: 0.85;">Espera, espera…</div>
        <div class="t" id="s2-l1" style="right: 460px; top: 330px; font-size: 76px; text-align: right;">¿O sea, que</div>
        <div class="t" id="s2-l2" style="right: 460px; top: 415px; font-size: 76px; text-align: right;">no pido una</div>
        <div class="t big" id="s2-demo" style="left: 680px; top: 300px; font-size: 150px;"><span class="sel"><span class="bx"></span><span class="h a"></span><span class="h b"></span><span class="h c"></span><span class="h d"></span>demo</span></div>
        <div class="t" id="s2-dir" style="left: 690px; top: 470px; font-size: 54px;">directamente?</div>
      </section>

      <!-- ============ S3 · host A, "No. Quiz Funnel" ============ -->
      <section id="s3" class="scene clip" data-start="9.35" data-duration="3.1" data-track-index="3">
        <div class="cam"><img src="assets/hostA.jpg" alt="" /></div>
        <div class="t big" id="s3-qf" style="left: 0; right: 0; top: 500px; font-size: 175px; display: flex; justify-content: center;"><span class="sel"><span class="bx"></span><span class="h a"></span><span class="h b"></span><span class="h c"></span><span class="h d"></span>Quiz Funnel</span></div>
        <div class="camfg"><img class="cut" src="assets/hostA_cut.png" alt="" /><img id="s3-mouth" class="mouth" src="assets/hostA_mouth.png" alt="" /></div>
        <div class="grade"></div>
        <div class="t big" id="s3-no" style="left: 70px; top: 230px; font-size: 220px;">No.</div>
        <div class="t" id="s3-creas" style="left: 90px; top: 430px; font-size: 56px;">Creas un</div>
      </section>

      <!-- ============ S4 · paper insert, 5–8 questions ============ -->
      <section id="s4" class="scene clip paper" data-start="12.45" data-duration="6.95" data-track-index="4">
        <div class="lbl" id="s4-lbl" style="left: 0; right: 0; top: 520px; justify-content: center;"><span class="dot"></span>Primero</div>
        <div id="s4-num" class="big" style="position: absolute; left: 0; right: 0; top: 600px; text-align: center; font-size: 520px; color: var(--ink); font-weight: 700; letter-spacing: -0.06em;"><span class="w" id="s4-5">5</span><span class="w" id="s4-dash">–</span><span class="w" id="s4-8">8</span></div>
        <div id="s4-sub" class="big" style="position: absolute; left: 0; right: 0; top: 1130px; text-align: center; font-size: 120px; color: var(--ink);">preguntas</div>
        <div id="s4-orb" class="full">
          <div class="ring" id="s4-r1" style="left: 90px; top: 760px; width: 900px; height: 520px;"></div>
          <div class="ring" id="s4-r2" style="left: 190px; top: 840px; width: 700px; height: 360px;"></div>
          <div class="pill" id="s4-pill" style="left: 290px; top: 920px; width: 500px; height: 200px; font-size: 78px; font-weight: 640;">Tu lead</div>
          <div class="q" id="s4-q1" style="left: 80px; top: 690px;">¿Quién <b>es</b>?</div>
          <div class="q" id="s4-q2" style="right: 60px; top: 1210px;">¿Qué quiere <b>conseguir</b>?</div>
          <div class="q" id="s4-q3" style="left: 70px; top: 1370px;">¿Su principal <b>problema</b>?</div>
        </div>
      </section>

      <!-- ============ S5 · host A, "Pero no hagas solo preguntas" ============ -->
      <section id="s5" class="scene clip" data-start="19.4" data-duration="2.35" data-track-index="5">
        <div class="cam"><img src="assets/hostA.jpg" alt="" /></div>
        <div class="t big" id="s5-solo" style="left: 0; right: 0; top: 470px; font-size: 300px; text-align: center;">{ solo }</div>
        <div class="camfg"><img class="cut" src="assets/hostA_cut.png" alt="" /><img id="s5-mouth" class="mouth" src="assets/hostA_mouth.png" alt="" /></div>
        <div class="grade"></div>
        <div class="t" id="s5-pero" style="left: 0; right: 0; top: 330px; font-size: 64px; text-align: center;">Pero no hagas</div>
        <div class="t big" id="s5-preg" style="left: 0; right: 0; top: 1480px; font-size: 140px; display: flex; justify-content: center;"><span class="sel"><span class="bx"></span><span class="h a"></span><span class="h b"></span><span class="h c"></span><span class="h d"></span>preguntas</span></div>
      </section>

      <!-- ============ S6 · paper insert, proof cards + "vale, esto tiene sentido" ============ -->
      <section id="s6" class="scene clip paper" data-start="21.75" data-duration="8.95" data-track-index="6">
        <div class="lbl" id="s6-lbl" style="left: 0; right: 0; top: 250px; justify-content: center; font-size: 40px;">{ entre medias }</div>
        <div class="big" id="s6-head" style="position: absolute; left: 0; right: 0; top: 320px; text-align: center; font-size: 120px; color: var(--ink);">pequeñas cards</div>
        <div class="card" id="s6-c1" style="left: 70px; top: 540px; width: 455px; height: 300px;"><span class="tag">Caso real</span><div class="v">4 → 19</div><div class="k">demos / mes</div></div>
        <div class="card" id="s6-c2" style="left: 555px; top: 540px; width: 455px; height: 300px;"><span class="tag">Dato</span><div class="v">+218</div><div class="k">founders ya lo usan</div></div>
        <div class="card" id="s6-c3" style="left: 70px; top: 870px; width: 455px; height: 300px;"><span class="tag">Resultado</span><div class="v">78K€</div><div class="k">MRR generado</div></div>
        <div class="card" id="s6-c4" style="left: 555px; top: 870px; width: 455px; height: 300px;"><span class="tag">Consejo</span><div class="v" style="font-size: 46px; line-height: 1.1;">Pregunta por su problema, no por su cargo</div></div>
        <div class="ex" id="s6-ex" style="position: absolute; left: 0; right: 0; top: 1192px; text-align: center;">datos de ejemplo</div>
        <div class="bar" id="s6-bar" style="top: 1330px;"><div style="font-size: 50px; font-weight: 520;"><span id="s6-typed"></span><span class="caret" id="s6-caret"></span></div>
          <div class="send" id="s6-send"><svg width="50" height="50" viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div></div>
        <div class="lbl" id="s6-think" style="left: 0; right: 0; top: 1530px; justify-content: center; color: var(--muted); font-size: 34px;">lo que piensa tu lead</div>
      </section>

      <!-- ============ S7 · red, personalised result ============ -->
      <section id="s7" class="scene clip" data-start="30.7" data-duration="4.35" data-track-index="7" style="background: var(--red);">
        <div id="s7-dots" class="full"></div>
        <div class="t" id="s7-seg" style="left: 0; right: 0; top: 700px; font-size: 50px; text-align: center; text-shadow: none;">según sus respuestas</div>
        <div class="t big" id="s7-res" style="left: 0; right: 0; top: 860px; font-size: 170px; text-align: center; text-shadow: none;">{ resultado }</div>
        <div class="center" style="position: absolute; left: 0; right: 0; top: 1080px; display: flex; justify-content: center;"><div id="s7-pers" style="background: #fff; color: var(--red); font-size: 64px; font-weight: 700; padding: 18px 44px; border-radius: 999px;">personalizado</div></div>
      </section>

      <!-- ============ S8 · host A, "la parte importante" ============ -->
      <section id="s8" class="scene clip" data-start="35.05" data-duration="2.5" data-track-index="8">
        <div class="cam"><img src="assets/hostA.jpg" alt="" /></div>
        <div class="t big" id="s8-imp" style="left: 0; right: 0; top: 520px; font-size: 220px; text-align: center;">importante</div>
        <div class="camfg"><img class="cut" src="assets/hostA_cut.png" alt="" /><img id="s8-mouth" class="mouth" src="assets/hostA_mouth.png" alt="" /></div>
        <div class="grade"></div>
        <div class="t" id="s8-a" style="left: 0; right: 0; top: 360px; font-size: 64px; text-align: center;">Y aquí viene la parte</div>
        <svg id="s8-swoosh" width="1080" height="400" style="position: absolute; left: 0; top: 1380px;" viewBox="0 0 1080 400"><path id="s8-path" d="M60 120 C 300 360, 520 -40, 700 180 S 1000 300, 1040 90" stroke="#e8382d" stroke-width="16" fill="none" stroke-linecap="round" /></svg>
      </section>

      <!-- ============ S9 · desk + curved wall of closing cards ============ -->
      <section id="s9" class="scene clip" data-start="37.55" data-duration="9.7" data-track-index="9" style="background: radial-gradient(ellipse 90% 70% at 50% 40%, #2a2026, #0b0b10);">
        <div id="s9-stage" class="full" style="perspective: 1400px;">
          <div class="wall" id="s9-wl" style="left: 30px; transform: rotateY(38deg); transform-origin: right center;">
            <div class="tile"><div class="n">✓</div><div class="s">encaja</div><div class="hl h1"></div></div>
            <div class="tile d"><div class="n">−30%</div><div class="s">oferta</div><div class="hl h2"></div></div>
            <div class="tile r"><div class="n" id="s9-cd1">14:59</div><div class="s">quedan</div><div class="hl h3"></div></div>
            <div class="tile"><div class="n">Pro</div><div class="s">tu plan</div><div class="hl h2"></div></div>
            <div class="tile d"><div class="n">B2B</div><div class="s">tu caso</div><div class="hl h1"></div></div>
            <div class="tile"><div class="n">€</div><div class="s">canjear</div><div class="hl h2"></div></div>
            <div class="tile"><div class="n">3/3</div><div class="s">perfil</div><div class="hl h1"></div></div>
            <div class="tile d"><div class="n">⏱</div><div class="s">24 h</div><div class="hl h3"></div></div>
          </div>
          <div class="wall" id="s9-wr" style="right: 30px; transform: rotateY(-38deg); transform-origin: left center;">
            <div class="tile d"><div class="n">SaaS</div><div class="s">para ti</div><div class="hl h1"></div></div>
            <div class="tile"><div class="n">−30%</div><div class="s">solo hoy</div><div class="hl h2"></div></div>
            <div class="tile"><div class="n">✓</div><div class="s">tu problema</div><div class="hl h1"></div></div>
            <div class="tile r"><div class="n" id="s9-cd2">14:59</div><div class="s">contador</div><div class="hl h3"></div></div>
            <div class="tile d"><div class="n">Demo</div><div class="s">reservar</div><div class="hl h2"></div></div>
            <div class="tile"><div class="n">92%</div><div class="s">encaje</div><div class="hl h1"></div></div>
            <div class="tile r"><div class="n">Ya</div><div class="s">canjear</div><div class="hl h3"></div></div>
            <div class="tile"><div class="n">Plan</div><div class="s">growth</div><div class="hl h2"></div></div>
          </div>
        </div>
        <div id="s9-table" style="position: absolute; left: -40px; right: -40px; top: 1600px; bottom: 0; background: linear-gradient(#c79c6b, #9a7247); border-top: 4px solid #e2bf92;"></div>
        <div class="camfg" id="s9-host"><img class="cut" src="assets/desk_cut.png" alt="" /></div>
        <div class="toplabel"><div class="p" id="s9-p0">Las últimas cards</div></div>
        <div class="toplabel"><div class="p" id="s9-p1">Encaje</div></div>
        <div class="toplabel"><div class="p" id="s9-p2">Oferta</div></div>
        <div class="toplabel"><div class="p" id="s9-p3">Contador</div></div>
        <div class="feat">
          <div id="s9-f0"><div class="big" style="font-size: 110px;">→ tu producto</div></div>
          <div id="s9-f1"><div class="big" style="font-size: 86px;">Por qué encaja<br />con su situación</div></div>
          <div id="s9-f2"><div class="big" style="font-size: 150px;">−30%</div><div style="font-size: 40px; opacity: 0.8;">oferta específica</div></div>
          <div id="s9-f3"><div class="big" id="s9-cd" style="font-size: 200px; font-variant-numeric: tabular-nums;">14:59</div><div style="font-size: 40px; opacity: 0.8;">para canjearla</div></div>
        </div>
      </section>

      <!-- ============ S10 · host A, "no solo captas el lead" ============ -->
      <section id="s10" class="scene clip" data-start="47.25" data-duration="2.2" data-track-index="1">
        <div class="cam"><img src="assets/hostA.jpg" alt="" /></div>
        <div class="t big" id="s10-lead" style="left: 0; right: 0; top: 395px; font-size: 300px; text-align: center;">el lead</div>
        <div class="camfg"><img class="cut" src="assets/hostA_cut.png" alt="" /><img id="s10-mouth" class="mouth" src="assets/hostA_mouth.png" alt="" /></div>
        <div class="grade"></div>
        <div class="t" id="s10-a" style="left: 0; right: 0; top: 270px; font-size: 64px; text-align: center;">Así no solo captas</div>
      </section>

      <!-- ============ S11 · host A punch-in, payoff ============ -->
      <section id="s11" class="scene clip" data-start="49.45" data-duration="4.1" data-track-index="2">
        <div class="cam"><img src="assets/hostA.jpg" alt="" /></div>
        <div class="t big" id="s11-compra" style="left: 0; right: 0; top: 330px; font-size: 300px; text-align: center;">compra</div>
        <div class="camfg"><img class="cut" src="assets/hostA_cut.png" alt="" /><img id="s11-mouth" class="mouth" src="assets/hostA_mouth.png" alt="" /></div>
        <div class="grade"></div>
        <div class="t" id="s11-a" style="left: 70px; top: 220px; font-size: 70px;"><span class="sel"><span class="bx"></span>Lo segmentas,</span></div>
        <div class="t" id="s11-b" style="right: 70px; top: 320px; font-size: 70px;"><span class="sel"><span class="bx"></span>lo educas,</span></div>
        <div class="t" id="s11-c" style="left: 0; right: 0; top: 1560px; font-size: 64px; text-align: center;">y lo llevas directamente a la</div>
      </section>

      <!-- ============ S12 · paper end card ============ -->
      <section id="s12" class="scene clip paper" data-start="53.55" data-duration="3.95" data-track-index="3">
        <div id="s12-dots" class="full"></div>
        <div style="position: absolute; left: 0; right: 0; top: 720px; display: flex; justify-content: center;">
          <div id="s12-cta" style="font-size: 64px; font-weight: 520; color: var(--ink); white-space: nowrap;"><span id="s12-l" style="color: var(--red);">←</span> { <span id="s12-typed"></span> } <span id="s12-r" style="color: var(--red);">→</span></div>
        </div>
        <div id="s12-lock" style="position: absolute; left: 0; right: 0; top: 960px; display: flex; justify-content: center; align-items: center; gap: 20px; color: var(--ink);">
          <div class="disp" style="font-size: 96px;">SaaS</div>
          <div id="s12-chip" class="px" style="font-size: 44px; background: var(--red); color: var(--cream); padding: 12px 16px 6px; border-radius: 12px; box-shadow: 6px 6px 0 var(--red-deep);">IN</div>
          <div class="disp" style="font-size: 96px;">House</div>
        </div>
        <div id="s12-sub" style="position: absolute; left: 0; right: 0; top: 1130px; text-align: center; font-size: 38px; color: var(--muted);">y te enseño cómo montarlo</div>
      </section>
    </div>

    <script>
      const ENV = /*ENV*/[]/*ENV*/; // founder-voice loudness per frame @30fps (0..1) -> mouth patch opacity
      const tl = gsap.timeline({ paused: true });
      let seed = 11;
      const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);

      // ---------- helpers ----------
      const inUp = (sel, at, d = 0.35) => tl.fromTo(sel, { opacity: 0, y: 26, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: d, ease: "power3.out" }, at);
      const inBig = (sel, at) => tl.fromTo(sel, { opacity: 0, scale: 1.12, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "power3.out" }, at);
      const out = (sel, at, d = 0.2) => tl.to(sel, { opacity: 0, duration: d }, at);
      const selIn = (sel, at) => {
        tl.fromTo(`${sel} .bx`, { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power3.out" }, at);
        tl.fromTo(`${sel} .h`, { scale: 0 }, { scale: 1, duration: 0.25, ease: "back.out(3)", stagger: 0.03 }, at + 0.15);
      };
      // talking-head "camera": slow push + tiny drift on plate and cutout together
      const cam = (scene, t0, t1, s0, s1, ox = "50%", oy = "50%") => {
        tl.set(`${scene} .cam, ${scene} .camfg`, { transformOrigin: `${ox} ${oy}` }, t0);
        tl.fromTo(`${scene} .cam, ${scene} .camfg`, { scale: s0, x: 0 }, { scale: s1, x: -10, duration: t1 - t0, ease: "none" }, t0);
      };
      // lip-flap: drive the mouth patch from the founder voice envelope
      const lips = (mouthId, t0, t1) => {
        const m = document.getElementById(mouthId);
        for (let f = Math.ceil(t0 * 30); f < t1 * 30; f++) tl.set(m, { opacity: ENV[f] || 0 }, f / 30);
      };

      // ---------- S1 · 0–4.75 ----------
      cam("#s1", 0, 4.75, 1.0, 1.07, "50%", "48%"); lips("s1-mouth", 0, 4.75);
      tl.set(["#s1-land", "#s1-strike", "#s1-a", "#s1-b", "#s1-c", "#s1-haz"], { opacity: 0 }, 0);
      tl.set(["#s1-a", "#s1-b", "#s1-c"], { opacity: 1 }, 0);
      [["#s1-w0", 0.3], ["#s1-w1", 0.64], ["#s1-w2", 0.96], ["#s1-w3", 1.57], ["#s1-w4", 2.15], ["#s1-w5", 2.68]].forEach(([s, at]) => inUp(s, at));
      inBig("#s1-land", 3.05);
      tl.fromTo("#s1-strike", { opacity: 1, scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.inOut" }, 3.45);
      out(["#s1-a", "#s1-b", "#s1-c"], 3.65);
      tl.set("#s1-haz", { opacity: 1 }, 3.72); selIn("#s1-haz .sel", 3.72);
      tl.fromTo("#s1-haz", { scale: 0.9 }, { scale: 1, duration: 0.4, ease: "back.out(2)" }, 3.72);

      // ---------- S2 · 4.75–9.35 (listening angle, no lip-flap) ----------
      cam("#s2", 4.75, 9.35, 1.04, 1.12, "45%", "45%");
      tl.set(["#s2-esp", "#s2-l1", "#s2-l2", "#s2-demo", "#s2-dir"], { opacity: 0 }, 4.75);
      tl.fromTo("#s2-g1", { scaleX: 0, transformOrigin: "left" }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, 4.8);
      tl.fromTo("#s2-g2", { scaleY: 0, transformOrigin: "top" }, { scaleY: 1, duration: 0.6, ease: "power2.out" }, 4.9);
      inUp("#s2-esp", 4.97);
      inUp("#s2-l1", 6.37); inUp("#s2-l2", 7.17);
      tl.set("#s2-demo", { opacity: 1 }, 7.92); selIn("#s2-demo .sel", 7.92);
      tl.fromTo("#s2-demo", { y: 20 }, { y: 0, duration: 0.3, ease: "back.out(2)" }, 7.92);
      inUp("#s2-dir", 8.16);

      // ---------- S3 · 9.35–12.45 ----------
      cam("#s3", 9.35, 12.45, 1.1, 1.16, "50%", "48%"); lips("s3-mouth", 9.35, 12.45);
      tl.set(["#s3-qf", "#s3-creas"], { opacity: 0 }, 9.35);
      tl.fromTo("#s3-no", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.3, ease: "power3.out" }, 9.45);
      out("#s3-no", 10.3); inUp("#s3-creas", 10.42); out("#s3-creas", 10.95);
      tl.set("#s3-qf", { opacity: 1 }, 11.03); selIn("#s3-qf .sel", 11.03);
      tl.fromTo("#s3-qf", { scale: 0.92 }, { scale: 1, duration: 0.5, ease: "back.out(1.6)" }, 11.03);

      // ---------- S4 · 12.45–19.4 (paper) ----------
      tl.fromTo("#s4", { clipPath: "inset(48% 0% 48% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.inOut" }, 12.45);
      tl.set(["#s4-5", "#s4-dash", "#s4-8", "#s4-sub", "#s4-orb"], { opacity: 0 }, 12.45);
      inUp("#s4-lbl", 12.55);
      tl.fromTo("#s4-5", { opacity: 0, yPercent: 40 }, { opacity: 1, yPercent: 0, duration: 0.35, ease: "power3.out" }, 13.5);
      tl.fromTo(["#s4-dash", "#s4-8"], { opacity: 0, yPercent: 40 }, { opacity: 1, yPercent: 0, duration: 0.35, ease: "power3.out", stagger: 0.08 }, 14.0);
      inUp("#s4-sub", 14.23);
      // numbers fly up and shrink, the orbit appears
      tl.to("#s4-num", { y: -420, scale: 0.36, duration: 0.55, ease: "power3.inOut" }, 14.95);
      tl.to("#s4-sub", { y: -610, scale: 0.5, duration: 0.55, ease: "power3.inOut" }, 14.95);
      tl.to("#s4-lbl", { opacity: 0, duration: 0.2 }, 14.95);
      tl.set("#s4-orb", { opacity: 1 }, 15.0);
      tl.set(["#s4-q1", "#s4-q2", "#s4-q3"], { opacity: 0 }, 15.0);
      tl.fromTo(["#s4-r1", "#s4-r2"], { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.6, ease: "power3.out", stagger: 0.08 }, 15.0);
      tl.fromTo("#s4-pill", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, 15.05);
      tl.to("#s4-r1", { rotation: 8, duration: 4, ease: "none" }, 15.4);
      tl.to("#s4-r2", { rotation: -10, duration: 4, ease: "none" }, 15.4);
      [["#s4-q1", 15.22], ["#s4-q2", 15.83], ["#s4-q3", 17.15]].forEach(([s, at]) => tl.fromTo(s, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.4)" }, at));
      tl.to("#s4-q3", { scale: 1.08, duration: 0.2, yoyo: true, repeat: 1 }, 18.16);

      // ---------- S5 · 19.4–21.75 ----------
      cam("#s5", 19.4, 21.75, 1.18, 1.24, "50%", "47%"); lips("s5-mouth", 19.4, 21.75);
      tl.set(["#s5-solo", "#s5-preg"], { opacity: 0 }, 19.4);
      inUp("#s5-pero", 19.45);
      inBig("#s5-solo", 20.18);
      tl.set("#s5-preg", { opacity: 1 }, 20.44); selIn("#s5-preg .sel", 20.44);

      // ---------- S6 · 21.75–30.7 (paper) ----------
      tl.fromTo("#s6", { clipPath: "inset(48% 0% 48% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "power3.inOut" }, 21.75);
      tl.set(["#s6-c1", "#s6-c2", "#s6-c3", "#s6-c4", "#s6-ex", "#s6-bar", "#s6-think", "#s6-send"], { opacity: 0 }, 21.75);
      inUp("#s6-lbl", 21.85); inUp("#s6-head", 23.07);
      [["#s6-c1", 24.23], ["#s6-c2", 25.13], ["#s6-c3", 25.69], ["#s6-c4", 26.38]].forEach(([s, at]) => tl.fromTo(s, { opacity: 0, y: 60, rotation: -3 }, { opacity: 1, y: 0, rotation: 0, duration: 0.45, ease: "back.out(1.7)" }, at));
      inUp("#s6-ex", 26.8);
      tl.fromTo("#s6-bar", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 27.3);
      inUp("#s6-think", 27.6);
      const TYPED = "Vale, esto tiene sentido";
      for (let i = 1; i <= TYPED.length; i++) tl.set("#s6-typed", { textContent: TYPED.slice(0, i) }, 28.58 + (i - 1) * (1.5 / TYPED.length));
      tl.set("#s6-typed", { textContent: "" }, 21.75);
      for (let k = 27.4; k < 30.7; k += 0.5) tl.set("#s6-caret", { opacity: 0 }, k + 0.25).set("#s6-caret", { opacity: 1 }, k + 0.5);
      tl.fromTo("#s6-send", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(3)" }, 30.15);
      tl.to(["#s6-c1", "#s6-c2", "#s6-c3", "#s6-c4"], { y: -10, duration: 1.2, ease: "sine.inOut", yoyo: true, repeat: 1 }, 27.4);

      // ---------- S7 · 30.7–35.05 (red) ----------
      (function dots() {
        const host = document.getElementById("s7-dots");
        const rings = [[230, 18], [330, 26], [430, 34], [540, 44], [660, 54]];
        rings.forEach(([r, n], ri) => {
          const g = document.createElement("div");
          g.id = `s7-ring${ri}`; g.className = "full";
          for (let i = 0; i < n; i++) {
            const a = (i / n) * Math.PI * 2, d = document.createElement("div");
            const sz = 14 + Math.round(rnd() * 16);
            d.style.cssText = `position:absolute;width:${sz}px;height:${sz}px;border-radius:50%;background:#fff;opacity:${(0.25 + rnd() * 0.6).toFixed(2)};left:${540 + Math.cos(a) * r - sz / 2}px;top:${960 + Math.sin(a) * r - sz / 2}px`;
            g.appendChild(d);
          }
          host.appendChild(g);
          tl.fromTo(g, { scale: 0.2, opacity: 0, rotation: 0, transformOrigin: "540px 960px" }, { scale: 1, opacity: 1, rotation: ri % 2 ? -25 : 25, duration: 4.3, ease: "power2.out" }, 30.75 + ri * 0.06);
        });
      })();
      tl.set(["#s7-seg", "#s7-res", "#s7-pers"], { opacity: 0 }, 30.7);
      inUp("#s7-seg", 31.46);
      inBig("#s7-res", 33.36);
      tl.fromTo("#s7-pers", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, 33.91);

      // ---------- S8 · 35.05–37.55 ----------
      cam("#s8", 35.05, 37.55, 1.0, 1.1, "50%", "48%"); lips("s8-mouth", 35.05, 37.55);
      tl.set("#s8-imp", { opacity: 0 }, 35.05);
      inUp("#s8-a", 35.13);
      inBig("#s8-imp", 36.06);
      const P = document.getElementById("s8-path"), L = 1400;
      tl.fromTo(P, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 0.7, ease: "power2.inOut" }, 36.2);

      // ---------- S9 · 37.55–47.25 (desk + wall) ----------
      tl.fromTo("#s9-stage", { scale: 1.25, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.9, ease: "power3.out" }, 37.55);
      tl.fromTo("#s9-host", { scale: 1.08 }, { scale: 1.0, duration: 9.7, ease: "none" }, 37.55);
      tl.fromTo(".wall .tile", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out", stagger: 0.03 }, 37.65);
      const P9 = ["#s9-p0", "#s9-p1", "#s9-p2", "#s9-p3"], F9 = ["#s9-f0", "#s9-f1", "#s9-f2", "#s9-f3"], T9 = [37.64, 40.8, 42.75, 44.14];
      tl.set([...P9, ...F9], { opacity: 0 }, 37.55);
      T9.forEach((at, i) => {
        if (i) { tl.to([P9[i - 1], F9[i - 1]], { opacity: 0, duration: 0.15 }, at - 0.1); tl.to(`.wall .h${i}`, { opacity: 0, duration: 0.15 }, T9[i + 1] ? T9[i + 1] - 0.1 : 99); }
        tl.fromTo(P9[i], { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, at);
        tl.fromTo(F9[i], { opacity: 0, scale: 0.9, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }, at + 0.05);
        if (i) tl.to(`.wall .h${i}`, { opacity: 1, duration: 0.2, stagger: 0.04 }, at);
      });
      // live countdown from 14:59 once the counter is introduced
      for (let s = 0; s <= 3; s++) {
        const txt = `14:${String(59 - s).padStart(2, "0")}`;
        tl.set(["#s9-cd", "#s9-cd1", "#s9-cd2"], { textContent: txt }, 44.14 + s);
      }
      tl.set(["#s9-cd", "#s9-cd1", "#s9-cd2"], { textContent: "14:59" }, 37.55);
      tl.to("#s9-wl", { rotationY: 32, duration: 9.7, ease: "none" }, 37.55);
      tl.to("#s9-wr", { rotationY: -32, duration: 9.7, ease: "none" }, 37.55);

      // ---------- S10 · 47.25–49.45 ----------
      cam("#s10", 47.25, 49.45, 1.04, 1.1, "50%", "48%"); lips("s10-mouth", 47.25, 49.45);
      tl.set("#s10-lead", { opacity: 0 }, 47.25);
      inUp("#s10-a", 47.37);
      inBig("#s10-lead", 48.75);

      // ---------- S11 · 49.45–53.55 ----------
      cam("#s11", 49.45, 53.55, 1.22, 1.3, "50%", "47%"); lips("s11-mouth", 49.45, 53.55);
      tl.set(["#s11-a", "#s11-b", "#s11-c", "#s11-compra"], { opacity: 0 }, 49.45);
      tl.set("#s11-a", { opacity: 1 }, 49.49); selIn("#s11-a .sel", 49.49);
      tl.set("#s11-b", { opacity: 1 }, 50.43); selIn("#s11-b .sel", 50.43);
      inUp("#s11-c", 51.21);
      out(["#s11-a", "#s11-b"], 52.1); inBig("#s11-compra", 52.3);
      tl.to("#s11-compra", { color: "#e8382d", duration: 0.25 }, 52.75);

      // ---------- S12 · 53.55–57.5 (end card) ----------
      (function endDots() {
        const host = document.getElementById("s12-dots");
        for (let i = 0; i < 16; i++) {
          const d = document.createElement("div");
          d.id = `s12-d${i}`;
          d.style.cssText = `position:absolute;width:10px;height:10px;background:#141217;left:${60 + Math.round(rnd() * 960)}px;top:${520 + Math.round(rnd() * 820)}px`;
          host.appendChild(d);
          tl.fromTo(d, { opacity: 0 }, { opacity: 1, duration: 0.05 }, 53.6 + rnd() * 1.2);
          tl.to(d, { opacity: 0, duration: 0.05 }, 55.2 + rnd() * 1.6);
        }
      })();
      tl.set(["#s12-lock", "#s12-sub"], { opacity: 0 }, 53.55);
      tl.fromTo("#s12-cta", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 53.6);
      const CTA = "comenta QUIZ";
      tl.set("#s12-typed", { textContent: "" }, 53.55);
      for (let i = 1; i <= CTA.length; i++) tl.set("#s12-typed", { textContent: CTA.slice(0, i) }, 53.8 + i * 0.07);
      tl.fromTo("#s12-l", { x: 30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 54.7);
      tl.fromTo("#s12-r", { x: -30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 54.7);
      tl.fromTo("#s12-lock", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 55.3);
      tl.fromTo("#s12-chip", { scale: 0, rotation: -20 }, { scale: 1, rotation: 0, duration: 0.4, ease: "back.out(3)" }, 55.5);
      inUp("#s12-sub", 55.9);
      tl.to(["#s12-l", "#s12-r"], { x: (i) => (i ? 12 : -12), duration: 0.5, yoyo: true, repeat: 2, ease: "sine.inOut" }, 56.0);
      tl.set({}, {}, 57.5);

      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
