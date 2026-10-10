#!/usr/bin/env python3
"""SaaS in House phone screen for the whiteboard-ad reveal: quiz-funnel result + offer + live countdown.

make_screen(w, h, seconds_left, ui) -> float32 RGB array (h, w, 3). Rendered at 2x, downsampled.
ui keys (all optional): fonts (dir with Archivo.ttf, Silkscreen-400/700.ttf), label, headline (list
of lines), offer, button.  Preview:  python3 phone_ui.py fonts_dir out.png
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BG, SURF, LINE = (11, 11, 16), (20, 20, 29), (48, 47, 58)
RED, DEEP, CREAM, MUTED, GOLD = (232, 56, 45), (126, 20, 13), (242, 239, 230), (163, 161, 173), (245, 197, 27)


def _arch(d, size, wght=900, wdth=118):
    f = ImageFont.truetype(os.path.join(d, "Archivo.ttf"), size)
    try:
        f.set_variation_by_axes([wght, wdth])
    except Exception:
        pass
    return f


def make_screen(w, h, secs, ui=None):
    ui = ui or {}
    fd = ui.get("fonts", "fonts")
    S = 2
    W, H = w * S, h * S
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    px = lambda s, b=False: ImageFont.truetype(os.path.join(fd, f"Silkscreen-{700 if b else 400}.ttf"), int(s * W / 1000))
    ar = lambda s, wg=900: _arch(fd, int(s * W / 1000), wg)
    u = W / 1000  # layout unit: 1000 = screen width
    # faint 60-unit grid like the brand films
    for x in range(0, W, int(70 * u)):
        d.line([(x, 0), (x, H)], fill=(18, 18, 25), width=max(1, int(2 * u)))
    for y in range(0, H, int(70 * u)):
        d.line([(0, y), (W, y)], fill=(18, 18, 25), width=max(1, int(2 * u)))
    y = 150 * u
    # wordmark: SaaS [IN] House
    f1, fchip = ar(92), px(46, True)
    x = 80 * u
    d.text((x, y), "SaaS", font=f1, fill=CREAM)
    x += d.textlength("SaaS", font=f1) + 24 * u
    cw = d.textlength("IN", font=fchip) + 36 * u
    d.rounded_rectangle([x + 8 * u, y + 22 * u, x + cw + 8 * u, y + 110 * u], 14 * u, fill=DEEP)
    d.rounded_rectangle([x, y + 14 * u, x + cw, y + 102 * u], 14 * u, fill=RED)
    d.text((x + 18 * u, y + 30 * u), "IN", font=fchip, fill=CREAM)
    d.text((x + cw + 24 * u, y), "House", font=f1, fill=CREAM)
    # progress
    y = 380 * u
    d.text((80 * u, y), ui.get("progress", "PREGUNTA 8/8"), font=px(34), fill=MUTED)
    d.rounded_rectangle([80 * u, y + 60 * u, 920 * u, y + 82 * u], 11 * u, fill=LINE)
    d.rounded_rectangle([80 * u, y + 60 * u, 920 * u, y + 82 * u], 11 * u, fill=RED)
    # result
    y = 570 * u
    d.text((80 * u, y), ui.get("label", "TU RESULTADO"), font=px(40, True), fill=GOLD)
    y += 80 * u
    for line in ui.get("headline", ["Tu SaaS ya tiene", "tráfico. Le falta", "segmentarlo."]):
        d.text((80 * u, y), line, font=ar(78, 800), fill=CREAM)
        y += 96 * u
    # offer card
    y += 60 * u
    d.rounded_rectangle([60 * u, y, 940 * u, y + 560 * u], 34 * u, fill=SURF, outline=LINE, width=int(3 * u))
    d.text((110 * u, y + 50 * u), ui.get("offer", "OFERTA PARA TI"), font=px(40, True), fill=RED)
    d.text((110 * u, y + 120 * u), ui.get("offer_sub", "Plan a medida de tu caso"), font=ar(52, 700), fill=CREAM)
    d.text((110 * u, y + 220 * u), "TERMINA EN", font=px(32), fill=MUTED)
    secs = max(0, secs)
    cd = f"{secs // 60:02d}:{secs % 60:02d}"
    d.text((110 * u, y + 275 * u), cd, font=px(170, True), fill=RED)
    # button
    y += 640 * u
    d.rounded_rectangle([70 * u, y + 12 * u, 940 * u, y + 172 * u], 30 * u, fill=DEEP)
    d.rounded_rectangle([60 * u, y, 930 * u, y + 160 * u], 30 * u, fill=RED)
    fb = px(48, True)
    bt = ui.get("button", "CANJEAR  >")
    d.text((495 * u - d.textlength(bt, font=fb) / 2, y + 52 * u), bt, font=fb, fill=CREAM)
    a = np.asarray(im.resize((w, h), Image.LANCZOS)).astype(np.float32)
    # subtle screen glare
    yy, xx = np.mgrid[0:h, 0:w]
    a += (np.clip(1 - (xx / w + yy / h * 0.6), 0, 1) ** 3 * 18)[..., None]
    return np.clip(a, 0, 255)


if __name__ == "__main__":
    Image.fromarray(make_screen(474, 1024, 899, {"fonts": sys.argv[1]}).astype(np.uint8)).save(sys.argv[2])
