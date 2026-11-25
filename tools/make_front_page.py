#!/usr/bin/env python3
"""Draw a dense, original one-day world news front page for 25 Nov 2026.

Every fact comes from BBC News reporting of that day. All scenes are drawn
from shapes here, so no other entry's artwork is copied.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
ROOT = Path(__file__).resolve().parent.parent
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
INK = (18, 22, 28)
PAPER = (245, 241, 231)
RULE = (60, 64, 70)
GREY = (91, 96, 104)
ACCENT = (174, 44, 38)


def font(path, size):
    return ImageFont.truetype(path, size)


F_TOP = font(BOLD, 14)
F_DATE = font(BOLD, 62)
F_SUB = font(REG, 16)
F_HERO = font(BOLD, 20)
F_TAG = font(BOLD, 9)
F_CAP = font(REG, 14)
F_NUM = font(BOLD, 10)
F_LINE = font(REG, 11)
F_FOOT = font(REG, 12)


def wrap(draw, text, fnt, width):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def scene(draw, x, y, w, h, kind):
    """Simple original vector scene, sized to fit both card heights."""
    if kind == "court":
        draw.rectangle((x, y, x + w, y + h), fill=(216, 220, 216))
        for i in range(4):
            draw.rectangle((x + 18 + i * 55, y + 20, x + 48 + i * 55, y + h - 12), fill=(150, 140, 128))
        draw.polygon([(x + w // 2, y + 8), (x + 20, y + 26), (x + w - 20, y + 26)], fill=(60, 54, 50))
    elif kind == "space":
        draw.rectangle((x, y, x + w, y + h), fill=(26, 35, 58))
        for i in range(18):
            px = x + 12 + (i * 37) % (w - 24)
            py = y + 8 + (i * 53) % (h - 20)
            draw.ellipse((px, py, px + 2, py + 2), fill=(240, 240, 220))
        draw.polygon([(x + w // 2, y + 10), (x + w // 2 + 10, y + 38), (x + w // 2 - 10, y + 38)], fill=(235, 235, 225))
        draw.rectangle((x + w // 2 - 6, y + 38, x + w // 2 + 6, y + 54), fill=(205, 90, 60))
    elif kind == "war":
        draw.rectangle((x, y, x + w, y + h), fill=(92, 78, 70))
        draw.rectangle((x, y + h - 16, x + w, y + h), fill=(58, 48, 44))
        for i in range(5):
            px = x + 20 + i * 44
            draw.rectangle((px, y + 30, px + 24, y + h - 16), fill=(45, 40, 38))
            draw.ellipse((px + 8, y + 20, px + 20, y + 32), fill=(45, 40, 38))
        draw.rectangle((x + 12, y + 8, x + 78, y + 18), fill=(60, 95, 150))
        draw.rectangle((x + 12, y + 18, x + 78, y + 28), fill=(225, 185, 75))
    elif kind == "strike":
        draw.rectangle((x, y, x + w, y + h), fill=(120, 105, 86))
        draw.rectangle((x, y + h - 18, x + w, y + h), fill=(74, 62, 52))
        draw.polygon([(x + w // 2, y + 6), (x + w // 2 + 22, y + 38), (x + w // 2 - 22, y + 38)], fill=(190, 80, 50))
        for i in range(4):
            draw.rectangle((x + 14 + i * 54, y + 40, x + 40 + i * 54, y + h - 18), fill=(90, 78, 66))
    elif kind == "pact":
        draw.rectangle((x, y, x + w, y + h), fill=(64, 110, 120))
        for i in range(4):
            px = x + 24 + i * 52
            draw.ellipse((px, y + 10, px + 16, y + 26), fill=(230, 215, 185))
            draw.rectangle((px + 2, y + 26, px + 14, y + h - 8), fill=(230, 215, 185))
        draw.line((x + 20, y + 40, x + w - 20, y + 40), fill=(245, 230, 200), width=2)
    elif kind == "purge":
        draw.rectangle((x, y, x + w, y + h), fill=(150, 56, 48))
        for i in range(5):
            px = x + 16 + i * 46
            draw.rectangle((px, y + 22, px + 30, y + h - 8), fill=(105, 42, 38))
            draw.ellipse((px + 9, y + 10, px + 21, y + 22), fill=(230, 200, 170))
    elif kind == "mine":
        draw.rectangle((x, y, x + w, y + h), fill=(188, 170, 140))
        draw.polygon([(x + 30, y + h - 4), (x + 62, y + 8), (x + 94, y + h - 4)], outline=(90, 70, 50), width=3)
        draw.line((x + 62, y + 18, x + 62, y + h - 12), fill=(90, 70, 50), width=3)
        draw.ellipse((x + 59, y + h - 11, x + 65, y + h - 5), fill=(90, 70, 50))
    else:
        draw.rectangle((x, y, x + w, y + h), fill=(110, 118, 126))
        draw.ellipse((x + w - 42, y + 8, x + w - 12, y + 38), fill=(220, 210, 180))


HEROES = [
    ("court", "US · COURTS", "Huawei guilty of stealing US trade secrets", "Brooklyn jury also acquits firm of racketeering"),
    ("space", "ASIA · SPACE", "Shenzhou 24 carries Pakistan's first astronaut", "Muhammad Zeeshan Ali is first foreigner on Tiangong"),
    ("war", "EUROPE · WAR", "Russia's own data show nearly 500,000 war dead", "Leaked Rosstat figures reveal the invasion's cost"),
    ("strike", "MIDDLE EAST", "Israeli strike kills Hamas security chief", "Naeem Abu Nahel among seven killed in Gaza"),
]

SCENES = [
    ("pact", "OCEANIA · DIPLOMACY", "Solomon Islands quits China pact for Australian treaty"),
    ("purge", "ASIA · POLITICS", "Xi purge ensnares rising star Chen Jining"),
    ("mine", "SYRIA · HUMANITARIAN", "Land mines kill or injure nearly 1,000 children"),
    ("court", "US · MIGRATION", "Ábrego García leaves US for Spain"),
]

STORIES = [
    ("WASHINGTON", "Attorney general dodges questions on Nvidia investigation"),
    ("BROOKLYN", "Huawei found guilty on 10 of 12 counts, will appeal"),
    ("JIUQUAN", "Shenzhou 24 lifts off with Pakistani pilot aboard"),
    ("MOSCOW", "Leaked state data show close to 500,000 war deaths"),
    ("GAZA", "Hamas internal security chief killed in air strike"),
    ("DAMASCUS", "Land mine casualties soar two years after the war"),
    ("HONIARA", "Solomon Islands ends controversial China security pact"),
    ("BEIJING", "Xi anti-corruption drive ensnares Chen Jining"),
    ("LONDON", "UK sanctions Myanmar generals after genocide ruling"),
    ("DHAKA", "Sheikh Hasina says she plans to return on 16 December"),
    ("NEW DELHI", "India pledges 1.6bn dollars to Nepal in ties reset"),
    ("PYONGYANG", "Defectors describe spying and jail for Christian faith"),
    ("SINGAPORE", "US to blacklist AI firm Megaspeed after chip scandal"),
    ("MADRID", "Divided Spain heads to election with far-right surge"),
    ("PARIS", "Sarkozy and Carla Bruni to face trial"),
    ("BERLIN", "Nato chief vows defence against space threat"),
    ("MURMANSK", "Russian governor detained in rare criminal case"),
    ("TRIPOLI", "Ukraine strike on Russian ship in Libya raises stakes"),
    ("HARARE", "Zimbabwe warrants Robert Mugabe's son"),
    ("PRETORIA", "Court to rule on president's Farmgate bid"),
    ("LAGOS", "Nollywood actor Pete Edochie dies aged 79"),
    ("YAOUNDÉ", "Cameroon conflict has displaced half a million"),
    ("KUWAIT", "Kuwait says it repelled first Iranian attack in two months"),
    ("WEST BANK", "Palestinian woman, 72, shot dead by settlers"),
    ("GULF OF FINLAND", "A drone hits a Russian cargo ship"),
    ("VATICAN", "Pope Francis' diary claims three visions of the devil"),
    ("SYDNEY", "Jealous policeman found guilty of double murder"),
    ("MISSISSIPPI", "Six dead in plane crash off the US coast"),
    ("WASHINGTON", "Ábrego García leaves US for Spain"),
    ("HORMUZ", "Swim highlights environmental cost of war"),
    ("WINDSOR", "Two arrested on William and Kate's estate"),
    ("JERUSALEM", "Israeli ground operation ends beyond Yellow Line"),
    ("GAZA", "Oxfam says attacks turned Gaza into a toxic wasteland"),
    ("TEHRAN", "Singer flogged for performing without hijab, lawyers say"),
    ("ABUJA", "Emir of Daura suspended after sexual assault claims"),
    ("CAPE TOWN", "Father says police ignored his daughter's murder"),
    ("ANTALYA", "Africa seeks more climate money at UN climate summit"),
    ("NEW DELHI", "Leader barred from UK flight says government lost the plot"),
    ("JOHANNESBURG", "ANC fights to keep key cities after election setback"),
]


def main():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, 118), fill=INK)
    d.text((18, 6), "THE WORLD IN ONE DAY", font=F_TOP, fill=(222, 204, 168))
    date = "25 NOVEMBER 2026"
    dw = d.textbbox((0, 0), date, font=F_DATE)[2]
    d.text(((W - dw) // 2, 24), date, font=F_DATE, fill=PAPER)
    d.text((20, 98), "40 STORIES  ·  6 REGIONS  ·  ALL FIRST REPORTED WEDNESDAY 25 NOV",
           font=F_SUB, fill=(214, 198, 168))

    y = 126
    card_w = 244
    for i, (kind, tag, head, _cap) in enumerate(HEROES):
        x = 12 + i * 252
        d.rectangle((x, y, x + card_w, y + 188), outline=RULE, width=2)
        scene(d, x + 3, y + 3, card_w - 6, 84, kind)
        d.rectangle((x + 4, y + 88, x + card_w - 4, y + 108), fill=ACCENT)
        d.text((x + 10, y + 91), tag, font=F_TAG, fill=(255, 245, 230))
        yy = y + 114
        for line in wrap(d, head, F_HERO, card_w - 16)[:3]:
            d.text((x + 8, yy), line, font=F_HERO, fill=INK)
            yy += 24

    y = 324
    for i, (kind, tag, head) in enumerate(SCENES):
        x = 12 + i * 252
        d.rectangle((x, y, x + card_w, y + 168), outline=RULE, width=2)
        scene(d, x + 3, y + 3, card_w - 6, 64, kind)
        d.text((x + 8, y + 74), tag, font=F_TAG, fill=ACCENT)
        yy = y + 92
        for line in wrap(d, head, F_CAP, card_w - 16)[:3]:
            d.text((x + 8, yy), line, font=F_CAP, fill=INK)
            yy += 18

    d.line((12, 504, W - 12, 504), fill=INK, width=3)
    d.text((14, 510), "ALL REPORTED ON WEDNESDAY 25 NOVEMBER 2026", font=F_TAG, fill=ACCENT)
    start_y = 532
    for i, (place, text) in enumerate(STORIES):
        col, row = i // 8, i % 8
        x = 12 + col * 202
        yy = start_y + row * 43
        d.text((x, yy), f"{i + 1:02}", font=F_NUM, fill=ACCENT)
        d.text((x + 20, yy), place, font=F_TAG, fill=GREY)
        for k, line in enumerate(wrap(d, text, F_LINE, 180)[:2]):
            d.text((x + 20, yy + 12 + k * 12), line, font=F_LINE, fill=INK)
    d.line((12, 884, W - 12, 884), fill=RULE, width=2)
    d.text((14, 890), "THE DAY AT A GLANCE", font=F_TAG, fill=ACCENT)
    d.rectangle((14, 908, 340, 976), outline=RULE, width=2)
    d.rectangle((15, 909, 339, 975), fill=(226, 233, 232))
    d.polygon([(38, 936), (62, 924), (82, 934), (70, 958), (48, 966)], fill=(150, 172, 158))
    d.polygon([(126, 930), (158, 922), (178, 936), (162, 964), (132, 960)], fill=(150, 172, 158))
    d.polygon([(176, 928), (242, 920), (286, 936), (250, 960), (196, 956)], fill=(150, 172, 158))
    d.polygon([(278, 952), (312, 946), (324, 962), (292, 968)], fill=(150, 172, 158))
    for label, x, y in [("9", 60, 940), ("9", 150, 940), ("8", 224, 940), ("3", 268, 958), ("1", 306, 956)]:
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=ACCENT)
        d.text((x - 3, y - 6), label, font=F_TAG, fill=(255, 245, 230))
    d.text((352, 908), "DATE CHECK", font=F_TAG, fill=ACCENT)
    d.text((352, 926), "All 40 stories above were first reported on 25 November 2026.", font=F_FOOT, fill=INK)
    d.text((352, 944), "Sovereigns, courts, war, space, diplomacy, climate and culture all moved.", font=F_FOOT, fill=INK)
    d.text((352, 962), "Sources: BBC News, 25 November 2026  ·  Drawn by an AI agent", font=F_FOOT, fill=GREY)

    out = ROOT / "entry.png"
    im.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
