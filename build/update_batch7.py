# -*- coding: utf-8 -*-
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

CONTENT = {
87: {"materials":"Самим подготовить: большой стакан с водой, пустой стакан, лист бумаги.",
"steps":["Скомкайте бумагу в шарик и закрепите на дне пустого стакана, чтобы она не выпала.",
"Переверните стакан вверх дном (донышком с бумагой вверх, горлышком вниз) и вертикально погрузите его в большой стакан с водой так, чтобы уровень воды был выше того места, где закреплена бумага.",
"Вертикально достаньте стакан из воды — бумага внутри останется сухой."],
"principle":"Хотя бумага в перевёрнутом стакане оказывается ниже уровня воды, кроме бумаги в стакане находится ещё и воздух. Когда стакан вертикально погружают в воду, воздух внутри не может выйти наружу и не пускает воду внутрь — так он и защищает бумагу от намокания."},
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

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated: 87")
