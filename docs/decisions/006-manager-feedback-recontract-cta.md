# Decision 006: Manager Feedback — Re-contract Eligibility & Banner CTA

**Date**: 2026-06-22
**Status**: Implemented
**Source**: Manager feedback (remote-control)

## Feedback
1. **Re-contract points**: Even users who previously cancelled Rakuten Mobile receive
   points when they re-contract — a perk specific to the employee referral program.
   The guide previously stated only "new subscribers" qualify (contradiction).
2. **Unclear entry point**: The campaign banner image links to the application
   (`r10.to/hUMVON` → Rakuten ID linkage screen), but nothing told users the image
   is clickable. Some users perceived the jump as accidental and stopped.

## Changes
### 1. Re-contract eligibility (7 referral guides)
`[lang]/guides/referral/index.html` for ja, en, zh-tw, zh-cn, vi, my, th:
- Softened the overview eligibility bullet — re-contract of previously-cancelled users
  now explicitly included.
- Reworded the "existing user" FAQ answer to mean *currently active* users (removes the
  contradiction).
- Added a new FAQ item: "Can someone who previously cancelled still qualify?" → Yes,
  framed as an employee-referral perk. FAQ items per guide: 4 → 5.

### 2. Banner CTA label (12 pages)
`index.html` and `sim/index.html` for ja, en, zh-tw, vi, my, th:
- Added a pink CTA bar directly under the campaign banner image, inside the existing
  `<a>` link, e.g. JA: "▶ タップして申し込む（楽天モバイル公式）".
- Per-language labels. Note: `my` = Burmese (Myanmar), not Malay.

## Notes
- This is a partial pass on the referral-guide accuracy items in
  `docs/knowledge/open-todos.md`. Point amounts (7,000/14,000/11,000), distribution
  timeline (months 4–6), and the Rakuten Link 10-sec call requirement are still pending.
