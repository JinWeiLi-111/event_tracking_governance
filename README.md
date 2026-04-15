# event-tracking-governance-agent

用于存量埋点治理中“补全元数据信息”的 Agent 代码框架。

当前仓库只提供框架与占位模板，不包含你的业务规则细节。你可以后续把补全方法、边界和样例填入配置与规则模块。

## 快速开始

1. 创建并激活虚拟环境（可选）
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. 安装项目（开发模式）
   - `pip install -e .`
3. 准备输入与配置
   - 复制 `configs/agent_config.example.json` 为你的配置文件
   - 复制 `templates/input/legacy_events.example.json` 为待处理存量埋点文件
4. 运行 Agent
   - `agent-cli --config configs/agent_config.example.json --input templates/input/legacy_events.example.json`

## 核心流程

1. 读取存量埋点元数据（JSON）
2. 按规则链补全字段
3. 输出补全后的元数据和审计报告

## 项目结构

- `AGENT.md`: 你的 Agent 说明文档（目前保持为空）
- `src/agent/main.py`: CLI 入口
- `src/agent/core/settings.py`: 运行配置模型
- `src/agent/domain/models.py`: 埋点元数据领域模型
- `src/agent/rules/`: 规则基类与默认规则注册
- `src/agent/services/`: 补全编排与审计输出
- `configs/`: 配置模板
- `templates/`: 输入/输出/报告样例模板
