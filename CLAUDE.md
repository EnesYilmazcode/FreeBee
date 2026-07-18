# FreeBee — shared context for ALL AI agents (Claude Code / Cursor / Codex)

**READ THIS FIRST.** This file keeps every teammate's AI agent in sync. It's a hackathon
(Ramp Builders Cup, NYC — demos **3:30 PM today**). Optimize for a **working demo**, not perfection.

---

## 🔴 GOLDEN RULE: commit + push after EVERY change
Small commits, pushed immediately to `main`, so everyone's agents stay up to date.

```bash
git pull --rebase origin main     # before you start editing
# ...make one small change...
git add -A && git commit -m "what you did" && git push origin main
```
**Never batch work.** One change = one commit = one push. If you generate a report/doc, push it too.

---

## What FreeBee is
Scan a receipt on your phone → a **browser agent** claims the free reward hiding on it
(survey-for-reward, rebate, etc.) → you get it emailed. **"Free money, zero effort."**

Tracks: **Save Time. Save Money.** (primary) · **Audience Favorite** · **Best Use of Sponsors** (Cursor + Codex).

## The 5 screens
`Scan` → `Found (reward)` → `Voice fills your email` → `Watch the bee (live browser + $ counter)` → `Emailed ✅`

---

## Settled decisions — DO NOT relitigate
- **Runtime "bee" = [browser-use](https://github.com/browser-use/browser-use)** (Python, local, headed). **NOT** Codex/Cursor browsers — those only open your *own* localhost to test code they wrote; they can't log into real sites. `Browserbase` = optional cloud upgrade.
- **Build the app with Cursor + Codex** — that IS the "Best Use of Sponsors" story. Show parallel Codex agents + a "Built with Cursor + Codex" slide.
- **Vision** (receipt→JSON) = GPT-4o / Claude vision, one call. Schema in `demo/seed-receipts.json`.
- **Voice intake** = Web Speech API now (in `index.html`) → OpenAI Realtime upgrade. Typed field is the fallback.
- **Demo layering (can't fail):** live = self-hosted `survey_clone.html` (always works) · proof = real McDonald's/Subway · fallback = recorded video.
- **Live reveal uses McDonald's / Subway** (instant on-screen code). **Chick-fil-A emails the code ~24h later** → narrative only, not the live money-shot.

## ⚠️ Demo discipline
- Survey codes are **one-time-use + expire in days** → grab 10–15 fresh receipts, **reserve 3 untouched** for the stage.
- Never parse a brand-new receipt live — seed known-good JSON.
- Invisible reCAPTCHA v3 can soft-block a fast agent → the **clone carries the live run**, real site is recorded proof.
- Full details: `research/RECEIPT-SURVEYS.md`.

---

## Repo map
| Path | What it is |
|---|---|
| `index.html` | Phone demo UI — 5 screens, no backend, autopilot money-shot. Live: https://enesyilmazcode.github.io/FreeBee/ |
| `agent/freebee_agent.py` | The **real** browser-use agent (Windows fix + top-box prompt) |
| `agent/survey_clone.html` | Self-hosted survey; `?auto=1` = autopilot for the UI demo |
| `agent/README.md` | How to run the agent + demo layering |
| `demo/seed-receipts.json` | Parsed receipt JSON (McDonald's + CVS) = hard-coded fallback |
| `demo/*-sample-receipt.txt` | Synthetic receipts to test the vision parser |
| `PLANNING.md` | Full build plan, architecture, scope, team lanes, receipt-run map |
| `research/TOOLING-AND-STRATEGY.md` | Verified: browser agents, sponsors, architecture, demo, prize tracks |
| `research/RECEIPT-SURVEYS.md` | Verified: every survey program, best live picks, agent execution reality |

## Run it
```bash
# Phone demo (no setup): open https://enesyilmazcode.github.io/FreeBee/
# ...or locally, from repo root:
python -m http.server 8000            # -> http://<laptop-ip>:8000 on your phone

# The REAL agent:
pip install browser-use && python -m playwright install chromium
python -m http.server 8000            # serve the clone
python agent/freebee_agent.py --url http://localhost:8000/agent/survey_clone.html --code 04289055172704311962883043
```

## Code style
Concise comments. No over-engineering. It's a hackathon — ship the smallest thing that demos.
Keep `survey_clone.html` a generic demo (not impersonating a real brand).
