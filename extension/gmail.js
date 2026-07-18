// FreeBee Gmail inbox integration.
//
// Edit this list to choose which messages receive a Claim button. A row must
// match every populated field in a rule. Within a field, matching any value is
// enough. Matching is case-insensitive.
const CLAIM_RULES = [
  {
    senderContains: ["mcdonald's", "mcdonalds", "mcdvoice"],
    subjectContains: ["survey", "tell us", "receipt", "visit"],
    claimUrl: "https://www.mcdvoice.com/",
  },
  {
    senderContains: ["subway", "tellsubway"],
    subjectContains: ["survey", "tell us", "receipt", "visit"],
    claimUrl: "https://www.tellsubway.com/",
  },
  {
    senderContains: ["cvs", "cvs/pharmacy"],
    subjectContains: ["survey", "feedback", "receipt", "visit"],
    claimUrl: "https://www.cvshealthsurvey.com/",
  },
];

const ROW_SELECTOR = "tr.zA";
const BUTTON_CLASS = "freebee-claim-button";
const CLAIMABLE_CLASS = "freebee-claimable";

function normalizedText(value) {
  return (value || "").toLocaleLowerCase().replace(/\s+/g, " ").trim();
}

function includesAny(text, needles) {
  return !needles?.length || needles.some((needle) => text.includes(normalizedText(needle)));
}

function readRow(row) {
  const senderNode = row.querySelector(".yW span[email], span[email]");
  const sender = normalizedText([
    senderNode?.getAttribute("email"),
    senderNode?.getAttribute("name"),
    senderNode?.textContent,
  ].filter(Boolean).join(" "));
  const subject = normalizedText(row.querySelector(".bog")?.textContent);
  const snippet = normalizedText(row.querySelector(".y2")?.textContent);
  return { sender, subject, snippet };
}

function matchingRule(message) {
  return CLAIM_RULES.find((rule) =>
    includesAny(message.sender, rule.senderContains) &&
    includesAny(message.subject, rule.subjectContains) &&
    includesAny(message.snippet, rule.snippetContains)
  );
}

function clearClaim(row) {
  row.classList.remove(CLAIMABLE_CLASS);
  row.querySelector(`.${BUTTON_CLASS}`)?.remove();
  row.querySelectorAll(".freebee-claim-cell").forEach((cell) =>
    cell.classList.remove("freebee-claim-cell")
  );
}

function addClaim(row, rule) {
  const targetCell = row.querySelector("td:last-of-type");
  if (!targetCell || row.querySelector(`.${BUTTON_CLASS}`)) return;

  row.classList.add(CLAIMABLE_CLASS);
  targetCell.classList.add("freebee-claim-cell");

  const button = document.createElement("button");
  button.type = "button";
  button.className = BUTTON_CLASS;
  button.textContent = "Claim";
  button.title = "Claim this offer with FreeBee";
  button.setAttribute("aria-label", "Claim this offer with FreeBee");

  // Keep Gmail from selecting or opening the message behind the button.
  for (const eventName of ["mousedown", "mouseup", "click", "keydown"]) {
    button.addEventListener(eventName, (event) => event.stopPropagation());
  }
  button.addEventListener("click", (event) => {
    event.preventDefault();
    window.open(rule.claimUrl, "_blank", "noopener,noreferrer");
  });

  targetCell.append(button);
}

function processRow(row) {
  const message = readRow(row);
  const signature = `${message.sender}|${message.subject}|${message.snippet}`;
  if (row.dataset.freebeeSignature === signature) return;
  row.dataset.freebeeSignature = signature;

  clearClaim(row);
  const rule = matchingRule(message);
  if (rule) addClaim(row, rule);
}

function scan(root = document) {
  if (root instanceof Element && root.matches(ROW_SELECTOR)) processRow(root);
  root.querySelectorAll?.(ROW_SELECTOR).forEach(processRow);
}

let scanQueued = false;
function queueScan() {
  if (scanQueued) return;
  scanQueued = true;
  requestAnimationFrame(() => {
    scanQueued = false;
    scan();
  });
}

// Gmail is a single-page app and reuses inbox rows while navigating and
// scrolling, so observe changes instead of relying only on the first load.
const observer = new MutationObserver(queueScan);
observer.observe(document.documentElement, { childList: true, subtree: true, characterData: true });
scan();
