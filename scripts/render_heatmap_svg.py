import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT = BASE_DIR / "data" / "contributions.json"
OUTPUT = BASE_DIR / "profile" / "contrib-heatmap.svg"

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

CELL_SIZE = 13
GAP = 3

LEFT = 45
TOP = 48

WEEKS = 53
DAYS = 7

GRID_WIDTH = WEEKS * (CELL_SIZE + GAP)
GRID_HEIGHT = DAYS * (CELL_SIZE + GAP)

WIDTH = LEFT + GRID_WIDTH + 20
HEIGHT = TOP + GRID_HEIGHT + 95

BACKGROUND = "#0d1117"

PALETTE = [
    "#161b22",  # 0
    "#0e4429",  # 1
    "#006d32",  # 2
    "#26a641",  # 3
    "#39d353",  # 4
]

TEXT = "#8b949e"
BRIGHT_TEXT = "#c9d1d9"
BORDER = "#30363d"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

if not INPUT.exists():
    raise FileNotFoundError(
        "contributions.json not found. "
        "Run fetch_contributions.py first."
    )

data = json.loads(
    INPUT.read_text(
        encoding="utf-8"
    )
)

days = data.get("days", [])
stats = data.get("stats", {})

# Convert to dictionary
contribution_map = {
    day["date"]: day
    for day in days
}


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def parse_date(value):
    return datetime.strptime(
        value,
        "%Y-%m-%d"
    ).date()


def escape_xml(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def get_level(day):
    if not day:
        return 0

    count = day.get("count", 0)

    if count <= 0:
        return 0
    elif count <= 2:
        return 1
    elif count <= 5:
        return 2
    elif count <= 10:
        return 3
    else:
        return 4


# ---------------------------------------------------------
# Sort contribution days
# ---------------------------------------------------------

sorted_days = sorted(
    days,
    key=lambda item: item["date"]
)

if not sorted_days:
    raise ValueError(
        "No contribution days available."
    )


# ---------------------------------------------------------
# Build SVG
# ---------------------------------------------------------

svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>

<style>

    .title {{
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;

        font-size: 17px;
        font-weight: 600;

        fill: {BRIGHT_TEXT};
    }}

    .label {{
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;

        font-size: 10px;

        fill: {TEXT};
    }}

    .stat {{
        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;

        font-size: 12px;

        fill: {TEXT};
    }}

    .cell {{
        opacity: 0;

        animation:
            revealCell
            0.35s
            ease-out
            forwards;
    }}

    @keyframes revealCell {{

        from {{
            opacity: 0;
            transform:
                translateY(-8px);
        }}

        to {{
            opacity: 1;
            transform:
                translateY(0);
        }}

    }}

</style>

<!-- Background -->

<rect
    x="0"
    y="0"
    width="100%"
    height="100%"
    rx="14"
    fill="{BACKGROUND}"
    stroke="{BORDER}"
    stroke-width="1"
/>


<!-- Terminal title -->

<text
    x="20"
    y="27"
    class="title"
>
    dk@github:~$ ./contributions.sh
</text>


<!-- Year / timeline -->

<text
    x="{LEFT}"
    y="43"
    class="label"
>
    53 weeks of contribution activity
</text>
'''


# ---------------------------------------------------------
# Day labels
# ---------------------------------------------------------

day_names = {
    1: "Mon",
    3: "Wed",
    5: "Fri"
}

for day_index, label in day_names.items():

    y = (
        TOP
        + day_index * (CELL_SIZE + GAP)
        + 10
    )

    svg += f'''
<text
    x="10"
    y="{y}"
    class="label"
>
    {label}
</text>
'''


# ---------------------------------------------------------
# Generate 53 x 7 grid
# ---------------------------------------------------------

# GitHub contribution calendars run Sunday -> Saturday.
# We create a fixed 53-week visual grid.

if sorted_days:

    first_date = parse_date(
        sorted_days[0]["date"]
    )

    # Move backwards to Sunday
    days_to_sunday = (
        first_date.weekday() + 1
    ) % 7

    grid_start = (
        first_date
        .fromordinal(
            first_date.toordinal()
            - days_to_sunday
        )
    )

else:

    grid_start = datetime.now().date()


for week in range(WEEKS):

    for day_index in range(DAYS):

        current_date = (
            grid_start
            .fromordinal(
                grid_start.toordinal()
                + week * 7
                + day_index
            )
        )

        date_string = current_date.isoformat()

        contribution = contribution_map.get(
            date_string
        )

        level = get_level(
            contribution
        )

        color = PALETTE[level]

        x = (
            LEFT
            + week * (CELL_SIZE + GAP)
        )

        y = (
            TOP
            + day_index * (CELL_SIZE + GAP)
        )

        # Diagonal reveal
        delay = (
            (week * 0.018)
            + (day_index * 0.012)
        )

        count = (
            contribution["count"]
            if contribution
            else 0
        )

        aria = (
            f"{count} contributions "
            f"on {date_string}"
        )

        svg += f'''
<rect
    class="cell"
    x="{x}"
    y="{y}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="3"
    fill="{color}"
    style="animation-delay:{delay:.3f}s"
>
    <title>
        {escape_xml(aria)}
    </title>
</rect>
'''


# ---------------------------------------------------------
# Legend
# ---------------------------------------------------------

legend_y = TOP + GRID_HEIGHT + 25

svg += f'''
<text
    x="{LEFT}"
    y="{legend_y}"
    class="label"
>
    Less
</text>
'''

for index, color in enumerate(PALETTE):

    x = (
        LEFT
        + 35
        + index * (CELL_SIZE + GAP)
    )

    svg += f'''
<rect
    x="{x}"
    y="{legend_y - 10}"
    width="{CELL_SIZE}"
    height="{CELL_SIZE}"
    rx="3"
    fill="{color}"
/>
'''


svg += f'''
<text
    x="{LEFT + 35 + len(PALETTE) * (CELL_SIZE + GAP) + 8}"
    y="{legend_y}"
    class="label"
>
    More
</text>
'''


# ---------------------------------------------------------
# Stats footer
# ---------------------------------------------------------

total = stats.get(
    "total",
    0
)

current_streak = stats.get(
    "current_streak",
    0
)

longest_streak = stats.get(
    "longest_streak",
    0
)

footer_y = HEIGHT - 20

svg += f'''
<text
    x="20"
    y="{footer_y}"
    class="stat"
>
    {total:,} contributions
    •
    Current streak: {current_streak}
    •
    Longest streak: {longest_streak}
</text>
'''


# ---------------------------------------------------------
# Close SVG
# ---------------------------------------------------------

svg += """

</svg>
"""


# ---------------------------------------------------------
# Write file
# ---------------------------------------------------------

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT.write_text(
    svg,
    encoding="utf-8"
)

print(
    f"Heatmap SVG created: {OUTPUT}"
)
