# A -> B 交接契约

该契约定义 Agent A 与 Agent B 的交接结构，默认使用“输入同构扁平字段”，避免格式转换误差。

## 单条记录契约（推荐：扁平同构）

```json
{
  "埋点id": "string",
  "页面位置": "string",
  "功能名称": "string",
  "事件类型": "string",
  "埋点中文名": "string",
  "埋点英文名": "string",
  "埋点描述": "string"
}
```

## 批次契约（推荐）

```json
{
  "batch_id": "batch1",
  "items": [
    {
      "埋点id": "string",
      "页面位置": "string",
      "功能名称": "string",
      "事件类型": "string",
      "埋点中文名": "string",
      "埋点英文名": "string",
      "埋点描述": "string"
    }
  ]
}
```

## 可选审计 sidecar（推荐）

为保留依据而不污染主结构，建议额外产出审计文件（如 `batch1_governed_audit.json`）：

```json
{
  "batch_id": "batch1",
  "items": [
    {
      "record_id": "string",
      "field_rationales": [
        {
          "field": "功能名称",
          "old_value": "NULL",
          "new_value": "职位搜索",
          "basis": "workflow 3.3"
        }
      ],
      "uncertainties": []
    }
  ]
}
```

## 兼容性说明

- Agent B 与 pipeline 脚本需优先支持扁平同构输入。
- 为兼容历史数据，仍允许读取旧格式（如 `governed_output`、`validated_output` 包裹结构）。
