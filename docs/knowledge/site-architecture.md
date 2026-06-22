# Site Architecture

## Overview
Multi-language personal finance & lifestyle affiliate portal for Japan (japanmobilesim.com). Hosted on GitHub Pages via repo `degeabb/kurashi-otoku`.

## Languages (8 total)
| Code | Directory | Logo | Status |
|------|-----------|------|--------|
| ja | `/` (root) | 暮らし**お得** | Full site |
| en | `/en/` | Japan**MobileSIM** | Full site |
| zh-tw | `/zh-tw/` | Japan**MobileSIM** | Full site |
| zh-cn | `/zh-cn/` | Japan**MobileSIM** | Guides only (no homepage/SIM page yet) |
| vi | `/vi/` | Japan**MobileSIM** | Full site |
| my | `/my/` | Japan**MobileSIM** | Full site |
| th | `/th/` | Japan**MobileSIM** | Full site |

## Page Types
1. **Homepage** (`index.html`) — savings calculator, NISA simulator, guide cards
2. **SIM Comparison** (`sim/index.html`) — 10 carriers ranked with pros/cons
3. **Credit Cards** (`credit-cards/index.html`) — JA only; other langs redirect to JA version
4. **Guides** (`guides/rakuten-registration/` and `guides/referral/`) — step-by-step with screenshots

## Directory Structure
```
/                          ← JA root
├── index.html
├── sim/index.html
├── credit-cards/index.html
├── guides/
│   ├── rakuten-registration/index.html
│   └── referral/index.html
├── en/                    ← same structure per language
│   ├── index.html
│   ├── sim/index.html
│   ├── credit-cards/index.html  (redirect)
│   └── guides/...
├── zh-tw/, vi/, my/, th/  ← same pattern
├── zh-cn/                 ← guides only
│   └── guides/...
├── assets/
│   ├── style.css          (shared CSS, ~480 lines)
│   ├── lang.js            (minimal, no auto-detection)
│   ├── guides/            (screenshot images)
│   ├── rakuten-campaign-banner.avif (JA)
│   ├── rakuten-campaign-banner-en.avif (non-JA)
│   └── qr-japanmobilesim.png
├── guide_screenshots/     (source files, not in site)
├── sitemap.xml
├── robots.txt
├── CNAME
└── .gitignore
```

## Tech Stack
- Pure HTML/CSS/vanilla JS (no frameworks)
- Single shared `style.css` with CSS custom properties
- Google Fonts: Noto Sans JP
- Responsive breakpoint: 750px
- Hamburger menu on mobile (all 27 non-redirect pages)

## CSS Design System
- Primary: `--pink: #FF008C` (Rakuten magenta)
- Green: `--green: #00963C` (pros)
- Orange: `--orange: #E67700` (cons)
- Components: `.btn`, `.chip`, `.tag`, `.plan-card`, `.guide-step`, `.timeline`, `.faq-item`

## Navigation
- Desktop: logo + nav-links (Home, SIM, Credit Cards, Guides) + lang-switcher
- Mobile: hamburger button → full-screen overlay with same links + lang buttons
- Language switcher buttons link to equivalent page in each language

## Affiliate Links
- Rakuten Mobile: `https://r10.to/hUMVON` (used across all pages)
