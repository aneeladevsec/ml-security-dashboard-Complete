# 🚀 Day 5 - Chrome Extension Deployment Guide

## Quick Start (5 Minutes)

### Prerequisites
- ✅ Backend running: `http://localhost:5000`
- ✅ Frontend running: `http://localhost:3001`
- ✅ Chrome browser installed
- ✅ Extension files in: `chrome-extension/` folder

---

## Step 1: Load Extension in Chrome

### Open Chrome Extensions Manager

```
1. Open Google Chrome
2. Type in address bar: chrome://extensions/
3. OR: Menu → More tools → Extensions
```

### Enable Developer Mode

```
1. Top right corner: Toggle "Developer mode" ON
2. New buttons appear: "Load unpacked", "Pack extension"
```

### Load Extension

```
1. Click "Load unpacked"
2. Navigation dialog opens
3. Go to: 10-Day-War/chrome-extension/
4. Click "Select Folder"
5. ✅ Extension loaded!
```

### Verify Installation

```
You should see:
- Extension ID (e.g., "ghklmkafinmhplmidngohjlfnjemfejb")
- Status: "Enabled"
- Icon appears in Chrome toolbar
```

---

## Step 2: Test Extension

### First Test

```
1. Open any website (e.g., google.com)
2. Click extension icon in toolbar
3. Popup opens showing:
   - Current website URL
   - 10 security features
   - Initial risk assessment
```

### Analyze with AI

```
1. In popup, click "🔍 Analyze with AI" button
2. Extension analyzes the website
3. Sends 10 features to backend API
4. Receives ML prediction result

Expected Result:
- HIGH RISK ⚠️ or LOW RISK ✅
- Confidence percentage
- Risk score
```

### Example Test Cases

**Test 1: HTTPS Website (Google.com)**
```
✅ Expected: Likely Safe / Low Risk
- HTTPS: Secure ✅
- SSL: Valid ✅
- Features: Mostly positive
```

**Test 2: HTTP Website**
```
⚠️ Expected: Warning / High Risk
- HTTPS: Not Secure ❌
- SSL: Invalid ❌
- Features: Mixed
```

**Test 3: Dashboard Link**
```
1. Click "📊 Open Dashboard" in popup
2. Opens http://localhost:3001 in new tab
3. Can login and view your predictions
```

---

## Step 3: Key Features

### Real-time Security Analysis

The extension analyzes:
1. **HTTPS/SSL** - Site encryption
2. **Certificates** - SSL validity
3. **Mixed Content** - Insecure resource loading
4. **Security Headers** - Security configuration
5. **Domain Age** - Domain establishment
6. **Redirects** - Redirect chains
7. **Forms** - Form detection
8. **Cookies** - Cookie tracking
9. **Third-party** - External scripts
10. **Load Time** - Page performance

### AI Prediction

Uses your trained ML model to:
- Analyze all 10 features
- Generate risk score (0-100%)
- Show confidence level
- Display risk assessment

### Local Storage

Extension saves scans locally:
- Access via chrome.storage API
- Up to 50 recent scans
- Timestamp for each scan
- Risk level recorded

### Dashboard Integration

```
1. Click "📊 Open Dashboard" → Dashboard opens
2. Click "📜 View History" → Dashboard history tab
3. Login optional (see below)
```

---

## Step 4: With Authentication (Optional)

### Login to Save History

```
1. Open Dashboard: http://localhost:3001
2. Click "🔐 Login"
3. Enter credentials:
   - Username: testuser
   - Password: password123
4. Get JWT token
5. Extension can now save scans to your account
```

### Auto-detect Token

```
1. After login, extension can detect JWT
2. Subsequent scans saved to database
3. Access from dashboard → History
4. Download PDF reports
```

---

## Troubleshooting

### Extension Not Appearing

**Problem**: Icon not visible in toolbar
```
Solution:
1. Go to chrome://extensions/
2. Find "AI Security Scanner"
3. Check if "Enabled" toggle is ON
4. Try pinning icon: Click extension button → Click pin icon
```

### "Connect to API" Fails

**Problem**: Extension shows "Offline"
```
Solution:
1. Check backend is running: http://localhost:5000/api/health
2. Check if CORS is enabled
3. Run: python test_day5.py
4. Look for "❌ CORS Check ERROR"
```

### CORS Errors in Console

**Problem**: Background script shows CORS error
```
Solution:
1. Backend must have CORS enabled
2. Check app.py has:
   CORS(app, resources={
       r"/api/*": {
           "origins": "*",
           ...
       }
   })
3. Restart backend: Kill terminal and restart
```

### Extension Crashes on Analyze

**Problem**: Click "Analyze" but nothing happens
```
Solution:
1. Check browser console (F12)
2. Look for JavaScript errors
3. Restart extension: 
   - Go to chrome://extensions/
   - Click reload button
4. Try different website
```

### API Returns 500 Error

**Problem**: Backend error response
```
Solution:
1. Check backend logs for errors
2. Test with: python test_day5.py
3. Look for missing dependencies
4. Ensure database file exists
```

---

## Advanced: Manual Testing

### Using cURL Commands

**Health Check**:
```bash
curl http://localhost:5000/api/health
```

**Test Prediction**:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1]}'
```

**With Authentication**:
```bash
# First login
TOKEN=$(curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' \
  | jq -r '.token')

# Then predict (scan saves to database)
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"features": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1]}'
```

---

## Extension Code Structure

### popup.html
```
Header with status indicator
├─ Current Site Info
│  ├─ URL display
│  └─ Risk badge (Safe/Warning/Danger)
├─ Security Features (10 items)
│  ├─ Each feature with status
│  └─ Color coded (Green/Yellow/Red)
├─ ML Prediction Section
│  ├─ Result display
│  └─ Analyze button
├─ Action Buttons
│  ├─ Open Dashboard
│  └─ View History
└─ Footer with API status
```

### popup.js (Main Logic)
```javascript
// 1. Initialize on popup open
DOMContentLoaded → checkApiStatus() 
                 → getCurrentTab()
                 → analyzeCurrentSite()

// 2. Analyze current website
analyzeCurrentSite() → Check HTTPS
                    → Check SSL
                    → Check headers
                    → ... (10 features)
                    → calculateInitialRisk()

// 3. Run ML analysis
runMLAnalysis() → generateFeaturesFromSite()
               → POST /api/predict
               → displayResult()
               → saveScanToHistory()

// 4. Save locally
saveScanToHistory() → chrome.storage.local.set()
                   → Keep last 50 scans
```

---

## Day 5 Deployment Checklist

- [ ] Backend running on port 5000
  - [ ] `python app.py` in Day3-Backend
  - [ ] Check `/api/health` returns 200

- [ ] Frontend running on port 3001
  - [ ] `npm run dev` in Day3-Frontend
  - [ ] Dashboard accessible

- [ ] Extension files created
  - [ ] `chrome-extension/manifest.json` exists
  - [ ] `chrome-extension/popup.html` exists
  - [ ] `chrome-extension/popup.js` exists
  - [ ] `chrome-extension/background.js` exists
  - [ ] `chrome-extension/icons/` folder with 3 PNGs

- [ ] Extension loaded in Chrome
  - [ ] `chrome://extensions/` shows extension
  - [ ] Developer mode enabled
  - [ ] Extension enabled (toggle ON)
  - [ ] Icon visible in toolbar

- [ ] Extension working
  - [ ] Can open popup
  - [ ] Shows current website
  - [ ] Features load correctly
  - [ ] "Analyze" button works
  - [ ] Receives prediction result
  - [ ] "Open Dashboard" link works

- [ ] Tests passing
  - [ ] `python test_day5.py` shows 5/5 PASSED
  - [ ] No CORS errors
  - [ ] API responds correctly

---

## File Locations

```
Extension Files:
├── manifest.json (379 bytes)
├── popup.html (3.2 KB)
├── popup.css (4.8 KB)
├── popup.js (4.1 KB)
├── background.js (0.7 KB)
└── icons/
    ├── icon16.png (634 bytes)
    ├── icon48.png (5.7 KB)
    └── icon128.png (21.6 KB)

Test Files:
├── test_day5.py (3.2 KB)
└── create_icons.py (1.1 KB)

Documentation:
├── DAY5-COMPLETION-SUMMARY.md ✨ NEW
└── DAY5-DEPLOYMENT-GUIDE.md ✨ NEW
```

---

## Next Steps

1. ✅ Install extension
2. ✅ Test on multiple websites
3. ✅ Verify API integration
4. 🎯 Create Chrome Web Store account (optional)
5. 🎯 Submit extension for review
6. 🎯 Promote extension

---

## Support

If extension not working:
1. Check console: F12 → Console tab
2. Run tests: `python test_day5.py`
3. Restart backend: Kill and restart python app.py
4. Reload extension: Go to chrome://extensions/ → reload button

---

**Status**: ✨ Extension Ready to Deploy ✨
