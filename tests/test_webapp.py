"""
Web app tests for the local Saudi Gov Navigator host.
"""

import json
import threading
import unittest
from urllib.request import urlopen

from saudi_gov.webapp import create_server


class TestWebApp(unittest.TestCase):
    """Basic endpoint tests for the local web host."""

    def setUp(self):
        self.server = create_server(host="127.0.0.1", port=0, language="ar")
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def _fetch_text(self, path: str) -> str:
        with urlopen(f"http://127.0.0.1:{self.port}{path}") as response:
            return response.read().decode("utf-8")

    def _fetch_json(self, path: str):
        return json.loads(self._fetch_text(path))

    def test_index_page_loads(self):
        html = self._fetch_text("/")
        self.assertIn("Saudi Gov Navigator", html)
        self.assertIn("دليل الخدمات الحكومية السعودية", html)

    def test_search_endpoint_returns_results(self):
        payload = self._fetch_json("/api/search?q=%D8%AC%D9%88%D8%A7%D8%B2")
        self.assertIn("results", payload)
        self.assertGreater(len(payload["results"]), 0)

    def test_service_detail_endpoint_returns_guide(self):
        payload = self._fetch_json("/api/service/absher_passport_renewal")
        self.assertEqual(payload["service_id"], "absher_passport_renewal")
        self.assertIn("requirements", payload)
        self.assertIn("steps", payload)


if __name__ == "__main__":
    unittest.main()
