#!/usr/bin/env python3
"""
Device Consistency Tracking Test - Focus on MongoDB Key Error Resolution
Testing POST /api/session-fingerprinting/track-device-consistency specifically for:
1. Multi-session tracking scenarios
2. Complex device data with arrays, nested objects
3. Edge cases to ensure no numeric keys cause MongoDB errors

Previous critical issue: "documents must have only string keys, key was 0" affecting multi-session tracking
"""

import requests
import json
import time
import os
import uuid
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://browser-dna-collect.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class DeviceConsistencyTrackingTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        self.test_device_ids = []
        
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

    def create_complex_device_signature(self, device_id, session_number=1, variation_level="low"):
        """Create complex device signature with arrays, nested objects, and potential numeric keys"""
        
        # Base device signature with complex data structures
        base_signature = {
            "device_id": device_id,
            "session_id": f"session_{device_id}_{session_number}",
            "hardware": {
                "cpu": {
                    "cores": 8,
                    "threads": 16,
                    "architecture": "x64",
                    "vendor": "Intel",
                    "model": "Core i7-10700K",
                    "frequency": 3800,
                    "cache_levels": {
                        "l1": 32768,
                        "l2": 262144,
                        "l3": 16777216
                    },
                    "features": ["SSE4.2", "AVX2", "AES-NI", "Hyper-Threading"],
                    "performance_cores": [
                        {"core_id": 0, "base_freq": 3800, "max_freq": 5100},
                        {"core_id": 1, "base_freq": 3800, "max_freq": 5100},
                        {"core_id": 2, "base_freq": 3800, "max_freq": 5100},
                        {"core_id": 3, "base_freq": 3800, "max_freq": 5100}
                    ]
                },
                "gpu": {
                    "vendor": "NVIDIA",
                    "renderer": "GeForce RTX 4090",
                    "version": "OpenGL 4.6.0",
                    "memory": 24576,
                    "cuda_cores": 16384,
                    "rt_cores": 128,
                    "tensor_cores": 512,
                    "memory_bandwidth": 1008,
                    "supported_apis": ["OpenGL", "DirectX 12", "Vulkan", "CUDA", "OpenCL"],
                    "display_outputs": [
                        {"port": "HDMI", "version": "2.1", "max_resolution": "7680x4320"},
                        {"port": "DisplayPort", "version": "1.4a", "max_resolution": "7680x4320"},
                        {"port": "USB-C", "version": "3.2", "max_resolution": "5120x2880"}
                    ]
                },
                "memory": {
                    "total_memory": 34359738368,
                    "available_memory": 24159738368,
                    "memory_type": "DDR4",
                    "speed": 3200,
                    "channels": 2,
                    "modules": [
                        {"slot": 0, "size": 17179869184, "speed": 3200, "manufacturer": "Corsair"},
                        {"slot": 1, "size": 17179869184, "speed": 3200, "manufacturer": "Corsair"}
                    ],
                    "timings": {
                        "cas_latency": 16,
                        "ras_to_cas": 18,
                        "ras_precharge": 18,
                        "cycle_time": 36
                    }
                },
                "storage": [
                    {
                        "drive_id": 0,
                        "type": "NVMe SSD",
                        "capacity": 2199023255552,
                        "available": 1649267441664,
                        "interface": "PCIe 4.0 x4",
                        "manufacturer": "Samsung",
                        "model": "980 PRO",
                        "read_speed": 7000,
                        "write_speed": 5100
                    },
                    {
                        "drive_id": 1,
                        "type": "SATA SSD",
                        "capacity": 1099511627776,
                        "available": 824633720832,
                        "interface": "SATA 3.0",
                        "manufacturer": "Crucial",
                        "model": "MX500",
                        "read_speed": 560,
                        "write_speed": 510
                    }
                ]
            },
            "os": {
                "platform": "Windows 11",
                "version": "10.0.22621",
                "build": "22621",
                "architecture": "AMD64",
                "kernel_version": "10.0.22621.2506",
                "language": "en-US",
                "timezone": "America/New_York",
                "timezone_offset": -300,
                "installed_updates": [
                    {"kb": "KB5031354", "installed": "2023-10-10", "type": "Security Update"},
                    {"kb": "KB5030219", "installed": "2023-09-12", "type": "Cumulative Update"},
                    {"kb": "KB5029263", "installed": "2023-08-08", "type": "Feature Update"}
                ],
                "services": {
                    "running": 156,
                    "stopped": 89,
                    "critical_services": ["Windows Security", "Windows Update", "Windows Defender"]
                }
            },
            "browser": {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "browser_name": "Chrome",
                "browser_version": "119.0.0.0",
                "engine_name": "Blink",
                "engine_version": "119.0.0.0",
                "plugins": [
                    {"name": "Chrome PDF Plugin", "version": "119.0.0.0", "enabled": True},
                    {"name": "Native Client", "version": "119.0.0.0", "enabled": True},
                    {"name": "Widevine Content Decryption Module", "version": "4.10.2557.0", "enabled": True}
                ],
                "mime_types": [
                    {"type": "application/pdf", "description": "Portable Document Format", "suffixes": "pdf"},
                    {"type": "application/x-google-chrome-pdf", "description": "Portable Document Format", "suffixes": "pdf"},
                    {"type": "application/x-nacl", "description": "Native Client Executable", "suffixes": "nexe"}
                ],
                "languages": ["en-US", "en", "es"],
                "cookie_enabled": True,
                "local_storage": True,
                "session_storage": True,
                "webgl_support": True,
                "canvas_support": True,
                "webrtc_support": True,
                "extensions": [
                    {"id": "nmmhkkegccagdldgiimedpiccmgmieda", "name": "Google Wallet", "version": "0.0.6.1"},
                    {"id": "mhjfbmdgcfjbbpaeojofohoefgiehjai", "name": "Chrome Web Store Payments", "version": "1.0.0.5"}
                ]
            },
            "network": {
                "ip_address": "192.168.1.100",
                "public_ip": "203.0.113.45",
                "connection_type": "ethernet",
                "isp": "Comcast Cable",
                "country": "US",
                "region": "California",
                "city": "San Francisco",
                "interfaces": [
                    {
                        "interface_id": 0,
                        "name": "Ethernet",
                        "type": "Ethernet",
                        "mac_address": "00:1B:44:11:3A:B7",
                        "speed": 1000,
                        "status": "connected"
                    },
                    {
                        "interface_id": 1,
                        "name": "Wi-Fi",
                        "type": "802.11ac",
                        "mac_address": "A4:C3:F0:85:AC:2D",
                        "speed": 867,
                        "status": "disconnected"
                    }
                ],
                "dns_servers": ["8.8.8.8", "8.8.4.4", "1.1.1.1"]
            },
            "screen": {
                "width": 3840,
                "height": 2160,
                "color_depth": 24,
                "pixel_ratio": 1.25,
                "orientation": "landscape",
                "available_width": 3840,
                "available_height": 2100,
                "monitors": [
                    {
                        "monitor_id": 0,
                        "width": 3840,
                        "height": 2160,
                        "refresh_rate": 144,
                        "is_primary": True,
                        "manufacturer": "ASUS",
                        "model": "PG32UQX"
                    },
                    {
                        "monitor_id": 1,
                        "width": 2560,
                        "height": 1440,
                        "refresh_rate": 165,
                        "is_primary": False,
                        "manufacturer": "Dell",
                        "model": "S2721DGF"
                    }
                ]
            },
            "performance": {
                "cpu_usage": 15.7,
                "memory_usage": 45.2,
                "disk_usage": 67.8,
                "network_usage": 2.1,
                "gpu_usage": 8.3,
                "temperature": {
                    "cpu": 42,
                    "gpu": 35,
                    "motherboard": 38
                },
                "benchmarks": {
                    "cpu_score": 28547,
                    "gpu_score": 45892,
                    "memory_score": 89234,
                    "storage_score": 12456
                }
            },
            "security": {
                "antivirus": "Windows Defender",
                "firewall_enabled": True,
                "secure_boot": True,
                "tpm_version": "2.0",
                "encryption": "BitLocker",
                "certificates": [
                    {"issuer": "Microsoft Root Certificate Authority", "valid_until": "2025-12-31"},
                    {"issuer": "DigiCert Global Root CA", "valid_until": "2024-11-10"}
                ]
            }
        }
        
        # Apply variations based on session number and variation level
        if variation_level == "medium":
            # Simulate minor hardware changes
            base_signature["hardware"]["cpu"]["frequency"] += session_number * 100
            base_signature["performance"]["cpu_usage"] += session_number * 2.5
            base_signature["performance"]["memory_usage"] += session_number * 1.8
            
        elif variation_level == "high":
            # Simulate significant changes (suspicious)
            base_signature["hardware"]["memory"]["available_memory"] -= session_number * 1073741824  # 1GB less each session
            base_signature["browser"]["browser_version"] = f"119.0.{session_number}.0"
            base_signature["network"]["ip_address"] = f"192.168.{session_number}.100"
            
        return base_signature

    def test_established_device_tracking(self):
        """Test established device tracking - multiple sessions for same device"""
        try:
            device_id = f"established_device_{uuid.uuid4().hex[:8]}"
            self.test_device_ids.append(device_id)
            
            # Simulate 5 sessions from the same established device
            sessions_completed = 0
            
            for session_num in range(1, 6):
                device_signature = self.create_complex_device_signature(
                    device_id, session_num, "low"
                )
                
                request_data = {
                    "device_id": device_id,
                    "current_signature": device_signature
                }
                
                response = self.session.post(
                    f"{BASE_URL}/session-fingerprinting/track-device-consistency",
                    json=request_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        sessions_completed += 1
                        
                        # Verify response structure
                        device_tracking = data.get("device_tracking", {})
                        consistency_score = device_tracking.get("consistency_score", 0)
                        
                        self.log_test(f"Established Device Session {session_num}", "PASS", 
                                    f"Consistency Score: {consistency_score:.3f}")
                    else:
                        self.log_test(f"Established Device Session {session_num}", "FAIL", 
                                    f"API returned success=False: {data}")
                        return False
                else:
                    self.log_test(f"Established Device Session {session_num}", "FAIL", 
                                f"HTTP {response.status_code}: {response.text}")
                    return False
                
                # Small delay between sessions
                time.sleep(0.2)
            
            if sessions_completed == 5:
                self.log_test("Established Device Tracking", "PASS", 
                            f"Successfully tracked {sessions_completed}/5 sessions without MongoDB key errors")
                return True
            else:
                self.log_test("Established Device Tracking", "FAIL", 
                            f"Only completed {sessions_completed}/5 sessions")
                return False
                
        except Exception as e:
            self.log_test("Established Device Tracking", "FAIL", f"Exception: {str(e)}")
            return False

    def test_suspicious_device_patterns(self):
        """Test suspicious device patterns - rapid device switching"""
        try:
            base_device_id = f"suspicious_device_{uuid.uuid4().hex[:8]}"
            
            # Simulate rapid device switching (high variation)
            sessions_completed = 0
            
            for session_num in range(1, 4):
                device_id = f"{base_device_id}_{session_num}"
                self.test_device_ids.append(device_id)
                
                device_signature = self.create_complex_device_signature(
                    device_id, session_num, "high"
                )
                
                request_data = {
                    "device_id": device_id,
                    "current_signature": device_signature
                }
                
                response = self.session.post(
                    f"{BASE_URL}/session-fingerprinting/track-device-consistency",
                    json=request_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        sessions_completed += 1
                        
                        device_tracking = data.get("device_tracking", {})
                        risk_assessment = device_tracking.get("risk_assessment", "unknown")
                        
                        self.log_test(f"Suspicious Device Pattern {session_num}", "PASS", 
                                    f"Risk Assessment: {risk_assessment}")
                    else:
                        self.log_test(f"Suspicious Device Pattern {session_num}", "FAIL", 
                                    f"API returned success=False: {data}")
                        return False
                else:
                    self.log_test(f"Suspicious Device Pattern {session_num}", "FAIL", 
                                f"HTTP {response.status_code}: {response.text}")
                    return False
                
                time.sleep(0.1)
            
            if sessions_completed == 3:
                self.log_test("Suspicious Device Patterns", "PASS", 
                            f"Successfully processed {sessions_completed}/3 suspicious patterns without MongoDB key errors")
                return True
            else:
                self.log_test("Suspicious Device Patterns", "FAIL", 
                            f"Only completed {sessions_completed}/3 patterns")
                return False
                
        except Exception as e:
            self.log_test("Suspicious Device Patterns", "FAIL", f"Exception: {str(e)}")
            return False

    def test_device_reputation_scoring(self):
        """Test device reputation scoring - device history analysis"""
        try:
            device_id = f"reputation_device_{uuid.uuid4().hex[:8]}"
            self.test_device_ids.append(device_id)
            
            # Build device reputation over multiple sessions with medium variations
            sessions_completed = 0
            reputation_scores = []
            
            for session_num in range(1, 8):
                device_signature = self.create_complex_device_signature(
                    device_id, session_num, "medium"
                )
                
                request_data = {
                    "device_id": device_id,
                    "current_signature": device_signature
                }
                
                response = self.session.post(
                    f"{BASE_URL}/session-fingerprinting/track-device-consistency",
                    json=request_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        sessions_completed += 1
                        
                        device_tracking = data.get("device_tracking", {})
                        consistency_score = device_tracking.get("consistency_score", 0)
                        reputation_scores.append(consistency_score)
                        
                        self.log_test(f"Reputation Building Session {session_num}", "PASS", 
                                    f"Consistency Score: {consistency_score:.3f}")
                    else:
                        self.log_test(f"Reputation Building Session {session_num}", "FAIL", 
                                    f"API returned success=False: {data}")
                        return False
                else:
                    self.log_test(f"Reputation Building Session {session_num}", "FAIL", 
                                f"HTTP {response.status_code}: {response.text}")
                    return False
                
                time.sleep(0.1)
            
            if sessions_completed == 7:
                avg_reputation = sum(reputation_scores) / len(reputation_scores)
                self.log_test("Device Reputation Scoring", "PASS", 
                            f"Built reputation over {sessions_completed} sessions, avg score: {avg_reputation:.3f}")
                return True
            else:
                self.log_test("Device Reputation Scoring", "FAIL", 
                            f"Only completed {sessions_completed}/7 reputation sessions")
                return False
                
        except Exception as e:
            self.log_test("Device Reputation Scoring", "FAIL", f"Exception: {str(e)}")
            return False

    def test_cross_session_correlation(self):
        """Test cross-session correlation - session linking analysis"""
        try:
            # Create related devices that should be correlated
            base_device_id = f"correlated_device_{uuid.uuid4().hex[:8]}"
            
            # Simulate devices from same network/location but different hardware
            correlated_devices = [
                f"{base_device_id}_laptop",
                f"{base_device_id}_desktop", 
                f"{base_device_id}_mobile"
            ]
            
            sessions_completed = 0
            
            for i, device_id in enumerate(correlated_devices):
                self.test_device_ids.append(device_id)
                
                # Create signatures with shared network characteristics but different hardware
                device_signature = self.create_complex_device_signature(
                    device_id, i + 1, "low"
                )
                
                # Keep same network info to simulate correlation
                device_signature["network"]["public_ip"] = "203.0.113.45"
                device_signature["network"]["isp"] = "Comcast Cable"
                device_signature["network"]["country"] = "US"
                device_signature["network"]["region"] = "California"
                
                # Vary hardware to simulate different devices
                if "laptop" in device_id:
                    device_signature["hardware"]["cpu"]["model"] = "Core i5-1135G7"
                    device_signature["hardware"]["gpu"]["renderer"] = "Intel Iris Xe Graphics"
                    device_signature["screen"]["width"] = 1920
                    device_signature["screen"]["height"] = 1080
                elif "mobile" in device_id:
                    device_signature["hardware"]["cpu"]["model"] = "Apple A16 Bionic"
                    device_signature["hardware"]["gpu"]["renderer"] = "Apple GPU"
                    device_signature["screen"]["width"] = 1179
                    device_signature["screen"]["height"] = 2556
                
                request_data = {
                    "device_id": device_id,
                    "current_signature": device_signature
                }
                
                response = self.session.post(
                    f"{BASE_URL}/session-fingerprinting/track-device-consistency",
                    json=request_data
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        sessions_completed += 1
                        
                        device_tracking = data.get("device_tracking", {})
                        consistency_analysis = device_tracking.get("consistency_analysis", {})
                        
                        self.log_test(f"Cross-Session Correlation {device_id.split('_')[-1]}", "PASS", 
                                    f"Device tracked successfully for correlation analysis")
                    else:
                        self.log_test(f"Cross-Session Correlation {device_id.split('_')[-1]}", "FAIL", 
                                    f"API returned success=False: {data}")
                        return False
                else:
                    self.log_test(f"Cross-Session Correlation {device_id.split('_')[-1]}", "FAIL", 
                                f"HTTP {response.status_code}: {response.text}")
                    return False
                
                time.sleep(0.1)
            
            if sessions_completed == 3:
                self.log_test("Cross-Session Correlation", "PASS", 
                            f"Successfully processed {sessions_completed}/3 correlated devices without MongoDB key errors")
                return True
            else:
                self.log_test("Cross-Session Correlation", "FAIL", 
                            f"Only completed {sessions_completed}/3 correlations")
                return False
                
        except Exception as e:
            self.log_test("Cross-Session Correlation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_edge_cases_numeric_keys(self):
        """Test edge cases with various device configurations to ensure no numeric keys cause MongoDB errors"""
        try:
            device_id = f"edge_case_device_{uuid.uuid4().hex[:8]}"
            self.test_device_ids.append(device_id)
            
            # Create device signature with potential problematic numeric keys
            problematic_signature = {
                "device_id": device_id,
                "session_id": f"session_{device_id}_edge",
                "hardware": {
                    "cpu": {
                        "cores": 8,
                        "cache_levels": {
                            0: 32768,    # Numeric key that could cause MongoDB error
                            1: 262144,   # Numeric key that could cause MongoDB error
                            2: 16777216  # Numeric key that could cause MongoDB error
                        },
                        "performance_cores": {
                            0: {"core_id": 0, "base_freq": 3800},  # Numeric key
                            1: {"core_id": 1, "base_freq": 3800},  # Numeric key
                            2: {"core_id": 2, "base_freq": 3800},  # Numeric key
                            3: {"core_id": 3, "base_freq": 3800}   # Numeric key
                        }
                    },
                    "memory": {
                        "modules": {
                            0: {"slot": 0, "size": 17179869184},  # Numeric key
                            1: {"slot": 1, "size": 17179869184}   # Numeric key
                        },
                        "timings": {
                            16: "cas_latency",    # Numeric key
                            18: "ras_to_cas",     # Numeric key
                            36: "cycle_time"      # Numeric key
                        }
                    },
                    "storage": {
                        0: {  # Numeric key
                            "type": "NVMe SSD",
                            "capacity": 2199023255552
                        },
                        1: {  # Numeric key
                            "type": "SATA SSD", 
                            "capacity": 1099511627776
                        }
                    }
                },
                "network": {
                    "interfaces": {
                        0: {"name": "Ethernet", "type": "Ethernet"},  # Numeric key
                        1: {"name": "Wi-Fi", "type": "802.11ac"}      # Numeric key
                    }
                },
                "screen": {
                    "monitors": {
                        0: {"width": 3840, "height": 2160},  # Numeric key
                        1: {"width": 2560, "height": 1440}   # Numeric key
                    }
                },
                "browser": {
                    "plugins": {
                        0: {"name": "Chrome PDF Plugin"},     # Numeric key
                        1: {"name": "Native Client"},         # Numeric key
                        2: {"name": "Widevine CDM"}          # Numeric key
                    }
                },
                "performance": {
                    "benchmarks": {
                        2023: 28547,  # Numeric key (year)
                        2024: 29123   # Numeric key (year)
                    }
                }
            }
            
            request_data = {
                "device_id": device_id,
                "current_signature": problematic_signature
            }
            
            response = self.session.post(
                f"{BASE_URL}/session-fingerprinting/track-device-consistency",
                json=request_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.log_test("Edge Cases - Numeric Keys", "PASS", 
                                "Successfully handled device signature with numeric keys - MongoDB key error resolved!")
                    return True
                else:
                    self.log_test("Edge Cases - Numeric Keys", "FAIL", 
                                f"API returned success=False: {data}")
                    return False
            else:
                error_text = response.text
                if "documents must have only string keys" in error_text or "key was" in error_text:
                    self.log_test("Edge Cases - Numeric Keys", "FAIL", 
                                f"MongoDB key error still present: {error_text}")
                else:
                    self.log_test("Edge Cases - Numeric Keys", "FAIL", 
                                f"HTTP {response.status_code}: {error_text}")
                return False
                
        except Exception as e:
            self.log_test("Edge Cases - Numeric Keys", "FAIL", f"Exception: {str(e)}")
            return False

    def test_device_consistency_history_retrieval(self):
        """Test device consistency history retrieval for tracked devices"""
        try:
            if not self.test_device_ids:
                self.log_test("Device Consistency History Retrieval", "FAIL", 
                            "No test device IDs available")
                return False
            
            # Test history retrieval for first tracked device
            test_device_id = self.test_device_ids[0]
            
            response = self.session.get(
                f"{BASE_URL}/session-fingerprinting/device-consistency/{test_device_id}"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    device_record = data.get("device_record", {})
                    tracking_history = data.get("tracking_history", [])
                    
                    self.log_test("Device Consistency History Retrieval", "PASS", 
                                f"Retrieved history for device {test_device_id}: {len(tracking_history)} tracking entries")
                    return True
                else:
                    self.log_test("Device Consistency History Retrieval", "FAIL", 
                                f"API returned success=False: {data}")
                    return False
            else:
                self.log_test("Device Consistency History Retrieval", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Device Consistency History Retrieval", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all device consistency tracking tests"""
        print("=" * 80)
        print("DEVICE CONSISTENCY TRACKING TEST - MONGODB KEY ERROR RESOLUTION")
        print("=" * 80)
        print("Testing POST /api/session-fingerprinting/track-device-consistency")
        print("Focus: Multi-session tracking scenarios that previously failed with 'documents must have only string keys, key was 0'")
        print()
        
        test_results = []
        
        # Test 1: Admin Authentication
        test_results.append(self.test_admin_authentication())
        
        if not self.admin_authenticated:
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Test 2: Established Device Tracking (Multi-session scenarios)
        test_results.append(self.test_established_device_tracking())
        
        # Test 3: Suspicious Device Patterns (Rapid device switching)
        test_results.append(self.test_suspicious_device_patterns())
        
        # Test 4: Device Reputation Scoring (Device history analysis)
        test_results.append(self.test_device_reputation_scoring())
        
        # Test 5: Cross-Session Correlation (Session linking analysis)
        test_results.append(self.test_cross_session_correlation())
        
        # Test 6: Edge Cases - Numeric Keys (Critical test for MongoDB key errors)
        test_results.append(self.test_edge_cases_numeric_keys())
        
        # Test 7: Device Consistency History Retrieval
        test_results.append(self.test_device_consistency_history_retrieval())
        
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
            print("\n🎉 ALL TESTS PASSED! Device consistency tracking is working correctly without MongoDB key errors.")
            print("✅ Multi-session tracking scenarios are now functional")
            print("✅ Complex device data with arrays and nested objects handled properly")
            print("✅ Edge cases with numeric keys resolved - no more 'documents must have only string keys' errors")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
            
            # Specific guidance for MongoDB key errors
            if not test_results[5]:  # Edge cases test failed
                print("\n🔍 CRITICAL: MongoDB key error may still be present!")
                print("   The convert_numeric_keys_to_strings() function may need review.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = DeviceConsistencyTrackingTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ DEVICE CONSISTENCY TRACKING TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ DEVICE CONSISTENCY TRACKING TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()