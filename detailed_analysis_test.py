#!/usr/bin/env python3
"""
Detailed Analysis Test for Statistical Anomaly Analyzer

This test validates the detailed response structures, scoring algorithms,
and specific functionality of each endpoint.
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import random

BACKEND_URL = "https://integrity-check-2.preview.emergentagent.com/api"

def create_comprehensive_session_data():
    """Create comprehensive session data with all required fields"""
    session_id = str(uuid.uuid4())
    base_time = datetime.utcnow() - timedelta(hours=2)
    
    responses = []
    for i in range(30):
        response_time = random.uniform(20, 180)
        difficulty = random.uniform(0.1, 0.9)
        
        # Create realistic accuracy based on difficulty
        accuracy_prob = max(0.1, 1.0 - (difficulty * 0.8))
        is_correct = random.random() < accuracy_prob
        
        # Add some answer changes for pattern analysis
        previous_response = None
        if i > 5 and random.random() < 0.15:  # 15% chance of answer change
            previous_response = random.choice(['A', 'B', 'C', 'D'])
        
        response_data = {
            'question_id': f'q_{i+1}',
            'response': random.choice(['A', 'B', 'C', 'D']),
            'is_correct': is_correct,
            'response_time': response_time,
            'difficulty': difficulty,
            'topic': random.choice(['numerical_reasoning', 'logical_reasoning', 'verbal_comprehension', 'spatial_reasoning']),
            'timestamp': (base_time + timedelta(seconds=sum(30 + j*45 for j in range(i)))).isoformat()
        }
        
        if previous_response:
            response_data['previous_response'] = previous_response
            response_data['change_timestamp'] = (base_time + timedelta(seconds=sum(30 + j*45 for j in range(i)) - 10)).isoformat()
        
        responses.append(response_data)
    
    return {
        'session_id': session_id,
        'candidate_name': 'Comprehensive Test Candidate',
        'responses': responses,
        'session_metadata': {
            'start_time': base_time.isoformat(),
            'end_time': (base_time + timedelta(hours=2, minutes=15)).isoformat(),
            'ip_address': '203.0.113.42',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'timezone': 'America/New_York',
            'location': {'country': 'US', 'region': 'NY', 'city': 'New York'}
        }
    }

def validate_detailed_analysis_structure(analysis_results, analysis_type):
    """Validate the detailed analysis structure"""
    print(f"🔍 Validating {analysis_type} detailed analysis structure...")
    
    required_top_level = ['success', 'session_id', 'analysis_type', 'analysis_timestamp', 'detailed_analysis']
    missing_top_level = [field for field in required_top_level if field not in analysis_results]
    
    if missing_top_level:
        print(f"❌ Missing top-level fields: {missing_top_level}")
        return False
    
    detailed_analysis = analysis_results.get('detailed_analysis', {})
    
    if analysis_type == 'answer_pattern_irregularities':
        expected_analyses = ['distribution_analysis', 'sequence_analysis', 'clustering_analysis', 'change_analysis', 'uniformity_analysis']
        
        for analysis_name in expected_analyses:
            if analysis_name in detailed_analysis:
                analysis_data = detailed_analysis[analysis_name]
                if analysis_data.get('available'):
                    print(f"✅ {analysis_name}: Available with data")
                else:
                    print(f"⚠️  {analysis_name}: Not available - {analysis_data.get('message', 'No message')}")
            else:
                print(f"❌ Missing analysis: {analysis_name}")
        
        # Check scoring
        score = analysis_results.get('irregularity_score', 0)
        risk_level = analysis_results.get('risk_level', 'UNKNOWN')
        print(f"📊 Irregularity Score: {score:.3f}, Risk Level: {risk_level}")
        
        # Validate score range
        if 0 <= score <= 1:
            print("✅ Score in valid range [0, 1]")
        else:
            print(f"❌ Score out of range: {score}")
    
    elif analysis_type == 'difficulty_progression_anomalies':
        expected_analyses = ['correlation_analysis', 'binned_analysis', 'progression_analysis', 'outlier_analysis', 'topic_analysis']
        
        for analysis_name in expected_analyses:
            if analysis_name in detailed_analysis:
                analysis_data = detailed_analysis[analysis_name]
                if analysis_data.get('available'):
                    print(f"✅ {analysis_name}: Available with data")
                    
                    # Special validation for correlation analysis
                    if analysis_name == 'correlation_analysis' and analysis_data.get('available'):
                        correlation = analysis_data.get('correlation_coefficient')
                        p_value = analysis_data.get('p_value')
                        if correlation is not None and p_value is not None:
                            print(f"   📈 Correlation: {correlation:.3f}, p-value: {p_value:.3f}")
                        
                else:
                    print(f"⚠️  {analysis_name}: Not available - {analysis_data.get('message', 'No message')}")
            else:
                print(f"❌ Missing analysis: {analysis_name}")
        
        # Check scoring
        score = analysis_results.get('anomaly_score', 0)
        risk_level = analysis_results.get('risk_level', 'UNKNOWN')
        print(f"📊 Anomaly Score: {score:.3f}, Risk Level: {risk_level}")
    
    elif analysis_type == 'collaborative_cheating_patterns':
        expected_analyses = ['internal_analysis', 'cross_session_analysis', 'timing_coordination_analysis', 'pattern_similarity_analysis', 'clustering_analysis']
        
        for analysis_name in expected_analyses:
            if analysis_name in detailed_analysis:
                analysis_data = detailed_analysis[analysis_name]
                if analysis_data.get('available'):
                    print(f"✅ {analysis_name}: Available with data")
                else:
                    print(f"⚠️  {analysis_name}: Not available - {analysis_data.get('message', 'No message')}")
            else:
                print(f"❌ Missing analysis: {analysis_name}")
        
        # Check scoring
        score = analysis_results.get('collaboration_score', 0)
        risk_level = analysis_results.get('risk_level', 'UNKNOWN')
        print(f"📊 Collaboration Score: {score:.3f}, Risk Level: {risk_level}")
    
    return True

def test_comprehensive_analysis():
    """Test comprehensive analysis with detailed validation"""
    print("🚀 Starting Comprehensive Analysis Testing")
    print("=" * 80)
    
    session_data = create_comprehensive_session_data()
    session_id = session_data['session_id']
    
    print(f"📋 Test Session ID: {session_id}")
    print(f"📊 Total Responses: {len(session_data['responses'])}")
    print(f"🎯 Topics Covered: {set(r['topic'] for r in session_data['responses'])}")
    print(f"📈 Difficulty Range: {min(r['difficulty'] for r in session_data['responses']):.2f} - {max(r['difficulty'] for r in session_data['responses']):.2f}")
    print()
    
    # Test 1: Answer Pattern Analysis
    print("🔍 Testing Answer Pattern Analysis...")
    try:
        response = requests.post(
            f"{BACKEND_URL}/statistical-analysis/detect-answer-pattern-irregularities",
            json={"session_data": session_data},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis_results = data['analysis_results']
                validate_detailed_analysis_structure(analysis_results, 'answer_pattern_irregularities')
                
                # Check recommendations
                recommendations = analysis_results.get('recommendations', [])
                print(f"💡 Recommendations: {len(recommendations)} provided")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"   {i}. {rec}")
                
                # Check statistical significance
                significance = analysis_results.get('statistical_significance', {})
                print(f"📊 Statistical Significance: {significance}")
                
            else:
                print(f"❌ Analysis failed: {data}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "-" * 60 + "\n")
    
    # Test 2: Difficulty Progression Analysis
    print("📊 Testing Difficulty Progression Analysis...")
    try:
        response = requests.post(
            f"{BACKEND_URL}/statistical-analysis/analyze-difficulty-progression-anomalies",
            json={"session_data": session_data},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis_results = data['analysis_results']
                validate_detailed_analysis_structure(analysis_results, 'difficulty_progression_anomalies')
                
                # Check difficulty range info
                difficulty_range = analysis_results.get('difficulty_range', {})
                print(f"📈 Difficulty Analysis Range: {difficulty_range}")
                
                # Check questions analyzed
                questions_analyzed = analysis_results.get('total_questions_analyzed', 0)
                print(f"🔢 Questions Analyzed: {questions_analyzed}")
                
            else:
                print(f"❌ Analysis failed: {data}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "-" * 60 + "\n")
    
    # Test 3: Collaborative Cheating Analysis with Comparison Sessions
    print("👥 Testing Collaborative Cheating Analysis...")
    
    # Create comparison sessions
    comparison_sessions = []
    for i in range(2):
        comp_session = create_comprehensive_session_data()
        # Make some responses similar to test collaboration detection
        for j in range(min(10, len(comp_session['responses']))):
            if random.random() < 0.4:  # 40% similarity
                comp_session['responses'][j]['response'] = session_data['responses'][j]['response']
        comparison_sessions.append(comp_session)
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/statistical-analysis/detect-collaborative-cheating-patterns",
            json={
                "session_data": session_data,
                "comparison_sessions": comparison_sessions
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analysis_results = data['analysis_results']
                validate_detailed_analysis_structure(analysis_results, 'collaborative_cheating_patterns')
                
                # Check comparison session count
                comparison_count = analysis_results.get('comparison_sessions_count', 0)
                print(f"🔗 Comparison Sessions: {comparison_count}")
                
            else:
                print(f"❌ Analysis failed: {data}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "-" * 60 + "\n")
    
    # Test 4: Database Storage Verification
    print("💾 Testing Database Storage...")
    try:
        response = requests.get(
            f"{BACKEND_URL}/statistical-analysis/session-analysis/{session_id}",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                analyses = data.get('analyses', [])
                print(f"✅ Database Storage: {len(analyses)} analyses stored")
                
                for analysis in analyses:
                    analysis_type = analysis.get('analysis_type', 'unknown')
                    risk_level = analysis.get('risk_level', 'unknown')
                    timestamp = analysis.get('analysis_timestamp', 'unknown')
                    print(f"   📋 {analysis_type}: {risk_level} risk, {timestamp}")
                
            else:
                print(f"❌ Retrieval failed: {data}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 80)
    print("🎯 COMPREHENSIVE TESTING COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_comprehensive_analysis()