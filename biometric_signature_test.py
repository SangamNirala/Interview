#!/usr/bin/env python3
"""
Test biometric signature generation with proper data
"""

import requests
import json
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://session-monitor.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

def create_session_with_keystroke_data(session_id):
    """Create a session with substantial keystroke data"""
    
    # Create realistic keystroke data for typing "Hello World"
    keystroke_data = []
    text = "Hello World"
    base_time = 1234567890.0
    
    for i, char in enumerate(text):
        keystroke_data.append({
            "key": char.lower(),
            "keydown_time": base_time + i * 0.15,
            "keyup_time": base_time + i * 0.15 + 0.08,
            "dwell_time": 80 + (i % 3) * 10,  # Vary dwell time
            "flight_time": 45 + (i % 4) * 5   # Vary flight time
        })
    
    test_data = {
        "session_id": session_id,
        "keystroke_data": keystroke_data,
        "mouse_data": [
            {
                "x": 100 + i * 10,
                "y": 200 + i * 5,
                "timestamp": base_time + i * 0.1,
                "velocity": 5.0 + i * 0.2,
                "acceleration": 1.0 + i * 0.1
            } for i in range(10)
        ],
        "consent_given": True
    }
    
    response = requests.post(
        f"{BASE_URL}/security/biometric-data/submit",
        json=test_data,
        timeout=30
    )
    
    return response.status_code == 200

def test_signature_generation():
    """Test signature generation with multiple sessions"""
    print("🧪 Testing Biometric Signature Generation with Proper Data")
    print("=" * 60)
    
    # Create 3 sessions with keystroke data
    session_ids = []
    for i in range(3):
        session_id = str(uuid.uuid4())
        session_ids.append(session_id)
        
        success = create_session_with_keystroke_data(session_id)
        if success:
            print(f"✅ Created session {i+1} with keystroke data: {session_id}")
        else:
            print(f"❌ Failed to create session {i+1}: {session_id}")
            return False
    
    # Now try to generate signature
    print(f"\n🔐 Attempting to generate biometric signature from {len(session_ids)} sessions...")
    
    response = requests.post(
        f"{BASE_URL}/security/biometric-signature/generate",
        json=session_ids,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            signature_id = result.get("signature_id")
            sessions_analyzed = result.get("sessions_analyzed")
            print(f"✅ Signature generated successfully!")
            print(f"   - Signature ID: {signature_id}")
            print(f"   - Sessions analyzed: {sessions_analyzed}")
            return True
        else:
            print(f"❌ API returned success=false: {result}")
            return False
    else:
        print(f"❌ HTTP {response.status_code}: {response.text}")
        return False

if __name__ == "__main__":
    success = test_signature_generation()
    if success:
        print("\n🎉 Biometric signature generation test PASSED!")
    else:
        print("\n❌ Biometric signature generation test FAILED!")