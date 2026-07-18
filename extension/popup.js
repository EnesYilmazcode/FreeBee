// FreeBee popup — profile autofill + survey history + reward wallet.
// All data lives in chrome.storage.local (device-only, no backend).

const DEFAULT_PROFILE = {
  firstName: "", lastName: "", email: "", phone: "", zip: "", birthYear: "", gender: ""
};

// Seeded on first run so the demo looks alive. Each survey optionally carries a reward.
const SEED_SURVEYS = [
  { id: "s1", merchant: "McDonald's", url: "https://www.mcdvoice.com", date: "2026-07-18",
    status: "claimed", reward: "FREE Medium Fries w/ sandwich", value: 4.29,
    code: "FB-7K2Q9", redeemBy: "2026-08-17" },
  { id: "s2", merchant: "Subway", url: "https://www.tellsubway.com", date: "2026-07-16",
    status: "claimed", reward: "FREE Cookie w/ purchase", value: 2.50,
    code: "FB-M4XP1", redeemBy: "2026-08-15" },
  { id: "s3", merchant: "CVS/pharmacy", url: "https://www.cvshealthsurvey.com", date: "2026-07-15",
    status: "entered", reward: "Entry: win a $1,000 gift card", value: 0,
    code: null, redeemBy: null },
];

const $ = (sel) => document.querySelector(sel);
const store = {
  get: (keys) => new Promise((r) => chrome.storage.local.get(keys, r)),
  set: (obj) => new Promise((r) => chrome.storage.local.set(obj, r)),
};

// ---------- tabs ----------
document.querySelectorAll(".tab").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    $("#" + btn.dataset.tab).classList.add("active");
  });
});

// ---------- init ----------
async function init() {
  const data = await store.get(["profile", "surveys", "seeded"]);
  if (!data.seeded) {
    await store.set({
      profile: { ...DEFAULT_PROFILE, email: "enesyilmaz5157@gmail.com" },
      surveys: SEED_SURVEYS,
      seeded: true,
    });
  }
  await renderAll();
}

async function renderAll() {
  const { profile = DEFAULT_PROFILE, surveys = [] } = await store.get(["profile", "surveys"]);
  fillProfileForm(profile);
  renderHistory(surveys);
  renderRewards(surveys);
  renderTotal(surveys);
}

// ---------- profile ----------
function fillProfileForm(profile) {
  const form = $("#profile-form");
  Object.keys(DEFAULT_PROFILE).forEach((k) => {
    if (form.elements[k]) form.elements[k].value = profile[k] || "";
  });
}

$("#profile-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const profile = {};
  Object.keys(DEFAULT_PROFILE).forEach((k) => (profile[k] = form.elements[k].value.trim()));
  await store.set({ profile });
  const note = $("#saved-note");
  note.textContent = "✓ Saved";
  setTimeout(() => (note.textContent = ""), 1600);
});

// ---------- autofill the active tab ----------
$("#autofill").addEventListener("click", async () => {
  const { profile = DEFAULT_PROFILE } = await store.get(["profile"]);
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) return;
  const note = $("#saved-note");
  try {
    const [res] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: autofillPage,
      args: [profile],
    });
    const n = res?.result ?? 0;
    note.textContent = n ? `⚡ Filled ${n} field${n > 1 ? "s" : ""}` : "No matching fields found";
  } catch (err) {
    note.textContent = "Can't autofill this page";
  }
  setTimeout(() => (note.textContent = ""), 2200);
});

// Injected into the page. Matches common survey field names and fills from the profile.
function autofillPage(profile) {
  const map = [
    { keys: ["email", "e-mail"], val: profile.email },
    { keys: ["firstname", "first_name", "fname", "given"], val: profile.firstName },
    { keys: ["lastname", "last_name", "lname", "surname", "family"], val: profile.lastName },
    { keys: ["fullname", "full_name", "yourname"], val: `${profile.firstName} ${profile.lastName}`.trim() },
    { keys: ["phone", "tel", "mobile"], val: profile.phone },
    { keys: ["zip", "postal", "postcode"], val: profile.zip },
    { keys: ["birthyear", "yob", "birth_year"], val: profile.birthYear },
  ];
  const fields = document.querySelectorAll("input, textarea");
  let filled = 0;
  fields.forEach((el) => {
    if (el.type === "hidden" || el.disabled || el.readOnly) return;
    const hay = `${el.name} ${el.id} ${el.placeholder} ${el.getAttribute("aria-label") || ""}`.toLowerCase();
    if (el.type === "email" && profile.email) {
      el.value = profile.email; el.dispatchEvent(new Event("input", { bubbles: true })); filled++; return;
    }
    for (const m of map) {
      if (m.val && m.keys.some((k) => hay.includes(k))) {
        el.value = m.val;
        el.dispatchEvent(new Event("input", { bubbles: true }));
        el.dispatchEvent(new Event("change", { bubbles: true }));
        filled++; break;
      }
    }
  });
  return filled;
}

// ---------- history ----------
function renderHistory(surveys) {
  const ul = $("#history-list");
  if (!surveys.length) { ul.innerHTML = `<div class="empty">No surveys yet.</div>`; return; }
  ul.innerHTML = surveys.map((s) => `
    <li class="item">
      <div class="top">
        <span class="merchant">${esc(s.merchant)}</span>
        <span class="badge ${s.status}">${s.status}</span>
        <span class="date">${esc(s.date)}</span>
      </div>
      <div class="desc">${esc(s.reward || "—")}</div>
    </li>`).join("");
}

// ---------- rewards ----------
function renderRewards(surveys) {
  const ul = $("#rewards-list");
  const rewarded = surveys.filter((s) => s.code);
  if (!rewarded.length) { ul.innerHTML = `<div class="empty">No reward codes yet.</div>`; return; }
  ul.innerHTML = rewarded.map((s) => `
    <li class="item">
      <div class="top">
        <span class="merchant">${esc(s.merchant)}</span>
        <span class="date">redeem by ${esc(s.redeemBy || "—")}</span>
      </div>
      <div class="desc">${esc(s.reward)}</div>
      <span class="code" data-code="${esc(s.code)}" title="Click to copy">${esc(s.code)}</span>
      ${s.value ? `<span class="val">$${Number(s.value).toFixed(2)}</span>` : ""}
    </li>`).join("");
  ul.querySelectorAll(".code").forEach((el) => {
    el.addEventListener("click", () => {
      navigator.clipboard.writeText(el.dataset.code);
      const prev = el.textContent;
      el.textContent = "Copied ✓";
      setTimeout(() => (el.textContent = prev), 1200);
    });
  });
}

function renderTotal(surveys) {
  const total = surveys.reduce((sum, s) => sum + (s.code ? Number(s.value || 0) : 0), 0);
  $("#total").textContent = "$" + total.toFixed(2);
}

// ---------- footer actions ----------
$("#add-demo").addEventListener("click", async () => {
  const { surveys = [] } = await store.get(["surveys"]);
  const picks = [
    { merchant: "Chick-fil-A", url: "https://www.mycfavisit.com", reward: "FREE Sandwich (emailed)", value: 4.19, code: "FB-Q8Z2K", redeemBy: "2026-08-20" },
    { merchant: "Panera Bread", url: "https://www.paneralistens.com", reward: "FREE Pastry", value: 3.29, code: "FB-R5N7T", redeemBy: "2026-08-19" },
    { merchant: "Wendy's", url: "https://www.talktowendys.com", reward: "FREE Small Frosty", value: 1.99, code: "FB-W3D6L", redeemBy: "2026-08-18" },
  ];
  const pick = picks[surveys.length % picks.length];
  surveys.unshift({ id: "s" + Date.now(), date: "2026-07-18", status: "claimed", ...pick });
  await store.set({ surveys });
  await renderAll();
});

$("#reset").addEventListener("click", async () => {
  await store.set({ profile: { ...DEFAULT_PROFILE }, surveys: [], seeded: false });
  await init();
});

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

init();
