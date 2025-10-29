import React, { useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './Map.css';

function Map({ predictions, regions, selectedRegion, onSelectRegion, getRegionColor }) {
  const getMarkerRadius = (demand) => {
    return Math.max(10, Math.min(30, demand / 2));
  };

  return (
    <MapContainer
      center={[40.758, -73.9855]}
      zoom={12}
      style={{ height: '500px', borderRadius: '12px' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      {predictions.map((pred) => {
        const region = regions[pred.region_id];
        if (!region) return null;

        const isSelected = pred.region_id === selectedRegion;
        const regionColor = getRegionColor(pred.region_id);

        return (
          <CircleMarker
            key={pred.region_id}
            center={[region.lat, region.lon]}
            radius={getMarkerRadius(pred.predicted_pickups)}
            fillColor={regionColor}
            color={isSelected ? '#fff' : regionColor}
            weight={isSelected ? 3 : 1}
            fillOpacity={0.7}
          >
            <Popup>
              <div className="popup-content">
                <h3>Region {pred.region_id}</h3>
                <p>
                  <strong>{region.name}</strong>
                </p>
                <p>
                  Predicted:{' '}
                  <strong>{pred.predicted_pickups.toFixed(1)}</strong>
                </p>
                {pred.actual_pickups && (
                  <p>
                    Actual: <strong>{pred.actual_pickups.toFixed(1)}</strong>
                  </p>
                )}
                <p className={pred.features.is_rush_hour ? 'rush-hour' : ''}>
                  {pred.features.is_rush_hour ? 'Rush Hour' : 'Normal Traffic'}
                </p>
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}

export default Map;
