# 东方财富 Push2 行情接口解析与实测笔记

> 主要来源：
>
> - [东方财富 Python 爬虫实战：破解 push2 接口与动态参数调用](https://blog.csdn.net/weixin_29313817/article/details/165633307)，王科特，2026-09
> - [东方财富 push2/push2his 行情接口调用规范](https://github.com/roiding/shadowflow/blob/main/docs/EASTMONEY_PUSH2_API.md)，ShadowFlow，版本 1.5，2026-08-17
>
> 整理与实测日期：2026-09-30
>
> 本文是对来源资料的归纳、纠错和补充测试，并非原文转载。东方财富没有为这些网页内部接口提供本文可引用的正式开放协议，字段、参数和风控行为都可能变化。仓库中的[验证脚本](./verify_eastmoney_push2_api.py)可重复检查主要结构和当前可用性。

## 1. 范围与结论

本文只讨论东方财富网页使用的以下只读行情接口：

- 单证券行情快照：`/api/qt/stock/get`
- 个股或板块历史 K 线：`/api/qt/stock/kline/get`
- 当日分时：`/api/qt/stock/trends2/get`

2026-09-30 从项目 FastAPI Docker 容器发起的测试得到以下结论：

1. 正确构造的快照、个股日 K、板块日 K 和 `push2delay` 分时请求都曾在不携带 Cookie 的情况下返回 HTTP 200、`rc=0` 和有效数据。
2. 同一客户端随后出现多次 `RemoteDisconnected`，服务端在返回 HTTP 状态前关闭连接。这证明当前访问具有状态性或客户端分类行为，但不能推出固定 QPS、固定 Cookie 有效期或统一冷却时间。
3. `secid=90.BK1650` 的板块日 K 当前可用，因此历史 K 线接口并不限于个股。
4. CSDN 文章给出的所谓最简 `stock/get` 请求混入了列表接口的 `fid`、`fs` 参数，却缺少单证券查询所需的 `secid`；不应原样使用。
5. CSDN 文章列出的 `/api/qt/stock/fund/get` 在本次测试中返回 HTTP 404，不能作为已验证接口。
6. Cookie、请求头、连接行为和短期服务端状态可能共同影响结果。一次成功只能证明该次请求有效，不能证明批量采集稳定。

## 2. 域名与接口

| 用途 | 域名与路径 | 2026-09-30 结果 |
| --- | --- | --- |
| 单证券快照 | `https://push2.eastmoney.com/api/qt/stock/get` | 成功一次，HTTP 200、`rc=0` |
| 历史 K 线 | `https://push2his.eastmoney.com/api/qt/stock/kline/get` | 个股和板块均成功 |
| 当日分时 | `https://push2delay.eastmoney.com/api/qt/stock/trends2/get` | 成功，完整收盘样本 241 条 |
| 当日分时候选域 | `push2his.eastmoney.com`、`push2.eastmoney.com` 的相同路径 | 后续请求被断开，本次无法判定内容 |
| 财务摘要 | `https://push2.eastmoney.com/api/qt/stock/fund/get` | HTTP 404，不可用 |

来源资料还列出 `/api/qt/clist/get`、`/api/qt/slist/get`、`/api/qt/stock/fflow/kline/get` 和 `/api/qt/ulist/get`。本次没有逐一验证，不能将它们的字段和访问条件直接套用到本文三个接口。

## 3. 证券标识与通用参数

### 3.1 `secid`

`secid` 由市场编号和证券代码组成，中间使用点号：

| `secid` | 含义 | 示例 |
| --- | --- | --- |
| `1.<code>` | 沪市证券 | `1.600519` 贵州茅台 |
| `0.<code>` | 深市证券 | `0.000001` 平安银行 |
| `90.<BKcode>` | 东方财富板块 | `90.BK1650` 通信技术 |

市场编号是供应商内部标识，不应与交易所代码混为一谈。调用方应显式保存原始 `secid`，避免只凭证券代码猜市场。

### 3.2 常见参数

| 参数 | 作用 | 验证状态 |
| --- | --- | --- |
| `fields` | 快照接口需要返回的字段列表 | 已验证 |
| `fields1` | K 线或分时的元数据字段列表 | 已验证请求可用，本文不解释每一位 |
| `fields2` | K 线或分时每行的字段顺序 | 已验证 |
| `ut` | 网页请求中常见的固定格式 token | 带该值的请求成功；是否必需未完成隔离测试 |
| `fltt` | 快照数值返回格式 | `fltt=1` 的 A 股价格以缩放整数返回 |
| `invt` | 网页快照请求中的格式参数 | 与成功样本一起使用，独立作用未验证 |
| `cb` | JSONP 回调函数名 | 响应去壳逻辑已测试；本轮实时 JSONP 请求被断开 |
| `_` | 网页常用的 epoch 毫秒缓存破坏参数 | 本文最小 JSON 请求没有使用 |

来源文档使用的 `ut` 值为：

```text
fa5fd1943c7b386f172d6893dbfba10b
```

它不是用户登录凭据，但也不是东方财富公开承诺的稳定参数。实现时应集中配置；测试开始失败时，应从当时真实网页请求重新核对，而不是永久硬编码后假设其不会变化。

`fltt=1` 的贵州茅台样本中，`f43=125862` 表示 `1258.62` 元，价格字段需按该证券的小数精度缩放。不同证券可能使用不同精度，不应全局写死除以 100。常见资料认为 `fltt=2` 可直接返回带小数的值，但本次后续验证请求被服务端断开，因此没有把它记录为本轮成功结论。

## 4. 单证券行情快照

### 4.1 正确请求

```text
GET https://push2.eastmoney.com/api/qt/stock/get
    ?secid=1.600519
    &ut=fa5fd1943c7b386f172d6893dbfba10b
    &invt=2
    &fltt=1
    &fields=f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f60,f116,f117,f162,f167
```

本次响应包含请求的 16 个字段：

| 字段 | 来源资料定义 | 本次可验证关系 |
| --- | --- | --- |
| `f43` | 最新价 | 位于最低价和最高价之间 |
| `f44` / `f45` | 最高价 / 最低价 | `f45 ≤ f43 ≤ f44` |
| `f46` | 开盘价 | 正数价格字段 |
| `f47` | 成交量 | 与当日日 K、分时累计量一致 |
| `f48` | 成交额 | 与当日日 K、分时累计额一致 |
| `f50` | 量比 | 来源定义；业务语义无法仅凭单个响应证明 |
| `f51` / `f52` | 涨停价 / 跌停价 | 贵州茅台样本约为昨收的 110% / 90% |
| `f57` / `f58` | 证券代码 / 名称 | 返回 `600519` / `贵州茅台` |
| `f60` | 昨收 | 可用于验证涨跌和涨跌停比例 |
| `f116` / `f117` | 总市值 / 流通市值 | 本样本两者相等；一般应满足总市值不小于流通市值 |
| `f162` | 市盈率动态值 | 来源定义，`fltt=1` 样本需缩放 |
| `f167` | 市净率 | 来源定义，`fltt=1` 样本需缩放 |

应先检查顶层 `rc == 0` 和 `data` 是对象，再读取字段。只检查 HTTP 200 不足以说明业务成功。

### 4.2 对 CSDN 请求示例的纠错

CSDN 文章的长 URL 存在以下问题：

- 对 `/api/qt/stock/get` 使用了 `fid` 和 `fs`，这组参数通常用于列表筛选；单证券快照应使用 `secid`。
- 请求没有指定证券，却声称能返回某只证券的完整行情，目标与参数不一致。
- `fields` 从 `f1` 连续罗列到上千位，既不是最小参数集，也会放大字段变更和服务端拒绝风险。实际请求只应声明业务需要的字段。
- 文章声称关键请求强制校验 `em_hq_cku`、`em_hq_cku2` Cookie，但本次无 Cookie 的四类正确请求均成功过，因而“强制”说法不成立。
- 文章把 `/api/qt/stock/fund/get` 列为财务摘要接口，本次实际返回 HTTP 404。
- “所有动态数据均通过 WebSocket 与 HTTP 长轮询混合通道”“存在毫秒级滑动窗口限流”等说法没有在文章中给出可复现证据，也未被本次普通 HTTPS GET 测试支持。

这些纠错不表示相关能力永远不存在，只表示该文章没有提供足够证据，且部分示例与当前接口行为直接冲突。

## 5. 历史 K 线

### 5.1 请求参数

```text
GET https://push2his.eastmoney.com/api/qt/stock/kline/get
```

| 参数 | 示例 | 含义 |
| --- | --- | --- |
| `secid` | `1.600519`、`90.BK1650` | 个股或板块标识 |
| `fields1` | `f1,f2,f3,f4,f5,f6` | 响应元数据字段集合 |
| `fields2` | `f51,...,f61` | 每条 K 线的字段顺序 |
| `klt` | `5`、`101`、`102`、`103` | 五分钟、日、周、月 |
| `fqt` | `0`、`1`、`2` | 不复权、前复权、后复权 |
| `beg` / `end` | `20260901` / `20260930` | 日期范围；也可使用 `0` / `20500101` |
| `lmt` | `30` | 请求返回数量限制之一 |
| `smplmt` | `460` | ShadowFlow 文档记录的网页采样限制参数；本轮未重新验证上限 |
| `cb` | `docCallback` | 可选 JSONP 回调名 |

测试请求使用：

```text
fields1=f1,f2,f3,f4,f5,f6
fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61
klt=101
fqt=1
beg=20260901
end=20260930
lmt=30
```

个股 `1.600519` 和板块 `90.BK1650` 均返回 21 条有效日 K。这里的 21 只是指定日期范围内的本次结果，不是固定协议长度。

### 5.2 响应与行字段

主要结构：

```json
{
  "rc": 0,
  "data": {
    "code": "600519",
    "market": 1,
    "name": "贵州茅台",
    "decimal": 2,
    "klines": [
      "2026-09-30,1239.53,1258.62,1268.00,1236.05,38331,4797246636.00,2.59,1.86,23.04,0.31"
    ]
  }
}
```

`fields2` 与逗号分隔行一一对应：

| 字段 | 含义 |
| --- | --- |
| `f51` | 日期或分钟时间 |
| `f52` / `f53` | 开盘 / 收盘 |
| `f54` / `f55` | 最高 / 最低 |
| `f56` / `f57` | 成交量 / 成交额 |
| `f58` / `f59` | 振幅 / 涨跌幅 |
| `f60` / `f61` | 涨跌额 / 换手率 |

样本满足以下关系：

- 最低价不高于开盘、收盘，最高价不低于开盘、收盘。
- `收盘 - 昨收 ≈ 涨跌额`。
- `涨跌额 ÷ 昨收 × 100 ≈ 涨跌幅`。
- `(最高 - 最低) ÷ 昨收 × 100 ≈ 振幅`。

`dktotal` 是服务端报告的总 K 线数量，不是本次 `klines` 已返回的数量。完整历史需要明确分页或分段策略，不能因响应包含 `dktotal` 就认为数据已经完整。

### 5.3 JSON 与 JSONP

不带 `cb` 的成功样本返回 JSON。带 `cb` 时预期为 JSONP，应提取第一个左括号和最后一个右括号之间的 JSON；不能用删除固定前后字符的方式去壳。实时 JSONP 请求在本轮第二阶段被服务端断开，所以本文只确认解析方法和来源资料记录，没有把该次请求写成成功。

## 6. 当日分时 `trends2`

候选地址：

```text
https://push2delay.eastmoney.com/api/qt/stock/trends2/get
https://push2his.eastmoney.com/api/qt/stock/trends2/get
https://push2.eastmoney.com/api/qt/stock/trends2/get
```

核心参数：

```text
secid=1.600519
ndays=1
iscr=0
ut=fa5fd1943c7b386f172d6893dbfba10b
fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13
fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62
```

`push2delay` 在收盘后返回 241 条分时记录。第一条时间为 09:30，最后一条为 15:00。241 是本次完整交易日样本，不应作为盘中、停牌、半日市或其他市场的固定断言。

本次数据支持以下行字段解释：

| 字段 | 含义 | 验证方式 |
| --- | --- | --- |
| `f51` | 分钟时间 | 可按 `%Y-%m-%d %H:%M` 解析 |
| `f52` / `f53` | 分钟开盘 / 收盘 | 最后一行分别为 `1257.93` / `1258.62` |
| `f54` / `f55` | 分钟最高 / 最低 | 满足 OHLC 高低关系 |
| `f56` / `f57` | 该分钟成交量 / 成交额 | 非负值 |
| `f58` | 截至该分钟的均价 | 与累计成交量、成交额计算结果接近 |
| `f59` / `f60` | 供应商扩展字段 | 本次未确定业务含义 |
| `f61` / `f62` | 累计成交量 / 累计成交额 | 整日单调不减，末值与快照及日 K 一致 |

ShadowFlow 文档使用当日 241 条一分钟数据聚合 48 根五分钟 K。实现聚合前必须先确定如何处理 09:30 的首条记录、午间休市和缺失分钟；不能简单按自然时间每五分钟切片后假设必然得到 48 根。

三个域名不能因路径相同就盲目轮换。主域失败后，只有网络错误、空响应或明确临时错误适合尝试候选域；参数错误、日期错误、`rc != 0` 或结构错误应先修正请求。

## 7. Cookie、限速和断连

### 7.1 能证明什么

本轮第一次测试按一秒间隔依次请求：

1. `push2` 单证券快照：成功。
2. `push2his` 个股日 K：成功。
3. `push2his` 板块日 K：成功。
4. `push2delay` 当日分时：成功。
5. CSDN 文章中的错误 `stock/get` 参数组合：服务端在返回 HTTP 状态前断开。
6. CSDN 文章中的 `stock/fund/get`：HTTP 404。

随后发起的 `fltt=2` 快照、JSONP 日 K、`push2his` 分时和 `push2` 分时都在约 0.1 秒内被断开。所有成功请求均未携带 Cookie。

这组结果说明：

- Cookie 不是每次成功请求的必要条件。
- 后续断连可能与连接特征、请求序列、短期状态或服务端风控有关。
- 错误请求与随后断连在时间上相邻，但不能据此断言它触发了惩罚。
- 无法从一次序列推导安全 QPS、固定冷却时间或 Cookie 有效期。

ShadowFlow 文档记录的“5 至 8 秒活跃窗口”和“20 至 40 秒恢复区间”属于其 2026-08-17 特定 curl 会话的实验结果。它们可用于设计下一轮实验，不是东方财富公开规则，也不应直接成为生产常量。

### 7.2 工程处理建议

1. 把“无 HTTP 响应”和“HTTP 4xx/5xx”分开记录。`RemoteDisconnected`、`EOF` 或连接重置不能伪装成 JSON 解析失败。
2. 第一次发生无响应时停止当前批次并熔断，不要立即轮换 Cookie、域名或 IP 连续探测。
3. 对成功响应缓存；历史日线不应重复抓取。
4. 批量任务限制并发，并记录端点、`secid`、请求时间、HTTP 阶段、响应长度和匿名会话哈希。
5. 日志不得写入完整 Cookie，也不要把来源文档中的示例 Cookie 当作固定身份复用。
6. 重新验证时隔离变量：分别测试无 Cookie、同一 Cookie 复用、请求头删减、连接复用和真实浏览器。每个结论至少重复多次。
7. 若浏览器成功而脚本失败，应比较 TLS/HTTP 栈、请求头、连接复用和请求顺序，不要只归因于频率。

## 8. Python 标准库示例

下面的示例不自动重试。调用方应在外层实现缓存、熔断和受控退避：

```python
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen


TOKEN = "fa5fd1943c7b386f172d6893dbfba10b"
HEADERS = {
    "Accept": "*/*",
    "Referer": "https://quote.eastmoney.com/sh600519.html",
    "User-Agent": "Mozilla/5.0 Chrome/140 Safari/537.36",
}


def unwrap_json_or_jsonp(body: bytes) -> dict:
    text = body.decode("utf-8").strip()
    if text.startswith("{"):
        return json.loads(text)

    start = text.find("(")
    end = text.rfind(")")
    if start <= 0 or end <= start:
        raise ValueError("Response is neither JSON nor JSONP")
    return json.loads(text[start + 1 : end])


def fetch_json(base_url: str, params: dict[str, str]) -> dict:
    url = f"{base_url}?{urlencode(params)}"
    request = Request(url, headers=HEADERS)
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected HTTP status {response.status}")
        return unwrap_json_or_jsonp(response.read())


def fetch_daily_klines(secid: str, limit: int = 120) -> list[str]:
    payload = fetch_json(
        "https://push2his.eastmoney.com/api/qt/stock/kline/get",
        {
            "secid": secid,
            "ut": TOKEN,
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": "101",
            "fqt": "1",
            "beg": "0",
            "end": "20500101",
            "lmt": str(limit),
        },
    )
    if payload.get("rc") != 0 or not isinstance(payload.get("data"), dict):
        raise ValueError("Eastmoney returned an unsuccessful K-line response")

    klines = payload["data"].get("klines")
    if not isinstance(klines, list) or not klines:
        raise ValueError("Eastmoney returned no K-line rows")
    return klines
```

对网络异常应保留原异常类型。不要把所有异常统一转换为“无数据”，否则服务端断连、参数错误和真正没有行情会混在一起。

## 9. 可重复验证

运行：

```bash
docker compose --env-file config/compose.dev.env -f docker-compose.dev.yaml \
  exec -T cogniz-api python - < docs/verify_eastmoney_push2_api.py
```

验证脚本包含：

- JSON 与 JSONP 去壳测试。
- 单证券快照字段和涨跌停关系。
- 个股与板块日 K 的结构、OHLC 和数量关系。
- 分时记录格式及累计成交量、成交额单调性。
- CSDN 所列 `stock/fund/get` 的当前 HTTP 状态。
- 至少一个实时请求必须产生 HTTP 响应；被服务端提前断开的单项会标为跳过，HTTP 404 仍作为可观测响应参与诊断。

实时测试只读取公开网页接口，不发送 Cookie，不写入第三方数据。由于服务端状态可能变化，某次跳过或失败本身也是诊断结果，不能通过无限重试把它“刷成成功”。

## 10. 接入检查清单

- [ ] 使用明确的 `secid`，不要把列表接口的 `fs` 当作单证券标识。
- [ ] 只请求业务需要的 `fields`，不要复制异常膨胀的字段列表。
- [ ] 检查 HTTP 状态、`rc`、`data` 类型和目标代码。
- [ ] 根据 `fltt` 和证券精度处理缩放，不能统一除以 100。
- [ ] 按 `fields2` 顺序解析 K 线或分时行，并检查列数。
- [ ] 区分本次返回数量与 `dktotal` 报告的总量。
- [ ] JSONP 按括号位置去壳，不使用固定字符长度。
- [ ] 区分断连、HTTP 错误、业务错误、空数据和结构变化。
- [ ] 对历史数据缓存，对批量任务限流并设置熔断。
- [ ] 不记录完整 Cookie，不把 Cookie 当作稳定认证凭据。
- [ ] 定期运行 `docs/verify_eastmoney_push2_api.py` 并保存日期化结果。
