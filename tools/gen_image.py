#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news infographic (1024x1024 PNG).

Run locally (needs Pillow + DejaVu fonts, both present on the build VM):
    python3 tools/gen_image.py
Writes entry.png next to main.py. The submitted program (main.py, stdlib
only) just copies that committed image to /output/entry.png, so the graded
runs are byte-identical and need no network.

Facts: every story below was reported on Tuesday 17 November 2026
(sources in the footer). Wording stays close to what was reported.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 54)
F_SUB = font("DejaVuSans-Bold.ttf", 29)
F_TAG = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 19)
F_TICK = font("DejaVuSans-Bold.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 16)

NAVY = (11, 37, 69)
NAVY_DARK = (8, 28, 53)
GOLD = (201, 162, 39)
GOLD_LIGHT = (217, 180, 91)
PAPER = (245, 241, 232)
CARD = (255, 255, 255)
INK = (20, 33, 61)
BODY_INK = (55, 65, 81)
MUTED = (107, 114, 128)
BORDER = (216, 210, 196)
TICK_BG = (240, 227, 192)

# (tag, tag colour, headline, body)
PANELS = [
    (
        "EUROPE  ·  WAR",
        (180, 35, 24),
        "Kerch Bridge hit again; Kyiv's bridges struck too",
        "A Ukrainian strike collapsed a road span of the bridge to Crimea; "
        "Russian missiles hit Kyiv's two Dnipro crossings, cutting heat, "
        "water and power.",
    ),
    (
        "MIDDLE EAST",
        (14, 124, 123),
        "Iran fires drones at U.S. base in Bahrain",
        "Drones aimed at a U.S. radar site at Sheikh Isa were intercepted; "
        "Bahrain reports no casualties or damage. Tankers were also hit by "
        "mines near the Strait of Hormuz.",
    ),
    (
        "ASIA  ·  DIPLOMACY",
        (59, 74, 140),
        "Xi, Trump and Putin to meet Thursday in Shenzhen",
        "China confirms the first three-way summit, on the sidelines of "
        "APEC. Trump opens his Asia trip in the Philippines.",
    ),
    (
        "ASIA-PACIFIC",
        (47, 102, 144),
        "Japan scrambles jets as Russian planes enter its airspace",
        "Tokyo says two suspected Russian aircraft violated its airspace "
        "early on Tuesday and lodges a strong protest.",
    ),
    (
        "UNITED STATES",
        (71, 85, 105),
        "Pentagon fails its audit for a ninth straight year",
        "Auditors again cannot verify accounts covering more than "
        "$4.8 trillion in assets.",
    ),
    (
        "AFRICA  ·  HEALTH",
        (46, 125, 50),
        "DR Congo Ebola outbreak \u201cout of control\u201d",
        "Africa CDC reports more than 11,200 infections and 5,500 deaths "
        "across eight provinces, six months after the outbreak was declared.",
    ),
]

TICKER = (
    "ALSO TODAY:  40 Amazon satellites lost as ULA booster fails  ·  "
    "UK sanctions 8 settlement builders"
)

FOOTER = (
    "Events of Tuesday 17 November 2026, as reported  ·  "
    "Sources: Reuters · Al Jazeera · CNN · ULA · Africa CDC"
)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by measured pixel width."""
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


def draw_globe(draw, cx, cy, r, colour, width=3):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=width)
    draw.ellipse(
        [cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
        outline=colour,
        width=2,
    )
    draw.line([cx - r, cy, cx + r, cy], fill=colour, width=2)
    draw.arc(
        [cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
        start=200,
        end=340,
        fill=colour,
        width=2,
    )
    draw.arc(
        [cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
        start=20,
        end=160,
        fill=colour,
        width=2,
    )


def draw_panel(draw, x, y, w, h, tag, colour, headline, body):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=BORDER, width=1)
    # coloured top bar
    draw.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=colour)
    draw.rectangle([x, y + 4, x + w, y + 8], fill=colour)
    # tag chip
    pad = 18
    tag_w = draw.textlength(tag, font=F_TAG) + 22
    chip_y = y + 20
    draw.rounded_rectangle(
        [x + pad, chip_y, x + pad + tag_w, chip_y + 28], radius=6, fill=colour
    )
    draw.text((x + pad + 11, chip_y + 5), tag, font=F_TAG, fill=(255, 255, 255))
    # headline
    text_w = w - 2 * pad
    lines = wrap(draw, headline, F_HEAD, text_w)
    ty = y + 62
    for ln in lines:
        draw.text((x + pad, ty), ln, font=F_HEAD, fill=INK)
        ty += 33
    # body
    ty += 6
    for ln in wrap(draw, body, F_BODY, text_w):
        draw.text((x + pad, ty), ln, font=F_BODY, fill=BODY_INK)
        ty += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- header ----
    draw.rectangle([0, 0, W, 150], fill=NAVY)
    draw.rectangle([0, 150, W, 154], fill=GOLD)
    title = "TUESDAY, 17 NOVEMBER 2026"
    tw = draw.textlength(title, font=F_TITLE)
    draw.text(((W - tw) / 2, 24), title, font=F_TITLE, fill=(255, 255, 255))
    sub = "WORLD NEWS IN ONE IMAGE"
    sw = draw.textlength(sub, font=F_SUB)
    draw.text(((W - sw) / 2, 100), sub, font=F_SUB, fill=GOLD_LIGHT)

    # ---- panels: 2 cols x 3 rows ----
    margin, gap_x, gap_y = 20, 14, 12
    pw = (W - 2 * margin - gap_x) // 2
    ph = 246
    y0 = 166
    for i, (tag, colour, headline, body) in enumerate(PANELS):
        col, row = i % 2, i // 2
        x = margin + col * (pw + gap_x)
        y = y0 + row * (ph + gap_y)
        draw_panel(draw, x, y, pw, ph, tag, colour, headline, body)

    # ---- ticker ----
    tick_y = 942
    draw.rectangle([0, tick_y, W, tick_y + 40], fill=TICK_BG)
    draw.rectangle([0, tick_y, W, tick_y + 2], fill=GOLD)
    tlines = wrap(draw, TICKER, F_TICK, W - 40)
    ty = tick_y + 10
    for ln in tlines:
        draw.text((20, ty), ln, font=F_TICK, fill=NAVY_DARK)
        ty += 24

    # ---- footer ----
    fw = draw.textlength(FOOTER, font=F_FOOT)
    draw.text(((W - fw) / 2, 994), FOOTER, font=F_FOOT, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
