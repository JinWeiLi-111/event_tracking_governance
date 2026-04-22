# Agent B 工具文档（最终校验）

## 1) 触发条件（Trigger）

当任务目标包含以下任一意图时，触发 Agent B：

- “对治理结果做门禁校验”
- “发现不合规字段并原地修正”
- “输出可直接落盘的最终同构结果”

若输入不是 Agent A 治理产物，不应直接触发本工具。

## 2) 必读依赖（Required Reads）

按顺序读取：

1. `AGENT.md`
2. `contracts/handoff_schema.md`
3. `knowledge/validation_rules.md`
4. `docs/background.md`（可选）

## 3) 输入格式（Input Contract）

输入必须满足 `contracts/handoff_schema.md` 的 `AgentAOutput`：

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

兼容输入：若出现旧字段 `governed_output`，先解包为同构 `items` 再校验。

## 4) 输出格式（Output Contract）

必须输出与输入同构的批次结构（不追加 verdict 字段）：

```json
{
  "batch_id": "batchX",
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

## 5) 执行步骤（Procedure）

1. 校验输入结构是否符合 `contracts/handoff_schema.md`。
2. 按 `knowledge/validation_rules.md` 的 Must 与 Forbidden 全量执行。
3. 对不合规字段进行“最小原地修正”，避免不必要改动。
4. 输出修正后的同构结果；如需证据，写入独立审计 sidecar。

## 6) 约束（Guardrails）

- 不改写业务语义，不做风格润色。
- 不引入输入外业务事实。
- 每条修正后必须做一次全量复校再输出。
