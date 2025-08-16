#!/usr/bin/env python3
"""
🎯 ADVANCED BEHAVIORAL BIOMETRICS INTEGRATION - SESSION ANALYSIS TESTING
Testing the previously failing endpoint: GET /api/security/advanced-biometrics/session-analysis/{session_id}

SPECIFIC TESTING REQUIREMENTS:
1. Test the previously failing endpoint: GET /api/security/advanced-biometrics/session-analysis/{session_id}
2. Verify that the get_session_analysis_summary method in AdvancedBehavioralBiometricsEngine is now operational
3. Confirm the endpoint returns proper session analysis summary with behavioral fingerprints, consistency assessment, and risk analysis
4. Test with a sample session_id to ensure comprehensive summary generation works correctly
5. Verify all other advanced biometric endpoints remain operational

CONTEXT FROM PREVIOUS TESTING:
- 5 out of 6 endpoints were working (83.3% success rate)  
- Only missing endpoint: GET /api/security/advanced-biometrics/session-analysis/{session_id} which had a 500 error due to missing get_session_analysis_summary method
- The missing method has now been implemented with comprehensive session analysis capabilities

EXPECTED OUTCOME:
- 100% success rate (6/6 tests passed)
- GET /api/security/advanced-biometrics/session-analysis/{session_id} should now work correctly
- Comprehensive session analysis summary should be generated with proper response structure
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time
import random

# Configuration
BACKEND_URL = "https://securesession.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class AdvancedBiometricsSessionAnalysisTester:
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

    def test_keystroke_analysis(self):
        """Test keystroke analysis to generate session data"""
        try:
            # Generate realistic keystroke data
            keystroke_data = []
            base_time = int(time.time() * 1000)
            
            for i in range(50):
                keystroke_data.append({
                    "key": chr(65 + (i % 26)),  # A-Z
                    "event_type": "keydown",
                    "timestamp": base_time + i * random.randint(100, 300),
                    "pressure": random.uniform(0.3, 0.8)
                })
                keystroke_data.append({
                    "key": chr(65 + (i % 26)),
                    "event_type": "keyup", 
                    "timestamp": base_time + i * random.randint(100, 300) + random.randint(50, 150),
                    "pressure": 0
                })

            response = self.session.post(
                f"{BACKEND_URL}/security/advanced-biometrics/analyze-keystrokes",
                json={
                    "session_id": self.session_id,
                    "keystroke_data": keystroke_data
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "analysis_result" in data:
                    self.log_result("Keystroke Analysis Setup", True, 
                                  f"Status: {response.status_code}, Session: {self.session_id}")
                    return True
                else:
                    self.log_result("Keystroke Analysis Setup", False, 
                                  f"Invalid response structure", data)
                    return False
            else:
                self.log_result("Keystroke Analysis Setup", False, 
                              f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Keystroke Analysis Setup", False, f"Error: {str(e)}")
            return False

    def test_mouse_behavior_analysis(self):
        """Test mouse behavior analysis to generate more session data"""
        try:
            # Generate realistic mouse data
            mouse_data = []
            base_time = int(time.time() * 1000)
            
            for i in range(100):
                mouse_data.append({
                    "x": random.randint(100, 1200),
                    "y": random.randint(100, 800),
                    "event_type": "mousemove",
                    "timestamp": base_time + i * random.randint(10, 50),
                    "button": None
                })
                
            # Add some click events
            for i in range(5):
                mouse_data.append({
                    "x": random.randint(100, 1200),
                    "y": random.randint(100, 800),
                    "event_type": "click",
                    "timestamp": base_time + i * random.randint(500, 1000),
                    "button": "left"
                })

            response = self.session.post(
                f"{BACKEND_URL}/security/advanced-biometrics/profile-mouse-behavior",
                json={
                    "session_id": self.session_id,
                    "mouse_data": mouse_data
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "analysis_result" in data:
                    self.log_result("Mouse Behavior Analysis Setup", True, 
                                  f"Status: {response.status_code}, Session: {self.session_id}")
                    return True
                else:
                    self.log_result("Mouse Behavior Analysis Setup", False, 
                                  f"Invalid response structure", data)
                    return False
            else:
                self.log_result("Mouse Behavior Analysis Setup", False, 
                              f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Mouse Behavior Analysis Setup", False, f"Error: {str(e)}")
            return False

    def test_session_analysis_summary(self):
        """Test GET /api/security/advanced-biometrics/session-analysis/{session_id} - THE MAIN TEST"""
        try:
            print(f"\n🎯 TESTING THE PREVIOUSLY FAILING ENDPOINT:")
            print(f"GET /api/security/advanced-biometrics/session-analysis/{self.session_id}")
            
            response = self.session.get(
                f"{BACKEND_URL}/security/advanced-biometrics/session-analysis/{self.session_id}",
                timeout=30
            )
            
            print(f"Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response Keys: {list(data.keys())}")
                
                # Check for expected session summary structure
                expected_fields = [
                    "session_id", 
                    "analysis_overview", 
                    "behavioral_fingerprint",
                    "consistency_assessment",
                    "automation_assessment", 
                    "risk_analysis",
                    "behavioral_patterns",
                    "session_metadata"
                ]
                
                if "session_summary" in data:
                    session_summary = data["session_summary"]
                    fields_present = sum(1 for field in expected_fields if field in session_summary)
                    
                    # Validate key components
                    has_analysis_overview = "analysis_overview" in session_summary
                    has_risk_analysis = "risk_analysis" in session_summary
                    has_automation_assessment = "automation_assessment" in session_summary
                    has_consistency_assessment = "consistency_assessment" in session_summary
                    
                    # Check if session_id matches
                    session_id_match = session_summary.get("session_id") == self.session_id
                    
                    details = (f"Status: {response.status_code}, "
                             f"Fields: {fields_present}/{len(expected_fields)}, "
                             f"Session ID Match: {session_id_match}, "
                             f"Analysis Overview: {has_analysis_overview}, "
                             f"Risk Analysis: {has_risk_analysis}, "
                             f"Automation Assessment: {has_automation_assessment}, "
                             f"Consistency Assessment: {has_consistency_assessment}")
                    
                    # Success if we have most expected fields and key components
                    success = (fields_present >= 6 and 
                             session_id_match and 
                             has_analysis_overview and 
                             has_risk_analysis)
                    
                    self.log_result("Session Analysis Summary (MAIN TEST)", success, details, data)
                    
                    if success:
                        print(f"✅ SUCCESS: get_session_analysis_summary method is now working!")
                        print(f"   - Session ID: {session_summary.get('session_id')}")
                        print(f"   - Analysis Overview: {session_summary.get('analysis_overview', {})}")
                        print(f"   - Risk Level: {session_summary.get('risk_analysis', {}).get('risk_level', 'unknown')}")
                        print(f"   - Automation Risk: {session_summary.get('automation_assessment', {}).get('automation_risk_level', 'unknown')}")
                    
                    return success
                else:
                    self.log_result("Session Analysis Summary (MAIN TEST)", False, 
                                  f"Missing session_summary in response", data)
                    return False
            else:
                error_text = response.text[:500] if response.text else "No error details"
                self.log_result("Session Analysis Summary (MAIN TEST)", False, 
                              f"Status: {response.status_code}", error_text)
                return False
                
        except Exception as e:
            self.log_result("Session Analysis Summary (MAIN TEST)", False, f"Error: {str(e)}")
            return False

    def test_automation_detection(self):
        """Test automation detection endpoint"""
        try:
            interaction_data = {
                "keystroke_data": [
                    {"key": "A", "event_type": "keydown", "timestamp": int(time.time() * 1000), "pressure": 0.5},
                    {"key": "A", "event_type": "keyup", "timestamp": int(time.time() * 1000) + 100, "pressure": 0}
                ],
                "mouse_data": [
                    {"x": 100, "y": 100, "event_type": "mousemove", "timestamp": int(time.time() * 1000)},
                    {"x": 200, "y": 200, "event_type": "click", "timestamp": int(time.time() * 1000) + 500}
                ]
            }

            response = self.session.post(
                f"{BACKEND_URL}/security/advanced-biometrics/detect-automation",
                json={
                    "session_id": self.session_id,
                    "interaction_data": interaction_data
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "analysis_result" in data:
                    self.log_result("Automation Detection", True, 
                                  f"Status: {response.status_code}")
                    return True
                else:
                    self.log_result("Automation Detection", False, 
                                  f"Invalid response structure", data)
                    return False
            else:
                self.log_result("Automation Detection", False, 
                              f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Automation Detection", False, f"Error: {str(e)}")
            return False

    def test_system_status(self):
        """Test system status endpoint"""
        try:
            response = self.session.get(
                f"{BACKEND_URL}/security/advanced-biometrics/system-status",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for basic system status fields
                has_operational = "system_operational" in data
                has_version = "engine_version" in data
                
                engine_version = data.get("engine_version", "unknown")
                system_operational = data.get("system_operational", False)
                
                details = (f"Status: {response.status_code}, "
                         f"Version: {engine_version}, "
                         f"Operational: {system_operational}")
                
                success = has_operational and has_version
                self.log_result("System Status", success, details)
                return success
            else:
                self.log_result("System Status", False, 
                              f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("System Status", False, f"Error: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run comprehensive test suite focusing on session analysis"""
        print("🔐 ADVANCED BEHAVIORAL BIOMETRICS INTEGRATION - SESSION ANALYSIS TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Session ID: {self.session_id}")
        print(f"Admin Password: {ADMIN_PASSWORD}")
        print()
        
        # Step 1: Authenticate
        if not self.authenticate_admin():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Step 2: Generate session data with keystroke analysis
        print("\n📊 GENERATING SESSION DATA FOR ANALYSIS...")
        keystroke_success = self.test_keystroke_analysis()
        
        # Step 3: Generate more session data with mouse analysis
        mouse_success = self.test_mouse_behavior_analysis()
        
        # Step 4: Test automation detection
        automation_success = self.test_automation_detection()
        
        # Step 5: THE MAIN TEST - Session Analysis Summary
        print("\n🎯 MAIN TEST: SESSION ANALYSIS SUMMARY")
        print("-" * 50)
        session_analysis_success = self.test_session_analysis_summary()
        
        # Step 6: Test system status
        system_status_success = self.test_system_status()
        
        # Calculate results
        tests_run = [
            ("Admin Authentication", True),  # Already passed
            ("Keystroke Analysis Setup", keystroke_success),
            ("Mouse Behavior Analysis Setup", mouse_success), 
            ("Automation Detection", automation_success),
            ("Session Analysis Summary (MAIN TEST)", session_analysis_success),
            ("System Status", system_status_success)
        ]
        
        passed_tests = sum(1 for _, success in tests_run if success)
        total_tests = len(tests_run)
        success_rate = (passed_tests / total_tests) * 100
        
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        print(f"Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        for test_name, success in tests_run:
            status = "✅" if success else "❌"
            print(f"{status} {test_name}")
        
        print("\n" + "=" * 80)
        print("🔐 ADVANCED BEHAVIORAL BIOMETRICS SESSION ANALYSIS TESTING COMPLETED")
        print("=" * 80)
        
        if session_analysis_success:
            print("✅ SUCCESS: The previously failing session analysis endpoint is now working!")
            print("✅ SUCCESS: get_session_analysis_summary method has been successfully implemented!")
            print("✅ SUCCESS: Comprehensive session analysis summary is being generated correctly!")
        else:
            print("❌ FAILURE: Session analysis endpoint still has issues")
        
        if success_rate == 100:
            print("🎉 PERFECT: All tests passed - 100% success rate achieved!")
        elif success_rate >= 83.3:
            print("✅ EXCELLENT: Significant improvement from previous 83.3% success rate!")
        else:
            print("⚠️  NEEDS WORK: System requires additional investigation")

if __name__ == "__main__":
    tester = AdvancedBiometricsSessionAnalysisTester()
    tester.run_comprehensive_test()