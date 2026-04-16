from os import path
import pandas as pd
import json
import sys
import math

def is_nan(value):
    # 检查是否为 NaN
    if value is None:
        return True
    try:
        return math.isnan(value)
    except Exception:
        return False

def excel_to_json(excel_path, output_json_path):
    # 读取Excel文件
    df = pd.read_excel(excel_path)

    # Excel列名与JSON字段名的映射
    columns_mapping = {
        "页面位置": "页面位置",
        "功能名称": "功能名称",
        "事件类型": "事件类型",
        "埋点中文名": "埋点中文名",
        "描述": "埋点描述"
    }
    items = []

    for idx, (_, row) in enumerate(df.iterrows(), start=1):
        item = {}
         # 添加 input_id 字段，第一行数据 input_id 为1，第二行为2，以此类推
        item["input_id"] = str(idx)
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

    # 写入json文件
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    path1 = 'TOP埋点治理记录_副本.xlsx'
    path2 = '1.json'
    excel_to_json(path1, path2)