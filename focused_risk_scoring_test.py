#!/usr/bin/env python3
"""
Focused Real-time Risk Scoring System Test
Testing specific endpoints that showed issues
"""

import requests
import json
import uuid
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BACKEND_URL = 'https://tracking-backend.preview.emergentagent.com'
BASE_URL = f"{BACKEND_URL}/api"

def test_endpoint(name, method, url, data=None):
    """Test a specific endpoint"""
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    try:
        if method == 'POST':
            response = session.post(url, json=data, timeout=30)
        else:
            response = session.get(url, timeout=30)
        
        print(f"🔍 {name}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        print()
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ {name}")
        print(f"   Error: {str(e)}")
        print()
        return False

def main():
    print("🎯 FOCUSED REAL-TIME RISK SCORING ENDPOINT TESTING")
    print("=" * 60)
    
    test_session_id = str(uuid.uuid4())
    
    # Test 1: Risk Factor Updates
    test_endpoint(
        "Risk Factor Updates",
        "POST",
        f"{BASE_URL}/risk-scoring/update-risk-factors",
        {
            "session_id": test_session_id,
            "new_response_data": {
                "question_id": "q1",
                "answer": "Test answer",
                "response_time": 30.0,
                "confidence_level": 0.8
            }
        }
    )
    
    # Test 2: Alert Triggering
    test_endpoint(
        "Alert Triggering",
        "POST", 
        f"{BASE_URL}/risk-scoring/trigger-alerts",
        {
            "session_id": test_session_id,
            "current_risk_assessment": {
                "composite_risk_score": 0.75,
                "risk_level": "HIGH"
            }
        }
    )
    
    # Test 3: Risk History
    test_endpoint(
        "Risk History",
        "GET",
        f"{BASE_URL}/risk-scoring/risk-history/{test_session_id}"
    )
    
    # Test 4: Composite Score Calculation
    test_endpoint(
        "Composite Score Calculation",
        "POST",
        f"{BASE_URL}/risk-scoring/calculate-composite-score",
        {
            "session_id": test_session_id,
            "current_response_data": {
                "question_id": "q1",
                "answer": "Test answer",
                "response_time": 30.0
            }
        }
    )

if __name__ == "__main__":
    main()