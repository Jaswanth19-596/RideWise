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

function DemandChart({ predictions, selectedRegion, getRegionColor, regions }) {
  const data = predictions.map((pred) => ({
    region: `${regions[pred.region_id].name}`,
    regionId: pred.region_id,
    predicted: pred.predicted_pickups,
    actual: pred.actual_pickups,
  }));

  return (
    <div className="chart-wrapper">
      <ResponsiveContainer
        width={Math.max(400, predictions.length * 50)}
        height={400}
      >
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#444" />
          <XAxis
            dataKey="region"
            stroke="#fff"
            angle={-45}
            textAnchor="end"
            height={150}
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
            itemStyle={{ color: '#fff' }}
          />
          <Legend />
          <Bar dataKey="predicted" name="Predicted Demand">
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={getRegionColor(entry.regionId)}
              />
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
