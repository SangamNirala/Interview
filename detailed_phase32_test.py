#!/usr/bin/env python3
"""
Detailed testing of Phase 3.2 remaining methods with response analysis
"""

import requests
import json
import uuid
from datetime import datetime

# Configuration
BACKEND_URL = "https://browser-fingerprint-1.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

def test_detailed_network_analysis():
    """Test network analysis with detailed response examination"""
    session = requests.Session()
    
    # Authenticate
    auth_response = session.post(f"{BACKEND_URL}/admin/login", json={"password": ADMIN_PASSWORD})
    if auth_response.status_code != 200:
        print("❌ Authentication failed")
        return
    
    print("✅ Admin authenticated successfully")
    
    # Test comprehensive network data
    network_data = {
        "ip_address": "192.168.1.100",
        "public_ip": "203.0.113.45",
        "isp_info": {
            "name": "Comcast Cable Communications",
            "organization": "Comcast",
            "country": "United States",
            "region": "California",
            "city": "San Francisco",
            "timezone": "America/Los_Angeles",
            "connection_type": "cable"
        },
        "geolocation": {
            "latitude": 37.7749,
            "longitude": -122.4194,
            "accuracy": 50,
            "country": "US",
            "region": "CA",
            "city": "San Francisco"
        },
        "network_performance": {
            "download_speed": 150.5,
            "upload_speed": 25.3,
            "latency": 15,
            "jitter": 2.1,
            "packet_loss": 0.1
        },
        "routing_info": {
            "hop_count": 12,
            "route_consistency": True,
            "autonomous_system": "AS7922",
            "bgp_prefix": "203.0.113.0/24"
        }
    }
    
    payload = {
        "session_id": str(uuid.uuid4()) + "_detailed_network_test",
        "network_data": network_data
    }
    
    response = session.post(f"{BACKEND_URL}/session-fingerprinting/monitor-network-characteristics", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Network Analysis Response Structure:")
        print(f"   - Success: {data.get('success')}")
        print(f"   - Network Analysis Keys: {list(data.get('network_analysis', {}).keys())}")
        
        network_analysis = data.get('network_analysis', {}).get('network_analysis', {})
        if network_analysis:
            print(f"   - IP Analysis: {network_analysis.get('ip_analysis', {}).get('geolocation', {}).get('ip_address')}")
            print(f"   - Reputation Score: {network_analysis.get('reputation_analysis', {}).get('score')}")
            print(f"   - Proxy Detected: {network_analysis.get('proxy_vpn_detection', {}).get('proxy_detected')}")
            print(f"   - Risk Level: {network_analysis.get('risk_assessment', {}).get('risk_level')}")
        
        print(f"   - Storage Confirmation: {data.get('storage_confirmation')}")
        print()
    else:
        print(f"❌ Network analysis failed: {response.status_code}")

def test_detailed_timezone_analysis():
    """Test timezone analysis with detailed response examination"""
    session = requests.Session()
    
    # Authenticate
    auth_response = session.post(f"{BACKEND_URL}/admin/login", json={"password": ADMIN_PASSWORD})
    if auth_response.status_code != 200:
        print("❌ Authentication failed")
        return
    
    print("✅ Admin authenticated successfully")
    
    # Test comprehensive timezone data with mismatches
    timezone_data = {
        "system_timezone": "America/Los_Angeles",  # West Coast
        "browser_timezone": "America/New_York",   # East Coast - mismatch!
        "timezone_offset": -480,  # PST offset but browser says EST
        "dst_active": False,
        "geolocation_timezone": "Europe/London",  # Different continent - major mismatch!
        "ip_timezone": "Asia/Tokyo",              # Another continent - major mismatch!
        "system_time": "2024-01-15T11:30:00-08:00",  # PST
        "browser_time": "2024-01-15T14:30:00-05:00", # EST - 3 hour difference
        "server_time": "2024-01-15T19:30:00Z",
        "time_sync_accuracy": {
            "ntp_synchronized": False,  # Not synchronized
            "time_drift": 15.5,  # Large drift
            "last_sync": "2024-01-10T10:00:00-08:00"  # Old sync
        },
        "geolocation_data": {
            "latitude": 51.5074,   # London coordinates
            "longitude": -0.1278,
            "accuracy": 1000,      # Low accuracy
            "country": "GB",
            "region": "England",
            "city": "London"
        },
        "user_behavior": {
            "active_hours": [2, 3, 4, 5, 6, 7, 8, 9, 10],  # Unusual hours for claimed timezone
            "typical_timezone": "America/Los_Angeles",
            "session_start_time": "2024-01-15T11:30:00-08:00"
        },
        "manipulation_indicators": {
            "timezone_spoofing": True,
            "geolocation_spoofing": True,
            "time_manipulation": True,
            "vpn_usage": True
        }
    }
    
    payload = {
        "session_id": str(uuid.uuid4()) + "_detailed_timezone_test",
        "timezone_data": timezone_data
    }
    
    response = session.post(f"{BACKEND_URL}/session-fingerprinting/track-timezone-consistency", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Timezone Analysis Response Structure:")
        print(f"   - Success: {data.get('success')}")
        print(f"   - Timezone Analysis Keys: {list(data.get('timezone_analysis', {}).keys())}")
        
        timezone_analysis = data.get('timezone_analysis', {}).get('timezone_analysis', {})
        if timezone_analysis:
            print(f"   - System Timezone: {timezone_analysis.get('timezone_identity', {}).get('system_timezone')}")
            print(f"   - Browser Timezone: {timezone_analysis.get('timezone_identity', {}).get('browser_timezone')}")
            print(f"   - Manipulation Detected: {timezone_analysis.get('manipulation_detection', {}).get('manipulation_detected')}")
            print(f"   - Consistency Score: {timezone_analysis.get('consistency_score')}")
            print(f"   - Risk Level: {timezone_analysis.get('risk_assessment', {}).get('risk_level')}")
        
        print(f"   - Storage Confirmation: {data.get('storage_confirmation')}")
        print()
    else:
        print(f"❌ Timezone analysis failed: {response.status_code}")

if __name__ == "__main__":
    print("🎯 DETAILED PHASE 3.2 TESTING - NETWORK & TIMEZONE ANALYSIS")
    print("=" * 70)
    
    print("📊 Testing Network Characteristics Analysis:")
    test_detailed_network_analysis()
    
    print("📊 Testing Timezone Consistency Analysis:")
    test_detailed_timezone_analysis()
    
    print("🎉 Detailed testing completed!")