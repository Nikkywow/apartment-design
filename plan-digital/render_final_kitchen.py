from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "design-visuals" / "26-kitchen-final-render.png"

WIDTH, HEIGHT = 1800, 1100

img = Image.new("RGBA", (WIDTH, HEIGHT), (241, 234, 225, 255))
d = ImageDraw.Draw(img)

# Colors
cream = (238, 230, 220)
wall = (230, 220, 209)
floor = (205, 179, 146)
walnut = (93, 61, 42)
walnut2 = (119, 83, 64)
olive = (110, 121, 90)
graphite = (54, 56, 54)
brass = (182, 147, 92)
stone = (217, 210, 197)
window = (177, 201, 196)
shadow = (35, 28, 26, 80)
plant = (62, 111, 73)
chair = (174, 164, 151)
fruit = (160, 88, 48)
light = (255, 223, 170)

# Room geometry
# left wall
left_wall = [(170, 150), (620, 150), (620, 760), (170, 900)]
d.polygon(left_wall, fill=wall)
# top wall
front_wall = [(620, 150), (1400, 150), (1600, 820), (620, 820)]
d.polygon(front_wall, fill=wall)
# floor
floor_poly = [(170, 900), (620, 760), (1600, 820), (1450, 1070), (300, 1070)]
d.polygon(floor_poly, fill=floor)

# window on right wall
window_poly = [(1360, 210), (1540, 210), (1575, 740), (1380, 760)]
d.polygon(window_poly, fill=window)
# window crossbars
for x in [1400, 1475]:
    d.line((x, 210, x, 740), fill=(210, 220, 214), width=4)
for y in [290, 420, 560, 680]:
    d.line((1360, y, 1575, y), fill=(210, 220, 214), width=3)

# Ceiling light glow
light_orb = [(920, 140), (1030, 140), (1030, 220), (920, 220)]
d.ellipse((890, 120, 1050, 180), fill=(255, 235, 202, 150))

# Left kitchen cabinets (perspective-ish)
# base cabinets group along left wall
cab_x = 255
cab_y = 730
cab_w = 250
cab_h = 180
for i, (color, w) in enumerate([(walnut, 120), (walnut2, 90), (walnut, 90), (walnut2, 90)]):
    x0 = cab_x + i * 65
    y0 = cab_y - i * 3
    d.rounded_rectangle((x0, y0, x0 + w, cab_y + 180), radius=12, fill=color)
    d.rounded_rectangle((x0, y0 - 130, x0 + w, y0 + 10), radius=8, fill=olive)
    # drawer lines
    for j in range(1, 3):
        yy = y0 + j * 45
        d.line((x0 + 8, yy, x0 + w - 8, yy), fill=(255, 255, 255, 70), width=2)

# Top wall cabinet run
for i in range(7):
    x0 = 680 + i * 95
    y0 = 340
    d.rounded_rectangle((x0, y0, x0 + 85, y0 + 150), radius=8, fill=walnut2)
    d.line((x0 + 10, y0 + 50, x0 + 75, y0 + 50), fill=(255,255,255,60), width=2)

# countertop and backsplash
counter_top = [(650, 510), (1240, 510), (1320, 610), (720, 610)]
d.polygon(counter_top, fill=graphite)
backpanel = [(700, 475), (1210, 475), (1255, 560), (700, 560)]
d.polygon(backpanel, fill=olive)

# Kitchen inner appliances
# fridge
fridge = (245, 260, 430, 620)
d.rounded_rectangle(fridge, radius=10, fill=walnut)
# freezer door line
for x in [290, 385]:
    d.line((x, 300, x, 590), fill=(255,255,255,80), width=3)

# sink base + hob + oven on top wall
sink = (630, 575, 760, 705)
d.rounded_rectangle(sink, radius=12, fill=walnut2)
# sink bowl
for a in [670, 700, 730]:
    d.arc((a, 600, a+35, 640), start=0, end=180, fill=(255,255,255,130), width=3)

# hob 
for i in range(3):
    x = 810 + i*75
    d.ellipse((x, 590, x+40, 630), fill=(20, 20, 20))
    d.line((x+16, 590, x+16, 630), fill=(255,255,255,60), width=2)
    d.line((x, 610, x+40, 610), fill=(255,255,255,60), width=2)

# oven block
oven = (1080, 560, 1185, 700)
d.rounded_rectangle(oven, radius=12, fill=walnut)
# microwave
microwave = (1195, 510, 1280, 640)
d.rounded_rectangle(microwave, radius=10, fill=walnut2)

# Coffee station niche 
coffee = (1200, 590, 1290, 690)
d.rounded_rectangle(coffee, radius=10, fill=olive)
# coffee mug
for mugx in [1226, 1260]:
    d.rounded_rectangle((mugx, 615, mugx+18, 650), radius=5, fill=(236, 234, 225, 150))

# stools and dining area
# round table shadow
shadow_table = (920, 655, 1120, 865)
d.ellipse((870, 715, 1170, 910), fill=shadow)
# table top
for radius in [130, 120]:
    d.ellipse((930, 720, 1090, 880), fill=(203, 183, 151))
# table base
for y in [760, 820]:
    d.line((1000, y, 1020, y), fill=(166, 128, 98), width=8)
# chairs around table
chair_positions = [(820, 750), (1080, 750), (900, 900), (1040, 900)]
for cx, cy in chair_positions:
    d.rounded_rectangle((cx-25, cy-20, cx+25, cy+50), radius=8, fill=chair)
    d.line((cx, cy+50, cx, cy+85), fill=(146,130,117), width=8)

# Sofa / living zone on left side of room
sofa = (820, 750, 1320, 930)
d.rounded_rectangle(sofa, radius=18, fill=(188, 170, 152))
# sofa back pillows
for px in [900, 1010, 1120]:
    d.rounded_rectangle((px, 760, px+80, 830), radius=10, fill=(201, 190, 176))
# plant
plant_pot = (540, 770, 600, 840)
d.rounded_rectangle(plant_pot, radius=8, fill=(120, 89, 72))
# leaves
for leaf_x in [540, 555, 570, 585]:
    d.ellipse((leaf_x, 720, leaf_x+35, 780), fill=plant)

# small details: plates on counter, fruit bowl
for fx in [730, 760, 805]:
    d.ellipse((fx, 623, fx+18, 640), fill=(245, 232, 223))
    d.ellipse((fx+5, 620, fx+13, 637), fill=fruit)

# tasks lights under cabinets
for x in [680, 770, 860, 950, 1040, 1130]:
    d.line((x, 515, x, 620), fill=(255, 219, 165, 180), width=6)

# final vignette
vignette = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
vd = ImageDraw.Draw(vignette)
for r in range(0, 900, 12):
    alpha = int(140 - r / 10)
    if alpha > 0:
        vd.ellipse((200-r, 120-r, WIDTH-200+r, HEIGHT-40+r), outline=(0,0,0,alpha), width=2)
img = Image.alpha_composite(img, vignette)

# Save
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
img = img.convert("RGB")
img.save(OUTPUT, quality=95)
print(f"Render created: {OUTPUT}")
