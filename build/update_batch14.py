# -*- coding: utf-8 -*-
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

CONTENT = {
180: {"materials":"Самим подготовить: фломастеры, вода, пластиковая бутылка с крышкой, лист A4.",
"steps":["Наполните пластиковую бутылку водой доверху, плотно закрутите крышку и вытряхните из воды пузырьки воздуха, постукивая по стенкам.",
"Возьмите четверть листа A4 и нарисуйте фломастером два противоположно направленных стрелки «⇄».",
"Разместите листок за бутылкой с водой и медленно двигайте его — что вы заметили?",
"На другом листе напишите несколько букв, переверните лист и понаблюдайте за ним через бутылку с водой — буквы будут выглядеть расположенными в правильном порядке."],
"principle":"Свет распространяется в разных веществах с разной скоростью, поэтому на границе двух сред его направление меняется — это называется преломлением. Когда свет из воздуха попадает в воду, среда распространения меняется, и происходит преломление. Кроме того, наполненная водой бутылка цилиндрической формы работает как собирающая линза: на определённом расстоянии изображение, которое мы видим через неё, оказывается зеркально перевёрнутым (лево и право меняются местами)."},
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
