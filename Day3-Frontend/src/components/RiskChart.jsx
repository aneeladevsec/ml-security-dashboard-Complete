import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

function RiskChart({ stats }) {
  const data = {
    labels: ['High Risk', 'Low Risk'],
    datasets: [
      {
        data: [
          stats?.high_risk_detected || 0,
          stats?.low_risk_detected || 0
        ],
        backgroundColor: ['#ff4757', '#2ed573'],
        borderColor: ['#ff4757', '#2ed573'],
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#ffffff',
          padding: 20,
          font: {
            size: 14,
          }
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return context.label + ': ' + context.parsed;
          }
        }
      }
    },
  };

  return (
    <div className="chart-container">
      <h2>📊 Risk Analysis</h2>
      <Pie data={data} options={options} />
    </div>
  );
}

export default RiskChart;
