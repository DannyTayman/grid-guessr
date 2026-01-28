# Grid Guessr - Setup and Run Guide

## Issues Fixed in Your Code

1. **App initialization error**: You had `app.add_middleware()` before `app = FastAPI()`
2. **Duplicate BASE_DIR definition**: Removed duplicate
3. **Duplicate normalize_city function**: Removed duplicate
4. **Missing Pydantic model**: Added proper request validation
5. **Hardcoded URLs**: Changed to relative paths for local development
6. **Missing error handling**: Added checks for missing folders

## Project Structure

```
grid_guessr/
├── grid_guessr.py       # FastAPI backend
├── home.html            # Home page
├── game.html            # Game page
├── static/              # Static assets
│   └── previews/        # Preview images
│       ├── nyc.jpg
│       ├── pit.jpg
│       ├── lub.jpg
│       ├── tor.jpg
│       ├── det.jpg
│       └── yel.jpg
├── USA_easy/            # Map images folder
├── USA_med/             # Map images folder
├── USA_extreme/         # Map images folder
├── NA_easy/             # Map images folder
├── NA_med/              # Map images folder
└── NA_extreme/          # Map images folder
```

## Installation Steps

### 1. Install Dependencies

```bash
pip install fastapi uvicorn --break-system-packages
```

### 2. Copy Your Files

Make sure your folder structure matches above. Place all your map folders (USA_easy, USA_med, etc.) in the same directory as `grid_guessr.py`.

### 3. Add Preview Images

Place preview images in `static/previews/` folder.

## Running Locally

### Option 1: Using uvicorn directly

```bash
cd grid_guessr
uvicorn grid_guessr:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Using the run script

```bash
cd grid_guessr
python run.py
```

Then open your browser to: **http://localhost:8000**

## Making it Shareable

### Option 1: Deploy to Railway (Recommended)

1. Create account at https://railway.app
2. Create new project
3. Connect your GitHub repo or upload files
4. Add environment variables if needed
5. Railway will auto-detect FastAPI and deploy

### Option 2: Deploy to Fly.io

1. Install flyctl: https://fly.io/docs/hands-on/install-flyctl/
2. Run `fly launch` in your project directory
3. Follow the prompts
4. Run `fly deploy`

### Option 3: Deploy to Render

1. Create account at https://render.com
2. New → Web Service
3. Connect your repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn grid_guessr:app --host 0.0.0.0 --port $PORT`

### Option 4: Share via ngrok (temporary)

```bash
# Install ngrok
# Then run your app locally and in another terminal:
ngrok http 8000
```

This gives you a public URL that works for a few hours (free tier).

## Files Needed for Deployment

### requirements.txt
```
fastapi
uvicorn
python-multipart
```

### Procfile (for some platforms)
```
web: uvicorn grid_guessr:app --host 0.0.0.0 --port $PORT
```

## Troubleshooting

**Problem**: "No maps found" error
- **Solution**: Make sure your map folders (USA_easy, etc.) are in the same directory as grid_guessr.py

**Problem**: Preview images not loading
- **Solution**: Make sure images are in `static/previews/` folder

**Problem**: Port already in use
- **Solution**: Use a different port: `uvicorn grid_guessr:app --port 8001`

**Problem**: CORS errors when deployed
- **Solution**: Update the CORS origins in grid_guessr.py to include your deployment URL

## Next Steps

1. Test locally first
2. Once working, choose a deployment platform
3. Update the domain in your code if needed
4. Share the link!
