"""Tests for the ad-disclosure guarantee in the social post generator.

Why it matters: every post promotes a site that earns a referral reward, so a post
without a visible #PR tag would be stealth marketing under Japan's rules.
Run: .venv/bin/python -m pytest social/test_generate.py -q
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate import DISCLOSURE_TAG, effective_length, with_disclosure  # noqa: E402


def test_untagged_post_gets_pr_prefix():
    assert with_disclosure("楽天モバイルで月額を節約") == f"{DISCLOSURE_TAG} 楽天モバイルで月額を節約"


def test_existing_disclosure_is_not_duplicated():
    for text in ("#PR Save on your phone bill", "節約しよう #広告", "Cheap SIM #ad", "Deal #Sponsored"):
        assert with_disclosure(text) == text


def test_lookalike_hashtags_do_not_count_as_disclosure():
    # '#PRice' or '#adventure' must not satisfy the requirement.
    assert with_disclosure("#PRice drop!").startswith(f"{DISCLOSURE_TAG} ")
    assert with_disclosure("#adventure in Japan").startswith(f"{DISCLOSURE_TAG} ")


def test_empty_text_stays_empty():
    # A failed generation must stay visibly empty, not become a bare '#PR'.
    assert with_disclosure("   ") == ""


def test_tag_counts_toward_platform_limit():
    base = "x" * 277
    assert effective_length(with_disclosure(base), "x", None) == 277 + len(DISCLOSURE_TAG) + 1
