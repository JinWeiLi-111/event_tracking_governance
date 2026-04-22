import json

with open("configs/enums/page_locations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

compact_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
print(compact_str)  # 紧凑的一行 JSON 字符串