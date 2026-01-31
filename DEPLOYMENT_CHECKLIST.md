# 🎉 AgriSmart - Quick Deployment Checklist

Your code is now on GitHub: **https://github.com/Maldini-el-Matador/AgriSmart**

## ✅ Step 1: Code on GitHub - COMPLETE

Your repository is live and ready for deployment.

---

## 🚀 Step 2: Deploy Backend on Render (5-10 minutes)

1. **Go to Render**: https://dashboard.render.com

2. **Sign up / Sign in with GitHub**
   - Click "Get Started" → "GitHub"
   - Authorize Render

3. **Create a new Blueprint**
   - Dashboard → "New" → "Blueprint"
   - Connect repository: `Maldini-el-Matador/AgriSmart`
   - Render will detect `render.yaml`
   - Click "Apply"

4. **Wait for deployment** (5-10 minutes)
   - Database: `agrismart-db` (PostgreSQL) - will create first
   - Backend: `agrismart-backend` - will build and deploy

5. **Get your backend URL**
   - Click on `agrismart-backend` service
   - Copy the URL (e.g., `https://agrismart-backend-xxxx.onrender.com`)
   - **Test it**: Open `https://YOUR-BACKEND-URL/health` in browser
   - Should show: `{"status":"ok","service":"agrismart-api"}`

6. **Check for errors** (if deployment fails)
   - Click on `agrismart-backend` → "Logs"
   - Common issues:
     - Model files > 100MB: See note below
     - Build timeout: Retry or upgrade to paid tier

---

## 📱 Step 3: Deploy Frontend on Streamlit Cloud (2-5 minutes)

1. **Go to Streamlit Cloud**: https://share.streamlit.io

2. **Sign in with GitHub**

3. **Create new app**
   - Click "New app"
   - Repository: `Maldini-el-Matador/AgriSmart`
   - Branch: `main`
   - Main file: `app.py`

4. **Add secrets (IMPORTANT)**
   - Click "Advanced settings" before deploying
   - Add to "Secrets":
     ```toml
     BACKEND_URL = "https://YOUR-BACKEND-URL-FROM-STEP-2"
     ```
   - Replace with your actual Render backend URL (no trailing slash)

5. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes

6. **Your app URL**
   - Will be: `https://maldini-el-matador-agrismart-app-xxxx.streamlit.app`
   - or similar

---

## ✅ Step 4: Test Your Live App

1. **Open your Streamlit URL**

2. **Check sidebar**
   - Should show "✅ Backend connected"
   - If not: check BACKEND_URL in Streamlit secrets

3. **Run analysis**
   - Upload a leaf image (JPG/PNG)
   - Enter location OR district
   - Click "Run analysis"
   - Should see disease detection + IFS recommendations

4. **Check History**
   - Click "History" in sidebar
   - Should show your query

---

## ⚠️ Important Notes

### Large Model Files

If your `.h5` or `.keras` files are > 100 MB, GitHub will reject them. Solutions:

**Option A: Git LFS** (Large File Storage)
```powershell
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.h5"
git lfs track "*.keras"

# Add, commit, push
git add .gitattributes
git add backend/plant_disease_recognition_model/*.h5
git commit -m "Add model files with Git LFS"
git push origin main
```

**Option B: Upload to cloud storage**
- Upload models to Google Drive, Dropbox, or AWS S3
- Modify `disease.py` to download the model on first startup

### Free Tier Limitations

- **Backend**: Spins down after 15 min of inactivity
- **First request**: Takes 30-60 seconds to wake up + load TensorFlow
- **Database**: 1 GB limit (plenty for this app)
- **Uptime**: Not 24/7 (sleeps when inactive)

### Upgrading (Optional)

For 24/7 uptime and faster response:
- Render: $7/month per service (backend stays awake)
- Streamlit: Free tier is fine for most uses

---

## 🌐 Your Live URLs

Once deployed, bookmark these:

- **Frontend**: `https://maldini-el-matador-agrismart-app-xxxx.streamlit.app`
- **Backend**: `https://agrismart-backend-xxxx.onrender.com`
- **Backend Health**: Add `/health` to backend URL
- **Backend Check**: Add `/check` to see if model files are found

---

## 🐛 Troubleshooting

### Backend won't start

1. Check Render logs: Dashboard → agrismart-backend → Logs
2. Look for:
   - `FileNotFoundError`: Model or CSV file missing from GitHub
   - `MemoryError`: Free tier RAM limit (512MB) exceeded
   - Module import errors: Check `requirements.txt`

### Frontend shows "Backend not connected"

1. Check BACKEND_URL in Streamlit secrets (must match Render URL exactly)
2. Test backend directly: open `https://YOUR-BACKEND-URL/health`
3. Check Render logs for errors

### 500 error on "Run analysis"

1. Check Streamlit frontend - shows error detail
2. Check Render backend logs - shows full Python traceback
3. Common causes:
   - Model file missing
   - CSV file missing
   - Database connection issue

---

## 📝 Next Steps After Deployment

1. **Share your app**: Send the Streamlit URL to users
2. **Monitor usage**: Check Render and Streamlit dashboards
3. **Update app**: Push to GitHub → auto-deploys
4. **Add custom domain** (optional): Configure in Render/Streamlit settings

---

🎉 **Congratulations!** Your AgriSmart app is now live on the internet with free hosting and a free subdomain!
