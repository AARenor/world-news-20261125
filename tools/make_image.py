#!/usr/bin/env python3
"""Draw the 25 November 2026 world news sheet as a 1024px PNG.

Run locally from this repository: python3 tools/make_image.py
The shipped entry.png is the output of this script, so the bytes are
reproducible and the artwork is original.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (10, 17, 31)
CARD = (19, 30, 48)
CARD_EDGE = (37, 55, 79)
WHITE = (242, 246, 252)
MUTED = (151, 169, 192)
GOLD = (240, 190, 92)
RED = (236, 104, 104)
BLUE = (104, 170, 246)
GREEN = (105, 207, 153)
PURPLE = (177, 139, 236)
ORANGE = (242, 153, 91)
CYAN = (103, 203, 212)
PINK = (231, 130, 175)

ROOT = Path(__file__).resolve().parent.parent
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path: str, size: int):
    return ImageFont.truetype(path, size)


F_DATE = font(BOLD, 48)
F_DATE2 = font(BOLD, 40)
F_SUB = font(REG, 20)
F_TAG = font(BOLD, 17)
F_HEAD = font(BOLD, 25)
F_BODY = font(REG, 17)
F_SMALL = font(REG, 17)
F_SOURCE = font(REG, 16)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def icon(draw, cx, cy, kind, color):
    """Small geometric glyph in a 48px circle."""
    r = 24
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(24, 39, 60), outline=color, width=2)
    if kind == "flag":
        draw.rectangle((cx - 13, cy - 9, cx + 13, cy - 1), fill=BLUE)
        draw.rectangle((cx - 13, cy, cx + 13, cy + 9), fill=GOLD)
    elif kind == "rocket":
        draw.polygon([(cx, cy - 15), (cx + 8, cy + 5), (cx - 8, cy + 5)], fill=WHITE)
        draw.rectangle((cx - 4, cy + 6, cx + 4, cy + 12), fill=color)
        draw.polygon([(cx - 8, cy + 3), (cx - 13, cy + 12), (cx - 6, cy + 10)], fill=color)
        draw.polygon([(cx + 8, cy + 3), (cx + 13, cy + 12), (cx + 6, cy + 10)], fill=color)
    elif kind == "chip":
        draw.rectangle((cx - 11, cy - 11, cx + 11, cy + 11), outline=WHITE, width=3)
        draw.rectangle((cx - 4, cy - 4, cx + 4, cy + 4), fill=color)
        for d in (-16, 16):
            draw.line((cx + d, cy - 6, cx + d, cy + 6), fill=WHITE, width=2)
            draw.line((cx - 6, cy + d, cx + 6, cy + d), fill=WHITE, width=2)
    elif kind == "scale":
        draw.line((cx, cy - 14, cx, cy + 13), fill=WHITE, width=3)
        draw.line((cx - 15, cy - 7, cx + 15, cy - 7), fill=WHITE, width=3)
        draw.ellipse((cx - 19, cy - 3, cx - 5, cy + 9), outline=color, width=2)
        draw.ellipse((cx + 5, cy - 3, cx + 19, cy + 9), outline=color, width=2)
    elif kind == "target":
        draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), outline=WHITE, width=3)
        draw.line((cx - 17, cy - 17, cx + 17, cy + 17), fill=color, width=3)
        draw.line((cx + 17, cy - 17, cx - 17, cy + 17), fill=color, width=3)
    elif kind == "mask":
        draw.rounded_rectangle((cx - 13, cy - 12, cx + 13, cy + 12), 7, outline=WHITE, width=3)
        draw.ellipse((cx - 8, cy - 7, cx - 2, cy - 1), fill=color)
        draw.ellipse((cx + 2, cy - 7, cx + 8, cy - 1), fill=color)
        draw.line((cx - 7, cy + 6, cx + 7, cy + 6), fill=WHITE, width=2)
    elif kind == "plane":
        draw.polygon([(cx - 16, cy + 2), (cx + 16, cy - 11), (cx + 8, cy + 14),
                      (cx + 1, cy + 5), (cx - 9, cy + 12), (cx - 8, cy + 3)], fill=WHITE)
        draw.line((cx - 4, cy + 1, cx + 12, cy - 7), fill=color, width=2)
    elif kind == "warning":
        draw.polygon([(cx, cy - 16), (cx + 16, cy + 13), (cx - 16, cy + 13)], outline=WHITE, width=3)
        draw.line((cx, cy - 5, cx, cy + 5), fill=color, width=3)
        draw.ellipse((cx - 2, cy + 8, cx + 2, cy + 12), fill=color)
    elif kind == "globe":
        draw.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), outline=WHITE, width=3)
        draw.ellipse((cx - 5, cy - 13, cx + 5, cy + 13), outline=color, width=2)
        draw.line((cx - 13, cy, cx + 13, cy), fill=color, width=2)


STORIES = [
    ("EUROPE · WAR", RED, "flag", "Russia data: 500,000 war deaths",
     "Leaked figures show the human cost of the invasion of Ukraine"),
    ("CHINA · SPACE", BLUE, "rocket", "Shenzhou 24 carries Pakistani astronaut",
     "Muhammad Zeeshan Ali becomes first foreigner aboard Tiangong"),
    ("US · TECHNOLOGY", GOLD, "chip", "Trump restores Nvidia CEO Huang",
     "Attorney general dodges questions; shares fall 7 percent"),
    ("US · JUSTICE", PURPLE, "scale", "Huawei guilty of stealing US secrets",
     "Acquitted of racketeering in a New York trial"),
    ("MIDDLE EAST", ORANGE, "target", "Israeli strike kills Hamas security chief",
     "Naeem Abu Nahel among seven killed in Gaza"),
    ("ASIA · CYBER", CYAN, "mask", "AI fakes target Taiwan election",
     "BBC Verify finds a network smearing DPP candidates"),
    ("US · MIGRATION", PINK, "plane", "Ábrego García leaves US for Spain",
     "Deportation battle ends after his transfer to El Salvador"),
    ("SYRIA · MINES", RED, "warning", "Land-mine casualties soar in Syria",
     "Nearly 1,000 children killed or injured by explosives"),
]


def card(draw, x, y, w, h, tag, color, glyph, headline, body):
    draw.rounded_rectangle((x, y, x + w, y + h), 12, fill=CARD, outline=CARD_EDGE, width=2)
    draw.rounded_rectangle((x, y, x + w, y + 6), 3, fill=color)
    draw.text((x + 20, y + 17), tag, font=F_TAG, fill=color)
    icon(draw, x + w - 45, y + 44, glyph, color)
    yy = y + 57
    for line in wrap(draw, headline, F_HEAD, w - 40)[:3]:
        draw.text((x + 20, yy), line, font=F_HEAD, fill=WHITE)
        yy += 32
    yy = y + 163
    for line in wrap(draw, body, F_BODY, w - 40)[:3]:
        draw.text((x + 20, yy), line, font=F_BODY, fill=MUTED)
        yy += 23


def main():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 64):
        d.line((x, 0, x, H), fill=(14, 23, 39), width=1)
    for y in range(0, H, 64):
        d.line((0, y, W, y), fill=(14, 23, 39), width=1)

    d.text((28, 22), "WORLD NEWS", font=F_DATE, fill=WHITE)
    date_w = d.textbbox((0, 0), "25 NOVEMBER 2026", font=F_DATE2)[2]
    d.text((W - 28 - date_w, 30), "25 NOVEMBER 2026", font=F_DATE2, fill=GOLD)
    d.line((28, 90, W - 28, 90), fill=GOLD, width=3)
    d.text((30, 106), "THE DAY IN EIGHT STORIES  ·  WEDNESDAY  ·  AS REPORTED ON 25 NOV 2026",
           font=F_SUB, fill=MUTED)

    xs = [24, 353, 682]
    ys = [156, 414, 672]
    for i, (tag, color, glyph, head, body) in enumerate(STORIES):
        col, row = i % 3, i // 3
        card(d, xs[col], ys[row], 318, 244, tag, color, glyph, head, body)

    x, y = xs[2], ys[2]
    d.rounded_rectangle((x, y, x + 318, y + 244), 12, fill=CARD, outline=CARD_EDGE, width=2)
    d.rounded_rectangle((x, y, x + 318, y + 6), 3, fill=WHITE)
    icon(d, x + 273, y + 44, "globe", CYAN)
    d.text((x + 20, y + 17), "ALSO TODAY", font=F_TAG, fill=CYAN)
    for j, line in enumerate([
        "Six dead in plane crash off Mississippi",
        "Zimbabwe warrants Mugabe's son",
        "Spain heads to a divided election",
    ]):
        yy = y + 62 + j * 56
        d.ellipse((x + 22, yy + 6, x + 32, yy + 16), fill=GOLD)
        for k, ln in enumerate(wrap(d, line, F_SMALL, 268)[:2]):
            d.text((x + 42, yy + k * 21), ln, font=F_SMALL, fill=WHITE)

    d.line((24, 936, W - 24, 936), fill=CARD_EDGE, width=2)
    d.text((26, 950), "Source: BBC News, 25 November 2026  ·  Original illustration by an AI agent",
           font=F_SOURCE, fill=MUTED)

    out = ROOT / "entry.png"
    im.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
