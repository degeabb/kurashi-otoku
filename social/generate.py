#!/usr/bin/env python3
"""Generate draft social posts (X / Threads / Instagram) from social/content.yaml.

Draft-only: the output is a local review queue (social/review.html + per-draft .txt
files). Nothing is posted automatically. Review, copy, and post by hand.

Usage (from repo root, with the .venv active or via .venv/bin/python):
    python social/generate.py --mock            # no API key needed; test plumbing
    python social/generate.py --dry-run         # one real API call (needs API key)
    python social/generate.py                    # full run (needs ANTHROPIC_API_KEY)
    python social/generate.py --items sim-savings --langs ja,en --platforms x,threads

See social/README.md for the full runbook.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from jinja2 import Template

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent

DEFAULT_MODEL = "claude-sonnet-5"
DEFAULT_MAX_TOKENS = 500
ALL_PLATFORMS = ["x", "threads", "instagram"]

# Platform posting constraints.
PLATFORMS = {
    "x":         {"limit": 280,  "weighted": True,  "shorten_link": True,  "include_link": True,  "needs_image": False},
    "threads":   {"limit": 500,  "weighted": False, "shorten_link": False, "include_link": True,  "needs_image": False},
    "instagram": {"limit": 2200, "weighted": False, "shorten_link": False, "include_link": False, "needs_image": True},
}

LANG_NAMES = {
    "ja": "Japanese", "en": "English", "zh-tw": "Traditional Chinese (Taiwan)",
    "zh-cn": "Simplified Chinese", "vi": "Vietnamese", "my": "Burmese (Myanmar)",
    "th": "Thai",
}

# X (twitter-text v3) weighting: characters default to weight 2; ONLY these ranges are
# weight 1. So CJK, Vietnamese accented letters (Latin Extended Additional), and emoji
# all count as 2. Ref: twitter-text config/v3.json — defaultWeight 200, weight-100 ranges
# 0x0000-0x10FF plus a few punctuation blocks; maxWeightedTweetLength 280.
_X_WEIGHT1_RANGES = [
    (0x0000, 0x10FF), (0x2000, 0x200D), (0x2010, 0x201F), (0x2032, 0x2037),
]


def _x_weight(cp: int) -> int:
    return 1 if any(a <= cp <= b for a, b in _X_WEIGHT1_RANGES) else 2


def _weighted_len(s: str) -> int:
    return sum(_x_weight(ord(c)) for c in s)


def effective_length(text: str, platform: str, url: Optional[str]) -> int:
    """Character count as the platform measures it (X: CJK=2, link=23)."""
    cfg = PLATFORMS[platform]
    t = text
    if cfg["shorten_link"] and url and url in t:
        t = t.replace(url, "u" * 23)  # X shortens every link to a 23-char t.co
    return _weighted_len(t) if cfg["weighted"] else len(t)


# --------------------------------------------------------------------------- #
# Content loading + link resolution
# --------------------------------------------------------------------------- #
@dataclass
class Draft:
    item_id: str
    platform: str
    lang: str
    text: str
    url: Optional[str]
    image_src: Optional[str]
    char_limit: int
    effective_count: int = 0
    over_limit: bool = False
    needs_image: bool = False
    image_rel: Optional[str] = None
    warn: Optional[str] = None
    uid: str = ""


def load_content(path: Path) -> dict:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        sys.exit(f"ERROR: cannot read content file {path}: {e}")
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        sys.exit(f"ERROR: invalid YAML in {path}: {e}")
    if not isinstance(data, dict) or "site" not in data or "items" not in data:
        sys.exit(f"ERROR: {path} must have top-level 'site' and 'items' keys.")
    site = data["site"]
    known = set(site.get("languages", []))
    if not known:
        sys.exit("ERROR: site.languages is empty.")
    for it in data["items"]:
        for req in ("id", "path", "facts"):
            if not it.get(req):
                sys.exit(f"ERROR: item {it.get('id', '?')} is missing required field '{req}'.")
        bad = set((it.get("link_lang_fallback") or {}).values()) - known
        if bad:
            sys.exit(f"ERROR: item {it['id']} link_lang_fallback targets unknown langs: {bad}")
    return data


def _local_index(path: str, lang: str) -> Path:
    rel = path.strip("/")
    parts: List[str] = []
    if lang != "ja":
        parts.append(lang)
    if rel:
        parts.append(rel)
    return REPO_ROOT.joinpath(*parts, "index.html") if parts else REPO_ROOT / "index.html"


def _is_real_page(p: Path) -> bool:
    """A real page exists locally and is not a meta-refresh redirect stub."""
    if not p.is_file():
        return False
    return 'http-equiv="refresh"' not in p.read_text(encoding="utf-8", errors="ignore")


def _build_url(base: str, path: str, lang: str) -> str:
    base = base.rstrip("/")
    if lang == "ja":
        return base + path
    return base + "/" + lang + path


def resolve_url(item: dict, lang: str, base_url: str) -> str:
    """Resolve to a real (non-stub) page, honoring link_lang_fallback then ja."""
    fb = item.get("link_lang_fallback") or {}
    target = fb.get(lang, lang)
    for cand in dict.fromkeys([target, "ja"]):  # ordered, deduped
        if _is_real_page(_local_index(item["path"], cand)):
            return _build_url(base_url, item["path"], cand)
    return _build_url(base_url, item["path"], "ja")  # last resort


# --------------------------------------------------------------------------- #
# Prompt building + generation
# --------------------------------------------------------------------------- #
def build_system(site: dict) -> str:
    return (
        f"You are a social media copywriter for {site.get('brand_name', 'the site')}, a "
        "neutral, honest comparison site that helps people living in Japan cut fixed costs "
        "(mobile SIM plans, credit cards).\n"
        f"Voice: {site.get('voice', 'Honest, neutral, no hype.')}\n"
        "Hard rules:\n"
        "- Write ENTIRELY and natively in the requested language; do not translate literally.\n"
        "- Use ONLY the facts provided. NEVER invent prices, percentages, point amounts, dates, or claims.\n"
        "- Neutral and honest: acknowledge trade-offs; no hype, no clickbait, no ALL-CAPS shouting.\n"
        "- Output ONLY the post text. No explanations, no surrounding quotes, no markdown, no labels."
    )


def build_user(item: dict, lang: str, platform: str, url: str) -> str:
    lang_name = LANG_NAMES.get(lang, lang)
    facts = " ".join(item["facts"].split())
    head = f"Platform: {platform}. Language: {lang_name}.\nFACTS (use only these): {facts}\n"
    if platform == "x":
        return head + (
            "Constraints:\n"
            "- Max 280 units. On X, any non-basic-Latin character counts as TWO units "
            "(this includes Japanese/Chinese/Korean, Vietnamese accented letters, and emoji), "
            "and the link counts as 23 units. So for those languages keep the text SHORT "
            "(roughly 100 characters of text or fewer).\n"
            f"- End the post with this exact link: {url}\n"
            "- Add 1-2 relevant hashtags."
        )
    if platform == "threads":
        return head + (
            "Constraints:\n"
            "- Max 500 characters total.\n"
            f"- End the post with this exact link: {url}\n"
            "- Conversational, peer tone; a few relevant hashtags are fine."
        )
    return head + (
        "Constraints:\n"
        "- This is an Instagram caption. Captions CANNOT contain a clickable link, so DO NOT "
        "paste any URL. Instead end with a short, natural call to action telling readers the "
        "link is in the profile/bio (phrased in the target language).\n"
        "- Open with a strong one-line hook, keep it concise, then add up to ~12 relevant hashtags."
    )


def clean_text(text: str) -> str:
    text = text.strip()
    if len(text) >= 2 and text[0] in "\"'“「" and text[-1] in "\"'”」":
        text = text[1:-1].strip()
    return text


def mock_text(item: dict, lang: str, platform: str, url: Optional[str]) -> str:
    tag = f"[MOCK {platform}/{lang}] {item['id']}"
    if platform == "instagram":
        return f"{tag} — save on fixed costs in Japan. Honest comparisons. Link in bio. #Japan #savings #格安SIM"
    return f"{tag} — cut your monthly costs. {url} #Japan #savings"


def generate_text(client, model, max_tokens, site, item, lang, platform, url, mock) -> str:
    if mock:
        return mock_text(item, lang, platform, url)
    system = build_system(site)
    user = build_user(item, lang, platform, url)
    resp = client.messages.create(
        model=model, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(getattr(b, "text", "") for b in resp.content if getattr(b, "type", "") == "text")
    return clean_text(text)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate draft social posts into a local review queue.")
    p.add_argument("--content", type=Path, default=SCRIPT_DIR / "content.yaml")
    p.add_argument("--template", type=Path, default=SCRIPT_DIR / "review_template.html")
    p.add_argument("--out", type=Path, default=SCRIPT_DIR / "review.html")
    p.add_argument("--drafts-dir", type=Path, default=SCRIPT_DIR / "drafts")
    p.add_argument("--items", default="", help="comma-separated item ids to include")
    p.add_argument("--langs", default="", help="comma-separated language codes to include")
    p.add_argument("--platforms", default="", help="comma-separated: x,threads,instagram")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--max-tokens", type=int, default=DEFAULT_MAX_TOKENS)
    p.add_argument("--mock", action="store_true", help="no API calls; placeholder text (test plumbing)")
    p.add_argument("--dry-run", action="store_true", help="one item x one lang x one platform (cheap API test)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    data = load_content(args.content)
    site = data["site"]
    all_langs = site["languages"]

    items = data["items"]
    if args.items:
        want = {s.strip() for s in args.items.split(",")}
        items = [it for it in items if it["id"] in want]
    langs = [s.strip() for s in args.langs.split(",")] if args.langs else list(all_langs)
    platforms = [s.strip() for s in args.platforms.split(",")] if args.platforms else list(ALL_PLATFORMS)

    bad_langs = set(langs) - set(all_langs)
    if bad_langs:
        sys.exit(f"ERROR: unknown langs {bad_langs}; known: {all_langs}")
    bad_plats = set(platforms) - set(ALL_PLATFORMS)
    if bad_plats:
        sys.exit(f"ERROR: unknown platforms {bad_plats}; known: {ALL_PLATFORMS}")

    if args.dry_run:
        items, langs, platforms = items[:1], langs[:1], platforms[:1]

    client = None
    if not args.mock:
        try:
            from anthropic import Anthropic
        except ImportError:
            sys.exit("ERROR: anthropic not installed. Run: .venv/bin/pip install -r social/requirements.txt")
        import os
        if not os.environ.get("ANTHROPIC_API_KEY"):
            sys.exit("ERROR: ANTHROPIC_API_KEY not set. `export ANTHROPIC_API_KEY=...` or use --mock.")
        client = Anthropic()

    run_label = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = args.drafts_dir / run_label
    run_dir.mkdir(parents=True, exist_ok=True)

    groups: Dict[str, dict] = {}
    ordered_ids: List[str] = []
    total = 0
    over_count = 0

    for item in items:
        item_langs = all_langs if item.get("languages", "all") == "all" else item["languages"]
        for lang in langs:
            if lang not in item_langs:
                continue
            cfg_url = resolve_url(item, lang, site["base_url"])
            for platform in platforms:
                cfg = PLATFORMS[platform]
                url = cfg_url if cfg["include_link"] else None
                warn = None
                try:
                    text = generate_text(client, args.model, args.max_tokens,
                                         site, item, lang, platform, url, args.mock)
                except Exception as e:  # noqa: BLE001 — keep prior (paid) drafts; flag this one
                    text = ""
                    warn = f"Generation failed: {e}"
                    print(f"  ! {item['id']}/{platform}/{lang}: {e}", file=sys.stderr)

                count = effective_length(text, platform, url)
                over = count > cfg["limit"]

                if not warn and cfg["include_link"] and url and url not in text:
                    text = f"{text}\n{url}".strip()
                    count = effective_length(text, platform, url)
                    over = count > cfg["limit"]
                    warn = "Model omitted the link; appended automatically — re-check length."
                over_count += 1 if over else 0
                total += 1

                image_src = item["image"].format(lang=lang) if cfg["needs_image"] and item.get("image") else None
                uid = re.sub(r"[^a-zA-Z0-9]+", "-", f"{item['id']}-{platform}-{lang}")
                d = Draft(
                    item_id=item["id"], platform=platform,
                    lang=lang, text=text, url=cfg_url, image_src=image_src,
                    char_limit=cfg["limit"], effective_count=count, over_limit=over,
                    needs_image=cfg["needs_image"], warn=warn, uid=uid,
                    image_rel=("../" + image_src) if image_src else None,
                )
                (run_dir / f"{platform}-{lang}-{item['id']}.txt").write_text(text, encoding="utf-8")

                if item["id"] not in groups:
                    groups[item["id"]] = {"id": item["id"], "type": item.get("type", ""), "drafts": []}
                    ordered_ids.append(item["id"])
                groups[item["id"]]["drafts"].append(d)

    # Render the review page. autoescape=True so model-generated text can't break out
    # of the markup (e.g. a stray </textarea> or <script> in a draft).
    try:
        template = Template(args.template.read_text(encoding="utf-8"), autoescape=True)
    except OSError as e:
        sys.exit(f"ERROR: cannot read template {args.template}: {e}")
    view_items = [groups[i] for i in ordered_ids]
    html = template.render(
        generated_at=run_label, total=total, over_count=over_count,
        model=("mock" if args.mock else args.model), mock=args.mock, items=view_items,
    )
    try:
        args.out.write_text(html, encoding="utf-8")
    except OSError as e:
        sys.exit(f"ERROR: cannot write review page {args.out}: {e}")

    print(f"Generated {total} drafts across {len(view_items)} items "
          f"({len(langs)} langs x {len(platforms)} platforms).")
    print(f"  Drafts:  {run_dir}")
    print(f"  Review:  {args.out}   ← open this in a browser")
    if over_count:
        print(f"  WARNING: {over_count} draft(s) exceed the platform limit (flagged red in review.html).")


if __name__ == "__main__":
    main()
