# -*- coding: utf-8 -*-
import os, glob, re

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")

with open(os.path.join(SITE, "style.css"), encoding="utf-8") as f:
    css = f.read()

style_block = "<style>\n" + css + "\n</style>"

# index.html
idx_path = os.path.join(SITE, "index.html")
with open(idx_path, encoding="utf-8") as f:
    html = f.read()
html = re.sub(r'<link rel="stylesheet" href="style\.css">', style_block, html)
with open(idx_path, "w", encoding="utf-8") as f:
    f.write(html)

# item pages
n = 0
for fp in glob.glob(os.path.join(SITE, "items", "item_*.html")):
    with open(fp, encoding="utf-8") as f:
        html = f.read()
    new = re.sub(r'<link rel="stylesheet" href="\.\./style\.css">', style_block, html)
    if new != html:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(new)
        n += 1

print("Inlined CSS into index + item pages:", n)
