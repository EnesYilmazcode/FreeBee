# Research: Receipt survey-for-reward programs (verified 2026-07-18)

The core FreeBee pattern: a receipt prints a **survey URL + code**; you fill a short
feedback survey; you get a **free item, coupon, or sweepstakes entry**. All login-free.

## Best targets for a LIVE demo (NYC Flatiron, login-free, instant reward)

| Merchant | Survey URL | Reward | Live safety | Notes |
|---|---|---|---|---|
| **McDonald's** | mcdvoice.com | FREE fries/QP — **instant code** | ★★★★ | 26-digit **self-contained** code (no store#/time match). Best real hero. |
| **Subway** | subwaylistens.com | FREE cookie — instant | ★★★★★ | **Shortest** survey (~4–6 Q), on every block. Most deterministic. |
| **Burger King** | mybkexperience.com | **free Whopper** — instant | ★★★★ | Wants store#+date+time; 48h window. |
| **Dunkin** | dunkinrunsonyou.com | free donut — instant | ★★★★ | 18-digit code; donut needs a paired drink. |

## Biggest counter numbers (sweepstakes entry — no instant reward)

| Merchant | URL | Prize | Notes |
|---|---|---|---|
| **Home Depot** | homedepot.com/survey | **$5,000** | Single User-ID+password. 40 W 23rd St. |
| **Best Buy** | bestbuycares.com | **$5,000** | 3-code (A/B/C) entry = more fragile. Union Sq. |
| **Target** | informtarget.com | $1,500 | Simple 2-code entry. Union Sq / 34th. |
| **CVS** | cvshealthsurvey.com | $1,000 | **Single 17-digit code = simplest.** CVS on every block. |
| **Walgreens** | walgreenslistens.com | $500 | Two fields. |
| **Whole Foods** | wfm.com/feedback | $250 | Closest store (Union Sq, ~2–3 blks) but 3-field entry. |

## Skip for LIVE runs
- **Chick-fil-A** (mycfavisit.com) — code **emailed ~24h later**, no on-screen reveal. Great "it emails you" narrative, bad live money-shot.
- **Chipotle / Taco Bell** — sweepstakes-first, no guaranteed instant free item.
- **Jack in the Box, Sonic, Walmart, Lowe's, Kroger, Costco, Dollar Tree/General** — no Manhattan location, can't get a fresh receipt. (Rite Aid = defunct, all NYC stores closed.)

## Agent execution reality (this is what makes or breaks it)
- **Top-box everything.** Tell the agent to pick the most-positive answer on every question. It's faster AND skips the conditional "what went wrong?" follow-up pages → shorter survey. (Baked into `agent/freebee_agent.py`.)
- **One-time-use + expiry.** Every real rehearsal run burns a code (McDVoice code dies on submit, expires 7 days after purchase). Grab 10–15 receipts; **physically reserve 3 unused** for the stage. #1 cause of live failure = "already used."
- **Invisible reCAPTCHA v3.** No checkbox — it silently scores mouse/keyboard cadence + IP reputation and can soft-block a fast headless agent even on "no-captcha" sites. → Run the **self-hosted clone live**, keep the real site as recorded/reserved proof.
- **Timing.** A full real survey is ~12–15 questions / 2–3 min = dead air on stage. The clone finishes in ~15s. For a real-site proof, play a recorded clip or cut away and back to the reveal.

## Receipt anatomy (for the vision parser)
Survey invite sits in the **footer** (after payment lines, before legal fine print): a CTA
("How was your visit?"), the URL, the code, the reward, and a blank "Validation Code: ___" line.
Code lengths: McD **26**, BK 16–20, Jack 14, CVS 17. Around it: store#, register#, order/txn#,
date (MM/DD/YYYY), time (AM/PM), total $ — these are the alt-entry fallback when code OCR is low-confidence.

### Extraction fields FreeBee should emit per receipt
`merchant` · `survey_url` (derive from merchant, don't trust OCR) · `survey_code` (digits only) ·
`survey_code_segments[]` · `store_number` · `register_number` · `transaction_number` · `date` (ISO) ·
`time` (24h) · `amount` · `reward_description` · `reward_value_usd` · `survey_deadline_days` ·
`captcha_expected` · `extraction_confidence`. See `demo/seed-receipts.json` for the shape.
