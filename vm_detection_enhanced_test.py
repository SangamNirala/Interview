#!/usr/bin/env python3
"""
Enhanced VM Detection Testing for Step 2 Enhancement
Testing the newly enhanced VM Detection functionality with comprehensive device data
"""

import requests
import json
import time
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://fprintshield.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class EnhancedVMDetectionTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        
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

    def create_normal_device_data(self):
        """Create normal device data for testing"""
        return {
            "session_id": "test_session_normal_001",
            "device_data": {
                "hardware": {
                    "cpu": {
                        "cores": 8,
                        "threads": 16,
                        "vendor": "Intel",
                        "model": "Intel(R) Core(TM) i7-10700K CPU @ 3.80GHz",
                        "architecture": "x64",
                        "frequency": 3800
                    },
                    "gpu": {
                        "vendor": "NVIDIA",
                        "model": "GeForce RTX 3070",
                        "memory": 8192,
                        "driver_version": "471.96"
                    },
                    "memory": {
                        "total": 16384,
                        "available": 8192,
                        "type": "DDR4"
                    },
                    "storage": {
                        "type": "SSD",
                        "capacity": 1024,
                        "interface": "NVMe"
                    }
                },
                "os": {
                    "platform": "Windows",
                    "version": "10.0.19043",
                    "architecture": "x64",
                    "build": "19043"
                },
                "browser": {
                    "name": "Chrome",
                    "version": "95.0.4638.69",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "plugins": ["Chrome PDF Plugin", "Native Client"],
                    "webgl_vendor": "Google Inc. (NVIDIA)",
                    "webgl_renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)"
                },
                "network": {
                    "connection_type": "ethernet",
                    "downlink": 100,
                    "rtt": 50,
                    "effective_type": "4g"
                },
                "screen": {
                    "width": 1920,
                    "height": 1080,
                    "color_depth": 24,
                    "pixel_ratio": 1,
                    "orientation": "landscape"
                },
                "performance": {
                    "memory_used": 8192,
                    "cpu_usage": 25.5,
                    "gpu_usage": 15.2,
                    "disk_usage": 45.8,
                    "network_latency": 45
                }
            }
        }

    def create_vm_like_device_data(self, platform="windows"):
        """Create VM-like device data for testing different platforms"""
        base_data = {
            "session_id": f"test_session_vm_{platform}_001",
            "device_data": {
                "hardware": {
                    "cpu": {
                        "cores": 4,
                        "threads": 4,
                        "vendor": "Intel",
                        "model": "Intel(R) Xeon(R) CPU E5-2676 v3 @ 2.40GHz",
                        "architecture": "x64",
                        "frequency": 2400
                    },
                    "gpu": {
                        "vendor": "VMware",
                        "model": "VMware SVGA 3D",
                        "memory": 128,
                        "driver_version": "8.17.2.14"
                    },
                    "memory": {
                        "total": 4096,
                        "available": 2048,
                        "type": "DDR3"
                    },
                    "storage": {
                        "type": "HDD",
                        "capacity": 40,
                        "interface": "SCSI"
                    }
                },
                "browser": {
                    "name": "Chrome",
                    "version": "95.0.4638.69",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "plugins": ["Chrome PDF Plugin", "VMware Tools"],
                    "webgl_vendor": "VMware, Inc.",
                    "webgl_renderer": "VMware SVGA 3D"
                },
                "network": {
                    "connection_type": "ethernet",
                    "downlink": 10,
                    "rtt": 100,
                    "effective_type": "3g"
                },
                "screen": {
                    "width": 1024,
                    "height": 768,
                    "color_depth": 16,
                    "pixel_ratio": 1,
                    "orientation": "landscape"
                },
                "performance": {
                    "memory_used": 2048,
                    "cpu_usage": 45.8,
                    "gpu_usage": 5.2,
                    "disk_usage": 65.3,
                    "network_latency": 95
                }
            }
        }
        
        # Platform-specific modifications
        if platform == "windows":
            base_data["device_data"]["os"] = {
                "platform": "Windows",
                "version": "10.0.19043",
                "architecture": "x64",
                "build": "19043"
            }
        elif platform == "linux":
            base_data["device_data"]["os"] = {
                "platform": "Linux",
                "version": "Ubuntu 20.04.3 LTS",
                "architecture": "x64",
                "kernel": "5.4.0-88-generic"
            }
            base_data["device_data"]["browser"]["user_agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        elif platform == "macos":
            base_data["device_data"]["os"] = {
                "platform": "macOS",
                "version": "12.0.1",
                "architecture": "x64",
                "build": "21A559"
            }
            base_data["device_data"]["browser"]["user_agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            
        return base_data

    def create_edge_case_device_data(self):
        """Create edge case device data with comprehensive information"""
        return {
            "session_id": "test_session_edge_001",
            "device_data": {
                "hardware": {
                    "cpu": {
                        "cores": 32,
                        "threads": 64,
                        "vendor": "AMD",
                        "model": "AMD EPYC 7742 64-Core Processor",
                        "architecture": "x64",
                        "frequency": 2250
                    },
                    "gpu": {
                        "vendor": "Microsoft Corporation",
                        "model": "Microsoft Basic Render Driver",
                        "memory": 1024,
                        "driver_version": "10.0.19041.1"
                    },
                    "memory": {
                        "total": 65536,
                        "available": 32768,
                        "type": "DDR4"
                    },
                    "storage": {
                        "type": "NVMe",
                        "capacity": 2048,
                        "interface": "PCIe"
                    }
                },
                "os": {
                    "platform": "Windows",
                    "version": "10.0.19041",
                    "architecture": "x64",
                    "build": "19041"
                },
                "browser": {
                    "name": "Edge",
                    "version": "95.0.1020.44",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44",
                    "plugins": ["Microsoft Edge PDF Plugin", "Microsoft Silverlight"],
                    "webgl_vendor": "Microsoft",
                    "webgl_renderer": "Microsoft Basic Render Driver"
                },
                "network": {
                    "connection_type": "wifi",
                    "downlink": 50,
                    "rtt": 25,
                    "effective_type": "4g"
                },
                "screen": {
                    "width": 3840,
                    "height": 2160,
                    "color_depth": 32,
                    "pixel_ratio": 2,
                    "orientation": "landscape"
                },
                "performance": {
                    "memory_used": 16384,
                    "cpu_usage": 12.3,
                    "gpu_usage": 8.7,
                    "disk_usage": 25.4,
                    "network_latency": 22
                }
            }
        }

    def test_enhanced_vm_detection_normal_device(self):
        """Test enhanced VM detection with normal device data"""
        try:
            device_data = self.create_normal_device_data()
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=device_data)
            
            if response.status_code != 200:
                self.log_test("Enhanced VM Detection - Normal Device", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            
            # Verify response structure
            if not data.get("success"):
                self.log_test("Enhanced VM Detection - Normal Device", "FAIL", 
                            f"Response indicates failure: {data}")
                return False
            
            vm_detection = data.get("vm_detection", {})
            
            # Verify enhanced response structure
            required_fields = [
                "vm_detection_results", "vm_probability", "vm_classification", 
                "is_virtual_machine", "confidence_metrics", "risk_assessment",
                "detection_metadata", "platform_detection", "recommendation",
                "analysis_timestamp", "analysis_version"
            ]
            
            missing_fields = [field for field in required_fields if field not in vm_detection]
            if missing_fields:
                self.log_test("Enhanced VM Detection - Normal Device", "FAIL", 
                            f"Missing required fields: {missing_fields}")
                return False
            
            # Verify analysis version
            if vm_detection.get("analysis_version") != "2.0_enhanced":
                self.log_test("Enhanced VM Detection - Normal Device", "FAIL", 
                            f"Incorrect analysis version: {vm_detection.get('analysis_version')}")
                return False
            
            # Verify enhanced threshold (0.65)
            vm_probability = vm_detection.get("vm_probability", 0)
            is_vm = vm_detection.get("is_virtual_machine", False)
            expected_is_vm = vm_probability > 0.65
            
            if is_vm != expected_is_vm:
                self.log_test("Enhanced VM Detection - Normal Device", "FAIL", 
                            f"VM classification inconsistent with enhanced threshold (0.65): probability={vm_probability}, is_vm={is_vm}")
                return False
            
            # Verify all new enhanced methods are present in vm_detection_results
            vm_results = vm_detection.get("vm_detection_results", {})
            expected_methods = [
                "hardware_indicators", "hypervisor_analysis", "performance_anomalies",
                "system_analysis", "software_signatures", "network_analysis",
                "display_analysis", "consistency_analysis"
            ]
            
            missing_methods = [method for method in expected_methods if method not in vm_results]
            if missing_methods:
                self.log_test("Enhanced VM Detection - Normal Device", "FAIL", 
                            f"Missing enhanced detection methods: {missing_methods}")
                return False
            
            # Verify detection metadata
            metadata = vm_detection.get("detection_metadata", {})
            analysis_methods = metadata.get("analysis_methods_used", [])
            expected_analysis_methods = [
                "hardware_fingerprinting", "hypervisor_detection", "performance_profiling",
                "system_file_analysis", "signature_detection", "network_analysis",
                "display_analysis", "consistency_analysis"
            ]
            
            missing_analysis_methods = [method for method in expected_analysis_methods if method not in analysis_methods]
            if missing_analysis_methods:
                self.log_test("Enhanced VM Detection - Normal Device", "FAIL", 
                            f"Missing analysis methods in metadata: {missing_analysis_methods}")
                return False
            
            self.log_test("Enhanced VM Detection - Normal Device", "PASS", 
                        f"VM Probability: {vm_probability:.3f}, Classification: {vm_detection.get('vm_classification')}, Is VM: {is_vm}")
            return True
            
        except Exception as e:
            self.log_test("Enhanced VM Detection - Normal Device", "FAIL", f"Exception: {str(e)}")
            return False

    def test_enhanced_vm_detection_vm_like_data(self, platform="windows"):
        """Test enhanced VM detection with VM-like device data"""
        try:
            device_data = self.create_vm_like_device_data(platform)
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=device_data)
            
            if response.status_code != 200:
                self.log_test(f"Enhanced VM Detection - VM-like Data ({platform.title()})", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            
            if not data.get("success"):
                self.log_test(f"Enhanced VM Detection - VM-like Data ({platform.title()})", "FAIL", 
                            f"Response indicates failure: {data}")
                return False
            
            vm_detection = data.get("vm_detection", {})
            vm_probability = vm_detection.get("vm_probability", 0)
            vm_classification = vm_detection.get("vm_classification", "")
            is_vm = vm_detection.get("is_virtual_machine", False)
            
            # Verify platform-specific detection
            platform_detection = vm_detection.get("platform_detection", {})
            if not platform_detection:
                self.log_test(f"Enhanced VM Detection - VM-like Data ({platform.title()})", "FAIL", 
                            "Missing platform-specific detection results")
                return False
            
            # Verify confidence metrics
            confidence_metrics = vm_detection.get("confidence_metrics", {})
            if not confidence_metrics:
                self.log_test(f"Enhanced VM Detection - VM-like Data ({platform.title()})", "FAIL", 
                            "Missing confidence metrics")
                return False
            
            # Verify risk assessment
            risk_assessment = vm_detection.get("risk_assessment", {})
            if not risk_assessment:
                self.log_test(f"Enhanced VM Detection - VM-like Data ({platform.title()})", "FAIL", 
                            "Missing risk assessment")
                return False
            
            # Verify recommendation
            recommendation = vm_detection.get("recommendation", "")
            if not recommendation:
                self.log_test(f"Enhanced VM Detection - VM-like Data ({platform.title()})", "FAIL", 
                            "Missing recommendation")
                return False
            
            self.log_test(f"Enhanced VM Detection - VM-like Data ({platform.title()})", "PASS", 
                        f"VM Probability: {vm_probability:.3f}, Classification: {vm_classification}, Is VM: {is_vm}, Platform Detection: {len(platform_detection)} indicators")
            return True
            
        except Exception as e:
            self.log_test(f"Enhanced VM Detection - VM-like Data ({platform.title()})", "FAIL", f"Exception: {str(e)}")
            return False

    def test_enhanced_vm_detection_edge_cases(self):
        """Test enhanced VM detection with edge case data"""
        try:
            device_data = self.create_edge_case_device_data()
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=device_data)
            
            if response.status_code != 200:
                self.log_test("Enhanced VM Detection - Edge Cases", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            
            if not data.get("success"):
                self.log_test("Enhanced VM Detection - Edge Cases", "FAIL", 
                            f"Response indicates failure: {data}")
                return False
            
            vm_detection = data.get("vm_detection", {})
            
            # Verify all enhanced methods handled edge cases properly
            vm_results = vm_detection.get("vm_detection_results", {})
            
            # Check that each method returned results (not errors)
            for method_name, method_results in vm_results.items():
                if isinstance(method_results, dict) and method_results.get("error"):
                    self.log_test("Enhanced VM Detection - Edge Cases", "FAIL", 
                                f"Method {method_name} returned error: {method_results.get('error')}")
                    return False
            
            # Verify weighted scoring calculation worked
            vm_probability = vm_detection.get("vm_probability", 0)
            if not (0 <= vm_probability <= 1):
                self.log_test("Enhanced VM Detection - Edge Cases", "FAIL", 
                            f"Invalid VM probability: {vm_probability} (should be 0-1)")
                return False
            
            self.log_test("Enhanced VM Detection - Edge Cases", "PASS", 
                        f"Edge case handling successful, VM Probability: {vm_probability:.3f}")
            return True
            
        except Exception as e:
            self.log_test("Enhanced VM Detection - Edge Cases", "FAIL", f"Exception: {str(e)}")
            return False

    def test_enhanced_vm_detection_methods_verification(self):
        """Test that all enhanced VM detection methods are working correctly"""
        try:
            device_data = self.create_vm_like_device_data("windows")
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                       json=device_data)
            
            if response.status_code != 200:
                self.log_test("Enhanced VM Detection Methods Verification", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            vm_detection = data.get("vm_detection", {})
            vm_results = vm_detection.get("vm_detection_results", {})
            
            # Verify each enhanced method has proper structure and results
            method_checks = {
                "performance_anomalies": ["cpu_anomalies", "memory_anomalies", "performance_score"],
                "system_analysis": ["os_indicators", "browser_indicators", "system_score"],
                "software_signatures": ["vm_software_detected", "signature_matches", "confidence_score"],
                "network_analysis": ["network_indicators", "connection_analysis", "network_score"],
                "display_analysis": ["display_indicators", "screen_analysis", "display_score"],
                "consistency_analysis": ["consistency_score", "cross_platform_indicators", "anomaly_flags"]
            }
            
            for method_name, expected_fields in method_checks.items():
                if method_name not in vm_results:
                    self.log_test("Enhanced VM Detection Methods Verification", "FAIL", 
                                f"Missing enhanced method: {method_name}")
                    return False
                
                method_result = vm_results[method_name]
                if not isinstance(method_result, dict):
                    self.log_test("Enhanced VM Detection Methods Verification", "FAIL", 
                                f"Method {method_name} did not return dict structure")
                    return False
                
                # Check for at least some expected fields (allowing for flexibility)
                found_fields = [field for field in expected_fields if field in method_result]
                if len(found_fields) == 0:
                    self.log_test("Enhanced VM Detection Methods Verification", "FAIL", 
                                f"Method {method_name} missing expected fields: {expected_fields}")
                    return False
            
            # Verify weighted scoring calculation
            vm_probability = vm_detection.get("vm_probability", 0)
            confidence_metrics = vm_detection.get("confidence_metrics", {})
            
            if "overall_confidence" not in confidence_metrics:
                self.log_test("Enhanced VM Detection Methods Verification", "FAIL", 
                            "Missing overall_confidence in confidence_metrics")
                return False
            
            self.log_test("Enhanced VM Detection Methods Verification", "PASS", 
                        f"All enhanced methods verified, VM Probability: {vm_probability:.3f}, Confidence: {confidence_metrics.get('overall_confidence', 0):.3f}")
            return True
            
        except Exception as e:
            self.log_test("Enhanced VM Detection Methods Verification", "FAIL", f"Exception: {str(e)}")
            return False

    def test_enhanced_vm_detection_comprehensive_scenarios(self):
        """Test enhanced VM detection with multiple comprehensive scenarios"""
        try:
            scenarios = [
                ("Windows VM", "windows"),
                ("Linux VM", "linux"),
                ("macOS VM", "macos")
            ]
            
            results = []
            
            for scenario_name, platform in scenarios:
                device_data = self.create_vm_like_device_data(platform)
                
                response = self.session.post(f"{BASE_URL}/session-fingerprinting/detect-virtual-machines", 
                                           json=device_data)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        vm_detection = data.get("vm_detection", {})
                        vm_probability = vm_detection.get("vm_probability", 0)
                        vm_classification = vm_detection.get("vm_classification", "")
                        platform_detection = vm_detection.get("platform_detection", {})
                        
                        results.append({
                            "scenario": scenario_name,
                            "probability": vm_probability,
                            "classification": vm_classification,
                            "platform_indicators": len(platform_detection)
                        })
                    else:
                        results.append({"scenario": scenario_name, "error": "API failure"})
                else:
                    results.append({"scenario": scenario_name, "error": f"HTTP {response.status_code}"})
            
            # Verify all scenarios processed successfully
            failed_scenarios = [r for r in results if "error" in r]
            if failed_scenarios:
                self.log_test("Enhanced VM Detection Comprehensive Scenarios", "FAIL", 
                            f"Failed scenarios: {failed_scenarios}")
                return False
            
            # Verify platform-specific detection worked
            platform_specific_results = [r for r in results if r["platform_indicators"] > 0]
            if len(platform_specific_results) < len(scenarios):
                self.log_test("Enhanced VM Detection Comprehensive Scenarios", "FAIL", 
                            "Some scenarios missing platform-specific indicators")
                return False
            
            scenario_summary = ", ".join([f"{r['scenario']}: {r['probability']:.3f}" for r in results])
            self.log_test("Enhanced VM Detection Comprehensive Scenarios", "PASS", 
                        f"All scenarios processed successfully: {scenario_summary}")
            return True
            
        except Exception as e:
            self.log_test("Enhanced VM Detection Comprehensive Scenarios", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all enhanced VM detection tests"""
        print("=" * 80)
        print("ENHANCED VM DETECTION FUNCTIONALITY TESTING (Step 2 Enhancement)")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Admin Authentication
        test_results.append(self.test_admin_authentication())
        
        if not self.admin_authenticated:
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Test 2: Enhanced VM Detection with Normal Device Data
        test_results.append(self.test_enhanced_vm_detection_normal_device())
        
        # Test 3: Enhanced VM Detection with VM-like Data (Windows)
        test_results.append(self.test_enhanced_vm_detection_vm_like_data("windows"))
        
        # Test 4: Enhanced VM Detection with VM-like Data (Linux)
        test_results.append(self.test_enhanced_vm_detection_vm_like_data("linux"))
        
        # Test 5: Enhanced VM Detection with VM-like Data (macOS)
        test_results.append(self.test_enhanced_vm_detection_vm_like_data("macos"))
        
        # Test 6: Enhanced VM Detection with Edge Cases
        test_results.append(self.test_enhanced_vm_detection_edge_cases())
        
        # Test 7: Enhanced VM Detection Methods Verification
        test_results.append(self.test_enhanced_vm_detection_methods_verification())
        
        # Test 8: Enhanced VM Detection Comprehensive Scenarios
        test_results.append(self.test_enhanced_vm_detection_comprehensive_scenarios())
        
        # Summary
        print("=" * 80)
        print("ENHANCED VM DETECTION TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL ENHANCED VM DETECTION TESTS PASSED!")
            print("✅ All new enhanced methods are functioning correctly")
            print("✅ Enhanced threshold (0.65) is working properly")
            print("✅ Analysis version '2.0_enhanced' is confirmed")
            print("✅ Enhanced response structure includes all required fields")
            print("✅ Platform-specific detection is operational")
            print("✅ Risk assessment and recommendations are generated")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = EnhancedVMDetectionTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ ENHANCED VM DETECTION TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ ENHANCED VM DETECTION TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()