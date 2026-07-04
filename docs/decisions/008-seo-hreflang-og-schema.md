# Decision 008: SEO Foundation — hreflang, OG images, JSON-LD + Jekyll fix

**Date**: 2026-07-04
**Status**: Implemented & deployed

## Context
Site had no analytics ("access numbers" unknown) and only partial SEO. Goal: fix the
technical-SEO foundation before investing in social promotion. Audit found real gaps.

## Critical infra fix — Pages build was silently broken
GitHub Pages served the site via the **legacy Jekyll** engine (no `.nojekyll`). The
Jekyll build **errored** on the first SEO commit and every push since would have
silently failed to deploy — the live site was frozen at the June commit (`4a813e9`).
**Fix:** added `.nojekyll` so Pages serves the static files as-is (faster, deterministic).
Builds now succeed in ~30s. **Lesson: verify the live URL after every push, not just
that `git push` succeeded.**

## SEO changes (all 41 real pages)
1. **hreflang** — replaced incomplete `ja`+`en` alternates with the full language set
   (6 for home/SIM, 7 for guides/privacy/about) + `x-default`→en. zh-tw/zh-cn/vi/my/th
   were previously invisible to each other in search.
2. **Redirect stubs** — the 5 non-JA `credit-cards` meta-refresh pages got
   `noindex,follow` + canonical→JA (stop indexing thin duplicates).
3. **OG images** — generated 7 branded 1200×630 cards (`assets/og-*.png`, PIL); added
   `og:image`/width/height/alt + `twitter:image` (+ `twitter:card` where missing).
   Previously **zero** share-preview images → blank cards on X/Threads/LINE.
4. **JSON-LD** — Organization + WebSite on homepages; BreadcrumbList on every sub-page;
   Article (with git-derived datePublished/Modified) on guides. Existing FAQPage on SIM
   pages preserved.

## Not done (needs user action / follow-up)
- **GA4** — privacy policy already references Google Analytics, but no snippet is
  installed. Needs the `G-…` Measurement ID from the user, then wire site-wide.
- **Search Console** — needs user to verify domain + submit sitemap.
- **og:image regen** if branding/taglines change (generator at scratchpad `make_og.py`).

## Follow-ups
See open-todos: GA4 + Search Console; social promotion + AI post system (X/Threads/IG,
draft→approve model).
