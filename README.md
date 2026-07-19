# 🐝 FreeBee

> **Free money, zero effort.** Snap a photo of a receipt, and a browser agent claims the free reward hiding on it, then sends it to you.

Almost every receipt has a reward printed on it: *"Take a 2-minute survey, get a free item."* Almost nobody does them. FreeBee does them for you. Point your phone at a receipt and a "bee" (an autonomous browser agent) fills out the survey, grabs the reward code, and delivers it.

Built at the **Ramp Builders Cup** (NYC, July 2026).

**Live demo:** https://enesyilmazcode.github.io/FreeBee/ — phone-friendly, no install.

---

## How it works

```
📱  Phone: snap the receipt (or pick a sample)
     │  photo
     ▼
🧠  Vision LLM (Gemini)  ──  reads merchant + survey code + amount  ──►  Receipt JSON
     │
     ▼
🎙️  Voice intake  ──  you say your email; open-ended survey answers are auto-filled
     │
     ▼
🐝  The bee (browser-use)  ──  opens the survey, answers every question, grabs the code
     │
     ▼
📧  Reward code back to your phone + a running "$ recovered" counter
```

The phone never runs the browser itself. It talks to a small relay (`agent/server.py`) on a
laptop that drives the real Chrome agent and streams live screenshots plus the reward code
back to the phone.

## The flow, screen by screen

1. **Scan** — snap the receipt, or tap *Try a sample*.
2. **Found** — FreeBee shows what it read and the reward it found (*"FREE Medium Fries — $4.29"*).
3. **Your info** — a voice agent asks where to send the reward; you just talk. Open-ended survey
   questions get a sensible auto-answer, so you type nothing.
4. **Watch the bee** — a live browser fills the survey while a *$ recovered* counter ticks up.
5. **Done** — the reward code, claimed and emailed.

## Repo map

| Path | What it is |
|---|---|
| `index.html` | The phone web app (all 5 screens). Runs standalone on GitHub Pages. |
| `watch.html` | Big-screen "live watch" view of the bee running + the $ counter. |
| `agent/server.py` | Flask relay between phone and agent. Endpoints: `/api/run`, `/api/state`, `/api/frame.png`. |
| `agent/freebee_agent.py` | The [browser-use](https://github.com/browser-use/browser-use) agent (Gemini, Windows event-loop fix, "top-box" survey prompt). |
| `agent/survey_clone.html` | A self-hosted demo survey (no captcha, any code works) for a guaranteed live run. |
| `extension/` | Chrome (MV3) companion: Gmail offer highlighting, one-tap autofill, reward wallet. |
| `demo/` | Sample receipts + seeded receipt JSON. |
| `PLANNING.md`, `research/` | The build plan, survey research, and demo strategy. |

## Run it

**Phone demo (no setup):** open https://enesyilmazcode.github.io/FreeBee/ on your phone.

**The real agent (laptop + phone):**

```bash
pip install -r agent/requirements.txt
python -m playwright install chromium
pip uninstall -y aiodns          # Windows: fixes a DNS bug that breaks LLM calls
# add your Gemini key to agent/.env  (copy agent/.env.example)

python agent/server.py           # prints http://<laptop-ip>:8000
```

Put the phone and laptop on the same network (a phone hotspot is the most reliable at a venue),
open that address on the phone, scan a receipt, and hit **Send the Bee**. The laptop drives real
Chrome; the phone mirrors it and shows the reward code. Full walkthrough in [`LAUNCH.md`](LAUNCH.md).

## The Chrome extension

`extension/` is a standalone MV3 companion that highlights claimable offers in Gmail, autofills
survey fields from a saved profile (stored only on your device via `chrome.storage.local`), and
keeps a wallet of reward codes and total $ recovered. Load it unpacked from `chrome://extensions`
— see [`extension/README.md`](extension/README.md).

## Tech stack

| Layer | Tech |
|---|---|
| Browser agent | [browser-use](https://github.com/browser-use/browser-use) (local, headed Chrome) |
| Vision | Gemini — receipt photo → JSON |
| Voice | Web Speech API |
| Relay / backend | Flask (`agent/server.py`) |
| Phone UI | Static HTML + JS |
| Hosting | GitHub Pages + Firebase |

## Why "the consumer Ramp"

FreeBee is the consumer mirror of Ramp. Ramp claws back wasted *business* spend; FreeBee claws
back wasted *personal* spend. Same loop: receipt → structured data → automated money movement.
Fitting, since it was built at Ramp's own Builders Cup.

## Status

A hackathon build, optimized for a live demo. The receipt-to-reward flow runs end to end (Gemini
vision plus a real browser-use agent, verified against mcdvoice.com). The bundled
`agent/survey_clone.html` is the always-works path for a stage demo, and the seed data in `demo/`
keeps the UI working even without live parsing.

---

Built with Cursor + Codex at the Ramp Builders Cup, NYC, July 2026.
