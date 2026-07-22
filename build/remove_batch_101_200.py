# -*- coding: utf-8 -*-
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

REMOVE_IDS = [113, 114, 116, 118, 119, 121, 122, 123, 124, 125, 126, 128, 129, 130, 133, 135, 137, 140, 146, 147, 150, 151, 152, 153, 156, 158, 159, 165, 166, 167, 168, 169, 170, 171, 173, 176, 177, 179, 180, 183, 184, 187, 188, 189, 190, 191, 192, 193, 194, 196, 197, 198, 199, 200]

by_id = {it["id"]: it for it in data}
for iid in REMOVE_IDS:
    by_id[iid]["status"] = "removed"

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Removed:", len(REMOVE_IDS), REMOVE_IDS)
