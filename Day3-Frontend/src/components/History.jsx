import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './History.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

function History({ token }) {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/history`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setScans(response.data.scans);
    } catch (err) {
      console.error('Failed to fetch history:', err);
    } finally {
      setLoading(false);
    }
  };

  const downloadReport = async (scanId) => {
    try {
      const response = await axios.get(`${API_URL}/api/report/${scanId}`, {
        headers: { 'Authorization': `Bearer ${token}` },
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `security_report_${scanId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert('Failed to download report');
    }
  };

  if (loading) return <div className="loading">📜 Loading history...</div>;

  return (
    <div className="history-container">
      <h2>📜 Scan History</h2>
      
      {scans.length === 0 ? (
        <p className="no-data">No scans yet. Run your first prediction!</p>
      ) : (
        <div className="scans-list">
          {scans.map(scan => (
            <div key={scan.id} className={`scan-card ${scan.prediction === 1 ? 'high-risk' : 'low-risk'}`}>
              <div className="scan-header">
                <span className="scan-id">Scan #{scan.id}</span>
                <span className="scan-date">{new Date(scan.created_at).toLocaleString()}</span>
              </div>
              
              <div className="scan-results">
                <div className="result-badge">
                  {scan.prediction === 1 ? '⚠️ HIGH RISK' : '✅ LOW RISK'}
                </div>
                <div className="confidence">
                  Confidence: {(scan.confidence * 100).toFixed(1)}%
                </div>
              </div>

              <button 
                onClick={() => downloadReport(scan.id)}
                className="download-btn"
              >
                📄 Download PDF Report
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default History;
