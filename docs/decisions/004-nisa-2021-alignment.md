# Decision 004: Align NISA Simulator to 2021 Start Year

**Date**: 2026-04-05
**Status**: Implemented

## Context
The JA homepage NISA simulator used 2021 as start year (matching Rakuten Mobile launch). Other language pages incorrectly used 2020 (default) with a 2022 option chip.

## Decision
1. Aligned all pages to use 2021 as the single fixed start year
2. Removed year selector chip buttons entirely (was showing "From 2020" / "From 2022" on non-JA pages)
3. Updated heading to explain the context: "since Rakuten Mobile launched (4 years ago)"

## Rationale
- Rakuten Mobile launched in 2021, so 2021 is the correct starting point for the "what if you'd invested savings" simulation
- Single fixed year is cleaner than a selector with arbitrary options
- The heading now tells the story better than a bare year chip

## Note
- The credit cards page (`credit-cards/index.html`) has a separate Points→NISA simulator starting from 2022 — this was NOT changed
