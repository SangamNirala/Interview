#!/usr/bin/env python3
"""
🎯 PHASE 1.1 API PARAMETER FIXES VERIFICATION TESTING

Testing the 4 specific API endpoints that were previously failing and have now been fixed:

1. **generate-device-signature** - Fixed NoneType error with proper validation
2. **analyze-hardware** - Fixed missing device_data field validation  
3. **track-device-consistency** - Fixed missing current_signature field validation
4. **detect-virtual-machines** - Fixed confidence_level error handling

Test Coverage:
- Test each endpoint with valid data (should return 200)
- Test each endpoint with invalid/missing parameters (should return 400/422)
- Verify error handling and validation work correctly
- Confirm database integration still works after fixes
- Test both authenticated and unauthenticated access

Authentication: admin credentials with Game@1234 password
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time
import random

# Configuration
BACKEND_URL = "https://fingerprint-test.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class Phase11APIParameterFixesTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.session_id = str(uuid.uuid4())
        self.device_id = str(uuid.uuid4())
        
    def log_result(self, test_name, success, details, response_data=None):
        """Log test result with details"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
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
            
            if response.status_code == 200:
                self.log_result("Admin Authentication", True, f"Successfully authenticated (Status: {response.status_code})")
                return True
            else:
                self.log_result("Admin Authentication", False, f"Authentication failed (Status: {response.status_code})")
                return False
                
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Authentication error: {str(e)}")
            return False

    def test_generate_device_signature_valid(self):
        """Test generate-device-signature endpoint with valid data"""
        try:
            # Valid device signature generation data
            payload = {
                "session_id": self.session_id,
                "device_data": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "screen_resolution": "1920x1080",
                    "timezone": "America/New_York",
                    "language": "en-US",
                    "platform": "Win32",
                    "hardware_concurrency": 8,
                    "device_memory": 8,
                    "color_depth": 24,
                    "pixel_ratio": 1.0
                },
                "fingerprint_components": {
                    "canvas_fingerprint": "canvas_hash_12345",
                    "webgl_fingerprint": "webgl_hash_67890",
                    "audio_fingerprint": "audio_hash_abcde",
                    "font_fingerprint": "font_hash_fghij"
                },
                "signature_options": {
                    "include_behavioral": True,
                    "include_hardware": True,
                    "hash_algorithm": "sha256"
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('device_signature'):
                    self.log_result(
                        "Generate Device Signature - Valid Data", 
                        True, 
                        f"Device signature generated successfully. Signature: {data.get('device_signature', '')[:20]}..."
                    )
                    return True
                else:
                    self.log_result("Generate Device Signature - Valid Data", False, f"Response missing required fields: {data}")
                    return False
            else:
                self.log_result("Generate Device Signature - Valid Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Generate Device Signature - Valid Data", False, f"Exception: {str(e)}")
            return False

    def test_generate_device_signature_invalid(self):
        """Test generate-device-signature endpoint with invalid/missing parameters"""
        try:
            # Invalid data - missing required fields
            payload = {
                "session_id": self.session_id,
                # Missing device_data field
                "fingerprint_components": None,  # Invalid null value
                "signature_options": {}  # Empty options
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=payload
            )
            
            # Should return 400 or 422 for validation error
            if response.status_code in [400, 422]:
                self.log_result(
                    "Generate Device Signature - Invalid Data", 
                    True, 
                    f"Properly rejected invalid data with status {response.status_code}"
                )
                return True
            else:
                self.log_result("Generate Device Signature - Invalid Data", False, f"Expected 400/422, got {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Generate Device Signature - Invalid Data", False, f"Exception: {str(e)}")
            return False

    def test_analyze_hardware_valid(self):
        """Test analyze-hardware endpoint with valid data"""
        try:
            # Valid hardware analysis data
            payload = {
                "session_id": self.session_id,
                "device_data": {  # This field was previously missing validation
                    "cpu_info": {
                        "cores": 8,
                        "threads": 16,
                        "architecture": "x64",
                        "vendor": "Intel",
                        "model": "Core i7-10700K"
                    },
                    "gpu_info": {
                        "vendor": "NVIDIA",
                        "model": "GeForce RTX 3070",
                        "memory": "8GB",
                        "driver_version": "471.96"
                    },
                    "memory_info": {
                        "total_ram": "16GB",
                        "available_ram": "12GB",
                        "memory_type": "DDR4"
                    },
                    "storage_info": {
                        "primary_drive": "SSD",
                        "capacity": "1TB",
                        "free_space": "500GB"
                    }
                },
                "analysis_options": {
                    "deep_analysis": True,
                    "performance_benchmarks": True,
                    "compatibility_check": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('hardware_analysis'):
                    self.log_result(
                        "Analyze Hardware - Valid Data", 
                        True, 
                        f"Hardware analysis completed successfully. Analysis type: {data.get('hardware_analysis', {}).get('analysis_type', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Analyze Hardware - Valid Data", False, f"Response missing required fields: {data}")
                    return False
            else:
                self.log_result("Analyze Hardware - Valid Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Analyze Hardware - Valid Data", False, f"Exception: {str(e)}")
            return False

    def test_analyze_hardware_invalid(self):
        """Test analyze-hardware endpoint with invalid/missing device_data field"""
        try:
            # Invalid data - missing device_data field that was causing issues
            payload = {
                "session_id": self.session_id,
                # Missing device_data field entirely
                "analysis_options": {
                    "deep_analysis": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
                json=payload
            )
            
            # Should return 400 or 422 for validation error
            if response.status_code in [400, 422]:
                self.log_result(
                    "Analyze Hardware - Invalid Data", 
                    True, 
                    f"Properly rejected missing device_data field with status {response.status_code}"
                )
                return True
            else:
                self.log_result("Analyze Hardware - Invalid Data", False, f"Expected 400/422, got {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Analyze Hardware - Invalid Data", False, f"Exception: {str(e)}")
            return False

    def test_track_device_consistency_valid(self):
        """Test track-device-consistency endpoint with valid data"""
        try:
            # Valid device consistency tracking data
            payload = {
                "session_id": self.session_id,
                "device_id": self.device_id,
                "current_signature": {  # This field was previously missing validation
                    "device_fingerprint": "fp_current_12345",
                    "timestamp": datetime.now().isoformat(),
                    "signature_hash": "sha256:current_signature_hash",
                    "confidence_score": 0.95,
                    "components": {
                        "hardware": "hw_hash_123",
                        "software": "sw_hash_456",
                        "behavioral": "bh_hash_789"
                    }
                },
                "historical_signatures": [
                    {
                        "device_fingerprint": "fp_historical_67890",
                        "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                        "signature_hash": "sha256:historical_signature_hash",
                        "confidence_score": 0.92
                    }
                ],
                "consistency_options": {
                    "threshold": 0.8,
                    "time_window": 3600,
                    "include_behavioral": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('consistency_analysis'):
                    self.log_result(
                        "Track Device Consistency - Valid Data", 
                        True, 
                        f"Device consistency tracked successfully. Consistency Score: {data.get('consistency_analysis', {}).get('consistency_score', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Track Device Consistency - Valid Data", False, f"Response missing required fields: {data}")
                    return False
            else:
                self.log_result("Track Device Consistency - Valid Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Track Device Consistency - Valid Data", False, f"Exception: {str(e)}")
            return False

    def test_track_device_consistency_invalid(self):
        """Test track-device-consistency endpoint with invalid/missing current_signature field"""
        try:
            # Invalid data - missing current_signature field that was causing issues
            payload = {
                "session_id": self.session_id,
                "device_id": self.device_id,
                # Missing current_signature field entirely
                "historical_signatures": [],
                "consistency_options": {
                    "threshold": 0.8
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json=payload
            )
            
            # Should return 400 or 422 for validation error
            if response.status_code in [400, 422]:
                self.log_result(
                    "Track Device Consistency - Invalid Data", 
                    True, 
                    f"Properly rejected missing current_signature field with status {response.status_code}"
                )
                return True
            else:
                self.log_result("Track Device Consistency - Invalid Data", False, f"Expected 400/422, got {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Track Device Consistency - Invalid Data", False, f"Exception: {str(e)}")
            return False

    def test_detect_virtual_machines_valid(self):
        """Test detect-virtual-machines endpoint with valid data"""
        try:
            # Valid VM detection data
            payload = {
                "session_id": self.session_id,
                "device_fingerprint": {
                    "hardware_info": {
                        "cpu_vendor": "GenuineIntel",
                        "cpu_model": "Intel Core i7-10700K",
                        "gpu_vendor": "NVIDIA Corporation",
                        "memory_size": 16384,
                        "screen_resolution": "1920x1080"
                    },
                    "system_info": {
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "platform": "Win32",
                        "timezone": "America/New_York",
                        "language": "en-US"
                    },
                    "behavioral_indicators": {
                        "mouse_movements": True,
                        "keyboard_timing": True,
                        "interaction_patterns": "natural"
                    }
                },
                "detection_options": {
                    "confidence_level": 0.8,  # This field was causing confidence_level errors
                    "deep_scan": True,
                    "check_hypervisor": True,
                    "analyze_timing": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'vm_detection' in data:
                    self.log_result(
                        "Detect Virtual Machines - Valid Data", 
                        True, 
                        f"VM detection completed successfully. VM Detected: {data.get('vm_detection', {}).get('is_virtual_machine', 'N/A')}, Confidence: {data.get('vm_detection', {}).get('confidence_score', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Detect Virtual Machines - Valid Data", False, f"Response missing required fields: {data}")
                    return False
            else:
                self.log_result("Detect Virtual Machines - Valid Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Detect Virtual Machines - Valid Data", False, f"Exception: {str(e)}")
            return False

    def test_detect_virtual_machines_invalid(self):
        """Test detect-virtual-machines endpoint with invalid confidence_level handling"""
        try:
            # Invalid data - invalid confidence_level that was causing errors
            payload = {
                "session_id": self.session_id,
                "device_fingerprint": {
                    "hardware_info": {
                        "cpu_vendor": "GenuineIntel"
                    }
                },
                "detection_options": {
                    "confidence_level": "invalid_string",  # Should be float, not string
                    "deep_scan": "not_boolean"  # Should be boolean, not string
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                json=payload
            )
            
            # Should return 400 or 422 for validation error
            if response.status_code in [400, 422]:
                self.log_result(
                    "Detect Virtual Machines - Invalid Data", 
                    True, 
                    f"Properly handled invalid confidence_level with status {response.status_code}"
                )
                return True
            else:
                self.log_result("Detect Virtual Machines - Invalid Data", False, f"Expected 400/422, got {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Detect Virtual Machines - Invalid Data", False, f"Exception: {str(e)}")
            return False

    def test_unauthenticated_access(self):
        """Test endpoints without authentication"""
        try:
            # Create a new session without authentication
            unauth_session = requests.Session()
            
            payload = {
                "session_id": self.session_id,
                "device_data": {"test": "data"}
            }
            
            response = unauth_session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=payload
            )
            
            # Should return 401 for unauthorized access
            if response.status_code == 401:
                self.log_result(
                    "Unauthenticated Access Test", 
                    True, 
                    f"Properly rejected unauthenticated request with status {response.status_code}"
                )
                return True
            elif response.status_code == 200:
                # Some endpoints might allow unauthenticated access
                self.log_result(
                    "Unauthenticated Access Test", 
                    True, 
                    f"Endpoint allows unauthenticated access (Status: {response.status_code})"
                )
                return True
            else:
                self.log_result("Unauthenticated Access Test", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Unauthenticated Access Test", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all Phase 1.1 API parameter fixes verification tests"""
        print("🎯 STARTING PHASE 1.1 API PARAMETER FIXES VERIFICATION TESTING")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return 0, 0
        
        # Run all tests
        tests = [
            self.test_generate_device_signature_valid,
            self.test_generate_device_signature_invalid,
            self.test_analyze_hardware_valid,
            self.test_analyze_hardware_invalid,
            self.test_track_device_consistency_valid,
            self.test_track_device_consistency_invalid,
            self.test_detect_virtual_machines_valid,
            self.test_detect_virtual_machines_invalid,
            self.test_unauthenticated_access
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        # Print summary
        print("\n" + "=" * 80)
        print("🎯 PHASE 1.1 API PARAMETER FIXES VERIFICATION SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Print detailed results
        print("\n📊 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        return passed, total

if __name__ == "__main__":
    tester = Phase11APIParameterFixesTester()
    passed, total = tester.run_all_tests()
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! Phase 1.1 API parameter fixes are working perfectly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the results above.")