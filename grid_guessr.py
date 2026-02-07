import random
import os
import csv
import math
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
    "Africa_extreme": "Africa_extreme"
}

def normalize_city(name: str) -> str:
    return name.replace("_", " ").lower().strip()

# Load city coordinates from CSV
CITY_COORDINATES = {}

def load_coordinates():
    """Load city coordinates from CSV file"""
    csv_path = os.path.join(BASE_DIR, 'cities_with_coordinates.csv')
    
    if not os.path.exists(csv_path):
        print(f"⚠️  Warning: {csv_path} not found. Distance calculation will not work.")
        return
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                city_id = row['city_id']
                lat = row.get('latitude', '')
                lon = row.get('longitude', '')
                
                if lat and lon:
                    CITY_COORDINATES[city_id] = {
                        'lat': float(lat),
                        'lon': float(lon),
                        'name': row['city_name']
                    }
        
        print(f"✅ Loaded coordinates for {len(CITY_COORDINATES)} cities")
    except Exception as e:
        print(f"❌ Error loading coordinates: {e}")

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points on Earth using Haversine formula
    Returns distance in miles
    """
    # Earth's radius in miles
    R = 3959
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    
    return round(distance)

def calculate_distance(city1_id, city2_id):
    """
    Calculate distance between two cities
    Returns distance in miles or None if coordinates not found
    """
    if city1_id not in CITY_COORDINATES or city2_id not in CITY_COORDINATES:
        return None
    
    coords1 = CITY_COORDINATES[city1_id]
    coords2 = CITY_COORDINATES[city2_id]
    
    return haversine_distance(
        coords1['lat'], coords1['lon'],
        coords2['lat'], coords2['lon']
    )

# Load coordinates on startup
load_coordinates()

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

    folder_name = LEVELS[level]
    folder = os.path.join(BASE_DIR, folder_name)
    
    # Try to get files from local folder if it exists
    if os.path.exists(folder):
        files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
    else:
        return {"error": f"Map folder not found: {folder_name}"}
    
    if not files:
        return {"error": f"No maps found in {folder_name}"}

    filename = random.choice(files)
    city_name = os.path.splitext(filename)[0]

    current_round["city"] = city_name
    current_round["guesses"] = []

    # Load image from Railway
    return {
    "image": f"https://res.cloudinary.com/dg7wer3du/image/upload/{folder_name}/{filename.replace('.png', '')}"
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

    # Wrong guess - calculate distance
    current_round["guesses"].append(user_guess)
    attempt_number = len(current_round["guesses"])

    # Try to calculate distance
    # Need to find the city_id for the guessed city
    guess_city_id = None
    for city_id in CITY_COORDINATES:
        if normalize_city(city_id) == user_guess_norm:
            guess_city_id = city_id
            break
    
    # Calculate distance if both cities have coordinates
    distance_miles = None
    if guess_city_id and correct_city in CITY_COORDINATES:
        distance_miles = calculate_distance(guess_city_id, correct_city)
    
    # Fallback to placeholder if distance couldn't be calculated
    if distance_miles is None:
        distance_miles = "?"

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
        response["correct_city"] = correct_city.replace("_", " ")

    return response

@app.get("/valid-cities/{level}")
def valid_cities(level: str):
    if level not in LEVELS:
        return {"error": "Invalid level"}

    folder_name = LEVELS[level]
    folder = os.path.join(BASE_DIR, folder_name)
    
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