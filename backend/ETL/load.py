import json
from pathlib import Path
from db.connection import get_connection
from logger import get_logger
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
cleaned_file_path = DATA_DIR / "cleaned_movie_data.json"

logger = get_logger(__name__)

DATA_PATH = Path(cleaned_file_path)


def safe_int(value):
    try:
        return int(value) if value is not None else None
    except:
        return None

def safe_float(value):
    try:
        return float(value) if value is not None else None
    except:
        return None


def load():
    logger.info("Load running...\n")
    print("Load running...\n")

    # Load JSON file
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        movies_batch = json.load(f)

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("BEGIN")

        # Clear old data
        cur.execute("""
            TRUNCATE locations, movie_genres, genres, movies
            RESTART IDENTITY CASCADE;
        """)

        # Insert movies
        for movie in movies_batch:
            year = safe_int(movie.get("year"))
            rating = safe_float(movie.get("rating"))
            budget = safe_int(movie.get("budget"))
            gross = safe_int(movie.get("gross"))

            roi = safe_float(movie.get("ROI"))
            if roi is None and budget and gross:
                roi = gross / budget

            # Get country safely
            country = movie.get("country")  # can be None

            cur.execute("""
                INSERT INTO movies (
                    source_id, title, year, rating,
                    budget, gross, roi, poster_url, country
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                movie["source_id"],
                movie["title"],
                year,
                rating,
                budget,
                gross,
                roi,
                movie.get("poster_url"),
                country
            ))

        # Insert genres and mappings
        genre_cache = {}
        for movie in movies_batch:
            for genre in set(movie.get("genres", [])):

                # Insert genre if not exists
                if genre not in genre_cache:
                    cur.execute("""
                        INSERT INTO genres (name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING
                        RETURNING id
                    """, (genre,))

                    row = cur.fetchone()
                    if row:
                        genre_id = row[0]
                    else:
                        cur.execute("SELECT id FROM genres WHERE name=%s", (genre,))
                        genre_id = cur.fetchone()[0]

                    genre_cache[genre] = genre_id

                cur.execute("""
                    INSERT INTO movie_genres (movie_id, genre_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    movie["source_id"],
                    genre_cache[genre]
                ))

        # Insert locations
        for movie in movies_batch:
            for loc in movie.get("filming_locations_coords", []):
                coords = loc.get("coords")
                if not coords:
                    continue

                lat = safe_float(coords.get("lat"))
                lng = safe_float(coords.get("lng"))
                address = loc.get("address")

                if lat is None or lng is None:
                    continue

                cur.execute("""
                    INSERT INTO locations (movie_id, lat, lng, address)
                    VALUES (%s,%s,%s,%s)
                """, (
                    movie["source_id"],
                    lat,
                    lng,
                    address
                ))

        cur.execute("COMMIT")

    logger.info("Loaded JSON data into Postgres successfully!")
    print("Loaded JSON data into Postgres successfully!")
