# Threads auto-posting — one-time setup (~20 min)

Daily posting is done by `.github/workflows/threads-post.yml` (20:00 JST). It posts the next
**approved** entry in `social/queue.yaml` — entries arrive as a weekly pull request and are
approved by merging it. Nothing is posted that you didn't merge.

## 1. Create the Meta app (Threads API)
1. Go to <https://developers.facebook.com/apps> → **Create app** → use case **"Access the Threads API"**.
2. In the app's Threads use case → **Permissions**: add `threads_basic` and `threads_content_publish`.
3. **App roles → Roles → Add Threads Tester** → enter your Threads username.
4. In the **Threads app** on your phone: Settings → Account → Website permissions → **Invites** → accept.
   (Skipping this causes an "Insecure Login Blocked"/permission error.)
   No App Review is needed: the app only posts to *your own* tester account.

## 2. Get a long-lived token and your user id
1. Threads use case → **Settings / User Token Generator** → generate a token for your account
   (this gives a long-lived token, valid 60 days).
2. Find your Threads user id: open
   `https://graph.threads.net/v1.0/me?fields=id,username&access_token=YOUR_TOKEN` in a browser.

## 3. Add GitHub repo secrets
GitHub → repo **degeabb/kurashi-otoku** → Settings → Secrets and variables → Actions → **New repository secret**:

| Name | Value |
|---|---|
| `THREADS_ACCESS_TOKEN` | the long-lived token |
| `THREADS_USER_ID` | the numeric id from step 2 |
| `SECRETS_PAT` | a fine-grained personal access token: <https://github.com/settings/personal-access-tokens/new> → only this repo → Repository permissions → **Secrets: Read and write**. Lets the weekly job store the refreshed token. |

## 4. Test
GitHub → **Actions → Threads daily post → Run workflow** (dry run ✓) → the log shows the next post.
Then run once with dry run unticked to publish for real. After that it runs daily at 20:00 JST.

## Keeping it alive
- `threads-token-refresh.yml` refreshes the token every Monday. If a run fails (e.g. the token
  expired because the job was off for 60+ days), repeat step 2 and update `THREADS_ACCESS_TOKEN`.
- GitHub emails you when a workflow fails — that's your alert.
- Queue empty → the daily job just logs "Nothing due today". Approve the next weekly batch.

## Safety rules enforced in `post_threads.py`
One post per run · `#PR` prefixed · ≤500 chars · must link to japanmobilesim.com ·
blocks confidential referral-reward terms. Tests: `social/test_post_threads.py`.
