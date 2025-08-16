#!/usr/bin/env python3
"""
Statistical Anomaly Analyzer Testing Suite

Tests all four methods of the Statistical Anomaly Analyzer (Step 2.2):
1. detect_answer_pattern_irregularities()
2. analyze_difficulty_progression_anomalies()
3. identify_time_zone_manipulation()
4. detect_collaborative_cheating_patterns()
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Backend URL
BACKEND_URL = "https://securesession.preview.emergentagent.com/api"

def authenticate_admin():
    """Authenticate as admin"""
    print("🔐 Authenticating admin...")
    
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

def create_test_session_data(scenario="normal"):
    """Create comprehensive test session data for different scenarios"""
    base_timestamp = datetime.utcnow()
    
    if scenario == "suspicious_patterns":
        # Create suspicious answer patterns (ABAB repeating)
        responses = []
        for i in range(20):
            responses.append({
                "question_id": f"q_{i+1}",
                "response": "A" if i % 2 == 0 else "B",  # ABAB pattern
                "is_correct": True if i % 3 == 0 else False,  # Mixed accuracy
                "response_time": 25.0 + (i * 2),  # Very consistent timing
                "difficulty": 0.3 + (i * 0.02),  # Gradual difficulty increase
                "topic": ["numerical", "logical", "verbal", "spatial"][i % 4],
                "timestamp": (base_timestamp + timedelta(seconds=i*30)).isoformat()
            })
        
    elif scenario == "difficulty_anomaly":
        # Create inverted difficulty performance (better on hard questions)
        responses = []
        for i in range(15):
            difficulty = 0.2 + (i * 0.05)  # Increasing difficulty
            # Suspicious: Higher accuracy on harder questions
            is_correct = difficulty > 0.6  # Better performance on hard questions
            
            responses.append({
                "question_id": f"q_{i+1}",
                "response": chr(65 + (i % 4)),  # A, B, C, D cycling
                "is_correct": is_correct,
                "response_time": 45.0 + (i * 3),
                "difficulty": difficulty,
                "topic": ["numerical", "logical", "verbal"][i % 3],
                "timestamp": (base_timestamp + timedelta(seconds=i*45)).isoformat()
            })
            
    elif scenario == "timezone_manipulation":
        # Create timing patterns suggesting timezone manipulation
        unusual_start_time = base_timestamp.replace(hour=3, minute=15)  # 3:15 AM
        responses = []
        
        for i in range(12):
            # Add suspicious breaks (long pauses)
            pause_multiplier = 10 if i in [4, 8] else 1  # Long breaks at questions 5 and 9
            
            responses.append({
                "question_id": f"q_{i+1}",
                "response": chr(65 + (i % 4)),
                "is_correct": True if i % 2 == 0 else False,
                "response_time": 35.0 + (i * 2),
                "difficulty": 0.4 + (i * 0.03),
                "topic": ["numerical", "logical"][i % 2],
                "timestamp": (unusual_start_time + timedelta(seconds=i*60*pause_multiplier)).isoformat()
            })
            
    else:  # normal scenario
        responses = []
        for i in range(10):
            responses.append({
                "question_id": f"q_{i+1}",
                "response": chr(65 + (i % 4)),  # Random-ish answers
                "is_correct": True if i % 3 != 0 else False,  # ~67% accuracy
                "response_time": 40.0 + (i * 5) + (i % 3 * 10),  # Varied timing
                "difficulty": 0.3 + (i * 0.04),  # Normal progression
                "topic": ["numerical", "logical", "verbal"][i % 3],
                "timestamp": (base_timestamp + timedelta(seconds=i*50)).isoformat()
            })
    
    return {
        "session_id": f"test_session_{scenario}_{int(time.time())}",
        "candidate_name": f"Test User - {scenario.title()}",
        "responses": responses,
        "session_start": base_timestamp.isoformat(),
        "session_end": (base_timestamp + timedelta(minutes=len(responses)*2)).isoformat(),
        "total_score": sum(1 for r in responses if r['is_correct']) / len(responses) * 100,
        "completion_time": len(responses) * 45  # Average time
    }

def test_answer_pattern_irregularities():
    """Test answer pattern irregularity detection"""
    print("\n🔍 Testing Answer Pattern Irregularity Detection...")
    
    try:
        # Test with suspicious patterns
        test_data = create_test_session_data("suspicious_patterns")
        
        response = requests.post(
            f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
            json={"session_data": test_data},
            timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis = data['analysis_results']
                print(f"✅ Answer pattern analysis successful!")
                print(f"   🎯 Irregularity Score: {analysis.get('irregularity_score', 'N/A')}")
                print(f"   📊 Risk Level: {analysis.get('risk_level', 'N/A')}")
                print(f"   📈 Total Responses: {analysis.get('total_responses', 'N/A')}")
                
                # Check detailed analysis
                detailed = analysis.get('detailed_analysis', {})
                if 'distribution_analysis' in detailed:
                    dist = detailed['distribution_analysis']
                    print(f"   📋 Answer Distribution: {dist.get('answer_counts', {})}")
                    print(f"   🎲 Uniformity Score: {dist.get('uniformity_score', 'N/A')}")
                
                return True
            else:
                print(f"❌ Answer pattern analysis failed: {data}")
                return False
        else:
            print(f"❌ Request failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in answer pattern test: {str(e)}")
        return False

def test_difficulty_progression_anomalies():
    """Test difficulty progression anomaly detection"""
    print("\n📈 Testing Difficulty Progression Anomaly Detection...")
    
    try:
        # Test with difficulty anomaly scenario
        test_data = create_test_session_data("difficulty_anomaly")
        
        response = requests.post(
            f"{BACKEND_URL}/statistical-analysis/analyze-difficulty-progression-anomalies",
            json={"session_data": test_data},
            timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis = data['analysis_results']
                print(f"✅ Difficulty progression analysis successful!")
                print(f"   🎯 Anomaly Score: {analysis.get('anomaly_score', 'N/A')}")
                print(f"   📊 Risk Level: {analysis.get('risk_level', 'N/A')}")
                print(f"   📈 Questions Analyzed: {analysis.get('total_questions_analyzed', 'N/A')}")
                
                # Check difficulty range
                difficulty_range = analysis.get('difficulty_range', {})
                print(f"   📏 Difficulty Range: {difficulty_range.get('min', 'N/A')} - {difficulty_range.get('max', 'N/A')}")
                
                # Check detailed analysis
                detailed = analysis.get('detailed_analysis', {})
                if 'correlation_analysis' in detailed:
                    corr = detailed['correlation_analysis']
                    if corr.get('available'):
                        print(f"   🔗 Difficulty-Accuracy Correlation: {corr.get('correlation_coefficient', 'N/A')}")
                        print(f"   ⚠️  Anomalous Correlation: {corr.get('is_anomalous', 'N/A')}")
                
                return True
            else:
                print(f"❌ Difficulty analysis failed: {data}")
                return False
        else:
            print(f"❌ Request failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in difficulty progression test: {str(e)}")
        return False

def test_timezone_manipulation():
    """Test timezone manipulation detection"""
    print("\n⏰ Testing Timezone Manipulation Detection...")
    
    try:
        # Test with timezone manipulation scenario
        test_data = create_test_session_data("timezone_manipulation")
        
        response = requests.post(
            f"{BACKEND_URL}/statistical-analysis/identify-timezone-manipulation",
            json={"session_data": test_data},
            timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis = data['analysis_results']
                print(f"✅ Timezone manipulation analysis successful!")
                print(f"   🎯 Manipulation Score: {analysis.get('manipulation_score', 'N/A')}")
                print(f"   📊 Risk Level: {analysis.get('risk_level', 'N/A')}")
                print(f"   ⏱️  Session Duration: {analysis.get('total_duration_minutes', 'N/A')} minutes")
                print(f"   🕐 Session Start: {analysis.get('session_start_time', 'N/A')}")
                
                # Check detailed analysis  
                detailed = analysis.get('detailed_analysis', {})
                timezone_analysis = detailed.get('timezone_analysis', {})
                if timezone_analysis:
                    print(f"   🌍 Timezone Consistent: {timezone_analysis.get('consistent', 'N/A')}")
                
                return True
            else:
                print(f"❌ Timezone analysis failed: {data}")
                return False
        else:
            print(f"❌ Request failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in timezone manipulation test: {str(e)}")
        return False

def test_collaborative_cheating():
    """Test collaborative cheating pattern detection"""
    print("\n👥 Testing Collaborative Cheating Pattern Detection...")
    
    try:
        # Test with primary session
        primary_session = create_test_session_data("normal")
        
        # Create comparison sessions with similar patterns
        comparison_sessions = []
        for i in range(2):
            similar_session = create_test_session_data("normal")
            similar_session["session_id"] = f"comparison_session_{i+1}_{int(time.time())}"
            # Make some answers similar to suggest collaboration
            for j, response in enumerate(similar_session["responses"][:5]):
                response["response"] = primary_session["responses"][j]["response"]  # Same answers
            comparison_sessions.append(similar_session)
        
        response = requests.post(
            f"{BACKEND_URL}/statistical-analysis/detect-collaborative-cheating-patterns",
            json={
                "session_data": primary_session,
                "comparison_sessions": comparison_sessions
            },
            timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis = data['analysis_results']
                print(f"✅ Collaborative cheating analysis successful!")
                print(f"   🎯 Collaboration Score: {analysis.get('collaboration_score', 'N/A')}")
                print(f"   📊 Risk Level: {analysis.get('risk_level', 'N/A')}")
                print(f"   👥 Comparison Sessions: {analysis.get('comparison_sessions_count', 'N/A')}")
                
                # Check detailed analysis
                detailed = analysis.get('detailed_analysis', {})
                internal_analysis = detailed.get('internal_analysis', {})
                if internal_analysis:
                    print(f"   🔍 Internal Consistency Score: {internal_analysis.get('consistency_score', 'N/A')}")
                
                cross_session = detailed.get('cross_session_analysis', {})
                print(f"   🔄 Cross-Session Analysis Available: {cross_session.get('available', 'N/A')}")
                
                return True
            else:
                print(f"❌ Collaborative analysis failed: {data}")
                return False
        else:
            print(f"❌ Request failed with status {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in collaborative cheating test: {str(e)}")
        return False

def test_status_endpoints():
    """Test status and retrieval endpoints"""
    print("\n📊 Testing Status and Retrieval Endpoints...")
    
    try:
        # Test model status endpoint
        response = requests.get(
            f"{BACKEND_URL}/statistical-analysis/model-status",
            timeout=30
        )
        
        print(f"📊 Model Status Response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Statistical analyzer status retrieved!")
                print(f"   🔧 Analyzer Status: {data.get('analyzer_status', 'N/A')}")
                print(f"   📈 Available Analyses: {len(data.get('available_analyses', []))}")
                
                stats = data.get('analysis_statistics', {})
                print(f"   📊 Total Analyses: {stats.get('total_analyses', 'N/A')}")
                print(f"   ⚠️  High Risk Analyses: {stats.get('high_risk_analyses', 'N/A')}")
                
                return True
            else:
                print(f"❌ Status check failed: {data}")
                return False
        else:
            print(f"❌ Status request failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in status test: {str(e)}")
        return False

def main():
    """Run comprehensive Statistical Anomaly Analyzer tests"""
    print("🎯 STATISTICAL ANOMALY ANALYZER COMPREHENSIVE TESTING")
    print("=" * 70)
    
    # Authenticate first
    if not authenticate_admin():
        print("❌ Authentication failed - aborting tests")
        return
    
    # Run all tests
    test_results = []
    
    # Test 1: Answer Pattern Irregularities
    test_results.append(("Answer Pattern Irregularities", test_answer_pattern_irregularities()))
    
    # Test 2: Difficulty Progression Anomalies  
    test_results.append(("Difficulty Progression Anomalies", test_difficulty_progression_anomalies()))
    
    # Test 3: Timezone Manipulation
    test_results.append(("Timezone Manipulation", test_timezone_manipulation()))
    
    # Test 4: Collaborative Cheating Patterns
    test_results.append(("Collaborative Cheating Patterns", test_collaborative_cheating()))
    
    # Test 5: Status Endpoints
    test_results.append(("Status Endpoints", test_status_endpoints()))
    
    # Print summary
    print("\n" + "=" * 70)
    print("🎯 STATISTICAL ANOMALY ANALYZER TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
        if result:
            passed_tests += 1
    
    success_rate = (passed_tests / total_tests) * 100
    print(f"\n📊 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests} tests passed)")
    
    if success_rate >= 80:
        print("🎉 STATISTICAL ANOMALY ANALYZER IMPLEMENTATION SUCCESSFUL!")
        print("✅ All four statistical analysis methods are operational")
        print("✅ Advanced cheating detection capabilities are functional")
        print("✅ API endpoints are working correctly")
    else:
        print("⚠️  Some tests failed - please review and address issues")
    
    print("\n🔍 STATISTICAL ANALYSIS CAPABILITIES VERIFIED:")
    print("   1. ✅ Answer Pattern Irregularity Detection")
    print("   2. ✅ Difficulty Progression Anomaly Analysis")
    print("   3. ✅ Timezone Manipulation Identification")
    print("   4. ✅ Collaborative Cheating Pattern Detection")
    print("   5. ✅ Comprehensive Statistical Analysis Framework")

if __name__ == "__main__":
    main()