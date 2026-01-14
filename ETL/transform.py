from geopy.geocoders import Nominatim
import json
import traceback

def transform():
    print("Transform running")
    print()
    geolocator = Nominatim(user_agent="movie_filming_locations_coords")

    cleaned_data = []

    try:
        with open("./data/raw_movie_data.json", 'r') as file:
            movie_data = json.load(file)
            length = len(movie_data)
            for i, movie in enumerate(movie_data):
                print(f"Transform progress: {i + 1} / {length}")
                cache_locations_coords = []
                for filming_location in movie.get("filming_locations", []):
                    location = geolocator.geocode(filming_location, timeout=10)
                    
                    if location is not None:
                        cache_locations_coords.append({
                            "address": location.address,
                            "coords": {
                                "lat": location.latitude,
                                "lon": location.longitude
                            }
                        })
                    else:
                        print(filming_location, "couldn't find coordinates")
                        cache_locations_coords.append({
                            "address": filming_location,
                            "coords": None
                        })

                movie[filming_location] = cache_locations_coords
                cleaned_data.append(movie)

        with open("./data/cleaned_movie_data.json", 'w') as file:
            json.dump(cleaned_data, file, ensure_ascii=False, indent=4)
    except Exception:
        print()
        print("Error: Did not convert all coordinates")
        print(traceback.format_exc())

        with open("./data/cleaned_movie_data.json", 'w') as file:
            json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

transform()
