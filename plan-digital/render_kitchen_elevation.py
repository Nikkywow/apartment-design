from pathlib import Path
import json

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "plan-digital" / "plan-model.json"
OUTPUT_PATH = ROOT / "design-visuals" / "16-kitchen-technical-elevation.png"

CANVAS = (2400, 1800)
WALL_ORIGIN = (260, 110)
SCALE_X = 0.46
SCALE_Y = 0.42

COLORS = {
    "paper": "#f3eee5",
    "wall": "#d7cec0",
    "line": "#292824",
    "muted": "#6c675f",
    "walnut": "#553729",
    "walnut_light": "#6a4634",
    "olive": "#596047",
    "graphite": "#2f302d",
    "brass": "#b4945a",
    "glass": "#b9c7c4",
    "socket": "#b8493f",
    "white": "#fffdf8",
}


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def mm_x(value):
    return int(round(value * SCALE_X))


def mm_y(value):
    return int(round(value * SCALE_Y))


def label_center(draw, box, text, size=22, fill=COLORS["white"], bold=False):
    selected_font = font(size, bold)
    left, top, right, bottom = box
    text_box = draw.multiline_textbbox((0, 0), text, font=selected_font, align="center", spacing=4)
    width = text_box[2] - text_box[0]
    height = text_box[3] - text_box[1]
    draw.multiline_text(
        ((left + right - width) / 2, (top + bottom - height) / 2),
        text,
        font=selected_font,
        fill=fill,
        align="center",
        spacing=4,
    )


def dimension(draw, start, end, text, offset=0, vertical=False):
    dim_font = font(22, True)
    if vertical:
        x = start[0] + offset
        y1, y2 = start[1], end[1]
        draw.line((x, y1, x, y2), fill=COLORS["line"], width=2)
        draw.line((x - 9, y1 + 14, x, y1), fill=COLORS["line"], width=2)
        draw.line((x + 9, y1 + 14, x, y1), fill=COLORS["line"], width=2)
        draw.line((x - 9, y2 - 14, x, y2), fill=COLORS["line"], width=2)
        draw.line((x + 9, y2 - 14, x, y2), fill=COLORS["line"], width=2)
        draw.text((x + 12, (y1 + y2) / 2 - 12), text, font=dim_font, fill=COLORS["line"])
    else:
        y = start[1] + offset
        x1, x2 = start[0], end[0]
        draw.line((x1, y, x2, y), fill=COLORS["line"], width=2)
        draw.line((x1 + 14, y - 9, x1, y), fill=COLORS["line"], width=2)
        draw.line((x1 + 14, y + 9, x1, y), fill=COLORS["line"], width=2)
        draw.line((x2 - 14, y - 9, x2, y), fill=COLORS["line"], width=2)
        draw.line((x2 - 14, y + 9, x2, y), fill=COLORS["line"], width=2)
        text_box = draw.textbbox((0, 0), text, font=dim_font)
        width = text_box[2] - text_box[0]
        draw.rectangle((x1 + (x2 - x1 - width) / 2 - 8, y - 18, x1 + (x2 - x1 + width) / 2 + 8, y + 18), fill=COLORS["paper"])
        draw.text((x1 + (x2 - x1 - width) / 2, y - 13), text, font=dim_font, fill=COLORS["line"])


def socket_marker(draw, x, y, number):
    radius = 18
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=COLORS["socket"], outline=COLORS["white"], width=3)
    marker_font = font(19, True)
    text_box = draw.textbbox((0, 0), str(number), font=marker_font)
    draw.text((x - (text_box[2] - text_box[0]) / 2, y - 12), str(number), font=marker_font, fill=COLORS["white"])


with MODEL_PATH.open(encoding="utf-8") as source:
    model = json.load(source)

wall_length = next(wall["length_m"] for wall in model["walls"] if wall["id"] == "W_R05_LEFT_KITCHEN")
ceiling_height = model["global"]["ceiling_height_m"]["value"]

image = Image.new("RGB", CANVAS, COLORS["paper"])
draw = ImageDraw.Draw(image)

title_font = font(42, True)
subtitle_font = font(22)
draw.text((260, 24), "Кухня — техническая развёртка", font=title_font, fill=COLORS["line"])
draw.text(
    (260, 74),
    "Стена R05: 3570 мм · потолок 3200 мм · слева фасадное окно, справа прихожая",
    font=subtitle_font,
    fill=COLORS["muted"],
)

wall_x, wall_y = WALL_ORIGIN
wall_w = mm_x(wall_length * 1000)
wall_h = mm_y(ceiling_height * 1000)
floor_y = wall_y + wall_h

draw.rectangle((wall_x, wall_y, wall_x + wall_w, floor_y), fill=COLORS["wall"], outline=COLORS["line"], width=4)
draw.line((wall_x - 40, floor_y, wall_x + wall_w + 40, floor_y), fill=COLORS["line"], width=5)

modules = [
    ("добор", 60),
    ("холодильник", 600),
    ("ящики", 450),
    ("мойка", 600),
    ("ПММ", 600),
    ("варочная", 600),
    ("колонна", 600),
    ("добор", 60),
]

base_top = floor_y - mm_y(900)
upper_bottom = floor_y - mm_y(1450)
upper_top = floor_y - mm_y(2750)
tall_top = upper_top
worktop_h = max(10, mm_y(22))

cursor = wall_x
module_boxes = {}
for name, width_mm in modules:
    width = mm_x(width_mm)
    module_boxes[name if name not in module_boxes else f"{name}-2"] = (cursor, width)
    if name == "холодильник":
        box = (cursor, tall_top, cursor + width, floor_y)
        draw.rectangle(box, fill=COLORS["walnut"], outline=COLORS["line"], width=3)
        draw.line((cursor, tall_top + (floor_y - tall_top) * .55, cursor + width, tall_top + (floor_y - tall_top) * .55), fill=COLORS["line"], width=2)
        label_center(draw, box, "ВСТРОЕННЫЙ\nХОЛОДИЛЬНИК\n600", 24, bold=True)
    elif name == "колонна":
        box = (cursor, tall_top, cursor + width, floor_y)
        draw.rectangle(box, fill=COLORS["walnut"], outline=COLORS["line"], width=3)
        drawer_top = floor_y - mm_y(380)
        oven_top = floor_y - mm_y(1120)
        coffee_top = floor_y - mm_y(1760)
        draw.line((cursor, drawer_top, cursor + width, drawer_top), fill=COLORS["line"], width=3)
        draw.rectangle((cursor + 18, oven_top, cursor + width - 18, drawer_top - 18), fill=COLORS["graphite"], outline=COLORS["brass"], width=3)
        label_center(draw, (cursor + 18, oven_top, cursor + width - 18, drawer_top - 18), "ДУХОВКА", 21, bold=True)
        draw.rectangle((cursor + 18, coffee_top, cursor + width - 18, oven_top - 18), fill=COLORS["olive"], outline=COLORS["brass"], width=3)
        label_center(draw, (cursor + 18, coffee_top, cursor + width - 18, oven_top - 18), "СКРЫТАЯ\nКОФЕ-ЗОНА", 20, bold=True)
        label_center(draw, (cursor, tall_top, cursor + width, coffee_top), "ХРАНЕНИЕ", 18)
        label_center(draw, (cursor, drawer_top, cursor + width, floor_y), "ЯЩИКИ", 18)
    elif name == "добор":
        draw.rectangle((cursor, tall_top, cursor + width, floor_y), fill=COLORS["walnut_light"], outline=COLORS["line"], width=2)
    else:
        base_box = (cursor, base_top, cursor + width, floor_y)
        draw.rectangle(base_box, fill=COLORS["walnut"], outline=COLORS["line"], width=3)
        draw.rectangle((cursor, base_top - worktop_h, cursor + width, base_top), fill=COLORS["graphite"], outline=COLORS["line"], width=2)
        if name == "ПММ":
            label_center(draw, base_box, "ВСТРОЕННАЯ\nПОСУДОМОЙКА\n600", 22, bold=True)
        elif name == "мойка":
            sink_left = cursor + width * .2
            sink_right = cursor + width * .8
            draw.rounded_rectangle((sink_left, base_top - 18, sink_right, base_top + 30), radius=12, fill=COLORS["graphite"], outline=COLORS["brass"], width=3)
            draw.arc((cursor + width * .45, base_top - 105, cursor + width * .72, base_top + 20), 160, 350, fill=COLORS["brass"], width=5)
            label_center(draw, base_box, "МОЙКА\n600", 22, bold=True)
        elif name == "варочная":
            draw.rounded_rectangle((cursor + 16, base_top - 23, cursor + width - 16, base_top + 2), radius=8, fill="#111211")
            label_center(draw, base_box, "ЯЩИКИ\nПОД ВАРОЧНОЙ\n600", 21, bold=True)
        else:
            draw.line((cursor, base_top + (floor_y - base_top) / 2, cursor + width, base_top + (floor_y - base_top) / 2), fill=COLORS["line"], width=2)
            label_center(draw, base_box, "РАБОЧИЕ\nЯЩИКИ\n450", 21, bold=True)

        upper_box = (cursor, upper_top, cursor + width, upper_bottom)
        upper_fill = COLORS["walnut_light"]
        if name == "варочная":
            upper_fill = COLORS["olive"]
        draw.rectangle(upper_box, fill=upper_fill, outline=COLORS["line"], width=3)
        if name == "варочная":
            label_center(draw, upper_box, "ВСТРОЕННАЯ\nВЫТЯЖКА", 20, bold=True)
        else:
            draw.line((cursor + width / 2, upper_top, cursor + width / 2, upper_bottom), fill=COLORS["line"], width=2)
            label_center(draw, upper_box, "ВЕРХНЕЕ\nХРАНЕНИЕ", 18, bold=True)

        draw.rectangle((cursor, upper_bottom, cursor + width, base_top - worktop_h), fill=COLORS["olive"], outline=COLORS["line"], width=2)
        for tile_x in range(int(cursor), int(cursor + width), 26):
            draw.line((tile_x, upper_bottom, tile_x, base_top - worktop_h), fill="#7b8068", width=1)
        draw.line((cursor, upper_bottom + 8, cursor + width, upper_bottom + 8), fill=COLORS["brass"], width=3)
    cursor += width

dimension(draw, (wall_x, floor_y), (wall_x + wall_w, floor_y), "3570 мм", offset=92)
cursor = wall_x
for name, width_mm in modules:
    width = mm_x(width_mm)
    if width_mm >= 400:
        dimension(draw, (cursor, floor_y), (cursor + width, floor_y), f"{width_mm}", offset=48)
    cursor += width
dimension(draw, (wall_x, wall_y), (wall_x, floor_y), "3200 мм", offset=-72, vertical=True)
dimension(draw, (wall_x + wall_w, base_top), (wall_x + wall_w, floor_y), "900", offset=54, vertical=True)
dimension(draw, (wall_x + wall_w, upper_bottom), (wall_x + wall_w, base_top), "550", offset=108, vertical=True)

fridge_x = module_boxes["холодильник"][0]
drawers_x = module_boxes["ящики"][0]
sink_x = module_boxes["мойка"][0]
dishwasher_x = module_boxes["ПММ"][0]
hob_x = module_boxes["варочная"][0]
column_x = module_boxes["колонна"][0]

socket_marker(draw, drawers_x + mm_x(70), floor_y - mm_y(300), 1)
socket_marker(draw, drawers_x + mm_x(220), floor_y - mm_y(1160), 2)
socket_marker(draw, sink_x + mm_x(120), floor_y - mm_y(300), 3)
socket_marker(draw, dishwasher_x + mm_x(300), floor_y - mm_y(1160), 4)
socket_marker(draw, hob_x + mm_x(110), floor_y - mm_y(280), 5)
socket_marker(draw, hob_x + mm_x(300), floor_y - mm_y(2240), 6)
socket_marker(draw, column_x + mm_x(75), floor_y - mm_y(1450), 7)
socket_marker(draw, sink_x + mm_x(500), upper_bottom + 16, 8)

legend_x = 1980
draw.rounded_rectangle((legend_x, 230, 2345, 1240), radius=24, fill="#fffaf1", outline=COLORS["line"], width=3)
draw.text((legend_x + 28, 260), "УСЛОВНЫЕ ОБОЗНАЧЕНИЯ", font=font(24, True), fill=COLORS["line"])

legend_items = [
    ("1", "Холодильник: отдельная точка,\nне за корпусом техники"),
    ("2", "Три розетки над столешницей"),
    ("3", "Посудомойка: отдельная точка\nв доступном шкафу мойки"),
    ("4", "Три розетки рабочей зоны"),
    ("5", "Силовой вывод варочной панели"),
    ("6", "Розетка вытяжки внутри шкафа"),
    ("7", "Раздельные точки духовки и кофе"),
    ("8", "Драйвер скрытого рабочего света"),
]

legend_y = 330
for number, description in legend_items:
    draw.ellipse((legend_x + 28, legend_y - 4, legend_x + 64, legend_y + 32), fill=COLORS["socket"])
    label_center(draw, (legend_x + 28, legend_y - 4, legend_x + 64, legend_y + 32), number, 18, bold=True)
    draw.multiline_text((legend_x + 82, legend_y - 3), description, font=font(17), fill=COLORS["line"], spacing=4)
    legend_y += 105

draw.text((legend_x + 28, 1180), "Высоты уточняются после выбора\nконкретной техники и чистового пола.", font=font(17, True), fill=COLORS["socket"], spacing=4)

draw.rounded_rectangle((260, 1585, 2345, 1740), radius=18, fill="#e4ddd1", outline=COLORS["muted"], width=2)
draw.multiline_text(
    (290, 1615),
    "Важно: посудомойка остаётся под столешницей рядом с мойкой. Духовка и скрытая кофейная зона находятся\n"
    "в отдельной колонне. Розетки стационарной техники вынесены в доступные соседние зоны, а не за корпуса.",
    font=font(21, True),
    fill=COLORS["line"],
    spacing=6,
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
image.save(OUTPUT_PATH, quality=96)
print(OUTPUT_PATH)
