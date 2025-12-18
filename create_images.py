from PIL import Image, ImageDraw, ImageFont

# Create icon (512x512)
icon = Image.new('RGB', (512, 512), color='#1E88E5')
draw = ImageDraw.Draw(icon)

# Draw simple NTRLI text
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
except:
    font = ImageFont.load_default()

text = "NTRLI"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (512 - text_width) / 2
y = (512 - text_height) / 2

draw.text((x, y), text, fill='white', font=font)
icon.save('app1/images/icon.png')

# Create presplash (800x480)
presplash = Image.new('RGB', (800, 480), color='#1E88E5')
draw2 = ImageDraw.Draw(presplash)

try:
    font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
except:
    font2 = ImageFont.load_default()

text2 = "NTRLI Superbot"
bbox2 = draw2.textbbox((0, 0), text2, font=font2)
text_width2 = bbox2[2] - bbox2[0]
text_height2 = bbox2[3] - bbox2[1]
x2 = (800 - text_width2) / 2
y2 = (480 - text_height2) / 2

draw2.text((x2, y2), text2, fill='white', font=font2)
presplash.save('app1/images/presplash.png')

print("✅ Icon and presplash created successfully!")
