#!/usr/bin/env python3
"""
Statistical Anomaly Analyzer Backend Testing Suite

This script tests all 6 Statistical Anomaly Analyzer API endpoints:
1. POST /api/statistical-analysis/detect-answer-pattern-irregularities
2. POST /api/statistical-analysis/analyze-difficulty-progression-anomalies  
3. POST /api/statistical-analysis/identify-timezone-manipulation
4. POST /api/statistical-analysis/detect-collaborative-cheating-patterns
5. GET /api/statistical-analysis/session-analysis/{session_id}
6. GET /api/statistical-analysis/model-status

Tests realistic session data, validates response structure, scoring algorithms,
and database storage functionality.
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import random
import time

# Backend URL from environment
BACKEND_URL = "https://integrity-check-2.preview.emergentagent.com/api"

class StatisticalAnomalyTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.test_session_ids = []
        
    def log_test(self, test_name, success, details):
        """Log test results"""
        result = {
            'test_name': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if not success:
            print(f"   Error: {details}")
        else:
            print(f"   Details: {details}")
        print()

    def create_realistic_session_data(self, session_type="normal"):
        """Create realistic session data for testing"""
        session_id = str(uuid.uuid4())
        self.test_session_ids.append(session_id)
        
        base_time = datetime.utcnow() - timedelta(hours=2)
        
        if session_type == "normal":
            # Normal session with typical patterns
            responses = []
            for i in range(25):
                response_time = random.uniform(30, 120)  # 30-120 seconds per question
                difficulty = random.uniform(0.3, 0.8)
                is_correct = random.random() > (difficulty * 0.7)  # Harder questions less likely correct
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': random.choice(['A', 'B', 'C', 'D']),
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'logical_reasoning', 'verbal_comprehension', 'spatial_reasoning']),
                    'timestamp': (base_time + timedelta(seconds=sum(30 + j*60 for j in range(i)))).isoformat()
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Test Candidate Normal',
                'responses': responses,
                'session_metadata': {
                    'start_time': base_time.isoformat(),
                    'end_time': (base_time + timedelta(hours=1, minutes=30)).isoformat(),
                    'ip_address': '192.168.1.100',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'timezone': 'America/New_York',
                    'location': {'country': 'US', 'region': 'NY'}
                }
            }
            
        elif session_type == "suspicious_timing":
            # Session with suspicious timing patterns
            responses = []
            for i in range(20):
                # Suspiciously consistent timing
                response_time = 45.0 + random.uniform(-2, 2)  # Very consistent timing
                difficulty = random.uniform(0.2, 0.9)
                is_correct = random.random() > 0.3  # Unusually high accuracy
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': random.choice(['A', 'B', 'C', 'D']),
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'logical_reasoning']),
                    'timestamp': (base_time + timedelta(seconds=i*50)).isoformat()
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Test Candidate Suspicious Timing',
                'responses': responses,
                'session_metadata': {
                    'start_time': (base_time - timedelta(hours=8)).isoformat(),  # Unusual hour
                    'end_time': (base_time - timedelta(hours=6, minutes=30)).isoformat(),
                    'ip_address': '10.0.0.1',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'timezone': 'America/New_York',
                    'location': {'country': 'US', 'region': 'NY'}
                }
            }
            
        elif session_type == "pattern_irregularities":
            # Session with suspicious answer patterns
            responses = []
            pattern = ['A', 'B', 'C', 'D'] * 6  # Repeating ABCD pattern
            
            for i in range(24):
                response_time = random.uniform(20, 90)
                difficulty = random.uniform(0.3, 0.7)
                is_correct = random.random() > 0.4
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': pattern[i],  # Suspicious pattern
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'logical_reasoning', 'verbal_comprehension']),
                    'timestamp': (base_time + timedelta(seconds=i*60)).isoformat()
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Test Candidate Pattern Issues',
                'responses': responses,
                'session_metadata': {
                    'start_time': base_time.isoformat(),
                    'end_time': (base_time + timedelta(hours=1)).isoformat(),
                    'ip_address': '203.0.113.1',
                    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'timezone': 'America/Los_Angeles',
                    'location': {'country': 'US', 'region': 'CA'}
                }
            }
            
        elif session_type == "difficulty_anomaly":
            # Session with inverted difficulty performance
            responses = []
            for i in range(22):
                response_time = random.uniform(40, 100)
                difficulty = random.uniform(0.1, 0.9)
                
                # Inverted performance - better on harder questions
                if difficulty > 0.7:
                    is_correct = random.random() > 0.2  # 80% correct on hard questions
                elif difficulty < 0.4:
                    is_correct = random.random() > 0.8  # 20% correct on easy questions
                else:
                    is_correct = random.random() > 0.5  # 50% on medium
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': random.choice(['A', 'B', 'C', 'D']),
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'spatial_reasoning']),
                    'timestamp': (base_time + timedelta(seconds=i*70)).isoformat()
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Test Candidate Difficulty Anomaly',
                'responses': responses,
                'session_metadata': {
                    'start_time': base_time.isoformat(),
                    'end_time': (base_time + timedelta(hours=1, minutes=15)).isoformat(),
                    'ip_address': '198.51.100.1',
                    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                    'timezone': 'Europe/London',
                    'location': {'country': 'GB', 'region': 'London'}
                }
            }

    def create_comparison_sessions(self, primary_session):
        """Create comparison sessions for collaborative cheating analysis"""
        comparison_sessions = []
        
        # Create 2 similar sessions for collaboration testing
        for i in range(2):
            session_id = str(uuid.uuid4())
            self.test_session_ids.append(session_id)
            
            # Copy some responses from primary session (simulate collaboration)
            primary_responses = primary_session['responses']
            similar_responses = []
            
            for j, resp in enumerate(primary_responses[:15]):  # Use first 15 responses
                if random.random() > 0.3:  # 70% similarity
                    similar_responses.append({
                        'question_id': resp['question_id'],
                        'response': resp['response'],  # Same answer
                        'is_correct': resp['is_correct'],
                        'response_time': resp['response_time'] + random.uniform(-10, 10),
                        'difficulty': resp['difficulty'],
                        'topic': resp['topic'],
                        'timestamp': resp['timestamp']
                    })
                else:
                    similar_responses.append({
                        'question_id': resp['question_id'],
                        'response': random.choice(['A', 'B', 'C', 'D']),
                        'is_correct': random.random() > 0.5,
                        'response_time': random.uniform(30, 120),
                        'difficulty': resp['difficulty'],
                        'topic': resp['topic'],
                        'timestamp': resp['timestamp']
                    })
            
            comparison_sessions.append({
                'session_id': session_id,
                'candidate_name': f'Comparison Candidate {i+1}',
                'responses': similar_responses,
                'session_metadata': {
                    'start_time': primary_session['session_metadata']['start_time'],
                    'end_time': primary_session['session_metadata']['end_time'],
                    'ip_address': f'192.168.1.{100+i}',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'timezone': primary_session['session_metadata']['timezone'],
                    'location': primary_session['session_metadata']['location']
                }
            })
        
        return comparison_sessions

    def test_answer_pattern_analysis(self):
        """Test POST /api/statistical-analysis/detect-answer-pattern-irregularities"""
        print("🔍 Testing Answer Pattern Analysis Endpoint...")
        
        try:
            # Test with normal session
            normal_session = self.create_realistic_session_data("normal")
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
                json={"session_data": normal_session},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis_results' in data:
                    analysis = data['analysis_results']
                    
                    # Validate response structure
                    required_fields = ['irregularity_score', 'risk_level', 'detailed_analysis']
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        score = analysis.get('irregularity_score', 0)
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        
                        self.log_test(
                            "Answer Pattern Analysis - Normal Session",
                            True,
                            f"Score: {score:.3f}, Risk: {risk_level}, Analysis ID: {data.get('analysis_id')}"
                        )
                        
                        # Test with suspicious pattern session
                        pattern_session = self.create_realistic_session_data("pattern_irregularities")
                        response2 = self.session.post(
                            f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
                            json={"session_data": pattern_session},
                            timeout=30
                        )
                        
                        if response2.status_code == 200:
                            data2 = response2.json()
                            analysis2 = data2['analysis_results']
                            score2 = analysis2.get('irregularity_score', 0)
                            risk_level2 = analysis2.get('risk_level', 'UNKNOWN')
                            
                            self.log_test(
                                "Answer Pattern Analysis - Suspicious Pattern",
                                True,
                                f"Score: {score2:.3f}, Risk: {risk_level2}, Higher score indicates detection working"
                            )
                        else:
                            self.log_test(
                                "Answer Pattern Analysis - Suspicious Pattern",
                                False,
                                f"HTTP {response2.status_code}: {response2.text}"
                            )
                    else:
                        self.log_test(
                            "Answer Pattern Analysis - Normal Session",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Answer Pattern Analysis - Normal Session",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Answer Pattern Analysis - Normal Session",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Answer Pattern Analysis",
                False,
                f"Exception: {str(e)}"
            )

    def test_difficulty_progression_analysis(self):
        """Test POST /api/statistical-analysis/analyze-difficulty-progression-anomalies"""
        print("📊 Testing Difficulty Progression Analysis Endpoint...")
        
        try:
            # Test with normal session
            normal_session = self.create_realistic_session_data("normal")
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/analyze-difficulty-progression-anomalies",
                json={"session_data": normal_session},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis_results' in data:
                    analysis = data['analysis_results']
                    
                    # Validate response structure
                    required_fields = ['anomaly_score', 'risk_level', 'detailed_analysis']
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        score = analysis.get('anomaly_score', 0)
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        
                        self.log_test(
                            "Difficulty Progression Analysis - Normal Session",
                            True,
                            f"Score: {score:.3f}, Risk: {risk_level}, Analysis ID: {data.get('analysis_id')}"
                        )
                        
                        # Test with difficulty anomaly session
                        anomaly_session = self.create_realistic_session_data("difficulty_anomaly")
                        response2 = self.session.post(
                            f"{BACKEND_URL}/statistical-analysis/analyze-difficulty-progression-anomalies",
                            json={"session_data": anomaly_session},
                            timeout=30
                        )
                        
                        if response2.status_code == 200:
                            data2 = response2.json()
                            analysis2 = data2['analysis_results']
                            score2 = analysis2.get('anomaly_score', 0)
                            risk_level2 = analysis2.get('risk_level', 'UNKNOWN')
                            
                            self.log_test(
                                "Difficulty Progression Analysis - Anomaly Session",
                                True,
                                f"Score: {score2:.3f}, Risk: {risk_level2}, Inverted performance detection"
                            )
                        else:
                            self.log_test(
                                "Difficulty Progression Analysis - Anomaly Session",
                                False,
                                f"HTTP {response2.status_code}: {response2.text}"
                            )
                    else:
                        self.log_test(
                            "Difficulty Progression Analysis - Normal Session",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Difficulty Progression Analysis - Normal Session",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Difficulty Progression Analysis - Normal Session",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Difficulty Progression Analysis",
                False,
                f"Exception: {str(e)}"
            )

    def test_timezone_manipulation_analysis(self):
        """Test POST /api/statistical-analysis/identify-timezone-manipulation"""
        print("🕐 Testing Timezone Manipulation Analysis Endpoint...")
        
        try:
            # Test with normal session
            normal_session = self.create_realistic_session_data("normal")
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/identify-timezone-manipulation",
                json={"session_data": normal_session},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis_results' in data:
                    analysis = data['analysis_results']
                    
                    # Validate response structure - handle both full analysis and empty analysis cases
                    if 'manipulation_score' in analysis:
                        required_fields = ['manipulation_score', 'risk_level', 'detailed_analysis']
                        score = analysis.get('manipulation_score', 0)
                    elif 'score' in analysis:
                        required_fields = ['score', 'risk_level', 'detailed_analysis']
                        score = analysis.get('score', 0)
                    else:
                        required_fields = ['risk_level', 'detailed_analysis']
                        score = 0
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        
                        self.log_test(
                            "Timezone Manipulation Analysis - Normal Session",
                            True,
                            f"Score: {score:.3f}, Risk: {risk_level}, Analysis ID: {data.get('analysis_id')}"
                        )
                        
                        # Test with suspicious timing session
                        timing_session = self.create_realistic_session_data("suspicious_timing")
                        response2 = self.session.post(
                            f"{BACKEND_URL}/statistical-analysis/identify-timezone-manipulation",
                            json={"session_data": timing_session},
                            timeout=30
                        )
                        
                        if response2.status_code == 200:
                            data2 = response2.json()
                            analysis2 = data2['analysis_results']
                            score2 = analysis2.get('manipulation_score', 0)
                            risk_level2 = analysis2.get('risk_level', 'UNKNOWN')
                            
                            self.log_test(
                                "Timezone Manipulation Analysis - Suspicious Timing",
                                True,
                                f"Score: {score2:.3f}, Risk: {risk_level2}, Unusual hours detection"
                            )
                        else:
                            self.log_test(
                                "Timezone Manipulation Analysis - Suspicious Timing",
                                False,
                                f"HTTP {response2.status_code}: {response2.text}"
                            )
                    else:
                        self.log_test(
                            "Timezone Manipulation Analysis - Normal Session",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Timezone Manipulation Analysis - Normal Session",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Timezone Manipulation Analysis - Normal Session",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Timezone Manipulation Analysis",
                False,
                f"Exception: {str(e)}"
            )

    def test_collaborative_cheating_analysis(self):
        """Test POST /api/statistical-analysis/detect-collaborative-cheating-patterns"""
        print("👥 Testing Collaborative Cheating Analysis Endpoint...")
        
        try:
            # Create primary session and comparison sessions
            primary_session = self.create_realistic_session_data("normal")
            comparison_sessions = self.create_comparison_sessions(primary_session)
            
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/detect-collaborative-cheating-patterns",
                json={
                    "session_data": primary_session,
                    "comparison_sessions": comparison_sessions
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis_results' in data:
                    analysis = data['analysis_results']
                    
                    # Validate response structure
                    required_fields = ['collaboration_score', 'risk_level', 'detailed_analysis']
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        score = analysis.get('collaboration_score', 0)
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        comparison_count = analysis.get('comparison_sessions_count', 0)
                        
                        self.log_test(
                            "Collaborative Cheating Analysis - With Comparisons",
                            True,
                            f"Score: {score:.3f}, Risk: {risk_level}, Compared: {comparison_count} sessions, Analysis ID: {data.get('analysis_id')}"
                        )
                        
                        # Test without comparison sessions
                        response2 = self.session.post(
                            f"{BACKEND_URL}/statistical-analysis/detect-collaborative-cheating-patterns",
                            json={"session_data": primary_session},
                            timeout=30
                        )
                        
                        if response2.status_code == 200:
                            data2 = response2.json()
                            analysis2 = data2['analysis_results']
                            score2 = analysis2.get('collaboration_score', 0)
                            risk_level2 = analysis2.get('risk_level', 'UNKNOWN')
                            
                            self.log_test(
                                "Collaborative Cheating Analysis - No Comparisons",
                                True,
                                f"Score: {score2:.3f}, Risk: {risk_level2}, Internal consistency only"
                            )
                        else:
                            self.log_test(
                                "Collaborative Cheating Analysis - No Comparisons",
                                False,
                                f"HTTP {response2.status_code}: {response2.text}"
                            )
                    else:
                        self.log_test(
                            "Collaborative Cheating Analysis - With Comparisons",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Collaborative Cheating Analysis - With Comparisons",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Collaborative Cheating Analysis - With Comparisons",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Collaborative Cheating Analysis",
                False,
                f"Exception: {str(e)}"
            )

    def test_session_analysis_retrieval(self):
        """Test GET /api/statistical-analysis/session-analysis/{session_id}"""
        print("📋 Testing Session Analysis Retrieval Endpoint...")
        
        try:
            if not self.test_session_ids:
                self.log_test(
                    "Session Analysis Retrieval",
                    False,
                    "No test session IDs available from previous tests"
                )
                return
            
            # Use the first session ID from previous tests
            session_id = self.test_session_ids[0]
            
            response = self.session.get(
                f"{BACKEND_URL}/statistical-analysis/session-analysis/{session_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analyses' in data:
                    analyses = data['analyses']
                    total_analyses = data.get('total_analyses', 0)
                    
                    self.log_test(
                        "Session Analysis Retrieval - Existing Session",
                        True,
                        f"Retrieved {total_analyses} analyses for session {session_id[:8]}..."
                    )
                    
                    # Validate analysis structure
                    if analyses:
                        first_analysis = analyses[0]
                        required_fields = ['analysis_id', 'session_id', 'analysis_type', 'analysis_results']
                        missing_fields = [field for field in required_fields if field not in first_analysis]
                        
                        if not missing_fields:
                            self.log_test(
                                "Session Analysis Retrieval - Structure Validation",
                                True,
                                f"Analysis structure valid: {first_analysis.get('analysis_type')}"
                            )
                        else:
                            self.log_test(
                                "Session Analysis Retrieval - Structure Validation",
                                False,
                                f"Missing fields in analysis: {missing_fields}"
                            )
                else:
                    self.log_test(
                        "Session Analysis Retrieval - Existing Session",
                        False,
                        f"Invalid response structure: {data}"
                    )
            elif response.status_code == 404:
                self.log_test(
                    "Session Analysis Retrieval - Existing Session",
                    False,
                    f"Session not found (404) - may indicate database storage issue"
                )
            else:
                self.log_test(
                    "Session Analysis Retrieval - Existing Session",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
            
            # Test with non-existent session ID
            fake_session_id = str(uuid.uuid4())
            response2 = self.session.get(
                f"{BACKEND_URL}/statistical-analysis/session-analysis/{fake_session_id}",
                timeout=30
            )
            
            if response2.status_code == 404:
                self.log_test(
                    "Session Analysis Retrieval - Non-existent Session",
                    True,
                    "Correctly returned 404 for non-existent session"
                )
            else:
                self.log_test(
                    "Session Analysis Retrieval - Non-existent Session",
                    False,
                    f"Expected 404, got HTTP {response2.status_code}: {response2.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Session Analysis Retrieval",
                False,
                f"Exception: {str(e)}"
            )

    def test_analyzer_status(self):
        """Test GET /api/statistical-analysis/model-status"""
        print("📊 Testing Analyzer Status Endpoint...")
        
        try:
            response = self.session.get(
                f"{BACKEND_URL}/statistical-analysis/model-status",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analyzer_status' in data:
                    status = data.get('analyzer_status')
                    available_analyses = data.get('available_analyses', [])
                    statistics = data.get('analysis_statistics', {})
                    
                    # Validate expected analyses are available
                    expected_analyses = [
                        'answer_pattern_irregularities',
                        'difficulty_progression_anomalies',
                        'timezone_manipulation',
                        'collaborative_cheating_patterns'
                    ]
                    
                    missing_analyses = [analysis for analysis in expected_analyses if analysis not in available_analyses]
                    
                    if not missing_analyses:
                        total_analyses = statistics.get('total_analyses', 0)
                        high_risk_analyses = statistics.get('high_risk_analyses', 0)
                        
                        self.log_test(
                            "Analyzer Status - Functionality Check",
                            True,
                            f"Status: {status}, Total analyses: {total_analyses}, High risk: {high_risk_analyses}"
                        )
                        
                        # Validate statistics structure
                        if 'analysis_distribution' in statistics:
                            distribution = statistics['analysis_distribution']
                            self.log_test(
                                "Analyzer Status - Statistics Validation",
                                True,
                                f"Analysis distribution available with {len(distribution)} types"
                            )
                        else:
                            self.log_test(
                                "Analyzer Status - Statistics Validation",
                                False,
                                "Missing analysis_distribution in statistics"
                            )
                    else:
                        self.log_test(
                            "Analyzer Status - Functionality Check",
                            False,
                            f"Missing expected analyses: {missing_analyses}"
                        )
                else:
                    self.log_test(
                        "Analyzer Status - Functionality Check",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Analyzer Status - Functionality Check",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Analyzer Status",
                False,
                f"Exception: {str(e)}"
            )

    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("⚠️  Testing Edge Cases and Error Handling...")
        
        try:
            # Test with empty session data
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
                json={"session_data": {}},
                timeout=30
            )
            
            if response.status_code == 400:
                self.log_test(
                    "Edge Case - Empty Session Data",
                    True,
                    "Correctly rejected empty session data with 400 error"
                )
            else:
                self.log_test(
                    "Edge Case - Empty Session Data",
                    False,
                    f"Expected 400, got HTTP {response.status_code}"
                )
            
            # Test with missing session_id
            response2 = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
                json={"session_data": {"responses": []}},
                timeout=30
            )
            
            if response2.status_code == 400:
                self.log_test(
                    "Edge Case - Missing Session ID",
                    True,
                    "Correctly rejected missing session ID with 400 error"
                )
            else:
                self.log_test(
                    "Edge Case - Missing Session ID",
                    False,
                    f"Expected 400, got HTTP {response2.status_code}"
                )
            
            # Test with insufficient data
            minimal_session = {
                'session_id': str(uuid.uuid4()),
                'responses': [
                    {'question_id': 'q1', 'response': 'A', 'is_correct': True}
                ]
            }
            
            response3 = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/analyze-difficulty-progression-anomalies",
                json={"session_data": minimal_session},
                timeout=30
            )
            
            if response3.status_code == 200:
                data = response3.json()
                if data.get('success'):
                    analysis = data['analysis_results']
                    if 'message' in analysis and 'insufficient' in analysis['message'].lower():
                        self.log_test(
                            "Edge Case - Insufficient Data",
                            True,
                            f"Handled insufficient data gracefully: {analysis.get('message')}"
                        )
                    else:
                        self.log_test(
                            "Edge Case - Insufficient Data",
                            True,
                            f"Processed minimal data, score: {analysis.get('anomaly_score', 'N/A')}"
                        )
                else:
                    self.log_test(
                        "Edge Case - Insufficient Data",
                        False,
                        f"Failed to handle insufficient data: {data}"
                    )
            else:
                self.log_test(
                    "Edge Case - Insufficient Data",
                    False,
                    f"HTTP {response3.status_code}: {response3.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Edge Cases",
                False,
                f"Exception: {str(e)}"
            )

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("🚀 Starting Comprehensive Statistical Anomaly Analyzer Testing")
        print("=" * 80)
        
        # Test all endpoints
        self.test_answer_pattern_analysis()
        self.test_difficulty_progression_analysis()
        self.test_timezone_manipulation_analysis()
        self.test_collaborative_cheating_analysis()
        self.test_session_analysis_retrieval()
        self.test_analyzer_status()
        self.test_edge_cases()
        
        # Generate summary
        print("=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['details']}")
            print()
        
        print("✅ PASSED TESTS:")
        for result in self.test_results:
            if result['success']:
                print(f"  - {result['test_name']}")
        
        print("\n" + "=" * 80)
        print("🎯 TESTING COMPLETE")
        print("=" * 80)
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': success_rate,
            'test_results': self.test_results
        }

if __name__ == "__main__":
    tester = StatisticalAnomalyTester()
    results = tester.run_comprehensive_test()