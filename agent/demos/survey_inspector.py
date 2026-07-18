"""No-key survey inspector: open any survey URL, screenshot it, and dump its
question text + form controls. Use this FIRST on a new survey to learn its
structure before writing/adapting a driver.

    pip install playwright && python -m playwright install chromium
    python agent/demos/survey_inspector.py "<survey-url>"

Screenshot is written to your temp dir (path printed at the end).
"""
import asyncio, sys, json, os, tempfile
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from playwright.async_api import async_playwright

if len(sys.argv) < 2:
    sys.exit("usage: python survey_inspector.py <survey-url>")
URL = sys.argv[1]
SHOT = os.path.join(tempfile.gettempdir(), "freebee_inspect.png")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1100, "height": 900})
        await page.goto(URL, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(2500)
        await page.screenshot(path=SHOT, full_page=True)

        text = await page.inner_text("body")
        controls = await page.evaluate("""() => {
            const out = [];
            document.querySelectorAll('input, textarea, select, button, [role=radio], [role=button]').forEach(el => {
                out.push({tag: el.tagName, type: el.type||'', role: el.getAttribute('role')||'',
                          name: el.name||'', id: (el.id||'').slice(0,30),
                          label: (el.getAttribute('aria-label')||el.value||el.innerText||'').replace(/\\s+/g,' ').slice(0,50)});
            });
            return out;
        }""")
        print("=== TITLE ===", await page.title())
        print("\n=== VISIBLE TEXT (first 1800) ===\n", text[:1800])
        print("\n=== CONTROLS (first 40) ===")
        print(json.dumps(controls[:40], indent=1)[:3500])
        print("\nScreenshot:", SHOT)
        await browser.close()

asyncio.run(main())
