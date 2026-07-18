# 🐝 FreeBee — launch it at the demo (2 minutes)

The bee agent runs a real Chrome browser, so it runs on the **laptop**. The **phone** is the
scanner + remote. They talk over a network you control (your phone's hotspot is most reliable
at a venue).

## One-time setup on the laptop
```bash
pip install -r agent/requirements.txt
python -m playwright install chromium
pip uninstall -y aiodns          # Windows: fixes a DNS bug that breaks LLM calls
# put your Gemini key in agent/.env  (copy agent/.env.example)
```

## Launch (every time)
1. **Phone:** turn on Personal Hotspot. **Laptop:** connect to that hotspot.
   (Or share a Wi-Fi you both trust — but a venue Wi-Fi may block phone↔laptop.)
2. **Laptop:** double-click **`run.bat`** (or `python agent/server.py`).
   It prints the address, e.g. `http://10.211.53.147:8000`.
3. **Phone:** open that address in the browser. You'll see the FreeBee app.
4. Scan or upload a receipt → confirm the code → **Send the Bee**.
   - The **laptop** shows the real Chrome doing the survey.
   - The **phone** shows the live frames + the reward code, and mirrors it.

## What's real
- Real receipt → **Gemini vision** reads the code (`/api/scan`).
- Real **Gemini browser-use agent** fills the real survey (mcdvoice.com verified working).
- Real reward/validation code comes back to the phone.

## Demo tips
- McDonald's codes are **one-time-use + expire in 30 days** — keep 2–3 fresh, unused receipts.
- OCR is ~99% on thermal paper; the code screen is **editable** so you can fix one digit.
- No laptop / opened on GitHub Pages? The app still runs a **visual** demo (not the real agent).
