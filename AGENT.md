# BOSS 直聘存量埋点治理（双 Agent 协作总入口）

## 项目目标

围绕 BOSS 直聘存量历史埋点治理场景，对历史埋点元数据进行补全、归一和最终门禁校验，确保结果可复核、可追踪、可落库。

## 协作模式（核心）

本项目采用双 Agent 协作，不再使用“单 Agent 既治理又校验”的模式。

- Agent A（治理执行）：
  - 负责字段补全、归一化、依据说明输出。
  - 不输出 PASS/WARN/FAIL 最终结论。
- Agent B（最终校验）：
  - 负责门禁规则审查、结论分级、失败打回。
  - 不臆造新业务事实，不做风格化润色。

## 通用工作边界

两个 Agent 均仅基于以下信息进行处理：

1. 埋点携带的基础属性（字段范围固定）：
  - 埋点id
  - 页面位置
  - 功能名称
  - 事件类型
  - 埋点中文名
  - 埋点英文名
  - 埋点描述
  - 主被动
  - 标签
2. 与该埋点绑定的需求文档（若有）

两个 Agent 均不得：

- 新增超出输入范围的业务事实
- 基于未提供的外部信息做结论

## 输入与输出定义

输入可为单条 JSON 或批次 JSON（`items` 数组），字段通常包含：

- 埋点id
- 页面位置
- 功能名称
- 事件类型
- 埋点中文名
- 埋点英文名
- 埋点描述
- 主被动
- 标签
- 需求文档信息（若有）

输出按 Agent 角色区分：

- Agent A 输出：治理结果 + 字段依据 + 不确定项（见 `agents/contracts/handoff_schema.md`）
- Agent B 输出：`PASS/WARN/FAIL` + 违规证据 + 修复建议

## 文档职责分工（单一真源）

- `AGENT.md`：
  - 定义双 Agent 协作边界、调度顺序、冲突优先级和回退原则。
- `agents/prompts/agent_a_governance.md`：
  - Agent A 角色入口与输出格式要求。
- `agents/prompts/agent_b_validation.md`：
  - Agent B 角色入口与校验输出格式要求。
- `docs/workflow.md`：
  - 字段级处理流程与补全步骤（严格按照此工作流程进行埋点各字段规范化）。
- `docs/domain_scenarios.md`：
  - 特定业务场景命中条件与归一目标。
- `docs/validation_rules.md`：
  - 最终门禁校验规则（Must/Forbidden、PASS/WARN/FAIL）。
- `docs/background.md`：
  - 治理背景与规范动机，仅用于背景理解。

## 读取隔离规则（必须遵循）

为避免角色混叠和确认偏差，必须遵循以下规则：

1. 任一单独 Agent 会话都必须先读取 `AGENT.md`。
2. Agent A 会话只允许额外读取：
  - `agents/prompts/agent_a_governance.md`
  - `docs/workflow.md`
  - `docs/domain_scenarios.md`
  - `docs/background.md`
  - `configs文件夹中的全部辅助文件`
3. Agent B 会话只允许额外读取：
  - `agents/prompts/agent_b_validation.md`
  - `docs/validation_rules.md`
  - `docs/background.md`
  - `configs文件夹中的全部辅助文件`
4. 禁止同一会话同时读取 `agent_a_governance.md` 与 `agent_b_validation.md`。

## 文档调度顺序（必须遵循）

每条埋点或每个批次按以下闭环执行：

1. Agent A 读取 A 侧文档并产出治理结果。
2. Agent A 输出按 `agents/contracts/handoff_schema.md` 交接给 Agent B。
3. Agent B 读取 B 侧文档并执行门禁校验，输出 PASS/WARN/FAIL。
4. 若结论为 FAIL，打回 Agent A 修正后重新进入 Agent B 全量复校。
5. 仅 PASS（或按策略允许的 WARN）结果可进入最终结果目录。

## 冲突处理优先级（必须遵循）

当多文档规则冲突时，优先级如下（高 -> 低）：

1. `docs/validation_rules.md`（最终门禁）
2. `docs/workflow.md`（字段流程）
3. `docs/domain_scenarios.md`（场景归一）
4. `docs/background.md`（背景说明）

## 失败与回退策略

- 命中 FAIL 时，禁止直接输出最终结果，必须修正后重跑全量校验。
- 若场景冲突无法判定，采用保守策略（不臆造页面位置，事件类型可降级为“其他”）。
- 任何自动修正必须保留可解释依据（命中规则、原值、修正值）。
- 最终目录仅接收通过校验的可追踪结果。

