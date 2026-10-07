from pathlib import Path
import html

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = BASE_DIR / "profile" / "tech-stack.svg"

TECH = [
    ("Java", "☕"),
    ("Spring Boot", "🍃"),
    ("React", "⚛"),
    ("Python", "🐍"),
    ("JavaScript", "JS"),
    ("C", "C"),
    ("PostgreSQL", "PG"),
    ("MySQL", "SQL"),
    ("Docker", "◆"),
    ("Git", "G"),
    ("GitHub", "GH"),
    ("Postman", "P"),
]

CARD_WIDTH = 210
CARD_HEIGHT = 90
GAP = 14
COLUMNS = 4
ROWS = (len(TECH) + COLUMNS - 1) // COLUMNS

WIDTH = COLUMNS * CARD_WIDTH + (COLUMNS - 1) * GAP
HEIGHT = ROWS * CARD_HEIGHT + (ROWS - 1) * GAP

svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.card {{
    fill: #0d1117;
    stroke: #30363d;
    stroke-width: 1.5;
    opacity: 0;
    animation: appear 0.6s ease-out forwards;
}}

.icon {{
    fill: #58a6ff;
    font-family: Arial, sans-serif;
    font-size: 25px;
    font-weight: bold;
}}

.name {{
    fill: #c9d1d9;
    font-family: Arial, sans-serif;
    font-size: 14px;
    font-weight: 600;
}}

@keyframes appear {{
    from {{
        opacity: 0;
        transform: translateY(15px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

</style>

<rect width="100%" height="100%"
      rx="16"
      fill="#010409"/>

'''

for index, (name, icon) in enumerate(TECH):

    row = index // COLUMNS
    column = index % COLUMNS

    x = column * (CARD_WIDTH + GAP)
    y = row * (CARD_HEIGHT + GAP)

    delay = index * 0.12

    safe_name = html.escape(name)
    safe_icon = html.escape(icon)

    svg += f'''
<g style="animation-delay:{delay:.2f}s">

    <rect
        class="card"
        x="{x}"
        y="{y}"
        width="{CARD_WIDTH}"
        height="{CARD_HEIGHT}"
        rx="12"
    />

    <text
        class="icon"
        x="{x + 25}"
        y="{y + 38}"
    >{safe_icon}</text>

    <text
        class="name"
        x="{x + 70}"
        y="{y + 37}"
    >{safe_name}</text>

</g>
'''

svg += '''
</svg>
'''

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(svg, encoding="utf-8")

print("SUCCESS!")
print(f"Tech stack SVG created: {OUTPUT}")