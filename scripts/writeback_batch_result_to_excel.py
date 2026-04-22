import json
import math
import sys

import pandas as pd


def is_nan(value):
    if value is None:
        return True
    try:
        return math.isnan(value)
    except Exception:
        return False


def is_null(value):
    if value is None:
        return True
    if is_nan(value):
        return True
    if isinstance(value, str) and value.strip() in ["", "NULL"]:
        return True
    return False


def load_batch_result(result_json_path):
    with open(result_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data.get("items", [])
    by_id = {}
    for it in items:
        if not isinstance(it, dict):
            continue
        k = it.get("埋点id", None)
        if is_null(k):
            continue
        by_id[str(k)] = it
    return by_id


def writeback_excel(excel_path, result_json_path, output_excel_path):
    df = pd.read_excel(excel_path, header=0)

    # Excel列名与JSON字段名的映射（与 scripts/excel_to_json.py 保持一致）
    columns_mapping = {
        "id": "埋点id",
        "页面位置-new": "页面位置",
        "功能名称-new": "功能名称",
        "事件类型-new": "事件类型",
        "埋点中文名-new": "埋点中文名",
        "埋点英文名": "埋点英文名",
        "描述-new": "埋点描述",
    }

    if "id" not in df.columns:
        raise ValueError(f"Excel缺少列: id, 当前列: {list(df.columns)}")

    # 确保目标列存在（如果Excel缺少某些列，自动补列）
    for excel_col in columns_mapping.keys():
        if excel_col not in df.columns:
            df[excel_col] = "NULL"
    if "操作人" not in df.columns:
        df["操作人"] = "NULL"

    by_id = load_batch_result(result_json_path)

    updated = 0
    not_found = 0
    skipped_has_operator = 0
    for idx, row in df.iterrows():
        # 如果原来的操作人存在值，这行就跳过不处理
        operator = row.get("操作人", None)
        if not is_null(operator):
            skipped_has_operator += 1
            continue

        excel_id = row.get("id", None)
        if is_null(excel_id):
            continue
        key = str(excel_id)
        result = by_id.get(key, None)
        if result is None:
            not_found += 1
            continue

        changed = False
        for excel_col, json_col in columns_mapping.items():
            if json_col == "埋点id":
                continue
            v = result.get(json_col, None)
            # 与 excel_to_json.py 一致：把 NaN/None 当做 NULL；这里默认不回写 NULL，避免覆盖原数据
            if is_null(v):
                continue
            # 对 columns_mapping 列做处理：如果该列已有值，默认不覆盖
            old_v = row.get(excel_col, None)
            if not is_null(old_v):
                continue
            df.at[idx, excel_col] = str(v)
            changed = True

        if changed:
            df.at[idx, "操作人"] = "Agent"
            updated += 1

    df.to_excel(output_excel_path, index=False)
    print(
        f"writeback done, updated={updated}, skipped_has_operator={skipped_has_operator}, "
        f"not_found={not_found}, output={output_excel_path}"
    )


if __name__ == "__main__":
    # 支持命令行参数：excel_path result_json_path output_excel_path
    excel_path = "TOP埋点治理记录_副本.xlsx"
    result_json_path = "orgin_input/all_batches_result.json"
    output_excel_path = "TOP埋点治理记录_副本_1.xlsx"

    if len(sys.argv) >= 2:
        excel_path = sys.argv[1]
    if len(sys.argv) >= 3:
        result_json_path = sys.argv[2]
    if len(sys.argv) >= 4:
        output_excel_path = sys.argv[3]

    writeback_excel(excel_path, result_json_path, output_excel_path)

