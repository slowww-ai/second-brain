"""Tiny status page for the second brain.

Usage:
    python scripts/dashboard.py            # serve on http://localhost:3100
    python scripts/dashboard.py --port 8000

Shows the number of unprocessed raw files (new or changed since last ingest,
plus non-markdown files still missing a companion .md).
"""
from __future__ import annotations
import argparse, hashlib, http.server, pathlib, sqlite3, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "wiki" / "raw"
NOTES = ROOT / "wiki" / "notes"
OUTPUTS = ROOT / "wiki" / "outputs"
DB = ROOT / "wiki" / "index.db"


def content_hash(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def count_unprocessed() -> tuple[int, int, int]:
    """Return (total_unprocessed, new_or_changed_md, non_md_missing_companion)."""
    ledger: dict[str, str] = {}
    if DB.exists():
        con = sqlite3.connect(DB)
        ledger = {row[0]: row[1] for row in con.execute("SELECT raw_file, content_hash FROM ingested")}
        con.close()

    new_md = 0
    missing_companion = 0
    for r in sorted(RAW.glob("*")):
        if r.is_dir() or r.name.startswith("."):
            continue
        if r.suffix.lower() != ".md":
            if not r.with_suffix(r.suffix + ".md").exists() and not r.with_suffix(".md").exists():
                missing_companion += 1
            continue
        if ledger.get(r.name) != content_hash(r):
            new_md += 1
    return new_md + missing_companion, new_md, missing_companion


def count_md(root: pathlib.Path) -> int:
    if not root.exists():
        return 0
    return sum(1 for _ in root.rglob("*.md"))


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>second brain — unprocessed</title>
<meta http-equiv="refresh" content="30">
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; background: #fafafa;
         color: #1a202c; display: grid; place-items: center; min-height: 100vh; margin: 0; padding: 24px; }}
  .wrap  {{ display: flex; flex-direction: column; gap: 16px; width: min(720px, 100%); }}
  .card  {{ background: #fff; border: 1px solid #ececec; border-radius: 14px;
           padding: 32px; box-shadow: 0 1px 3px rgba(16,24,40,.06); text-align: center; }}
  .hero  {{ padding: 48px 32px; }}
  .row   {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }}
  .label {{ text-transform: uppercase; font-size: 12px; letter-spacing: .1em; color: #718096; }}
  .count {{ font-weight: 600; line-height: 1; margin: 8px 0 4px; }}
  .hero .count {{ font-size: 96px; color: {tone}; }}
  .tile .count {{ font-size: 40px; color: #1a202c; }}
  .sub   {{ font-size: 13px; color: #718096; }}
</style>
</head>
<body>
  <div class="wrap">
    <div class="card hero">
      <div class="label">unprocessed raw files</div>
      <div class="count">{total}</div>
      <div class="sub">{breakdown}</div>
    </div>
    <div class="row">
      <div class="card tile">
        <div class="label">raw captures</div>
        <div class="count">{raw_total}</div>
      </div>
      <div class="card tile">
        <div class="label">notes</div>
        <div class="count">{notes_total}</div>
      </div>
      <div class="card tile">
        <div class="label">final</div>
        <div class="count">{final_total}</div>
      </div>
    </div>
  </div>
</body>
</html>
"""


def render() -> bytes:
    total, new_md, missing = count_unprocessed()
    tone = "#059669" if total == 0 else "#d97706" if total <= 5 else "#dc2626"
    if total == 0:
        breakdown = "all caught up"
    else:
        parts = []
        if new_md:
            parts.append(f"{new_md} new/changed markdown")
        if missing:
            parts.append(f"{missing} needs companion .md")
        breakdown = " · ".join(parts)
    return PAGE.format(
        total=total,
        tone=tone,
        breakdown=html.escape(breakdown),
        raw_total=count_md(RAW),
        notes_total=count_md(NOTES),
        final_total=count_md(OUTPUTS),
    ).encode()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = render()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=3100)
    ap.add_argument("--host", default="127.0.0.1")
    args = ap.parse_args()
    srv = http.server.HTTPServer((args.host, args.port), Handler)
    print(f"dashboard at http://{args.host}:{args.port}  (Ctrl-C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.server_close()


if __name__ == "__main__":
    main()
