# -*- coding: utf-8 -*-
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

CONTENT = {
305: {"materials":"Самим подготовить: деревянный шарик, 2 деревянные палочки, деталь №1, деталь №2, деталь №3, ограничитель.",
"steps":["Сначала соедините деталь №2 и деталь №3, как показано в видео.",
"Вставьте деталь №1 и ограничитель в паз детали №2, как показано в видео.",
"Вставьте обе деревянные палочки по очереди в отверстия деталей №3 и №1, как показано в видео.",
"Положите деревянный шарик между двумя палочками — он скатится вниз. Когда вы постепенно разводите концы палочек друг от друга под определённым углом, шарик сам «взбирается» вверх."],
"principle":"Центр тяжести шарика находится в его центре. Когда палочки расположены параллельно рядом друг с другом, расстояние между центром тяжести шарика и палочками остаётся неизменным, поэтому в горизонтальном положении шарик остаётся неподвижным, а при наклоне палочек скатывается вниз по склону. Когда же палочки разводят под определённым углом, по мере увеличения угла шарик всё сильнее «проваливается» между ними по своей траектории — то есть его центр тяжести опускается всё ниже. Поскольку диаметр шарика достаточно большой, даже у «подножия склона» его центр тяжести оказывается выше, чем у «вершины» (из-за этого проваливания), — так и возникает оптическая иллюзия «подъёма в гору»."},
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
