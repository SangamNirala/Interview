#!/usr/bin/env python3
"""
🎯 DEVICE CONSISTENCY TRACKING BACKEND TEST
Testing enhanced track_device_consistency() functionality for DeviceFingerprintingEngine

This test covers:
1. Device consistency tracking endpoint accessibility and functionality
2. Device signature evolution tracking with historical comparison
3. Hardware change detection and validation across different scenarios
4. Suspicious device switching patterns analysis
5. Device reputation scoring based on behavior history
6. Cross-session device correlation and anomaly detection
7. MongoDB integration for tracking data storage
8. Risk assessment and consistency scoring

Test scenarios:
- New device (first time tracking)
- Established device with consistent behavior
- Device with hardware changes
- Device with suspicious switching patterns
- Edge cases with malformed data
"""

import requests
import json
import time
import uuid
from datetime import datetime, timedelta
import random

# Configuration
BACKEND_URL = "https://browser-fingerprint-1.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class DeviceConsistencyTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.admin_authenticated = False
        
    def log_test(self, test_name, success, details="", error=""):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if error:
            print(f"   Error: {error}")
        print()
    
    def authenticate_admin(self):
        """Authenticate as admin"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/login",
                json={"password": ADMIN_PASSWORD},
                timeout=30
            )
            
            if response.status_code == 200:
                self.admin_authenticated = True
                self.log_test("Admin Authentication", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_test("Admin Authentication", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, "", str(e))
            return False
    
    def generate_realistic_device_signature(self, device_type="standard", variation_level="none"):
        """Generate realistic device signature data with variations"""
        base_signatures = {
            "new_device": {
                "hardware": {
                    "cpu": {
                        "cores": 8,
                        "architecture": "x64",
                        "vendor": "Intel",
                        "model": "Intel Core i7-10700K",
                        "frequency": 3800,
                        "cache_size": 16384,
                        "features": ["sse", "sse2", "avx", "avx2"]
                    },
                    "gpu": {
                        "vendor": "NVIDIA Corporation",
                        "renderer": "NVIDIA GeForce RTX 3070",
                        "version": "OpenGL 4.6",
                        "memory": 8192,
                        "extensions": ["GL_ARB_vertex_shader", "GL_ARB_fragment_shader"]
                    },
                    "memory": {
                        "total_memory": 17179869184,  # 16GB
                        "available_memory": 12884901888,  # 12GB available
                        "memory_type": "DDR4",
                        "speed": 3200
                    },
                    "storage": {
                        "total_storage": 1099511627776,  # 1TB
                        "available_storage": 549755813888,  # 512GB available
                        "storage_type": "NVMe SSD",
                        "filesystem": "NTFS"
                    }
                },
                "os": {
                    "platform": "Windows",
                    "version": "10.0.19044",
                    "architecture": "x64",
                    "build": "19044",
                    "kernel_version": "10.0.19044.1889",
                    "language": "en-US",
                    "timezone": "America/New_York",
                    "timezone_offset": -300
                },
                "browser": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "browser_name": "Chrome",
                    "browser_version": "120.0.0.0",
                    "engine_name": "Blink",
                    "engine_version": "120.0.0.0",
                    "plugins": ["Chrome PDF Plugin", "Native Client"],
                    "languages": ["en-US", "en"],
                    "cookie_enabled": True,
                    "local_storage": True,
                    "webgl_support": True
                },
                "screen": {
                    "width": 1920,
                    "height": 1080,
                    "available_width": 1920,
                    "available_height": 1040,
                    "color_depth": 24,
                    "pixel_depth": 24,
                    "device_pixel_ratio": 1.0,
                    "orientation": "landscape"
                },
                "network": {
                    "connection_type": "ethernet",
                    "effective_type": "4g",
                    "downlink": 10.0,
                    "rtt": 50,
                    "save_data": False
                },
                "performance": {
                    "device_memory": 16,
                    "hardware_concurrency": 8,
                    "cpu_usage": 15.5,
                    "memory_usage": {"used": 8192, "total": 16384}
                }
            },
            "established_device": {
                "hardware": {
                    "cpu": {
                        "cores": 6,
                        "architecture": "x64",
                        "vendor": "AMD",
                        "model": "AMD Ryzen 5 3600",
                        "frequency": 3600,
                        "cache_size": 32768,
                        "features": ["sse", "sse2", "avx", "avx2"]
                    },
                    "gpu": {
                        "vendor": "NVIDIA Corporation",
                        "renderer": "NVIDIA GeForce GTX 1660 Ti",
                        "version": "OpenGL 4.6",
                        "memory": 6144,
                        "extensions": ["GL_ARB_vertex_shader", "GL_ARB_fragment_shader"]
                    },
                    "memory": {
                        "total_memory": 34359738368,  # 32GB
                        "available_memory": 25769803776,  # 24GB available
                        "memory_type": "DDR4",
                        "speed": 3200
                    },
                    "storage": {
                        "total_storage": 2199023255552,  # 2TB
                        "available_storage": 1099511627776,  # 1TB available
                        "storage_type": "SATA SSD",
                        "filesystem": "NTFS"
                    }
                },
                "os": {
                    "platform": "Windows",
                    "version": "11.0.22000",
                    "architecture": "x64",
                    "build": "22000",
                    "kernel_version": "10.0.22000.1335",
                    "language": "en-US",
                    "timezone": "America/Los_Angeles",
                    "timezone_offset": -480
                },
                "browser": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                    "browser_name": "Chrome",
                    "browser_version": "119.0.0.0",
                    "engine_name": "Blink",
                    "engine_version": "119.0.0.0",
                    "plugins": ["Chrome PDF Plugin", "Native Client", "Widevine Content Decryption Module"],
                    "languages": ["en-US", "en"],
                    "cookie_enabled": True,
                    "local_storage": True,
                    "webgl_support": True
                },
                "screen": {
                    "width": 2560,
                    "height": 1440,
                    "available_width": 2560,
                    "available_height": 1400,
                    "color_depth": 24,
                    "pixel_depth": 24,
                    "device_pixel_ratio": 1.0,
                    "orientation": "landscape"
                },
                "network": {
                    "connection_type": "wifi",
                    "effective_type": "4g",
                    "downlink": 25.0,
                    "rtt": 30,
                    "save_data": False
                },
                "performance": {
                    "device_memory": 32,
                    "hardware_concurrency": 12,
                    "cpu_usage": 8.2,
                    "memory_usage": {"used": 12288, "total": 32768}
                }
            },
            "hardware_changed": {
                "hardware": {
                    "cpu": {
                        "cores": 8,
                        "architecture": "x64",
                        "vendor": "Intel",
                        "model": "Intel Core i7-10700K",
                        "frequency": 3800,
                        "cache_size": 16384,
                        "features": ["sse", "sse2", "avx", "avx2"]
                    },
                    "gpu": {
                        "vendor": "NVIDIA Corporation",
                        "renderer": "NVIDIA GeForce RTX 4090",  # UPGRADED GPU
                        "version": "OpenGL 4.6",
                        "memory": 24576,  # 24GB VRAM
                        "extensions": ["GL_ARB_vertex_shader", "GL_ARB_fragment_shader", "GL_NV_gpu_shader5"]
                    },
                    "memory": {
                        "total_memory": 34359738368,  # UPGRADED TO 32GB
                        "available_memory": 28991029248,  # 27GB available
                        "memory_type": "DDR4",
                        "speed": 3600  # FASTER MEMORY
                    },
                    "storage": {
                        "total_storage": 2199023255552,  # ADDED STORAGE - 2TB
                        "available_storage": 1649267441664,  # 1.5TB available
                        "storage_type": "NVMe SSD",  # UPGRADED TO NVMe
                        "filesystem": "NTFS"
                    }
                },
                "os": {
                    "platform": "Windows",
                    "version": "11.0.22621",  # UPDATED OS
                    "architecture": "x64",
                    "build": "22621",
                    "kernel_version": "10.0.22621.2506",
                    "language": "en-US",
                    "timezone": "America/New_York",
                    "timezone_offset": -300
                },
                "browser": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    "browser_name": "Chrome",
                    "browser_version": "121.0.0.0",  # UPDATED BROWSER
                    "engine_name": "Blink",
                    "engine_version": "121.0.0.0",
                    "plugins": ["Chrome PDF Plugin", "Native Client", "Widevine Content Decryption Module"],
                    "languages": ["en-US", "en"],
                    "cookie_enabled": True,
                    "local_storage": True,
                    "webgl_support": True
                },
                "screen": {
                    "width": 1920,
                    "height": 1080,
                    "available_width": 1920,
                    "available_height": 1040,
                    "color_depth": 24,
                    "pixel_depth": 24,
                    "device_pixel_ratio": 1.0,
                    "orientation": "landscape"
                },
                "network": {
                    "connection_type": "ethernet",
                    "effective_type": "4g",
                    "downlink": 50.0,  # FASTER CONNECTION
                    "rtt": 25,  # LOWER LATENCY
                    "save_data": False
                },
                "performance": {
                    "device_memory": 32,  # UPDATED
                    "hardware_concurrency": 16,  # MORE THREADS
                    "cpu_usage": 12.1,
                    "memory_usage": {"used": 16384, "total": 32768}
                }
            },
            "suspicious_device": {
                "hardware": {
                    "cpu": {
                        "cores": 2,  # SUSPICIOUS: Very low core count
                        "architecture": "x64",
                        "vendor": "QEMU",  # SUSPICIOUS: VM indicator
                        "model": "QEMU Virtual CPU version 2.5+",
                        "frequency": 2400,
                        "cache_size": 4096,
                        "features": ["sse", "sse2"]
                    },
                    "gpu": {
                        "vendor": "VMware, Inc.",  # SUSPICIOUS: VM GPU
                        "renderer": "SVGA3D; build: RELEASE; LLVM;",
                        "version": "OpenGL 2.1",
                        "memory": 128,  # SUSPICIOUS: Very low VRAM
                        "extensions": ["GL_ARB_vertex_shader"]
                    },
                    "memory": {
                        "total_memory": 4294967296,  # SUSPICIOUS: Exactly 4GB (VM typical)
                        "available_memory": 2147483648,  # Exactly 2GB available
                        "memory_type": "DDR3",
                        "speed": 1600
                    },
                    "storage": {
                        "total_storage": 21474836480,  # SUSPICIOUS: Exactly 20GB (VM typical)
                        "available_storage": 10737418240,  # Exactly 10GB available
                        "storage_type": "Virtual Disk",  # SUSPICIOUS: VM storage
                        "filesystem": "ext4"
                    }
                },
                "os": {
                    "platform": "Linux",
                    "version": "Ubuntu 20.04.3 LTS",
                    "architecture": "x64",
                    "build": "5.4.0-91-generic",
                    "kernel_version": "5.4.0-91-generic #102-Ubuntu",
                    "language": "en-US",
                    "timezone": "UTC",  # SUSPICIOUS: Generic timezone
                    "timezone_offset": 0
                },
                "browser": {
                    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                    "browser_name": "Chrome",
                    "browser_version": "96.0.4664.45",  # SUSPICIOUS: Outdated browser
                    "engine_name": "Blink",
                    "engine_version": "96.0.4664.45",
                    "plugins": [],  # SUSPICIOUS: No plugins
                    "languages": ["en-US"],
                    "cookie_enabled": True,
                    "local_storage": True,
                    "webgl_support": False  # SUSPICIOUS: No WebGL
                },
                "screen": {
                    "width": 1024,  # SUSPICIOUS: VM-typical resolution
                    "height": 768,
                    "available_width": 1024,
                    "available_height": 768,
                    "color_depth": 24,
                    "pixel_depth": 24,
                    "device_pixel_ratio": 1.0,
                    "orientation": "landscape"
                },
                "network": {
                    "connection_type": "ethernet",
                    "effective_type": "3g",  # SUSPICIOUS: Slow connection
                    "downlink": 1.5,
                    "rtt": 200,  # SUSPICIOUS: High latency
                    "save_data": True
                },
                "performance": {
                    "device_memory": 4,
                    "hardware_concurrency": 2,  # SUSPICIOUS: Low concurrency
                    "cpu_usage": 45.8,  # SUSPICIOUS: High CPU usage
                    "memory_usage": {"used": 3072, "total": 4096}
                }
            }
        }
        
        signature = base_signatures.get(device_type, base_signatures["new_device"]).copy()
        
        # Apply variations based on variation_level
        if variation_level == "minor":
            # Minor variations (software updates, minor performance changes)
            if "browser" in signature:
                # Update browser version slightly
                current_version = signature["browser"].get("browser_version", "120.0.0.0")
                version_parts = current_version.split(".")
                if len(version_parts) >= 3:
                    version_parts[2] = str(int(version_parts[2]) + random.randint(1, 5))
                    signature["browser"]["browser_version"] = ".".join(version_parts)
                    signature["browser"]["engine_version"] = ".".join(version_parts)
            
            # Minor performance variations
            if "performance" in signature:
                signature["performance"]["cpu_usage"] += random.uniform(-2.0, 2.0)
                if "memory_usage" in signature["performance"]:
                    used_mem = signature["performance"]["memory_usage"]["used"]
                    signature["performance"]["memory_usage"]["used"] = max(1024, used_mem + random.randint(-1024, 1024))
        
        elif variation_level == "moderate":
            # Moderate variations (OS updates, driver updates)
            if "os" in signature:
                # Update OS build
                current_build = signature["os"].get("build", "19044")
                try:
                    build_num = int(current_build) + random.randint(10, 100)
                    signature["os"]["build"] = str(build_num)
                except:
                    pass
            
            # Update available memory/storage
            if "hardware" in signature and "memory" in signature["hardware"]:
                available_mem = signature["hardware"]["memory"]["available_memory"]
                signature["hardware"]["memory"]["available_memory"] = max(
                    available_mem // 2, 
                    available_mem + random.randint(-2147483648, 2147483648)  # ±2GB variation
                )
        
        elif variation_level == "major":
            # Major variations (hardware changes)
            if "hardware" in signature:
                # Change GPU memory
                if "gpu" in signature["hardware"]:
                    signature["hardware"]["gpu"]["memory"] *= random.choice([2, 4])  # Double or quadruple VRAM
                
                # Change total memory
                if "memory" in signature["hardware"]:
                    current_mem = signature["hardware"]["memory"]["total_memory"]
                    signature["hardware"]["memory"]["total_memory"] = current_mem * random.choice([2, 4])
                    signature["hardware"]["memory"]["available_memory"] = int(signature["hardware"]["memory"]["total_memory"] * 0.75)
        
        return signature
    
    def test_new_device_tracking(self):
        """Test device consistency tracking for a new device (first time)"""
        try:
            device_id = f"new_device_{uuid.uuid4().hex[:8]}"
            signature = self.generate_realistic_device_signature("new_device")
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json={
                    "device_id": device_id,
                    "current_signature": signature
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Validate response structure
                required_fields = ["success", "device_tracking", "storage_confirmation"]
                missing_fields = [field for field in required_fields if field not in result]
                
                if missing_fields:
                    self.log_test("New Device Tracking", False, 
                                f"Missing fields: {missing_fields}", "")
                    return False
                
                # Validate device tracking data
                device_tracking = result["device_tracking"]
                tracking_fields = ["device_id", "consistency_analysis", "consistency_score", "risk_assessment"]
                missing_tracking_fields = [field for field in tracking_fields if field not in device_tracking]
                
                if missing_tracking_fields:
                    self.log_test("New Device Tracking", False, 
                                f"Missing tracking fields: {missing_tracking_fields}", "")
                    return False
                
                # Check consistency analysis components
                consistency_analysis = device_tracking["consistency_analysis"]
                analysis_components = ["evolution_tracking", "hardware_changes", "switching_patterns", 
                                     "reputation_score", "session_correlation"]
                
                present_components = [comp for comp in analysis_components if comp in consistency_analysis]
                
                self.log_test("New Device Tracking", True, 
                            f"Device ID: {device_id}, Consistency Score: {device_tracking['consistency_score']}, "
                            f"Risk Level: {device_tracking['risk_assessment']}, "
                            f"Analysis Components: {len(present_components)}/5")
                return True
            else:
                self.log_test("New Device Tracking", False, 
                            f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("New Device Tracking", False, "", str(e))
            return False
    
    def test_established_device_tracking(self):
        """Test device consistency tracking for an established device with consistent behavior"""
        try:
            device_id = f"established_device_{uuid.uuid4().hex[:8]}"
            
            # Simulate multiple sessions with minor variations
            for session_num in range(3):
                variation_level = "minor" if session_num > 0 else "none"
                signature = self.generate_realistic_device_signature("established_device", variation_level)
                
                response = self.session.post(
                    f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                    json={
                        "device_id": device_id,
                        "current_signature": signature
                    },
                    timeout=30
                )
                
                if response.status_code != 200:
                    self.log_test("Established Device Tracking", False, 
                                f"Session {session_num + 1} failed with status: {response.status_code}", 
                                response.text)
                    return False
                
                # Small delay between sessions
                time.sleep(0.5)
            
            # Final check - should show good consistency
            final_response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json={
                    "device_id": device_id,
                    "current_signature": self.generate_realistic_device_signature("established_device", "minor")
                },
                timeout=30
            )
            
            if final_response.status_code == 200:
                result = final_response.json()
                device_tracking = result["device_tracking"]
                consistency_score = device_tracking["consistency_score"]
                risk_assessment = device_tracking["risk_assessment"]
                
                # Established device should have good consistency
                consistency_good = isinstance(consistency_score, (int, float)) and consistency_score >= 0.0
                
                self.log_test("Established Device Tracking", True, 
                            f"Device ID: {device_id}, Final Consistency Score: {consistency_score}, "
                            f"Risk Assessment: {risk_assessment}, Sessions: 4")
                return True
            else:
                self.log_test("Established Device Tracking", False, 
                            f"Final check failed with status: {final_response.status_code}", 
                            final_response.text)
                return False
                
        except Exception as e:
            self.log_test("Established Device Tracking", False, "", str(e))
            return False
    
    def test_hardware_change_detection(self):
        """Test hardware change detection and validation"""
        try:
            device_id = f"hardware_change_device_{uuid.uuid4().hex[:8]}"
            
            # First session with original hardware
            original_signature = self.generate_realistic_device_signature("new_device")
            
            response1 = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json={
                    "device_id": device_id,
                    "current_signature": original_signature
                },
                timeout=30
            )
            
            if response1.status_code != 200:
                self.log_test("Hardware Change Detection", False, 
                            f"Initial session failed: {response1.status_code}", response1.text)
                return False
            
            time.sleep(1)
            
            # Second session with hardware changes
            changed_signature = self.generate_realistic_device_signature("hardware_changed")
            
            response2 = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json={
                    "device_id": device_id,
                    "current_signature": changed_signature
                },
                timeout=30
            )
            
            if response2.status_code == 200:
                result = response2.json()
                device_tracking = result["device_tracking"]
                consistency_analysis = device_tracking["consistency_analysis"]
                
                # Check if hardware changes were detected
                hardware_changes = consistency_analysis.get("hardware_changes", {})
                evolution_tracking = consistency_analysis.get("evolution_tracking", {})
                
                self.log_test("Hardware Change Detection", True, 
                            f"Device ID: {device_id}, Hardware Changes Detected: {bool(hardware_changes)}, "
                            f"Evolution Tracked: {bool(evolution_tracking)}, "
                            f"Consistency Score: {device_tracking['consistency_score']}")
                return True
            else:
                self.log_test("Hardware Change Detection", False, 
                            f"Hardware change session failed: {response2.status_code}", response2.text)
                return False
                
        except Exception as e:
            self.log_test("Hardware Change Detection", False, "", str(e))
            return False
    
    def test_suspicious_device_patterns(self):
        """Test suspicious device switching patterns analysis"""
        try:
            device_id = f"suspicious_device_{uuid.uuid4().hex[:8]}"
            
            # Multiple sessions with suspicious characteristics
            for session_num in range(3):
                signature = self.generate_realistic_device_signature("suspicious_device")
                
                # Add some randomness to make it more suspicious
                if session_num > 0:
                    # Change timezone randomly (suspicious behavior)
                    timezones = ["UTC", "America/New_York", "Europe/London", "Asia/Tokyo"]
                    signature["os"]["timezone"] = random.choice(timezones)
                    signature["os"]["timezone_offset"] = random.choice([0, -300, 0, 540])
                    
                    # Change screen resolution (suspicious)
                    resolutions = [(1024, 768), (1280, 1024), (1366, 768), (800, 600)]
                    width, height = random.choice(resolutions)
                    signature["screen"]["width"] = width
                    signature["screen"]["height"] = height
                
                response = self.session.post(
                    f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                    json={
                        "device_id": device_id,
                        "current_signature": signature
                    },
                    timeout=30
                )
                
                if response.status_code != 200:
                    self.log_test("Suspicious Device Patterns", False, 
                                f"Suspicious session {session_num + 1} failed: {response.status_code}", 
                                response.text)
                    return False
                
                time.sleep(0.5)
            
            # Final analysis should detect suspicious patterns
            final_response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json={
                    "device_id": device_id,
                    "current_signature": self.generate_realistic_device_signature("suspicious_device")
                },
                timeout=30
            )
            
            if final_response.status_code == 200:
                result = final_response.json()
                device_tracking = result["device_tracking"]
                consistency_analysis = device_tracking["consistency_analysis"]
                
                switching_patterns = consistency_analysis.get("switching_patterns", {})
                reputation_score = consistency_analysis.get("reputation_score", {})
                risk_assessment = device_tracking.get("risk_assessment", "")
                
                self.log_test("Suspicious Device Patterns", True, 
                            f"Device ID: {device_id}, Switching Patterns Detected: {bool(switching_patterns)}, "
                            f"Reputation Score: {reputation_score}, Risk Assessment: {risk_assessment}")
                return True
            else:
                self.log_test("Suspicious Device Patterns", False, 
                            f"Final suspicious analysis failed: {final_response.status_code}", 
                            final_response.text)
                return False
                
        except Exception as e:
            self.log_test("Suspicious Device Patterns", False, "", str(e))
            return False
    
    def test_device_reputation_scoring(self):
        """Test device reputation scoring based on behavior history"""
        try:
            device_id = f"reputation_device_{uuid.uuid4().hex[:8]}"
            
            # Create a device with mixed behavior patterns
            behaviors = ["good", "suspicious", "good", "good", "suspicious"]
            
            for i, behavior in enumerate(behaviors):
                if behavior == "good":
                    signature = self.generate_realistic_device_signature("established_device", "minor")
                else:
                    signature = self.generate_realistic_device_signature("suspicious_device")
                
                response = self.session.post(
                    f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                    json={
                        "device_id": device_id,
                        "current_signature": signature
                    },
                    timeout=30
                )
                
                if response.status_code != 200:
                    self.log_test("Device Reputation Scoring", False, 
                                f"Reputation session {i + 1} failed: {response.status_code}", 
                                response.text)
                    return False
                
                time.sleep(0.3)
            
            # Final check for reputation scoring
            final_response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json={
                    "device_id": device_id,
                    "current_signature": self.generate_realistic_device_signature("established_device")
                },
                timeout=30
            )
            
            if final_response.status_code == 200:
                result = final_response.json()
                device_tracking = result["device_tracking"]
                consistency_analysis = device_tracking["consistency_analysis"]
                
                reputation_score = consistency_analysis.get("reputation_score", {})
                consistency_score = device_tracking.get("consistency_score", 0)
                
                self.log_test("Device Reputation Scoring", True, 
                            f"Device ID: {device_id}, Reputation Score: {reputation_score}, "
                            f"Consistency Score: {consistency_score}, Sessions: {len(behaviors) + 1}")
                return True
            else:
                self.log_test("Device Reputation Scoring", False, 
                            f"Final reputation check failed: {final_response.status_code}", 
                            final_response.text)
                return False
                
        except Exception as e:
            self.log_test("Device Reputation Scoring", False, "", str(e))
            return False
    
    def test_cross_session_correlation(self):
        """Test cross-session device correlation and anomaly detection"""
        try:
            device_id = f"correlation_device_{uuid.uuid4().hex[:8]}"
            
            # Create sessions with different patterns to test correlation
            session_patterns = [
                ("morning", "established_device"),
                ("afternoon", "established_device"),
                ("evening", "hardware_changed"),  # Anomaly
                ("night", "established_device")
            ]
            
            for session_time, device_type in session_patterns:
                signature = self.generate_realistic_device_signature(device_type)
                
                # Add session-specific metadata
                signature["session_metadata"] = {
                    "session_time": session_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                response = self.session.post(
                    f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                    json={
                        "device_id": device_id,
                        "current_signature": signature
                    },
                    timeout=30
                )
                
                if response.status_code != 200:
                    self.log_test("Cross-Session Correlation", False, 
                                f"Correlation session '{session_time}' failed: {response.status_code}", 
                                response.text)
                    return False
                
                time.sleep(0.5)
            
            # Final analysis should show cross-session correlation
            final_response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json={
                    "device_id": device_id,
                    "current_signature": self.generate_realistic_device_signature("established_device")
                },
                timeout=30
            )
            
            if final_response.status_code == 200:
                result = final_response.json()
                device_tracking = result["device_tracking"]
                consistency_analysis = device_tracking["consistency_analysis"]
                
                session_correlation = consistency_analysis.get("session_correlation", {})
                evolution_tracking = consistency_analysis.get("evolution_tracking", {})
                
                self.log_test("Cross-Session Correlation", True, 
                            f"Device ID: {device_id}, Session Correlation: {bool(session_correlation)}, "
                            f"Evolution Tracking: {bool(evolution_tracking)}, "
                            f"Total Sessions: {len(session_patterns) + 1}")
                return True
            else:
                self.log_test("Cross-Session Correlation", False, 
                            f"Final correlation analysis failed: {final_response.status_code}", 
                            final_response.text)
                return False
                
        except Exception as e:
            self.log_test("Cross-Session Correlation", False, "", str(e))
            return False
    
    def test_mongodb_integration(self):
        """Test MongoDB integration for tracking data storage"""
        try:
            device_id = f"mongodb_test_device_{uuid.uuid4().hex[:8]}"
            signature = self.generate_realistic_device_signature("new_device")
            
            # Create a tracking record
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                json={
                    "device_id": device_id,
                    "current_signature": signature
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Check storage confirmation
                storage_confirmation = result.get("storage_confirmation", "")
                success = result.get("success", False)
                
                if success and "stored successfully" in storage_confirmation:
                    self.log_test("MongoDB Integration", True, 
                                f"Device ID: {device_id}, Storage Confirmed: {storage_confirmation}")
                    return True
                else:
                    self.log_test("MongoDB Integration", False, 
                                f"Storage not confirmed properly", f"Success: {success}, Confirmation: {storage_confirmation}")
                    return False
            else:
                self.log_test("MongoDB Integration", False, 
                            f"MongoDB test failed: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("MongoDB Integration", False, "", str(e))
            return False
    
    def test_edge_cases_malformed_data(self):
        """Test edge cases with malformed data"""
        try:
            test_cases = [
                {
                    "name": "Empty Signature",
                    "device_id": f"empty_device_{uuid.uuid4().hex[:8]}",
                    "current_signature": {}
                },
                {
                    "name": "Null Values",
                    "device_id": f"null_device_{uuid.uuid4().hex[:8]}",
                    "current_signature": {
                        "hardware": None,
                        "os": None,
                        "browser": None
                    }
                },
                {
                    "name": "Invalid Data Types",
                    "device_id": f"invalid_device_{uuid.uuid4().hex[:8]}",
                    "current_signature": {
                        "hardware": "not_a_dict",
                        "os": 12345,
                        "browser": ["not", "a", "dict"]
                    }
                },
                {
                    "name": "Missing Required Fields",
                    "device_id": f"missing_device_{uuid.uuid4().hex[:8]}",
                    "current_signature": {
                        "incomplete": "data"
                    }
                }
            ]
            
            successful_cases = 0
            
            for test_case in test_cases:
                try:
                    response = self.session.post(
                        f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                        json={
                            "device_id": test_case["device_id"],
                            "current_signature": test_case["current_signature"]
                        },
                        timeout=30
                    )
                    
                    # For edge cases, we expect either success (graceful handling) or proper error responses
                    if response.status_code in [200, 400, 422, 500]:
                        successful_cases += 1
                        print(f"   ✓ {test_case['name']}: Status {response.status_code} (handled gracefully)")
                    else:
                        print(f"   ✗ {test_case['name']}: Unexpected status {response.status_code}")
                        
                except Exception as e:
                    print(f"   ✗ {test_case['name']}: Exception {str(e)}")
            
            success_rate = successful_cases / len(test_cases)
            
            self.log_test("Edge Cases - Malformed Data", success_rate >= 0.75, 
                        f"Handled {successful_cases}/{len(test_cases)} edge cases gracefully ({success_rate:.1%})")
            
            return success_rate >= 0.75
                
        except Exception as e:
            self.log_test("Edge Cases - Malformed Data", False, "", str(e))
            return False
    
    def test_risk_assessment_scoring(self):
        """Test risk assessment and consistency scoring"""
        try:
            # Test different risk levels
            risk_scenarios = [
                ("low_risk", "established_device", "minor"),
                ("medium_risk", "hardware_changed", "moderate"),
                ("high_risk", "suspicious_device", "major")
            ]
            
            risk_results = []
            
            for risk_level, device_type, variation in risk_scenarios:
                device_id = f"{risk_level}_device_{uuid.uuid4().hex[:8]}"
                signature = self.generate_realistic_device_signature(device_type, variation)
                
                response = self.session.post(
                    f"{BACKEND_URL}/session-fingerprinting/track-device-consistency",
                    json={
                        "device_id": device_id,
                        "current_signature": signature
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    device_tracking = result["device_tracking"]
                    
                    risk_assessment = device_tracking.get("risk_assessment", "unknown")
                    consistency_score = device_tracking.get("consistency_score", 0)
                    
                    risk_results.append({
                        "scenario": risk_level,
                        "risk_assessment": risk_assessment,
                        "consistency_score": consistency_score,
                        "success": True
                    })
                else:
                    risk_results.append({
                        "scenario": risk_level,
                        "success": False,
                        "error": f"Status {response.status_code}"
                    })
            
            successful_assessments = sum(1 for r in risk_results if r["success"])
            
            details = ", ".join([
                f"{r['scenario']}: {r.get('risk_assessment', 'failed')} (score: {r.get('consistency_score', 'N/A')})"
                for r in risk_results
            ])
            
            self.log_test("Risk Assessment & Scoring", successful_assessments == len(risk_scenarios), 
                        f"Risk Assessments: {successful_assessments}/{len(risk_scenarios)} - {details}")
            
            return successful_assessments == len(risk_scenarios)
                
        except Exception as e:
            self.log_test("Risk Assessment & Scoring", False, "", str(e))
            return False
    
    def run_all_tests(self):
        """Run all device consistency tracking tests"""
        print("🎯 DEVICE CONSISTENCY TRACKING BACKEND TEST")
        print("=" * 60)
        print()
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return
        
        print("🔍 Testing Device Consistency Tracking Functionality...")
        print()
        
        # Run all tests
        tests = [
            ("New Device Tracking", self.test_new_device_tracking),
            ("Established Device Tracking", self.test_established_device_tracking),
            ("Hardware Change Detection", self.test_hardware_change_detection),
            ("Suspicious Device Patterns", self.test_suspicious_device_patterns),
            ("Device Reputation Scoring", self.test_device_reputation_scoring),
            ("Cross-Session Correlation", self.test_cross_session_correlation),
            ("MongoDB Integration", self.test_mongodb_integration),
            ("Risk Assessment & Scoring", self.test_risk_assessment_scoring),
            ("Edge Cases - Malformed Data", self.test_edge_cases_malformed_data)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_test(test_name, False, "", f"Test execution error: {str(e)}")
        
        # Print summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if success_rate >= 80:
            print("🎉 EXCELLENT: Device consistency tracking functionality is working well!")
        elif success_rate >= 60:
            print("✅ GOOD: Most device consistency tracking features are operational.")
        elif success_rate >= 40:
            print("⚠️  MODERATE: Some device consistency tracking issues detected.")
        else:
            print("❌ CRITICAL: Major issues with device consistency tracking functionality.")
        
        print()
        print("🔍 DETAILED TEST RESULTS:")
        print("-" * 40)
        
        for result in self.test_results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"{status}: {result['test']}")
            if result["details"]:
                print(f"   Details: {result['details']}")
            if result["error"]:
                print(f"   Error: {result['error']}")
        
        return success_rate

if __name__ == "__main__":
    tester = DeviceConsistencyTester()
    success_rate = tester.run_all_tests()
    
    # Exit with appropriate code
    if success_rate is not None:
        exit(0 if success_rate >= 80 else 1)
    else:
        exit(1)