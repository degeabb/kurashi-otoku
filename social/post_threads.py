#!/usr/bin/env python3
"""Post the next approved, due draft from social/queue.yaml to Threads.

Run daily by .github/workflows/threads-post.yml. Approval happens BEFORE a post reaches
queue.yaml: drafts arrive as a pull request and only merged (approved) entries live here.

Rules enforced in code (not left to whoever wrote the draft):
  * at most ONE post per run — a missed day never floods the timeline
  * #PR ad disclosure prefixed (stealth-marketing rule), counted toward the 500-char limit
  * must link to the site; must not contain confidential referral-reward terms
Usage:
    python social/post_threads.py --dry-run     # show what would be posted, no API call
    python social/post_threads.py               # needs THREADS_ACCESS_TOKEN, THREADS_USER_ID
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional
from zoneinfo import ZoneInfo

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate import with_disclosure  # noqa: E402  (single source of the #PR rule)

SCRIPT_DIR = Path(__file__).resolve().parent
QUEUE = SCRIPT_DIR / "queue.yaml"
POSTED = SCRIPT_DIR / "posted.yaml"
API = "https://graph.threads.net/v1.0"
JST = ZoneInfo("Asia/Tokyo")
LIMIT = 500
SITE = "https://japanmobilesim.com"
# The referral reward terms are confidential (owner's employer). Block anything that
# looks like them, in every language we post in.
FORBIDDEN = ["楽天キャッシュ", "Rakuten Cash", "15%", "15％", "60カ月", "60ヶ月", "60か月", "60 months"]


class PostError(Exception):
    """A draft that must not be published as-is."""


def load_yaml(path: Path, key: str) -> List[dict]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    items = data.get(key) or []
    if not isinstance(items, list):
        raise PostError(f"{path.name}: '{key}' must be a list")
    return items


def next_due(queue: List[dict], posted_ids: set, today: date) -> Optional[dict]:
    """Earliest-dated queued post that is due (date <= today) and not yet posted."""
    due = []
    for p in queue:
        for req in ("id", "date", "lang", "text"):
            if not p.get(req):
                raise PostError(f"queue entry {p.get('id', '?')} is missing '{req}'")
        d = p["date"] if isinstance(p["date"], date) else date.fromisoformat(str(p["date"]))
        if d <= today and p["id"] not in posted_ids:
            due.append((d, p["id"], p))
    return min(due)[2] if due else None


def prepare_text(text: str) -> str:
    """Apply #PR and validate. Raises PostError instead of publishing a bad post."""
    text = with_disclosure(str(text))
    if len(text) > LIMIT:
        raise PostError(f"{len(text)} chars > Threads limit {LIMIT}")
    if SITE not in text:
        raise PostError(f"post has no link to {SITE}")
    hit = [w for w in FORBIDDEN if w.lower() in text.lower()]
    if hit:
        raise PostError(f"post contains confidential reward terms: {hit}")
    return text


def _post(url: str, params: Dict[str, str]) -> dict:
    req = urllib.request.Request(url, data=urllib.parse.urlencode(params).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:  # surface Meta's error body, never the token
        raise PostError(f"Threads API {e.code}: {e.read().decode(errors='replace')[:300]}") from None


def publish(text: str, user_id: str, token: str, http: Callable[[str, Dict[str, str]], dict] = _post) -> str:
    """Two-step Threads publish: create a TEXT container, then publish it. Returns post id."""
    container = http(f"{API}/{user_id}/threads", {"media_type": "TEXT", "text": text, "access_token": token})
    if "id" not in container:
        raise PostError(f"no container id in response: {container}")
    result = http(f"{API}/{user_id}/threads_publish", {"creation_id": container["id"], "access_token": token})
    if "id" not in result:
        raise PostError(f"no post id in publish response: {result}")
    return result["id"]


def record(entry: dict, threads_id: str, path: Path = POSTED) -> None:
    posted = load_yaml(path, "posted")
    posted.append({"id": entry["id"], "lang": entry["lang"], "threads_id": threads_id,
                   "posted_at": datetime.now(JST).isoformat(timespec="seconds")})
    path.write_text(yaml.safe_dump({"posted": posted}, allow_unicode=True, sort_keys=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    queue = load_yaml(QUEUE, "posts")
    posted_ids = {p["id"] for p in load_yaml(POSTED, "posted")}
    entry = next_due(queue, posted_ids, datetime.now(JST).date())
    if entry is None:
        print("Nothing due today (queue empty or all posted). Approve the next weekly batch.")
        return 0
    text = prepare_text(entry["text"])
    print(f"Next post: {entry['id']} ({entry['lang']}, {len(text)} chars)\n---\n{text}\n---")
    if args.dry_run:
        print("Dry run: not posted.")
        return 0
    token, user_id = os.environ.get("THREADS_ACCESS_TOKEN"), os.environ.get("THREADS_USER_ID")
    if not token or not user_id:
        raise PostError("THREADS_ACCESS_TOKEN / THREADS_USER_ID are not set (GitHub repo secrets)")
    threads_id = publish(text, user_id, token)
    record(entry, threads_id)
    print(f"Posted {entry['id']} → Threads id {threads_id}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PostError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
