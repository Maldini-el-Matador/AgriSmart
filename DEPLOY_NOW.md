# AgriSmart - Complete Deployment Guide

This guide will deploy AgriSmart with:
- **Backend API**: Render (free tier with auto-sleep)
- **Database**: PostgreSQL on Render (free tier)
- **Frontend**: Streamlit Community Cloud (free)
- **Domain**: Free subdomain (e.g., `yourapp.onrender.com` and `yourapp.streamlit.app`)

---

## Prerequisites

1. **GitHub account** - [github.com](https://github.com)
2. **Render account** - [render.com](https://render.com) (sign up with GitHub)
3. **Streamlit Community Cloud account** - [share.streamlit.io](https://share.streamlit.io) (sign up with GitHub)

---

## Step 1: Push to GitHub

### 1.1 Create a new repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Name: `AgriSmart` (or your preferred name)
3. Choose **Public** (required for free tiers)
4. **Do NOT** initialize with README (you already have one)
5. Click **Create repository**

### 1.2 Push your code

Open **PowerShell** or **Command Prompt** in your AgriSmart folder and run:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Check what will be committed
git status

# Commit
git commit -m "Initial commit: AgriSmart full-stack app"

# Add your GitHub repo as remote (replace YOUR_USERNAME)
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/AgriSmart.git

# Push to GitHub
git push -u origin main
```

**Enter your GitHub credentials when prompted.**

If you use 2FA, create a **Personal Access Token**:
- GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
- Select scopes: `repo` (full control)
- Use the token as your password when pushing

---

## Step 2: Deploy Backend + Database on Render

### 2.1 Sign up on Render

1. Go to [render.com](https://render.com)
2. Click **Get Started** → **Sign up with GitHub**
3. Authorize Render to access your GitHub repositories

### 2.2 Deploy using Blueprint

1. In Render dashboard, click **New** → **Blueprint**
2. Connect your GitHub repository: `YOUR_USERNAME/AgriSmart`
3. Render will detect `render.yaml` and show:
   - **Database**: `agrismart-db` (PostgreSQL free tier)
   - **Web Service**: `agrismart-backend` (Python web service)
4. Click **Apply** and wait 5-10 minutes for deployment

**What happens:**
- Render creates a free PostgreSQL database
- Deploys the FastAPI backend
- Sets `DATABASE_URL` automatically
- Your backend will be at: `https://agrismart-backend.onrender.com`

### 2.3 Verify backend deployment

Once deployed, click on the **agrismart-backend** service and:
1. Copy the URL (e.g., `https://agrismart-backend-xxxx.onrender.com`)
2. Open in browser: `https://agrismart-backend-xxxx.onrender.com/health`
3. You should see: `{"status":"ok","service":"agrismart-api"}`

**Important**: Free tier backends **spin down after 15 minutes of inactivity**. The first request after sleep takes ~30-60 seconds to wake up.

---

## Step 3: Deploy Frontend on Streamlit Cloud

### 3.1 Sign up on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **Sign in** → **Continue with GitHub**
3. Authorize Streamlit

### 3.2 Deploy your app

1. Click **New app**
2. Select:
   - **Repository**: `YOUR_USERNAME/AgriSmart`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **Advanced settings**
4. Add **Environment variables** (Secrets):
   ```
   BACKEND_URL = "https://agrismart-backend-xxxx.onrender.com"
   ```
   (Use your actual backend URL from Step 2.3)
5. Click **Deploy**

Wait 2-5 minutes. Your frontend will be at:
- `https://YOUR_USERNAME-agrismart.streamlit.app`
- or `https://agrismart.streamlit.app` (if available)

### 3.3 Test the deployment

1. Open your Streamlit app URL
2. Check sidebar - it should show **Backend connected**
3. Upload a leaf image + enter location/district
4. Click **Run analysis**
5. Check **History** page

---

## Step 4: Custom Domain (Optional)

### Free subdomain options

**Backend**: Render gives you `yourapp.onrender.com` (free)

**Frontend**: Streamlit gives you `yourapp.streamlit.app` (free)

### Custom domain (paid or free)

If you have a custom domain:
- **Render**: Settings → Custom Domains → Add your domain
- **Streamlit**: Not supported on free tier

For a **free domain** (e.g., `.tk`, `.ml`, `.ga`):
1. Register at [Freenom](https://www.freenom.com)
2. Point DNS to your Render/Streamlit URLs (CNAME record)

---

## Troubleshooting

### Backend issues

**Check logs**: Render dashboard → agrismart-backend → Logs

Common issues:
1. **Model/CSV files not in repo**: Make sure `backend/plant_disease_recognition_model/*.h5` and `backend/ifs_recommender/*.csv` are committed to GitHub
2. **Build fails**: Check `backend/api/requirements.txt` - TensorFlow might take 5-10 minutes to install
3. **Health check fails**: Check logs for Python errors

### Frontend issues

**Check logs**: Streamlit dashboard → Your app → Manage app → Logs

Common issues:
1. **Backend not connected**: Check `BACKEND_URL` in secrets (must match Render backend URL)
2. **Import errors**: Make sure `requirements.txt` is in repo root

### Database issues

**Connection string**: Render → Dashboard → agrismart-db → Info → Internal/External Connection String

The backend automatically uses the internal connection string from `DATABASE_URL`.

---

## Cost Summary

| Service | Tier | Cost | Limits |
|---------|------|------|--------|
| **Render Backend** | Free | $0/month | Spins down after 15 min inactivity; 750 hours/month |
| **Render PostgreSQL** | Free | $0/month | 1 GB storage, 97 connection limit |
| **Streamlit Cloud** | Community | $0/month | 1 app, public repos only |

**Total: $0/month** with free subdomains!

---

## Next Steps

1. **Monitor**: Check logs on Render and Streamlit dashboards
2. **Improve cold starts**: Free tier spins down; consider upgrading to paid ($7/month on Render) for 24/7 uptime
3. **Add features**: The app is now live; you can push updates by committing to GitHub (auto-deploys)

---

## Important Notes

- **Large files**: If your model files (`.h5`, `.keras`) are over 100 MB, GitHub will reject them. Use [Git LFS](https://git-lfs.github.com/) or upload them directly to Render via a custom build script.
- **Cold start time**: First request after sleep on free tier can take 30-60 seconds (loading TensorFlow model).
- **Rate limits**: OpenStreetMap (geocoding for IFS) has rate limits; consider caching or using district directly.

Your app is now deployed! 🎉
