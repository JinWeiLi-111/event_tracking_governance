# BOSS 直聘存量埋点治理（Agent 工具入口）

## 1) 本文件职责（必须先读）

`AGENT.md` 是系统级调度入口，不承载具体规则细节，只负责：

- 定义 Agent A / Agent B 的职责边界。
- 提供“触发条件 -> 必读文档 -> 输入输出契约”的索引。
- 规定冲突优先级、回退策略和重试闭环。

任何 Agent 会话都必须先读取本文件，再按角色进入对应工具文档。

## 2) 文档分层（单一真源）

### 系统层

- `AGENT.md`：协作协议、调度顺序、优先级。

### 契约层（Agent 间数据协议）

- `contracts/handoff_schema.md`：Agent A -> Agent B 交接输入输出格式（含必填字段、校验结论结构）。

### Agent 工具层（角色入口）

- `agents/agent_a_governance.md`：Agent A 触发条件、输入格式、输出格式、调用步骤。
- `agents/agent_b_validation.md`：Agent B 触发条件、输入格式、输出格式、门禁执行方式。

### 流程层

- `workflows/workflow.md`：字段治理流程（按步骤调用知识层文档）。

### 知识层（按需检索）

- `knowledge/common_rules.md`：Agent A 通用规则与跨场景速查约束。
- `knowledge/domain_scenarios.md`：场景命中与归一卡片。
- `knowledge/validation_rules.md`：Must/Forbidden 校验规则与结论分级。

### 背景层（可选）

- `docs/background.md`：背景动机，不可替代流程/规则/契约。

## 3) Agent 职责边界（强约束）

### Agent A（治理执行）

- 负责字段补全、归一、依据说明。
- 不输出最终 `PASS/WARN/FAIL` 结论。
- 输出必须符合 `contracts/handoff_schema.md` 的 A 侧结构。

### Agent B（最终校验）

- 负责门禁校验与原地修正，输出修正后的同构结果。
- 不臆造新业务事实，不做风格化润色。
- 输入必须是符合 `contracts/handoff_schema.md` 的 A 侧产物。

## 4) 统一输入范围（强约束）

仅允许使用以下字段和附加资料：

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

禁止：

- 新增输入与需求文档之外的业务事实。
- 基于外部未提供信息做结论。

## 5) 读取隔离与触发（必须遵循）

1. 任一 Agent 会话先读 `AGENT.md`。
2. 触发 Agent A 时，仅允许继续读取：
   - `agents/agent_a_governance.md`
   - `workflows/workflow.md`
   - `knowledge/common_rules.md`
   - `knowledge/domain_scenarios.md`
   - `contracts/handoff_schema.md`
   - `docs/background.md`（可选）
   - `configs/` 下枚举文件
3. 触发 Agent B 时，仅允许继续读取：
   - `agents/agent_b_validation.md`
   - `knowledge/validation_rules.md`
   - `contracts/handoff_schema.md`
   - `docs/background.md`（可选）
   - `configs/` 下枚举文件
4. 同一会话禁止同时读取两个 Agent 主文档，避免角色混叠。

## 6) 闭环调度顺序（必须遵循）

1. Agent A 按 `agents/agent_a_governance.md` + `workflows/workflow.md` 执行治理。
2. Agent A 输出按 `contracts/handoff_schema.md` 交接给 Agent B。
3. Agent B 按 `agents/agent_b_validation.md` + `knowledge/validation_rules.md` 完成校验并原地修正。
4. Agent B 对修正结果执行全量复校后输出同构结果。
5. 必要时输出独立审计 sidecar，用于追溯修正依据。

## 7) 规则冲突优先级

当多文档冲突时，优先级从高到低：

1. `knowledge/validation_rules.md`
2. `contracts/handoff_schema.md`
3. `workflows/workflow.md`
4. `knowledge/common_rules.md`
5. `knowledge/domain_scenarios.md`
6. `docs/background.md`

## 8) 失败与回退策略

- Agent B 发现问题时优先原地修正，不中断主输出结构。
- 场景冲突无法判定时，采用保守策略：不臆造页面位置，事件类型可降级为“其他”。
- 自动修正必须可追溯：记录规则 ID、原值、新值、修正理由（建议写入 sidecar）。
