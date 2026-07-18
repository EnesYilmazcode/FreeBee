# FreeBee — browser extension

Chrome/Edge (Manifest V3) companion for FreeBee. It adds claimable offers to Gmail
and includes a popup with three tabs:

- **Gmail claims** — selected inbox messages are highlighted in yellow. Hover a
  highlighted row to reveal **Claim**, which opens that message's configured URL.
  The matching rules and URLs are intentionally hardcoded at the top of `gmail.js`.

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
4. Open or refresh `mail.google.com`. Hover a highlighted offer and click **Claim**.

After changing `gmail.js`, go back to `chrome://extensions`, click the extension's
reload button, and refresh Gmail.

## How it fits the product
The autofill logic (`autofillPage` in `popup.js`) matches common field names
(email/name/phone/zip) — the same job the runtime browser agent does, but manual and instant.
In the full flow, the agent would push completed surveys + reward codes into this same wallet.

## Files
| File | What |
|---|---|
| `manifest.json` | MV3 config (storage + activeTab + scripting) |
| `popup.html/.css/.js` | The 3-tab UI + all logic |
| `gmail.js` | Hardcoded email match rules, per-rule links, and Gmail DOM integration |
| `gmail.css` | Highlight and hover-only Claim button styles |
| `icons/` | Generated bee icons (16/48/128) |
