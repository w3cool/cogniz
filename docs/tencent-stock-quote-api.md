# 腾讯股票行情接口解析与实测笔记

> 主要来源：
>
> - [腾讯股票行情接口 `qt.gtimg.cn` 完整格式解析](https://www.cnblogs.com/soarowl/p/20523904)，卓能文，2026
> - [腾讯股票数据接口 HTTP/JavaScript](https://developer.aliyun.com/article/545892)，阿里云开发者社区转载的历史资料，2017
> - [腾讯股票分时接口](https://www.cnblogs.com/soarowl/p/20516538)，卓能文，2026
> - [获取股票数据（腾讯接口）](https://zhuanlan.zhihu.com/p/1979132128676573377)，一条狗，2025
>
> 整理日期：2026-09-29
>
> 说明：本文是对来源文章的归纳、交叉对照和补充示例，并非原文转载。阿里云资料使用的是 2012 年行情样本，适合了解接口变体，不应直接视为当前协议。两篇分时资料对第 4 列的解释存在冲突，本文依据实时响应给出验证结论。本文引用的来源没有提供正式协议承诺，生产使用前应以实际响应验证字段。仓库中的[实时验证脚本](./verify_tencent_stock_quote_api.py)可重复检查本文的可验证结论。

## 1. 接口概览

本文涉及两类腾讯财经接口：`qt.gtimg.cn` 的行情快照返回以 `~` 分隔的纯文本，`web.ifzq.gtimg.cn` 的当日分时接口返回 JSON。A 股快照请求通常把市场前缀和证券代码拼接到查询参数中：

```text
https://qt.gtimg.cn/q=sh600000
```

HTTP 和 HTTPS 在 2026-09-29 的实测中都能返回数据。新代码应优先使用 HTTPS，避免明文传输以及浏览器的混合内容限制。

常见市场前缀：

| 前缀 | 市场 | 示例 |
| --- | --- | --- |
| `sh` | 上海证券交易所 | `sh600000` |
| `sz` | 深圳证券交易所 | `sz000001` |
| `hk` | 港股 | 字段可能与 A 股不同 |
| `us` | 美股 | 字段可能与 A 股不同 |

响应外层大致如下：

```text
v_sh600000="字段0~字段1~字段2~...";
```

解析时应当：

1. 按 GBK 解码响应字节。
2. 找到第一个 `="` 和结尾的 `";`，取出中间内容。
3. 使用 `~` 分割字段，同时保留空字符串。
4. 按字段下标读取数据，不要过滤空字段，否则后续下标会错位。

## 2. 核心行情字段

以下下标经过行情快照资料的原始响应和 2026-09-29 实时响应交叉对照。第 0 至 49 位核心结构在本次沪深 A 股样本中一致；第 50 位之后仍应视为易变的扩展字段。

“字段位置可验证”和“业务名称有官方保证”是两件事。价格、涨跌、高低价、成交量、成交额和盘口位置可以通过计算关系、重复字段及简要接口交叉验证；外盘/内盘、换手率、市盈率、市值、市净率和量比等业务名称来自来源文章，实时响应只能证明这些位置存在且数值形态合理。由于没有腾讯正式协议，后者应视为“来源定义”，不应当作官方契约。

| 下标 | 含义 | 常见单位或格式 |
| ---: | --- | --- |
| 0 | 供应商市场标识 | 沪市样本为 `1`，深市样本为 `51` |
| 1 | 证券名称 | 文本 |
| 2 | 证券代码 | 六位代码 |
| 3 | 最新价 | 元 |
| 4 | 昨日收盘价 | 元 |
| 5 | 今日开盘价 | 元 |
| 6 | 当日累计成交量 | 手 |
| 7 | 外盘 | 手，来源文章解释为主动买入量，科创板1手=200股，其他板1手=100股 |
| 8 | 内盘 | 手，来源文章解释为主动卖出量，科创板1手=200股，其他板1手=100股 |
| 30 | 数据更新时间 | `yyyyMMddHHmmss` |
| 31 | 涨跌额 | 元 |
| 32 | 涨跌幅 | 百分比数值 |
| 33 | 当日最高价 | 元 |
| 34 | 当日最低价 | 元 |
| 35 | 价格、成交量和成交额组合 | 使用 `/` 再次分隔 |
| 36 | 成交量 | 手，与下标 6 含义接近 |
| 37 | 成交额 | 万元 |
| 38 | 换手率 | 百分比数值 |
| 39 | 市盈率 TTM | 倍数 |
| 40 | 预留字段 | 当前沪深样本为空 |
| 41 | 当日最高价的重复字段 | 元 |
| 42 | 当日最低价的重复字段 | 元 |
| 43 | 振幅 | 百分比数值 |
| 44 | 流通市值 | 亿元 |
| 45 | 总市值 | 亿元；与简要接口下标 9 一致 |
| 46 | 市净率 | 倍数 |
| 47 | 涨停价 | 元 |
| 48 | 跌停价 | 元 |
| 49 | 量比 | 倍数 |

### 来源文章中的下标纠错

第一篇文章的原始响应在市盈率后包含一个空字段，即下标 40。其释义表跳过这个空字段后，把后续字段从 42 开始编号，造成了一位偏移。原始响应、第二篇历史资料以及本次实时测试共同支持上表中的排列：最高价重复字段从 41 开始，市净率为 46，涨停价和跌停价分别为 47、48，量比为 49。

来源文章将下标 50 之后解释为委差、均价、资金流向、币种、证券类别和接口标记等扩展数据。本次测试只确认部分位置可解析以及下标 61 的证券分类标记，不足以证明其余业务含义。它们可能随市场和版本变化，应先作为未知供应商字段保存，不宜建立强约束。

### 原始字段对照方法

来源文章将原始响应按下标展开，这种方法适合发现空字段和编号错位。实际排查时不要手工数分隔符，可以直接枚举：

```python
for index, value in enumerate(fields):
    print(f"{index:>2}: {value!r}")
```

除了查看单个字段，还应检查重复字段和可计算字段是否自洽：

| 校验 | 关系 |
| --- | --- |
| 涨跌额 | `字段 3 - 字段 4 ≈ 字段 31` |
| 涨跌幅 | `字段 31 / 字段 4 × 100 ≈ 字段 32` |
| 振幅 | `(字段 33 - 字段 34) / 字段 4 × 100 ≈ 字段 43` |
| 最高价重复值 | `字段 33 = 字段 41` |
| 最低价重复值 | `字段 34 = 字段 42` |
| 成交量重复值 | `字段 6 = 字段 36` |
| 组合字段 | 字段 35 的三段应分别对应最新价、成交量和成交额 |
| 成交额单位换算 | 字段 35 第三段（元）除以 10,000，约等于字段 37（万元） |

价格字段通常保留两位或更多小数，百分比字段也会舍入，因此数值比较应使用容差而非字符串严格计算。涨停、跌停比例还取决于板块和证券类型，不能统一假设为 10%。

## 3. 五档盘口字段

买卖盘口占用下标 9 至 28，每一档由价格和委托量两个字段组成：

| 档位 | 买价 | 买量 | 卖价 | 卖量 |
| --- | ---: | ---: | ---: | ---: |
| 一档 | 9 | 10 | 19 | 20 |
| 二档 | 11 | 12 | 21 | 22 |
| 三档 | 13 | 14 | 23 | 24 |
| 四档 | 15 | 16 | 25 | 26 |
| 五档 | 17 | 18 | 27 | 28 |

其中价格通常以元表示，数量通常以手表示。下标 29 可能承载逐笔成交信息，休市或非交易时段为空属于正常情况。历史样本显示，多条逐笔记录使用 `|` 分隔，单条记录内部再使用 `/` 分隔，内容包含成交时间、价格、数量、买卖方向标记等信息。该内部格式并未在两篇资料中形成完整、稳定的字段定义，建议先作为原始字符串保存，再用独立解析器处理。

可利用固定间隔生成盘口数据，而不必逐项硬编码：

```python
buy_levels = [
    {"level": level, "price": fields[9 + (level - 1) * 2], "volume": fields[10 + (level - 1) * 2]}
    for level in range(1, 6)
]

sell_levels = [
    {"level": level, "price": fields[19 + (level - 1) * 2], "volume": fields[20 + (level - 1) * 2]}
    for level in range(1, 6)
]
```

## 4. Python 解析示例

下面的示例只依赖 Python 标准库，并对响应外层格式和最低字段数进行检查：

```python
import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from urllib.request import urlopen
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Quote:
    name: str
    code: str
    latest: Decimal
    previous_close: Decimal
    open_price: Decimal
    volume_lots: int
    change: Decimal
    change_percent: Decimal
    updated_at: datetime


def fetch_quote(symbol: str) -> Quote:
    if not re.fullmatch(r"(?:sh|sz)\d{6}", symbol):
        raise ValueError("Unsupported symbol format")

    url = f"https://qt.gtimg.cn/q={symbol}"
    with urlopen(url, timeout=5) as response:
        text = response.read().decode("gbk")

    prefix = f'v_{symbol}="'
    if not text.startswith(prefix) or not text.rstrip().endswith('";'):
        raise ValueError("Unexpected quote response")

    payload = text[len(prefix) : text.rfind('";')]
    fields = payload.split("~")
    if len(fields) < 50:
        raise ValueError(f"Quote response has only {len(fields)} fields")

    return Quote(
        name=fields[1],
        code=fields[2],
        latest=Decimal(fields[3]),
        previous_close=Decimal(fields[4]),
        open_price=Decimal(fields[5]),
        volume_lots=int(fields[6]),
        change=Decimal(fields[31]),
        change_percent=Decimal(fields[32]),
        updated_at=datetime.strptime(fields[30], "%Y%m%d%H%M%S").replace(
            tzinfo=ZoneInfo("Asia/Shanghai")
        ),
    )
```

金额与价格建议使用 `Decimal`，避免二进制浮点数带来的精度误差。网络请求还应增加重试、速率限制和日志，但不要在日志中保存不必要的完整行情响应。

## 5. TypeScript 解析示例

浏览器直接调用第三方 HTTP 接口可能遇到跨域和 HTTPS 混合内容限制，因此更适合由后端请求，再向前端提供结构化 JSON。以下函数用于解析后端已经取得并正确解码的文本：

```ts
type Quote = {
  name: string
  code: string
  latest: number
  previousClose: number
  open: number
  volumeLots: number
  change: number
  changePercent: number
  updatedAt: string
}

export function parseTencentQuote(symbol: string, text: string): Quote {
  if (!/^(?:sh|sz)\d{6}$/.test(symbol)) {
    throw new Error("Unsupported symbol format")
  }

  const prefix = `v_${symbol}="`
  const normalized = text.trim()

  if (!normalized.startsWith(prefix) || !normalized.endsWith('";')) {
    throw new Error("Unexpected quote response")
  }

  const fields = normalized.slice(prefix.length, -2).split("~")
  if (fields.length < 50) {
    throw new Error(`Quote response has only ${fields.length} fields`)
  }

  const required = (index: number) => {
    const value = fields[index]
    if (value === undefined || value === "") {
      throw new Error(`Missing quote field ${index}`)
    }
    return value
  }

  const requiredNumber = (index: number) => {
    const value = Number(required(index))
    if (!Number.isFinite(value)) {
      throw new Error(`Invalid numeric quote field ${index}`)
    }
    return value
  }

  const updatedAt = required(30)
  if (!/^\d{14}$/.test(updatedAt)) {
    throw new Error("Invalid quote timestamp")
  }

  return {
    name: required(1),
    code: required(2),
    latest: requiredNumber(3),
    previousClose: requiredNumber(4),
    open: requiredNumber(5),
    volumeLots: requiredNumber(6),
    change: requiredNumber(31),
    changePercent: requiredNumber(32),
    updatedAt,
  }
}
```

## 6. 数据处理注意事项

### 编码

证券名称等中文内容使用 GBK 编码。Python 可直接按 GBK 解码；Node.js 原生 `TextDecoder` 对 GBK 的运行时支持需实际验证，也可以使用可靠的字符编码库在服务端完成转换。

### 空字段

连续两个分隔符表示中间字段为空。不要先删除空字符串再读取字段，否则所有后续字段都会发生偏移。

### 单位

- 价格通常为人民币元。
- 成交量通常以手计，A 股一手一般为 100 股。
- 成交额在不同字段中可能分别使用元或万元。
- 市值字段通常以亿元计。
- 百分比字段返回的是百分比数值，例如 `2.35` 表示 `2.35%`。

### 时间与交易状态

更新时间是行情数据自身的时间，不等同于 HTTP 响应到达时间。休市、停牌或盘后场景可能出现价格不变、盘口为空或逐笔数据缺失，调用方应当同时保留更新时间并判断数据是否过期。

### 字段稳定性

最新价、昨收、开盘、成交量、五档盘口、更新时间和涨跌等核心字段相对稳定；后部扩展字段更容易随市场和版本变化。建议：

1. 只解析业务确实使用的字段。
2. 检查最低字段数和必填字段。
3. 保留未知字段用于短期诊断，但不要向业务层暴露无语义下标。
4. 为不同市场分别维护解析器和样本测试。
5. 定期用实际响应回归验证字段含义。

## 7. 建议的数据模型

不要让业务代码直接依赖 `fields[31]` 这类下标。可以把解析结果分成以下结构：

```text
Quote
├── identity        名称、代码、市场
├── price           最新、昨收、开盘、最高、最低
├── change          涨跌额、涨跌幅、振幅
├── trading         成交量、成交额、换手率、量比
├── orderBook       买一至买五、卖一至卖五
├── valuation       市盈率、市净率、市值、每股净资产
└── sourceMetadata  数据时间、原始字段数量、接口来源
```

这样可以把第三方接口的字段变化限制在适配层内，避免影响数据库、API 响应和前端组件。

## 8. 其他接口变体

历史资料还记录了同一域名下的三种查询前缀。它们返回相同的 JavaScript 变量赋值外壳，但内部字段结构彼此独立。

| 用途 | 查询形式 | 预期响应变量前缀 | 2026-09-29 实测 |
| --- | --- | --- | --- |
| 完整行情 | `q=sz000858` | `v_sz000858` | 可用，返回 88 个字段 |
| 资金流向 | `q=ff_sz000858` | `v_ff_sz000858` | 不可用，返回 `v_pv_none_match="1";` |
| 盘口分析 | `q=s_pksz000858` | `v_s_pksz000858` | 可用，返回 4 个字段 |
| 简要行情 | `q=s_sz000858` | `v_s_sz000858` | 可用，返回 12 个字段 |

这些接口来自非正式的历史观察资料，没有稳定性承诺。上表只表示本次测试结果，不代表未来可用性或访问频率限制。

### 8.1 简要行情 `s_`

简要接口适合只需要名称、价格、涨跌和成交数据的场景。历史样本包含 10 个字段；本次沪深样本包含 12 个字段，前 10 位含义保持一致，随后新增证券类别和一个空字段。

| 下标 | 含义 |
| ---: | --- |
| 0 | 市场标识或未知标识 |
| 1 | 证券名称 |
| 2 | 证券代码 |
| 3 | 当前价格 |
| 4 | 涨跌额 |
| 5 | 涨跌幅 |
| 6 | 成交量，单位为手 |
| 7 | 成交额，单位为万元 |
| 8 | 预留或空字段 |
| 9 | 总市值 |
| 10 | 供应商证券分类标记，如 `GP-A`、`GP-A-CYB` |
| 11 | 扩展字段，本次样本为空 |

调用形式：

```text
https://qt.gtimg.cn/q=s_sz000858
```

完整行情和简要行情虽然包含部分相同数据，但字段下标不同，应使用不同的数据模型与解析函数。

本次四个股票样本中，简要接口的名称、代码、现价、涨跌额、涨跌幅、成交量、成交额和总市值分别与完整接口的下标 1、2、3、31、32、6、37、45 一致。这种跨接口一致性支持上表的位置判断，但仍不构成长期稳定性承诺。

### 8.2 盘口分析 `s_pk`

历史资料把盘口分析响应的四个比例解释为：

| 下标 | 含义 |
| ---: | --- |
| 0 | 买盘大单占比 |
| 1 | 买盘小单占比 |
| 2 | 卖盘大单占比 |
| 3 | 卖盘小单占比 |

调用形式：

```text
https://qt.gtimg.cn/q=s_pksz000858
```

这些数值采用 0 至 1 之间的小数比例，而不是带 `%` 的字符串。2026-09-29 实测中，浦发银行四项之和为 `0.999`，五粮液四项之和为 `1.000`，差异符合三位小数四舍五入。因此按百分比展示时应乘以 100，并允许总和存在小幅舍入误差。

实时响应只能验证“四个 0 至 1 的比例、总和约为 1”，无法仅凭这四个数证明它们依次代表大单买入、小单买入、大单卖出和小单卖出。表中的业务名称属于历史资料定义；若该分类会影响交易判断，应使用另一份独立数据源交叉验证。

### 8.3 资金流向 `ff_`

资金流向接口的历史样本包含代码、两组流入/流出/净额/比例数据、若干汇总金额、证券名称和日期：

```text
https://qt.gtimg.cn/q=ff_sz000858
```

但在 2026-09-29 对 `ff_sh600000` 和 `ff_sz000858` 的测试中，服务端都返回：

```text
v_pv_none_match="1";
```

这表示请求未匹配到该历史接口，当前不能依赖 `ff_` 获取资金流向。以下结构说明仅用于解读旧数据或兼容已有存档。

历史文章给出了样本，却没有逐一可靠说明全部下标的业务含义。可以确认的结构特征包括：

- 下标 0 是带市场前缀的证券代码。
- 下标 3 等于前一组两个金额字段之差，下标 4 是对应比例。
- 下标 7 等于后一组两个金额字段之差，下标 8 是对应比例。
- 尾部包含证券名称和 `yyyyMMdd` 日期。

在没有当前接口说明或多组样本交叉验证前，建议把中间字段命名为供应商原始字段，不要擅自解释成主力、散户、超大单等具体概念。错误的资金分类会比缺少该字段更具误导性。新功能应选择有正式文档和可用性承诺的数据源。

### 8.4 通用外壳解析器

不同前缀可以共享外层解析逻辑，再交给各自的字段解析器：

```python
import re


RESPONSE_PATTERN = re.compile(r'^v_([^=]+)="(.*)";$')


def split_tencent_response(text: str) -> tuple[str, list[str]]:
    match = RESPONSE_PATTERN.fullmatch(text.strip())
    if not match:
        raise ValueError("Unexpected Tencent quote response")

    response_key, payload = match.groups()
    return response_key, payload.split("~")
```

调用方应验证 `response_key` 是否与请求参数匹配，例如请求 `s_sz000858` 时只接受 `v_s_sz000858` 对应的 key。

### 8.5 当日分时接口

两篇新增资料都介绍了当日分钟级走势接口：

```text
https://web.ifzq.gtimg.cn/appstock/app/minute/query?code=sz159326
```

请求方式为 `GET`，`code` 使用与快照接口相同的市场前缀，例如 `sh600000`、`sz000858`、`sz159326`。2026-09-29 实测响应是 UTF-8 JSON，但服务器声明的 `Content-Type` 是 `text/html; charset=UTF-8`，因此调用方不应只根据 MIME 类型决定是否解析 JSON。

当前响应的关键结构如下：

```json
{
  "code": 0,
  "msg": "",
  "data": {
    "sz159326": {
      "data": {
        "data": [
          "0930 1.536 9134 1402982.40"
        ],
        "date": "20260929"
      },
      "qt": {
        "v_ff_sz159326": [],
        "sz159326": [],
        "market": []
      },
      "mx_price": {
        "price": "",
        "mx": ""
      }
    }
  }
}
```

示例为了简洁省略了 `qt.sz159326` 的 88 个快照字段和 `market` 的市场状态字符串。若完整响应保存在变量 `response` 中，分钟数组的路径为：

```python
response["data"][symbol]["data"]["data"]
```

每条分钟记录由四个空格分隔字段组成：

| 位置 | 含义 | 格式或单位 |
| ---: | --- | --- |
| 0 | 时间 | 中国标准时间 `HHmm` |
| 1 | 当分钟价格 | 元 |
| 2 | 截至该分钟的累计成交量 | 手，通常每手 100 股 |
| 3 | 截至该分钟的累计成交额 | 元 |

第三、第四列都是累计值。若需要单分钟成交量和成交额，应使用相邻记录相减；跨交易日、数据回补或累计值下降时必须重新建立基线，不能产生负数增量。

#### 两篇分时资料的差异与纠错

博客园文章把四列解释为时间、价格、累计成交量和累计成交额，这与本次三个有效样本一致。知乎文章把第 4 列解释为均价，但实时值达到数百万或数亿元，且整日单调不减，实际是累计成交额。成交均价需要计算：

```text
成交均价 = 累计成交额（元）÷（累计成交量（手）× 100）
```

例如 `0930 1.536 9134 1402982.40` 的计算结果约为 `1.536` 元。不要把第四列直接作为均价，也不要遗漏每手 100 股的换算。

博客园文章对内嵌 `qt[symbol]` 数组的部分下标也存在错位。2026-09-29 的 ETF 和两个 A 股样本中，该数组均有 88 个字段，抽查的身份、价格、五档盘口、涨跌、高低价、涨跌停价和证券类型字段与同一时刻 `https://qt.gtimg.cn/q={symbol}` 完全一致。因此本次样本可复用第 2、3 节的快照字段映射：下标 4、5 分别是昨收和今开，下标 33、34 分别是当日最高和最低，9 至 18 是买一至买五，19 至 28 是卖一至卖五。仍应通过字段数和数值关系识别版本，不能假设所有市场永久一致。

还有三个边界值得单独处理：

- `qt.market` 是包含各市场开闭市状态的字符串数组，不是单个证券的分钟点。
- `mx_price` 和 `qt.v_ff_{symbol}` 在本次样本中为空，不能作为必填字段。
- 分钟数组最后一条的累计成交量不一定等于 `qt[symbol][6]`。三个样本在 15:30 均出现小幅差异，因此不能用二者严格相等作为有效性条件。

下面的解析器显式校验日期、快照数组和每条分钟记录，并按中国标准时间生成带时区时间：

```python
import json
import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlencode
from urllib.request import urlopen
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class MinutePoint:
    timestamp: datetime
    price: Decimal
    cumulative_volume_lots: int
    cumulative_amount_yuan: Decimal

    @property
    def vwap(self) -> Decimal | None:
        if self.cumulative_volume_lots == 0:
            return None
        shares = Decimal(self.cumulative_volume_lots * 100)
        return self.cumulative_amount_yuan / shares


def fetch_minute_points(symbol: str) -> list[MinutePoint]:
    if not re.fullmatch(r"(?:sh|sz)\d{6}", symbol):
        raise ValueError("Unsupported symbol format")

    query = urlencode({"code": symbol})
    url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?{query}"
    with urlopen(url, timeout=5) as response:
        payload = json.loads(response.read())

    if payload.get("code") != 0:
        raise ValueError(f"Minute endpoint error: {payload.get('msg', '')}")

    try:
        symbol_data = payload["data"][symbol]
        date_text = symbol_data["data"]["date"]
        rows = symbol_data["data"]["data"]
        quote_fields = symbol_data["qt"][symbol]
    except (KeyError, TypeError) as error:
        raise ValueError("Unexpected minute response structure") from error

    if (
        not re.fullmatch(r"\d{8}", date_text)
        or not isinstance(rows, list)
        or not rows
        or not isinstance(quote_fields, list)
        or len(quote_fields) < 50
    ):
        raise ValueError("Missing valid date or quote fields")

    points: list[MinutePoint] = []
    previous_volume = -1
    previous_amount = Decimal("-1")

    for row in rows:
        parts = row.split()
        if len(parts) != 4 or not re.fullmatch(r"\d{4}", parts[0]):
            raise ValueError(f"Invalid minute row: {row!r}")

        volume = int(parts[2])
        amount = Decimal(parts[3])
        if volume < previous_volume or amount < previous_amount:
            raise ValueError("Cumulative minute values moved backwards")

        timestamp = datetime.strptime(
            date_text + parts[0], "%Y%m%d%H%M"
        ).replace(tzinfo=ZoneInfo("Asia/Shanghai"))
        points.append(
            MinutePoint(
                timestamp=timestamp,
                price=Decimal(parts[1]),
                cumulative_volume_lots=volume,
                cumulative_amount_yuan=amount,
            )
        )
        previous_volume = volume
        previous_amount = amount

    return points
```

无效代码不能只看顶层状态判断。实测 `sh999999` 仍返回 `code=0` 和空 `msg`，但日期为空、`qt.sh999999` 是空数组，分钟数组只有异常哨兵字符串 `"  0"`。上面的日期、字段数和行格式校验会正确拒绝这种响应。

## 9. 版本识别建议

由于来源资料跨越多年，应显式记录解析版本：

```text
TencentQuoteEnvelope
├── requestedKey       请求参数，例如 sz000858 或 s_sz000858
├── responseKey        响应变量中的 key
├── parserVersion      解析规则版本
├── fieldCount         原始字段数
├── sourceTimestamp    行情时间（如接口提供）
├── receivedAt         系统接收时间
├── parsed             结构化结果
└── rawFields          原始字段数组（短期诊断使用）
```

版本选择至少应考虑：

1. 请求前缀：无前缀、`s_`、`s_pk` 或 `ff_`。
2. 市场前缀：`sh`、`sz`、`hk`、`us` 等。
3. 字段总数以及关键空字段的位置。
4. 数据时间和已验证的样本版本。
5. 数值关系是否满足预期，例如涨跌额约等于最新价减昨收。

如果无法识别版本，应返回“暂不支持的响应格式”，而不是用最接近的字段表强行解析。

## 10. 2026-09-29 实测记录

测试从项目的 FastAPI Docker 容器发起。第一轮使用浦发银行 `sh600000` 和五粮液 `sz000858`；第二轮扩大到浦发银行、五粮液、中国平安 `sh601318`、宁德时代 `sz300750`，并增加无效代码 `sh999999`；第三轮使用电网设备 ETF 华夏 `sz159326`、浦发银行和五粮液测试分时接口，并把内嵌快照与独立快照接口交叉对照。测试只读取公开响应，没有写入外部数据。

最终回归由仓库内的验证脚本执行，共 9 项测试：

```bash
docker compose --env-file config/compose.dev.env -f docker-compose.dev.yaml \
  exec -T cogniz-api python - < docs/verify_tencent_stock_quote_api.py
```

| 检查项 | 结果 |
| --- | --- |
| HTTP 完整行情 | 通过，响应声明 `charset=GBK` |
| HTTPS 完整行情 | 通过，响应声明 `charset=GBK` |
| 完整行情响应外壳 | 通过，变量 key 与请求参数一致 |
| 完整行情字段数 | 四个有效股票样本均为 88 |
| 名称和代码 | 通过 |
| `最新价 - 昨收 = 涨跌额` | 通过 |
| 涨跌幅计算 | 通过，允许小数舍入误差 |
| `最低价 ≤ 最新价 ≤ 最高价` | 通过 |
| 下标 35 的三段组合字段 | 通过 |
| 下标 35 成交额与下标 37 的单位换算 | 通过 |
| 下标 6 与 36 的成交量 | 四个样本均一致 |
| 下标 33/41 与 34/42 的高低价重复字段 | 四个样本均一致 |
| 下标 40 的预留字段 | 四个样本均为空 |
| 下标 43 的振幅公式 | 通过 |
| 下标 44/45 的流通市值和总市值关系 | 通过，总市值不小于流通市值 |
| 下标 47/48 的涨跌停价 | 通过；主板样本约为 ±10%，创业板样本约为 ±20% |
| 下标 49 的量比 | 四个样本均可解析为数值 |
| 五档盘口字段可解析为数值 | 通过 |
| 简要行情与完整行情的前六个业务字段 | 通过 |
| 简要行情成交额和总市值 | 分别与完整行情下标 37、45 一致 |
| 简要行情证券分类 | 主板样本为 `GP-A`，创业板样本为 `GP-A-CYB` |
| 盘口分析字段数与总和 | 通过，4 项之和约为 1；具体业务名称未独立验证 |
| 资金流向 `ff_` | 失败，接口返回 `pv_none_match` |
| 无效代码 | 返回 `v_pv_none_match="1";` |
| 分时接口 HTTP 与编码 | 通过，返回 UTF-8 JSON；MIME 类型误报为 `text/html` |
| 分时响应嵌套路径和日期 | 三个有效样本均通过 |
| 分时记录格式 | 三个有效样本各返回 267 条，均为 4 列且时间为 `HHmm` |
| 分时累计成交量和成交额 | 三个样本均单调不减 |
| 分时第 4 列语义 | 验证为累计成交额，不能直接作为均价 |
| 分时内嵌快照 | 三个样本均为 88 个字段；抽查字段与独立快照一致 |
| 分时接口无效代码 | 顶层仍为 `code=0`，但日期、快照和分钟行校验均失败 |
| 文档 Python 示例 | 6 个代码块均编译通过，快照和分时请求示例可执行 |
| 文档 TypeScript 示例 | 通过 TypeScript 5.9.3 严格模式编译 |
| 文档 JSON 示例 | 可被标准 JSON 解析器读取 |

本次测试发生在 A 股收盘后，下标 29 的最近逐笔成交字段为空，因此没有验证其内部记录格式。分时接口覆盖了一个 ETF，但仍没有覆盖停牌证券、指数、其他基金、港股、美股和交易时段内响应。267 条是本次样本结果，不应写成固定协议长度。

测试结论只说明“2026-09-29 的这些样本符合本文规则”。其中字段算术关系、重复位置、跨接口一致性和错误响应已由脚本强验证；外盘/内盘、估值字段、盘口分析四类占比及第 50 位之后多数扩展字段仍是来源资料的业务命名，没有腾讯正式协议或独立权威数据支持。

## 11. 验证清单

- [ ] 使用 GBK 解码，而不是默认 UTF-8。
- [ ] 保留分隔产生的空字段。
- [ ] 验证响应变量名与请求代码一致。
- [ ] 根据查询前缀选择独立解析器，不混用完整、简要、盘口和资金流向字段。
- [ ] 对分时 JSON 校验 `data[symbol].data.date`、`qt[symbol]` 和每条四列记录，不能只看顶层 `code`。
- [ ] 把分时第 3、4 列作为累计手数和累计成交额；均价需换算股数后计算。
- [ ] 验证字段总数和核心字段非空。
- [ ] 对第 50 位之后的扩展字段执行版本识别，不假设尾部下标长期稳定。
- [ ] 用涨跌额、涨跌幅、振幅、重复高低价和成交额换算检查响应自洽性。
- [ ] 使用十进制类型处理价格和金额。
- [ ] 明确区分手、股、元、万元和亿元。
- [ ] 将接口时间与系统接收时间分别保存。
- [ ] 为开盘、盘中、收盘、停牌和无效代码准备样本测试。
- [ ] 针对沪市、深市、港股和美股使用独立验证规则。
- [ ] 在升级解析规则或部署前运行 `docs/verify_tencent_stock_quote_api.py`。
- [ ] 将第三方接口视为非正式依赖，准备缓存、降级和字段变化监控。
