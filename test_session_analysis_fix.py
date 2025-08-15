#!/usr/bin/env python3
"""
Quick test to verify the session analysis endpoint fix
"""

import requests
import json
import uuid
from datetime import datetime
import time
import random

# Configuration
BACKEND_URL = "https://security-keystroke.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

def test_session_analysis_endpoint():
    """Test the session analysis endpoint directly"""
    session = requests.Session()
    
    # Authenticate
    print("🔐 Authenticating...")
    auth_response = session.post(
        f"{BACKEND_URL}/admin/login",
        json={"password": ADMIN_PASSWORD}
    )
    
    if auth_response.status_code != 200:
        print(f"❌ Authentication failed: {auth_response.status_code}")
        return False
    
    print("✅ Authentication successful")
    
    # Test session analysis with a sample session ID
    test_session_id = str(uuid.uuid4())
    print(f"🎯 Testing session analysis for session: {test_session_id}")
    
    try:
        response = session.get(
            f"{BACKEND_URL}/security/advanced-biometrics/session-analysis/{test_session_id}",
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS: Session analysis endpoint is working!")
            print(f"Response keys: {list(data.keys())}")
            
            if "session_summary" in data:
                session_summary = data["session_summary"]
                print(f"Session summary keys: {list(session_summary.keys())}")
                print(f"Session ID: {session_summary.get('session_id')}")
                print(f"Analysis Overview: {session_summary.get('analysis_overview', {})}")
            
            return True
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Error: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 TESTING SESSION ANALYSIS ENDPOINT FIX")
    print("=" * 50)
    
    success = test_session_analysis_endpoint()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 SUCCESS: Session analysis endpoint is working correctly!")
    else:
        print("❌ FAILURE: Session analysis endpoint still has issues")