# Decision 010: Social post system — AI drafts, manual posting

**Date**: 2026-07-19
**Status**: Implemented (draft-generation MVP); auto-posting deferred to Phase 2

## Context
Last item on the SEO/analytics track (after GA4 + Search Console, decision 009): a system
to promote the site on social media and drive traffic. Constraints: static site (no
backend), solo operator, ~¥10K/yr budget, 7 languages.

## Key finding that shaped the design (platform API economics, July 2026)
- **X**: no free tier; pay-per-use **$0.20 per post containing a link**. Our posts are all
  affiliate links → automated X posting alone would blow the annual budget. Manual = free.
- **Threads**: API free (250 posts/day) but requires Meta App Review (~2–4 wks) + OAuth upkeep.
- **Instagram**: API free but requires a Business account + FB Page + App Review + an image
  every post (JPEG), 25/day cap.
- **Drafting with Claude + a local run**: effectively free (pennies/run).

## Decision
Build a **draft-only** generator; **post manually**. This is $0 platform cost, works for X,
needs no app review, and fits the budget. User choices: platforms = X + Threads + Instagram;
languages = all 7.

**Generation engine (updated 2026-07-20):** the user has only a Claude Code subscription
(no separate Anthropic API key), so the **no-key path is the default**: Claude Code writes
the post text into `social/batch.yaml`, and `generate.py --from-drafts` renders the review
page with zero API calls. The API-key path (`generate.py` calling Claude directly) still
works for anyone who sets `ANTHROPIC_API_KEY`. `make_draft()` is shared by both paths, so
link resolution / char-limit checks / HTML are identical regardless of engine.

## What was built (`social/`)
- `content.yaml` — single source of truth: ~6 promotable items (SIM savings, fixed-cost
  overview, Rakuten campaign, Rakuten registration, credit cards, evergreen tip). The model
  may use ONLY each item's `facts` — instructed to never invent prices/points/dates.
- `generate.py` — loads content, resolves a real (non-stub) link per language with
  `link_lang_fallback` (zh-cn→zh-tw for /sim/; non-JA→JA for the JA-only /credit-cards/),
  calls Claude per (item × lang × platform), enforces platform char limits
  (**X counts CJK as 2 and links as 23**; Threads 500; IG 2200, no link → "link in bio"),
  and writes a review queue. `--mock` (no API) and `--dry-run` (one API call) modes.
- `review_template.html` — the approve UI: per-draft card, char count (red if over),
  target link, Copy button, IG image thumbnail. Opened locally; `noindex`, never published.
- `requirements.txt`, `README.md` (runbook). Generated `drafts/` + `review.html` are gitignored.

## Verification
`--mock` produced 126 drafts (6×7×3). Link resolution verified (zh-cn→zh-tw, credit-cards→ja,
native pages native); all resolved URLs return HTTP 200. CJK weighting unit-checked
(120 JA + link = 264 ≤ 280; 140 JA = 304 flagged over). Not yet run against the live API
(needs the user's `ANTHROPIC_API_KEY`).

## Not done (Phase 2 / follow-ups)
- Optional **Threads auto-post** (free API) after Meta App Review — the only economical
  auto-post path; X auto-post stays off (link cost), IG only if desired.
- Proper 1080×1080 Instagram images (extend the OG generator; currently reuses 1200×630 OG cards).
- `workflow_dispatch` GitHub Action wrapper for cloud runs.
- LINE Official Account as a future channel.
