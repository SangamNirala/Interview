#!/usr/bin/env python3
"""
Testing script to verify the 4 API parameter fixes for PHASE 1.1 Enhanced Device Fingerprinting
"""

import requests
import json
import uuid

# Configuration
BACKEND_URL = "https://deviceprint.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class ParameterFixTester:
    def __init__(self):
        self.session = requests.Session()
        self.session_id = str(uuid.uuid4())
        self.device_id = str(uuid.uuid4())
        self.test_results = []
        
    def log_result(self, test_name, success, details):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
    def authenticate_admin(self):
        """Authenticate as admin"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/login",
                json={"password": ADMIN_PASSWORD}
            )
            return response.status_code == 200
        except:
            return False

    def generate_test_device_data(self):
        """Generate test device data"""
        return {
            "hardware": {
                "cpu": {"cores": 8, "architecture": "x64", "vendor": "Intel", "model": "Core i7", "frequency": 3200},
                "gpu": {"vendor": "NVIDIA", "renderer": "GeForce RTX 3070", "version": "OpenGL 4.6", "memory": 8192},
                "memory": {"total_memory": 17179869184, "available_memory": 8589934592, "memory_type": "DDR4", "speed": 3200},
                "storage": {"total_storage": 1099511627776, "available_storage": 549755813888, "storage_type": "SSD", "filesystem": "NTFS"}
            },
            "os": {
                "platform": "Windows 10", "version": "10.0.19042", "architecture": "AMD64", "build": "19042"
            },
            "browser": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "browser_name": "Chrome", "browser_version": "96.0.4664.110"
            },
            "network": {
                "connection_type": "ethernet", "effective_type": "4g"
            },
            "screen": {
                "width": 1920, "height": 1080, "color_depth": 24
            },
            "performance": {
                "memory_usage": {"used": 8589934592, "total": 17179869184}
            }
        }

    def test_generate_device_signature_fix(self):
        """Test Fix 1: generate-device-signature (NoneType error)"""
        try:
            # Test 1: Valid device data (should work)
            valid_data = {
                "device_data": self.generate_test_device_data(),
                "session_id": self.session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=valid_data
            )
            
            if response.status_code == 200:
                self.log_result("Generate Device Signature (Valid Data)", True, f"Success: {response.status_code}")
            else:
                self.log_result("Generate Device Signature (Valid Data)", False, f"Failed: {response.status_code} - {response.text}")
                
            # Test 2: None device data (should return 400)
            invalid_data = {
                "device_data": None,
                "session_id": self.session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=invalid_data
            )
            
            if response.status_code == 400:
                self.log_result("Generate Device Signature (None Data)", True, f"Correctly rejected: {response.status_code}")
            else:
                self.log_result("Generate Device Signature (None Data)", False, f"Should be 400: {response.status_code}")
                
        except Exception as e:
            self.log_result("Generate Device Signature Fix", False, f"Exception: {str(e)}")

    def test_detect_virtual_machines_fix(self):
        """Test Fix 2: detect-virtual-machines (confidence_level error)"""
        try:
            valid_data = {
                "device_data": self.generate_test_device_data(),
                "session_id": self.session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                json=valid_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'vm_detection' in data and 'confidence_level' in str(data):
                    self.log_result("Detect Virtual Machines", True, f"Success with confidence_level: {response.status_code}")
                else:
                    self.log_result("Detect Virtual Machines", False, f"Missing confidence_level in response")
            else:
                self.log_result("Detect Virtual Machines", False, f"Failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.log_result("Detect Virtual Machines Fix", False, f"Exception: {str(e)}")

    def test_analyze_hardware_fix(self):
        """Test Fix 3: analyze-hardware (missing device_data field)"""
        try:
            # Test 1: Valid device data with hardware field
            valid_data = {
                "device_data": self.generate_test_device_data(),
                "session_id": self.session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
                json=valid_data
            )
            
            if response.status_code == 200:
                self.log_result("Analyze Hardware (Valid Data)", True, f"Success: {response.status_code}")
            else:
                self.log_result("Analyze Hardware (Valid Data)", False, f"Failed: {response.status_code} - {response.text}")
                
            # Test 2: Device data without hardware field
            invalid_data = {
                "device_data": {"os": {"platform": "Windows"}},  # No hardware field
                "session_id": self.session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
                json=invalid_data
            )
            
            if response.status_code == 400:
                self.log_result("Analyze Hardware (No Hardware Field)", True, f"Correctly rejected: {response.status_code}")
            else:
                self.log_result("Analyze Hardware (No Hardware Field)", False, f"Should be 400: {response.status_code}")
                
        except Exception as e:
            self.log_result("Analyze Hardware Fix", False, f"Exception: {str(e)}")

    def test_track_device_consistency_fix(self):
        """Test Fix 4: track-device-consistency (missing current_signature field)"""
        try:
            # Test 1: Valid data with current_signature
            valid_data = {
                "device_id": self.device_id,
                "current_signature": {
                    "hardware": {"cpu": "Intel Core i7"},
                    "signature_hash": "test_hash_123"
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json=valid_data
            )
            
            if response.status_code == 200:
                self.log_result("Track Device Consistency (Valid Data)", True, f"Success: {response.status_code}")
            else:
                self.log_result("Track Device Consistency (Valid Data)", False, f"Failed: {response.status_code} - {response.text}")
                
            # Test 2: Missing current_signature
            invalid_data = {
                "device_id": self.device_id,
                "current_signature": None
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json=invalid_data
            )
            
            if response.status_code == 400:
                self.log_result("Track Device Consistency (None Signature)", True, f"Correctly rejected: {response.status_code}")
            else:
                self.log_result("Track Device Consistency (None Signature)", False, f"Should be 400: {response.status_code}")
                
        except Exception as e:
            self.log_result("Track Device Consistency Fix", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all parameter fix tests"""
        print("🧪 Testing PHASE 1.1 API Parameter Fixes")
        print("=" * 50)
        
        # Authenticate
        if not self.authenticate_admin():
            print("❌ Admin authentication failed")
            return
        
        print("✅ Admin authenticated successfully")
        print()
        
        # Run individual tests
        self.test_generate_device_signature_fix()
        self.test_detect_virtual_machines_fix()
        self.test_analyze_hardware_fix()
        self.test_track_device_consistency_fix()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests / total_tests) * 100:.1f}%")

if __name__ == "__main__":
    tester = ParameterFixTester()
    tester.run_all_tests()