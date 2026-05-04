/**
 * CraveAI — script.js
 * Connects the static UI to the FastAPI backend at /api/v1/recommend.
 * Backend URL can be overridden by setting window.API_BASE_URL before this script loads.
 */

// ── CONFIG ────────────────────────────────────────────────────
const API_BASE = window.API_BASE_URL || "http://localhost:8000";
const ENDPOINT = `${API_BASE}/api/v1/recommend`;

// ── DOM REFERENCES ────────────────────────────────────────────
const inputLocation  = document.getElementById("input-location");
const inputCuisines  = document.getElementById("input-cuisines");
const inputPrefs     = document.getElementById("input-prefs");
const inputRating    = document.getElementById("input-rating");
const ratingVal      = document.getElementById("rating-val");
const budgetTabs     = document.querySelectorAll(".budget-tab");
const btnRecommend   = document.getElementById("btn-recommend");
const btnReset       = document.getElementById("btn-reset");
const resultsGrid    = document.getElementById("results-grid");
const loadingState   = document.getElementById("loading-state");
const emptyState     = document.getElementById("empty-state");
const resultsHeader  = document.getElementById("results-header");

// ── STATE ─────────────────────────────────────────────────────
let selectedBudget = "medium";

// ── BUDGET TAB SELECTION ──────────────────────────────────────
budgetTabs.forEach(tab => {
  tab.addEventListener("click", () => {
    budgetTabs.forEach(t => t.classList.remove("active"));
    tab.classList.add("active");
    selectedBudget = tab.dataset.value;
  });
});

// ── RATING SLIDER ─────────────────────────────────────────────
inputRating.addEventListener("input", () => {
  const v = parseFloat(inputRating.value);
  ratingVal.textContent = v.toFixed(1);
  // Update track fill
  const pct = (v / 5) * 100;
  inputRating.style.background =
    `linear-gradient(to right, var(--red) ${pct}%, var(--gray-200) ${pct}%)`;
});

// ── SHOW / HIDE HELPERS ───────────────────────────────────────
function showLoading() {
  resultsGrid.innerHTML   = "";
  resultsHeader.style.display = "none";
  loadingState.style.display  = "block";
  emptyState.style.display    = "none";
}

function showEmpty() {
  loadingState.style.display  = "none";
  resultsGrid.innerHTML   = "";
  resultsHeader.style.display = "none";
  emptyState.style.display    = "flex";
}

function showResults(recs) {
  loadingState.style.display  = "none";
  emptyState.style.display    = "none";
  resultsHeader.style.display = "flex";
  resultsGrid.innerHTML       = recs.map(buildCard).join("");
}

// ── CARD BUILDER ──────────────────────────────────────────────
function starIcon() {
  return `<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
  </svg>`;
}

function buildCard(rec) {
  const rating   = rec.rating        ? parseFloat(rec.rating).toFixed(1) : "N/A";
  const cost     = rec.estimated_cost || "N/A";
  const cuisines = Array.isArray(rec.cuisines) ? rec.cuisines.join(" • ") : (rec.cuisines || "");
  const name     = rec.restaurant_name || "Unknown";
  const explain  = rec.explanation   || "";

  return `
    <div class="card">
      <div class="card-top">
        <div class="card-rating-badge">${starIcon()} ${rating}</div>
        <button class="card-heart" aria-label="Save">
          <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M4.318 6.318a4.5 4.5 0 016.364 0L12 7.636l1.318-1.318a4.5 4.5 0 116.364 6.364L12 20.364l-7.682-7.682a4.5 4.5 0 010-6.364z"/>
          </svg>
        </button>
      </div>

      <div class="card-name">${escapeHtml(name)}</div>

      <div class="card-meta">
        ${cuisines ? `${escapeHtml(cuisines)} • ` : ""}₹${escapeHtml(String(cost))} for two
      </div>

      ${explain ? `
      <div class="card-insight">
        <div class="insight-header">
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>
          </svg>
          AI INSIGHT
        </div>
        <p class="insight-text">"${escapeHtml(explain)}"</p>
      </div>` : ""}
    </div>`;
}

// ── SAFETY ────────────────────────────────────────────────────
function escapeHtml(str) {
  const d = document.createElement("div");
  d.textContent = str;
  return d.innerHTML;
}

// ── MAIN: FETCH RECOMMENDATIONS ───────────────────────────────
async function fetchRecommendations() {
  const location = inputLocation.value.trim();
  const cuisines = inputCuisines.value.trim();
  const minRating = parseFloat(inputRating.value);
  const extraPrefs = inputPrefs.value.trim();

  if (!location) {
    inputLocation.focus();
    inputLocation.style.border = "1px solid var(--red)";
    setTimeout(() => (inputLocation.style.border = ""), 1500);
    return;
  }

  btnRecommend.disabled = true;
  btnRecommend.textContent = "Finding...";
  showLoading();

  const payload = {
    location,
    cuisines: cuisines ? cuisines.split(",").map(s => s.trim()).filter(Boolean) : ["Any"],
    budget: {
      mode: "category",
      category: selectedBudget,
    },
    min_rating: minRating,
    max_rating: 5.0,
    extra_preferences: extraPrefs
      ? extraPrefs.split(",").map(s => s.trim()).filter(Boolean)
      : [],
  };

  try {
    const res  = await fetch(ENDPOINT, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(`Server error: ${res.status}`);

    const data = await res.json();

    if (data.ok && Array.isArray(data.recommendations) && data.recommendations.length > 0) {
      showResults(data.recommendations);
    } else {
      showEmpty();
    }
  } catch (err) {
    console.error("API error:", err);
    showEmpty();
  } finally {
    btnRecommend.disabled = false;
    btnRecommend.innerHTML = `
      <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
      </svg>
      Get Recommendations`;
  }
}

// ── RESET ─────────────────────────────────────────────────────
function resetFilters() {
  inputLocation.value = "Bellandur";
  inputCuisines.value = "Italian, Indian";
  inputPrefs.value    = "";
  inputRating.value   = "3.5";
  ratingVal.textContent = "3.5";
  inputRating.style.background = "linear-gradient(to right, var(--red) 70%, var(--gray-200) 70%)";
  budgetTabs.forEach(t => t.classList.toggle("active", t.dataset.value === "medium"));
  selectedBudget = "medium";

  resultsGrid.innerHTML       = "";
  resultsHeader.style.display = "none";
  loadingState.style.display  = "none";
  emptyState.style.display    = "flex";
}

// ── EVENTS ────────────────────────────────────────────────────
btnRecommend.addEventListener("click", fetchRecommendations);
btnReset.addEventListener("click", resetFilters);

// Allow pressing Enter in text inputs to trigger search
[inputLocation, inputCuisines, inputPrefs].forEach(el => {
  el.addEventListener("keydown", e => {
    if (e.key === "Enter") fetchRecommendations();
  });
});

// ── INIT ──────────────────────────────────────────────────────
// Show empty state on page load
emptyState.style.display = "flex";
