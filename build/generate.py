# -*- coding: utf-8 -*-
import re, os, json, html
from translations import TITLES, translate_materials

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "..", "site")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "items"), exist_ok=True)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def parse_section(path, category_label):
    with open(path, encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]
    items = []
    buf = []
    title = None
    for line in lines:
        if DATE_RE.match(line.strip()):
            date = line.strip()
            # first non-empty buffered line before this date, minus the title itself, is details
            details = "".join(buf).strip()
            if title:
                items.append({
                    "category": category_label,
                    "title_zh": title,
                    "details_zh": details,
                    "date": date,
                })
            title = None
            buf = []
        elif line.strip() == "":
            continue
        else:
            if title is None:
                title = line.strip()
            else:
                buf.append(line.strip())
    return items

sections = [
    ("section1.txt", "1-100"),
    ("section2.txt", "101-200"),
    ("section3.txt", "201-300"),
    ("section4.txt", "301-368"),
]

all_items = []
for fname, cat in sections:
    all_items.extend(parse_section(os.path.join(BASE, fname), cat))

# assign global ids
missing_titles = []
for i, it in enumerate(all_items, start=1):
    it["id"] = i
    zh = it["title_zh"]
    ru = TITLES.get(zh)
    if not ru:
        missing_titles.append(zh)
        ru = zh  # fallback: keep chinese, mark for manual translation
        it["needs_translation"] = True
    else:
        it["needs_translation"] = False
    it["title_ru"] = ru
    it["materials_hint_ru"] = translate_materials(it["details_zh"])

print(f"Total items parsed: {len(all_items)}")
print(f"Missing translations: {len(missing_titles)}")
if missing_titles:
    for t in missing_titles:
        print("  MISSING:", t)

# Save raw data as JSON for future incremental updates
with open(os.path.join(OUT, "data.json"), "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)

CSS = """
:root{--bg:#f6f8fb;--card:#ffffff;--accent:#2f8fdd;--accent2:#37b6a3;--text:#1f2937;--muted:#6b7280;--border:#e5e7eb;}
*{box-sizing:border-box;}
body{margin:0;font-family:'Segoe UI',Arial,sans-serif;background:var(--bg);color:var(--text);}
header{background:linear-gradient(135deg,#2f8fdd,#37b6a3);color:#fff;padding:32px 20px;text-align:center;}
header h1{margin:0 0 8px;font-size:28px;}
header p{margin:0;opacity:.9;}
.container{max-width:1100px;margin:0 auto;padding:24px 16px 60px;}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0;justify-content:center;}
.filters button{border:1px solid var(--border);background:#fff;padding:8px 16px;border-radius:20px;cursor:pointer;font-size:14px;color:var(--text);}
.filters button.active{background:var(--accent);color:#fff;border-color:var(--accent);}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px;text-decoration:none;color:var(--text);transition:.15s;display:flex;flex-direction:column;gap:6px;}
.card:hover{box-shadow:0 6px 18px rgba(0,0,0,.08);transform:translateY(-2px);}
.card .num{font-size:12px;color:var(--muted);}
.card h3{margin:0;font-size:17px;line-height:1.3;}
.card .zh{font-size:13px;color:var(--muted);}
.badge{display:inline-block;font-size:11px;padding:2px 8px;border-radius:10px;background:#fde68a;color:#92400e;width:fit-content;}
.badge.ok{background:#d1fae5;color:#065f46;}
.top-actions{text-align:center;margin:20px 0;}
.top-actions a{color:var(--accent);text-decoration:none;font-size:14px;}
.item-page .container{max-width:760px;}
.item-page h1{font-size:26px;margin-bottom:4px;}
.item-page .zh-title{color:var(--muted);margin-top:0;}
.section-block{background:#fff;border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:16px;}
.section-block h2{margin-top:0;font-size:16px;color:var(--accent);}
.video-placeholder{aspect-ratio:16/9;background:#eef2f7;border:2px dashed var(--border);border-radius:10px;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:14px;text-align:center;padding:20px;}
.back-link{display:inline-block;margin-bottom:16px;color:var(--accent);text-decoration:none;font-size:14px;}
.pending{color:#92400e;background:#fffbeb;border:1px solid #fde68a;padding:10px 14px;border-radius:8px;font-size:14px;}
footer{text-align:center;color:var(--muted);font-size:13px;padding:30px 16px;}
"""

with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as f:
    f.write(CSS)

def esc(s):
    return html.escape(s or "")

# ---------- item pages ----------
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
{materials_block}
</div>

<div class="section-block">
<h2>Шаги эксперимента</h2>
<p class="pending">Полный текст шагов ещё не добавлен. Он появится здесь после того, как будет скопирован из
оригинальной статьи и переведён.</p>
</div>

</div>
<footer>Каталог научных опытов &middot; черновая версия</footer>
</body></html>
"""

def materials_block(it):
    parts = []
    if it["materials_hint_ru"]:
        parts.append(f'<p><b>Похоже, встречаются:</b> {esc(it["materials_hint_ru"])}</p>')
    parts.append(f'<p style="color:#6b7280;font-size:14px;">Оригинал (кит., отрывок): {esc(it["details_zh"])}</p>')
    parts.append('<p class="pending">Полный список материалов будет уточнён по мере добавления полного текста статьи.</p>')
    return "\n".join(parts)

for it in all_items:
    page = item_tpl.format(
        title_ru=esc(it["title_ru"]),
        title_zh=esc(it["title_zh"]),
        category=esc(it["category"]),
        id=it["id"],
        materials_block=materials_block(it),
    )
    with open(os.path.join(OUT, "items", f"item_{it['id']:03d}.html"), "w", encoding="utf-8") as f:
        f.write(page)

# ---------- index page ----------
cats = ["1-100", "101-200", "201-300", "301-368"]
cards_by_cat = {c: [] for c in cats}
for it in all_items:
    badge = '<span class="badge">название требует проверки</span>' if it["needs_translation"] else ""
    card = f"""<a class="card" data-cat="{esc(it['category'])}" href="items/item_{it['id']:03d}.html">
<span class="num">№{it['id']}</span>
<h3>{esc(it['title_ru'])}</h3>
<span class="zh">{esc(it['title_zh'])}</span>
{badge}
</a>"""
    cards_by_cat[it["category"]].append(card)

all_cards = []
for c in cats:
    all_cards.extend(cards_by_cat[c])

index_tpl = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Научные опыты для детей — русский каталог</title>
<link rel="stylesheet" href="style.css">
</head><body>
<header>
<h1>Научные опыты для детей</h1>
<p>Русскоязычный каталог наборов &middot; {count} позиций</p>
</header>
<div class="container">
<div class="filters" id="filters">
<button class="active" data-filter="all">Все ({count})</button>
{filter_buttons}
</div>
<div class="grid" id="grid">
{cards}
</div>
</div>
<footer>Каталог создаётся на основе оригинального китайского сайта. Видео и полные инструкции добавляются постепенно.</footer>
<script>
const buttons = document.querySelectorAll('#filters button');
const cards = document.querySelectorAll('#grid .card');
buttons.forEach(b => b.addEventListener('click', () => {{
  buttons.forEach(x => x.classList.remove('active'));
  b.classList.add('active');
  const f = b.dataset.filter;
  cards.forEach(c => {{
    c.style.display = (f === 'all' || c.dataset.cat === f) ? '' : 'none';
  }});
}}));
</script>
</body></html>
"""

filter_buttons = "\n".join(
    f'<button data-filter="{c}">{c} ({len(cards_by_cat[c])})</button>' for c in cats
)

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_tpl.format(count=len(all_items), filter_buttons=filter_buttons, cards="\n".join(all_cards)))

print("Site generated at", OUT)
