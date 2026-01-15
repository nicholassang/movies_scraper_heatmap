import { useState, useEffect, useRef } from 'react';
import Globe from 'globe.gl';
import type { Movie, LocationPoint } from "./types";
import './App.css'

function App() {
  const globeEl = useRef<HTMLDivElement>(null);
  const globeInstance = useRef<any>(null);
  const [locations, setLocations] = useState<LocationPoint[]>([]);
  const [globeToggle, setGlobeToggle] = useState<boolean>(true);
  const [selectedPoint, setSelectedPoint] = useState<any>(null)
  const [selectedMovie, setSelectedMovie] = useState<Movie>()

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
        setSelectedMovie(d.movie)
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

  // prevent zooming for the user
  useEffect(() => {
    const handler = (e: WheelEvent | KeyboardEvent) => {
      if (
        e.ctrlKey ||
        (e instanceof KeyboardEvent &&
          (e.key === "+" || e.key === "-" || e.key === "="))
      ) {
        e.preventDefault();
      }
    };

    window.addEventListener("wheel", handler, { passive: false });
    window.addEventListener("keydown", handler);

    return () => {
      window.removeEventListener("wheel", handler);
      window.removeEventListener("keydown", handler);
    };
  }, []);

  function GenreTags({ genres }: { genres: string[] }) {
    const [expanded, setExpanded] = useState(false);
    const baseline = 3; // show 3 by default

    if (!genres || genres.length === 0) return null;

    const displayedGenres = expanded ? genres : genres.slice(0, baseline);

    return (
      <div>
        <div id="genre_tag_group">
          {displayedGenres.map((g, i) => (
            <div key={i} className="genre_tag">
              {g}
            </div>
          ))}
        </div>
        {genres.length > baseline && (
          <button
            className="genre_expand_btn"
            onClick={() => setExpanded((prev) => !prev)}
          >
            {expanded ? "-" : "+"}
          </button>
        )}
      </div>
    );
  }

  return (<>
    <button id="toggle_globe" onClick={() => setGlobeToggle(!globeToggle)}>toggle</button>
    <div id="display_panel">
      <h3>{ selectedMovie?.title }</h3>
      <img id="poster_image" src={selectedMovie?.poster_url}/>
      <GenreTags genres={selectedMovie?.genres || []}/>
      <div id="movie_info_grid">
        <div className="movie_info_grid_item">
          <span>Gross</span>
          <p className="movie_info_value">
            {selectedMovie?.gross
              ? "$" + selectedMovie.gross.toLocaleString() + " (est.)"
              : "Not available"}
          </p>
        </div>

        <div className="movie_info_grid_item">
          <span>Budget</span>
          <p className="movie_info_value">
            {selectedMovie?.budget
              ? "$" + selectedMovie.budget.toLocaleString()
              : "Not available"}
          </p>
        </div>

        <div className="movie_info_grid_item">
          <span>Production Country</span>
          <p className="movie_info_value">
            {selectedMovie?.country || "Not available"}
          </p>
        </div>
      </div>
      <span>Filming locations</span>
      <div id="loc_tag_group">{ 
          selectedMovie?.filming_locations.map((loc) => {
            return (
              <div className="loc_tag">
                {loc}
              </div>
            )
          }) 
        }
      </div>
    </div>
    <div ref={globeEl} style={{ width: '100vw', height: '100vh' }} />
  </>);
}

export default App;