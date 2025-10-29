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
  const [loading, setLoading] = useState(false);
  const [regions, setRegions] = useState({});

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
      const response = await predictionService.predictAllRegions();
      setPredictions(response.data.predictions);
      setCurrentTime(response.data.timestamp);
    } catch (error) {
      console.error('Error fetching predictions:', error);
      alert(
        'Failed to fetch predictions. Make sure the backend is running on http://localhost:8000'
      );
    } finally {
      setLoading(false);
    }
  };

  const userPrediction = predictions.find(
    (p) => p.region_id === selectedRegion
  );
  const totalDemand = predictions.reduce(
    (sum, p) => sum + p.predicted_pickups,
    0
  );

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>🚕 RideWise - Taxi Demand Forecaster</h1>
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

        <button
          className="predict-button"
          onClick={fetchPredictions}
          disabled={loading}
        >
          {loading ? '⏳ Calculating...' : '🔮 Predict Demand'}
        </button>

        {currentTime && (
          <div className="time-display">
            🕐 {new Date(currentTime).toLocaleString()}
          </div>
        )}
      </div>

      {/* Stats Cards */}
      {predictions.length > 0 && userPrediction && (
        <div className="stats-container">
          <StatsCard
            title="Your Region"
            value={`Region ${selectedRegion}`}
            icon="📍"
          />
          <StatsCard
            title="Your Region Demand"
            value={`${userPrediction.predicted_pickups.toFixed(0)} pickups`}
            icon="🚖"
            color="#ff6b6b"
          />
          <StatsCard
            title="Total City Demand"
            value={`${totalDemand.toFixed(0)} pickups`}
            icon="🌆"
            color="#4ecdc4"
          />
          {userPrediction.actual_pickups && (
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
              icon="🎯"
              color="#95e1d3"
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
              <h2>🗺️ Demand Heatmap</h2>
              <Map
                predictions={predictions}
                regions={regions}
                selectedRegion={selectedRegion}
                onSelectRegion={setSelectedRegion}
              />
            </div>

            {/* Chart */}
            <div className="chart-container">
              <h2>📊 Demand by Region</h2>
              <DemandChart
                predictions={predictions}
                selectedRegion={selectedRegion}
              />
            </div>
          </div>

          {/* Details Table */}
          <div className="table-container">
            <h2>📋 Detailed Predictions</h2>
            <div className="table-wrapper">
              <table className="predictions-table">
                <thead>
                  <tr>
                    <th>Region</th>
                    <th>Location</th>
                    <th>Predicted</th>
                    <th>Actual</th>
                    <th>Error</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {predictions.map((pred) => (
                    <tr
                      key={pred.region_id}
                      className={
                        pred.region_id === selectedRegion ? 'selected' : ''
                      }
                      onClick={() => setSelectedRegion(pred.region_id)}
                    >
                      <td>{pred.region_id}</td>
                      <td>{regions[pred.region_id]?.name}</td>
                      <td className="demand-high">
                        {pred.predicted_pickups.toFixed(1)}
                      </td>
                      <td>{pred.actual_pickups?.toFixed(1) || 'N/A'}</td>
                      <td>
                        {pred.actual_pickups
                          ? Math.abs(
                              pred.predicted_pickups - pred.actual_pickups
                            ).toFixed(1)
                          : 'N/A'}
                      </td>
                      <td>
                        <span
                          className={`badge ${
                            pred.features.is_rush_hour ? 'rush' : ''
                          }`}
                        >
                          {pred.features.is_rush_hour ? '🚨 Rush' : '✅ Normal'}
                        </span>
                        <span
                          className={`badge ${
                            pred.features.is_weekend ? 'weekend' : ''
                          }`}
                        >
                          {pred.features.is_weekend
                            ? '🎉 Weekend'
                            : '💼 Weekday'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      ) : (
        <div className="empty-state">
          <h2>👆 Click "Predict Demand" to get started!</h2>
          <p>Select your region and see real-time taxi demand predictions</p>
        </div>
      )}
    </div>
  );
}

export default App;
