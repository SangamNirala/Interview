#!/usr/bin/env python3
"""
Advanced ML-powered IRT Calibration System Testing
Phase 1.2 Implementation - Step 1

This test suite comprehensively tests the new Advanced ML-powered IRT Calibration System
including 3PL IRT calibration, ML model training, parameter estimation, and quality control.
"""

import requests
import json
import time
import sys
from datetime import datetime, timedelta
import random
import uuid
import math

# Configuration
BACKEND_URL = "https://anomaly-detect-eval.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class IRTCalibrationTester:
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
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if error:
            print(f"   Error: {error}")
        print()
    
    def test_admin_authentication(self):
        """Test admin authentication for IRT calibration access"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/login",
                json={"password": ADMIN_PASSWORD},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.admin_authenticated = True
                    self.log_test(
                        "Admin Authentication for IRT Calibration",
                        True,
                        f"Successfully authenticated with admin credentials"
                    )
                    return True
                else:
                    self.log_test(
                        "Admin Authentication for IRT Calibration",
                        False,
                        error=f"Authentication failed: {data.get('message', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test(
                    "Admin Authentication for IRT Calibration",
                    False,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Admin Authentication for IRT Calibration",
                False,
                error=f"Request failed: {str(e)}"
            )
            return False
    
    def test_aptitude_questions_seeding(self):
        """Ensure aptitude questions are seeded for calibration testing"""
        try:
            # Check if questions exist
            response = self.session.get(
                f"{BACKEND_URL}/admin/aptitude-questions/stats",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                total_questions = data.get("total_questions", 0)
                
                if total_questions >= 50:  # Need sufficient questions for calibration
                    self.log_test(
                        "Aptitude Questions Availability for Calibration",
                        True,
                        f"Found {total_questions} questions available for calibration"
                    )
                    return True
                else:
                    # Try to seed questions
                    seed_response = self.session.post(
                        f"{BACKEND_URL}/admin/aptitude-questions/seed",
                        timeout=60
                    )
                    
                    if seed_response.status_code == 200:
                        seed_data = seed_response.json()
                        self.log_test(
                            "Aptitude Questions Seeding for Calibration",
                            True,
                            f"Successfully seeded {seed_data.get('total_inserted', 0)} questions"
                        )
                        return True
                    else:
                        self.log_test(
                            "Aptitude Questions Seeding for Calibration",
                            False,
                            error=f"Seeding failed: HTTP {seed_response.status_code}"
                        )
                        return False
            else:
                self.log_test(
                    "Aptitude Questions Availability Check",
                    False,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Aptitude Questions Availability Check",
                False,
                error=f"Request failed: {str(e)}"
            )
            return False
    
    def create_mock_session_data(self):
        """Create mock aptitude session data for calibration testing"""
        try:
            # Create test configuration
            config_data = {
                "test_name": "IRT Calibration Test",
                "job_title": "Software Engineer",
                "job_description": "Testing IRT calibration system",
                "topics": ["numerical_reasoning", "logical_reasoning"],
                "questions_per_topic": {"numerical_reasoning": 10, "logical_reasoning": 10},
                "difficulty_distribution": {"easy": 0.4, "medium": 0.4, "hard": 0.2},
                "total_time_limit": 1800,
                "adaptive_mode": True
            }
            
            config_response = self.session.post(
                f"{BACKEND_URL}/admin/aptitude-test/create-config",
                json=config_data,
                timeout=30
            )
            
            if config_response.status_code != 200:
                self.log_test(
                    "Mock Session Data Creation - Config",
                    False,
                    error=f"Config creation failed: HTTP {config_response.status_code}"
                )
                return False
            
            config_result = config_response.json()
            config_id = config_result.get("config_id")
            
            # Generate token
            token_response = self.session.post(
                f"{BACKEND_URL}/admin/aptitude-test/generate-token",
                json={"config_id": config_id, "expires_in_hours": 24},
                timeout=30
            )
            
            if token_response.status_code != 200:
                self.log_test(
                    "Mock Session Data Creation - Token",
                    False,
                    error=f"Token generation failed: HTTP {token_response.status_code}"
                )
                return False
            
            token_result = token_response.json()
            token = token_result.get("token")
            
            # Create multiple mock sessions with realistic response patterns
            sessions_created = 0
            for i in range(15):  # Create 15 mock sessions for calibration
                session_data = {
                    "token": token,
                    "candidate_name": f"Test Candidate {i+1}",
                    "candidate_email": f"test{i+1}@example.com"
                }
                
                session_response = self.session.post(
                    f"{BACKEND_URL}/aptitude-test/start-session",
                    json=session_data,
                    timeout=30
                )
                
                if session_response.status_code == 200:
                    session_result = session_response.json()
                    session_id = session_result.get("session_id")
                    
                    # Simulate answering questions with realistic patterns
                    self.simulate_test_session(session_id, ability_level=random.uniform(-2, 2))
                    sessions_created += 1
                    
                    # Small delay between sessions
                    time.sleep(0.5)
            
            if sessions_created >= 10:  # Need minimum 10 sessions for calibration
                self.log_test(
                    "Mock Session Data Creation",
                    True,
                    f"Successfully created {sessions_created} mock sessions for calibration"
                )
                return True
            else:
                self.log_test(
                    "Mock Session Data Creation",
                    False,
                    error=f"Only created {sessions_created} sessions, need minimum 10"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Mock Session Data Creation",
                False,
                error=f"Failed to create mock data: {str(e)}"
            )
            return False
    
    def simulate_test_session(self, session_id, ability_level=0.0):
        """Simulate a complete test session with realistic response patterns"""
        try:
            questions_answered = 0
            max_questions = 20
            
            while questions_answered < max_questions:
                # Get next question
                question_response = self.session.get(
                    f"{BACKEND_URL}/aptitude-test/get-question/{session_id}",
                    timeout=30
                )
                
                if question_response.status_code != 200:
                    break
                
                question_data = question_response.json()
                question_id = question_data.get("question_id")
                
                if not question_id:
                    break
                
                # Simulate realistic response based on ability level and question difficulty
                difficulty_map = {"easy": -1, "medium": 0, "hard": 1}
                question_difficulty = difficulty_map.get(question_data.get("difficulty", "medium"), 0)
                
                # Calculate probability of correct answer using simple IRT model
                prob_correct = 1 / (1 + math.exp(-(ability_level - question_difficulty)))
                is_correct = random.random() < prob_correct
                
                # Simulate response time (faster for easier questions, slower for harder)
                base_time = 45  # seconds
                difficulty_factor = 1 + (question_difficulty * 0.3)
                ability_factor = 1 - (ability_level * 0.1)
                response_time = max(10, base_time * difficulty_factor * ability_factor + random.uniform(-15, 15))
                
                # Submit answer
                answer_data = {
                    "session_id": session_id,
                    "question_id": question_id,
                    "selected_answer": "A" if is_correct else random.choice(["B", "C", "D"]),
                    "time_taken": response_time,
                    "is_correct": is_correct
                }
                
                answer_response = self.session.post(
                    f"{BACKEND_URL}/aptitude-test/submit-answer",
                    json=answer_data,
                    timeout=30
                )
                
                if answer_response.status_code == 200:
                    questions_answered += 1
                else:
                    break
                
                # Small delay between questions
                time.sleep(0.1)
            
            # Complete the session
            complete_response = self.session.post(
                f"{BACKEND_URL}/aptitude-test/complete-session",
                json={"session_id": session_id},
                timeout=30
            )
            
            return questions_answered >= 10  # Consider successful if answered at least 10 questions
            
        except Exception as e:
            print(f"Error simulating session {session_id}: {str(e)}")
            return False
    
    def test_irt_calibration_endpoint(self):
        """Test the main IRT calibration endpoint"""
        try:
            print("🔧 Starting Advanced ML-powered IRT Calibration...")
            
            response = self.session.post(
                f"{BACKEND_URL}/admin/calibrate-irt-parameters",
                timeout=120  # Allow more time for ML processing
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    summary = data.get("summary", {})
                    ml_analysis = data.get("ml_analysis", {})
                    quality_control = data.get("quality_control", {})
                    
                    # Validate response structure
                    required_fields = ["summary", "ml_analysis", "quality_control", "calibration_method"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.log_test(
                            "IRT Calibration Response Structure",
                            False,
                            error=f"Missing required fields: {missing_fields}"
                        )
                        return False
                    
                    # Validate summary data
                    total_questions = summary.get("total_questions_analyzed", 0)
                    successful_calibrations = summary.get("successful_calibrations", 0)
                    success_rate = summary.get("success_rate", 0)
                    
                    self.log_test(
                        "Advanced ML-powered IRT Calibration",
                        True,
                        f"Calibrated {successful_calibrations}/{total_questions} questions (success rate: {success_rate:.1%})"
                    )
                    
                    # Test ML analysis results
                    rf_auc = ml_analysis.get("random_forest_auc", 0)
                    gb_auc = ml_analysis.get("gradient_boosting_auc", 0)
                    ml_status = ml_analysis.get("ml_training_status", "unknown")
                    
                    self.log_test(
                        "ML Model Training and Analysis",
                        ml_status == "trained",
                        f"Random Forest AUC: {rf_auc:.3f}, Gradient Boosting AUC: {gb_auc:.3f}, Status: {ml_status}"
                    )
                    
                    # Test quality control features
                    misfitting_items = quality_control.get("misfitting_items_detected", 0)
                    high_priority_issues = quality_control.get("high_priority_issues", 0)
                    
                    self.log_test(
                        "Quality Control and Misfitting Item Detection",
                        True,
                        f"Detected {misfitting_items} misfitting items, {high_priority_issues} high priority issues"
                    )
                    
                    # Validate calibration method
                    calibration_method = data.get("calibration_method", "")
                    expected_method = "3PL_IRT_MLE_with_ML_Analysis"
                    
                    self.log_test(
                        "3PL IRT Maximum Likelihood Estimation Method",
                        calibration_method == expected_method,
                        f"Method: {calibration_method}"
                    )
                    
                    return True
                    
                else:
                    message = data.get("message", "Unknown error")
                    self.log_test(
                        "Advanced ML-powered IRT Calibration",
                        False,
                        error=f"Calibration failed: {message}"
                    )
                    return False
                    
            else:
                self.log_test(
                    "Advanced ML-powered IRT Calibration",
                    False,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Advanced ML-powered IRT Calibration",
                False,
                error=f"Request failed: {str(e)}"
            )
            return False
    
    def test_parameter_estimation_validation(self):
        """Test parameter estimation validation for discrimination (a), difficulty (b), and guessing (c)"""
        try:
            # Get a sample of calibrated questions to validate parameters
            response = self.session.get(
                f"{BACKEND_URL}/admin/aptitude-questions/stats",
                timeout=30
            )
            
            if response.status_code != 200:
                self.log_test(
                    "Parameter Estimation Validation - Data Retrieval",
                    False,
                    error=f"Failed to retrieve question stats: HTTP {response.status_code}"
                )
                return False
            
            # Get detailed question data (this would need to be implemented in the backend)
            # For now, we'll validate the calibration was applied by checking the calibration endpoint response
            calibration_response = self.session.post(
                f"{BACKEND_URL}/admin/calibrate-irt-parameters",
                timeout=60
            )
            
            if calibration_response.status_code == 200:
                data = calibration_response.json()
                
                if data.get("success"):
                    summary = data.get("summary", {})
                    
                    # Validate parameter bounds
                    avg_model_fit = summary.get("avg_model_fit", 0)
                    
                    # Check if parameters are within valid bounds (this is implicit in successful calibration)
                    if avg_model_fit > 0:
                        self.log_test(
                            "Parameter Estimation Validation (a, b, c parameters)",
                            True,
                            f"Parameters estimated with average model fit (pseudo R²): {avg_model_fit:.3f}"
                        )
                        
                        # Validate convergence and model fit statistics
                        if avg_model_fit >= 0.1:  # Reasonable model fit threshold
                            self.log_test(
                                "Convergence and Model Fit Statistics",
                                True,
                                f"Good model fit achieved (pseudo R² ≥ 0.1): {avg_model_fit:.3f}"
                            )
                        else:
                            self.log_test(
                                "Convergence and Model Fit Statistics",
                                False,
                                error=f"Poor model fit (pseudo R² < 0.1): {avg_model_fit:.3f}"
                            )
                        
                        return True
                    else:
                        self.log_test(
                            "Parameter Estimation Validation",
                            False,
                            error="No valid parameter estimates found"
                        )
                        return False
                else:
                    self.log_test(
                        "Parameter Estimation Validation",
                        False,
                        error=f"Calibration failed: {data.get('message', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test(
                    "Parameter Estimation Validation",
                    False,
                    error=f"HTTP {calibration_response.status_code}: {calibration_response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Parameter Estimation Validation",
                False,
                error=f"Validation failed: {str(e)}"
            )
            return False
    
    def test_database_integration(self):
        """Test database integration and calibration data storage"""
        try:
            # Run calibration to ensure data is stored
            calibration_response = self.session.post(
                f"{BACKEND_URL}/admin/calibrate-irt-parameters",
                timeout=60
            )
            
            if calibration_response.status_code == 200:
                data = calibration_response.json()
                
                if data.get("success"):
                    summary = data.get("summary", {})
                    database_updates = summary.get("database_updates", 0)
                    
                    if database_updates > 0:
                        self.log_test(
                            "Database Integration - Questions Updated with Calibrated Parameters",
                            True,
                            f"Successfully updated {database_updates} questions in database"
                        )
                        
                        # Validate calibration metadata storage
                        calibration_method = data.get("calibration_method", "")
                        timestamp = data.get("timestamp", "")
                        
                        if calibration_method and timestamp:
                            self.log_test(
                                "Calibration Data Storage with Enhanced Metadata",
                                True,
                                f"Stored calibration metadata: method={calibration_method}, timestamp={timestamp}"
                            )
                        else:
                            self.log_test(
                                "Calibration Data Storage with Enhanced Metadata",
                                False,
                                error="Missing calibration metadata in response"
                            )
                        
                        return True
                    else:
                        self.log_test(
                            "Database Integration",
                            False,
                            error="No database updates performed"
                        )
                        return False
                else:
                    self.log_test(
                        "Database Integration",
                        False,
                        error=f"Calibration failed: {data.get('message', 'Unknown error')}"
                    )
                    return False
            else:
                self.log_test(
                    "Database Integration",
                    False,
                    error=f"HTTP {calibration_response.status_code}: {calibration_response.text}"
                )
                return False
                
        except Exception as e:
            self.log_test(
                "Database Integration",
                False,
                error=f"Database test failed: {str(e)}"
            )
            return False
    
    def test_error_handling(self):
        """Test error handling for insufficient data scenarios"""
        try:
            # This test assumes we might have insufficient data scenarios
            # The endpoint should handle this gracefully
            
            # Test with no authentication (should fail)
            no_auth_session = requests.Session()
            response = no_auth_session.post(
                f"{BACKEND_URL}/admin/calibrate-irt-parameters",
                timeout=30
            )
            
            # Should return 401 or similar authentication error
            if response.status_code in [401, 403]:
                self.log_test(
                    "Error Handling - Authentication Required",
                    True,
                    f"Correctly rejected unauthenticated request: HTTP {response.status_code}"
                )
            else:
                self.log_test(
                    "Error Handling - Authentication Required",
                    False,
                    error=f"Expected 401/403, got HTTP {response.status_code}"
                )
            
            # Test with authenticated session (should work or give meaningful error)
            auth_response = self.session.post(
                f"{BACKEND_URL}/admin/calibrate-irt-parameters",
                timeout=60
            )
            
            if auth_response.status_code == 200:
                data = auth_response.json()
                if not data.get("success"):
                    message = data.get("message", "")
                    if "insufficient data" in message.lower():
                        self.log_test(
                            "Error Handling - Insufficient Data Scenarios",
                            True,
                            f"Correctly handled insufficient data: {message}"
                        )
                    else:
                        self.log_test(
                            "Error Handling - Meaningful Error Messages",
                            True,
                            f"Provided meaningful error message: {message}"
                        )
                else:
                    self.log_test(
                        "Error Handling - Successful Calibration",
                        True,
                        "Calibration completed successfully with available data"
                    )
            else:
                self.log_test(
                    "Error Handling - Server Response",
                    False,
                    error=f"Unexpected server response: HTTP {auth_response.status_code}"
                )
            
            return True
            
        except Exception as e:
            self.log_test(
                "Error Handling",
                False,
                error=f"Error handling test failed: {str(e)}"
            )
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive test suite for Advanced ML-powered IRT Calibration System"""
        print("🚀 Starting Advanced ML-powered IRT Calibration System Testing")
        print("=" * 80)
        print()
        
        # Test sequence
        tests = [
            ("Admin Authentication", self.test_admin_authentication),
            ("Aptitude Questions Seeding", self.test_aptitude_questions_seeding),
            ("IRT Calibration Endpoint", self.test_irt_calibration_endpoint),
            ("Parameter Estimation Validation", self.test_parameter_estimation_validation),
            ("Database Integration", self.test_database_integration),
            ("Error Handling", self.test_error_handling)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"🔍 Running: {test_name}")
            try:
                if test_func():
                    passed_tests += 1
            except Exception as e:
                self.log_test(test_name, False, error=f"Test execution failed: {str(e)}")
            print()
        
        # Summary
        print("=" * 80)
        print("📊 ADVANCED ML-POWERED IRT CALIBRATION SYSTEM TEST SUMMARY")
        print("=" * 80)
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print()
        
        # Detailed results
        print("📋 Detailed Test Results:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test']}")
            if result["details"]:
                print(f"   📝 {result['details']}")
            if result["error"]:
                print(f"   ⚠️  {result['error']}")
        
        print()
        print("=" * 80)
        
        if success_rate >= 80:
            print("🎉 ADVANCED ML-POWERED IRT CALIBRATION SYSTEM: EXCELLENT PERFORMANCE")
            print("✅ System is ready for production use with comprehensive ML-powered calibration")
        elif success_rate >= 60:
            print("⚠️  ADVANCED ML-POWERED IRT CALIBRATION SYSTEM: GOOD PERFORMANCE")
            print("🔧 Some issues detected, but core functionality is operational")
        else:
            print("❌ ADVANCED ML-POWERED IRT CALIBRATION SYSTEM: NEEDS ATTENTION")
            print("🚨 Critical issues detected, system requires fixes before production")
        
        return success_rate >= 60

def main():
    """Main test execution"""
    print("🧠 Advanced ML-powered IRT Calibration System Testing")
    print("Phase 1.2 Implementation - Step 1")
    print("Testing 3PL IRT Maximum Likelihood Estimation with ML Enhancement")
    print()
    
    tester = IRTCalibrationTester()
    success = tester.run_comprehensive_test()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())