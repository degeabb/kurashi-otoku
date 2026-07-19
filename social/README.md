# Social post generator

Generates **draft** social media posts (X / Threads / Instagram) in all 7 site
languages from a single content file, into a local review queue you approve and post
**by hand**. Nothing is posted automatically — there is no platform API integration.

**Why draft-only?** (July 2026) X charges **$0.20 per link-containing post** via API →
over the ~¥10K/yr budget. Manual posting is free on every platform. Threads/Instagram
auto-posting would also need Meta App Review. So the system does the expensive part
(writing good copy in 7 languages) and leaves the free part (posting) to you.
See `docs/decisions/010-social-post-system.md`.

## Setup (one time)

1. **Anthropic API key** (separate from the Claude Code subscription — pay-as-you-go,
   ~pennies per full run). Get one at <https://console.anthropic.com>, then:
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-...
   ```
   (add it to your `~/.zshrc` to persist).
2. **Install deps** into the repo's `.venv`:
   ```bash
   .venv/bin/pip install -r social/requirements.txt
   ```

## Usage

Run from the repo root:

```bash
# Offline plumbing test — no API key, placeholder text:
.venv/bin/python social/generate.py --mock

# Cheap real test — ONE draft via the API:
.venv/bin/python social/generate.py --dry-run

# Full run — every item x 7 langs x 3 platforms:
.venv/bin/python social/generate.py

# Filtered runs:
.venv/bin/python social/generate.py --items sim-savings,rakuten-campaign
.venv/bin/python social/generate.py --langs ja,en --platforms x,threads
.venv/bin/python social/generate.py --model claude-haiku-4-5-20251001   # cheaper
```

Output:
- `social/review.html` — **open this in a browser.** One card per draft with a live
  character count (red if over the limit), the target link, a Copy button, and (for
  Instagram) the image to attach.
- `social/drafts/<timestamp>/` — the same drafts as plain `.txt` files.

Both are git-ignored (regenerated each run).

## Approve → post workflow

1. Run the generator, open `social/review.html`.
2. Read each draft. Edit inline in the textarea if you want to tweak wording.
3. Click **Copy**, switch to the app, paste, and post.
4. **Instagram**: captions can't hold a clickable link — the draft ends with a
   "link in bio" CTA, so set your profile link to the site (or the specific page).
   Attach the image shown on the card (currently the 1200×630 OG card — crop to
   square in-app; proper 1080×1080 images are a planned follow-up).

## Editing what gets promoted

Everything lives in **`social/content.yaml`**. Each item's `facts:` field is the ONLY
source the model may use — it is instructed never to invent prices, percentages, point
amounts, or dates. So:

- **Keep `facts` accurate.** Verify prices/campaign terms before a run (the site has a
  price-audit history — see `docs/decisions/007`).
- Items marked `verify_before_posting: true` (e.g. the Rakuten campaign) change often —
  re-check the live guide first.
- `link_lang_fallback` repoints the *link* (not the post language) when a page doesn't
  exist for a language — e.g. zh-cn has no `/sim/` page (→ zh-tw), and `/credit-cards/`
  is JA-only (→ ja). The generator also auto-detects redirect stubs and falls back to ja.

## Character limits enforced

| Platform  | Limit | Notes |
|-----------|-------|-------|
| X         | 280   | CJK (JA/ZH/KR) chars count **2** each; links count 23. So JA posts fit ~110 chars of text. |
| Threads   | 500   | plain character count |
| Instagram | 2200  | caption; no clickable link (use "link in bio") |

Over-limit drafts are flagged red in `review.html` and never silently truncated.

## Not included (future phases)

- Auto-posting to **Threads** (free API) after Meta App Review — the only economical
  auto-post option.
- Proper 1080×1080 Instagram images (extend the OG image generator).
- A `workflow_dispatch` GitHub Action to run this in the cloud.
- LINE Official Account as a channel.
