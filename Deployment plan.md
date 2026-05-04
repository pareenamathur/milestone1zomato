# Deployment Plan: Railway (Backend) + Vercel (Frontend)

Deploy the **CraveAI** Restaurant Recommender as two independent services on modern cloud platforms. 

This plan covers deploying the new **standalone HTML/JS UI** in `src/milestone_1/phase_5_output/ui/` on Vercel, and the FastAPI backend on Railway.

---

## Architecture After Deployment

```
User → Vercel (CraveAI Static UI) → Railway (FastAPI) → Groq API
```

---

## Part 1 — Backend on Railway

### What Railway needs
| File | Status |
|---|---|
| `Dockerfile` | ✅ Ready (Updated for Railway's dynamic `$PORT`) |

### Steps

1. **Go to** [railway.app](https://railway.app/) → Login with GitHub.
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select your repository `pareenamathur/milestone1zomato`.
4. Click **Add Variables** before deploying, and add these:
   - `GROQ_API_KEY`: Your Groq API key
   - `M1_GROQ_API_KEY`: Your Groq API key (same as above)
   - `FRONTEND_URL`: Leave blank for now, you will update this after Vercel is deployed.
5. Click **Deploy**. Railway will automatically detect the `Dockerfile` and build your image.
6. **Generate a Domain**: 
   - Go to the **Settings** tab for your deployed service.
   - Under **Networking**, click **Generate Domain**.
   - Copy the public URL (e.g., `https://milestone1zomato-production.up.railway.app`).

---

## Part 2 — Frontend on Vercel

Since we just built a new vanilla HTML/CSS/JS frontend, the deployment is incredibly fast as it's purely static.

### Steps

1. **Go to** [vercel.com](https://vercel.com) → Sign in with GitHub
2. **Add New Project** → Import `pareenamathur/milestone1zomato`
3. Configure the Project:
   | Setting | Value |
   |---|---|
   | Framework Preset | **Other** (Do not use Next.js!) |
   | Root Directory | `src/milestone_1/phase_5_output/ui` |
   | Build Command | *(leave empty)* |
   | Output Directory | *(leave empty)* |
4. Click **Deploy** — Vercel will instantly publish your static files.
5. Your app is live at `https://<your-project>.vercel.app`

### Linking Frontend to Backend

To point your Vercel frontend to the Railway backend:
1. Open your code editor.
2. Go to `src/milestone_1/phase_5_output/ui/vercel.json`.
3. Change the `destination` line to your exact Railway URL:
   ```json
   "destination": "https://<your-railway-url>.up.railway.app/api/:path*"
   ```
4. Save the file and commit/push to GitHub. Vercel will automatically redeploy with the new configuration.

---

## Part 3 — Finalizing the Connection

Once both are connected:
1. Go back to your **Railway Dashboard**.
2. Go to the **Variables** tab.
3. Update the `FRONTEND_URL` environment variable to your new Vercel URL (e.g., `https://milestone1zomato.vercel.app`).
4. This locks down CORS so that ONLY your Vercel frontend can talk to your backend.
