#!/usr/bin/env python3
"""Live and offline checks for docs/eastmoney-push2-api.md.

The live endpoints may deliberately close a connection before returning HTTP.
Such cases are reported as skipped individual checks, while the suite still
requires at least one successful live response.
"""

from __future__ import annotations

import http.client
import json
import time
import unittest
from datetime import date, datetime
from decimal import Decimal
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TOKEN = "fa5fd1943c7b386f172d6893dbfba10b"
STOCK_SECID = "1.600519"
BOARD_SECID = "90.BK1650"
FIELDS1 = "f1,f2,f3,f4,f5,f6"
KLINE_FIELDS2 = "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
TREND_FIELDS1 = "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13"
TREND_FIELDS2 = "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62"
HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://quote.eastmoney.com/sh600519.html",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    ),
}


class EndpointUnavailable(Exception):
    """The endpoint closed or failed before a usable HTTP response arrived."""


def unwrap_json_or_jsonp(body: bytes) -> dict:
    text = body.decode("utf-8").strip()
    if text.startswith("{"):
        return json.loads(text)

    start = text.find("(")
    end = text.rfind(")")
    if start <= 0 or end <= start:
        raise ValueError("Response is neither JSON nor JSONP")
    return json.loads(text[start + 1 : end])


def request_bytes(url: str) -> tuple[bytes, str]:
    request = Request(url, headers=HEADERS)
    try:
        with urlopen(request, timeout=15) as response:
            if response.status != 200:
                raise AssertionError(f"Unexpected HTTP status {response.status}")
            return response.read(), response.headers.get("Content-Type", "")
    except HTTPError:
        raise
    except (http.client.RemoteDisconnected, URLError, TimeoutError, ConnectionResetError) as error:
        raise EndpointUnavailable(f"{type(error).__name__}: {error}") from error


def request_json(base_url: str, params: dict[str, str]) -> tuple[dict, str]:
    body, content_type = request_bytes(f"{base_url}?{urlencode(params)}")
    return unwrap_json_or_jsonp(body), content_type


def parse_kline(row: str) -> tuple[date, list[Decimal]]:
    fields = row.split(",")
    if len(fields) != 11:
        raise ValueError(f"Expected 11 K-line fields, got {len(fields)}")
    day = datetime.strptime(fields[0], "%Y-%m-%d").date()
    return day, [Decimal(value) for value in fields[1:]]


class EastmoneyPush2DocumentTest(unittest.TestCase):
    live_responses = 0
    last_request_at = 0.0

    def live_json(self, base_url: str, params: dict[str, str]) -> tuple[dict, str]:
        wait_seconds = 1.0 - (time.monotonic() - type(self).last_request_at)
        if wait_seconds > 0:
            time.sleep(wait_seconds)
        try:
            payload, content_type = request_json(base_url, params)
        except EndpointUnavailable as error:
            self.skipTest(str(error))
        finally:
            type(self).last_request_at = time.monotonic()
        type(self).live_responses += 1
        return payload, content_type

    def test_00_json_and_jsonp_unwrap(self) -> None:
        expected = {"rc": 0, "data": {"code": "600519"}}
        self.assertEqual(unwrap_json_or_jsonp(json.dumps(expected).encode()), expected)
        wrapped = b'docCallback({"rc":0,"data":{"code":"600519"}});'
        self.assertEqual(unwrap_json_or_jsonp(wrapped), expected)

    def test_01_stock_quote(self) -> None:
        payload, content_type = self.live_json(
            "https://push2.eastmoney.com/api/qt/stock/get",
            {
                "secid": STOCK_SECID,
                "ut": TOKEN,
                "invt": "2",
                "fltt": "1",
                "fields": ("f43,f44,f45,f46,f47,f48,f50,f51,f52,f57,f58,f60,f116,f117,f162,f167"),
            },
        )
        self.assertIn("application/json", content_type.lower())
        self.assertEqual(payload["rc"], 0)
        data = payload["data"]
        self.assertEqual(data["f57"], "600519")
        self.assertEqual(data["f58"], "贵州茅台")
        self.assertLessEqual(data["f45"], data["f43"])
        self.assertLessEqual(data["f43"], data["f44"])
        self.assertGreaterEqual(data["f116"], data["f117"])
        self.assertLessEqual(abs(data["f51"] / data["f60"] - 1.10), 0.002)
        self.assertLessEqual(abs(data["f52"] / data["f60"] - 0.90), 0.002)

    def assert_kline_payload(self, payload: dict, expected_code: str) -> None:
        self.assertEqual(payload["rc"], 0)
        data = payload["data"]
        self.assertEqual(data["code"], expected_code)
        self.assertGreater(len(data["klines"]), 0)
        self.assertGreaterEqual(data["dktotal"], len(data["klines"]))
        for row in data["klines"]:
            _, values = parse_kline(row)
            open_price, close, high, low = values[:4]
            volume, amount, amplitude, change_percent, change, turnover = values[4:]
            self.assertLessEqual(low, min(open_price, close))
            self.assertGreaterEqual(high, max(open_price, close))
            self.assertGreaterEqual(volume, 0)
            self.assertGreaterEqual(amount, 0)
            Decimal(amplitude)
            Decimal(change_percent)
            Decimal(change)
            Decimal(turnover)

    def kline_params(self, secid: str) -> dict[str, str]:
        return {
            "secid": secid,
            "ut": TOKEN,
            "fields1": FIELDS1,
            "fields2": KLINE_FIELDS2,
            "klt": "101",
            "fqt": "1",
            "beg": "0",
            "end": "20500101",
            "lmt": "5",
        }

    def test_02_stock_kline(self) -> None:
        payload, _ = self.live_json(
            "https://push2his.eastmoney.com/api/qt/stock/kline/get",
            self.kline_params(STOCK_SECID),
        )
        self.assert_kline_payload(payload, "600519")

    def test_03_board_kline(self) -> None:
        payload, _ = self.live_json(
            "https://push2his.eastmoney.com/api/qt/stock/kline/get",
            self.kline_params(BOARD_SECID),
        )
        self.assert_kline_payload(payload, "BK1650")

    def test_04_trends(self) -> None:
        payload, _ = self.live_json(
            "https://push2delay.eastmoney.com/api/qt/stock/trends2/get",
            {
                "secid": STOCK_SECID,
                "ndays": "1",
                "iscr": "0",
                "ut": TOKEN,
                "fields1": TREND_FIELDS1,
                "fields2": TREND_FIELDS2,
            },
        )
        self.assertEqual(payload["rc"], 0)
        data = payload["data"]
        self.assertEqual(data["code"], "600519")
        self.assertGreater(len(data["trends"]), 0)
        previous_volume = Decimal("-1")
        previous_amount = Decimal("-1")
        for row in data["trends"]:
            fields = row.split(",")
            self.assertEqual(len(fields), 12)
            datetime.strptime(fields[0], "%Y-%m-%d %H:%M")
            cumulative_volume = Decimal(fields[10])
            cumulative_amount = Decimal(fields[11])
            self.assertGreaterEqual(cumulative_volume, previous_volume)
            self.assertGreaterEqual(cumulative_amount, previous_amount)
            previous_volume = cumulative_volume
            previous_amount = cumulative_amount

    def test_05_csdn_fund_endpoint_claim(self) -> None:
        url = "https://push2.eastmoney.com/api/qt/stock/fund/get?" + urlencode(
            {"secid": STOCK_SECID, "ut": TOKEN}
        )
        try:
            request_bytes(url)
        except HTTPError as error:
            try:
                self.assertEqual(error.code, 404)
                type(self).live_responses += 1
            finally:
                error.close()
        except EndpointUnavailable as error:
            self.skipTest(str(error))
        else:
            self.fail("CSDN fund endpoint unexpectedly returned HTTP 200")

    def test_99_at_least_one_live_http_response(self) -> None:
        self.assertGreater(
            type(self).live_responses,
            0,
            "No live request produced an HTTP response; retry after the provider state changes",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
