from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from xquik_signals import collect_xquik_signal_markdown


class FakeResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {
            "tweets": [
                {
                    "id": "123",
                    "text": "Vendor launched an integration for customers.",
                    "createdAt": "2026-06-01T12:00:00Z",
                    "likeCount": 3,
                    "retweetCount": 1,
                    "replyCount": 2,
                    "quoteCount": 0,
                    "author": {"username": "vendor"},
                }
            ]
        }


class XquikSignalsTest(unittest.TestCase):
    def test_returns_empty_without_key(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(collect_xquik_signal_markdown("Vendor"), "")

    def test_renders_signal_rows_without_key_disclosure(self) -> None:
        calls = []

        def fake_get(url: str, headers: dict, params: dict, timeout: int) -> FakeResponse:
            calls.append({"url": url, "headers": headers, "params": params, "timeout": timeout})
            return FakeResponse()

        with patch.dict(os.environ, {"XQUIK_API_KEY": "fake-key"}, clear=True):
            with patch("xquik_signals.requests.get", fake_get):
                markdown = collect_xquik_signal_markdown("Vendor", ticker="VND", website="https://vendor.example")

        self.assertIn("Optional Xquik Public X Signal Context", markdown)
        self.assertIn("https://x.com/vendor/status/123", markdown)
        self.assertIn("Vendor launched an integration for customers.", markdown)
        self.assertEqual(markdown.count("https://x.com/vendor/status/123"), 1)
        self.assertNotIn("fake-key", markdown)
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0]["headers"]["x-api-key"], "fake-key")
        self.assertEqual(calls[0]["params"]["queryType"], "Latest")
        self.assertEqual(calls[0]["params"]["limit"], 5)


if __name__ == "__main__":
    unittest.main()
