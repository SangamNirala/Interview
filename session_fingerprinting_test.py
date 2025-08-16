#!/usr/bin/env python3
"""
Module 3: Advanced Session Fingerprinting System Backend Testing
Testing comprehensive device fingerprinting, VM detection, hardware analysis, and device tracking
"""

import requests
import json
import time
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://interviewmate-1.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class SessionFingerprintingTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        self.test_session_id = "test_session_12345"
        self.test_device_id = None
        
    def log_test(self, test_name, status, details=""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()

    def test_admin_authentication(self):
        """Test admin authentication with Game@1234 password"""
        try:
            response = self.session.post(f"{BASE_URL}/admin/login", 
                                       json={"password": "Game@1234"})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.admin_authenticated = True
                    self.log_test("Admin Authentication", "PASS", 
                                f"Successfully authenticated with Game@1234 password")
                    return True
                else:
                    self.log_test("Admin Authentication", "FAIL", 
                                f"Authentication failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Admin Authentication", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", "FAIL", f"Exception: {str(e)}")
            return False

    def get_comprehensive_device_data(self):
        """Get comprehensive device data for testing"""
        return {
            "device_data": {
                "hardware": {
                    "cpu": {
                        "cores": 8,
                        "architecture": "x64",
                        "vendor": "Intel",
                        "model": "Core i7-10700K",
                        "frequency": 3200,
                        "cache_l1": 512,
                        "cache_l2": 2048,
                        "cache_l3": 16384
                    },
                    "gpu": {
                        "vendor": "NVIDIA",
                        "renderer": "GeForce RTX 3070",
                        "version": "OpenGL 4.6",
                        "memory": 8192,
                        "driver_version": "472.12",
                        "compute_capability": "8.6"
                    },
                    "memory": {
                        "total_memory": 17179869184,
                        "available_memory": 8589934592,
                        "memory_type": "DDR4",
                        "speed": 3200,
                        "channels": 2,
                        "ecc_support": False
                    },
                    "storage": {
                        "total_storage": 1099511627776,
                        "available_storage": 549755813888,
                        "storage_type": "SSD",
                        "filesystem": "NTFS",
                        "interface": "NVMe",
                        "rpm": 0
                    }
                },
                "os": {
                    "platform": "Windows 10",
                    "version": "10.0.19042",
                    "architecture": "AMD64",
                    "build": "19042",
                    "kernel_version": "10.0.19042",
                    "language": "en-US",
                    "timezone": "America/New_York",
                    "timezone_offset": -300,
                    "uptime": 86400
                },
                "browser": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
                    "browser_name": "Chrome",
                    "browser_version": "96.0.4664.110",
                    "engine_name": "Blink",
                    "engine_version": "96.0.4664.110",
                    "plugins": ["Chrome PDF Plugin", "Native Client"],
                    "mime_types": ["application/pdf", "text/html"],
                    "languages": ["en-US", "en"],
                    "cookie_enabled": True,
                    "local_storage": True,
                    "session_storage": True,
                    "webgl_support": True,
                    "canvas_support": True,
                    "webrtc_support": True
                },
                "network": {
                    "connection_type": "ethernet",
                    "effective_type": "4g",
                    "downlink": 10,
                    "rtt": 50,
                    "save_data": False,
                    "ip_address": "192.168.1.100",
                    "country": "US",
                    "region": "NY",
                    "city": "New York",
                    "timezone": "America/New_York",
                    "isp": "Verizon"
                },
                "screen": {
                    "width": 1920,
                    "height": 1080,
                    "available_width": 1920,
                    "available_height": 1040,
                    "color_depth": 24,
                    "pixel_depth": 24,
                    "device_pixel_ratio": 1,
                    "orientation": "landscape",
                    "touch_support": False,
                    "max_touch_points": 0
                },
                "performance": {
                    "memory_usage": {
                        "used": 8589934592,
                        "total": 17179869184
                    },
                    "cpu_usage": 25,
                    "battery_level": 85,
                    "battery_charging": False,
                    "device_memory": 16384,
                    "hardware_concurrency": 8,
                    "max_touch_points": 0,
                    "benchmarks": {
                        "javascript_performance": 1200,
                        "webgl_performance": 850,
                        "canvas_performance": 950
                    }
                }
            },
            "session_id": self.test_session_id
        }

    def test_device_fingerprinting_engine_loading(self):
        """Test if the session fingerprinting engine loads correctly"""
        try:
            # Test by making a simple request to check if endpoints are accessible
            response = self.session.options(f"{BASE_URL}/session-fingerprinting/generate-device-signature")
            
            if response.status_code in [200, 405]:  # 405 is expected for OPTIONS on POST endpoint
                self.log_test("Device Fingerprinting Engine Loading", "PASS", 
                            "Session fingerprinting endpoints are accessible")
                return True
            else:
                self.log_test("Device Fingerprinting Engine Loading", "FAIL", 
                            f"Endpoints not accessible: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Device Fingerprinting Engine Loading", "FAIL", f"Exception: {str(e)}")
            return False

    def test_device_signature_generation(self):
        """Test POST /api/session-fingerprinting/generate-device-signature endpoint"""
        try:
            device_data = self.get_comprehensive_device_data()
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/generate-device-signature", 
                                       json=device_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "device_signature" in data:
                    device_signature = data["device_signature"]
                    
                    # Extract device_id for later tests
                    if "device_fingerprint" in device_signature:
                        self.test_device_id = device_signature["device_fingerprint"].get("device_id")
                    
                    # Validate response structure
                    required_fields = ["device_fingerprint", "hardware_analysis", "environment_analysis"]
                    missing_fields = [field for field in required_fields if field not in device_signature]
                    
                    if not missing_fields:
                        self.log_test("Device Signature Generation", "PASS", 
                                    f"Generated device signature successfully. Device ID: {self.test_device_id}")
                        return True
                    else:
                        self.log_test("Device Signature Generation", "FAIL", 
                                    f"Missing required fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Device Signature Generation", "FAIL", 
                                f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Device Signature Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Device Signature Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_virtual_machine_detection(self):
        """Test POST /api/session-fingerprinting/detect-virtual-machines endpoint"""
        try:
            device_data = self.get_comprehensive_device_data()
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=device_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "vm_detection" in data:
                    vm_detection = data["vm_detection"]
                    
                    # Validate response structure
                    required_fields = ["vm_detection_results", "vm_probability", "vm_classification", "is_virtual_machine"]
                    missing_fields = [field for field in required_fields if field not in vm_detection]
                    
                    if not missing_fields:
                        vm_status = "Virtual Machine" if vm_detection.get("is_virtual_machine") else "Physical Machine"
                        vm_probability = vm_detection.get("vm_probability", 0)
                        self.log_test("Virtual Machine Detection", "PASS", 
                                    f"VM Detection completed. Status: {vm_status}, Probability: {vm_probability:.2f}")
                        return True
                    else:
                        self.log_test("Virtual Machine Detection", "FAIL", 
                                    f"Missing required fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Virtual Machine Detection", "FAIL", 
                                f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Virtual Machine Detection", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Virtual Machine Detection", "FAIL", f"Exception: {str(e)}")
            return False

    def test_hardware_analysis(self):
        """Test POST /api/session-fingerprinting/analyze-hardware endpoint"""
        try:
            device_data = self.get_comprehensive_device_data()
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                       json=device_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "hardware_analysis" in data:
                    hardware_analysis = data["hardware_analysis"]
                    
                    # Validate response structure
                    required_fields = ["hardware_analysis", "hardware_profile", "overall_hardware_score"]
                    missing_fields = [field for field in required_fields if field not in hardware_analysis]
                    
                    if not missing_fields:
                        hardware_score = hardware_analysis.get("overall_hardware_score", 0)
                        self.log_test("Hardware Analysis", "PASS", 
                                    f"Hardware analysis completed. Overall score: {hardware_score}")
                        return True
                    else:
                        self.log_test("Hardware Analysis", "FAIL", 
                                    f"Missing required fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Hardware Analysis", "FAIL", 
                                f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Hardware Analysis", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Hardware Analysis", "FAIL", f"Exception: {str(e)}")
            return False

    def test_device_tracking(self):
        """Test POST /api/session-fingerprinting/track-device-consistency endpoint"""
        try:
            if not self.test_device_id:
                self.log_test("Device Tracking", "SKIP", "No device ID available from previous tests")
                return False
            
            # Create a mock current signature for tracking
            current_signature = {
                "hardware_hash": "abc123def456",
                "os_hash": "def456ghi789",
                "browser_hash": "ghi789jkl012",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            tracking_data = {
                "device_id": self.test_device_id,
                "current_signature": current_signature
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/track-device-consistency", 
                                       json=tracking_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "device_tracking" in data:
                    device_tracking = data["device_tracking"]
                    
                    # Validate response structure
                    required_fields = ["consistency_analysis", "consistency_score", "risk_assessment"]
                    missing_fields = [field for field in required_fields if field not in device_tracking]
                    
                    if not missing_fields:
                        consistency_score = device_tracking.get("consistency_score", 0)
                        self.log_test("Device Tracking", "PASS", 
                                    f"Device tracking completed. Consistency score: {consistency_score}")
                        return True
                    else:
                        self.log_test("Device Tracking", "FAIL", 
                                    f"Missing required fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Device Tracking", "FAIL", 
                                f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Device Tracking", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Device Tracking", "FAIL", f"Exception: {str(e)}")
            return False

    def test_device_analytics(self):
        """Test GET /api/session-fingerprinting/device-analytics/{session_id} endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/session-fingerprinting/device-analytics/{self.test_session_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "analytics" in data:
                    analytics = data["analytics"]
                    
                    # Validate response structure
                    required_fields = ["session_id", "analysis_summary"]
                    missing_fields = [field for field in required_fields if field not in analytics]
                    
                    if not missing_fields:
                        analysis_summary = analytics.get("analysis_summary", {})
                        device_identified = analysis_summary.get("device_identified", False)
                        vm_detected = analysis_summary.get("vm_detected", False)
                        hardware_analyzed = analysis_summary.get("hardware_analyzed", False)
                        
                        self.log_test("Device Analytics", "PASS", 
                                    f"Analytics retrieved. Device ID: {device_identified}, VM: {vm_detected}, HW: {hardware_analyzed}")
                        return True
                    else:
                        self.log_test("Device Analytics", "FAIL", 
                                    f"Missing required fields: {missing_fields}")
                        return False
                else:
                    self.log_test("Device Analytics", "FAIL", 
                                f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("Device Analytics", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Device Analytics", "FAIL", f"Exception: {str(e)}")
            return False

    def test_mongodb_integration(self):
        """Test MongoDB integration by verifying data storage in new collections"""
        try:
            # This test verifies that the previous API calls have stored data correctly
            # We'll check the device analytics endpoint which retrieves from multiple collections
            
            response = self.session.get(f"{BASE_URL}/session-fingerprinting/device-analytics/{self.test_session_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "analytics" in data:
                    analytics = data["analytics"]
                    
                    # Check if data exists in different collections
                    collections_data = {
                        "device_fingerprints": analytics.get("device_fingerprint") is not None,
                        "vm_detections": analytics.get("vm_detection") is not None,
                        "hardware_analyses": analytics.get("hardware_analysis") is not None
                    }
                    
                    stored_collections = [name for name, has_data in collections_data.items() if has_data]
                    
                    if len(stored_collections) >= 2:  # At least 2 collections should have data
                        self.log_test("MongoDB Integration", "PASS", 
                                    f"Data stored in collections: {', '.join(stored_collections)}")
                        return True
                    else:
                        self.log_test("MongoDB Integration", "FAIL", 
                                    f"Insufficient data storage. Only found data in: {stored_collections}")
                        return False
                else:
                    self.log_test("MongoDB Integration", "FAIL", 
                                f"Invalid response structure: {data}")
                    return False
            else:
                self.log_test("MongoDB Integration", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("MongoDB Integration", "FAIL", f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all session fingerprinting tests"""
        print("=" * 80)
        print("MODULE 3: ADVANCED SESSION FINGERPRINTING SYSTEM TESTING")
        print("=" * 80)
        print()
        
        tests = [
            ("Admin Authentication", self.test_admin_authentication),
            ("Device Fingerprinting Engine Loading", self.test_device_fingerprinting_engine_loading),
            ("Device Signature Generation", self.test_device_signature_generation),
            ("Virtual Machine Detection", self.test_virtual_machine_detection),
            ("Hardware Analysis", self.test_hardware_analysis),
            ("Device Tracking", self.test_device_tracking),
            ("Device Analytics", self.test_device_analytics),
            ("MongoDB Integration", self.test_mongodb_integration)
        ]
        
        results = []
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, "PASS" if result else "FAIL"))
            except Exception as e:
                print(f"❌ {test_name} - EXCEPTION: {str(e)}")
                results.append((test_name, "FAIL"))
        
        # Print summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for _, status in results if status == "PASS")
        total = len(results)
        
        for test_name, status in results:
            status_symbol = "✅" if status == "PASS" else "❌"
            print(f"{status_symbol} {test_name}")
        
        print()
        print(f"OVERALL RESULT: {passed}/{total} tests passed ({passed/total*100:.1f}% success rate)")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Module 3: Advanced Session Fingerprinting System is working correctly.")
        elif passed >= total * 0.8:
            print("✅ MOSTLY WORKING! Most functionality is operational with minor issues.")
        else:
            print("⚠️  SIGNIFICANT ISSUES DETECTED! Multiple components need attention.")
        
        return passed, total

if __name__ == "__main__":
    tester = SessionFingerprintingTester()
    tester.run_all_tests()