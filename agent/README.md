# FreeBee — runtime agent kit

This folder is the **"worker bee"**: the browser agent that completes a receipt survey
and collects the reward. It's standalone — the dashboard (built in Cursor) just needs to
shell out to `freebee_agent.py` and embed / mirror the browser.

## Files
- **`survey_clone.html`** — a self-hosted survey that looks like a real receipt survey but
  **accepts any code, has no captcha, and can never fail.** This is your **guaranteed live
  money-shot.** Rehearse against this infinitely, for free.
- **`freebee_agent.py`** — browser-use agent. Windows event-loop fix baked in + the
  **top-box** system prompt (answer every question with the most positive option → fast
  AND skips the "what went wrong?" follow-up pages).
- **`../demo/seed-receipts.json`** — parsed receipt JSON (McDonald's + CVS) = hard-coded
  fallback so the UI demo runs even if live vision parsing misfires.
- **`../demo/*-sample-receipt.txt`** — synthetic receipts to test the vision parser.

## Run it in 3 commands (Windows PowerShell, from repo root)
```powershell
pip install browser-use ; python -m playwright install chromium
$env:OPENAI_API_KEY = "sk-..."                      # sponsor-aligned (or ANTHROPIC_API_KEY)
python -m http.server 8000 --directory agent        # serve the clone
# second terminal:
python agent/freebee_agent.py --url http://localhost:8000/survey_clone.html --code 04289055172704311962883043
```
A visible Chrome window opens → mirror it to the projector.

## The demo layering (memorize this)
```
LIVE money-shot   → agent runs survey_clone.html  (always works, ~15s, reward reveal ticks the counter)
"it's real" proof → agent runs mcdvoice.com       (recorded rehearsal, OR one RESERVED fresh code live)
ultimate fallback → pre-recorded video            (cued, identical narration)
```
The `$ recovered` counter animation lives in the dashboard and is **client-side** — it
looks perfect no matter which layer fires. `survey_clone.html` `postMessage`s a
`freebee:reward` event to the parent window when the reward reveals, so an embedding
iframe can tick the counter automatically.

## Best REAL survey targets (verified, NYC-Flatiron, login-free, instant reward)
| Merchant | URL | Reward | Why | Watch out |
|---|---|---|---|---|
| **McDonald's** | mcdvoice.com | FREE fries / QP (instant code) | self-contained 26-digit code (no store#/time match), NYC-dense, no captcha | 26 digits = OCR care; code valid 7 days |
| **Subway** | subwaylistens.com | FREE cookie (instant code) | **shortest** (~4-6 Qs), no captcha, a Subway on every block | small reward |
| **Burger King** | mybkexperience.com | FREE Whopper (instant code) | marquee reward, no captcha | wants store#+date+time; 48h window |
| **Home Depot** (big number) | homedepot.com/survey | **$5,000** sweepstakes entry | biggest counter number, single ID+password | 40 W 23rd St; no instant reward |
| **Target** | informtarget.com | $1,500 sweepstakes | simple 2-code entry, near Flatiron | no instant reward |

## ⚠️ Non-negotiable discipline
1. **Survey codes are ONE-TIME-USE and expire in days.** Every real rehearsal run burns a
   code. Grab **10–15 fresh McDonald's/Subway receipts** on demo day; **physically set
   aside 2–3 you've NEVER submitted** for the stage. The #1 way this demo dies is running a
   code you already used in testing → "already used."
2. **Invisible reCAPTCHA v3** (no checkbox — it silently scores you) can soft-block a fast
   agent on shared wifi. Another reason the **clone carries the live run** and the real site
   is recorded/verified proof.
3. **Never let the crowd watch all 15 questions** on a real survey (dead air). Clone for
   live; for the real-site proof, play a recorded clip or cut away and back to the reveal.
4. **Verify morning-of** that mcdvoice.com still shows no captcha on the code-entry page.

> `survey_clone.html` is a clearly-labeled demo page (generic "Guest Experience Survey"),
> not an impersonation of any real merchant — keep it that way.
