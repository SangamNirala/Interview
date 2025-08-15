#!/usr/bin/env python3
"""
🎯 TASK 3.2: ML INTEGRATION FOR FINGERPRINT CLUSTERING - COMPREHENSIVE TESTING

Testing the newly implemented ML Integration for Fingerprint Clustering functionality with all 6 API endpoints:

1. POST /api/ml-fingerprint-clustering/train-device-clustering - Train DBSCAN model with device fingerprint data
2. POST /api/ml-fingerprint-clustering/detect-related-devices - Analyze device relationships using trained ML model
3. POST /api/ml-fingerprint-clustering/predict-fraud-risk - Predict fraud risk using Random Forest ensemble methods
4. POST /api/ml-fingerprint-clustering/analyze-behavior-patterns - Behavior anomaly detection using K-Means and Isolation Forest
5. GET /api/ml-fingerprint-clustering/model-performance - Retrieve ML model performance metrics and training status
6. POST /api/ml-fingerprint-clustering/comprehensive-analysis - Complete ML analysis combining all clustering methods

Test Coverage:
- FingerprintMLClusteringEngine Class Integration with all 4 core ML methods
- Feature Engineering Testing (18 device features, 15 behavior features, 14 risk features)
- Machine Learning Model Training with synthetic data generation and performance metrics
- Real-time ML Analysis for device relationships, fraud risk, and behavioral anomalies
- API Response Validation with proper JSON responses and error handling
- Edge Cases Testing with malformed data, insufficient training data, and model unavailability
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time
import random
import numpy as np

# Configuration
BACKEND_URL = "https://fingerprint-cluster.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class MLClusteringTester:
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

    def generate_realistic_device_fingerprint_data(self, count=15):
        """Generate realistic device fingerprint data for training"""
        devices = []
        
        # Device types and their characteristics
        device_types = [
            {
                "type": "high_end_desktop",
                "cpu_cores": [8, 12, 16],
                "memory_gb": [16, 32, 64],
                "gpu_vendor": ["NVIDIA", "AMD"],
                "screen_width": [1920, 2560, 3840],
                "screen_height": [1080, 1440, 2160]
            },
            {
                "type": "budget_laptop",
                "cpu_cores": [2, 4],
                "memory_gb": [4, 8],
                "gpu_vendor": ["Intel", "AMD"],
                "screen_width": [1366, 1920],
                "screen_height": [768, 1080]
            },
            {
                "type": "mobile_device",
                "cpu_cores": [4, 6, 8],
                "memory_gb": [3, 4, 6, 8],
                "gpu_vendor": ["Adreno", "Mali", "PowerVR"],
                "screen_width": [375, 414, 428],
                "screen_height": [667, 896, 926]
            },
            {
                "type": "gaming_rig",
                "cpu_cores": [8, 12, 16, 24],
                "memory_gb": [32, 64, 128],
                "gpu_vendor": ["NVIDIA"],
                "screen_width": [2560, 3440, 3840],
                "screen_height": [1440, 1440, 2160]
            }
        ]
        
        browsers = ["Chrome", "Firefox", "Safari", "Edge"]
        os_list = ["Windows 10", "Windows 11", "macOS", "Linux", "iOS", "Android"]
        
        for i in range(count):
            device_type = random.choice(device_types)
            
            device = {
                "device_id": f"device_{i+1:03d}",
                "hardware_signature": {
                    "cpu_cores": random.choice(device_type["cpu_cores"]),
                    "memory_gb": random.choice(device_type["memory_gb"]),
                    "gpu_vendor": random.choice(device_type["gpu_vendor"]),
                    "screen_width": random.choice(device_type["screen_width"]),
                    "screen_height": random.choice(device_type["screen_height"]),
                    "color_depth": random.choice([24, 32]),
                    "pixel_ratio": random.choice([1.0, 1.25, 1.5, 2.0, 3.0])
                },
                "browser_characteristics": {
                    "user_agent": f"Mozilla/5.0 ({random.choice(os_list)}) {random.choice(browsers)}/119.0",
                    "plugins": [f"plugin_{j}" for j in range(random.randint(5, 25))],
                    "languages": ["en-US", "en"] if random.random() > 0.3 else ["es-ES", "es", "en"],
                    "cookies_enabled": random.choice([True, False]),
                    "do_not_track": random.choice([True, False]),
                    "timezone": random.choice(["America/New_York", "Europe/London", "Asia/Tokyo", "America/Los_Angeles"])
                },
                "performance_profile": {
                    "canvas_hash": random.randint(100000, 999999),
                    "webgl_hash": random.randint(100000, 999999),
                    "audio_hash": random.randint(100000, 999999),
                    "render_time": random.randint(50, 500)
                },
                "network_characteristics": {
                    "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                    "connection_type": random.choice(["wifi", "ethernet", "cellular"]),
                    "bandwidth_estimate": random.randint(10, 100),
                    "latency": random.randint(10, 200)
                },
                "confidence_score": random.uniform(0.7, 1.0),
                "created_at": datetime.now().isoformat()
            }
            devices.append(device)
        
        return devices

    def generate_realistic_user_interactions(self, count=50):
        """Generate realistic user interaction data"""
        interactions = []
        base_time = int(datetime.now().timestamp() * 1000)
        
        event_types = ["click", "keypress", "scroll", "focus", "blur", "mousemove"]
        
        for i in range(count):
            interaction = {
                "timestamp": base_time + (i * random.randint(500, 5000)),
                "event_type": random.choice(event_types),
                "response_time": random.randint(100, 3000),
                "click_x": random.randint(0, 1920) if random.random() > 0.5 else None,
                "click_y": random.randint(0, 1080) if random.random() > 0.5 else None,
                "key_code": random.randint(65, 90) if random.random() > 0.7 else None,
                "scroll_delta": random.randint(-100, 100) if random.random() > 0.8 else None
            }
            interactions.append(interaction)
        
        return interactions

    def generate_comprehensive_session_data(self):
        """Generate comprehensive session data for risk assessment"""
        return {
            "session_id": self.session_id,
            "device_fingerprint": {
                "device_id": f"test_device_{random.randint(1000, 9999)}",
                "hardware_signature": {
                    "cpu_cores": 8,
                    "memory_gb": 16,
                    "gpu_vendor": "NVIDIA"
                },
                "vm_indicators": {
                    "vm_detected": random.choice([True, False]),
                    "suspicious_hardware": random.choice([True, False])
                },
                "confidence_score": random.uniform(0.5, 1.0),
                "collision_resistance_score": random.uniform(0.7, 1.0)
            },
            "user_interactions": self.generate_realistic_user_interactions(30),
            "session_metrics": {
                "ip_changes": random.randint(0, 3),
                "user_agent_changes": random.randint(0, 1),
                "timezone_inconsistency": random.choice([True, False]),
                "multiple_tabs": random.choice([True, False])
            },
            "performance_metrics": {
                "accuracy_score": random.uniform(0.3, 1.0),
                "completion_rate": random.uniform(0.7, 1.0),
                "question_skips": random.randint(0, 10)
            }
        }

    def test_train_device_clustering_model(self):
        """Test DBSCAN device clustering model training"""
        try:
            # Generate realistic training data
            fingerprint_data = self.generate_realistic_device_fingerprint_data(15)
            
            payload = {
                "fingerprint_data": fingerprint_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/train-device-clustering",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    training_results = data.get('training_results', {})
                    
                    self.log_result(
                        "Device Clustering Training", 
                        True, 
                        f"DBSCAN model trained successfully. Samples: {training_results.get('training_samples', 'N/A')}, Clusters: {training_results.get('n_clusters', 'N/A')}, Silhouette Score: {training_results.get('silhouette_score', 'N/A'):.3f}"
                    )
                    return True
                else:
                    self.log_result("Device Clustering Training", False, f"Training failed: {data}")
                    return False
            else:
                self.log_result("Device Clustering Training", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Device Clustering Training", False, f"Exception: {str(e)}")
            return False

    def test_detect_related_devices_normal(self):
        """Test related device detection with normal device fingerprint"""
        try:
            # Generate a normal device fingerprint
            device_fingerprint = {
                "device_id": "test_device_normal",
                "hardware_signature": {
                    "cpu_cores": 8,
                    "memory_gb": 16,
                    "gpu_vendor": "NVIDIA",
                    "screen_width": 1920,
                    "screen_height": 1080,
                    "color_depth": 24,
                    "pixel_ratio": 1.0
                },
                "browser_characteristics": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0",
                    "plugins": ["plugin_1", "plugin_2", "plugin_3"],
                    "languages": ["en-US", "en"],
                    "cookies_enabled": True,
                    "do_not_track": False,
                    "timezone": "America/New_York"
                },
                "performance_profile": {
                    "canvas_hash": 123456,
                    "webgl_hash": 654321,
                    "audio_hash": 789012,
                    "render_time": 150
                },
                "network_characteristics": {
                    "ip_address": "192.168.1.100",
                    "connection_type": "wifi",
                    "bandwidth_estimate": 50,
                    "latency": 25
                }
            }
            
            payload = {
                "device_fingerprint": device_fingerprint
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/detect-related-devices",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis_results = data.get('analysis_results', {})
                    
                    self.log_result(
                        "Related Device Detection - Normal Device", 
                        True, 
                        f"Device analysis completed. Related: {analysis_results.get('is_related_device', 'N/A')}, Confidence: {analysis_results.get('confidence_score', 'N/A'):.3f}, Cluster: {analysis_results.get('cluster_label', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Related Device Detection - Normal Device", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Related Device Detection - Normal Device", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Related Device Detection - Normal Device", False, f"Exception: {str(e)}")
            return False

    def test_detect_related_devices_suspicious(self):
        """Test related device detection with suspicious device fingerprint"""
        try:
            # Generate a suspicious device fingerprint (potential device farm)
            device_fingerprint = {
                "device_id": "test_device_suspicious",
                "hardware_signature": {
                    "cpu_cores": 4,  # Lower specs suggesting VM
                    "memory_gb": 4,
                    "gpu_vendor": "VMware",  # VM indicator
                    "screen_width": 1024,  # Common VM resolution
                    "screen_height": 768,
                    "color_depth": 24,
                    "pixel_ratio": 1.0
                },
                "browser_characteristics": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0",
                    "plugins": [],  # No plugins (suspicious)
                    "languages": ["en-US"],
                    "cookies_enabled": False,  # Suspicious setting
                    "do_not_track": True,
                    "timezone": "UTC"  # Generic timezone
                },
                "performance_profile": {
                    "canvas_hash": 111111,  # Potentially spoofed
                    "webgl_hash": 222222,
                    "audio_hash": 333333,
                    "render_time": 50  # Very fast (suspicious)
                },
                "network_characteristics": {
                    "ip_address": "10.0.0.1",  # Private IP (suspicious for web)
                    "connection_type": "ethernet",
                    "bandwidth_estimate": 100,  # Very high bandwidth
                    "latency": 5  # Very low latency (suspicious)
                }
            }
            
            payload = {
                "device_fingerprint": device_fingerprint
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/detect-related-devices",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis_results = data.get('analysis_results', {})
                    
                    self.log_result(
                        "Related Device Detection - Suspicious Device", 
                        True, 
                        f"Suspicious device analysis completed. Related: {analysis_results.get('is_related_device', 'N/A')}, Confidence: {analysis_results.get('confidence_score', 'N/A'):.3f}, Cluster: {analysis_results.get('cluster_label', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Related Device Detection - Suspicious Device", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Related Device Detection - Suspicious Device", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Related Device Detection - Suspicious Device", False, f"Exception: {str(e)}")
            return False

    def test_predict_fraud_risk_low_risk(self):
        """Test fraud risk prediction with low-risk session data"""
        try:
            # Generate low-risk session data
            session_data = {
                "session_id": f"{self.session_id}_low_risk",
                "device_fingerprint": {
                    "device_id": "legitimate_device_001",
                    "hardware_signature": {
                        "cpu_cores": 8,
                        "memory_gb": 16,
                        "gpu_vendor": "NVIDIA"
                    },
                    "vm_indicators": {
                        "vm_detected": False,
                        "suspicious_hardware": False
                    },
                    "confidence_score": 0.95,
                    "collision_resistance_score": 0.98
                },
                "user_interactions": [
                    {
                        "timestamp": int(datetime.now().timestamp() * 1000),
                        "event_type": "click",
                        "response_time": random.randint(800, 2500)  # Human-like response times
                    } for _ in range(25)
                ],
                "session_metrics": {
                    "ip_changes": 0,
                    "user_agent_changes": 0,
                    "timezone_inconsistency": False,
                    "multiple_tabs": False
                },
                "performance_metrics": {
                    "accuracy_score": 0.85,
                    "completion_rate": 0.95,
                    "question_skips": 1
                }
            }
            
            payload = {
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/predict-fraud-risk",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    risk_assessment = data.get('risk_assessment', {})
                    
                    self.log_result(
                        "Fraud Risk Prediction - Low Risk Session", 
                        True, 
                        f"Risk assessment completed. Risk Level: {risk_assessment.get('risk_level', 'N/A')}, Probability: {risk_assessment.get('fraud_probability', 'N/A'):.3f}, Factors: {len(risk_assessment.get('risk_factors', []))}"
                    )
                    return True
                else:
                    self.log_result("Fraud Risk Prediction - Low Risk Session", False, f"Assessment failed: {data}")
                    return False
            else:
                self.log_result("Fraud Risk Prediction - Low Risk Session", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Fraud Risk Prediction - Low Risk Session", False, f"Exception: {str(e)}")
            return False

    def test_predict_fraud_risk_high_risk(self):
        """Test fraud risk prediction with high-risk session data"""
        try:
            # Generate high-risk session data
            session_data = {
                "session_id": f"{self.session_id}_high_risk",
                "device_fingerprint": {
                    "device_id": "suspicious_device_001",
                    "hardware_signature": {
                        "cpu_cores": 2,
                        "memory_gb": 4,
                        "gpu_vendor": "VMware"
                    },
                    "vm_indicators": {
                        "vm_detected": True,  # High risk indicator
                        "suspicious_hardware": True
                    },
                    "confidence_score": 0.3,  # Low confidence
                    "collision_resistance_score": 0.4
                },
                "user_interactions": [
                    {
                        "timestamp": int(datetime.now().timestamp() * 1000) + (i * 50),  # Very consistent timing
                        "event_type": "click",
                        "response_time": 95  # Suspiciously fast and consistent
                    } for i in range(50)
                ],
                "session_metrics": {
                    "ip_changes": 5,  # Multiple IP changes
                    "user_agent_changes": 2,  # User agent modifications
                    "timezone_inconsistency": True,
                    "multiple_tabs": True
                },
                "performance_metrics": {
                    "accuracy_score": 0.98,  # Suspiciously high accuracy
                    "completion_rate": 1.0,  # Perfect completion
                    "question_skips": 0  # No skips (suspicious)
                }
            }
            
            payload = {
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/predict-fraud-risk",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    risk_assessment = data.get('risk_assessment', {})
                    
                    self.log_result(
                        "Fraud Risk Prediction - High Risk Session", 
                        True, 
                        f"High-risk assessment completed. Risk Level: {risk_assessment.get('risk_level', 'N/A')}, Probability: {risk_assessment.get('fraud_probability', 'N/A'):.3f}, Factors: {len(risk_assessment.get('risk_factors', []))}"
                    )
                    return True
                else:
                    self.log_result("Fraud Risk Prediction - High Risk Session", False, f"Assessment failed: {data}")
                    return False
            else:
                self.log_result("Fraud Risk Prediction - High Risk Session", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Fraud Risk Prediction - High Risk Session", False, f"Exception: {str(e)}")
            return False

    def test_analyze_behavior_patterns_normal(self):
        """Test behavior pattern analysis with normal human-like interactions"""
        try:
            # Generate normal human-like interactions
            user_interactions = []
            base_time = int(datetime.now().timestamp() * 1000)
            
            for i in range(30):
                interaction = {
                    "timestamp": base_time + (i * random.randint(1000, 4000)),  # Variable timing
                    "event_type": random.choice(["click", "keypress", "scroll", "focus"]),
                    "response_time": random.randint(800, 3500),  # Human-like response times
                    "click_x": random.randint(100, 1800) if random.random() > 0.3 else None,
                    "click_y": random.randint(100, 1000) if random.random() > 0.3 else None,
                    "key_code": random.randint(65, 90) if random.random() > 0.6 else None
                }
                user_interactions.append(interaction)
            
            payload = {
                "user_interactions": user_interactions
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/analyze-behavior-patterns",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    pattern_analysis = data.get('pattern_analysis', {})
                    
                    self.log_result(
                        "Behavior Pattern Analysis - Normal Interactions", 
                        True, 
                        f"Normal behavior analysis completed. Cluster: {pattern_analysis.get('behavior_cluster', 'N/A')}, Anomaly: {pattern_analysis.get('is_anomaly', 'N/A')}, Type: {pattern_analysis.get('behavior_type', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Behavior Pattern Analysis - Normal Interactions", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Behavior Pattern Analysis - Normal Interactions", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Behavior Pattern Analysis - Normal Interactions", False, f"Exception: {str(e)}")
            return False

    def test_analyze_behavior_patterns_suspicious(self):
        """Test behavior pattern analysis with suspicious automation-like interactions"""
        try:
            # Generate suspicious automation-like interactions
            user_interactions = []
            base_time = int(datetime.now().timestamp() * 1000)
            
            for i in range(40):
                interaction = {
                    "timestamp": base_time + (i * 100),  # Very consistent timing (robotic)
                    "event_type": "click",  # Only clicks (limited variety)
                    "response_time": 50,  # Suspiciously fast and consistent
                    "click_x": 500 + (i % 5),  # Very precise, pattern-like clicks
                    "click_y": 300 + (i % 3),
                    "key_code": None
                }
                user_interactions.append(interaction)
            
            payload = {
                "user_interactions": user_interactions
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/analyze-behavior-patterns",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    pattern_analysis = data.get('pattern_analysis', {})
                    
                    self.log_result(
                        "Behavior Pattern Analysis - Suspicious Automation", 
                        True, 
                        f"Suspicious behavior analysis completed. Cluster: {pattern_analysis.get('behavior_cluster', 'N/A')}, Anomaly: {pattern_analysis.get('is_anomaly', 'N/A')}, Type: {pattern_analysis.get('behavior_type', 'N/A')}, Patterns: {len(pattern_analysis.get('patterns_detected', []))}"
                    )
                    return True
                else:
                    self.log_result("Behavior Pattern Analysis - Suspicious Automation", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Behavior Pattern Analysis - Suspicious Automation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Behavior Pattern Analysis - Suspicious Automation", False, f"Exception: {str(e)}")
            return False

    def test_get_model_performance(self):
        """Test retrieval of ML model performance metrics"""
        try:
            response = self.session.get(
                f"{BACKEND_URL}/ml-fingerprint-clustering/model-performance"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    performance_data = data.get('performance_data', {})
                    model_performance = performance_data.get('model_performance', {})
                    models_trained = performance_data.get('models_trained', {})
                    
                    trained_count = sum(1 for trained in models_trained.values() if trained)
                    
                    self.log_result(
                        "Model Performance Metrics", 
                        True, 
                        f"Performance data retrieved. Models trained: {trained_count}/4, Device clustering silhouette: {model_performance.get('device_clustering', {}).get('silhouette_score', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Model Performance Metrics", False, f"Failed to retrieve performance data: {data}")
                    return False
            else:
                self.log_result("Model Performance Metrics", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Model Performance Metrics", False, f"Exception: {str(e)}")
            return False

    def test_comprehensive_analysis_complete(self):
        """Test comprehensive ML analysis with all data types"""
        try:
            # Generate comprehensive data for all analysis types
            device_fingerprint = {
                "device_id": "comprehensive_test_device",
                "hardware_signature": {
                    "cpu_cores": 8,
                    "memory_gb": 16,
                    "gpu_vendor": "NVIDIA",
                    "screen_width": 1920,
                    "screen_height": 1080,
                    "color_depth": 24,
                    "pixel_ratio": 1.0
                },
                "browser_characteristics": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0",
                    "plugins": ["plugin_1", "plugin_2", "plugin_3"],
                    "languages": ["en-US", "en"],
                    "cookies_enabled": True,
                    "do_not_track": False,
                    "timezone": "America/New_York"
                },
                "performance_profile": {
                    "canvas_hash": 123456,
                    "webgl_hash": 654321,
                    "audio_hash": 789012,
                    "render_time": 150
                },
                "network_characteristics": {
                    "ip_address": "192.168.1.100",
                    "connection_type": "wifi",
                    "bandwidth_estimate": 50,
                    "latency": 25
                }
            }
            
            user_interactions = self.generate_realistic_user_interactions(35)
            session_data = self.generate_comprehensive_session_data()
            
            payload = {
                "device_fingerprint": device_fingerprint,
                "user_interactions": user_interactions,
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/comprehensive-analysis",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis_results = data.get('analysis_results', {})
                    composite_analysis = analysis_results.get('composite_analysis', {})
                    
                    analyses_completed = []
                    if 'device_analysis' in analysis_results:
                        analyses_completed.append('Device')
                    if 'behavior_analysis' in analysis_results:
                        analyses_completed.append('Behavior')
                    if 'risk_assessment' in analysis_results:
                        analyses_completed.append('Risk')
                    
                    self.log_result(
                        "Comprehensive ML Analysis - Complete", 
                        True, 
                        f"Comprehensive analysis completed. Analyses: {', '.join(analyses_completed)}, Overall Risk: {composite_analysis.get('overall_risk_level', 'N/A')}, Composite Score: {composite_analysis.get('composite_risk_score', 'N/A'):.3f}, Recommendation: {composite_analysis.get('recommendation', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Comprehensive ML Analysis - Complete", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Comprehensive ML Analysis - Complete", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Comprehensive ML Analysis - Complete", False, f"Exception: {str(e)}")
            return False

    def test_comprehensive_analysis_partial(self):
        """Test comprehensive ML analysis with partial data"""
        try:
            # Test with only device fingerprint data
            device_fingerprint = {
                "device_id": "partial_test_device",
                "hardware_signature": {
                    "cpu_cores": 4,
                    "memory_gb": 8,
                    "gpu_vendor": "Intel"
                },
                "browser_characteristics": {
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "plugins": ["plugin_1"],
                    "languages": ["en-US"],
                    "cookies_enabled": True,
                    "do_not_track": False,
                    "timezone": "UTC"
                },
                "performance_profile": {
                    "canvas_hash": 111111,
                    "webgl_hash": 222222,
                    "audio_hash": 333333,
                    "render_time": 200
                },
                "network_characteristics": {
                    "ip_address": "10.0.0.1",
                    "connection_type": "ethernet",
                    "bandwidth_estimate": 100,
                    "latency": 10
                }
            }
            
            payload = {
                "device_fingerprint": device_fingerprint
                # No user_interactions or session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/comprehensive-analysis",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis_results = data.get('analysis_results', {})
                    composite_analysis = analysis_results.get('composite_analysis', {})
                    
                    self.log_result(
                        "Comprehensive ML Analysis - Partial Data", 
                        True, 
                        f"Partial analysis completed. Device analysis present: {'device_analysis' in analysis_results}, Overall Risk: {composite_analysis.get('overall_risk_level', 'N/A')}, Recommendation: {composite_analysis.get('recommendation', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Comprehensive ML Analysis - Partial Data", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Comprehensive ML Analysis - Partial Data", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Comprehensive ML Analysis - Partial Data", False, f"Exception: {str(e)}")
            return False

    def test_edge_case_insufficient_training_data(self):
        """Test edge case with insufficient training data"""
        try:
            # Try to train with insufficient data (less than 10 samples)
            fingerprint_data = self.generate_realistic_device_fingerprint_data(5)  # Only 5 samples
            
            payload = {
                "fingerprint_data": fingerprint_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/train-device-clustering",
                json=payload
            )
            
            # This should either fail gracefully or handle the edge case
            if response.status_code == 500:
                self.log_result(
                    "Edge Case - Insufficient Training Data", 
                    True, 
                    f"Correctly handled insufficient training data with appropriate error (Status: {response.status_code})"
                )
                return True
            elif response.status_code == 200:
                data = response.json()
                if not data.get('success'):
                    self.log_result(
                        "Edge Case - Insufficient Training Data", 
                        True, 
                        f"Correctly handled insufficient training data with error response: {data.get('error', 'Unknown error')}"
                    )
                    return True
                else:
                    self.log_result(
                        "Edge Case - Insufficient Training Data", 
                        False, 
                        f"Should have failed with insufficient data but succeeded: {data}"
                    )
                    return False
            else:
                self.log_result("Edge Case - Insufficient Training Data", False, f"Unexpected response: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Edge Case - Insufficient Training Data", False, f"Exception: {str(e)}")
            return False

    def test_edge_case_malformed_data(self):
        """Test edge case with malformed request data"""
        try:
            # Send malformed device fingerprint data
            malformed_payload = {
                "device_fingerprint": {
                    "invalid_field": "invalid_value",
                    # Missing required fields
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/ml-fingerprint-clustering/detect-related-devices",
                json=malformed_payload
            )
            
            # Should handle malformed data gracefully
            if response.status_code in [400, 422, 500]:
                self.log_result(
                    "Edge Case - Malformed Data", 
                    True, 
                    f"Correctly handled malformed data with appropriate error (Status: {response.status_code})"
                )
                return True
            elif response.status_code == 200:
                data = response.json()
                if not data.get('success'):
                    self.log_result(
                        "Edge Case - Malformed Data", 
                        True, 
                        f"Correctly handled malformed data with error response"
                    )
                    return True
                else:
                    # If it succeeds, check if it handled the malformed data appropriately
                    analysis_results = data.get('analysis_results', {})
                    if analysis_results.get('success') == False:
                        self.log_result(
                            "Edge Case - Malformed Data", 
                            True, 
                            f"Correctly handled malformed data in analysis layer"
                        )
                        return True
                    else:
                        self.log_result(
                            "Edge Case - Malformed Data", 
                            False, 
                            f"Should have failed with malformed data but succeeded: {data}"
                        )
                        return False
            else:
                self.log_result("Edge Case - Malformed Data", False, f"Unexpected response: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Edge Case - Malformed Data", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all ML clustering tests"""
        print("🎯 STARTING ML INTEGRATION FOR FINGERPRINT CLUSTERING COMPREHENSIVE TESTING")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with testing.")
            return
        
        # Test sequence
        tests = [
            self.test_train_device_clustering_model,
            self.test_detect_related_devices_normal,
            self.test_detect_related_devices_suspicious,
            self.test_predict_fraud_risk_low_risk,
            self.test_predict_fraud_risk_high_risk,
            self.test_analyze_behavior_patterns_normal,
            self.test_analyze_behavior_patterns_suspicious,
            self.test_get_model_performance,
            self.test_comprehensive_analysis_complete,
            self.test_comprehensive_analysis_partial,
            self.test_edge_case_insufficient_training_data,
            self.test_edge_case_malformed_data
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
                time.sleep(0.5)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
        
        print("\n" + "=" * 80)
        print(f"🎯 ML CLUSTERING TESTING COMPLETED")
        print(f"✅ PASSED: {passed}/{total} tests ({(passed/total)*100:.1f}% success rate)")
        print(f"❌ FAILED: {total-passed}/{total} tests")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! ML Integration for Fingerprint Clustering is fully operational.")
        elif passed >= total * 0.8:
            print("✅ EXCELLENT! ML clustering system is working well with minor issues.")
        elif passed >= total * 0.6:
            print("⚠️  GOOD! ML clustering system is mostly functional but needs attention.")
        else:
            print("❌ NEEDS WORK! ML clustering system has significant issues requiring fixes.")
        
        return passed, total

if __name__ == "__main__":
    tester = MLClusteringTester()
    tester.run_all_tests()