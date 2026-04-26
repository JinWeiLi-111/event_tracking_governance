# 业务场景知识库（Agent A 按需调用）

## 1) 调用触发条件

当出现以下任一情况，必须调用本知识库：

- 仅靠字段字面值无法稳定确定 `页面位置/功能名称/事件类型`
- 输入命中高频模式（如 `list`、`search`、`detail`、道具词）
- 输出字段间出现语义冲突，需要场景优先级裁决

## 2) 查询输入格式

查询时请构造统一检索对象：

```json
{
  "埋点英文名": "string",
  "埋点中文名": "string",
  "埋点描述": "string",
  "页面位置": "string",
  "功能名称": "string"
}
```

## 3) 查询输出格式

命中场景后返回：

```json
{
  "scenario_id": "SCN_XXX",
  "confidence": 0.0,
  "matched_signals": ["string"],
  "normalize_targets": {
    "页面位置": "string",
    "功能名称": "string",
    "事件类型": "string"
  },
  "fallback": "string"
}
```

## 4) 全局规则

- 先匹配，再归一；不允许反推场景。
- 冲突优先级：`英文名前缀/正则` > `中文名关键词` > `描述关键词` > `页面位置原值`。
- 无法判定时保守降级：`事件类型=其他`，页面位置走 `workflows/workflow.md` 兜底。
- 本文档与流程冲突时，以 `workflows/workflow.md` 为准。

## 5) 场景索引（速查）

| 场景ID | 主要触发信号 | 归一核心 |
| --- | --- | --- |
| `SCN_LIST_REFRESH_RECOMMEND` | `英文名` 以 `list` 开头，或 `描述` 含“刷新列表/下拉刷新/重新拉取列表” | 功能名称归一为“推荐列表刷新”，`事件类型=浏览`，如果英文名称中出现'use'动词，就选为``|
| `SCN_SEARCH_RESULT_BROWSE` | `英文名` 含 `search/result_list` 且 `描述` 含“搜索结果/检索结果” | `事件类型=浏览`，功能归一为“搜索结果列表查看” |
| `SCN_DETAIL_PAGE` | `英文名` 以 `detail` 开头 | `事件类型=点击`，功能归一为“查看xx详情页” |
| `SCN_JOB_PUBLISH_OR_CHANGE_GOVERN` | 字段语义命中“B端职位发布/修改管理” | 仅可落 B 端职位相关页面 |
| `SCN_EXPECT_JOB_PUBLISH_OR_CHANGE_GOVERN` | 字段语义命中“C端期望职位发布/修改管理” | 仅可落 C 端职位相关页面 |
| `SCN_EXCHANGE_PHONE` | 字段中出现“交换电话”语义 | `事件类型=点击`，功能名称选择为“交换电话” |
| `SCN_BIZ_OR_BLOCK` | `英文名` 含 `block`，且中文名/描述含商业阻断词 | 页面优先阻断相关位置 |
| `SCN_READ_MESSAGES` | `英文名` 含 `read`，且中文名/描述含“已读” | `事件类型=浏览`，功能“已读消息” |
| `SCN_ITEM_TOOL` | 任一字段命中 `B_items/C_items` 道具名 | 功能保留道具语义，页面优先道具路径 |
| `SCN_LOGIN_OR_SIGNUP` | 任一字段命中“注册/登录/启动” | 页面位置选择登录注册启动相关 |
| `SCN_ITEM_AI_ASSITANT` | 任一字段命中“AI 沟通助手”语义 | 页面位置优先道具相关 |
| `SCN_Boss_OR_Geek_BG`  | bg字段命中`boss`,`geek`    | 命中boss，则页面位置优先考虑B端的相关页面，如果命中geek，页面位置优先考虑C端的页面。 | 
| `SCN_CV_RESUME`   | 中文名称字段命中`直聘简历`    | 不处理这个埋点，原封不动返回即可 |
| `SCN_JOB_MANAGEMENT` | 中文名称字段命中`编辑职位`,`发布职位`,`关闭职位`,`开放职位`  |  页面位置只能选择职位管理相关页面。除非发布职位和完善、首善、同时出现才选择完善/发布职位这个页面。 |
| `SCN_CUSTOMER_SUPPORT` | 任一字段命中`智慧石`  | 页面位置选择/Web_B/我的客服 | 

## 6) 场景卡片（执行区）

### SCN_LIST_REFRESH_RECOMMEND

- **match**
  - `埋点英文名` 以 `list` 开头
  - 或 `埋点描述` 包含：`刷新列表`、`下拉刷新`、`重新拉取列表`
- **normalize**
  - `事件类型`：`浏览`
  - `功能名称`：`推荐列表刷新`
  - `页面位置`：优先匹配推荐相关页面（必须来自 `configs/enums/page_locations.json`）
- **constraints**
  - `功能名称` 不得出现事件词
- **fallback**
  - 页面位置无高置信匹配时，按 `workflows/workflow.md` 兜底

### SCN_SEARCH_RESULT_BROWSE

- **match**
  - `埋点英文名` 包含 `search` 或 `result_list`
  - 且 `埋点描述` 包含 `搜索结果` 或 `检索结果`
- **normalize**
  - `事件类型`：`浏览`
  - `功能名称`：`搜索结果列表查看`
  - `页面位置`：搜索结果对应枚举路径
- **constraints**
  - `功能名称` 不得混入事件词
- **fallback**
  - 页面位置不确定时按 `workflows/workflow.md` 兜底

### SCN_DETAIL_PAGE

- **match**
  - `埋点英文名` 以 `detail` 开头
- **normalize**
  - `事件类型`：`点击`
  - `功能名称`：`查看xx详情页`
  - `页面位置`：详情相关枚举路径
- **constraints**
  - 页面位置必须来自 `configs/enums/page_locations.json`
- **fallback**
  - 无法确定详情页时，按 `workflows/workflow.md` 兜底

### SCN_JOB_PUBLISH_OR_CHANGE_GOVERN

- **match**
  - 命中“B 端职位发布/修改管理”语义
- **normalize**
  - `事件类型`：`点击`
  - `功能名称`：`职位发布` 或 `职位管理`
  - `页面位置`：仅 B 端职位相关页面
- **constraints**
  - 不允许落到 C 端职位页面
- **fallback**
  - 无法确认时按 `workflows/workflow.md` 保守兜底，并标记“场景未确定”

### SCN_EXPECT_JOB_PUBLISH_OR_CHANGE_GOVERN

- **match**
  - 命中“C 端期望职位发布/修改管理”语义
- **normalize**
  - `事件类型`：`点击`
  - `功能名称`：`职位发布` 或 `职位管理`
  - `页面位置`：仅 C 端职位相关页面
- **constraints**
  - 不允许落到 B 端职位页面
- **fallback**
  - 无法确认时按 `workflows/workflow.md` 保守兜底，并标记“场景未确定”

### SCN_EXCHANGE_PHONE

- **match**
  - 基础字段出现“交换电话”相关语义
- **normalize**
  - `事件类型`：`点击`
  - `功能名称`：`交换电话`
  - `页面位置`：消息详情相关页面
- **constraints**
  - 页面位置必须来自枚举集合
- **fallback**
  - 页面位置不确定时按 `workflows/workflow.md` 兜底

### SCN_BIZ_OR_BLOCK

- **match**
  - `埋点英文名` 含 `block`
  - 且 `埋点描述` 或 `埋点中文名` 出现商业阻断词
- **normalize**
  - `事件类型`：按历史信息与描述判断
  - `功能名称`：按 `workflows/workflow.md` 推断
  - `页面位置`：阻断相关页面位置
- **constraints**
  - 页面位置必须来自枚举集合
- **fallback**
  - 无法确定时按 `workflows/workflow.md` 兜底

### SCN_READ_MESSAGES

- **match**
  - `埋点英文名` 含 `read`
  - 且 `埋点描述` 或 `埋点中文名` 出现已读相关词语
- **normalize**
  - `事件类型`：`浏览`
  - `功能名称`：`已读消息`
  - `页面位置`：消息详情相关页面
- **constraints**
  - 功能名称不得混入事件词
- **fallback**
  - 页面位置不确定时按 `workflows/workflow.md` 兜底

### SCN_ITEM_TOOL

- **match**
  - 任一字段命中 `configs/enums/B_items.json` 或 `configs/enums/C_items.json` 的 `tool_names`
- **normalize**
  - `事件类型`：按语义归一
  - `功能名称`：必须保留道具语义
  - `页面位置`：
    - 命中 B 端道具：优先 `Web_B-道具` 及其子路径
    - 命中 C 端道具：优先 C 端道具相关页面
    - 同时命中 B/C：允许多页面位置
- **constraints**
  - 禁止在命中道具后退回无关页面
- **fallback**
  - 无法匹配合法道具页面时，按 `workflows/workflow.md` 兜底
