# Phase-wise architecture: AI-powered restaurant recommender (Zomato use case)

This document translates `Docs/problemstatement.md` into an implementation-ready, phase-by-phase architecture. Each phase has a clear purpose, core components, and concrete outputs.

## Phase 0 — Project foundation (contracts + configuration)
**Goal**: Establish stable interfaces so later phases can evolve independently.

- **Core components**
  - **Configuration**: dataset source, column mapping, defaults (top-K), thresholds (min rating), and LLM settings
  - **Data contracts (schemas)**:
    - `UserPreferences`: location, budget, cuisine(s), min_rating, extra_preferences
    - `RestaurantRecord`: normalized restaurant fields
    - `CandidateSet`: reduced candidate list prepared for ranking
    - `Recommendation`: ranked results + explanations for display
- **Outputs**
  - Agreed schemas and config layout used by all phases

## Phase 1 — Data ingestion & preprocessing
**Goal**: Load the dataset and normalize it into a reliable, queryable form.

- **Core components**
  - **Dataset loader**: fetches `ManikaSaini/zomato-restaurant-recommendation` from Hugging Face
  - **Preprocessor/normalizer**:
    - standardizes location (city), cuisine list, rating type, and cost/price representation
    - handles missing or malformed values
  - **Feature extraction** (derived fields):
    - `price_category` (e.g., low/medium/high) derived from cost
    - canonical cuisine tags (lowercased/trimmed)
  - **Storage/cache**:
    - persist cleaned dataset to a local file (CSV/Parquet) for fast startup
- **Outputs**
  - Clean `RestaurantRecord[]` (or dataframe) ready for filtering

## Phase 2 — User input collection & validation
**Goal**: Collect preferences and transform them into a consistent internal representation.

- **Core components**
  - **Input layer (Milestone 1 choice)**: **basic web UI** (simple form to collect preferences)
  - **Validator**:
    - required fields: location, budget, cuisine, min_rating
    - validates allowed ranges (e.g., rating 0–5)
  - **Normalizer**:
    - converts budget to a numeric range or category
    - splits and canonicalizes cuisines
- **Outputs**
  - Validated `UserPreferences`

## Phase 3 — Candidate selection (structured filtering + lightweight ranking)
**Goal**: Produce a small, high-quality candidate list using deterministic logic before calling the LLM.

- **Core components**
  - **Filter engine** (hard constraints):
    - location match
    - rating >= min_rating
    - cuisine match (any/all depending on UX choice)
    - cost fits budget range/category
  - **Lightweight scoring (optional but recommended)**:
    - boosts higher ratings, closer budget match, stronger cuisine match
  - **Candidate reducer**:
    - selects top N (e.g., 25–50) to keep the LLM prompt compact
- **Outputs**
  - `CandidateSet` with the key fields needed for ranking and display

## Phase 4 — LLM integration (ranking + explanations)
**Goal**: Use the LLM to rank candidates and generate short, preference-aware explanations.

- **Core components**
  - **Prompt builder**
    - includes user preferences + compact candidate list
    - instructs the model to only use provided candidates
    - requests a structured response (recommended: JSON)
  - **LLM client**
    - handles API calls, retries, timeouts, and token limits
  - **Response validator/parser**
    - validates schema, enforces that restaurant IDs/names exist in the candidate list
    - fallback behavior if parsing fails (use Phase 3 heuristic ranking)
- **Outputs**
  - Ranked `Recommendation[]` with 1–3 sentence explanations

## Phase 5 — Presentation layer (results display)
**Goal**: Display recommendations in a clear, consistent format.

- **Core components**
  - **Renderer**
    - prints/displays top K recommendations
    - consistent fields: name, cuisine, rating, estimated cost, explanation
  - **User experience details**
    - show “no results” guidance (e.g., widen budget or lower rating)
    - optionally show “why these were selected” as short bullets
- **Outputs**
  - User-facing results view

## Phase 6 — Quality, evaluation, and hardening
**Goal**: Make the system reliable and measurable.

- **Core components**
  - **Testing**
    - unit tests for parsing, filtering, normalization
    - contract tests for LLM response schema parsing
  - **Observability**
    - logs: input summary, filter counts, latency, LLM failures, fallback usage
    - metrics: “no results” rate, average response time, token usage (if applicable)
- **Outputs**
  - A stable system that meets the success criteria in `problemstatement.md`

## Phase 7 — Full-Stack Decoupling (Modern Backend & Frontend)
**Goal**: Evolve the monolithic "basic web UI" into a production-ready, fully decoupled full-stack application.

- **Core components**
  - **Backend API (FastAPI)**
    - Expose robust RESTful endpoints (e.g., `POST /api/v1/recommend`) that wrap the Phase 1–4 pipeline.
    - Serve standard JSON responses to any client.
    - Handle CORS, rate limiting, and API security.
  - **Frontend Client (Modern Web App)**
    - Build a dedicated, modern frontend (e.g., using React, Next.js, or Vite).
    - Implement the Phase 5 Presentation layer aesthetics natively in the client with rich, dynamic web design (vibrant colors, glassmorphism, smooth gradients, and micro-animations).
    - Handle client-side state management, loading skeletons during LLM generation, and responsive layouts.
- **Outputs**
  - A decoupled backend API server and a high-fidelity frontend web application.

## Phase 8 — Production Deployment (Render + Vercel)
**Goal**: Deploy the decoupled system to production using free-tier cloud platforms — backend on Render, frontend on Vercel.

- **Core components**
  - **Backend — Render (Docker)**
    - The FastAPI backend is containerized using `Dockerfile` and deployed as a Render Web Service.
    - `render.yaml` provides one-click infrastructure configuration.
    - Secrets (`GROQ_API_KEY`, `FRONTEND_URL`) are injected at runtime via Render's dashboard — never committed to source control.
    - A `/health` endpoint is exposed for Render's uptime monitoring.
  - **Frontend — Vercel (Next.js)**
    - The Next.js frontend is deployed directly from the GitHub repo via Vercel's automatic CI/CD.
    - `NEXT_PUBLIC_API_URL` env var is set in Vercel's dashboard to point to the Render backend URL.
    - `vercel.json` and `next.config.js` handle API proxy rewrites so the frontend never hardcodes backend addresses.
  - **Security**
    - CORS is locked to the Vercel domain via the `FRONTEND_URL` env var on Render.
    - All secrets remain in platform dashboards and `.env` files which are git-ignored.
- **Deployment flow**
  1. Push code to GitHub `main` branch
  2. Render auto-deploys backend from Dockerfile
  3. Vercel auto-deploys frontend from `frontend/` directory
- **Outputs**
  - Backend: `https://<service>.onrender.com` (FastAPI + Swagger docs at `/docs`)
  - Frontend: `https://<project>.vercel.app` (production Next.js app)

## End-to-end flow (summary)
**Backend**: `UserPreferences` → Validation/Normalization → Structured Filter/Score → Top-N `CandidateSet` → Prompt → LLM Rank + Explain → Parse/Validate → JSON API Response
**Frontend**: User Form → Loading State → Fetch API → Render Premium UI

