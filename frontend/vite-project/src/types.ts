export interface Movie {
  source_id: string;
  title: string;
  year: number;
  country: string;
  rating: number | null;
  budget: number | null;
  gross: number | null;
  ROI: number | null;
  genres: string[];
  production_country: string;
  poster_url: string;
  filming_locations: string[];
}

export interface LocationPoint {
  lat: number;
  lon: number;
  address: string;
  movie: Movie;
}