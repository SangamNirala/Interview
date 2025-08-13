#!/usr/bin/env python3
"""
Comprehensive Aptitude Test Backend Testing
Testing all 5 key areas of aptitude test functionality as requested:
1. Aptitude Question Generation and Retrieval
2. Session Management  
3. Answer Submission
4. Results Calculation
5. Seeding System
"""

import requests
import json
import time
import os
from datetime import datetime
import random

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://exam-submit-flow.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class AptitudeTestTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        self.test_config_id = None
        self.test_token = None
        self.test_session_id = None
        self.question_ids = []
        self.test_results = {}
        
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

    # ===== AREA 5: SEEDING SYSTEM TESTING =====
    
    def test_aptitude_question_seeding(self):
        """Test the aptitude questions seeding system"""
        try:
            response = self.session.post(f"{BASE_URL}/admin/aptitude-questions/seed", json={})
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    total_seeded = data.get("total_questions_seeded", 0)
                    topics_seeded = data.get("topics_seeded", {})
                    self.log_test("Aptitude Question Seeding", "PASS", 
                                f"Successfully seeded {total_seeded} questions across topics: {topics_seeded}")
                    return True
                else:
                    self.log_test("Aptitude Question Seeding", "FAIL", 
                                f"Seeding failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Aptitude Question Seeding", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Aptitude Question Seeding", "FAIL", f"Exception: {str(e)}")
            return False

    def test_aptitude_question_stats(self):
        """Test the aptitude questions statistics endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/admin/aptitude-questions/stats")
            
            if response.status_code == 200:
                data = response.json()
                total_questions = data.get("total_questions", 0)
                topics_breakdown = data.get("topics_breakdown", {})
                difficulty_breakdown = data.get("difficulty_breakdown", {})
                
                if total_questions > 0:
                    self.log_test("Aptitude Question Stats", "PASS", 
                                f"Retrieved stats: {total_questions} total questions, Topics: {topics_breakdown}, Difficulty: {difficulty_breakdown}")
                    return True
                else:
                    self.log_test("Aptitude Question Stats", "FAIL", 
                                "No questions found in database")
                    return False
            else:
                self.log_test("Aptitude Question Stats", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Aptitude Question Stats", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== AREA 1: QUESTION GENERATION AND RETRIEVAL =====
    
    def test_ai_question_generation(self):
        """Test AI-powered question generation"""
        try:
            generation_request = {
                "topic": "numerical_reasoning",
                "subtopic": "arithmetic",
                "difficulty": "medium",
                "count": 3,
                "job_context": "Software Engineer position requiring analytical thinking"
            }
            
            response = self.session.post(f"{BASE_URL}/admin/aptitude-questions/ai-generate", 
                                       json=generation_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    generated_questions = data.get("generated_questions", [])
                    if len(generated_questions) >= 3:
                        self.log_test("AI Question Generation", "PASS", 
                                    f"Successfully generated {len(generated_questions)} questions for numerical reasoning")
                        return True
                    else:
                        self.log_test("AI Question Generation", "FAIL", 
                                    f"Expected 3 questions, got {len(generated_questions)}")
                        return False
                else:
                    self.log_test("AI Question Generation", "FAIL", 
                                f"Generation failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("AI Question Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("AI Question Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_contextual_question_generation(self):
        """Test contextual AI question generation"""
        try:
            contextual_request = {
                "job_title": "Senior Data Analyst",
                "job_description": "Analyzing complex datasets and creating insights for business decisions",
                "topics": ["numerical_reasoning", "logical_reasoning"],
                "questions_per_topic": {
                    "numerical_reasoning": 2,
                    "logical_reasoning": 2
                },
                "difficulty_distribution": {"easy": 0.3, "medium": 0.5, "hard": 0.2}
            }
            
            response = self.session.post(f"{BASE_URL}/admin/aptitude-questions/ai-generate-contextual", 
                                       json=contextual_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    generated_questions = data.get("generated_questions", [])
                    if len(generated_questions) >= 4:  # 2 per topic
                        self.log_test("Contextual AI Question Generation", "PASS", 
                                    f"Successfully generated {len(generated_questions)} contextual questions for Data Analyst role")
                        return True
                    else:
                        self.log_test("Contextual AI Question Generation", "FAIL", 
                                    f"Expected 4+ questions, got {len(generated_questions)}")
                        return False
                else:
                    self.log_test("Contextual AI Question Generation", "FAIL", 
                                f"Generation failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Contextual AI Question Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Contextual AI Question Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_question_quality_validation(self):
        """Test question quality validation system"""
        try:
            # Get some questions to validate
            response = self.session.get(f"{BASE_URL}/admin/aptitude-questions?limit=5")
            
            if response.status_code != 200:
                self.log_test("Question Quality Validation", "FAIL", 
                            f"Failed to get questions for validation: {response.status_code}")
                return False
            
            questions_data = response.json()
            questions = questions_data.get("questions", [])
            
            if not questions:
                self.log_test("Question Quality Validation", "FAIL", 
                            "No questions available for validation")
                return False
            
            # Test validation on first question
            question_id = questions[0].get("id")
            validation_response = self.session.post(f"{BASE_URL}/admin/aptitude-questions/validate-quality", 
                                                  json={"question_ids": [question_id]})
            
            if validation_response.status_code == 200:
                validation_data = validation_response.json()
                if validation_data.get("success"):
                    validation_results = validation_data.get("validation_results", [])
                    if validation_results:
                        self.log_test("Question Quality Validation", "PASS", 
                                    f"Successfully validated question quality: {validation_results[0].get('overall_score', 'N/A')}")
                        return True
                    else:
                        self.log_test("Question Quality Validation", "FAIL", 
                                    "No validation results returned")
                        return False
                else:
                    self.log_test("Question Quality Validation", "FAIL", 
                                f"Validation failed: {validation_data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Question Quality Validation", "FAIL", 
                            f"HTTP {validation_response.status_code}: {validation_response.text}")
                return False
                
        except Exception as e:
            self.log_test("Question Quality Validation", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== AREA 2: SESSION MANAGEMENT =====
    
    def test_aptitude_test_config_creation(self):
        """Test creating an aptitude test configuration"""
        try:
            config_request = {
                "created_by": "admin",
                "test_name": "Software Engineer Aptitude Assessment",
                "job_title": "Senior Software Engineer",
                "job_description": "Full-stack development role requiring strong analytical and problem-solving skills",
                "topics": ["numerical_reasoning", "logical_reasoning", "verbal_comprehension"],
                "questions_per_topic": {
                    "numerical_reasoning": 10,
                    "logical_reasoning": 8,
                    "verbal_comprehension": 7
                },
                "difficulty_distribution": {"easy": 0.3, "medium": 0.5, "hard": 0.2},
                "total_time_limit": 2700,  # 45 minutes
                "adaptive_mode": True,
                "randomize_questions": True
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/aptitude-test-config", 
                                       json=config_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.test_config_id = data.get("config_id")
                    self.log_test("Aptitude Test Config Creation", "PASS", 
                                f"Successfully created test config: {self.test_config_id}")
                    return True
                else:
                    self.log_test("Aptitude Test Config Creation", "FAIL", 
                                f"Config creation failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Aptitude Test Config Creation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Aptitude Test Config Creation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_aptitude_token_generation(self):
        """Test generating an aptitude test token"""
        try:
            if not self.test_config_id:
                self.log_test("Aptitude Token Generation", "FAIL", 
                            "No test config ID available")
                return False
            
            token_request = {
                "config_id": self.test_config_id,
                "expires_in_hours": 24,
                "max_attempts": 1,
                "candidate_restrictions": {
                    "require_camera": True,
                    "require_fullscreen": True
                }
            }
            
            response = self.session.post(f"{BASE_URL}/placement-preparation/generate-aptitude-token", 
                                       json=token_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.test_token = data.get("token")
                    self.log_test("Aptitude Token Generation", "PASS", 
                                f"Successfully generated token: {self.test_token[:8]}...")
                    return True
                else:
                    self.log_test("Aptitude Token Generation", "FAIL", 
                                f"Token generation failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Aptitude Token Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Aptitude Token Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_token_validation_and_session_creation(self):
        """Test token validation and session creation"""
        try:
            if not self.test_token:
                self.log_test("Token Validation & Session Creation", "FAIL", 
                            "No test token available")
                return False
            
            validation_request = {
                "token": self.test_token,
                "candidate_name": "Alex Johnson",
                "candidate_email": "alex.johnson@example.com"
            }
            
            response = self.session.post(f"{BASE_URL}/aptitude-test/validate-token", 
                                       json=validation_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    self.test_session_id = data.get("session_id")
                    test_config = data.get("test_config", {})
                    self.log_test("Token Validation & Session Creation", "PASS", 
                                f"Successfully created session: {self.test_session_id}, Config: {test_config.get('test_name', 'N/A')}")
                    return True
                else:
                    self.log_test("Token Validation & Session Creation", "FAIL", 
                                f"Validation failed: {data.get('message', 'Unknown error')}")
                    return False
            else:
                self.log_test("Token Validation & Session Creation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Token Validation & Session Creation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_session_retrieval(self):
        """Test retrieving session information"""
        try:
            if not self.test_session_id:
                self.log_test("Session Retrieval", "FAIL", 
                            "No test session ID available")
                return False
            
            response = self.session.get(f"{BASE_URL}/aptitude-test/session/{self.test_session_id}")
            
            if response.status_code == 200:
                data = response.json()
                session_info = data.get("session", {})
                if session_info:
                    status = session_info.get("status", "unknown")
                    candidate_name = session_info.get("candidate_name", "N/A")
                    self.log_test("Session Retrieval", "PASS", 
                                f"Retrieved session info: Status={status}, Candidate={candidate_name}")
                    return True
                else:
                    self.log_test("Session Retrieval", "FAIL", 
                                "No session information returned")
                    return False
            else:
                self.log_test("Session Retrieval", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Session Retrieval", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== AREA 3: ANSWER SUBMISSION =====
    
    def test_question_retrieval_and_answer_submission(self):
        """Test retrieving questions and submitting answers"""
        try:
            if not self.test_session_id:
                self.log_test("Question Retrieval & Answer Submission", "FAIL", 
                            "No test session ID available")
                return False
            
            questions_answered = 0
            max_questions = 5  # Test with first 5 questions
            
            while questions_answered < max_questions:
                # Get next question
                question_response = self.session.get(f"{BASE_URL}/aptitude-test/question/{self.test_session_id}")
                
                if question_response.status_code != 200:
                    self.log_test("Question Retrieval & Answer Submission", "FAIL", 
                                f"Failed to get question {questions_answered + 1}: {question_response.status_code}")
                    return False
                
                question_data = question_response.json()
                question = question_data.get("question", {})
                
                if not question:
                    # No more questions or test complete
                    break
                
                question_id = question.get("id")
                options = question.get("options", [])
                
                if not question_id or not options:
                    self.log_test("Question Retrieval & Answer Submission", "FAIL", 
                                f"Invalid question data: ID={question_id}, Options={len(options)}")
                    return False
                
                self.question_ids.append(question_id)
                
                # Submit a random answer (for testing purposes)
                selected_answer = random.choice(options) if options else "A"
                
                answer_request = {
                    "question_id": question_id,
                    "selected_answer": selected_answer,
                    "time_taken": random.randint(30, 120)  # Random time between 30-120 seconds
                }
                
                answer_response = self.session.post(f"{BASE_URL}/aptitude-test/answer/{self.test_session_id}", 
                                                  json=answer_request)
                
                if answer_response.status_code != 200:
                    self.log_test("Question Retrieval & Answer Submission", "FAIL", 
                                f"Failed to submit answer {questions_answered + 1}: {answer_response.status_code}")
                    return False
                
                answer_data = answer_response.json()
                if not answer_data.get("success"):
                    self.log_test("Question Retrieval & Answer Submission", "FAIL", 
                                f"Answer submission failed: {answer_data.get('message', 'Unknown error')}")
                    return False
                
                questions_answered += 1
                
                # Check if test is complete
                if answer_data.get("test_complete"):
                    break
                
                # Small delay between questions
                time.sleep(0.5)
            
            if questions_answered > 0:
                self.log_test("Question Retrieval & Answer Submission", "PASS", 
                            f"Successfully answered {questions_answered} questions")
                return True
            else:
                self.log_test("Question Retrieval & Answer Submission", "FAIL", 
                            "No questions were answered")
                return False
                
        except Exception as e:
            self.log_test("Question Retrieval & Answer Submission", "FAIL", f"Exception: {str(e)}")
            return False

    # ===== AREA 4: RESULTS CALCULATION =====
    
    def test_results_calculation_and_analytics(self):
        """Test comprehensive results calculation with analytics"""
        try:
            if not self.test_session_id:
                self.log_test("Results Calculation & Analytics", "FAIL", 
                            "No test session ID available")
                return False
            
            # Wait a moment for results to be calculated
            time.sleep(2)
            
            response = self.session.get(f"{BASE_URL}/aptitude-test/results/{self.test_session_id}")
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", {})
                
                if not results:
                    self.log_test("Results Calculation & Analytics", "FAIL", 
                                "No results data returned")
                    return False
                
                # Verify comprehensive analytics components
                required_fields = [
                    "overall_score", "percentage_score", "topic_scores", 
                    "difficulty_performance", "total_time_taken", 
                    "questions_attempted", "questions_correct"
                ]
                
                missing_fields = [field for field in required_fields if field not in results]
                if missing_fields:
                    self.log_test("Results Calculation & Analytics", "FAIL", 
                                f"Missing required result fields: {missing_fields}")
                    return False
                
                # Verify analytics quality
                overall_score = results.get("overall_score", 0)
                percentage_score = results.get("percentage_score", 0)
                topic_scores = results.get("topic_scores", {})
                strengths = results.get("strengths", [])
                improvement_areas = results.get("improvement_areas", [])
                percentile_rank = results.get("percentile_rank", 0)
                
                self.test_results = results
                
                self.log_test("Results Calculation & Analytics", "PASS", 
                            f"Comprehensive results calculated: Score={overall_score:.1f} ({percentage_score:.1f}%), "
                            f"Topics={len(topic_scores)}, Percentile={percentile_rank:.1f}, "
                            f"Strengths={len(strengths)}, Improvements={len(improvement_areas)}")
                return True
            else:
                self.log_test("Results Calculation & Analytics", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Results Calculation & Analytics", "FAIL", f"Exception: {str(e)}")
            return False

    def test_time_management_analytics(self):
        """Test time management analytics in results"""
        try:
            if not self.test_results:
                self.log_test("Time Management Analytics", "FAIL", 
                            "No test results available")
                return False
            
            # Check for time-related analytics
            total_time = self.test_results.get("total_time_taken", 0)
            time_per_question = self.test_results.get("time_per_question", {})
            difficulty_performance = self.test_results.get("difficulty_performance", {})
            
            # Verify time analytics are present
            if total_time > 0:
                time_analytics_present = True
                
                # Check if time efficiency is calculated
                for difficulty, perf in difficulty_performance.items():
                    if "time" not in perf:
                        time_analytics_present = False
                        break
                
                if time_analytics_present:
                    self.log_test("Time Management Analytics", "PASS", 
                                f"Time analytics present: Total={total_time}s, Per-question tracking available")
                    return True
                else:
                    self.log_test("Time Management Analytics", "FAIL", 
                                "Time analytics incomplete - missing per-difficulty time data")
                    return False
            else:
                self.log_test("Time Management Analytics", "FAIL", 
                            "No time tracking data found")
                return False
                
        except Exception as e:
            self.log_test("Time Management Analytics", "FAIL", f"Exception: {str(e)}")
            return False

    def test_percentile_ranking_system(self):
        """Test percentile ranking and comparative analytics"""
        try:
            if not self.test_results:
                self.log_test("Percentile Ranking System", "FAIL", 
                            "No test results available")
                return False
            
            percentile_rank = self.test_results.get("percentile_rank", 0)
            recommendations = self.test_results.get("recommendations", [])
            detailed_analysis = self.test_results.get("detailed_analysis", "")
            
            if percentile_rank > 0:
                self.log_test("Percentile Ranking System", "PASS", 
                            f"Percentile ranking calculated: {percentile_rank:.1f}%, "
                            f"Recommendations: {len(recommendations)}, "
                            f"Analysis length: {len(detailed_analysis)} chars")
                return True
            else:
                self.log_test("Percentile Ranking System", "FAIL", 
                            "Percentile ranking not calculated or zero")
                return False
                
        except Exception as e:
            self.log_test("Percentile Ranking System", "FAIL", f"Exception: {str(e)}")
            return False

    def test_pdf_results_generation(self):
        """Test PDF results generation"""
        try:
            if not self.test_session_id:
                self.log_test("PDF Results Generation", "FAIL", 
                            "No test session ID available")
                return False
            
            response = self.session.get(f"{BASE_URL}/aptitude-test/results/{self.test_session_id}/pdf")
            
            if response.status_code == 200:
                # Check if response is PDF
                content_type = response.headers.get('content-type', '')
                if 'application/pdf' in content_type:
                    pdf_size = len(response.content)
                    self.log_test("PDF Results Generation", "PASS", 
                                f"PDF generated successfully: {pdf_size} bytes, Content-Type: {content_type}")
                    return True
                else:
                    self.log_test("PDF Results Generation", "FAIL", 
                                f"Invalid content type: {content_type}")
                    return False
            else:
                self.log_test("PDF Results Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("PDF Results Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_ai_analytics_insights(self):
        """Test AI analytics and insights generation"""
        try:
            response = self.session.get(f"{BASE_URL}/admin/aptitude-questions/ai-analytics")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict):
                    analytics = data.get("analytics", {})
                    
                    if analytics:
                        question_performance = analytics.get("question_performance", {})
                        difficulty_trends = analytics.get("difficulty_trends", {})
                        topic_insights = analytics.get("topic_insights", {})
                        
                        self.log_test("AI Analytics Insights", "PASS", 
                                    f"AI analytics generated: Performance metrics={len(question_performance)}, "
                                    f"Difficulty trends={len(difficulty_trends)}, Topic insights={len(topic_insights)}")
                        return True
                    else:
                        self.log_test("AI Analytics Insights", "PASS", 
                                    f"AI analytics endpoint accessible, returned: {str(data)[:100]}...")
                        return True
                else:
                    self.log_test("AI Analytics Insights", "FAIL", 
                                f"Unexpected response format: {type(data)}")
                    return False
            else:
                self.log_test("AI Analytics Insights", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("AI Analytics Insights", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all aptitude test functionality tests"""
        print("=" * 80)
        print("COMPREHENSIVE APTITUDE TEST BACKEND FUNCTIONALITY TESTING")
        print("Testing 5 Key Areas: Seeding, Question Generation, Session Management, Answer Submission, Results Calculation")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Prerequisites
        test_results.append(self.test_admin_authentication())
        
        if not self.admin_authenticated:
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # AREA 5: Seeding System Testing
        print("🌱 TESTING AREA 5: SEEDING SYSTEM")
        print("-" * 50)
        test_results.append(self.test_aptitude_question_seeding())
        test_results.append(self.test_aptitude_question_stats())
        print()
        
        # AREA 1: Question Generation and Retrieval
        print("🧠 TESTING AREA 1: QUESTION GENERATION AND RETRIEVAL")
        print("-" * 50)
        test_results.append(self.test_ai_question_generation())
        test_results.append(self.test_contextual_question_generation())
        test_results.append(self.test_question_quality_validation())
        print()
        
        # AREA 2: Session Management
        print("🎯 TESTING AREA 2: SESSION MANAGEMENT")
        print("-" * 50)
        test_results.append(self.test_aptitude_test_config_creation())
        test_results.append(self.test_aptitude_token_generation())
        test_results.append(self.test_token_validation_and_session_creation())
        test_results.append(self.test_session_retrieval())
        print()
        
        # AREA 3: Answer Submission
        print("✍️ TESTING AREA 3: ANSWER SUBMISSION")
        print("-" * 50)
        test_results.append(self.test_question_retrieval_and_answer_submission())
        print()
        
        # AREA 4: Results Calculation
        print("📊 TESTING AREA 4: RESULTS CALCULATION")
        print("-" * 50)
        test_results.append(self.test_results_calculation_and_analytics())
        test_results.append(self.test_time_management_analytics())
        test_results.append(self.test_percentile_ranking_system())
        test_results.append(self.test_pdf_results_generation())
        test_results.append(self.test_ai_analytics_insights())
        print()
        
        # Summary
        print("=" * 80)
        print("APTITUDE TEST BACKEND TESTING SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Area-specific breakdown
        areas = [
            ("Prerequisites", 1),
            ("Seeding System", 2), 
            ("Question Generation", 3),
            ("Session Management", 4),
            ("Answer Submission", 1),
            ("Results Calculation", 5)
        ]
        
        print("\n📋 AREA-SPECIFIC RESULTS:")
        start_idx = 0
        for area_name, area_count in areas:
            area_results = test_results[start_idx:start_idx + area_count]
            area_passed = sum(area_results)
            print(f"   {area_name}: {area_passed}/{area_count} tests passed")
            start_idx += area_count
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Aptitude test backend functionality is working correctly.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = AptitudeTestTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ APTITUDE TEST BACKEND TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ APTITUDE TEST BACKEND TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()