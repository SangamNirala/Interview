#!/usr/bin/env python3
"""
VM Detection Endpoint Testing
Testing the POST /api/session-fingerprinting/detect-virtual-machines endpoint
Focus on finding and verifying the fix for 'str' object has no attribute 'get' errors
"""

import requests
import json
import time
import os
from datetime import datetime
import uuid

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://netdata-collector.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class VMDetectionTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()
        return status == "PASS"

    def create_normal_device_data(self):
        """Create normal device data for testing"""
        return {
            "hardware": {
                "cpu": {
                    "cores": 8,
                    "architecture": "x64",
                    "vendor": "Intel",
                    "model": "Core i7-10700K",
                    "frequency": 3800
                },
                "gpu": {
                    "vendor": "NVIDIA",
                    "renderer": "GeForce RTX 3070",
                    "version": "OpenGL 4.6",
                    "memory": 8192
                },
                "memory": {
                    "total": 16384,
                    "available": 8192
                },
                "storage": {
                    "type": "SSD",
                    "size": 1024000
                }
            },
            "os": {
                "platform": "Win32",
                "version": "Windows 10",
                "architecture": "x64"
            },
            "browser": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "plugins": [
                    {"name": "Chrome PDF Plugin", "version": "1.0"},
                    {"name": "Native Client", "version": "1.0"}
                ]
            },
            "performance": {
                "device_memory": 16384,
                "hardware_concurrency": 8
            },
            "screen": {
                "width": 1920,
                "height": 1080,
                "color_depth": 24
            },
            "network": {
                "connection_type": "ethernet",
                "downlink": 100
            }
        }

    def create_vm_device_data(self):
        """Create device data that should trigger VM detection"""
        return {
            "hardware": {
                "cpu": {
                    "cores": 4,
                    "architecture": "x64",
                    "vendor": "Intel",
                    "model": "Virtual CPU",
                    "frequency": 2400
                },
                "gpu": {
                    "vendor": "VMware",
                    "renderer": "VMware SVGA 3D",
                    "version": "OpenGL 3.3",
                    "memory": 256
                },
                "memory": {
                    "total": 4096,
                    "available": 2048
                },
                "storage": {
                    "type": "Virtual Disk",
                    "size": 40000
                }
            },
            "os": {
                "platform": "Linux",
                "version": "Ubuntu 20.04 (Virtual)",
                "architecture": "x64"
            },
            "browser": {
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64; VirtualBox) AppleWebKit/537.36",
                "plugins": [
                    {"name": "VirtualBox Guest Additions", "version": "6.1"},
                    {"name": "VMware Tools", "version": "11.0"}
                ]
            },
            "performance": {
                "device_memory": 4096,
                "hardware_concurrency": 4
            },
            "screen": {
                "width": 1024,
                "height": 768,
                "color_depth": 24
            },
            "network": {
                "connection_type": "virtual",
                "downlink": 10
            }
        }

    def create_edge_case_device_data(self):
        """Create edge case device data that might cause type errors"""
        return {
            "hardware": {
                "cpu": "Intel Core i7",  # String instead of dict
                "gpu": None,  # None value
                "memory": {
                    "total": "16GB",  # String instead of number
                    "available": 8192
                },
                "storage": []  # Empty list instead of dict
            },
            "os": {
                "platform": 123,  # Number instead of string
                "version": None,
                "architecture": ""
            },
            "browser": {
                "user_agent": None,
                "plugins": "Chrome PDF Plugin"  # String instead of list
            },
            "performance": {
                "device_memory": None,
                "hardware_concurrency": "8"  # String instead of number
            },
            "screen": {},  # Empty dict
            "network": "ethernet"  # String instead of dict
        }

    def create_malformed_device_data(self):
        """Create malformed device data to test error handling"""
        return {
            "hardware": "invalid",  # String instead of dict
            "os": [],  # List instead of dict
            "browser": 123,  # Number instead of dict
            "performance": None,
            "screen": "1920x1080",
            "network": True
        }

    def create_missing_fields_device_data(self):
        """Create device data with missing fields"""
        return {
            "hardware": {
                "cpu": {"cores": 4}  # Missing other fields
            }
            # Missing os, browser, performance, screen, network
        }

    def test_normal_device_data(self):
        """Test VM detection with normal device data"""
        try:
            session_id = str(uuid.uuid4())
            device_data = self.create_normal_device_data()
            
            request_data = {
                "session_id": session_id,
                "device_data": device_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "vm_detection" in data:
                    vm_detection = data["vm_detection"]
                    vm_probability = vm_detection.get("vm_probability", 0)
                    is_vm = vm_detection.get("is_virtual_machine", False)
                    
                    return self.log_test("Normal Device Data VM Detection", "PASS", 
                                       f"VM Probability: {vm_probability:.3f}, Is VM: {is_vm}")
                else:
                    return self.log_test("Normal Device Data VM Detection", "FAIL", 
                                       f"Invalid response structure: {data}")
            else:
                return self.log_test("Normal Device Data VM Detection", "FAIL", 
                                   f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            return self.log_test("Normal Device Data VM Detection", "FAIL", f"Exception: {str(e)}")

    def test_vm_device_data(self):
        """Test VM detection with VM-like device data"""
        try:
            session_id = str(uuid.uuid4())
            device_data = self.create_vm_device_data()
            
            request_data = {
                "session_id": session_id,
                "device_data": device_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "vm_detection" in data:
                    vm_detection = data["vm_detection"]
                    vm_probability = vm_detection.get("vm_probability", 0)
                    is_vm = vm_detection.get("is_virtual_machine", False)
                    vm_classification = vm_detection.get("vm_classification", "Unknown")
                    
                    return self.log_test("VM Device Data Detection", "PASS", 
                                       f"VM Probability: {vm_probability:.3f}, Is VM: {is_vm}, Type: {vm_classification}")
                else:
                    return self.log_test("VM Device Data Detection", "FAIL", 
                                       f"Invalid response structure: {data}")
            else:
                return self.log_test("VM Device Data Detection", "FAIL", 
                                   f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            return self.log_test("VM Device Data Detection", "FAIL", f"Exception: {str(e)}")

    def test_edge_case_device_data(self):
        """Test VM detection with edge case device data that might cause 'str' object errors"""
        try:
            session_id = str(uuid.uuid4())
            device_data = self.create_edge_case_device_data()
            
            request_data = {
                "session_id": session_id,
                "device_data": device_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "vm_detection" in data:
                    vm_detection = data["vm_detection"]
                    vm_probability = vm_detection.get("vm_probability", 0)
                    
                    return self.log_test("Edge Case Device Data VM Detection", "PASS", 
                                       f"Handled edge cases successfully, VM Probability: {vm_probability:.3f}")
                else:
                    return self.log_test("Edge Case Device Data VM Detection", "FAIL", 
                                       f"Invalid response structure: {data}")
            elif response.status_code == 500:
                error_text = response.text
                if "'str' object has no attribute 'get'" in error_text:
                    return self.log_test("Edge Case Device Data VM Detection", "FAIL", 
                                       f"'str' object has no attribute 'get' error detected: {error_text}")
                else:
                    return self.log_test("Edge Case Device Data VM Detection", "FAIL", 
                                       f"HTTP 500 error (different issue): {error_text}")
            else:
                return self.log_test("Edge Case Device Data VM Detection", "FAIL", 
                                   f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            return self.log_test("Edge Case Device Data VM Detection", "FAIL", f"Exception: {str(e)}")

    def test_malformed_device_data(self):
        """Test VM detection with malformed device data"""
        try:
            session_id = str(uuid.uuid4())
            device_data = self.create_malformed_device_data()
            
            request_data = {
                "session_id": session_id,
                "device_data": device_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "vm_detection" in data:
                    return self.log_test("Malformed Device Data VM Detection", "PASS", 
                                       "Handled malformed data gracefully")
                else:
                    return self.log_test("Malformed Device Data VM Detection", "FAIL", 
                                       f"Invalid response structure: {data}")
            elif response.status_code == 500:
                error_text = response.text
                if "'str' object has no attribute 'get'" in error_text:
                    return self.log_test("Malformed Device Data VM Detection", "FAIL", 
                                       f"'str' object has no attribute 'get' error detected: {error_text}")
                else:
                    return self.log_test("Malformed Device Data VM Detection", "PASS", 
                                       f"Expected error handling for malformed data: {response.status_code}")
            else:
                return self.log_test("Malformed Device Data VM Detection", "PASS", 
                                   f"Expected error response: HTTP {response.status_code}")
                
        except Exception as e:
            return self.log_test("Malformed Device Data VM Detection", "FAIL", f"Exception: {str(e)}")

    def test_missing_fields_device_data(self):
        """Test VM detection with missing fields in device data"""
        try:
            session_id = str(uuid.uuid4())
            device_data = self.create_missing_fields_device_data()
            
            request_data = {
                "session_id": session_id,
                "device_data": device_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "vm_detection" in data:
                    return self.log_test("Missing Fields Device Data VM Detection", "PASS", 
                                       "Handled missing fields gracefully")
                else:
                    return self.log_test("Missing Fields Device Data VM Detection", "FAIL", 
                                       f"Invalid response structure: {data}")
            elif response.status_code == 500:
                error_text = response.text
                if "'str' object has no attribute 'get'" in error_text:
                    return self.log_test("Missing Fields Device Data VM Detection", "FAIL", 
                                       f"'str' object has no attribute 'get' error detected: {error_text}")
                else:
                    return self.log_test("Missing Fields Device Data VM Detection", "PASS", 
                                       f"Expected error handling for missing fields: {response.status_code}")
            else:
                return self.log_test("Missing Fields Device Data VM Detection", "PASS", 
                                   f"Expected error response: HTTP {response.status_code}")
                
        except Exception as e:
            return self.log_test("Missing Fields Device Data VM Detection", "FAIL", f"Exception: {str(e)}")

    def test_rapid_requests(self):
        """Test multiple rapid requests to check for intermittent issues"""
        try:
            session_id = str(uuid.uuid4())
            device_data = self.create_normal_device_data()
            
            request_data = {
                "session_id": session_id,
                "device_data": device_data
            }
            
            success_count = 0
            error_count = 0
            str_errors = 0
            
            for i in range(10):  # Send 10 rapid requests
                try:
                    response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                               json=request_data)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success"):
                            success_count += 1
                        else:
                            error_count += 1
                    elif response.status_code == 500:
                        error_text = response.text
                        if "'str' object has no attribute 'get'" in error_text:
                            str_errors += 1
                        error_count += 1
                    else:
                        error_count += 1
                        
                    # Small delay between requests
                    time.sleep(0.1)
                    
                except Exception as e:
                    error_count += 1
                    if "'str' object has no attribute 'get'" in str(e):
                        str_errors += 1
            
            if str_errors > 0:
                return self.log_test("Rapid Requests VM Detection", "FAIL", 
                                   f"Detected {str_errors} 'str' object errors out of 10 requests")
            elif success_count >= 8:  # Allow for some network issues
                return self.log_test("Rapid Requests VM Detection", "PASS", 
                                   f"Success: {success_count}/10, Errors: {error_count}/10")
            else:
                return self.log_test("Rapid Requests VM Detection", "FAIL", 
                                   f"Too many failures - Success: {success_count}/10, Errors: {error_count}/10")
                
        except Exception as e:
            return self.log_test("Rapid Requests VM Detection", "FAIL", f"Exception: {str(e)}")

    def test_vm_detection_methods_individually(self):
        """Test that all VM detection methods work without 'str' object errors"""
        try:
            session_id = str(uuid.uuid4())
            device_data = self.create_vm_device_data()
            
            request_data = {
                "session_id": session_id,
                "device_data": device_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "vm_detection" in data:
                    vm_detection = data["vm_detection"]
                    vm_results = vm_detection.get("vm_detection_results", {})
                    
                    # Check that all expected methods returned results
                    expected_methods = [
                        "hardware_indicators",
                        "hypervisor_analysis", 
                        "performance_anomalies",
                        "system_analysis",
                        "software_signatures"
                    ]
                    
                    missing_methods = []
                    for method in expected_methods:
                        if method not in vm_results:
                            missing_methods.append(method)
                    
                    if missing_methods:
                        return self.log_test("VM Detection Methods Individual Test", "FAIL", 
                                           f"Missing methods: {missing_methods}")
                    else:
                        return self.log_test("VM Detection Methods Individual Test", "PASS", 
                                           f"All {len(expected_methods)} VM detection methods returned results")
                else:
                    return self.log_test("VM Detection Methods Individual Test", "FAIL", 
                                       f"Invalid response structure: {data}")
            elif response.status_code == 500:
                error_text = response.text
                if "'str' object has no attribute 'get'" in error_text:
                    return self.log_test("VM Detection Methods Individual Test", "FAIL", 
                                       f"'str' object has no attribute 'get' error in VM detection methods: {error_text}")
                else:
                    return self.log_test("VM Detection Methods Individual Test", "FAIL", 
                                       f"HTTP 500 error: {error_text}")
            else:
                return self.log_test("VM Detection Methods Individual Test", "FAIL", 
                                   f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            return self.log_test("VM Detection Methods Individual Test", "FAIL", f"Exception: {str(e)}")

    def run_comprehensive_test(self):
        """Run all VM detection tests"""
        print("=" * 80)
        print("VM DETECTION ENDPOINT COMPREHENSIVE TESTING")
        print("Focus: Finding and verifying fix for 'str' object has no attribute 'get' errors")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Normal device data
        test_results.append(self.test_normal_device_data())
        
        # Test 2: VM-like device data
        test_results.append(self.test_vm_device_data())
        
        # Test 3: Edge case device data (most likely to trigger 'str' object errors)
        test_results.append(self.test_edge_case_device_data())
        
        # Test 4: Malformed device data
        test_results.append(self.test_malformed_device_data())
        
        # Test 5: Missing fields device data
        test_results.append(self.test_missing_fields_device_data())
        
        # Test 6: Rapid requests (intermittent issues)
        test_results.append(self.test_rapid_requests())
        
        # Test 7: Individual VM detection methods
        test_results.append(self.test_vm_detection_methods_individually())
        
        # Summary
        print("=" * 80)
        print("VM DETECTION TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! VM Detection endpoint is working correctly without 'str' object errors.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = VMDetectionTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ VM DETECTION TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ VM DETECTION TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()