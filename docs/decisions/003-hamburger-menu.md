# Decision 003: Add Hamburger Menu for Mobile

**Date**: 2026-04-05
**Status**: Implemented

## Context
Desktop nav links (`Home | SIM Comparison | Credit Cards | Guides`) were hidden on mobile via `display: none` with no replacement. Users on iPhone/Android Chrome couldn't see or access navigation.

## Decision
Added a hamburger menu (☰) that appears on screens ≤ 750px. Tapping it opens a full-screen overlay with all nav links and language switcher buttons.

## Implementation
- Pure CSS + inline JS (no library)
- Hamburger animates to X on open
- Added to all 27 non-redirect HTML pages
- Each page's mobile nav mirrors its desktop nav exactly (same links, active states, lang buttons)

## Alternatives Considered
- **Leave as-is** (rely on footer/in-page links) — rejected because Guides page was undiscoverable on mobile
- **Bottom tab bar** — not chosen, hamburger is simpler and more standard
