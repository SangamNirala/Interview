#!/usr/bin/env python3
"""
Debug Alert Triggering Issue - Test with proper format
"""

import requests
import json
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BACKEND_URL = 'https://dbcollections-setup.preview.emergentagent.com'
BASE_URL = f"{BACKEND_URL}/api"

def test_alert_with_proper_format():
    """Test alert triggering with proper risk assessment format"""
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    # Test with proper format including success field
    test_data = {
        "session_id": "proper-format-test",
        "current_risk_assessment": {
            "success": True,
            "composite_risk_score": 0.4,
            "risk_level": "MEDIUM",
            "risk_breakdown": {
                "statistical_anomalies": 0.4,
                "behavioral_biometrics": 0.3
            }
        }
    }
    
    try:
        response = session.post(f"{BASE_URL}/risk-scoring/trigger-alerts", 
                              json=test_data, timeout=30)
        
        print(f"Proper Format Test - Status: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
    except Exception as e:
        print(f"Error: {str(e)}")

def test_alert_with_high_risk():
    """Test alert triggering with high risk score"""
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    # Test with high risk score to trigger alerts
    test_data = {
        "session_id": "high-risk-test",
        "current_risk_assessment": {
            "success": True,
            "composite_risk_score": 0.8,
            "risk_level": "HIGH",
            "risk_breakdown": {
                "statistical_anomalies": 0.8,
                "behavioral_biometrics": 0.7
            }
        }
    }
    
    try:
        response = session.post(f"{BASE_URL}/risk-scoring/trigger-alerts", 
                              json=test_data, timeout=30)
        
        print(f"High Risk Test - Status: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("🔍 DEBUG ALERT TRIGGERING - PROPER FORMAT")
    print("=" * 50)
    
    print("\n1. Testing with proper format (MEDIUM risk):")
    test_alert_with_proper_format()
    
    print("\n2. Testing with high risk score:")
    test_alert_with_high_risk()