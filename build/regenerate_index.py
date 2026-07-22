# -*- coding: utf-8 -*-
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")

with open(os.path.join(SITE, "data.json"), encoding="utf-8") as f:
    data = json.load(f)

def esc(s):
    return html.escape(s or "")

cards = []
done_count = 0
removed_count = 0
total_active = 0
for it in data:
    status = it.get("status", "draft")
    if status == "removed":
        removed_count += 1
        continue
    total_active += 1
    if status == "full":
        done_count += 1
        badge = '<span class="badge ok">готово</span>'
    else:
        badge = ""
    card = f"""<a class="card" href="items/item_{it['id']:03d}.html">
<h3>{esc(it['title_ru'])}</h3>
<span class="zh">{esc(it['title_zh'])}</span>
{badge}
</a>"""
    cards.append(card)

index_tpl = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Научные опыты для детей — русский каталог</title>
<link rel="stylesheet" href="style.css">
</head><body>
<header>
<h1>Научные опыты для детей</h1>
<p>Русскоязычный каталог наборов &middot; {count} опытов</p>
</header>
<div class="container">
<div class="grid" id="grid">
{cards}
</div>
</div>
<footer>Каталог создаётся на основе оригинального китайского сайта. Видео и полные инструкции добавляются постепенно.</footer>
</body></html>
"""

with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_tpl.format(count=total_active, cards="\n".join(cards)))

print("Index regenerated. Active:", total_active, "Done:", done_count, "Removed:", removed_count)
