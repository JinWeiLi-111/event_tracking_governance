# Workspace 数据流转

该目录只用于双 Agent 协同过程中的中间与最终产物，不建议手工混放其他文件。

## 子目录

- `input/`：待处理输入。
- `agent_a_output/`：治理结果（含字段依据）。
- `agent_b_review/`：校验并原地修正后的同构结果。
- `final/`：通过校验可落库结果。

## 命名建议

- 输入：`batch1_input.json`
- A 输出：`batch1_governed.json`
- B 结果：`batch1_review.json`
- 最终：`batch1_result.json`

## 流转原则

1. 不跳过 Agent B，不直接把 A 输出当最终结果。
2. Agent B 在校验中发现问题应直接原地修正并复校。
3. `final/` 目录中的文件应全部可追溯到对应 review 文件（可选 sidecar 审计）。
