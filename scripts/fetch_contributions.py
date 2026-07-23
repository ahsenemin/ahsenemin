"""
Step 5a - Fetch a public GitHub contribution calendar with NO auth / NO token.

GitHub serves this as plain HTML at:
    https://github.com/users/<username>/contributions

Each day is a <td class="ContributionCalendar-day"> with data-date and
data-level (0-4) attributes. The exact count lives in a sibling <tool-tip>
element, e.g. "18 contributions on July 20th." / "No contributions on Sep 1st."

Writes data/contributions.json with:
    - days: [{date, level, count}, ...]   (raw, oldest -> newest)
    - stats: {total, current_streak, longest_streak, best_day, monthly}

Usage:
    python scripts/fetch_contributions.py
"""
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GITHUB_USERNAME, CONTRIB_JSON

URL_TMPL = "https://github.com/users/{username}/contributions"
COUNT_RE = re.compile(r"^(\d+)\s+contributions?\s+on", re.IGNORECASE)


def fetch_html(username: str) -> str:
    url = URL_TMPL.format(username=username)
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    return resp.text


def parse_days(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tooltip_by_for = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        if target:
            tooltip_by_for[target] = tip.get_text(strip=True)

    days = []
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        d = td.get("data-date")
        if not d:
            continue
        level = int(td.get("data-level", 0))
        tip_text = tooltip_by_for.get(td.get("id"), "")
        m = COUNT_RE.match(tip_text)
        count = int(m.group(1)) if m else 0
        days.append({"date": d, "level": level, "count": count})

    days.sort(key=lambda x: x["date"])
    return days


def compute_stats(days):
    total = sum(d["count"] for d in days)

    # streaks
    longest = current = 0
    for d in days:
        if d["count"] > 0:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    # current streak must be anchored to the most recent day(s)
    current_streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    best_day = max(days, key=lambda x: x["count"], default=None)

    monthly = defaultdict(int)
    for d in days:
        month_key = d["date"][:7]  # YYYY-MM
        monthly[d["count"]] if False else None
        monthly[month_key] += d["count"]

    return {
        "total": total,
        "current_streak": current_streak,
        "longest_streak": longest,
        "best_day": best_day,
        "monthly": dict(sorted(monthly.items())),
    }


def main():
    html = fetch_html(GITHUB_USERNAME)
    days = parse_days(html)
    if not days:
        print("Uyari: hic gun bulunamadi, GitHub HTML yapisi degismis olabilir.", file=sys.stderr)
    stats = compute_stats(days)

    os.makedirs(os.path.dirname(CONTRIB_JSON), exist_ok=True)
    with open(CONTRIB_JSON, "w", encoding="utf-8") as f:
        json.dump({"username": GITHUB_USERNAME, "days": days, "stats": stats}, f, indent=2)

    print(f"{len(days)} gun yazildi -> {CONTRIB_JSON}")
    print(f"Toplam katki: {stats['total']}, guncel seri: {stats['current_streak']}, en uzun seri: {stats['longest_streak']}")


if __name__ == "__main__":
    main()
