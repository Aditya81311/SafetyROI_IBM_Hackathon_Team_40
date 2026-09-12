import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";

const API_BASE =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

const riskColorMap = {
  Low: "#22c55e",
  Medium: "#f59e0b",
  High: "#f97316",
  Critical: "#991b1b",
};

export default function HotspotMap() {
  const [hotspots, setHotspots] = useState([]);
  const [selectedSpot, setSelectedSpot] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    const loadHotspots = async () => {
      try {
        const response = await axios.get(`${API_BASE}/hotspots`);
        if (active) {
          setHotspots(response.data || []);
        }
      } catch {
        if (active) {
          setError("Unable to retrieve hotspot data.");
        }
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    };

    loadHotspots();
    return () => {
      active = false;
    };
  }, []);

  const mapLegend = useMemo(
    () => [
      { label: "Low Risk", color: riskColorMap.Low },
      { label: "Medium Risk", color: riskColorMap.Medium },
      { label: "High Risk", color: riskColorMap.High },
      { label: "Critical Risk", color: riskColorMap.Critical },
    ],
    []
  );

  if (loading) {
    return <div className="map-loading">Loading hotspot network...</div>;
  }

  if (error) {
    return (
      <div className="map-error">
        <p>{error}</p>
        <button className="inline-link" onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    );
  }

  if (!hotspots.length) {
    return <div className="empty-state">No hotspots available right now.</div>;
  }

  return (
    <div className="map-layout">
      <div className="map-legend" aria-label="Risk legend">
        {mapLegend.map((item) => (
          <div key={item.label} className="legend-item">
            <span className="legend-dot" style={{ background: item.color }} />
            {item.label}
          </div>
        ))}
      </div>

      <MapContainer
        center={[22.5937, 78.9629]}
        zoom={5}
        style={{ height: "500px", width: "100%", borderRadius: "18px" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {hotspots.map((spot, index) => (
          <CircleMarker
            key={`${spot.city}-${index}`}
            center={[spot.lat, spot.lng]}
            radius={10}
            pathOptions={{ color: riskColorMap[spot.risk] || riskColorMap.Medium }}
            eventHandlers={{
              click: () => setSelectedSpot(spot),
            }}
          >
            <Popup>
              <strong>{spot.city}</strong>
              <br />
              Risk Level: {spot.risk}
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>

      {selectedSpot && (
        <div className="hotspot-detail">
          <div className="eyebrow">Hotspot Details</div>
          <h3>{selectedSpot.city}</h3>
          <div className="detail-grid">
            <div>
              <span>Risk score</span>
              <strong>{selectedSpot.risk}</strong>
            </div>
            <div>
              <span>Traffic</span>
              <strong>{selectedSpot.traffic || "High"}</strong>
            </div>
            <div>
              <span>Weather</span>
              <strong>{selectedSpot.weather || "Rain"}</strong>
            </div>
            <div>
              <span>Incident</span>
              <strong>{selectedSpot.incident || "High density corridor"}</strong>
            </div>
          </div>
          <button className="secondary-btn">View Risk Details</button>
        </div>
      )}
    </div>
  );
}