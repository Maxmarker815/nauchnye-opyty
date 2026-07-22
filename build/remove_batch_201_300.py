# -*- coding: utf-8 -*-
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "..", "site")
DATA_PATH = os.path.join(SITE, "data.json")
with open(DATA_PATH, encoding="utf-8") as f:
    data = json.load(f)

REMOVE_IDS = [201, 202, 203, 205, 206, 207, 208, 209, 211, 213, 214, 217, 218, 219, 220, 221, 223, 226, 227, 228, 229, 230, 231, 234, 235, 236, 237, 238, 239, 240, 242, 243, 244, 245, 249, 250, 253, 254, 256, 260, 262, 263, 264, 265, 267, 268, 269, 270, 271, 273, 274, 275, 276, 277, 278, 280, 282, 283, 284, 285, 286, 287, 289, 292, 294, 295, 296, 297, 298, 299, 300]

by_id = {it["id"]: it for it in data}
for iid in REMOVE_IDS:
    by_id[iid]["status"] = "removed"

with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Removed:", len(REMOVE_IDS), REMOVE_IDS)
