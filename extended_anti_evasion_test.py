#!/usr/bin/env python3
"""
Extended Anti-Evasion Backend Testing Suite
Tests additional functionality including database storage, error handling, and edge cases
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

class ExtendedAntiEvasionTester:
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
    
    def test_error_handling(self) -> bool:
        """Test error handling for invalid inputs"""
        try:
            print("\n🚨 Testing Error Handling...")
            
            # Test analyze-patterns with invalid data
            url = f"{self.backend_url}/anti-evasion/analyze-patterns"
            invalid_data = {"fingerprint_data": "invalid_string_instead_of_dict"}
            
            start_time = time.time()
            response = requests.post(url, json=invalid_data, headers=self.get_auth_headers(), timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code >= 400:
                self.log_test_result("Error Handling - Invalid Fingerprint Data", True, 
                                   f"Properly rejected invalid data: {response.status_code}", response_time)
            else:
                self.log_test_result("Error Handling - Invalid Fingerprint Data", False, 
                                   "Should reject invalid data but didn't", response_time)
            
            # Test detect-virtualization with empty data
            vm_url = f"{self.backend_url}/anti-evasion/detect-virtualization"
            empty_data = {"device_data": {}}
            
            start_time = time.time()
            vm_response = requests.post(vm_url, json=empty_data, headers=self.get_auth_headers(), timeout=10)
            vm_response_time = time.time() - start_time
            
            if vm_response.status_code == 200:
                vm_data = vm_response.json()
                if vm_data.get('success'):
                    self.log_test_result("Error Handling - Empty Device Data", True, 
                                       "Handled empty device data gracefully", vm_response_time)
                else:
                    self.log_test_result("Error Handling - Empty Device Data", False, 
                                       "Failed to handle empty device data", vm_response_time)
            else:
                self.log_test_result("Error Handling - Empty Device Data", False, 
                                   f"Unexpected error: {vm_response.status_code}", vm_response_time)
            
            # Test validate-consistency with missing historical data
            consistency_url = f"{self.backend_url}/anti-evasion/validate-consistency"
            missing_data = {"historical_data": [], "current_data": {"test": "data"}}
            
            start_time = time.time()
            consistency_response = requests.post(consistency_url, json=missing_data, headers=self.get_auth_headers(), timeout=10)
            consistency_response_time = time.time() - start_time
            
            if consistency_response.status_code == 200:
                consistency_data = consistency_response.json()
                if consistency_data.get('success'):
                    self.log_test_result("Error Handling - Missing Historical Data", True, 
                                       "Handled missing historical data gracefully", consistency_response_time)
                else:
                    self.log_test_result("Error Handling - Missing Historical Data", False, 
                                       "Failed to handle missing historical data", consistency_response_time)
            else:
                self.log_test_result("Error Handling - Missing Historical Data", False, 
                                   f"Unexpected error: {consistency_response.status_code}", consistency_response_time)
            
            return True
            
        except Exception as e:
            self.log_test_result("Error Handling - Exception", False, f"Exception: {str(e)}")
            return False
    
    def test_database_storage_verification(self) -> bool:
        """Test database storage and retrieval of analysis results"""
        try:
            print("\n🗄️  Testing Database Storage Verification...")
            
            # First, run multiple analyses to store data
            url = f"{self.backend_url}/anti-evasion/analyze-patterns"
            
            # Store initial system status
            status_url = f"{self.backend_url}/anti-evasion/system-status"
            start_time = time.time()
            initial_response = requests.get(status_url, headers=self.get_auth_headers(), timeout=10)
            initial_response_time = time.time() - start_time
            
            initial_analyses_count = 0
            if initial_response.status_code == 200:
                initial_data = initial_response.json()
                if initial_data.get('success'):
                    db_stats = initial_data['status'].get('database_statistics', {})
                    initial_analyses_count = db_stats.get('evasion_analyses', 0)
            
            # Run 3 analyses to generate database entries
            for i in range(3):
                fingerprint_data = {
                    'session_id': f'db_test_session_{i}_{int(time.time())}',
                    'canvas_fingerprint': {
                        'hash': hashlib.md5(f'canvas_test_{i}_{time.time()}'.encode()).hexdigest(),
                        'hash_consistency': 0.95 - (i * 0.1),
                        'timing_variance': 0.05 + (i * 0.02)
                    },
                    'webgl_fingerprint': {
                        'renderer_info': f'Test Renderer {i}',
                        'parameters_consistency': 0.88 - (i * 0.05)
                    }
                }
                
                test_data = {
                    'fingerprint_data': fingerprint_data,
                    'session_id': fingerprint_data['session_id'],
                    'user_id': f'db_test_user_{i}'
                }
                
                start_time = time.time()
                response = requests.post(url, json=test_data, headers=self.get_auth_headers(), timeout=15)
                response_time = time.time() - start_time
                
                if response.status_code == 200 and response.json().get('success'):
                    self.log_test_result(f"Database Storage - Analysis {i+1}", True, 
                                       f"Analysis stored successfully", response_time)
                else:
                    self.log_test_result(f"Database Storage - Analysis {i+1}", False, 
                                       f"Failed to store analysis: {response.status_code}", response_time)
            
            # Wait a moment for database writes to complete
            time.sleep(1)
            
            # Check if database statistics reflect the new entries
            start_time = time.time()
            final_response = requests.get(status_url, headers=self.get_auth_headers(), timeout=10)
            final_response_time = time.time() - start_time
            
            if final_response.status_code == 200:
                final_data = final_response.json()
                if final_data.get('success'):
                    db_stats = final_data['status'].get('database_statistics', {})
                    final_analyses_count = db_stats.get('evasion_analyses', 0)
                    
                    if final_analyses_count > initial_analyses_count:
                        increase = final_analyses_count - initial_analyses_count
                        self.log_test_result("Database Storage - Verification", True, 
                                           f"Database entries increased by {increase} (from {initial_analyses_count} to {final_analyses_count})", final_response_time)
                        return True
                    else:
                        self.log_test_result("Database Storage - Verification", False, 
                                           f"No increase in database entries: {initial_analyses_count} -> {final_analyses_count}", final_response_time)
                else:
                    self.log_test_result("Database Storage - Verification", False, 
                                       "Failed to get final system status", final_response_time)
            else:
                self.log_test_result("Database Storage - Verification", False, 
                                   f"Status endpoint failed: {final_response.status_code}", final_response_time)
            
            return False
            
        except Exception as e:
            self.log_test_result("Database Storage - Verification", False, f"Exception: {str(e)}")
            return False
    
    def test_performance_under_load(self) -> bool:
        """Test performance under concurrent load"""
        try:
            print("\n⚡ Testing Performance Under Load...")
            
            # Test concurrent requests to different endpoints
            endpoints = [
                ('analyze-patterns', {
                    'fingerprint_data': {
                        'session_id': f'load_test_{int(time.time())}',
                        'canvas_fingerprint': {'hash': 'test_hash', 'hash_consistency': 0.95}
                    },
                    'session_id': f'load_test_{int(time.time())}'
                }),
                ('detect-virtualization', {
                    'device_data': {
                        'system_info': {'platform': 'Windows', 'version': '10.0'},
                        'hardware_signatures': {'cpu_model': 'Test CPU'}
                    }
                }),
                ('validate-consistency', {
                    'historical_data': [{'test': 'data1'}, {'test': 'data2'}],
                    'current_data': {'test': 'current_data'}
                })
            ]
            
            response_times = []
            success_count = 0
            
            for i in range(5):  # 5 rounds of concurrent-like requests
                for endpoint, data in endpoints:
                    url = f"{self.backend_url}/anti-evasion/{endpoint}"
                    
                    start_time = time.time()
                    response = requests.post(url, json=data, headers=self.get_auth_headers(), timeout=15)
                    response_time = time.time() - start_time
                    
                    response_times.append(response_time)
                    if response.status_code == 200 and response.json().get('success'):
                        success_count += 1
            
            total_requests = len(endpoints) * 5
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            success_rate = (success_count / total_requests) * 100
            
            details = f"Success: {success_count}/{total_requests} ({success_rate:.1f}%), Avg: {avg_response_time:.3f}s, Min: {min_response_time:.3f}s, Max: {max_response_time:.3f}s"
            
            # Consider test successful if at least 90% of requests succeed and average response time is reasonable
            if success_rate >= 90 and avg_response_time < 5.0:
                self.log_test_result("Performance - Load Testing", True, details, avg_response_time)
                return True
            else:
                self.log_test_result("Performance - Load Testing", False, details, avg_response_time)
                return False
            
        except Exception as e:
            self.log_test_result("Performance - Load Testing", False, f"Exception: {str(e)}")
            return False
    
    def test_comprehensive_integration(self) -> bool:
        """Test comprehensive integration with EvasionDetectionEngine"""
        try:
            print("\n🔗 Testing Comprehensive Integration...")
            
            # Test the built-in detection test endpoint with custom data
            url = f"{self.backend_url}/anti-evasion/test-detection"
            
            custom_test_data = {
                'session_id': f'integration_test_{int(time.time())}',
                'canvas_fingerprint': {
                    'hash': 'suspicious_canvas_hash_12345',
                    'hash_consistency': 0.45,  # Low consistency to trigger detection
                    'timing_variance': 0.25,   # High variance to trigger detection
                    'rendering_time': 150.0    # Unusual rendering time
                },
                'webgl_fingerprint': {
                    'renderer_info': 'Fake WebGL Renderer',
                    'vendor': 'Suspicious Vendor Inc.',
                    'parameters_consistency': 0.35,  # Very low consistency
                    'extensions_count': 50  # Unusually high extension count
                },
                'user_agent': 'Mozilla/5.0 (Suspicious OS) FakeChrome/999.0.0.0',
                'timing_data': {
                    'performance_now_precision': 1,  # Low precision indicating manipulation
                    'date_now_correlation': 0.25,   # Poor correlation indicating manipulation
                    'high_resolution_time': False,
                    'timing_manipulation_detected': True
                },
                'hardware_characteristics': {
                    'cpu_info': {
                        'model_name': 'Virtual CPU Emulator 3000',  # Obviously virtual
                        'cores': 1,
                        'threads': 1
                    },
                    'memory_info': {
                        'total_gb': 2,  # Typical VM allocation
                        'available_gb': 1.8
                    }
                }
            }
            
            start_time = time.time()
            response = requests.post(url, json=custom_test_data, headers=self.get_auth_headers(), timeout=30)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'test_results' in data:
                    test_results = data['test_results']
                    
                    overall_success = test_results.get('overall_success', False)
                    successful_tests = test_results.get('successful_tests', 0)
                    total_tests = test_results.get('total_tests', 0)
                    success_rate = test_results.get('success_rate', 0)
                    
                    # Check individual component results
                    pattern_analysis = test_results.get('pattern_analysis', {})
                    virtualization_detection = test_results.get('virtualization_detection', {})
                    consistency_validation = test_results.get('consistency_validation', {})
                    
                    details = f"Overall: {overall_success}, Tests: {successful_tests}/{total_tests}, Rate: {success_rate}%"
                    
                    # Validate that the suspicious data triggered appropriate detections
                    evasion_score = pattern_analysis.get('evasion_score', 0)
                    vm_detected = virtualization_detection.get('virtualization_detected', False)
                    consistency_score = consistency_validation.get('consistency_score', 1.0)
                    
                    if evasion_score > 0.1 or vm_detected or consistency_score < 0.8:
                        details += f" | Detections: Evasion={evasion_score:.3f}, VM={vm_detected}, Consistency={consistency_score:.3f}"
                        self.log_test_result("Integration - Suspicious Data Detection", True, details, response_time)
                    else:
                        details += " | Warning: Suspicious data not properly detected"
                        self.log_test_result("Integration - Suspicious Data Detection", False, details, response_time)
                    
                    return True
                else:
                    self.log_test_result("Integration - Suspicious Data Detection", False, 
                                       f"Invalid response structure: {data}", response_time)
            else:
                self.log_test_result("Integration - Suspicious Data Detection", False, 
                                   f"HTTP {response.status_code}: {response.text}", response_time)
            
            return False
            
        except Exception as e:
            self.log_test_result("Integration - Suspicious Data Detection", False, f"Exception: {str(e)}")
            return False
    
    def run_extended_tests(self):
        """Run all extended anti-evasion tests"""
        print("🚀 Starting Extended Anti-Evasion Backend Testing Suite")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with testing.")
            return
        
        # Run extended tests
        test_methods = [
            self.test_error_handling,
            self.test_database_storage_verification,
            self.test_performance_under_load,
            self.test_comprehensive_integration
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
        print("📊 EXTENDED ANTI-EVASION TESTING SUMMARY")
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
            print("🎉 EXCELLENT: Extended anti-evasion testing passed with flying colors!")
        elif success_rate >= 80:
            print("✅ GOOD: Extended anti-evasion testing shows good system health.")
        elif success_rate >= 60:
            print("⚠️  FAIR: Extended anti-evasion testing shows some areas for improvement.")
        else:
            print("❌ POOR: Extended anti-evasion testing reveals significant issues.")

if __name__ == "__main__":
    tester = ExtendedAntiEvasionTester()
    tester.run_extended_tests()