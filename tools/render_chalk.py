#!/usr/bin/env python3
"""Chalkboard explainer renderer: reveals a finished chalkboard image stroke by stroke over an
empty board, with a hand holding chalk following the drawing point. No AI video needed.

Usage: python3 render_chalk.py config.json out.mp4 [--preview t1,t2,...]
"""
import json
import math
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

cfg = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
PREVIEW = [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 3 and sys.argv[3] == "--preview" else None
W, H, FPS = 1080, 1920, 30
G = cfg["geometry"]  # scale + offset from source board px to output px
sc, ox, oy = G["scale"], G["ox"], G["oy"]


def place(img):
    """Scale source-board image into the 1080x1920 frame, padding with replicated wall."""
    im = Image.open(img).convert("RGB")
    im = im.resize((round(im.size[0] * sc), round(im.size[1] * sc)), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    canvas = np.zeros((H, W, 3), np.float32)
    # source pixel (x,y) -> (x*sc+ox, y*sc+oy); fill by edge-replicating out-of-range coords
    ys = np.clip(np.arange(H) - oy, 0, a.shape[0] - 1).astype(int)
    xs = np.clip(np.arange(W) - ox, 0, a.shape[1] - 1).astype(int)
    canvas[:] = a[ys][:, xs]
    return canvas


final, empty = place(cfg["final"]), place(cfg["empty"])
Lf, Le = final.mean(-1), empty.mean(-1)
# chalk alpha: how much brighter the finished board is than the empty one
A = np.clip((Lf - Le - 18) / 45, 0, 1)
A = ndimage.gaussian_filter(A, 0.6)
chalk = A > 0.05


def box_out(b):  # source-board box -> output px box
    x0, y0, x1, y1 = b
    return (int(x0 * sc + ox), int(y0 * sc + oy), int(x1 * sc + ox), int(y1 * sc + oy))


T = np.full((H, W), np.inf, np.float32)  # time each pixel gets drawn
assigned = np.zeros((H, W), bool)
strokes = []  # per element: list of (t, x, y) samples of the pen path, for the hand

# assignment priority = list order; draw time = element's own start/dur
for el in cfg["elements"]:
    x0, y0, x1, y1 = box_out(el["box"])
    region = np.zeros((H, W), bool)
    region[y0:y1, x0:x1] = True
    m = chalk & region & ~assigned
    assigned |= m
    el["_mask"] = m

for el in cfg["elements"]:
    m, kind = el["_mask"], el.get("kind", "text")
    if not m.any():
        continue
    lab, n = ndimage.label(ndimage.binary_dilation(m, iterations=2 if kind == "text" else 4))
    lab = lab * m
    comps = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        if sl is None:
            continue
        ys, xs = np.where(lab[sl] == i)
        if len(xs) < 12:
            continue
        comps.append((ys + sl[0].start, xs + sl[1].start))
    # component order: text = reading order (line band, then x); drawing = top-to-bottom, left-to-right
    lines = el.get("lines", 1)
    by0, by1 = box_out(el["box"])[1], box_out(el["box"])[3]
    lh = (by1 - by0) / lines

    def key(c):
        cy, cx = c[0].mean(), c[1].mean()
        band = min(lines - 1, int((cy - by0) / lh)) if kind == "text" else 0
        return (band, cx) if kind == "text" else (round(c[0].min() / 40), cx)

    comps.sort(key=key)
    sizes = np.array([len(c[0]) for c in comps], float)
    # each component gets time proportional to its ink (+ a small pen-lift gap)
    weights = sizes ** 0.85 + 30
    t0, dur = el["start"], el["dur"]
    cum = np.concatenate([[0], np.cumsum(weights)]) / weights.sum() * dur
    path = []
    for (ys, xs), a, b in zip(comps, cum[:-1], cum[1:]):
        b = a + (b - a) * 0.88  # leave a little lift between letters
        cy, cx = ys.mean(), xs.mean()
        h, w = np.ptp(ys) + 1, np.ptp(xs) + 1
        if kind != "text" and h > 25 and w > 25:
            # closed-ish shape: trace around the centroid starting at the top, clockwise
            ang = (np.arctan2(xs - cx, -(ys - cy)) + 2 * np.pi) % (2 * np.pi)
            f = ang / (2 * np.pi)
        elif kind != "text":
            f = (ys - ys.min()) / h if h >= w else (xs - xs.min()) / w
        else:
            # letter: diagonal sweep top-left -> bottom-right feels like strokes
            f = ((ys - ys.min()) / max(h, 1) * 0.65 + (xs - xs.min()) / max(w, 1) * 0.35)
        f = (f - f.min()) / max(np.ptp(f), 1e-6)
        T[ys, xs] = t0 + a + f * (b - a)
        # pen path samples: follow the ink front inside this component
        for k in np.linspace(0, 1, max(3, int((b - a) * FPS * 2))):
            sel = np.abs(f - k) < 0.08
            if sel.any():
                path.append((t0 + a + k * (b - a), xs[sel].mean(), ys[sel].mean()))
    strokes.append(path)

pen = sorted(p for s in strokes for p in s)
pen_t = np.array([p[0] for p in pen])
pen_xy = np.array([[p[1], p[2]] for p in pen])

# ---- hand sprite: extend the forearm along its axis so it always leaves the frame ----
hand = Image.open(cfg["hand"]).convert("RGBA")
ang = cfg.get("arm_angle_deg", 23)  # arm axis tilt from vertical (toward the right)
r = hand.rotate(-ang, expand=True, resample=Image.BICUBIC)
ra = np.asarray(r).copy()
rows = np.where(ra[..., 3].max(1) > 0)[0]
# cut where the forearm is widest and still whole (lower part may be clipped by the source crop)
lo, hi = rows[0] + int(0.55 * len(rows)), rows[0] + int(0.85 * len(rows))
widths = (ra[lo:hi, :, 3] > 128).sum(1)
cut = lo + int(np.argmax(widths))
ext = np.repeat(ra[cut][None], 1400, 0).astype(np.float32)
# borrow the real skin texture: tile the 120 rows above the cut (minus their mean) onto the flat extension
blk = ra[cut - 120 : cut].astype(np.float32)
solid = (blk[..., 3:] > 250) & (ra[cut][None, :, 3:] > 250)  # skin in both: no edge pixels
tex = (blk[..., :3] - blk[..., :3].mean(0, keepdims=True)) * solid
tex = np.concatenate([tex, tex[::-1]], 0)  # mirrored tiles: no seams
ext[..., :3] += np.tile(tex, (6, 1, 1))[:1400] * 0.8
ext = np.clip(ext, 0, 255).astype(np.uint8)
ra2 = np.concatenate([ra[:cut], ext], 0)
hand2 = Image.fromarray(ra2).rotate(ang, expand=True, resample=Image.BICUBIC)
hand2 = hand2.rotate(cfg.get("sprite_rotate_deg", 0), expand=True, resample=Image.BICUBIC)  # + = arm more horizontal
hs = cfg.get("hand_scale", 0.78)
hand2 = hand2.resize((round(hand2.size[0] * hs), round(hand2.size[1] * hs)), Image.LANCZOS)
H2 = np.asarray(hand2).astype(np.float32)
# chalk tip = top-left-most bright opaque pixel
hb = (H2[..., 3] > 200) & (H2[..., :3].min(-1) > 215)
ys, xs = np.where(hb)
i = np.argmin(xs + ys)
TIP = np.array([xs[i], ys[i]], float)
hand_rgb, hand_a = H2[..., :3], H2[..., 3:] / 255


def pen_pos(t):
    """Smoothed pen position; between elements the hand drifts down-right off the ink."""
    if t < pen_t[0] - 0.6:
        return np.array([W + 200, H * 0.75]), False
    j = np.searchsorted(pen_t, t)
    if j == 0:
        a = (t - (pen_t[0] - 0.6)) / 0.6
        return np.array([W + 200, H * 0.75]) * (1 - a) + pen_xy[0] * a, False
    if j >= len(pen_t):
        dt = t - pen_t[-1]
        a = min(1, dt / 0.7)
        return pen_xy[-1] * (1 - a) + np.array([W + 300, H + 200]) * a, False
    ta, tb = pen_t[j - 1], pen_t[j]
    pa, pb = pen_xy[j - 1], pen_xy[j]
    gap = tb - ta
    u = (t - ta) / max(gap, 1e-6)
    if gap > 0.5:  # pause: lift and rest just below-right of the last mark, then travel
        rest = pa + np.array([60, 90])
        if u < 0.35:
            return pa + (rest - pa) * (u / 0.35), False
        if u < 0.7:
            return rest, False
        v = (u - 0.7) / 0.3
        v = v * v * (3 - 2 * v)
        return rest + (pb - rest) * v, False
    return pa + (pb - pa) * u, True


def comp_hand(frame, t):
    p, writing = pen_pos(t)
    p = p.copy()
    if writing:  # tiny tremor while writing
        p += np.array([math.sin(t * 41) * 1.5, math.cos(t * 37) * 1.5])
    x0, y0 = int(round(p[0] - TIP[0])), int(round(p[1] - TIP[1]))
    hh, hw = hand_a.shape[:2]
    fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + hw), min(H, y0 + hh)
    if fx0 >= fx1 or fy0 >= fy1:
        return
    sx0, sy0 = fx0 - x0, fy0 - y0
    a = hand_a[sy0 : sy0 + fy1 - fy0, sx0 : sx0 + fx1 - fx0]
    # soft contact shadow, offset down-right
    sh = ndimage.shift(a[..., 0], (14, 18), order=0) * 0.25
    reg = frame[fy0:fy1, fx0:fx1]
    reg *= 1 - sh[..., None]
    frame[fy0:fy1, fx0:fx1] = reg * (1 - a) + hand_rgb[sy0 : sy0 + fy1 - fy0, sx0 : sx0 + fx1 - fx0] * a


FADE = 0.06
diff = final - empty


def frame_at(t):
    m = np.clip((t - T) / FADE, 0, 1) * A
    f = empty + diff * m[..., None]
    comp_hand(f, t)
    return np.clip(f, 0, 255).astype(np.uint8)


DUR = cfg["duration"]
if PREVIEW:
    for t in PREVIEW:
        Image.fromarray(frame_at(t)).save(f"{OUT}_{t:05.2f}.jpg", quality=88)
    sys.exit()

ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                       "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                       "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for k in range(int(DUR * FPS)):
    ff.stdin.write(frame_at(k / FPS).tobytes())
ff.stdin.close()
ff.wait()
print("video ->", OUT)
