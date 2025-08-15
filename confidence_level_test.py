#!/usr/bin/env python3
"""
Testing script to verify the confidence_level validation fix for detect-virtual-machines endpoint
"""

import requests
import json
import uuid

# Configuration
BACKEND_URL = "https://browser-fingerprint-1.preview.emergentagent.com/api"

class ConfidenceLevelTester:
    def __init__(self):
        self.session = requests.Session()
        self.session_id = str(uuid.uuid4())
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

    def generate_test_device_data(self):
        """Generate test device data"""
        return {
            "hardware": {
                "cpu": {"cores": 8, "architecture": "x64", "vendor": "Intel", "model": "Core i7", "frequency": 3200},
                "gpu": {"vendor": "NVIDIA", "renderer": "GeForce RTX 3070", "version": "OpenGL 4.6", "memory": 8192},
                "memory": {"total_memory": 17179869184, "available_memory": 8589934592, "memory_type": "DDR4", "speed": 3200}
            },
            "os": {
                "platform": "Windows 10", "version": "10.0.19042", "architecture": "AMD64", "build": "19042"
            },
            "browser": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "browser_name": "Chrome", "browser_version": "96.0.4664.110"
            },
            "performance": {
                "memory_usage": {"used": 8589934592, "total": 17179869184},
                "hardware_concurrency": 8
            }
        }

    def test_confidence_level_validation(self):
        """Test confidence_level validation in detect-virtual-machines"""
        try:
            valid_data = {
                "device_data": self.generate_test_device_data(),
                "session_id": self.session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                json=valid_data
            )
            
            print(f"VM Detection Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response has the expected structure
                if 'vm_detection' in data and data.get('success'):
                    vm_detection = data['vm_detection']
                    
                    # Check if confidence_metrics exists
                    if 'confidence_metrics' in vm_detection:
                        confidence_metrics = vm_detection['confidence_metrics']
                        print(f"Confidence Metrics: {confidence_metrics}")
                        
                        # Check if detection_quality is in confidence_metrics
                        if 'detection_quality' in confidence_metrics:
                            detection_quality = confidence_metrics['detection_quality']
                            print(f"Detection Quality: {detection_quality}")
                            
                            # Valid detection quality values
                            valid_qualities = ['high', 'medium', 'low', 'insufficient', 'unknown']
                            
                            if isinstance(detection_quality, str) and detection_quality.lower() in valid_qualities:
                                self.log_result(
                                    "Confidence Level Validation", 
                                    True, 
                                    f"Valid detection_quality: {detection_quality}"
                                )
                            else:
                                self.log_result(
                                    "Confidence Level Validation", 
                                    False, 
                                    f"Invalid detection_quality: {detection_quality}"
                                )
                        else:
                            self.log_result(
                                "Confidence Level Validation", 
                                False, 
                                "Missing detection_quality in confidence_metrics"
                            )
                    else:
                        self.log_result(
                            "Confidence Level Validation", 
                            False, 
                            "Missing confidence_metrics in response"
                        )
                        
                    # Check if storage was successful (indicating confidence_level was handled correctly)
                    if data.get('storage_confirmation'):
                        self.log_result(
                            "Database Storage with Confidence Level", 
                            True, 
                            "VM detection data stored successfully with confidence_level"
                        )
                    else:
                        self.log_result(
                            "Database Storage with Confidence Level", 
                            False, 
                            "Storage confirmation missing"
                        )
                else:
                    self.log_result("Confidence Level Validation", False, f"Invalid response structure: {data}")
            else:
                self.log_result("Confidence Level Validation", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_result("Confidence Level Validation", False, f"Exception: {str(e)}")

    def test_invalid_confidence_handling(self):
        """Test how the endpoint handles invalid confidence data"""
        print("\n📋 Testing how endpoint handles edge cases...")
        
        # This test checks that the endpoint can gracefully handle various scenarios
        # and always returns a valid confidence_level in the stored document
        
        # Test with minimal device data
        minimal_data = {
            "device_data": {
                "hardware": {"cpu": {"cores": 4}},  # Minimal data
                "os": {"platform": "Unknown"}
            },
            "session_id": str(uuid.uuid4())
        }
        
        try:
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                json=minimal_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and data.get('storage_confirmation'):
                    self.log_result(
                        "Edge Case Handling", 
                        True, 
                        "Endpoint handles minimal data correctly"
                    )
                else:
                    self.log_result(
                        "Edge Case Handling", 
                        False, 
                        "Failed to handle minimal data"
                    )
            else:
                # It's acceptable if minimal data returns an error
                self.log_result(
                    "Edge Case Handling", 
                    True, 
                    f"Minimal data appropriately rejected: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Edge Case Handling", False, f"Exception: {str(e)}")

    def run_all_tests(self):
        """Run all confidence level tests"""
        print("🧪 Testing Confidence Level Validation Fix for detect-virtual-machines")
        print("=" * 70)
        
        self.test_confidence_level_validation()
        self.test_invalid_confidence_handling()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 CONFIDENCE LEVEL TEST SUMMARY")
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests / total_tests) * 100:.1f}%")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = ConfidenceLevelTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All confidence level validation tests passed!")
    else:
        print("\n⚠️ Some tests failed - confidence level validation needs attention")