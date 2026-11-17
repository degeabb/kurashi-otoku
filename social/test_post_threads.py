"""Tests for the Threads auto-poster.

Why these matter: the poster runs unattended. A bug could flood the timeline after a
missed day, publish without the #PR disclosure, publish confidential reward terms, or
post a draft that was never approved. Each test pins one of those guarantees.
Run: .venv/bin/python -m pytest social/test_post_threads.py -q
"""
import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from post_threads import PostError, next_due, prepare_text, publish, record, load_yaml  # noqa: E402

LINK = "https://japanmobilesim.com/sim/"


def q(i, d, lang="ja", text=f"Compare SIMs {LINK}"):
    return {"id": i, "date": d, "lang": lang, "text": text}


def test_only_one_post_even_after_missed_days():
    # Three overdue posts: only the earliest goes out today; the rest wait for later runs.
    queue = [q("c", "2026-11-20"), q("a", "2026-11-18"), q("b", "2026-11-19")]
    assert next_due(queue, set(), date(2026, 11, 22))["id"] == "a"


def test_future_and_already_posted_are_skipped():
    queue = [q("past", "2026-11-18"), q("future", "2026-12-01")]
    assert next_due(queue, {"past"}, date(2026, 11, 20)) is None


def test_entry_missing_fields_is_rejected():
    with pytest.raises(PostError):
        next_due([{"id": "x", "date": "2026-11-18", "lang": "ja"}], set(), date(2026, 11, 20))


def test_pr_disclosure_is_always_added():
    assert prepare_text(f"楽天モバイルの比較 {LINK}").startswith("#PR ")


def test_over_limit_is_refused_not_truncated():
    with pytest.raises(PostError, match="limit"):
        prepare_text("x" * 480 + " " + LINK)


def test_post_without_site_link_is_refused():
    with pytest.raises(PostError, match="link"):
        prepare_text("Great SIM deals today!")


@pytest.mark.parametrize("secret", ["楽天キャッシュがもらえる", "earn Rakuten Cash", "15%還元", "60 months of rewards"])
def test_confidential_reward_terms_are_blocked(secret):
    with pytest.raises(PostError, match="confidential"):
        prepare_text(f"{secret} {LINK}")


def test_publish_creates_container_then_publishes_it():
    calls = []

    def fake_http(url, params):
        calls.append((url, dict(params)))
        return {"id": "container-1"} if url.endswith("/threads") else {"id": "post-9"}

    assert publish("#PR hi " + LINK, "123", "tok", http=fake_http) == "post-9"
    assert calls[0][0].endswith("/123/threads") and calls[0][1]["media_type"] == "TEXT"
    assert calls[1][0].endswith("/123/threads_publish") and calls[1][1]["creation_id"] == "container-1"


def test_publish_fails_loudly_on_bad_api_response():
    with pytest.raises(PostError):
        publish("#PR hi " + LINK, "123", "tok", http=lambda url, params: {"error": "nope"})


def test_record_appends_to_posted_log(tmp_path):
    log = tmp_path / "posted.yaml"
    record(q("a", "2026-11-18"), "post-1", path=log)
    record(q("b", "2026-11-19", lang="en"), "post-2", path=log)
    assert [p["id"] for p in load_yaml(log, "posted")] == ["a", "b"]
