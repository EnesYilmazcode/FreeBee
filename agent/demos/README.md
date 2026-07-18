# No-key survey demo drivers

Deterministic Playwright scripts that fill real surveys **without an API key** — used to
prove the "given a link → fill the form" flow on stage when a key isn't handy. They open a
visible browser you can mirror to the projector.

```bash
pip install playwright && python -m playwright install chromium

python agent/demos/survey_inspector.py   "<any-survey-url>"   # learn a survey's structure first
python agent/demos/topbox_surveymonkey.py "<surveymonkey-url>" # fill SurveyMonkey (stops before submit)
python agent/demos/topbox_qualtrics.py    "<qualtrics-url>"    # drive Qualtrics (capped at 5 pages)
```

## What these prove — and their hard limit

Tested live on a real Uber (SurveyMonkey) and United (Qualtrics) survey:

| | Standard radio questions | Custom widgets (tiles, multi-select boxes) |
|---|---|---|
| **SurveyMonkey** | ✅ top-boxed, even as question text randomized per load | — |
| **Qualtrics** | ✅ NPS 0–10 → picked 10; passed the intro gate + reCAPTCHA v3 | ❌ **stalls** — "select up to 4 areas" tiles aren't `<input type=radio>` |

**The lesson (this is the whole point):** a hardcoded, selector-based script generalizes to the
*easy ~70%* — standard radios across different platforms — but **breaks on the long tail of custom
widgets** (Qualtrics select-boxes, drop-downs, sliders) and on new platforms it's never seen.

That is exactly why FreeBee's runtime "bee" is an **LLM browser agent** (`../freebee_agent.py`,
powered by [browser-use](https://github.com/browser-use/browser-use)), not a script: it *looks at
the rendered page* and clicks the right thing regardless of widget type or platform. Use these
deterministic drivers as a no-key fallback/illustration; use the LLM agent for real generalization.

## Safety notes
- URLs are passed as arguments — **no personal survey tokens are committed to this repo.**
- The drivers **stop before final submit** (SurveyMonkey) or **cap at 5 pages** (Qualtrics) so they
  don't send real responses to a live merchant during testing.
- Screenshots are written to your system temp dir (path printed on exit).
