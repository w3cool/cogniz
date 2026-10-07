# 百度千帆 百度百科 API 文档

> 本文档整理自百度千帆「AI 应用开发者中心 - API 参考（qianfan-api）」中「百度百科」栏目，覆盖百科星图、秒懂百科、百科词条、百度百科共 5 个接口，各接口标题下均附原始文档 URL：
>
> | 功能分组 | 接口 | 方法 | 端点地址 | 原始文档 |
> | --- | --- | --- | --- | --- |
> | 百科星图 | 根据星图主题查询星图列表 | GET | `https://qianfan.baidubce.com/v2/tools/baike/starmap/get_starmap_by_title` | [4mocj9hkl](https://cloud.baidu.com/doc/qianfan-api/s/4mocj9hkl) |
> | 百科星图 | 根据星图ID查询星图详情 | GET | `https://qianfan.baidubce.com/v2/tools/baike/starmap/get_starmap_by_id` | [xmocjbmc3](https://cloud.baidu.com/doc/qianfan-api/s/xmocjbmc3) |
> | 秒懂百科 | 秒懂百科（视频检索） | GET | `https://qianfan.baidubce.com/v2/baike/second_know/search_video` | [jmocjhoic](https://cloud.baidu.com/doc/qianfan-api/s/jmocjhoic) |
> | 百科词条 | 百科词条（词条列表检索） | GET | `https://appbuilder.baidu.com/v2/baike/lemma/get_list_by_title` | [0mocjdxi9](https://cloud.baidu.com/doc/qianfan-api/s/0mocjdxi9) |
> | 百度百科 | 百度百科（词条详情内容） | GET | `https://appbuilder.baidu.com/v2/baike/lemma/get_content` | [Cmocj7w03](https://cloud.baidu.com/doc/qianfan-api/s/Cmocj7w03) |
>
> 鉴权方式相同：请求头携带 `Authorization: Bearer <API Key>`，具体流程见[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。
>
> **域名说明**：「秒懂百科」与「百科词条」两个接口的原始文档中，页面调试地址与请求示例所用域名不一致（`qianfan.baidubce.com` 与 `appbuilder.baidu.com` 混用），本文以页面调试地址为准，示例代码保持原样，两个域名均可访问。

---

## 一、根据星图主题查询星图列表

`GET https://qianfan.baidubce.com/v2/tools/baike/starmap/get_starmap_by_title`

> 原始文档：[根据星图主题查询星图列表](https://cloud.baidu.com/doc/qianfan-api/s/4mocj9hkl)

### 概述

本接口支持按主题名称查询星图列表。

### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`）外，无其它特殊头域。

**Query 参数**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `starmap_title` | `string` | 否 | 星图主题，支持根据主题名称过滤。若不传，则分页查询所有的星图。 |
| `page` | `integer` | 否 | 页码，从 1 开始，默认值为 1。 |

### 请求结构

```http
GET /v2/tools/baike/starmap/get_starmap_by_title?starmap_title=&page=1 HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
```

### 请求示例

```bash
curl -X GET "https://qianfan.baidubce.com/v2/tools/baike/starmap/get_starmap_by_title?starmap_title=节日&page=1" \
  -H "Authorization: Bearer bce-v3/ALTAK-******ZftZDTn7/125eeb1c5e9ddc8cf3edf18ef6d03f1517ec9408"
```

### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `code` | `string` | 否 | 返回码，`0` 表示成功，其他值表示异常。 |
| `message` | `string` | 否 | 错误消息，成功时为空字符串。 |
| `requestId` | `string` | 否 | 请求 ID，用于问题追踪。 |
| `hasMore` | `integer` | 否 | 是否还有更多数据。<br>1：有更多数据<br>0：没有更多数据 |
| `list` | `array<object>` | 否 | 星图列表。 |
| `list[].encodeId` | `string` | 是 | 星图 ID。 |
| `list[].name` | `string` | 否 | 星图主题名。 |

### 响应示例

```json
{
    "code": "0",
    "message": "",
    "requestId": "",
    "hasMore": 1,
    "list": [
        {
            "encodeId": "7e4db7417680674e5dd90ca6",
            "name": "中国传统节日"
        },
        {
            "encodeId": "6937242830a70d08a0384769",
            "name": "西方主要节日"
        },
        {
            "encodeId": "60005a46c78a716712e12e7b",
            "name": "农历正月传统节日"
        }
    ]
}
```

> 注：原始文档的完整响应示例包含 30 条星图数据（`hasMore=1` 表示仍有更多），此处仅展示前 3 条。

---

## 二、根据星图ID查询星图详情

`GET https://qianfan.baidubce.com/v2/tools/baike/starmap/get_starmap_by_id`

> 原始文档：[根据星图ID查询星图详情](https://cloud.baidu.com/doc/qianfan-api/s/xmocjbmc3)

### 概述

本接口支持根据星图ID查询星图详情。

### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`）外，无其它特殊头域。

**Query 参数**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `starmap_id` | `string` | 是 | 星图ID，星图列表查询接口返回的星图ID |
| `page` | `integer` | 否 | 页码，从1开始，默认是1 |

### 请求结构

```http
GET /v2/tools/baike/starmap/get_starmap_by_id?starmap_id={starmap_id}&page={page} HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
```

### 请求示例

```bash
curl -i --location 'https://qianfan.baidubce.com/v2/tools/baike/starmap/get_starmap_by_id?starmap_id=63ebc0fd5280431e5c1a3dce&page=1'\
  -H "Authorization: Bearer bce-v3/ALTAK-******ZftZDTn7/125eeb1c5e9ddc8cf3edf18ef6d03f1517ec9408"
```

### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `code` | `string` | 否 | 0 表示成功，其他都是异常 |
| `message` | `string` | 否 | 错误消息 |
| `requestId` | `string` | 否 | 请求ID |
| `encodeId` | `string` | 否 | 星图ID |
| `name` | `string` | 否 | 星图主题名 |
| `total` | `integer` | 否 | 对应星图下总词条数 |
| `url` | `string` | 否 | 星图wap端落地页地址 |
| `lemmaList` | `array<object>` | 否 | 词条列表 |
| `lemmaList[].lemmaId` | `integer` | 否 | 词条ID |
| `lemmaList[].lemmaTitle` | `string` | 否 | 词条名 |
| `lemmaList[].descText` | `string` | 否 | 描述 |
| `lemmaList[].lemmaUrl` | `string` | 否 | 词条PC端链接 |

### 响应示例

```json
{
    "code": "0",
    "message": "",
    "requestId": "",
    "encodeId": "63ebc0fd5280431e5c1a3dce",
    "name": "韩国节日",
    "total": 9,
    "url": "https://wapbaike.baidu.com/starmap/view?nodeId=63ebc0fd5280431e5c1a3dce&fr=api_ACG_sales",
    "lemmaList": [
        {
            "lemmaId": 23330100,
            "lemmaTitle": "三一节",
            "descText": "3月1日",
            "lemmaUrl": "https://baike.baidu.com/item/%E4%B8%89%E4%B8%80%E8%8A%82/23330100?fr=api_ACG_sales"
        },
        {
            "lemmaId": 51151422,
            "lemmaTitle": "植木日",
            "descText": "4月5日",
            "lemmaUrl": "https://baike.baidu.com/item/%E6%A4%8D%E6%9C%A8%E6%97%A5/51151422?fr=api_ACG_sales"
        },
        {
            "lemmaId": 4757640,
            "lemmaTitle": "韩国儿童节",
            "descText": "5月5日",
            "lemmaUrl": "https://baike.baidu.com/item/%E9%9F%A9%E5%9B%BD%E5%84%BF%E7%AB%A5%E8%8A%82/4757640?fr=api_ACG_sales"
        },
        {
            "lemmaId": 6839118,
            "lemmaTitle": "父母节",
            "descText": "5月8日",
            "lemmaUrl": "https://baike.baidu.com/item/%E7%88%B6%E6%AF%8D%E8%8A%82/6839118?fr=api_ACG_sales"
        },
        {
            "lemmaId": 7673239,
            "lemmaTitle": "制宪节",
            "descText": "7月17日",
            "lemmaUrl": "https://baike.baidu.com/item/%E5%88%B6%E5%AE%AA%E8%8A%82/7673239?fr=api_ACG_sales"
        },
        {
            "lemmaId": 10835902,
            "lemmaTitle": "光复节",
            "descText": "8月15日",
            "lemmaUrl": "https://baike.baidu.com/item/%E5%85%89%E5%A4%8D%E8%8A%82/10835902?fr=api_ACG_sales"
        },
        {
            "lemmaId": 128234,
            "lemmaTitle": "中秋节",
            "descText": "农历八月十五",
            "lemmaUrl": "https://baike.baidu.com/item/%E4%B8%AD%E7%A7%8B%E8%8A%82/128234?fr=api_ACG_sales"
        },
        {
            "lemmaId": 8576430,
            "lemmaTitle": "开天节",
            "descText": "10月3日",
            "lemmaUrl": "https://baike.baidu.com/item/%E5%BC%80%E5%A4%A9%E8%8A%82/8576430?fr=api_ACG_sales"
        },
        {
            "lemmaId": 9742981,
            "lemmaTitle": "韩文节",
            "descText": "10月9日",
            "lemmaUrl": "https://baike.baidu.com/item/%E9%9F%A9%E6%96%87%E8%8A%82/9742981?fr=api_ACG_sales"
        }
    ]
}
```

---

## 三、秒懂百科（视频检索）

`GET https://qianfan.baidubce.com/v2/baike/second_know/search_video`

> 原始文档：[秒懂百科](https://cloud.baidu.com/doc/qianfan-api/s/jmocjhoic)

### 概述

本接口通过词条内容或词条ID查询秒懂百科相关视频内容，返回视频列表信息。

> 注：原始文档页的调试地址为 `qianfan.baidubce.com`，但其「请求结构」HOST 与请求示例均使用 `appbuilder.baidu.com`，两个域名均可访问，下文示例保持原样。

### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`）外，无其它特殊头域。

**Query 参数**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `search_type` | `string` | 是 | 检索类型。<br>可选值：<br>lemmaTitle：按百科词条名<br>lemmaId：按百科词条ID |
| `search_key` | `string` | 是 | 检索关键字。与search_type对应的检索条件 |
| `limit` | `integer` | 否 | 限制获取数量。默认值：1。<br>匹配到多个百科词条时，此参数指每个词条的限制数量。 |
| `type` | `integer` | 否 | 视频类型。默认值：0<br>0：全部视频<br>1：概述型视频 |
| `platform` | `string` | 否 | 视频来源。可以取多值，用逗号隔开，默认值：user<br>user：高级用户（默认）<br>app：App用户<br>partner：合作方<br>pgc：PGC |

### 请求结构

```http
GET /v2/baike/second_know/search_video?search_type={search_type}&search_key={search_key} HTTP/1.1
HOST: appbuilder.baidu.com
Authorization: Bearer <API Key>
```

### 请求示例

```bash
curl --location 'https://appbuilder.baidu.com/v2/baike/second_know/search_video?search_type=lemmaTitle&search_key=人工智能' \
--header 'Authorization: Bearer ****'
```

### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 否 | 请求唯一标识ID |
| `code` | `string` | 否 | 响应状态码。`0` 表示成功，其他值表示异常。 |
| `message` | `string` | 否 | 错误消息 |
| `result` | `array<object>` | 否 | 返回的数据内容，秒懂视频数据列表 |
| `result[].lemma_id` | `integer` | 否 | 词条ID |
| `result[].lemma_title` | `string` | 否 | 词条名 |
| `result[].lemma_desc` | `string` | 否 | 百科义项名 |
| `result[].second_id` | `integer` | 否 | 秒懂视频ID |
| `result[].second_title` | `string` | 否 | 秒懂视频标题 |
| `result[].cover_pic_url` | `string` | 否 | 横版封面图URL |
| `result[].cover_pic` | `object` | 否 | 封面图数据 |
| `result[].cover_pic.src` | `string` | 否 | 封面图hiphotos的加密ID |
| `result[].forever_play_url_mp4` | `string` | 否 | 视频永久播放URL（mp4） |
| `result[].play_url_mp4` | `string` | 否 | 视频播放URL（mp4），时效URL |
| `result[].play_url_mp3` | `string` | 否 | 音频播放URL（mp3），时效URL |
| `result[].play_time` | `integer` | 否 | 视频时长，单位为秒 |
| `result[].second_type` | `integer` | 否 | 视频类型。1：概述型，2：解释型，3：延展阅读；根据话题查询无此字段 |
| `result[].status` | `integer` | 否 | 视频状态。0：新建转码中，1：转码完成，2：删除，1001：上线，1002：下线 |
| `result[].is_vertical` | `integer` | 否 | 横竖屏属性。0：横屏，1：竖屏 |

### 响应示例

```json
{
    "request_id": "fcf5d6a8-b569-41d5-a944-a193ebbde4dd",
    "result": [
        {
            "lemma_id": 9180,
            "lemma_title": "人工智能",
            "lemma_desc": "智能科学与技术专业术语",
            "second_id": 586534,
            "cover_pic_url": "https://bkimg.cdn.bcebos.com/pic/9d82d158ccbf6c81151d1e0db23eb13533fa4028?x-bce-process=image/format,f_auto",
            "second_title": "全球首个AI设计药物，AI再添新功能",
            "forever_play_url_mp4": "https://baikevideo.cdn.bcebos.com/media/mda-Og3jUzKHv5Z824nu/573d0831e9a74957667c783c4d0f4648.mp4?platform=ACG_sales",
            "play_time": 53,
            "is_vertical": 1,
            "status": 1001,
            "second_type": 2,
            "cover_pic": {
                "src": "9d82d158ccbf6c81151d1e0db23eb13533fa4028",
                "verticalSrc": "e4dde71190ef76c6d1dec9ce9316fdfaae5167c2"
            },
            "play_url_mp3": "https://second-know.cdn.bcebos.com/media/mda-Og3jUzKHv5Z824nu/0d869eff5d70f5d3ddfc8280aee405a6.mp3?auth_key=1777022813-931769-0-43feefafacce514427c013f9483f3d20&platform=ACG_sales",
            "play_url_mp4": "https://second-know.cdn.bcebos.com/media/mda-Og3jUzKHv5Z824nu/573d0831e9a74957667c783c4d0f4648.mp4?auth_key=1777022813-569990-0-f4a583b200ea99ec1721a02028f23a80&platform=ACG_sales"
        },
        {
            "lemma_id": 3751704,
            "lemma_title": "人工智能",
            "lemma_desc": "2001年史蒂文·斯皮尔伯格执导的电影",
            "second_id": 36287,
            "cover_pic_url": "https://bkimg.cdn.bcebos.com/pic/b21c8701a18b87d6e25eddfa0a0828381f30fd33?x-bce-process=image/format,f_auto",
            "second_title": "一分钟了解人工智能",
            "forever_play_url_mp4": "https://baikevideo.cdn.bcebos.com/media/mda-Og9wCU7ehu4iIlST/920a917ee6da376fa7ac2b91bca32138.mp4?platform=ACG_sales",
            "play_time": 45,
            "is_vertical": 0,
            "status": 1001,
            "second_type": 1,
            "cover_pic": {
                "src": "b21c8701a18b87d6e25eddfa0a0828381f30fd33",
                "verticalSrc": ""
            },
            "play_url_mp3": "https://second-know.cdn.bcebos.com/media/mda-Og9wCU7ehu4iIlST/015d0d239fd2e78853aa0aa67901e68b.mp3?auth_key=1777022813-396674-0-5f082f97c8bdf92f44414027de0c7ff2&platform=ACG_sales",
            "play_url_mp4": "https://second-know.cdn.bcebos.com/media/mda-Og9wCU7ehu4iIlST/920a917ee6da376fa7ac2b91bca32138.mp4?auth_key=1777022813-511754-0-a3e42adf5be60a0219943f071440feb3&platform=ACG_sales"
        },
        {
            "lemma_id": 58131596,
            "lemma_title": "人工智能",
            "lemma_desc": "博士、硕士层次专业",
            "second_id": 76692570,
            "cover_pic_url": "https://bkimg.cdn.bcebos.com/pic/faf2b2119313b07eca806c3e4880862397dda14426f4?x-bce-process=image/format,f_auto",
            "second_title": "一分钟了解人工智能",
            "forever_play_url_mp4": "https://baikevideo.cdn.bcebos.com/media/mda-OdZqVczOmPXU0VoI/4ff381d2776072e43d0bc166525facb7.mp4?platform=ACG_sales",
            "play_time": 51,
            "is_vertical": 0,
            "status": 1001,
            "second_type": 1,
            "cover_pic": {
                "src": "faf2b2119313b07eca806c3e4880862397dda14426f4",
                "verticalSrc": ""
            },
            "play_url_mp3": "https://second-know.cdn.bcebos.com/media/mda-OdZqVczOmPXU0VoI/38207825ad74040007a1d935fed87029.mp3?auth_key=1777022813-234312-0-2fa4ec71e1689d8a5c2cb7833d587276&platform=ACG_sales",
            "play_url_mp4": "https://second-know.cdn.bcebos.com/media/mda-OdZqVczOmPXU0VoI/4ff381d2776072e43d0bc166525facb7.mp4?auth_key=1777022813-292326-0-afef89145afdbef6cfd7b3fd7032487b&platform=ACG_sales"
        }
    ]
}
```

---

## 四、百科词条（词条列表检索）

`GET https://appbuilder.baidu.com/v2/baike/lemma/get_list_by_title`

> 原始文档：[百科词条](https://cloud.baidu.com/doc/qianfan-api/s/0mocjdxi9)

### 概述

本接口用于通过输入的词条内容查询到相关的百科词条列表。

**计费方式**：详情可见[组件计费](https://cloud.baidu.com/doc/qianfan/s/Umh4sv6gb)。

> 注：原始文档页的调试地址与「请求结构」HOST 为 `appbuilder.baidu.com`，但其请求示例使用 `qianfan.baidubce.com`，两个域名均可访问，下文示例保持原样。

### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`）外，无其它特殊头域。

**Query 参数**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `lemma_title` | `string` | 是 | 词条名 |
| `top_k` | `integer` | 否 | 返回的结果数量。默认值：5。取值范围：[1，100] |

### 请求结构

```http
GET /v2/baike/lemma/get_list_by_title?lemma_title={词条名}&top_k={值} HTTP/1.1
HOST: appbuilder.baidu.com
Authorization: Bearer <API Key>
```

### 请求示例

```bash
curl -X GET "https://qianfan.baidubce.com/v2/baike/lemma/get_list_by_title?lemma_title=刘德华&top_k=5" \
  -H "Authorization: Bearer bce-v3/ALTAK-******ZftZDTn7/125eeb1c5e9ddc8cf3edf18ef6d03f1517ec9408"
```

### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 否 | 请求ID |
| `code` | `string` | 否 | 0 表示成功，其他都是异常 |
| `message` | `string` | 否 | 错误消息 |
| `result` | `array<object>` | 否 | 返回结果列表 |
| `result[].lemma_id` | `integer` | 否 | 词条ID |
| `result[].lemma_title` | `string` | 否 | 词条名 |
| `result[].lemma_desc` | `string` | 否 | 义项描述 |
| `result[].is_default` | `integer` | 否 | 是否主义项<br>0：非主义项<br>1：主义项 |
| `result[].url` | `string` | 否 | 词条页URL |

### 响应示例

```json
[
  {
    "lemma_desc": "华语影视男演员、流行乐歌手、电影制片人、作词人",
    "lemma_id": 114923,
    "lemma_title": "刘德华",
    "url": "https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/114923?fr=api_ACG_sales"
  },
  {
    "lemma_desc": "民航局空中交通管理局原局长助理",
    "lemma_id": 18059685,
    "lemma_title": "刘德华",
    "url": "https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/18059685?fr=api_ACG_sales"
  },
  {
    "lemma_desc": "清华大学教授",
    "lemma_id": 18062692,
    "lemma_title": "刘德华",
    "url": "https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/18062692?fr=api_ACG_sales"
  },
  {
    "lemma_desc": "江西弋阳籍烈士",
    "lemma_id": 21508047,
    "lemma_title": "刘德华",
    "url": "https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/21508047?fr=api_ACG_sales"
  },
  {
    "lemma_desc": "国家税务总局广安经济技术开发区税务局党委委员、副局长",
    "lemma_id": 20869893,
    "lemma_title": "刘德华",
    "url": "https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/20869893?fr=api_ACG_sales"
  }
]
```

> 注：原始文档的响应示例仅展示了 `result` 数组部分（未包含 `request_id`、`code`、`message` 外层字段），此处保持原样。

---

## 五、百度百科（词条详情内容）

`GET https://appbuilder.baidu.com/v2/baike/lemma/get_content`

> 原始文档：[百度百科](https://cloud.baidu.com/doc/qianfan-api/s/Cmocj7w03)

### 概述

本接口可通过输入词条内容或词条ID查询到详细的百科内容。

### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`）外，无其它特殊头域。

**Query 参数**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `search_type` | `string` | 是 | 检索类型，指定按哪种方式查询词条。<br>可选值：<br>lemmaTitle：按百科词条名<br>lemmaId：按百科词条ID |
| `search_key` | `string` | 是 | 检索关键字，与 `search_type` 对应的检索条件。<br>当 `search_type` 为 `lemmaTitle` 时，填写词条名称；为 `lemmaId` 时，填写词条ID。 |

### 请求结构

```http
GET /v2/baike/lemma/get_content?search_type=lemmaTitle&search_key=刘德华 HTTP/1.1
HOST: appbuilder.baidu.com
Authorization: Bearer <API Key>
```

### 请求示例

按词条名查询：

```bash
curl -X GET "https://appbuilder.baidu.com/v2/baike/lemma/get_content?search_type=lemmaTitle&search_key=刘德华" \
  -H "Authorization: Bearer bce-v3/ALTAK-******ZftZDTn7/125eeb1c5e9ddc8cf3edf18ef6d03f1517ec9408"
```

按词条ID查询：

```bash
curl -X GET "https://appbuilder.baidu.com/v2/baike/lemma/get_content?search_type=lemmaId&search_key=114923" \
  -H "Authorization: Bearer bce-v3/ALTAK-******ZftZDTn7/125eeb1c5e9ddc8cf3edf18ef6d03f1517ec9408"
```

### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `request_id` | `string` | 否 | 请求唯一标识ID |
| `code` | `string` | 否 | 响应状态码。`0` 表示成功，其他值表示异常。 |
| `message` | `string` | 否 | 错误消息 |
| `result` | `object` | 否 | 义项内容，请求成功时返回词条的详细结构化数据 |
| `result.lemma_id` | `integer` | 否 | 词条ID |
| `result.lemma_title` | `string` | 否 | 词条名 |
| `result.lemma_desc` | `string` | 否 | 义项描述 |
| `result.url` | `string` | 否 | 词条页URL，移动设备支持自动适配 |
| `result.summary` | `string` | 否 | 词条摘要，优先提取概述内容；无概述时提取正文前若干字，不超过400字节 |
| `result.abstract_plain` | `string` | 否 | 词条概述（纯文本格式），使用 `\n` 换行 |
| `result.abstract_html` | `string` | 否 | 词条概述（HTML格式） |
| `result.abstract_structured` | `string` | 否 | 词条概述（结构化数据格式） |
| `result.pic_url` | `string` | 否 | 概述图片URL |
| `result.square_pic_url` | `string` | 否 | 概述图片URL（自动裁切为方图），可用于分享、icon等场景 |
| `result.square_pic_url_wap` | `string` | 否 | 移动端概述图片URL（自动裁切为方图），可用于分享、icon等场景 |
| `result.card` | `array<object>` | 否 | 基本信息栏项目列表 |
| `result.card_type` | `integer` | 否 | 基本信息栏类型 |
| `result.albums` | `array<object>` | 否 | 图册列表 |
| `result.classify` | `array<string>` | 否 | 词条分类标签列表，例如：`["演员", "体育人物"]` |
| `result.star_map` | `array<object>` | 否 | 星图列表 |
| `result.videos` | `array<object>` | 否 | 视频列表，包含与该词条相关的秒懂视频信息 |
| `result.videos[].second_id` | `integer` | 否 | 秒懂视频ID |
| `result.videos[].second_title` | `string` | 否 | 秒懂词条名 |
| `result.videos[].cover_pic_url` | `string` | 否 | 视频封面原图URL |
| `result.videos[].page_url` | `string` | 否 | 视频播放页URL |
| `result.relations` | `array<object>` | 否 | 关系列表，包含与该词条相关联的其他词条信息 |
| `result.relations[].lemma_title` | `string` | 否 | 客体词条名 |
| `result.relations[].lemma_id` | `integer` | 否 | 客体词条ID |
| `result.relations[].relation_name` | `string` | 否 | 关系名，描述当前词条与客体词条之间的关系，例如：妻子、导演等 |
| `result.relations[].square_pic_url` | `string` | 否 | 客体词条方图URL |

### 响应示例

```json
{
  "request_id": "7d932904-be53-456b-8783-efb0d8c9dc0c",
  "result": {
    "content_plain": null,
    "lemma_desc": "华语影视男演员、流行乐歌手、电影制片人、作词人",
    "lemma_id": 114923,
    "lemma_title": "刘德华",
    "pic_url": "https://bkimg.cdn.bcebos.com/pic/bd315c6034a85edf8db1a7cc510c1e23dd54574edf9e",
    "relations": [
      {
        "lemma_id": 63815079,
        "lemma_title": "朱丽蒨",
        "relation_name": "妻子",
        "square_pic_url": "https://bkimg.cdn.bcebos.com/pic/a044ad345982b2b7d0a25312c6f7dcef76094a362de8?x-bce-process=image/resize,m_fill,w_1024,h_1024,align_0,limit_0/format,f_auto"
      }
    ],
    "summary": "刘德华（Andy Lau），1961年9月27日出生于中国香港，华语影视男演员、流行乐歌手、电影制片人、作词人。1981年，出演首部电影《彩云曲》并进入演艺圈。1985年，发行首张专辑《只知道此刻爱你》。1990年，凭借专辑《可不可以》在歌坛获得关注；同年，主演陈木胜执导的爱情片《天若有情》。1992年，发行的粤语专辑《真我的风采》在中国香港取得40万张销量。1993年，首次在红馆举行个人演唱会。1994年，获十大劲歌金曲最受欢迎男歌星奖。1995年，登上央视春晚并演唱歌曲《忘情水》。2000年，凭借警匪片《暗战》获第19届香港电影金像奖最佳男主角奖；同年，发行音乐专辑《男人的爱》，并被《吉尼斯世界纪录大全》评为\"获奖最多的香港男歌手\"。2002年，主演的警匪片《无间道》成为其电影生涯代表作。2004年，凭剧情片《大块头有大智慧》获第23届香港电影金像奖最佳男主角奖，又凭警匪片《无间道3：",
    "url": "https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/114923?fr=api_ACG_sales",
    "videos": [
      {
        "cover_pic_url": "https://bkimg.cdn.bcebos.com/pic/29381f30e924b899a901feef3f4d0a950a7b0308589a",
        "page_url": "https://baike.baidu.com/item/%E5%88%98%E5%BE%B7%E5%8D%8E/114923?secondId=27412799&fr=api_ACG_sales",
        "second_id": 27412799,
        "second_title": "「贤于」刘德华，你凭什么能红一辈子？"
      }
    ]
  }
}
```
