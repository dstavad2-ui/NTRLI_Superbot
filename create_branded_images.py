from PIL import Image, ImageDraw, ImageFont
import math

# Create icon with NTRLI branding (matching screenshot style)
size = 512
icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(icon)

# Background - dark with gradient effect
for i in range(size):
    alpha = int(255 * (1 - i / size * 0.3))
    draw.rectangle([(0, i), (size, i+1)], fill=(10, 10, 30, alpha))

# Draw star/sparkle decorations (matching screenshot)
def draw_star(x, y, size, color):
    points = []
    for i in range(8):
        angle = i * math.pi / 4
        if i % 2 == 0:
            r = size
        else:
            r = size / 3
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, fill=color)

# Add decorative stars (blue and purple like screenshot)
stars = [
    (100, 100, 20, (100, 150, 255, 200)),
    (412, 100, 20, (180, 120, 255, 200)),
    (100, 412, 20, (150, 100, 255, 200)),
    (412, 412, 20, (100, 180, 255, 200)),
    (256, 80, 15, (200, 150, 255, 200)),
]
for x, y, s, color in stars:
    draw_star(x, y, s, color)

# Draw main NTRLI text with gradient effect
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
except:
    font = ImageFont.load_default()

text = "NTRLI"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (size - text_width) / 2
y = (size - text_height) / 2

# Text with blue-purple gradient (matching screenshot)
for offset in range(5, 0, -1):
    draw.text((x+offset, y+offset), text, fill=(50, 50, 100, 100), font=font)

# Main text - gradient from blue to purple
draw.text((x, y), text, fill=(150, 180, 255, 255), font=font)

# Add sparkle effect
draw_star(420, 250, 25, (255, 200, 255, 180))

icon.save('app1/images/icon.png')
print("✅ NTRLI branded icon created!")

# Create presplash with same style
presplash = Image.new('RGB', (800, 480), (10, 10, 30))
draw2 = ImageDraw.Draw(presplash)

# Add stars to presplash
stars_splash = [
    (100, 80, 15, (100, 150, 255)),
    (700, 80, 15, (180, 120, 255)),
    (100, 400, 15, (150, 100, 255)),
    (700, 400, 15, (100, 180, 255)),
    (400, 50, 20, (200, 150, 255)),
]
for x, y, s, color in stars_splash:
    draw_star(x, y, s, color)

# Main text
try:
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
except:
    font2 = ImageFont.load_default()

text2 = "NTRLI"
bbox2 = draw2.textbbox((0, 0), text2, font=font2)
text_width2 = bbox2[2] - bbox2[0]
text_height2 = bbox2[3] - bbox2[1]
x2 = (800 - text_width2) / 2
y2 = (480 - text_height2) / 2

draw2.text((x2, y2), text2, fill=(150, 180, 255), font=font2)

presplash.save('app1/images/presplash.png')
print("✅ NTRLI branded presplash created!")
