/**
 * CraveAI — script.js
 * Connects the modern UI to the FastAPI backend.
 */

// ── CONFIG ────────────────────────────────────────────────────
const isLocalhost = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
const API_BASE = isLocalhost ? "http://localhost:8000" : "";
const ENDPOINT = `${API_BASE}/api/v1/recommend`;

// ── DOM REFERENCES ────────────────────────────────────────────
const inputLocation  = document.getElementById("input-location");
const inputCuisines  = document.getElementById("input-cuisines");
const inputPrefs     = document.getElementById("input-prefs");
const inputRating    = document.getElementById("input-rating");
const ratingVal      = document.getElementById("rating-val");
const budgetTabs     = document.querySelectorAll(".budget-tab");
const btnRecommend   = document.getElementById("btn-recommend");
const btnText        = document.getElementById("btn-text");
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
  ratingVal.textContent = parseFloat(inputRating.value).toFixed(1);
});

// ── UI HELPERS ────────────────────────────────────────────────
function showLoading() {
  resultsGrid.innerHTML   = "";
  resultsHeader.style.display = "none";
  loadingState.style.display  = "block";
  emptyState.style.display    = "none";
  btnRecommend.disabled = true;
  btnText.textContent = "Finding restaurants...";
}

function showEmpty(msg) {
  loadingState.style.display  = "none";
  resultsGrid.innerHTML   = "";
  resultsHeader.style.display = "none";
  emptyState.style.display    = "block";
  emptyState.querySelector("p").textContent = msg || 'No matches found. Try broadening your preferences.';
  btnRecommend.disabled = false;
  btnText.textContent = "Find Best Matches";
}

function showResults(recs) {
  loadingState.style.display  = "none";
  emptyState.style.display    = "none";
  resultsHeader.style.display = "flex";
  resultsGrid.innerHTML       = recs.map(buildCard).join("");
  btnRecommend.disabled = false;
  btnText.textContent = "Find Best Matches";
}

// ── CARD BUILDER ──────────────────────────────────────────────
function buildCard(rec) {
  const rating   = rec.rating ? parseFloat(rec.rating).toFixed(1) : "N/A";
  const cost     = rec.estimated_cost || "N/A";
  const cuisines = Array.isArray(rec.cuisines) ? rec.cuisines.join(", ") : (rec.cuisines || "Various");
  const name     = rec.restaurant_name || "Unknown";
  const explain  = rec.explanation || "Highly recommended based on your preferences.";

  return `
    <div class="card">
      <div class="card-badge">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
        ${rating}
      </div>
      <h3 class="card-name">${escapeHtml(name)}</h3>
      <div class="card-meta">
        <div class="meta-item">${escapeHtml(cuisines)}</div>
        <div class="meta-item">|</div>
        <div class="meta-item">₹${escapeHtml(String(cost))} for two</div>
      </div>
      <div class="card-explanation">
        <span class="exp-label">AI Explanation</span>
        ${escapeHtml(explain)}
      </div>
    </div>`;
}

function escapeHtml(str) {
  const d = document.createElement("div");
  d.textContent = str;
  return d.innerHTML;
}

// ── API FETCH ─────────────────────────────────────────────────
async function fetchRecommendations() {
  const location = inputLocation.value.trim();
  if (!location) {
    inputLocation.focus();
    return;
  }

  showLoading();

  const payload = {
    location,
    cuisines: inputCuisines.value ? inputCuisines.value.split(",").map(s => s.trim()) : [],
    budget: { mode: "category", category: selectedBudget },
    min_rating: parseFloat(inputRating.value),
    extra_preferences: inputPrefs.value ? inputPrefs.value.split(",").map(s => s.trim()) : []
  };

  try {
    const res = await fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error("API Failure");

    const data = await res.json();
    if (data.ok && data.recommendations && data.recommendations.length > 0) {
      showResults(data.recommendations);
    } else {
      showEmpty("We couldn't find matches for those exact filters. Try a different location or lower rating.");
    }
  } catch (err) {
    showEmpty("Connection error. Please ensure the backend is running.");
  }
}

// ── EVENTS ────────────────────────────────────────────────────
btnRecommend.addEventListener("click", fetchRecommendations);

[inputLocation, inputCuisines, inputPrefs].forEach(el => {
  el.addEventListener("keydown", e => {
    if (e.key === "Enter") fetchRecommendations();
  });
});
