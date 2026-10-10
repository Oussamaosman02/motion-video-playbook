// Isometric SVG helpers from iso-data-twin (paste into a HyperFrames <script> after the gsap timeline 'tl' exists).
// P() projects plane (x,y,z) to screen; prism() extrudes any polygon with shaded visible sides; recolor() tweens every face;
// iris() is the octagon wipe; typeLine() is the per-character typewriter with cursor. Seek-safe: all DOM is built at load.
      /* ---------- isometric helpers ---------- */
      const C30 = Math.cos(Math.PI / 6);
      const P = (o, x, y, z) => [o.cx + (x - y) * C30 * o.s, o.cy + (x + y) * 0.5 * o.s - z * o.s];
      const pts = (a) => a.map((p) => p[0].toFixed(1) + "," + p[1].toFixed(1)).join(" ");
      const rgb = (h) => [1, 3, 5].map((i) => parseInt(h.substr(i, 2), 16));
      const shade = (h, f) => "#" + rgb(h).map((v) => Math.max(0, Math.min(255, Math.round(v * f))).toString(16).padStart(2, "0")).join("");
      const polyN = (n, r, rot, cx = 0, cy = 0) => Array.from({ length: n }, (_, i) => [cx + r * Math.cos(rot + (i * 2 * Math.PI) / n), cy + r * Math.sin(rot + (i * 2 * Math.PI) / n)]);
      const OCT = Math.PI / 8;
      const isoPoly = (o, poly, z, attrs, parent) => el("polygon", Object.assign({ points: pts(poly.map((p) => P(o, p[0], p[1], z))) }, attrs), parent);
      const isoLine = (o, poly, z, attrs, parent) => el("polyline", Object.assign({ points: pts(poly.map((p) => P(o, p[0], p[1], z))), fill: "none", "stroke-linecap": "round", "stroke-linejoin": "round" }, attrs), parent);
      // extruded prism: visible side faces (normal facing the viewer) shaded, then the top face
      function prism(parent, o, poly, z0, z1, col, opt = {}) {
        const g = el("g", {}, parent);
        const n = poly.length, mx0 = poly.reduce((s, p) => s + p[0], 0) / n, my0 = poly.reduce((s, p) => s + p[1], 0) / n;
        const sides = [];
        for (let i = 0; i < n; i++) {
          const a = poly[i], b = poly[(i + 1) % n];
          let nx = b[1] - a[1], ny = -(b[0] - a[0]);
          if (nx * ((a[0] + b[0]) / 2 - mx0) + ny * ((a[1] + b[1]) / 2 - my0) < 0) { nx = -nx; ny = -ny; }
          const L = Math.hypot(nx, ny); nx /= L; ny /= L;
          if (nx + ny <= 0.001) continue;
          sides.push({ a, b, f: 0.76 + 0.13 * (nx - ny), d: a[0] + b[0] + a[1] + b[1] });
        }
        sides.sort((u, v) => u.d - v.d);
        const faces = [];
        const st = { stroke: opt.stroke || "none", "stroke-width": opt.sw || 1, "stroke-linejoin": "round" };
        if (z1 - z0 > 0.001) sides.forEach((sd) => {
          const q = [P(o, sd.a[0], sd.a[1], z0), P(o, sd.b[0], sd.b[1], z0), P(o, sd.b[0], sd.b[1], z1), P(o, sd.a[0], sd.a[1], z1)];
          faces.push({ e: el("polygon", Object.assign({ points: pts(q), fill: shade(col, sd.f) }, st), g), f: sd.f });
        });
        const top = isoPoly(o, poly, z1, Object.assign({ fill: col }, st), g);
        faces.push({ e: top, f: 1 });
        return { g, faces, top };
      }
      const recolor = (pr, col, at, dur = 0.4) => pr.faces.forEach((fc) => tl.to(fc.e, { attr: { fill: shade(col, fc.f) }, duration: dur, ease: "power1.inOut" }, at));

      /* ---------- scenes (hard cuts under octagon irises) ---------- */
      const S = { s1: 0, s3: t(16), s4: t(27), s6: t(54), s7: t(74), s8: t(83), s9: t(89), s10: t(121), s11: 54.6 };
      const SC = [["s1", S.s1, S.s3], ["s3", S.s3, S.s4], ["s4", S.s4, S.s6], ["s6", S.s6, S.s7], ["s7", S.s7, S.s8], ["s8", S.s8, S.s9], ["s9", S.s9, S.s10], ["s10", S.s10, S.s11], ["s11", S.s11, END]];
      SC.forEach(([id, a, b]) => { tl.set("#" + id, { visibility: "visible" }, a); if (b < END) tl.set("#" + id, { visibility: "hidden" }, b); });

      // octagon iris: grows from the centre and covers the frame exactly at the cut
      function iris(col, a, b, cx = 540, cy = 960) {
        const p = el("polygon", { points: pts(polyN(8, 100, OCT, cx, cy)), fill: col, opacity: 0 }, $("iris"));
        tl.set(p, { opacity: 1 }, a);
        tl.fromTo(p, { scale: 0.02, rotation: -22.5, svgOrigin: `${cx} ${cy}` }, { scale: 13, rotation: 0, svgOrigin: `${cx} ${cy}`, duration: b - a, ease: "power3.in" }, a);
        tl.set(p, { opacity: 0 }, b);
      }

      /* ---------- typewriter headline: per-character, cursor, dim previous lines ---------- */
      function blinkEl(c, a, b) { for (let k = a; k < b - 0.25; k += 0.5) tl.set(c, { opacity: 0 }, k + 0.25).set(c, { opacity: 1 }, k + 0.5); }
      function typeLine(host, text, at, opts = {}) {
        const line = document.createElement("div");
        line.className = "hl " + (opts.cls || "");
        if (opts.style) line.style.cssText = opts.style;
        (typeof host === "string" ? $(host) : host).appendChild(line);
        const cps = opts.cps || 34, chars = [...text];
        chars.forEach((ch, k) => { const s = document.createElement("span"); s.textContent = ch; s.style.display = "none"; line.appendChild(s); tl.set(s, { display: "inline" }, at + k / cps); });
        const done = at + chars.length / cps;
        if (opts.cursor !== false) {
          const c = document.createElement("span"); c.className = "cur"; c.style.opacity = 0; line.appendChild(c);
          const end = opts.curEnd !== undefined ? opts.curEnd : done + 0.5;
          tl.set(c, { opacity: 1 }, at); blinkEl(c, done, end); tl.set(c, { opacity: 0 }, end);
        }
        return line;
      }
      const dim = (line, at, col = "#586075") => tl.to(line, { color: col, duration: 0.3 }, at);
      const counter = (node, from, to, at, dur, fmt = (v) => Math.round(v).toString()) => {
        const o = { v: from }; node.textContent = fmt(from);
        tl.to(o, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { node.textContent = fmt(o.v); } }, at);
      };
      const es = (v) => Math.round(v).toLocaleString("es-ES").replace(/,/g, ".");
      const thousands = (v) => { const n = Math.round(v); return n >= 1000 ? Math.floor(n / 1000) + "." + String(n % 1000).padStart(3, "0") : String(n); };
