import random
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LEVELS = {
    "easy": "USA_easy",
    "med": "USA_med",
    "extreme": "USA_extreme",
    "NA_easy": "NA_easy",
    "NA_med": "NA_med",
    "NA_extreme": "NA_extreme",
    "Europe_easy": "Europe_easy",
    "Europe_med": "Europe_med",
    "Europe_extreme": "Europe_extreme",
    "SA_easy": "SA_easy",
    "SA_med": "SA_med",
    "SA_extreme": "SA_extreme",
    "Oceania_easy": "Oceania_easy",
    "Oceania_med": "Oceania_med",
    "Oceania_extreme": "Oceania_extreme",
    "Africa_easy": "Africa_easy",
    "Africa_med": "Africa_med",
    "Africa_extreme": "Africa_extreme",
}

def normalize_city(name: str) -> str:
    return name.replace("_", " ").lower().strip()

# Serve static files (preview images) - only if folder exists
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount(
        "/static",
        StaticFiles(directory=static_dir),
        name="static"
    )

# Serve game maps - only if folders exist
if os.path.exists(os.path.join(BASE_DIR, "USA_easy")):
    app.mount(
        "/maps",
        StaticFiles(directory=BASE_DIR),
        name="maps"
    )

current_round = {
    "city": None,
    "guesses": []
}

@app.get("/")
def home():
    return FileResponse(os.path.join(BASE_DIR, "home.html"))

@app.get("/play/{level}")
def play(level: str):
    if level not in LEVELS:
        return {"error": "Invalid level"}
    return FileResponse(os.path.join(BASE_DIR, "game.html"))

@app.get("/new-round/{level}")
def new_round(level: str):
    if level not in LEVELS:
        return {"error": "Invalid level"}

    folder = os.path.join(BASE_DIR, LEVELS[level])
    
    # Check if folder exists
    if not os.path.exists(folder):
        return {"error": f"Map folder not found: {LEVELS[level]}"}
    
    files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
    
    if not files:
        return {"error": f"No maps found in {LEVELS[level]}"}

    filename = random.choice(files)
    city_name = os.path.splitext(filename)[0]

    current_round["city"] = city_name
    current_round["guesses"] = []

    # Use relative path for local testing
    return {
        "image": f"https://res.cloudinary.com/dg7wer3du/image/upload/{LEVELS[level]}/{filename}"
    }

class GuessPayload(BaseModel):
    guess: str

@app.post("/guess")
def guess(payload: GuessPayload):
    user_guess = payload.guess.strip()
    correct_city = current_round["city"]

    if not correct_city:
        return {"error": "No active round"}

    # Normalize
    user_guess_norm = normalize_city(user_guess)
    correct_norm = normalize_city(correct_city)

    # Correct guess
    if user_guess_norm == correct_norm:
        return {
            "result": "correct",
            "attempt": len(current_round["guesses"]) + 1
        }

    # Wrong guess
    current_round["guesses"].append(user_guess)

    attempt_number = len(current_round["guesses"])

    # Placeholder distance (to be replaced later)
    distance_miles = "x"

    response = {
        "result": "wrong",
        "attempt": attempt_number,
        "guess": user_guess,
        "distance": distance_miles,
        "remaining": 5 - attempt_number
    }

    # Reveal answer after 5th guess
    if attempt_number >= 5:
        response["result"] = "lost"
        response["correct_city"] = correct_city

    return response

@app.get("/valid-cities/{level}")
def valid_cities(level: str):
    if level not in LEVELS:
        return {"error": "Invalid level"}

    folder = os.path.join(BASE_DIR, LEVELS[level])
    
    if not os.path.exists(folder):
        return {"cities": []}
    
    files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]

    cities = [
        normalize_city(os.path.splitext(f)[0])
        for f in files
    ]

    return {
        "cities": cities
    }
