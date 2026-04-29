# Event Tracking Governance

This repository is a fixed workflow for BOSS tracking governance. The primary entrypoint is `AGENT.md`.

## How Cursor Should Work Here

Cursor is configured by `.cursor/rules/event-tracking-governance.mdc` to read:

1. `AGENT.md`
2. `workflows/cursor_execution_manifest.json`
3. The selected role documents in the manifest order

Do not bypass the role split:

- Agent A performs field completion and normalization.
- Agent B validates Agent A output and performs minimal in-place correction.

## Key Files

- `AGENT.md`: scheduling protocol, read isolation, conflict priority, retry rules.
- `workflows/cursor_execution_manifest.json`: machine-readable execution router for Cursor.
- `agents/agent_a_governance.md`: Agent A trigger, reads, input, output, and guardrails.
- `agents/agent_b_validation.md`: Agent B trigger, reads, input, output, and guardrails.
- `workflows/workflow.md`: Agent A executable field workflow.
- `knowledge/common_rules.md`: Agent A common rules.
- `knowledge/domain_scenarios.md`: scenario matching and normalization targets.
- `knowledge/validation_rules.md`: Agent B Must and Forbidden rules.
- `contracts/handoff_schema.md`: human-readable handoff contract.
- `contracts/handoff_schema.json`: machine-checkable batch output schema.
- `configs/enums/*.json`: canonical enum and lexicon references.

## Workspace Convention

- Inputs: `workspace/turn_*/input/*_input.json`
- Agent A outputs: `workspace/turn_*/agent_a_output/*_governed.json`
- Agent B outputs: `workspace/turn_*/agent_b_review/*_review.json`
- Final merged outputs: `workspace/turn_*/final/all_batches_result.json`

Main outputs must preserve the nine record fields from `contracts/handoff_schema.md`. Audit evidence belongs in a sidecar, not in the main batch JSON.
