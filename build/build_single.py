# -*- coding: utf-8 -*-
import json, os, re, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
OUT = os.path.join(BASE, "..", "katalog_odin_fajl.html")

with open(os.path.join(SITE, "data.json"), encoding="utf-8") as f:
    data = json.load(f)
by_id = {it["id"]: it for it in data}

GROUPS = [
    ("Цвет, радуга и расслоение жидкостей", [3,4,7,14,30,127,55,79,12,60,54,175,212]),
    ("Химические реакции: вулканы, газировка, кислоты", [13,160,37,61,281,132,5,143,82,45,52,248]),
    ("Масло, вода, плотность и плавучесть", [17,47,154,258,39]),
    ("Опыты с яйцами", [15,40,19,148,109,204]),
    ("Воздушные шарики", [10,22,157,174,103,106,94,233,182,136,104]),
    ("Шарики для пинг-понга", [16,74,131,210,96]),
    ("Мыльные пузыри", [141,162]),
    ("Вода: поверхностное натяжение и атмосферное давление", [34,138,100,18,134,87,178,181,92,77,68,97,149,252,222]),
    ("Свечи", [6,102,107]),
    ("Стаканы, банки и бутылки", [36,38,117,120,257,272,186]),
    ("Баланс, центр тяжести и инерция", [89,59,112,95,41,62,224,139,251]),
    ("Статическое электричество", [110,246,111,288,266]),
    ("Звук", [48,72,216,144]),
    ("Свет, зрение и оптические иллюзии", [56,35,161,172,145,215,293,164]),
    ("Бумага: складывание, резка, конструкции", [108,163,155,90,142,195,105]),
    ("Температура, тепло и лёд", [28,91,261]),
    ("Механика и разное", [51,64,93,115,247,255,290]),
]

def extract(iid):
    with open(os.path.join(SITE, "items", f"item_{iid:03d}.html"), encoding="utf-8") as f:
        h = f.read()
    def block(title):
        m = re.search(r'<h2>'+re.escape(title)+r'</h2>\s*(.*?)</div>', h, re.S)
        return m.group(1) if m else ""
    mat_html = block("Материалы")
    mat = re.search(r'<p>(.*?)</p>', mat_html, re.S)
    materials = html.unescape(mat.group(1).strip()) if mat else ""
    steps_html = block("Шаги эксперимента")
    steps = [html.unescape(s.strip()) for s in re.findall(r'<li>(.*?)</li>', steps_html, re.S)]
    prin_html = block("Научный принцип")
    pr = re.search(r'<p>(.*?)</p>', prin_html, re.S)
    principle = html.unescape(pr.group(1).strip()) if pr else ""
    return materials, steps, principle

items_js = []
groups_js = []
for gname, ids in GROUPS:
    gitem_ids = []
    for iid in ids:
        it = by_id[iid]
        materials, steps, principle = extract(iid)
        items_js.append({
            "id": iid,
            "title": it["title_ru"],
            "materials": materials,
            "steps": steps,
            "principle": principle,
        })
        gitem_ids.append(iid)
    groups_js.append({"name": gname, "ids": gitem_ids})

data_json = json.dumps({"groups": groups_js, "items": {str(i["id"]): i for i in items_js}}, ensure_ascii=False)

with open(os.path.join(SITE, "style.css"), encoding="utf-8") as f:
    css = f.read()

page = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Научные опыты для детей</title>
<style>
""" + css + """
.detail{display:none;}
.detail.active{display:block;}
#listView.hidden{display:none;}
.card{cursor:pointer;}
</style>
</head><body>

<div id="listView">
<header>
<h1>Научные опыты для детей</h1>
<p>Русскоязычный каталог наборов &middot; ID_COUNT опытов, сгруппированы по темам</p>
</header>
<div class="searchbar">
<div class="search-wrap">
<span class="search-icon">&#128269;</span>
<input type="search" id="search" placeholder="Поиск опыта по названию..." autocomplete="off">
<button type="button" id="search-clear" aria-label="Очистить">&times;</button>
</div>
</div>
<div class="container" id="listContainer"></div>
<footer>Каталог научных опытов. Видео и полные инструкции добавляются постепенно.</footer>
</div>

<div id="detailView" class="item-page" style="display:none;">
<div class="container" id="detailContainer"></div>
<footer>Каталог научных опытов</footer>
</div>

<script>
var DATA = __DATA__;
var listView=document.getElementById('listView');
var detailView=document.getElementById('detailView');
var listContainer=document.getElementById('listContainer');
var detailContainer=document.getElementById('detailContainer');

function esc(s){var d=document.createElement('div');d.textContent=s;return d.innerHTML;}

function renderList(){
  var htmlStr='';
  DATA.groups.forEach(function(g){
    var cards='';
    g.ids.forEach(function(id){
      var it=DATA.items[id];
      cards+='<div class="card" data-search="'+esc(it.title.toLowerCase())+'" onclick="openItem('+id+')">'
        +'<h3>'+esc(it.title)+'</h3><span class="badge ok">готово</span></div>';
    });
    htmlStr+='<section class="group"><h2 class="group-title">'+esc(g.name)+' <span class="group-count">('+g.ids.length+')</span></h2><div class="grid">'+cards+'</div></section>';
  });
  htmlStr+='<p id="no-results" class="no-results" hidden>Ничего не найдено</p>';
  listContainer.innerHTML=htmlStr;
  bindSearch();
}

function openItem(id){
  var it=DATA.items[id];
  var steps='';
  it.steps.forEach(function(s){steps+='<li>'+esc(s)+'</li>';});
  detailContainer.innerHTML=
    '<a class="back-link" href="#" onclick="closeItem();return false;">&larr; Ко всему каталогу</a>'
    +'<h1>'+esc(it.title)+'</h1>'
    +'<div class="section-block"><h2>Видео</h2><div class="video-placeholder">Видео добавится позже</div></div>'
    +'<div class="section-block"><h2>Материалы</h2><p>'+esc(it.materials)+'</p></div>'
    +'<div class="section-block"><h2>Шаги эксперимента</h2><ol>'+steps+'</ol></div>'
    +'<div class="section-block"><h2>Научный принцип</h2><p>'+esc(it.principle)+'</p></div>';
  listView.style.display='none';
  detailView.style.display='block';
  window.scrollTo(0,0);
}
function closeItem(){
  detailView.style.display='none';
  listView.style.display='block';
  window.scrollTo(0,0);
}

function bindSearch(){
  var input=document.getElementById('search');
  var clearBtn=document.getElementById('search-clear');
  var noRes=document.getElementById('no-results');
  function apply(){
    var q=input.value.trim().toLowerCase();
    clearBtn.style.display=q?'block':'none';
    var any=false;
    document.querySelectorAll('.card').forEach(function(c){
      var m=!q||c.getAttribute('data-search').indexOf(q)!==-1;
      c.style.display=m?'':'none'; if(m)any=true;
    });
    document.querySelectorAll('.group').forEach(function(g){
      var vis=g.querySelectorAll('.card:not([style*="display: none"])').length>0;
      g.style.display=vis?'':'none';
    });
    noRes.hidden=any;
  }
  input.addEventListener('input',apply);
  clearBtn.addEventListener('click',function(){input.value='';apply();input.focus();});
}

renderList();
</script>
</body></html>
"""

page = page.replace("__DATA__", data_json).replace("ID_COUNT", str(len(items_js)))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print("Built single file:", OUT, "items:", len(items_js))
