import React, { useState, useEffect } from 'react';
import Map from './components/Map';
import RegionSelector from './components/RegionSelector';
import DemandChart from './components/DemandChart';
import StatsCard from './components/StatsCard';
import { predictionService } from './services/api';
import './App.css';

function App() {
  const [selectedRegion, setSelectedRegion] = useState(5);
  const [predictions, setPredictions] = useState([]);
  const [currentTime, setCurrentTime] = useState('');
  const [predictionTime, setPredictionTime] = useState('');
  const [loading, setLoading] = useState(false);
  const [regions, setRegions] = useState({});
  const [viewType, setViewType] = useState('all'); // 'all' or 'neighbors'

  // Utility function to generate a consistent color for each region
  const getRegionColor = (regionId) => {
    const hue = (regionId * 137) % 360; // Use a prime number to spread colors evenly
    return `hsl(${hue}, 70%, 60%)`;
  };

  // Fetch regions on mount
  useEffect(() => {
    predictionService
      .getRegions()
      .then((res) => setRegions(res.data))
      .catch((err) => console.error('Error fetching regions:', err));
  }, []);

  // Fetch predictions
  const fetchPredictions = async () => {
    setLoading(true);
    try {
      let response;
      if (viewType === 'all') {
        response = await predictionService.predictAllRegions(selectedRegion);
        setPredictions(response.data.predictions);
      } else {
        response = await predictionService.predictRegion(selectedRegion);
        setPredictions(response.data.predictions); // Wrap in array
      }
      const now = new Date();
      setCurrentTime(now.toLocaleString());
      now.setMinutes(now.getMinutes() + 15);
      setPredictionTime(now.toLocaleString());
    } catch (error) {
      console.error('Error fetching predictions:', error);
      alert(
        'Failed to fetch predictions. Make sure the backend is running on http://localhost:8000'
      );
    } finally {
      setLoading(false);
    }
  };

  // Fetch predictions when selectedRegion changes (if viewType is 'neighbors') or when viewType changes
  useEffect(() => {
    if (viewType === 'neighbors' && selectedRegion) {
      fetchPredictions();
    } else if (viewType === 'all') {
      fetchPredictions();
    }
  }, [selectedRegion, viewType]);

  const userPrediction = predictions.find(
    (p) => p.region_id === selectedRegion
  );
  const totalDemand = predictions.reduce(
    (sum, p) => sum + (p?.predicted_pickups || 0),
    0
  );

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>RideWise - Taxi Demand Forecaster</h1>
        <p className="subtitle">
          Real-time predictive analytics for urban mobility
        </p>
      </header>

      {/* Control Panel */}
      <div className="control-panel">
        <RegionSelector
          regions={regions}
          selectedRegion={selectedRegion}
          onSelectRegion={setSelectedRegion}
        />

        <div className="view-selector">
          <button
            className={`view-button ${viewType === 'all' ? 'active' : ''}`}
            onClick={() => setViewType('all')}
          >
            All NYC
          </button>
          <button
            className={`view-button ${
              viewType === 'neighbors' ? 'active' : ''
            }`}
            onClick={() => setViewType('neighbors')}
          >
            Closest Regions
          </button>
        </div>

        {currentTime && (
          <div className="time-display">
            Current Time: {currentTime}
            <br />
            Prediction Time: {predictionTime}
          </div>
        )}
      </div>

      {/* Stats Cards */}
      {predictions.length > 0 && userPrediction && (
        <div className="stats-container">
          <StatsCard
            title="Your Region"
            value={`Region ${selectedRegion}`}
            icon="#"
          />
          <StatsCard
            title="Your Region Demand"
            value={`${
              userPrediction?.predicted_pickups?.toFixed(0) || 'N/A'
            } pickups`}
            icon="↑"
            color="#007aff"
          />
          <StatsCard
            title="Total City Demand"
            value={`${totalDemand.toFixed(0)} pickups`}
            icon="∑"
            color="#1e90ff"
          />
          {userPrediction?.actual_pickups && (
            <StatsCard
              title="Prediction Accuracy"
              value={`${(
                100 -
                (Math.abs(
                  userPrediction.predicted_pickups -
                    userPrediction.actual_pickups
                ) /
                  userPrediction.actual_pickups) *
                  100
              ).toFixed(1)}%`}
              icon="%"
              color="#28a745"
            />
          )}
        </div>
      )}

      {/* Main Content */}
      {predictions.length > 0 ? (
        <>
          <div className="main-content">
            {/* Map */}
            <div className="map-container">
              <h2>
                <span className="icon">📍</span> Demand Heatmap
              </h2>
              <Map
                predictions={predictions}
                regions={regions}
                selectedRegion={selectedRegion}
                onSelectRegion={setSelectedRegion}
                getRegionColor={getRegionColor}
              />
            </div>

            {/* Chart */}
            <div className="chart-container">
              <h2>Demand by Region</h2>
              <DemandChart
                predictions={predictions}
                selectedRegion={selectedRegion}
                getRegionColor={getRegionColor}
                regions={regions}
              />
            </div>
          </div>

          {/* Details Table */}
          <div className="table-container">
            <h2>Detailed Predictions</h2>
            <div className="table-wrapper">
              <table className="predictions-table">
                <thead>
                  <tr>
                    <th>Region</th>
                    <th>Location</th>
                    <th>Pickups</th>
                    {viewType === 'neighbors' && <th>Distance</th>}
                  </tr>
                </thead>
                <tbody>
                  {predictions.map((pred) => (
                    <tr
                      key={pred.region_id}
                      className={
                        pred.region_id === selectedRegion ? 'neighbors' : ''
                      }
                      onClick={() => setSelectedRegion(pred.region_id)}
                    >
                      <td>{pred.region_id}</td>
                      <td>{regions[pred.region_id]?.name}</td>
                      <td className="demand-high">
                        {pred.predicted_pickups?.toFixed(1) || 'N/A'}
                      </td>
                      {viewType == 'neighbors' && (
                        <td>{pred.distance || 'N/A'}</td>
                      )}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      ) : (
        <div className="empty-state">
          <h2>Select a region to view predictions</h2>
          <p>
            Choose a region from the dropdown to see real-time taxi demand
            forecasts.
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
