#!/usr/bin/env python3
"""Render entry.png — front-page newspaper, WORLD NEWS, Wednesday 25 Nov 2026.
Deterministic PIL render. All facts/text taken ONLY from research.md.
Palette: paper / ink / red (3 main colours). Fonts: Anton (display) +
Montserrat Bold (tags/body) — 2 families, per Headline Studio V3.
Hero photo: AI-generated courthouse exterior (no people, no text),
cropped/resized to 300x210 as hero.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (166, 30, 30)
GREY = (96, 92, 84)

ANTON = "/home/hatch/.fonts/Anton-Regular.ttf"
MONTS = "/home/hatch/.fonts/Montserrat-Bold.ttf"

M = 44  # margin

def font(path, size):
    return ImageFont.truetype(path, size)

def tracked_width(draw, text, fnt, tracking):
    w = 0
    for ch in text:
        w += draw.textlength(ch, font=fnt) + tracking
    return w - tracking

def draw_tracked(draw, x, y, text, fnt, fill, tracking=2):
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking

def draw_tracked_center(draw, cx, y, text, fnt, fill, tracking=2):
    w = tracked_width(draw, text, fnt, tracking)
    draw_tracked(draw, cx - w / 2, y, text, fnt, fill, tracking)

def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

# ---------------- pictograms (simple PIL line art, ink + red accent) -------
def icon_ship(d, x, y, s, ink, red):
    d.polygon([(x + 2, y + s * 0.55), (x + s - 2, y + s * 0.55),
               (x + s * 0.82, y + s * 0.78), (x + s * 0.18, y + s * 0.78)],
              outline=ink, width=4)
    d.line([x + s * 0.5, y + s * 0.08, x + s * 0.5, y + s * 0.55], fill=ink, width=4)
    d.polygon([(x + s * 0.5, y + s * 0.08), (x + s * 0.78, y + s * 0.20),
               (x + s * 0.5, y + s * 0.30)], fill=red)
    d.arc([x, y + s * 0.82, x + s * 0.45, y + s + 6], 180, 360, fill=ink, width=3)
    d.arc([x + s * 0.55, y + s * 0.82, x + s, y + s + 6], 180, 360, fill=ink, width=3)

def icon_building(d, x, y, s, ink, red):
    d.rectangle([x + s * 0.12, y + s * 0.18, x + s * 0.55, y + s * 0.95],
                outline=ink, width=4)
    d.rectangle([x + s * 0.60, y + s * 0.38, x + s * 0.88, y + s * 0.95],
                outline=ink, width=4)
    for wy in (0.32, 0.52, 0.72):
        d.line([x + s * 0.20, y + s * wy, x + s * 0.47, y + s * wy],
               fill=ink, width=2)
    d.line([(x + s * 0.34, y + s * 0.18), (x + s * 0.28, y + s * 0.40),
            (x + s * 0.38, y + s * 0.55), (x + s * 0.30, y + s * 0.75),
            (x + s * 0.36, y + s * 0.95)], fill=red, width=4, joint="curve")

def icon_chart(d, x, y, s, ink, red):
    d.line([x + s * 0.08, y + s * 0.08, x + s * 0.08, y + s * 0.92,
            x + s * 0.95, y + s * 0.92], fill=ink, width=4)
    pts = [(x + s * 0.14, y + s * 0.30), (x + s * 0.36, y + s * 0.42),
           (x + s * 0.52, y + s * 0.36), (x + s * 0.74, y + s * 0.62),
           (x + s * 0.90, y + s * 0.78)]
    d.line(pts, fill=red, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=red)

def icon_scroll(d, x, y, s, ink, red):
    # treaty document with seal
    d.rectangle([x + s * 0.18, y + s * 0.08, x + s * 0.82, y + s * 0.92],
                outline=ink, width=4)
    for wy in (0.28, 0.44, 0.60):
        d.line([x + s * 0.28, y + s * wy, x + s * 0.72, y + s * wy],
               fill=ink, width=3)
    d.ellipse([x + s * 0.58, y + s * 0.66, x + s * 0.86, y + s * 0.94],
              outline=red, width=4)
    d.ellipse([x + s * 0.66, y + s * 0.74, x + s * 0.78, y + s * 0.86],
              fill=red)

def icon_lock(d, x, y, s, ink, red):
    d.arc([x + s * 0.28, y + s * 0.06, x + s * 0.72, y + s * 0.55], 180, 360,
          fill=ink, width=5)
    d.rectangle([x + s * 0.16, y + s * 0.42, x + s * 0.84, y + s * 0.94],
                outline=ink, width=4)
    d.ellipse([x + s * 0.43, y + s * 0.58, x + s * 0.57, y + s * 0.72],
              fill=red)
    d.line([x + s * 0.5, y + s * 0.70, x + s * 0.5, y + s * 0.84],
           fill=red, width=4)

def icon_store(d, x, y, s, ink, red):
    # shop awning + door
    d.line([x + s * 0.06, y + s * 0.34, x + s * 0.94, y + s * 0.34],
           fill=ink, width=4)
    for i in range(5):
        x0 = x + s * (0.06 + i * 0.176)
        d.arc([x0, y + s * 0.34, x0 + s * 0.176, y + s * 0.52], 0, 180,
              fill=red if i % 2 == 0 else ink, width=3)
    d.rectangle([x + s * 0.10, y + s * 0.52, x + s * 0.90, y + s * 0.94],
                outline=ink, width=4)
    d.rectangle([x + s * 0.40, y + s * 0.62, x + s * 0.60, y + s * 0.94],
                outline=ink, width=3)
    d.line([x + s * 0.50, y + s * 0.62, x + s * 0.50, y + s * 0.94],
           fill=ink, width=2)

# ---------------- content (verbatim facts from research.md) ---------------
LEAD = dict(
    tag="TECHNOLOGY  ·  LAW  ·  BROOKLYN, NEW YORK",
    headline="US JURY CONVICTS HUAWEI ON 10 OF 12 COUNTS",
    summary="Bank fraud, wire fraud, sanctions violations, trade-secret theft — cleared on RICO and obstruction of justice",
)
ROWS = [
    dict(tag="PACIFIC  ·  CANBERRA",
         headline="AUSTRALIA, SOLOMON ISLANDS SIGN SECURITY PACT",
         summary="China pact to lapse in 2027; A$740m pledged over a decade",
         icon=icon_scroll),
    dict(tag="CYBERSECURITY  ·  WASHINGTON",
         headline="CIA AND ODNI HIT BY HACK",
         summary="Unclassified OSINT system hit; no classified data affected",
         icon=icon_lock),
    dict(tag="MIDDLE EAST  ·  TEHRAN",
         headline="IRAN ORDERS HORMUZ CLOSED 'DAY BY DAY'",
         summary="Tehran claims tankers hit by mines; US denies, lanes cleared",
         icon=icon_ship),
    dict(tag="UKRAINE WAR  ·  ZAPORIZHZHIA",
         headline="PUTIN VOWS 'INEVITABLE' RETALIATION",
         summary="Zaporizhzhia strike kills 2, injures about 40–48",
         icon=icon_building),
    dict(tag="COLOMBIA  ·  CARTAGENA",
         headline="GUNMEN HOLD DOZENS HOSTAGE IN SUPERMARKET",
         summary="About 30 held in Cartagena; 10 freed, about 20 still inside",
         icon=icon_store),
    dict(tag="MARKETS  ·  TECHNOLOGY",
         headline="NVIDIA GIVES BACK 5.86%; NASDAQ FALLS 1.48%",
         summary="Dow tops 50,000 for the first time, closing at 50,018.70",
         icon=icon_chart),
]

# ---------------- render ---------------------------------------------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

y = 30
# dateline
f_date = font(MONTS, 22)
draw_tracked_center(d, W // 2, y, "WEDNESDAY, 25 NOVEMBER 2026", f_date, RED, 4)
y += 34
d.line([M, y, W - M, y], fill=RED, width=3)
y += 12
# masthead
f_mast = font(ANTON, 112)
draw_tracked_center(d, W // 2, y, "WORLD NEWS", f_mast, INK, 6)
asc, desc = f_mast.getmetrics()
y += asc + desc + 12
d.line([M, y, W - M, y], fill=INK, width=4)
y += 6
d.line([M, y, W - M, y], fill=INK, width=1)
y += 14

# lead story (hero photo on the right)
HERO_W, HERO_H = 300, 210
hero = Image.open(os.path.join(HERE, "hero.png")).convert("RGB")
assert hero.size == (HERO_W, HERO_H), hero.size
f_tag = font(MONTS, 20)
f_lead = font(ANTON, 46)
f_sum = font(MONTS, 20)
lead_text_w = W - 2 * M - HERO_W - 24
lead_top = y
draw_tracked(d, M, y, LEAD["tag"], f_tag, RED, 2)
y += 30
lines = wrap(d, LEAD["headline"], f_lead, lead_text_w)
assert len(lines) <= 2, lines
ly = y
for ln in lines:
    d.text((M, ly), ln, font=f_lead, fill=INK)
    ly += 52
y = ly + 6
slines = wrap(d, LEAD["summary"], f_sum, lead_text_w)
assert len(slines) <= 2, slines
for ln in slines:
    d.text((M, y), ln, font=f_sum, fill=INK)
    y += 27
lead_bottom = y
hero_y = lead_top + (lead_bottom - lead_top - HERO_H) // 2
img.paste(hero, (W - M - HERO_W, hero_y))
d.rectangle([W - M - HERO_W, hero_y, W - M - 1, hero_y + HERO_H - 1],
            outline=INK, width=2)
y = max(lead_bottom, hero_y + HERO_H) + 10
d.line([M, y, W - M, y], fill=INK, width=2)
y += 12

# rows
f_rtag = font(MONTS, 17)
f_rhead = font(ANTON, 28)
f_rsum = font(MONTS, 19)
ROW_H = 77
ICON = 56
tx = M + ICON + 22
text_w = W - M - tx
for row in ROWS:
    ry = y
    row["icon"](d, M, ry + 6, ICON, INK, RED)
    draw_tracked(d, tx, ry, row["tag"], f_rtag, RED, 2)
    size = 28
    while size > 22 and d.textlength(row["headline"], font=font(ANTON, size)) > text_w:
        size -= 1
    d.text((tx, ry + 21), row["headline"], font=font(ANTON, size), fill=INK)
    d.text((tx, ry + 55), row["summary"], font=f_rsum, fill=INK)
    y = ry + ROW_H
    if row is not ROWS[-1]:
        d.line([M, y - 6, W - M, y - 6], fill=(200, 194, 182), width=1)
assert y <= H - 56, f"rows overflow: y={y}"

# footer
f_foot = font(MONTS, 15)
draw_tracked_center(d, W // 2, H - 34,
                    "SOURCES: REUTERS  ·  CNN  ·  AP  ·  DOJ  ·  THE TIMES",
                    f_foot, GREY, 2)
d.line([M, H - 52, W - M, H - 52], fill=INK, width=1)

out = os.path.join(HERE, "entry.png")
img.save(out)
print("saved", img.size, "rows_end_y=", y)
