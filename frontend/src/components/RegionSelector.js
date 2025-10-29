import React from 'react';
import './RegionSelector.css';

function RegionSelector({ regions, selectedRegion, onSelectRegion }) {
  return (
    <div className="region-selector">
      <label>📍 Select Your Region:</label>
      <select
        value={selectedRegion}
        onChange={(e) => onSelectRegion(Number(e.target.value))}
      >
        {Object.entries(regions).map(([id, region]) => (
          <option key={id} value={id}>
            Region {id} - {region.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export default RegionSelector;
