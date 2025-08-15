#!/usr/bin/env python3
"""
Behavioral Biometric Analysis Endpoints Testing
Testing specific endpoints reported as returning 404 errors
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')
load_dotenv('/app/frontend/.env')

# Get backend URL from frontend environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://biometric-engine.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

print(f"🔗 Testing Backend URL: {BASE_URL}")

class BiometricEndpointsTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_session_id = str(uuid.uuid4())
        self.test_candidate_id = str(uuid.uuid4())
        self.results = []
        
    def log_result(self, test_name, success, details):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        self.results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def test_backend_connectivity(self):
        """Test basic backend connectivity"""
        try:
            response = self.session.get(f"{BASE_URL}/admin/login", timeout=10)
            if response.status_code in [200, 405, 422]:  # 405 for OPTIONS, 422 for missing data
                self.log_result("Backend Connectivity", True, f"Backend accessible (Status: {response.status_code})")
                return True
            else:
                self.log_result("Backend Connectivity", False, f"Backend not accessible (Status: {response.status_code})")
                return False
        except Exception as e:
            self.log_result("Backend Connectivity", False, f"Connection error: {str(e)}")
            return False
    
    def test_biometric_data_submit(self):
        """Test POST /api/security/biometric-data/submit"""
        try:
            # Create realistic biometric data
            test_data = {
                "session_id": self.test_session_id,
                "keystroke_data": [
                    {
                        "key": "a",
                        "keydown_time": 1234567890.123,
                        "keyup_time": 1234567890.223,
                        "dwell_time": 100,
                        "flight_time": 50
                    },
                    {
                        "key": "b",
                        "keydown_time": 1234567890.273,
                        "keyup_time": 1234567890.373,
                        "dwell_time": 100,
                        "flight_time": 50
                    }
                ],
                "mouse_data": [
                    {
                        "x": 100,
                        "y": 200,
                        "timestamp": 1234567890.123,
                        "velocity": 5.2,
                        "acceleration": 1.1
                    },
                    {
                        "x": 150,
                        "y": 250,
                        "timestamp": 1234567890.223,
                        "velocity": 6.1,
                        "acceleration": 0.9
                    }
                ],
                "scroll_data": [
                    {
                        "scroll_x": 0,
                        "scroll_y": 100,
                        "timestamp": 1234567890.323,
                        "velocity": 2.5
                    }
                ],
                "click_data": [
                    {
                        "x": 200,
                        "y": 300,
                        "timestamp": 1234567890.423,
                        "button": "left",
                        "duration": 150
                    }
                ],
                "timing_data": [
                    {
                        "question_id": "q1",
                        "start_time": 1234567890.123,
                        "end_time": 1234567920.123,
                        "response_time": 30.0
                    }
                ],
                "consent_given": True
            }
            
            response = self.session.post(
                f"{BASE_URL}/security/biometric-data/submit",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_result("Biometric Data Submit", True, 
                                  f"Data submitted successfully (Session: {result.get('session_id')})")
                    return True
                else:
                    self.log_result("Biometric Data Submit", False, 
                                  f"API returned success=false: {result}")
                    return False
            else:
                self.log_result("Biometric Data Submit", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Biometric Data Submit", False, f"Request failed: {str(e)}")
            return False
    
    def test_biometric_anomaly_detection(self):
        """Test POST /api/security/biometric-analysis/detect-anomalies"""
        try:
            test_data = {
                "session_id": self.test_session_id,
                "analysis_types": ["keystroke_dynamics", "interaction_patterns", "response_timing"],
                "baseline_comparison": False
            }
            
            response = self.session.post(
                f"{BASE_URL}/security/biometric-analysis/detect-anomalies",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    anomaly_score = result.get("overall_anomaly_score", 0)
                    self.log_result("Biometric Anomaly Detection", True, 
                                  f"Anomaly detection completed (Score: {anomaly_score})")
                    return True
                else:
                    self.log_result("Biometric Anomaly Detection", False, 
                                  f"API returned success=false: {result}")
                    return False
            elif response.status_code == 404:
                self.log_result("Biometric Anomaly Detection", False, 
                              f"Session data not found (expected after data submit)")
                return False
            else:
                self.log_result("Biometric Anomaly Detection", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Biometric Anomaly Detection", False, f"Request failed: {str(e)}")
            return False
    
    def test_biometric_signature_generation(self):
        """Test POST /api/security/biometric-signature/generate"""
        try:
            # Generate multiple session IDs for signature generation
            session_ids = [self.test_session_id, str(uuid.uuid4()), str(uuid.uuid4())]
            
            response = self.session.post(
                f"{BASE_URL}/security/biometric-signature/generate",
                json=session_ids,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    signature_id = result.get("signature_id")
                    self.log_result("Biometric Signature Generation", True, 
                                  f"Signature generated (ID: {signature_id})")
                    return True
                else:
                    self.log_result("Biometric Signature Generation", False, 
                                  f"API returned success=false: {result}")
                    return False
            elif response.status_code == 400:
                self.log_result("Biometric Signature Generation", False, 
                              f"Insufficient data for signature generation (expected)")
                return False
            else:
                self.log_result("Biometric Signature Generation", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Biometric Signature Generation", False, f"Request failed: {str(e)}")
            return False
    
    def test_biometric_config_update(self):
        """Test POST /api/security/biometric-config/update"""
        try:
            test_data = {
                "session_id": self.test_session_id,
                "enable_biometric_tracking": True,
                "tracking_sensitivity": "high",
                "real_time_analysis": True,
                "intervention_enabled": True
            }
            
            response = self.session.post(
                f"{BASE_URL}/security/biometric-config/update",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_result("Biometric Config Update", True, 
                                  f"Configuration updated successfully")
                    return True
                else:
                    self.log_result("Biometric Config Update", False, 
                                  f"API returned success=false: {result}")
                    return False
            else:
                self.log_result("Biometric Config Update", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Biometric Config Update", False, f"Request failed: {str(e)}")
            return False
    
    def test_get_biometric_analysis(self):
        """Test GET /api/security/biometric-analysis/{session_id}"""
        try:
            response = self.session.get(
                f"{BASE_URL}/security/biometric-analysis/{self.test_session_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    analysis_results = result.get("analysis_results", {})
                    self.log_result("Get Biometric Analysis", True, 
                                  f"Analysis retrieved (Keys: {list(analysis_results.keys())})")
                    return True
                else:
                    self.log_result("Get Biometric Analysis", False, 
                                  f"API returned success=false: {result}")
                    return False
            elif response.status_code == 404:
                self.log_result("Get Biometric Analysis", False, 
                              f"No analysis found for session (expected if data submit failed)")
                return False
            else:
                self.log_result("Get Biometric Analysis", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Get Biometric Analysis", False, f"Request failed: {str(e)}")
            return False
    
    def test_data_privacy_consent(self):
        """Test POST /api/security/data-privacy/consent"""
        try:
            test_data = {
                "session_id": self.test_session_id,
                "candidate_id": self.test_candidate_id,
                "consent_given": True,
                "data_types": ["keystroke", "mouse", "scroll", "timing"]
            }
            
            response = self.session.post(
                f"{BASE_URL}/security/data-privacy/consent",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_result("Data Privacy Consent", True, 
                                  f"Consent recorded successfully")
                    return True
                else:
                    self.log_result("Data Privacy Consent", False, 
                                  f"API returned success=false: {result}")
                    return False
            else:
                self.log_result("Data Privacy Consent", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Data Privacy Consent", False, f"Request failed: {str(e)}")
            return False
    
    def test_purge_expired_data(self):
        """Test POST /api/security/data-privacy/purge-expired"""
        try:
            response = self.session.post(
                f"{BASE_URL}/security/data-privacy/purge-expired",
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    purge_results = result.get("purge_results", {})
                    total_purged = sum([
                        purge_results.get("biometric_data_purged", 0),
                        purge_results.get("consent_records_purged", 0),
                        purge_results.get("interventions_purged", 0)
                    ])
                    self.log_result("Purge Expired Data", True, 
                                  f"Data purged successfully (Total: {total_purged} records)")
                    return True
                else:
                    self.log_result("Purge Expired Data", False, 
                                  f"API returned success=false: {result}")
                    return False
            else:
                self.log_result("Purge Expired Data", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Purge Expired Data", False, f"Request failed: {str(e)}")
            return False
    
    def test_get_security_interventions(self):
        """Test GET /api/security/interventions/{session_id}"""
        try:
            response = self.session.get(
                f"{BASE_URL}/security/interventions/{self.test_session_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    interventions = result.get("interventions", [])
                    total_interventions = result.get("total_interventions", 0)
                    self.log_result("Get Security Interventions", True, 
                                  f"Interventions retrieved (Count: {total_interventions})")
                    return True
                else:
                    self.log_result("Get Security Interventions", False, 
                                  f"API returned success=false: {result}")
                    return False
            else:
                self.log_result("Get Security Interventions", False, 
                              f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Get Security Interventions", False, f"Request failed: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all biometric endpoint tests"""
        print("🎯 BEHAVIORAL BIOMETRIC ANALYSIS ENDPOINTS TESTING")
        print("=" * 60)
        
        # Test backend connectivity first
        if not self.test_backend_connectivity():
            print("❌ Backend not accessible, skipping endpoint tests")
            return
        
        print(f"\n🧪 Testing with Session ID: {self.test_session_id}")
        print(f"🧪 Testing with Candidate ID: {self.test_candidate_id}")
        print()
        
        # Test all endpoints in logical order
        self.test_biometric_data_submit()
        self.test_biometric_anomaly_detection()
        self.test_biometric_signature_generation()
        self.test_biometric_config_update()
        self.test_get_biometric_analysis()
        self.test_data_privacy_consent()
        self.test_purge_expired_data()
        self.test_get_security_interventions()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"✅ Passed: {passed}/{total} ({success_rate:.1f}%)")
        print(f"❌ Failed: {total - passed}/{total}")
        
        if passed == total:
            print("🎉 ALL BIOMETRIC ENDPOINTS WORKING CORRECTLY!")
        else:
            print("⚠️  Some endpoints have issues - see details above")
        
        return success_rate >= 75  # Consider 75%+ as success

def main():
    """Main test execution"""
    tester = BiometricEndpointsTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Biometric endpoints testing completed successfully")
    else:
        print("\n❌ Biometric endpoints testing found critical issues")
    
    return success

if __name__ == "__main__":
    main()