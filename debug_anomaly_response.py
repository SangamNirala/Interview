#!/usr/bin/env python3
"""
Debug script to see what the anomaly detection endpoint actually returns
"""

import requests
import json

# Backend URL
BACKEND_URL = "https://fprintshield.preview.emergentagent.com/api"

def test_response_structure():
    print("🔍 Debugging Anomaly Detection Response Structure")
    
    # Authenticate
    auth_response = requests.post(
        f"{BACKEND_URL}/admin/login",
        json={"password": "Game@1234"},
        timeout=30
    )
    
    if auth_response.status_code != 200:
        print(f"❌ Authentication failed: {auth_response.status_code}")
        return
    
    # Test session data
    test_session = {
        "session_id": "debug_session_001",
        "candidate_name": "Debug User",
        "responses": [
            {
                "question_id": "q1",
                "response": "A", 
                "is_correct": True,
                "response_time": 45.2,
                "difficulty": 0.5,
                "topic": "numerical"
            },
            {
                "question_id": "q2",
                "response": "B", 
                "is_correct": False,
                "response_time": 38.7,
                "difficulty": 0.6,
                "topic": "logical"
            }
        ]
    }
    
    # Call anomaly detection
    response = requests.post(
        f"{BACKEND_URL}/anomaly-detection/calculate-anomaly-probability-scores",
        json={"session_data": test_session},
        timeout=60
    )
    
    print(f"📊 Response Status: {response.status_code}")
    print(f"📝 Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        response_data = response.json()
        print(f"✅ Response successful!")
        print(f"📋 Full Response Structure:")
        print(json.dumps(response_data, indent=2))
        
        if 'probability_results' in response_data:
            print(f"\n🎯 Probability Results Structure:")
            print(json.dumps(response_data['probability_results'], indent=2))
        else:
            print(f"\n⚠️  No 'probability_results' field found in response")
            print(f"Available fields: {list(response_data.keys())}")
    else:
        print(f"❌ Response failed: {response.text}")

if __name__ == "__main__":
    test_response_structure()