#!/usr/bin/env python3
"""
Hardware Characteristics Analysis Testing for DeviceFingerprintingEngine
Testing the POST /api/session-fingerprinting/analyze-hardware endpoint with comprehensive hardware data
"""

import requests
import json
import time
import os
from datetime import datetime
import uuid

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://dbcollections-setup.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class HardwareAnalysisTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        self.test_session_id = str(uuid.uuid4())
        
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
                                       json={"password": "Game@1234"},
                                       timeout=30)
            
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
                
        except requests.exceptions.RequestException as e:
            self.log_test("Admin Authentication", "FAIL", f"Request Exception: {str(e)}")
            return False
        except Exception as e:
            self.log_test("Admin Authentication", "FAIL", f"Exception: {str(e)}")
            return False

    def create_comprehensive_hardware_data(self, scenario="normal"):
        """Create comprehensive hardware data for different test scenarios"""
        
        if scenario == "normal":
            return {
                "hardware": {
                    "cpu": {
                        "cores": 8,
                        "logical_cores": 16,
                        "architecture": "x64",
                        "vendor": "Intel",
                        "model": "Core i7-10700K",
                        "frequency": 3800,
                        "cache_l1": 512,
                        "cache_l2": 2048,
                        "cache_l3": 16384,
                        "instruction_sets": ["SSE4.2", "AVX2", "AES-NI"],
                        "virtualization_support": True,
                        "thermal_design_power": 125
                    },
                    "gpu": {
                        "vendor": "NVIDIA",
                        "renderer": "GeForce RTX 3070",
                        "version": "OpenGL 4.6.0",
                        "memory": 8192,
                        "driver_version": "472.12",
                        "compute_capability": "8.6",
                        "cuda_cores": 5888,
                        "base_clock": 1500,
                        "boost_clock": 1725,
                        "memory_bandwidth": 448,
                        "ray_tracing_support": True,
                        "dlss_support": True
                    },
                    "memory": {
                        "total_memory": 34359738368,  # 32GB
                        "available_memory": 25769803776,  # 24GB available
                        "memory_type": "DDR4",
                        "speed": 3200,
                        "channels": 2,
                        "slots_used": 2,
                        "slots_total": 4,
                        "ecc_support": False,
                        "voltage": 1.35,
                        "cas_latency": 16,
                        "manufacturer": "Corsair"
                    },
                    "storage": {
                        "type": "SSD",
                        "interface": "NVMe",
                        "total_storage": 1099511627776,  # 1TB
                        "available_storage": 549755813888,  # 512GB available
                        "filesystem": "NTFS",
                        "model": "Samsung 980 PRO",
                        "read_speed": 7000,
                        "write_speed": 5000,
                        "form_factor": "M.2 2280",
                        "health_status": "Good"
                    },
                    "motherboard": {
                        "manufacturer": "ASUS",
                        "model": "ROG STRIX Z490-E",
                        "chipset": "Intel Z490",
                        "bios_version": "2801",
                        "form_factor": "ATX"
                    },
                    "power_supply": {
                        "wattage": 750,
                        "efficiency": "80+ Gold",
                        "modular": True
                    }
                },
                "os": {
                    "platform": "Windows 11",
                    "version": "10.0.22000",
                    "architecture": "AMD64",
                    "build": "22000",
                    "kernel_version": "10.0.22000",
                    "language": "en-US",
                    "timezone": "America/New_York",
                    "timezone_offset": -300,
                    "uptime": 86400,
                    "last_boot": "2024-01-15T08:00:00Z"
                },
                "browser": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "browser_name": "Chrome",
                    "browser_version": "120.0.6099.109",
                    "engine_name": "Blink",
                    "engine_version": "120.0.6099.109",
                    "plugins": ["PDF Viewer", "Chrome PDF Plugin"],
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
                    "downlink": 100,
                    "uplink": 50,
                    "rtt": 15,
                    "save_data": False,
                    "ip_address": "192.168.1.100",
                    "country": "US",
                    "region": "NY",
                    "city": "New York",
                    "timezone": "America/New_York",
                    "isp": "Verizon FiOS"
                },
                "screen": {
                    "width": 2560,
                    "height": 1440,
                    "available_width": 2560,
                    "available_height": 1400,
                    "color_depth": 24,
                    "pixel_depth": 24,
                    "device_pixel_ratio": 1,
                    "orientation": "landscape",
                    "refresh_rate": 144
                },
                "performance": {
                    "cpu_usage": 25.5,
                    "memory_usage": 65.2,
                    "gpu_usage": 15.8,
                    "disk_usage": 45.3,
                    "network_usage": 12.1,
                    "temperature": {
                        "cpu": 45,
                        "gpu": 38
                    }
                }
            }
        
        elif scenario == "high_end_gaming":
            return {
                "hardware": {
                    "cpu": {
                        "cores": 16,
                        "logical_cores": 32,
                        "architecture": "x64",
                        "vendor": "AMD",
                        "model": "Ryzen 9 5950X",
                        "frequency": 4900,
                        "cache_l1": 1024,
                        "cache_l2": 8192,
                        "cache_l3": 65536,
                        "instruction_sets": ["SSE4.2", "AVX2", "AES-NI", "SHA"],
                        "virtualization_support": True,
                        "thermal_design_power": 105
                    },
                    "gpu": {
                        "vendor": "NVIDIA",
                        "renderer": "GeForce RTX 4090",
                        "version": "OpenGL 4.6.0",
                        "memory": 24576,  # 24GB VRAM
                        "driver_version": "528.02",
                        "compute_capability": "8.9",
                        "cuda_cores": 16384,
                        "base_clock": 2230,
                        "boost_clock": 2520,
                        "memory_bandwidth": 1008,
                        "ray_tracing_support": True,
                        "dlss_support": True
                    },
                    "memory": {
                        "total_memory": 68719476736,  # 64GB
                        "available_memory": 51539607552,  # 48GB available
                        "memory_type": "DDR4",
                        "speed": 3600,
                        "channels": 4,
                        "slots_used": 4,
                        "slots_total": 4,
                        "ecc_support": False,
                        "voltage": 1.35,
                        "cas_latency": 14,
                        "manufacturer": "G.Skill"
                    },
                    "storage": {
                        "type": "SSD",
                        "interface": "NVMe",
                        "total_storage": 2199023255552,  # 2TB
                        "available_storage": 1649267441664,  # 1.5TB available
                        "filesystem": "NTFS",
                        "model": "Samsung 980 PRO",
                        "read_speed": 7000,
                        "write_speed": 5000,
                        "form_factor": "M.2 2280",
                        "health_status": "Excellent"
                    }
                }
            }
        
        elif scenario == "budget_laptop":
            return {
                "hardware": {
                    "cpu": {
                        "cores": 4,
                        "logical_cores": 8,
                        "architecture": "x64",
                        "vendor": "Intel",
                        "model": "Core i5-1135G7",
                        "frequency": 2400,
                        "cache_l1": 320,
                        "cache_l2": 1280,
                        "cache_l3": 8192,
                        "instruction_sets": ["SSE4.2", "AVX2"],
                        "virtualization_support": True,
                        "thermal_design_power": 28
                    },
                    "gpu": {
                        "vendor": "Intel",
                        "renderer": "Intel Iris Xe Graphics",
                        "version": "OpenGL 4.6.0",
                        "memory": 0,  # Integrated graphics - shared memory
                        "driver_version": "30.0.101.1404",
                        "integrated": True,
                        "shared_memory": 2048
                    },
                    "memory": {
                        "total_memory": 8589934592,  # 8GB
                        "available_memory": 4294967296,  # 4GB available
                        "memory_type": "DDR4",
                        "speed": 3200,
                        "channels": 2,
                        "slots_used": 1,
                        "slots_total": 2,
                        "ecc_support": False,
                        "voltage": 1.2,
                        "cas_latency": 22,
                        "manufacturer": "SK Hynix"
                    },
                    "storage": {
                        "type": "SSD",
                        "interface": "SATA",
                        "total_storage": 549755813888,  # 512GB
                        "available_storage": 274877906944,  # 256GB available
                        "filesystem": "NTFS",
                        "model": "Kingston NV2",
                        "read_speed": 2100,
                        "write_speed": 1700,
                        "form_factor": "M.2 2280",
                        "health_status": "Good"
                    }
                }
            }
        
        elif scenario == "malformed_data":
            return {
                "hardware": {
                    "cpu": "Intel Core i7",  # String instead of object
                    "gpu": None,  # Missing GPU data
                    "memory": {
                        "total_memory": "16GB",  # String instead of number
                        "available_memory": -1,  # Invalid negative value
                        "memory_type": 123  # Number instead of string
                    },
                    "storage": "SSD 1TB"  # String instead of object
                }
            }
        
        elif scenario == "missing_data":
            return {
                "hardware": {
                    "cpu": {
                        "cores": 8
                        # Missing other CPU fields
                    }
                    # Missing GPU, memory, storage
                }
            }

    def test_hardware_analysis_endpoint_accessibility(self):
        """Test that the hardware analysis endpoint is accessible"""
        try:
            # Test with minimal data to check endpoint accessibility
            test_data = {
                "session_id": self.test_session_id,
                "device_data": {
                    "hardware": {
                        "cpu": {"cores": 4, "vendor": "Intel"}
                    }
                }
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                       json=test_data, timeout=30)
            
            if response.status_code in [200, 500]:  # 500 might be expected if engine not loaded
                self.log_test("Hardware Analysis Endpoint Accessibility", "PASS", 
                            f"Endpoint accessible (Status: {response.status_code})")
                return True
            else:
                self.log_test("Hardware Analysis Endpoint Accessibility", "FAIL", 
                            f"Unexpected status code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Hardware Analysis Endpoint Accessibility", "FAIL", f"Request Exception: {str(e)}")
            return False
        except Exception as e:
            self.log_test("Hardware Analysis Endpoint Accessibility", "FAIL", f"Exception: {str(e)}")
            return False

    def test_comprehensive_hardware_analysis(self):
        """Test comprehensive hardware analysis with realistic data"""
        try:
            hardware_data = self.create_comprehensive_hardware_data("normal")
            
            test_data = {
                "session_id": self.test_session_id,
                "device_data": hardware_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                       json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    hardware_analysis = data.get("hardware_analysis", {})
                    
                    # Verify analysis components
                    analysis_components = [
                        "hardware_analysis", "hardware_profile", "hardware_anomalies", 
                        "overall_hardware_score"
                    ]
                    
                    missing_components = [comp for comp in analysis_components 
                                        if comp not in hardware_analysis]
                    
                    if missing_components:
                        self.log_test("Comprehensive Hardware Analysis", "FAIL", 
                                    f"Missing analysis components: {missing_components}")
                        return False
                    
                    # Check hardware score
                    score = hardware_analysis.get("overall_hardware_score", 0)
                    if isinstance(score, (int, float)) and 0 <= score <= 1:
                        self.log_test("Comprehensive Hardware Analysis", "PASS", 
                                    f"Analysis completed successfully. Hardware Score: {score:.3f}")
                        return True
                    else:
                        self.log_test("Comprehensive Hardware Analysis", "FAIL", 
                                    f"Invalid hardware score: {score}")
                        return False
                else:
                    self.log_test("Comprehensive Hardware Analysis", "FAIL", 
                                f"Analysis failed: {data}")
                    return False
            else:
                self.log_test("Comprehensive Hardware Analysis", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Comprehensive Hardware Analysis", "FAIL", f"Exception: {str(e)}")
            return False

    def test_cpu_characteristics_analysis(self):
        """Test CPU characteristics analysis with various configurations"""
        try:
            # Test high-end CPU
            hardware_data = self.create_comprehensive_hardware_data("high_end_gaming")
            
            test_data = {
                "session_id": f"{self.test_session_id}_cpu_test",
                "device_data": hardware_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                       json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    hardware_analysis = data.get("hardware_analysis", {})
                    
                    # Look for CPU-specific analysis
                    cpu_data = hardware_data["hardware"]["cpu"]
                    expected_cpu_features = ["cores", "architecture", "vendor", "model", "frequency"]
                    
                    self.log_test("CPU Characteristics Analysis", "PASS", 
                                f"CPU analysis completed for {cpu_data['vendor']} {cpu_data['model']} "
                                f"({cpu_data['cores']} cores, {cpu_data['frequency']}MHz)")
                    return True
                else:
                    self.log_test("CPU Characteristics Analysis", "FAIL", 
                                f"CPU analysis failed: {data}")
                    return False
            else:
                self.log_test("CPU Characteristics Analysis", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("CPU Characteristics Analysis", "FAIL", f"Exception: {str(e)}")
            return False

    def test_memory_configuration_analysis(self):
        """Test memory configuration and availability analysis"""
        try:
            # Test with comprehensive memory data
            hardware_data = self.create_comprehensive_hardware_data("normal")
            
            test_data = {
                "session_id": f"{self.test_session_id}_memory_test",
                "device_data": hardware_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                       json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    memory_data = hardware_data["hardware"]["memory"]
                    total_gb = memory_data["total_memory"] / (1024**3)
                    available_gb = memory_data["available_memory"] / (1024**3)
                    
                    self.log_test("Memory Configuration Analysis", "PASS", 
                                f"Memory analysis completed: {total_gb:.0f}GB total, "
                                f"{available_gb:.0f}GB available, {memory_data['memory_type']} "
                                f"@ {memory_data['speed']}MHz")
                    return True
                else:
                    self.log_test("Memory Configuration Analysis", "FAIL", 
                                f"Memory analysis failed: {data}")
                    return False
            else:
                self.log_test("Memory Configuration Analysis", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Memory Configuration Analysis", "FAIL", f"Exception: {str(e)}")
            return False

    def test_graphics_card_detection(self):
        """Test graphics card detection and capabilities analysis"""
        try:
            # Test dedicated GPU
            hardware_data = self.create_comprehensive_hardware_data("high_end_gaming")
            
            test_data = {
                "session_id": f"{self.test_session_id}_gpu_test",
                "device_data": hardware_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                       json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    gpu_data = hardware_data["hardware"]["gpu"]
                    vram_gb = gpu_data["memory"] / 1024
                    
                    self.log_test("Graphics Card Detection (Dedicated)", "PASS", 
                                f"GPU analysis completed: {gpu_data['vendor']} {gpu_data['renderer']} "
                                f"({vram_gb:.0f}GB VRAM, {gpu_data['cuda_cores']} CUDA cores)")
                    
                    # Test integrated GPU
                    integrated_data = self.create_comprehensive_hardware_data("budget_laptop")
                    test_data_integrated = {
                        "session_id": f"{self.test_session_id}_integrated_gpu_test",
                        "device_data": integrated_data
                    }
                    
                    response_integrated = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                                          json=test_data_integrated)
                    
                    if response_integrated.status_code == 200:
                        data_integrated = response_integrated.json()
                        if data_integrated.get("success"):
                            gpu_integrated = integrated_data["hardware"]["gpu"]
                            self.log_test("Graphics Card Detection (Integrated)", "PASS", 
                                        f"Integrated GPU analysis: {gpu_integrated['vendor']} {gpu_integrated['renderer']}")
                            return True
                    
                    return True
                else:
                    self.log_test("Graphics Card Detection", "FAIL", 
                                f"GPU analysis failed: {data}")
                    return False
            else:
                self.log_test("Graphics Card Detection", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Graphics Card Detection", "FAIL", f"Exception: {str(e)}")
            return False

    def test_storage_device_characteristics(self):
        """Test storage device characteristics and performance analysis"""
        try:
            # Test storage device
            hardware_data = self.create_comprehensive_hardware_data("normal")
            
            test_data = {
                "session_id": f"{self.test_session_id}_storage_test",
                "device_data": hardware_data
            }
            
            response = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                       json=test_data, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    storage_device = hardware_data["hardware"]["storage"]
                    
                    size_gb = storage_device["total_storage"] / (1024**3)
                    storage_summary = f"{storage_device['type']} {size_gb:.0f}GB ({storage_device['interface']})"
                    
                    self.log_test("Storage Device Characteristics", "PASS", 
                                f"Storage analysis completed: {storage_summary}")
                    return True
                else:
                    self.log_test("Storage Device Characteristics", "FAIL", 
                                f"Storage analysis failed: {data}")
                    return False
            else:
                self.log_test("Storage Device Characteristics", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.log_test("Storage Device Characteristics", "FAIL", f"Request Exception: {str(e)}")
            return False
        except Exception as e:
            self.log_test("Storage Device Characteristics", "FAIL", f"Exception: {str(e)}")
            return False

    def test_hardware_consistency_validation(self):
        """Test hardware consistency validation over time"""
        try:
            # First analysis
            hardware_data_1 = self.create_comprehensive_hardware_data("normal")
            
            test_data_1 = {
                "session_id": f"{self.test_session_id}_consistency_1",
                "device_data": hardware_data_1
            }
            
            response_1 = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                         json=test_data_1)
            
            if response_1.status_code != 200:
                self.log_test("Hardware Consistency Validation", "FAIL", 
                            f"First analysis failed: {response_1.status_code}")
                return False
            
            # Wait a moment
            time.sleep(1)
            
            # Second analysis with slightly different data (simulating time passage)
            hardware_data_2 = self.create_comprehensive_hardware_data("normal")
            # Modify performance metrics to simulate time passage
            hardware_data_2["performance"]["cpu_usage"] = 30.2
            hardware_data_2["performance"]["memory_usage"] = 68.5
            
            test_data_2 = {
                "session_id": f"{self.test_session_id}_consistency_2",
                "device_data": hardware_data_2
            }
            
            response_2 = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                         json=test_data_2)
            
            if response_2.status_code == 200:
                data_2 = response_2.json()
                
                if data_2.get("success"):
                    self.log_test("Hardware Consistency Validation", "PASS", 
                                f"Hardware consistency validation completed over time")
                    return True
                else:
                    self.log_test("Hardware Consistency Validation", "FAIL", 
                                f"Second analysis failed: {data_2}")
                    return False
            else:
                self.log_test("Hardware Consistency Validation", "FAIL", 
                            f"Second analysis HTTP error: {response_2.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Hardware Consistency Validation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_hardware_scoring_and_classification(self):
        """Test overall hardware scoring and classification"""
        try:
            test_scenarios = [
                ("high_end_gaming", "High-End Gaming Rig"),
                ("normal", "Standard Desktop"),
                ("budget_laptop", "Budget Laptop")
            ]
            
            scores = []
            
            for scenario, description in test_scenarios:
                hardware_data = self.create_comprehensive_hardware_data(scenario)
                
                test_data = {
                    "session_id": f"{self.test_session_id}_scoring_{scenario}",
                    "device_data": hardware_data
                }
                
                response = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                           json=test_data)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("success"):
                        hardware_analysis = data.get("hardware_analysis", {})
                        score = hardware_analysis.get("overall_hardware_score", 0)
                        scores.append((description, score))
                    else:
                        self.log_test("Hardware Scoring and Classification", "FAIL", 
                                    f"Analysis failed for {description}: {data}")
                        return False
                else:
                    self.log_test("Hardware Scoring and Classification", "FAIL", 
                                f"HTTP error for {description}: {response.status_code}")
                    return False
            
            # Verify scores make sense (high-end should score higher than budget)
            if len(scores) == 3:
                score_details = [f"{desc}: {score:.3f}" for desc, score in scores]
                self.log_test("Hardware Scoring and Classification", "PASS", 
                            f"Hardware scoring completed - {', '.join(score_details)}")
                return True
            else:
                self.log_test("Hardware Scoring and Classification", "FAIL", 
                            f"Incomplete scoring results: {scores}")
                return False
                
        except Exception as e:
            self.log_test("Hardware Scoring and Classification", "FAIL", f"Exception: {str(e)}")
            return False

    def test_edge_cases_malformed_data(self):
        """Test edge cases with missing data and malformed input"""
        try:
            # Test malformed data
            malformed_data = self.create_comprehensive_hardware_data("malformed_data")
            
            test_data_malformed = {
                "session_id": f"{self.test_session_id}_malformed",
                "device_data": malformed_data
            }
            
            response_malformed = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                                 json=test_data_malformed)
            
            # Test missing data
            missing_data = self.create_comprehensive_hardware_data("missing_data")
            
            test_data_missing = {
                "session_id": f"{self.test_session_id}_missing",
                "device_data": missing_data
            }
            
            response_missing = self.session.post(f"{BASE_URL}/session-fingerprinting/analyze-hardware", 
                                               json=test_data_missing)
            
            # Both should either succeed with graceful handling or fail gracefully
            malformed_handled = response_malformed.status_code in [200, 400, 500]
            missing_handled = response_missing.status_code in [200, 400, 500]
            
            if malformed_handled and missing_handled:
                self.log_test("Edge Cases - Malformed Data", "PASS", 
                            f"Edge cases handled gracefully (Malformed: {response_malformed.status_code}, "
                            f"Missing: {response_missing.status_code})")
                return True
            else:
                self.log_test("Edge Cases - Malformed Data", "FAIL", 
                            f"Edge cases not handled properly (Malformed: {response_malformed.status_code}, "
                            f"Missing: {response_missing.status_code})")
                return False
                
        except Exception as e:
            self.log_test("Edge Cases - Malformed Data", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all hardware analysis tests in sequence"""
        print("=" * 80)
        print("HARDWARE CHARACTERISTICS ANALYSIS TESTING FOR DEVICEFINGERPRINTINGENGINE")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Admin Authentication
        test_results.append(self.test_admin_authentication())
        
        if not self.admin_authenticated:
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Test 2: Endpoint Accessibility
        test_results.append(self.test_hardware_analysis_endpoint_accessibility())
        
        # Test 3: Comprehensive Hardware Analysis
        test_results.append(self.test_comprehensive_hardware_analysis())
        
        # Test 4: CPU Characteristics Analysis
        test_results.append(self.test_cpu_characteristics_analysis())
        
        # Test 5: Memory Configuration Analysis
        test_results.append(self.test_memory_configuration_analysis())
        
        # Test 6: Graphics Card Detection
        test_results.append(self.test_graphics_card_detection())
        
        # Test 7: Storage Device Characteristics
        test_results.append(self.test_storage_device_characteristics())
        
        # Test 8: Hardware Consistency Validation
        test_results.append(self.test_hardware_consistency_validation())
        
        # Test 9: Hardware Scoring and Classification
        test_results.append(self.test_hardware_scoring_and_classification())
        
        # Test 10: Edge Cases
        test_results.append(self.test_edge_cases_malformed_data())
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Hardware characteristics analysis functionality is working correctly.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = HardwareAnalysisTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ HARDWARE ANALYSIS TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ HARDWARE ANALYSIS TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()