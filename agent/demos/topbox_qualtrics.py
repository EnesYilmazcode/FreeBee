"""No-key deterministic top-box driver for Qualtrics surveys.
Passes the intro gate, then on each page selects the MOST POSITIVE choice in every
radio group (scored by label text: "Extremely satisfied", "Strongly agree", high
numbers, etc.), clicks Next, and screenshots. Capped at MAX_PAGES so it never
reaches the final submit on a long survey.

    python agent/demos/topbox_qualtrics.py "<qualtrics-url>"

LIMITATION (by design): this only handles standard radio groups. Qualtrics also
uses custom "select box" / tile widgets that are NOT <input type=radio> -- this
script CANNOT click those and will stall on them. That is exactly why the real
runtime bee is the LLM agent (../freebee_agent.py), which reads any widget. See README.md.
"""
import asyncio, sys, os, tempfile
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from playwright.async_api import async_playwright

if len(sys.argv) < 2:
    sys.exit("usage: python topbox_qualtrics.py <qualtrics-url>")
URL = sys.argv[1]
OUTDIR = tempfile.gettempdir()
MAX_PAGES = 5  # safety cap: never reach the final submit on a long real survey

TOPBOX_JS = r"""
() => {
  const POS = [/extremely likely/i,/extremely satisfied/i,/strongly agree/i,
               /very satisfied/i,/completely/i,/excellent/i,/^\s*yes\s*$/i,
               /definitely/i,/always/i,/outstanding/i];
  const groups = {};
  document.querySelectorAll('input[type=radio]').forEach(inp => {
    if (inp.name === 'g-recaptcha-response') return;
    const lab = inp.closest('label') ||
                document.querySelector('label[for="' + (window.CSS?CSS.escape(inp.id):inp.id) + '"]');
    const text = ((lab && lab.innerText) || inp.getAttribute('aria-label') || '').trim();
    (groups[inp.name] = groups[inp.name] || []).push({inp, text});
  });
  const chosen = [];
  Object.entries(groups).forEach(([name, opts]) => {
    let best = null, bestScore = -1e9;
    opts.forEach(o => {
      let s = 0;
      POS.forEach(rx => { if (rx.test(o.text)) s += 100; });
      const n = parseInt(o.text, 10);
      if (!isNaN(n)) s += n;            // higher number = more positive (NPS, 1-5, 1-7)
      if (s > bestScore) { bestScore = s; best = o; }
    });
    if (best) {
      (best.inp.closest('label') || best.inp).click();
      best.inp.click();
      chosen.push(name + ' -> "' + (best.text || '?') + '"');
    }
  });
  return chosen;
}
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=450)
        page = await browser.new_page(viewport={"width": 1100, "height": 900})
        await page.goto(URL, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(1800)

        try:
            await page.locator("#NextButton").click(timeout=6000)
            print("-> passed intro gate")
        except Exception:
            print("-> no intro gate")
        await page.wait_for_timeout(2500)

        for pg in range(1, MAX_PAGES + 1):
            body = (await page.inner_text("body")).lower()
            if any(k in body for k in ["thank you", "response has been recorded",
                                       "already responded", "survey is complete"]):
                print(f"-> reached end screen on page {pg}, stopping")
                break
            chosen = await page.evaluate(TOPBOX_JS)
            print(f"-> page {pg}: top-boxed {len(chosen)} question(s)")
            for c in chosen:
                print("     " + c)
            await page.wait_for_timeout(700)
            await page.screenshot(path=os.path.join(OUTDIR, f"freebee_q_page{pg}.png"), full_page=True)
            try:
                await page.locator("#NextButton").click(timeout=6000)
            except Exception:
                print("-> no Next button, stopping")
                break
            await page.wait_for_timeout(2600)

        print(f"\n=== Stopped after up to {MAX_PAGES} pages (never submitted). Shots in {OUTDIR} ===")
        await page.wait_for_timeout(2500)
        await browser.close()

asyncio.run(main())
