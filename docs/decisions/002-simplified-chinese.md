# Decision 002: Add Simplified Chinese (zh-cn)

**Date**: 2026-04-05
**Status**: Partial

## Context
User requested Simplified Chinese in addition to existing Traditional Chinese (zh-tw).

## Decision
Added zh-cn as a new language, starting with guide pages only.

## Current State
- `zh-cn/guides/rakuten-registration/index.html` — complete
- `zh-cn/guides/referral/index.html` — complete
- **No homepage, SIM page, or credit cards page yet**
- zh-cn not added to lang-switcher on non-guide pages (only guide pages have the 简中 button)
- zh-cn not added to sitemap hreflang groups for homepage/SIM pages

## TODO
- Create `zh-cn/index.html` (homepage)
- Create `zh-cn/sim/index.html` (SIM comparison)
- Create `zh-cn/credit-cards/index.html` (redirect to JA)
- Add 简中 button to lang-switcher on ALL pages
- Add zh-cn homepage/SIM URLs to sitemap
