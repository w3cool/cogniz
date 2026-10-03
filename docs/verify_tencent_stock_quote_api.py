#!/usr/bin/env python3
"""Live verification for docs/tencent-stock-quote-api.md.

The checks use only Python's standard library and make read-only requests to
the public endpoints described by the document. Run them from the development
container so no local Python dependencies are required.
"""

from __future__ import annotations

import json
import re
import unittest
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlencode
from urllib.request import Request, urlopen

QUOTE_ENDPOINT = "{scheme}://qt.gtimg.cn/q={query}"
MINUTE_ENDPOINT = "https://web.ifzq.gtimg.cn/appstock/app/minute/query"
STOCK_SYMBOLS = ("sh600000", "sz000858", "sh601318", "sz300750")
MINUTE_SYMBOLS = ("sz159326", "sh600000", "sz000858")
INVALID_SYMBOL = "sh999999"
USER_AGENT = "cogniz-doc-verifier/1.0"


def get(url: str) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=15) as response:
        if response.status != 200:
            raise AssertionError(f"{url} returned HTTP {response.status}")
        return response.read(), response.headers.get("Content-Type", "")


def parse_quote_response(body: bytes, requested_query: str) -> tuple[str, list[str]]:
    text = body.decode("gbk").strip()
    match = re.fullmatch(r'v_([^=]+)="(.*)";', text, re.DOTALL)
    if not match:
        raise AssertionError(f"Unexpected quote envelope for {requested_query}: {text!r}")
    response_key, payload = match.groups()
    return response_key, payload.split("~")


def fetch_quote(query: str, scheme: str = "https") -> tuple[list[str], str]:
    body, content_type = get(QUOTE_ENDPOINT.format(scheme=scheme, query=query))
    response_key, fields = parse_quote_response(body, query)
    if response_key != query:
        raise AssertionError(f"Requested {query!r}, received {response_key!r}")
    return fields, content_type


def fetch_minute(symbol: str) -> tuple[dict, str]:
    url = f"{MINUTE_ENDPOINT}?{urlencode({'code': symbol})}"
    body, content_type = get(url)
    return json.loads(body), content_type


def decimal(fields: list[str], index: int) -> Decimal:
    try:
        return Decimal(fields[index])
    except (IndexError, ValueError) as error:
        raise AssertionError(
            f"Field {index} is not decimal: {fields[index : index + 1]!r}"
        ) from error


class TencentQuoteDocumentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.quotes: dict[str, list[str]] = {}
        cls.quote_content_types: dict[str, str] = {}
        for symbol in STOCK_SYMBOLS:
            fields, content_type = fetch_quote(symbol)
            cls.quotes[symbol] = fields
            cls.quote_content_types[symbol] = content_type

    def test_http_and_https_quote_endpoints(self) -> None:
        https_fields = self.quotes["sh600000"]
        http_fields, http_content_type = fetch_quote("sh600000", scheme="http")
        self.assertEqual(http_fields[2], https_fields[2])
        self.assertIn("gbk", http_content_type.lower())
        self.assertIn("gbk", self.quote_content_types["sh600000"].lower())

    def test_full_quote_core_field_mapping_and_units(self) -> None:
        for symbol, fields in self.quotes.items():
            with self.subTest(symbol=symbol):
                self.assertEqual(len(fields), 88)
                self.assertEqual(fields[2], symbol[2:])
                self.assertEqual(fields[40], "")

                latest = decimal(fields, 3)
                previous_close = decimal(fields, 4)
                open_price = decimal(fields, 5)
                volume = decimal(fields, 6)
                change = decimal(fields, 31)
                change_percent = decimal(fields, 32)
                high = decimal(fields, 33)
                low = decimal(fields, 34)
                amount_ten_thousand_yuan = decimal(fields, 37)
                amplitude = decimal(fields, 43)

                self.assertGreater(previous_close, 0)
                self.assertGreater(open_price, 0)
                self.assertGreaterEqual(volume, 0)
                self.assertLessEqual(low, latest)
                self.assertLessEqual(latest, high)
                self.assertLessEqual(abs((latest - previous_close) - change), Decimal("0.011"))
                expected_change_percent = change / previous_close * 100
                self.assertLessEqual(abs(expected_change_percent - change_percent), Decimal("0.02"))
                expected_amplitude = (high - low) / previous_close * 100
                self.assertLessEqual(abs(expected_amplitude - amplitude), Decimal("0.02"))

                combined = fields[35].split("/")
                self.assertEqual(len(combined), 3)
                self.assertEqual(Decimal(combined[0]), latest)
                self.assertEqual(Decimal(combined[1]), volume)
                self.assertLessEqual(
                    abs(Decimal(combined[2]) / 10_000 - amount_ten_thousand_yuan),
                    Decimal("1"),
                )
                self.assertEqual(fields[6], fields[36])
                self.assertEqual(fields[33], fields[41])
                self.assertEqual(fields[34], fields[42])
                self.assertGreaterEqual(decimal(fields, 45), decimal(fields, 44))
                decimal(fields, 46)
                decimal(fields, 49)
                datetime.strptime(fields[30], "%Y%m%d%H%M%S")

    def test_price_limit_fields_for_board_samples(self) -> None:
        expected_ratios = {
            "sh600000": (Decimal("1.10"), Decimal("0.90")),
            "sz000858": (Decimal("1.10"), Decimal("0.90")),
            "sh601318": (Decimal("1.10"), Decimal("0.90")),
            "sz300750": (Decimal("1.20"), Decimal("0.80")),
        }
        for symbol, (upper_ratio, lower_ratio) in expected_ratios.items():
            with self.subTest(symbol=symbol):
                fields = self.quotes[symbol]
                previous_close = decimal(fields, 4)
                self.assertLessEqual(
                    abs(decimal(fields, 47) / previous_close - upper_ratio), Decimal("0.002")
                )
                self.assertLessEqual(
                    abs(decimal(fields, 48) / previous_close - lower_ratio), Decimal("0.002")
                )

    def test_order_book_positions(self) -> None:
        for symbol, fields in self.quotes.items():
            with self.subTest(symbol=symbol):
                buy_prices = [decimal(fields, index) for index in range(9, 19, 2)]
                buy_volumes = [decimal(fields, index) for index in range(10, 19, 2)]
                sell_prices = [decimal(fields, index) for index in range(19, 29, 2)]
                sell_volumes = [decimal(fields, index) for index in range(20, 29, 2)]
                self.assertEqual(buy_prices, sorted(buy_prices, reverse=True))
                self.assertEqual(sell_prices, sorted(sell_prices))
                self.assertTrue(all(value >= 0 for value in buy_volumes + sell_volumes))
                self.assertLessEqual(buy_prices[0], sell_prices[0])

    def test_simplified_quote_matches_full_quote(self) -> None:
        for symbol, full in self.quotes.items():
            with self.subTest(symbol=symbol):
                simple, _ = fetch_quote(f"s_{symbol}")
                self.assertEqual(len(simple), 12)
                for simple_index, full_index in (
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 31),
                    (5, 32),
                    (6, 6),
                    (7, 37),
                    (9, 45),
                ):
                    self.assertEqual(simple[simple_index], full[full_index])
                self.assertEqual(simple[8], "")
                self.assertEqual(simple[11], "")
                self.assertTrue(simple[10].startswith("GP-A"))

    def test_order_flow_ratio_shape_only(self) -> None:
        for symbol in ("sh600000", "sz000858"):
            with self.subTest(symbol=symbol):
                fields, _ = fetch_quote(f"s_pk{symbol}")
                self.assertEqual(len(fields), 4)
                ratios = [Decimal(value) for value in fields]
                self.assertTrue(all(Decimal("0") <= value <= Decimal("1") for value in ratios))
                self.assertLessEqual(abs(sum(ratios) - Decimal("1")), Decimal("0.002"))

    def test_retired_fund_flow_and_invalid_quote(self) -> None:
        for query in ("ff_sh600000", "ff_sz000858", INVALID_SYMBOL):
            with self.subTest(query=query):
                body, _ = get(QUOTE_ENDPOINT.format(scheme="https", query=query))
                response_key, fields = parse_quote_response(body, query)
                self.assertEqual(response_key, "pv_none_match")
                self.assertEqual(fields, ["1"])

    def test_minute_structure_cumulative_fields_and_embedded_quote(self) -> None:
        for symbol in MINUTE_SYMBOLS:
            with self.subTest(symbol=symbol):
                payload, content_type = fetch_minute(symbol)
                self.assertIn("text/html", content_type.lower())
                self.assertIn("utf-8", content_type.lower())
                self.assertEqual(payload["code"], 0)
                self.assertEqual(payload["msg"], "")

                symbol_data = payload["data"][symbol]
                date_text = symbol_data["data"]["date"]
                rows = symbol_data["data"]["data"]
                embedded_quote = symbol_data["qt"][symbol]
                self.assertRegex(date_text, r"^\d{8}$")
                self.assertGreater(len(rows), 0)
                self.assertEqual(len(embedded_quote), 88)
                self.assertEqual(embedded_quote[2], symbol[2:])
                self.assertEqual(embedded_quote[33], embedded_quote[41])
                self.assertEqual(embedded_quote[34], embedded_quote[42])

                previous_volume = Decimal("-1")
                previous_amount = Decimal("-1")
                prices: list[Decimal] = []
                for row in rows:
                    parts = row.split()
                    self.assertEqual(len(parts), 4)
                    datetime.strptime(date_text + parts[0], "%Y%m%d%H%M")
                    price = Decimal(parts[1])
                    volume = Decimal(parts[2])
                    amount = Decimal(parts[3])
                    self.assertGreater(price, 0)
                    self.assertGreaterEqual(volume, previous_volume)
                    self.assertGreaterEqual(amount, previous_amount)
                    prices.append(price)
                    previous_volume = volume
                    previous_amount = amount

                self.assertGreater(previous_volume, 0)
                self.assertGreater(previous_amount, previous_volume)
                final_vwap = previous_amount / (previous_volume * 100)
                self.assertGreaterEqual(final_vwap, min(prices))
                self.assertLessEqual(final_vwap, max(prices))
                print(
                    f"{symbol}: {len(rows)} minute rows, date={date_text}, "
                    f"final_vwap={final_vwap:.4f}"
                )

    def test_invalid_minute_symbol_requires_structural_validation(self) -> None:
        payload, _ = fetch_minute(INVALID_SYMBOL)
        self.assertEqual(payload["code"], 0)
        symbol_data = payload["data"][INVALID_SYMBOL]
        self.assertEqual(symbol_data["data"]["date"], "")
        self.assertEqual(symbol_data["qt"][INVALID_SYMBOL], [])
        self.assertEqual(symbol_data["data"]["data"], ["  0"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
