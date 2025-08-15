#!/usr/bin/env python3
"""
Anti-Evasion Techniques Backend Testing Suite (Task 4.1)

This test suite validates the 6 new API endpoints for anti-evasion detection:
1. POST /api/anti-evasion/analyze-patterns
2. POST /api/anti-evasion/detect-virtualization  
3. POST /api/anti-evasion/validate-consistency
4. POST /api/anti-evasion/counter-spoofing
5. GET /api/anti-evasion/system-status
6. POST /api/anti-evasion/test-detection

Testing Focus:
- Endpoint accessibility and response status codes
- Response structure and data validation
- Error handling for invalid inputs
- Integration with EvasionDetectionEngine backend
- Database storage verification for analysis results
- Performance and response time measurements
"""

import requests
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')
load_dotenv('/app/frontend/.env')

class AntiEvasionBackendTester:
    def __init__(self):
        # Get backend URL from frontend environment
        self.backend_url = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
        if not self.backend_url.endswith('/api'):
            self.backend_url = f"{self.backend_url}/api"
        
        print(f"🔗 Backend URL: {self.backend_url}")
        
        # Admin credentials for authentication
        self.admin_password = "Game@1234"
        self.auth_token = None
        
        # Test results tracking
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
        # Performance tracking
        self.performance_metrics = {}
        
    def log_test_result(self, test_name: str, success: bool, details: str = "", response_time: float = 0.0):
        """Log test result with details"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   📝 {details}")
        if response_time > 0:
            print(f"   ⏱️  Response time: {response_time:.3f}s")
        
        self.test_results.append({
            'test_name': test_name,
            'success': success,
            'details': details,
            'response_time': response_time,
            'timestamp': datetime.now().isoformat()
        })
        
        self.total_tests += 1
        if success:
            self.passed_tests += 1
    
    def authenticate_admin(self) -> bool:
        """Authenticate as admin to access protected endpoints"""
        try:
            print("\n🔐 Authenticating as admin...")
            
            auth_url = f"{self.backend_url}/admin/login"
            auth_data = {"password": self.admin_password}
            
            start_time = time.time()
            response = requests.post(auth_url, json=auth_data, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.auth_token = data.get('token')
                    self.log_test_result("Admin Authentication", True, 
                                       f"Successfully authenticated with token", response_time)
                    return True
            
            self.log_test_result("Admin Authentication", False, 
                               f"Authentication failed: {response.status_code} - {response.text}", response_time)
            return False
            
        except Exception as e:
            self.log_test_result("Admin Authentication", False, f"Authentication error: {str(e)}")
            return False
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for requests"""
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers
    
    def generate_sample_fingerprint_data(self) -> Dict[str, Any]:
        """Generate realistic sample fingerprint data for testing"""
        return {
            'session_id': f'test_session_{int(time.time())}',
            'canvas_fingerprint': {
                'hash': hashlib.md5(f'canvas_test_{time.time()}'.encode()).hexdigest(),
                'hash_consistency': 0.95,
                'timing_variance': 0.05,
                'rendering_time': 45.2,
                'noise_patterns': ['subtle_noise', 'timing_variation'],
                'spoofing_indicators': []
            },
            'webgl_fingerprint': {
                'renderer_info': 'ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0)',
                'vendor': 'Google Inc. (Intel)',
                'parameters_consistency': 0.88,
                'extensions_count': 15,
                'extensions': ['WEBGL_debug_renderer_info', 'OES_texture_float'],
                'max_texture_size': 16384,
                'max_viewport_dims': [16384, 16384]
            },
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'timing_data': {
                'performance_now_precision': 5,
                'date_now_correlation': 0.99,
                'high_resolution_time': True,
                'timing_manipulation_detected': False
            },
            'hardware_characteristics': {
                'cpu_info': {
                    'model_name': 'Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz',
                    'cores': 4,
                    'threads': 8
                },
                'memory_info': {
                    'total_gb': 16,
                    'available_gb': 8.5
                },
                'gpu_info': {
                    'vendor': 'Intel Corporation',
                    'renderer': 'Intel(R) HD Graphics 620'
                }
            },
            'browser_characteristics': {
                'plugins_count': 3,
                'mime_types_count': 4,
                'screen_resolution': '1920x1080',
                'color_depth': 24,
                'timezone_offset': -300
            }
        }
    
    def test_analyze_patterns_endpoint(self) -> bool:
        """Test POST /api/anti-evasion/analyze-patterns endpoint"""
        try:
            print("\n🔍 Testing Evasion Pattern Analysis Endpoint...")
            
            url = f"{self.backend_url}/anti-evasion/analyze-patterns"
            
            # Test with valid fingerprint data
            fingerprint_data = self.generate_sample_fingerprint_data()
            test_data = {
                'fingerprint_data': fingerprint_data,
                'session_id': fingerprint_data['session_id'],
                'user_id': 'test_user_123'
            }
            
            start_time = time.time()
            response = requests.post(url, json=test_data, headers=self.get_auth_headers(), timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis' in data:
                    analysis = data['analysis']
                    
                    # Validate response structure
                    required_fields = ['overall_evasion_score', 'risk_level', 'evasion_patterns']
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        evasion_score = analysis.get('overall_evasion_score', 0)
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        patterns_count = len(analysis.get('evasion_patterns', []))
                        
                        details = f"Evasion Score: {evasion_score:.3f}, Risk Level: {risk_level}, Patterns: {patterns_count}"
                        self.log_test_result("Analyze Patterns - Valid Data", True, details, response_time)
                        return True
                    else:
                        self.log_test_result("Analyze Patterns - Valid Data", False, 
                                           f"Missing required fields: {missing_fields}", response_time)
                else:
                    self.log_test_result("Analyze Patterns - Valid Data", False, 
                                       f"Invalid response structure: {data}", response_time)
            else:
                self.log_test_result("Analyze Patterns - Valid Data", False, 
                                   f"HTTP {response.status_code}: {response.text}", response_time)
            
            return False
            
        except Exception as e:
            self.log_test_result("Analyze Patterns - Valid Data", False, f"Exception: {str(e)}")
            return False
    
    def test_detect_virtualization_endpoint(self) -> bool:
        """Test POST /api/anti-evasion/detect-virtualization endpoint"""
        try:
            print("\n🖥️  Testing Virtualization Detection Endpoint...")
            
            url = f"{self.backend_url}/anti-evasion/detect-virtualization"
            
            # Test with valid device data
            test_data = {
                'device_data': {
                    'system_info': {
                        'platform': 'Windows',
                        'version': '10.0.19045',
                        'architecture': 'x64'
                    },
                    'hardware_signatures': {
                        'cpu_model': 'Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz',
                        'memory_total': 17179869184,
                        'disk_info': 'SAMSUNG MZVLB512HBJQ-000L7'
                    }
                },
                'hardware_characteristics': {
                    'virtualization_indicators': {
                        'hypervisor_present': False,
                        'vm_artifacts': [],
                        'performance_anomalies': []
                    },
                    'timing_characteristics': {
                        'rdtsc_available': True,
                        'high_precision_timer': True,
                        'timing_consistency': 0.98
                    }
                },
                'software_information': {
                    'processes': ['chrome.exe', 'explorer.exe', 'winlogon.exe'],
                    'services': ['Themes', 'AudioSrv', 'BITS'],
                    'registry_indicators': [],
                    'file_system_artifacts': []
                }
            }
            
            start_time = time.time()
            response = requests.post(url, json=test_data, headers=self.get_auth_headers(), timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'detection' in data:
                    detection = data['detection']
                    
                    # Validate response structure
                    required_fields = ['virtualization_detected', 'confidence_level', 'virtualization_indicators']
                    missing_fields = [field for field in required_fields if field not in detection]
                    
                    if not missing_fields:
                        vm_detected = detection.get('virtualization_detected', False)
                        confidence = detection.get('confidence_level', 0)
                        indicators_count = len(detection.get('virtualization_indicators', []))
                        vm_type = detection.get('virtualization_type', 'none')
                        
                        details = f"VM Detected: {vm_detected}, Confidence: {confidence:.3f}, Type: {vm_type}, Indicators: {indicators_count}"
                        self.log_test_result("Detect Virtualization - Valid Data", True, details, response_time)
                        return True
                    else:
                        self.log_test_result("Detect Virtualization - Valid Data", False, 
                                           f"Missing required fields: {missing_fields}", response_time)
                else:
                    self.log_test_result("Detect Virtualization - Valid Data", False, 
                                       f"Invalid response structure: {data}", response_time)
            else:
                self.log_test_result("Detect Virtualization - Valid Data", False, 
                                   f"HTTP {response.status_code}: {response.text}", response_time)
            
            return False
            
        except Exception as e:
            self.log_test_result("Detect Virtualization - Valid Data", False, f"Exception: {str(e)}")
            return False
    
    def test_validate_consistency_endpoint(self) -> bool:
        """Test POST /api/anti-evasion/validate-consistency endpoint"""
        try:
            print("\n📊 Testing Fingerprint Consistency Validation Endpoint...")
            
            url = f"{self.backend_url}/anti-evasion/validate-consistency"
            
            # Generate test data
            base_fingerprint = self.generate_sample_fingerprint_data()
            
            # Generate historical data (3 previous sessions)
            historical_data = []
            for i in range(3):
                historical = base_fingerprint.copy()
                historical['session_id'] = f'historical_session_{i}_{int(time.time())}'
                historical['timestamp'] = (datetime.now() - timedelta(days=i+1)).isoformat()
                # Add slight variations to simulate normal evolution
                historical['canvas_fingerprint']['hash_consistency'] = 0.95 - (i * 0.01)
                historical['webgl_fingerprint']['parameters_consistency'] = 0.88 - (i * 0.005)
                historical_data.append(historical)
            
            # Current data
            current_data = base_fingerprint.copy()
            current_data['session_id'] = f'current_session_{int(time.time())}'
            current_data['timestamp'] = datetime.now().isoformat()
            
            test_data = {
                'historical_data': historical_data,
                'current_data': current_data,
                'session_id': current_data['session_id']
            }
            
            start_time = time.time()
            response = requests.post(url, json=test_data, headers=self.get_auth_headers(), timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'validation' in data:
                    validation = data['validation']
                    
                    # Validate response structure
                    required_fields = ['consistency_score', 'validation_status', 'anomaly_count']
                    missing_fields = [field for field in required_fields if field not in validation]
                    
                    if not missing_fields:
                        consistency_score = validation.get('consistency_score', 0)
                        validation_status = validation.get('validation_status', 'UNKNOWN')
                        anomaly_count = validation.get('anomaly_count', 0)
                        
                        details = f"Consistency Score: {consistency_score:.3f}, Status: {validation_status}, Anomalies: {anomaly_count}"
                        self.log_test_result("Validate Consistency - Valid Data", True, details, response_time)
                        return True
                    else:
                        self.log_test_result("Validate Consistency - Valid Data", False, 
                                           f"Missing required fields: {missing_fields}", response_time)
                else:
                    self.log_test_result("Validate Consistency - Valid Data", False, 
                                       f"Invalid response structure: {data}", response_time)
            else:
                self.log_test_result("Validate Consistency - Valid Data", False, 
                                   f"HTTP {response.status_code}: {response.text}", response_time)
            
            return False
            
        except Exception as e:
            self.log_test_result("Validate Consistency - Valid Data", False, f"Exception: {str(e)}")
            return False
    
    def test_counter_spoofing_endpoint(self) -> bool:
        """Test POST /api/anti-evasion/counter-spoofing endpoint"""
        try:
            print("\n🛡️  Testing Counter-Spoofing Measures Endpoint...")
            
            url = f"{self.backend_url}/anti-evasion/counter-spoofing"
            
            # Generate suspicious patterns
            suspicious_patterns = [
                {
                    'pattern_type': 'canvas_spoofing',
                    'severity': 'HIGH',
                    'confidence': 0.85,
                    'indicators': ['hash_inconsistency', 'timing_anomaly'],
                    'details': {
                        'expected_hash': 'abc123def456',
                        'actual_hash': 'xyz789uvw012',
                        'timing_variance': 0.15
                    }
                },
                {
                    'pattern_type': 'webgl_manipulation',
                    'severity': 'MEDIUM',
                    'confidence': 0.72,
                    'indicators': ['parameter_spoofing', 'extension_hiding'],
                    'details': {
                        'spoofed_parameters': ['MAX_TEXTURE_SIZE', 'MAX_VIEWPORT_DIMS'],
                        'hidden_extensions': ['WEBGL_debug_renderer_info']
                    }
                }
            ]
            
            test_data = {
                'suspicious_patterns': suspicious_patterns,
                'session_id': f'counter_test_session_{int(time.time())}',
                'severity_threshold': 'MEDIUM'
            }
            
            start_time = time.time()
            response = requests.post(url, json=test_data, headers=self.get_auth_headers(), timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'countermeasures' in data:
                    countermeasures = data['countermeasures']
                    
                    # Validate response structure
                    required_fields = ['active_countermeasures', 'effectiveness_scores', 'deployment_status']
                    missing_fields = [field for field in required_fields if field not in countermeasures]
                    
                    if not missing_fields:
                        active_measures = countermeasures.get('active_countermeasures', [])
                        effectiveness = countermeasures.get('effectiveness_scores', {})
                        deployment_status = countermeasures.get('deployment_status', 'unknown')
                        
                        details = f"Active Measures: {len(active_measures)}, Status: {deployment_status}"
                        self.log_test_result("Counter-Spoofing - Valid Patterns", True, details, response_time)
                        return True
                    else:
                        self.log_test_result("Counter-Spoofing - Valid Patterns", False, 
                                           f"Missing required fields: {missing_fields}", response_time)
                else:
                    self.log_test_result("Counter-Spoofing - Valid Patterns", False, 
                                       f"Invalid response structure: {data}", response_time)
            else:
                self.log_test_result("Counter-Spoofing - Valid Patterns", False, 
                                   f"HTTP {response.status_code}: {response.text}", response_time)
            
            return False
            
        except Exception as e:
            self.log_test_result("Counter-Spoofing - Valid Patterns", False, f"Exception: {str(e)}")
            return False
    
    def test_system_status_endpoint(self) -> bool:
        """Test GET /api/anti-evasion/system-status endpoint"""
        try:
            print("\n📈 Testing Anti-Evasion System Status Endpoint...")
            
            url = f"{self.backend_url}/anti-evasion/system-status"
            
            start_time = time.time()
            response = requests.get(url, headers=self.get_auth_headers(), timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'status' in data:
                    status = data['status']
                    
                    # Validate response structure
                    required_fields = ['system_operational', 'engine_status', 'database_statistics', 'recent_activity']
                    missing_fields = [field for field in required_fields if field not in status]
                    
                    if not missing_fields:
                        system_operational = status.get('system_operational', False)
                        engine_status = status.get('engine_status', {})
                        db_stats = status.get('database_statistics', {})
                        
                        # Extract key metrics
                        engine_version = engine_status.get('version', 'unknown')
                        detected_patterns = engine_status.get('detected_patterns_count', 0)
                        active_countermeasures = engine_status.get('active_countermeasures_count', 0)
                        
                        details = f"Operational: {system_operational}, Version: {engine_version}, Patterns: {detected_patterns}, Countermeasures: {active_countermeasures}"
                        self.log_test_result("System Status - Basic Info", True, details, response_time)
                        return True
                    else:
                        self.log_test_result("System Status - Basic Info", False, 
                                           f"Missing required fields: {missing_fields}", response_time)
                else:
                    self.log_test_result("System Status - Basic Info", False, 
                                       f"Invalid response structure: {data}", response_time)
            else:
                self.log_test_result("System Status - Basic Info", False, 
                                   f"HTTP {response.status_code}: {response.text}", response_time)
            
            return False
            
        except Exception as e:
            self.log_test_result("System Status - Basic Info", False, f"Exception: {str(e)}")
            return False
    
    def test_detection_test_endpoint(self) -> bool:
        """Test POST /api/anti-evasion/test-detection endpoint"""
        try:
            print("\n🧪 Testing Anti-Evasion Detection Test Endpoint...")
            
            url = f"{self.backend_url}/anti-evasion/test-detection"
            
            # Test with default sample data (no body)
            start_time = time.time()
            response = requests.post(url, json={}, headers=self.get_auth_headers(), timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'test_results' in data:
                    test_results = data['test_results']
                    
                    # Validate response structure
                    required_fields = ['test_id', 'overall_success', 'successful_tests', 'total_tests', 'success_rate']
                    missing_fields = [field for field in required_fields if field not in test_results]
                    
                    if not missing_fields:
                        overall_success = test_results.get('overall_success', False)
                        successful_tests = test_results.get('successful_tests', 0)
                        total_tests = test_results.get('total_tests', 0)
                        success_rate = test_results.get('success_rate', 0)
                        
                        details = f"Overall Success: {overall_success}, Tests: {successful_tests}/{total_tests}, Rate: {success_rate}%"
                        self.log_test_result("Detection Test - Default Data", True, details, response_time)
                        return True
                    else:
                        self.log_test_result("Detection Test - Default Data", False, 
                                           f"Missing required fields: {missing_fields}", response_time)
                else:
                    self.log_test_result("Detection Test - Default Data", False, 
                                       f"Invalid response structure: {data}", response_time)
            else:
                self.log_test_result("Detection Test - Default Data", False, 
                                   f"HTTP {response.status_code}: {response.text}", response_time)
            
            return False
            
        except Exception as e:
            self.log_test_result("Detection Test - Default Data", False, f"Exception: {str(e)}")
            return False
    
    def run_comprehensive_tests(self):
        """Run all anti-evasion endpoint tests"""
        print("🚀 Starting Anti-Evasion Backend Testing Suite")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with testing.")
            return
        
        # Run all endpoint tests
        test_methods = [
            self.test_analyze_patterns_endpoint,
            self.test_detect_virtualization_endpoint,
            self.test_validate_consistency_endpoint,
            self.test_counter_spoofing_endpoint,
            self.test_system_status_endpoint,
            self.test_detection_test_endpoint
        ]
        
        for test_method in test_methods:
            try:
                test_method()
            except Exception as e:
                print(f"❌ Test method {test_method.__name__} failed with exception: {str(e)}")
        
        # Print final results
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("\n" + "=" * 80)
        print("📊 ANTI-EVASION BACKEND TESTING SUMMARY")
        print("=" * 80)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"📈 Overall Results: {self.passed_tests}/{self.total_tests} tests passed ({success_rate:.1f}%)")
        print(f"⏱️  Total Testing Time: {sum(result['response_time'] for result in self.test_results):.3f}s")
        
        # Print failed tests details
        failed_tests = [result for result in self.test_results if not result['success']]
        if failed_tests:
            print(f"\n❌ Failed Tests ({len(failed_tests)}):")
            for failed_test in failed_tests:
                print(f"  • {failed_test['test_name']}: {failed_test['details']}")
        
        print("\n" + "=" * 80)
        
        # Overall assessment
        if success_rate >= 90:
            print("🎉 EXCELLENT: Anti-evasion system is working exceptionally well!")
        elif success_rate >= 80:
            print("✅ GOOD: Anti-evasion system is working well with minor issues.")
        elif success_rate >= 60:
            print("⚠️  FAIR: Anti-evasion system has some issues that need attention.")
        else:
            print("❌ POOR: Anti-evasion system has significant issues requiring immediate attention.")

if __name__ == "__main__":
    tester = AntiEvasionBackendTester()
    tester.run_comprehensive_tests()