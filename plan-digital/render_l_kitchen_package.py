from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "plan-digital" / "kitchen-spec.json"
OUTPUT_PATH = ROOT / "design-visuals" / "18-kitchen-L-technical-package.png"

COLORS = {
    "paper": "#f3eee5",
    "panel": "#fffaf2",
    "wall": "#c9c0b3",
    "line": "#292824",
    "muted": "#6c675f",
    "walnut": "#57382a",
    "walnut2": "#6c4835",
    "olive": "#62694f",
    "graphite": "#30312e",
    "brass": "#b5945a",
    "socket": "#be4d43",
    "white": "#fffdf8",
}


def font(size, bold=False):
    path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
    return ImageFont.truetype(path, size=size) if Path(path).exists() else ImageFont.load_default()


def centered(draw, box, text, size=20, fill=COLORS["white"], bold=True):
    selected = font(size, bold)
    left, top, right, bottom = box
    bounds = draw.multiline_textbbox((0, 0), text, font=selected, align="center", spacing=3)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    draw.multiline_text(((left + right - width) / 2, (top + bottom - height) / 2), text, font=selected, fill=fill, align="center", spacing=3)


def panel(draw, box, title):
    draw.rounded_rectangle(box, radius=22, fill=COLORS["panel"], outline=COLORS["line"], width=3)
    draw.text((box[0] + 28, box[1] + 22), title, font=font(29, True), fill=COLORS["line"])


def dim_h(draw, x1, x2, y, text):
    draw.line((x1, y, x2, y), fill=COLORS["line"], width=2)
    draw.line((x1 + 13, y - 8, x1, y), fill=COLORS["line"], width=2)
    draw.line((x1 + 13, y + 8, x1, y), fill=COLORS["line"], width=2)
    draw.line((x2 - 13, y - 8, x2, y), fill=COLORS["line"], width=2)
    draw.line((x2 - 13, y + 8, x2, y), fill=COLORS["line"], width=2)
    selected = font(20, True)
    width = draw.textbbox((0, 0), text, font=selected)[2]
    draw.rectangle((x1 + (x2 - x1 - width) / 2 - 8, y - 16, x1 + (x2 - x1 + width) / 2 + 8, y + 16), fill=COLORS["panel"])
    draw.text((x1 + (x2 - x1 - width) / 2, y - 12), text, font=selected, fill=COLORS["line"])


def dim_v(draw, x, y1, y2, text):
    draw.line((x, y1, x, y2), fill=COLORS["line"], width=2)
    draw.line((x - 8, y1 + 13, x, y1), fill=COLORS["line"], width=2)
    draw.line((x + 8, y1 + 13, x, y1), fill=COLORS["line"], width=2)
    draw.line((x - 8, y2 - 13, x, y2), fill=COLORS["line"], width=2)
    draw.line((x + 8, y2 - 13, x, y2), fill=COLORS["line"], width=2)
    draw.text((x + 10, (y1 + y2) / 2 - 10), text, font=font(20, True), fill=COLORS["line"])


def marker(draw, x, y, number):
    radius = 16
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=COLORS["socket"], outline=COLORS["white"], width=3)
    centered(draw, (x - radius, y - radius, x + radius, y + radius), str(number), 17)


with SPEC_PATH.open(encoding="utf-8") as source:
    spec = json.load(source)

image = Image.new("RGB", (2600, 1900), COLORS["paper"])
draw = ImageDraw.Draw(image)
draw.text((90, 42), "Кухня R05 — Г-образная схема, техника и электрика", font=font(44, True), fill=COLORS["line"])
draw.text((92, 96), "Длинное плечо 3570 мм · короткое плечо по стене 1720 мм · потолок 3200 мм", font=font(23), fill=COLORS["muted"])

# Panel 1: top-down plan
plan_box = (70, 145, 1320, 930)
panel(draw, plan_box, "1. План сверху — стена за кухней сохранена")
scale = 0.19
corner_x, corner_y = 260, 300
depth = int(600 * scale)
leg_a = int(3570 * scale)
leg_b = int(1720 * scale)

draw.line((corner_x, corner_y, corner_x + leg_b + 20, corner_y), fill=COLORS["line"], width=18)
draw.line((corner_x, corner_y, corner_x, corner_y + leg_a + 20), fill=COLORS["line"], width=18)
draw.text((corner_x + 110, corner_y - 46), "СТЕНА ЗА КОРОТКИМ ПЛЕЧОМ", font=font(19, True), fill=COLORS["socket"])

# Long leg modules, ordered from facade upward.
long_modules = [
    ("A00", "добор", 60, COLORS["wall"]),
    ("A01", "холодильник", 600, COLORS["walnut"]),
    ("A02", "ящики", 450, COLORS["walnut2"]),
    ("A03", "мойка", 600, COLORS["walnut2"]),
    ("A04", "ПММ", 600, COLORS["walnut2"]),
    ("A05", "варочная", 600, COLORS["olive"]),
    ("A06", "угол", 600, COLORS["walnut"]),
    ("A07", "добор", 60, COLORS["wall"]),
]

cursor_y = corner_y + leg_a
plan_positions = {}
for module_id, name, width_mm, fill in long_modules:
    length = max(7, int(width_mm * scale))
    top = cursor_y - length
    box = (corner_x, top, corner_x + depth, cursor_y)
    draw.rectangle(box, fill=fill, outline=COLORS["line"], width=2)
    plan_positions[module_id] = box
    if width_mm >= 400:
        centered(draw, box, f"{module_id}\n{name}", 15)
    cursor_y = top

return_modules = [
    ("B01", "угол", 600, COLORS["walnut"]),
    ("B02", "духовка\n+ кофе", 600, COLORS["olive"]),
    ("B03", "пенал", 450, COLORS["walnut"]),
    ("B04", "добор", 70, COLORS["wall"]),
]
cursor_x = corner_x
for module_id, name, width_mm, fill in return_modules:
    length = max(7, int(width_mm * scale))
    box = (cursor_x, corner_y, cursor_x + length, corner_y + depth)
    draw.rectangle(box, fill=fill, outline=COLORS["line"], width=2)
    if width_mm >= 400:
        centered(draw, box, f"{module_id}\n{name}", 14)
    cursor_x += length

draw.text((corner_x - 42, corner_y + leg_a + 32), "ФАСАД / ОКНО", font=font(19, True), fill=COLORS["muted"])
draw.text((corner_x + leg_b + 16, corner_y + 42), "К ХОЛЛУ", font=font(19, True), fill=COLORS["muted"])
dim_v(draw, corner_x - 70, corner_y, corner_y + leg_a, "3570")
dim_h(draw, corner_x, corner_x + leg_b, corner_y - 54, "1720")

# Circulation and electrical markers in plan.
marker(draw, plan_positions["A02"][2] + 28, sum(plan_positions["A02"][1::2]) / 2, 2)
marker(draw, plan_positions["A03"][2] + 28, sum(plan_positions["A03"][1::2]) / 2, 3)
marker(draw, plan_positions["A04"][2] + 28, sum(plan_positions["A04"][1::2]) / 2, 4)
marker(draw, plan_positions["A05"][2] + 28, sum(plan_positions["A05"][1::2]) / 2, 5)

draw.text((750, 400), "Кухня занимает угол, а не одну линию.\nВысокая колонна и пенал находятся\nна коротком плече вдоль стены R01/R05.", font=font(25, True), fill=COLORS["line"], spacing=8)
draw.text((750, 540), "Проход в гостиную остаётся открытым.\nХолодильник стоит у фасадного окна,\nкак указано в пожеланиях.", font=font(23), fill=COLORS["muted"], spacing=8)

# Panel 2: elevation A
elev_a = (70, 970, 1660, 1815)
panel(draw, elev_a, "2. Фасад A — длинное плечо 3570 мм")
ex, ey = 140, 1060
sx, sy = 0.36, 0.20
floor_y = ey + int(3200 * sy)
wall_w = int(3570 * sx)
draw.rectangle((ex, ey, ex + wall_w, floor_y), fill=COLORS["wall"], outline=COLORS["line"], width=3)
base_top = floor_y - int(900 * sy)
upper_bottom = floor_y - int(1450 * sy)
upper_top = floor_y - int(2750 * sy)

cursor = ex
for module_id, name, width_mm, fill in long_modules:
    width = max(8, int(width_mm * sx))
    if module_id == "A01":
        box = (cursor, upper_top, cursor + width, floor_y)
        draw.rectangle(box, fill=COLORS["walnut"], outline=COLORS["line"], width=2)
        centered(draw, box, "A01\nХОЛОДИЛЬНИК\n600", 18)
        marker(draw, cursor + width - 22, floor_y - 58, 1)
    elif module_id in {"A00", "A07"}:
        draw.rectangle((cursor, upper_top, cursor + width, floor_y), fill=COLORS["wall"], outline=COLORS["line"], width=1)
    else:
        base = (cursor, base_top, cursor + width, floor_y)
        draw.rectangle(base, fill=fill, outline=COLORS["line"], width=2)
        draw.rectangle((cursor, base_top - 9, cursor + width, base_top), fill=COLORS["graphite"], outline=COLORS["line"], width=1)
        upper = (cursor, upper_top, cursor + width, upper_bottom)
        draw.rectangle(upper, fill=COLORS["olive"] if module_id == "A05" else COLORS["walnut2"], outline=COLORS["line"], width=2)
        draw.rectangle((cursor, upper_bottom, cursor + width, base_top - 9), fill=COLORS["olive"], outline=COLORS["line"], width=1)
        labels = {
            "A02": "ЯЩИКИ\n450",
            "A03": "МОЙКА\n600",
            "A04": "ПММ\n600",
            "A05": "ВАРОЧНАЯ\n600",
            "A06": "УГЛОВАЯ\nБАЗА 600",
        }
        centered(draw, base, f"{module_id}\n{labels[module_id]}", 17)
        if module_id == "A05":
            centered(draw, upper, "ВЫТЯЖКА", 16)
    cursor += width

dim_h(draw, ex, ex + wall_w, floor_y + 54, "3570 мм")
dim_v(draw, ex - 48, ey, floor_y, "3200")
marker(draw, ex + int((60 + 600 + 225) * sx), floor_y - int(1160 * sy), 2)
marker(draw, ex + int((60 + 600 + 450 + 120) * sx), floor_y - 58, 3)
marker(draw, ex + int((60 + 600 + 450 + 600 + 300) * sx), floor_y - int(1160 * sy), 4)
marker(draw, ex + int((60 + 600 + 450 + 600 + 600 + 110) * sx), floor_y - 56, 5)
marker(draw, ex + int((60 + 600 + 450 + 600 + 600 + 300) * sx), floor_y - int(2220 * sy), 6)
marker(draw, ex + int((60 + 600 + 450 + 520) * sx), upper_bottom + 10, 8)

# Panel 3: elevation B
elev_b = (1370, 145, 2530, 930)
panel(draw, elev_b, "3. Фасад B — короткое плечо 1720 мм")
bx, by = 1450, 255
bsx, bsy = 0.50, 0.18
bfloor = by + int(3200 * bsy)
bw = int(1720 * bsx)
draw.rectangle((bx, by, bx + bw, bfloor), fill=COLORS["wall"], outline=COLORS["line"], width=3)
cursor = bx
for module_id, name, width_mm, fill in return_modules:
    width = max(8, int(width_mm * bsx))
    if module_id == "B01":
        base_top_b = bfloor - int(900 * bsy)
        draw.rectangle((cursor, base_top_b, cursor + width, bfloor), fill=COLORS["walnut"], outline=COLORS["line"], width=2)
        draw.rectangle((cursor, by + int(450 * bsy), cursor + width, bfloor - int(1450 * bsy)), fill=COLORS["walnut2"], outline=COLORS["line"], width=2)
        centered(draw, (cursor, base_top_b, cursor + width, bfloor), "B01\nУГОЛ 600", 18)
    elif module_id == "B02":
        draw.rectangle((cursor, by + int(450 * bsy), cursor + width, bfloor), fill=COLORS["walnut"], outline=COLORS["line"], width=2)
        coffee = (cursor + 16, by + int(1050 * bsy), cursor + width - 16, by + int(1750 * bsy))
        oven = (cursor + 16, by + int(1800 * bsy), cursor + width - 16, by + int(2500 * bsy))
        draw.rectangle(coffee, fill=COLORS["olive"], outline=COLORS["brass"], width=3)
        draw.rectangle(oven, fill=COLORS["graphite"], outline=COLORS["brass"], width=3)
        centered(draw, coffee, "СКРЫТАЯ\nКОФЕ-ЗОНА", 17)
        centered(draw, oven, "ДУХОВКА", 18)
        marker(draw, cursor + 28, by + int(1450 * bsy), 7)
    elif module_id == "B03":
        box = (cursor, by + int(450 * bsy), cursor + width, bfloor)
        draw.rectangle(box, fill=COLORS["walnut"], outline=COLORS["line"], width=2)
        centered(draw, box, "B03\nПЕНАЛ\n450", 18)
    else:
        draw.rectangle((cursor, by + int(450 * bsy), cursor + width, bfloor), fill=COLORS["wall"], outline=COLORS["line"], width=1)
    cursor += width

dim_h(draw, bx, bx + bw, bfloor + 48, "1720 мм")
dim_v(draw, bx - 48, by, bfloor, "3200")
draw.text((1450, 865), "Эта стена и поворот обязательны по исходному плану.", font=font(20, True), fill=COLORS["socket"])

# Legend
legend = (1710, 970, 2530, 1815)
panel(draw, legend, "4. Электрические точки")
legend_items = [
    (1, "Холодильник — отдельная доступная точка"),
    (2, "3×230 В над зоной A02"),
    (3, "ПММ — точка в доступном шкафу мойки"),
    (4, "3×230 В над рабочей поверхностью A04"),
    (5, "Силовой вывод варочной панели"),
    (6, "Розетка вытяжки внутри верхнего шкафа"),
    (7, "Раздельные точки духовки и кофемашины"),
    (8, "Драйвер функционального света"),
]
ly = 1055
for number, text in legend_items:
    marker(draw, 1760, ly + 8, number)
    draw.text((1795, ly - 6), text, font=font(18), fill=COLORS["line"])
    ly += 82

draw.multiline_text((1740, 1730), "Предварительная схема. Перед производством нужны\nмодели техники, лазерный обмер и проект электрики.", font=font(18, True), fill=COLORS["socket"], spacing=5)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
image.save(OUTPUT_PATH, quality=96)
print(OUTPUT_PATH)
