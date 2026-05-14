#!/usr/bin/env python3
"""
check_links.py — verify every `url:` in standards/*.yaml is reachable.

Usage (from repo root or anywhere):
    python3 standards/check_links.py                 # check all yaml files
    python3 standards/check_links.py itu-t.yaml      # check one file
    python3 standards/check_links.py --workers 16    # tweak parallelism
    python3 standards/check_links.py --csv out.csv   # also write a CSV report

What it does:
    - Loads each YAML and walks `standards[].url`.
    - Issues a HEAD request first (cheap); falls back to GET if HEAD is
      rejected (some hosts return 405/403 on HEAD).
    - Follows redirects, accepts 200/301/302/303/307/308 as "ok".
    - Flags every other outcome (timeout, connection error, 4xx/5xx)
      with the body id and the offending URL.
    - Concurrency via thread-pool (URLs are I/O bound).

What it does NOT do:
    - Crawl into page content (a "200" page that says "this standard
      has moved" still counts as ok — link-rot detection at content
      level is a separate problem).
    - Cache results — fresh probe every run. Add --cache later if the
      runtime matters.
"""

from __future__ import annotations
import argparse
import csv as csvmod
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    sys.exit("requests not installed. Run: pip3 install requests pyyaml")

try:
    import yaml
except ImportError:
    sys.exit("PyYAML not installed. Run: pip3 install pyyaml")

HERE = Path(__file__).resolve().parent

# Servers reliably reject Python's default UA; pretend to be a normal browser.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/17.5 Safari/605.1.15"
    ),
    # Some hosts (BSI in particular) reject `Accept: */*` — they want a
    # specific HTML-flavoured Accept. Match what a real browser sends.
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

OK_STATUSES = {200, 301, 302, 303, 307, 308}


def collect_urls(yaml_path: Path):
    """Return [(body_id, std_id, url), ...] for every standard with a url."""
    with yaml_path.open() as f:
        doc = yaml.safe_load(f)
    body_id = (doc.get("body") or {}).get("id") or yaml_path.stem
    out = []
    for std in doc.get("standards") or []:
        url = std.get("url")
        if not url:
            continue
        out.append((body_id, std.get("id", "?"), url.strip()))
    return out


def probe(url: str, timeout: int = 15) -> tuple[int | None, str]:
    """Return (status_code or None, note). None means network failure."""
    try:
        # HEAD first
        r = requests.head(
            url,
            headers=HEADERS,
            allow_redirects=True,
            timeout=timeout,
            verify=True,
        )
        if r.status_code in OK_STATUSES:
            return r.status_code, ""
        if r.status_code in (400, 403, 405, 501):
            # Some hosts block HEAD (BSI returns 400, others 403/405/501).
            # Retry with GET (stream so we don't pull the full body).
            # Give GET its own full timeout since the host is often slow.
            r = requests.get(
                url,
                headers=HEADERS,
                allow_redirects=True,
                timeout=timeout * 2,
                stream=True,
                verify=True,
            )
            r.close()
            return r.status_code, "via GET"
        return r.status_code, ""
    except requests.exceptions.SSLError as e:
        return None, f"SSL: {type(e).__name__}"
    except requests.exceptions.Timeout:
        return None, "timeout"
    except requests.exceptions.ConnectionError as e:
        return None, f"connection: {type(e).__name__}"
    except requests.exceptions.RequestException as e:
        return None, f"req: {type(e).__name__}"


def fmt_row(body: str, sid: str, url: str, status, note: str) -> str:
    short = url if len(url) <= 80 else url[:77] + "..."
    if status in OK_STATUSES:
        marker = "OK   "
    elif status is None:
        marker = "ERR  "
    else:
        marker = f"{status:>4} "
    return f"{marker}  {body:<8} {sid:<28} {short} {note}".rstrip()


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("files", nargs="*", help="yaml files (default: all in standards/)")
    ap.add_argument("--workers", type=int, default=12, help="parallel probes (default 12)")
    ap.add_argument("--timeout", type=int, default=15, help="per-request timeout in s")
    ap.add_argument("--csv", metavar="PATH", help="write a full CSV report")
    ap.add_argument("--only-fail", action="store_true", help="suppress OK rows on stdout")
    args = ap.parse_args()

    if args.files:
        paths = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute() and not p.exists():
                p = HERE / Path(f).name
            paths.append(p)
    else:
        paths = sorted(HERE.glob("*.yaml"))

    urls: list[tuple[str, str, str, str]] = []
    for p in paths:
        for body, sid, url in collect_urls(p):
            urls.append((p.name, body, sid, url))

    print(f"Probing {len(urls)} URLs across {len(paths)} files "
          f"(workers={args.workers}, timeout={args.timeout}s)\n", file=sys.stderr)

    results = []  # (file, body, sid, url, status, note)
    started = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(probe, u, args.timeout): (f, b, s, u)
                   for (f, b, s, u) in urls}
        done = 0
        for fut in as_completed(futures):
            f, b, s, u = futures[fut]
            status, note = fut.result()
            results.append((f, b, s, u, status, note))
            done += 1
            if done % 25 == 0 or done == len(urls):
                print(f"  ... {done}/{len(urls)}", file=sys.stderr)

    # Sort: failures first (by file, body, id), then OKs.
    def sort_key(r):
        f, b, s, u, status, note = r
        is_ok = status in OK_STATUSES
        return (is_ok, f, b, s)
    results.sort(key=sort_key)

    fails = [r for r in results if r[4] not in OK_STATUSES]
    oks = [r for r in results if r[4] in OK_STATUSES]

    if fails:
        print(f"\n{len(fails)} broken / suspect link(s):\n")
        for (f, b, sid, u, status, note) in fails:
            print(fmt_row(b, sid, u, status, note))
    if not args.only_fail and oks:
        print(f"\n{len(oks)} OK:\n")
        for (f, b, sid, u, status, note) in oks:
            print(fmt_row(b, sid, u, status, note))

    elapsed = time.time() - started
    print(f"\nDone in {elapsed:.1f}s — {len(oks)} OK, {len(fails)} broken/suspect.",
          file=sys.stderr)

    if args.csv:
        with open(args.csv, "w", newline="") as cf:
            w = csvmod.writer(cf)
            w.writerow(["file", "body", "id", "url", "status", "note"])
            for row in results:
                w.writerow(row)
        print(f"Wrote {args.csv}", file=sys.stderr)

    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
