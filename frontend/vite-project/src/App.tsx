import { useState, useEffect, useRef } from 'react';
import Globe from 'globe.gl';
import type { LocationPoint } from "./types";

function App() {
  const globeEl = useRef<HTMLDivElement>(null);
  const [locations, setLocations] = useState<LocationPoint[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/movies")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => setLocations(data))
      .catch((err) => {
        console.error("Fetch error:", err);
        alert("Failed to load movie data. Please try again later.");
      });
  }, []);

 // Initialize globe once
  useEffect(() => {
    if (!globeEl.current || locations.length === 0) return;

    new Globe(globeEl.current)
      .globeImageUrl("//unpkg.com/three-globe/example/img/earth-night.jpg")
      .pointsData(locations)
      .pointLat((d: any) => d.lat)
      .pointLng((d: any) => d.lon)
      .pointAltitude(0.02)
      .pointColor(() => "orange")
      .onPointClick((d: any) =>
        alert(`Movie: ${d.movie.title}\nYear: ${d.movie.year}\nRating: ${d.movie.rating}`)
      );
  }, [locations]);

  return <div ref={globeEl} style={{ width: '100vw', height: '100vh' }} />;
}

export default App;