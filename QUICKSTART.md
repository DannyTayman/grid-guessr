# 🎮 Grid Guessr - Quick Start

## To Run Locally RIGHT NOW:

### Step 1: Copy Your Files
Copy your complete `grid_guessr` folder to a location on your computer.

Make sure it has this structure:
```
grid_guessr/
├── grid_guessr.py       ← Fixed version I created
├── game.html            ← Fixed version I created  
├── home.html            ← Your original
├── run.py               ← Convenience script
├── requirements.txt     ← Dependencies
├── USA_easy/            ← YOUR map files here
├── USA_med/             ← YOUR map files here
├── USA_extreme/         ← YOUR map files here
├── NA_easy/             ← YOUR map files here
├── NA_med/              ← YOUR map files here
├── NA_extreme/          ← YOUR map files here
└── static/
    └── previews/        ← YOUR preview images here
        ├── nyc.jpg
        ├── pit.jpg
        ├── lub.jpg
        ├── tor.jpg
        ├── det.jpg
        └── yel.jpg
```

### Step 2: Install Dependencies
Open terminal/command prompt in the grid_guessr folder and run:

```bash
pip install fastapi uvicorn
```

### Step 3: Run the App
```bash
python run.py
```

Or:
```bash
uvicorn grid_guessr:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Open Browser
Go to: **http://localhost:8000**

---

## What I Fixed:

1. ✅ **App initialization bug** - middleware was being added before app was created
2. ✅ **Duplicate definitions** - removed duplicate BASE_DIR and normalize_city
3. ✅ **API URL** - changed from hardcoded Railway URL to relative paths
4. ✅ **Error handling** - added checks for missing folders
5. ✅ **Type validation** - added Pydantic model for request validation

---

## To Share Online:

See **DEPLOYMENT.md** for full guide. Quick recommendation:

**Railway (Easiest):**
1. Sign up at https://railway.app
2. Create new project from GitHub or upload manually
3. Railway auto-deploys FastAPI apps
4. Get public URL in ~5 minutes

---

## Troubleshooting:

**"uvicorn: command not found"**
→ Run: `pip install uvicorn fastapi`

**"No maps found in USA_easy"**
→ Make sure your map PNG files are in the correct folders

**Preview images not loading**
→ Put .jpg files in `static/previews/` folder

**Port 8000 already in use**
→ Run: `uvicorn grid_guessr:app --port 8001`

---

## Files You Can Download:

I've created fixed versions of your files in `/home/claude/grid_guessr/`:
- `grid_guessr.py` (fixed backend)
- `game.html` (fixed frontend)
- `README.md` (full setup guide)
- `DEPLOYMENT.md` (deployment options)
- `run.py` (easy run script)
- `requirements.txt` (dependencies)
