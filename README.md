# Day 1: AI Security Dashboard - 10 Day War Challenge

## Project Overview
A real-time AI Security Dashboard with:
- **Backend**: Flask API with ML Model (Random Forest Classifier)
- **Frontend**: React Dashboard with real-time predictions
- **ML Model**: Security risk prediction (0-1 scale)

## Project Structure

```
10-Day-War/
├── Day1-Backend/
│   ├── app.py              # Flask API
│   ├── model.py            # ML Model Class
│   ├── requirements.txt    # Python dependencies
│   ├── security_model.pkl  # Trained model (auto-generated)
│   └── __pycache__/
│
└── Day1-Frontend/
    ├── src/
    │   ├── components/
    │   │   ├── StatsCard.jsx
    │   │   ├── StatsCard.css
    │   │   ├── PredictionForm.jsx
    │   │   ├── PredictionForm.css
    │   │   ├── RiskChart.jsx
    │   ├── App.jsx
    │   ├── App.css
    │   ├── main.jsx
    │   └── index.css
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── .env
    └── README.md
```

## Quick Start

### Backend Setup

```powershell
cd Day1-Backend

# Activate Python virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run API server
python app.py
```

Backend will be running at: **http://localhost:5000**

### Frontend Setup

```powershell
cd Day1-Frontend

# Install dependencies (if not already done)
npm install

# Start dev server
npm run dev
```

Frontend will be running at: **http://localhost:5000** (with proxy to backend)

## API Endpoints

### 1. Health Check
```
GET http://localhost:5000/api/health
```
Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2026-03-19T12:00:00"
}
```

### 2. Get Statistics
```
GET http://localhost:5000/api/stats
```
Response:
```json
{
  "total_predictions": 150,
  "high_risk_detected": 23,
  "low_risk_detected": 127,
  "average_confidence": 0.89,
  "last_updated": "2026-03-19T12:00:00"
}
```

### 3. Predict Security Risk
```
POST http://localhost:5000/api/predict
Content-Type: application/json

{
  "features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
}
```

Response:
```json
{
  "prediction": 0,
  "confidence": 0.85,
  "risk_score": 0.15,
  "timestamp": "2026-03-19T12:00:00",
  "input_features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
  "model_version": "1.0.0"
}
```

## Features

### Backend Features
- ✅ Flask REST API with CORS support
- ✅ ML Model (scikit-learn RandomForest)
- ✅ Health check endpoint
- ✅ Statistics endpoint
- ✅ Security prediction endpoint

### Frontend Features
- ✅ Real-time statistics dashboard
- ✅ Risk analysis pie chart
- ✅ ML model prediction form
- ✅ Feature input validation
- ✅ Random data generator
- ✅ Responsive design
- ✅ Dark theme UI

## Testing

### Test with cURL (Backend)
```powershell
# Health check
curl -X GET http://localhost:5000/api/health

# Predict risk
curl -X POST http://localhost:5000/api/predict `
  -H "Content-Type: application/json" `
  -d '{"features": [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]}'
```

### Test with Frontend
1. Open http://localhost:3000 in browser
2. Check system status (should show 🟢 Online)
3. View statistics dashboard
4. Enter feature values or use "🎲 Random Values"
5. Click "🔍 Predict Security Risk"
6. View prediction results

## GitHub Integration

Already initialized and pushed to: `https://github.com/aneeladevsec/ml-security-dashboard`

To push new changes:
```powershell
cd Day1-Backend
git add .
git commit -m "Your message"
git push -u origin main
```

## Dependencies

### Python (Backend)
- flask==2.3.3
- flask-cors==4.0.0
- scikit-learn==1.3.0
- joblib==1.3.2
- numpy==1.24.3
- pandas==2.0.3
- python-dotenv==1.0.0
- gunicorn==21.2.0

### Node.js (Frontend)
- react@18.2.0
- axios for API calls
- chart.js for data visualization
- @mui/material for UI components
- react-icons for iconography

## Environment Variables

### Backend (.env)
```
PORT=5000
FLASK_ENV=development
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000
```

## Next Steps (Day 2+)

- [ ] Add authentication (JWT)
- [ ] Database integration (PostgreSQL)
- [ ] Advanced analytics
- [ ] Email notifications
- [ ] Mobile app support
- [ ] Docker containerization
- [ ] Deployment to cloud

## Project Completed ✅
**Status**: Day 1 Complete - Backend API + ML Model + React Dashboard

**Total Time**: ~6 hours (Phase 1 + Phase 2 + Phase 3)

---
*Built as part of 10-Day War Coding Challenge by Aneela Ameen*
