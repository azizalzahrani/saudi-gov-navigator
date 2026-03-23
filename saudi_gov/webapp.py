"""
Local Web App for Saudi Gov Navigator.

Hosts a lightweight Arabic-first browser UI on localhost without extra
runtime dependencies.
"""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, unquote, urlparse

from saudi_gov.agents.requirements_agent import RequirementsAgent
from saudi_gov.agents.service_finder import ServiceFinder
from saudi_gov.search import SemanticSearch

INDEX_HTML = """<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Saudi Gov Navigator | دليل الخدمات الحكومية السعودية</title>
    <style>
      :root {
        --bg: #f6f2e8;
        --panel: rgba(255, 255, 255, 0.82);
        --panel-strong: #ffffff;
        --text: #14261d;
        --muted: #5d6f62;
        --line: rgba(20, 38, 29, 0.09);
        --green: #0f6d46;
        --green-deep: #083a29;
        --gold: #b78b3e;
        --sand: #efe0bf;
        --shadow: 0 18px 45px rgba(13, 46, 30, 0.08);
      }

      * { box-sizing: border-box; }

      body {
        margin: 0;
        font-family: "DIN Next LT Arabic", "SF Arabic", "Segoe UI", Tahoma, sans-serif;
        color: var(--text);
        background:
          radial-gradient(circle at top right, rgba(183, 139, 62, 0.16), transparent 28%),
          radial-gradient(circle at left 20%, rgba(15, 109, 70, 0.12), transparent 30%),
          linear-gradient(180deg, #fbf9f3 0%, var(--bg) 100%);
        min-height: 100vh;
      }

      .shell {
        width: min(1200px, calc(100% - 32px));
        margin: 24px auto 40px;
      }

      .hero {
        background: linear-gradient(135deg, rgba(8, 58, 41, 0.96), rgba(15, 109, 70, 0.88));
        color: #f8f3e8;
        border-radius: 28px;
        padding: 28px;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
      }

      .hero::after {
        content: "";
        position: absolute;
        inset: auto -40px -60px auto;
        width: 240px;
        height: 240px;
        background: radial-gradient(circle, rgba(239, 224, 191, 0.22), transparent 65%);
      }

      .hero h1 {
        margin: 0 0 8px;
        font-size: clamp(28px, 4vw, 42px);
        line-height: 1.15;
      }

      .hero p {
        margin: 0;
        max-width: 760px;
        color: rgba(248, 243, 232, 0.86);
        font-size: 16px;
        line-height: 1.8;
      }

      .search-panel {
        margin-top: 22px;
        display: grid;
        gap: 14px;
      }

      form {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
      }

      input[type="search"] {
        flex: 1 1 480px;
        min-height: 58px;
        border: 0;
        border-radius: 18px;
        padding: 0 18px;
        font-size: 17px;
        color: var(--text);
        background: rgba(255, 255, 255, 0.95);
        outline: none;
      }

      button {
        min-height: 58px;
        border: 0;
        border-radius: 18px;
        padding: 0 22px;
        background: linear-gradient(135deg, #d8b46a, var(--gold));
        color: #182218;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
      }

      button.secondary {
        min-height: 42px;
        padding: 0 14px;
        background: rgba(255, 255, 255, 0.14);
        color: #fff8ea;
        border: 1px solid rgba(255, 255, 255, 0.12);
      }

      .quick-actions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
      }

      .layout {
        display: grid;
        grid-template-columns: 1.1fr 0.9fr;
        gap: 20px;
        margin-top: 20px;
      }

      .panel {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 24px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(14px);
      }

      .panel-header {
        padding: 20px 22px 0;
      }

      .panel h2, .panel h3 {
        margin: 0;
      }

      .panel-subtitle {
        margin-top: 8px;
        color: var(--muted);
        font-size: 14px;
      }

      .results {
        padding: 18px 18px 20px;
        display: grid;
        gap: 12px;
      }

      .result-card {
        background: var(--panel-strong);
        border: 1px solid rgba(8, 58, 41, 0.08);
        border-radius: 18px;
        padding: 16px;
        cursor: pointer;
        transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
      }

      .result-card:hover,
      .result-card.active {
        transform: translateY(-1px);
        border-color: rgba(15, 109, 70, 0.25);
        box-shadow: 0 14px 28px rgba(15, 109, 70, 0.09);
      }

      .result-card h3 {
        font-size: 18px;
        margin-bottom: 8px;
      }

      .meta {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-bottom: 10px;
      }

      .pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 10px;
        border-radius: 999px;
        background: #eef6f0;
        color: var(--green-deep);
        font-size: 12px;
        font-weight: 700;
      }

      .result-card p,
      .detail-copy {
        margin: 0;
        color: var(--muted);
        line-height: 1.8;
      }

      .detail {
        padding: 22px;
        display: grid;
        gap: 18px;
      }

      .detail-title {
        display: grid;
        gap: 10px;
      }

      .detail-title h2 {
        font-size: clamp(24px, 3vw, 34px);
      }

      .stats {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
      }

      .stat-box {
        background: linear-gradient(180deg, #fffdf7, #f7f1e4);
        border: 1px solid rgba(183, 139, 62, 0.16);
        border-radius: 18px;
        padding: 14px;
      }

      .stat-box span {
        display: block;
        color: var(--muted);
        font-size: 12px;
        margin-bottom: 6px;
      }

      .stat-box strong {
        display: block;
        font-size: 15px;
        line-height: 1.6;
      }

      .detail-section {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 16px 18px;
      }

      .detail-section ol,
      .detail-section ul {
        margin: 10px 0 0;
        padding-right: 18px;
        color: var(--muted);
        line-height: 1.9;
      }

      .platforms {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 16px;
      }

      .platform-tag {
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(15, 109, 70, 0.08);
        color: var(--green-deep);
        font-size: 13px;
      }

      .status {
        color: var(--muted);
        font-size: 14px;
      }

      .empty {
        padding: 22px;
        color: var(--muted);
      }

      @media (max-width: 980px) {
        .layout {
          grid-template-columns: 1fr;
        }
      }

      @media (max-width: 640px) {
        .shell {
          width: min(100% - 18px, 1200px);
          margin-top: 10px;
        }

        .hero {
          border-radius: 22px;
          padding: 22px 18px;
        }

        .stats {
          grid-template-columns: 1fr;
        }

        button,
        input[type="search"] {
          width: 100%;
        }
      }
    </style>
  </head>
  <body>
    <main class="shell">
      <section class="hero">
        <h1>دليل الخدمات الحكومية السعودية</h1>
        <p>
          واجهة محلية سريعة للبحث في الخدمات الحكومية السعودية، مراجعة المتطلبات،
          قراءة الخطوات، واستكشاف المنصات المناسبة للمواطنين والمقيمين ورواد الأعمال.
        </p>

        <div class="search-panel">
          <form id="search-form">
            <input id="search-input" type="search" placeholder="ابحث مثلاً: تجديد جواز السفر، نقل كفالة، تأسيس شركة" />
            <button type="submit">ابحث الآن</button>
          </form>

          <div class="quick-actions">
            <button class="secondary" data-scenario="وافد جديد">وافد جديد</button>
            <button class="secondary" data-scenario="تأسيس شركة">تأسيس شركة</button>
            <button class="secondary" data-scenario="كيف أنقل عاملي في معايش؟">نقل عامل</button>
            <button class="secondary" data-scenario="أنا أريد تجديد جواز سفري، ما الخطوات؟">تجديد جواز السفر</button>
          </div>
        </div>
      </section>

      <section class="layout">
        <section class="panel">
          <div class="panel-header">
            <h2>النتائج</h2>
            <div id="status" class="panel-subtitle">جارٍ تحميل المنصات والاقتراحات...</div>
            <div id="platforms" class="platforms"></div>
          </div>
          <div id="results" class="results"></div>
        </section>

        <aside class="panel">
          <div id="detail" class="detail">
            <div class="detail-title">
              <h2>ابدأ من اليسار</h2>
              <p class="detail-copy">
                ابحث عن خدمة أو اختر سيناريو جاهز لعرض التفاصيل الكاملة والخطوات والمتطلبات.
              </p>
            </div>
          </div>
        </aside>
      </section>
    </main>

    <script>
      const resultsEl = document.getElementById("results");
      const detailEl = document.getElementById("detail");
      const statusEl = document.getElementById("status");
      const platformsEl = document.getElementById("platforms");
      const searchInput = document.getElementById("search-input");
      let activeServiceId = null;

      async function fetchJson(url) {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error("Failed request");
        }
        return response.json();
      }

      function renderPlatforms(platforms) {
        platformsEl.innerHTML = platforms
          .map((platform) => `<span class="platform-tag">${platform.name_ar} · ${platform.services_count} خدمة</span>`)
          .join("");
      }

      function renderResults(items) {
        if (!items.length) {
          resultsEl.innerHTML = `<div class="empty">لا توجد نتائج مطابقة. جرّب كلمات أقصر أو استخدم أحد السيناريوهات الجاهزة.</div>`;
          return;
        }

        resultsEl.innerHTML = items.map((item) => `
          <article class="result-card ${item.id === activeServiceId ? "active" : ""}" data-id="${item.id}">
            <h3>${item.name}</h3>
            <div class="meta">
              <span class="pill">${item.platform}</span>
              <span class="pill">${item.category}</span>
            </div>
            <p>${item.description}</p>
          </article>
        `).join("");

        for (const card of resultsEl.querySelectorAll(".result-card")) {
          card.addEventListener("click", () => loadService(card.dataset.id));
        }
      }

      function renderDetail(service) {
        detailEl.innerHTML = `
          <div class="detail-title">
            <h2>${service.name}</h2>
            <p class="detail-copy">${service.description}</p>
          </div>

          <div class="stats">
            <div class="stat-box">
              <span>المنصة</span>
              <strong>${service.platform}</strong>
            </div>
            <div class="stat-box">
              <span>الرسوم</span>
              <strong>${service.fees_note}</strong>
            </div>
            <div class="stat-box">
              <span>وقت المعالجة</span>
              <strong>${service.processing_time}</strong>
            </div>
          </div>

          <section class="detail-section">
            <h3>المتطلبات</h3>
            <ul>${service.requirements.map((item) => `<li>${item}</li>`).join("")}</ul>
          </section>

          <section class="detail-section">
            <h3>الخطوات</h3>
            <ol>${service.steps.map((item) => `<li>${item}</li>`).join("")}</ol>
          </section>

          <section class="detail-section">
            <h3>نصائح مهمة</h3>
            <ul>${service.tips.map((item) => `<li>${item}</li>`).join("")}</ul>
          </section>

          <section class="detail-section">
            <h3>رابط المنصة</h3>
            <p class="detail-copy"><a href="${service.platform_url}" target="_blank" rel="noreferrer">${service.platform_url}</a></p>
          </section>
        `;
      }

      async function loadService(serviceId) {
        activeServiceId = serviceId;
        statusEl.textContent = "جارٍ تحميل تفاصيل الخدمة...";
        const service = await fetchJson(`/api/service/${encodeURIComponent(serviceId)}`);
        renderDetail(service);
        for (const card of resultsEl.querySelectorAll(".result-card")) {
          card.classList.toggle("active", card.dataset.id === serviceId);
        }
        statusEl.textContent = `تم تحميل الخدمة: ${service.name}`;
      }

      async function runSearch(query) {
        statusEl.textContent = "جارٍ البحث...";
        const payload = await fetchJson(`/api/search?q=${encodeURIComponent(query)}`);
        renderResults(payload.results);
        statusEl.textContent = `تم العثور على ${payload.results.length} نتيجة`;
        if (payload.results.length) {
          await loadService(payload.results[0].id);
        } else {
          detailEl.innerHTML = `
            <div class="detail-title">
              <h2>لا توجد نتائج</h2>
              <p class="detail-copy">جرّب صياغة أخرى أو استخدم سيناريو جاهز من الأعلى.</p>
            </div>
          `;
        }
      }

      async function runScenario(name) {
        statusEl.textContent = `جارٍ تحميل سيناريو: ${name}`;
        const payload = await fetchJson(`/api/scenario?name=${encodeURIComponent(name)}`);
        renderResults(payload.results);
        statusEl.textContent = `سيناريو ${name}: ${payload.results.length} خدمات مقترحة`;
        if (payload.results.length) {
          await loadService(payload.results[0].id);
        }
      }

      document.getElementById("search-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const query = searchInput.value.trim();
        if (!query) {
          return;
        }
        await runSearch(query);
      });

      for (const button of document.querySelectorAll("[data-scenario]")) {
        button.addEventListener("click", async () => {
          searchInput.value = button.dataset.scenario;
          await runScenario(button.dataset.scenario);
        });
      }

      async function bootstrap() {
        const platforms = await fetchJson("/api/platforms");
        renderPlatforms(platforms.platforms);
        await runScenario("وافد جديد");
      }

      bootstrap().catch(() => {
        statusEl.textContent = "تعذر تحميل البيانات المحلية.";
      });
    </script>
  </body>
</html>
"""


def _localized_key(base_key: str, language: str) -> str:
    return f"{base_key}_en" if language == "en" else f"{base_key}_ar"


class SaudiGovLocalApp:
    """Application state and serialization helpers for the local web UI."""

    def __init__(self, language: str = "ar"):
        self.language = language
        self.search = SemanticSearch(language=language)
        self.finder = ServiceFinder(language=language)
        self.requirements = RequirementsAgent(language=language)
        self._service_platform_map = self._build_service_platform_map()

    def _build_service_platform_map(self) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        for platform_name, platform_data in self.finder.platforms.items():
            for service in platform_data.get("services", []):
                service_id = service.get("id")
                if service_id:
                    mapping[service_id] = platform_name
        return mapping

    def _serialize_service_card(self, service: Dict[str, Any]) -> Dict[str, Any]:
        name_key = _localized_key("name", self.language)
        description_key = _localized_key("description", self.language)
        category_key = "category_en" if self.language == "en" else "category"
        fees_key = "fees_en" if self.language == "en" else "fees"
        time_key = "processing_time_en" if self.language == "en" else "processing_time"
        fees = service.get(fees_key, {})

        return {
            "id": service.get("id"),
            "name": service.get(name_key, ""),
            "description": service.get(description_key, ""),
            "category": service.get(category_key, ""),
            "platform": self._service_platform_map.get(service.get("id", ""), ""),
            "fees_note": fees.get("note", ""),
            "processing_time": service.get(time_key, ""),
        }

    def search_services(self, query: str, max_results: int = 8) -> List[Dict[str, Any]]:
        results = self.search.search(query, max_results=max_results)
        return [self._serialize_service_card(item["service"]) for item in results]

    def scenario_services(self, scenario: str, max_results: int = 8) -> List[Dict[str, Any]]:
        services = self.finder.suggest_services(scenario)[:max_results]
        return [self._serialize_service_card(service) for service in services]

    def service_detail(self, service_id: str) -> Optional[Dict[str, Any]]:
        guide = self.requirements.get_full_service_guide(service_id)
        if not guide:
            return None

        platform_name = self._service_platform_map.get(service_id, "")
        platform_info = self.finder.get_platform_info(platform_name) if platform_name else None

        fees = guide.get("fees", {})
        return {
            "service_id": service_id,
            "name": guide.get("name", ""),
            "description": guide.get("description", ""),
            "category": guide.get("category", ""),
            "requirements": guide.get("requirements", []),
            "steps": guide.get("steps", []),
            "tips": guide.get("tips", []),
            "fees_note": fees.get("note", ""),
            "processing_time": guide.get("processing_time", ""),
            "platform": platform_name,
            "platform_url": platform_info.get("url", "") if platform_info else "",
        }

    def platforms(self) -> List[Dict[str, Any]]:
        items = []
        for platform_name in self.finder.get_all_platforms().keys():
            info = self.finder.get_platform_info(platform_name)
            if info:
                items.append(info)
        return items


def create_handler(app: SaudiGovLocalApp):
    """Create a request handler bound to a specific app instance."""

    class SaudiGovRequestHandler(BaseHTTPRequestHandler):
        server_version = "SaudiGovNavigator/0.1"

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
            return

        def do_GET(self) -> None:  # noqa: N802
            self._dispatch_request(include_body=True)

        def do_HEAD(self) -> None:  # noqa: N802
            self._dispatch_request(include_body=False)

        def _dispatch_request(self, include_body: bool) -> None:
            parsed = urlparse(self.path)

            try:
                if parsed.path == "/":
                    self._send_html(INDEX_HTML, include_body=include_body)
                    return

                if parsed.path == "/health":
                    self._send_json({"status": "ok"}, include_body=include_body)
                    return

                if parsed.path == "/api/search":
                    query = parse_qs(parsed.query).get("q", [""])[0].strip()
                    self._send_json(
                        {"results": app.search_services(query) if query else []},
                        include_body=include_body,
                    )
                    return

                if parsed.path == "/api/scenario":
                    name = parse_qs(parsed.query).get("name", [""])[0].strip()
                    self._send_json(
                        {"results": app.scenario_services(name) if name else []},
                        include_body=include_body,
                    )
                    return

                if parsed.path == "/api/platforms":
                    self._send_json({"platforms": app.platforms()}, include_body=include_body)
                    return

                if parsed.path.startswith("/api/service/"):
                    service_id = unquote(parsed.path.split("/api/service/", 1)[1])
                    service = app.service_detail(service_id)
                    if service is None:
                        self._send_json(
                            {"error": "Service not found"},
                            status=HTTPStatus.NOT_FOUND,
                            include_body=include_body,
                        )
                    else:
                        self._send_json(service, include_body=include_body)
                    return

                self._send_json(
                    {"error": "Not found"},
                    status=HTTPStatus.NOT_FOUND,
                    include_body=include_body,
                )
            except Exception as exc:  # pragma: no cover - defensive path
                self._send_json(
                    {"error": str(exc)},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                    include_body=include_body,
                )

        def _send_html(
            self,
            html: str,
            status: HTTPStatus = HTTPStatus.OK,
            include_body: bool = True,
        ) -> None:
            payload = html.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            if include_body:
                self.wfile.write(payload)

        def _send_json(
            self,
            data: Dict[str, Any],
            status: HTTPStatus = HTTPStatus.OK,
            include_body: bool = True,
        ) -> None:
            payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            if include_body:
                self.wfile.write(payload)

    return SaudiGovRequestHandler


def create_server(host: str = "127.0.0.1", port: int = 8000, language: str = "ar") -> ThreadingHTTPServer:
    """Create a configured local HTTP server."""
    app = SaudiGovLocalApp(language=language)
    handler = create_handler(app)
    return ThreadingHTTPServer((host, port), handler)


def main() -> None:
    """Run the local web app."""
    parser = argparse.ArgumentParser(description="Run Saudi Gov Navigator locally")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument(
        "--language",
        choices=["ar", "en"],
        default="ar",
        help="Primary UI language for localized service content",
    )
    args = parser.parse_args()

    server = create_server(host=args.host, port=args.port, language=args.language)
    print(f"Saudi Gov Navigator running at http://{args.host}:{args.port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
