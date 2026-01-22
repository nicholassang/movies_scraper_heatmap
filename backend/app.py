from fastapi import FastAPI, HTTPException, Query
import psycopg2
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
def search_movies(
    search: str | None = None,
    genre: str | None = None,
    year: int | None = None,
    sort: str = Query("title", regex="^(title|year|rating)$"),
    order: str = Query("asc", regex="^(asc|desc)$"),
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    try:
        sql = """
            SELECT m.source_id, m.title, m.year, m.rating, m.budget, m.gross,
                   m.roi, m.poster_url, ARRAY_AGG(g.name) AS genres
            FROM movies m
            LEFT JOIN movie_genres mg ON mg.movie_id = m.source_id
            LEFT JOIN genres g ON g.id = mg.genre_id
            WHERE 1=1
        """
        params = []

        if search:
            sql += " AND m.title ILIKE %s"
            params.append(f"%{search}%")

        if genre:
            sql += " AND g.name = %s"
            params.append(genre)

        if year:
            sql += " AND m.year = %s"
            params.append(year)

        sql += """
            GROUP BY m.source_id, m.title, m.year, m.rating, m.budget, m.gross, m.roi, m.poster_url
            ORDER BY {} {}
            LIMIT %s OFFSET %s
        """.format(sort, order)

        params.extend([limit, offset])

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "source_id": row[0],
                "title": row[1],
                "year": row[2],
                "rating": row[3],
                "budget": row[4],
                "gross": row[5],
                "roi": row[6],
                "poster_url": row[7],
                "genres": row[8]
            })

        return {"count": len(results), "results": results}

    except psycopg2.Error as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror or str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/movies/{source_id}")
def get_movie(source_id: str):
    try:
        with get_connection() as conn:
            cur = conn.cursor()

            # Fetch movie details + genres
            cur.execute("""
                SELECT m.source_id, m.title, m.year, m.rating, m.budget, m.gross,
                       m.roi, m.poster_url, m.country, ARRAY_AGG(g.name) AS genres
                FROM movies m
                LEFT JOIN movie_genres mg ON mg.movie_id = m.source_id
                LEFT JOIN genres g ON g.id = mg.genre_id
                WHERE m.source_id = %s
                GROUP BY m.source_id, m.title, m.year, m.rating, m.budget, m.gross, m.roi, m.poster_url, m.country
            """, (source_id,))
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Movie not found")

            movie_data = {
                "source_id": row[0],
                "title": row[1],
                "year": row[2],
                "rating": row[3],
                "budget": row[4],
                "gross": row[5],
                "roi": row[6],
                "poster_url": row[7],
                "country": row[8],
                "genres": row[9]
            }

            # Fetch filming locations for this movie
            cur.execute("""
                SELECT address
                FROM locations
                WHERE movie_id = %s
            """, (source_id,))
            locations_rows = cur.fetchall() or []

            filming_locations = [loc[0] for loc in locations_rows]

            movie_data["filming_locations"] = filming_locations

        return movie_data

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/genres")
def get_genres(search: str | None = None):
    try:
        sql = "SELECT name FROM genres WHERE 1=1"
        params = []

        if search:
            sql += " AND name ILIKE %s"
            params.append(f"%{search}%")

        sql += " ORDER BY name ASC"

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()

        results = [row[0] for row in rows]
        return {"count": len(results), "results": results}

    except psycopg2.Error as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror or str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/locations")
def get_locations(
    search: str | None = None,
    movie_id: str | None = None,
    genre: str | None = None,
    min_lat: float | None = None,
    max_lat: float | None = None,
    min_lng: float | None = None,
    max_lng: float | None = None,
    sort: str = "title",
    order: str = "asc",
    limit: int = 500,
    offset: int = 0
):
    allowed_sort_fields = {"title": "m.title", "year": "m.year", "rating": "m.rating"}
    sort_column = allowed_sort_fields.get(sort, "m.title")
    order = "DESC" if order.lower() == "desc" else "ASC"

    try:
        sql = """
            SELECT
                l.id, l.lat, l.lng, l.address,
                m.source_id, m.title, m.year, m.poster_url,
                ARRAY_AGG(g.name) AS genres
            FROM locations l
            JOIN movies m ON m.source_id = l.movie_id
            LEFT JOIN movie_genres mg ON mg.movie_id = m.source_id
            LEFT JOIN genres g ON g.id = mg.genre_id
            WHERE 1=1
        """
        params = []

        if search:
            sql += " AND m.title ILIKE %s"
            params.append(f"%{search}%")
        if movie_id:
            sql += " AND m.source_id = %s"
            params.append(movie_id)
        if genre:
            sql += " AND g.name = %s"
            params.append(genre)
        if min_lat is not None:
            sql += " AND l.lat BETWEEN %s AND %s"
            params.extend([min_lat, max_lat])
        if min_lng is not None:
            sql += " AND l.lng BETWEEN %s AND %s"
            params.extend([min_lng, max_lng])

        sql += f"""
            GROUP BY l.id, m.source_id
            ORDER BY {sort_column} {order}
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])

        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "location_id": row[0],
                "lat": row[1],
                "lng": row[2],
                "address": row[3],
                "source_id": row[4]
            })

        return {"count": len(results), "results": results}

    except psycopg2.Error as e:
        # Database error
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Database error: {e.pgerror or str(e)}")
    except Exception as e:
        # Catch-all for any other error
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@app.get("/locations/{source_id}")
def get_locations_for_movie(source_id: str):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, lat, lng, address
                FROM locations
                WHERE movie_id = %s
                ORDER BY id
            """, (source_id,))

            rows = cur.fetchall()

            return {
                "results": [
                    {
                        "location_id": row[0],
                        "lat": row[1],
                        "lng": row[2],
                        "address": row[3]
                    }
                    for row in rows
                ]
            }

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))