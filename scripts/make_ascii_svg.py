"""
Step 3b - Convert the prepped grayscale photo into a self-typing,
monochrome ASCII SVG. Each row wipes in left-to-right, staggered top to
bottom. Prints once and freezes (no looping).

Usage:
    python scripts/make_ascii_svg.py
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ASCII_SVG, PREPPED_PHOTO

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense); leading space = blank
GRID_COLS = 100
GRID_ROWS = 53

CHAR_W = 6.2
CHAR_H = 11.0
FONT_SIZE = 11
FILL_COLOR = "#cfd8e3"   # single monochrome fill - no per-char color
ROW_DELAY = 0.045        # seconds between each row starting
WIPE_DURATION = 0.35


def image_to_ascii_rows(path: str, cols: int = GRID_COLS, rows: int = GRID_ROWS):
    img = Image.open(path).convert("L").resize((cols, rows))
    pixels = list(img.getdata())
    ramp_len = len(RAMP) - 1
    ascii_rows = []
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            brightness = pixels[r * cols + c]  # 0 = black .. 255 = white
            idx = int((255 - brightness) / 255 * ramp_len)
            row_chars.append(RAMP[idx])
        ascii_rows.append("".join(row_chars))
    return ascii_rows


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg(ascii_rows, out_path: str):
    width = GRID_COLS * CHAR_W
    height = GRID_ROWS * CHAR_H

    parts = [
        f'<svg viewBox="0 0 {width:.0f} {height:.0f}" xmlns="http://www.w3.org/2000/svg" '
        f'font-family="monospace" font-size="{FONT_SIZE}">'
    ]

    for i, row_text in enumerate(ascii_rows):
        y = (i + 1) * CHAR_H - 2
        begin = i * ROW_DELAY
        clip_id = f"clip{i}"
        text = esc(row_text)

        # a rect that widens from 0 -> full width clips the row's text,
        # producing the left-to-right "typing" wipe
        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(
            f'  <rect x="0" y="{y - CHAR_H:.1f}" height="{CHAR_H:.1f}" width="0">'
            f'<animate attributeName="width" from="0" to="{width:.0f}" '
            f'begin="{begin:.3f}s" dur="{WIPE_DURATION}s" fill="freeze" '
            f'calcMode="spline" keySplines="0.25 0.1 0.25 1"/></rect>'
        )
        parts.append("</clipPath>")

        parts.append(
            f'<text x="0" y="{y:.1f}" fill="{FILL_COLOR}" clip-path="url(#{clip_id})" '
            f'xml:space="preserve">{text}</text>'
        )

    parts.append("</svg>")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Wrote {out_path}")


def main():
    if not os.path.exists(PREPPED_PHOTO):
        print(
            f"'{PREPPED_PHOTO}' bulunamadi. Once 'python scripts/prep_photo.py <foto.jpg>' calistir.",
            file=sys.stderr,
        )
        sys.exit(1)
    rows = image_to_ascii_rows(PREPPED_PHOTO)
    build_svg(rows, ASCII_SVG)


if __name__ == "__main__":
    main()
