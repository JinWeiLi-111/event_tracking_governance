# Agent A -> Agent B 交接契约（唯一真源）

## 1) 目的

定义双 Agent 之间可机器校验的数据契约，避免“口头约定”造成格式漂移。

## 2) 字段清单（RecordFields）

每条埋点必须包含以下字段（允许空字符串，但字段不可缺失）：

- `埋点id`
- `页面位置`
- `功能名称`
- `事件类型`
- `埋点中文名`
- `埋点英文名`
- `埋点描述`
- `主被动`
- `标签`

## 3) Agent A 输出契约（AgentAOutput）

### 单条

```json
{
  "埋点id": "string",
  "页面位置": "string",
  "功能名称": "string",
  "事件类型": "string",
  "埋点中文名": "string",
  "埋点英文名": "string",
  "埋点描述": "string",
  "主被动": "string",
  "标签": "string"
}
```

### 批次（推荐）

```json
{
  "batch_id": "string",
  "items": [
    {
      "埋点id": "string",
      "页面位置": "string",
      "功能名称": "string",
      "事件类型": "string",
      "埋点中文名": "string",
      "埋点英文名": "string",
      "埋点描述": "string",
      "主被动": "string",
      "标签": "string"
    }
  ]
}
```

## 4) Agent B 输出契约（AgentBOutput）

```json
{
  "batch_id": "string",
  "items": [
    {
      "埋点id": "string",
      "页面位置": "string",
      "功能名称": "string",
      "事件类型": "string",
      "埋点中文名": "string",
      "埋点英文名": "string",
      "埋点描述": "string",
      "主被动": "string",
      "标签": "string"
    }
  ]
}
```

说明：

- Agent B 在校验过程中发现问题时，直接原地修正字段值。
- 主输出保持与 Agent A 同构，不追加 `verdict`、`violations` 等字段。

## 5) 可选审计 sidecar（推荐）

若需要保留校验证据，建议单独输出 sidecar 文件，不污染主输出结构：

```json
{
  "batch_id": "string",
  "items": [
    {
      "埋点id": "string",
      "changes": [
        {
          "rule_id": "M01|F01|...",
          "field": "事件类型",
          "old_value": "view",
          "new_value": "浏览",
          "reason": "事件类型枚举归一"
        }
      ],
      "needs_manual_review": false
    }
  ]
}
```

## 6) 兼容规则（Backward Compatibility）

- 若输入含 `governed_output`，Agent B 必须先解包为 `AgentAOutput` 再执行校验。
- 若缺少 `batch_id`，允许自动补 `batch_id="ad-hoc"`，但需在输出中保留。

## 7) 错误处理

- 契约字段缺失：按最小可用原则补空值并记录审计 `SCHEMA_REQUIRED_FIELD_MISSING`。
- 字段名不一致：不改写字段名，记录审计 `SCHEMA_FIELD_NAME_INVALID`，并标记 `needs_manual_review=true`。
- 类型错误（非字符串/数组）：尝试安全转换；无法转换时记录 `SCHEMA_TYPE_INVALID` 并标记人工处理。
