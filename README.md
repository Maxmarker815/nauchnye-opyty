ПРОЕКТ: Русскоязычный каталог детских научных опытов
=====================================================

Содержимое:
- katalog_odin_fajl.html — весь сайт в одном файле (открывается сразу, ничего распаковывать не нужно)
- site/                   — исходники сайта:
    - index.html          — главная страница (стили уже встроены)
    - items/item_XXX.html — страница каждого опыта
    - data.json           — данные всех позиций (id, названия, статус, порядок)
    - style.css           — общий файл стилей
- build/                  — Python-скрипты, которыми собирался сайт:
    - generate.py             — первичная генерация
    - update_batchN.py        — наполнение опытов контентом
    - group_and_index.py      — группировка по темам + сборка index.html
    - inline_css.py           — встраивание CSS в страницы
    - build_single.py         — сборка единого файла katalog_odin_fajl.html
    - remove_batch_*.py       — пометка удалённых позиций
    - regenerate_index.py     — пересборка index.html из data.json
    - translations.py         — словарь переводов заголовков
    - section1..4.txt         — исходный текст китайского каталога (для сверки)

Статусы в data.json: "full" — активная позиция (122 шт), "removed" — исключена (246 шт).

Как пересобрать единый файл после правок:
    cd build && python3 group_and_index.py && python3 inline_css.py && python3 build_single.py
