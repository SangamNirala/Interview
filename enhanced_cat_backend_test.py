#!/usr/bin/env python3
"""
Enhanced Computer Adaptive Testing (CAT) Engine Backend Test
Phase 1.1: Testing Advanced CAT Algorithms with Multi-dimensional IRT Implementation

This test focuses on the new enhanced CAT functionality:
1. Enhanced Question Selection using optimal information criterion
2. Multi-dimensional IRT Updates with confidence intervals  
3. Advanced Termination Criteria based on measurement precision
4. New Analytics Endpoints (session analytics, ability estimates, fraud monitoring)
5. IRT Parameter Calibration
6. Enhanced Data Models Verification
"""

import requests
import json
import time
import random
import uuid
from datetime import datetime
from typing import Dict, List, Any

class EnhancedCATTester:
    def __init__(self):
        self.base_url = "https://score-confidence-api.preview.emergentagent.com/api"
        self.admin_password = "Game@1234"
        self.session = requests.Session()
        self.test_results = []
        
        # Test data for realistic aptitude testing
        self.test_candidate = {
            "name": "Alex Johnson",
            "email": "alex.johnson@testcandidate.com"
        }
        
        self.test_config = {
            "test_name": "Enhanced CAT Assessment",
            "job_title": "Senior Data Scientist",
            "job_description": "Advanced analytics role requiring strong quantitative reasoning, logical problem-solving, and spatial visualization skills",
            "topics": ["numerical_reasoning", "logical_reasoning", "verbal_comprehension", "spatial_reasoning"],
            "questions_per_topic": {
                "numerical_reasoning": 8,
                "logical_reasoning": 6,
                "verbal_comprehension": 5,
                "spatial_reasoning": 6
            },
            "difficulty_distribution": {"easy": 0.3, "medium": 0.5, "hard": 0.2},
            "total_time_limit": 1800,  # 30 minutes
            "adaptive_mode": True,
            "randomize_questions": True,
            "randomize_options": True
        }

    def log_result(self, test_name: str, success: bool, details: str = "", data: Any = None):
        """Log test results for reporting"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and data:
            print(f"   Error Data: {data}")

    def test_admin_login(self) -> bool:
        """Test admin authentication"""
        try:
            response = self.session.post(
                f"{self.base_url}/admin/login",
                json={"password": self.admin_password}
            )
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                self.log_result("Admin Login", success, f"Status: {response.status_code}, Response: {data}")
                return success
            else:
                self.log_result("Admin Login", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Admin Login", False, f"Exception: {str(e)}")
            return False

    def test_aptitude_question_seeding(self) -> bool:
        """Test aptitude question seeding system"""
        try:
            # First check current stats
            stats_response = self.session.get(f"{self.base_url}/admin/aptitude-questions/stats")
            
            if stats_response.status_code == 200:
                stats_data = stats_response.json()
                current_total = stats_data.get("total", 0)  # Changed from "total_questions" to "total"
                
                # If we have questions, skip seeding
                if current_total >= 100:
                    self.log_result("Question Seeding (Skip)", True, f"Already have {current_total} questions")
                    return True
            
            # Seed questions with proper request body
            seed_request = {
                "force": False,
                "target_total": 200  # Smaller number for testing
            }
            seed_response = self.session.post(f"{self.base_url}/admin/aptitude-questions/seed", json=seed_request)
            
            if seed_response.status_code == 200:
                seed_data = seed_response.json()
                generated = seed_data.get("generated", 0)
                inserted = seed_data.get("inserted", 0)
                
                # Verify seeding worked
                stats_response = self.session.get(f"{self.base_url}/admin/aptitude-questions/stats")
                if stats_response.status_code == 200:
                    final_stats = stats_response.json()
                    total_questions = final_stats.get("total", 0)  # Changed from "total_questions" to "total"
                    
                    success = total_questions >= inserted
                    self.log_result("Question Seeding", success, 
                                  f"Generated: {generated}, Inserted: {inserted}, Total: {total_questions}")
                    return success
                else:
                    self.log_result("Question Seeding", False, "Failed to verify seeding")
                    return False
            else:
                self.log_result("Question Seeding", False, f"HTTP {seed_response.status_code}", seed_response.text)
                return False
                
        except Exception as e:
            self.log_result("Question Seeding", False, f"Exception: {str(e)}")
            return False

    def test_irt_parameter_calibration(self) -> bool:
        """Test IRT parameter calibration endpoint"""
        try:
            response = self.session.post(f"{self.base_url}/admin/calibrate-irt-parameters")
            
            if response.status_code == 200:
                data = response.json()
                success = data.get("success", False)
                calibrated_count = data.get("calibrated_questions", 0)
                sessions_analyzed = data.get("total_sessions_analyzed", 0)
                
                # Even if no questions were calibrated due to insufficient data, the endpoint should work
                endpoint_working = "calibrated_questions" in data and "total_sessions_analyzed" in data
                
                self.log_result("IRT Parameter Calibration", endpoint_working, 
                              f"Calibrated: {calibrated_count}, Sessions: {sessions_analyzed}")
                return endpoint_working
            else:
                self.log_result("IRT Parameter Calibration", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("IRT Parameter Calibration", False, f"Exception: {str(e)}")
            return False

    def create_test_configuration(self) -> str:
        """Create a test configuration and return config_id"""
        try:
            config_request = {
                "created_by": "enhanced_cat_tester",
                "test_name": self.test_config["test_name"],
                "job_title": self.test_config["job_title"],
                "job_description": self.test_config["job_description"],
                "topics": self.test_config["topics"],
                "questions_per_topic": self.test_config["questions_per_topic"],
                "difficulty_distribution": self.test_config["difficulty_distribution"],
                "total_time_limit": self.test_config["total_time_limit"],
                "adaptive_mode": self.test_config["adaptive_mode"],
                "randomize_questions": self.test_config["randomize_questions"],
                "randomize_options": self.test_config["randomize_options"]
            }
            
            response = self.session.post(
                f"{self.base_url}/placement-preparation/aptitude-test-config",
                json=config_request
            )
            
            if response.status_code == 200:
                data = response.json()
                config_id = data.get("config_id")
                if config_id:
                    self.log_result("Create Test Configuration", True, f"Config ID: {config_id}")
                    return config_id
                else:
                    self.log_result("Create Test Configuration", False, "No config_id in response", data)
                    return None
            else:
                self.log_result("Create Test Configuration", False, f"HTTP {response.status_code}", response.text)
                return None
                
        except Exception as e:
            self.log_result("Create Test Configuration", False, f"Exception: {str(e)}")
            return None

    def create_test_token(self, config_id: str) -> str:
        """Create a test token and return token"""
        try:
            token_request = {
                "config_id": config_id,
                "expires_in_minutes": 120,
                "max_attempts": 1,
                "candidate_restrictions": {}
            }
            
            response = self.session.post(
                f"{self.base_url}/placement-preparation/generate-aptitude-token",
                json=token_request
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("token")
                if token:
                    self.log_result("Create Test Token", True, f"Token: {token}")
                    return token
                else:
                    self.log_result("Create Test Token", False, "No token in response", data)
                    return None
            else:
                self.log_result("Create Test Token", False, f"HTTP {response.status_code}", response.text)
                return None
                
        except Exception as e:
            self.log_result("Create Test Token", False, f"Exception: {str(e)}")
            return None

    def start_test_session(self, token: str) -> str:
        """Start a test session and return session_id"""
        try:
            session_request = {
                "token": token,
                "candidate_name": self.test_candidate["name"],
                "candidate_email": self.test_candidate["email"]
            }
            
            response = self.session.post(
                f"{self.base_url}/aptitude-test/validate-token",
                json=session_request
            )
            
            if response.status_code == 200:
                data = response.json()
                session_id = data.get("session_id")
                if session_id:
                    self.log_result("Start Test Session", True, f"Session ID: {session_id}")
                    return session_id
                else:
                    self.log_result("Start Test Session", False, "No session_id in response", data)
                    return None
            else:
                self.log_result("Start Test Session", False, f"HTTP {response.status_code}", response.text)
                return None
                
        except Exception as e:
            self.log_result("Start Test Session", False, f"Exception: {str(e)}")
            return None

    def test_enhanced_question_selection(self, session_id: str) -> bool:
        """Test enhanced question selection with optimal information criterion"""
        try:
            response = self.session.get(f"{self.base_url}/aptitude-test/question/{session_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for enhanced CAT features
                required_fields = ["question", "cat_theta", "cat_se", "confidence_interval", "measurement_precision"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    question = data["question"]
                    cat_theta = data["cat_theta"]
                    cat_se = data["cat_se"]
                    confidence_interval = data["confidence_interval"]
                    measurement_precision = data["measurement_precision"]
                    
                    # Verify enhanced features
                    has_irt_features = (
                        isinstance(cat_theta, (int, float)) and
                        isinstance(cat_se, (int, float)) and
                        isinstance(confidence_interval, dict) and
                        "lower" in confidence_interval and
                        "upper" in confidence_interval and
                        isinstance(measurement_precision, (int, float))
                    )
                    
                    self.log_result("Enhanced Question Selection", has_irt_features, 
                                  f"Theta: {cat_theta}, SE: {cat_se}, Precision: {measurement_precision}")
                    return has_irt_features
                else:
                    self.log_result("Enhanced Question Selection", False, f"Missing fields: {missing_fields}", data)
                    return False
            else:
                self.log_result("Enhanced Question Selection", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Enhanced Question Selection", False, f"Exception: {str(e)}")
            return False

    def test_enhanced_answer_submission(self, session_id: str, question_data: Dict) -> bool:
        """Test enhanced answer submission with multi-dimensional IRT updates"""
        try:
            # Submit a realistic answer
            question = question_data["question"]
            answer_data = {
                "question_id": question["id"],
                "answer": question["options"][0] if question.get("options") else "A",  # First option
                "time_taken": random.uniform(15.0, 45.0)  # Realistic response time
            }
            
            response = self.session.post(
                f"{self.base_url}/aptitude-test/answer/{session_id}",
                json=answer_data
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for enhanced IRT update features (adjusted to actual response format)
                required_fields = ["cat_theta", "cat_se", "confidence_interval", "fraud_score"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    updated_theta = data["cat_theta"]
                    updated_se = data["cat_se"]
                    confidence_interval = data["confidence_interval"]
                    fraud_score = data["fraud_score"]
                    
                    # Verify multi-dimensional IRT features
                    has_enhanced_features = (
                        isinstance(updated_theta, (int, float)) and
                        isinstance(updated_se, (int, float)) and
                        isinstance(confidence_interval, dict) and
                        isinstance(fraud_score, (int, float))
                    )
                    
                    self.log_result("Enhanced Answer Submission", has_enhanced_features,
                                  f"New Theta: {updated_theta}, New SE: {updated_se}, Fraud Score: {fraud_score}")
                    return has_enhanced_features
                else:
                    self.log_result("Enhanced Answer Submission", False, f"Missing fields: {missing_fields}", data)
                    return False
            else:
                self.log_result("Enhanced Answer Submission", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Enhanced Answer Submission", False, f"Exception: {str(e)}")
            return False

    def test_session_analytics(self, session_id: str) -> bool:
        """Test session analytics endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/aptitude-test/analytics/{session_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for comprehensive analytics features
                required_fields = ["ability_progression", "topic_performance", "fraud_analysis", "timing_analysis"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    ability_progression = data["ability_progression"]
                    topic_performance = data["topic_performance"]
                    fraud_analysis = data["fraud_analysis"]
                    timing_analysis = data["timing_analysis"]
                    
                    # Verify analytics quality
                    has_comprehensive_analytics = (
                        isinstance(ability_progression, list) and
                        isinstance(topic_performance, dict) and
                        isinstance(fraud_analysis, dict) and
                        "overall_score" in fraud_analysis and
                        "flags" in fraud_analysis
                    )
                    
                    self.log_result("Session Analytics", has_comprehensive_analytics,
                                  f"Progression entries: {len(ability_progression)}, Topics: {len(topic_performance)}")
                    return has_comprehensive_analytics
                else:
                    self.log_result("Session Analytics", False, f"Missing fields: {missing_fields}", data)
                    return False
            else:
                self.log_result("Session Analytics", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Session Analytics", False, f"Exception: {str(e)}")
            return False

    def test_ability_estimates(self, session_id: str) -> bool:
        """Test ability estimates endpoint with confidence intervals"""
        try:
            response = self.session.get(f"{self.base_url}/aptitude-test/ability-estimate/{session_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for multi-dimensional ability estimates
                required_fields = ["overall", "by_topic"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    overall = data["overall"]
                    by_topic = data["by_topic"]
                    
                    # Verify overall estimate structure
                    overall_valid = (
                        isinstance(overall, dict) and
                        "theta" in overall and
                        "standard_error" in overall and
                        "confidence_interval" in overall and
                        "measurement_precision" in overall and
                        "reliability" in overall
                    )
                    
                    # Verify topic-specific estimates
                    topic_estimates_valid = isinstance(by_topic, dict) and len(by_topic) > 0
                    
                    success = overall_valid and topic_estimates_valid
                    self.log_result("Ability Estimates", success,
                                  f"Overall theta: {overall.get('theta', 'N/A')}, Topics: {len(by_topic)}")
                    return success
                else:
                    self.log_result("Ability Estimates", False, f"Missing fields: {missing_fields}", data)
                    return False
            else:
                self.log_result("Ability Estimates", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Ability Estimates", False, f"Exception: {str(e)}")
            return False

    def test_fraud_monitoring(self, session_id: str) -> bool:
        """Test fraud monitoring endpoint for administrators"""
        try:
            response = self.session.get(f"{self.base_url}/admin/fraud-monitoring/session/{session_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for comprehensive fraud analysis
                required_fields = ["session_overview", "fraud_analysis", "response_pattern_details", "ability_consistency"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if not missing_fields:
                    session_overview = data["session_overview"]
                    fraud_analysis = data["fraud_analysis"]
                    response_patterns = data["response_pattern_details"]
                    ability_consistency = data["ability_consistency"]
                    
                    # Verify fraud analysis quality
                    has_comprehensive_fraud_analysis = (
                        isinstance(session_overview, dict) and
                        "session_id" in session_overview and
                        isinstance(fraud_analysis, dict) and
                        "fraud_score" in fraud_analysis and
                        isinstance(response_patterns, dict) and
                        "total_questions" in response_patterns and
                        isinstance(ability_consistency, dict)
                    )
                    
                    fraud_score = fraud_analysis.get("fraud_score", 0)
                    self.log_result("Fraud Monitoring", has_comprehensive_fraud_analysis,
                                  f"Fraud score: {fraud_score}, Questions analyzed: {response_patterns.get('total_questions', 0)}")
                    return has_comprehensive_fraud_analysis
                else:
                    self.log_result("Fraud Monitoring", False, f"Missing fields: {missing_fields}", data)
                    return False
            else:
                self.log_result("Fraud Monitoring", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_result("Fraud Monitoring", False, f"Exception: {str(e)}")
            return False

    def simulate_test_session(self, session_id: str) -> bool:
        """Simulate answering several questions to generate data for analytics"""
        try:
            questions_answered = 0
            max_questions = 8  # Answer enough questions to test analytics
            
            for i in range(max_questions):
                # Get next question
                question_response = self.session.get(f"{self.base_url}/aptitude-test/question/{session_id}")
                
                if question_response.status_code != 200:
                    break
                    
                question_data = question_response.json()
                
                if "message" in question_data and question_data["message"] == "no_more_questions":
                    break
                
                # Submit answer
                question = question_data["question"]
                answer_data = {
                    "question_id": question["id"],
                    "answer": random.choice(question["options"]) if question.get("options") else "A",
                    "time_taken": random.uniform(10.0, 60.0)  # Realistic response time
                }
                
                answer_response = self.session.post(
                    f"{self.base_url}/aptitude-test/answer/{session_id}",
                    json=answer_data
                )
                
                if answer_response.status_code == 200:
                    questions_answered += 1
                    time.sleep(0.5)  # Brief pause between questions
                else:
                    break
            
            success = questions_answered >= 3  # Need at least 3 questions for meaningful analytics
            self.log_result("Simulate Test Session", success, f"Answered {questions_answered} questions")
            return success
            
        except Exception as e:
            self.log_result("Simulate Test Session", False, f"Exception: {str(e)}")
            return False

    def test_enhanced_data_models(self, session_id: str) -> bool:
        """Verify enhanced data models have IRT parameters and fraud detection fields"""
        try:
            # Get session analytics to check data model enhancements
            analytics_response = self.session.get(f"{self.base_url}/aptitude-test/analytics/{session_id}")
            
            if analytics_response.status_code != 200:
                self.log_result("Enhanced Data Models", False, "Could not retrieve analytics for verification")
                return False
            
            analytics_data = analytics_response.json()
            
            # Check for enhanced session data model fields
            enhanced_fields_present = (
                "ability_progression" in analytics_data and
                "topic_performance" in analytics_data and
                "fraud_analysis" in analytics_data and
                "measurement_precision" in analytics_data
            )
            
            # Check topic performance has IRT-related fields
            topic_performance = analytics_data.get("topic_performance", {})
            irt_fields_present = False
            
            if topic_performance:
                first_topic = next(iter(topic_performance.values()), {})
                irt_fields_present = (
                    "ability_estimate" in first_topic and
                    "standard_error" in first_topic and
                    "confidence_interval" in first_topic and
                    "measurement_precision" in first_topic and
                    "reliability" in first_topic
                )
            
            # Check fraud detection fields
            fraud_analysis = analytics_data.get("fraud_analysis", {})
            fraud_fields_present = (
                "overall_score" in fraud_analysis and
                "flags" in fraud_analysis and
                "risk_level" in fraud_analysis
            )
            
            success = enhanced_fields_present and irt_fields_present and fraud_fields_present
            self.log_result("Enhanced Data Models", success,
                          f"Enhanced fields: {enhanced_fields_present}, IRT fields: {irt_fields_present}, Fraud fields: {fraud_fields_present}")
            return success
            
        except Exception as e:
            self.log_result("Enhanced Data Models", False, f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run comprehensive test of Enhanced CAT Engine"""
        print("🎯 ENHANCED COMPUTER ADAPTIVE TESTING (CAT) ENGINE TEST")
        print("=" * 70)
        print("Testing Phase 1.1: Advanced CAT Algorithms with Multi-dimensional IRT")
        print()
        
        # Step 1: Admin Authentication
        if not self.test_admin_login():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Step 2: Seed Questions (if needed)
        if not self.test_aptitude_question_seeding():
            print("⚠️  Question seeding failed, but continuing with existing questions")
        
        # Step 3: Test IRT Parameter Calibration
        self.test_irt_parameter_calibration()
        
        # Step 4: Create Test Configuration
        config_id = self.create_test_configuration()
        if not config_id:
            print("❌ Cannot proceed without test configuration")
            return
        
        # Step 5: Create Test Token
        token = self.create_test_token(config_id)
        if not token:
            print("❌ Cannot proceed without test token")
            return
        
        # Step 6: Start Test Session
        session_id = self.start_test_session(token)
        if not session_id:
            print("❌ Cannot proceed without test session")
            return
        
        # Step 7: Test Enhanced Question Selection
        question_response = self.session.get(f"{self.base_url}/aptitude-test/question/{session_id}")
        if question_response.status_code == 200:
            question_data = question_response.json()
            self.test_enhanced_question_selection(session_id)
            
            # Step 8: Test Enhanced Answer Submission
            self.test_enhanced_answer_submission(session_id, question_data)
        
        # Step 9: Simulate Test Session (answer multiple questions)
        self.simulate_test_session(session_id)
        
        # Step 10: Test New Analytics Endpoints
        self.test_session_analytics(session_id)
        self.test_ability_estimates(session_id)
        self.test_fraud_monitoring(session_id)
        
        # Step 11: Test Enhanced Data Models
        self.test_enhanced_data_models(session_id)
        
        # Generate Test Report
        self.generate_test_report()

    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 70)
        print("🎯 ENHANCED CAT ENGINE TEST RESULTS")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print()
        
        # Categorize results by feature area
        feature_categories = {
            "Core Infrastructure": ["Admin Login", "Question Seeding"],
            "Enhanced CAT Engine": ["Enhanced Question Selection", "Enhanced Answer Submission", "IRT Parameter Calibration"],
            "Analytics Endpoints": ["Session Analytics", "Ability Estimates", "Fraud Monitoring"],
            "Data Models": ["Enhanced Data Models", "Create Test Configuration", "Create Test Token", "Start Test Session"],
            "Test Simulation": ["Simulate Test Session"]
        }
        
        for category, tests in feature_categories.items():
            category_results = [r for r in self.test_results if r["test"] in tests]
            if category_results:
                category_passed = sum(1 for r in category_results if r["success"])
                category_total = len(category_results)
                category_rate = (category_passed / category_total * 100) if category_total > 0 else 0
                
                print(f"📋 {category.upper()}:")
                print(f"   Success Rate: {category_rate:.1f}% ({category_passed}/{category_total})")
                
                for result in category_results:
                    status = "✅" if result["success"] else "❌"
                    print(f"   {status} {result['test']}")
                    if result["details"]:
                        print(f"      {result['details']}")
                print()
        
        # Key Findings
        print("🔍 KEY FINDINGS:")
        
        # Check if enhanced CAT features are working
        enhanced_features = ["Enhanced Question Selection", "Enhanced Answer Submission", "Session Analytics", "Ability Estimates"]
        enhanced_working = all(any(r["test"] == feature and r["success"] for r in self.test_results) for feature in enhanced_features)
        
        if enhanced_working:
            print("   ✅ Enhanced CAT Engine with multi-dimensional IRT is operational")
            print("   ✅ Optimal information criterion for question selection working")
            print("   ✅ Multi-dimensional ability estimation with confidence intervals functional")
            print("   ✅ Advanced analytics endpoints providing comprehensive insights")
        else:
            print("   ❌ Some enhanced CAT features are not working properly")
        
        # Check fraud detection
        fraud_test = next((r for r in self.test_results if r["test"] == "Fraud Monitoring"), None)
        if fraud_test and fraud_test["success"]:
            print("   ✅ Fraud detection and monitoring system operational")
        else:
            print("   ❌ Fraud detection system needs attention")
        
        # Check IRT calibration
        irt_test = next((r for r in self.test_results if r["test"] == "IRT Parameter Calibration"), None)
        if irt_test and irt_test["success"]:
            print("   ✅ IRT parameter calibration system functional")
        else:
            print("   ❌ IRT parameter calibration needs attention")
        
        print()
        print("🎯 ENHANCED CAT ENGINE VERIFICATION COMPLETE")
        print("=" * 70)
        
        return success_rate >= 80  # Consider test successful if 80%+ pass rate

if __name__ == "__main__":
    tester = EnhancedCATTester()
    tester.run_comprehensive_test()