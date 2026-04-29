# Negative Examples

These examples are not canonical outputs. Use them to identify common violations before Agent B writes the final same-shape result.

## F01 功能名称包含事件词

```json
{
  "埋点id": "bad_001",
  "页面位置": "APP_C-职位列表-搜索",
  "功能名称": "搜索结果列表浏览",
  "事件类型": "浏览",
  "埋点中文名": "C_职位列表_搜索-搜索结果列表浏览-浏览",
  "埋点英文名": "search_result_list_view",
  "埋点描述": "用户在职位搜索结果页浏览搜索结果列表时上报",
  "主被动": "主动",
  "标签": ""
}
```

Why invalid: `功能名称` contains the event word `浏览`. Agent B must minimally correct it to a business feature such as `搜索结果列表查看`.

## M01 事件类型枚举非法

```json
{
  "埋点id": "bad_002",
  "页面位置": "APP_C-职位列表-搜索",
  "功能名称": "搜索结果列表查看",
  "事件类型": "view",
  "埋点中文名": "C_职位列表_搜索-搜索结果列表查看-view",
  "埋点英文名": "search_result_list_view",
  "埋点描述": "用户在职位搜索结果页浏览搜索结果列表时上报",
  "主被动": "主动",
  "标签": ""
}
```

Why invalid: `事件类型` must be one of `点击`、`曝光`、`浏览`、`时长`、`性能`、`其他`.

## F03 页面位置非枚举

```json
{
  "埋点id": "bad_003",
  "页面位置": "职位搜索页",
  "功能名称": "搜索结果列表查看",
  "事件类型": "浏览",
  "埋点中文名": "职位搜索页-搜索结果列表查看-浏览",
  "埋点英文名": "search_result_list_view",
  "埋点描述": "用户在职位搜索结果页浏览搜索结果列表时上报",
  "主被动": "主动",
  "标签": ""
}
```

Why invalid: `页面位置` must match `configs/enums/page_locations.json` or use the documented fallback `无页面位置`.

## F04 中文名结构错误

```json
{
  "埋点id": "bad_004",
  "页面位置": "APP_C-职位列表-搜索",
  "功能名称": "搜索结果列表查看",
  "事件类型": "浏览",
  "埋点中文名": "搜索结果列表查看-C_职位列表_搜索-浏览",
  "埋点英文名": "search_result_list_view",
  "埋点描述": "用户在职位搜索结果页浏览搜索结果列表时上报",
  "主被动": "主动",
  "标签": ""
}
```

Why invalid: `埋点中文名` must be `cn_name-功能名称-事件类型`.

## F06 多值分隔错误

```json
{
  "埋点id": "bad_005",
  "页面位置": "APP_C-消息-消息详情，APP_B-消息-消息详情",
  "功能名称": "已读消息",
  "事件类型": "浏览",
  "埋点中文名": "BC_消息_消息详情-已读消息-浏览",
  "埋点英文名": "message_read_status_view",
  "埋点描述": "用户进入消息详情后消息被标记为已读时上报",
  "主被动": "主动",
  "标签": ""
}
```

Why invalid: multiple page locations must use the English comma `,`.
