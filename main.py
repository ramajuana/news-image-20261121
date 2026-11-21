#!/usr/bin/env python3
"""news-image-20261121 -- "THE WORLD TODAY": one image summing up the world
news of Saturday 21 November 2026.

The program draws a newspaper front page as a PNG using only the Python
standard library: its own 5x7 pixel font, its own drawing primitives and its
own PNG encoder (zlib). No network, no clock, no randomness -- two runs
write byte-identical files.

Run it the way the grader does:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out python3 main.py

It writes entry.png into MAKEFUN_OUTPUT_DIR (default /output).

The stories are the day's most consequential, as reported on 21 Nov 2026 by
the BBC, AP, Reuters, UN News and Al Jazeera:

  * Russian missiles and a drone land in Poland near allied drills;
    PM Tusk calls it a deliberate provocation, NATO's Rutte heads to Warsaw.
  * Denmark expels a Russian diplomat; Copenhagen accuses Moscow of a plot
    to kill a US-Ukrainian rapper.
  * Trump threatens a ban on US firms building AI data centres overseas.
  * A tech sell-off rocks markets; Anthropic shares slide, S&P 500 -3.7%.
  * COP31 climate talks in Antalya spill into overtime after fossil-fuel
    wording is cut from the draft deal.
  * Anthropic's AI may have solved the Riemann puzzle, maths' biggest
    open problem (BBC).
  * Trump says Iran wants a deal to end the conflict (AP).
  * Cost-of-living protests spread as workers and students march in Europe.
  * England captain Harry Kane is out for 'a few months' with an ankle
    ligament tear.
"""

import math
import os
import struct
import zlib

# --------------------------------------------------------------------------
# 5x7 pixel font. Each glyph is 7 rows of 5 pixels, '#' = ink.
# --------------------------------------------------------------------------

FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".##..", ".#...", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "..#..", "..#..", ".....", "..#.."),
    "%": ("##..#", "##.#.", "...#.", "..#..", ".#...", ".#.##", "#..##"),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "/": ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
}

INK = (20, 22, 26)
PAPER = (246, 241, 227)
PANEL = (255, 253, 246)
RED = (163, 22, 33)
NAVY = (29, 62, 110)
GREEN = (24, 96, 56)
TEAL = (12, 102, 108)
PURPLE = (92, 48, 130)
BROWN = (150, 84, 20)
GREY = (70, 74, 80)
WHITE = (255, 255, 255)
ICON_BG = (238, 233, 218)


# --------------------------------------------------------------------------
# Canvas: a plain RGB pixel buffer plus drawing primitives.
# --------------------------------------------------------------------------

class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg) * (w * h)

    def set_px(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def frame_rect(self, x, y, w, h, color, t=2):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def fill_circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            dy = yy - cy
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.fill_rect(cx - dx, yy, 2 * dx + 1, 1, color)

    def ring_circle(self, cx, cy, r, color, t=2):
        for yy in range(cy - r - t, cy + r + t + 1):
            for xx in range(cx - r - t, cx + r + t + 1):
                d = math.hypot(xx - cx, yy - cy)
                if r - t <= d <= r:
                    self.set_px(xx, yy, color)

    def line(self, x0, y0, x1, y1, color, t=2):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            x = x0 + (x1 - x0) * i // steps
            y = y0 + (y1 - y0) * i // steps
            self.fill_rect(x - t // 2, y - t // 2, t, t, color)

    # -- text ---------------------------------------------------------------

    def text_width(self, s, scale):
        if not s:
            return 0
        return len(s) * 6 * scale - scale

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[" "])
            for gy, row in enumerate(glyph):
                for gx, cell in enumerate(row):
                    if cell == "#":
                        self.fill_rect(cx + gx * scale, y + gy * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx

    def text_centered(self, cx, y, s, scale, color):
        x = cx - self.text_width(s, scale) // 2
        self.text(x, y, s, scale, color)

    def wrap(self, s, scale, max_w):
        words = s.split()
        lines = []
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if self.text_width(trial, scale) <= max_w:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


# --------------------------------------------------------------------------
# Icons. Each draws inside a 40x40 box at (x, y) unless noted.
# --------------------------------------------------------------------------

def icon_door(cv, x, y, color):
    # A door with an arrow leaving it: expulsion.
    cv.frame_rect(x + 4, y + 3, 16, 34, color, 3)
    cv.line(x + 14, y + 20, x + 34, y + 20, color, 4)
    cv.line(x + 27, y + 12, x + 35, y + 20, color, 4)
    cv.line(x + 27, y + 28, x + 35, y + 20, color, 4)


def icon_chip(cv, x, y, color):
    cv.frame_rect(x + 9, y + 9, 22, 22, color, 3)
    cv.frame_rect(x + 16, y + 16, 8, 8, color, 2)
    for i in range(3):
        px = x + 13 + i * 7
        cv.fill_rect(px, y + 2, 3, 7, color)
        cv.fill_rect(px, y + 31, 3, 7, color)
        py = y + 13 + i * 7
        cv.fill_rect(x + 2, py, 7, 3, color)
        cv.fill_rect(x + 31, py, 7, 3, color)


def icon_chart_down(cv, x, y, color):
    cv.line(x + 5, y + 4, x + 5, y + 35, color, 3)
    cv.line(x + 5, y + 35, x + 36, y + 35, color, 3)
    cv.line(x + 8, y + 10, x + 17, y + 17, color, 4)
    cv.line(x + 17, y + 17, x + 22, y + 12, color, 4)
    cv.line(x + 22, y + 12, x + 33, y + 27, color, 4)
    cv.line(x + 26, y + 27, x + 34, y + 27, color, 4)
    cv.line(x + 34, y + 19, x + 34, y + 28, color, 4)


def icon_globe(cv, x, y, color):
    cx, cy = x + 20, y + 20
    cv.ring_circle(cx, cy, 15, color, 2)
    cv.line(cx - 15, cy, cx + 15, cy, color, 2)
    cv.line(cx, cy - 15, cx, cy + 15, color, 2)
    for yy in range(cy - 15, cy + 16):
        dy = yy - cy
        half = math.sqrt(max(0, 15 * 15 - dy * dy))
        ex = half * 0.45
        cv.set_px(int(cx - ex), yy, color)
        cv.set_px(int(cx + ex), yy, color)


def icon_atom(cv, x, y, color):
    cx, cy = x + 20, y + 20
    cv.fill_circle(cx, cy, 3, color)
    for angle in (0.0, 60.0, 120.0):
        rad = math.radians(angle)
        ca, sa = math.cos(rad), math.sin(rad)
        for i in range(90):
            t = 2 * math.pi * i / 90
            ex, ey = 17 * math.cos(t), 7 * math.sin(t)
            px = cx + int(ex * ca - ey * sa)
            py = cy + int(ex * sa + ey * ca)
            cv.fill_rect(px - 1, py - 1, 2, 2, color)


def icon_bubble(cv, x, y, color):
    cv.frame_rect(x + 4, y + 6, 32, 20, color, 3)
    cv.line(x + 10, y + 26, x + 8, y + 36, color, 3)
    cv.line(x + 10, y + 26, x + 20, y + 26, color, 3)
    for i in range(3):
        cv.fill_circle(x + 12 + i * 8, y + 16, 2, color)


def icon_placard(cv, x, y, color):
    cv.frame_rect(x + 5, y + 4, 30, 20, color, 3)
    cv.line(x + 11, y + 14, x + 29, y + 14, color, 3)
    cv.fill_rect(x + 18, y + 24, 4, 13, color)


def icon_ball(cv, x, y, color):
    cx, cy = x + 20, y + 20
    cv.ring_circle(cx, cy, 16, color, 3)
    cv.fill_circle(cx, cy, 5, color)
    for dx, dy in ((-11, -9), (11, -9), (-13, 8), (13, 8), (0, 14)):
        cv.fill_circle(cx + dx, cy + dy, 3, color)


ICONS = {
    "door": icon_door,
    "chip": icon_chip,
    "chart": icon_chart_down,
    "globe": icon_globe,
    "atom": icon_atom,
    "bubble": icon_bubble,
    "placard": icon_placard,
    "ball": icon_ball,
}


def lead_scene(cv, x, y, w, h):
    """The lead picture: a missile falling past clouds, a burst over fields."""
    sky = (206, 224, 238)
    cv.fill_rect(x, y, w, h, sky)
    # clouds
    for cx, cy, r in ((38, 34, 13), (58, 28, 10), (150, 150, 12), (168, 142, 9)):
        cv.fill_circle(x + cx, y + cy, r, WHITE)
    # fields
    cv.fill_rect(x, y + h - 34, w, 34, (148, 168, 120))
    cv.fill_rect(x, y + h - 34, w, 3, (110, 130, 88))
    # missile, nose down-left, tail up-right with flame
    cv.line(x + 138, y + 36, x + 84, y + 108, (52, 56, 64), 17)
    cv.line(x + 84, y + 108, x + 66, y + 130, (52, 56, 64), 8)
    cv.line(x + 138, y + 36, x + 152, y + 22, RED, 7)
    cv.fill_circle(x + 158, y + 16, 7, (240, 150, 40))
    cv.fill_circle(x + 164, y + 10, 4, (250, 200, 90))
    # fins
    cv.line(x + 128, y + 52, x + 146, y + 58, (52, 56, 64), 6)
    cv.line(x + 122, y + 62, x + 128, y + 80, (52, 56, 64), 6)
    # burst where it lands
    bx, by = x + 52, y + h - 40
    for ang in range(0, 360, 24):
        rad = math.radians(ang)
        cv.line(bx, by, bx + int(24 * math.cos(rad)), by + int(19 * math.sin(rad)),
                (240, 150, 40), 5)
    cv.fill_circle(bx, by, 8, RED)
    cv.fill_circle(bx, by, 4, (250, 200, 90))


# --------------------------------------------------------------------------
# The page.
# --------------------------------------------------------------------------

def panel(cv, x, y, w, h, kicker, kcolor, head1, head2, label, icon):
    cv.fill_rect(x, y, w, h, PANEL)
    cv.frame_rect(x, y, w, h, INK, 2)
    cv.text(x + 14, y + 12, kicker, 2, kcolor)
    cv.fill_rect(x + w - 52, y + 10, 40, 40, ICON_BG)
    ICONS[icon](cv, x + w - 52, y + 10, kcolor)
    cv.text(x + 14, y + 34, head1, 4, INK)
    cv.text(x + 14, y + 68, head2, 4, INK)
    cv.text(x + 14, y + 104, label, 2, GREY)


def build_image():
    cv = Canvas(1000, 1000, PAPER)

    # Masthead.
    cv.text_centered(500, 34, "THE WORLD TODAY", 10, INK)
    cv.fill_rect(36, 112, 928, 4, INK)
    cv.fill_rect(36, 120, 928, 2, INK)

    # Date band.
    cv.fill_rect(20, 130, 960, 58, RED)
    cv.text_centered(500, 138, "SATURDAY 21 NOVEMBER 2026", 6, WHITE)

    # Lead story: Russian missiles land in Poland.
    lx, ly, lw, lh = 36, 204, 928, 224
    cv.fill_rect(lx, ly, lw, lh, PANEL)
    cv.frame_rect(lx, ly, lw, lh, INK, 3)
    lead_scene(cv, lx + 16, ly + 16, 190, 192)
    cv.frame_rect(lx + 16, ly + 16, 190, 192, INK, 2)
    tx = lx + 226
    cv.text(tx, ly + 18, "EUROPE - WAR IN UKRAINE", 2, RED)
    cv.text(tx, ly + 42, "RUSSIAN MISSILES", 6, INK)
    cv.text(tx, ly + 94, "LAND IN POLAND", 6, INK)
    label = "TUSK: A DELIBERATE PROVOCATION - NATO CHIEF RUTTE HEADS TO WARSAW"
    for i, line in enumerate(cv.wrap(label, 3, lw - 226 - 20)):
        cv.text(tx, ly + 154 + i * 30, line, 3, GREY)

    # The day's other stories, two columns by four rows.
    stories = [
        ("EUROPE", NAVY, "DENMARK EXPELS", "RUSSIAN ENVOY",
         "ACCUSED OF PLOT TO KILL RAPPER", "door"),
        ("UNITED STATES", NAVY, "TRUMP THREATENS", "AI DATA CENTRE BAN",
         "US FIRMS WARNED OVER CENTRES ABROAD", "chip"),
        ("MARKETS", GREEN, "TECH SELL-OFF", "ROCKS MARKETS",
         "S&P 500 -3.7% AS ANTHROPIC SLIDES", "chart"),
        ("CLIMATE", TEAL, "COP31 TALKS SPILL", "INTO OVERTIME",
         "FOSSIL FUEL WORDS CUT FROM DRAFT", "globe"),
        ("SCIENCE", PURPLE, "AI MAY HAVE SOLVED", "RIEMANN PUZZLE",
         "BIGGEST OPEN PROBLEM IN MATHS", "atom"),
        ("MIDDLE EAST", BROWN, "TRUMP: IRAN", "WANTS A DEAL",
         "TEHRAN SEEKS END TO CONFLICT - AP", "bubble"),
        ("EUROPE", NAVY, "COST-OF-LIVING", "PROTESTS SPREAD",
         "WORKERS, STUDENTS MARCH IN EUROPE", "placard"),
        ("SPORT", RED, "KANE OUT FOR", "'A FEW MONTHS'",
         "ANKLE INJURY SIDELINES CAPTAIN", "ball"),
    ]
    col_x = (36, 508)
    for i, (kicker, kc, h1, h2, label, icon) in enumerate(stories):
        x = col_x[i % 2]
        y = 440 + (i // 2) * 136
        panel(cv, x, y, 456, 128, kicker, kc, h1, h2, label, icon)

    return cv


# --------------------------------------------------------------------------
# PNG encoder (zlib streams are deterministic for a fixed level).
# --------------------------------------------------------------------------

def png_bytes(cv):
    raw = bytearray()
    row_len = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * row_len:(yy + 1) * row_len]

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(build_image())
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
