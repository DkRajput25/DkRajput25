from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT = BASE_DIR / "profile" / "profile-photo.png"
OUTPUT = BASE_DIR / "profile" / "source-prepped.png"

# Load image
img = Image.open(INPUT).convert("RGB")

# Make it square using a center crop
size = min(img.width, img.height)
left = (img.width - size) // 2
top = (img.height - size) // 2

img = img.crop((
    left,
    top,
    left + size,
    top + size
))

# Resize for ASCII processing
img = img.resize((160, 160), Image.Resampling.LANCZOS)

# Convert to grayscale
gray = ImageOps.grayscale(img)

# Improve contrast
gray = ImageEnhance.Contrast(gray).enhance(2.0)

# Slightly sharpen details
gray = gray.filter(ImageFilter.SHARPEN)

# Invert if needed? No — dark stays dark, bright stays bright.

# Save prepared image
gray.save(OUTPUT)

print(f"Prepared image saved to: {OUTPUT}")