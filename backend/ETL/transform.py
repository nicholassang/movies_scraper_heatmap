from geopy.geocoders import Nominatim
import json
import traceback
from logger import get_logger
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
raw_file_path = DATA_DIR / "raw_movie_data.json"
cleaned_file_path = DATA_DIR / "cleaned_movie_data.json"

logger = get_logger(__name__)

def transform():
    logger.info("Transform running...")
    print("Transform running...")
    print()
    geolocator = Nominatim(user_agent="movie_filming_locations_coords")

    cleaned_data = []

    try:
        with open(raw_file_path, 'r') as file:
            movie_data = json.load(file)
            length = len(movie_data)
            for i, movie in enumerate(movie_data):
                logger.info(f"Transform progress: {i + 1} / {length}")
                print(f"Transform progress: {i + 1} / {length}")
                cache_locations_coords = []
                for filming_location in movie.get("filming_locations", []):
                    location = geolocator.geocode(filming_location, timeout=10)
                    
                    if location is not None:
                        cache_locations_coords.append({
                            "address": location.address,
                            "coords": {
                                "lat": location.latitude,
                                "lng": location.longitude
                            }
                        })
                    else:
                        print(filming_location, "couldn't find coordinates")
                        cache_locations_coords.append({
                            "address": filming_location,
                            "coords": None
                        })

                movie["filming_locations_coords"] = cache_locations_coords
                cleaned_data.append(movie)

        with open(cleaned_file_path, 'w', encoding='utf-8') as file:
            json.dump(cleaned_data, file, ensure_ascii=False, indent=4)
    except Exception:
        logger.error("Error: Did not convert all coordinates")
        logger.error(traceback.format_exc())
        print()
        print("Error: Did not convert all coordinates")
        print(traceback.format_exc())

        with open(cleaned_file_path, 'w', encoding='utf-8') as file:
            json.dump(cleaned_data, file, ensure_ascii=False, indent=4)