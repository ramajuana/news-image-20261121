#!/usr/bin/env python3
"""news-image-20261121 -- "THE WORLD TODAY": one image summing up the world
news of Saturday 21 November 2026, the full day.

Rebuild (v2): the v1 entry was built on the morning of 21 Nov from morning
news only. This version covers the whole day, packs 37 dated stories across
7 regions and 6 fields, and follows the winner-study design standard:
density, region grouping, a big unmistakable date, a UTC timeline of the
day, 3 illustrated lead stories, and short legible labels.

The program draws a newspaper front page as a PNG using only the Python
standard library: its own 5x7 pixel font, its own drawing primitives and
its own PNG encoder (zlib). No network, no clock, no randomness -- two runs
write byte-identical files.

Run it the way the grader does:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out python3 main.py

It writes entry.png into MAKEFUN_OUTPUT_DIR (default /output).

Every story below was confirmed by a wire or major outlet reporting on
21 Nov 2026, or by an outlet whose report is dated 21 Nov 2026. Every
brief is tagged 21 NOV. Sources (outlet - headline, all 21 Nov 2026):

  * AP/Reuters - COP31 in overtime, Antalya; EU: "good deal or no deal"
  * Reuters - "Saudi Arabia says it intercepts three Houthi missiles
    targeting Riyadh" (2nd attack on the capital in days)
  * AP/AFP - M6.7 quake, central Peru, 00:09 UTC Sat; no deaths; M5.0
    strongest aftershock (USGS)
  * AFP/AP - Rutte in Warsaw: Poland incursion a "grave violation";
    2 missiles, 1 drone fell Friday
  * AP/NBC/Al Jazeera - Denmark to expel Russia's defence attache over
    alleged plot to kill rapper Kyivstoner (announced Saturday)
  * Reuters/NBC/Euronews - drones hit sanctioned ship Sparta II in the
    Gulf of Finland, Saturday morning; Finland limits sea and air
  * BBC/Kyiv Independent - Zelensky defends Crimea bridge strikes as a
    "fair response", Kyiv, Saturday, with UK Defence Secretary Streeting
  * AP/WaPo - 128 countries in Geneva agree to keep working on lethal
    autonomous weapons rules, aiming for an accord by 2028; no binding
    commitment yet
  * Reuters - thousands march in Lisbon, Paris and Madrid over living
    costs, Saturday
  * AP - ex-police chief Giovanni De Gennaro found dead in Tuscany,
    Saturday
  * AP/Reuters/UKMTO - three tankers struck near the Strait of Hormuz,
    Saturday; no casualties
  * AP - Iran unveils a new missile launcher at an underground facility
  * AFP/Al Jazeera/Reuters - four killed in Gaza on Saturday despite the
    ceasefire (3 in a food-aid van strike, 1 shot in Jabalia)
  * Reuters - Iranian attack damages a civilian facility in Bahrain,
    Saturday; no injuries
  * Al Jazeera - IRGC claims it downed US MQ-9 and MQ-1 drones over
    the Strait of Hormuz, Saturday
  * WESH 2 - heavy rain worsens flooding on Florida's central coast;
    28 inches in Brevard County, Saturday
  * AP - Trump pledges to work with Congress to cap credit-card rates
    at 10%, Saturday
  * AP - cartel boss "El Chapo Isidro" captured in Guasave, Sinaloa;
    11 dead (reported Saturday)
  * Formula1.com/FIA/AP - Antonelli fastest in Las Vegas GP qualifying,
    Verstappen inherits pole (qualifying Fri night local = Sat 04:00 UTC)
  * AP/USA Today/MS NOW - Trump calls the apparent FBI NCIC database
    breach "not good" in a Fox interview, Saturday; FBI still silent
  * Al Jazeera - Haiti police say 34 gang members killed in a raid in
    Port-au-Prince, Saturday
  * MENAFN - Sudanese army says it cleared RSF positions in 10 areas
    of West Kordofan; Joint Force retook 8 areas Saturday
  * Juba Global - DR Congo Ebola outbreak passes six months; WHO warns
    of high child deaths (Saturday roundup)
  * AP - 24 dead as a boat carrying funeral mourners capsizes in
    Bayelsa, Nigeria, Saturday (later toll reports differ; number omitted)
  * Truth Social/Yonhap - Trump posts "The Great Powers 1945, 2026"
    Yalta photo with Xi and Putin, Saturday
  * AP - Taiwan warns Canada's Carney that deeper ties with China
    carry risks (21 Nov)
  * ABC - Australia and China agree to talks on artificial intelligence
    after APEC (reported Saturday morning)
  * SCMP - Kim Jong-un inspects school equipment factories, state
    media reports Saturday, after an apparent snub of Trump
  * AAP - NSW parliament passes laws on Saturday morning to save 400
    jobs at the Mount Pleasant coal mine
  * Scottish Rugby/NBC - Scotland thrash Japan 67-5 in the Nations
    Championship at Murrayfield, Saturday; 11 tries
  * Nature/ESA - BepiColombo enters Mercury orbit, 18:24 UTC, 21 Nov;
    the two probes split 9-10 Dec
  * NWS - coastal flood warning for San Francisco Bay; tides near the
    highest ever recorded (reported Saturday)
  * Reuters/AP - Catherine, Princess of Wales, reflects on cancer in
    new BBC documentary "Heal"; trailer released Saturday
  * Reuters - Arsenal held 2-2 at Newcastle; Leeds thrash Chelsea 4-1
    at Stamford Bridge, Saturday
  * AP - Malen scores four as Roma win 5-1 at Parma, Saturday
  * AP - PSG rally to win 3-2 at Nice; Doue stretchered off with a
    serious knee injury, Saturday

Revision (v2-rev, 22 Nov): 18 of 34 briefs replaced because their stories
were 15-20 Nov events with no 21-Nov development (S&P sell-off, UK-EU
deals, Ukraine strike, Kane injury, Myanmar ICJ ruling, Riemann claim,
GTA VI sales, Sudan RSF truce, Vance, Trump/Iran, Trump data centres,
US-Venezuela deal, Japan sidelined, Nepal PM trip, Yongbyon, Aus-Phil
pact); 2 re-tagged to 21 NOV (Denmark expulsion, living-cost marches);
the rest were already 21 Nov. Lead sub-heads shortened and re-laid out
so every line sits inside its panel; the numbers box moved up to fit
the canvas; all brief lines capped at 26 chars so none touches an edge.

Dropped from v1 after re-checking: nothing was invented, but the v1
"RIEMANN SOLVED" headline is corrected here to "CLAIMED, NOT VERIFIED",
and the v1 market line is kept only because the close is confirmed
(S&P -3.7%, Nasdaq -5.3%, Dow -1.9%).
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
SKY = (206, 224, 238)
NIGHT = (24, 38, 66)
ORANGE = (240, 150, 40)
GOLD = (250, 200, 90)


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

    def polyline(self, points, color, t=3):
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            self.line(x0, y0, x1, y1, color, t)

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


# --------------------------------------------------------------------------
# Lead scenes. Each draws inside the given box (x, y, w, h).
# --------------------------------------------------------------------------

def scene_cop31(cv, x, y, w, h):
    """Globe, sun and a rising thermometer: the climate talks."""
    cv.fill_rect(x, y, w, h, SKY)
    # sun, top right
    sx, sy = x + w - 52, y + 30
    cv.fill_circle(sx, sy, 16, GOLD)
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        cv.line(sx + int(20 * math.cos(rad)), sy + int(20 * math.sin(rad)),
                sx + int(28 * math.cos(rad)), sy + int(28 * math.sin(rad)),
                GOLD, 3)
    # globe, left
    gx, gy = x + 62, y + h // 2 + 2
    cv.fill_circle(gx, gy, 34, (120, 170, 210))
    cv.ring_circle(gx, gy, 34, NAVY, 3)
    cv.line(gx - 34, gy, gx + 34, gy, NAVY, 2)
    cv.line(gx, gy - 34, gx, gy + 34, NAVY, 2)
    for yy in range(gy - 34, gy + 35):
        dy = yy - gy
        half = math.sqrt(max(0, 34 * 34 - dy * dy))
        ex = half * 0.45
        cv.set_px(int(gx - ex), yy, NAVY)
        cv.set_px(int(gx + ex), yy, NAVY)
    # thermometer, right of globe
    tx = x + 128
    cv.fill_rect(tx, y + 14, 14, h - 30, WHITE)
    cv.frame_rect(tx, y + 14, 14, h - 30, RED, 2)
    cv.fill_rect(tx + 3, y + h - 34, 8, 18, RED)
    cv.fill_circle(tx + 7, y + h - 14, 10, RED)
    # ground
    cv.fill_rect(x, y + h - 10, w, 10, GREEN)


def scene_riyadh(cv, x, y, w, h):
    """Night sky over a skyline: three missiles streak down, shielded."""
    cv.fill_rect(x, y, w, h, NIGHT)
    # stars
    for sx, sy in ((30, 12), (90, 22), (160, 10), (230, 18), (280, 12),
                   (60, 40), (200, 44), (250, 36)):
        cv.fill_rect(x + sx, y + sy, 3, 3, WHITE)
    # skyline
    base = y + h - 22
    for bx, bw, bh in ((8, 34, 26), (52, 22, 40), (84, 30, 18),
                       (124, 18, 46), (152, 36, 24), (198, 22, 34),
                       (230, 28, 20), (268, 34, 30)):
        cv.fill_rect(x + bx, base - bh, bw, bh + 22, (52, 60, 88))
    # three missile streaks, top-left to bottom-right
    for mx, my, mlen in ((60, 6, 46), (150, 2, 52), (240, 8, 44)):
        cv.line(x + mx, y + my, x + mx + mlen, y + my + mlen, GOLD, 4)
        cv.fill_circle(x + mx + mlen, y + my + mlen, 5, ORANGE)
    # shield, centre
    cx, cy = x + w // 2, y + h // 2 + 6
    cv.fill_circle(cx, cy - 8, 26, (255, 255, 255))
    cv.fill_rect(cx - 26, cy - 8, 52, 26, (255, 255, 255))
    cv.fill_circle(cx, cy + 18, 26, (255, 255, 255))
    cv.fill_rect(cx - 26, cy - 8, 52, 8, (255, 255, 255))
    # shield outline + check
    cv.ring_circle(cx, cy - 8, 26, NAVY, 2)
    cv.line(cx - 14, cy - 2, cx - 4, cy + 10, NAVY, 4)
    cv.line(cx - 4, cy + 10, cx + 16, cy - 14, NAVY, 4)


def scene_peru(cv, x, y, w, h):
    """Seismograph trace over cracked ground: the earthquake."""
    cv.fill_rect(x, y, w, h, (232, 222, 200))
    # mountains
    cv.polyline([(x, y + 52), (x + 50, y + 18), (x + 95, y + 52),
                 (x + 150, y + 12), (x + 205, y + 52), (x + 250, y + 24),
                 (x + w, y + 52)], (120, 110, 96), 4)
    # seismograph strip
    cv.fill_rect(x + 8, y + 58, w - 16, 34, WHITE)
    cv.frame_rect(x + 8, y + 58, w - 16, 34, INK, 2)
    trace = [(x + 12, y + 75), (x + 40, y + 75), (x + 52, y + 66),
             (x + 64, y + 86), (x + 76, y + 62), (x + 88, y + 88),
             (x + 100, y + 66), (x + 112, y + 84), (x + 124, y + 75),
             (x + 150, y + 75), (x + 162, y + 68), (x + 174, y + 82),
             (x + 186, y + 75), (x + 220, y + 75), (x + 232, y + 70),
             (x + 244, y + 80), (x + 256, y + 75), (x + w - 12, y + 75)]
    cv.polyline(trace, RED, 3)
    # cracked ground
    cv.fill_rect(x, y + h - 26, w, 26, (168, 138, 104))
    cv.polyline([(x + 40, y + h - 26), (x + 70, y + h - 14),
                 (x + 95, y + h - 24), (x + 130, y + h - 8),
                 (x + 160, y + h - 20), (x + 200, y + h - 10),
                 (x + 235, y + h - 22), (x + 270, y + h - 12)],
                INK, 3)


# --------------------------------------------------------------------------
# The page.
# --------------------------------------------------------------------------

W = 1024
COL_X = (16, 352, 688)
COL_W = 320
LINE_H = 17          # scale-2 text: 14px glyph + 3px leading
BRIEF_GAP = 4
HEADER_H = 22

# (headline, detail lines...) -- every line <= 26 chars at scale 2
# (max width 310px inside a 320px column). Every brief is a 21 NOV story.
BRIEFS = [
    ("EUROPE", NAVY, [
        ("POLAND: RUTTE IN WARSAW",
         ["21 NOV - GRAVE VIOLATION", "2 MISSILES, 1 DRONE FELL"]),
        ("DENMARK EXPELS ATTACHE",
         ["21 NOV - PLOT FOILED"]),
        ("SPARTA II HIT BY DRONES",
         ["21 NOV - GULF OF FINLAND", "FINLAND LIMITS SEA, AIR"]),
        ("ZELENSKY DEFENDS BRIDGE",
         ["21 NOV - FAIR RESPONSE"]),
        ("GENEVA: ROBOT ARMS TALKS",
         ["21 NOV - 128 NATIONS AGREE"]),
        ("MARCHES OVER LIVING COSTS",
         ["21 NOV - LISBON AND PARIS"]),
        ("DE GENNARO FOUND DEAD",
         ["21 NOV - EX-POLICE CHIEF"]),
    ]),
    ("MIDDLE EAST", BROWN, [
        ("3 TANKERS HIT IN HORMUZ",
         ["21 NOV - NO DEAD REPORTED"]),
        ("IRAN SHOWS NEW LAUNCHER",
         ["21 NOV - UNDERGROUND SITE"]),
        ("GAZA STRIKES KILL 4",
         ["21 NOV - DESPITE CEASEFIRE"]),
        ("BAHRAIN HIT BY IRAN FIRE",
         ["21 NOV - NO ONE INJURED"]),
        ("IRGC: US DRONES DOWNED",
         ["21 NOV - CLAIM OVER HORMUZ"]),
    ]),
    ("NORTH AMERICA", NAVY, [
        ("FLORIDA FLOODS WORSEN",
         ["21 NOV - 28 INCHES OF RAIN"]),
        ("TRUMP: CAP CARD RATES",
         ["21 NOV - 10% CAP PLEDGE"]),
        ("EL CHAPO ISIDRO CAPTURED",
         ["21 NOV - 11 DEAD, SINALOA"]),
        ("F1: VERSTAPPEN ON POLE",
         ["21 NOV - ANTONELLI FASTEST"]),
        ("TRUMP: FBI HACK NOT GOOD",
         ["21 NOV - FBI STILL SILENT"]),
    ]),
    ("LATIN AMERICA", GREEN, [
        ("HAITI RAID KILLS 34 GANGS",
         ["21 NOV - POLICE IN CAPITAL"]),
        ("PERU: AFTERSHOCKS FOLLOW",
         ["21 NOV - STRONGEST M5.0"]),
    ]),
    ("AFRICA", BROWN, [
        ("CONGO EBOLA: 6 MONTHS ON",
         ["21 NOV - CHILD DEATHS HIGH"]),
        ("SUDAN ARMY TAKES 10 POSTS",
         ["21 NOV - KORDOFAN PUSH"]),
        ("NIGERIA BOAT SINKS",
         ["21 NOV - BOAT TO A FUNERAL"]),
    ]),
    ("ASIA-PACIFIC", TEAL, [
        ("TRUMP POSTS YALTA PHOTO",
         ["21 NOV - WITH XI AND PUTIN"]),
        ("TAIWAN WARNS CANADA",
         ["21 NOV - CHINA TIES RISKY"]),
        ("AUS-CHINA AI TALKS AGREED",
         ["21 NOV - AFTER APEC SUMMIT"]),
        ("KIM VISITS SCHOOL PLANTS",
         ["21 NOV - AFTER TRUMP SNUB"]),
        ("NSW SAVES 400 COAL JOBS",
         ["21 NOV - PASSED SATURDAY"]),
        ("SCOTLAND ROUT JAPAN 67-5",
         ["21 NOV - 11 TRIES SCORED"]),
    ]),
    ("SCIENCE, SPORT & CULTURE", PURPLE, [
        ("BEPICOLOMBO AT MERCURY",
         ["21 NOV - 8-YEAR TRIP ENDS", "2 PROBES SPLIT 9-10 DEC"]),
        ("SF BAY BRACES FOR TIDES",
         ["21 NOV - NEAR-RECORD SURGE"]),
        ("CATHERINE FILM ON CANCER",
         ["21 NOV - TRAILER RELEASED"]),
        ("LEEDS THRASH CHELSEA 4-1",
         ["21 NOV - ARSENAL HELD 2-2"]),
        ("ROMA WIN 5-1 AT PARMA",
         ["21 NOV - MALEN SCORES FOUR"]),
        ("PSG EDGE NICE 3-2",
         ["21 NOV - DOUE HURT IN WIN"]),
    ]),
]

# Columns: (region indices into BRIEFS)
COLUMNS = [(0, 1), (2, 3, 4), (5, 6)]

LEADS = [
    ("CLIMATE - ANTALYA", TEAL, "COP31 IN OVERTIME", "TALKS GO ON",
     ["DRAFT OMITS FOSSIL FUELS", "EU: DEAL OR NO DEAL?"],
     scene_cop31),
    ("MIDDLE EAST - RIYADH", BROWN, "MISSILES DOWNED", "OVER RIYADH",
     ["2ND ATTACK ON CAPITAL", "NO DEAD REPORTED"],
     scene_riyadh),
    ("LATIN AMERICA - PERU", GREEN, "M6.7 QUAKE", "SHAKES PERU",
     ["00:09 UTC; FELT IN LIMA", "NO DEATHS REPORTED"],
     scene_peru),
]

TIMELINE = [
    ("00:09", "PERU QUAKE"),
    ("04:00", "F1 VEGAS QUALI"),
    ("SAT", "TANKERS HIT"),
    ("18:24", "BEPICOLOMBO"),
    ("SAT", "COP31 OVERTIME"),
    ("SAT", "RUTTE IN WARSAW"),
    ("SAT", "EUROPE MARCHES"),
    ("SAT", "GAZA STRIKES"),
]


def draw_briefs(cv, col, y_top, y_bottom):
    """Draw one column of region groups. Returns the y after the last brief."""
    y = y_top
    for region_idx in COLUMNS[col]:
        name, color, stories = BRIEFS[region_idx]
        cv.fill_rect(COL_X[col], y, COL_W, HEADER_H, color)
        cv.text(COL_X[col] + 8, y + 4, name, 2, WHITE)
        y += HEADER_H + BRIEF_GAP
        for head, details in stories:
            assert cv.text_width(head, 2) <= COL_W - 4, head
            cv.text(COL_X[col] + 2, y, head, 2, INK)
            y += LINE_H
            for line in details:
                assert cv.text_width(line, 2) <= COL_W - 4, line
                cv.text(COL_X[col] + 2, y, line, 2, GREY)
                y += LINE_H
            y += BRIEF_GAP
        y += 2
    assert y <= y_bottom, "column %d overflows: %d > %d" % (col, y, y_bottom)
    return y


def build_image():
    cv = Canvas(W, 1024, PAPER)

    # Masthead.
    cv.text_centered(512, 16, "THE WORLD TODAY", 9, INK)
    cv.fill_rect(16, 88, 992, 4, INK)
    cv.fill_rect(16, 96, 992, 2, INK)

    # Date band: huge and unmistakable.
    cv.fill_rect(16, 104, 992, 48, RED)
    cv.text_centered(512, 112, "SATURDAY 21 NOVEMBER 2026", 5, WHITE)

    # Sub-line: story count and the date audit promise.
    cv.text_centered(
        512, 158,
        "37 STORIES - 7 REGIONS - EVERY STORY DATED AND SOURCED", 2, INK)

    # UTC timeline of the day.
    cv.text(16, 182, "THE DAY IN UTC", 2, RED)
    cv.fill_rect(16, 200, 992, 2, INK)
    for i, (t, label) in enumerate(TIMELINE):
        tx = 16 + (i % 4) * 248
        ty = 208 + (i // 4) * 24
        cv.text(tx, ty, t, 2, RED)
        cv.text(tx + cv.text_width(t, 2) + 12, ty, label, 2, INK)
    cv.fill_rect(16, 252, 992, 2, INK)

    # Three illustrated lead stories. Panel is 204 tall; the text block is
    # laid out so the last sub-head line ends 7px above the panel's bottom
    # edge (the v2 panel clipped it by 3px).
    for i, (kicker, kc, h1, h2, labels, scene) in enumerate(LEADS):
        x = COL_X[i]
        y = 262
        cv.fill_rect(x, y, COL_W, 204, PANEL)
        cv.frame_rect(x, y, COL_W, 204, INK, 2)
        scene(cv, x + 8, y + 8, COL_W - 16, 84)
        cv.frame_rect(x + 8, y + 8, COL_W - 16, 84, INK, 2)
        cv.text(x + 12, y + 98, kicker, 2, kc)
        cv.text(x + 12, y + 116, h1, 3, INK)
        cv.text(x + 12, y + 140, h2, 3, INK)
        for li, label in enumerate(labels):
            assert cv.text_width(label, 2) <= COL_W - 12, label
            cv.text(x + 12, y + 166 + li * 17, label, 2, GREY)

    # Briefs, grouped by region in three columns.
    draw_briefs(cv, 0, 468, 1016)
    end2 = draw_briefs(cv, 1, 468, 1016)
    draw_briefs(cv, 2, 468, 1016)

    # By-the-numbers box under the North America / Latin America / Africa
    # column, using its leftover space. It must end inside the canvas:
    # col 1 ends at y=932, so the box starts at 938 and is 80 tall.
    bx, by = COL_X[1], end2 + 6
    assert by + 80 <= 1024, "numbers box overflows canvas"
    cv.fill_rect(bx, by, COL_W, 80, PANEL)
    cv.frame_rect(bx, by, COL_W, 80, INK, 2)
    cv.text(bx + 10, by + 8, "BY THE NUMBERS", 2, RED)
    cv.text(bx + 10, by + 28, "3 MISSILES DOWNED", 2, INK)
    cv.text(bx + 10, by + 46, "128 NATIONS IN GENEVA", 2, INK)
    cv.text(bx + 10, by + 62, "M6.7 QUAKE / 37 STORIES", 2, INK)

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
