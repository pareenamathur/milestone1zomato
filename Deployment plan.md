# Deployment Plan: Render (Backend) + Vercel (Frontend)

Deploy the **CraveAI** Restaurant Recommender as two independent services on free-tier cloud platforms. 

This plan covers deploying the new **standalone HTML/JS UI** we just created in `src/milestone_1/phase_5_output/ui/` on Vercel, and the FastAPI backend on Render.

---

## Architecture After Deployment

```
User → Vercel (CraveAI Static UI) → Render (FastAPI) → Groq API
```

---

## Part 1 — Backend on Render

### What Render needs
| File | Status |
|---|---|
| `Dockerfile` | ✅ Ready (Fixed for production, no secrets baked in) |
| `render.yaml` | ✅ Ready (One-click deployment config) |

### Steps

1. **Go to** [render.com](https://render.com) → Sign in with GitHub
2. **New → Web Service** 
3. Connect your repository `pareenamathur/milestone1zomato`
4. Render should automatically detect `render.yaml`. 
5. In the Render dashboard, you **must manually set these Environment Variables**:
   - `GROQ_API_KEY`: Your Groq API key
   - `M1_GROQ_API_KEY`: Your Groq API key (same as above)
   - `FRONTEND_URL`: Leave blank for now, you will update this after Vercel is deployed.
6. Click **Deploy** — Render builds the Docker image and starts the FastAPI server.
7. After deploy, copy the public URL (e.g., `https://milestone1zomato.onrender.com`)

> [!IMPORTANT]
> Free Render instances **spin down after 15 minutes of inactivity** and take ~30s to wake up on the next request. This is a free-tier limitation.

---

## Part 2 — Frontend on Vercel

Since we just built a new vanilla HTML/CSS/JS frontend, the deployment is incredibly fast as it's purely static.

### Steps

1. **Go to** [vercel.com](https://vercel.com) → Sign in with GitHub
2. **Add New Project** → Import `pareenamathur/milestone1zomato`
3. Configure the Project:
   | Setting | Value |
   |---|---|
   | Framework Preset | Other |
   | Root Directory | `src/milestone_1/phase_5_output/ui` |
   | Build Command | *(leave empty)* |
   | Output Directory | *(leave empty)* |
4. Click **Deploy** — Vercel will instantly publish your static files.
5. Your app is live at `https://<your-project>.vercel.app`

### Linking Frontend to Backend

Because this is a static frontend, `script.js` uses `window.API_BASE_URL` to know where the backend is. By default, it points to `http://localhost:8000`.

To point it to Render, we will need to create a `vercel.json` in the `ui` folder that sets up an API proxy, OR inject the Render URL into `index.html`. 

**Proposed Action before you deploy:**
I will create a `vercel.json` file inside `src/milestone_1/phase_5_output/ui/` that rewrites `/api/v1/recommend` to your Render URL. 

---

## Part 3 — Finalizing the Connection

Once both are deployed:
1. Go back to your **Render Dashboard**
2. Update the `FRONTEND_URL` environment variable to your new Vercel URL (e.g., `https://milestone1zomato.vercel.app`).
3. This locks down CORS so that ONLY your Vercel frontend can talk to your backend.

---

## Open Questions

> [!IMPORTANT]
> **Q1**: Would you like me to go ahead and create the `vercel.json` inside the new UI folder so that it's ready for you to deploy?
> 
> **Q2**: Once I create that file, you can follow the steps above on Render and Vercel. Does this plan sound good?
