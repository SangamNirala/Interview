#!/usr/bin/env python3
"""
Enhanced Fingerprinting Backend Integration Test
Testing backend integration with 150+ helper methods from SessionFingerprintCollector.js

Focus Areas:
1. Basic Backend Connectivity
2. Admin Authentication  
3. Fingerprinting Endpoints (Device, Browser, Session)
4. Database Integration
5. API Response Validation
"""

import requests
import json
import time
import uuid
from datetime import datetime
import sys
import os

# Backend URL from environment - use local for testing
BACKEND_URL = "http://127.0.0.1:8001/api"
ADMIN_PASSWORD = "Game@1234"

class EnhancedFingerprintingBackendTest:
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
        
    def test_basic_connectivity(self):
        """Test 1: Basic Backend Connectivity"""
        try:
            response = self.session.get(f"{BACKEND_URL}/languages", timeout=10)
            if response.status_code == 200:
                self.log_result("Basic Backend Connectivity", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_result("Basic Backend Connectivity", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Basic Backend Connectivity", False, f"Connection error: {str(e)}")
            return False
            
    def test_admin_authentication(self):
        """Test 2: Admin Authentication"""
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
            
    def test_database_initialization(self):
        """Test 3: Database Initialization & Verification"""
        if not self.admin_authenticated:
            self.log_result("Database Initialization", False, "Admin not authenticated")
            return False
            
        try:
            response = self.session.post(f"{BACKEND_URL}/admin/database/initialize-fingerprinting", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    collections_created = data.get("collections_created", 0)
                    indexes_created = data.get("indexes_created", 0)
                    self.log_result("Database Initialization", True, 
                                  f"Collections: {collections_created}, Indexes: {indexes_created}")
                    return True
                else:
                    self.log_result("Database Initialization", False, f"Response: {data}")
                    return False
            else:
                self.log_result("Database Initialization", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Database Initialization", False, f"Error: {str(e)}")
            return False
            
    def test_database_verification(self):
        """Test 4: Database Verification"""
        if not self.admin_authenticated:
            self.log_result("Database Verification", False, "Admin not authenticated")
            return False
            
        try:
            response = self.session.get(f"{BACKEND_URL}/admin/database/verify-fingerprinting", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    collections_verified = data.get("collections_verified", 0)
                    self.log_result("Database Verification", True, 
                                  f"Collections verified: {collections_verified}")
                    return True
                else:
                    self.log_result("Database Verification", False, f"Response: {data}")
                    return False
            else:
                self.log_result("Database Verification", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Database Verification", False, f"Error: {str(e)}")
            return False
            
    def test_device_signature_generation(self):
        """Test 5: Device Signature Generation Endpoint"""
        try:
            # Enhanced device fingerprint data matching the 150+ helper methods
            device_data = {
                "device_data": {
                    # GPU Analysis (from helper methods)
                    "gpu_characteristics": {
                        "vendor": "NVIDIA Corporation",
                        "renderer": "NVIDIA GeForce RTX 3080",
                        "webgl_version": "WebGL 2.0",
                        "extensions": ["WEBGL_debug_renderer_info", "OES_texture_float"],
                        "max_texture_size": 16384,
                        "max_viewport_dims": [16384, 16384]
                    },
                    # CPU Analysis (from helper methods)
                    "cpu_characteristics": {
                        "vendor": "Intel-like",
                        "cores": 8,
                        "architecture": "x64",
                        "instruction_sets": ["SIMD", "WebAssembly", "BigInt"],
                        "cache_analysis": {
                            "l1_cache_score": 95.2,
                            "l2_cache_score": 87.4,
                            "l3_cache_score": 78.9
                        }
                    },
                    # Browser Engine Analysis (from helper methods)
                    "browser_engine": {
                        "rendering_engine": "Blink",
                        "javascript_engine": "V8",
                        "engine_version": "109.0.5414.74",
                        "rendering_quirks": ["subpixel_rendering", "anti_aliasing"]
                    },
                    # Memory Analysis (from helper methods)
                    "memory_analysis": {
                        "js_heap_used": 45.2,
                        "js_heap_total": 67.8,
                        "js_heap_limit": 2048.0,
                        "memory_health": "good",
                        "allocation_patterns": ["normal_growth", "efficient_gc"]
                    },
                    # CSS Feature Detection (from helper methods)
                    "css_features": {
                        "transforms_3d": True,
                        "animations": True,
                        "filters": True,
                        "blend_modes": True,
                        "grid_layout": True,
                        "flexbox": True
                    },
                    # Sensor Analysis (from helper methods)
                    "sensor_data": {
                        "accelerometer": {"available": True, "stability": 0.95},
                        "gyroscope": {"available": True, "stability": 0.92},
                        "magnetometer": {"available": False, "stability": 0.0},
                        "ambient_light": {"available": True, "lux_level": 250},
                        "proximity": {"available": False, "distance": None},
                        "battery": {
                            "available": True,
                            "level": 0.85,
                            "charging": False,
                            "health_estimate": "good"
                        }
                    },
                    # Network Information (from enhanced methods)
                    "network_info": {
                        "connection_type": "wifi",
                        "effective_bandwidth": "4g",
                        "rtt": 45,
                        "downlink": 10.2,
                        "webrtc_ips": ["192.168.1.100"],
                        "dns_resolution_time": 12.5
                    },
                    # Environmental Data (from enhanced methods)
                    "environmental_data": {
                        "timezone": "America/New_York",
                        "locale": "en-US",
                        "dst_active": True,
                        "device_orientation": {"alpha": 0, "beta": 0, "gamma": 0},
                        "media_devices": {
                            "audio_input": 1,
                            "video_input": 1,
                            "audio_output": 2
                        }
                    }
                },
                "session_id": str(uuid.uuid4()),
                "timestamp": datetime.now().isoformat()
            }
            
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                                       json=device_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                device_signature = data.get("device_signature", {})
                confidence_score = device_signature.get("confidence_score", 0)
                self.log_result("Device Signature Generation", True, 
                              f"Confidence: {confidence_score}, Signature generated")
                return True
            else:
                self.log_result("Device Signature Generation", False, 
                              f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_result("Device Signature Generation", False, f"Error: {str(e)}")
            return False
            
    def test_browser_fingerprint_analysis(self):
        """Test 6: Browser Fingerprint Analysis"""
        try:
            # Enhanced browser fingerprint data
            browser_data = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "browser_data": {
                    "browser_characteristics": {
                        # Enhanced browser identification (from helper methods)
                        "browser_name": "Chrome",
                        "browser_version": "109.0.0.0",
                        "engine_name": "Blink",
                        "engine_version": "109.0.5414.74",
                        "build_info": {
                            "build_number": "5414.74",
                            "branch": "stable",
                            "architecture": "x64"
                        },
                        # JavaScript engine profiling (from helper methods)
                        "js_engine": {
                            "name": "V8",
                            "version": "10.9.194.4",
                            "features": ["BigInt", "WebAssembly", "SharedArrayBuffer"],
                            "performance_characteristics": {
                                "integer_ops_score": 95.2,
                                "float_ops_score": 87.4,
                                "memory_management": "efficient"
                            }
                        },
                        # Rendering engine analysis (from helper methods)
                        "rendering_engine": {
                            "layout_engine": "Blink",
                            "css_feature_matrix": {
                                "grid": True,
                                "flexbox": True,
                                "transforms_3d": True,
                                "filters": True
                            },
                            "rendering_quirks": ["subpixel_rendering"],
                            "graphics_acceleration": True
                        }
                    },
                    "plugins": [],
                    "screen_info": {
                        "width": 1920,
                        "height": 1080,
                        "color_depth": 24,
                        "pixel_ratio": 1
                    },
                    "timezone": "America/New_York",
                    "language": "en-US",
                    "session_id": str(uuid.uuid4())
                }
            }
            
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                                       json=browser_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                analysis = data.get("browser_analysis", {})
                fingerprint_entropy = analysis.get("fingerprint_entropy", 0)
                self.log_result("Browser Fingerprint Analysis", True, 
                              f"Entropy: {fingerprint_entropy}, Analysis completed")
                return True
            else:
                self.log_result("Browser Fingerprint Analysis", False, 
                              f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_result("Browser Fingerprint Analysis", False, f"Error: {str(e)}")
            return False
            
    def test_hardware_analysis(self):
        """Test 7: Hardware Analysis Endpoint"""
        try:
            # Enhanced hardware data from the 150+ helper methods
            hardware_data = {
                "device_data": {
                    "hardware": {
                        # WebGL Hardware Analysis (from Phase 1.1 methods)
                        "webgl_hardware": {
                            "gpu_vendor": "NVIDIA Corporation",
                            "gpu_renderer": "NVIDIA GeForce RTX 3080",
                            "webgl_capabilities": {
                                "max_texture_size": 16384,
                                "max_viewport_dims": [16384, 16384],
                                "max_vertex_attribs": 16,
                                "max_uniform_vectors": 1024
                            },
                            "rendering_performance": {
                                "shader_compilation_time": 2.5,
                                "draw_call_performance": 95.2,
                                "fps_benchmark": 144.0
                            },
                            "gpu_memory_estimate": {
                                "total_memory_mb": 10240,
                                "available_memory_mb": 8192,
                                "memory_bandwidth_gbps": 760.0
                            }
                        },
                        # CPU Performance Analysis (from Phase 1.1 methods)
                        "cpu_analysis": {
                            "architecture_detection": {
                                "vendor": "Intel-like",
                                "family": "x64",
                                "instruction_sets": ["SSE4.2", "AVX2", "AES-NI"],
                                "core_count_estimate": 8
                            },
                            "performance_benchmarks": {
                                "integer_performance": 95.2,
                                "floating_point_performance": 87.4,
                                "vector_operations": 92.1,
                                "cache_performance": 85.6
                            },
                            "thermal_analysis": {
                                "throttling_detected": False,
                                "performance_consistency": 0.98,
                                "sustained_performance": 94.1
                            }
                        },
                        # Memory and Storage Analysis (from Phase 1.1 methods)
                        "memory_storage": {
                            "system_memory_estimate": {
                                "total_memory_gb": 16.0,
                                "available_memory_gb": 12.4,
                                "memory_bandwidth_gbps": 51.2
                            },
                            "storage_performance": {
                                "sequential_read_mbps": 3500.0,
                                "sequential_write_mbps": 3000.0,
                                "random_read_iops": 500000,
                                "storage_type": "NVMe SSD"
                            },
                            "cache_hierarchy": {
                                "l1_cache_kb": 32,
                                "l2_cache_kb": 256,
                                "l3_cache_mb": 16
                            }
                        },
                        # Screen Analysis (from Phase 1.1 methods)
                        "display_analysis": {
                            "color_profile": {
                                "color_gamut": "sRGB",
                                "hdr_support": False,
                                "wide_gamut": False,
                                "bit_depth": 8
                            },
                            "display_capabilities": {
                                "refresh_rate": 144,
                                "variable_refresh": True,
                                "display_technology": "LCD",
                                "pixel_density": 91.79
                            },
                            "multi_monitor": {
                                "screen_count": 1,
                                "primary_display": True,
                                "extended_desktop": False
                            }
                        }
                    }
                },
                "session_id": str(uuid.uuid4())
            }
            
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
                                       json=hardware_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                analysis = data.get("hardware_analysis", {})
                confidence_score = analysis.get("confidence_score", 0)
                self.log_result("Hardware Analysis", True, 
                              f"Confidence: {confidence_score}, Hardware analyzed")
                return True
            else:
                self.log_result("Hardware Analysis", False, 
                              f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_result("Hardware Analysis", False, f"Error: {str(e)}")
            return False
            
    def test_device_analytics_retrieval(self):
        """Test 8: Device Analytics Retrieval"""
        try:
            session_id = str(uuid.uuid4())
            response = self.session.get(f"{BACKEND_URL}/session-fingerprinting/device-analytics/{session_id}",
                                      timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                analytics = data.get("device_analytics", {})
                self.log_result("Device Analytics Retrieval", True, 
                              f"Analytics retrieved for session: {session_id}")
                return True
            else:
                self.log_result("Device Analytics Retrieval", False, 
                              f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_result("Device Analytics Retrieval", False, f"Error: {str(e)}")
            return False
            
    def test_ml_fingerprint_clustering(self):
        """Test 9: ML Fingerprint Clustering Integration"""
        try:
            # Test comprehensive ML analysis with enhanced fingerprint data
            analysis_data = {
                "device_fingerprint": {
                    "hardware_signature": "enhanced_gpu_cpu_memory_analysis",
                    "browser_characteristics": "enhanced_browser_engine_analysis",
                    "sensor_data": "comprehensive_sensor_analysis",
                    "network_characteristics": "enhanced_network_analysis"
                },
                "user_interactions": [
                    {"type": "mouse_move", "timestamp": time.time(), "x": 100, "y": 200},
                    {"type": "key_press", "timestamp": time.time(), "key": "a", "duration": 120}
                ],
                "session_data": {
                    "session_id": str(uuid.uuid4()),
                    "duration": 300,
                    "activity_level": "high"
                }
            }
            
            response = self.session.post(f"{BACKEND_URL}/ml-fingerprint-clustering/comprehensive-analysis",
                                       json=analysis_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                ml_analysis = data.get("comprehensive_analysis", {})
                fraud_risk = ml_analysis.get("fraud_risk_score", 0)
                self.log_result("ML Fingerprint Clustering", True, 
                              f"Fraud risk: {fraud_risk}, ML analysis completed")
                return True
            else:
                self.log_result("ML Fingerprint Clustering", False, 
                              f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_result("ML Fingerprint Clustering", False, f"Error: {str(e)}")
            return False
            
    def test_virtual_machine_detection(self):
        """Test 10: Virtual Machine Detection"""
        try:
            vm_data = {
                "device_data": {
                    "hardware_indicators": {
                        "cpu_vendor": "GenuineIntel",
                        "gpu_vendor": "NVIDIA Corporation",
                        "system_manufacturer": "Dell Inc.",
                        "bios_vendor": "Dell Inc."
                    },
                    "hypervisor_detection": {
                        "hypervisor_present": False,
                        "vm_artifacts": [],
                        "performance_indicators": {
                            "cpu_performance_ratio": 0.98,
                            "memory_access_latency": 12.5,
                            "disk_io_performance": 0.95
                        }
                    }
                },
                "confidence_level": 0.95,
                "session_id": str(uuid.uuid4())
            }
            
            response = self.session.post(f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                                       json=vm_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                vm_analysis = data.get("vm_detection", {})
                is_vm = vm_analysis.get("is_virtual_machine", False)
                confidence = vm_analysis.get("confidence_score", 0)
                self.log_result("Virtual Machine Detection", True, 
                              f"VM detected: {is_vm}, Confidence: {confidence}")
                return True
            else:
                self.log_result("Virtual Machine Detection", False, 
                              f"Status: {response.status_code}, Response: {response.text[:200]}")
                return False
        except Exception as e:
            self.log_result("Virtual Machine Detection", False, f"Error: {str(e)}")
            return False
            
    def run_all_tests(self):
        """Run all enhanced fingerprinting backend tests"""
        print("🧪 Enhanced Fingerprinting Backend Integration Test")
        print("=" * 60)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test started at: {datetime.now().isoformat()}")
        print()
        
        # Core connectivity and authentication tests
        self.test_basic_connectivity()
        self.test_admin_authentication()
        
        # Database integration tests
        self.test_database_initialization()
        self.test_database_verification()
        
        # Enhanced fingerprinting endpoint tests
        self.test_device_signature_generation()
        self.test_browser_fingerprint_analysis()
        self.test_hardware_analysis()
        self.test_device_analytics_retrieval()
        self.test_ml_fingerprint_clustering()
        self.test_virtual_machine_detection()
            
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        print(f"\nTest completed at: {datetime.now().isoformat()}")
        
        return success_rate >= 70.0  # Consider 70%+ success rate as acceptable

def main():
    """Main test execution"""
    test_runner = EnhancedFingerprintingBackendTest()
    success = test_runner.run_all_tests()
    
    if success:
        print("\n🎉 Enhanced Fingerprinting Backend Integration Test PASSED")
        return 0
    else:
        print("\n💥 Enhanced Fingerprinting Backend Integration Test FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())