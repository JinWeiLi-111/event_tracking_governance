# Agents 协同说明

本目录用于拆分两个独立 Agent 的职责，避免“同一个 Agent 既治理又验收”导致的确认偏差。

## 角色定义

- Agent A（治理执行）：
  - 负责字段补全、归一化、可解释依据输出。
  - 不输出最终 PASS/WARN/FAIL 结论。
- Agent B（最终校验）：
  - 负责门禁规则审查与原地修正输出。
  - 不臆造新业务事实，不做风格型润色。

## 子目录

- `agent_a_governance.md`：Agent A 主文档（触发条件、输入输出、调用步骤）。
- `agent_b_validation.md`：Agent B 主文档（触发条件、输入输出、门禁执行）。
- `prompts/`：旧路径兼容入口（已迁移，请勿作为真源）。

## 读取顺序建议

1. Agent A 读取：`AGENT.md` -> `agents/agent_a_governance.md` -> `workflows/workflow.md` -> `knowledge/domain_scenarios.md`。
2. Agent B 读取：`AGENT.md` -> `agents/agent_b_validation.md` -> `knowledge/validation_rules.md` -> `contracts/handoff_schema.md`。
