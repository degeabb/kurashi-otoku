# Decision 007: June 2026 Price/Info Audit + Legal Pages

**Date**: 2026-06-22
**Status**: Implemented

## Context
User asked to web-verify that the site's numbers were still current (site disclaimer
said "as of March 2026"). Verified all figures against official carrier/campaign sources.

## Verification outcome
**Current & correct:** Rakuten employee-referral points (MNP 14,000 / new 11,000 /
referrer 7,000, "増量中"); re-contract eligibility (出戻りOK); ahamo (¥2,970 / ¥4,950);
LINEMO (¥990 / ¥2,970); mineo (3GB ¥1,298 / 7GB ¥1,518 — already updated); povo
(¥0 / ¥330 24h); au 使い放題MAX＋ ¥7,238.

**Was outdated → fixed:**
- Referral payout timing 1-2 months → **months 4-6** (in installments); added the
  **Rakuten Link 10-sec call** requirement (since 2026-03-02). All 7 referral guides.
- **UQ**: discontinued ミニミニ/コミコミ → **コミコミプランバリュー 35GB ¥3,828** +
  **トクトクプラン2 ¥4,048〜** (min ¥2,948). Old plans closed 2025-06-02.
- **docomo**: eximo/irumo → ドコモMAX/mini; fixed mini entry ¥1,628 → **¥2,750**.
- **SoftBank**: メリハリ無制限＋ closed 2026-06-01 → **テイガク無制限 / ペイトク2 ¥10,538**
  (base; +¥550 hike from 2026-07-01).
- **Rakuten** card: noted ¥3,168 is the 最強家族割 price (standard ¥3,278).

**Unresolved / flagged:** IIJmio 5GB shows ¥950 (official ¥990 — couldn't load table);
"March 2026" disclaimer left as-is (speed-ranking data not re-measured); banner image
numbers baked into rakuten-campaign-banner.avif.

## Legal pages
Added `/privacy/` (Privacy Policy) and `/about/` (運営者情報) in 7 languages
(ja, en, zh-tw, zh-cn, vi, my, th). zh-cn uses minimal chrome (no homepage yet).
- Operator handle: 暮らしお得 (ja) / Japan Mobile SIM (others); team = "編集部".
- Contact: **contact@japanmobilesim.com** (to be set up via Cloudflare Email Routing).
- Wired footer Privacy/About links on all 27 existing pages (were `href="#"`).
- Privacy covers: access logs, cookies/Google Analytics + opt-out, affiliate
  disclosure, third-party ads, disclaimer, contact.

## Follow-ups
See open-todos: set up Cloudflare email forwarding; verify IIJmio ¥950;
generic "employee referral" wording; real screenshots.
