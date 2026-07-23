"""
Step 5b - Render data/contributions.json as an animated 53-week x 7-day
contribution heatmap SVG.

Boxes reveal with a diagonal, line-after-line slide-down (CSS keyframes,
play once on load, then freeze - no looping). Adds a Less->More legend and
a stats footer.

Usage:
    python scripts/render_heatmap_svg.py
"""
import calendar
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CONTRIB_JSON, HEATMAP_SVG

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
# none -> brightest

BOX = 11
GAP = 3
CELL = BOX + GAP
LEFT_PAD = 28        # room for weekday labels
TOP_PAD = 22          # room for month labels
LEGEND_H = 26
FOOTER_H = 22
STEP_DELAY = 0.012    # seconds added per diagonal step (week + day index)
REVEAL_DUR = 0.28


def ordinal(n: int) -> str:
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def load_grid(days):
    if not days:
        return [], 0
    first_weekday = (datetime.strptime(days[0]["date"], "%Y-%m-%d").isoweekday()) % 7  # 0=Sun
    grid = {}
    max_col = 0
    for i, d in enumerate(days):
        col = (i + first_weekday) // 7
        row = (i + first_weekday) % 7
        grid[(col, row)] = d
        max_col = max(max_col, col)
    return grid, max_col


def month_labels(days):
    """Return {col: 'Jan'} for the first week-column each month first appears in."""
    if not days:
        return {}
    first_weekday = (datetime.strptime(days[0]["date"], "%Y-%m-%d").isoweekday()) % 7
    labels = {}
    seen_months = set()
    for i, d in enumerate(days):
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        key = (dt.year, dt.month)
        if key not in seen_months:
            seen_months.add(key)
            col = (i + first_weekday) // 7
            labels[col] = calendar.month_abbr[dt.month]
    return labels


def build(days, stats, username: str, out_path: str):
    grid, max_col = load_grid(days)
    cols = max_col + 1
    width = LEFT_PAD + cols * CELL
    height = TOP_PAD + 7 * CELL + LEGEND_H + FOOTER_H

    parts = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system, Segoe UI, sans-serif">']

    # once-only reveal animation, defined per-box via inline <style> keyframes
    parts.append("<style>")
    parts.append(
        "@keyframes revealBox { from { opacity: 0; transform: translate(0px,-6px); } "
        "to { opacity: 1; transform: translate(0px,0px); } }"
        ".day-box { opacity: 0; animation-name: revealBox; animation-duration: "
        f"{REVEAL_DUR}s; animation-timing-function: ease-out; animation-fill-mode: forwards; }}"
    )
    parts.append("</style>")

    # weekday labels (Mon/Wed/Fri, GitHub-style sparse labels)
    weekday_names = {1: "Mon", 3: "Wed", 5: "Fri"}
    for row, name in weekday_names.items():
        y = TOP_PAD + row * CELL + BOX - 2
        parts.append(
            f'<text x="0" y="{y}" font-size="9" fill="#7d8590">{name}</text>'
        )

    # month labels
    for col, label in month_labels(days).items():
        x = LEFT_PAD + col * CELL
        parts.append(f'<text x="{x}" y="{TOP_PAD - 8}" font-size="9" fill="#7d8590">{label}</text>')

    # boxes
    for col in range(cols):
        for row in range(7):
            d = grid.get((col, row))
            level = d["level"] if d else 0
            color = PALETTE[min(level, len(PALETTE) - 1)]
            x = LEFT_PAD + col * CELL
            y = TOP_PAD + row * CELL
            delay = (col + row) * STEP_DELAY
            title = ""
            if d:
                dt = datetime.strptime(d["date"], "%Y-%m-%d")
                nice_date = f"{calendar.month_name[dt.month]} {ordinal(dt.day)}"
                count = d["count"]
                title = f"{count} contribution{'s' if count != 1 else ''} on {nice_date}"
            parts.append(
                f'<rect class="day-box" x="{x}" y="{y}" width="{BOX}" height="{BOX}" rx="2" '
                f'fill="{color}" style="animation-delay:{delay:.3f}s">'
                + (f'<title>{title}</title>' if title else "")
                + "</rect>"
            )

    # legend (Less -> More)
    legend_y = TOP_PAD + 7 * CELL + 14
    lx = width - LEFT_PAD - len(PALETTE) * CELL - 40
    parts.append(f'<text x="{lx - 34}" y="{legend_y + 8}" font-size="9" fill="#7d8590">Less</text>')
    for i, color in enumerate(PALETTE):
        parts.append(
            f'<rect x="{lx + i * CELL}" y="{legend_y}" width="{BOX}" height="{BOX}" rx="2" fill="{color}"/>'
        )
    parts.append(
        f'<text x="{lx + len(PALETTE) * CELL + 6}" y="{legend_y + 8}" font-size="9" fill="#7d8590">More</text>'
    )

    # stats footer
    footer_y = legend_y + LEGEND_H
    total = stats.get("total", 0)
    streak = stats.get("longest_streak", 0)
    parts.append(
        f'<text x="{LEFT_PAD}" y="{footer_y}" font-size="10.5" fill="#c9d1d9">'
        f'{total:,} contributions in the last year &#183; longest streak {streak} days'
        f'</text>'
    )

    parts.append("</svg>")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(f"Wrote {out_path}")


def main():
    with open(CONTRIB_JSON, encoding="utf-8") as f:
        data = json.load(f)
    build(data["days"], data["stats"], data.get("username", ""), HEATMAP_SVG)


if __name__ == "__main__":
    main()
