# 🚀 Deploy AgriSmart in 3 Clicks

## Your GitHub Repository
✅ **DONE**: https://github.com/Maldini-el-Matador/AgriSmart

---

## Step 1: Deploy Backend (Click Here)

### 🔗 [Deploy on Render (Blueprint)](https://dashboard.render.com/select-repo?type=blueprint)

1. **Sign in with GitHub** on Render
2. **Select repository**: `Maldini-el-Matador/AgriSmart`
3. **Click "Apply"** (Render will read `render.yaml` automatically)
4. **Wait 5-10 minutes** for build to complete
5. **Copy your backend URL** from the dashboard (looks like `https://agrismart-backend-xxxx.onrender.com`)

---

## Step 2: Deploy Frontend (Click Here)

### 🔗 [Deploy on Streamlit Cloud](https://share.streamlit.io/deploy)

1. **Sign in with GitHub**
2. **Fill in the form**:
   - Repository: `Maldini-el-Matador/AgriSmart`
   - Branch: `main`
   - Main file: `app.py`
3. **Click "Advanced settings"**
4. **Add secret** (paste this, replacing YOUR-BACKEND-URL):
   ```toml
   BACKEND_URL = "https://YOUR-BACKEND-URL-FROM-STEP-1"
   ```
5. **Click "Deploy"**
6. **Wait 2-5 minutes**

---

## Step 3: Test Your App

Your app will be live at:
- `https://maldini-el-matador-agrismart-app-xxxx.streamlit.app`

Test:
1. Upload a leaf image
2. Enter a location or district
3. Click "Run analysis"
4. See results and history

---

## 💰 Cost: $0/month

Everything runs on free tiers:
- Render Backend: Free (sleeps after 15 min)
- Render PostgreSQL: Free (1 GB)
- Streamlit Cloud: Free

---

## Need Help?

See **DEPLOYMENT_CHECKLIST.md** for detailed troubleshooting and tips.
