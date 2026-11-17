# Open TODOs

## SEO / Analytics (2026-07-04 — see decisions/008)
- [x] Fix broken Pages deploy (added `.nojekyll`; Jekyll build was erroring silently)
- [x] Complete hreflang across all languages + x-default
- [x] noindex on credit-cards redirect stubs
- [x] Per-language OG share images + twitter cards (all 41 pages)
- [x] JSON-LD: Organization/WebSite/BreadcrumbList/Article
- [x] **GA4** — installed site-wide (`G-Z2WT21RFVT`) on all 41 real pages 2026-07-19;
      gtag.js placed after `<meta charset>`, redirect stubs excluded
      (privacy policy already references Google Analytics)
- [x] **Google Search Console** — URL-prefix property auto-verified via Google Analytics
      + sitemap.xml submitted 2026-07-19 (see decisions/009)
- [x] **Social promo + AI post system** — draft-generation MVP built 2026-07-19 in `social/`
      (X/Threads/Instagram, 7 langs, draft→manual-post; see decisions/010). Needs user's
      `ANTHROPIC_API_KEY` to run for real.
  - [ ] Phase 2: optional Threads auto-post (free API) after Meta App Review
  - [ ] Proper 1080×1080 Instagram images (currently reuses 1200×630 OG cards)
- [ ] Regenerate OG images if branding/taglines change (gen script: scratchpad/make_og.py)

## High Priority
- [x] Fix referral guide inaccuracies — done 2026-06-22 (see decisions/006, 007)
  - [x] Re-contract eligibility for previously-cancelled users (decisions/006)
  - [x] Point distribution timeline → months 4-6 (decisions/007)
  - [x] Rakuten Link 10-sec call requirement added (decisions/007)
  - [ ] Point amounts 7,000/14,000/11,000 are in the banner IMAGE (rakuten-campaign-banner.avif); verified current but require image regen to change
  - [x] Clarify it's Rakuten Group employee referral; only referrer must be an employee, referee can be anyone (2026-06-22)
- [x] Make application entry obvious — banner CTA + floating side banner (decisions/006)
- [ ] Add real screenshots to referral guide (all languages still have placeholders)
- [x] Fix password requirement in registration guide — done 2026-11-14, all 7 langs (decisions/011)

## Medium Priority
- [x] Complete zh-cn language (homepage, SIM page, credit cards redirect) — done 2026-11-14 via OpenCC from zh-tw (decisions/011)
  - [ ] Optional: native-speaker polish of zh-cn home/SIM wording
- [x] Add 简中 button to lang-switcher + zh-cn hreflang on all home/SIM pages (2026-11-14)
- [ ] **vi referral guide body has no Vietnamese diacritics** (whole page, e.g. "Huong dan tung buoc") — needs re-translation
- [ ] Sitemap lacks privacy/about pages (all langs)
- [ ] Burmese (my) guide-card copy on homepage written 2026-11-14 — have a native speaker check
- [x] **Cloudflare Email Routing** — done 2026-11-17: contact@japanmobilesim.com → owner's Gmail (rule Active; MX route1-3.mx.cloudflare.net + SPF verified). Catch-all disabled (drop).
  - [ ] Optional: "Send mail as" contact@ from Gmail (needs SMTP relay) so replies don't expose personal address
- [ ] Verify au/SoftBank prices periodically (IIJmio 5GB ¥950 confirmed correct by user 2026-06-22)
  - 2026-11-14 web check → updated SIM pages (7 langs): docomo MAX ¥7,315→¥8,448, au MAX+ ¥7,238→¥7,788,
    Rakuten shown at regular price ¥1,078~/¥3,278 (family-discount ¥3,168 noted), ahamo shown at new
    Dec 1 2026 tiers (40GB ¥3,135 / 60GB ¥4,125 / 120GB ¥5,115) with "¥2,970 until Nov 30" note
  - [ ] After 2026-12-01: drop the ahamo "until Nov 30" note
  - [ ] Not yet re-checked: mineo, UQ mobile, SoftBank "PayToku Unlimited ¥9,625" con
- [ ] **Referral new-line points**: site/banner say 11,000; Nov 2026 sources say 12,000–13,000 — confirm on official Rakuten page, then regen banner + text
- [ ] Bump "情報は2026年3月時点" disclaimers to current once speed-ranking data is re-measured
- [ ] Verify guide accuracy periodically (Rakuten may change their registration flow)

## Low Priority
- [ ] Embed QR code somewhere on the site (currently just a generated asset)
- [x] Add guide cards section to non-JA/EN homepages — done 2026-11-14
- [ ] Consider adding more guide topics (e.g., Rakuten Card application, MNP transfer)
