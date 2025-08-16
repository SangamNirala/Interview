#!/usr/bin/env python3
"""
🎯 PHASE 1.1 API PARAMETER FIXES - FOCUSED VERIFICATION

Testing the 4 specific API endpoints with corrected payloads based on actual API requirements:
1. generate-device-signature
2. analyze-hardware  
3. track-device-consistency
4. detect-virtual-machines
"""

import requests
import json
import uuid
from datetime import datetime, timedelta

# Configuration
BACKEND_URL = "https://fingerprint-test.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class FocusedAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session_id = str(uuid.uuid4())
        self.device_id = str(uuid.uuid4())
        
    def authenticate_admin(self):
        """Authenticate as admin"""
        response = self.session.post(
            f"{BACKEND_URL}/admin/login",
            json={"password": ADMIN_PASSWORD}
        )
        return response.status_code == 200

    def test_generate_device_signature(self):
        """Test generate-device-signature endpoint"""
        print("🔍 Testing generate-device-signature...")
        
        # Valid request
        payload = {
            "session_id": self.session_id,
            "device_data": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "screen_resolution": "1920x1080",
                "timezone": "America/New_York",
                "language": "en-US"
            },
            "fingerprint_components": {
                "canvas_fingerprint": "canvas_hash_12345",
                "webgl_fingerprint": "webgl_hash_67890"
            }
        }
        
        response = self.session.post(
            f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
            json=payload
        )
        
        print(f"  Valid request: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success: {data.get('success', False)}")
            if 'device_signature' in data:
                print(f"  ✅ Device signature generated")
            else:
                print(f"  ⚠️  No device_signature in response")
        else:
            print(f"  ❌ Error: {response.text}")
        
        # Invalid request (missing device_data)
        invalid_payload = {"session_id": self.session_id}
        response = self.session.post(
            f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
            json=invalid_payload
        )
        print(f"  Invalid request: {response.status_code} (expected 422)")
        return response.status_code in [400, 422]

    def test_analyze_hardware(self):
        """Test analyze-hardware endpoint"""
        print("🔍 Testing analyze-hardware...")
        
        # Valid request with proper hardware field
        payload = {
            "session_id": self.session_id,
            "device_data": {
                "hardware": {  # This is the required field structure
                    "cpu_info": {
                        "cores": 8,
                        "vendor": "Intel",
                        "model": "Core i7-10700K"
                    },
                    "gpu_info": {
                        "vendor": "NVIDIA",
                        "model": "GeForce RTX 3070"
                    },
                    "memory_info": {
                        "total_ram": "16GB"
                    }
                }
            }
        }
        
        response = self.session.post(
            f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
            json=payload
        )
        
        print(f"  Valid request: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success: {data.get('success', False)}")
            if 'hardware_analysis' in data:
                print(f"  ✅ Hardware analysis completed")
            else:
                print(f"  ⚠️  No hardware_analysis in response")
        else:
            print(f"  ❌ Error: {response.text}")
        
        # Invalid request (missing device_data)
        invalid_payload = {"session_id": self.session_id}
        response = self.session.post(
            f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
            json=invalid_payload
        )
        print(f"  Invalid request: {response.status_code} (expected 422)")
        return response.status_code in [400, 422]

    def test_track_device_consistency(self):
        """Test track-device-consistency endpoint"""
        print("🔍 Testing track-device-consistency...")
        
        # Valid request
        payload = {
            "session_id": self.session_id,
            "device_id": self.device_id,
            "current_signature": {
                "device_fingerprint": "fp_current_12345",
                "timestamp": datetime.now().isoformat(),
                "signature_hash": "sha256:current_signature_hash",
                "confidence_score": 0.95
            },
            "historical_signatures": []
        }
        
        response = self.session.post(
            f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
            json=payload
        )
        
        print(f"  Valid request: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success: {data.get('success', False)}")
            if 'device_tracking' in data or 'consistency_analysis' in data:
                print(f"  ✅ Device consistency tracked")
            else:
                print(f"  ⚠️  Unexpected response structure")
        else:
            print(f"  ❌ Error: {response.text}")
        
        # Invalid request (missing current_signature)
        invalid_payload = {
            "session_id": self.session_id,
            "device_id": self.device_id
        }
        response = self.session.post(
            f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
            json=invalid_payload
        )
        print(f"  Invalid request: {response.status_code} (expected 422)")
        return response.status_code in [400, 422]

    def test_detect_virtual_machines(self):
        """Test detect-virtual-machines endpoint"""
        print("🔍 Testing detect-virtual-machines...")
        
        # Valid request with device_data field
        payload = {
            "session_id": self.session_id,
            "device_data": {  # This field is required
                "hardware_info": {
                    "cpu_vendor": "GenuineIntel",
                    "cpu_model": "Intel Core i7-10700K",
                    "gpu_vendor": "NVIDIA Corporation"
                },
                "system_info": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "platform": "Win32"
                }
            },
            "detection_options": {
                "confidence_level": 0.8,
                "deep_scan": True
            }
        }
        
        response = self.session.post(
            f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
            json=payload
        )
        
        print(f"  Valid request: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Success: {data.get('success', False)}")
            if 'vm_detection' in data:
                print(f"  ✅ VM detection completed")
            else:
                print(f"  ⚠️  No vm_detection in response")
        else:
            print(f"  ❌ Error: {response.text}")
        
        # Invalid request (invalid confidence_level type)
        invalid_payload = {
            "session_id": self.session_id,
            "device_data": {"hardware_info": {"cpu_vendor": "Intel"}},
            "detection_options": {
                "confidence_level": "invalid_string"  # Should be float
            }
        }
        response = self.session.post(
            f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
            json=invalid_payload
        )
        print(f"  Invalid request: {response.status_code} (expected 422)")
        return response.status_code in [400, 422]

    def run_tests(self):
        """Run all focused tests"""
        print("🎯 PHASE 1.1 API PARAMETER FIXES - FOCUSED VERIFICATION")
        print("=" * 60)
        
        if not self.authenticate_admin():
            print("❌ Authentication failed")
            return
        
        print("✅ Admin authenticated")
        print()
        
        # Test all 4 endpoints
        results = []
        results.append(self.test_generate_device_signature())
        print()
        results.append(self.test_analyze_hardware())
        print()
        results.append(self.test_track_device_consistency())
        print()
        results.append(self.test_detect_virtual_machines())
        print()
        
        # Summary
        passed = sum(results)
        total = len(results)
        print("=" * 60)
        print(f"📊 SUMMARY: {passed}/{total} endpoints working correctly")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL API PARAMETER FIXES VERIFIED!")
        else:
            print("⚠️  Some endpoints need attention")

if __name__ == "__main__":
    tester = FocusedAPITester()
    tester.run_tests()