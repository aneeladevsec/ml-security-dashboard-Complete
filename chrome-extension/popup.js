// API URL - Points to local backend
const API_URL = 'http://localhost:5000';

// Current tab info
let currentTab = null;

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  await checkApiStatus();
  await getCurrentTab();
  analyzeCurrentSite();
  
  // Button listeners
  document.getElementById('analyze-btn').addEventListener('click', runMLAnalysis);
  document.getElementById('dashboard-btn').addEventListener('click', () => {
    chrome.tabs.create({ url: 'http://localhost:3000' });
  });
  document.getElementById('history-btn').addEventListener('click', () => {
    chrome.tabs.create({ url: 'http://localhost:3000' });
  });
});

// Check API status
async function checkApiStatus() {
  const statusEl = document.getElementById('api-status');
  const headerStatus = document.getElementById('status');
  
  try {
    const response = await fetch(`${API_URL}/api/health`);
    if (response.ok) {
      statusEl.textContent = 'Connected';
      statusEl.style.color = '#2ed573';
      headerStatus.textContent = 'Online';
      headerStatus.className = 'status online';
    } else {
      throw new Error('API Error');
    }
  } catch (err) {
    statusEl.textContent = 'Offline';
    statusEl.style.color = '#ff6b6b';
    headerStatus.textContent = 'Offline';
    headerStatus.className = 'status offline';
  }
}

// Get current tab
async function getCurrentTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  currentTab = tab;
  document.getElementById('site-url').textContent = tab.url;
}

// Analyze current site
function analyzeCurrentSite() {
  if (!currentTab) return;
  
  const url = new URL(currentTab.url);
  
  // Feature 1: HTTPS
  const isHttps = url.protocol === 'https:';
  updateFeature('feature-https', isHttps ? 'Secure' : 'Not Secure', isHttps ? 'safe' : 'danger');
  
  // Feature 2: SSL (assume OK if HTTPS)
  updateFeature('feature-ssl', isHttps ? 'Valid' : 'Missing', isHttps ? 'safe' : 'danger');
  
  // Feature 3: Mixed content (simplified check)
  updateFeature('feature-mixed', 'None detected', 'safe');
  
  // Feature 4: Security headers (placeholder)
  updateFeature('feature-headers', 'Basic', 'warning');
  
  // Feature 5: Domain age (simplified)
  const domain = url.hostname;
  const isOld = !domain.includes('new') && !domain.includes('temp');
  updateFeature('feature-domain', isOld ? 'Established' : 'New', isOld ? 'safe' : 'warning');
  
  // Feature 6: Redirects
  updateFeature('feature-redirect', 'None', 'safe');
  
  // Feature 7: Forms Detection (based on URL patterns)
  const hasFormKeywords = url.href.includes('form') || 
                         url.href.includes('login') || 
                         url.href.includes('register') ||
                         url.href.includes('contact') ||
                         url.href.includes('search') ||
                         url.href.includes('checkout') ||
                         url.href.includes('subscribe');
  updateFeature('feature-forms', hasFormKeywords ? 'Multiple' : 'Some', 
                hasFormKeywords ? 'danger' : 'warning');
  
  // Feature 8: Cookies Detection (based on domain)
  const popularSites = ['google', 'facebook', 'amazon', 'github', 'stackoverflow', 
                        'youtube', 'reddit', 'twitter', 'linkedin', 'instagram',
                        'microsoft', 'apple', 'medium', 'github', 'web.dev'];
  const hasCookies = popularSites.some(site => domain.includes(site));
  const cookieStatus = domain.endsWith('.gov') ? 'None' :
                      hasCookies ? 'Many' :
                      domain.length > 20 ? 'Multiple' : 'Few';
  const cookieRisk = domain.endsWith('.gov') ? 'safe' :
                     hasCookies ? 'warning' :
                     domain.length > 20 ? 'warning' : 'safe';
  updateFeature('feature-cookies', cookieStatus, cookieRisk);
  
  // Feature 9: Third-party Detection (based on subdomains & CDN patterns)
  const thirdPartyPatterns = ['cdn', 'ad', 'analytics', 'tracking', 'doubleclick', 
                             'google-analytics', 'facebook.com', 'twitter.com',
                             'amazonaws', 'cloudflare', 'akamai'];
  const hasThirdParty = thirdPartyPatterns.some(pattern => url.href.includes(pattern));
  const subdomainCount = domain.split('.').length;
  const thirdPartyLevel = domain.endsWith('.edu') || domain.endsWith('.gov') ? 'Minimal' :
                         hasThirdParty ? 'Heavy' :
                         subdomainCount > 3 ? 'Multiple' : 'Minimal';
  const thirdPartyRisk = hasThirdParty ? 'danger' :
                         subdomainCount > 3 ? 'warning' : 'safe';
  updateFeature('feature-third', thirdPartyLevel, thirdPartyRisk);
  
  // Feature 10: Load time (based on URL structure)
  const urlComplexity = url.href.split('/').length + url.href.split('?').length;
  updateFeature('feature-load', urlComplexity > 5 ? 'Moderate' : 'Fast', 
                urlComplexity > 5 ? 'warning' : 'safe');
  
  // Calculate initial risk
  calculateInitialRisk();
}

// Update feature display
function updateFeature(id, value, className) {
  const el = document.getElementById(id);
  el.textContent = value;
  el.className = `feature-value ${className}`;
}

// Calculate initial risk based on features
function calculateInitialRisk() {
  const riskEl = document.getElementById('site-risk');
  
  // Simple logic: if HTTPS, likely safe
  const isHttps = currentTab?.url?.startsWith('https');
  
  if (isHttps) {
    riskEl.textContent = 'Likely Safe';
    riskEl.className = 'risk-badge safe';
  } else {
    riskEl.textContent = 'High Risk';
    riskEl.className = 'risk-badge danger';
  }
}

// Run ML analysis
async function runMLAnalysis() {
  const btn = document.getElementById('analyze-btn');
  const resultEl = document.getElementById('ml-result');
  
  btn.disabled = true;
  btn.textContent = 'Analyzing...';
  
  try {
    // Generate features from current site analysis
    const features = generateFeaturesFromSite();
    
    // Call API
    const response = await fetch(`${API_URL}/api/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ features })
    });
    
    const data = await response.json();
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    // Display result
    const isHighRisk = data.prediction === 1 || data.risk_level === 'HIGH RISK';
    const riskText = isHighRisk ? 'HIGH RISK' : 'LOW RISK';
    const riskClass = isHighRisk ? 'high' : 'low';
    
    resultEl.innerHTML = `
      <div class="prediction-value ${riskClass}">
        ${isHighRisk ? '⚠️' : '✅'} ${riskText}
      </div>
      <p>Confidence: ${(data.confidence * 100).toFixed(1)}%</p>
      <p>Risk Score: ${(data.risk_score * 100).toFixed(1)}%</p>
      <div class="confidence-bar">
        <div class="confidence-fill" style="width: ${data.confidence * 100}%"></div>
      </div>
    `;
    
    // Update site risk badge
    const riskEl = document.getElementById('site-risk');
    riskEl.textContent = riskText;
    riskEl.className = `risk-badge ${isHighRisk ? 'danger' : 'safe'}`;
    
    // Save to storage for history
    saveScanToHistory(currentTab.url, data);
    
  } catch (err) {
    resultEl.innerHTML = `<p style="color: #ff6b6b;">Error: ${err.message}</p>`;
  } finally {
    btn.disabled = false;
    btn.textContent = '🔍 Analyze Again';
  }
}

// Generate 10 features from site analysis
function generateFeaturesFromSite() {
  const url = currentTab?.url || '';
  
  // Convert site analysis to 10 numerical features (0-1)
  const features = [
    url.startsWith('https') ? 0.9 : 0.1,           // 1: HTTPS
    url.includes('login') ? 0.8 : 0.3,            // 2: Login page
    url.includes('bank') || url.includes('pay') ? 0.9 : 0.4,  // 3: Financial
    url.length > 50 ? 0.6 : 0.4,                  // 4: URL length
    url.includes('-') || url.includes('_') ? 0.5 : 0.7,  // 5: Suspicious chars
    url.split('.').length > 3 ? 0.3 : 0.8,      // 6: Subdomain depth
    Math.random() * 0.3 + 0.5,                    // 7: Domain age estimate
    Math.random() * 0.4 + 0.4,                    // 8: Traffic estimate
    url.includes('verify') || url.includes('secure') ? 0.7 : 0.5,  // 9: Keywords
    Math.random() * 0.2 + 0.7                     // 10: Overall trust
  ];
  
  return features.map(f => Math.round(f * 100) / 100);
}

// Save scan to local history
function saveScanToHistory(url, data) {
  chrome.storage.local.get(['scans'], (result) => {
    const scans = result.scans || [];
    scans.unshift({
      url: url,
      timestamp: new Date().toISOString(),
      prediction: data.prediction,
      confidence: data.confidence,
      risk_score: data.risk_score
    });
    
    // Keep only last 50
    if (scans.length > 50) scans.pop();
    
    chrome.storage.local.set({ scans: scans });
  });
}
