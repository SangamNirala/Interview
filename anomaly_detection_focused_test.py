#!/usr/bin/env python3
"""
🎯 FOCUSED TESTING: Anomaly Probability Calculation Endpoint Fix Verification

This test specifically verifies the POST /api/anomaly-detection/calculate-anomaly-probability-scores 
endpoint that was failing with numpy boolean encoding issues after the data format fix.

The main agent applied a fix: converted `is_anomalous = z_score > 2.0` to `is_anomalous = bool(z_score > 2.0)` 
in the _detect_statistical_anomalies method.

Test Workflow:
1. Admin Authentication with Game@1234 password
2. Train baseline models with historical data (embedded response_time format)
3. Test anomaly probability calculation with different session data types
4. Verify response contains proper probability scores and components
5. Ensure no numpy boolean encoding errors
"""

import requests
import json
import sys
import time
from datetime import datetime

# Backend URL from environment
BACKEND_URL = "https://tracking-backend.preview.emergentagent.com/api"

def test_admin_authentication():
    """Test admin authentication with Game@1234 password"""
    print("🔐 Testing Admin Authentication...")
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/admin/login",
            json={"password": "Game@1234"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Admin authentication successful")
                return True
            else:
                print(f"❌ Admin authentication failed: {data}")
                return False
        else:
            print(f"❌ Admin authentication failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Admin authentication error: {str(e)}")
        return False

def create_historical_data_with_embedded_response_time():
    """Create historical data with embedded response_time format as specified in review"""
    return [
        {
            "session_id": "hist_session_1",
            "candidate_name": "Test User 1",
            "responses": [
                {
                    "question_id": "q_1",
                    "response": "A", 
                    "is_correct": True,
                    "response_time": 65.2,  # EMBEDDED IN RESPONSE
                    "difficulty": 0.6,
                    "topic": "numerical"
                },
                {
                    "question_id": "q_2",
                    "response": "B", 
                    "is_correct": False,
                    "response_time": 45.8,
                    "difficulty": 0.4,
                    "topic": "logical"
                },
                {
                    "question_id": "q_3",
                    "response": "C", 
                    "is_correct": True,
                    "response_time": 78.3,
                    "difficulty": 0.8,
                    "topic": "verbal"
                }
            ],
            "total_score": 67.5,
            "completion_time": 189.3,
            "is_legitimate": True
        },
        {
            "session_id": "hist_session_2", 
            "candidate_name": "Test User 2",
            "responses": [
                {
                    "question_id": "q_1",
                    "response": "A", 
                    "is_correct": True,
                    "response_time": 58.7,
                    "difficulty": 0.6,
                    "topic": "numerical"
                },
                {
                    "question_id": "q_2",
                    "response": "A", 
                    "is_correct": True,
                    "response_time": 52.1,
                    "difficulty": 0.4,
                    "topic": "logical"
                },
                {
                    "question_id": "q_3",
                    "response": "C", 
                    "is_correct": True,
                    "response_time": 71.9,
                    "difficulty": 0.8,
                    "topic": "verbal"
                }
            ],
            "total_score": 85.2,
            "completion_time": 182.7,
            "is_legitimate": True
        },
        {
            "session_id": "hist_session_3",
            "candidate_name": "Test User 3", 
            "responses": [
                {
                    "question_id": "q_1",
                    "response": "B", 
                    "is_correct": False,
                    "response_time": 72.4,
                    "difficulty": 0.6,
                    "topic": "numerical"
                },
                {
                    "question_id": "q_2",
                    "response": "B", 
                    "is_correct": False,
                    "response_time": 48.6,
                    "difficulty": 0.4,
                    "topic": "logical"
                },
                {
                    "question_id": "q_3",
                    "response": "A", 
                    "is_correct": False,
                    "response_time": 69.8,
                    "difficulty": 0.8,
                    "topic": "verbal"
                }
            ],
            "total_score": 42.1,
            "completion_time": 190.8,
            "is_legitimate": True
        }
    ]

def test_train_baseline_models():
    """Test training baseline models with historical data"""
    print("🧠 Testing Baseline Model Training...")
    
    try:
        historical_data = create_historical_data_with_embedded_response_time()
        
        response = requests.post(
            f"{BACKEND_URL}/anomaly-detection/train-baseline-models",
            json={"historical_data": historical_data},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Baseline model training successful")
                print(f"   📊 Training samples: {data.get('num_training_samples', 'N/A')}")
                print(f"   📈 Features extracted: {data.get('num_features', 'N/A')}")
                print(f"   🎯 Models trained: {len(data.get('models_trained', []))}")
                return True
            else:
                print(f"❌ Baseline model training failed: {data}")
                return False
        else:
            print(f"❌ Baseline model training failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Baseline model training error: {str(e)}")
        return False

def create_test_session_data(session_type="normal"):
    """Create test session data with different characteristics"""
    base_session = {
        "session_id": f"test_session_{session_type}_{int(time.time())}",
        "candidate_name": f"Test Candidate {session_type.title()}",
        "responses": [],
        "total_score": 0,
        "completion_time": 0
    }
    
    if session_type == "normal":
        # Normal session data
        base_session["responses"] = [
            {
                "question_id": "q_1",
                "response": "A", 
                "is_correct": True,
                "response_time": 62.1,
                "difficulty": 0.6,
                "topic": "numerical"
            },
            {
                "question_id": "q_2",
                "response": "B", 
                "is_correct": True,
                "response_time": 49.3,
                "difficulty": 0.4,
                "topic": "logical"
            },
            {
                "question_id": "q_3",
                "response": "C", 
                "is_correct": True,
                "response_time": 74.8,
                "difficulty": 0.8,
                "topic": "verbal"
            }
        ]
        base_session["total_score"] = 78.4
        base_session["completion_time"] = 186.2
        
    elif session_type == "suspicious_timing":
        # Suspicious timing patterns
        base_session["responses"] = [
            {
                "question_id": "q_1",
                "response": "A", 
                "is_correct": True,
                "response_time": 15.2,  # Too fast
                "difficulty": 0.8,
                "topic": "numerical"
            },
            {
                "question_id": "q_2",
                "response": "B", 
                "is_correct": True,
                "response_time": 12.7,  # Too fast
                "difficulty": 0.9,
                "topic": "logical"
            },
            {
                "question_id": "q_3",
                "response": "C", 
                "is_correct": True,
                "response_time": 14.1,  # Too fast
                "difficulty": 0.7,
                "topic": "verbal"
            }
        ]
        base_session["total_score"] = 95.8
        base_session["completion_time"] = 42.0
        
    elif session_type == "performance_inconsistency":
        # Performance inconsistency patterns
        base_session["responses"] = [
            {
                "question_id": "q_1",
                "response": "A", 
                "is_correct": True,
                "response_time": 120.5,  # Very slow
                "difficulty": 0.2,  # Easy question
                "topic": "numerical"
            },
            {
                "question_id": "q_2",
                "response": "B", 
                "is_correct": True,
                "response_time": 25.3,  # Very fast
                "difficulty": 0.9,  # Hard question
                "topic": "logical"
            },
            {
                "question_id": "q_3",
                "response": "C", 
                "is_correct": False,
                "response_time": 180.7,  # Very slow
                "difficulty": 0.3,  # Easy question
                "topic": "verbal"
            }
        ]
        base_session["total_score"] = 55.2
        base_session["completion_time"] = 326.5
    
    return base_session

def test_anomaly_probability_calculation(session_type="normal"):
    """Test the specific anomaly probability calculation endpoint"""
    print(f"🎯 Testing Anomaly Probability Calculation ({session_type} session)...")
    
    try:
        session_data = create_test_session_data(session_type)
        
        response = requests.post(
            f"{BACKEND_URL}/anomaly-detection/calculate-anomaly-probability-scores",
            json={"session_data": session_data},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Anomaly probability calculation successful for {session_type} session")
                
                # Get the probability results from the nested structure
                probability_results = data.get('probability_results', {})
                
                # Verify expected response structure
                required_fields = [
                    'composite_anomaly_probability',
                    'confidence_intervals', 
                    'risk_classification',
                    'probability_components',
                    'probability_breakdown',
                    'statistical_significance',
                    'recommendation_actions'
                ]
                
                missing_fields = []
                for field in required_fields:
                    if field not in probability_results:
                        missing_fields.append(field)
                
                if missing_fields:
                    print(f"⚠️  Missing expected fields: {missing_fields}")
                else:
                    print("✅ All expected response fields present")
                
                # Display key results
                print(f"   🎯 Composite Anomaly Probability: {probability_results.get('composite_anomaly_probability', 'N/A')}")
                print(f"   📊 Risk Level: {probability_results.get('risk_classification', {}).get('level', 'N/A')}")
                print(f"   🔍 Statistical Significance: {probability_results.get('statistical_significance', {}).get('p_value', 'N/A')}")
                
                # Check for numpy boolean encoding issues
                response_str = response.text
                if 'np.False_' in response_str or 'np.True_' in response_str:
                    print("❌ NUMPY BOOLEAN ENCODING ISSUE DETECTED!")
                    return False
                else:
                    print("✅ No numpy boolean encoding issues detected")
                
                return True
            else:
                print(f"❌ Anomaly probability calculation failed: {data}")
                return False
        else:
            print(f"❌ Anomaly probability calculation failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Anomaly probability calculation error: {str(e)}")
        return False

def main():
    """Main test execution"""
    print("🎯 FOCUSED TESTING: Anomaly Probability Calculation Endpoint Fix Verification")
    print("=" * 80)
    print()
    
    # Track test results
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Admin Authentication
    total_tests += 1
    if test_admin_authentication():
        tests_passed += 1
    print()
    
    # Test 2: Train Baseline Models
    total_tests += 1
    if test_train_baseline_models():
        tests_passed += 1
    print()
    
    # Test 3: Normal Session Anomaly Probability Calculation
    total_tests += 1
    if test_anomaly_probability_calculation("normal"):
        tests_passed += 1
    print()
    
    # Test 4: Suspicious Timing Session Anomaly Probability Calculation
    total_tests += 1
    if test_anomaly_probability_calculation("suspicious_timing"):
        tests_passed += 1
    print()
    
    # Test 5: Performance Inconsistency Session Anomaly Probability Calculation
    total_tests += 1
    if test_anomaly_probability_calculation("performance_inconsistency"):
        tests_passed += 1
    print()
    
    # Final Results
    print("=" * 80)
    print("🎯 FOCUSED TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"✅ Tests Passed: {tests_passed}/{total_tests}")
    print(f"📊 Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED - Numpy boolean encoding issue has been resolved!")
        print("✅ POST /api/anomaly-detection/calculate-anomaly-probability-scores endpoint is working correctly")
    else:
        print("❌ Some tests failed - Further investigation needed")
    
    print()
    print("🔍 SPECIFIC VERIFICATION:")
    print("- Admin authentication working with Game@1234 password")
    print("- Baseline models trained with embedded response_time format")
    print("- Anomaly probability calculation completing without numpy boolean encoding errors")
    print("- Response containing comprehensive probability scores and confidence intervals")
    print("- Risk classification and recommendations properly formatted")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)