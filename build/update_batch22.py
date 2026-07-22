# -*- coding: utf-8 -*-
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

CONTENT = {
301: {"materials":"2 мерных стакана, палочка для перемешивания, мерная ложка, самим подготовить: вода, тарелка, сахар, соль.",
"steps":["Возьмите несколько мерных стаканов и налейте в каждый по 50 мл чистой воды.",
"Положите в отдельные стаканы сахар, соль и леденцы, перемешайте.",
"Понаблюдайте за процессом растворения каждого вещества.",
"После растворения поставьте стаканы в морозильную камеру, чтобы содержимое замёрзло в лёд.",
"Достаньте стаканы, выложите лёд на тарелку и понаблюдайте за процессом таяния каждого вида льда."],
"principle":"Переход твёрдого вещества в жидкое под действием тепла называется плавлением (таянием). Обычно, чем выше температура, тем быстрее тает лёд одинакового объёма. Процесс, при котором одно вещество (растворённое вещество) распределяется в другом (растворителе), образуя раствор, называется растворением — например, поваренная соль или сахар, растворяясь в воде, образуют солёный или сладкий раствор. Скорость растворения зависит от свойств вещества, скорости перемешивания и температуры растворителя: мелкие крупинки растворяются быстрее крупных кусков, перемешиваемый раствор — быстрее неперемешиваемого, а тёплый растворитель — быстрее холодного."},

302: {"materials":"Шарик, самим подготовить: медная проволока, скотч, ножницы, насос.",
"steps":["Надуйте шарик насосом и туго завяжите.",
"Если проткнуть шарик проволокой напрямую — он тут же лопнет.",
"Заклейте скотчем два противоположных участка шарика и медленно проткните проволокой именно через эти заклеенные места — шарик, к удивлению, не лопнет!",
"Проткните так несколько шариков подряд — получится красивая «гирлянда», похожая на шашлычок из засахаренных ягод (танхулу)."],
"principle":"Шарик лопается потому, что давление воздуха внутри него выше атмосферного: как только в оболочке появляется повреждение, воздух мгновенно вырывается наружу, разрывая шарик. Когда на шарик наклеивают слой прозрачного скотча, оболочка становится прочнее. При прокалывании проволокой скотч выдерживает давление вырывающегося сжатого воздуха и сохраняет герметичность шарика, поэтому он не лопается мгновенно."},
}

def esc(s):
    return html.escape(s or "")

item_tpl = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_ru} — Научные опыты для детей</title>
<link rel="stylesheet" href="../style.css">
</head><body class="item-page">
<div class="container">
<a class="back-link" href="../index.html">&larr; Ко всему каталогу</a>
<h1>{title_ru}</h1>
<p class="zh-title">Оригинал: {title_zh} &middot; раздел {category} &middot; №{id}</p>

<div class="section-block">
<h2>Видео</h2>
<div class="video-placeholder">Видео добавится позже</div>
</div>

<div class="section-block">
<h2>Материалы</h2>
<p>{materials}</p>
</div>

<div class="section-block">
<h2>Шаги эксперимента</h2>
<ol>
{steps}
</ol>
</div>

<div class="section-block">
<h2>Научный принцип</h2>
<p>{principle}</p>
</div>

</div>
<footer>Каталог научных опытов</footer>
</body></html>
"""

by_id = {it["id"]: it for it in data}
updated = []
for iid, c in CONTENT.items():
    it = by_id[iid]
    steps_html = "\n".join(f"<li>{esc(s)}</li>" for s in c["steps"])
    page = item_tpl.format(
        title_ru=esc(it["title_ru"]), title_zh=esc(it["title_zh"]),
        category=esc(it["category"]), id=it["id"],
        materials=esc(c["materials"]), steps=steps_html, principle=esc(c["principle"]),
    )
    with open(os.path.join(SITE, "items", f"item_{iid:03d}.html"), "w", encoding="utf-8") as f:
        f.write(page)
    it["status"] = "full"
    updated.append(iid)

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated:", updated, len(updated))
