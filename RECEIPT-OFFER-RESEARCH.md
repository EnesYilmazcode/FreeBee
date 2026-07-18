# FreeBee receipt-offer research

Research date: 2026-07-18

## Executive summary

There is a real, repeatable pattern behind FreeBee:

1. A receipt contains a survey URL, QR code, invitation number, survey code, or receipt/invoice number.
2. The customer visits a web form and answers feedback or promotion questions.
3. The customer receives a coupon, points, instant-win result, or sweepstakes entry.
4. Some promotions require a receipt photo upload instead of (or in addition to) a printed code.

For the hackathon demo, the best story is **“FreeBee finds the action hidden in the receipt, explains the opportunity, and prepares the form.”** The browser agent should stop before final submission unless the user explicitly confirms. Use synthetic receipts and a mock form for the live demo; do not submit real entries with invented or recycled personal information.

## Best examples to model

| Example | What the receipt/form contains | Reward or outcome | Evidence | Demo value |
|---|---|---|---|---|
| Walgreens Customer Satisfaction Sweepstakes | Receipt or invoice may include an invitation; the entry site asks for a survey number + password or invoice number | One entry into a monthly drawing; July 2026 rules list a $500 digital Walgreens gift card | [Official July 2026 rules](https://www.walgreens.com/images/adaptive/pdf/sweepstakes/csat_sweepstakesrules_Eng.pdf) | Excellent end-to-end model: code extraction, date window, eligibility, and sweepstakes disclosure |
| Ritchies Spin to Win | Qualifying receipt QR code or online entry path | Spin-to-win promotion | [Ritchies promotion page](https://www.ritchies.com.au/spin-win) | Good QR-first example; shows that the CTA can be on the receipt or entered online |
| IGA Win Instantly | Unique code associated with a qualifying purchase/receipt | Instant-win promotion; page advertises a winner every 10 minutes | [IGA promotion page](https://www.iga.com.au/win/) | Good “opportunity card” for a dashboard because the outcome is immediate and easy to visualize |
| Colgate at Coles | QR code or web entry; each entry supported by a separate qualifying receipt | Promotional prize/offer entry | [Official FAQ](https://www.winwithcolgate.com.au/faq) | Shows product-level matching: receipt must contain qualifying products and each receipt is unique |
| P&G receipt upload sweepstakes | Photo upload of the entire receipt; qualifying product detection | Extra entries based on qualifying products; official rules also describe a no-purchase mail-in method | [Official rules example](https://www.pgsweepstakes.com/rules.pdf) | Closest to FreeBee’s receipt-vision pitch: image → line-item verification → eligibility explanation |
| COURTS Guess & Win | Receipt photo, membership number, and a guess submitted through a QR-linked form | Chance to win HomeClub points | [Official campaign terms](https://www.courts.com.sg/media/wysiwyg/fy25/wk45/instore/COURTS_Raya_Campaign_Guess_Win_Terms_Conditions.pdf) | Strong example of a form requiring both receipt evidence and user-provided fields |

## Receipt-image references for the visual demo

These are useful examples of how the call-to-action is printed at the bottom of a receipt. Several are old or third-party images, so treat them as **UI/vision training references**, not live offers:

- [Nike receipt photo](https://hip2save.com/2017/08/10/nike-outlet-stores-possible-free-10-nike-gift-code-check-store-receipt-for-offer/) — bottom CTA says to visit `mynikevisit-na.com`, enter a receipt code, complete a survey, and receive a coupon. Historical example; verify before presenting as active.
- [Chick-fil-A receipt photo](https://thekrazycouponlady.com/tips/store-hacks/chick-fil-a-free-chicken) — receipt shows `mycfavisit.com`, a serial number, a short validity window, and a free sandwich offer after survey completion. Historical/third-party reference.
- [KFC receipt photo](https://www.moneysavingexpert.com/deals/kfc-money-saving-hacks/) — receipt shows `yourKFC.co.uk`, a short entry window, and a free snack/side validation code. UK example; historical/third-party reference.
- [Woods receipt survey image](https://community.qualtrics.com/custom-code-12/how-do-i-setup-a-custom-survey-code-for-a-receipt-survey-so-is-both-validates-and-embeds-4126) — sample receipt footer prominently shows a survey URL, phone fallback, prize language, and a long survey code. Particularly useful as a layout reference.
- [McDonald’s receipt survey image](https://survey.fast-insight.com/mcd/cz/) — receipt shows a QR code, fallback URL, and unique survey code. International example.
- [Co-op receipt/invite image](https://winonlinefreebies.medium.com/starbucks-customer-experience-surveystarbucks-customer-experience-survey-win-online-freebies-d3474eb95d41) — visual reference for a receipt/invite card offering a chance to win vouchers.

## Fields FreeBee should extract

```json
{
  "merchant": "Walgreens",
  "receipt_date": "2026-07-18",
  "receipt_id_or_survey_code": "redacted-demo-code",
  "cta_type": "survey_sweepstakes",
  "entry_url": "https://example.test/receipt-offer",
  "reward": "$500 gift-card sweepstakes entry",
  "deadline_or_validity": "within 72 hours / promotion window",
  "purchase_requirements": [],
  "required_fields": ["survey code", "honest feedback", "email if claiming a result"],
  "confidence": 0.94,
  "needs_user_confirmation": true
}
```

Important extraction targets:

- URL, QR code, phone number, and fallback instructions
- Receipt date/time and expiration window
- Survey/transaction/invoice number
- Qualifying product names, quantities, and spend threshold
- Reward type: coupon, free item, points, instant win, or drawing entry
- Geographic/age/employee restrictions
- Whether a no-purchase alternative exists
- Whether the promotion prohibits automated entries

## Recommended live demo fixture

Create one clearly labeled synthetic receipt with:

```text
YOUR RECEIPT IS AN INVITATION
Tell us about your visit at demo.freebee.local
Survey code: 4829-0133-9384-502184
Complete within 72 hours for a chance to win a $500 gift card.
No purchase necessary where required by official rules.
```

Then have FreeBee:

1. OCR the receipt.
2. Highlight the CTA and code on the image.
3. Produce an opportunity card with reward, deadline, confidence, and required fields.
4. Open a local mock form.
5. Fill only synthetic demo values.
6. Pause at **“Review before submit”** and show the policy/eligibility warning.

This gives you a convincing browser-agent moment without relying on a live contest, risking duplicate entries, or transmitting a real person’s identity to a third party.

## Safety and product boundary

FreeBee should not guess a person’s name, address, phone number, age, or email, and it should not mass-submit sweepstakes. The product can discover and prepare an entry, but the user should review eligibility, terms, privacy disclosures, and the final payload before submission. This matters because at least one official ruleset explicitly warns that automated computer systems can be prohibited and entries can be disqualified.

## Source-quality notes

- **Official/primary:** Walgreens rules, Ritchies promotion page, IGA promotion page, Colgate FAQ, P&G rules, and COURTS terms.
- **Visual/secondary:** receipt photos and write-ups from Hip2Save, Krazy Coupon Lady, MoneySavingExpert, Qualtrics Community, Medium, and the McDonald’s survey page.
- Promotions change quickly. FreeBee should display “checked on” and “source” metadata and re-check the live rules before calling an opportunity active.

## Narrowed target: receipt survey → free food

This is the exact category the team described. It is different from a sweepstakes: the reward is usually a coupon or validation code issued after a short customer-experience survey.

### Confirmed examples

- **Chick-fil-A:** the official survey page asks for the serial number printed on the receipt and says that, after completion, a code for a free sandwich is sent by email within 24 hours. Chick-fil-A’s support page confirms that the survey invitation appears on the printed receipt or in the app. ([survey](https://www.mycfavisit.com/Survey?AspxAutoDetectCookieSupport=1), [support page](https://www.chick-fil-a.com/customer-support/events-and-promotions/receipt-survey/where-can-i-find-the-customer-experience-survey))
- **KFC UK:** the official terms say customers can receive a free side/snack after completing the Guest Satisfaction Survey, and the survey must be completed within three days of the date on the retained receipt for a valid code to be generated. ([official terms](https://www.kfc.co.uk/terms-conditions))
- **McDonald’s:** the exact offer varies by restaurant, country, and time. Current official McDonald’s sources more prominently document app rewards and receipt-based “missing points” flows than a universal free-nuggets survey. Treat McDonald’s as a great visual concept reference, but verify the offer printed on the specific receipt before describing it as active. ([official rewards page](https://www.mcdonalds.com/us/en-us/mymcdonalds.html))

### What the agent actually needs to do

The interesting automation is not just clicking “Next.” It is:

1. Read the tiny footer and extract the survey URL, serial number, restaurant/store number, visit date, and deadline.
2. Navigate to the correct site and enter the receipt-specific code.
3. Answer factual questions from the receipt where possible: location, date, time, order channel, and purchased items.
4. Ask the user only for subjective answers the agent cannot truthfully know, such as food quality, wait time, or staff interaction.
5. Detect the reward result, save the code, expiration, redemption restrictions, and whether a purchase is required.
6. Stop before final submission or redemption unless the user confirms.

## Recommended wow factor

Build a **“receipt-to-reward autopilot”** with a visible human-in-the-loop moment:

> Drop in a receipt. FreeBee highlights the tiny offer, opens the right form, answers everything it can prove, asks only one missing question, then returns a redeemable reward card.

For the stage demo, use a synthetic Chick-fil-A-style receipt and a local mock survey that returns a free-sandwich code. Show three synchronized panels:

- **Receipt lens:** bounding box around the footer CTA, URL, code, and expiry.
- **Agent trace:** “Found survey → entered serial → answered 7 factual fields → need your experience of wait time.”
- **Reward wallet:** “Free sandwich — valid 14 days — in-store only — source receipt attached.”

The strongest moment is when the agent refuses to invent an answer: it pauses and asks one natural question, then continues automatically. That makes the product feel useful and trustworthy rather than like a form-filling macro.

Optional second wow moment: upload three receipts at once and show FreeBee ranking them by estimated value, confidence, and time remaining. Keep all three forms mocked for the demo and label them “demo data.”

## Hackathon asset strategy: no physical receipt required

Do not lose build time buying food solely to obtain a receipt. Do not submit a receipt image or receipt code copied from a stranger online: those identifiers are often unique, may already be used or expired, and can be tied to a real purchase.

Use a two-part demo fixture instead:

1. **Synthetic receipt image:** design a realistic narrow receipt containing a fictional restaurant, a QR code pointing to `http://freebee.local/survey`, a fake serial number, a two-day expiration window, and the free-item CTA. Add a visible “SYNTHETIC DEMO RECEIPT — NOT VALID FOR REDEMPTION” mark.
2. **Local mock survey:** create a form that accepts the fake serial number, asks 5–7 survey questions, returns a fake reward code, and displays the redemption restrictions. Seed it with a small scriptable dataset so the browser agent has a reliable target during judging.

The audience will see the real product behavior—vision extraction, browser navigation, selective questioning, completion, and reward capture—without depending on a live restaurant site or a one-time receipt code.
