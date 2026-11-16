#!/usr/bin/env python3
"""ai-excited-01 v2 — LAVA SURF PENGUIN.

A colossal wave of glowing lava curls over a night volcano and a tiny
penguin rides it on a red surfboard, scarf streaming, sparks flying at
the viewer. One look: a giant orange diagonal, a brave little penguin.

Drawn procedurally, Python 3.13 standard library only, no network, fully
deterministic. Writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).
"""
import math
import os
import random
import struct
import zlib

W = H = 1024


def clamp(v, lo=0, hi=255):
    return lo if v < lo else hi if v > hi else v


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return (int(lerp(c1[0], c2[0], t)),
            int(lerp(c1[1], c2[1], t)),
            int(lerp(c1[2], c2[2], t)))


class Canvas:
    """An RGB canvas with flat-vector drawing primitives."""

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)

    def set(self, x, y, color):
        x = int(x)
        y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def blend(self, x, y, color, alpha):
        """Source-over blend, alpha 0..255, destination assumed opaque."""
        x = int(x)
        y = int(y)
        if alpha <= 0 or not (0 <= x < self.w and 0 <= y < self.h):
            return
        if alpha >= 255:
            self.set(x, y, color)
            return
        i = (y * self.w + x) * 3
        ia = 255 - alpha
        self.px[i] = (color[0] * alpha + self.px[i] * ia) // 255
        self.px[i + 1] = (color[1] * alpha + self.px[i + 1] * ia) // 255
        self.px[i + 2] = (color[2] * alpha + self.px[i + 2] * ia) // 255

    def add(self, x, y, color, alpha):
        """Additive blend (glow)."""
        x = int(x)
        y = int(y)
        if alpha <= 0 or not (0 <= x < self.w and 0 <= y < self.h):
            return
        i = (y * self.w + x) * 3
        self.px[i] = clamp(self.px[i] + color[0] * alpha // 255)
        self.px[i + 1] = clamp(self.px[i + 1] + color[1] * alpha // 255)
        self.px[i + 2] = clamp(self.px[i + 2] + color[2] * alpha // 255)

    def hline(self, x0, x1, y, color, alpha=255):
        """Inline hot path: one horizontal run, no per-pixel call."""
        y = int(y)
        if x0 > x1:
            x0, x1 = x1, x0
        x0 = max(0, int(x0))
        x1 = min(self.w - 1, int(x1))
        if x0 > x1 or not (0 <= y < self.h):
            return
        px = self.px
        i = (y * self.w + x0) * 3
        r, g, b = color
        if alpha >= 255:
            for _ in range(x0, x1 + 1):
                px[i] = r
                px[i + 1] = g
                px[i + 2] = b
                i += 3
            return
        ia = 255 - alpha
        for _ in range(x0, x1 + 1):
            px[i] = (r * alpha + px[i] * ia) // 255
            px[i + 1] = (g * alpha + px[i + 1] * ia) // 255
            px[i + 2] = (b * alpha + px[i + 2] * ia) // 255
            i += 3

    def vgrad(self, y0, y1, stops):
        """Vertical gradient between (pos, color) stops over [y0, y1]."""
        for y in range(max(0, y0), min(self.h, y1)):
            t = (y - y0) / max(1, y1 - y0)
            for k in range(len(stops) - 1):
                p0, c0 = stops[k]
                p1, c1 = stops[k + 1]
                if p0 <= t <= p1:
                    self.hline(0, self.w - 1, y,
                               lerp_color(c0, c1, (t - p0) / max(1e-9, p1 - p0)))
                    break

    def disc(self, cx, cy, r, color, alpha=255, feather=0):
        r = int(r)
        if r <= 0:
            return
        for dy in range(-r - feather, r + feather + 1):
            yy = cy + dy
            if not (0 <= yy < self.h):
                continue
            half = math.sqrt(max(0, r * r - dy * dy))
            a = alpha
            if feather and abs(dy) > r - feather:
                a = int(alpha * max(0.0, (r + feather - abs(dy)) / feather))
            self.hline(cx - half, cx + half, yy, color, a)

    def ellipse(self, cx, cy, rx, ry, color, alpha=255, rot=0.0):
        n = 48
        pts = []
        c, s = math.cos(rot), math.sin(rot)
        for k in range(n):
            a = 2 * math.pi * k / n
            x = rx * math.cos(a)
            y = ry * math.sin(a)
            pts.append((cx + x * c - y * s, cy + x * s + y * c))
        self.poly(pts, color, alpha)

    def poly(self, pts, color, alpha=255):
        """Scanline fill of a simple polygon."""
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        y0 = max(0, int(math.ceil(min(ys))))
        y1 = min(self.h - 1, int(math.floor(max(ys))))
        n = len(pts)
        for y in range(y0, y1 + 1):
            xs = []
            for k in range(n):
                x0, y0p = pts[k]
                x1, y1p = pts[(k + 1) % n]
                if (y0p <= y < y1p) or (y1p <= y < y0p):
                    t = (y - y0p) / (y1p - y0p)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.hline(xs[k], xs[k + 1], y, color, alpha)

    def thick_line(self, x0, y0, x1, y1, width, color, alpha=255):
        dist = math.hypot(x1 - x0, y1 - y0)
        steps = max(2, int(dist / max(1.0, width * 0.4)))
        for k in range(steps + 1):
            t = k / steps
            self.disc(lerp(x0, x1, t), lerp(y0, y1, t), width / 2, color, alpha)

    def bezier(self, pts, width, color, alpha=255, taper=1.0):
        segs = 40
        prev = None
        for k in range(segs + 1):
            t = k / segs
            p = _bezier_point(pts, t)
            if prev is not None:
                w = width * lerp(1.0, taper, t)
                self.thick_line(prev[0], prev[1], p[0], p[1], w, color, alpha)
            prev = p

    def glow(self, cx, cy, r, color, strength=160):
        """Additive radial glow; per-row squared distances, no hypot."""
        r = int(r)
        px = self.px
        w = self.w
        cr, cg, cb = color
        for dy in range(-r, r + 1):
            yy = cy + dy
            if not (0 <= yy < self.h):
                continue
            dy2 = dy * dy
            half = int(math.sqrt(max(0, r * r - dy2)))
            x0 = max(0, cx - half)
            x1 = min(w - 1, cx + half)
            base = (yy * w + x0) * 3
            for x in range(x0, x1 + 1):
                d = math.sqrt((x - cx) * (x - cx) + dy2) / r
                a = int(strength * (1 - d) * (1 - d))
                if a > 0:
                    i = base + (x - x0) * 3
                    px[i] = clamp(px[i] + cr * a // 255)
                    px[i + 1] = clamp(px[i + 1] + cg * a // 255)
                    px[i + 2] = clamp(px[i + 2] + cb * a // 255)

    def sparkle(self, cx, cy, size, color, alpha=255):
        """Four-point star."""
        s = size
        pts = [(cx, cy - s), (cx + s * 0.22, cy - s * 0.22),
               (cx + s, cy), (cx + s * 0.22, cy + s * 0.22),
               (cx, cy + s), (cx - s * 0.22, cy + s * 0.22),
               (cx - s, cy), (cx - s * 0.22, cy - s * 0.22)]
        self.poly(pts, color, alpha)
        self.disc(cx, cy, max(1, s * 0.22), color, alpha)

    def vignette(self, strength=70):
        """Darken only the corners: skip the interior band per row."""
        cx, cy = self.w / 2, self.h / 2
        maxd = math.hypot(cx, cy)
        r0 = 0.55 * maxd
        r02 = r0 * r0
        for y in range(self.h):
            dy = y - cy
            dy2 = dy * dy
            if dy2 >= r02:
                x_lo, x_hi = 0, self.w - 1
            else:
                dx = math.sqrt(r02 - dy2)
                x_lo, x_hi = int(cx - dx), int(cx + dx)
            for x in list(range(0, x_lo)) + list(range(x_hi + 1, self.w)):
                d = math.hypot(x - cx, dy) / maxd
                a = int(strength * ((d - 0.55) / 0.45) ** 2)
                self.blend(x, y, (8, 6, 20), a)


def _bezier_point(pts, t):
    if len(pts) == 3:  # quadratic
        (x0, y0), (x1, y1), (x2, y2) = pts
        u = 1 - t
        return (u * u * x0 + 2 * u * t * x1 + t * t * x2,
                u * u * y0 + 2 * u * t * y1 + t * t * y2)
    if len(pts) == 4:  # cubic
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
        u = 1 - t
        return (u ** 3 * x0 + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
                u ** 3 * y0 + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3)
    raise ValueError("bezier needs 3 or 4 points")


def write_png(canvas, path):
    """Deterministic RGB PNG (filter 0, zlib level 9)."""
    w, h = canvas.w, canvas.h
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += canvas.px[y * w * 3:(y + 1) * w * 3]
    data = zlib.compress(bytes(raw), 9)

    def chunk(tag, payload):
        c = struct.pack(">I", len(payload)) + tag + payload
        return c + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", data) + chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- scene ----
SKY = [(0.00, (12, 8, 30)), (0.45, (38, 16, 52)), (0.75, (86, 30, 52)),
       (1.00, (150, 52, 44))]
BASALT = (34, 22, 26)
LAVA_DEEP = (214, 72, 24)
LAVA = (255, 128, 32)
LAVA_HOT = (255, 196, 80)
LAVA_CORE = (255, 240, 170)
GOLD = (255, 190, 70)
PENGUIN = (16, 16, 24)
SCARF = (220, 40, 40)


def stroke_poly(cv, pts, width, color, alpha=255):
    for k in range(len(pts) - 1):
        cv.thick_line(pts[k][0], pts[k][1], pts[k + 1][0], pts[k + 1][1],
                      width, color, alpha)


def stamp_spiral(cv, cx, cy, r0, r1, a0, a1, width, color, steps=44):
    """A spiral drawn as stamped discs (fast, smooth)."""
    for k in range(steps + 1):
        t = k / steps
        a = a0 + (a1 - a0) * t
        r = r0 + (r1 - r0) * t
        cv.disc(cx + r * math.cos(a), cy + r * math.sin(a), width / 2, color)


def draw_penguin(cv, cx, cy, s, lean=-0.35, scarf=True):
    """A small brave penguin, facing left, flippers out. s = body height."""
    # scarf streaming up-right behind (motion is down-left)
    if scarf:
        cv.bezier([(cx - 6, cy - 0.30 * s), (cx + 60, cy - 0.62 * s),
                   (cx + 118, cy - 0.52 * s)], 0.13 * s, SCARF, taper=0.5)
        cv.bezier([(cx - 6, cy - 0.30 * s), (cx + 52, cy - 0.40 * s),
                   (cx + 96, cy - 0.22 * s)], 0.10 * s, (255, 80, 60),
                  taper=0.5)
    # body + belly
    cv.ellipse(cx, cy, 0.32 * s, 0.50 * s, PENGUIN, rot=lean)
    cv.ellipse(cx - 0.05 * s, cy + 0.08 * s, 0.21 * s, 0.36 * s,
               (250, 248, 240), rot=lean)
    # head
    hx, hy = cx - 0.10 * s, cy - 0.52 * s
    cv.disc(hx, hy, 0.27 * s, PENGUIN)
    # white face patches
    cv.ellipse(hx - 0.10 * s, hy - 0.02 * s, 0.11 * s, 0.13 * s,
               (250, 248, 240), rot=0.4)
    cv.ellipse(hx - 0.02 * s, hy - 0.10 * s, 0.09 * s, 0.12 * s,
               (250, 248, 240), rot=-0.3)
    # eyes: wide, thrilled
    cv.disc(hx - 0.13 * s, hy - 0.05 * s, 0.045 * s, (8, 8, 12))
    cv.disc(hx - 0.03 * s, hy - 0.11 * s, 0.045 * s, (8, 8, 12))
    cv.disc(hx - 0.12 * s, hy - 0.07 * s, 0.015 * s, (255, 255, 255))
    cv.disc(hx - 0.02 * s, hy - 0.13 * s, 0.015 * s, (255, 255, 255))
    # beak pointing left (direction of travel)
    cv.poly([(hx - 0.24 * s, hy + 0.04 * s), (hx - 0.42 * s, hy + 0.10 * s),
             (hx - 0.22 * s, hy + 0.14 * s)], (255, 150, 40))
    # scarf band around the neck
    cv.ellipse(hx + 0.02 * s, hy + 0.22 * s, 0.24 * s, 0.09 * s, SCARF,
               rot=lean)
    # flippers: one up waving, one out for balance
    cv.ellipse(cx - 0.34 * s, cy - 0.28 * s, 0.07 * s, 0.20 * s, PENGUIN,
               rot=0.9)
    cv.ellipse(cx + 0.30 * s, cy + 0.02 * s, 0.07 * s, 0.20 * s, PENGUIN,
               rot=-0.7)
    # feet on the board
    cv.ellipse(cx - 0.12 * s, cy + 0.50 * s, 0.09 * s, 0.05 * s,
               (255, 150, 40), rot=lean)
    cv.ellipse(cx + 0.12 * s, cy + 0.50 * s, 0.09 * s, 0.05 * s,
               (255, 150, 40), rot=lean)


def draw_scene(cv, rng):
    # night sky over the volcano
    cv.vgrad(0, H, SKY)
    for _ in range(110):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, 620)
        cv.disc(x, y, rng.uniform(1, 2.4), (255, 255, 255),
                alpha=rng.randint(50, 180))
    # rising embers
    for _ in range(70):
        x = rng.randint(0, W - 1)
        y = rng.randint(60, 980)
        cv.disc(x, y, rng.uniform(2, 5),
                GOLD if rng.random() < 0.6 else (255, 110, 40),
                alpha=rng.randint(90, 220))
    # glow behind the curl and along the flow
    cv.glow(880, 210, 420, (255, 120, 30), 110)
    cv.glow(520, 620, 300, (255, 140, 40), 70)
    # the lava wave: layered strokes along one spine curve
    spine = [(1060, 150), (860, 280), (600, 480), (360, 960)]
    cv.bezier(spine, 340, BASALT)
    cv.bezier(spine, 250, LAVA_DEEP)
    cv.bezier(spine, 160, LAVA)
    cv.bezier(spine, 84, LAVA_HOT)
    cv.bezier(spine, 34, LAVA_CORE)
    # the curling lip: a spiral at the top end of the wave
    for (r0, r1, w, col) in [(150, 52, 96, BASALT), (132, 46, 62, LAVA_DEEP),
                             (112, 40, 38, LAVA), (92, 34, 18, LAVA_HOT)]:
        stamp_spiral(cv, 880, 210, r0, r1, math.radians(100),
                     math.radians(470), w, col)
    cv.disc(880 + 52 * math.cos(math.radians(470)),
            210 + 52 * math.sin(math.radians(470)), 26, LAVA_CORE)
    # glowing cracks: short, jagged, inside the flow, along its direction
    cracks = [[(950, 330), (905, 385), (865, 430)],
              [(790, 520), (745, 575), (705, 625)],
              [(640, 660), (600, 720), (565, 775)],
              [(880, 560), (835, 615), (795, 665)],
              [(700, 360), (655, 410), (620, 455)]]
    for pts in cracks:
        stroke_poly(cv, pts, 11, LAVA_DEEP, alpha=130)
        stroke_poly(cv, pts, 5, (255, 220, 90))
    # splash where the flow crashes out of the frame at the bottom
    cv.glow(330, 1010, 260, (255, 140, 40), 90)
    for k in range(26):
        a = rng.uniform(-2.6, -0.5)
        r = rng.uniform(20, 170)
        x = 330 + r * math.cos(a)
        y = 1010 + r * math.sin(a) * 0.7
        cv.disc(x, y, rng.uniform(3, 9), LAVA_HOT,
                alpha=rng.randint(160, 255))
        if rng.random() < 0.35:
            cv.sparkle(x, y, rng.uniform(5, 9), LAVA_CORE)
    # crest spray: droplets flying off the lip
    for k in range(30):
        t = k / 29
        x = 900 - t * 260 + rng.uniform(-30, 30)
        y = 120 + t * 180 + rng.uniform(-40, 40)
        cv.disc(x, y, rng.uniform(3, 10), LAVA_HOT,
                alpha=rng.randint(150, 255))
        if rng.random() < 0.4:
            cv.sparkle(x, y, rng.uniform(5, 10), LAVA_CORE)
    # the surfer: red board, penguin riding the glowing face
    cv.thick_line(372, 712, 566, 668, 26, (200, 30, 30))
    cv.thick_line(372, 712, 566, 668, 14, (240, 60, 50))
    cv.thick_line(430, 700, 510, 684, 5, (255, 220, 200))
    draw_penguin(cv, 470, 612, 132)
    # a few sharp foreground droplets flying toward the viewer
    for _ in range(22):
        x = rng.randint(20, 1004)
        y = rng.randint(520, 1000)
        r = rng.uniform(4, 11)
        col = LAVA_HOT if rng.random() < 0.5 else LAVA_CORE
        cv.disc(x, y, r, col, alpha=rng.randint(150, 230))
    # rocky shore, bottom-left, with two tiny penguins watching
    cv.poly([(0, 1024), (0, 946), (120, 902), (260, 948), (310, 1024)],
            (22, 15, 19))
    cv.poly([(0, 946), (120, 902), (150, 922), (40, 962)], (40, 28, 32))
    draw_penguin(cv, 108, 872, 46, lean=-0.15, scarf=False)
    draw_penguin(cv, 182, 890, 40, lean=0.12, scarf=False)
    # sparkles in the spray
    for _ in range(16):
        cv.sparkle(rng.randint(300, 980), rng.randint(80, 700),
                   rng.uniform(4, 9), LAVA_CORE, alpha=rng.randint(140, 255))
    # grain + vignette
    for _ in range(1400):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        cv.blend(x, y, (255, 255, 255) if rng.random() < 0.5 else (0, 0, 0),
                 rng.randint(4, 12))
    cv.vignette(64)


def main():
    rng = random.Random(20261116)
    cv = Canvas(W, H)
    draw_scene(cv, rng)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    size = write_png(cv, path)
    print(f"wrote {path} ({size} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
