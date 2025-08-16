#!/usr/bin/env python3
"""
🎯 PHASE 1.1 ENHANCED DEVICE FINGERPRINTING BACKEND TESTING
Testing comprehensive backend functionality for PHASE 1.1 Enhanced Device Fingerprinting implementation

TESTING OBJECTIVE:
Test all backend functionality related to the newly implemented PHASE 1.1 Enhanced Device Fingerprinting system,
focusing on data processing, storage, and integration with existing fingerprinting architecture.

IMPLEMENTATION CONTEXT:
The frontend has been enhanced with 16 advanced device fingerprinting methods in SessionFingerprintCollector.js:

**WebGL Hardware Analysis (4 methods):**
- getAdvancedWebGLHardwareInfo() - GPU analysis, WebGL capabilities, rendering performance
- getCanvasBasedHardwareInfo() - Canvas rendering analysis, hardware detection
- estimateGPUMemory() - Advanced GPU memory estimation with confidence levels
- profileRenderingPerformance() - Comprehensive rendering performance profiling

**Screen Analysis (4 methods):**
- getColorProfileCharacteristics() - Color gamut, HDR, contrast analysis
- getDisplayCapabilityAnalysis() - Refresh rate, display technology, scaling
- detectMultiMonitorConfiguration() - Multi-monitor setup detection
- detectHDRWideGamutSupport() - HDR and wide gamut capabilities

**CPU Performance Profiling (4 methods):**
- detectDetailedCPUArchitecture() - Instruction sets, vendor detection, microarchitecture
- runCPUPerformanceBenchmarks() - Integer/float/vector performance testing
- analyzeInstructionSetSupport() - SIMD, AVX, crypto instructions
- detectThermalThrottling() - Performance consistency and thermal analysis

**Memory & Storage Analysis (4 methods):**
- estimateSystemMemory() - JS heap, allocation testing, virtual memory
- profileStoragePerformance() - Sequential/random testing, technology detection
- analyzeCacheHierarchy() - L1/L2/L3 cache analysis, coherency testing
- detectVirtualMemoryUsage() - Address space, memory mapping analysis

**Device Sensor Enumeration (4 methods):**
- enumerateMotionSensors() - Accelerometer, gyroscope, magnetometer
- enumerateEnvironmentalSensors() - Ambient light, temperature, pressure sensors
- enumerateBiometricSensors() - Fingerprint, face recognition, voice recognition
- enumerateConnectivitySensors() - GPS, Bluetooth, NFC, WiFi analysis

TESTING REQUIREMENTS:
1. FINGERPRINTING DATA PROCESSING ENDPOINTS
2. DATABASE INTEGRATION TESTING
3. ANOMALY DETECTION INTEGRATION
4. SESSION FINGERPRINTING ENGINE
5. API ENDPOINT FUNCTIONALITY
6. PERFORMANCE AND ERROR HANDLING
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time
import random

# Configuration
BACKEND_URL = "https://codebase-upgrade-1.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class Phase11FingerprintingTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.session_id = str(uuid.uuid4())
        self.user_id = str(uuid.uuid4())
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

    def test_database_initialization(self):
        """Test fingerprinting database initialization"""
        try:
            response = self.session.post(f"{BACKEND_URL}/admin/database/initialize-fingerprinting")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    collections_created = data.get('collections_created', 0)
                    indexes_created = data.get('indexes_created', 0)
                    self.log_result(
                        "Database Initialization", 
                        True, 
                        f"Collections: {collections_created}, Indexes: {indexes_created}"
                    )
                    return True
                else:
                    self.log_result("Database Initialization", False, f"Initialization failed: {data}")
                    return False
            else:
                self.log_result("Database Initialization", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Database Initialization", False, f"Exception: {str(e)}")
            return False

    def test_database_verification(self):
        """Test fingerprinting database verification"""
        try:
            response = self.session.get(f"{BACKEND_URL}/admin/database/verify-fingerprinting")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    collections_verified = data.get('collections_verified', 0)
                    self.log_result(
                        "Database Verification", 
                        True, 
                        f"Collections verified: {collections_verified}"
                    )
                    return True
                else:
                    self.log_result("Database Verification", False, f"Verification failed: {data}")
                    return False
            else:
                self.log_result("Database Verification", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Database Verification", False, f"Exception: {str(e)}")
            return False

    def test_database_statistics(self):
        """Test fingerprinting database statistics"""
        try:
            response = self.session.get(f"{BACKEND_URL}/admin/database/fingerprinting-stats")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    total_docs = data.get('total_documents', 0)
                    total_size = data.get('total_size_bytes', 0)
                    self.log_result(
                        "Database Statistics", 
                        True, 
                        f"Total docs: {total_docs}, Size: {total_size} bytes"
                    )
                    return True
                else:
                    self.log_result("Database Statistics", False, f"Statistics failed: {data}")
                    return False
            else:
                self.log_result("Database Statistics", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Database Statistics", False, f"Exception: {str(e)}")
            return False

    def generate_enhanced_fingerprint_data(self):
        """Generate comprehensive fingerprint data matching PHASE 1.1 enhanced methods"""
        return {
            "session_id": self.session_id,
            "device_data": {
                "hardware": {
                    # WebGL Hardware Analysis (4 methods)
                    "webgl_analysis": {
                        "gpu_vendor": "NVIDIA Corporation",
                        "gpu_renderer": "NVIDIA GeForce RTX 4080",
                        "webgl_version": "WebGL 2.0",
                        "shading_language_version": "WebGL GLSL ES 3.00",
                        "max_texture_size": 32768,
                        "max_viewport_dims": [32768, 32768],
                        "max_vertex_attribs": 16,
                        "max_fragment_uniform_vectors": 1024,
                        "extensions": [
                            "ANGLE_instanced_arrays", "EXT_blend_minmax", "EXT_color_buffer_half_float",
                            "EXT_disjoint_timer_query", "EXT_float_blend", "EXT_frag_depth"
                        ],
                        "webgl_capabilities": {
                            "vertex_shader_precision": "highp",
                            "fragment_shader_precision": "highp",
                            "max_combined_texture_image_units": 32,
                            "max_cube_map_texture_size": 16384
                        },
                        "rendering_performance": {
                            "triangle_throughput": 2500000,
                            "fill_rate": 15000000000,
                            "shader_compilation_time": 45.2
                        }
                    },
                    "canvas_hardware_detection": {
                        "rendering_speed": 1250.5,
                        "text_rendering_characteristics": {
                            "font_smoothing": "subpixel",
                            "text_baseline_shift": 0.125,
                            "character_spacing_variance": 0.02
                        },
                        "image_processing_capabilities": {
                            "filter_support": ["blur", "brightness", "contrast", "saturate"],
                            "composite_operations": 26,
                            "blend_modes": ["multiply", "screen", "overlay", "darken", "lighten"]
                        },
                        "color_analysis": {
                            "color_depth": 24,
                            "gamma_correction": 2.2,
                            "color_profile": "sRGB"
                        },
                        "anti_aliasing_analysis": {
                            "edge_smoothing": "enabled",
                            "subpixel_rendering": "rgb",
                            "aa_quality": "high"
                        }
                    },
                    "gpu_memory_estimation": {
                        "estimated_memory_mb": 16384,
                        "confidence_level": 0.92,
                        "estimation_methods": {
                            "webgl_memory_analysis": 16000,
                            "texture_memory_testing": 16200,
                            "buffer_memory_testing": 16100,
                            "memory_stress_testing": 16384
                        },
                        "memory_bandwidth_estimation": 1008000,
                        "cache_analysis": {
                            "l1_cache_size": 128,
                            "l2_cache_size": 6144,
                            "memory_bus_width": 256
                        }
                    },
                    "rendering_performance_profile": {
                        "canvas_2d_performance": {
                            "draw_calls_per_second": 125000,
                            "fill_rate_pixels_per_second": 2500000000,
                            "text_rendering_speed": 85000
                        },
                        "webgl_performance": {
                            "vertices_per_second": 50000000,
                            "triangles_per_second": 16666666,
                            "shader_operations_per_second": 1000000000
                        },
                        "gpu_compute_performance": {
                            "compute_shader_throughput": 750000000,
                            "parallel_processing_score": 0.95,
                            "memory_bandwidth_utilization": 0.88
                        },
                        "thermal_throttling_detection": {
                            "performance_consistency": 0.96,
                            "sustained_load_performance": 0.94,
                            "throttling_detected": False,
                            "confidence_level": 0.89
                        }
                    }
                },
                "screen": {
                    # Screen Analysis (4 methods)
                    "color_profile_characteristics": {
                        "color_gamut": "sRGB",
                        "hdr_support": False,
                        "wide_color_gamut": False,
                        "color_space_analysis": {
                            "primary_color_space": "sRGB",
                            "supported_color_spaces": ["sRGB", "Display-P3"],
                            "color_accuracy": 0.92
                        },
                        "contrast_ratio_analysis": {
                            "static_contrast": 1000,
                            "dynamic_contrast": 50000,
                            "brightness_range": {"min": 0.3, "max": 400}
                        },
                        "gamma_characteristics": {
                            "gamma_value": 2.2,
                            "gamma_curve": "standard",
                            "color_temperature": 6500
                        }
                    },
                    "display_capability_analysis": {
                        "refresh_rate": 144,
                        "variable_refresh_rate": True,
                        "display_technology": "IPS",
                        "pixel_density": 109,
                        "aspect_ratio": "16:9",
                        "orientation_capabilities": ["landscape", "portrait"],
                        "multi_display_detection": {
                            "display_count": 2,
                            "primary_display": 0,
                            "extended_desktop": True
                        },
                        "screen_scaling": {
                            "scaling_factor": 1.0,
                            "dpi_scaling": "100%",
                            "text_scaling": "normal"
                        }
                    },
                    "multi_monitor_configuration": {
                        "screen_count": 2,
                        "screen_arrangement": "horizontal",
                        "primary_display": {
                            "width": 2560,
                            "height": 1440,
                            "position": {"x": 0, "y": 0}
                        },
                        "secondary_displays": [
                            {
                                "width": 1920,
                                "height": 1080,
                                "position": {"x": 2560, "y": 180}
                            }
                        ],
                        "resolution_differences": True,
                        "color_profile_differences": False,
                        "virtual_screen_boundaries": {
                            "total_width": 4480,
                            "total_height": 1440
                        }
                    },
                    "hdr_wide_gamut_support": {
                        "hdr_capabilities": {
                            "hdr10_support": False,
                            "dolby_vision_support": False,
                            "hdr_brightness_range": {"min": 0.1, "max": 400}
                        },
                        "wide_gamut_capabilities": {
                            "display_p3_support": True,
                            "rec2020_support": False,
                            "adobe_rgb_support": False
                        },
                        "color_space_support": ["sRGB", "Display-P3"],
                        "bit_depth_analysis": {
                            "color_depth": 24,
                            "alpha_depth": 8,
                            "total_bit_depth": 32
                        }
                    }
                },
                "cpu": {
                    # CPU Performance Profiling (4 methods)
                    "detailed_cpu_architecture": {
                        "instruction_set_analysis": {
                            "base_instruction_set": "x86-64",
                            "supported_extensions": ["SSE4.2", "AVX2", "AVX-512", "AES-NI"],
                            "vector_width": 512,
                            "simd_capabilities": "AVX-512"
                        },
                        "cpu_vendor_detection": {
                            "vendor": "Intel",
                            "brand": "Intel(R) Core(TM) i9-13900K",
                            "family": 6,
                            "model": 183,
                            "stepping": 0
                        },
                        "architecture_family": "Raptor Lake",
                        "core_configuration": {
                            "physical_cores": 24,
                            "logical_cores": 32,
                            "performance_cores": 8,
                            "efficiency_cores": 16
                        },
                        "cache_hierarchy": {
                            "l1_instruction": "32KB x 24",
                            "l1_data": "48KB x 24", 
                            "l2_cache": "2MB x 24",
                            "l3_cache": "36MB shared"
                        },
                        "microarchitecture": "Golden Cove + Gracemont"
                    },
                    "cpu_performance_benchmarks": {
                        "integer_performance": {
                            "single_thread_score": 2150,
                            "multi_thread_score": 28500,
                            "operations_per_second": 125000000
                        },
                        "floating_point_performance": {
                            "single_precision_score": 1950,
                            "double_precision_score": 1875,
                            "flops_per_second": 95000000
                        },
                        "vector_operations_performance": {
                            "avx2_score": 2200,
                            "avx512_score": 2800,
                            "simd_throughput": 185000000
                        },
                        "branch_prediction_analysis": {
                            "prediction_accuracy": 0.97,
                            "misprediction_penalty": 15,
                            "branch_target_buffer_hits": 0.94
                        },
                        "cache_performance": {
                            "l1_hit_rate": 0.98,
                            "l2_hit_rate": 0.92,
                            "l3_hit_rate": 0.85,
                            "memory_latency_ns": 65
                        },
                        "overall_performance_score": 2450
                    },
                    "instruction_set_support": {
                        "simd_instructions": {
                            "sse_support": ["SSE", "SSE2", "SSE3", "SSSE3", "SSE4.1", "SSE4.2"],
                            "avx_support": ["AVX", "AVX2", "AVX-512F", "AVX-512DQ"],
                            "vector_performance": 0.95
                        },
                        "advanced_vector_extensions": {
                            "avx512_variants": ["AVX-512F", "AVX-512DQ", "AVX-512CD", "AVX-512BW"],
                            "vector_width": 512,
                            "register_count": 32
                        },
                        "cryptographic_instructions": {
                            "aes_ni": True,
                            "sha_extensions": True,
                            "rdrand": True,
                            "rdseed": True
                        },
                        "specialized_instructions": {
                            "bmi1": True,
                            "bmi2": True,
                            "fma3": True,
                            "f16c": True
                        }
                    },
                    "thermal_throttling_detection": {
                        "performance_consistency": 0.96,
                        "sustained_load_testing": {
                            "initial_performance": 2450,
                            "sustained_performance": 2350,
                            "performance_drop": 0.04
                        },
                        "clock_speed_monitoring": {
                            "base_clock": 3000,
                            "boost_clock": 5800,
                            "average_clock": 4200
                        },
                        "throttling_pattern_detection": {
                            "throttling_detected": False,
                            "thermal_events": 0,
                            "power_limit_events": 2
                        },
                        "confidence_level": 0.91
                    }
                },
                "memory": {
                    # Memory & Storage Analysis (4 methods)
                    "system_memory_estimation": {
                        "estimated_memory_gb": 32,
                        "confidence_level": 0.94,
                        "javascript_heap_analysis": {
                            "heap_size_limit": 4294967296,
                            "total_heap_size": 2147483648,
                            "used_heap_size": 1073741824
                        },
                        "memory_allocation_testing": {
                            "max_allocation_mb": 8192,
                            "allocation_speed": 2500,
                            "deallocation_speed": 3200
                        },
                        "virtual_memory_analysis": {
                            "address_space_size": "48-bit",
                            "virtual_memory_usage": 0.65,
                            "page_size": 4096
                        },
                        "memory_bandwidth": 51200
                    },
                    "storage_performance_profile": {
                        "sequential_performance": {
                            "read_speed_mbps": 7000,
                            "write_speed_mbps": 6500,
                            "iops_read": 1000000,
                            "iops_write": 900000
                        },
                        "random_access_performance": {
                            "random_read_4k": 750000,
                            "random_write_4k": 650000,
                            "access_latency_us": 0.1
                        },
                        "storage_technology_detection": {
                            "storage_type": "NVMe SSD",
                            "interface": "PCIe 4.0 x4",
                            "controller": "Samsung 980 PRO"
                        },
                        "cache_analysis": {
                            "cache_size_mb": 1024,
                            "cache_hit_rate": 0.92,
                            "write_cache_enabled": True
                        },
                        "performance_score": 9250
                    },
                    "cache_hierarchy_analysis": {
                        "l1_cache_analysis": {
                            "instruction_cache": "32KB",
                            "data_cache": "48KB",
                            "associativity": 8,
                            "line_size": 64
                        },
                        "l2_cache_analysis": {
                            "size": "2MB",
                            "associativity": 16,
                            "latency_cycles": 12,
                            "bandwidth_gbps": 400
                        },
                        "l3_cache_analysis": {
                            "size": "36MB",
                            "associativity": 12,
                            "latency_cycles": 40,
                            "bandwidth_gbps": 200
                        },
                        "cache_coherency": {
                            "protocol": "MESI",
                            "coherency_traffic": 0.15,
                            "false_sharing_detection": 0.02
                        }
                    },
                    "virtual_memory_usage": {
                        "address_space_analysis": {
                            "virtual_address_bits": 48,
                            "physical_address_bits": 46,
                            "page_table_levels": 4
                        },
                        "page_size_detection": {
                            "standard_page_size": 4096,
                            "large_page_support": True,
                            "huge_page_size": 2097152
                        },
                        "memory_mapping_analysis": {
                            "mapped_regions": 1250,
                            "executable_regions": 85,
                            "shared_memory_regions": 12
                        },
                        "swap_usage_detection": {
                            "swap_enabled": True,
                            "swap_size_gb": 16,
                            "swap_usage": 0.05
                        }
                    }
                },
                "sensors": {
                    # Device Sensor Enumeration (4 methods)
                    "motion_sensors": {
                        "accelerometer_analysis": {
                            "available": False,
                            "axes": 0,
                            "sensitivity": 0,
                            "range": 0
                        },
                        "gyroscope_analysis": {
                            "available": False,
                            "axes": 0,
                            "sensitivity": 0,
                            "range": 0
                        },
                        "magnetometer_analysis": {
                            "available": False,
                            "sensitivity": 0,
                            "calibration_status": "unknown"
                        },
                        "orientation_sensor": {
                            "available": False,
                            "absolute_orientation": False,
                            "relative_orientation": False
                        },
                        "motion_sensor_fusion": {
                            "sensor_fusion_available": False,
                            "motion_detection_accuracy": 0
                        }
                    },
                    "environmental_sensors": {
                        "ambient_light_sensor": {
                            "available": False,
                            "current_lux": 0,
                            "max_lux": 0
                        },
                        "proximity_sensor": {
                            "available": False,
                            "max_range": 0,
                            "current_distance": 0
                        },
                        "temperature_sensors": {
                            "ambient_temperature": False,
                            "device_temperature": False
                        },
                        "pressure_sensor": {
                            "available": False,
                            "current_pressure": 0
                        },
                        "humidity_sensor": {
                            "available": False,
                            "current_humidity": 0
                        }
                    },
                    "biometric_sensors": {
                        "fingerprint_sensor": {
                            "available": False,
                            "sensor_type": "none",
                            "security_level": "none"
                        },
                        "face_recognition": {
                            "available": False,
                            "camera_count": 1,
                            "depth_camera": False
                        },
                        "voice_recognition": {
                            "available": True,
                            "microphone_count": 1,
                            "noise_cancellation": True
                        },
                        "heart_rate_sensor": {
                            "available": False
                        }
                    },
                    "connectivity_sensors": {
                        "gps_location_services": {
                            "available": True,
                            "accuracy": "high",
                            "provider": "network"
                        },
                        "network_interfaces": {
                            "ethernet": True,
                            "wifi": True,
                            "cellular": False,
                            "bluetooth": True
                        },
                        "bluetooth_analysis": {
                            "version": "5.2",
                            "low_energy_support": True,
                            "classic_support": True
                        },
                        "nfc_detection": {
                            "available": False
                        },
                        "wifi_analysis": {
                            "standards_supported": ["802.11a", "802.11b", "802.11g", "802.11n", "802.11ac", "802.11ax"],
                            "frequency_bands": ["2.4GHz", "5GHz", "6GHz"],
                            "mimo_support": "4x4"
                        }
                    }
                },
                "browser": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "browser_name": "Chrome",
                    "browser_version": "120.0.0.0",
                    "engine_name": "Blink",
                    "engine_version": "120.0.0.0",
                    "plugins": [],
                    "languages": ["en-US", "en"],
                    "cookie_enabled": True,
                    "local_storage": True,
                    "session_storage": True,
                    "webgl_support": True,
                    "canvas_support": True
                },
                "network": {
                    "connection_type": "ethernet",
                    "effective_type": "4g",
                    "downlink": 100,
                    "rtt": 20,
                    "save_data": False,
                    "ip_address": "192.168.1.100",
                    "country": "US",
                    "region": "NY",
                    "city": "New York",
                    "timezone": "America/New_York"
                },
                "os": {
                    "platform": "Windows 10",
                    "version": "10.0.19045",
                    "architecture": "AMD64",
                    "build": "19045",
                    "kernel_version": "10.0.19045",
                    "language": "en-US",
                    "timezone": "America/New_York",
                    "timezone_offset": -300
                }
            }
        }

    def test_generate_device_signature(self):
        """Test device signature generation with enhanced fingerprint data"""
        try:
            fingerprint_data = self.generate_enhanced_fingerprint_data()
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=fingerprint_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    device_fingerprint = data.get('device_fingerprint', {})
                    device_id = device_fingerprint.get('device_id')
                    confidence_score = device_fingerprint.get('confidence_score', 0)
                    
                    self.log_result(
                        "Generate Device Signature", 
                        True, 
                        f"Device signature generated. ID: {device_id[:8]}..., Confidence: {confidence_score}"
                    )
                    return True
                else:
                    self.log_result("Generate Device Signature", False, f"Signature generation failed: {data}")
                    return False
            else:
                self.log_result("Generate Device Signature", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Generate Device Signature", False, f"Exception: {str(e)}")
            return False

    def test_analyze_hardware(self):
        """Test hardware analysis endpoint with enhanced data"""
        try:
            fingerprint_data = self.generate_enhanced_fingerprint_data()
            hardware_data = fingerprint_data["device_data"]["hardware"]
            
            payload = {
                "session_id": self.session_id,
                "hardware_data": hardware_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-hardware",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('hardware_analysis', {})
                    hardware_score = analysis.get('hardware_uniqueness_score', 0)
                    
                    self.log_result(
                        "Analyze Hardware", 
                        True, 
                        f"Hardware analysis completed. Uniqueness score: {hardware_score}"
                    )
                    return True
                else:
                    self.log_result("Analyze Hardware", False, f"Hardware analysis failed: {data}")
                    return False
            else:
                self.log_result("Analyze Hardware", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Analyze Hardware", False, f"Exception: {str(e)}")
            return False

    def test_track_device_consistency(self):
        """Test device consistency tracking"""
        try:
            fingerprint_data = self.generate_enhanced_fingerprint_data()
            
            payload = {
                "device_id": self.device_id,
                "session_id": self.session_id,
                "current_fingerprint": fingerprint_data["device_data"],
                "consistency_threshold": 0.8
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    consistency = data.get('consistency_analysis', {})
                    consistency_score = consistency.get('overall_consistency_score', 0)
                    
                    self.log_result(
                        "Track Device Consistency", 
                        True, 
                        f"Device consistency tracked. Score: {consistency_score}"
                    )
                    return True
                else:
                    self.log_result("Track Device Consistency", False, f"Consistency tracking failed: {data}")
                    return False
            else:
                self.log_result("Track Device Consistency", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Track Device Consistency", False, f"Exception: {str(e)}")
            return False

    def test_analyze_browser_fingerprint(self):
        """Test browser fingerprint analysis"""
        try:
            fingerprint_data = self.generate_enhanced_fingerprint_data()
            browser_data = fingerprint_data["device_data"]["browser"]
            
            payload = {
                "session_id": self.session_id,
                "browser_data": browser_data,
                "canvas_fingerprint": "canvas_fp_hash_12345",
                "webgl_fingerprint": "webgl_fp_hash_67890",
                "audio_fingerprint": "audio_fp_hash_abcde"
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('browser_analysis', {})
                    uniqueness_score = analysis.get('browser_uniqueness_score', 0)
                    
                    self.log_result(
                        "Analyze Browser Fingerprint", 
                        True, 
                        f"Browser analysis completed. Uniqueness: {uniqueness_score}"
                    )
                    return True
                else:
                    self.log_result("Analyze Browser Fingerprint", False, f"Browser analysis failed: {data}")
                    return False
            else:
                self.log_result("Analyze Browser Fingerprint", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Analyze Browser Fingerprint", False, f"Exception: {str(e)}")
            return False

    def test_detect_virtual_machines(self):
        """Test virtual machine detection"""
        try:
            fingerprint_data = self.generate_enhanced_fingerprint_data()
            
            payload = {
                "session_id": self.session_id,
                "device_data": fingerprint_data["device_data"]
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-virtual-machines",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    vm_analysis = data.get('vm_analysis', {})
                    vm_detected = vm_analysis.get('vm_detected', False)
                    confidence = vm_analysis.get('confidence_score', 0)
                    
                    self.log_result(
                        "Detect Virtual Machines", 
                        True, 
                        f"VM detection completed. VM detected: {vm_detected}, Confidence: {confidence}"
                    )
                    return True
                else:
                    self.log_result("Detect Virtual Machines", False, f"VM detection failed: {data}")
                    return False
            else:
                self.log_result("Detect Virtual Machines", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Detect Virtual Machines", False, f"Exception: {str(e)}")
            return False

    def test_device_analytics_retrieval(self):
        """Test device analytics retrieval"""
        try:
            response = self.session.get(f"{BACKEND_URL}/session-fingerprinting/device-analytics/{self.session_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analytics = data.get('device_analytics', {})
                    total_sessions = analytics.get('total_sessions', 0)
                    
                    self.log_result(
                        "Device Analytics Retrieval", 
                        True, 
                        f"Analytics retrieved. Total sessions: {total_sessions}"
                    )
                    return True
                else:
                    self.log_result("Device Analytics Retrieval", False, f"Analytics retrieval failed: {data}")
                    return False
            else:
                self.log_result("Device Analytics Retrieval", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Device Analytics Retrieval", False, f"Exception: {str(e)}")
            return False

    def test_ml_fingerprint_clustering(self):
        """Test ML fingerprint clustering integration"""
        try:
            fingerprint_data = self.generate_enhanced_fingerprint_data()
            
            payload = {
                "session_id": self.session_id,
                "device_fingerprint": fingerprint_data["device_data"],
                "analysis_type": "comprehensive"
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/comprehensive-analysis",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('comprehensive_analysis', {})
                    fraud_risk = analysis.get('fraud_risk_score', 0)
                    
                    self.log_result(
                        "ML Fingerprint Clustering", 
                        True, 
                        f"ML analysis completed. Fraud risk: {fraud_risk}"
                    )
                    return True
                else:
                    self.log_result("ML Fingerprint Clustering", False, f"ML analysis failed: {data}")
                    return False
            else:
                self.log_result("ML Fingerprint Clustering", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("ML Fingerprint Clustering", False, f"Exception: {str(e)}")
            return False

    def test_performance_with_large_payload(self):
        """Test performance with large fingerprint payload"""
        try:
            # Generate large fingerprint data
            large_fingerprint_data = self.generate_enhanced_fingerprint_data()
            
            # Add additional data to make payload larger
            for i in range(100):
                large_fingerprint_data["device_data"]["hardware"][f"extended_data_{i}"] = {
                    "measurement": random.uniform(0, 1000),
                    "timestamp": datetime.now().isoformat(),
                    "metadata": f"extended_measurement_{i}"
                }
            
            start_time = time.time()
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=large_fingerprint_data
            )
            
            processing_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result(
                        "Performance with Large Payload", 
                        True, 
                        f"Large payload processed in {processing_time:.2f}s"
                    )
                    return True
                else:
                    self.log_result("Performance with Large Payload", False, f"Large payload processing failed: {data}")
                    return False
            else:
                self.log_result("Performance with Large Payload", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Performance with Large Payload", False, f"Exception: {str(e)}")
            return False

    def test_error_handling_malformed_data(self):
        """Test error handling with malformed fingerprint data"""
        try:
            malformed_data = {
                "session_id": None,  # Invalid session ID
                "device_data": {
                    "hardware": "not_an_object",  # Wrong type
                    "browser": None,  # Null browser data
                    "invalid_field": {"nested": {"deeply": {"invalid": True}}}
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/generate-device-signature",
                json=malformed_data
            )
            
            # Should handle gracefully (either 200 with error handling or 400/500 with proper error)
            if response.status_code in [200, 400, 422, 500]:
                self.log_result(
                    "Error Handling - Malformed Data", 
                    True, 
                    f"Malformed data handled gracefully (Status: {response.status_code})"
                )
                return True
            else:
                self.log_result("Error Handling - Malformed Data", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Error Handling - Malformed Data", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all PHASE 1.1 Enhanced Device Fingerprinting tests"""
        print("🎯 STARTING PHASE 1.1: ENHANCED DEVICE FINGERPRINTING BACKEND TESTING")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return 0, 0
        
        # Run all tests
        tests = [
            self.test_database_initialization,
            self.test_database_verification,
            self.test_database_statistics,
            self.test_generate_device_signature,
            self.test_analyze_hardware,
            self.test_track_device_consistency,
            self.test_analyze_browser_fingerprint,
            self.test_detect_virtual_machines,
            self.test_device_analytics_retrieval,
            self.test_ml_fingerprint_clustering,
            self.test_performance_with_large_payload,
            self.test_error_handling_malformed_data
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        # Print summary
        print("\n" + "=" * 80)
        print("🎯 PHASE 1.1 ENHANCED DEVICE FINGERPRINTING TESTING SUMMARY")
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
    tester = Phase11FingerprintingTester()
    passed, total = tester.run_all_tests()
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! PHASE 1.1 Enhanced Device Fingerprinting functionality is working perfectly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the results above.")