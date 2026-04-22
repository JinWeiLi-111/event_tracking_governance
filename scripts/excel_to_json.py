import pandas as pd
import json
import math
from pathlib import Path

def is_nan(value):
    # 检查是否为 NaN
    if value is None:
        return True
    try:
        return math.isnan(value)
    except Exception:
        return False

def _id_sort_key(value):
    """把 id 转成可排序值，优先按数值排序。"""
    if is_nan(value):
        return float("inf")
    try:
        return int(float(str(value).strip()))
    except Exception:
        return str(value)


def excel_to_json_batches(excel_path, output_dir, batch_size=10, filename_prefix="batch2"):
    # 读取Excel文件
    df = pd.read_excel(excel_path)
    # 按 id 升序排序
    if "id" in df.columns:
        df = df.sort_values(by="id", key=lambda col: col.map(_id_sort_key))

    # Excel列名与JSON字段名的映射
    columns_mapping = {
        "id" : "埋点id",
        "页面位置": "页面位置",
        "功能名称": "功能名称",
        "事件类型": "事件类型",
        "埋点中文名": "埋点中文名",
        "埋点英文名": "埋点英文名",
        "描述": "埋点描述"
    }
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    total_rows = len(df)
    batch_count = math.ceil(total_rows / batch_size) if total_rows else 0

    for batch_index in range(batch_count):
        start = batch_index * batch_size
        end = start + batch_size
        batch_df = df.iloc[start:end]

        items = []
        for _, row in batch_df.iterrows():
            item = {}
            for excel_col, json_col in columns_mapping.items():
                # 获取值
                v = row.get(excel_col, None) if excel_col in row else None
                # 将 NaN、None 均转为字符串 "NULL"
                if is_nan(v):
                    item[json_col] = "NULL"
                else:
                    item[json_col] = str(v) if v is not None else "NULL"
            items.append(item)

        result = {"items": items}
        output_json_path = output_dir / f"{filename_prefix}{batch_index + 1}_input.json"
        # 写入json文件
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"Generated {output_json_path} ({len(items)} items)")

if __name__ == "__main__":
    excel_path = "埋点100_v2.xlsx"
    output_dir = "./workspace/turn_2/input"
    excel_to_json_batches(excel_path, output_dir, batch_size=10, filename_prefix="batch2")