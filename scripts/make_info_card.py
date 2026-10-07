from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT = BASE_DIR / "profile" / "info-card.svg"

WIDTH = 490
HEIGHT = 520

rows = [
    ("NAME", "Dikshant Chauhan"),
    ("ROLE", "Java Backend Developer"),
    ("STACK", "Java • Spring Boot • React"),
    ("DATABASE", "MySQL • PostgreSQL"),
    ("TOOLS", "Git • Docker • Postman"),
    ("FOCUS", "Backend • REST APIs • DSA"),
    ("PROJECT", "CodeSphere"),
    ("PROJECT", "DocMind"),
]

svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

<style>
    .title {{
        font-family: monospace;
        font-size: 22px;
        font-weight: bold;
        fill: #58a6ff;
    }}

    .key {{
        font-family: monospace;
        font-size: 16px;
        font-weight: bold;
        fill: #7ee787;
    }}

    .value {{
        font-family: monospace;
        font-size: 16px;
        fill: #c9d1d9;
    }}

    .line {{
        opacity: 0;
        animation: appear 0.45s ease-out forwards;
    }}

    @keyframes appear {{
        from {{
            opacity: 0;
            transform: translateX(15px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
</style>

<rect
    x="0"
    y="0"
    width="100%"
    height="100%"
    rx="16"
    fill="#0d1117"
    stroke="#30363d"
    stroke-width="2"
/>

<text
    x="25"
    y="42"
    class="title"
>
    dk@github:~$ neofetch
</text>

<line
    x1="25"
    y1="58"
    x2="465"
    y2="58"
    stroke="#30363d"
/>
'''

start_y = 100

for i, (key, value) in enumerate(rows):
    y = start_y + i * 45
    delay = 0.5 + i * 0.18

    svg += f'''
<g
    class="line"
    style="animation-delay:{delay:.2f}s"
>
    <text
        x="25"
        y="{y}"
        class="key"
    >{key}</text>

    <text
        x="145"
        y="{y}"
        class="value"
    >{value}</text>
</g>
'''

svg += f'''
<line
    x1="25"
    y1="475"
    x2="465"
    y2="475"
    stroke="#30363d"
/>

<text
    x="25"
    y="505"
    class="value"
>
    $ build • learn • solve • repeat
</text>

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Info card created: {OUTPUT}")