# Decision 001: Add Guide Pages

**Date**: 2026-04-05
**Status**: Implemented

## Context
The site needed tutorial-style content to help users register for Rakuten services and understand the employee referral program.

## Decision
Created two guide page types with a new step-by-step CSS component system:
1. **Rakuten Account Registration** — with real screenshots (EN + JA versions)
2. **Employee Referral Program** — with placeholder screenshots

## Details
- 14 guide pages total (7 languages × 2 guides)
- JA page uses Japanese-language screenshots; all other languages use EN screenshots
- Guide-specific CSS components added to shared `style.css`
- Added "Guides" nav link to all existing pages
- Added guide cards section to JA and EN homepages
- Updated `sitemap.xml` with all 14 new URLs

## Trade-offs
- Each language is a full HTML file (no templating) — consistent with existing site pattern but means 14 files to maintain
- Referral guide still has placeholder screenshots — needs real screenshots from user
- Referral guide has factual inaccuracies identified via web research (see docs/knowledge/guide-pages.md) — not yet fixed
