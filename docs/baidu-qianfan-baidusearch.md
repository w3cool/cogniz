# 百度千帆 · 百度AI搜索 API 文档

> 本文档整理自百度智能云千帆「百度 AI 搜索 - 百度搜索」官方 API 参考，涵盖联网搜索接口、阿拉丁卡结构化信息，以及特定 query 干预策略的新增 / 查询 / 删除接口。
>
> - 服务域名：`https://qianfan.baidubce.com`
> - 鉴权方式：API Key（`Authorization: Bearer <API Key>`），详见[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)
> - 文档更新时间：2026-09-28

## 接口索引

| # | 接口 | 方法 | 路径 | 原始文档 |
|---|------|------|------|----------|
| 1 | [百度搜索](#1-百度搜索web_search) | POST | `/v2/ai_search/web_search` | https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5 |
| 2 | [阿拉丁卡结构化信息（beta）](#2-阿拉丁卡结构化信息beta) | — | — | https://cloud.baidu.com/doc/qianfan-api/s/Xmjsa5ct9 |
| 3 | [新增干预项](#3-新增干预项) | POST | `/v2/ai_search/web_search/intervention` | https://cloud.baidu.com/doc/qianfan-api/s/ymlajdi7w |
| 4 | [删除干预项](#4-删除干预项) | DELETE | `/v2/ai_search/web_search/intervention` | https://cloud.baidu.com/doc/qianfan-api/s/lmlak5rye |
| 5 | [查询干预项](#5-查询干预项) | GET | `/v2/ai_search/web_search/intervention` | https://cloud.baidu.com/doc/qianfan-api/s/Omlakcyf4 |

---

## 1. 百度搜索（web_search）

- **原始文档**：https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5
- **接口地址**：`POST https://qianfan.baidubce.com/v2/ai_search/web_search`
- **在线调试**：[千帆 API 调试台](https://console.bce.baidu.com/support/#/api?product=QIANFAN&project=%E5%8D%83%E5%B8%86Agent%E5%BC%80%E5%8F%91%E5%B9%B3%E5%8F%B0&parent=%E7%99%BE%E5%BA%A6AI%E6%90%9C%E7%B4%A2&api=v2%2Fai_search%2Fweb_search&method=post)

**概述**：可根据用户输入 query，搜索全网实时信息，并返回摘要、网址等信息。

**计费**：每月免费额度为 1500 次（按天发放），支持按量后付费（为不影响使用体验，可先去[开通后付费](https://console.bce.baidu.com/qianfan/studio/resource)），默认优先抵扣免费资源。如有其他需求请[联系我们](https://cloud.baidu.com/survey/baiduaisearch.html)，费用详情请查看[计费说明](https://cloud.baidu.com/doc/qianfan/s/1mh4sv6c4)。

**使用方式**：API、[工具及 MCP](https://console.bce.baidu.com/qianfan/tools/toolsCenter/57d4e765-8af5-4ec0-8f9b-47075ec349e0/detail)。

### 权限说明

调用本 API 需使用 API Key 鉴权方式，具体调用流程请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域外，无其它特殊头域。

**Body 参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|:----:|------|
| `messages` | object | 是 | 搜索输入。在百度搜索时仅支持单轮输入，若传入多轮输入，则以用户传入最后的 `content` 为输入查询。 |
| `messages.role` | string | 是 | 角色设定，可选值：`user`（用户）、`assistant`（模型）。 |
| `messages.content` | string | 是 | 对应对话内容，即用户的 query 问题。不能为空，长度限制在 72 个字符以内（一个汉字占两个字符），输入过长时只取前 72 个字符检索。 |
| `query_policy` | object | 否 | query 处理策略，用于控制 query 处理流程中各项能力是否启用。 |
| `query_policy.enable_rewrite` | boolean | 否 | 是否开启 query 改写，默认 `false`；开启后会针对长 query 改写，提升搜索效果，预计增加 10～20ms 搜索耗时。 |
| `search_source` | string | 否 | 使用的搜索引擎版本。固定值：`baidu_search_v2`。 |
| `resource_type_filter` | array&lt;object&gt; | 否 | 搜索模态及返回数量配置。turbo 版仅支持 `web` 类型；standard 版支持网页、视频、图片、阿拉丁。网页 `top_k` 最大 50，视频最大 10，图片最大 30，阿拉丁最大 5。默认值：`[{"type":"web","top_k":20},{"type":"video","top_k":0},{"type":"image","top_k":0},{"type":"aladdin","top_k":0}]`。 |
| `resource_type_filter[].type` | string | 是 | 搜索资源类型。可选值：`web`（网页）、`video`（视频）、`image`（图片）、`aladdin`（阿拉丁）。 |
| `resource_type_filter[].top_k` | integer | 是 | 指定模态最大返回个数。 |
| `edition` | string | 否 | 搜索版本。默认 `standard`，可选值：`standard`（标准版）、`turbo`（增强版）。增强版与标准版计费规则不同，详情查看[计费文档](https://cloud.baidu.com/doc/qianfan/s/1mh4sv6c4)。 |
| `compliance_scene` | string | 否 | 国内外内容控制，仅 `edition=turbo` 时生效。枚举值：`domestic`（国内内容，默认）、`abroad`（国外内容）、`auto`（根据 query 语言自动选择）。 |
| `search_filter` | object | 否 | 根据 SearchFilter 下的子条件做检索过滤。 |
| `search_filter.match` | object | 否 | 条件查询。 |
| `search_filter.match.site` | array&lt;string&gt; | 否 | 指定站点搜索，仅在设置的站点中搜索内容，支持设置 100 个站点。示例：`["tieba.baidu.com","baike.baidu.com"]`。**注意：此为付费功能，目前限时免费中。** |
| `search_filter.match.image` | object | 否 | 图片过滤参数，仅支持 standard 版。 |
| `search_filter.match.image.size` | integer | 否 | 图片尺寸大小，默认 `0`。枚举：0-全部尺寸；4-小图(1px～300px)；5-中图(300px～600px)；6-大图(600～1080px)；7-超大图(1080px 以上)。 |
| `search_filter.match.image.ratio` | integer | 否 | 图片比例，默认 `0`。枚举：0-全部比例；1-细长竖图；2-竖图；3-方图；4-横图；5-细长横图。 |
| `search_filter.match.image.format` | integer | 否 | 图片格式，默认 `0`。枚举：0-全部格式；2-BMP；3-JPG；4-PNG；5-JPEG；6-GIF。 |
| `search_filter.match.image.simi_threshold` | float | 否 | 相似图片识别与过滤，取值 0～1，值越小过滤越严格；传入时会去重相似度大于该阈值的图片。 |
| `search_filter.range` | object | 否 | 范围查询，可用于数值型、日期型字段。详见下方[范围查询（range）说明](#范围查询range说明)。 |
| `search_filter.range.page_time` | object | 否 | 发布时间范围查询（对应响应数据中的 `page_time` 字段）。 |
| `search_filter.range.page_time.gte` | string | 否 | 时间查询参数，大于或等于。 |
| `search_filter.range.page_time.gt` | string | 否 | 时间查询参数，大于。 |
| `search_filter.range.page_time.lte` | string | 否 | 时间查询参数，小于或等于。 |
| `search_filter.range.page_time.lt` | string | 否 | 时间查询参数，小于。 |
| `search_filter.range.geo` | object | 否 | 地理位置信息，仅支持 standard 版。 |
| `search_filter.range.geo.city` | array&lt;string&gt; | 否 | 城市；当前仅支持传入一个城市，直辖市不支持指定区级行政区。普通城市如「沈阳」，直辖市如「北京」。 |
| `block_websites` | array&lt;string&gt; | 否 | 需要屏蔽的站点列表。过滤属于该站点及其子站点的搜索结果。示例：`["tieba.baidu.com"]`。 |
| `search_recency_filter` | string | 否 | 根据网页发布时间筛选。枚举值：`week`（最近 7 天）、`month`（最近 30 天）、`semiyear`（最近 180 天）、`year`（最近 365 天）。 |
| `safe_search` | boolean | 否 | 是否开启安全搜索，默认 `false`。开启后采用更严格的风控策略，部分可能涉黄、涉恐 query 将不返回搜索结果。 |
| `config_id` | string | 否 | query 干预配置项的配置 ID，默认为空。传入时会根据 `config_id` 中的策略进行 query 干预。 |
| `chunks_per_doc` | integer | 否 | 配置 snippet 返回数量，默认 `1`，取值 1～3。结果通过 `snippet` 字段返回，多个 Chunk 使用 `[...]` 分隔；仅支持 turbo 版。 |

> **阿拉丁（aladdin）使用注意**：① 不支持站点、时效过滤；② 建议搭配网页模态使用，增加搜索返回数量；③ 返回参数为 beta 版本，后续可能变更。

#### 范围查询（range）说明

语法格式：

```jsonc
"range": {
  "{field}": {
    "gte": "{lowerBound}",
    "gt":  "{lowerBound}",
    "lte": "{upperBound}",
    "lt":  "{upperBound}"
  }
}
```

- **实体（field）**：`page_time` 为发布时间的实体名，表示针对 `page_time` 做范围查询，对应响应数据中的 `page_time` 字段。网页发布时间的筛选功能只适用于可利用与可展现库，其他结果（如视频等）不召回。
- **查询范围（lowerBound / upperBound）**：
  1. **指定日期**：格式 `YYYY-MM-DD`，例如：
     ```json
     "range": { "page_time": { "gte": "2025-11-01", "lte": "2025-11-04" } }
     ```
  2. **固定套餐**：支持的时间单位 `y`（年）、`M`（月）、`w`（周）、`d`（日）。`now` 表示当前时间，可添加数学表达式（`-1w` 减 1 周、`-1M` 减 1 月、`-1y` 减 1 年、`/d` 归一化到当天起始/结束时间）。可用套餐：
     - `now/d`
     - `now-1w/d`：一周
     - `now-2w/d`：两周
     - `now-1M/d`：一个月
     - `now-3M/d`：三个月
     - `now-6M/d`：六个月
     - `now-1y/d`：一年

**参数限制说明**：
1. `lte` 使用注意：range 范围会参与检索系统的 cache key 计算，`lte` 在做向上归一舍入后，由于 cache 可能导致结果时效性落后于 match 指定的 `lte` 值。
2. 起始（lowerBound）和截止（upperBound）时间必须同时存在，否则该功能不生效。
3. `gte` 和 `gt` 只传其中一个即可，都传只生效 `gt`；`lte` 和 `lt` 只传其中一个即可，都传只生效 `lt`。

> **page_time 示例**（假设 now 为 2024-07-16，查询当天前 7 天、不含当天发布的网页结果）：
> ```json
> { "filter": { "range": { "page_time": { "gte": "now-1w/d", "lt": "now/d" } } } }
> ```
> - `gte` `now-1w/d`：向下舍入，即 ≥ 2024-07-09 00:00:00（含 07-09 完整天）。
> - `gt` `now-1w/d`：向上舍入，即 > 2024-07-09 23:59:59（不含 07-09 完整天）。
> - `lte` `now-1w/d`：向上舍入，即 ≤ 2024-07-09 23:59:59（含 07-09 完整天）。
> - `lt` `now-1w/d`：向下舍入，即 < 2024-07-09 00:00:00（不含 07-09 完整天）。

### 请求结构

```http
POST /v2/ai_search/web_search HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json

{
  "messages": [
    {
      "content": "北京有哪些旅游景区",
      "role": "user"
    }
  ],
  "search_source": "baidu_search_v2",
  "resource_type_filter": [{ "type": "web", "top_k": 20 }],
  "search_filter": {
    "match": {
      "site": ["www.weather.com.cn"]
    }
  },
  "search_recency_filter": "year"
}
```

### 示例代码

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/web_search' \
--header 'Authorization: Bearer <YOUR_BAIDU_API_KEY>' \
--header 'Content-Type: application/json' \
--data '{
  "messages": [
    {
      "role": "user",
      "content": "北京今日天气与出行建议"
    }
  ],
  "search_source": "baidu_search_v2",
  "edition": "standard",
  "resource_type_filter": [
    {"type": "web", "top_k": 10},
    {"type": "aladdin", "top_k": 2}
  ],
  "search_filter": {
    "range": {
      "page_time": {
        "gte": "now-1w/d",
        "lte": "now/d"
      }
    }
  },
  "query_policy": {
    "enable_rewrite": true
  }
}'
```

### 返回响应

**Headers**：除公共头域外，无其它特殊头域。

**返回参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|:----:|------|
| `request_id` | string | 是 | 请求 ID。 |
| `code` | string | 否 | 错误码，当发生异常时返回。 |
| `message` | string | 否 | 错误消息，当发生异常时返回。 |
| `references` | array&lt;object&gt; | 否 | 模型回答详情列表。 |
| `references[].id` | integer | 是 | 引用编号 1、2、3。 |
| `references[].title` | string | 是 | 网页标题。 |
| `references[].url` | string | 是 | 网页地址。 |
| `references[].web_anchor` | string | 是 | 网站锚文本或网站标题。 |
| `references[].icon` | string | 否 | 网站图标地址。 |
| `references[].website` | string | 否 | 站点名称。 |
| `references[].snippet` | string | 否 | 网页内容摘要。 |
| `references[].content` | string | 否 | 网页内容，显示 2000 字以内的相关信息原文片段（当前与 `snippet` 内容一致）。 |
| `references[].date` | string | 否 | 网页日期。 |
| `references[].type` | string | 否 | 检索资源类型：`web`（网页）、`image`（图像内容）、`video`（视频内容）。 |
| `references[].image` | object | 否 | 图片详情。 |
| `references[].image.url` | string | 否 | 图片链接。 |
| `references[].image.height` | string | 否 | 图片高度。 |
| `references[].image.width` | string | 否 | 图片宽度。 |
| `references[].video` | object | 否 | 视频详情。 |
| `references[].video.url` | string | 否 | 视频链接。 |
| `references[].video.height` | string | 否 | 视频高度。 |
| `references[].video.width` | string | 否 | 视频宽度。 |
| `references[].video.size` | string | 否 | 视频大小，单位 Bytes。 |
| `references[].video.duration` | string | 否 | 视频长度，单位秒。 |
| `references[].video.hover_pic` | string | 否 | 视频封面图。 |
| `references[].is_aladdin` | boolean | 否 | 是否为阿拉丁内容。 |
| `references[].aladdin` | string | 否 | 阿拉丁详细内容，参考[阿拉丁卡结构化信息](#2-阿拉丁卡结构化信息beta)。 |
| `references[].web_extensions` | object | 否 | 网页扩展信息。 |
| `references[].web_extensions.images` | array&lt;object&gt; | 否 | 网页相关图片。 |
| `references[].web_extensions.images[].url` | string | 否 | 图片链接。 |
| `references[].web_extensions.images[].height` | string | 否 | 图片高度。 |
| `references[].web_extensions.images[].width` | string | 否 | 图片宽度。 |
| `references[].web_extensions.author_info` | object | 否 | 作者信息，仅百家号站点存在。 |
| `references[].web_extensions.author_info.name` | string | 否 | 作者名字。 |
| `references[].web_extensions.author_info.signature` | string | 否 | 作者签名。 |
| `references[].web_extensions.author_info.verified_type` | integer | 否 | 作者认证类型。 |

**正确响应示例**：

```json
{
  "references": [
    {
      "content": "河北天气预报,及时准确发布中央气象台天气信息,便捷查询河北今日天气,河北周末天气,河北一周天气预报,河北蓝天预报,河北天气预报,河北40日天气预报,还提供河北的生活指数、健康指数、交通...",
      "date": "2025-04-27 18:02:00",
      "icon": null,
      "id": 1,
      "image": null,
      "title": "【河北天气】河北天气预报,蓝天,蓝天预报,雾霾,雾霾...",
      "type": "web",
      "url": "https://www.weather.com.cn/html/weather/101031600.shtml",
      "video": null,
      "web_anchor": "【河北天气】河北天气预报,蓝天,蓝天预报,雾霾,雾霾..."
    },
    {
      "content": "保定天气预报,及时准确发布中央气象台天气信息,便捷查询保定今日天气,保定周末天气,保定一周天气预报,保定蓝天预报,保定天气预报,保定40日天气预报,还提供保定的生活指数、健康指数、交通...",
      "date": "2025-05-20 11:58:00",
      "icon": null,
      "id": 2,
      "image": null,
      "title": "保定天气预报,保定7天天气预报,保定15天天气预报,保定...",
      "type": "web",
      "url": "https://www.weather.com.cn/weather/101090201.shtml",
      "video": null,
      "web_anchor": "保定天气预报,保定7天天气预报,保定15天天气预报,保定..."
    },
    {
      "content": "河北省气象台2025年05月23日11时发布天气预报: 今天下午到夜间,保定西部、石家庄西部、邢台西部阴有小雨或零星小雨转晴,其他地区阴转晴。最高气温,张家口、承德北部、保定西北部13～17...",
      "date": "2025-05-23 00:00:00",
      "icon": null,
      "id": 3,
      "image": null,
      "title": "今天西部部分地区仍有降水 其它地区阴转晴-河北首页...",
      "type": "web",
      "url": "http://hebei.weather.com.cn/tqxs/4190923_m.shtml",
      "video": null,
      "web_anchor": "今天西部部分地区仍有降水 其它地区阴转晴-河北首页..."
    },
    {
      "content": "河北省气象台2025年05月22日05时发布天气预报 今天白天,保定、廊坊及以北地区阴有小雨或阵雨,其中张家口、保定西北部有中到大雨;其他地区多云转阴有小雨或阵雨,其中邯郸大部有中雨。...",
      "date": "2025-05-22 09:07:22",
      "icon": null,
      "id": 4,
      "image": null,
      "title": "今天白天到夜间,我省大部分地区有降水-河北首页-中国...",
      "type": "web",
      "url": "http://hebei.weather.com.cn/tqxs/4189523_m.shtml",
      "video": null,
      "web_anchor": "今天白天到夜间,我省大部分地区有降水-河北首页-中国..."
    }
  ],
  "request_id": "ca749cb1-26db-4ff6-9735-f7b472d59003"
}
```

**错误响应示例**：

```json
{
  "requestId": "00000000-0000-0000-0000-000000000000",
  "code": 216003,
  "message": "Authentication error: ( [Code: InvalidHTTPAuthHeader; Message: Fail to parse apikey authorization; RequestId: ea6ffeca-a136-401b-ba30-61c910c02ead] )"
}
```

### 错误码

| 错误码 | 描述 |
|--------|------|
| 400 | 客户端请求参数错误 |
| 500 | 服务端执行错误 |
| 501 | 调用模型服务超时 |
| 502 | 模型流式输出超时 |
| 其它 | 详见[模型返回错误码](https://cloud.baidu.com/doc/qianfan/s/Pmh4sv5qa)。 |

---

## 2. 阿拉丁卡结构化信息（beta）

- **原始文档**：https://cloud.baidu.com/doc/qianfan-api/s/Xmjsa5ct9

### 概述

本文档描述了百度搜索接口中返回的阿拉丁卡片的结构化信息。当前阿拉丁卡正在快速开放中，对于已经开发的阿拉丁卡，响应参数和数据结构可能存在进一步优化。

> 阿拉丁卡内容通过[百度搜索](#1-百度搜索web_search)接口 `references[].aladdin` 字段返回（需将 `resource_type_filter` 中 `aladdin` 的 `top_k` 设为大于 0）。
>
> 下表使用 `+` 前缀表示字段的嵌套层级（`+` 为一级子字段，`++` 为二级子字段，以此类推）。

### 天气（weather）

**易命中该卡的用户 query**：天气相关的问题。示例：明天北京天气如何。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `weather` |
| `day_forecast` | object | 天级天气信息 | `{}` |
| `+info` | array | 每日天气预报列表 | `[]` |
| `++date` | string | 日期 | `2025-08-15` |
| `++humidity` | object | 湿度信息 | `{}` |
| `+++text` | string | 湿度值 | `82` |
| `+++tip` | string | 湿度提示 | `湿度` |
| `+pm25` | object | PM2.5 信息 | `{}` |
| `++list_quality` | object | 空气质量详情 | `{}` |
| `+++list_aqi_val` | string | AQI 值 | `60` |
| `+++list_value` | string | 空气质量等级 | `良` |
| `+precipitation_probability` | string | 总降水概率 | `70%` |
| `+temperature_day` | string | 白天温度 | `30` |
| `+temperature_night` | string | 夜晚温度 | `24` |
| `+weather_day` | string | 白天天气 | `雷阵雨` |
| `+weather_night` | string | 夜晚天气 | `中雨` |
| `+wind_direction_day` | string | 白天风向 | `南风` |
| `+wind_direction_night` | string | 夜晚风向 | `东北风` |
| `+wind_power_day` | string | 白天风力 | `1级` |
| `+wind_power_night` | string | 夜晚风力 | `1级` |
| `f1h` | object | 每 1h 天气 | `{}` |
| `+info` | array | 每小时天气预报列表 | `[]` |
| `++hour` | string | 小时时间戳 (YYYYMMDDHH) | `2025081519` |
| `++pm25` | object | PM2.5 信息 | `{}` |
| `+++list_aqi_val` | string | AQI 值 | `60` |
| `+++list_value` | string | 空气质量等级 | `良` |
| `++precipitation` | string | 降水量 | `1.0` |
| `++precipitation_probability` | string | 降水概率 | |
| `++temperature` | string | 温度 | `28` |
| `++wind_direction` | string | 风向 | `西南风` |
| `++wind_power` | string | 风力 | `3级` |
| `yesterday_15d` | object | 过去 15 日天气（示例中为昨日天气信息） | `{}` |
| `+date` | string | 日期 | `2025-08-14` |
| `+pm25` | object | PM2.5 信息 | `{}` |
| `++list_quality` | object | 空气质量详情 | `{}` |
| `+++list_aqi_val` | string | AQI 值 | `29` |
| `+++list_value` | string | 空气质量等级 | `优` |
| `+temperature_day` | string | 白天温度 | `30` |
| `+temperature_night` | string | 夜晚温度 | `23` |
| `+weather_day` | string | 白天天气 | `雷阵雨` |
| `+weather_night` | string | 夜晚天气 | `雷阵雨` |
| `+wind_direction_day` | string | 白天风向 | `东北风` |
| `+wind_direction_night` | string | 夜晚风向 | `北风` |
| `+wind_power_day` | string | 白天风力 | `1级` |
| `+wind_power_night` | string | 夜晚风力 | `1级` |

### 彩票开奖（lottery_draw）

**易命中该卡的用户 query**：××彩票开奖结果。必须是某一个具体的彩票名称，而且是确实存在的彩票名称，比如：大乐透、排列 5 体彩、双色球、福彩 3d、七星彩等具体彩票的开奖结果，不要过多的描述性语言，否则无法命中。示例：排列 5 体彩开奖。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `lottery_draw` |
| `data` | array | 开奖结果信息 | `[]` |
| `+award_description` | array | 开奖结果 | `["一等奖：12注，每注6161412元", "二等奖：136注，每注128096元"]` |
| `+slink` | array | 玩法说明、往期开奖、公益金、开奖直播 | `[]` |
| `++name` | string | 链接名称 | `"玩法说明"` |
| `++text` | string | 链接文本 | `"玩法说明"` |
| `++wap_url` | string | 链接地址 | `"https://www.cwl.gov.cn/fcpz/yxjs/ssq/"` |

### 彩票走势（lottery_trend）

**易命中该卡的用户 query**：××彩票名称。必须是某一个具体的彩票名称，而且是确实存在的彩票名称，比如：大乐透、排列 5 体彩、双色球、福彩 3d、七星彩等具体彩票，不要过多的描述性语言，否则无法命中。示例：双色球。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `lottery_trend` |
| `sub_result` | array | 走势详情落地页列表 | |
| `+sub_supp_info` | string | 走势详情页信息，通常包含彩票类型、功能、开奖时间等 | `"双色球 专家预测 开奖直播 往期开奖 玩法说明 开奖 2025-08-14 21:15:00"` |
| `+sub_title` | string | 走势详情页的标题 | `"双色球-彩票走势图"` |
| `+sub_url` | string | 走势详情页的跳转链接 | `https://lotto.sina.cn/trend/qxc_qlc_proxy.d.html?lottoType=ssq&actionType=chzs` |
| `provider` | array | 各类走势结果提供方列表 | |
| `+image` | string | 走势图相关的图片 URL 地址 | `https://edge.caitong.sina.com.cn/caitong/lottery/zst_cover/ssq_chzs.jpg` |
| `+intent` | object | 意图信息，包含彩票名称和省份 | |
| `++lottery_name` | string | 彩票名称 | `"双色球"` |
| `++lottery_province` | string | 彩票所属省份 | `""` |
| `+sub_title` | string | 走势结果的开奖时间 | `"开奖 2025-08-14 21:15:00"` |
| `+tag_list` | array | 走势图分类标签列表，每个标签对应一个走势图类型 | |
| `++text` | string | 标签的显示文本，如「基本走势」「红球走势」等 | `"基本走势"` |
| `++url` | object | 标签对应的走势图 URL 详细信息 | |
| `+++src` | string | 源 URL | `https://lotto.sina.cn/trend/qxc_qlc_proxy.d.html?lottoType=ssq&actionType=chzs` |

### 日历（calender）

**易命中该卡的用户 query**：必须输入日历、万年历这样的字样，或者具体的日期。示例：2025 年 10 月 1 号。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `calender` |
| `select_day` | string | 日期信息 | `2025-10-1` |
| `almanac` | array | 完整日期信息说明 | |
| `+animal` | string | 生肖 | `蛇` |
| `+avoid` | string | 农历当日不宜做的事情 | `买房.搬新房.开业.祭祀.补垣.塞穴` |
| `+cn_day` | string | 星期几的中文表示 | `五` |
| `+day` | string | 公历日期（日） | `24` |
| `+festival_list` | string | 节日名称列表，逗号分隔 | `程序员节,联合国日` |
| `+gz_date` | string | 农历当日的天干地支 | `丙寅` |
| `+gz_month` | string | 农历当月的月干地支 | `丙戌` |
| `+gz_year` | string | 农历当年的年干地支 | `乙巳` |
| `+l_date` | string | 农历日期（初几） | `初四` |
| `+l_month` | string | 农历月份（中文） | `九` |
| `+lunar_date` | string | 农历日期（数字） | `4` |
| `+lunar_month` | string | 农历月份（数字） | `9` |
| `+lunar_year` | string | 农历年份 | `2025` |
| `+month` | string | 公历月份 | `10` |
| `+suit` | string | 农历当日适宜做的事情 | `安葬.入殓.馀事勿取.成服.除服.破土.迁坟` |
| `+value` | string | 节日名称，空格分隔 | `程序员节 联合国日` |
| `+year` | string | 公历年份 | `2025` |
| `+yj_jump_url` | string | 宜忌跳转 URL | `https://mobile.51wnl-cq.com/huangli_tab_h5/?posId=BDSS&STIME=2025-10-24` |

### 单词翻译（word_translate）

**易命中该卡的用户 query**：需要输入单个单词，不能多个单词，不能有中文，只能是存在的单个单词，否则无法命中。示例：good。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `word_translate` |
| `origin_query` | string | 原始 query | `"good"` |
| `extra` | object | 单词相关变形介绍 | |
| `+transform` | object | 单词变形信息 | |
| `++word_er` | string | 比较级 | `"better"` |
| `++word_est` | string | 最高级 | `"best"` |
| `++word_pl` | string | 复数形式 | `"goods"` |
| `result_new` | object | 翻译结果 | |
| `+part` | array | 词性及释义列表 | |
| `++mean` | array | 释义列表 | |
| `+++text` | string | 释义文本 | `"好的"` |
| `++part_name` | string | 词性 | `"adj."` |

### 车型信息（car_information）

**易命中该卡的用户 query**：需要指定具体的车型号，比如：比亚迪 g6、东风风神 l8、宝马 6 等车型，否则无法命中。也不要使用疑问句、问题之类，比如「宝马 6 系车型有哪些」，直接输入「宝马 6 系车型」即可。示例：小米 SU7。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `car_information` |
| `sub_result` | array | 相关车型 | |
| `+sub_title` | string | 标题 | `"小米汽车小米SU7-车型大全"` |
| `+sub_url` | string | 详情页链接 | `https://m.yoojia.com/s-1006962?sa=ala_4526_title` |
| `dealer_price` | string | 成交价 | `"21.59-29.99万"` |
| `dealer_source` | string | 成交来源 | `"zhijia"` |
| `engine_drive_type` | string | 驱动方式 | `"暂无"` |
| `engine_oil_standard` | string | 环保标准 | `"暂无"` |
| `engine_oil_type` | string | 燃料类型 | `"暂无"` |
| `guide_price` | string | 经销商价格 | `"21.59-29.99万"` |
| `header_title` | string | 车系名称 | `"小米汽车小米SU7"` |
| `img_list` | array&lt;string&gt; | 车型图 | `["https://youjia-image.cdn.bcebos.com/modelImage/....jpg@!thumbnail"]` |
| `kingkong_data` | array&lt;string&gt; | 车型参数详情页 | `["https://m.yoojia.com/pages/parameter/index?serid=1006962&hasSummary=1"]` |
| `oil` | string | 综合油耗 | `"暂无"` |
| `parameter_list` | array | 关键参数 | |
| `+key` | string | 参数名称 | `"续航"` |
| `+value` | string | 参数值 | `"700-830 Km"` |

### 作文（composition）

**易命中该卡的用户 query**：作文题目查询。示例：我最爱的玩具作文。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `composition` |
| `ori_query` | string | 查询作文题目 | `"我最爱的玩具作文"` |
| `res_num` | string | 资源数量 | `"20"` |
| `pc_url` | string | 作文列表 | `https://easylearn.baidu.com/edu-page/tiangong/composition/list?...` |

### 人物百科（character）

**易命中该卡的用户 query**：需指定明星查询。示例：孙怡、刘德华。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `character` |
| `name` | string | 人物姓名 | `"孙怡"` |
| `intro` | array | 人物标签 | `["中国内地影视女演员"]` |
| `attribute` | array | 人物信息 | `["32岁", "170cm", "双子座", "A型"]` |
| `other_attribute` | array | 人物代表作 | `代表作品:十五年等待候鸟` |
| `desc` | string | 人物介绍 | `"孙怡，1993年6月4日出生于吉林省集安市，中国内地女演员……"` |
| `url` | string | 明星主页链接 | `https://author.baidu.com/home/711` |

### 找商品（wares）

**易命中该卡的用户 query**：输入商品词，查询商品列表。示例：沧州装修。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `wares` |
| `title` | string | 标题 | `"沧州装修 - 商品批发价格 - 百度爱采购"` |
| `product_list` | array | 产品列表 | |
| `+fullname` | string | 商品全名 | `"沧州 老房翻新/新房装修=齐家网=装修报价明细"` |
| `+fullprovidername` | string | 提供商名称 | `"上海齐家网信息科技股份有限公司"` |
| `+price` | string | 商品价格 | `"面议"` |
| `+show_address` | string | 显示地址 | `"江苏常州"` |
| `+jump_url` | string | 跳转 URL | `https://b2b.baidu.com/b2bsearch/jump?...` |

### 找厂家（factory）

**易命中该卡的用户 query**：输入商品词，查询厂家列表。示例：长沙办公桌批发市场在哪里。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `factory` |
| `title` | string | 标题 | `"长沙办公桌 - 精选厂家 - 百度爱采购"` |
| `list` | array | 厂家列表 | |
| `+fullprovidername` | string | 企业名称 | `"河南天卓家具有限公司"` |
| `+business_scope` | string | 企业经营范围 | `"办公桌、办公家具、幼儿园家具、屏风隔断桌……"` |
| `+jump_url` | string | 跳转 URL | `https://b2b.baidu.com/b2bsearch/jump?...` |

### 查企业（enterprise）

**易命中该卡的用户 query**：输入公司名，查询公司基础客观信息和售卖商品信息。示例：泰星减速机股份有限公司。

| 名称 | 类型 | 描述 | 示例值 |
|------|------|------|--------|
| `aladdin_resource_type` | string | 阿拉丁资源类型 | 固定值: `enterprise` |
| `list` | array | 企业列表 | |
| `+enterprise_name` | string | 企业名称 | `"泰星减速机股份有限公司"` |
| `+registered_capital` | string | 注册资本 | `"7658万元"` |
| `+registered_address` | string | 注册地址 | `"江苏省泰兴市姚王镇泰姚北路10号"` |
| `+operation_scope` | string | 企业经营范围 | `"减速机、齿轮箱、油冷式电动滚筒……"` |
| `+prod_list` | array | 产品列表 | |
| `++fullname` | string | 企业的商品名称 | `"泰星减速机股份 硬齿面圆柱齿轮系列 机械传动配件 坚固耐用"` |
| `++price` | string | 商品价格 | `"4100.00"` |
| `++jump_url` | string | 跳转 URL | `https://b2b.baidu.com/b2bsearch/jump?...` |

---

## 3. 新增干预项

- **原始文档**：https://cloud.baidu.com/doc/qianfan-api/s/ymlajdi7w
- **接口地址**：`POST https://qianfan.baidubce.com/v2/ai_search/web_search/intervention`

在调用百度搜索 API 进行联网搜索时，可设置一系列特定的用户输入，通过完全匹配、语义匹配或关键词匹配的方式命中后，进行联网搜索。

### 权限说明

调用本文 API 需使用 API Key 鉴权方式，具体调用流程请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域外，无其它特殊头域。

**Body 参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|:----:|------|
| `query` | string | 是 | 问答 query，不超过 256 个字符。 |
| `config_id` | string | 是 | 策略配置 id，需要提前调用配置接口配置 id（config_id 配置[请参考文档](https://cloud.baidu.com/doc/qianfan-api/s/0mbt1iwfq)）。 |
| `query_match_strategy` | object | 是 | query 匹配策略。 |
| `query_match_strategy.name` | string | 否 | 匹配策略：`exact`（完全匹配）、`semantic`（语义）、`keyword`（关键词匹配）。 |
| `query_match_strategy.similarity_threshold` | float | 否 | 语义匹配阈值，0～1 之间，默认 0.9。 |
| `query_match_strategy.keywords` | string | 否 | 关键词匹配时，设置用于匹配的关键词，长度不超过 256。 |
| `result` | object | 是 | 干预策略。 |
| `result.documents` | array&lt;object&gt; | 否 | 预置回答策略。 |
| `result.documents[].id` | string | 是 | 文档唯一标识。 |
| `result.documents[].url` | string | 是 | 文档 URL 地址。 |
| `result.documents[].title` | string | 否 | 文档标题。 |
| `result.documents[].date` | string | 否 | 网页发布时间。 |
| `result.documents[].content` | string | 否 | 文档正文内容。 |
| `result.documents[].icon` | string | 否 | 图标 URL。 |
| `result.documents[].web_anchor` | string | 否 | 网页来源。 |
| `result.documents[].type` | string | 否 | 资源类型。 |
| `result.documents[].website` | string | 否 | 站点名称。 |
| `result.documents[].snippet` | string | 否 | 摘要文本。 |
| `result.documents[].rerank_score` | float | 否 | 重排序分数。 |
| `result.documents[].authority_score` | float | 否 | 权威性分数。 |
| `result.documents[].markdown_text` | string | 否 | Markdown 格式文本。 |
| `result.documents[].is_aladdin` | boolean | 否 | 是否来自阿拉丁。 |
| `result.documents[].aladdin` | object | 否 | 阿拉丁详细内容，详见[阿拉丁卡结构化信息](#2-阿拉丁卡结构化信息beta)。 |
| `result.documents[].image` | object | 否 | 图片信息。 |
| `result.documents[].image.url` | string | 否 | 图片链接。 |
| `result.documents[].image.height` | string | 否 | 图片高度。 |
| `result.documents[].image.width` | string | 否 | 图片宽度。 |
| `result.documents[].video` | object | 否 | 视频信息。 |
| `result.documents[].video.url` | string | 否 | 视频链接。 |
| `result.documents[].video.height` | string | 否 | 视频高度。 |
| `result.documents[].video.width` | string | 否 | 视频宽度。 |
| `result.documents[].video.size` | string | 否 | 视频大小，单位 Bytes。 |
| `result.documents[].video.hover_pic` | string | 否 | 视频封面图。 |
| `result.documents[].video.duration` | string | 否 | 视频长度，单位秒。 |
| `result.documents[].web_extesions` | object | 否 | 网页扩展信息。 |
| `result.documents[].web_extesions.images` | array&lt;object&gt; | 否 | 网页相关图片。 |
| `result.documents[].web_extesions.images[].url` | string | 否 | 图片链接。 |
| `result.documents[].web_extesions.images[].height` | string | 否 | 图片高度。 |
| `result.documents[].web_extesions.images[].width` | string | 否 | 图片宽度。 |

> 注：`web_extesions` 字段名沿用官方文档拼写。

### 请求结构

```http
POST /v2/ai_search/web_search/intervention
Content-Type: application/json
Authorization: Bearer <API Key>

{
  "query": "2026年春节放假时间",
  "config_id": "",
  "query_match_strategy": {
    "name": "exact"
  },
  "result": {
    "documents": [
      {
        "id": 1,
        "url": "https://www.gov.cn/zhengce/content/2025-11/20/content_6968789.htm",
        "title": "2026年春节放假安排通知",
        "date": "2025-11-20",
        "content": "2026年春节放假时间为2月10日至16日放假调休，共7天。2月8日（星期日）、2月17日（星期一）上班。",
        "icon": "https://www.gov.cn/favicon.ico",
        "web_anchor": "中国政府网",
        "type": "web",
        "website": "www.gov.cn",
        "video": null,
        "image": null,
        "is_aladdin": false,
        "aladdin": null,
        "snippet": "2026年春节放假时间为2月10日至16日放假调休，共7天...",
        "web_extensions": null,
        "rerank_score": 0.98,
        "authority_score": 0.95,
        "markdown_text": "## 2026年春节放假安排\n\n2026年春节放假时间为2月10日至16日放假调休，共7天。2月8日（星期日）、2月17日（星期一）上班。"
      },
      {
        "id": 2,
        "url": "https://example.com/2026-spring-festival.jpg",
        "title": "2026春节放假日历",
        "date": "2025-11-21",
        "content": "2026年春节放假日历高清版，包含调休安排和出行提示。",
        "icon": "",
        "web_anchor": "",
        "type": "image",
        "website": "",
        "video": null,
        "image": {
          "url": "https://example.com/2026-spring-festival.jpg",
          "height": "1080",
          "width": "1920"
        },
        "is_aladdin": false,
        "aladdin": null,
        "snippet": "",
        "web_extensions": {
          "images": [
            {
              "url": "https://example.com/2026-spring-festival-1.jpg",
              "height": "720",
              "width": "1080"
            }
          ]
        },
        "rerank_score": null,
        "authority_score": null,
        "markdown_text": ""
      }
    ]
  }
}
```

### 示例代码

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/web_search/intervention' \
--header 'Authorization: Bearer <API Key>' \
--header 'content-type: application/json' \
--data '
{
  "query": "2026年春节放假时间",
  "config_id": "",
  "query_match_strategy": {
    "name": "exact"
  },
  "result": {
    "documents": [
      {
        "id": 1,
        "url": "https://www.gov.cn/zhengce/content/2025-11/20/content_6968789.htm",
        "title": "2026年春节放假安排通知",
        "date": "2025-11-20",
        "content": "2026年春节放假时间为2月10日至16日放假调休，共7天。2月8日（星期日）、2月17日（星期一）上班。",
        "icon": "https://www.gov.cn/favicon.ico",
        "web_anchor": "中国政府网",
        "type": "web",
        "website": "www.gov.cn",
        "video": null,
        "image": null,
        "is_aladdin": false,
        "aladdin": null,
        "snippet": "2026年春节放假时间为2月10日至16日放假调休，共7天...",
        "web_extensions": null,
        "rerank_score": 0.98,
        "authority_score": 0.95,
        "markdown_text": "## 2026年春节放假安排\n\n2026年春节放假时间为2月10日至16日放假调休，共7天。2月8日（星期日）、2月17日（星期一）上班。"
      },
      {
        "id": 2,
        "url": "https://example.com/2026-spring-festival.jpg",
        "title": "2026春节放假日历",
        "date": "2025-11-21",
        "content": "2026年春节放假日历高清版，包含调休安排和出行提示。",
        "icon": "",
        "web_anchor": "",
        "type": "image",
        "website": "",
        "video": null,
        "image": {
          "url": "https://example.com/2026-spring-festival.jpg",
          "height": "1080",
          "width": "1920"
        },
        "is_aladdin": false,
        "aladdin": null,
        "snippet": "",
        "web_extensions": {
          "images": [
            {
              "url": "https://example.com/2026-spring-festival-1.jpg",
              "height": "720",
              "width": "1080"
            }
          ]
        },
        "rerank_score": null,
        "authority_score": null,
        "markdown_text": ""
      }
    ]
  }
}'
```

### 返回响应

**Headers**：除公共头域外，无其它特殊头域。

**返回参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|:----:|------|
| `request_id` | string | 否 | 请求 id。 |

**响应示例**：

```json
{ "request_id": "123" }
```

---

## 4. 删除干预项

- **原始文档**：https://cloud.baidu.com/doc/qianfan-api/s/lmlak5rye
- **接口地址**：`DELETE https://qianfan.baidubce.com/v2/ai_search/web_search/intervention`

### 权限说明

调用本文 API 需使用 API Key 鉴权方式，具体调用流程请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域外，无其它特殊头域。

**Query 参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|:----:|------|
| `query` | string | 是 | 请求前需对 `query` 参数进行 URL Encode 编码。 |
| `config_id` | string | 否 | 用户配置 ID。如果为空，则只查询全局干预；如果不为空，则先查全局干预，再根据 `config_id` 查询用户特定的干预策略。 |

### 请求结构

```http
DELETE /v2/ai_search/web_search/intervention HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json

query=%E5%B0%8F%E7%B1%B3%E6%98%AF%E7%BB%84%E8%A3%85%E5%8E%82%E5%90%97%EF%BC%9F
```

### 示例代码

```bash
curl -X "DELETE" \
-H "Authorization: Bearer <API Key>" \
--location 'https://qianfan.baidubce.com/v2/ai_search/web_search/intervention?query=%E5%B0%8F%E7%B1%B3%E6%98%AF%E7%BB%84%E8%A3%85%E5%8E%82%E5%90%97%EF%BC%9F'
```

### 返回响应

**Headers**：除公共头域外，无其它特殊头域。

**返回参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|:----:|------|
| `request_id` | string | 是 | 请求 request_id。 |
| `code` | string | 否 | 错误代码，当发生异常时返回。 |
| `message` | string | 否 | 错误消息，当发生异常时返回。 |

---

## 5. 查询干预项

- **原始文档**：https://cloud.baidu.com/doc/qianfan-api/s/Omlakcyf4
- **接口地址**：`GET https://qianfan.baidubce.com/v2/ai_search/web_search/intervention`

### 权限说明

调用本文 API 需使用 API Key 鉴权方式，具体调用流程请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域外，无其它特殊头域。

**Query 参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|:----:|------|
| `offset` | string | 否 | 偏移量，默认为 0。 |
| `limit` | string | 否 | 条数限制，最大不超过 100，默认为 10。 |
| `config_id` | string | 是 | 配置 id。 |

### 请求结构

```http
GET /v2/ai_search/web_search/intervention HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json

?offset=2&limit=4
```

### 示例代码

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/web_search/intervention?offset=2&limit=4' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <API Key>'
```

### 返回响应

**Headers**：除公共头域外，无其它特殊头域。

**返回参数**：

| 参数 | 类型 | 必选 | 说明 |
|------|------|:----:|------|
| `request_id` | string | 是 | 请求 request_id。 |
| `limit` | integer | 是 | 分页大小。 |
| `offset` | integer | 是 | 分页偏移。 |
| `total` | integer | 是 | 结果总数。 |
| `code` | string | 否 | 错误代码，当发生异常时返回。 |
| `message` | string | 否 | 错误消息，当发生异常时返回。 |
| `items` | array&lt;object&gt; | 是 | 问答策略数组。 |
| `items[].id` | integer | 是 | 文档唯一标识。 |
| `items[].query` | string | 是 | 搜索 query。 |
| `items[].config_id` | string | 是 | 配置 id。 |
| `items[].intervention_strategy` | object | 是 | 干预策略。 |
| `items[].intervention_strategy.query_match_strategy` | object | 是 | query 匹配策略。 |
| `items[].intervention_strategy.query_match_strategy.name` | string | 是 | 匹配策略名字：`exact`（完全匹配）、`semantic`（语义）、`keyword`（关键词匹配）。 |
| `items[].intervention_strategy.query_match_strategy.similarity_threshold` | float | 否 | 语义匹配阈值，0～1 之间，默认 0.9。 |
| `items[].intervention_strategy.query_match_strategy.keywords` | array&lt;string&gt; | 否 | 关键词匹配时，设置用于匹配的关键词，长度不超过 256。 |
| `items[].intervention_strategy.result` | object | 是 | 干预结果。 |
| `items[].intervention_strategy.result.documents` | array&lt;object&gt; | 否 | 预置回答策略。 |
| `...documents[].id` | string | 是 | 文档唯一标识。 |
| `...documents[].url` | string | 是 | 文档 URL 地址。 |
| `...documents[].title` | string | 否 | 文档标题。 |
| `...documents[].date` | string | 否 | 网页发布时间。 |
| `...documents[].content` | string | 否 | 文档正文内容。 |
| `...documents[].icon` | string | 否 | 图标 URL。 |
| `...documents[].web_anchor` | string | 否 | 网页来源。 |
| `...documents[].type` | string | 否 | 资源类型。 |
| `...documents[].website` | string | 否 | 站点名称。 |
| `...documents[].snippet` | string | 否 | 摘要文本。 |
| `...documents[].rerank_score` | float | 否 | 重排序分数。 |
| `...documents[].authority_score` | float | 否 | 权威性分数。 |
| `...documents[].markdown_text` | string | 否 | Markdown 格式文本。 |
| `...documents[].is_aladdin` | boolean | 否 | 是否来自阿拉丁。 |
| `...documents[].aladdin` | object | 否 | 阿拉丁详细内容。 |
| `...documents[].image` | object | 否 | 图片信息。 |
| `...documents[].video` | object | 否 | 视频信息。 |
| `...documents[].web_extesions` | object | 否 | 网页扩展信息。 |

> `documents[]` 内各字段含义与[新增干预项](#3-新增干预项)的请求体一致。
