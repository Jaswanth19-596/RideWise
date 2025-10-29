import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import './DemandChart.css';

function DemandChart({ predictions, selectedRegion }) {
  const data = predictions.map((pred) => ({
    region: `Region ${pred.region_id}`,
    regionId: pred.region_id,
    predicted: pred.predicted_pickups,
    actual: pred.actual_pickups,
  }));

  const getColor = (regionId) => {
    return regionId === selectedRegion ? '#ff6b6b' : '#4ecdc4';
  };

  return (
    <div className="chart-wrapper">
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#444" />
          <XAxis
            dataKey="region"
            stroke="#fff"
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            stroke="#fff"
            label={{
              value: 'Pickups',
              angle: -90,
              position: 'insideLeft',
              fill: '#fff',
            }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1a1a1a',
              border: '1px solid #444',
              borderRadius: '8px',
            }}
            labelStyle={{ color: '#fff' }}
          />
          <Legend />
          <Bar dataKey="predicted" name="Predicted Demand">
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.regionId)} />
            ))}
          </Bar>
          {data.some((d) => d.actual) && (
            <Bar dataKey="actual" fill="#95e1d3" name="Actual Demand" />
          )}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default DemandChart;
