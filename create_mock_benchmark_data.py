#!/usr/bin/env python3
"""
Create Mock Benchmark Data
Creates realistic test session and result data for Industry Benchmark Engine testing
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import uuid

# MongoDB connection
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database"

async def create_mock_data():
    """Create mock test session and result data"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Generate test session ID
    test_session_id = str(uuid.uuid4())
    print(f"Creating mock data for session ID: {test_session_id}")
    
    # Mock session data
    mock_session_data = {
        "session_id": test_session_id,
        "token": "TEST123",
        "config_id": str(uuid.uuid4()),
        "candidate_name": "Test Candidate",
        "candidate_email": "test@example.com",
        "status": "completed",
        "start_time": datetime.utcnow(),
        "end_time": datetime.utcnow(),
        "current_question_index": 55,
        "questions_sequence": [str(i) for i in range(1, 56)],
        "answers": {
            str(i): {
                "selected": ["A", "B", "C", "D"][i % 4],
                "correct": i % 3 == 0,  # Every 3rd question correct
                "time_taken": 45 + (i % 30)
            } for i in range(1, 56)
        },
        "time_per_question": {
            str(i): 45.0 + (i % 30) for i in range(1, 56)
        },
        "adaptive_score": 75.5,
        "ip_address": "127.0.0.1",
        "user_agent": "Test Agent",
        "created_at": datetime.utcnow(),
        
        # Enhanced CAT: Multi-dimensional IRT
        "theta_estimates": {
            "numerical_reasoning": 0.8,
            "logical_reasoning": 0.6,
            "verbal_comprehension": 0.9,
            "spatial_reasoning": 0.4
        },
        "se_estimates": {
            "numerical_reasoning": 0.15,
            "logical_reasoning": 0.18,
            "verbal_comprehension": 0.12,
            "spatial_reasoning": 0.22
        },
        "confidence_intervals": {
            "numerical_reasoning": {"lower": 0.65, "upper": 0.95},
            "logical_reasoning": {"lower": 0.42, "upper": 0.78},
            "verbal_comprehension": {"lower": 0.78, "upper": 1.02},
            "spatial_reasoning": {"lower": 0.18, "upper": 0.62}
        },
        "cat_se": 0.16,
        "cat_info_sum": 38.5,
        "ability_history": [],
        
        # Enhanced CAT: Fraud Detection
        "fraud_score": 0.1,
        "fraud_flags": [],
        "response_patterns": {},
        "timing_anomalies": [],
        "behavioral_flags": []
    }
    
    # Mock result data
    mock_result_data = {
        "result_id": str(uuid.uuid4()),
        "session_id": test_session_id,
        "overall_score": 65.5,
        "percentage_score": 65.5,
        "topic_scores": {
            "numerical_reasoning": {
                "score": 66.7,
                "correct": 8,
                "total": 12,
                "percentage": 66.7,
                "difficulty_average": 0.6,
                "time": 540
            },
            "logical_reasoning": {
                "score": 66.7,
                "correct": 10,
                "total": 15,
                "percentage": 66.7,
                "difficulty_average": 0.5,
                "time": 675
            },
            "verbal_comprehension": {
                "score": 80.0,
                "correct": 12,
                "total": 15,
                "percentage": 80.0,
                "difficulty_average": 0.7,
                "time": 675
            },
            "spatial_reasoning": {
                "score": 46.2,
                "correct": 6,
                "total": 13,
                "percentage": 46.2,
                "difficulty_average": 0.4,
                "time": 585
            }
        },
        "difficulty_performance": {
            "easy": {"correct": 15, "total": 18, "percentage": 83.3},
            "medium": {"correct": 15, "total": 22, "percentage": 68.2},
            "hard": {"correct": 6, "total": 15, "percentage": 40.0}
        },
        "total_time_taken": 2475,  # seconds
        "questions_attempted": 55,
        "questions_correct": 36,
        "strengths": ["Verbal Comprehension", "Numerical Reasoning"],
        "improvement_areas": ["Spatial Reasoning", "Logical Reasoning"],
        "percentile_rank": 65.0,
        "recommendations": [
            "Focus on spatial reasoning practice",
            "Improve logical deduction skills",
            "Continue building on verbal strengths"
        ],
        "detailed_analysis": "Strong performance in verbal comprehension with room for improvement in spatial reasoning.",
        "created_at": datetime.utcnow(),
        
        # Enhanced CAT: Multi-dimensional Results
        "theta_final": {
            "numerical_reasoning": 0.8,
            "logical_reasoning": 0.6,
            "verbal_comprehension": 0.9,
            "spatial_reasoning": 0.4
        },
        "se_final": {
            "numerical_reasoning": 0.15,
            "logical_reasoning": 0.18,
            "verbal_comprehension": 0.12,
            "spatial_reasoning": 0.22
        },
        "confidence_intervals_final": {
            "numerical_reasoning": {"lower": 0.65, "upper": 0.95},
            "logical_reasoning": {"lower": 0.42, "upper": 0.78},
            "verbal_comprehension": {"lower": 0.78, "upper": 1.02},
            "spatial_reasoning": {"lower": 0.18, "upper": 0.62}
        },
        "measurement_precision": 6.25,
        "adaptive_efficiency": 0.85,
        
        # Enhanced CAT: Fraud Analysis Results
        "fraud_analysis": {
            "overall_risk": "low",
            "confidence": 0.95,
            "indicators": []
        },
        "integrity_score": 0.95,
        "reliability_score": 0.92
    }
    
    try:
        # Insert session data
        await db.aptitude_sessions.insert_one(mock_session_data)
        print("✅ Mock session data inserted successfully")
        
        # Insert result data
        await db.aptitude_results.insert_one(mock_result_data)
        print("✅ Mock result data inserted successfully")
        
        print(f"\n📊 Mock Data Summary:")
        print(f"   Session ID: {test_session_id}")
        print(f"   Overall Score: {mock_result_data['percentage_score']}%")
        print(f"   Questions Correct: {mock_result_data['questions_correct']}/{mock_result_data['questions_attempted']}")
        print(f"   Topic Performance:")
        for topic, scores in mock_result_data['topic_scores'].items():
            print(f"     {topic.replace('_', ' ').title()}: {scores['percentage']:.1f}%")
        
        return test_session_id
        
    except Exception as e:
        print(f"❌ Error creating mock data: {e}")
        return None
    finally:
        client.close()

async def main():
    """Main function"""
    print("🔧 Creating Mock Benchmark Data for Industry Benchmark Engine Testing")
    print("=" * 70)
    
    session_id = await create_mock_data()
    
    if session_id:
        print(f"\n✅ Mock data creation completed successfully!")
        print(f"📋 Use this session ID for testing: {session_id}")
        
        # Write session ID to a file for the test script to use
        with open('/app/test_session_id.txt', 'w') as f:
            f.write(session_id)
        print(f"📝 Session ID saved to /app/test_session_id.txt")
    else:
        print(f"\n❌ Mock data creation failed!")
    
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())