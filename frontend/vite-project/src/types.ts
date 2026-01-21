export interface Movie {
  source_id: string;
  title: string;
  poster_url: string;
  year: string;
  country: string,
  rating?: number;
  budget?: number;
  gross?: number;
  roi?: number;
  genres?: string[];
  filming_locations?: string[];
}

export interface LocationPoint {
  location_id: number;
  lat: number;
  lng: number;
  address: string;
  source_id: string;
}