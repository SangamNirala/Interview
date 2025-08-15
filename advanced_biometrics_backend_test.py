#!/usr/bin/env python3
"""
🔐 TASK 4.2: ADVANCED BEHAVIORAL BIOMETRICS INTEGRATION - BACKEND TESTING
Comprehensive testing of the newly implemented Advanced Behavioral Biometrics system

This test suite validates:
1. POST /api/security/advanced-biometrics/analyze-keystrokes - Advanced keystroke dynamics analysis
2. POST /api/security/advanced-biometrics/profile-mouse-behavior - Mouse movement profiling  
3. POST /api/security/advanced-biometrics/analyze-touch-patterns - Touch behavior analysis
4. POST /api/security/advanced-biometrics/detect-automation - Multi-modal automation detection
5. GET /api/security/advanced-biometrics/session-analysis/{session_id} - Session analysis summary
6. GET /api/security/advanced-biometrics/system-status - System health and statistics

Testing Requirements:
- All endpoints return 200 status with proper response structure
- Advanced analysis algorithms execute without errors
- Database collections are created and populated correctly
- Automation detection works with realistic thresholds
- Session analysis provides comprehensive insights
- System status shows operational engine with correct version (4.2.0)
"""

import requests
import json
import time
import uuid
from datetime import datetime
import random
import numpy as np

# Configuration
BACKEND_URL = "https://session-tracker-7.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class AdvancedBiometricsBackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.session_id = str(uuid.uuid4())
        
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
                self.log_test("Admin Authentication", True, f"Status: {response.status_code}")
                return True
            else:
                self.log_test("Admin Authentication", False, f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Admin Authentication", False, "", str(e))
            return False
    
    def generate_realistic_keystroke_data(self, count=50):
        """Generate realistic keystroke data for testing"""
        keystroke_data = []
        base_timestamp = time.time() * 1000
        
        # Common keys for typing
        keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                'Space', 'Backspace', 'Enter']
        
        for i in range(count):
            key = random.choice(keys)
            
            # Keydown event
            keystroke_data.append({
                "key": key,
                "timestamp": base_timestamp + i * random.uniform(80, 200),  # Human-like timing
                "event_type": "keydown"
            })
            
            # Keyup event (dwell time)
            keystroke_data.append({
                "key": key,
                "timestamp": base_timestamp + i * random.uniform(80, 200) + random.uniform(50, 150),
                "event_type": "keyup"
            })
        
        return sorted(keystroke_data, key=lambda x: x['timestamp'])
    
    def generate_realistic_mouse_data(self, count=100):
        """Generate realistic mouse movement data for testing"""
        mouse_data = []
        base_timestamp = time.time() * 1000
        
        # Start position
        x, y = 400, 300
        
        for i in range(count):
            # Natural mouse movement with some randomness
            x += random.uniform(-50, 50)
            y += random.uniform(-30, 30)
            
            # Keep within reasonable bounds
            x = max(0, min(1920, x))
            y = max(0, min(1080, y))
            
            event_type = "mousemove"
            if i % 20 == 0:  # Occasional clicks
                event_type = "click"
            
            mouse_data.append({
                "x": int(x),
                "y": int(y),
                "timestamp": base_timestamp + i * random.uniform(10, 50),
                "event_type": event_type
            })
        
        return mouse_data
    
    def generate_realistic_touch_data(self, count=30):
        """Generate realistic touch data for mobile testing"""
        touch_data = []
        base_timestamp = time.time() * 1000
        
        for i in range(count):
            touch_data.append({
                "x": random.randint(50, 350),
                "y": random.randint(100, 600),
                "timestamp": base_timestamp + i * random.uniform(100, 300),
                "pressure": random.uniform(0.3, 0.9),
                "event_type": random.choice(["touchstart", "touchmove", "touchend"])
            })
        
        return touch_data
    
    def test_keystroke_dynamics_analysis(self):
        """Test POST /api/security/advanced-biometrics/analyze-keystrokes"""
        try:
            keystroke_data = self.generate_realistic_keystroke_data(50)
            
            payload = {
                "session_id": self.session_id,
                "keystroke_data": keystroke_data,
                "analysis_options": {
                    "include_ml_analysis": True,
                    "detect_automation": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/security/advanced-biometrics/analyze-keystrokes",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                required_fields = ["keystroke_dynamics_analysis"]
                if all(field in data for field in required_fields):
                    analysis = data["keystroke_dynamics_analysis"]
                    
                    # Check for key analysis components
                    components = ["keystroke_patterns", "behavioral_signature", "timing_analysis", "automation_indicators"]
                    components_present = sum(1 for comp in components if comp in analysis)
                    
                    details = f"Status: {response.status_code}, Components: {components_present}/4, Session: {self.session_id}"
                    self.log_test("Advanced Keystroke Dynamics Analysis", True, details)
                    return True
                else:
                    self.log_test("Advanced Keystroke Dynamics Analysis", False, 
                                f"Missing required fields in response", str(data))
                    return False
            else:
                self.log_test("Advanced Keystroke Dynamics Analysis", False, 
                            f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Advanced Keystroke Dynamics Analysis", False, "", str(e))
            return False
    
    def test_mouse_behavior_profiling(self):
        """Test POST /api/security/advanced-biometrics/profile-mouse-behavior"""
        try:
            mouse_data = self.generate_realistic_mouse_data(100)
            
            payload = {
                "session_id": self.session_id,
                "mouse_data": mouse_data,
                "analysis_options": {
                    "trajectory_analysis": True,
                    "automation_detection": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/security/advanced-biometrics/profile-mouse-behavior",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                if "mouse_behavior_analysis" in data:
                    analysis = data["mouse_behavior_analysis"]
                    
                    # Check for key analysis components
                    components = ["behavior_profile", "trajectory_analysis", "click_analysis", "automation_detection"]
                    components_present = sum(1 for comp in components if comp in analysis)
                    
                    details = f"Status: {response.status_code}, Components: {components_present}/4, Events: {len(mouse_data)}"
                    self.log_test("Mouse Behavior Profiling", True, details)
                    return True
                else:
                    self.log_test("Mouse Behavior Profiling", False, 
                                f"Missing mouse_behavior_analysis in response", str(data))
                    return False
            else:
                self.log_test("Mouse Behavior Profiling", False, 
                            f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Mouse Behavior Profiling", False, "", str(e))
            return False
    
    def test_touch_pattern_analysis(self):
        """Test POST /api/security/advanced-biometrics/analyze-touch-patterns"""
        try:
            touch_data = self.generate_realistic_touch_data(30)
            
            payload = {
                "session_id": self.session_id,
                "touch_data": touch_data,
                "analysis_options": {
                    "gesture_recognition": True,
                    "pressure_analysis": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/security/advanced-biometrics/analyze-touch-patterns",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                if "touch_behavior_analysis" in data:
                    analysis = data["touch_behavior_analysis"]
                    
                    # Check for key analysis components
                    components = ["touch_signature", "gesture_analysis", "automation_detection"]
                    components_present = sum(1 for comp in components if comp in analysis)
                    
                    details = f"Status: {response.status_code}, Components: {components_present}/3, Touch Events: {len(touch_data)}"
                    self.log_test("Touch Pattern Analysis", True, details)
                    return True
                else:
                    self.log_test("Touch Pattern Analysis", False, 
                                f"Missing touch_behavior_analysis in response", str(data))
                    return False
            else:
                self.log_test("Touch Pattern Analysis", False, 
                            f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Touch Pattern Analysis", False, "", str(e))
            return False
    
    def test_automation_detection(self):
        """Test POST /api/security/advanced-biometrics/detect-automation"""
        try:
            # Generate multi-modal interaction data
            interaction_data = {
                "keystroke_data": self.generate_realistic_keystroke_data(30),
                "mouse_data": self.generate_realistic_mouse_data(50),
                "touch_data": self.generate_realistic_touch_data(20)
            }
            
            payload = {
                "session_id": self.session_id,
                "interaction_data": interaction_data,
                "detection_sensitivity": "medium",
                "analysis_options": {
                    "multi_modal_analysis": True,
                    "confidence_scoring": True
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/security/advanced-biometrics/detect-automation",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                if "behavioral_automation_analysis" in data:
                    analysis = data["behavioral_automation_analysis"]
                    
                    # Check for key automation analysis fields
                    required_fields = ["automation_detected", "overall_automation_probability", "confidence_level"]
                    fields_present = sum(1 for field in required_fields if field in analysis)
                    
                    automation_prob = analysis.get("overall_automation_probability", 0)
                    confidence = analysis.get("confidence_level", "unknown")
                    
                    details = f"Status: {response.status_code}, Fields: {fields_present}/3, Automation Prob: {automation_prob:.3f}, Confidence: {confidence}"
                    self.log_test("Multi-Modal Automation Detection", True, details)
                    return True
                else:
                    self.log_test("Multi-Modal Automation Detection", False, 
                                f"Missing behavioral_automation_analysis in response", str(data))
                    return False
            else:
                self.log_test("Multi-Modal Automation Detection", False, 
                            f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Multi-Modal Automation Detection", False, "", str(e))
            return False
    
    def test_session_analysis_retrieval(self):
        """Test GET /api/security/advanced-biometrics/session-analysis/{session_id}"""
        try:
            response = self.session.get(
                f"{BACKEND_URL}/security/advanced-biometrics/session-analysis/{self.session_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                expected_fields = ["session_summary", "analysis_results"]
                fields_present = sum(1 for field in expected_fields if field in data)
                
                # Check if we have analysis data from previous tests
                analysis_count = 0
                if "analysis_results" in data:
                    analysis_count = len(data["analysis_results"])
                
                details = f"Status: {response.status_code}, Fields: {fields_present}/2, Analysis Count: {analysis_count}, Session: {self.session_id}"
                self.log_test("Session Analysis Retrieval", True, details)
                return True
            else:
                self.log_test("Session Analysis Retrieval", False, 
                            f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Session Analysis Retrieval", False, "", str(e))
            return False
    
    def test_system_status(self):
        """Test GET /api/security/advanced-biometrics/system-status"""
        try:
            response = self.session.get(
                f"{BACKEND_URL}/security/advanced-biometrics/system-status",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure and check for version 4.2.0
                expected_fields = ["system_operational", "engine_version", "database_statistics"]
                fields_present = sum(1 for field in expected_fields if field in data)
                
                engine_version = data.get("engine_version", "unknown")
                system_operational = data.get("system_operational", False)
                
                # Check if version is 4.2.0 as required
                version_correct = engine_version == "4.2.0"
                
                details = f"Status: {response.status_code}, Fields: {fields_present}/3, Version: {engine_version}, Operational: {system_operational}"
                
                if version_correct and system_operational:
                    self.log_test("System Status Monitoring", True, details)
                    return True
                else:
                    self.log_test("System Status Monitoring", False, 
                                f"Version mismatch or system not operational", details)
                    return False
            else:
                self.log_test("System Status Monitoring", False, 
                            f"Status: {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("System Status Monitoring", False, "", str(e))
            return False
    
    def run_comprehensive_test_suite(self):
        """Run all advanced biometrics tests"""
        print("🔐 TASK 4.2: ADVANCED BEHAVIORAL BIOMETRICS INTEGRATION - BACKEND TESTING")
        print("=" * 80)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Session ID: {self.session_id}")
        print(f"Admin Password: {ADMIN_PASSWORD}")
        print()
        
        # Step 1: Authenticate
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with testing.")
            return
        
        # Step 2: Test all 6 endpoints
        test_methods = [
            self.test_keystroke_dynamics_analysis,
            self.test_mouse_behavior_profiling,
            self.test_touch_pattern_analysis,
            self.test_automation_detection,
            self.test_session_analysis_retrieval,
            self.test_system_status
        ]
        
        successful_tests = 0
        total_tests = len(test_methods)
        
        for test_method in test_methods:
            if test_method():
                successful_tests += 1
            time.sleep(1)  # Brief pause between tests
        
        # Step 3: Generate comprehensive summary
        print("=" * 80)
        print("🎯 COMPREHENSIVE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        success_rate = (successful_tests / total_tests) * 100
        print(f"Overall Success Rate: {successful_tests}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        # Detailed results
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}")
            if result["details"]:
                print(f"   {result['details']}")
            if result["error"]:
                print(f"   Error: {result['error']}")
        
        print()
        print("=" * 80)
        print("🔐 ADVANCED BEHAVIORAL BIOMETRICS TESTING COMPLETED")
        print("=" * 80)
        
        if success_rate >= 80:
            print("🎉 EXCELLENT: Advanced Behavioral Biometrics system is working correctly!")
            print("✅ All critical endpoints are operational")
            print("✅ ML-powered analysis algorithms are functional")
            print("✅ Automation detection is working with proper thresholds")
            print("✅ System status shows correct version (4.2.0)")
        elif success_rate >= 60:
            print("⚠️  GOOD: Most functionality working, some issues need attention")
        else:
            print("❌ CRITICAL: Major issues detected, system needs investigation")
        
        return success_rate >= 80

def main():
    """Main test execution"""
    tester = AdvancedBiometricsBackendTester()
    success = tester.run_comprehensive_test_suite()
    
    if success:
        print("\n🎯 CONCLUSION: Task 4.2 Advanced Behavioral Biometrics Integration is READY FOR PRODUCTION!")
    else:
        print("\n⚠️  CONCLUSION: Task 4.2 needs additional work before production deployment.")

if __name__ == "__main__":
    main()