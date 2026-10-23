# Кухня — warm organic modern, вариант 36

Дата: 22 октября 2026 года.
Режим: встроенный image_gen, генерация с референсами и последующее уточнение фасадов.
Итог: ../design-visuals/36-kitchen-warm-organic-modern.png

## Основа

- Обмерный план: ../updated-measured-plan-rotated.jpeg.
- Программа кухни: kitchen-spec.json, версия 2.1.
- Существующая размерная модель: kitchen-3d.html, указанная в kitchen-spec.json.
- Изображение 25 использовано как вспомогательный композиционный референс.
- 20,5 м² — кухня-гостиная в квартире общей площадью 52 м².
- Рабочая схема: длинная ветвь 3570 мм, короткая 1720 мм, потолок 3200 мм.
- Камера: из гостиной со стороны нижней правой части плана к верхнему левому кухонному углу; фасадная стена слева в кадре, колонны на коротком возврате справа.

## Проверка результата

- Сохранилась Г-образная композиция с читаемым перпендикулярным возвратом.
- У фасадной стороны — высокий холодильный пенал с отдельным нижним фасадом морозильной камеры.
- На длинном плече видны мойка, рабочая поверхность и индукционная зона.
- Духовка и отдельная СВЧ находятся в высокой колонне на коротком плече.
- Кофе-ниша показана открытой; верхнее и нижнее хранение закрыто, предусмотрены задвигаемые фасады.
- В кадре круглый стол и четыре кресла-стула, два частично обрезаны границами изображения.
- Фасады гладкие ореховые, фартук оливковый, столешница графитовая, детали латунные.
- Один существующий фасадный проём показан частично, второй вне кадра. Новых окон и балкона не добавлено.
- Визуализация концептуальная: она передаёт композицию, материалы и свет. Точные размеры мебели, открывания и проходы не подтверждаются генеративным изображением.

## Основной prompt

Use case: sketch-to-render / photorealistic-natural.
Create ONE premium photorealistic architectural interior image, landscape aspect ratio 16:10, of the user's actual L-shaped kitchen within a 20.5 m² kitchen-living room in a 52 m² apartment. This is a carefully proportioned compact residential interior, not a large villa.

REFERENCE ROLES:
Image 1, updated-measured-plan-rotated.jpeg: authoritative apartment plan for wall orientation and openings. The kitchen-living room is the bottom-left room marked 20.5. Keep the existing L at the plan-left wall and plan-top-left return. Do not mirror the plan.
Image 2, 25-kitchen-measured-plan-render.png: supporting reference for the camera direction, placement of integrated equipment and overall composition ONLY. Replace its framed/Victorian cabinetry with refined organic modern flat walnut fronts. Do not copy extra decorative cabinet framing, thick cornices or excess countertop length on the short return. The dimensioned specification below governs geometry.

LOCKED SPATIAL SPECIFICATION:
Room working maximum dimensions 5900 mm along the facade by 3570 mm deep, ceiling height 3200 mm. Long kitchen wall 3570 mm, perpendicular short return wall 1720 mm. Both arms attach to continuous solid walls; no island or peninsula. Full-depth base and tall cabinets 600 mm, stone worktop depth 620 mm at 900 mm high; upper cabinets visibly shallower, 350 mm. Tall fronts top at 2750 mm with cream wall above.
Along the LONG wall, starting at the facade end and proceeding toward the internal L corner: 60 mm filler; 600 mm integrated refrigerator with a SEPARATE LOWER FREEZER behind two vertically stacked matching walnut doors; 450 mm drawer/landing unit; 600 mm sink cabinet; 600 mm fully integrated dishwasher with clear preparation counter above; 600 mm induction hob above drawers with a concealed hood in the upper cabinet; 600 mm blind corner; 60 mm corner filler. Total 3570 mm. Sink and hob are separate, with the 600 mm preparation surface between them.
Along the SHORT RETURN, from the same internal corner toward the hall: 600 mm shared corner overlap; ONE 600 mm tall column with a real separate built-in microwave immediately above an ergonomic oven; ONE narrower 450 mm breakfast/coffee pantry; 70 mm filler. Total 1720 mm. The two appliance/pantry columns belong to the PERPENDICULAR return plane, not to the long wall. No extra base modules between the shared corner and the oven column. The corner is continuous and usable, not an empty gap.
The coffee pantry is a closable pocket-door appliance garage, shown open only in its middle niche to reveal a compact coffee machine and cups, with closed walnut storage above and below. Subtle internal warm light. No full-height open shelving.
Dining: a physically plausible 1100 mm DIAMETER ROUND walnut table with exactly FOUR compact upholstered dining chairs, placed on the facade/dining side, offset from the kitchen working aisle; retain usable circulation, do not overlap chairs or cabinets. Show all four distinct chairs legibly, allowing natural partial occlusion. Avoid enormous table or overlarge armchairs. A small partial view of the olive living-room sofa at the far foreground edge is acceptable only if it fits.
Openings: existing glazed openings are on the FACADE wall PERPENDICULAR to the long kitchen wall, not behind the cooktop. The room has TWO facade glazed openings in total, 1490 and 2190 mm wide. Frame the view so only a cropped portion of the nearer existing opening and cream linen curtain appears at the FAR LEFT edge; its sill and lower threshold are outside the crop, as their heights are not known. The second facade opening is outside the frame. No invented balcony, terrace, railing, extra window, added doorway or relocated opening. Hall access is beyond the end of the short return, at frame right, and may be cropped out.

COMPOSITION AND CAMERA:
A single eye-level architectural photograph looking obliquely from the living area on the plan-bottom-right side toward the plan-left/plan-top-left kitchen corner. In the IMAGE the facade/daylight edge and fridge are LEFT, the long sink/prep/hob run spans the middle and the short perpendicular oven/coffee return is RIGHT. Show the L corner clearly. Moderate 28–32 mm full-frame lens, corrected verticals, realistic perspective without stretching; camera height around 1500 mm. Pull back enough for the round dining table and four chairs while keeping the kitchen readable. Restrained depth of field, only nearest edges gently soft, architecture and cabinetry sharp.

DESIGN / MATERIALS:
Warm organic modern, sophisticated moody mid-century influence, refined minimalism, cozy elegant premium residential atmosphere. Dark chocolate walnut cabinetry with beautiful authentic natural vertical wood grain, flat slab fronts and clean aligned seams, understated small aged-brass hardware. Muted olive green vertical ceramic tile backsplash with subtle handmade variation, honed graphite stone countertop, warm cream softly textured walls, warm ivory plain ceiling, elegant warm natural timber floor with quiet grain. NO ornate cornices, shaker frames, Victorian mouldings or rustic cottage styling.
Soft natural daylight from the existing facade opening blended with warm 2700K practical lighting, concealed continuous under-cabinet task light, restrained ambient glow and a modest warm dining pendant. Cream chair upholstery and tactile linen soften the walnut and graphite. Premium matte and satin materials with realistic microtexture and restrained reflections, believable contact shadows. Polished but relaxed, intimate, warm, expensive, high detail. Only restrained functional styling, no clutter, no people.

DELIVERABLE:
One seamless full-frame realistic interior photograph, not a collage, not a drawing. No text, no dimensions, no UI, no logo or watermark. Prioritize credible compact room proportions, the specified two perpendicular arms and equipment over decorative additions.

## Финальная правка

Use case: precise-object-edit. Edit ONLY cabinetry front styling in the supplied kitchen photograph. Preserve the complete composition, camera, exact L-shaped cabinet footprints, room proportions, ceiling, table and exactly four chairs, appliance positions, fridge/freezer two-door split, olive tile backsplash, graphite countertop, pendant, soft daylight and 2700K task lighting, flooring and sofa unchanged. Preserve 16:10 landscape framing.

Replace ALL framed / recessed-panel / shaker cabinet door and drawer fronts with true FLAT SLAB dark chocolate walnut veneer fronts: smooth unbroken face planes, finely matched natural vertical grain, precise minimal reveals, no picture-frame rails, no raised perimeter, no applied mouldings. Include fridge and freezer fronts, base units, wall units, oven-column storage and the coffee pantry. Keep understated small aged-brass pulls. Refined premium organic modern with subtle mid-century influence, warm and cozy.

In the existing narrow coffee pantry at far right, replace ONLY its open upper display shelves with closed FLAT walnut doors aligned with the neighboring microwave/oven-column storage, and keep its lower storage closed too. Retain a single central coffee-machine niche at normal work height with recessed pocket doors visibly stowed to the sides and concealed warm lighting: a closable, integrated hidden coffee station, not a full-height display bookshelf. The coffee machine and one cup remain visible. Do not widen or move the pantry. Keep the natural photographic realism, materials and all other surfaces unchanged. No text or watermarks.

