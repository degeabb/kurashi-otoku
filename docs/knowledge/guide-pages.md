# Guide Pages

## Rakuten Account Registration Guide
- **Path**: `[lang]/guides/rakuten-registration/index.html`
- **Languages**: JA, EN, zh-tw, zh-cn, vi, my, th (7 total)
- **Screenshots**: stored in `assets/guides/`

### EN screenshots (used by all non-JA pages)
| File | Step |
|------|------|
| `create_new_acc_EN.jpg` | Login page → "Create a new Rakuten account" button |
| `email_input_EN.jpg` | Email input + send verification code |
| `input_verification_code_EN.jpg` | Verification code page (empty) |
| `input_verification_code_2_EN.jpg` | Verification code page (filled with code) |
| `pw_and_names_EN.jpg` | Username, password, name fields |
| `confirm_page_EN.jpg` | Confirmation page → "Complete registration" |

### JA screenshots (used by JA page only)
| File | Step |
|------|------|
| `rakuten-reg-login-ja.jpg` | ログイン画面 → 楽天会員登録(無料) |
| `rakuten-reg-email-ja.jpg` | メールアドレス入力 → 認証コード送信 |
| `rakuten-reg-verify-ja.jpg` | 認証コード入力画面 |
| `rakuten-reg-verify-email-ja.jpg` | 認証コードメール |
| `rakuten-reg-password-ja.jpg` | ユーザー名・パスワード入力 |
| `rakuten-reg-name-ja.jpg` | 氏名入力・ニュースレター・確認ボタン |

### Actual Registration Flow (verified April 2026)
1. Go to Rakuten login page → click "Create a new Rakuten account (free)"
2. Enter email → send verification code
3. Enter 6-digit verification code (valid 10 min)
4. Set username, password (8+ chars, uppercase + special), first/last name
5. Confirm information → complete registration

### Password requirement
- Fixed 2026-11-14 (decisions/011): all languages now state **8+ characters with uppercase and special characters**

## Employee Referral Guide
- **Path**: `[lang]/guides/referral/index.html`
- **Languages**: JA, EN, zh-tw, zh-cn, vi, my, th (7 total)
- **Audience**: the general public applying via the site owner's employee referral link (r10.to/hUMVON) — NOT employees
- **Structure** (rewritten 2026-11-17): 14,000/13,000 cards → conditions → 8 steps (login, password, member info,
  plan, phone number/MNP, identity check, delivery/payment/options, activation + Rakuten Link call) → FAQ → CTA
- **Screenshots**: `assets/guides/referee-*.webp` (personal data masked, watermarked). Sources + clean originals live in
  `guide_screenshots/` which is gitignored (local only, not published) since 2026-11-17. Re-run the watermark when replacing images.
- **Generator**: body built from per-language string tables (zh-cn = OpenCC tw2sp of zh-tw + vocab fixes, Japanese UI labels protected)

### Known Inaccuracies (not yet fixed)
The referral guide has factual issues identified via web research:
1. It's specifically a **Rakuten Group employee referral** — only Rakuten employees can be referrers (guide is too generic)
2. Point amounts (official, applications from 2026-09-17): Referee 14,000pts (MNP) or 13,000pts (new line); Rakuten Turbo 7,000pts. (2025-09-01 → 2026-09-16 new line was 11,000.) Granted over 3 months from the 4th month after referral login; 期間限定, 6-month validity
3. Points distributed over **months 4-6** (guide says 1-2 months)
4. Referee must make a **10+ second call via Rakuten Link app** (not mentioned)
5. Points are "limited-time points" with 6-month expiry

## CSS Components for Guides
Added to `style.css`:
- `.guide-intro` — hero section
- `.guide-step` + `.step-number` + `.step-body` — numbered step cards
- `.step-img` / `.step-img-placeholder` — screenshot containers
- `.guide-tip` (green) / `.guide-warning` (orange) — callout boxes
- `.guide-cta` — call-to-action section
- Mobile: `.guide-step { flex-direction: column; }`
