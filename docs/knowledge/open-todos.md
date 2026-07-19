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
- [ ] **Google Search Console** — verify domain + submit sitemap.xml (user action;
      GA tag now live → verify via "Google Analytics" method)
- [ ] **Social promo + AI post system** — X / Threads / Instagram, draft→approve model
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
- [ ] Fix password requirement in registration guide (should be 8+ chars with uppercase + special)

## Medium Priority
- [ ] Complete zh-cn language (homepage, SIM page, credit cards redirect) — privacy/about pages now exist (decisions/007)
- [ ] Add 简中 button to lang-switcher on all non-guide pages
- [ ] **Set up Cloudflare Email Routing** for contact@japanmobilesim.com → forward to personal Gmail (user action; pages already reference this address)
- [ ] Verify au/SoftBank prices periodically (IIJmio 5GB ¥950 confirmed correct by user 2026-06-22)
- [ ] Bump "情報は2026年3月時点" disclaimers to current once speed-ranking data is re-measured
- [ ] Verify guide accuracy periodically (Rakuten may change their registration flow)

## Low Priority
- [ ] Embed QR code somewhere on the site (currently just a generated asset)
- [ ] Add guide cards section to non-JA/EN homepages (currently only JA and EN have them)
- [ ] Consider adding more guide topics (e.g., Rakuten Card application, MNP transfer)
