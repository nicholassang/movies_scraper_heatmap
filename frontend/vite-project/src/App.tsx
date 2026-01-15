import { useState, useEffect, useRef } from 'react';
import Globe from 'globe.gl';
import type { LocationPoint } from "./types";
import './App.css'

function App() {
  const globeEl = useRef<HTMLDivElement>(null);
  const globeInstance = useRef<any>(null);
  const [locations, setLocations] = useState<LocationPoint[]>([]);
  const [globeToggle, setGlobeToggle] = useState<boolean>(true);
  const [selectedPoint, setSelectedPoint] = useState<any>(null)

  // Fetch data from backend
  useEffect(() => {
    fetch("http://127.0.0.1:8000/movies")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          const locationsData: LocationPoint[] = data
            .filter(
              (d) =>
                d &&
                typeof d.lat === "number" &&
                typeof d.lng === "number" &&
                typeof d.address === "string" &&
                typeof d.movie === "object"
            )
            .map((d) => ({
              lat: d.lat,
              lng: d.lng,
              address: d.address,
              movie: d.movie,
            }));

          setLocations(locationsData);
        } else {
          console.error("Invalid data format:", data);
        }
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        alert("Failed to load movie data. Please try again later.");
      });
  }, []);


  // Initial globe 
  useEffect(() => {
    if (!globeEl.current || locations.length === 0) return;
    if (globeInstance.current) return;

    const globe = new Globe(globeEl.current)
      .globeImageUrl("//unpkg.com/three-globe/example/img/earth-night.jpg")
      .pointLat((d: any) => d.lat)
      .pointLng((d: any) => d.lng)
      .pointAltitude(0.02)
      .onPointClick((d: any) => {
        setSelectedPoint(d);
/*         alert(
          `Movie: ${d.movie.title}\nYear: ${d.movie.year}\nRating: ${d.movie.rating}`
        ); */
      });

    globeInstance.current = globe;
  }, [locations]);


  // Selected Point update
  useEffect(() => {
    const globe = globeInstance.current;
    if (!globe) return;

    globe
      .pointsData(locations)
      .pointRadius((d: any) => (d === selectedPoint ? 0.4 : 0.12))
      .pointColor((d: any) => (d === selectedPoint ? "red" : "orange"))
      .pointsTransitionDuration(100)
  }, [selectedPoint, locations]);


  // Toggle between Heatmap & Pointmap
  useEffect(() => {
    const globe = globeInstance.current;
    if (!globe) return;

    if (globeToggle) {
      globe
        .heatmapsData([]) 
        .pointsData(locations)
        .enablePointerInteraction(true);
    } else {
      const gData = locations.map((loc) => ({
        lat: loc.lat,
        lng: loc.lng,
        weight: 1
      }));

      globe
        .pointsData([])
        .heatmapsData([gData])
        .heatmapPointLat("lat")
        .heatmapPointLng("lng")
        .heatmapPointWeight("weight")
        .heatmapTopAltitude(0.1)
        .heatmapsTransitionDuration(1000)
        .enablePointerInteraction(false);
    }
  }, [globeToggle, locations]);

  return (<>
    <button id="toggle_globe" onClick={() => setGlobeToggle(!globeToggle)}>toggle</button>
    <div id="display_panel">Movie Title</div>
    <div ref={globeEl} style={{ width: '100vw', height: '100vh' }} />
  </>);
}

export default App;