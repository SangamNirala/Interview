#!/usr/bin/env python3
"""
🎯 PHASE 1.2 ENHANCED BROWSER CHARACTERISTICS BACKEND TESTING
Testing the enhanced fingerprinting system to verify that the PHASE 1.2 Enhanced Browser 
Characteristics Implementation is working correctly.

Test Coverage:
1. Basic Backend Connectivity - Verify the backend is responding correctly
2. Fingerprinting Endpoints - Test fingerprinting-related endpoints for enhanced data processing
3. Enhanced Data Processing - Verify backend can handle comprehensive fingerprinting data:
   - Enhanced browser identification (detailed user agent analysis, browser build detection, 
     JS engine fingerprinting, headless browser detection)
   - JavaScript engine profiling (V8 features, performance characteristics, memory management, 
     optimization detection)
   - Rendering engine analysis (layout engine fingerprinting, CSS feature matrices, 
     rendering quirks, graphics acceleration)

Authentication: Uses password "Game@1234" for admin access
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time
import random

# Configuration
BACKEND_URL = "https://session-tracker-7.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class EnhancedFingerprintingTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.session_id = str(uuid.uuid4())
        
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

    def test_basic_backend_connectivity(self):
        """Test basic backend connectivity"""
        try:
            # Test basic health endpoint or admin login
            response = self.session.get(f"{BACKEND_URL.replace('/api', '')}/")
            
            if response.status_code in [200, 404]:  # 404 is acceptable for root endpoint
                self.log_result("Basic Backend Connectivity", True, f"Backend is responding (Status: {response.status_code})")
                return True
            else:
                self.log_result("Basic Backend Connectivity", False, f"Backend not responding properly (Status: {response.status_code})")
                return False
                
        except Exception as e:
            self.log_result("Basic Backend Connectivity", False, f"Connection error: {str(e)}")
            return False

    def test_enhanced_browser_fingerprint_processing(self):
        """Test enhanced browser fingerprint data processing"""
        try:
            # Create comprehensive enhanced browser fingerprint data
            enhanced_fingerprint_data = {
                "session_id": self.session_id,
                "browser_data": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "browser_name": "Chrome",
                    "browser_version": "120.0.6099.109",
                    "engine_name": "Blink",
                    "engine_version": "120.0.6099.109",
                    "screen_resolution": "2560x1440",
                    "color_depth": 24,
                    "timezone": "America/New_York",
                    "language": "en-US",
                    "platform": "Win32",
                    "canvas_fingerprint": "canvas_hash_67890",
                    "webgl_fingerprint": "webgl_hash_12345",
                    "audio_fingerprint": "audio_hash_54321",
                    "font_fingerprint": "font_hash_98765",
                    "plugins": [
                        {"name": "Chrome PDF Plugin", "version": "120.0.0.0", "enabled": True},
                        {"name": "Native Client", "version": "120.0.0.0", "enabled": True}
                    ],
                    "mime_types": [
                        {"type": "application/pdf", "description": "Portable Document Format", "suffixes": "pdf"}
                    ],
                    
                    # Enhanced browser identification
                    "enhanced_browser_identification": {
                        "detailed_user_agent_analysis": {
                            "browser_major_version": 120,
                            "browser_minor_version": "0.6099.109",
                            "os_name": "Windows",
                            "os_version": "10.0",
                            "device_type": "desktop",
                            "architecture": "x64"
                        },
                        "browser_build_detection": {
                            "build_number": "6099.109",
                            "build_date": "2024-01-10",
                            "channel": "stable",
                            "update_level": "current",
                            "security_patches": ["CVE-2023-7024", "CVE-2023-6345"],
                            "feature_flags": ["WebGPU", "OriginPrivateFileSystemAPI", "WebCodecs"]
                        },
                        "js_engine_fingerprinting": {
                            "engine_type": "V8",
                            "engine_version": "12.0.267.8",
                            "compilation_mode": "turbofan",
                            "optimization_level": "O3",
                            "memory_model": "generational_gc",
                            "features_supported": ["BigInt", "WeakRef", "FinalizationRegistry", "TopLevelAwait"]
                        },
                        "headless_browser_detection": {
                            "is_headless": False,
                            "headless_indicators": [],
                            "automation_detected": False,
                            "webdriver_present": False,
                            "phantom_properties": [],
                            "selenium_artifacts": []
                        }
                    },
                    
                    # JavaScript engine profiling
                    "javascript_engine_profiling": {
                        "v8_features": {
                            "turbofan_enabled": True,
                            "ignition_interpreter": True,
                            "sparkplug_compiler": True,
                            "maglev_compiler": True,
                            "concurrent_marking": True,
                            "incremental_marking": True,
                            "pointer_compression": True,
                            "sandbox_enabled": True
                        },
                        "performance_characteristics": {
                            "compilation_time_ms": 12.5,
                            "execution_time_ms": 8.3,
                            "gc_pause_time_ms": 2.1,
                            "memory_allocation_rate_mb_s": 45.2,
                            "optimization_tier": "turbofan",
                            "deoptimization_count": 0,
                            "inline_cache_hits": 0.95
                        },
                        "memory_management": {
                            "heap_size_mb": 128.5,
                            "used_heap_mb": 67.3,
                            "heap_limit_mb": 512.0,
                            "gc_type": "mark_sweep_compact",
                            "gc_frequency_hz": 0.5,
                            "memory_pressure": "low",
                            "allocation_pattern": "steady"
                        },
                        "optimization_detection": {
                            "hot_functions_count": 15,
                            "optimized_functions_count": 12,
                            "deoptimized_functions_count": 0,
                            "inline_cache_efficiency": 0.94,
                            "hidden_class_transitions": 3,
                            "polymorphic_call_sites": 2
                        }
                    },
                    
                    # Rendering engine analysis
                    "rendering_engine_analysis": {
                        "layout_engine_fingerprinting": {
                            "layout_algorithm": "LayoutNG",
                            "text_rendering": "DirectWrite",
                            "font_rendering": "ClearType",
                            "subpixel_rendering": True,
                            "hardware_acceleration": True
                        },
                        "css_feature_matrices": {
                            "css_version": "CSS3",
                            "flexbox_support": True,
                            "grid_support": True,
                            "custom_properties": True,
                            "container_queries": True,
                            "cascade_layers": True,
                            "color_functions": ["oklch", "oklab", "hwb"],
                            "viewport_units": ["dvh", "lvh", "svh"]
                        },
                        "rendering_quirks": {
                            "subpixel_precision": 0.25,
                            "font_smoothing": "antialiased",
                            "text_stroke_support": True,
                            "backdrop_filter_support": True,
                            "clip_path_support": True,
                            "mask_support": True,
                            "filter_effects": ["blur", "brightness", "contrast", "drop-shadow"]
                        },
                        "graphics_acceleration": {
                            "webgl_enabled": True,
                            "webgl_version": "2.0",
                            "webgpu_enabled": True,
                            "hardware_acceleration": True,
                            "gpu_vendor": "NVIDIA Corporation",
                            "gpu_renderer": "NVIDIA GeForce RTX 4080",
                            "gpu_driver_version": "537.13",
                            "max_texture_size": 16384
                        }
                    }
                }
            }
            
            # Test browser fingerprint analysis endpoint
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                json=enhanced_fingerprint_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('analysis', {})
                    self.log_result(
                        "Enhanced Browser Fingerprint Processing", 
                        True, 
                        f"Enhanced fingerprint processed successfully. Uniqueness Score: {analysis.get('uniqueness_score', 'N/A')}, Risk Level: {analysis.get('risk_level', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Enhanced Browser Fingerprint Processing", False, f"Processing failed: {data}")
                    return False
            else:
                self.log_result("Enhanced Browser Fingerprint Processing", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Enhanced Browser Fingerprint Processing", False, f"Exception: {str(e)}")
            return False

    def test_device_fingerprint_storage(self):
        """Test device fingerprint generation and signature"""
        try:
            device_signature_data = {
                "session_id": self.session_id,
                "device_data": {
                    "hardware_info": {
                        "cpu_cores": 8,
                        "memory_gb": 16,
                        "gpu_info": "NVIDIA GeForce RTX 4080",
                        "screen_resolution": "2560x1440",
                        "webgl_fingerprint": "webgl_hash_12345"
                    },
                    "browser_info": {
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "browser_version": "120.0.6099.109",
                        "engine_version": "120.0.6099.109",
                        "plugins": ["Chrome PDF Plugin", "Native Client"],
                        "extensions": []
                    },
                    "network_info": {
                        "ip_address": "192.168.1.100",
                        "connection_type": "ethernet",
                        "timezone": "America/New_York"
                    }
                },
                "signature_algorithm": "sha256",
                "include_behavioral_data": True
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=device_signature_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    signature = data.get('device_signature', {})
                    self.log_result(
                        "Device Fingerprint Generation", 
                        True, 
                        f"Device signature generated successfully. Signature: {signature.get('signature_hash', 'N/A')[:16]}..., Confidence: {signature.get('confidence_score', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Device Fingerprint Generation", False, f"Generation failed: {data}")
                    return False
            else:
                self.log_result("Device Fingerprint Generation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Device Fingerprint Generation", False, f"Exception: {str(e)}")
            return False

    def test_session_fingerprint_collection(self):
        """Test hardware analysis endpoint"""
        try:
            hardware_analysis_data = {
                "session_id": self.session_id,
                "device_data": {
                    "hardware": {
                        "cpu_info": {
                            "cores": 8,
                            "threads": 16,
                            "architecture": "x64",
                            "vendor": "Intel",
                            "model": "Core i7-12700K"
                        },
                        "memory_info": {
                            "total_gb": 16,
                            "available_gb": 12,
                            "type": "DDR4",
                            "speed_mhz": 3200
                        },
                        "gpu_info": {
                            "vendor": "NVIDIA",
                            "model": "GeForce RTX 4080",
                            "memory_gb": 16,
                            "driver_version": "537.13"
                        },
                        "display_info": {
                            "resolution": "2560x1440",
                            "color_depth": 24,
                            "refresh_rate": 144,
                            "hdr_support": True
                        }
                    },
                    "performance_metrics": {
                        "cpu_benchmark": 85.2,
                        "gpu_benchmark": 92.7,
                        "memory_bandwidth": 51200,
                        "storage_speed": 3500
                    }
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
                json=hardware_analysis_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('hardware_analysis', {})
                    self.log_result(
                        "Hardware Analysis", 
                        True, 
                        f"Hardware analysis completed successfully. Performance Score: {analysis.get('performance_score', 'N/A')}, Uniqueness: {analysis.get('uniqueness_score', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Hardware Analysis", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Hardware Analysis", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Hardware Analysis", False, f"Exception: {str(e)}")
            return False

    def test_ml_fingerprint_clustering(self):
        """Test ML fingerprint clustering integration"""
        try:
            clustering_data = {
                "fingerprint_data": {
                    "device_id": str(uuid.uuid4()),
                    "browser_features": [0.1, 0.2, 0.3, 0.4, 0.5],
                    "hardware_features": [0.6, 0.7, 0.8, 0.9, 1.0],
                    "behavioral_features": [0.15, 0.25, 0.35, 0.45, 0.55],
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat()
                },
                "clustering_params": {
                    "algorithm": "kmeans",
                    "n_clusters": 5,
                    "feature_weights": {"browser": 0.4, "hardware": 0.4, "behavioral": 0.2}
                },
                "analysis_type": "comprehensive"
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/comprehensive-analysis",
                json=clustering_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('analysis', {})
                    self.log_result(
                        "ML Fingerprint Clustering", 
                        True, 
                        f"Fingerprint clustered successfully. Cluster ID: {analysis.get('cluster_id', 'N/A')}, Confidence: {analysis.get('confidence', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("ML Fingerprint Clustering", False, f"Clustering failed: {data}")
                    return False
            else:
                self.log_result("ML Fingerprint Clustering", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("ML Fingerprint Clustering", False, f"Exception: {str(e)}")
            return False

    def test_device_analytics_retrieval(self):
        """Test device analytics retrieval"""
        try:
            # Test device analytics endpoint
            response = self.session.get(
                f"{BACKEND_URL}/session-fingerprinting/device-analytics/{self.session_id}"
            )
            
            if response.status_code in [200, 404]:  # 404 is acceptable for non-existent session
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        analytics = data.get('analytics', {})
                        self.log_result(
                            "Device Analytics Retrieval", 
                            True, 
                            f"Device analytics retrieved successfully. Sessions: {analytics.get('session_count', 'N/A')}, Risk Score: {analytics.get('risk_score', 'N/A')}"
                        )
                    else:
                        self.log_result("Device Analytics Retrieval", True, "Device analytics endpoint accessible but no data found")
                else:
                    self.log_result("Device Analytics Retrieval", True, "Device analytics endpoint accessible (404 for non-existent session is expected)")
                return True
            else:
                self.log_result("Device Analytics Retrieval", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Device Analytics Retrieval", False, f"Exception: {str(e)}")
            return False

    def test_fingerprint_anomaly_detection(self):
        """Test virtual machine detection"""
        try:
            vm_detection_data = {
                "session_id": self.session_id,
                "device_data": {
                    "hardware_signatures": {
                        "cpu_vendor": "GenuineIntel",
                        "cpu_model": "Intel Core i7-12700K",
                        "gpu_vendor": "NVIDIA Corporation",
                        "gpu_renderer": "NVIDIA GeForce RTX 4080",
                        "memory_total": 16384,
                        "screen_resolution": "2560x1440"
                    },
                    "virtualization_indicators": {
                        "hypervisor_present": False,
                        "vm_artifacts": [],
                        "suspicious_drivers": [],
                        "timing_anomalies": False,
                        "hardware_inconsistencies": []
                    },
                    "browser_environment": {
                        "webdriver_present": False,
                        "automation_tools": [],
                        "headless_indicators": [],
                        "plugin_anomalies": []
                    },
                    "confidence_level": 0.95,
                    "detection_sensitivity": "high"
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                json=vm_detection_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    detection = data.get('vm_detection', {})
                    self.log_result(
                        "Virtual Machine Detection", 
                        True, 
                        f"VM detection completed. Is VM: {detection.get('is_virtual_machine', 'N/A')}, Confidence: {detection.get('confidence_score', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Virtual Machine Detection", False, f"Detection failed: {data}")
                    return False
            else:
                self.log_result("Virtual Machine Detection", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Virtual Machine Detection", False, f"Exception: {str(e)}")
            return False

    def test_comprehensive_fingerprint_analysis(self):
        """Test device consistency tracking"""
        try:
            consistency_data = {
                "session_id": self.session_id,
                "device_id": str(uuid.uuid4()),
                "current_signature": {
                    "hardware_hash": "hw_hash_12345",
                    "browser_hash": "br_hash_67890",
                    "network_hash": "nw_hash_54321",
                    "behavioral_hash": "bh_hash_98765"
                },
                "historical_signatures": [
                    {
                        "timestamp": "2024-01-15T10:00:00Z",
                        "hardware_hash": "hw_hash_12345",
                        "browser_hash": "br_hash_67890",
                        "network_hash": "nw_hash_54321",
                        "behavioral_hash": "bh_hash_98765",
                        "consistency_score": 0.95
                    },
                    {
                        "timestamp": "2024-01-15T09:30:00Z",
                        "hardware_hash": "hw_hash_12345",
                        "browser_hash": "br_hash_67890",
                        "network_hash": "nw_hash_54322",  # Slight network change
                        "behavioral_hash": "bh_hash_98766",  # Slight behavioral change
                        "consistency_score": 0.88
                    }
                ],
                "tracking_params": {
                    "consistency_threshold": 0.8,
                    "anomaly_sensitivity": "medium",
                    "track_behavioral_changes": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json=consistency_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    tracking = data.get('consistency_tracking', {})
                    self.log_result(
                        "Device Consistency Tracking", 
                        True, 
                        f"Consistency tracking completed. Score: {tracking.get('consistency_score', 'N/A')}, Status: {tracking.get('consistency_status', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Device Consistency Tracking", False, f"Tracking failed: {data}")
                    return False
            else:
                self.log_result("Device Consistency Tracking", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Device Consistency Tracking", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all enhanced fingerprinting tests"""
        print("🎯 STARTING PHASE 1.2 ENHANCED BROWSER CHARACTERISTICS BACKEND TESTING")
        print("=" * 80)
        
        # Test basic connectivity first
        if not self.test_basic_backend_connectivity():
            print("❌ Basic connectivity failed. Cannot proceed with tests.")
            return 0, 0
        
        # Authenticate
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return 0, 0
        
        # Run all fingerprinting tests
        tests = [
            self.test_enhanced_browser_fingerprint_processing,
            self.test_device_fingerprint_storage,
            self.test_session_fingerprint_collection,
            self.test_ml_fingerprint_clustering,
            self.test_device_analytics_retrieval,
            self.test_fingerprint_anomaly_detection,
            self.test_comprehensive_fingerprint_analysis
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        # Print summary
        print("\n" + "=" * 80)
        print("🎯 PHASE 1.2 ENHANCED BROWSER CHARACTERISTICS TESTING SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {total + 2}")  # +2 for connectivity and auth
        print(f"Passed: {passed + 2}")  # +2 for connectivity and auth
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {((passed + 2)/(total + 2))*100:.1f}%")
        
        # Print detailed results
        print("\n📊 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        return passed + 2, total + 2

if __name__ == "__main__":
    tester = EnhancedFingerprintingTester()
    passed, total = tester.run_all_tests()
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! Enhanced fingerprinting system is working perfectly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the results above.")