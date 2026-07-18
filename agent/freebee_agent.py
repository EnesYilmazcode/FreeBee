"""
FreeBee -- the runtime "worker bee".
Dispatches a browser-use agent to complete a receipt survey and read back the reward code.

QUICK START (Windows PowerShell, from the repo root):

    pip install browser-use
    python -m playwright install chromium
    $env:OPENAI_API_KEY = "sk-..."          # sponsor-aligned; or set ANTHROPIC_API_KEY

    # 1) serve the self-hosted survey clone (this is the GUARANTEED live money-shot):
    python -m http.server 8000 --directory agent
    #    -> clone is now at http://localhost:8000/survey_clone.html

    # 2) in a second terminal, send the bee at it:
    python agent/freebee_agent.py --url http://localhost:8000/survey_clone.html --code 04289055172704311962883043

    # 3) the "it works on REAL sites" proof run (use a FRESH, UNUSED code -- see README):
    python agent/freebee_agent.py --url https://www.mcdvoice.com --code <FRESH_26_DIGIT_CODE>

A visible Chrome window opens (headless=False) -- mirror it to the projector so the
audience watches the bee fill the survey and collect the reward.

NOTE: browser-use's import names / signatures shift between minor versions. If an import
below fails, check docs.browser-use.com -- the concepts (Agent, a chat model, a browser
session, agent.run) are stable even when the exact names move.
"""

import argparse
import asyncio
import sys

# --- MUST run before anything touches Playwright, or Win11 throws NotImplementedError ---
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from browser_use import Agent, BrowserSession  # noqa: E402

# Sponsor-aligned default (OpenAI). Pass --model to override (e.g. a current Claude id).
try:
    from browser_use import ChatOpenAI as Chat  # noqa: E402
    DEFAULT_MODEL = "gpt-4o"
except Exception:  # fall back to Anthropic if the OpenAI shim isn't present
    from browser_use import ChatAnthropic as Chat  # noqa: E402
    DEFAULT_MODEL = "claude-sonnet-4-5"  # <- update to your current Claude model id

# The single highest-leverage tactic: TOP-BOX every answer. Picking the most-positive
# option is not only fast, it SKIPS the conditional "what went wrong?" follow-up pages
# that negative answers trigger -- so the survey stays short and deterministic on stage.
SYSTEM_RULES = (
    "You are completing a receipt satisfaction survey to unlock a reward code. "
    "On EVERY question, select the MOST POSITIVE / highest-satisfaction option "
    "(e.g. 'Highly Satisfied', '5', 'Yes' -- usually the leftmost or top choice). "
    "For any matrix/grid, set EVERY row to the top rating. "
    "Leave open-ended text boxes blank, or type 'Great service, fast and friendly.' "
    "only if a value is required. After each page, click the Next / Continue / Submit "
    "button. Do not deliberate. Continue until a validation/reward code is shown, then "
    "read that code aloud and STOP."
)


def build_task(url: str, code: str) -> str:
    # Pre-chunk long codes so the agent doesn't fat-finger multi-box entry (McDVoice = 26 digits).
    chunks = " ".join(code[i:i + 5] for i in range(0, len(code), 5)) if len(code) > 6 else code
    return (
        f"{SYSTEM_RULES}\n\n"
        f"Step 1: Go to {url}\n"
        f"Step 2: Enter this survey code into the code field(s): {code}  (grouped: {chunks})\n"
        f"Step 3: Start the survey, then answer every question with the TOP rating and "
        f"advance through all pages until the reward / validation code appears.\n"
        f"Step 4: Report the final reward/validation code."
    )


async def main() -> None:
    ap = argparse.ArgumentParser(description="FreeBee runtime survey agent")
    ap.add_argument("--url", required=True, help="survey URL (self-hosted clone or the real site)")
    ap.add_argument("--code", required=True, help="survey code read off the receipt")
    ap.add_argument("--model", default=DEFAULT_MODEL, help=f"LLM model (default {DEFAULT_MODEL})")
    ap.add_argument("--max-steps", type=int, default=25,
                    help="hard cap so the agent can't loop forever on stage")
    args = ap.parse_args()

    session = BrowserSession(headless=False)  # visible window -> mirror to the projector
    agent = Agent(
        task=build_task(args.url, args.code),
        llm=Chat(model=args.model),
        browser_session=session,
    )

    result = await agent.run(max_steps=args.max_steps)
    print("\n=== FreeBee agent finished ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
