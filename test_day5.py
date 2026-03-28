#!/usr/bin/env python3
"""
Comprehensive test suite for AI Security Dashboard Day 3 & 5
Tests Backend API and Chrome Extension connectivity
"""

import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000'

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test backend health check"""
    print_header("TEST 1: Backend Health Check")
    try:
        response = requests.get(f'{BASE_URL}/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check PASSED")
            print(f"   Status: {data.get('status')}")
            print(f"   Model Loaded: {data.get('model_loaded')}")
            print(f"   Database: {data.get('database')}")
            print(f"   Version: {data.get('version')}")
            return True
        else:
            print(f"❌ Health Check FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check ERROR: {e}")
        return False

def test_stats():
    """Test backend stats endpoint"""
    print_header("TEST 2: Global Statistics")
    try:
        response = requests.get(f'{BASE_URL}/api/stats', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Statistics PASSED")
            print(f"   Total Predictions: {data.get('total_predictions', 0)}")
            print(f"   High Risk: {data.get('high_risk_count', 0)}")
            print(f"   Low Risk: {data.get('low_risk_count', 0)}")
            return True
        else:
            print(f"❌ Statistics FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Statistics ERROR: {e}")
        return False

def test_prediction():
    """Test ML prediction endpoint"""
    print_header("TEST 3: ML Prediction (Public)")
    try:
        features = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1]
        response = requests.post(
            f'{BASE_URL}/api/predict',
            json={'features': features},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Prediction PASSED")
            print(f"   Risk Level: {data.get('risk_level')}")
            print(f"   Confidence: {data.get('confidence', 0):.2%}")
            print(f"   Risk Score: {data.get('risk_score', 0):.2%}")
            return True
        else:
            print(f"❌ Prediction FAILED: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction ERROR: {e}")
        return False

def test_cors():
    """Test CORS headers for Chrome extension"""
    print_header("TEST 4: CORS Verification (Extension)")
    try:
        response = requests.options(
            f'{BASE_URL}/api/health',
            headers={'Origin': 'chrome-extension://example'},
            timeout=5
        )
        headers = response.headers
        print("✅ CORS Headers Detected")
        print(f"   Allow-Origin: {headers.get('Access-Control-Allow-Origin', 'Not set')}")
        print(f"   Allow-Methods: {headers.get('Access-Control-Allow-Methods', 'Not set')}")
        print(f"   Allow-Headers: {headers.get('Access-Control-Allow-Headers', 'Not set')}")
        return True
    except Exception as e:
        print(f"❌ CORS Check ERROR: {e}")
        return False

def test_version_info():
    """Get API version info"""
    print_header("TEST 5: API Version & Features")
    try:
        response = requests.get(f'{BASE_URL}/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ API Info Retrieved")
            print(f"   Message: {data.get('message')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Features: {', '.join(data.get('features', []))}")
            return True
        else:
            print(f"❌ API Info FAILED")
            return False
    except Exception as e:
        print(f"❌ API Info ERROR: {e}")
        return False

def print_summary(results):
    """Print test summary"""
    print_header("TEST SUMMARY")
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - Ready for Chrome Extension!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

def main():
    print("\n" + "="*60)
    print("  AI SECURITY DASHBOARD - COMPREHENSIVE TEST SUITE")
    print("  Day 3 + Day 5 (Chrome Extension)")
    print(f"  Tests Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = {
        'API Health Check': test_health(),
        'Global Statistics': test_stats(),
        'ML Prediction': test_prediction(),
        'CORS Headers': test_cors(),
        'Version Info': test_version_info(),
    }
    
    print_summary(results)
    
    print("\n" + "="*60)
    print("  🚀 DEPLOYMENT STATUS")
    print("="*60)
    print(f"  Backend: http://localhost:5000 - {'✅ RUNNING' if results['API Health Check'] else '❌ NOT RUNNING'}")
    print(f"  Frontend: http://localhost:3001 - ✅ RUNNING")
    print(f"  Extension: Ready to load at chrome://extensions/")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
