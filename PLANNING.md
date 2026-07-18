# FreeBee — Build Plan (Ramp Builders Cup, Jul 18 2026)

**One line:** Scan a receipt on your phone → a browser agent claims the free reward hiding on it → you get it emailed. *Free money, zero effort.*

Tracks we're aiming at: **Save Time. Save Money.** (primary) · **Audience Favorite** · **Best Use of Sponsors** (Cursor + Codex).

---

## The product, screen by screen (this is "what it looks like")

1. **Scan** — phone camera opens, snap the receipt (or "Try a sample").
2. **Found** — FreeBee shows what it read + the reward it found: *"FREE Medium Fries — $4.29."*
3. **Your info (hands-free)** — a **voice agent** asks *"What email should I send your reward to?"*, you just talk, it writes it down. For any open-ended survey question, FreeBee **makes up a nice answer** ("Great service, fast and friendly"). You type nothing.
4. **Watch the bee** — a live browser fills the survey; a **$ recovered counter** ticks up.
5. **Done** — *"Reward claimed & emailed 🎉"* + the validation code.

A **working version of all 5 screens is already in the repo** (`index.html`) — runs on a phone with no backend.

---

## Architecture

```
📱 Phone (index.html)
   │  photo / voice
   ▼
🧠 Vision LLM  ── reads merchant + survey code + amount ──►  Receipt JSON
   │                                                          (schema in demo/seed-receipts.json)
   ▼
🎙️ Voice agent ── collects email; fabricates open-response answers
   │
   ▼
🐝 Browser agent (browser-use)  ── opens the survey site, top-boxes every question, grabs the reward code
   │
   ▼
📧 Email the reward + tick the $ counter
```

---

## Tech stack (and the sponsor answer, settled)

| Layer | Use | Notes |
|---|---|---|
| **Build the app** | **Cursor + Codex** | = our "Best Use of Sponsors" story. Codex runs parallel agents on the modules; Cursor for the interactive UI. |
| **Runtime bee** | **browser-use** (local, headed) | Already working in `agent/`. `Browserbase` = optional cloud upgrade for the phone→email flow. |
| **Vision** | GPT-4o / Claude vision | one call: receipt photo → JSON. |
| **Voice intake** | **Web Speech API** (fast, free, in `index.html`) → upgrade to **OpenAI Realtime** | typed field is always the fallback. |
| **App shell** | the static `index.html`, or rebuild in Next.js in Cursor | |

**Codex/Cursor do NOT have a usable runtime browser agent** — their browsers only open your own localhost to test code they wrote (no logins). The bee is browser-use.

---

## The demo, layered so it can't fail

```
LIVE money-shot   → agent runs agent/survey_clone.html   (always works, ~15s, reward reveal)
"it's real" proof → agent runs mcdvoice.com               (recorded, OR one RESERVED fresh code)
ultimate fallback → pre-recorded video                    (cued, identical narration)
```
The `$ recovered` counter is client-side, so it looks perfect regardless.

---

## Scope

**MVP (must have by 3:00 freeze):**
- [x] Runtime bee working (`agent/freebee_agent.py` + `survey_clone.html`)
- [x] Phone UI, 5 screens (`index.html`)
- [ ] One real receipt scanned → parsed (vision) OR seeded
- [ ] The live money-shot rehearsed twice
- [ ] Fallback video recorded

**Stretch (only if MVP is locked):**
- Real vision parsing of a photographed receipt (backend)
- OpenAI Realtime voice instead of Web Speech
- Real browser-use run against mcdvoice.com wired to the phone
- Bee-swarm animation / multiple rewards at once
- Real email send (Resend/SendGrid) instead of the "emailed" confirmation

---

## Team (3 people)

- **Person 1 — Pitch + AI:** the 90-sec story, the Ramp angle, the vision + voice prompts, seed data, timekeeper, sponsor slide. *Also does the receipt run first.*
- **Person 2 — UI:** polish `index.html` / rebuild in Cursor; the money-shot visuals + counter.
- **Person 3 — Bee:** `freebee_agent.py` hardening, the fallback video, the receipt logistics. **One job: the money-shot never fails.**

---

## Ramp angle (there are recruiters in the room)

FreeBee = **the consumer mirror of Ramp.** Ramp claws back wasted *business* spend; FreeBee claws back wasted *personal* spend — same loop: receipt → structured data → automated money movement. Close with it.

---

## Receipt run — where to go (near 873 Broadway / Madison Square Park)

Grab **10–15 receipts**, and **set 3 aside untouched** for the stage (codes are one-time-use).

| Priority | Store | Buy | Reward | Survey |
|---|---|---|---|---|
| 1 (closest/easiest) | **CVS** (1–2 blks) | gum ~$1 | $1,000 sweepstakes | cvshealthsurvey.com |
| 2 (food, shortest survey) | **Subway** (1 blk) | cookie ~$1 | FREE cookie, instant code | subwaylistens.com |
| 3 (biggest number) | **Home Depot** — 40 W 23rd (~5 blks, right by you) | anything ~$1 | **$5,000** sweepstakes | homedepot.com/survey |
| 4 (best live hero) | **McDonald's** (Union Sq area) | fries | FREE fries, **instant** code | mcdvoice.com |
| 5 (the "email" story) | **Chick-fil-A** (further, Midtown) | nuggets | free item, **emailed ~24h** | mycfavisit.com |

Also nearby: **Whole Foods Union Sq** ($250), **Best Buy Union Sq / 52 E 14th** ($5,000).

**Live-reveal rule:** demo with **McDonald's/Subway** (instant on-screen code). Chick-fil-A is the *"and it just emails you the free nuggets"* narrative — its code arrives a day later, so don't put it on the live counter.
