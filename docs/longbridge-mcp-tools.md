 **Longbridge 给 AI Agent 暴露的 MCP Tool Surface**。

我查到了更关键的东西：**Longbridge 官方 MCP Server 已经开源**，仓库就是 `longbridge/longbridge-mcp`。官方 MCP 文档目前写的是 **160+ tools**，而当前 GitHub 源码里我直接按 `pub async fn` 扫描，已经能看到约 **190 个 tool handler**；其中有一些是新加入、地区限定、账户限定或尚未在文档统计数字里同步的工具，所以 README、server.json 和官网看到的总数会略有差异。:chatgpt-content-reference{index="0"}

[Longbridge MCP 官方文档](https://open.longbridge.com/zh-CN/docs/mcp?utm_source=chatgpt.com)  
[Longbridge MCP 官方 GitHub](https://github.com/longbridge/longbridge-mcp?utm_source=chatgpt.com)

## 1. 当前源码里的完整 Tool 分组

这是我直接从官方 MCP 源码 `src/tools/*.rs` 中提取出来的。

| 模块 | 数量 | Tools |
|---|---:|---|
| Quote 行情 | 32 | `static_info`, `quote`, `option_quote`, `warrant_quote`, `depth`, `brokers`, `participants`, `trades`, `intraday`, `candlesticks`, `history_candlesticks_by_offset`, `history_candlesticks_by_date`, `trading_days`, `option_chain_expiry_date_list`, `option_chain_info_by_date`, `capital_flow`, `capital_distribution`, `trading_session`, `market_temperature`, `history_market_temperature`, `watchlist`, `filings`, `warrant_issuers`, `warrant_list`, `calc_indexes`, `create_watchlist_group`, `delete_watchlist_group`, `update_watchlist_group`, `security_list`, `short_positions`, `option_volume`, `option_volume_daily` |
| Trade 交易 | 16 | `account_balance`, `stock_positions`, `fund_positions`, `margin_ratio`, `today_orders`, `order_detail`, `cancel_order`, `today_executions`, `history_orders`, `history_executions`, `cash_flow`, `submit_order`, `submit_multileg_order`, `replace_order`, `estimate_max_purchase_quantity`, `short_margin` |
| Fundamental 基本面 | 33 | `financial_report`, `institution_rating`, `institution_rating_detail`, `dividend`, `dividend_detail`, `forecast_eps`, `consensus`, `valuation`, `valuation_history`, `industry_valuation`, `industry_valuation_dist`, `company`, `executive`, `shareholder`, `fund_holder`, `corp_action`, `invest_relation`, `operating`, `financial_statement`, `financial_report_key_metrics`, `etf_docs`, `financial_report_latest`, `valuation_rank`, `institution_rating_history`, `institution_rating_industry_rank`, `business_segments`, `business_segments_history`, `institutional_views`, `industry_peers`, `financial_report_snapshot`, `shareholder_top`, `shareholder_detail`, `valuation_comparison` |
| Market 市场 | 14 | `market_status`, `broker_holding`, `broker_holding_detail`, `broker_holding_daily`, `ah_premium`, `ah_premium_intraday`, `trade_stats`, `anomaly`, `constituent`, `industry_rank`, `short_trades`, `top_movers`, `rank_categories`, `rank_list` |
| Content / 新闻社区 | 7 | `news`, `news_detail`, `topic`, `topic_detail`, `topic_replies`, `topic_create`, `topic_create_reply` |
| Search | 2 | `news_search`, `topic_search` |
| Screener 选股 | 5 | `screener_recommend_strategies`, `screener_user_strategies`, `screener_strategy`, `screener_search`, `screener_indicators` |
| Portfolio | 4 | `exchange_rate`, `profit_analysis`, `profit_analysis_detail`, `profit_analysis_realized` |
| DCA 定投 | 9 | `dca_list`, `dca_create`, `dca_update`, `dca_pause`, `dca_resume`, `dca_stop`, `dca_history`, `dca_stats`, `dca_check` |
| IPO | 7 | `ipo_subscriptions`, `ipo_calendar`, `ipo_listed`, `ipo_detail`, `ipo_orders`, `ipo_order_detail`, `ipo_profit_loss` |
| Alert | 5 | `alert_list`, `alert_add`, `alert_delete`, `alert_enable`, `alert_disable` |
| Sharelist | 8 | `sharelist_list`, `sharelist_detail`, `sharelist_create`, `sharelist_delete`, `sharelist_add`, `sharelist_remove`, `sharelist_sort`, `sharelist_popular` |
| Statement | 2 | `statement_list`, `statement_export` |
| Macro | 2 | `macrodata_indicators`, `macrodata` |
| Calendar | 1 | `finance_calendar` |
| Fund | 28 | `fund_hot`, `fund_list`, `fund_filters`, `fund_detail`, `fund_analysis`, `fund_analysis_detail`, `fund_trend`, `fund_annual_returns`, `fund_quarterly_returns`, `fund_performance`, `fund_performance_comparison`, `fund_nav`, `fund_nav_history`, `fund_nav_range`, `fund_holdings`, `fund_stock_holdings`, `fund_position_overview`, `fund_position`, `fund_position_performance`, `fund_position_profits`, `fund_position_nav`, `fund_position_dividends`, `fund_orders`, `fund_order`, `fund_transactions`, `fund_validate_order`, `fund_submit_order`, `fund_cancel_order` |
| Grid 网格交易 | 10 | `grid_symbol_info`, `grid_list`, `grid_list_by_ids`, `grid_detail`, `grid_trigger_history`, `grid_submit`, `grid_replace`, `grid_cancel`, `grid_suspend`, `grid_restart` |
| Signal | 3 | `signals`, `signal_detail`, `security_facts` |
| ATM / 出入金 | 3 | `bank_cards`, `withdrawals`, `deposits` |
| Quant | 1 | `run_script` |

源码结构本身也明确按 Quote、Trade、Fundamental、Market、IPO、Search、Portfolio、DCA 等模块拆分。官方 README 的某个较早统计版本列的是 148 个工具、19 个类别，因此**不要把 148 当成固定数字**。:chatgpt-content-reference{index="3"}

---

# 2. 对 cogniz 最重要的其实只有大约 30～40 个

如果你的目标是：

> 用户问：「分析一下苹果最近行情和走势，结合财报、估值、新闻判断当前情况。」

那么根本没必要一开始照抄 Longbridge 的 190 个 Tool。

我会给 cogniz 第一阶段做下面这些：

| cogniz Tool | Longbridge 对应 Tool | 输入 | 主要输出 | 用途 |
|---|---|---|---|---|
| `get_quote` | `quote` | `symbols[]` | last、prev_close、OHLC、volume、turnover、change | 实时行情 |
| `get_static_info` | `static_info` | `symbols[]` | 名称、市场、币种、lot size 等 | 标的信息 |
| `get_candlesticks` | `candlesticks` | symbol, period, count | OHLCV[] | 技术分析 |
| `get_history_candlesticks` | `history_candlesticks_by_date` | symbol,start,end,period | OHLCV[] | 历史走势 |
| `get_intraday` | `intraday` | symbol | 分时价格/成交 | 日内走势 |
| `get_trades` | `trades` | symbol,count | price,volume,time,direction | 逐笔成交 |
| `get_depth` | `depth` | symbol | bids[],asks[] | 买卖盘 |
| `get_trade_stats` | `trade_stats` | symbol | buy/sell/neutral volume | 主动买卖结构 |
| `get_capital_flow` | `capital_flow` | symbol | inflow,outflow,net_flow | 资金流 |
| `get_capital_distribution` | `capital_distribution` | symbol | 大/中/小单分布 | 资金结构 |
| `get_short_positions` | `short_positions` | symbol | short data | 空头数据 |
| `get_option_volume` | `option_volume` | symbol | option statistics | 期权情绪 |
| `get_calc_indexes` | `calc_indexes` | symbols,indexes | PE/PB/市值/换手等 | 快速指标 |
| `get_company` | `company` | symbol | 公司简介 | 基本信息 |
| `get_financial_report` | `financial_report` | symbol,... | 财务指标 | 财报 |
| `get_financial_statement` | `financial_statement` | symbol,... | 三大表 | 深度财务分析 |
| `get_financial_snapshot` | `financial_report_snapshot` | symbol | 核心指标摘要 | 给 LLM 快速阅读 |
| `get_key_metrics` | `financial_report_key_metrics` | symbol | 财务比率 | 盈利/偿债分析 |
| `get_valuation` | `valuation` | symbol | PE/PB/PS 等 | 当前估值 |
| `get_valuation_history` | `valuation_history` | symbol | historical PE/PB | 历史估值 |
| `get_valuation_rank` | `valuation_rank` | symbol | percentile/rank | 贵不贵 |
| `get_industry_peers` | `industry_peers` | symbol | peers[] | 同行业比较 |
| `get_valuation_comparison` | `valuation_comparison` | symbol | peer valuation | 相对估值 |
| `get_consensus` | `consensus` | symbol | consensus estimates | 市场预期 |
| `get_forecast_eps` | `forecast_eps` | symbol | EPS estimates | 盈利预测 |
| `get_institution_rating` | `institution_rating` | symbol | analyst ratings | 分析师观点 |
| `get_business_segments` | `business_segments` | symbol | segment revenue | 业务构成 |
| `get_dividend` | `dividend` | symbol | dividend history | 分红 |
| `get_corp_action` | `corp_action` | symbol | splits/buyback etc. | 公司行为 |
| `get_news` | `news` | symbol | news[] | 最新新闻 |
| `search_news` | `news_search` | keyword | news[] | 主题新闻搜索 |
| `get_filings` | `filings` | symbol | filings[] | SEC/公告 |
| `get_market_status` | `market_status` | market | session/status | 市场状态 |
| `get_market_temperature` | `market_temperature` | market | sentiment metrics | 市场情绪 |
| `get_top_movers` | `top_movers` | market | symbols[] | 大盘背景 |
| `get_industry_rank` | `industry_rank` | market | industries[] | 板块强弱 |
| `get_macrodata` | `macrodata` | indicator | timeseries | 宏观环境 |
| `get_finance_calendar` | `finance_calendar` | dates/types | events[] | 财报/宏观事件 |

这一套已经足够构成你之前设想的 cogniz 分析 Agent。

---

# 3.几个 Tool 的真实参数长什么样

例如 Longbridge 官方 MCP 的：

### `quote`

输入：

```json
{
  "symbols": [
    "AAPL.US",
    "TSLA.US"
  ]
}
```

主要返回：

```json
{
  "symbol": "AAPL.US",
  "last_done": "...",
  "prev_close": "...",
  "open": "...",
  "high": "...",
  "low": "...",
  "volume": "...",
  "turnover": "...",
  "change_rate": "...",
  "change_value": "...",
  "trade_status": "...",
  "timestamp": "..."
}
```

官方就是这么描述的。:chatgpt-content-reference{index="4"}

---

### `candlesticks`

实际 Schema 类似：

```json
{
  "symbol": "AAPL.US",
  "period": "day",
  "count": 100,
  "forward_adjust": false,
  "trade_sessions": "all"
}
```

其中：

```text
period:
1m
5m
15m
30m
60m
day
week
month
year
```

最多可以请求 1000 根 K 线。:chatgpt-content-reference{index="5"}

这个接口对 cogniz 极其重要。

---

### `calc_indexes`

这个工具非常值得你直接借鉴。

输入可以：

```json
{
  "symbols": [
    "AAPL.US",
    "NVDA.US"
  ],
  "indexes": [
    "LastDone",
    "ChangeRate",
    "TurnoverRate",
    "TotalMarketValue",
    "PeTtmRatio",
    "PbRatio"
  ]
}
```

Longbridge 支持一次计算很多指标，包括：

```text
LastDone
ChangeValue
ChangeRate
Volume
Turnover
YtdChangeRate
TurnoverRate
TotalMarketValue
CapitalFlow
Amplitude
VolumeRatio

PeTtmRatio
PbRatio
DividendRatioTtm

FiveDayChangeRate
TenDayChangeRate
HalfYearChangeRate
FiveMinutesChangeRate

OpenInterest
ImpliedVolatility
Delta
Gamma
Theta
Vega
Rho
...
``` :chatgpt-content-reference{index="6"}


这其实就是你之前问我的：

```text
change_1d_pct
PE
PB
market_cap
turnover_rate
```

这一类东西最好的实现方式。

---

# 4. `trade_stats` 就是你之前问的买/卖/中性成交

Longbridge MCP 的定义：

```text
trade_stats(symbol)
```

返回：

```json
{
  "items": [
    {
      "price_range": "...",
      "buy_volume": "...",
      "sell_volume": "...",
      "neutral_volume": "..."
    }
  ]
}
```

也就是你之前看到的：

```text
buy_amount
sell_amount
neutral_amount
```

这类信息。

官方说明它是 price-volume profile / buy-sell-neutral distribution。:chatgpt-content-reference{index="7"}

所以在 cogniz 里我甚至会把名字改得更明确：

```text
get_trade_distribution
```

而不是照抄：

```text
trade_stats
```

这样 LLM 更容易选择正确工具。

---

# 5. Longbridge 的 Tool 架构其实很值得 cogniz 抄

官方实现大概是：

```text
LLM
 │
 │ tool call
 ▼
MCP Server
 │
 ├── quote.rs
 ├── trade.rs
 ├── fundamental.rs
 ├── market.rs
 ├── content.rs
 ├── search.rs
 ├── screener.rs
 ├── portfolio.rs
 └── ...
       │
       ▼
Longbridge SDK / HTTP API / WebSocket
```

Longbridge 自己的 CLI 更进一步，把底层分成：

```text
quote.*
trade.*
api.get
api.post
quote.subscribe
quote.unsubscribe
```

其中 Fundamental、Screener、IPO、News 等大量功能走 REST，而 Quote / Trade 核心接口通过 SDK 调用。:chatgpt-content-reference{index="8"}

这和你的 cogniz 非常接近。

---

# 6. 我建议 cogniz 不要做成 190 个 Tool 平铺

比如不要直接：

```text
LLM
 ├── quote
 ├── depth
 ├── trades
 ├── candlesticks
 ├── financial_report
 ├── financial_report_snapshot
 ├── valuation
 ├── valuation_rank
 ├── valuation_comparison
 ├── ...
 └── 190 tools
```

这会让模型的 Tool Selection 变得很混乱。

我更建议：

```text
                    Cogniz Agent
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Market Tool   Fundamental Tool   News Tool
          │              │              │
          ▼              ▼              ▼
      provider        provider        provider
          │              │              │
    Longbridge       Longbridge       Longbridge
    Polygon          SEC              Search API
    Futu             FMP              News API
```

然后 Tool 层控制在：

```text
market.quote
market.candles
market.intraday
market.depth
market.trades
market.capital_flow
market.options

fundamental.company
fundamental.financials
fundamental.valuation
fundamental.consensus
fundamental.peers

news.latest
news.search
news.filings

market.overview
market.sector
macro.data
```

大约 **20～30 个高层 Tool**。

底层再映射：

```text
market.quote
        ↓
Provider Router
        ↓
Longbridge.quote
Polygon.snapshot
Futu.get_market_snapshot
```

这样以后你换数据源完全不用修改 Agent。

---

# 7. 还有一个特别值得你参考的设计：输出 Schema

Longbridge MCP 不只是返回任意 JSON。

官方现在明确提供：

```text
tools/list
        ↓
typed outputSchema
```

并且完整 schema 可以通过：

```text
lb://tools/{tool}/output-schema
```

获取。:chatgpt-content-reference{index="9"}

这对 cogniz 非常重要。

你可以做：

```python
class QuoteResult(BaseModel):
    symbol: str
    last: Decimal
    prev_close: Decimal
    change: Decimal
    change_pct: Decimal
    open: Decimal
    high: Decimal
    low: Decimal
    volume: int
    turnover: Decimal
    timestamp: datetime
```

也就是说：

```text
Provider 原始 JSON
        ↓
Adapter
        ↓
Cogniz 标准数据模型
        ↓
Agent
```

而不是：

```text
Longbridge JSON ───────────────┐
Polygon JSON ──────────────────┼→ LLM
Futu JSON ─────────────────────┘
```

后者以后一定会越来越乱。

---

# 8. 这次我发现了一个对你项目很重要的新变化

Longbridge 的 MCP 已经远远不只是：

```text
quote
candlesticks
financial
news
trade
```

现在连：

```text
fund
grid
signal
quant
screener
macro
analyst consensus
industry peers
valuation comparison
broker holdings
short trades
option volume
```

都已经开始 Tool 化。

换句话说，**Longbridge 本身已经是一个非常好的“金融 AI Agent Tool Architecture”参考实现。**

而且官方直接说明这个 MCP 面向 ChatGPT、Claude、Cursor 等 AI 客户端，连接之后 Tool 会自动 discovery；具体可用 Tool 会根据地区、账户等级和 OAuth scope 不同而变化。:chatgpt-content-reference{index="10"}

### 对 cogniz 最值得研究的几个源码文件

你可以直接重点看：

```text
src/tools/mod.rs
src/tools/quote.rs
src/tools/fundamental.rs
src/tools/market.rs
src/tools/content.rs
src/tools/search.rs
src/tools/trade.rs
```

[查看 Longbridge MCP 源码](https://github.com/longbridge/longbridge-mcp/tree/main/src/tools?utm_source=chatgpt.com)

其中 **`mod.rs` + `quote.rs` + `fundamental.rs`** 对你目前的 cogniz 最有参考价值。

下一步你其实可以直接以 Longbridge 这套为蓝本，把 cogniz 定成 **Market / Fundamental / News / Research / Portfolio 五大 Tool Domain**，而不是继续纠结 LangGraph 里应该堆多少节点。这样 PydanticAI 或 LangGraph 都只是上层 Agent Runtime，下面的 Tool 层保持独立。