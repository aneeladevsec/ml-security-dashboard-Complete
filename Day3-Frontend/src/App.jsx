import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Login from './components/Login';
import History from './components/History';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [activeTab, setActiveTab] = useState('dashboard');

  // Check auth on load
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
    }
  }, [token]);

  const handleLogin = (userData) => {
    setUser(userData);
    setToken(localStorage.getItem('token'));
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setToken(null);
    setActiveTab('dashboard');
  };

  // If not logged in, show login
  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>🔒 AI Security Dashboard</h1>
          <div className="user-info">
            <span>Welcome, <strong>{user.username}</strong></span>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        </div>
        <div className="status-badge online">🟢 System Online</div>
      </header>

      <nav className="tab-nav">
        <button 
          className={activeTab === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
        <button 
          className={activeTab === 'predict' ? 'active' : ''}
          onClick={() => setActiveTab('predict')}
        >
          🧪 Predict
        </button>
        <button 
          className={activeTab === 'history' ? 'active' : ''}
          onClick={() => setActiveTab('history')}
        >
          📜 History
        </button>
      </nav>

      <main className="dashboard">
        {activeTab === 'dashboard' && <Dashboard token={token} />}
        {activeTab === 'predict' && <Predict token={token} />}
        {activeTab === 'history' && <History token={token} />}
      </main>

      <footer>
        <p>Built in 10-Day Challenge by Aneela Ameen | Day 3/10 - Advanced Features</p>
        <p className="features">🔐 Auth | 💾 Database | 📄 PDF Reports | 📜 History</p>
      </footer>
    </div>
  );
}

// Dashboard Component
function Dashboard({ token }) {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/dashboard`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setStats(response.data);
    } catch (err) {
      console.error('Failed to fetch dashboard:', err);
    }
  };

  if (!stats) return <div className="loading">📊 Loading dashboard...</div>;

  return (
    <div className="tab-content">
      <h2>Security Overview</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🔍</div>
          <div className="stat-content">
            <h3>Your Scans</h3>
            <p className="stat-value">{stats.user_stats.total_scans}</p>
          </div>
        </div>
        <div className="stat-card danger">
          <div className="stat-icon">⚠️</div>
          <div className="stat-content">
            <h3>High Risk</h3>
            <p className="stat-value">{stats.user_stats.high_risk}</p>
          </div>
        </div>
        <div className="stat-card safe">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>Low Risk</h3>
            <p className="stat-value">{stats.user_stats.low_risk}</p>
          </div>
        </div>
      </div>

      <h3 style={{marginTop: '30px', marginBottom: '15px'}}>Global Statistics</h3>
      <div className="global-stats">
        <p>📈 Total Predictions (All Users): <strong>{stats.global_stats.total_predictions}</strong></p>
        <p>⚠️ Global High Risk: <strong>{stats.global_stats.high_risk_detected}</strong></p>
        <p>✅ Global Low Risk: <strong>{stats.global_stats.low_risk_detected}</strong></p>
        <p>🎯 Avg Confidence: <strong>{(stats.global_stats.average_confidence * 100).toFixed(1)}%</strong></p>
      </div>
    </div>
  );
}

// Predict Component (Updated with auth)
function Predict({ token }) {
  const [features, setFeatures] = useState(Array(10).fill(0.5));
  const [prediction, setPrediction] = useState(null);
  const [predicting, setPredicting] = useState(false);

  const handlePredict = async () => {
    setPredicting(true);
    try {
      const response = await axios.post(`${API_URL}/api/predict`, {
        features: features
      }, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      setPrediction(response.data);
    } catch (err) {
      alert('Prediction failed: ' + (err.response?.data?.error || err.message));
    } finally {
      setPredicting(false);
    }
  };

  const setRandomValues = () => {
    const random = Array(10).fill(0).map(() => Math.round(Math.random() * 100) / 100);
    setFeatures(random);
  };

  const setHighRisk = () => {
    const high = Array(10).fill(0).map(() => 0.7 + Math.random() * 0.3);
    setFeatures(high.map(v => Math.round(v * 100) / 100));
  };

  const setLowRisk = () => {
    const low = Array(10).fill(0).map(() => Math.random() * 0.3);
    setFeatures(low.map(v => Math.round(v * 100) / 100));
  };

  return (
    <div className="tab-content">
      <h2>Test ML Model Security</h2>
      
      <div className="quick-actions">
        <button onClick={setRandomValues} className="btn btn-secondary">🎲 Random Values</button>
        <button onClick={setHighRisk} className="btn btn-danger">⚠️ High Risk</button>
        <button onClick={setLowRisk} className="btn btn-success">✅ Low Risk</button>
      </div>

      <div className="features-grid">
        {features.map((f, i) => (
          <div key={i} className="feature-input">
            <label>Feature {i + 1}</label>
            <input
              type="number"
              step="0.01"
              min="0"
              max="1"
              value={f}
              onChange={(e) => {
                const newFeatures = [...features];
                newFeatures[i] = parseFloat(e.target.value) || 0;
                setFeatures(newFeatures);
              }}
            />
          </div>
        ))}
      </div>
      
      <button 
        onClick={handlePredict} 
        disabled={predicting}
        className="predict-btn"
      >
        {predicting ? 'Analyzing...' : '🔍 Predict Security Risk'}
      </button>

      {prediction && (
        <div className={`result-card ${prediction.prediction === 1 ? 'high-risk' : 'low-risk'}`}>
          <h3>Prediction Result</h3>
          <div className="result-item">
            <span>Risk Level:</span>
            <strong className={prediction.prediction === 1 ? 'danger' : 'safe'}>
              {prediction.prediction === 1 ? '⚠️ HIGH RISK' : '✅ LOW RISK'}
            </strong>
          </div>
          <div className="result-item">
            <span>Confidence:</span>
            <strong>{(prediction.confidence * 100).toFixed(2)}%</strong>
          </div>
          <div className="result-item">
            <span>Risk Score:</span>
            <strong>{(prediction.risk_score * 100).toFixed(2)}%</strong>
          </div>
          <div className="result-item">
            <span>Scan ID:</span>
            <strong>#{prediction.scan_id}</strong>
          </div>
          <div className="result-meta">
            <small>✅ Automatically saved to your history</small>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
