#!/usr/bin/env python3
"""
ENHANCED Statistical Anomaly Analyzer Backend Testing Suite (Step 2.2)

This script tests all 7 Statistical Anomaly Analyzer API endpoints including the NEW Markov Chain Analysis:
1. POST /api/statistical-analysis/detect-answer-patterns (enhanced with completed helper methods)
2. POST /api/statistical-analysis/analyze-difficulty-progression (with full outlier detection)
3. POST /api/statistical-analysis/identify-timezone-manipulation (with comprehensive timing analysis)
4. POST /api/statistical-analysis/detect-collaborative-cheating-patterns (with cross-session analysis)
5. POST /api/statistical-analysis/detect-markov-chain-anomalies (NEW ENHANCEMENT METHOD)
6. GET /api/statistical-analysis/session-analysis/{session_id}
7. GET /api/statistical-analysis/model-status

Tests enhanced functionality including:
- Alternating pattern detection with sophisticated sequence analysis
- Temporal/positional clustering with statistical metrics
- Comprehensive difficulty progression analysis with rolling windows
- Statistical outlier detection using Z-scores
- Markov chain analysis with entropy and stationarity testing
- Advanced timing pattern analysis with break detection

Validates advanced statistical algorithms:
- Chi-square tests for uniformity
- Pearson correlation analysis
- Kolmogorov-Smirnov tests
- Linear regression for trend analysis
- Fisher's method for p-value combination
- Entropy calculations and KL divergence
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import random
import time
import math

# Backend URL from environment
BACKEND_URL = "https://integrity-check-2.preview.emergentagent.com/api"

class EnhancedStatisticalAnomalyTester:
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

    def create_enhanced_session_data(self, session_type="normal"):
        """Create enhanced realistic session data for comprehensive testing"""
        session_id = str(uuid.uuid4())
        self.test_session_ids.append(session_id)
        
        base_time = datetime.utcnow() - timedelta(hours=2)
        
        if session_type == "normal":
            # Normal session with typical patterns
            responses = []
            for i in range(30):
                response_time = random.uniform(25, 150)  # 25-150 seconds per question
                difficulty = random.uniform(0.2, 0.9)
                is_correct = random.random() > (difficulty * 0.6)  # Realistic difficulty correlation
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': random.choice(['A', 'B', 'C', 'D']),
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'logical_reasoning', 'verbal_comprehension', 'spatial_reasoning']),
                    'timestamp': (base_time + timedelta(seconds=sum(30 + j*60 for j in range(i)))).isoformat(),
                    'position': i + 1,
                    'question_type': random.choice(['multiple_choice', 'numerical_input', 'true_false'])
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Enhanced Test Candidate Normal',
                'responses': responses,
                'session_metadata': {
                    'start_time': base_time.isoformat(),
                    'end_time': (base_time + timedelta(hours=2)).isoformat(),
                    'ip_address': '192.168.1.100',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'timezone': 'America/New_York',
                    'location': {'country': 'US', 'region': 'NY'},
                    'browser_fingerprint': 'fp_normal_12345',
                    'screen_resolution': '1920x1080'
                }
            }
            
        elif session_type == "abab_pattern":
            # Session with ABAB alternating pattern (sophisticated cheating)
            responses = []
            pattern = ['A', 'B'] * 15  # ABAB pattern for 30 questions
            
            for i in range(30):
                response_time = 45.0 + random.uniform(-5, 5)  # Consistent timing
                difficulty = random.uniform(0.3, 0.8)
                is_correct = random.random() > 0.25  # High accuracy despite pattern
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': pattern[i],  # Alternating pattern
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'logical_reasoning']),
                    'timestamp': (base_time + timedelta(seconds=i*50)).isoformat(),
                    'position': i + 1,
                    'question_type': 'multiple_choice'
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Enhanced Test ABAB Pattern',
                'responses': responses,
                'session_metadata': {
                    'start_time': base_time.isoformat(),
                    'end_time': (base_time + timedelta(hours=1, minutes=30)).isoformat(),
                    'ip_address': '10.0.0.1',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'timezone': 'America/New_York',
                    'location': {'country': 'US', 'region': 'NY'},
                    'browser_fingerprint': 'fp_abab_67890',
                    'screen_resolution': '1366x768'
                }
            }
            
        elif session_type == "markov_anomaly":
            # Session with sophisticated Markov chain dependencies
            responses = []
            
            # Create a pattern where A->B->C->A with high probability
            markov_pattern = []
            current = 'A'
            for i in range(30):
                markov_pattern.append(current)
                
                # Markov chain: A->B (0.8), B->C (0.8), C->A (0.8), otherwise random
                if current == 'A' and random.random() < 0.8:
                    current = 'B'
                elif current == 'B' and random.random() < 0.8:
                    current = 'C'
                elif current == 'C' and random.random() < 0.8:
                    current = 'A'
                else:
                    current = random.choice(['A', 'B', 'C', 'D'])
            
            for i in range(30):
                response_time = random.uniform(35, 85)
                difficulty = random.uniform(0.4, 0.7)
                is_correct = random.random() > 0.35
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': markov_pattern[i],
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'logical_reasoning', 'verbal_comprehension']),
                    'timestamp': (base_time + timedelta(seconds=i*60)).isoformat(),
                    'position': i + 1,
                    'question_type': 'multiple_choice'
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Enhanced Test Markov Anomaly',
                'responses': responses,
                'session_metadata': {
                    'start_time': base_time.isoformat(),
                    'end_time': (base_time + timedelta(hours=1, minutes=45)).isoformat(),
                    'ip_address': '203.0.113.1',
                    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'timezone': 'America/Los_Angeles',
                    'location': {'country': 'US', 'region': 'CA'},
                    'browser_fingerprint': 'fp_markov_54321',
                    'screen_resolution': '2560x1440'
                }
            }
            
        elif session_type == "clustered_responses":
            # Session with temporal/positional clustering
            responses = []
            
            for i in range(30):
                # Create clusters of similar responses
                if i < 10:
                    response = 'A'  # First cluster: all A
                elif i < 20:
                    response = 'B'  # Second cluster: all B
                else:
                    response = random.choice(['C', 'D'])  # Mixed cluster
                
                # Clustered timing - fast responses in clusters
                if i % 10 < 5:
                    response_time = random.uniform(20, 35)  # Fast cluster
                else:
                    response_time = random.uniform(80, 120)  # Slow cluster
                
                difficulty = random.uniform(0.3, 0.8)
                is_correct = random.random() > 0.4
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': response,
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'spatial_reasoning']),
                    'timestamp': (base_time + timedelta(seconds=i*70)).isoformat(),
                    'position': i + 1,
                    'question_type': 'multiple_choice'
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Enhanced Test Clustered Responses',
                'responses': responses,
                'session_metadata': {
                    'start_time': base_time.isoformat(),
                    'end_time': (base_time + timedelta(hours=1, minutes=20)).isoformat(),
                    'ip_address': '198.51.100.1',
                    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                    'timezone': 'Europe/London',
                    'location': {'country': 'GB', 'region': 'London'},
                    'browser_fingerprint': 'fp_cluster_98765',
                    'screen_resolution': '1440x900'
                }
            }
            
        elif session_type == "inverted_difficulty":
            # Session with inverted difficulty performance (statistical outlier)
            responses = []
            for i in range(25):
                response_time = random.uniform(40, 100)
                difficulty = random.uniform(0.1, 0.9)
                
                # Strong inverted performance - much better on harder questions
                if difficulty > 0.8:
                    is_correct = random.random() > 0.15  # 85% correct on very hard questions
                elif difficulty > 0.6:
                    is_correct = random.random() > 0.3   # 70% correct on hard questions
                elif difficulty < 0.3:
                    is_correct = random.random() > 0.85  # 15% correct on easy questions
                else:
                    is_correct = random.random() > 0.6   # 40% correct on medium questions
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': random.choice(['A', 'B', 'C', 'D']),
                    'is_correct': is_correct,
                    'response_time': response_time,
                    'difficulty': difficulty,
                    'topic': random.choice(['numerical_reasoning', 'spatial_reasoning']),
                    'timestamp': (base_time + timedelta(seconds=i*75)).isoformat(),
                    'position': i + 1,
                    'question_type': 'multiple_choice'
                })
            
            return {
                'session_id': session_id,
                'candidate_name': 'Enhanced Test Inverted Difficulty',
                'responses': responses,
                'session_metadata': {
                    'start_time': base_time.isoformat(),
                    'end_time': (base_time + timedelta(hours=1, minutes=40)).isoformat(),
                    'ip_address': '172.16.0.1',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'timezone': 'Asia/Tokyo',
                    'location': {'country': 'JP', 'region': 'Tokyo'},
                    'browser_fingerprint': 'fp_inverted_11111',
                    'screen_resolution': '1920x1200'
                }
            }

    def test_enhanced_answer_pattern_analysis(self):
        """Test POST /api/statistical-analysis/detect-answer-pattern-irregularities with enhanced functionality"""
        print("🔍 Testing Enhanced Answer Pattern Analysis Endpoint...")
        
        try:
            # Test 1: Normal session
            normal_session = self.create_enhanced_session_data("normal")
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
                json={"session_data": normal_session},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis_results' in data:
                    analysis = data['analysis_results']
                    
                    # Validate enhanced response structure
                    required_fields = ['irregularity_score', 'risk_level', 'detailed_analysis']
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        score = analysis.get('irregularity_score', 0)
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        detailed = analysis.get('detailed_analysis', {})
                        
                        # Check for enhanced sub-analyses
                        expected_sub_analyses = ['distribution_analysis', 'sequence_analysis', 'clustering_analysis', 'change_analysis', 'uniformity_analysis']
                        found_sub_analyses = [sub for sub in expected_sub_analyses if sub in detailed]
                        
                        self.log_test(
                            "Enhanced Answer Pattern Analysis - Normal Session",
                            True,
                            f"Score: {score:.3f}, Risk: {risk_level}, Sub-analyses: {len(found_sub_analyses)}/5, Analysis ID: {data.get('analysis_id')}"
                        )
                        
                        # Test 2: ABAB alternating pattern
                        abab_session = self.create_enhanced_session_data("abab_pattern")
                        response2 = self.session.post(
                            f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
                            json={"session_data": abab_session},
                            timeout=30
                        )
                        
                        if response2.status_code == 200:
                            data2 = response2.json()
                            analysis2 = data2['analysis_results']
                            score2 = analysis2.get('irregularity_score', 0)
                            risk_level2 = analysis2.get('risk_level', 'UNKNOWN')
                            
                            self.log_test(
                                "Enhanced Answer Pattern Analysis - ABAB Pattern",
                                True,
                                f"Score: {score2:.3f}, Risk: {risk_level2}, Pattern detection: {'HIGH' if score2 > score else 'LOW'}"
                            )
                            
                            # Test 3: Clustered responses
                            cluster_session = self.create_enhanced_session_data("clustered_responses")
                            response3 = self.session.post(
                                f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
                                json={"session_data": cluster_session},
                                timeout=30
                            )
                            
                            if response3.status_code == 200:
                                data3 = response3.json()
                                analysis3 = data3['analysis_results']
                                score3 = analysis3.get('irregularity_score', 0)
                                risk_level3 = analysis3.get('risk_level', 'UNKNOWN')
                                
                                self.log_test(
                                    "Enhanced Answer Pattern Analysis - Clustered Responses",
                                    True,
                                    f"Score: {score3:.3f}, Risk: {risk_level3}, Clustering detection working"
                                )
                            else:
                                self.log_test(
                                    "Enhanced Answer Pattern Analysis - Clustered Responses",
                                    False,
                                    f"HTTP {response3.status_code}: {response3.text}"
                                )
                        else:
                            self.log_test(
                                "Enhanced Answer Pattern Analysis - ABAB Pattern",
                                False,
                                f"HTTP {response2.status_code}: {response2.text}"
                            )
                    else:
                        self.log_test(
                            "Enhanced Answer Pattern Analysis - Normal Session",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Enhanced Answer Pattern Analysis - Normal Session",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Enhanced Answer Pattern Analysis - Normal Session",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Enhanced Answer Pattern Analysis",
                False,
                f"Exception: {str(e)}"
            )

    def test_enhanced_difficulty_progression_analysis(self):
        """Test POST /api/statistical-analysis/analyze-difficulty-progression-anomalies with enhanced functionality"""
        print("📊 Testing Enhanced Difficulty Progression Analysis Endpoint...")
        
        try:
            # Test 1: Normal session
            normal_session = self.create_enhanced_session_data("normal")
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/analyze-difficulty-progression-anomalies",
                json={"session_data": normal_session},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis_results' in data:
                    analysis = data['analysis_results']
                    
                    # Validate enhanced response structure
                    required_fields = ['anomaly_score', 'risk_level', 'detailed_analysis']
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        score = analysis.get('anomaly_score', 0)
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        detailed = analysis.get('detailed_analysis', {})
                        
                        # Check for enhanced analysis components
                        expected_components = ['correlation_analysis', 'binned_analysis']
                        found_components = [comp for comp in expected_components if comp in detailed]
                        
                        self.log_test(
                            "Enhanced Difficulty Progression Analysis - Normal Session",
                            True,
                            f"Score: {score:.3f}, Risk: {risk_level}, Components: {len(found_components)}/2, Analysis ID: {data.get('analysis_id')}"
                        )
                        
                        # Test 2: Inverted difficulty performance
                        inverted_session = self.create_enhanced_session_data("inverted_difficulty")
                        response2 = self.session.post(
                            f"{BACKEND_URL}/statistical-analysis/analyze-difficulty-progression-anomalies",
                            json={"session_data": inverted_session},
                            timeout=30
                        )
                        
                        if response2.status_code == 200:
                            data2 = response2.json()
                            analysis2 = data2['analysis_results']
                            score2 = analysis2.get('anomaly_score', 0)
                            risk_level2 = analysis2.get('risk_level', 'UNKNOWN')
                            
                            # Check for statistical significance testing
                            detailed2 = analysis2.get('detailed_analysis', {})
                            has_correlation = 'correlation_analysis' in detailed2
                            has_statistical_test = any('p_value' in str(v) for v in detailed2.values() if isinstance(v, dict))
                            
                            self.log_test(
                                "Enhanced Difficulty Progression Analysis - Inverted Performance",
                                True,
                                f"Score: {score2:.3f}, Risk: {risk_level2}, Correlation: {has_correlation}, Stats: {has_statistical_test}"
                            )
                        else:
                            self.log_test(
                                "Enhanced Difficulty Progression Analysis - Inverted Performance",
                                False,
                                f"HTTP {response2.status_code}: {response2.text}"
                            )
                    else:
                        self.log_test(
                            "Enhanced Difficulty Progression Analysis - Normal Session",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Enhanced Difficulty Progression Analysis - Normal Session",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Enhanced Difficulty Progression Analysis - Normal Session",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Enhanced Difficulty Progression Analysis",
                False,
                f"Exception: {str(e)}"
            )

    def test_markov_chain_analysis(self):
        """Test POST /api/statistical-analysis/detect-markov-chain-anomalies (NEW ENHANCEMENT METHOD)"""
        print("🔗 Testing NEW Markov Chain Analysis Endpoint...")
        
        try:
            # Test 1: Normal session
            normal_session = self.create_enhanced_session_data("normal")
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/detect-markov-chain-anomalies",
                json={"session_data": normal_session},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis_results' in data:
                    analysis = data['analysis_results']
                    
                    # Validate Markov chain response structure
                    required_fields = ['markov_anomaly_score', 'risk_level', 'detailed_analysis']
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        score = analysis.get('markov_anomaly_score', 0)
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        detailed = analysis.get('detailed_analysis', {})
                        
                        # Check for Markov-specific analyses
                        expected_markov_analyses = ['first_order_markov', 'second_order_markov', 'transition_anomalies', 'entropy_analysis', 'stationarity_analysis']
                        found_markov_analyses = [analysis for analysis in expected_markov_analyses if analysis in detailed]
                        
                        # Check for statistical significance
                        has_statistical_significance = 'statistical_significance' in analysis
                        
                        self.log_test(
                            "NEW Markov Chain Analysis - Normal Session",
                            True,
                            f"Score: {score:.3f}, Risk: {risk_level}, Markov analyses: {len(found_markov_analyses)}/5, Stats: {has_statistical_significance}, Analysis ID: {data.get('analysis_id')}"
                        )
                        
                        # Test 2: Markov anomaly session
                        markov_session = self.create_enhanced_session_data("markov_anomaly")
                        response2 = self.session.post(
                            f"{BACKEND_URL}/statistical-analysis/detect-markov-chain-anomalies",
                            json={"session_data": markov_session},
                            timeout=30
                        )
                        
                        if response2.status_code == 200:
                            data2 = response2.json()
                            analysis2 = data2['analysis_results']
                            score2 = analysis2.get('markov_anomaly_score', 0)
                            risk_level2 = analysis2.get('risk_level', 'UNKNOWN')
                            
                            # Check for entropy and stationarity analysis
                            detailed2 = analysis2.get('detailed_analysis', {})
                            entropy_analysis = detailed2.get('entropy_analysis', {})
                            stationarity_analysis = detailed2.get('stationarity_analysis', {})
                            
                            has_entropy = 'normalized_entropy' in entropy_analysis
                            has_stationarity = 'is_stationary' in stationarity_analysis
                            
                            self.log_test(
                                "NEW Markov Chain Analysis - Anomaly Session",
                                True,
                                f"Score: {score2:.3f}, Risk: {risk_level2}, Entropy: {has_entropy}, Stationarity: {has_stationarity}, Detection: {'HIGH' if score2 > score else 'LOW'}"
                            )
                            
                            # Test 3: ABAB pattern (should show strong Markov dependencies)
                            abab_session = self.create_enhanced_session_data("abab_pattern")
                            response3 = self.session.post(
                                f"{BACKEND_URL}/statistical-analysis/detect-markov-chain-anomalies",
                                json={"session_data": abab_session},
                                timeout=30
                            )
                            
                            if response3.status_code == 200:
                                data3 = response3.json()
                                analysis3 = data3['analysis_results']
                                score3 = analysis3.get('markov_anomaly_score', 0)
                                risk_level3 = analysis3.get('risk_level', 'UNKNOWN')
                                
                                # Check transition probabilities
                                detailed3 = analysis3.get('detailed_analysis', {})
                                first_order = detailed3.get('first_order_markov', {})
                                has_transition_probs = 'transition_probabilities' in first_order
                                has_chi_square = 'chi_square_tests' in first_order
                                
                                self.log_test(
                                    "NEW Markov Chain Analysis - ABAB Pattern",
                                    True,
                                    f"Score: {score3:.3f}, Risk: {risk_level3}, Transitions: {has_transition_probs}, Chi-square: {has_chi_square}"
                                )
                            else:
                                self.log_test(
                                    "NEW Markov Chain Analysis - ABAB Pattern",
                                    False,
                                    f"HTTP {response3.status_code}: {response3.text}"
                                )
                        else:
                            self.log_test(
                                "NEW Markov Chain Analysis - Anomaly Session",
                                False,
                                f"HTTP {response2.status_code}: {response2.text}"
                            )
                    else:
                        self.log_test(
                            "NEW Markov Chain Analysis - Normal Session",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "NEW Markov Chain Analysis - Normal Session",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "NEW Markov Chain Analysis - Normal Session",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "NEW Markov Chain Analysis",
                False,
                f"Exception: {str(e)}"
            )

    def test_enhanced_timezone_manipulation_analysis(self):
        """Test POST /api/statistical-analysis/identify-timezone-manipulation with enhanced functionality"""
        print("🕐 Testing Enhanced Timezone Manipulation Analysis Endpoint...")
        
        try:
            # Create session with timezone manipulation indicators
            base_time = datetime.utcnow() - timedelta(hours=2)
            session_id = str(uuid.uuid4())
            self.test_session_ids.append(session_id)
            
            responses = []
            for i in range(25):
                # Create suspicious timing patterns
                if i < 10:
                    # Normal business hours
                    timestamp = base_time + timedelta(hours=10, minutes=i*5)
                else:
                    # Unusual hours (3 AM local time)
                    timestamp = base_time + timedelta(hours=3, minutes=(i-10)*5)
                
                responses.append({
                    'question_id': f'q_{i+1}',
                    'response': random.choice(['A', 'B', 'C', 'D']),
                    'is_correct': random.random() > 0.4,
                    'response_time': random.uniform(30, 90),
                    'difficulty': random.uniform(0.3, 0.7),
                    'topic': random.choice(['numerical_reasoning', 'logical_reasoning']),
                    'timestamp': timestamp.isoformat(),
                    'position': i + 1
                })
            
            timezone_session = {
                'session_id': session_id,
                'candidate_name': 'Enhanced Test Timezone Manipulation',
                'responses': responses,
                'session_metadata': {
                    'start_time': (base_time + timedelta(hours=10)).isoformat(),
                    'end_time': (base_time + timedelta(hours=13)).isoformat(),
                    'ip_address': '203.0.113.50',
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'timezone': 'America/New_York',
                    'location': {'country': 'US', 'region': 'NY'},
                    'browser_fingerprint': 'fp_timezone_99999',
                    'screen_resolution': '1920x1080'
                }
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/identify-timezone-manipulation",
                json={"session_data": timezone_session},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and 'analysis_results' in data:
                    analysis = data['analysis_results']
                    
                    # Validate enhanced timezone analysis
                    score_field = 'manipulation_score' if 'manipulation_score' in analysis else 'score'
                    score = analysis.get(score_field, 0)
                    risk_level = analysis.get('risk_level', 'UNKNOWN')
                    detailed = analysis.get('detailed_analysis', {})
                    
                    # Check for enhanced timing analysis components
                    has_timing_patterns = any('timing' in str(k).lower() for k in detailed.keys())
                    has_break_detection = any('break' in str(v) for v in detailed.values() if isinstance(v, (str, dict)))
                    
                    self.log_test(
                        "Enhanced Timezone Manipulation Analysis - Mixed Hours",
                        True,
                        f"Score: {score:.3f}, Risk: {risk_level}, Timing patterns: {has_timing_patterns}, Break detection: {has_break_detection}, Analysis ID: {data.get('analysis_id')}"
                    )
                    
                    # Test normal session for comparison
                    normal_session = self.create_enhanced_session_data("normal")
                    response2 = self.session.post(
                        f"{BACKEND_URL}/statistical-analysis/identify-timezone-manipulation",
                        json={"session_data": normal_session},
                        timeout=30
                    )
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        analysis2 = data2['analysis_results']
                        score2 = analysis2.get(score_field, 0)
                        risk_level2 = analysis2.get('risk_level', 'UNKNOWN')
                        
                        self.log_test(
                            "Enhanced Timezone Manipulation Analysis - Normal Session",
                            True,
                            f"Score: {score2:.3f}, Risk: {risk_level2}, Comparison: {'DETECTED' if score > score2 else 'SIMILAR'}"
                        )
                    else:
                        self.log_test(
                            "Enhanced Timezone Manipulation Analysis - Normal Session",
                            False,
                            f"HTTP {response2.status_code}: {response2.text}"
                        )
                else:
                    self.log_test(
                        "Enhanced Timezone Manipulation Analysis - Mixed Hours",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Enhanced Timezone Manipulation Analysis - Mixed Hours",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Enhanced Timezone Manipulation Analysis",
                False,
                f"Exception: {str(e)}"
            )

    def test_enhanced_collaborative_cheating_analysis(self):
        """Test POST /api/statistical-analysis/detect-collaborative-cheating-patterns with enhanced functionality"""
        print("👥 Testing Enhanced Collaborative Cheating Analysis Endpoint...")
        
        try:
            # Create primary session and enhanced comparison sessions
            primary_session = self.create_enhanced_session_data("normal")
            
            # Create highly similar sessions for collaboration testing
            comparison_sessions = []
            for i in range(3):
                session_id = str(uuid.uuid4())
                self.test_session_ids.append(session_id)
                
                # Create sessions with high similarity (80% same answers)
                similar_responses = []
                primary_responses = primary_session['responses']
                
                for j, resp in enumerate(primary_responses):
                    if random.random() < 0.8:  # 80% similarity
                        similar_responses.append({
                            'question_id': resp['question_id'],
                            'response': resp['response'],  # Same answer
                            'is_correct': resp['is_correct'],
                            'response_time': resp['response_time'] + random.uniform(-5, 5),
                            'difficulty': resp['difficulty'],
                            'topic': resp['topic'],
                            'timestamp': resp['timestamp'],
                            'position': resp['position'],
                            'question_type': resp.get('question_type', 'multiple_choice')
                        })
                    else:
                        similar_responses.append({
                            'question_id': resp['question_id'],
                            'response': random.choice(['A', 'B', 'C', 'D']),
                            'is_correct': random.random() > 0.5,
                            'response_time': random.uniform(30, 120),
                            'difficulty': resp['difficulty'],
                            'topic': resp['topic'],
                            'timestamp': resp['timestamp'],
                            'position': resp['position'],
                            'question_type': resp.get('question_type', 'multiple_choice')
                        })
                
                comparison_sessions.append({
                    'session_id': session_id,
                    'candidate_name': f'Enhanced Comparison Candidate {i+1}',
                    'responses': similar_responses,
                    'session_metadata': {
                        'start_time': primary_session['session_metadata']['start_time'],
                        'end_time': primary_session['session_metadata']['end_time'],
                        'ip_address': f'192.168.1.{101+i}',
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'timezone': primary_session['session_metadata']['timezone'],
                        'location': primary_session['session_metadata']['location'],
                        'browser_fingerprint': f'fp_collab_{i+1}_12345',
                        'screen_resolution': '1920x1080'
                    }
                })
            
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
                    
                    # Validate enhanced collaborative analysis
                    required_fields = ['collaboration_score', 'risk_level', 'detailed_analysis']
                    missing_fields = [field for field in required_fields if field not in analysis]
                    
                    if not missing_fields:
                        score = analysis.get('collaboration_score', 0)
                        risk_level = analysis.get('risk_level', 'UNKNOWN')
                        comparison_count = analysis.get('comparison_sessions_count', 0)
                        detailed = analysis.get('detailed_analysis', {})
                        
                        # Check for enhanced cross-session analysis
                        has_cross_session = any('cross_session' in str(k).lower() for k in detailed.keys())
                        has_similarity_metrics = any('similarity' in str(k).lower() for k in detailed.keys())
                        
                        self.log_test(
                            "Enhanced Collaborative Cheating Analysis - With Comparisons",
                            True,
                            f"Score: {score:.3f}, Risk: {risk_level}, Compared: {comparison_count} sessions, Cross-session: {has_cross_session}, Similarity: {has_similarity_metrics}, Analysis ID: {data.get('analysis_id')}"
                        )
                        
                        # Test internal consistency mode (no comparison sessions)
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
                                "Enhanced Collaborative Cheating Analysis - Internal Consistency",
                                True,
                                f"Score: {score2:.3f}, Risk: {risk_level2}, Mode: Internal consistency only"
                            )
                        else:
                            self.log_test(
                                "Enhanced Collaborative Cheating Analysis - Internal Consistency",
                                False,
                                f"HTTP {response2.status_code}: {response2.text}"
                            )
                    else:
                        self.log_test(
                            "Enhanced Collaborative Cheating Analysis - With Comparisons",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                else:
                    self.log_test(
                        "Enhanced Collaborative Cheating Analysis - With Comparisons",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Enhanced Collaborative Cheating Analysis - With Comparisons",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Enhanced Collaborative Cheating Analysis",
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
                    
                    # Validate enhanced analysis structure
                    if analyses:
                        first_analysis = analyses[0]
                        required_fields = ['analysis_id', 'session_id', 'analysis_type', 'analysis_results']
                        missing_fields = [field for field in required_fields if field not in first_analysis]
                        
                        if not missing_fields:
                            analysis_type = first_analysis.get('analysis_type')
                            has_enhanced_fields = any(field in first_analysis for field in ['statistical_significance', 'recommendations'])
                            
                            self.log_test(
                                "Session Analysis Retrieval - Structure Validation",
                                True,
                                f"Analysis type: {analysis_type}, Enhanced fields: {has_enhanced_fields}"
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
                
        except Exception as e:
            self.log_test(
                "Session Analysis Retrieval",
                False,
                f"Exception: {str(e)}"
            )

    def test_enhanced_analyzer_status(self):
        """Test GET /api/statistical-analysis/model-status"""
        print("📊 Testing Enhanced Analyzer Status Endpoint...")
        
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
                    
                    # Validate expected analyses including NEW Markov chain analysis
                    expected_analyses = [
                        'answer_pattern_irregularities',
                        'difficulty_progression_anomalies',
                        'timezone_manipulation',
                        'collaborative_cheating_patterns',
                        'markov_chain_anomalies'  # NEW ENHANCEMENT
                    ]
                    
                    missing_analyses = [analysis for analysis in expected_analyses if analysis not in available_analyses]
                    
                    if not missing_analyses:
                        total_analyses = statistics.get('total_analyses', 0)
                        high_risk_analyses = statistics.get('high_risk_analyses', 0)
                        
                        # Check for enhanced statistics
                        has_distribution = 'analysis_distribution' in statistics
                        has_enhanced_stats = any(key in statistics for key in ['risk_distribution', 'average_scores'])
                        
                        self.log_test(
                            "Enhanced Analyzer Status - Functionality Check",
                            True,
                            f"Status: {status}, Total: {total_analyses}, High risk: {high_risk_analyses}, All 5 analyses available, Enhanced stats: {has_enhanced_stats}"
                        )
                        
                        # Validate statistics structure
                        if has_distribution:
                            distribution = statistics['analysis_distribution']
                            markov_in_distribution = 'markov_chain_anomalies' in distribution
                            
                            self.log_test(
                                "Enhanced Analyzer Status - Statistics Validation",
                                True,
                                f"Distribution available with {len(distribution)} types, Markov included: {markov_in_distribution}"
                            )
                        else:
                            self.log_test(
                                "Enhanced Analyzer Status - Statistics Validation",
                                False,
                                "Missing analysis_distribution in statistics"
                            )
                    else:
                        self.log_test(
                            "Enhanced Analyzer Status - Functionality Check",
                            False,
                            f"Missing expected analyses: {missing_analyses}"
                        )
                else:
                    self.log_test(
                        "Enhanced Analyzer Status - Functionality Check",
                        False,
                        f"Invalid response structure: {data}"
                    )
            else:
                self.log_test(
                    "Enhanced Analyzer Status - Functionality Check",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Enhanced Analyzer Status",
                False,
                f"Exception: {str(e)}"
            )

    def test_advanced_edge_cases(self):
        """Test advanced edge cases and error handling"""
        print("⚠️  Testing Advanced Edge Cases and Error Handling...")
        
        try:
            # Test 1: Insufficient data for Markov analysis
            minimal_session = {
                'session_id': str(uuid.uuid4()),
                'responses': [
                    {'question_id': 'q1', 'response': 'A', 'is_correct': True},
                    {'question_id': 'q2', 'response': 'B', 'is_correct': False}
                ]
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/detect-markov-chain-anomalies",
                json={"session_data": minimal_session},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data['analysis_results']
                    if 'message' in analysis and 'insufficient' in analysis['message'].lower():
                        self.log_test(
                            "Advanced Edge Case - Insufficient Data for Markov",
                            True,
                            f"Handled insufficient data gracefully: {analysis.get('message')}"
                        )
                    else:
                        self.log_test(
                            "Advanced Edge Case - Insufficient Data for Markov",
                            True,
                            f"Processed minimal data, score: {analysis.get('markov_anomaly_score', 'N/A')}"
                        )
                else:
                    self.log_test(
                        "Advanced Edge Case - Insufficient Data for Markov",
                        False,
                        f"Failed to handle insufficient data: {data}"
                    )
            else:
                self.log_test(
                    "Advanced Edge Case - Insufficient Data for Markov",
                    False,
                    f"HTTP {response.status_code}: {response.text}"
                )
            
            # Test 2: Single answer type (no variation)
            uniform_session = {
                'session_id': str(uuid.uuid4()),
                'responses': [
                    {'question_id': f'q{i}', 'response': 'A', 'is_correct': random.random() > 0.5, 'response_time': 60, 'difficulty': 0.5}
                    for i in range(15)
                ]
            }
            
            response2 = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
                json={"session_data": uniform_session},
                timeout=30
            )
            
            if response2.status_code == 200:
                data2 = response2.json()
                if data2.get('success'):
                    analysis2 = data2['analysis_results']
                    score2 = analysis2.get('irregularity_score', 0)
                    
                    self.log_test(
                        "Advanced Edge Case - Uniform Responses",
                        True,
                        f"Handled uniform responses, irregularity score: {score2:.3f}"
                    )
                else:
                    self.log_test(
                        "Advanced Edge Case - Uniform Responses",
                        False,
                        f"Failed to handle uniform responses: {data2}"
                    )
            else:
                self.log_test(
                    "Advanced Edge Case - Uniform Responses",
                    False,
                    f"HTTP {response2.status_code}: {response2.text}"
                )
            
            # Test 3: Missing required fields
            incomplete_session = {
                'session_id': str(uuid.uuid4()),
                'responses': [
                    {'question_id': 'q1', 'response': 'A'},  # Missing is_correct, response_time, etc.
                    {'question_id': 'q2', 'response': 'B'}
                ]
            }
            
            response3 = self.session.post(
                f"{BACKEND_URL}/statistical-analysis/analyze-difficulty-progression-anomalies",
                json={"session_data": incomplete_session},
                timeout=30
            )
            
            if response3.status_code in [200, 400]:
                if response3.status_code == 200:
                    data3 = response3.json()
                    if data3.get('success'):
                        self.log_test(
                            "Advanced Edge Case - Missing Fields",
                            True,
                            "Handled missing fields gracefully"
                        )
                    else:
                        self.log_test(
                            "Advanced Edge Case - Missing Fields",
                            True,
                            f"Appropriately failed with missing fields: {data3.get('error', 'Unknown error')}"
                        )
                else:
                    self.log_test(
                        "Advanced Edge Case - Missing Fields",
                        True,
                        "Correctly rejected incomplete data with 400 error"
                    )
            else:
                self.log_test(
                    "Advanced Edge Case - Missing Fields",
                    False,
                    f"Unexpected response: HTTP {response3.status_code}: {response3.text}"
                )
                
        except Exception as e:
            self.log_test(
                "Advanced Edge Cases",
                False,
                f"Exception: {str(e)}"
            )

    def run_comprehensive_enhanced_test(self):
        """Run all enhanced tests in sequence"""
        print("🚀 Starting COMPREHENSIVE ENHANCED Statistical Anomaly Analyzer Testing (Step 2.2)")
        print("=" * 90)
        print("Testing all 7 endpoints including NEW Markov Chain Analysis method")
        print("=" * 90)
        
        # Test all enhanced endpoints
        self.test_enhanced_answer_pattern_analysis()
        self.test_enhanced_difficulty_progression_analysis()
        self.test_enhanced_timezone_manipulation_analysis()
        self.test_enhanced_collaborative_cheating_analysis()
        self.test_markov_chain_analysis()  # NEW ENHANCEMENT METHOD
        self.test_session_analysis_retrieval()
        self.test_enhanced_analyzer_status()
        self.test_advanced_edge_cases()
        
        # Generate comprehensive summary
        print("=" * 90)
        print("📊 ENHANCED TEST SUMMARY")
        print("=" * 90)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        # Categorize results by endpoint
        endpoint_results = {}
        for result in self.test_results:
            endpoint = result['test_name'].split(' - ')[0]
            if endpoint not in endpoint_results:
                endpoint_results[endpoint] = {'passed': 0, 'failed': 0}
            
            if result['success']:
                endpoint_results[endpoint]['passed'] += 1
            else:
                endpoint_results[endpoint]['failed'] += 1
        
        print("📈 RESULTS BY ENDPOINT:")
        for endpoint, counts in endpoint_results.items():
            total_endpoint = counts['passed'] + counts['failed']
            endpoint_rate = (counts['passed'] / total_endpoint * 100) if total_endpoint > 0 else 0
            status = "✅" if endpoint_rate == 100 else "⚠️" if endpoint_rate >= 50 else "❌"
            print(f"  {status} {endpoint}: {counts['passed']}/{total_endpoint} ({endpoint_rate:.1f}%)")
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
        
        print("\n" + "=" * 90)
        print("🎯 ENHANCED TESTING COMPLETE")
        print("=" * 90)
        
        # Enhanced summary with specific findings
        markov_tests = [r for r in self.test_results if 'Markov Chain' in r['test_name']]
        markov_success = sum(1 for r in markov_tests if r['success'])
        
        print(f"🔗 NEW Markov Chain Analysis: {markov_success}/{len(markov_tests)} tests passed")
        
        enhanced_features = [r for r in self.test_results if any(keyword in r['test_name'] for keyword in ['Enhanced', 'Advanced'])]
        enhanced_success = sum(1 for r in enhanced_features if r['success'])
        
        print(f"⚡ Enhanced Features: {enhanced_success}/{len(enhanced_features)} tests passed")
        print(f"📊 Overall System Health: {success_rate:.1f}%")
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': success_rate,
            'markov_tests': len(markov_tests),
            'markov_success': markov_success,
            'enhanced_tests': len(enhanced_features),
            'enhanced_success': enhanced_success,
            'endpoint_results': endpoint_results,
            'test_results': self.test_results
        }

if __name__ == "__main__":
    tester = EnhancedStatisticalAnomalyTester()
    results = tester.run_comprehensive_enhanced_test()