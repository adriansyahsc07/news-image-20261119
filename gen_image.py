#!/usr/bin/env python3
"""Generate entry.png: a 1024x1024 infographic summarising the world news
of Thursday, 19 November 2026. Uses Pillow only; no network access."""

import os

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1024, 1024

NAVY = (10, 22, 40)
NAVY_LIGHT = (16, 34, 60)
GOLD = (245, 197, 66)
WHITE = (245, 247, 250)
MUTED = (176, 190, 208)
ACCENT = (84, 160, 255)
CARD = (21, 43, 74)
DIVIDER = (70, 95, 132)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")

STORIES = [
    (
        "TRUMP, XI & PUTIN MEET IN SHENZHEN",
        "First-ever three-way summit on APEC sidelines; talks on nuclear risks, Ukraine and trade.",
    ),
    (
        "GTA VI IS OUT — AFTER 13 YEARS",
        "Rockstar's blockbuster launches worldwide at local midnight; critics give it 99 on Metacritic.",
    ),
    (
        "TOP UN COURT: MYANMAR COMMITTED GENOCIDE",
        "ICJ rules in The Gambia's case over the 2017 crackdown on the Rohingya — a first against a state.",
    ),
    (
        "UKRAINE HITS CRIMEAN BRIDGE AGAIN",
        "Third strike on the bridge in a week; Putin vows a 'far more painful' response.",
    ),
    (
        "ANTHROPIC'S RECORD $81BN IPO DEBUTS",
        "Claude maker's shares start trading on Nasdaq as ANT, priced at $83 — the largest IPO ever.",
    ),
    (
        "CYCLONE AKVAN NEARS INDIA'S EAST COAST",
        "Storm due to cross the Andhra Pradesh–Odisha coast on Friday, winds gusting to 110 km/h.",
    ),
]

FOOTER = "Sources: AP, BBC, Reuters, UN News · Compiled 19 Nov 2026 · Built by an AI agent for make.fun"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start_size, max_width, min_size=16):
    """Largest font size (<= start_size) that keeps text on one line."""
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, min_size)


def main():
    img = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(img)

    # Subtle top band and a thin gold divider rule under the header,
    # inset from the edges with a faint hairline beneath it.
    draw.rectangle([0, 0, WIDTH, 8], fill=GOLD)
    draw.rectangle([40, 168, WIDTH - 40, 171], fill=GOLD)
    draw.rectangle([40, 178, WIDTH - 40, 179], fill=DIVIDER)

    # Header.
    title = "THE DAY IN ONE IMAGE"
    title_font = fit_font(draw, title, BOLD, 62, WIDTH - 80)
    tw = draw.textlength(title, font=title_font)
    draw.text(((WIDTH - tw) / 2, 36), title, font=title_font, fill=WHITE)

    date_text = "Thursday, 19 November 2026"
    date_font = font(REGULAR, 30)
    dw = draw.textlength(date_text, font=date_font)
    draw.text(((WIDTH - dw) / 2, 118), date_text, font=date_font, fill=GOLD)

    # Story blocks.
    top = 196
    block_h = 118
    gap = 12
    margin = 40
    card_w = WIDTH - 2 * margin

    for i, (headline, subhead) in enumerate(STORIES):
        y = top + i * (block_h + gap)
        draw.rounded_rectangle(
            [margin, y, margin + card_w, y + block_h], radius=14, fill=CARD
        )
        # Subtle separator line in the gap before the next story block.
        if i < len(STORIES) - 1:
            sep_y = y + block_h + gap // 2
            draw.line(
                [margin + 24, sep_y, WIDTH - margin - 24, sep_y],
                fill=DIVIDER,
                width=1,
            )
        # Number badge.
        cx, cy, r = margin + 46, y + block_h // 2, 30
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
        num = str(i + 1)
        num_font = font(BOLD, 30)
        nw = draw.textlength(num, font=num_font)
        nh = num_font.getbbox(num)[3]
        draw.text((cx - nw / 2, cy - nh / 2 - 2), num, font=num_font, fill=NAVY)

        text_x = margin + 96
        text_w = WIDTH - margin - 24 - text_x

        head_font = fit_font(draw, headline, BOLD, 30, text_w)
        draw.text((text_x, y + 22), headline, font=head_font, fill=WHITE)

        sub_font = fit_font(draw, subhead, REGULAR, 22, text_w)
        draw.text((text_x, y + 66), subhead, font=sub_font, fill=MUTED)

    # Footer.
    footer_font = fit_font(draw, FOOTER, REGULAR, 19, WIDTH - 60)
    fw = draw.textlength(FOOTER, font=footer_font)
    draw.text(((WIDTH - fw) / 2, HEIGHT - 52), FOOTER, font=footer_font, fill=MUTED)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out_path, format="PNG", optimize=True)
    print(f"Wrote {out_path} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
