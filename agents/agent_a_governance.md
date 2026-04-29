# Agent A 工具文档（治理执行）

## 1) 触发条件（Trigger）

当任务目标包含以下任一意图时，触发 Agent A：

- “补全/归一化埋点字段”
- “将历史埋点改造成规范结构”
- “生成可交接给校验 Agent 的治理产物”

不满足以上意图时，不应调用本工具文档。

## 2) 必读依赖（Required Reads）

按顺序读取：

1. `AGENT.md`
2. `workflows/workflow.md`
3. `knowledge/common_rules.md`
4. `knowledge/domain_scenarios.md`
5. `contracts/handoff_schema.md`
6. `docs/background.md`（可选，仅用于背景理解）

## 3) 输入格式（Input Contract）

支持两种输入（字段名必须一致）：

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

### 批次

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

## 4) 输出格式（Output Contract）

必须输出给 Agent B 可直接消费的结构（与 `contracts/handoff_schema.md` 一致）：

- 主输出：治理后的 `governed_output`
- 可选副输出：审计信息 `audit_sidecar`

最小主输出示例：

```json
{
  "batch_id": "batchX",
  "items": [
    {
      "埋点id": "id_001",
      "页面位置": "APP_C-职位列表-搜索",
      "功能名称": "搜索结果列表查看",
      "事件类型": "浏览",
      "埋点中文名": "C_职位列表_搜索-搜索结果列表查看-浏览",
      "埋点英文名": "search_result_list_view",
      "埋点描述": "用户在职位搜索结果页浏览结果列表并触发上报",
      "主被动": "主动",
      "标签": "求职行为"
    }
  ]
}
```

## 5) 执行步骤（Procedure）

1. 按 `workflows/workflow.md` 执行字段级补全，严格按步骤顺序处理。
2. 命中业务语义时，调用 `knowledge/domain_scenarios.md` 对字段归一。
3. 结果结构化为 `contracts/handoff_schema.md` 中定义的 Agent A 输出结构。
4. 若信息不足，保留不确定标记到审计 sidecar，不得臆造事实。

## 6) 约束（Guardrails）

- 不输出 `PASS/WARN/FAIL`。
- 不修改输入字段名和层级结构。
- 不引入外部未知事实。
