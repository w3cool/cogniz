# 百度千帆 AI Search API 文档

> 本文档整理自百度千帆「AI 应用开发者中心 - API 参考（qianfan-api）」中「百度 AI 搜索」栏目，覆盖智能搜索生成与干预策略全系列共 13 个接口，各接口标题下均附原始文档 URL：
>
> | 功能分组 | 接口 | 方法 | 端点地址 | 原始文档 |
> | --- | --- | --- | --- | --- |
> | 智能搜索生成 | 智能搜索生成 | POST | `https://qianfan.baidubce.com/v2/ai_search/chat/completions` | [Hmbu8m06u](https://cloud.baidu.com/doc/qianfan-api/s/Hmbu8m06u) |
> | 智能搜索生成 | 智能搜索生成（高性能版） | POST | `https://qianfan.baidubce.com/v2/ai_search/web_summary` | [wmjqtqr7w](https://cloud.baidu.com/doc/qianfan-api/s/wmjqtqr7w) |
> | 干预策略 · 策略隔离 | 创建账号下配置 | POST | `https://qianfan.baidubce.com/v2/ai_search/config` | [0mbt1iwfq](https://cloud.baidu.com/doc/qianfan-api/s/0mbt1iwfq) |
> | 干预策略 · 策略隔离 | 获取账号下配置信息 | GET | `https://qianfan.baidubce.com/v2/ai_search/config` | [Bmbt1trek](https://cloud.baidu.com/doc/qianfan-api/s/Bmbt1trek) |
> | 干预策略 · 网页黑名单 | 增加黑名单 | POST | `https://qianfan.baidubce.com/v2/ai_search/url_black_list` | [1m8wrz29n](https://cloud.baidu.com/doc/qianfan-api/s/1m8wrz29n) |
> | 干预策略 · 网页黑名单 | 查询黑名单 | GET | `https://qianfan.baidubce.com/v2/ai_search/url_black_list` | [embu7wyc6](https://cloud.baidu.com/doc/qianfan-api/s/embu7wyc6) |
> | 干预策略 · 网页黑名单 | 删除黑名单 | DELETE | `https://qianfan.baidubce.com/v2/ai_search/url_black_list` | [Qm8ws3hjs](https://cloud.baidu.com/doc/qianfan-api/s/Qm8ws3hjs) |
> | 干预策略 · 特定query干预 | 新增问答策略 | POST | `https://qianfan.baidubce.com/v2/ai_search/qa_strategy` | [Dm8wragrc](https://cloud.baidu.com/doc/qianfan-api/s/Dm8wragrc) |
> | 干预策略 · 特定query干预 | 查询问答策略 | GET | `https://qianfan.baidubce.com/v2/ai_search/qa_strategy` | [Zm8wrsske](https://cloud.baidu.com/doc/qianfan-api/s/Zm8wrsske) |
> | 干预策略 · 特定query干预 | 删除问答策略 | DELETE | `https://qianfan.baidubce.com/v2/ai_search/qa_strategy` | [rm8wrntap](https://cloud.baidu.com/doc/qianfan-api/s/rm8wrntap) |
> | 干预策略 · 领域知识注入 | 增加领域知识 | POST | `https://qianfan.baidubce.com/v2/ai_search/domain_knowledge` | [xmbt23j3t](https://cloud.baidu.com/doc/qianfan-api/s/xmbt23j3t) |
> | 干预策略 · 领域知识注入 | 删除领域知识 | DELETE | `https://qianfan.baidubce.com/v2/ai_search/domain_knowledge` | [ymbt2du3u](https://cloud.baidu.com/doc/qianfan-api/s/ymbt2du3u) |
> | 干预策略 · 领域知识注入 | 查询领域知识 | GET | `https://qianfan.baidubce.com/v2/ai_search/domain_knowledge` | [Ymbt2kyit](https://cloud.baidu.com/doc/qianfan-api/s/Ymbt2kyit) |
>
> 鉴权方式相同：请求头携带 `Authorization: Bearer <API Key>`，具体流程见[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。
>
> 干预策略系列接口（第三～六节）配合智能搜索生成接口的 `config_id` 请求参数使用：先通过「创建账号下配置」生成 `config_id`，再在该 `config_id` 下配置网页黑名单、问答干预策略、领域知识注入，调用智能搜索生成时传入该 `config_id` 即可生效。

---

## 一、智能搜索生成（Chat Completions）

`POST https://qianfan.baidubce.com/v2/ai_search/chat/completions`

> 原始文档：[智能搜索生成](https://cloud.baidu.com/doc/qianfan-api/s/Hmbu8m06u)

### 概述

**概述：**可根据用户输入query搜索全网实时信息后，并进行智能总结回答。

**计费：**每日免费额度为100次，支持按量后付费（为不影响使用体验，可先去[开通后付费](https://console.bce.baidu.com/qianfan/studio/resource)），默认优先抵扣免费资源。如有其他需求请您[联系我们](https://cloud.baidu.com/survey/baiduaisearch.html)，费用详情请查看[计费说明](https://cloud.baidu.com/doc/qianfan/s/Mmh4sv6ec)。

**使用方式：**API、[工具及MCP](https://console.bce.baidu.com/qianfan/tools/toolsCenter/6dbfaa2c-4d84-44e0-9383-df15eff5bd6b/detail)、[SDK](https://github.com/baidubce/app-builder/blob/master/java/src/test/java/com/baidubce/appbuilder/AISearchTest.java)

### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求结构

```http
POST /v2/ai_search/chat/completions HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
{
    "messages": [
        {
            "content": "近日油价调整消息。",
            "role": "user"
        }
    ],
    "stream": false,
    "model": "ernie-4.5-turbo-32k",
    "instruction": "##",
    "enable_corner_markers": true,
    "enable_deep_search": true
}
```

### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**Body**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `messages` | `array<object>` | 是 | 搜索输入；<br>array的长度需要是奇数, role必须是user-assistant-user交替，以user开始以user结束;在百度搜索时，仅支持单论输入，若传入多轮输入，则以用户传入最后的content为输入查询。 |
| `messages[].role` | `string` | 是 | 角色设定，可选值：<br>user：用户<br>assistant：模型 |
| `messages[].content` | `string` | 是 | 1. 当content为文本时, 对应对话内容，说明：<br>1.1 不能为空<br>1.2 最后一个message对应的content不能为blank字符，如空格、"\n"、“\r”、“\f”等 |
| `model` | `string` | 是 | 使用的模型名。**不传模型名称时，搜索模式为百度搜索，传入模型名称时则为智能搜索生成**。<br>目前支持千帆官网开通的模型，详细列表内容见[模型列表](https://cloud.baidu.com/doc/qianfan/s/rmh4stp0j)<br>常见模型选项如下：<br>1. deepseek-v4-flash<br>2. deepseek-v4-pro .... |
| `search_source` | `string` | 否 | 使用的搜索引擎版本；<br>可选值：baidu\_search\_v1、baidu\_search\_v2<br>**智能搜索生成**时均可输入，兼容性考虑默认为baidu\_search\_v1<br>**V2相比于V1**：提升了性能表现，提升了数据内容的丰富度，更适用于结合大模型使用的场景，建议默认使用V2。 |
| `resource_type_filter` | `array<object>` | 否 | 单次搜索最大返回数量。<br>search\_source为**baidu\_search\_v1**时：<br>默认为返回网页top 10搜索结果，{"type": "web","top\_k": 10}]，每种搜索类型支持返回的数量范围为：1\~10<br>示例：<br>\[{"type": "image","top\_k": 4},<br>{"type": "video","top\_k": 4},<br>{"type": "web","top\_k": 4}]<br>当search\_source为**baidu\_search\_v2**时:<br>仅支持设置网页、视频搜索模态，top\_k最大取值为20.<br>\[{"type": "web","top\_k": 4},<br>{"type": "video","top\_k": 4}] <br>特别的，如需单次返回更多链接，可在智能搜索生成中开启深度搜索 |
| `resource_type_filter[].type` | `string` | 是 | 搜索资源类型。<br>**baidu_search_v1时，可选值：**<br>video: 视频<br>image: 图片<br>web：网页<br>**baidu_search_v2时，可选值：**<br>video: 视频<br>web：网页 |
| `resource_type_filter[].top_k` | `integer` | 是 | 指定模态最大返回个数 |
| `search_recency_filter` | `string` | 否 | 根据网页发布时间进行筛选；<br>枚举值:<br>week:最近7天<br>month：最近30天<br>semiyear：最近180天<br>year：最近365天 |
| `search_filter` | `object` | 否 | 根据SearchFilter下的子条件做检索过滤，使用方式详见后文；<br>**仅search\_source为baidu\_search\_v2时生效** |
| `search_filter.match` | `object` | 否 | 条件查询 |
| `search_filter.match.site` | `string` | 否 | 支持设置指定站点的搜索条件，即仅在设置的站点中进行内容搜索。支持设置100个站点。示例：["tieba.baidu.com"] |
| `search_filter.range` | `object` | 否 | 范围查询，更多内容可查看范围查询详情 |
| `search_filter.range.page_time` | `object` | 否 | 假设下述的now时间是2024-07-16 |
| `search_filter.range.page_time.gte` | `string` | 否 | 时间查询参数，值为"now-1d/d"，表示含义：大于2024-07-15 00:00:00，包含2024-07-15完整天 |
| `search_filter.range.page_time.gt` | `string` | 否 | 时间查询参数，值为"now-1d/d"，表示含义：大于2024-07-15 23:59:59，不包含2024-07-15完整天 |
| `search_filter.range.page_time.lte` | `string` | 否 | 时间查询参数，值为"now-1d/d"，表示含义：小于2024-07-15 23:59:00，包含2024-07-15完整天 |
| `search_filter.range.page_time.lt` | `string` | 否 | 时间查询参数，值为"now-1d/d"，表示含义：小于2024-07-15 00:00:00，不包含2024-07-15完整天 |
| `model_appid` | `string` | 否 | 模型调用appid |
| `instruction` | `string` | 否 | 人设指令，用于设定输出风格等。<br>默认值：""<br>注意：字符长度需要小于等于4000 |
| `temperature` | `float` | 否 | 模型采样参数。较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定。<br>值范围：(0, 1]<br>默认值：1e-10<br>注意：该值越大，模型输出越多样，也越不稳定 |
| `top_p` | `float` | 否 | 模型采样参数。<br>影响输出文本的多样性，取值越大，生成文本的多样性越强。<br>值范围：(0, 1]<br>默认值：1e-10<br>注意：该值越大，模型输出越多样，也越不稳定 |
| `prompt_template` | `string` | 否 | 面向高阶用户开放自定义prompt模版，普通用户不需要设置，支持添加的变量包括：<br>query：经过改写等处理后的query<br>original\_query：用户原始query<br>history：对话历史<br>context\_out：搜索结果（如果传入个性化知识，则是个性化知识 + 搜索结果）<br>instruction：人设<br>time：当前时间<br>其中变量query或original\_query（至少一个）、context\_out必须出现在prompt\_template中，其他变量可选。<br>样例："搜索结果：<br>{{context\_out}}<br>用户query：<br>{{query}} "。 |
| `search_mode` | `string` | 否 | 控制是否进行智能联网搜索。默认为 auto。<br>可选值：<br>auto：自动判断是否需要搜索<br>required： 必须执行搜索<br>disabled： 禁用搜索功能仅模型回答 |
| `response_format` | `object` | 否 | 设置输出内容样式。 |
| `response_format.type` | `string` | 是 | 输出格式类型，可选值：text、rich_text、json_object、json_schema，默认值text； |
| `response_format.json_schema` | `object` | 否 | 当 type为json_schema 时，属于必填字段 |
| `enable_reasoning` | `boolean` | 否 | 是否开启深度思考，仅对DeepSeek-R1、文心X1模型生效，开启后，在总结前会进行模型推理和思考并输出相关内容。<br>默认值：默认值：true<br> 可选值：<br>true：开启<br>false：不开启 |
| `enable_deep_search` | `boolean` | 否 | 是否开启深搜索。- 深搜索会产生10次以内的智能搜索生成服务调用<br>默认值：false<br>可选值：<br>true：开启，每种搜索类型最多返回100个搜索结果。<br>false：不开启，每种搜索类型最多返回10个搜索结果。 |
| `max_search_query_num` | `integer` | 否 | 当开启深度搜索时，用于搜索的最大子query个数，默认为10 |
| `additional_knowledge` | `array<object>` | 否 | 调用方提供的定制化知识内容集合，与公开的联网搜索结果构成合集，注入到模型中进行问答总结。知识注入的条数和长度， 与模型有关，限制最大10条。<br>可以配合 priority（优先级参数）使用，让本地搜索结果在能回答问题时优先被采用。当前支持三个优先级：-1、0、1，数值越小优先级越高，回答时会优先选择高优先级的内容。其中，百度搜索结果的优先级为 0。 |
| `additional_knowledge[].priority` | `string` | 否 | 搜索结果的优先级: 数字值越小，优先级越高。<br>取值范围【-1,1】<br>默认值为0；<br>举例：<br>-1是优先级最高，如果与百度搜索结果优先级相同，优先使用定制化知识点，默认值为0 |
| `additional_knowledge[].data_type` | `string` | 否 | 数据类型 |
| `additional_knowledge[].data` | `object` | 是 | 数据对象 |
| `additional_knowledge[].data.content` | `string` | 是 | 知识点内容 |
| `additional_knowledge[].data.title` | `string` | 否 | 知识点标题 |
| `additional_knowledge[].data.url` | `string` | 否 | 知识点url地址 |
| `additional_knowledge[].data.release_date` | `string` | 否 | 发布日期 |
| `enable_web_page_safety` | `boolean` | 否 | 是否开启网页安全检查，默认为true |
| `max_completion_tokens` | `string` | 否 | 默认2048，不同模型支持的最大输出token不一样，具体参考[模型列表](https://cloud.baidu.com/doc/qianfan/s/rmh4stp0j) |
| `enable_corner_markers` | `boolean` | 否 | 用于设置在最后生成的总结内容正文时，是否返回角标用于标记模型输出内容的参考来源。<br>值含义：<br>true：开启角标<br>false：隐藏角标<br>默认值：true |
| `max_refer_search_items` | `integer` | 否 | 调节用于模型问答总结的最大搜索条数，默认是全部搜索结果。 |
| `enable_followup_queries` | `boolean` | 否 | 针对用户问题和大模型回答结果，给出推荐的追问。<br>默认为false<br>可选值：true: 开启追问<br>false：不开启追问 |
| `stream` | `string` | 否 | 是否为流式请求。<br>值含义：<br>true：使用HTTP SSE流式响应<br>false：以非流式结果返回<br>默认值为false； |
| `config_id` | `string` | 否 | 指定使用该配置id下的领域知识注入、网页黑名单、问答干预策略等配置 |
| `enable_entity_selection_search` | `boolean` | 否 | 是否开启划词搜索，默认为false，不开启。开启之后将自动针对大模型返回内容抽取实体，挂载百度百科词条链接。 |
| `search_items_postprocess` | `object` | 否 | 是否启用切片重排策略，默认值为 None，表示不启用。启用后，将根据配置参数对搜索结果进行切片，并按相关性筛选出最优切片传递给大模型，以降低响应时延。 |
| `search_items_postprocess.window_size` | `integer` | 否 | 控制切片的大小，默认值400字符，推荐值[300-400] |
| `search_items_postprocess.stride_size` | `integer` | 否 | 控制下一个切片相对于上一个切片起始位置的偏移量，默认值300字符，推荐值[300-400] |
| `search_items_postprocess.max_slice` | `integer` | 否 | 用于大模型总结的最大切片个数，默认值4 |
| `enable_processing_state` | `boolean` | 否 | 首token返回之前输出关键过程信息，仅在流式场景下生效 |
| `user_profile` | `array<string>` | 否 | 用户画像。支持根据用户画像改写query，当前支持设备信息、位置信息。<br>中文key示例：<br>{<br> "设备信息": "iphone 14 pro",<br>"位置信息": "辽宁省丹东市振兴区铁成佳园"<br>}<br>英文key示例：<br>{<br>"device": "iphone 14 pro",<br> "location": "辽宁省丹东市振兴区铁成佳园"<br>} |

### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/chat/completions' \
--header 'Authorization: Bearer <API Key>' \
--header 'Content-Type: application/json' \
--data '{
  "messages": [
    {
      "content": "北京有哪些景点",
      "role": "user"
    }
  ],
  "search_source": "baidu_search_v1",
  "resource_type_filter": [
      {"type": "image","top_k": 4},
      {"type": "video","top_k": 4},
      {"type": "web","top_k": 4}
  ],
  "search_recency_filter": "year",
  "stream": false,
  "model": "ernie-4.5-turbo-32k",
  "enable_deep_search": false,
  "enable_followup_query": false,
  "temperature": 0.11,
  "top_p": 0.55,
  "search_mode": "auto",
  "enable_reasoning": true
}'
```


### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_Id` | `string` | 是 | 请求ID。 |
| `code` | `string` | 否 | 错误码，当发生异常时返回。 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回。 |
| `choices` | `array<object>` | 是 | 模型生成的 completion 的选择列表 |
| `choices[].finish_reason` | `string` | 否 | 模型停止生成token的原因。<br>返回值:<br>stop：模型自然停止生成。<br>length：输出长度达到了模型上下文长度限制。 |
| `choices[].index` | `integer` | 是 | 该completion在选择列表中的索引。 |
| `choices[].message` | `object` | 否 | 非流式模型生成的completion消息。 |
| `choices[].message.content` | `string` | 否 | completion内容 |
| `choices[].message.reasoning_content` | `string` | 否 | 仅适用于deepseek思考系列模型。<br>内容为 assistant 消息中在最终答案之前的推理内容。 |
| `choices[].message.role` | `string` | 是 | 固定值assistant |
| `choices[].delta` | `object` | 否 | 流式返回的completion增量。 |
| `choices[].delta.content` | `string` | 是 | completion内容 |
| `choices[].delta.reasoning_content` | `string` | 否 | 仅适用于deepseek思考系列模型。<br>内容为assistant消息中在最终答案之前的推理内容。 |
| `choices[].delta.role` | `string` | 否 | 固定值assistant。 |
| `choices[].delta.processing_state` | `object` | 否 | 执行状态。 |
| `choices[].delta.processing_state.action` | `string` | 否 | 执行动作。返回值如下，对应description参数的描述。<br>1.query_understanding<br>2.search_begin<br>3.search_finish |
| `choices[].delta.processing_state.description` | `string` | 否 | 执行动作描述。<br>1.正在理解问题<br>2.正在搜索网页<br>3.已搜索X个网页 |
| `usage` | `object` | 否 | token开销 |
| `usage.prompt_tokens` | `integer` | 否 | prompt（输入）token数 |
| `usage.completion_tokens` | `integer` | 否 | completion（输出）token数 |
| `usage.total_tokens` | `integer` | 否 | 总token数 |
| `is_safe` | `string` | 是 | 用户输入query是否涉及安全问题。 |
| `references` | `array<object>` | 否 | 模型回答参考引用内容 |
| `references[].icon` | `string` | 否 | 网站图标地址 |
| `references[].id` | `string` | 是 | 引用编号1、2、3 |
| `references[].title` | `string` | 是 | 网页标题 |
| `references[].url` | `string` | 是 | 网页地址 |
| `references[].web_anchor` | `string` | 是 | 网站锚文本或网站标题 |
| `references[].website` | `string` | 否 | 站点名称 |
| `references[].content` | `string` | 否 | 网页内容，显示200字以内的相关信息原文片段。 |
| `references[].date` | `string` | 否 | 网页日期 |
| `references[].type` | `string` | 否 | 检索资源类型。返回值如下：<br>web:网页<br>image:图像<br>video:视频 |
| `references[].image` | `object` | 否 | 图片详情 |
| `references[].image.url` | `string` | 否 | 图片链接 |
| `references[].image.height` | `string` | 否 | 图片高度 |
| `references[].image.width` | `string` | 否 | 图片宽度 |
| `references[].video` | `object` | 否 | 视频详情 |
| `references[].video.url` | `string` | 否 | 视频链接 |
| `references[].video.height` | `string` | 否 | 视频高度 |
| `references[].video.width` | `string` | 否 | 视频宽度 |
| `references[].video.size` | `string` | 否 | 视频大小，单位Bytes |
| `references[].video.duration` | `string` | 否 | 视频长度，单位秒 |
| `references[].video.hover_pic` | `string` | 否 | 视频封面图 |
| `followup_queries` | `array<string>` | 否 | 追问问题 |
| `entities` | `array<object>` | 否 | 实体百科词条信息，只有当请求参数word_selection_search=true并且识别到返回文本内容中出现了对应实体之后，才会返回该内容。 |
| `entities[].keyword` | `string` | 是 | 实体名称 |
| `entities[].offset` | `integer` | 是 | 实体首字偏移量，实体的第一个字符相对于整个回答的偏移量。 |
| `entities[].length` | `integer` | 是 | 实体字数 |
| `entities[].lemma_title` | `string` | 是 | 百度词条名称 |
| `entities[].lemma_url` | `string` | 是 | 百度词条链接 |
| `entities[].lemma_id` | `integer` | 是 | 百度词条ID |

### 响应示例

#### 正确响应示例

```json
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "北京的景点非常丰富，其中包括：\n1. 故宫博物院（紫禁城）：是世界上现存规模最大、保存最为完整的木质结构古建筑群之一，也是明清两代的皇家宫殿。\n2. 八达岭长城：是万里长城的重要组成部分，也是明长城的一个隘口，雄伟壮观，历史底蕴深厚。\n3. 颐和园：是清朝时期的皇家园林，以昆明湖、万寿山为基址，以杭州西湖为蓝本，汲取江南园林的设计手法而建成的一座大型山水园林，被誉为“皇家园林博物馆”。\n4. 北京天安门广场：是世界最大的城市广场，见证了许多重大历史时刻。\n5. 天坛公园：是明清皇帝祭天的地方，建筑独特，寓意“天圆地方”。\n6. 圆明园：是清代大型皇家园林，虽遭破坏，但仍能感受到昔日的辉煌与沧桑。\n7. 香山公园：是北京西郊的山林公园，景色秀丽，秋季红叶更是美不胜收。\n8. 恭王府：是规模宏大的王府建筑群，建筑精美。\n9. 什刹海：包括前海、后海等，有老北京的韵味，可乘船赏景。\n10. 奥林匹克公园：体现了“科技、绿色、人文”的理念，有鸟巢、水立方等标志性建筑。\n\n除了这些，北京还有许多其他值得一游的景点，如法海寺、龙庆峡、古北水镇、红螺寺等。",
                "role": "assistant"
            }
        }
    ],
    "is_safe": true,
    "references": [
        {
            "content": "1. 故宫（紫禁城）地址：东城区景山前街4号。门票：60元（旺季）/40元（淡季）开放时间：8:30-17:00（周一闭馆）。 为什么必去？故宫是世界现存最大、最完整的木质结构古建筑群，600年明清皇家历史的见证者，每一砖一瓦都藏着故事。必玩体验：中轴线游览（太和殿、乾清宫、御花园）感受皇家气派。打卡网红角落：延禧宫的西洋楼、红墙拍照（建议穿汉服）。珍宝馆+钟表馆（另收费），...",
            "date": "2025-4-24",
            "icon": "https://pic.rmb.bdstatic.com/bjh/user/f1c77bf4fc9f3651df29e52acde36e94.jpeg",
            "id": 1,
            "image": null,
            "title": "北京必玩景点TOP10|2025最新攻略,带你玩转帝都!",
            "type": "web",
            "url": "https://baijiahao.baidu.com/s?id=1830291819430711070&wfr=spider&for=pc",
            "video": null,
            "web_anchor": "老六爱玩"
        },
        {
            "content": "北京景点攻略 如果你是第一次去北京旅游可要千万要收藏好了",
            "date": "2024-06-01 03:18",
            "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/default.png",
            "id": 2,
            "image": {
                "height": "674",
                "url": "http://img0.baidu.com/it/u=1145656209,2145532403&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=674",
                "width": "500"
            },
            "title": "北京景点攻略 如果你是第一次去北京旅游可要千万要收藏好了",
            "type": "image",
            "url": "http://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_5388334462984511033",
            "video": null,
            "web_anchor": "全网资源"
        },
        {
            "content": "哪些北京京郊的景点 外地同学值得自驾车去 跟着UP主出行看世界 /生活/出行/北京旅游避坑指南/北京去哪玩好/干货实用攻略/自驾游北京攻略/亲子游/周边游/周末去哪玩/北京旅游攻略/保姆级攻略 哪些北京京郊景点值得外地同学自驾车去 北京公义 大八山面 北京京郊大部分景点都在六环外 办理六环外的进京证就行 当然您要办理六环内的更好一些 下面就给您推荐一些京郊自驾游 外地同学值得去的景点(北京同学也值...",
            "date": "2025-5-23",
            "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/bilibili.ico",
            "id": 3,
            "image": null,
            "title": "哪些北京京郊的景点 外地同学值得自驾车去",
            "type": "web",
            "url": "https://www.bilibili.com/video/BV1hE421K7K1",
            "video": null,
            "web_anchor": "哔哩哔哩"
        },
        {
            "content": "北京旅游必去的十大景点推荐",
            "date": "2024-06-19 13:00",
            "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/default.png",
            "id": 4,
            "image": {
                "height": "1067",
                "url": "http://img2.baidu.com/it/u=80406124,3208002747&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1067",
                "width": "800"
            },
            "title": "北京旅游必去的十大景点推荐",
            "type": "image",
            "url": "http://www.douyin.com/note/7382074689126010131",
            "video": null,
            "web_anchor": "全网资源"
        },
        {
            "content": "北京景区排名必玩十大景点?有世界最大城市广场,有大型皇家园林 北京景区排名必玩十大景点?有世界最大城市广场,有大型皇家园林 北京景区 城市广场 旅游攻略 旅游资讯 皇家园林 北京有很多值得一去的景点推荐10个:1.故宫: 位于北京中心明清皇宫建筑辉煌藏品丰富 尽显皇家风范 2.颐和园 清朝皇家园林有山有水融合江南园林风格 风景如画 3.八达岭长城:在延庆万里长城重要部分 雄伟壮观历史底蕴深厚 4....",
            "date": "2025-5-22",
            "icon": "https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=76251347,1123177279&fm=195&app=88&f=PNG?w=200&h=200",
            "id": 5,
            "image": null,
            "title": "北京景区排名必玩十大景点?有世界最大城市广场,有大型...",
            "type": "web",
            "url": "https://haokan.baidu.com/v?pd=wisenatural&vid=14103857872992752240",
            "video": null,
            "web_anchor": "好看视频"
        },
        {
            "content": "北京必去十大景点 新手必看‼️附旅游攻略.熬夜整理出来的必打",
            "date": "2024-06-15 20:25",
            "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/default.png",
            "id": 6,
            "image": {
                "height": "1342",
                "url": "http://img1.baidu.com/it/u=17130128,3218194790&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1342",
                "width": "800"
            },
            "title": "北京必去十大景点 新手必看‼附旅游攻略.熬夜整理出来的必打",
            "type": "image",
            "url": "http://www.douyin.com/note/7380319151006436646",
            "video": null,
            "web_anchor": "全网资源"
        },
        {
            "content": "揭秘！北京好玩的十大景点排行榜，你去过几个？北京，这座古老又现代的城市，藏着无数好玩的地方。想知道哪些景点能跻身北京好玩的地方排行榜前十名吗？接下来，我们就为你揭开谜底，带你领略京城最值得一去的精华景点，让你的北京之行不留遗憾。1. 故宫博物院 故宫，旧称紫禁城，是中国明清两代的皇家宫殿，也是世界上现存规模最大、保存最为完整的木质结构古建筑群之一。走进故宫，仿佛穿越回了古代，红墙黄瓦、飞檐斗拱，处...",
            "date": "2025-5-4",
            "icon": "https://pic.rmb.bdstatic.com/bjh/user/84f5641182eb2b574909828a3fa8f9b0.jpeg",
            "id": 7,
            "image": null,
            "title": "揭秘!北京好玩的十大景点排行榜,你去过几个?",
            "type": "web",
            "url": "https://baijiahao.baidu.com/s?id=1830726637146162329&wfr=spider&for=pc",
            "video": null,
            "web_anchor": "炫拍客旅途志"
        },
        {
            "content": "北京必去十大景点新手必看.亲亲记滴点赞收藏! 1 no.1",
            "date": "2024-08-17 11:00",
            "icon": "https://appbuilder.bj.bcebos.com/baidu-search-rag-pro/icon/default.png",
            "id": 8,
            "image": {
                "height": "1067",
                "url": "http://img0.baidu.com/it/u=3343386837,4291065808&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1067",
                "width": "800"
            },
            "title": "北京必去十大景点新手必看.亲亲记滴点赞收藏! 1 no.1",
            "type": "image",
            "url": "http://www.douyin.com/note/7403937889005882650",
            "video": null,
            "web_anchor": "全网资源"
        }
    ],
    "request_id": "ad524989-be46-48fd-b2ec-344683b28305",
    "usage": {
        "completion_tokens": 295,
        "prompt_tokens": 1919,
        "total_tokens": 2214
    }
}
```

#### 错误响应示例

```json
{
    "requestId": "00000000-0000-0000-0000-000000000000",
    "code": 216003,
    "message": "Authentication error: ( [Code: InvalidHTTPAuthHeader; Message: Fail to parse apikey authorization; RequestId: ea6ffeca-a136-401b-ba30-61c910c02ead] )"
}
```


### 错误码

| 错误码 | 描述                                                                     |
| :-- | :--------------------------------------------------------------------- |
| 400 | 客户端请求参数错误                                                              |
| 500 | 服务端执行错误                                                                |
| 501 | 调用模型服务超时                                                               |
| 502 | 模型流式输出超时                                                               |
| 其它  | 详见[模型返回错误码](https://cloud.baidu.com/doc/qianfan/s/Pmh4sv5qa) |

---

## 二、智能搜索生成高性能版（Web Summary）

`POST https://qianfan.baidubce.com/v2/ai_search/web_summary`

> 原始文档：[智能搜索生成（高性能版）](https://cloud.baidu.com/doc/qianfan-api/s/wmjqtqr7w)

### 概述

**概述：**智能搜索生成高性能版整合了大模型与搜索的能力，可根据用户输入的query进行全网实时信息检索，并总结输出内容。高性能版具有快的响应速度，同时不再区分搜索费用和大模型费用，仅按照调用量收费。

**计费：**每日免费额度为100次，支持按量后付费（为不影响使用体验，可先去[开通后付费](https://console.bce.baidu.com/ai_apaas/resource)），默认优先抵扣免费资源的免费额度，费用详情请查看[计费说明](https://cloud.baidu.com/doc/qianfan/s/8miy9o4o6)。

**使用方式：**API

### 权限说明

调用本API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**Body**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `instruction` | `string` | 否 | 人设指令，用于设定模型的输出角色与表达风格，对生成内容的语气、风格等进行约束。 |
| `messages` | `array<object>` | 是 | 对话历史 array的长度需要是奇数, role必须是user-assistant-user交替，以user开始以user结束。仅搜索时按照获取最后一次对话，作为搜索query。  <br>例子：[{"role": "user", "content":"你觉得xx的发布会上把xx的100pro手机的芯片搞错了需要道歉吗"},{"role": "assistant", "content": "是的，如果xx在发布会上错误地标注了xx100 Pro的芯片信息，那么向xx和用户道歉是合适的。这种错误可能会对xx品牌和用户造成困扰和误解，因此公开道歉并纠正错误是一个负责任的行为。同时，这也展示了xx对于准确性和专业性的重视，有助于维护品牌形象和信誉。"},{"role": "user", "content": "今天xx有道歉吗"}] |
| `messages[].role` | `string` | 是 | 角色设定，可选值包括user、assistant user：用户 assistant：模型 |
| `messages[].content` | `string` | 是 | content为文本时, 对应对话内容，即用户query问题，说明： 不能为空。 多轮对话中，用户最后一次输入message对应的content不能为空字符，如空格、"\n"、“\r”、“\f”等。 |
| `stream` | `boolean` | 否 | 是否为流式请求。值含义： true：使用HTTP SSE流式响应 false：以非流式结果返回 默认值为false； |
| `resource_type_filter` | `array<object>` | 否 | 支持设置网页、视频、图片搜索模态，网页top_k最大取值为50，视频top_k最大为10，图片top_k最大为30，默认值为： [{"type": "web","top_k": 20}，{"type": "video","top_k": 0}，{"type": "image","top_k": 0}] |
| `resource_type_filter[].type` | `string` | 是 | 可选值：video、image、web video: 视频 image: 图片 web：网页 |
| `resource_type_filter[].top_k` | `integer` | 是 | 指定模态最大返回个数 |
| `search_filter` | `object` | 否 | 定义检索过滤条件，search_source为baidu_search_v1时后置站点过滤， 当search_source为baidu_search_v2时为指定站点搜索 |
| `search_filter.match` | `object` | 否 | 条件查询。 |
| `search_filter.match.site` | `array<string>` | 否 | 支持设置指定站点的搜索条件，即仅在设置的站点中进行内容搜索，仅对网页、视频结果生效。目前支持设置100个站点。示例：["tieba.baidu.com","baike.baidu.com"]<br>注意：此为付费功能，目前限时免费中 |
| `search_filter.range` | `object` | 否 | 范围查询 |
| `search_filter.range.page_time` | `object` | 否 | 假设下述的now时间是2024-07-16。 |
| `search_filter.range.page_time.gte` | `string` | 否 | 时间查询参数，大于或等于。"now-1w/d"，2024-07-16前一周、向下做舍入，即大于2024-07-09 00:00:00，包含2024-07-09完整天。 |
| `search_filter.range.page_time.gt` | `string` | 否 | 时间查询参数，大于。"now-1w/d"，2024-07-16前一周、向上做舍入，即大于2024-07-09 23:59:59，不包含2024-07-09完整天。 |
| `search_filter.range.page_time.lte` | `string` | 否 | 时间查询参数，小于或等于。"now-1w/d"，2024-07-16前一周、向上做舍入，即小于2024-07-09 23:59:59，包含2024-07-09完整天。 |
| `search_filter.range.page_time.lt` | `string` | 否 | 时间查询参数，小于。"now-1w/d"，2024-07-16前一周、向下做舍入，即小于2024-07-09 00:00:00，不包含2024-07-09完整天。 |
| `temperature` | `float` | 否 | 模型采样参数。较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定 值范围：(0, 1] 默认值：1e-6 注意：该值越大，模型输出越多样，也越不稳定 |
| `top_p` | `float` | 否 | 模型采样参数。影响输出文本的多样性，取值越大，生成文本的多样性越强 值范围：(0, 1] 默认值：1e-10 注意：该值越大，模型输出越多样，也越不稳定 |
| `response_format` | `object` | 否 | 默认文本输出 |
| `response_format.type` | `string` | 是 | 输出格式类型，可选值：text、json_object、json_schema，默认值text； |
| `response_format.json_schema` | `object` | 否 | 当 type 为 json_schema 时，必填；详细信息请参考[协议文档](https://json-schema.org/overview/what-is-jsonschema) |
| `model` | `string` | 否 | 是否开启思考能力，枚举值：thinking, auto_thinking, non_thinking。<br>默认值：non_thinking<br>枚举值及含义：<br>thinking: 智能总结开启模型思考能力，使用思考模型。限时免费中<br>auto_thinking: 根据query自动判断是否需要思考，自适应开启思考能力<br>non_thinking: 智能总结不开启模型思考能力，使用非思考模型 |

### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/web_summary' \
--header 'Authorization: Bearer <API Key>' \
--header 'X-Appbuilder-Request-Id: a728c65f-840a-4769-a37f-5639a1ad8b1f' \
--header 'X-Appbuilder-User-Id: f96e262041644ce2a0670bdc57f3cd7b' \
--header 'Content-Type: application/json' \
--data '{"messages": [{"role": "user", "content": "北戴河景区"}], "stream": true}'
```


### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 否 | 请求ID |
| `code` | `string` | 否 | 错误代码，当发生异常时返回 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |
| `choices` | `array<object>` | 否 | 模型生成的 completion 的选择列表 |
| `choices[].message` | `object` | 否 | 非流式模型生成的completion消息 |
| `choices[].message.content` | `string` | 否 | completion内容 |
| `choices[].message.role` | `string` | 否 | 固定值assistant |
| `choices[].delta` | `object` | 否 | 流式返回的completion增量 |
| `choices[].delta.content` | `string` | 否 | completion内容 |
| `choices[].delta.role` | `string` | 否 | 固定值assistant |
| `references` | `array<object>` | 否 | 模型回答参考引用内容 |
| `references[].icon` | `string` | 否 | 站点图标 |
| `references[].id` | `integer` | 否 | 网页编号1、2、3 |
| `references[].title` | `string` | 否 | 网页标题 |
| `references[].url` | `string` | 否 | 网页地址 |
| `references[].content` | `string` | 否 | 当enable_full_content设为true时，该字段为网页内容全文；当enable_full_content设为false时，为网页内容摘要，此时与snippet字段内容相同。 |
| `references[].date` | `string` | 否 | 网页日期 |
| `references[].type` | `string` | 否 | 检索资源类型： web:网页 image:图像内容 video:视频内容 aladdin:阿拉丁 |
| `references[].website` | `string` | 否 | 站点名称 |
| `references[].image` | `object` | 否 | 图片详情 |
| `references[].image.url` | `string` | 否 | 图片链接 |
| `references[].image.height` | `string` | 否 | 图片高度 |
| `references[].image.width` | `string` | 否 | 图片宽度 |
| `references[].video` | `object` | 否 | 视频详情 |
| `references[].video.url` | `string` | 否 | 视频链接 |
| `references[].video.height` | `string` | 否 | 视频高度 |
| `references[].video.width` | `string` | 否 | 视频宽度 |
| `references[].video.size` | `string` | 否 | 视频大小，单位Bytes |
| `references[].video.duration` | `string` | 否 | 视频长度，单位秒 |
| `references[].video.hover_pic` | `string` | 否 | 视频封面图 |
| `references[].aladdin` | `object` | 否 | 阿拉丁详细内容，见文档对外公布文档-[阿拉丁卡结构化信息（beta）](https://cloud.baidu.com/doc/qianfan-api/s/Xmjsa5ct9) |
| `references[].snippet` | `string` | 否 | 网页内容摘要（非网页内容原文） |
| `references[].web_extensions` | `object` | 否 | 网页相关图片 |
| `references[].web_extensions.images` | `object` | 否 | 网页相关图片 |
| `references[].web_extensions.images.images[0].url` | `string` | 否 | 图片链接 |
| `references[].web_extensions.images.images[0].height` | `string` | 否 | 图片高度 |
| `references[].web_extensions.images.images[0].width` | `string` | 否 | 图片宽度 |
| `references[].rerank_score` | `float` | 否 | 网页、视频、图片相关性得分，取值范围0～1 |
| `references[].authority_score` | `float` | 否 | 网页权威性评分，取值范围0～1 |

### 响应示例

#### 非流式
```json
{"request_id":"a728c65f-840a-4769-a37f-5639a1ad8b1f","choices":[{"finish_reason":"stop","message":{"role":"assistant","content":"北戴河景区位于河北省秦皇岛市西南部，南临渤海，北靠联峰山，地处燕山余脉与渤海交汇地带，是华北地区著名的滨海旅游与避暑胜地。作为中国四大避暑地之一，北戴河景区不仅自然风光秀美，而且历史文化底蕴深厚，兼具生态价值与旅游功能。\n\n### 一、地理与规划概况\n\n| 属性 | 信息 |\n|------|------|\n| 地理位置 | 河北省秦皇岛市西南部，南临渤海，北靠联峰山，东接辽宁，西连京津 |\n| 地理范围 | 地跨秦皇岛市四区三县，规划总面积约 **365.97 平方千米** |\n| 地形地貌 | 以海滨平原和低山丘陵为主，地质结构稳定，拥有典型海蚀地貌 |\n| 气候类型 | 暖温带半湿润大陆性季风气候，夏季凉爽宜人，年均气温约12℃ |\n\n\u003e **信息来源**：网页2、网页3、网页4\n\n---\n\n### 二、核心景区构成与功能分区\n\n北戴河景区属于**分散型风景区**，由六大特色景区构成，按地理方位自北向南划分为五大功能区域：\n\n1. **北部山林区域**：以联峰山为核心，植被茂密，为城市绿肺与生态屏障。\n2. **低山丘陵区域**：兼具自然景观与人文遗迹，如鸽子窝公园、老虎石公园等。\n3. **山间盆地区域**：地形相对封闭，适宜生态保育与休闲康养。\n4. **冲积平原区域**：地势平坦，是城市建设和农业活动的主要区域。\n5. **东部沿海区域**：拥有长达二十里的优质沙滩，是海滨度假的核心地带。\n\n**六大具体景区**包括：\n- 北戴河海滨风景区（核心）\n- 山海关（历史名城，长城起点）\n- 南戴河（以“海上乐园”著称）\n- 黄金海岸（国家级海洋公园）\n- 祖山（燕山山脉重要支脉，自然生态保护区）\n- 碣石山（古代帝王巡游之地，文化底蕴深厚）\n\n\u003e **信息来源**：网页2、网页3\n\n---\n\n### 三、生态与环境价值\n\n北戴河不仅是旅游胜地，更是重要的生态节点。其周边生态系统包括：\n- **滨海湿地系统**：如七里海潟湖，是东亚—澳大利西亚候鸟迁徙通道的关键中转站。\n- **海洋碳汇功能**：通过退养还湿、微地形改造、岸线修复等措施，七里海潟湖水面面积已恢复至2015年的**3倍**，显著提升区域碳汇能力。\n- **灾害预警体系**：已构建“空—天—地—海”一体化海洋灾害监测预警系统，增强防灾减灾能力。\n\n\u003e **信息来源**：网页1\n\n---\n\n### 四、旅游与文化地位\n\n北戴河景区享有极高声誉，曾获多项国家级荣誉：\n- 首批国家级重点风景名胜区\n- 首批全国旅游示范区\n- 中国优秀旅游城市\n- 全国文明城市\n- 国家森林城市\n\n同时，北戴河地处“京津冀黄金旅游圈”核心节点，与北京、天津、承德共同构成区域旅游联动网络，是国内外游客理想的休闲度假目的地。\n\n---\n\n### 五、未来发展方向\n\n随着生态文明建设深入推进，北戴河景区正从传统观光型向**生态旅游+智慧管理+可持续发展**转型：\n- 推进生态修复工程（如七里海潟湖恢复项目）\n- 强化智慧化监测与预警系统建设\n- 发展低碳旅游与绿色交通体系\n- 深化文化遗产保护与活化利用\n\n---\n\n### 总结\n\n北戴河景区集自然之美、历史之韵、生态之重于一体，既是避暑胜地，也是生态屏障与文化地标。其在地理区位、生态功能、旅游价值与政策支持方面均具备显著优势，未来将持续发挥京津冀协同发展中的重要支点作用。\n\n如需了解具体景区开放时间、门票信息或交通指南，可进一步查阅官方旅游平台或景区公告。"}}],"references":[{"id":1,"url":"https://i.ifeng.com/c/8oU2F1wG30G","title":"万鸟归来 七里海潟湖十年重生","date":"2025-10-12 00:00:00","content":"七里海潟湖位于秦皇岛市北戴河新区,是华北地区最大的潟湖、东亚—澳大利西亚候鸟迁徙通道的重要节点,也是我省提升海洋碳汇能力、增强海洋防灾减灾功能的重要海洋生态系统。 通过协议退养还湿、微地形改造、岸线修复等生态减灾修复措施,目前七里海潟湖水面面积恢复至2015年的3倍,同时构建起“空—天—地—海”一体化海洋灾害预警监测体系,区域生态功能得到改善,防灾减灾能力有效提升。 退养还湿 水面面积扩大至十年前的3倍 10月20日,秦皇岛市北戴河新区秋高气爽。","icon":"http://x0.ifengimg.com/fe/custom/ifeng.f52bd6.png","web_anchor":"","type":"web","website":"凤凰网","video":null,"image":null,"is_aladdin":false,"aladdin":null,"snippet":"七里海潟湖位于秦皇岛市北戴河新区,是华北地区最大的潟湖、东亚—澳大利西亚候鸟迁徙通道的重要节点,也是我省提升海洋碳汇能力、增强海洋防灾减灾功能的重要海洋生态系统。 通过协议退养还湿、微地形改造、岸线修复等生态减灾修复措施,目前七里海潟湖水面面积恢复至2015年的3倍,同时构建起“空—天—地—海”一体化海洋灾害预警监测体系,区域生态功能得到改善,防灾减灾能力有效提升。 退养还湿 水面面积扩大至十年前的3倍 10月20日,秦皇岛市北戴河新区秋高气爽。","web_extensions":{"images":null},"rerank_score":1,"authority_score":0.5},{"id":2,"url":"https://baike.baidu.com/item/北戴河景区/10433529","title":"北戴河景区","date":"2025-10-23 11:06:41","content":" 北戴河景区,位于河北省秦皇岛市西南部,南临渤海,北靠联峰山,东临辽宁、西接京津,北枕燕山,地跨秦皇岛市的四区三县,规划总面积约为365.97平方千米。 [3] [6] [16] 北戴河景区的地形地貌以海滨平原和丘陵为主,地质结构稳定,拥有多处海蚀地貌。水文特征显著,毗邻渤海,海岸线绵长,海水清澈。气候类型为暖温带半湿润大陆性季风气候。植被类型包括温带落叶阔叶林及沿海盐生植被。生物资源包括多种海洋生物和内陆野生动物。北戴河景区属于分散型风景区,包含六大特色景区。景区由北向南划分为五大区域:北部山林区域、低山丘陵区域、山间盆地区域、冲积平原区域和东部沿海区域。景区还包括山海关、北戴河、南戴河、黄金海岸、祖山和碣石山六大具体景区。 [7] 北戴河景区是中国四大避暑地之一,先后被评为首批国家级重点风景名胜区、首批全国旅游示范区、中国优秀旅游城市,荣获全国文明城市、国家森林城市桂冠。","icon":"https://mbs1.bdstatic.com/searchbox/mappconsole/image/20200630/db4d874a-872b-4b27-931d-775a91ed0003.png","web_anchor":"","type":"web","website":"百度百科","video":null,"image":null,"is_aladdin":true,"aladdin":null,"snippet":" 北戴河景区,位于河北省秦皇岛市西南部,南临渤海,北靠联峰山,东临辽宁、西接京津,北枕燕山,地跨秦皇岛市的四区三县,规划总面积约为365.97平方千米。 [3] [6] [16] 北戴河景区的地形地貌以海滨平原和丘陵为主,地质结构稳定,拥有多处海蚀地貌。水文特征显著,毗邻渤海,海岸线绵长,海水清澈。气候类型为暖温带半湿润大陆性季风气候。植被类型包括温带落叶阔叶林及沿海盐生植被。生物资源包括多种海洋生物和内陆野生动物。北戴河景区属于分散型风景区,包含六大特色景区。景区由北向南划分为五大区域:北部山林区域、低山丘陵区域、山间盆地区域、冲积平原区域和东部沿海区域。景区还包括山海关、北戴河、南戴河、黄金海岸、祖山和碣石山六大具体景区。 [7] 北戴河景区是中国四大避暑地之一,先后被评为首批国家级重点风景名胜区、首批全国旅游示范区、中国优秀旅游城市,荣获全国文明城市、国家森林城市桂冠。","web_extensions":{"images":[{"url":"https://bkimg.cdn.bcebos.com/pic/2934349b033b5bb5ab25ff723cd3d539b700bc48","height":"450","width":"600"},{"url":"https://bkimg.cdn.bcebos.com/pic/08f790529822720e9dda7f477dcb0a46f21fab73","height":"492","width":"779"},{"url":"https://bkimg.cdn.bcebos.com/pic/f29faa8fe1e485aaf11f3651","height":"274","width":"400"},{"url":"https://bkimg.cdn.bcebos.com/pic/3812b31bb051f8196d4316fbdab44aed2e73e719","height":"600","width":"800"},{"url":"https://bkimg.cdn.bcebos.com/pic/0d729944ce3d0b08500ffe2e","height":"329","width":"453"}]},"rerank_score":1,"authority_score":1},{"id":3,"url":"https://baike.baidu.com/item/北戴河风景名胜区/6749014","title":"北戴河风景名胜区","date":"2025-10-21 16:29:05","content":" 北戴河风景名胜区因为它拥有避暑胜地北戴河、历史名城山海关和天然不冻良港而驰名天下。 秦皇岛北戴河风景名胜区位于渤海之滨,东临辽宁、西接京津,北枕燕山,地跨秦皇岛市的四区三县,规划总面积约为365.97平方公里,是我国第一批国家重点风景名胜区之一。 北戴河风景名胜区位于河北省秦皇岛市西南,南临渤海,北靠联峰山。","icon":"https://mbs1.bdstatic.com/searchbox/mappconsole/image/20200630/db4d874a-872b-4b27-931d-775a91ed0003.png","web_anchor":"","type":"web","website":"百度百科","video":null,"image":null,"is_aladdin":true,"aladdin":null,"snippet":" 北戴河风景名胜区因为它拥有避暑胜地北戴河、历史名城山海关和天然不冻良港而驰名天下。 秦皇岛北戴河风景名胜区位于渤海之滨,东临辽宁、西接京津,北枕燕山,地跨秦皇岛市的四区三县,规划总面积约为365.97平方公里,是我国第一批国家重点风景名胜区之一。 北戴河风景名胜区位于河北省秦皇岛市西南,南临渤海,北靠联峰山。","web_extensions":{"images":[{"url":"https://bkimg.cdn.bcebos.com/pic/562c11dfa9ec8a131b0ac69cf903918fa0ecc0be","height":"0","width":"0"},{"url":"https://bkimg.cdn.bcebos.com/pic/d8f9d72a6059252d009a5041319b033b5ab5b9e2","height":"0","width":"0"},{"url":"https://bkimg.cdn.bcebos.com/pic/4ec2d5628535e5dd8ebf8f6e76c6a7efcf1b62eb","height":"0","width":"0"},{"url":"https://bkimg.cdn.bcebos.com/pic/42166d224f4a20a47817f53f90529822720ed039","height":"0","width":"0"},{"url":"https://bkimg.cdn.bcebos.com/pic/d01373f082025aaf51f2b033fbedab64024f1a02","height":"0","width":"0"}]},"rerank_score":1,"authority_score":1},{"id":4,"url":"https://baike.baidu.com/item/北戴河海滨风景区/3233396","title":"北戴河海滨风景区","date":"2025-03-04 15:08:06","content":" 北戴河海滨风景区地处河北省秦皇岛市中心的西部。是秦皇岛的城市区之一,气候宜人,二十里长、曲折平坦的沙质海滩,沙软潮平,背靠树木葱郁的联峰山,自然环境优美。与北京、天津、承德共同构成京津冀黄金旅游圈,北戴河处于旅游圈的重要节点地位。北戴河海滨风景区,中国著名海滨避暑胜地,拥有优质海滩、丰富自然与人文景观,适合休闲度假、观海赏日及体验渔家生活。 南京汤山温泉旅游度假区 南京汤山温泉旅游度假区位于南京市江宁区东部,区域面积29.74平方公里,2007年启动汤山新城建设,2012年","icon":"https://mbs1.bdstatic.com/searchbox/mappconsole/image/20200630/db4d874a-872b-4b27-931d-775a91ed0003.png","web_anchor":"","type":"web","website":"百度百科","video":null,"image":null,"is_aladdin":true,"aladdin":null,"snippet":" 北戴河海滨风景区地处河北省秦皇岛市中心的西部。是秦皇岛的城市区之一,气候宜人,二十里长、曲折平坦的沙质海滩,沙软潮平,背靠树木葱郁的联峰山,自然环境优美。与北京、天津、承德共同构成京津冀黄金旅游圈,北戴河处于旅游圈的重要节点地位。北戴河海滨风景区,中国著名海滨避暑胜地,拥有优质海滩、丰富自然与人文景观,适合休闲度假、观海赏日及体验渔家生活。 南京汤山温泉旅游度假区 南京汤山温泉旅游度假区位于南京市江宁区东部,区域面积29.74平方公里,2007年启动汤山新城建设,2012年","web_extensions":{"images":null},"rerank_score":1,"authority_score":1}]}
```

#### 流式
```text
data: {"request_id":"a728c65f-840a-4769-a37f-5639a1ad8b1f","choices":null,"references":[{"id":1,"url":"https://i.ifeng.com/c/8oU2F1wG30G","title":"万鸟归来 七里海潟湖十年重生","date":"2025-10-12 00:00:00","content":"七里海潟湖位于秦皇岛市北戴河新区,是华北地区最大的潟湖、东亚—澳大利西亚候鸟迁徙通道的重要节点,也是我省提升海洋碳汇能力、增强海洋防灾减灾功能的重要海洋生态系统。 通过协议退养还湿、微地形改造、岸线修复等生态减灾修复措施,目前七里海潟湖水面面积恢复至2015年的3倍,同时构建起“空—天—地—海”一体化海洋灾害预警监测体系,区域生态功能得到改善,防灾减灾能力有效提升。 退养还湿 水面面积扩大至十年前的3倍 10月20日,秦皇岛市北戴河新区秋高气爽。","icon":"http://x0.ifengimg.com/fe/custom/ifeng.f52bd6.png","web_anchor":"","type":"web","website":"凤凰网","video":null,"image":null,"is_aladdin":false,"aladdin":null,"snippet":"七里海潟湖位于秦皇岛市北戴河新区,是华北地区最大的潟湖、东亚—澳大利西亚候鸟迁徙通道的重要节点,也是我省提升海洋碳汇能力、增强海洋防灾减灾功能的重要海洋生态系统。 通过协议退养还湿、微地形改造、岸线修复等生态减灾修复措施,目前七里海潟湖水面面积恢复至2015年的3倍,同时构建起“空—天—地—海”一体化海洋灾害预警监测体系,区域生态功能得到改善,防灾减灾能力有效提升。 退养还湿 水面面积扩大至十年前的3倍 10月20日,秦皇岛市北戴河新区秋高气爽。","web_extensions":{"images":null},"rerank_score":1,"authority_score":0.5},{"id":2,"url":"https://baike.baidu.com/item/北戴河景区/10433529","title":"北戴河景区","date":"2025-10-23 11:06:41","content":" 北戴河景区,位于河北省秦皇岛市西南部,南临渤海,北靠联峰山,东临辽宁、西接京津,北枕燕山,地跨秦皇岛市的四区三县,规划总面积约为365.97平方千米。 [3] [6] [16] 北戴河景区的地形地貌以海滨平原和丘陵为主,地质结构稳定,拥有多处海蚀地貌。水文特征显著,毗邻渤海,海岸线绵长,海水清澈。气候类型为暖温带半湿润大陆性季风气候。植被类型包括温带落叶阔叶林及沿海盐生植被。生物资源包括多种海洋生物和内陆野生动物。北戴河景区属于分散型风景区,包含六大特色景区。景区由北向南划分为五大区域:北部山林区域、低山丘陵区域、山间盆地区域、冲积平原区域和东部沿海区域。景区还包括山海关、北戴河、南戴河、黄金海岸、祖山和碣石山六大具体景区。 [7] 北戴河景区是中国四大避暑地之一,先后被评为首批国家级重点风景名胜区、首批全国旅游示范区、中国优秀旅游城市,荣获全国文明城市、国家森林城市桂冠。","icon":"https://mbs1.bdstatic.com/searchbox/mappconsole/image/20200630/db4d874a-872b-4b27-931d-775a91ed0003.png","web_anchor":"","type":"web","website":"百度百科","video":null,"image":null,"is_aladdin":true,"aladdin":null,"snippet":" 北戴河景区,位于河北省秦皇岛市西南部,南临渤海,北靠联峰山,东临辽宁、西接京津,北枕燕山,地跨秦皇岛市的四区三县,规划总面积约为365.97平方千米。 [3] [6] [16] 北戴河景区的地形地貌以海滨平原和丘陵为主,地质结构稳定,拥有多处海蚀地貌。水文特征显著,毗邻渤海,海岸线绵长,海水清澈。气候类型为暖温带半湿润大陆性季风气候。植被类型包括温带落叶阔叶林及沿海盐生植被。生物资源包括多种海洋生物和内陆野生动物。北戴河景区属于分散型风景区,包含六大特色景区。景区由北向南划分为五大区域:北部山林区域、低山丘陵区域、山间盆地区域、冲积平原区域和东部沿海区域。景区还包括山海关、北戴河、南戴河、黄金海岸、祖山和碣石山六大具体景区。 [7] 北戴河景区是中国四大避暑地之一,先后被评为首批国家级重点风景名胜区、首批全国旅游示范区、中国优秀旅游城市,荣获全国文明城市、国家森林城市桂冠。","web_extensions":{"images":[{"url":"https://bkimg.cdn.bcebos.com/pic/2934349b033b5bb5ab25ff723cd3d539b700bc48","height":"450","width":"600"},{"url":"https://bkimg.cdn.bcebos.com/pic/08f790529822720e9dda7f477dcb0a46f21fab73","height":"492","width":"779"},{"url":"https://bkimg.cdn.bcebos.com/pic/f29faa8fe1e485aaf11f3651","height":"274","width":"400"},{"url":"https://bkimg.cdn.bcebos.com/pic/3812b31bb051f8196d4316fbdab44aed2e73e719","height":"600","width":"800"},{"url":"https://bkimg.cdn.bcebos.com/pic/0d729944ce3d0b08500ffe2e","height":"329","width":"453"}]},"rerank_score":1,"authority_score":1},{"id":3,"url":"https://baike.baidu.com/item/北戴河风景名胜区/6749014","title":"北戴河风景名胜区","date":"2025-10-21 16:29:05","content":" 北戴河风景名胜区因为它拥有避暑胜地北戴河、历史名城山海关和天然不冻良港而驰名天下。 秦皇岛北戴河风景名胜区位于渤海之滨,东临辽宁、西接京津,北枕燕山,地跨秦皇岛市的四区三县,规划总面积约为365.97平方公里,是我国第一批国家重点风景名胜区之一。 北戴河风景名胜区位于河北省秦皇岛市西南,南临渤海,北靠联峰山。","icon":"https://mbs1.bdstatic.com/searchbox/mappconsole/image/20200630/db4d874a-872b-4b27-931d-775a91ed0003.png","web_anchor":"","type":"web","website":"百度百科","video":null,"image":null,"is_aladdin":true,"aladdin":null,"snippet":" 北戴河风景名胜区因为它拥有避暑胜地北戴河、历史名城山海关和天然不冻良港而驰名天下。 秦皇岛北戴河风景名胜区位于渤海之滨,东临辽宁、西接京津,北枕燕山,地跨秦皇岛市的四区三县,规划总面积约为365.97平方公里,是我国第一批国家重点风景名胜区之一。 北戴河风景名胜区位于河北省秦皇岛市西南,南临渤海,北靠联峰山。","web_extensions":{"images":[{"url":"https://bkimg.cdn.bcebos.com/pic/562c11dfa9ec8a131b0ac69cf903918fa0ecc0be","height":"0","width":"0"},{"url":"https://bkimg.cdn.bcebos.com/pic/d8f9d72a6059252d009a5041319b033b5ab5b9e2","height":"0","width":"0"},{"url":"https://bkimg.cdn.bcebos.com/pic/4ec2d5628535e5dd8ebf8f6e76c6a7efcf1b62eb","height":"0","width":"0"},{"url":"https://bkimg.cdn.bcebos.com/pic/42166d224f4a20a47817f53f90529822720ed039","height":"0","width":"0"},{"url":"https://bkimg.cdn.bcebos.com/pic/d01373f082025aaf51f2b033fbedab64024f1a02","height":"0","width":"0"}]},"rerank_score":1,"authority_score":1},{"id":4,"url":"https://baike.baidu.com/item/北戴河海滨风景区/3233396","title":"北戴河海滨风景区","date":"2025-03-04 15:08:06","content":" 北戴河海滨风景区地处河北省秦皇岛市中心的西部。是秦皇岛的城市区之一,气候宜人,二十里长、曲折平坦的沙质海滩,沙软潮平,背靠树木葱郁的联峰山,自然环境优美。与北京、天津、承德共同构成京津冀黄金旅游圈,北戴河处于旅游圈的重要节点地位。北戴河海滨风景区,中国著名海滨避暑胜地,拥有优质海滩、丰富自然与人文景观,适合休闲度假、观海赏日及体验渔家生活。 南京汤山温泉旅游度假区 南京汤山温泉旅游度假区位于南京市江宁区东部,区域面积29.74平方公里,2007年启动汤山新城建设,2012年","icon":"https://mbs1.bdstatic.com/searchbox/mappconsole/image/20200630/db4d874a-872b-4b27-931d-775a91ed0003.png","web_anchor":"","type":"web","website":"百度百科","video":null,"image":null,"is_aladdin":true,"aladdin":null,"snippet":" 北戴河海滨风景区地处河北省秦皇岛市中心的西部。是秦皇岛的城市区之一,气候宜人,二十里长、曲折平坦的沙质海滩,沙软潮平,背靠树木葱郁的联峰山,自然环境优美。与北京、天津、承德共同构成京津冀黄金旅游圈,北戴河处于旅游圈的重要节点地位。北戴河海滨风景区,中国著名海滨避暑胜地,拥有优质海滩、丰富自然与人文景观,适合休闲度假、观海赏日及体验渔家生活。 南京汤山温泉旅游度假区 南京汤山温泉旅游度假区位于南京市江宁区东部,区域面积29.74平方公里,2007年启动汤山新城建设,2012年","web_extensions":{"images":null},"rerank_score":1,"authority_score":1}]}

data: {"request_id":"a728c65f-840a-4769-a37f-5639a1ad8b1f","choices":[{"finish_reason":"","delta":{"role":"assistant","content":"北"}}]}

data: {"request_id":"a728c65f-840a-4769-a37f-5639a1ad8b1f","choices":[{"finish_reason":"","delta":{"role":"","content":"戴"}}]}

data: {"request_id":"a728c65f-840a-4769-a37f-5639a1ad8b1f","choices":[{"finish_reason":"","delta":{"role":"","content":"河"}}]}

data: {"request_id":"a728c65f-840a-4769-a37f-5639a1ad8b1f","choices":[{"finish_reason":"","delta":{"role":"","content":"景区"}}]}

...
```

---

## 三、干预策略 · 策略隔离（配置管理）

干预策略系列接口（第三～六节）用于为智能搜索生成接口配置网页黑名单、特定 query 干预（问答策略）、领域知识注入等干预策略。使用流程：

1. 调用「创建账号下配置」生成 `config_id`；
2. 在该 `config_id` 下按需配置网页黑名单、问答策略、领域知识；
3. 调用智能搜索生成（第一节）时在请求体中传入该 `config_id`，即可使对应配置生效。

### 3.1 创建账号下配置

`POST https://qianfan.baidubce.com/v2/ai_search/config`

> 原始文档：[创建账号下配置](https://cloud.baidu.com/doc/qianfan-api/s/0mbt1iwfq)

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**Body**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `description` | `string` | 否 | 配置简要描述 |

#### 请求结构

```http
POST /v2/ai_search/config HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
```

#### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/config' \
--header 'Content-Type: application/json' \
--header 'Authorization: <API Key>' \
--data '{"description": "xx场景下的配置"
}'
```

#### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 是 | 请求request_id |
| `config_id` | `string` | 是 | 配置id，后续可使用此id创建问答策略配置、网页黑名单、领域知识注入等配置 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |

#### 响应示例

```json
{"config_id":"5578e04d148248e59900f478dd561195","request_id":"49a57d49-9363-4df3-802a-78e825dfaec4"}
```

### 3.2 获取账号下配置信息

`GET https://qianfan.baidubce.com/v2/ai_search/config`

> 原始文档：[获取账号下配置信息](https://cloud.baidu.com/doc/qianfan-api/s/Bmbt1trek)

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`）外，无其它特殊头域；无 Body 参数。

#### 请求结构

```http
GET /v2/ai_search/config HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
```

#### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/config' \
--header 'Authorization: Bearer <API Key>'
```

#### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 是 | 请求request_id |
| `items` | `array<object>` | 是 | 配置列表 |
| `items[].config_id` | `string` | 是 | 配置id |
| `items[].description` | `string` | 否 | 配置文本描述 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |

#### 响应示例

```json
{"items": [{"config_id":"5578e04d148248e59900f478dd561195", "description": "手机搜图场景"}],"request_id":"49a57d49-9363-4df3-802a-78e825dfaec4"}
```

---

## 四、干预策略 · 网页黑名单

### 4.1 增加黑名单

`POST https://qianfan.baidubce.com/v2/ai_search/url_black_list`

> 原始文档：[增加黑名单](https://cloud.baidu.com/doc/qianfan-api/s/1m8wrz29n)

往黑名单中添加URL，用于检测和拦截访问，防止用户访问恶意或受限制的网站。

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 注意事项

1. 按照用户id（鉴权token对应的用户id）来区分过滤规则，某个用户id配置的规则，仅对该用户生效；
2. 调用网页黑名单接口的用户id要和调用问答接口的用户id保持一致；
3. 网页过滤发生在百度搜索之后，过滤掉的网页，不参与模型问答总结。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**Body**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `black_item` | `object` | 是 | 黑名单url内容 |
| `black_item.url` | `string` | 是 | 按照url进行前缀匹配过滤，对应以下两种情况：<br>1. 如果url设置为 `https://unsafe.com/`，则该站点下的所有网页均会被过滤；<br>2. 如果url设置为 `https://zhidao.baidu.com/question/1.html`，则仅会过滤 `https://zhidao.baidu.com/question/1.html` 网页。 |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id（见 3.1） |

#### 请求结构

```http
POST /v2/ai_search/url_black_list HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
{
    "black_item": {
        "url": "https://zhidao.baidu.com/question/1506466702568519979.html"
    }
}
```

#### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/url_black_list' \
--header 'Authorization: Bearer <API Key>' \
--header 'X-Appbuilder-Authorization: <token>' \
--data '{
    "black_item": {
        "url": "https://zhidao.baidu.com/question/1***79.html"
    }
}'
```

#### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 是 | 请求request_id |
| `code` | `string` | 否 | 错误代码，当发生异常时返回 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |

#### 响应示例

```json
{"request_id": "123"}
```

### 4.2 查询黑名单

`GET https://qianfan.baidubce.com/v2/ai_search/url_black_list`

> 原始文档：[查询黑名单](https://cloud.baidu.com/doc/qianfan-api/s/embu7wyc6)

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`）外，无其它特殊头域。

**URL 参数**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `offset` | `string` | 否 | 偏移量 |
| `limit` | `string` | 否 | 条数限制，最大不超过 50 |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id |

#### 请求结构

```http
GET /v2/ai_search/url_black_list HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
```

> 原始文档未提供该接口的示例代码。

#### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 是 | 请求request_id |
| `count` | `integer` | 是 | 黑名单列表总长度 |
| `items` | `array<object>` | 是 | 黑名单列表 |
| `items[].url` | `string` | 是 | 网页地址 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |

#### 响应示例

```json
{
    "count": 4,
    "items": [
        {
            "url": "http://abc.com"
        },
        {
            "url": "http://efg.com"
        }
    ],
    "request_id": "94c0df15-993b-4ab4-8e92-2d6272255dfb"
}
```

### 4.3 删除黑名单

`DELETE https://qianfan.baidubce.com/v2/ai_search/url_black_list`

> 原始文档：[删除黑名单](https://cloud.baidu.com/doc/qianfan-api/s/Qm8ws3hjs)

删除黑名单中的URL。

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`）外，无其它特殊头域。

**Body**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `url` | `string` | 是 | 待删除的url |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id |

#### 请求结构

```http
DELETE /v2/ai_search/url_black_list?url=<待删除的url，需urlencode> HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
```

> 注：原始文档页的「请求结构」代码块误复用了「增加黑名单」（POST + `black_item` 请求体）的内容，此处已按接口方法（DELETE）与示例代码（`url` 以 URL 参数传递）整理。

#### 请求示例

```bash
curl -X DELETE \
-H "Authorization: Bearer <API Key>" \
'https://qianfan.baidubce.com/v2/ai_search/url_black_list?url=https%3A%2F%2Fzhidao.baidu.com%2Fquestion%2F10**79.html'
```

#### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 是 | 请求request_id |
| `code` | `string` | 否 | 错误代码，当发生异常时返回 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |

#### 响应示例

```json
{"request_id": "123"}
```

---

## 五、干预策略 · 特定query干预（问答策略）

### 5.1 新增问答策略

`POST https://qianfan.baidubce.com/v2/ai_search/qa_strategy`

> 原始文档：[新增问答策略](https://cloud.baidu.com/doc/qianfan-api/s/Dm8wragrc)

在调用百度AI搜索API进行联网搜索总结时，可设置一系列特定的用户输入，通过完全匹配、语义匹配或关键词匹配的方式命中后，进行特定知识库检索后总结、特定知识库检索+联网搜索后总结、预置特定回答等方式进行输出，确保符合品牌立场、人设、形象。

**调用该接口前：**

- 准备好需要干预的输入清单；
- 准备好对应不同输入的回答（可选）；
- 准备好对不同输入进行回答需要参考的知识库，并准备好知识库ID（可选）；
- 在千帆上[创建知识库](https://console.bce.baidu.com/qianfan/studio/personalSpace/knowledgeBase)。

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**Body**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `query` | `string` | 是 | 问答query，不超过256个字符 |
| `query_match_strategy` | `object` | 是 | query匹配策略 |
| `query_match_strategy.name` | `string` | 否 | 匹配策略名字：<br>exact - 完全匹配<br>semantic - 语义匹配<br>keyword - 关键词匹配 |
| `query_match_strategy.similarity_threshold` | `number` | 否 | 当语义匹配时，该字段会被用到，值介于0～1之间，默认0.9 |
| `query_match_strategy.keywords` | `array<string>` | 否 | 当关键词匹配时，该字段会被用到，范围为0～256 |
| `answer_strategy` | `object` | 是 | 回复策略 |
| `answer_strategy.name` | `string` | 是 | 回复策略：<br>preset_answer - 预置答案<br>baidusearch_and_knowledge_base - 参考百度搜索知识库进行回答<br>knowledge_base - 知识库 |
| `answer_strategy.preset_answer_strategy_detail` | `object` | 否 | 预置回答策略 |
| `answer_strategy.preset_answer_strategy_detail.content` | `string` | 是 | 预设答案内容 |
| `answer_strategy.preset_answer_strategy_detail.references` | `array` | 是 | 参考信息来源（格式和百度AI搜索的响应参数中的[Reference对象](https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5#%E8%BF%94%E5%9B%9E%E5%93%8D%E5%BA%94)一致） |
| `answer_strategy.knowledge_base_answer_strategy_detail` | `object` | 否 | 知识库回答策略 |
| `answer_strategy.knowledge_base_answer_strategy_detail.knowledge_base_ids` | `array<string>` | 是 | 知识库id数组 |
| `answer_strategy.knowledge_base_answer_strategy_detail.document_ids` | `array<string>` | 是 | 文档id数组 |
| `answer_strategy.knowledge_base_answer_strategy_detail.top_k` | `integer` | 否 | 最相关的前k个结果，默认top6 |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id（见 3.1） |

#### 请求结构

```http
POST /v2/ai_search/qa_strategy HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json

{
    "query": "xx是组装厂吗？",
    "query_match_strategy": {
        "name": "keyword",
        "keywords": [
            "xx", "组装厂"
        ]
    },
    "answer_strategy": {
        "name": "preset_answer",
        "preset_answer_strategy_detail": {
            "content": "xx不是组装厂",
            "references": []
        }
    }
}
```

#### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/qa_strategy' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <API Key>' \
--data '{
    "query": "xx是组装厂吗？",
    "query_match_strategy": {
        "name": "keyword",
        "keywords": [
            "xx", "组装厂"
        ]
    },
    "answer_strategy": {
        "name": "preset_answer",
        "preset_answer_strategy_detail": {
            "content": "xx不是组装厂",
            "references": []
        }
    }
}'
```

#### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 是 | 请求request_id |
| `code` | `string` | 否 | 错误代码，当发生异常时返回 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |

#### 响应示例

```json
{"request_id": "123"}
```

### 5.2 查询问答策略

`GET https://qianfan.baidubce.com/v2/ai_search/qa_strategy`

> 原始文档：[查询问答策略](https://cloud.baidu.com/doc/qianfan-api/s/Zm8wrsske)

分页查询问答策略。

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**URL 参数**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `offset` | `string` | 否 | 偏移量 |
| `limit` | `string` | 否 | 条数限制，最大不超过50 |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id |

#### 请求结构

```http
GET /v2/ai_search/qa_strategy?offset=2&limit=4 HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
```

#### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/qa_strategy?offset=2&limit=4' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <API Key>'
```

#### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 是 | 请求request_id |
| `code` | `string` | 否 | 错误代码，当发生异常时返回 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |
| `count` | `integer` | 是 | 结果总数 |
| `items` | `array<object>` | 是 | 问答策略数组 |
| `items[].qa_strategy` | `object` | 否 | 问答策略详情（结构见响应示例） |
| `items[].qa_strategy.query` | `string` | 否 | query |
| `items[].qa_strategy.query_match_strategy` | `object` | 否 | query匹配策略，结构同「新增问答策略」请求参数 `query_match_strategy` |
| `items[].qa_strategy.answer_strategy` | `object` | 否 | 回复策略，结构同「新增问答策略」请求参数 `answer_strategy` |

#### 响应示例

```json
{
    "request_id": "123",
    "count": 14,
    "items": [{
        "qa_strategy": {
            "answer_strategy": {
                "knowledge_base_answer_strategy_detail": null,
                "name": "preset_answer",
                "preset_answer_strategy_detail": {
                    "content": "今天xx价格多钱",
                    "references": [{
                        "content": "快讯 美元指数再次冲高!金价小幅上涨!...",
                        "date": "2024-12-03",
                        "given_to_llm": true,
                        "icon": "https://****.bj.bcebos.com/baidu-searag-pro/icon/default.png",
                        "image_detail": {
                            "height": null,
                            "url": null,
                            "width": null
                        },
                        "ref_num": "1",
                        "resource_type": "web",
                        "title": "今天xx价格多少多少钱...",
                        "url": "http://www.hgjinjiage.cn/",
                        "video": null,
                        "web_anchor": "xx查询网"
                    }]
                }
            },
            "query_match_strategy": {
                "name": "exact",
                "similarity_threshold": 0.0
            },
            "query": "xx是组装厂吗"
        }
    }]
}
```

### 5.3 删除问答策略

`DELETE https://qianfan.baidubce.com/v2/ai_search/qa_strategy`

> 原始文档：[删除问答策略](https://cloud.baidu.com/doc/qianfan-api/s/rm8wrntap)

删除问答策略。

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**Body**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `query` | `string` | 是 | 待删除的问答策略匹配query |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id |

#### 请求结构

```http
DELETE /v2/ai_search/qa_strategy HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
query=%E5%B0%8F%E7%B1%B3%E6%98%AF%E7%BB%84%E8***82%E5%90%97%EF%BC%9F
```

> 注：`query` 需以 urlencode 形式传递（原始示例已部分脱敏，对应「小米是组装厂吗？」之类的 query）。

#### 请求示例

```bash
curl -X "DELETE" \
--header 'Authorization: Bearer <API Key>' \
--location 'https://qianfan.baidubce.com/v2/ai_search/qa_strategy?query=%E5%B0**E5%90%97%EF%BC%9F'
```

#### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 是 | 请求request_id |
| `code` | `string` | 否 | 错误代码，当发生异常时返回 |
| `message` | `string` | 否 | 错误消息，当发生异常时返回 |

#### 响应示例

```json
{"request_id": "123"}
```

---

## 六、干预策略 · 领域知识注入

### 6.1 增加领域知识

`POST https://qianfan.baidubce.com/v2/ai_search/domain_knowledge`

> 原始文档：[增加领域知识](https://cloud.baidu.com/doc/qianfan-api/s/xmbt23j3t)

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**Body**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `items` | `array<object>` | 是 | 领域知识不能超过十个、每个领域知识长度不能超过200个字符 |
| `items[].key` | `string` | 是 | 原始关键词key |
| `items[].value` | `string` | 是 | 对应规范领域知识value |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id（见 3.1） |

#### 请求结构

```http
POST /v2/ai_search/domain_knowledge HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
{
 "items":[
 {"key":"艾酷","value":"iqoo,IQOO"},
 {"key":"南航","value":"南方航空"}
 ]
}
```

#### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/domain_knowledge' \
--header 'X-Appbuilder-Authorization: Bearer <token>' \
--header 'X-Appbuilder-User-Id: 56db3ee88b9e4c4dad3294ba9ffe44a6' \
--header 'Content-Type: application/json' \
--data '{
 "items":[
 {"key":"艾酷","value":"iqoo,IQOO"},
 {"key":"南航","value":"南方航空"}
 ]
}'
```

#### 响应参数

暂无参数（原始文档标注）。

#### 响应示例

```json
{"request_id": "123"}
```

### 6.2 删除领域知识

`DELETE https://qianfan.baidubce.com/v2/ai_search/domain_knowledge`

> 原始文档：[删除领域知识](https://cloud.baidu.com/doc/qianfan-api/s/ymbt2du3u)

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**URL 参数**（请求params入参）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `key` | `string` | 是 | 需要对key进行urlencode |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id |

#### 请求结构

```http
DELETE /v2/ai_search/domain_knowledge?key=%E8%89%BE%E9%85%B7 HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
```

> 注：原始文档页「请求结构」示例中的路径误写为 `/v2/app/conversation`，此处已按接口调试地址（`https://qianfan.baidubce.com/v2/ai_search/domain_knowledge?key=%E8%89%BE%E9%85%B7`）修正；`%E8%89%BE%E9%85%B7` 即「艾酷」urlencode 后的结果。原始文档未提供该接口的示例代码。

#### 响应参数

暂无参数（原始文档标注）。原始文档未提供响应示例。

### 6.3 查询领域知识

`GET https://qianfan.baidubce.com/v2/ai_search/domain_knowledge`

> 原始文档：[查询领域知识](https://cloud.baidu.com/doc/qianfan-api/s/Ymbt2kyit)

#### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

#### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**URL 参数**（请求params入参）：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `offset` | `string` | 否 | 偏移量 |
| `limit` | `string` | 否 | 条数限制，最大不超过 50 |
| `config_id` | `string` | 否 | 策略配置id，需要提前调用配置接口创建id |

#### 请求结构

```http
GET /v2/ai_search/domain_knowledge?offset=0&limit=50 HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
```

#### 请求示例

```bash
curl --location 'https://qianfan.baidubce.com/v2/ai_search/domain_knowledge?offset=0&limit=50' \
--header 'X-Appbuilder-Authorization: Bearer <token>' \
--header 'X-Appbuilder-User-Id: 56db3ee88b9e4c4dad3294ba9ffe44a6' \
--header 'Content-Type: application/json'
```

#### 响应参数

暂无参数（原始文档标注）。原始文档未提供响应示例。
