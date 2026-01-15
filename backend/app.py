from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from db.connection import get_connection
import traceback


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/movies")
def get_movies():
    try:
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT source_id, title, year, country, rating, budget, gross, roi, genres,
                    production_country, poster_url, filming_locations, filming_locations_coords
                FROM movies;
            """)

            rows = cur.fetchall() or []
            cur.close()
            conn.close()

            data = []

            for row in rows:
                movie_info = {
                    "source_id": row[0],
                    "title": row[1],
                    "year": row[2],
                    "country": row[3],
                    "rating": row[4],
                    "budget": row[5],
                    "gross": row[6],
                    "ROI": row[7],
                    "genres": row[8],
                    "production_country": row[9],
                    "poster_url": row[10],
                    "filming_locations": row[11]
                }

                coords_list = row[12] 
                if coords_list:
                    for loc in coords_list:
                        if loc["coords"] is None or loc["address"] is None:
                            continue
                        # Each point contains lat/lon + full movie info
                        data.append({
                            "lat": loc["coords"]["lat"],
                            "lng": loc["coords"]["lng"],
                            "address": loc["address"],
                            "movie": movie_info
                        })

            return data
    except Exception as e:
        traceback.print_exc()
        print("Error in /movies:", e)
        return {"error": str(e)}