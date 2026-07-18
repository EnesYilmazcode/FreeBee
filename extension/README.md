# FreeBee — browser extension

Chrome/Edge (Manifest V3) companion for FreeBee. Three tabs:

1. **Profile** — save the personal info common surveys ask for (name, email, phone, ZIP,
   birth year, gender). Stored **only on your device** via `chrome.storage.local`.
   Hit **⚡ Autofill this page** to drop those values into the survey open in the active tab.
2. **History** — every survey the bee has completed (merchant, date, status).
3. **Rewards** — your reward codes + values. Tap a code to copy it. Header shows total $ recovered.

Seeded with demo data on first run so it looks alive for a demo. **+ Add demo reward** appends
more; **Reset data** clears everything and re-seeds.

## Load it (unpacked)
1. `chrome://extensions` → toggle **Developer mode** (top-right).
2. **Load unpacked** → select this `extension/` folder.
3. Pin the 🐝 icon, click it to open the popup.

## How it fits the product
The autofill logic (`autofillPage` in `popup.js`) matches common field names
(email/name/phone/zip) — the same job the runtime browser agent does, but manual and instant.
In the full flow, the agent would push completed surveys + reward codes into this same wallet.

## Files
| File | What |
|---|---|
| `manifest.json` | MV3 config (storage + activeTab + scripting) |
| `popup.html/.css/.js` | The 3-tab UI + all logic |
| `icons/` | Generated bee icons (16/48/128) |
