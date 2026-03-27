import React, { useState } from 'react';
import axios from 'axios';
import './PredictionForm.css';

function PredictionForm({ apiUrl }) {
  const [features, setFeatures] = useState(Array(10).fill(0));
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(`${apiUrl}/api/predict`, {
        features: features.map(f => parseFloat(f))
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    }
    setLoading(false);
  };

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...features];
    newFeatures[index] = value;
    setFeatures(newFeatures);
  };

  const handleRandom = () => {
    setFeatures(Array(10).fill(0).map(() => Math.random()));
  };

  return (
    <div className="prediction-form">
      <h2>🧪 Test ML Model Security</h2>
      <p>Enter 10 feature values to predict security risk:</p>
      
      <form onSubmit={handleSubmit}>
        <div className="features-grid">
          {features.map((f, i) => (
            <div key={i} className="feature-input">
              <label>Feature {i + 1}</label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="1"
                value={f.toFixed(2)}
                onChange={(e) => handleFeatureChange(i, e.target.value)}
                required
              />
            </div>
          ))}
        </div>
        
        <div className="form-buttons">
          <button type="submit" disabled={loading} className="predict-btn">
            {loading ? 'Analyzing...' : '🔍 Predict Security Risk'}
          </button>
          <button type="button" onClick={handleRandom} className="random-btn" disabled={loading}>
            🎲 Random Values
          </button>
        </div>
      </form>

      {error && (
        <div className="error-card">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className={`result-card ${result.prediction === 1 ? 'high-risk' : 'low-risk'}`}>
          <h3>Prediction Result</h3>
          <div className="result-item">
            <span>Risk Level:</span>
            <strong className={result.prediction === 1 ? 'danger' : 'safe'}>
              {result.prediction === 1 ? '⚠️ HIGH RISK' : '✅ SAFE'}
            </strong>
          </div>
          <div className="result-item">
            <span>Confidence:</span>
            <strong>{(result.confidence * 100).toFixed(2)}%</strong>
          </div>
          <div className="result-item">
            <span>Risk Score:</span>
            <strong>{(result.risk_score * 100).toFixed(2)}%</strong>
          </div>
          <div className="result-meta">
            <small>Model: {result.model_version} | {new Date(result.timestamp).toLocaleString()}</small>
          </div>
        </div>
      )}
    </div>
  );
}

export default PredictionForm;
