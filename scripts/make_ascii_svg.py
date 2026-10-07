from pathlib import Path
from PIL import Image
import html

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT = BASE_DIR / "profile" / "source-prepped.png"
OUTPUT = BASE_DIR / "profile" / "ascii.svg"

print("Input:", INPUT)
print("Input exists:", INPUT.exists())

if not INPUT.exists():
    raise FileNotFoundError(f"Image not found: {INPUT}")

RAMP = " .:-=+*#%@"

COLS = 90
ROWS = 55
CHAR_WIDTH = 8
CHAR_HEIGHT = 11

WIDTH = COLS * CHAR_WIDTH
HEIGHT = ROWS * CHAR_HEIGHT

img = Image.open(INPUT).convert("L")
img = img.resize((COLS, ROWS))

pixels = list(img.getdata())

lines = []

for y in range(ROWS):
    line = ""

    for x in range(COLS):
        brightness = pixels[y * COLS + x]

        index = int((255 - brightness) / 256 * len(RAMP))
        index = min(index, len(RAMP) - 1)

        char = RAMP[index]

        if char == " ":
            char = "&#160;"
        else:
            char = html.escape(char)

        line += char

    lines.append(line)

svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.ascii {{
    font-family: "Courier New", monospace;
    font-size: 11px;
    font-weight: bold;
    fill: #c9d1d9;
}}

.row {{
    opacity: 0;
    animation: reveal 0.4s ease-out forwards;
}}

@keyframes reveal {{
    from {{
        opacity: 0;
        transform: translateX(-15px);
    }}

    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

</style>

<rect width="100%" height="100%" fill="#0d1117"/>

'''

for y, line in enumerate(lines):

    delay = y * 0.04

    svg += f'''
<text
    class="ascii row"
    x="0"
    y="{(y + 1) * CHAR_HEIGHT}"
    style="animation-delay:{delay:.3f}s"
>
{line}
</text>
'''

svg += """
</svg>
"""

OUTPUT.write_text(svg, encoding="utf-8")

print()
print("SUCCESS!")
print("ASCII SVG created:")
print(OUTPUT)
print("File exists:", OUTPUT.exists())
print("File size:", OUTPUT.stat().st_size, "bytes")