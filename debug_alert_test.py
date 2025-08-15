#!/usr/bin/env python3
"""
Debug Alert Triggering Issue
"""

import requests
import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BACKEND_URL = 'https://session-monitor.preview.emergentagent.com'
BASE_URL = f"{BACKEND_URL}/api"

def test_alert_with_minimal_data():
    """Test alert triggering with minimal data"""
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    # Test with minimal data
    test_data = {
        "session_id": "minimal-test"
    }
    
    try:
        response = session.post(f"{BASE_URL}/risk-scoring/trigger-alerts", 
                              json=test_data, timeout=30)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def test_alert_with_low_risk():
    """Test alert triggering with low risk score"""
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    # Test with low risk score (should not trigger alerts)
    test_data = {
        "session_id": "low-risk-test",
        "current_risk_assessment": {
            "composite_risk_score": 0.1,
            "risk_level": "MINIMAL"
        }
    }
    
    try:
        response = session.post(f"{BASE_URL}/risk-scoring/trigger-alerts", 
                              json=test_data, timeout=30)
        
        print(f"Low Risk Test - Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("🔍 DEBUG ALERT TRIGGERING")
    print("=" * 40)
    
    print("\n1. Testing with minimal data:")
    test_alert_with_minimal_data()
    
    print("\n2. Testing with low risk score:")
    test_alert_with_low_risk()