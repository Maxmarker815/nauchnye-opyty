# -*- coding: utf-8 -*-
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

REMOVE_IDS = [1, 2, 8, 9, 11, 21, 23, 24, 25, 26, 29, 31, 32, 33, 42, 43, 44, 46, 49, 50, 53, 57, 58, 66, 67, 69, 70, 71, 75, 76, 78, 80, 81, 83, 84, 85, 86, 88, 98, 99]

by_id = {it["id"]: it for it in data}
for iid in REMOVE_IDS:
    by_id[iid]["status"] = "removed"

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Removed:", len(REMOVE_IDS), REMOVE_IDS)
