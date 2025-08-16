#!/usr/bin/env python3
"""
TASK 4: PHASE 5 - CRITICAL BUG FIXES & OPTIMIZATION Backend Test

Focus Areas:
1. VM Detection Confidence Level Bug Fix - Test confidence_level field presence
2. Enhanced Fingerprinting Backend Integration - Test enhanced SessionFingerprintCollector.js integration
3. Error Handling Verification - Test enhanced error handling system
4. Performance Testing - Test that enhancements don't negatively impact performance

Key Bug Fix: detect_virtual_machines method must return confidence_level field correctly
"""

import requests
import json
import time
import uuid
from datetime import datetime
import sys
import os

# Get backend URL from environment
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://fingerprint-test.preview.emergentagent.com') + '/api'
ADMIN_PASSWORD = "Game@1234"

class Phase5CriticalBugFixesTest:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.admin_authenticated = False
        
    def log_result(self, test_name, success, details="", response_data=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        if response_data and not success:
            print(f"    Response: {response_data}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
    def test_admin_authentication(self):
        """Test: Admin Authentication"""
        try:
            payload = {"password": ADMIN_PASSWORD}
            response = self.session.post(f"{BACKEND_URL}/admin/login", json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.admin_authenticated = True
                    self.log_result("Admin Authentication", True, f"Successfully authenticated")
                    return True
                else:
                    self.log_result("Admin Authentication", False, f"Auth failed: {data}")
                    return False
            else:
                self.log_result("Admin Authentication", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Error: {str(e)}")
            return False
            
    def test_vm_detection_confidence_level_bug_fix(self):
        """Test 1: VM Detection Confidence Level Bug Fix - CRITICAL"""
        try:
            # Test data for VM detection with confidence_level field
            vm_data = {
                "device_data": {
                    "hardware_indicators": {
                        "cpu_vendor": "GenuineIntel",
                        "gpu_vendor": "NVIDIA Corporation", 
                        "gpu_renderer": "NVIDIA GeForce RTX 3080",
                        "system_manufacturer": "Dell Inc.",
                        "bios_vendor": "Dell Inc.",
                        "hypervisor_present": False,
                        "vm_artifacts": [],
                        "performance_indicators": {
                            "cpu_performance_ratio": 0.98,
                            "memory_access_latency": 12.5,
                            "disk_io_performance": 0.95,
                            "graphics_performance": 0.97
                        }
                    },
                    "system_characteristics": {
                        "registry_keys": [],
                        "process_list": ["explorer.exe", "chrome.exe"],
                        "driver_signatures": ["nvidia", "intel"],
                        "hardware_ids": ["PCI\\VEN_10DE&DEV_2206"]
                    }
                },
                "session_id": str(uuid.uuid4())
            }
            
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                                       json=vm_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response has the required structure
                if "vm_detection" in data:
                    vm_detection = data["vm_detection"]
                    
                    # CRITICAL BUG FIX CHECK: confidence_level field must be present
                    required_fields = ["vm_detected", "vm_type", "confidence_level", "vm_indicators", "confidence_score"]
                    missing_fields = []
                    
                    for field in required_fields:
                        if field not in vm_detection:
                            missing_fields.append(field)
                    
                    if not missing_fields:
                        confidence_level = vm_detection.get("confidence_level")
                        vm_detected = vm_detection.get("vm_detected", False)
                        vm_type = vm_detection.get("vm_type", "")
                        confidence_score = vm_detection.get("confidence_score", 0)
                        
                        self.log_result("VM Detection Confidence Level Bug Fix", True, 
                                      f"✅ ALL REQUIRED FIELDS PRESENT - confidence_level: {confidence_level}, vm_detected: {vm_detected}, vm_type: {vm_type}, confidence_score: {confidence_score}")
                        return True
                    else:
                        self.log_result("VM Detection Confidence Level Bug Fix", False, 
                                      f"❌ MISSING REQUIRED FIELDS: {missing_fields}")
                        return False
                else:
                    self.log_result("VM Detection Confidence Level Bug Fix", False, 
                                  f"❌ Missing vm_detection in response: {data}")
                    return False
            elif response.status_code == 500:
                # Check if this is a module loading issue
                data = response.json()
                error_detail = data.get("detail", "")
                if "Module not loaded" in error_detail:
                    self.log_result("VM Detection Confidence Level Bug Fix", False, 
                                  f"⚠️ MODULE NOT LOADED - Cannot test confidence_level bug fix: {error_detail}")
                    return False
                else:
                    self.log_result("VM Detection Confidence Level Bug Fix", False, 
                                  f"❌ Server error: {error_detail}")
                    return False
            else:
                self.log_result("VM Detection Confidence Level Bug Fix", False, 
                              f"❌ Status: {response.status_code}, Response: {response.text[:300]}")
                return False
        except Exception as e:
            self.log_result("VM Detection Confidence Level Bug Fix", False, f"❌ Error: {str(e)}")
            return False
            
    def test_enhanced_browser_fingerprint_analysis(self):
        """Test 2: Enhanced Browser Fingerprint Analysis with Enhanced SessionFingerprintCollector.js"""
        try:
            # Enhanced fingerprint data from SessionFingerprintCollector.js with error handling and caching
            enhanced_browser_data = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "session_id": str(uuid.uuid4()),
                "browser_data": {
                    # Enhanced browser characteristics with error handling
                    "browser_characteristics": {
                        "browser_name": "Chrome",
                        "browser_version": "120.0.0.0",
                        "engine_name": "Blink",
                        "engine_version": "120.0.6099.109",
                        "error_handling_enabled": True,
                        "caching_enabled": True,
                        "enhanced_features": {
                            "webgl_enhanced": True,
                            "canvas_enhanced": True,
                            "audio_context_enhanced": True,
                            "sensor_api_enhanced": True
                        }
                    },
                    # Enhanced WebGL analysis with error handling
                    "webgl_analysis": {
                        "vendor": "Google Inc. (NVIDIA)",
                        "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
                        "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
                        "extensions": ["WEBGL_debug_renderer_info", "OES_texture_float", "WEBGL_lose_context"],
                        "parameters": {
                            "MAX_TEXTURE_SIZE": 16384,
                            "MAX_VIEWPORT_DIMS": [16384, 16384],
                            "MAX_VERTEX_ATTRIBS": 16,
                            "MAX_UNIFORM_VECTORS": 1024
                        },
                        "error_handling": {
                            "context_lost_handling": True,
                            "extension_error_handling": True,
                            "parameter_validation": True
                        }
                    },
                    # Enhanced Canvas analysis with caching
                    "canvas_analysis": {
                        "canvas_fingerprint": "enhanced_canvas_hash_with_caching",
                        "text_rendering": {
                            "font_smoothing": "subpixel",
                            "text_baseline": "alphabetic",
                            "text_align": "start"
                        },
                        "image_rendering": {
                            "image_smoothing": True,
                            "image_smoothing_quality": "high"
                        },
                        "caching": {
                            "cache_enabled": True,
                            "cache_hit_rate": 0.85,
                            "cache_size": 1024
                        }
                    },
                    # Enhanced Audio Context with error handling
                    "audio_context": {
                        "sample_rate": 48000,
                        "state": "running",
                        "max_channel_count": 2,
                        "number_of_inputs": 1,
                        "number_of_outputs": 1,
                        "error_handling": {
                            "audio_context_errors": [],
                            "oscillator_errors": [],
                            "analyser_errors": []
                        }
                    },
                    # Enhanced Sensor Data with error handling
                    "sensor_data": {
                        "accelerometer": {
                            "available": True,
                            "permission_state": "granted",
                            "error_handling": True,
                            "readings": [{"x": 0.1, "y": 0.2, "z": 9.8}]
                        },
                        "gyroscope": {
                            "available": True,
                            "permission_state": "granted", 
                            "error_handling": True,
                            "readings": [{"x": 0.01, "y": 0.02, "z": 0.01}]
                        },
                        "magnetometer": {
                            "available": False,
                            "permission_state": "denied",
                            "error_handling": True,
                            "error_message": "Magnetometer not supported"
                        }
                    },
                    # Performance metrics with caching
                    "performance_metrics": {
                        "navigation_timing": {
                            "dns_lookup": 12,
                            "tcp_connect": 25,
                            "request_response": 45,
                            "dom_processing": 120
                        },
                        "memory_info": {
                            "used_js_heap_size": 45234567,
                            "total_js_heap_size": 67890123,
                            "js_heap_size_limit": 2147483648
                        },
                        "caching_performance": {
                            "cache_hits": 850,
                            "cache_misses": 150,
                            "cache_efficiency": 0.85
                        }
                    }
                }
            }
            
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                                       json=enhanced_browser_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if "browser_analysis" in data:
                    analysis = data["browser_analysis"]
                    fingerprint_entropy = analysis.get("fingerprint_entropy", 0)
                    uniqueness_score = analysis.get("uniqueness_score", 0)
                    
                    self.log_result("Enhanced Browser Fingerprint Analysis", True, 
                                  f"✅ Enhanced fingerprint processed - Entropy: {fingerprint_entropy}, Uniqueness: {uniqueness_score}")
                    return True
                else:
                    self.log_result("Enhanced Browser Fingerprint Analysis", False, 
                                  f"❌ Missing browser_analysis in response")
                    return False
            else:
                self.log_result("Enhanced Browser Fingerprint Analysis", False, 
                              f"❌ Status: {response.status_code}, Response: {response.text[:300]}")
                return False
        except Exception as e:
            self.log_result("Enhanced Browser Fingerprint Analysis", False, f"❌ Error: {str(e)}")
            return False
            
    def test_device_consistency_tracking(self):
        """Test 3: Device Consistency Tracking with Enhanced Error Handling"""
        try:
            # Test device consistency with enhanced error handling
            consistency_data = {
                "device_id": str(uuid.uuid4()),
                "current_signature": {
                    "hardware_signature": "enhanced_hardware_signature_v2",
                    "browser_signature": "enhanced_browser_signature_v2",
                    "network_signature": "enhanced_network_signature_v2",
                    "error_handling": {
                        "signature_generation_errors": [],
                        "validation_errors": [],
                        "consistency_check_errors": []
                    },
                    "enhanced_features": {
                        "caching_enabled": True,
                        "error_recovery": True,
                        "performance_monitoring": True
                    }
                }
            }
            
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                                       json=consistency_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if "consistency_analysis" in data:
                    analysis = data["consistency_analysis"]
                    consistency_score = analysis.get("consistency_score", 0)
                    device_changed = analysis.get("device_changed", False)
                    
                    self.log_result("Device Consistency Tracking", True, 
                                  f"✅ Enhanced consistency tracking - Score: {consistency_score}, Changed: {device_changed}")
                    return True
                else:
                    self.log_result("Device Consistency Tracking", False, 
                                  f"❌ Missing consistency_analysis in response")
                    return False
            else:
                self.log_result("Device Consistency Tracking", False, 
                              f"❌ Status: {response.status_code}, Response: {response.text[:300]}")
                return False
        except Exception as e:
            self.log_result("Device Consistency Tracking", False, f"❌ Error: {str(e)}")
            return False
            
    def test_device_analytics_retrieval(self):
        """Test 4: Device Analytics Retrieval with Enhanced Data"""
        try:
            session_id = str(uuid.uuid4())
            response = self.session.get(f"{BACKEND_URL}/session-fingerprinting/device-analytics/{session_id}",
                                      timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "device_analytics" in data:
                    analytics = data["device_analytics"]
                    
                    self.log_result("Device Analytics Retrieval", True, 
                                  f"✅ Enhanced analytics retrieved for session: {session_id}")
                    return True
                else:
                    self.log_result("Device Analytics Retrieval", False, 
                                  f"❌ Missing device_analytics in response")
                    return False
            else:
                self.log_result("Device Analytics Retrieval", False, 
                              f"❌ Status: {response.status_code}, Response: {response.text[:300]}")
                return False
        except Exception as e:
            self.log_result("Device Analytics Retrieval", False, f"❌ Error: {str(e)}")
            return False
            
    def test_error_handling_verification(self):
        """Test 5: Enhanced Error Handling System Verification"""
        try:
            # Test with intentionally malformed data to verify error handling
            malformed_data = {
                "invalid_field": "test",
                "missing_required_fields": True,
                # Intentionally missing required fields to test error handling
            }
            
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                                       json=malformed_data, timeout=10)
            
            # Should return proper error response, not crash
            if response.status_code in [400, 422]:  # Bad Request or Unprocessable Entity
                data = response.json()
                if "error" in data or "detail" in data:
                    self.log_result("Error Handling Verification", True, 
                                  f"✅ Proper error handling - Status: {response.status_code}")
                    return True
                else:
                    self.log_result("Error Handling Verification", False, 
                                  f"❌ Error response missing error details")
                    return False
            elif response.status_code == 500:
                self.log_result("Error Handling Verification", False, 
                              f"❌ Server error - Error handling needs improvement")
                return False
            else:
                self.log_result("Error Handling Verification", False, 
                              f"❌ Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Error Handling Verification", False, f"❌ Error: {str(e)}")
            return False
            
    def test_performance_impact(self):
        """Test 6: Performance Impact of Enhancements"""
        try:
            # Test performance with large enhanced fingerprint data
            large_enhanced_data = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "session_id": str(uuid.uuid4()),
                "browser_data": {
                    "enhanced_features": {
                        "large_dataset": True,
                        "performance_test": True
                    },
                    # Large dataset to test performance
                    "webgl_extensions": ["WEBGL_debug_renderer_info"] * 50,
                    "canvas_operations": [{"operation": f"test_{i}", "result": f"result_{i}"} for i in range(100)],
                    "audio_analysis": [{"frequency": i, "amplitude": i * 0.1} for i in range(200)],
                    "sensor_readings": [{"timestamp": time.time() + i, "x": i, "y": i*2, "z": i*3} for i in range(150)],
                    "performance_metrics": {
                        "memory_samples": [{"timestamp": time.time() + i, "usage": i * 1000} for i in range(100)]
                    }
                }
            }
            
            start_time = time.time()
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                                       json=large_enhanced_data, timeout=30)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            if response.status_code == 200:
                if processing_time < 5.0:  # Should process within 5 seconds
                    self.log_result("Performance Impact Test", True, 
                                  f"✅ Good performance - Processing time: {processing_time:.2f}s")
                    return True
                else:
                    self.log_result("Performance Impact Test", False, 
                                  f"❌ Slow performance - Processing time: {processing_time:.2f}s")
                    return False
            else:
                self.log_result("Performance Impact Test", False, 
                              f"❌ Status: {response.status_code}, Time: {processing_time:.2f}s")
                return False
        except Exception as e:
            self.log_result("Performance Impact Test", False, f"❌ Error: {str(e)}")
            return False
            
    def test_database_fingerprinting_stats(self):
        """Test 7: Database Fingerprinting Statistics - Working Endpoint"""
        try:
            response = self.session.get(f"{BACKEND_URL}/admin/database/fingerprinting-stats", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "collection_stats" in data.get("details", {}):
                    collection_stats = data["details"]["collection_stats"]
                    collections = ["device_fingerprints", "browser_fingerprints", "session_integrity_profiles", 
                                 "fingerprint_violations", "device_reputation_scores", "fingerprint_analytics"]
                    
                    all_collections_present = all(col in collection_stats for col in collections)
                    
                    if all_collections_present:
                        self.log_result("Database Fingerprinting Statistics", True, 
                                      f"✅ All 6 fingerprinting collections present and accessible")
                        return True
                    else:
                        missing = [col for col in collections if col not in collection_stats]
                        self.log_result("Database Fingerprinting Statistics", False, 
                                      f"❌ Missing collections: {missing}")
                        return False
                else:
                    self.log_result("Database Fingerprinting Statistics", False, 
                                  f"❌ Invalid response structure: {data}")
                    return False
            else:
                self.log_result("Database Fingerprinting Statistics", False, 
                              f"❌ Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Database Fingerprinting Statistics", False, f"❌ Error: {str(e)}")
            return False
            
    def run_all_tests(self):
        """Run all Phase 5 critical bug fixes and optimization tests"""
        print("🧪 TASK 4: PHASE 5 - CRITICAL BUG FIXES & OPTIMIZATION Test")
        print("=" * 70)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test started at: {datetime.now().isoformat()}")
        print()
        
        # Authentication
        self.test_admin_authentication()
        
        # Critical bug fixes and optimization tests
        print("\n🔧 CRITICAL BUG FIXES TESTING:")
        self.test_vm_detection_confidence_level_bug_fix()
        
        print("\n🚀 ENHANCED FINGERPRINTING INTEGRATION TESTING:")
        self.test_enhanced_browser_fingerprint_analysis()
        self.test_device_consistency_tracking()
        self.test_device_analytics_retrieval()
        
        print("\n🛡️ ERROR HANDLING & PERFORMANCE TESTING:")
        self.test_error_handling_verification()
        self.test_performance_impact()
        
        print("\n🗃️ DATABASE INTEGRATION TESTING:")
        self.test_database_fingerprinting_stats()
            
        # Print summary
        print("\n" + "=" * 70)
        print("📊 PHASE 5 TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Critical bug fix status
        vm_detection_test = next((r for r in self.test_results if "VM Detection Confidence Level" in r["test"]), None)
        if vm_detection_test:
            if vm_detection_test["success"]:
                print("\n✅ CRITICAL BUG FIX STATUS: VM Detection confidence_level field bug RESOLVED")
            else:
                print("\n❌ CRITICAL BUG FIX STATUS: VM Detection confidence_level field bug NOT RESOLVED")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        print(f"\nTest completed at: {datetime.now().isoformat()}")
        
        return success_rate >= 80.0  # Higher threshold for critical bug fixes

def main():
    """Main test execution"""
    test_runner = Phase5CriticalBugFixesTest()
    success = test_runner.run_all_tests()
    
    if success:
        print("\n🎉 PHASE 5 CRITICAL BUG FIXES & OPTIMIZATION Test PASSED")
        return 0
    else:
        print("\n💥 PHASE 5 CRITICAL BUG FIXES & OPTIMIZATION Test FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())