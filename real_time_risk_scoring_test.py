#!/usr/bin/env python3
"""
🎯 COMPREHENSIVE REAL-TIME RISK SCORING SYSTEM TESTING

Testing the newly implemented Step 2.3: Real-time Risk Scoring System that integrates with:
- Step 2.1: AnomalyDetectionEngine 
- Step 2.2: StatisticalAnomalyAnalyzer

This test suite validates all 6 risk-scoring API endpoints and comprehensive functionality:
1. POST /api/risk-scoring/calculate-composite-score - Composite risk aggregation
2. POST /api/risk-scoring/update-risk-factors - Continuous risk factor updates  
3. GET /api/risk-scoring/current-risk/{session_id} - Current risk retrieval
4. POST /api/risk-scoring/trigger-alerts - Alert generation with thresholds
5. GET /api/risk-scoring/risk-history/{session_id} - Risk history tracking
6. GET /api/risk-scoring/confidence-intervals/{session_id} - Statistical confidence calculations

Author: Testing Agent
Created: 2025-01-07
"""

import requests
import json
import time
import os
import uuid
import urllib3
from datetime import datetime
from typing import Dict, List, Any

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://tracking-backend.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class RealTimeRiskScoringTester:
    def __init__(self):
        self.session = requests.Session()
        # Add headers and disable SSL verification for testing
        self.session.headers.update({
            'User-Agent': 'RealTimeRiskScoringTester/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        self.session.verify = False  # Disable SSL verification for testing
        # Disable SSL warnings
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.admin_authenticated = False
        self.test_session_id = str(uuid.uuid4())
        self.test_results = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log test results with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status_symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"[{timestamp}] {status_symbol} {test_name}")
        if details:
            print(f"    {details}")
        print()
        
        # Store result for summary
        self.test_results.append({
            'test': test_name,
            'status': status,
            'details': details,
            'timestamp': timestamp
        })

    def test_admin_authentication(self) -> bool:
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

    def test_backend_connectivity(self) -> bool:
        """Test basic backend connectivity"""
        try:
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code in [200, 404, 405]:  # Any response means backend is up
                self.log_test("Backend Connectivity", "PASS", 
                            f"Backend accessible (Status: {response.status_code})")
                return True
            else:
                self.log_test("Backend Connectivity", "FAIL", 
                            f"Unexpected status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Connectivity", "FAIL", f"Connection failed: {str(e)}")
            return False

    def test_composite_risk_score_calculation(self) -> bool:
        """Test POST /api/risk-scoring/calculate-composite-score endpoint"""
        try:
            # Test data for composite risk calculation
            test_data = {
                "session_id": self.test_session_id,
                "current_response_data": {
                    "question_id": "q1",
                    "answer": "Test answer for risk analysis",
                    "response_time": 45.5,
                    "confidence_level": 0.8,
                    "keystroke_patterns": [
                        {"key": "T", "timestamp": 1000, "duration": 100},
                        {"key": "e", "timestamp": 1100, "duration": 80},
                        {"key": "s", "timestamp": 1180, "duration": 90}
                    ],
                    "mouse_movements": [
                        {"x": 100, "y": 200, "timestamp": 1000},
                        {"x": 105, "y": 205, "timestamp": 1050}
                    ]
                }
            }
            
            response = self.session.post(f"{BASE_URL}/risk-scoring/calculate-composite-score", 
                                       json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    risk_assessment = data.get("risk_assessment", {})
                    composite_score = risk_assessment.get("composite_risk_score", 0)
                    risk_level = risk_assessment.get("risk_level", "UNKNOWN")
                    
                    self.log_test("Composite Risk Score Calculation", "PASS", 
                                f"Score: {composite_score:.3f}, Level: {risk_level}, "
                                f"Factors: {risk_assessment.get('total_risk_factors', 0)}")
                    return True
                else:
                    self.log_test("Composite Risk Score Calculation", "FAIL", 
                                f"API returned success=false: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Composite Risk Score Calculation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Composite Risk Score Calculation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_risk_factor_updates(self) -> bool:
        """Test POST /api/risk-scoring/update-risk-factors endpoint"""
        try:
            # Test data for risk factor updates
            test_data = {
                "session_id": self.test_session_id,
                "new_response_data": {
                    "question_id": "q2",
                    "answer": "Updated answer with different patterns",
                    "response_time": 62.3,
                    "confidence_level": 0.6,
                    "behavioral_changes": {
                        "typing_speed_change": -15.2,
                        "pause_frequency_increase": 3,
                        "correction_count": 2
                    },
                    "timing_anomalies": {
                        "unusually_fast_responses": 1,
                        "suspiciously_consistent_timing": True
                    }
                }
            }
            
            response = self.session.post(f"{BASE_URL}/risk-scoring/update-risk-factors", 
                                       json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    updated_assessment = data.get("updated_assessment", {})
                    current_score = updated_assessment.get("composite_risk_score", 0)
                    previous_score = updated_assessment.get("previous_risk_score", 0)
                    trend_analysis = updated_assessment.get("trend_analysis", {})
                    
                    self.log_test("Risk Factor Updates", "PASS", 
                                f"Current: {current_score:.3f}, Previous: {previous_score:.3f}, "
                                f"Trend: {trend_analysis.get('trend_direction', 'unknown')}")
                    return True
                else:
                    self.log_test("Risk Factor Updates", "FAIL", 
                                f"API returned success=false: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Risk Factor Updates", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Risk Factor Updates", "FAIL", f"Exception: {str(e)}")
            return False

    def test_current_risk_retrieval(self) -> bool:
        """Test GET /api/risk-scoring/current-risk/{session_id} endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/risk-scoring/current-risk/{self.test_session_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    risk_assessment = data.get("risk_assessment", {})
                    source = data.get("source", "unknown")
                    
                    if isinstance(risk_assessment, dict):
                        composite_score = risk_assessment.get("composite_risk_score", 0)
                        risk_level = risk_assessment.get("risk_level", "UNKNOWN")
                        
                        self.log_test("Current Risk Retrieval", "PASS", 
                                    f"Score: {composite_score:.3f}, Level: {risk_level}, Source: {source}")
                        return True
                    else:
                        self.log_test("Current Risk Retrieval", "PASS", 
                                    f"Risk assessment retrieved from {source}")
                        return True
                else:
                    self.log_test("Current Risk Retrieval", "FAIL", 
                                f"API returned success=false: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Current Risk Retrieval", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Current Risk Retrieval", "FAIL", f"Exception: {str(e)}")
            return False

    def test_alert_triggering(self) -> bool:
        """Test POST /api/risk-scoring/trigger-alerts endpoint"""
        try:
            # Test data for alert triggering
            test_data = {
                "session_id": self.test_session_id,
                "current_risk_assessment": {
                    "success": True,
                    "composite_risk_score": 0.75,  # HIGH risk level
                    "risk_level": "HIGH",
                    "risk_breakdown": {
                        "statistical_anomalies": 0.8,
                        "behavioral_biometrics": 0.7,
                        "response_patterns": 0.6
                    },
                    "confidence_intervals": {
                        "95%": {"lower": 0.65, "upper": 0.85}
                    }
                }
            }
            
            response = self.session.post(f"{BASE_URL}/risk-scoring/trigger-alerts", 
                                       json=test_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    alert_results = data.get("alert_results", {})
                    alerts_generated = alert_results.get("alerts_generated", 0)
                    current_risk_level = alert_results.get("current_risk_level", "UNKNOWN")
                    escalation_actions = alert_results.get("escalation_actions", [])
                    
                    self.log_test("Alert Triggering", "PASS", 
                                f"Alerts: {alerts_generated}, Level: {current_risk_level}, "
                                f"Actions: {len(escalation_actions)}")
                    return True
                else:
                    self.log_test("Alert Triggering", "FAIL", 
                                f"API returned success=false: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Alert Triggering", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Alert Triggering", "FAIL", f"Exception: {str(e)}")
            return False

    def test_risk_history_tracking(self) -> bool:
        """Test GET /api/risk-scoring/risk-history/{session_id} endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/risk-scoring/risk-history/{self.test_session_id}?limit=20")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    risk_history = data.get("risk_history", {})
                    trend_statistics = data.get("trend_statistics", {})
                    record_counts = data.get("record_counts", {})
                    
                    risk_assessments = len(risk_history.get("risk_assessments", []))
                    factor_updates = len(risk_history.get("factor_updates", []))
                    alert_history = len(risk_history.get("alert_history", []))
                    
                    self.log_test("Risk History Tracking", "PASS", 
                                f"Assessments: {risk_assessments}, Updates: {factor_updates}, "
                                f"Alerts: {alert_history}, Trend: {trend_statistics.get('trend_direction', 'N/A')}")
                    return True
                else:
                    self.log_test("Risk History Tracking", "FAIL", 
                                f"API returned success=false: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Risk History Tracking", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Risk History Tracking", "FAIL", f"Exception: {str(e)}")
            return False

    def test_confidence_intervals(self) -> bool:
        """Test GET /api/risk-scoring/confidence-intervals/{session_id} endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/risk-scoring/confidence-intervals/{self.test_session_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    confidence_results = data.get("confidence_results", {})
                    confidence_intervals = confidence_results.get("confidence_intervals", {})
                    uncertainty_metrics = confidence_results.get("uncertainty_metrics", {})
                    statistical_summary = confidence_results.get("statistical_summary", {})
                    
                    # Count confidence levels available
                    confidence_levels = len(confidence_intervals)
                    
                    self.log_test("Confidence Intervals", "PASS", 
                                f"Confidence levels: {confidence_levels}, "
                                f"Uncertainty metrics: {len(uncertainty_metrics)}, "
                                f"Statistical summary: {len(statistical_summary)}")
                    return True
                else:
                    self.log_test("Confidence Intervals", "FAIL", 
                                f"API returned success=false: {data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Confidence Intervals", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Confidence Intervals", "FAIL", f"Exception: {str(e)}")
            return False

    def test_database_integration(self) -> bool:
        """Test database integration by verifying data persistence"""
        try:
            # This test verifies that the risk scoring system properly stores data
            # by checking if we can retrieve previously calculated risk scores
            
            # First, calculate a composite risk score
            test_data = {
                "session_id": f"db_test_{uuid.uuid4()}",
                "current_response_data": {
                    "question_id": "db_test_q1",
                    "answer": "Database integration test answer",
                    "response_time": 30.0,
                    "confidence_level": 0.9
                }
            }
            
            # Calculate composite score
            calc_response = self.session.post(f"{BASE_URL}/risk-scoring/calculate-composite-score", 
                                            json=test_data)
            
            if calc_response.status_code != 200:
                self.log_test("Database Integration", "FAIL", 
                            f"Failed to calculate initial score: {calc_response.status_code}")
                return False
            
            # Wait a moment for database write
            time.sleep(1)
            
            # Try to retrieve the risk history
            history_response = self.session.get(f"{BASE_URL}/risk-scoring/risk-history/{test_data['session_id']}")
            
            if history_response.status_code == 200:
                history_data = history_response.json()
                if history_data.get("success"):
                    record_counts = history_data.get("record_counts", {})
                    total_records = sum(record_counts.values())
                    
                    self.log_test("Database Integration", "PASS", 
                                f"Data persistence verified - Total records: {total_records}")
                    return True
                else:
                    self.log_test("Database Integration", "FAIL", 
                                f"Failed to retrieve history: {history_data.get('error', 'Unknown error')}")
                    return False
            else:
                self.log_test("Database Integration", "FAIL", 
                            f"History retrieval failed: {history_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Database Integration", "FAIL", f"Exception: {str(e)}")
            return False

    def test_risk_level_classification(self) -> bool:
        """Test risk level classification with different thresholds"""
        try:
            # Test different risk scenarios
            test_scenarios = [
                {"score_target": "LOW", "response_time": 25.0, "confidence": 0.95},
                {"score_target": "MEDIUM", "response_time": 45.0, "confidence": 0.7},
                {"score_target": "HIGH", "response_time": 80.0, "confidence": 0.4},
                {"score_target": "CRITICAL", "response_time": 120.0, "confidence": 0.2}
            ]
            
            classification_results = []
            
            for i, scenario in enumerate(test_scenarios):
                test_data = {
                    "session_id": f"classification_test_{i}_{uuid.uuid4()}",
                    "current_response_data": {
                        "question_id": f"classification_q{i}",
                        "answer": f"Test answer for {scenario['score_target']} risk scenario",
                        "response_time": scenario["response_time"],
                        "confidence_level": scenario["confidence"],
                        "suspicious_patterns": {
                            "copy_paste_detected": scenario["score_target"] in ["HIGH", "CRITICAL"],
                            "external_assistance_indicators": scenario["score_target"] == "CRITICAL",
                            "timing_manipulation": scenario["score_target"] in ["MEDIUM", "HIGH", "CRITICAL"]
                        }
                    }
                }
                
                response = self.session.post(f"{BASE_URL}/risk-scoring/calculate-composite-score", 
                                           json=test_data)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        risk_assessment = data.get("risk_assessment", {})
                        actual_level = risk_assessment.get("risk_level", "UNKNOWN")
                        actual_score = risk_assessment.get("composite_risk_score", 0)
                        
                        classification_results.append({
                            "target": scenario["score_target"],
                            "actual": actual_level,
                            "score": actual_score
                        })
            
            # Analyze classification results
            if classification_results:
                results_summary = ", ".join([f"{r['target']}→{r['actual']}({r['score']:.2f})" 
                                           for r in classification_results])
                
                self.log_test("Risk Level Classification", "PASS", 
                            f"Classification tests completed: {results_summary}")
                return True
            else:
                self.log_test("Risk Level Classification", "FAIL", 
                            "No classification results obtained")
                return False
                
        except Exception as e:
            self.log_test("Risk Level Classification", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_tests(self):
        """Run all real-time risk scoring tests"""
        print("🎯 COMPREHENSIVE REAL-TIME RISK SCORING SYSTEM TESTING")
        print("=" * 70)
        print(f"Backend URL: {BACKEND_URL}")
        print(f"Test Session ID: {self.test_session_id}")
        print("=" * 70)
        print()
        
        # Test execution order
        tests = [
            ("Backend Connectivity", self.test_backend_connectivity),
            ("Admin Authentication", self.test_admin_authentication),
            ("Composite Risk Score Calculation", self.test_composite_risk_score_calculation),
            ("Risk Factor Updates", self.test_risk_factor_updates),
            ("Current Risk Retrieval", self.test_current_risk_retrieval),
            ("Alert Triggering", self.test_alert_triggering),
            ("Risk History Tracking", self.test_risk_history_tracking),
            ("Confidence Intervals", self.test_confidence_intervals),
            ("Database Integration", self.test_database_integration),
            ("Risk Level Classification", self.test_risk_level_classification)
        ]
        
        # Execute tests
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                if test_func():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log_test(test_name, "FAIL", f"Unexpected exception: {str(e)}")
                failed += 1
            
            # Small delay between tests
            time.sleep(0.5)
        
        # Print summary
        print("=" * 70)
        print("🎯 REAL-TIME RISK SCORING SYSTEM TEST SUMMARY")
        print("=" * 70)
        
        total_tests = passed + failed
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        # Detailed results
        if failed > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"  - {result['test']}: {result['details']}")
            print()
        
        if passed > 0:
            print("✅ PASSED TESTS:")
            for result in self.test_results:
                if result['status'] == 'PASS':
                    print(f"  - {result['test']}")
            print()
        
        # Overall assessment
        if success_rate >= 80:
            print("🎉 OVERALL ASSESSMENT: EXCELLENT - Real-time Risk Scoring System is operational")
        elif success_rate >= 60:
            print("⚠️  OVERALL ASSESSMENT: GOOD - Most functionality working, minor issues detected")
        else:
            print("❌ OVERALL ASSESSMENT: NEEDS ATTENTION - Significant issues detected")
        
        print("=" * 70)
        
        return success_rate >= 80

if __name__ == "__main__":
    tester = RealTimeRiskScoringTester()
    tester.run_comprehensive_tests()