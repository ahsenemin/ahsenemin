"""
Step 4 - Neofetch-style info card SVG.

Reads content from config.py (INFO_CARD, GITHUB_USERNAME). Each line fades
and slides in on a short stagger. Set STATIC=1 in the environment to emit a
frozen frame (handy for local previews where you don't want animation).

Usage:
    python scripts/make_info_card.py
    STATIC=1 python scripts/make_info_card.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GITHUB_USERNAME, INFO_CARD, INFO_CARD_SVG

WIDTH = 490
PAD_X = 20
LINE_H = 25
HIGHLIGHT_LINE_H = 20
FONT = "monospace"
BG = "#0d1117"
BORDER = "#30363d"
TITLE_FG = "#7d8590"
KEY_FG = "#58a6ff"
VAL_FG = "#c9d1d9"

STATIC = os.environ.get("STATIC") == "1"
STEP = 0.12
FADE_DUR = 0.35


def esc(s: str) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fade_in_line(x, y, text, delay, size=13, color=VAL_FG, indent_extra=0):
    """One <text> element that fades + slides in, or is static if STATIC=1."""
    opacity = "1" if STATIC else "0"
    anim = ""
    if not STATIC:
        anim = (
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{delay:.2f}s" dur="{FADE_DUR}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="-10,0" to="0,0" begin="{delay:.2f}s" dur="{FADE_DUR}s" '
            f'fill="freeze"/>'
        )
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'fill="{color}" opacity="{opacity}">{esc(text)}{anim}</text>'
    )


def build():
    lines_svg = []
    y = 46
    delay = 0.1

    lines_svg.append(fade_in_line(PAD_X, y, "now:", delay, color=KEY_FG))
    lines_svg.append(fade_in_line(PAD_X + 85, y, INFO_CARD["now"], delay))
    y += LINE_H
    delay += STEP

    lines_svg.append(fade_in_line(PAD_X, y, "prev:", delay, color=KEY_FG))
    lines_svg.append(fade_in_line(PAD_X + 85, y, INFO_CARD["prev"], delay))
    y += LINE_H
    delay += STEP

    lines_svg.append(fade_in_line(PAD_X, y, "stack:", delay, color=KEY_FG))
    lines_svg.append(fade_in_line(PAD_X + 85, y, ", ".join(INFO_CARD["stack"]), delay))
    y += LINE_H
    delay += STEP

    lines_svg.append(fade_in_line(PAD_X, y, "highlights:", delay, color=KEY_FG))
    y += LINE_H
    delay += STEP * 0.8

    for h in INFO_CARD["highlights"]:
        lines_svg.append(fade_in_line(PAD_X + 16, y, f"- {h}", delay, size=12.5))
        y += HIGHLIGHT_LINE_H
        delay += STEP * 0.6

    height = y + 20

    svg = [
        f'<svg viewBox="0 0 {WIDTH} {height}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="8" '
        f'fill="{BG}" stroke="{BORDER}"/>',
        '<circle cx="20" cy="20" r="6" fill="#ff5f56"/>',
        '<circle cx="40" cy="20" r="6" fill="#ffbd2e"/>',
        '<circle cx="60" cy="20" r="6" fill="#27c93f"/>',
        f'<text x="{WIDTH / 2}" y="24" text-anchor="middle" font-family="{FONT}" '
        f'font-size="12" fill="{TITLE_FG}">{esc(GITHUB_USERNAME)}@github: neofetch</text>',
        f'<line x1="0" y1="34" x2="{WIDTH}" y2="34" stroke="{BORDER}"/>',
    ]
    svg.extend(lines_svg)
    svg.append("</svg>")

    with open(INFO_CARD_SVG, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Wrote {INFO_CARD_SVG}")


if __name__ == "__main__":
    build()
