-- Enable pg_trgm extension for fast text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Movies table
CREATE TABLE movies (
    source_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    country TEXT,
    year INT,
    rating FLOAT,
    budget BIGINT,
    gross BIGINT,
    roi FLOAT,
    poster_url TEXT
);

-- Genres table
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Junction table for many-to-many relationship
CREATE TABLE movie_genres (
    movie_id TEXT REFERENCES movies(source_id) ON DELETE CASCADE,
    genre_id INT REFERENCES genres(id) ON DELETE CASCADE,
    PRIMARY KEY (movie_id, genre_id)
);

-- Locations table
CREATE TABLE locations (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    movie_id TEXT REFERENCES movies(source_id) ON DELETE CASCADE,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL,
    address TEXT
);

-- Indexes for performance
CREATE INDEX idx_movies_title_trgm ON movies USING GIN (title gin_trgm_ops);
CREATE INDEX idx_movies_year ON movies(year);
CREATE INDEX idx_locations_lat_lng ON locations(lat, lng);
CREATE INDEX idx_locations_movie_id ON locations(movie_id);
CREATE INDEX idx_movie_genres_genre_id ON movie_genres(genre_id);