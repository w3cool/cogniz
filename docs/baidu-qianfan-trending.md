# 百度千帆 百度热搜 API 文档

> 本文档整理自百度千帆「AI 应用开发者中心 - API 参考（qianfan-api）」中「热搜榜单 - 百度热搜」页面：
>
> | 接口 | 方法 | 端点地址 | 原始文档 |
> | --- | --- | --- | --- |
> | 百度热搜 | GET | `https://qianfan.baidubce.com/v2/tools/baidu_trending` | [Rmp2ixg31](https://cloud.baidu.com/doc/qianfan-api/s/Rmp2ixg31) |
>
> 鉴权方式：请求头携带 `Authorization: Bearer <API Key>`，具体流程见[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

---

## 百度热搜（Baidu Trending）

`GET https://qianfan.baidubce.com/v2/tools/baidu_trending`

> 原始文档：[百度热搜](https://cloud.baidu.com/doc/qianfan-api/s/Rmp2ixg31)

### 概述

百度热搜工具可帮助用户快速获取当前最受关注的热搜内容。工具覆盖民生榜、电影榜、小说榜等多个垂直榜单，支持按领域高效查找热榜列表，呈现各类话题的关注焦点。

### 权限说明

调用本文API，需使用API Key鉴权方式。使用API Key鉴权调用API流程，具体调用流程，请查看[认证鉴权](https://cloud.baidu.com/doc/qianfan/s/Kmh4sutww)。

### 请求参数

**Headers**：除公共头域（`Authorization: Bearer <API Key>`、`Content-Type: application/json`）外，无其它特殊头域。

**URL 参数**：

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `tab` | `string` | 是 | 榜单类型，枚举值见下表 |

`tab` 枚举值：

| 取值 | 榜单 |
| --- | --- |
| `livelihood` | 民生榜 |
| `finance` | 财经榜 |
| `sports` | 体育榜 |
| `new_entertainment` | 文娱榜 |
| `internation_news` | 国际榜 |
| `challenge` | 挑战榜 |
| `movie` | 电影榜 |
| `teleplay` | 电视剧榜 |
| `novel` | 小说榜 |

### 请求结构

```http
GET /v2/tools/baidu_trending HTTP/1.1
HOST: qianfan.baidubce.com
Authorization: Bearer <API Key>
Content-Type: application/json
```

### 请求示例

```bash
curl --request GET \
  --url 'https://qianfan.baidubce.com/v2/tools/baidu_trending?tab=livelihood' \
  --header 'Authorization: Bearer bce-v3/ALTAK-*********VwdRiskoq/5fe76a06b6c27aa3bc51a82507075435269f681a'
```

### 响应参数

| 参数 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| `code` | `string` | 否 | 错误码，正常响应返回 0。 |
| `requestId` | `string` | 否 | 请求ID，问题定位时使用，当接口报错时请记录此ID。 |
| `message` | `string` | 否 | 错误描述。 |
| `logid` | `string` | 否 | 下游的请求ID。 |
| `data` | `array<object>` | 否 | 榜单结果列表。 |
| `data[].word` | `string` | 否 | 关键词，词条名。 |
| `data[].index` | `integer` | 否 | 索引排序号。 |
| `data[].query` | `string` | 否 | 用户搜索的问题。 |
| `data[].desc` | `string` | 否 | 描述信息。 |
| `data[].url` | `string` | 否 | 对应的热搜网页地址。 |
| `data[].img` | `string` | 否 | 对应的图片地址。 |
| `data[].show` | `array<string>` | 否 | 对应的标签列表，主要用于页面展示标签。 |
| `data[].hotScore` | `string` | 否 | 热度分数。 |
| `data[].hotChange` | `string` | 否 | 热度改变状态。 |
| `data[].hotTag` | `string` | 否 | 搜索标签值。枚举值：0：无；1：新；2：商；3：热；4：沸；5：爆。 |
| `data[].hotTagImg` | `string` | 否 | 搜索标签图片地址。 |

### 响应示例

```json
{
    "code": "0",
    "data": [
        {
            "desc": "七年连载，千万粉丝捧心期待。《骄阳似我》绝对不可错过的经典珍藏。“千金小姐”聂曦光行事低调，迷糊善良，大学时期经历了一次告白后没有回应而“单恋”后，黯然神伤，后来因为工作，她结识了家世相当的体贴温柔又有点傲娇自恋的林屿森，经历过一番误会和沟通后，才知道林屿森对她的用心专情，心中的天秤逐渐向林屿森倾斜，最终，二人的误会解开，开始了甜甜的恋爱故事。“如果比喜欢多一点就是爱，那么，比爱多一点是什么？”“比爱还要多一点？对我来说，就是你。”“我从来都是，为你而来。”",
            "hotChange": "down",
            "hotScore": "411472",
            "hotTag": "",
            "img": "https://fyb-2.cdn.bcebos.com/hotboard_image/28c13cf1cd5504672e9107601c61c7b2",
            "index": 0,
            "query": "骄阳似我（上） 小说",
            "show": [
                "作者：顾漫",
                "类型：现代言情"
            ],
            "url": "https://www.baidu.com/s?wd=%E9%AA%84%E9%98%B3%E4%BC%BC%E6%88%91%EF%BC%88%E4%B8%8A%EF%BC%89+%E5%B0%8F%E8%AF%B4&sa=fyb_novel_all&rsv_dl=fyb_novel_all",
            "word": "骄阳似我（上）"
        },
        {
            "desc": "大墟的祖训说，天黑，别出门。大墟残老村的老弱病残们从江边捡到了一个婴儿，取名秦牧，含辛茹苦将他养大。这一天夜幕降临，黑暗笼罩大墟，秦牧走出了家门……做个春风中荡漾的反派吧！瞎子对他说。秦牧的反派之路，正在崛起！书友群：600290060，624672265，VIP群：663057414（有验证）普通群：424940671",
            "hotChange": "up",
            "hotScore": "116047",
            "hotTag": "",
            "img": "https://fyb-2.cdn.bcebos.com/hotboard_image/8f2b9f1c08ee7971447c006705bfe5ae",
            "index": 1,
            "query": "牧神记 小说",
            "show": [
                "作者：宅猪",
                "类型：玄幻"
            ],
            "url": "https://www.baidu.com/s?wd=%E7%89%A7%E7%A5%9E%E8%AE%B0+%E5%B0%8F%E8%AF%B4&sa=fyb_novel_all&rsv_dl=fyb_novel_all",
            "word": "牧神记"
        },
        {
            "desc": "蒸汽与机械的浪潮中，谁能触及非凡？历史和黑暗的迷雾里，又是谁在耳语？我从诡秘中醒来，睁眼看见这个世界： 枪械，大炮，巨舰，飞空艇，差分机；魔药，占卜，诅咒，倒吊人，封印物……光明依旧照耀，神秘从未远离，这是一段“愚者”的传说。",
            "hotChange": "down",
            "hotScore": "98613",
            "hotTag": "",
            "img": "https://fyb-2.cdn.bcebos.com/hotboard_image/6b1e8f4838a31a95ebdf3690e56a2fcb",
            "index": 2,
            "query": "诡秘之主 小说",
            "show": [
                "作者：爱潜水的乌贼",
                "类型：奇幻"
            ],
            "url": "https://www.baidu.com/s?wd=%E8%AF%A1%E7%A7%98%E4%B9%8B%E4%B8%BB+%E5%B0%8F%E8%AF%B4&sa=fyb_novel_all&rsv_dl=fyb_novel_all",
            "word": "诡秘之主"
        }
    ],
    "logid": "28932854",
    "message": "api response ok",
    "requestId": "aa02c1d2-1e3a-4e6b-9a23-e78b4199eced"
}
```

> 注：原始文档的完整响应示例包含 30 条榜单数据（示例数据实际对应小说榜 `tab=novel` 的返回，与其请求示例中的民生榜 `tab=livelihood` 不一致），此处仅展示前 3 条。
