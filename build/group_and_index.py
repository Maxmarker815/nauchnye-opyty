# -*- coding: utf-8 -*-
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

def esc(s):
    return html.escape(s or "")

# Тематические группы: (название, [id опытов в нужном порядке])
GROUPS = [
    ("Цвет, радуга и расслоение жидкостей",
     [3, 4, 7, 14, 30, 127, 55, 79, 12, 60, 54, 175, 212]),
    ("Химические реакции: вулканы, газировка, кислоты",
     [13, 160, 37, 61, 281, 132, 5, 143, 82, 45, 52, 248]),
    ("Масло, вода, плотность и плавучесть",
     [17, 47, 154, 258, 39]),
    ("Опыты с яйцами",
     [15, 40, 19, 148, 109, 204]),
    ("Воздушные шарики",
     [10, 22, 157, 174, 103, 106, 94, 233, 182, 136, 104]),
    ("Шарики для пинг-понга",
     [16, 74, 131, 210, 96]),
    ("Мыльные пузыри",
     [141, 162]),
    ("Вода: поверхностное натяжение и атмосферное давление",
     [34, 138, 100, 18, 134, 87, 178, 181, 92, 77, 68, 97, 149, 252, 222]),
    ("Свечи",
     [6, 102, 107]),
    ("Стаканы, банки и бутылки",
     [36, 38, 117, 120, 257, 272, 186]),
    ("Баланс, центр тяжести и инерция",
     [89, 59, 112, 95, 41, 62, 224, 139, 251]),
    ("Статическое электричество",
     [110, 246, 111, 288, 266]),
    ("Звук",
     [48, 72, 216, 144]),
    ("Свет, зрение и оптические иллюзии",
     [56, 35, 161, 172, 145, 215, 293, 164]),
    ("Бумага: складывание, резка, конструкции",
     [108, 163, 155, 90, 142, 195, 105]),
    ("Температура, тепло и лёд",
     [28, 91, 261]),
    ("Механика и разное",
     [51, 64, 93, 115, 247, 255, 290]),
]

by_id = {it["id"]: it for it in data}

# Проверка: все активные позиции распределены ровно один раз
active_ids = {it["id"] for it in data if it.get("status") == "full"}
grouped_ids = [iid for _, ids in GROUPS for iid in ids]
assert len(grouped_ids) == len(set(grouped_ids)), "Дубликаты в группах!"
missing = active_ids - set(grouped_ids)
extra = set(grouped_ids) - active_ids
assert not missing, f"Не распределены: {missing}"
assert not extra, f"Лишние id: {extra}"

# Проставим порядок в data.json
order = 0
for _, ids in GROUPS:
    for iid in ids:
        by_id[iid]["order"] = order
        order += 1
with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = len(grouped_ids)

sections_html = []
for gname, ids in GROUPS:
    cards = []
    for iid in ids:
        it = by_id[iid]
        search_key = esc(it['title_ru'].lower())
        cards.append(f"""<a class="card" href="items/item_{iid:03d}.html" data-search="{search_key}">
<h3>{esc(it['title_ru'])}</h3>
<span class="badge ok">готово</span>
</a>""")
    sections_html.append(
        f'<section class="group">\n'
        f'<h2 class="group-title">{esc(gname)} <span class="group-count">({len(ids)})</span></h2>\n'
        f'<div class="grid">\n' + "\n".join(cards) + "\n</div>\n</section>"
    )

index_tpl = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Научные опыты для детей — русский каталог</title>
<link rel="stylesheet" href="style.css">
</head><body>
<header>
<h1>Научные опыты для детей</h1>
<p>Русскоязычный каталог наборов &middot; {count} опытов, сгруппированы по темам</p>
</header>
<div class="searchbar">
<div class="search-wrap">
<span class="search-icon">&#128269;</span>
<input type="search" id="search" placeholder="Поиск опыта по названию..." autocomplete="off">
<button type="button" id="search-clear" aria-label="Очистить">&times;</button>
</div>
</div>
<div class="container">
{sections}
<p id="no-results" class="no-results" hidden>Ничего не найдено</p>
</div>
<footer>Каталог создаётся на основе оригинального китайского сайта. Видео и полные инструкции добавляются постепенно.</footer>
<script>
(function(){{
  var input=document.getElementById('search');
  var clearBtn=document.getElementById('search-clear');
  var cards=Array.prototype.slice.call(document.querySelectorAll('.card'));
  var groups=Array.prototype.slice.call(document.querySelectorAll('.group'));
  var noRes=document.getElementById('no-results');
  function apply(){{
    var q=input.value.trim().toLowerCase();
    clearBtn.style.display=q?'block':'none';
    var anyVisible=false;
    cards.forEach(function(c){{
      var match=!q||c.getAttribute('data-search').indexOf(q)!==-1;
      c.style.display=match?'':'none';
      if(match)anyVisible=true;
    }});
    groups.forEach(function(g){{
      var vis=g.querySelectorAll('.card:not([style*="display: none"])').length>0;
      g.style.display=vis?'':'none';
    }});
    noRes.hidden=anyVisible;
  }}
  input.addEventListener('input',apply);
  clearBtn.addEventListener('click',function(){{input.value='';apply();input.focus();}});
}})();
</script>
</body></html>
"""

with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_tpl.format(count=total, sections="\n\n".join(sections_html)))

print("Index regenerated. Total:", total, "Groups:", len(GROUPS))
