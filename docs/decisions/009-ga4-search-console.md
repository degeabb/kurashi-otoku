# Decision 009: GA4 analytics + Google Search Console live

**Date**: 2026-07-19
**Status**: Implemented & deployed

## Context
Decision 008 laid the technical-SEO foundation but left two items blocked on the
user: GA4 (needed a Measurement ID) and Search Console (needed the user to verify
the domain). Both are now done.

## GA4 (Google Analytics 4)
- Measurement ID: **`G-Z2WT21RFVT`** (property reused an existing empty GA account;
  data stream created for `https://japanmobilesim.com`).
- Standard `gtag.js` snippet installed on **all 41 real pages**, inserted right after
  `<meta charset="UTF-8">` in `<head>` (Google's recommended high placement).
- The 5 `credit-cards` meta-refresh redirect stubs were **excluded** — they `noindex`
  and redirect before the tag can fire. Install script auto-detected them via
  `http-equiv="refresh"` (idempotent; skips files already containing the ID).
- Commit `49f19a9`; verified live via curl on homepage + `/en/`, `/zh-tw/sim/`,
  `/th/guides/referral/` after the Pages rebuild.
- Privacy policy already references Google Analytics, so no policy change needed.

## Google Search Console
- Property type: **URL prefix** (`https://japanmobilesim.com`), chosen over Domain to
  avoid a DNS TXT edit.
- **Auto-verified** via Google Analytics (same Google account owns the live GA tag) —
  no manual verification step was shown; SC reported "你是已驗證擁有者".
- `sitemap.xml` submitted (robots.txt already advertised it).

## Notes / follow-ups
- GA reporting data lags 24–48h; use **Realtime** for instant confirmation.
- Search Console may show "Couldn't fetch" on the sitemap briefly; clears within ~a day.
- Remaining SEO/analytics item: **social promo + AI post system** (X/Threads/IG,
  draft→approve) — not started, scoped separately.
- Optional hardening later: consent mode / cookie banner if targeting stricter privacy
  regimes; a Domain-level SC property if www/subdomain coverage is ever needed.
