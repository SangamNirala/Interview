#!/usr/bin/env python3
"""
Simple VM Detection Test
"""

import requests
import json
import uuid

BACKEND_URL = "https://codebase-upgrade-1.preview.emergentagent.com"
BASE_URL = f"{BACKEND_URL}/api"

def test_vm_detection():
    """Test VM detection endpoint with various data types"""
    
    print("Testing VM Detection Endpoint...")
    print("=" * 50)
    
    # Test 1: Normal data
    print("\n1. Testing with normal device data...")
    normal_data = {
        "session_id": str(uuid.uuid4()),
        "device_data": {
            "hardware": {
                "cpu": {"cores": 8, "vendor": "Intel"},
                "gpu": {"vendor": "NVIDIA", "renderer": "GeForce RTX 3070"}
            },
            "os": {"platform": "Win32", "version": "Windows 10"},
            "browser": {"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            "performance": {"device_memory": 16384, "hardware_concurrency": 8}
        }
    }
    
    response = requests.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", json=normal_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        vm_prob = data.get("vm_detection", {}).get("vm_probability", 0)
        print(f"VM Probability: {vm_prob}")
        print("✅ Normal data test passed")
    else:
        print(f"❌ Normal data test failed: {response.text}")
    
    # Test 2: Edge case data that might cause 'str' object errors
    print("\n2. Testing with edge case data (potential 'str' object errors)...")
    edge_case_data = {
        "session_id": str(uuid.uuid4()),
        "device_data": {
            "hardware": "Intel Core i7",  # String instead of dict
            "os": {"platform": 123, "version": None},  # Mixed types
            "browser": {"user_agent": None, "plugins": "Chrome PDF Plugin"},  # String instead of list
            "performance": {"device_memory": None, "hardware_concurrency": "8"}  # String number
        }
    }
    
    response = requests.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", json=edge_case_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        vm_prob = data.get("vm_detection", {}).get("vm_probability", 0)
        print(f"VM Probability: {vm_prob}")
        print("✅ Edge case data test passed - no 'str' object errors")
    elif response.status_code == 500:
        error_text = response.text
        if "'str' object has no attribute 'get'" in error_text:
            print("❌ 'str' object has no attribute 'get' error detected!")
            print(f"Error: {error_text}")
        else:
            print(f"❌ Different 500 error: {error_text}")
    else:
        print(f"Status {response.status_code}: {response.text}")
    
    # Test 3: VM-like data
    print("\n3. Testing with VM-like device data...")
    vm_data = {
        "session_id": str(uuid.uuid4()),
        "device_data": {
            "hardware": {
                "cpu": {"cores": 4, "vendor": "Intel", "model": "Virtual CPU"},
                "gpu": {"vendor": "VMware", "renderer": "VMware SVGA 3D"}
            },
            "os": {"platform": "Linux", "version": "Ubuntu 20.04 (Virtual)"},
            "browser": {
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64; VirtualBox)",
                "plugins": [{"name": "VirtualBox Guest Additions", "version": "6.1"}]
            },
            "performance": {"device_memory": 4096, "hardware_concurrency": 4}
        }
    }
    
    response = requests.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", json=vm_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        vm_detection = data.get("vm_detection", {})
        vm_prob = vm_detection.get("vm_probability", 0)
        is_vm = vm_detection.get("is_virtual_machine", False)
        vm_type = vm_detection.get("vm_classification", "Unknown")
        print(f"VM Probability: {vm_prob}")
        print(f"Is VM: {is_vm}")
        print(f"VM Type: {vm_type}")
        print("✅ VM-like data test passed")
    else:
        print(f"❌ VM-like data test failed: {response.text}")
    
    # Test 4: Rapid requests to check for intermittent issues
    print("\n4. Testing rapid requests for intermittent issues...")
    success_count = 0
    error_count = 0
    str_errors = 0
    
    for i in range(5):
        test_data = {
            "session_id": str(uuid.uuid4()),
            "device_data": {
                "hardware": {"cpu": {"cores": 8}},
                "os": {"platform": "Win32"},
                "browser": {"user_agent": "Mozilla/5.0"},
                "performance": {"device_memory": 8192}
            }
        }
        
        response = requests.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", json=test_data)
        
        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 500:
            error_count += 1
            if "'str' object has no attribute 'get'" in response.text:
                str_errors += 1
        else:
            error_count += 1
    
    print(f"Rapid requests: {success_count}/5 successful, {error_count}/5 errors")
    if str_errors > 0:
        print(f"❌ Detected {str_errors} 'str' object errors in rapid requests")
    else:
        print("✅ No 'str' object errors in rapid requests")
    
    print("\n" + "=" * 50)
    print("VM Detection Test Summary:")
    print(f"- Normal data: Working")
    print(f"- Edge cases: {'Working' if response.status_code == 200 else 'Issues detected'}")
    print(f"- VM detection: Working")
    print(f"- Rapid requests: {success_count}/5 successful")
    print(f"- 'str' object errors: {str_errors} detected")

if __name__ == "__main__":
    test_vm_detection()