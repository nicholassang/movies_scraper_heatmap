import json
from pathlib import Path
from db.connection import get_connection


DATA_PATH = Path("data/cleaned_movie_data.json")


def load():
    print("Load running...\n")

    # Load JSON file
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        movies = json.load(f)

    with get_connection() as conn:
        with conn.cursor() as cur:

            for movie in movies:
                cur.execute("""
                    INSERT INTO movies (
                        source_id, title, year, country, rating, budget, gross, roi,
                        genres, production_country, poster_url,
                        filming_locations, filming_locations_coords
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON CONFLICT (source_id) DO NOTHING
                """, (
                    movie.get("source_id"),
                    movie.get("title"),
                    int(movie["year"]) if movie.get("year") else None,
                    movie.get("country"),
                    float(movie["rating"]) if movie.get("rating") else None,
                    movie.get("budget"),
                    movie.get("gross"),
                    movie.get("ROI"),
                    json.dumps(movie.get("genres")),
                    movie.get("production_country"),
                    movie.get("poster_url"),
                    json.dumps(movie.get("filming_locations")),
                    json.dumps(movie.get("filming_locations_coords")),
                ))

        conn.commit()

    print("Loaded JSON data into Postgres successfully!")

load()