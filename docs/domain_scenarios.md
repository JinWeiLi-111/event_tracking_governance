# 存量埋点治理：业务场景卡片（Agent A）

> 用途：按“场景 -> 字段归一”执行快速命中。  
> 目标：命中特定业务模式时，页面位置、功能名称、事件类型保持一致。

## 1) 全局执行规则（必须）

- 先用 `埋点英文名/埋点中文名/埋点描述/页面位置` 进行场景命中，再应用对应卡片的归一规则。
- 若场景规则与 `docs/workflow.md` 冲突，以 `docs/workflow.md` 为准。
- 场景匹配优先级：`英文名前缀或正则` > `中文名关键词` > `描述关键词` > `页面位置原值`。
- 多场景同时命中时，选优先级高者；同优先级时，选关键词命中数更多者。
- 仍无法判定时：`事件类型=其他`，`页面位` 按 `docs/workflow.md` 兜底，并标记“场景未确定”。

## 2) 场景索引（速查）

| 场景ID                                    | 主要触发信号                                     | 归一核心                      |
| ----------------------------------------- | ------------------------------------------------ | ------------------------- |
| `SCN_LIST_REFRESH_RECOMMEND`              | `英文名` 以 `list` 开头，或 `描述` 含“刷新列表/下拉刷新/重新拉取列表”     | `事件类型=浏览`，功能归一为“推荐列表刷新”   |
| `SCN_SEARCH_RESULT_BROWSE`                | `英文名` 含 `search/result_list` 且 `描述` 含“搜索结果/检索结果” | `事件类型=浏览`，功能归一为“搜索结果列表查看” |
| `SCN_DETAIL_PAGE`                         | `英文名` 以 `detail` 开头                        | `事件类型=点击`，功能归一为“查看xx详情页”  |
| `SCN_JOB_PUBLISH_OR_CHANGE_GOVERN`        | 字段语义命中“B端职位发布/修改管理”                              | 仅可落 B 端职位相关页面             |
| `SCN_EXPECT_JOB_PUBLISH_OR_CHANGE_GOVERN` | 字段语义命中“C端期望职位发布/修改管理”                            | 仅可落 C 端职位相关页面             |
| `SCN_EXCHANGE_PHONE`                      | 字段中出现“交换电话”语义                                    | `事件类型=点击`，功能“交换电话”        |
| `SCN_BIZ_OR_BLOCK`                        | `英文名` 含 `block`，且中文名/描述含商业阻断词                    | 页面优先阻断相关位置                |
| `SCN_READ_MESSAGES`                       | `英文名` 含 `read`，且中文名/描述含“已读”                      | `事件类型=浏览`，功能“已读消息”        |
| `SCN_ITEM_TOOL`                           | 任一字段命中 `B_items` 或 `C_items` 道具名                 | 功能必须保留道具语义，页面优先道具路径       |
| `SCN_LOGIN_OR_SIGNUP`                     |  任一字段名字`注册,登录,启动`                              | 页面位置选择登录、注册、启动相关的页面，而不是无页面位置  |
| `SCN_ITEM_AI_ASSITANT`                    | 任一字段语义命中`AI 沟通助手`                              | 页面位置选择道具相关的页面                  |

## 3) 场景卡片（执行区）

### SCN_LIST_REFRESH_RECOMMEND

- **match**
  - `埋点英文名` 以 `list` 开头
  - 或 `埋点描述` 包含：`刷新列表`、`下拉刷新`、`重新拉取列表`
- **normalize**
  - `事件类型`：`浏览`
  - `功能名称`：`推荐列表刷新`
  - `页面位置`：优先匹配“推荐相关”页面路径（必须来自 `configs/enums/page_locations.json`）
- **constraints**
  - `功能名称` 不得出现 `点击/曝光/浏览/时长/其他` 等事件词
- **fallback**
  - 页面位置无高置信匹配时，按服务端/非服务端规则走 `docs/workflow.md` 兜底

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
  - 页面位置不确定时按 `docs/workflow.md` 兜底

### SCN_DETAIL_PAGE

- **match**
  - `埋点英文名` 以 `detail` 开头
- **normalize**
  - `事件类型`：`点击`
  - `功能名称`：`查看xx详情页`（`xx` 需结合输入字段判断）
  - `页面位置`：详情相关枚举路径
- **constraints**
  - 页面位置必须来自 `configs/enums/page_locations.json`
- **fallback**
  - 无法确定详情页时，按 `docs/workflow.md` 兜底

### SCN_JOB_PUBLISH_OR_CHANGE_GOVERN

- **match**
  - 结合所有基础字段，命中“BOSS（B端）提交职位/职位发布/修改管理”语义
- **normalize**
  - `事件类型`：`点击`
  - `功能名称`：`职位发布` 或 `职位管理`
  - `页面位置`：仅 B 端职位相关页面
- **constraints**
  - 不允许落到 C 端职位页面
- **fallback**
  - 无法确认时按 `docs/workflow.md` 保守兜底，并标记“场景未确定”

### SCN_EXPECT_JOB_PUBLISH_OR_CHANGE_GOVERN

- **match**
  - 结合所有基础字段，命中“牛人（C端）提交期望职位/期望职位发布/修改管理”语义
- **normalize**
  - `事件类型`：`点击`
  - `功能名称`：`职位发布` 或 `职位管理`
  - `页面位置`：仅 C 端职位相关页面
- **constraints**
  - 不允许落到 B 端职位页面
- **fallback**
  - 无法确认时按 `docs/workflow.md` 保守兜底，并标记“场景未确定”

### SCN_EXCHANGE_PHONE

- **match**
  - 埋点基础字段出现“交换电话”相关语义
- **normalize**
  - `事件类型`：`点击`
  - `功能名称`：`交换电话`
  - `页面位置`：消息详情相关页面
- **constraints**
  - 页面位置必须来自枚举集合
- **fallback**
  - 页面位置不确定时按 `docs/workflow.md` 兜底

### SCN_BIZ_OR_BLOCK

- **match**
  - `埋点英文名` 含 `block`
  - 且 `埋点描述` 或 `埋点中文名` 出现商业阻断相关词语
- **normalize**
  - `事件类型`：按历史信息与描述判断
  - `功能名称`：按 `docs/workflow.md` 推断
  - `页面位置`：阻断相关页面位置
- **constraints**
  - 页面位置必须来自枚举集合
- **fallback**
  - 无法确定时按 `docs/workflow.md` 兜底

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
  - 页面位置不确定时按 `docs/workflow.md` 兜底

### SCN_ITEM_TOOL

- **match**
  - 任一字段（`埋点中文名/埋点英文名/埋点描述/功能名称`）命中 `configs/enums/B_items.json` 的 `tool_names`
  - 或任一字段命中 `configs/enums/C_items.json` 的 `tool_names`
- **normalize**
  - `事件类型`：按语义归一（如 `click/show/view/other -> 点击/曝光/浏览/其他`）
  - `功能名称`：必须保留道具语义（道具名、道具动作、道具效果）
  - `页面位置`：
    - 命中 B 端道具：优先 `Web_B-道具` 及其子路径
    - 命中 C 端道具：优先 C 端道具相关页面
    - 同时命中 B/C：允许多页面位置
- **constraints**
  - 禁止在命中道具后退回非道具无关页面（除非证据明确且通过校验规则）
- **fallback**
  - 无法匹配合法道具页面时，按 `docs/workflow.md` 兜底

## 4) 示例卡片（最小样例）

### SAMPLE_LIST_REFRESH

- **positive**
  - 输入：`埋点英文名=list--refresh_recommend_job`，`埋点描述=用户下拉后刷新推荐职位列表`
  - 输出：`事件类型=浏览`，`功能名称=推荐列表刷新`，页面位置为推荐相关枚举路径
- **negative**
  - 输入：`埋点英文名=list--refresh_recommend_job`，`功能名称=刷新列表浏览`
  - 问题：功能名称混入事件词 `浏览`
  - 修正：`功能名称=推荐列表刷新`，`事件类型=浏览`

## 5) 维护规则

- 新增业务模式时，新增一个 `SCN_`* 场景卡片，不改已有卡片结构。
- 每个卡片至少包含：`match`、`normalize`、`constraints`、`fallback`。
- 示例区每类高频场景至少保留 1 组正反例。
- 优先沉淀高频错判场景，不追求一次性覆盖全部场景。

