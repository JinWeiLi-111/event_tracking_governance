# Agents 协同说明

本目录用于拆分两个独立 Agent 的职责，避免“同一个 Agent 既治理又验收”导致的确认偏差。

## 角色定义

- Agent A（治理执行）：
  - 负责字段补全、归一化、可解释依据输出。
  - 不输出最终 PASS/WARN/FAIL 结论。
- Agent B（最终校验）：
  - 负责门禁规则审查与结论输出。
  - 不臆造新业务事实，不做风格型润色。

## 子目录

- `prompts/`：两个 Agent 的系统提示词模板。
- `contracts/`：A 到 B 的交接数据契约。

## 读取顺序建议

1. Agent A 读取：`AGENT.md` -> `docs/workflow.md` -> `docs/domain_scenarios.md`。
2. Agent B 读取：`AGENT.md` -> `docs/validation_rules.md` -> `configs/hard_constraints.json`（若存在）。
