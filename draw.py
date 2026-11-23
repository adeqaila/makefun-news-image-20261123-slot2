#!/usr/bin/env python3
"""Render news-image-20261123 slot 2: 'Monday's Own Front Page'.

Fresh code, written in this session for this bounty only. Deterministic:
no randomness, no timestamps, no network.
Run: python3 draw.py [v1|v2]  -> entry-v1.png / entry-v2.png (1024x1024).
"""
import math
import os
import sys
import hashlib
from PIL import Image, ImageDraw, ImageFont

VARIANT = sys.argv[1] if len(sys.argv) > 1 else "v1"
W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (18, 18, 18)
RED = (178, 34, 34)
DARKRED = (140, 28, 40)
NAVY = (22, 52, 84)
GREY = (92, 90, 82)
PALE = (234, 229, 215)
RULE = (42, 42, 42)
WHITE = (255, 255, 255)

SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SNB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, width, fill, leading=None, max_lines=None):
    leading = leading or int(f.size * 1.18)
    lines = wrap(d, text, f, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def shrink(d, text, f, width):
    cur = f
    while d.textlength(text, font=cur) > width and cur.size > 7:
        cur = ImageFont.truetype(cur.path, cur.size - 1)
    return cur


def chip(d, x, y, label, f, bg, fg=WHITE):
    tw = d.textlength(label, font=f)
    d.rectangle([x, y, x + tw + 12, y + f.size + 7], fill=bg)
    d.text((x + 6, y + 3), label, font=f, fill=fg)
    return tw + 12


# ------------------------------------------------------------------ art
def art_chart(d, x, y, w, h):
    """Falling market chart: axes, candlesticks, red down-line, big drop."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 34))
    d.line([x + 14, y + h - 18, x + w - 8, y + h - 18], fill=(90, 110, 130), width=2)
    d.line([x + 14, y + 10, x + 14, y + h - 18], fill=(90, 110, 130), width=2)
    # candlesticks descending left to right
    tops = [0.25, 0.35, 0.30, 0.45, 0.55, 0.50, 0.68, 0.78]
    bw = (w - 40) // len(tops)
    for i, t in enumerate(tops):
        cx = x + 22 + i * bw
        top = y + 12 + t * (h - 40)
        bot = top + 14
        col = (210, 60, 50) if i >= 3 else (90, 190, 120)
        d.rectangle([cx, top, cx + bw - 6, bot], fill=col)
        d.line([cx + (bw - 6) // 2, top - 6, cx + (bw - 6) // 2, bot + 6],
               fill=col, width=2)
    # bold red down trend line
    pts = [(x + 22, y + 16), (x + w * 0.4, y + h * 0.42),
           (x + w * 0.7, y + h * 0.55), (x + w - 12, y + h - 26)]
    d.line(pts, fill=(255, 70, 55), width=4)
    d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5],
              fill=(255, 70, 55))
    f = font(SNB, 20)
    d.text((x + w - 92, y + 6), "-5.1%", font=f, fill=(255, 90, 70))


def art_tanker(d, x, y, w, h):
    """Supertanker on fire at dusk near Hormuz."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 44, 66))
    d.ellipse([x + w - 66, y + 8, x + w - 22, y + 52], fill=(240, 224, 180))
    # sea
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(24, 96, 140))
    # tanker hull
    d.polygon([(x + 18, y + h - 52), (x + w - 18, y + h - 52),
               (x + w - 34, y + h - 26), (x + 34, y + h - 26)], fill=(24, 24, 28))
    d.rectangle([x + 40, y + h - 76, x + 66, y + h - 52], fill=(70, 70, 78))
    d.rectangle([x + w - 66, y + h - 70, x + w - 44, y + h - 52], fill=(70, 70, 78))
    # fire + smoke from midship
    for cx, s in [(x + w * 0.45, 15), (x + w * 0.58, 11)]:
        d.polygon([(cx - s, y + h - 52), (cx - s * 0.5, y + h - 52 - s * 1.6),
                   (cx, y + h - 52 - s), (cx + s * 0.55, y + h - 52 - s * 1.8),
                   (cx + s, y + h - 52)], fill=(255, 140, 30))
        d.polygon([(cx - s * 0.4, y + h - 52), (cx, y + h - 52 - s * 0.7),
                   (cx + s * 0.4, y + h - 52)], fill=(255, 210, 80))
    for dx, dy, r in [(-18, -34, 9), (0, -44, 11), (16, -30, 8)]:
        d.ellipse([x + w * 0.5 + dx - r, y + h - 52 + dy - r,
                   x + w * 0.5 + dx + r, y + h - 52 + dy + r], fill=(190, 190, 190))


def art_summit(d, x, y, w, h):
    """Climate summit hall: delegate desks, big clock, NO DEAL banner."""
    d.rectangle([x, y, x + w, y + h], fill=(22, 50, 74))
    for r in range(3):
        yy = y + h - 46 + r * 12
        d.rectangle([x + 16, yy, x + w - 16, yy + 5], fill=(122, 92, 62))
        for c in range(7):
            cx = x + 32 + c * 42
            d.ellipse([cx - 6, yy - 12, cx + 6, yy - 2], fill=(233, 211, 171))
    # wall clock
    d.ellipse([x + w - 62, y + 10, x + w - 14, y + 58], fill=(241, 239, 226))
    d.ellipse([x + w - 58, y + 14, x + w - 18, y + 54], fill=(22, 50, 74))
    d.line([x + w - 38, y + 34, x + w - 38, y + 20], fill=(241, 239, 226), width=2)
    d.line([x + w - 38, y + 34, x + w - 26, y + 38], fill=(241, 239, 226), width=2)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=RED)
    f = font(SNB, 12)
    t = "NO DEAL"
    d.text((x + (w - d.textlength(t, font=f)) / 2, y + h - 15), t, font=f, fill=WHITE)


def art_ship(d, x, y, w, h):
    """Warship listing, smoke and flame."""
    d.rectangle([x, y, x + w, y + h], fill=(14, 34, 51))
    d.ellipse([x + w - 70, y + 10, x + w - 30, y + 50], fill=(236, 231, 211))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(28, 80, 120))
    # listing hull
    d.polygon([(x + 26, y + h - 34), (x + w - 26, y + h - 44),
               (x + w - 40, y + h - 24), (x + 40, y + h - 24)], fill=(20, 20, 24))
    d.rectangle([x + 60, y + h - 58, x + 84, y + h - 36], fill=(62, 62, 68))
    for cx, s in [(x + 90, 10), (x + 130, 8)]:
        base = y + h - 28
        d.polygon([(cx - s, base), (cx - s * 0.5, base - s * 1.4),
                   (cx, base - s), (cx + s * 0.55, base - s * 1.5),
                   (cx + s, base)], fill=(255, 140, 30))
    # smoke stays inside the art box (never above its top edge)
    for cx, cy, r in [(x + 108, y + 12, 8), (x + 128, y + 18, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(185, 185, 185))


def art_rubble(d, x, y, w, h):
    """Collapsed apartment block, cracked facade, search light."""
    d.rectangle([x, y, x + w, y + h], fill=(52, 58, 72))
    d.rectangle([x + 34, y + 6, x + 104, y + h - 4], fill=(72, 72, 80))
    for i in range(3):
        for j in range(4):
            d.rectangle([x + 40 + i * 22, y + 10 + j * 10,
                         x + 48 + i * 22, y + 18 + j * 10], fill=(255, 220, 120))
    d.polygon([(x + 66, y + 6), (x + 78, y + h * 0.45), (x + 62, y + h * 0.7),
               (x + 76, y + h - 4)], fill=(20, 20, 24))
    d.polygon([(x + 104, y + h - 4), (x + 150, y + h - 4), (x + 128, y + 18)],
              fill=(96, 96, 104))
    d.ellipse([x + 150, y + 8, x + 172, y + 30], fill=(255, 220, 120))


def art_drones(d, x, y, w, h):
    """Night sky, drone silhouettes, interception bursts."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 26, 44))
    for sx in range(14):
        d.ellipse([x + 12 + sx * 13, y + 8 + (sx % 3) * 5,
                   x + 15 + sx * 13, y + 11 + (sx % 3) * 5], fill=(255, 255, 255))
    # drones: small crosses with rotor blur
    for cx, cy in [(x + 40, y + 22), (x + 90, y + 16), (x + 140, y + 26),
                   (x + 60, y + 38), (x + 120, y + 40)]:
        d.line([cx - 7, cy, cx + 7, cy], fill=(220, 220, 220), width=2)
        d.line([cx, cy - 7, cx, cy + 7], fill=(220, 220, 220), width=2)
    # interception bursts
    for cx, cy in [(x + 165, y + 20), (x + 30, y + 40)]:
        for k in range(6):
            a = k * math.pi / 3
            d.line([cx, cy, cx + 9 * math.cos(a), cy + 9 * math.sin(a)],
                   fill=(255, 200, 60), width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 220, 120))


def art_dome(d, x, y, w, h):
    """US Capitol dome with stars row and 258 badge."""
    d.rectangle([x, y, x + w, y + h], fill=(26, 47, 94))
    for sx in range(12):
        d.text((x + 14 + sx * 15, y + 8), "*", font=font(SNB, 12),
               fill=(255, 220, 120))
    cx = x + w / 2
    base = y + h - 6
    d.rectangle([cx - 82, base - 18, cx + 82, base], fill=(236, 231, 216))
    d.rectangle([cx - 24, base - 38, cx + 24, base - 16], fill=(236, 231, 216))
    d.pieslice([cx - 24, base - 62, cx + 24, base - 18], 180, 360,
               fill=(236, 231, 216))
    d.rectangle([cx - 3, base - 72, cx + 3, base - 60], fill=(236, 231, 216))
    d.ellipse([cx - 4, base - 78, cx + 4, base - 70], fill=(236, 231, 216))
    d.rectangle([x + 10, base - 30, x + 92, base - 8], fill=RED)
    d.text((x + 18, base - 28), "258", font=font(SNB, 15), fill=WHITE)


def art_fire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 48, 32))
    d.rectangle([x + 20, y + h - 18, x + w - 20, y + h], fill=(30, 30, 34))
    for cx, s in [(x + w * 0.38, 14), (x + w * 0.62, 10)]:
        d.polygon([(cx - s, y + h - 14), (cx - s * 0.5, y + h - 14 - s * 1.6),
                   (cx, y + h - 14 - s), (cx + s * 0.55, y + h - 14 - s * 1.8),
                   (cx + s, y + h - 14)], fill=(255, 140, 30))
        d.polygon([(cx - s * 0.4, y + h - 14), (cx, y + h - 14 - s * 0.7),
                   (cx + s * 0.4, y + h - 14)], fill=(255, 210, 80))
    d.ellipse([x + w * 0.5 - 8, y + 8, x + w * 0.5 + 8, y + 24], fill=(200, 200, 200))


def art_congress(d, x, y, w, h):
    """Congress steps + calendar page showing 11 DEC."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 64, 110))
    d.rectangle([x + 14, y + h - 12, x + w - 14, y + h - 6], fill=(200, 196, 180))
    d.rectangle([x + 58, y + 6, x + w - 58, y + h - 14], fill=(255, 255, 255))
    d.rectangle([x + 58, y + 6, x + w - 58, y + 14], fill=(236, 231, 216))
    d.text((x + 66, y + 16), "11 DEC", font=font(SNB, 11), fill=RED)


def art_bridge(d, x, y, w, h):
    """Bridge span, broken mid-section, sparks."""
    d.rectangle([x, y, x + w, y + h], fill=(60, 60, 70))
    d.rectangle([x + 12, y + h - 22, x + w // 2 - 14, y + h - 14], fill=(200, 196, 180))
    d.rectangle([x + w // 2 + 14, y + h - 22, x + w - 12, y + h - 14],
                fill=(200, 196, 180))
    d.polygon([(x + w // 2 - 14, y + h - 22), (x + w // 2 + 14, y + h - 22),
               (x + w // 2, y + h - 34)], fill=(120, 116, 104))
    for k in range(5):
        a = k * math.pi / 2.5
        d.line([x + w // 2, y + h - 34, x + w // 2 + 10 * math.cos(a),
                y + h - 34 + 10 * math.sin(a)], fill=(255, 200, 60), width=2)
    d.line([x + 30, y + 10, x + 30, y + h - 22], fill=(160, 156, 144), width=3)
    d.line([x + w - 30, y + 10, x + w - 30, y + h - 22], fill=(160, 156, 144), width=3)


def art_cap(d, x, y, w, h):
    """Graduation cap + AI chip."""
    d.rectangle([x, y, x + w, y + h], fill=(90, 40, 70))
    d.polygon([(x + 55, y + 12), (x + 135, y + 12), (x + 95, y + 32)],
              fill=(20, 20, 24))
    d.rectangle([x + 75, y + 32, x + 115, y + 38], fill=(20, 20, 24))
    d.text((x + 148, y + 16), "AI", font=font(SNB, 14), fill=(255, 220, 120))


def art_sun(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(110, 70, 20))
    d.ellipse([x + 78, y + 4, x + 112, y + 38], fill=(255, 180, 60))
    for k in range(8):
        a = k * math.pi / 4
        d.line([x + 95 + 20 * math.cos(a), y + 21 + 20 * math.sin(a),
                x + 95 + 26 * math.cos(a), y + 21 + 26 * math.sin(a)],
               fill=(255, 180, 60), width=2)
    d.rectangle([x + 20, y + 40, x + w - 20, y + 46], fill=(90, 60, 30))


def art_flag(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 64, 110))
    d.line([x + 40, y + 8, x + 40, y + h - 8], fill=INK, width=2)
    d.polygon([(x + 40, y + 8), (x + 100, y + h * 0.3), (x + 40, y + h * 0.5)],
              fill=(200, 40, 40))
    d.line([x + 110, y + 12, x + 110, y + h - 8], fill=INK, width=2)
    d.polygon([(x + 110, y + 12), (x + 160, y + h * 0.3), (x + 110, y + h * 0.5)],
              fill=(30, 80, 160))


def art_chequer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 30, 90))
    for i in range(4):
        for j in range(2):
            col = (20, 20, 20) if (i + j) % 2 == 0 else (245, 245, 245)
            d.rectangle([x + 60 + i * 18, y + 10 + j * 18,
                         x + 78 + i * 18, y + 28 + j * 18], fill=col)
    d.text((x + 140, y + 16), "F1", font=font(SNB, 14), fill=WHITE)


# ------------------------------------------------------------------ data
HEROES = [
    dict(tag="MARKETS ROUT", tagbg=RED, bg=(16, 22, 34),
         kick="1 WORLD · MARKETS", head="AI sell-off routs world markets",
         body=("Nikkei −5.06% on Monday, S&P −3.7%; Nasdaq −10% in a week, "
               "worst since 2020. Gold +3.1%. (CNBC)"),
         art="chart"),
    dict(tag="HORMUZ: ALL MEANS", tagbg=(20, 20, 24), bg=(18, 44, 66),
         kick="2 STRAIT OF HORMUZ · CONFLICT", head="Iran vows 'all means' against US blockade",
         body=("Two supertankers hit mines near Hormuz and burn; a Bahrain "
               "strike wounds two. Trump waits till 2027. (CBS)"),
         art="tanker"),
    dict(tag="COP31: NO DEAL", tagbg=RED, bg=(22, 50, 74),
         kick="3 ANTALYA · CLIMATE", head="COP31 collapses with no deal as talks run out of road",
         body=("The longest climate summit ends with no deal — first failure "
               "since Copenhagen 2009 — as the EU rejects a text naming no "
               "fossil fuels. (Reuters, AP)"),
         art="summit"),
]

PANELS = [
    dict(tag="ZELENSKYY CLAIMS IT", bg=(14, 34, 51), kick="4 BENGHAZI · WAR",
         head="Kyiv says it sank the Merkury",
         body="Seven sea drones; a second vessel also hit, 10 hurt. UN seeks inquiry. (BBC)",
         art="ship"),
    dict(tag="11 KILLED", bg=(52, 58, 72), kick="5 DYMER · UKRAINE",
         head="Dymer toll rises; boy, 7, pulled alive",
         body="Rescued after 14 hours in the rubble; 15 dead across the Kyiv region. (BBC)",
         art="rubble"),
    dict(tag="153 DRONES", bg=(18, 26, 44), kick="6 UKRAINE · WAR",
         head="153 drones in one night; 134 downed",
         body="Overnight barrage, 60 jet-powered; strikes land at 11 sites. (Air Force)",
         art="drones"),
    dict(tag="258 SEATS", bg=(26, 47, 94), kick="7 WASHINGTON · POLITICS",
         head="Democrats clinch 258 House seats",
         body="Largest majority since 1992; four races still undecided. (AP, BBC)",
         art="dome"),
    dict(tag="24 KILLED", bg=(96, 48, 32), kick="8 SERANG · DISASTER",
         head="Factory fire toll reaches 24",
         body="Candy plant blaze; dozens missing, DNA needed to name the dead. (Guardian)",
         art="fire"),
    dict(tag="11 DEC", bg=(24, 64, 110), kick="9 WASHINGTON · CONGRESS",
         head="Funding runs out 11 Dec; no bill passed",
         body="Congress leaves for Thanksgiving; not one FY2027 bill signed. (Reports)",
         art="congress"),
    dict(tag="BRIDGE HIT", bg=(60, 60, 70), kick="10 KERCH · WAR",
         head="Kerch Bridge crippled in strikes",
         body="Energy sites and three Kyiv bridges hit; nuclear output cut. (Reports)",
         art="bridge"),
    dict(tag="RESIGNS", bg=(90, 40, 70), kick="11 SEOUL · EDUCATION",
         head="Korea minister quits over AI cheating",
         body="Choi Kyo-jin goes after CSAT exam chaos; 111 cases suspected. (AP)",
         art="cap"),
    dict(tag="24 KILLED", bg=(110, 70, 20), kick="12 WARRAP · CONFLICT",
         head="Raid on cattle camp kills 24",
         body="SPLA-IO blamed; 7 children among the dead. (AFP)",
         art="sun"),
    dict(tag="35 LEAD CHANGES", bg=(140, 30, 90), kick="13 LAS VEGAS · SPORT",
         head="Verstappen wins wild Vegas GP",
         body="75th win; Ferraris collide again. (F1)",
         art="chequer"),
]

ALSO_V1 = [
    "14  Sparta II still on fire off Finland (Sun)",
    "15  Myanmar slams ASEAN ruling as 'unfair' (Sat)",
    "16  Saudi coalition intercepts Houthi missile (Sun)",
    "17  UKMTO: tanker incident in Gulf of Oman (Sun)",
    "18  Pakistan FM hopeful on US-Iran deal (Sun)",
    "19  WHO: fighting disrupts Congo Ebola response",
    "20  Malaysia to work with UN, OIC on Myanmar",
    "21  Australia rebukes US budget office on AUKUS",
    "22  Governor calls ICE 'out of control' in Seattle",
    "23  Eisenkot: settler attacks are 'Jewish terrorism'",
    "24  Delta glitch delays 400+ Atlanta flights (Sun)",
    "25  India post record 720/9d in Wellington Test",
    "26  Liverpool thrash 10-man Man Utd (Sun)",
    "27  'Sunrise on the Reaping': $120m opening (Sun)",
    "28  Miley Cyrus marries Maxx Morando (Sun)",
    "29  Ohio baby-shower shooting: 3 killed (Sun)",
    "30  Tom Jackson, ex-Broncos star, dies at 75",
    "31  India-EU trade pact likely signed 16 Dec",
    "32  Modi opens AI centre at IIT Patna (Mon)",
    "33  MP Ramrao Wadkute dies in Delhi (Sun)",
    "34  Nine killed in Kota pilgrim crash (Sun)",
    "35  Philippines leads farm talks, 23–26 Nov",
    "36  Nvidia chip row: new Alice Huang details",
]

# V2: same heroes + panels, shorter ALSO list, bigger type.
ALSO_V2 = ALSO_V1[:17]  # 14–30, total 3 + 10 + 17 = 30 stories

REGIONS = [("EUROPE 6", (29, 78, 137)), ("AMERICAS 9", (139, 46, 60)),
           ("ASIA 10", (180, 90, 27)), ("MIDDLE EAST 5", (107, 107, 30)),
           ("AFRICA 3", (30, 122, 76)), ("OCEANIA 1", (15, 122, 122)),
           ("WORLD 2", (85, 85, 85))]

ART = {"chart": art_chart, "tanker": art_tanker, "summit": art_summit,
       "ship": art_ship, "rubble": art_rubble, "drones": art_drones,
       "dome": art_dome, "fire": art_fire, "congress": art_congress,
       "bridge": art_bridge, "cap": art_cap, "sun": art_sun,
       "flag": art_flag, "chequer": art_chequer}


def render(variant):
    also = ALSO_V1 if variant == "v1" else ALSO_V2
    total = 3 + len(PANELS) + len(also)
    big = variant == "v2"  # bigger type, roomier layout
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 14
    CW = W - 2 * MX

    # ---- masthead
    f_top = font(SNB, 13)
    d.text((MX, 8), "THE WORLD IN ONE DAY", font=f_top, fill=RED)
    right = ("%d STORIES  ·  7 REGIONS  ·  EVERY ONE DATED MONDAY 23 NOVEMBER 2026"
             % total)
    f_topr = font(SNB, 11)
    d.text((W - MX - d.textlength(right, font=f_topr), 9), right, font=f_topr,
           fill=INK)
    d.line([MX, 26, W - MX, 26], fill=RULE, width=2)

    # ---- headline
    f_head = font(SB, 62)
    head = "Monday 23 November 2026"
    d.text(((W - d.textlength(head, font=f_head)) / 2, 30), head, font=f_head,
           fill=INK)
    f_sub = font(SR, 17)
    sub = ("Markets rout as AI sell-off spreads  ·  Iran vows 'all means' "
           "over Hormuz  ·  COP31 ends with no deal")
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 100), sub, font=f_sub,
           fill=INK)
    d.line([MX, 124, W - MX, 124], fill=RULE, width=3)

    # ---- stat strip
    stats = [
        ("-5.1%", "Nikkei on Monday"),
        ("-3.7%", "S&P 500"),
        ("+3.1%", "gold, as investors flee"),
        ("153", "drones in one night"),
        ("2", "tankers hit near Hormuz"),
        ("11", "killed in Dymer, Kyiv region"),
    ]
    f_num = font(SB, 30)
    f_lab = font(SN, 10)
    sx = MX
    sw = CW / 6
    for num, lab in stats:
        d.text((sx + 2, 130), num, font=f_num, fill=INK)
        para(d, sx + 2, 164, lab, f_lab, sw - 8, GREY, leading=12, max_lines=2)
        sx += sw
    d.line([MX, 190, W - MX, 190], fill=RULE, width=1)

    # ---- region bar
    f_reg = font(SNB, 11)
    rx = MX
    tot = sum(len(t) for t, _ in REGIONS)
    for label, col in REGIONS:
        seg = CW * len(label) / tot
        d.rectangle([rx, 196, rx + seg - 2, 216], fill=col)
        tw = d.textlength(label, font=f_reg)
        d.text((rx + (seg - 2 - tw) / 2, 201), label, font=f_reg, fill=WHITE)
        rx += seg

    # ---- heroes
    hy = 224
    hw = (CW - 2 * 12) / 3
    ah = 108
    for i, hh in enumerate(HEROES):
        x0 = MX + i * (hw + 12)
        ART[hh["art"]](d, x0, hy, hw, ah)
        chip(d, x0, hy, hh["tag"], font(SNB, 11), hh["tagbg"])
        d.text((x0, hy + ah + 8), hh["kick"], font=font(SNB, 11), fill=RED)
        y = para(d, x0, hy + ah + 24, hh["head"], font(SB, 19), hw, INK,
                 leading=21, max_lines=2)
        para(d, x0, y + 3, hh["body"], font(SN, 11), hw, INK, leading=13,
             max_lines=2)

    # ---- panels (5 x 2)
    py = 446
    pw = (CW - 4 * 8) / 5
    ph = 48
    prow_h = 118 if not big else 124
    for r in range(2):
        for c in range(5):
            p = PANELS[r * 5 + c]
            x0 = MX + c * (pw + 8)
            y0 = py + r * (prow_h + 8)
            ART[p["art"]](d, x0, y0, pw, ph)
            chip(d, x0, y0, p["tag"], font(SNB, 9), (20, 20, 24))
            d.text((x0, y0 + ph + 4), p["kick"], font=font(SNB, 9), fill=RED)
            f_ph = font(SB, 13 if big else 12)
            y = para(d, x0, y0 + ph + 15, p["head"], f_ph, pw, INK,
                     leading=15 if big else 14, max_lines=2)
            f_pb = font(SN, 10 if big else 9)
            para(d, x0, y + 1, p["body"], f_pb, pw, INK,
                 leading=12 if big else 11, max_lines=2)

    # ---- map + ALSO
    my = 702
    d.line([MX, my - 6, W - MX, my - 6], fill=RULE, width=2)
    f_sec = font(SNB, 12)
    d.text((MX, my), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((MX + 350, my),
           "ALSO ON MONDAY 23 NOVEMBER — %d MORE STORIES" % len(also),
           font=f_sec, fill=INK)

    mapx, mapy, mapw, maph = MX, my + 18, 330, 132
    d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(214, 228, 235))
    LAND = (222, 196, 140)
    OUTL = (170, 145, 95)

    def ll(lon, lat):
        return (mapx + (lon + 180) / 360 * mapw,
                mapy + (90 - lat) / 180 * maph)

    def poly(points):
        d.polygon([ll(lo, la) for lo, la in points], fill=LAND, outline=OUTL)

    poly([(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
          (-55, 47), (-70, 42), (-80, 32), (-85, 26), (-97, 26), (-105, 20),
          (-95, 16), (-83, 9), (-90, 14), (-105, 20), (-115, 28), (-125, 40),
          (-125, 49), (-140, 60), (-168, 66)])
    poly([(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
          (-58, -35), (-65, -40), (-70, -50), (-73, -40), (-70, -20),
          (-75, -15), (-80, -5), (-80, 10)])
    poly([(-10, 36), (-5, 44), (0, 46), (5, 55), (8, 58), (18, 60), (25, 70),
          (30, 70), (40, 68), (45, 60), (40, 50), (30, 45), (23, 40), (20, 36),
          (12, 44), (3, 43), (-2, 37), (-10, 36)])
    poly([(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
          (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20),
          (30, -30), (20, -35), (15, -27), (12, -18), (9, -1), (9, 4),
          (-8, 5), (-17, 15)])
    poly([(40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72),
          (160, 70), (178, 66), (170, 60), (160, 55), (150, 60), (142, 50),
          (140, 40), (130, 35), (127, 38), (122, 30), (115, 22), (108, 12),
          (105, 5), (100, 8), (95, 15), (90, 22), (80, 15), (75, 8), (70, 20),
          (60, 25), (55, 28), (48, 30), (43, 38), (40, 45), (40, 60), (40, 68)])
    poly([(113, -22), (114, -30), (120, -34), (130, -32), (140, -38),
          (150, -37), (153, -27), (146, -19), (142, -11), (135, -12),
          (130, -13), (122, -14), (114, -21), (113, -22)])

    # numbered dots: (lon, lat, story no, dx, dy) — offsets keep crowded
    # Europe / Middle East numbers from colliding, as News22 did.
    dots = [
        (139.7, 35.7, 1, 0, 0),   # Markets: Nikkei, Tokyo
        (56.5, 26.5, 2, 0, 0),    # Hormuz
        (30.7, 36.9, 3, 0, 0),    # COP31 Antalya
        (20.1, 32.1, 4, -12, 10),  # Merkury Benghazi (offset from COP31)
        (-77.0, 38.9, 7, 0, 0),   # Democrats Washington
        (30.2, 50.8, 5, -20, 10),  # Dymer (spread from Kerch/drones)
        (30.2, 50.8, 6, 20, 14),  # drones (same region, offset)
        (106.1, -6.1, 8, 0, 0),   # Serang
        (-77.0, 38.9, 9, 14, 10),  # Congress (same city, offset)
        (35.4, 45.3, 10, 20, -14),  # Kerch (spread from Dymer)
        (127.0, 37.5, 11, 0, 0),  # Seoul
        (28.5, 7.5, 12, 0, 0),    # Warrap
        (-115.1, 36.2, 13, 0, 0),  # Las Vegas
    ]
    f_dot = font(SNB, 8)
    for lo, la, n, dx, dy in dots:
        cx, cy = ll(lo, la)
        cx += dx
        cy += dy
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED, outline=WHITE)
        t = str(n)
        d.text((cx - d.textlength(t, font=f_dot) / 2, cy - 5), t, font=f_dot,
               fill=WHITE)
    d.text((mapx, mapy + maph + 4), "Red numbers mark stories 1–13 on the map.",
           font=font(SN, 9), fill=GREY)

    # ALSO list, two columns
    f_also = font(SN, 10)
    ax0 = MX + 350
    colw = (W - MX - ax0 - 8) / 2
    ay0 = my + 18
    half = (len(also) + 1) // 2
    for idx, item in enumerate(also):
        col = 0 if idx < half else 1
        row = idx if idx < half else idx - half
        x = ax0 + col * (colw + 8)
        y = ay0 + row * 15
        f = shrink(d, item, f_also, colw)
        d.text((x, y), item, font=f, fill=INK)

    # ---- by the clock
    cy = 904
    d.line([MX, cy, W - MX, cy], fill=RULE, width=1)
    d.text((MX, cy + 5), "BY THE CLOCK", font=font(SNB, 10), fill=RED)
    clock = ("Mon 00:02 UTC Australia rebukes CBO over AUKUS  ·  08:00 Air "
             "Force: 134 of 153 drones downed  ·  10:30 Kerch Bridge strikes "
             "reported  ·  Mon morning Nikkei closes −5.06%  ·  Mon midday "
             "Euro Stoxx +0.94%  ·  Mon Iran vows 'all means' on Hormuz  ·  "
             "Mon evening US futures point to a rebound")
    para(d, MX + 92, cy + 5, clock, font(SN, 10), W - MX - 92, INK,
         leading=13, max_lines=2)

    # ---- date check box
    dy = 936
    d.rectangle([MX, dy, W - MX, dy + 60], outline=RED, width=2)
    d.text((MX + 8, dy + 5), "DATE CHECK", font=font(SNB, 10), fill=RED)
    dc = ("Left out as other days' news: the Kyiv barrage (400 drones, 110 "
          "missiles) and missiles over Poland (Fri 20 Nov) · Wall Street's "
          "correction (Fri 20 Nov) · the Anthropic IPO debut and GTA VI launch "
          "(Thu 19 Nov) · the Peru quake (Fri 20 Nov local) · the APEC "
          "trilateral in Shenzhen (Thu 19 Nov) · the Iran strikes on the US "
          "base in Kuwait (Wed 18 Nov). Not yet happened, so not shown: any "
          "COP32 venue decision; the final Indonesia fire toll.")
    para(d, MX + 8, dy + 20, dc, font(SN, 10), W - 2 * MX - 16, INK,
         leading=13, max_lines=3)

    # ---- footer
    f_foot = font(SN, 9)
    d.text((MX, 1000),
           "Every story here happened, or was first reported, on Monday 23 "
           "November 2026. Officials' counts are attributed.",
           font=f_foot, fill=GREY)
    foot_r = "Sources named beside each story · original drawings"
    d.text((W - MX - d.textlength(foot_r, font=f_foot), 1000), foot_r,
           font=f_foot, fill=GREY)

    out = "entry-%s.png" % variant
    img.save(out, optimize=True)
    print("saved", out, hashlib.sha256(open(out, "rb").read()).hexdigest())
    print("bytes:", os.path.getsize(out), "| stories:", total)


if __name__ == "__main__":
    render(VARIANT)
