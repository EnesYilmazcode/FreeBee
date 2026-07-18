"""No-key deterministic top-box filler for SurveyMonkey surveys.
Fills every radio group with the MOST POSITIVE option (assumes the standard
negative->positive scale order, so top-box = the last choice), then STOPS
before the final submit. Watchable (headed + slow_mo).

    python agent/demos/topbox_surveymonkey.py "<surveymonkey-url>"

This is a no-API-key STAND-IN that shows the top-box strategy. It only handles
standard radio groups -- the real, cross-platform generalizer is the LLM agent
in ../freebee_agent.py. See README.md.
"""
import asyncio, sys, os, tempfile
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from playwright.async_api import async_playwright

if len(sys.argv) < 2:
    sys.exit("usage: python topbox_surveymonkey.py <surveymonkey-url>")
URL = sys.argv[1]
SHOT = os.path.join(tempfile.gettempdir(), "freebee_sm_filled.png")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=600)
        page = await browser.new_page(viewport={"width": 1100, "height": 900})
        await page.goto(URL, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(1500)

        # dismiss a privacy/consent gate if present
        try:
            await page.get_by_role("button", name="OK").click(timeout=4000)
        except Exception:
            pass
        await page.wait_for_timeout(800)

        # every distinct radio group, in page order
        names = await page.evaluate("""() => {
            const seen = [];
            document.querySelectorAll('input[type=radio]').forEach(r => {
                if (r.name && !seen.includes(r.name)) seen.push(r.name);
            });
            return seen;
        }""")

        for i, g in enumerate(names, 1):
            radios = page.locator(f"input[name='{g}']")
            n = await radios.count()
            if n == 0:
                continue
            target = radios.nth(n - 1)  # last = most positive on a standard scale
            # SurveyMonkey radios are custom: click the LABEL, then verify + retry
            label_id = await target.get_attribute("aria-labelledby")
            clickable = page.locator(f'[id="{label_id}"]') if label_id else target
            await clickable.scroll_into_view_if_needed()
            checked = "false"
            for _ in range(3):
                await clickable.click(force=True)
                await page.wait_for_timeout(400)
                checked = await target.get_attribute("aria-checked")
                if checked == "true":
                    break
            print(f"-> Q{i}: top-boxed group {g} [checked={checked}]")

        await page.wait_for_timeout(800)
        await page.screenshot(path=SHOT, full_page=True)
        print(f"\n=== Filled {len(names)} question(s). Stopped BEFORE submit. ===")
        print("Screenshot:", SHOT)
        await page.wait_for_timeout(5000)
        await browser.close()

asyncio.run(main())
