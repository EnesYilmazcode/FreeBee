# Research: Tooling & strategy (verified 2026-07-18)

## Runtime browser agents (the "bee")

| Tool | What | Live view | Setup | Verdict |
|---|---|---|---|---|
| **browser-use** (OSS Python) | LLM drives a real Chrome; #1 on web-agent leaderboards (~87%) | headed window → mirror to projector | ~10–15 min | ✅ **PICK** — fastest to a working, watchable agent. |
| **Browserbase + Stagehand** | hosted cloud Chrome + live-view iframe you embed in your app | embedded iframe, human-takeover | ~25–40 min | Runner-up / cloud upgrade for the phone→email flow. |
| OpenAI computer-use (CUA) | model emits click/type, you drive the browser | DIY | 45–90 min | Tier 3–5 gated; a fresh account may not qualify. |
| Claude computer use | screenshot→action over a whole desktop/VM | VNC desktop | 45–90 min | Desktop-flavored, heavier to stage. |
| Playwright + LLM DIY | roll your own agent loop | headed if you build it | 90+ min | Reinvents the wheel. |

**Windows gotcha:** set `asyncio.WindowsProactorEventLoopPolicy()` as line 1 or Playwright throws
`NotImplementedError` on Win11. (Already baked into `agent/freebee_agent.py`.)

## Sponsors — Codex & Cursor (Best Use of Sponsors track)
- **Codex** and **Cursor** are *dev* tools that write FreeBee. Their in-app browsers **only open your
  own localhost** to verify code they wrote — **no cookies/login**, so **neither can be the runtime bee.**
- **Win the track by using BOTH to build, visibly:** run parallel Codex agents on the modules
  (ingestion / detection / agent-wiring / fixtures), use Cursor's browser tool to verify the UI +
  record the demo clip, and show a "Built with Cursor + Codex" slide with commit counts.
- Keep an OpenAI model driving browser-use so an OpenAI model is in the *live* run too.

## Architecture (demo-first, ~4 hrs)
`Receipt (.eml/paste/photo)` → `Vision LLM → Receipt JSON` → `Detection LLM (grounded by a merchant-policy
table)` → `Opportunity cards` → `"Send a Bee" → browser-use` → `$ recovered tally`.
Fastest path = ONE app (Next.js on Vercel, or the static `index.html`), state in memory/JSON, no Gmail OAuth,
no DB migrations.

## Prize tracks
| Track | Fit | Winnability |
|---|---|---|
| **Save Time. Save Money.** | FreeBee is literally this | 🔴 HIGH — the track to win. Anchor on a hard $ number. |
| **Audience Favorite** | "free money" + live browser clawing it back + jackpot counter | 🔴 HIGH if the live demo lands. |
| **Best Use of Sponsors** | build with Codex + Cursor, shown | 🟠 HIGH-MED — everyone claims it; differentiate with parallel Codex agents. |
| **Best Game** | not a game | ⚪ LOW — don't chase; add only light gamification. |

## 90-second demo script
1. **Hook:** "Who's gotten a price-drop / survey offer and never claimed it? That's free money you left on the table. FreeBee is the bee that claws it back."
2. **Ingest:** drop a seeded receipt → parses on screen.
3. **Detect:** reward cards appear → "FreeBee found $X you're owed."
4. **💰 Money shot:** "Watch it go get it." Live browser fills the survey → counter ticks $0→$X with a ding. Say nothing; let them watch.
5. **Ramp tie-in + close:** "Ramp claws back business spend; FreeBee does it for your personal wallet. One receipt, $X back, zero clicks."
6. **CTA:** "Vote FreeBee — Audience Favorite."
If the live agent stalls → cut to the pre-recorded run mid-sentence, same counter, same story.

## Other freebie types (beyond surveys — for the "and it also does…" slide)
Price-drop/price-adjustment refunds · mail-in/online rebates · warranty registration ·
unclaimed card cashback · easy returns · subscription-cancel reminders · no-proof class-action
settlements · **expense reimbursement submission (Ramp)** — the strongest host tie-in.
Most of these need login → keep them on the roadmap slide, demo the login-free survey live.
