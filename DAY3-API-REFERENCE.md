# 🔌 Day 3 - API Reference Guide

## Base URL
```
http://localhost:5000
```

---

## 📚 Complete API Endpoints

### 1️⃣ HOME ENDPOINT

```
GET /
```

**Description**: Get API information and available endpoints

**Response**:
```json
{
  "message": "AI Security Dashboard API - Day 3",
  "status": "Live",
  "version": "3.0.0",
  "features": ["User Auth", "Scan History", "PDF Reports", "Database Storage"],
  "timestamp": "2026-03-27T11:36:03.236832"
}
```

---

### 2️⃣ HEALTH CHECK

```
GET /api/health
```

**Description**: Check if backend is running and healthy

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database": "connected",
  "version": "3.0.0",
  "timestamp": "2026-03-27T11:36:03.236832"
}
```

---

### 3️⃣ GLOBAL STATISTICS

```
GET /api/stats
```

**Description**: Get global statistics from all users

**Response**:
```json
{
  "total_predictions": 1,
  "high_risk_detected": 1,
  "low_risk_detected": 0,
  "average_confidence": 0.61,
  "last_updated": "2026-03-27T11:36:03.236832"
}
```

---

## 🔐 AUTHENTICATION ENDPOINTS

### 4️⃣ USER REGISTRATION

```
POST /api/auth/register
Content-Type: application/json
```

**Request Body**:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123"
}
```

**Success Response** (201):
```json
{
  "message": "User registered successfully",
  "user_id": 1
}
```

**Error Response** (400):
```json
{
  "error": "Username or email already exists"
}
```

**Validation Rules**:
- Username must be unique
- Email must be unique
- Password must be at least 6 characters

---

### 5️⃣ USER LOGIN

```
POST /api/auth/login
Content-Type: application/json
```

**Request Body**:
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Success Response**:
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

**Error Response** (401):
```json
{
  "error": "Invalid password"
}
```

**Token Info**:
- Format: JWT (JSON Web Token)
- Expires in: 7 days
- Use in header: `Authorization: Bearer <token>`

---

## 🔒 PROTECTED ENDPOINTS

> **Important**: All endpoints below require authentication!

### How to Authenticate
Add this header to your request:
```
Authorization: Bearer YOUR_JWT_TOKEN_HERE
```

---

### 6️⃣ ML PREDICTION

```
POST /api/predict
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body**:
```json
{
  "features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1]
}
```

**Validation**:
- Features must be array of exactly 10 numbers
- Each number must be between 0 and 1
- Array length must equal 10

**Success Response**:
```json
{
  "prediction": 1,
  "confidence": 0.61,
  "risk_score": 0.61,
  "risk_level": "HIGH",
  "scan_id": 1,
  "input_features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1],
  "model_version": "3.0.0",
  "timestamp": "2026-03-27T11:37:01.637281",
  "status": "success",
  "saved_to_history": true
}
```

**Error Response** (400):
```json
{
  "error": "Features must be array of exactly 10 values"
}
```

**Prediction Output**:
- `prediction`: 0 = Low Risk, 1 = High Risk
- `confidence`: 0-1 (how confident the model is)
- `risk_score`: 0-1 (quantified risk level)
- `risk_level`: "LOW" or "HIGH"
- `scan_id`: Unique identifier for this prediction

---

### 7️⃣ SCAN HISTORY

```
GET /api/history
Authorization: Bearer <token>
```

**Response**:
```json
{
  "scans": [
    {
      "id": 1,
      "features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1],
      "prediction": 1,
      "confidence": 0.61,
      "risk_score": 0.61,
      "model_version": "3.0.0",
      "created_at": "2026-03-27 06:37:01"
    }
  ],
  "total": 1,
  "user": "testuser"
}
```

**Features**:
- Returns all scans for authenticated user
- Ordered by newest first
- Limited to last 50 scans (default)
- Each scan contains full prediction data

---

### 8️⃣ DASHBOARD DATA

```
GET /api/dashboard
Authorization: Bearer <token>
```

**Response**:
```json
{
  "user": "testuser",
  "recent_scans": [
    {
      "id": 1,
      "features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1],
      "prediction": 1,
      "confidence": 0.61,
      "risk_score": 0.61,
      "model_version": "3.0.0",
      "created_at": "2026-03-27 06:37:01"
    }
  ],
  "global_stats": {
    "total_predictions": 1,
    "high_risk_detected": 1,
    "low_risk_detected": 0,
    "average_confidence": 0.61
  },
  "user_stats": {
    "total_scans": 1,
    "high_risk": 1,
    "low_risk": 0
  }
}
```

**Data Provided**:
- Last 10 scans for user
- User-specific statistics
- Global statistics from all users

---

### 9️⃣ PDF REPORT DOWNLOAD

```
GET /api/report/<scan_id>
Authorization: Bearer <token>
```

**Example**:
```
GET /api/report/1
```

**Response**: Binary PDF file

**Headers**:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename=security_report_1.pdf
```

**PDF Contains**:
- Report generation timestamp
- Model version used
- User information
- Risk assessment (HIGH/LOW)
- Confidence score
- Risk score
- Input features analysis
- Professional formatting

**Error Response** (404):
```json
{
  "error": "Scan not found"
}
```

---

## 🛠️ Usage Examples

### Example 1: Complete Workflow in PowerShell

```powershell
# 1. Register user
$register = @{
    username = 'developer'
    email = 'dev@example.com'
    password = 'dev123456'
} | ConvertTo-Json

$regResponse = Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/register' `
    -Method POST -ContentType 'application/json' -Body $register

Write-Output "User registered: $($regResponse.Content)"

# 2. Login user
$login = @{
    username = 'developer'
    password = 'dev123456'
} | ConvertTo-Json

$loginResponse = Invoke-WebRequest -Uri 'http://localhost:5000/api/auth/login' `
    -Method POST -ContentType 'application/json' -Body $login

$token = ($loginResponse.Content | ConvertFrom-Json).token
Write-Output "Token: $token"

# 3. Make prediction
$headers = @{'Authorization' = "Bearer $token"; 'Content-Type' = 'application/json'}
$features = @(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
$predict = @{features = $features} | ConvertTo-Json

$predResponse = Invoke-WebRequest -Uri 'http://localhost:5000/api/predict' `
    -Method POST -Headers $headers -Body $predict

$scanId = ($predResponse.Content | ConvertFrom-Json).scan_id
Write-Output "Scan ID: $scanId"

# 4. Get history
$histResponse = Invoke-WebRequest -Uri 'http://localhost:5000/api/history' `
    -Headers $headers -UseBasicParsing

Write-Output "Scan History: $($histResponse.Content)"

# 5. Download PDF
Invoke-WebRequest -Uri "http://localhost:5000/api/report/$scanId" `
    -Headers $headers -OutFile "report_$scanId.pdf"

Write-Output "PDF downloaded to: report_$scanId.pdf"
```

### Example 2: cURL Commands

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user1@test.com","password":"pass123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123"}'

# Predict (with token)
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"features":[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]}'

# Get History
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:5000/api/history

# Download PDF
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:5000/api/report/1 > report.pdf
```

### Example 3: Python Requests

```python
import requests
import json

BASE_URL = 'http://localhost:5000'

# Register
reg_data = {
    'username': 'pythonuser',
    'email': 'python@test.com',
    'password': 'pypass123'
}
req = requests.post(f'{BASE_URL}/api/auth/register', json=reg_data)
print(req.json())

# Login
login_data = {'username': 'pythonuser', 'password': 'pypass123'}
req = requests.post(f'{BASE_URL}/api/auth/login', json=login_data)
token = req.json()['token']

# Predict
headers = {'Authorization': f'Bearer {token}'}
features = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1]
predict_data = {'features': features}
req = requests.post(f'{BASE_URL}/api/predict', json=predict_data, headers=headers)
print(req.json())

# Download PDF
req = requests.get(f'{BASE_URL}/api/report/1', headers=headers)
with open('report.pdf', 'wb') as f:
    f.write(req.content)
```

---

## 🔄 Request/Response Flow

```
1. Register/Login → Get JWT Token
         ↓
2. Include Token in Headers → Authorization: Bearer <token>
         ↓
3. Make Prediction → Data saved to database
         ↓
4. Query History/Dashboard → Get saved data
         ↓
5. Download Report → Generate PDF from saved data
```

---

## ⚠️ Error Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET /api/health |
| 201 | Created | POST /api/auth/register |
| 400 | Bad Request | Invalid features |
| 401 | Unauthorized | Missing or invalid token |
| 404 | Not Found | Scan ID doesn't exist |
| 500 | Server Error | Internal error |

---

## 🔑 Authentication Details

### JWT Token Structure
```
Header.Payload.Signature

Where:
- Header: { "alg": "HS256", "typ": "JWT" }
- Payload: { "user_id": 1, "username": "testuser", "exp": 1234567890 }
- Signature: HMAC-SHA256 encrypted
```

### Token Validation
- Tokens expire after 7 days
- Invalid/expired tokens return 401
- Re-login to get a new token

---

## 📊 Rate Limiting

Currently **unlimited** requests (add in future releases)

---

## 🚀 Performance Tips

1. **Cache tokens** - Don't re-login every request
2. **Batch predictions** - Group multiple predictions
3. **Paginate history** - Load old scans on demand
4. **Compress PDFs** - Large files take time to generate

---

## 📝 CORS Settings

Frontend can access backend from:
- `http://localhost:3000`
- `http://localhost:5000`
- Any origin (currently open for testing)

---

## 🔐 Security Notes

⚠️ **FOR DEVELOPMENT ONLY**

Before production deployment:
- [ ] Hash passwords with bcrypt
- [ ] Use environment variables for SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Restrict CORS to specific domains
- [ ] Add rate limiting
- [ ] Add request validation
- [ ] Add audit logging
- [ ] Enable database encryption

---

## 📞 Support

For API issues:
1. Check backend terminal for errors
2. Verify token is valid
3. Ensure features are correct format
4. Check database file exists
5. Restart backend if needed

---

This is your complete Day 3 API reference! 🎉
