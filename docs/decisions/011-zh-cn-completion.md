# Decision 011: Complete Simplified Chinese (zh-cn) + no-input TODO sweep

**Date**: 2026-11-14
**Status**: Implemented

## Context
zh-cn had only guides/about/privacy. Its guide nav already linked to `zh-cn/index.html`,
`zh-cn/sim/` and `zh-cn/credit-cards/` → those were live 404s. No page offered a 简中 button
except the zh-cn pages themselves.

## Decision
Generate zh-cn homepage + SIM page from zh-tw rather than translating from scratch:
1. OpenCC `tw2sp` (Taiwan → mainland, with phrase conversion), installed in `.venv`.
2. Vocabulary pass aligned with existing zh-cn guides: 方案→套餐, 申办→申请, 点数→积分,
   回馈→返现, 电信业者→运营商, 收讯→信号, 帐户→账户, 行销→营销, 仿真→模拟 (OpenCC mis-maps 模擬),
   计算机→计算器. Lines containing kana are skipped so Japanese text is untouched.
3. `zh-cn/credit-cards/` = same noindex redirect stub as other languages.
4. Added `hreflang="zh-cn"` + 简中 button (after 繁中) to all home/SIM pages; sitemap gets
   `zh-Hans` alternates and the two new URLs.

Some Taiwan-flavoured words remain (品质, 门市, 弹性) — understandable to mainland readers;
a native-speaker pass would polish it.

## Same sweep (items needing no owner input)
- Registration guide password rule → 8+ chars incl. uppercase + special char (7 langs; JA said 6+).
- Guide cards section added to zh-tw / zh-cn / vi / my / th homepages (EN pattern).
- "Also available in … (coming soon)" notices on en/zh-tw homepages listed live languages as
  coming soon → replaced with links to all 7.
- JA `sim/` and `credit-cards/` favicon paths were broken (`favicon.png` → `../favicon.png`).
- vi nav labels lacked diacritics (Huong dan → Hướng dẫn, etc.).
- `assets/qr-japanmobilesim.png` committed (was untracked since decision 005).
