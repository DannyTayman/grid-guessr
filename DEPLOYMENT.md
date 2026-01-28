# Deployment Guide for Grid Guessr

## Quick Deployment Options

### 🚀 Railway (Easiest - Recommended)

**Why Railway?**
- Free tier available
- Auto-detects FastAPI
- Easy to use
- Good for hobby projects

**Steps:**
1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo" (or "Empty Project" to upload manually)
3. If using GitHub:
   - Connect your GitHub account
   - Select your grid_guessr repository
   - Railway will auto-detect it's a Python project
4. If uploading manually:
   - Create empty project
   - Use Railway CLI or drag/drop your files
5. Railway will automatically:
   - Install dependencies from requirements.txt
   - Start your app with uvicorn
6. Get your public URL from Railway dashboard
7. **Important**: Update game.html if needed to use your Railway URL

**Environment Variables:** None needed for basic setup

---

### ☁️ Render (Also Easy)

**Steps:**
1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository (or upload via Git)
4. Configure:
   - **Name**: grid-guessr
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn grid_guessr:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Wait for deployment (5-10 minutes)
7. Get your URL: `https://grid-guessr.onrender.com`

**Free Tier Notes:**
- App sleeps after 15 min of inactivity
- First load after sleep takes ~30 seconds

---

### 🛩️ Fly.io (More Control)

**Prerequisites:**
- Install flyctl: `curl -L https://fly.io/install.sh | sh`

**Steps:**
1. Create `fly.toml` file (see below)
2. Run: `fly launch`
3. Follow prompts:
   - Choose app name
   - Select region
   - Don't deploy Postgres
4. Run: `fly deploy`
5. Access at: `https://your-app-name.fly.dev`

**fly.toml:**
```toml
app = "grid-guessr"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

---

### 🔒 Vercel (Serverless)

**Note**: Requires slight modifications for serverless

**Steps:**
1. Create `vercel.json`:
```json
{
  "builds": [
    {
      "src": "grid_guessr.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "grid_guessr.py"
    }
  ]
}
```

2. Install Vercel CLI: `npm i -g vercel`
3. Run: `vercel`
4. Follow prompts

---

### 🌐 ngrok (Temporary Sharing)

**Best for:** Testing with friends before deploying

**Steps:**
1. Install ngrok: https://ngrok.com/download
2. Run your app locally: `python run.py`
3. In another terminal: `ngrok http 8000`
4. Share the https URL ngrok gives you

**Limitations:**
- URL changes each time
- Free tier has limits
- Not for permanent hosting

---

## Post-Deployment Checklist

After deploying, you may need to update `game.html`:

### If your maps aren't loading:

Change line 78 in `new_round()` function in `grid_guessr.py`:

**Current (for local):**
```python
return {
    "image": f"/maps/{LEVELS[level]}/{filename}"
}
```

**For deployed:**
```python
return {
    "image": f"https://your-app.railway.app/maps/{LEVELS[level]}/{filename}"
}
```

Or keep it relative and it should work!

---

## Uploading Your Map Images

Your map folders are large. Here's how to handle them:

### Option 1: Include in Git (if small enough)
- Total size < 100MB: Just commit everything
- Add to `.gitignore` if too large

### Option 2: Use Cloud Storage
1. Upload maps to AWS S3, Google Cloud Storage, or Cloudinary
2. Update `new_round()` to return cloud URLs
3. Much faster deployments

### Option 3: Railway/Render Persistent Storage
- Both platforms offer persistent storage volumes
- Useful for large files

---

## Recommended Approach for You

**For your first deployment, I recommend Railway:**

1. Create a GitHub repo with your project
2. Push all files including map folders (if < 500MB total)
3. Connect to Railway
4. Deploy
5. Test
6. Share the URL!

**Time estimate:** 15-30 minutes including signup

---

## Monitoring & Debugging

After deployment:

### Check Logs
- **Railway**: Dashboard → Deployments → View Logs
- **Render**: Dashboard → Logs tab
- **Fly.io**: `fly logs`

### Common Issues

**Maps not loading:**
- Check file paths are correct
- Verify folders uploaded
- Check logs for 404 errors

**App crashes on startup:**
- Check logs for Python errors
- Verify requirements.txt is correct
- Check Python version (use 3.11+)

**CORS errors:**
- Already handled with `allow_origins=["*"]`
- If issues persist, add specific domain

---

## Need Help?

Let me know which platform you choose and I can help troubleshoot!
