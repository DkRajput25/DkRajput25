import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent.parent

USERNAME = "DkRajput25"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUTPUT = BASE_DIR / "data" / "contributions.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}


def fetch_page():

    print(f"Fetching contributions for @{USERNAME}...")

    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=30
    )

    print(
        f"GitHub response: {response.status_code}"
    )

    response.raise_for_status()

    return response.text


def extract_count(label):

    if not label:
        return 0

    # Handles:
    # "1 contribution on..."
    # "25 contributions on..."
    match = re.search(
        r"(\d[\d,]*)\s+contributions?",
        label,
        re.IGNORECASE
    )

    if match:

        return int(
            match.group(1).replace(",", "")
        )

    return 0


def parse_contributions(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    days = []

    cells = soup.select(
        "[data-date][data-level]"
    )

    print(
        f"Contribution cells found: {len(cells)}"
    )

    for cell in cells:

        date = cell.get(
            "data-date"
        )

        level = cell.get(
            "data-level",
            "0"
        )

        if not date:
            continue

        label = cell.get(
            "aria-label",
            ""
        )

        count = extract_count(
            label
        )

        # GitHub can also expose the
        # contribution text inside a
        # title element.
        if count == 0:

            title = cell.find(
                "title"
            )

            if title:

                count = extract_count(
                    title.get_text(
                        strip=True
                    )
                )

        days.append({
            "date": date,
            "count": count,
            "level": int(level)
        })

    return days


def calculate_stats(days):

    total = sum(
        day["count"]
        for day in days
    )

    best_day = max(
        days,
        key=lambda day: day["count"],
        default=None
    )

    sorted_days = sorted(
        days,
        key=lambda day: day["date"]
    )

    longest_streak = 0
    streak = 0
    previous_date = None

    for day in sorted_days:

        current_date = datetime.strptime(
            day["date"],
            "%Y-%m-%d"
        ).date()

        if day["count"] > 0:

            if (
                previous_date is not None
                and
                (current_date - previous_date).days == 1
            ):
                streak += 1
            else:
                streak = 1

            longest_streak = max(
                longest_streak,
                streak
            )

            previous_date = current_date

        else:

            streak = 0
            previous_date = None

    current_streak = 0

    for day in reversed(sorted_days):

        if day["count"] > 0:
            current_streak += 1
        else:
            break

    return {
        "total": total,
        "longest_streak": longest_streak,
        "current_streak": current_streak,
        "best_day": best_day
    }


def main():

    try:

        html = fetch_page()

        days = parse_contributions(
            html
        )

        if not days:

            print(
                "ERROR: No contribution cells found."
            )

            sys.exit(1)

        stats = calculate_stats(
            days
        )

        result = {
            "username": USERNAME,
            "updated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "days": days,
            "stats": stats
        }

        OUTPUT.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        OUTPUT.write_text(
            json.dumps(
                result,
                indent=2
            ),
            encoding="utf-8"
        )

        print()
        print("SUCCESS!")
        print(
            f"Saved {len(days)} days."
        )
        print(
            f"Total contributions: "
            f"{stats['total']}"
        )
        print(
            f"Current streak: "
            f"{stats['current_streak']}"
        )
        print(
            f"Longest streak: "
            f"{stats['longest_streak']}"
        )
        print(
            f"File: {OUTPUT}"
        )

    except requests.RequestException as error:

        print(
            f"NETWORK ERROR: {error}"
        )

        sys.exit(1)

    except Exception as error:

        print(
            f"ERROR: {error}"
        )

        sys.exit(1)


if __name__ == "__main__":
    main()