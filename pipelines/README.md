# Dual-Agent Pipeline

本目录定义 A（治理）-> B（校验）的固定流程，目标是稳定批量治理质量。

## 目录约定

- `workspace/input/`：输入批次（建议命名 `batchX_input.json`）。
- `workspace/agent_a_output/`：Agent A 输出（建议命名 `batchX_governed.json`，与输入同构扁平字段）。
- `workspace/agent_b_review/`：Agent B 校验结果（建议命名 `batchX_review.json`）。
- `workspace/final/`：仅存放 Agent B 判定为 PASS 的最终文件。

## 执行顺序

1. 准备输入：
   - 将待治理数据放入 `workspace/input/`。
2. 运行 Agent A：
   - 使用 `agents/agent_a_governance.md`。
   - 输出到 `workspace/agent_a_output/`，每条记录保持七字段扁平结构。
3. 运行 Agent B：
   - 使用 `agents/agent_b_validation.md`。
   - 输入为 A 输出，校验中发现问题直接原地修正，输出仍为扁平同构字段结构。
4. 产出结果：
   - 将 B 修正后的结果写入 `workspace/agent_b_review/`。
   - 通过流程策略可直接同步到 `workspace/final/`。

## 与现有脚本衔接

- Excel 转 JSON：`python scripts/excel_to_json.py`
- 合并批次：`python scripts/merge_batch_results.py --input-dir workspace/final --output-file workspace/final/all_batches_result.json`
- 写回 Excel：`python scripts/writeback_batch_result_to_excel.py "TOP埋点治理记录_副本.xlsx" "workspace/final/all_batches_result.json" "TOP埋点治理记录_副本_1.xlsx"`
