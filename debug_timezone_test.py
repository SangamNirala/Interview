#!/usr/bin/env python3
"""
Debug test for timezone manipulation endpoint
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import random

BACKEND_URL = "https://integrity-check-2.preview.emergentagent.com/api"

def create_test_session():
    session_id = str(uuid.uuid4())
    base_time = datetime.utcnow() - timedelta(hours=2)
    
    responses = []
    for i in range(10):
        responses.append({
            'question_id': f'q_{i+1}',
            'response': random.choice(['A', 'B', 'C', 'D']),
            'is_correct': random.random() > 0.5,
            'response_time': random.uniform(30, 120),
            'difficulty': random.uniform(0.3, 0.8),
            'topic': 'numerical_reasoning',
            'timestamp': (base_time + timedelta(seconds=i*60)).isoformat()
        })
    
    return {
        'session_id': session_id,
        'candidate_name': 'Debug Test Candidate',
        'responses': responses,
        'session_metadata': {
            'start_time': base_time.isoformat(),
            'end_time': (base_time + timedelta(hours=1)).isoformat(),
            'ip_address': '192.168.1.100',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'timezone': 'America/New_York',
            'location': {'country': 'US', 'region': 'NY'}
        }
    }

def test_timezone_endpoint():
    session_data = create_test_session()
    
    print("Testing timezone manipulation endpoint...")
    print(f"Session ID: {session_data['session_id']}")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/statistical-analysis/identify-timezone-manipulation",
            json={"session_data": session_data},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_timezone_endpoint()