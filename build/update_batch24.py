# -*- coding: utf-8 -*-
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

CONTENT = {
303: {"materials":"Самим подготовить: бумажный цилиндр (гильза).",
"steps":["Подготовьте лёгкий и достаточно упругий бумажный цилиндр, а также гладкую поверхность стола.",
"Поднимите цилиндр вертикально над столом и отпустите пальцы — после нескольких попыток цилиндр всякий раз падает набок.",
"Поверните цилиндр на 90°, чтобы он лежал горизонтально относительно стола, поднимите на определённую высоту и отпустите в свободном падении — на этот раз цилиндр встаёт вертикально."],
"principle":"Способность цилиндра «вставать» объясняется физическим явлением отскока: падающий цилиндр не может опуститься абсолютно вертикально, поэтому одна из его сторон касается стола первой. Возникающая от этого касания сила отскока толкает цилиндр в противоположном направлении; эта сила в сочетании с силой тяжести создаёт суммарную силу, из-за которой цилиндр движется по параболической траектории с вращением. При правильно подобранной высоте падения сила отскока как раз успевает подбросить цилиндр и повернуть его на 90°, прежде чем он коснётся стола, — поэтому цилиндр, упавший горизонтально, встаёт вертикально."},
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
