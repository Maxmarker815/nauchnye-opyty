# -*- coding: utf-8 -*-
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

by_id = {it["id"]: it for it in data}
by_id[241]["status"] = "removed"

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Removed: 241")
