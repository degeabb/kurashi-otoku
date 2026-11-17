#!/usr/bin/env python3
"""Refresh the long-lived Threads access token (valid 60 days; refreshable after 24h).

Prints ONLY the refreshed token on stdout so the workflow can mask it and store it back
into the THREADS_ACCESS_TOKEN repo secret. Diagnostics go to stderr. Never logs the token.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

URL = "https://graph.threads.net/refresh_access_token"


def main() -> int:
    token = os.environ.get("THREADS_ACCESS_TOKEN")
    if not token:
        print("ERROR: THREADS_ACCESS_TOKEN is not set", file=sys.stderr)
        return 1
    q = urllib.parse.urlencode({"grant_type": "th_refresh_token", "access_token": token})
    try:
        with urllib.request.urlopen(f"{URL}?{q}", timeout=30) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:300]
        print(f"ERROR: refresh failed ({e.code}): {body}. If the token already expired, "
              "generate a new one in the Meta app dashboard (see social/THREADS_SETUP.md).", file=sys.stderr)
        return 1
    new = data.get("access_token")
    if not new:
        print(f"ERROR: unexpected response keys: {sorted(data)}", file=sys.stderr)
        return 1
    days = int(data.get("expires_in", 0)) // 86400
    print(f"Token refreshed; valid for about {days} more days.", file=sys.stderr)
    print(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
