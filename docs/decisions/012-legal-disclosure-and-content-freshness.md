# Decision 012: Legal disclosure, PR labelling and content freshness

**Date**: 2026-11-17
**Status**: Implemented (About/Privacy affiliate wording pending owner input)

## Context
- The "Apply" link (r10.to/hUMVON) resolves to refer.rakuten.co.jp — it is the operator's
  **Rakuten employee referral link**, not an affiliate-network link. Other outbound links go to
  official carrier/card sites with no compensation.
- Old footers claimed "this site participates in affiliate programs with the carriers listed" — inaccurate.
- Japan's stealth-marketing rule (景品表示法 告示, Oct 2023) expects advertising to be identifiable
  to ordinary readers, not only in fine print.

## Decision
1. **PR line at the top** of every page carrying the referral link (home, SIM, both guides × 7 langs = 28 pages):
   states it is promotional, the operator is a Rakuten Group employee, and Apply = employee referral link.
2. **Standard legal notice** (bottom, 29 pages incl. JA credit-cards) replacing old disclaimers:
   independence/non-endorsement, employee status + referral link, no pay for other links, prices/terms
   change and official info prevails (as of Nov 2026), no guarantee (points/screening/savings),
   not financial/legal/investment advice, limitation of liability, trademarks;
   page extras: speeds (SIM), revolving credit (cards), screenshot attribution + campaign rules 2162 (guides).
3. SIM page subway claims corrected (7 langs, incl. FAQ JSON-LD): ~95% by Mar 2026, July target,
   some stations upgraded from Aug 2026, no official completion announcement found as of Nov 2026.

## Update (same day)
- Owner confirmed: they receive a referrer reward from Rakuten for sign-ups via their link, paid as
  miscellaneous income (雑所得). The reward terms are **confidential** — the site must only state that the
  operator receives a reward from Rakuten; never publish rate, duration or payment form.
- PR line, legal notice, referral-guide FAQ, About, Privacy (§3 renamed "Referral link & compensation")
  and SIM FAQ ("how rankings are decided" → explicit conflict-of-interest note) updated in 7 langs.
  The incorrect "Rakuten Affiliate / affiliate programs" claims are gone.

## Open
- (Resolved 2026-11-17) Owner confirmed Rakuten encourages posting the employee referral link on the web
  and social media (Threads, X, Instagram, etc.).
- Social posts: generator now enforces a #PR prefix on every draft (see social/README.md).
