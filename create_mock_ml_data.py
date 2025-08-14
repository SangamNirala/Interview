#!/usr/bin/env python3
"""
Create mock aptitude session and result data for ML prediction testing
"""

import asyncio
import os
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import uuid
import random
import json

# MongoDB connection
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database"

async def create_mock_data():
    """Create mock aptitude sessions and results for ML testing"""
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🎯 Creating mock aptitude session and result data for ML testing...")
    
    # Clear existing test data
    await db.aptitude_sessions.delete_many({"candidate_name": {"$regex": "^Test Candidate"}})
    await db.aptitude_results.delete_many({"session_id": {"$regex": "^test-session"}})
    
    sessions_created = 0
    results_created = 0
    
    # Create 25 mock sessions with results
    for i in range(25):
        session_id = f"test-session-{i+1:03d}"
        candidate_name = f"Test Candidate {i+1}"
        
        # Create realistic session data
        session_data = {
            "session_id": session_id,
            "candidate_name": candidate_name,
            "candidate_email": f"test{i+1}@example.com",
            "status": "completed",
            "start_time": datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            "end_time": None,
            "current_question_index": 45,
            "questions_sequence": [f"q_{j+1}" for j in range(45)],
            "answers": {},
            "time_per_question": {},
            "adaptive_score": random.uniform(-1.0, 1.0),
            "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            "theta_estimates": {
                "numerical_reasoning": random.uniform(-2.0, 2.0),
                "logical_reasoning": random.uniform(-2.0, 2.0),
                "verbal_comprehension": random.uniform(-2.0, 2.0),
                "spatial_reasoning": random.uniform(-2.0, 2.0)
            },
            "se_estimates": {
                "numerical_reasoning": random.uniform(0.3, 0.8),
                "logical_reasoning": random.uniform(0.3, 0.8),
                "verbal_comprehension": random.uniform(0.3, 0.8),
                "spatial_reasoning": random.uniform(0.3, 0.8)
            }
        }
        
        # Add realistic answers and timing data
        topics = ["numerical_reasoning", "logical_reasoning", "verbal_comprehension", "spatial_reasoning"]
        for j in range(45):
            question_id = f"q_{j+1}"
            topic = topics[j % 4]
            
            # Simulate realistic performance patterns
            base_accuracy = 0.6 + (session_data["theta_estimates"][topic] * 0.2)
            is_correct = random.random() < max(0.1, min(0.9, base_accuracy))
            
            session_data["answers"][question_id] = {
                "selected_answer": random.choice(["A", "B", "C", "D"]),
                "correct": is_correct,
                "question_topic": topic,
                "difficulty": random.choice(["easy", "medium", "hard"]),
                "timestamp": (datetime.utcnow() - timedelta(minutes=45-j)).isoformat()
            }
            
            # Realistic timing patterns
            base_time = 60 + random.randint(-20, 30)
            if not is_correct:
                base_time += random.randint(10, 40)  # Incorrect answers take longer
            
            session_data["time_per_question"][question_id] = {
                "time_taken": base_time,
                "start_time": (datetime.utcnow() - timedelta(minutes=45-j)).isoformat()
            }
        
        # Set end time
        session_data["end_time"] = session_data["start_time"] + timedelta(minutes=45)
        
        # Insert session
        await db.aptitude_sessions.insert_one(session_data)
        sessions_created += 1
        
        # Create corresponding result data
        correct_answers = sum(1 for ans in session_data["answers"].values() if ans["correct"])
        total_questions = len(session_data["answers"])
        overall_score = (correct_answers / total_questions) * 100
        
        # Calculate topic-wise scores
        topic_scores = {}
        for topic in topics:
            topic_answers = [ans for ans in session_data["answers"].values() if ans["question_topic"] == topic]
            topic_correct = sum(1 for ans in topic_answers if ans["correct"])
            topic_total = len(topic_answers)
            topic_percentage = (topic_correct / topic_total) * 100 if topic_total > 0 else 0
            
            topic_scores[topic] = {
                "score": topic_correct,
                "total": topic_total,
                "percentage": topic_percentage,
                "time": sum(session_data["time_per_question"][qid]["time_taken"] 
                           for qid, ans in session_data["answers"].items() 
                           if ans["question_topic"] == topic)
            }
        
        result_data = {
            "result_id": str(uuid.uuid4()),
            "session_id": session_id,
            "overall_score": correct_answers,
            "percentage_score": overall_score,
            "topic_scores": topic_scores,
            "difficulty_performance": {
                "easy": {"correct": 0, "total": 0, "percentage": 0},
                "medium": {"correct": 0, "total": 0, "percentage": 0},
                "hard": {"correct": 0, "total": 0, "percentage": 0}
            },
            "total_time_taken": sum(t["time_taken"] for t in session_data["time_per_question"].values()),
            "questions_attempted": total_questions,
            "questions_correct": correct_answers,
            "strengths": [],
            "improvement_areas": [],
            "percentile_rank": random.uniform(20, 95),
            "recommendations": [],
            "detailed_analysis": f"Comprehensive analysis for {candidate_name}",
            "created_at": session_data["created_at"],
            "theta_final": session_data["theta_estimates"],
            "se_final": session_data["se_estimates"]
        }
        
        # Calculate difficulty performance
        for difficulty in ["easy", "medium", "hard"]:
            diff_answers = [ans for ans in session_data["answers"].values() if ans["difficulty"] == difficulty]
            diff_correct = sum(1 for ans in diff_answers if ans["correct"])
            diff_total = len(diff_answers)
            
            result_data["difficulty_performance"][difficulty] = {
                "correct": diff_correct,
                "total": diff_total,
                "percentage": (diff_correct / diff_total) * 100 if diff_total > 0 else 0
            }
        
        # Insert result
        await db.aptitude_results.insert_one(result_data)
        results_created += 1
        
        if (i + 1) % 5 == 0:
            print(f"   Created {i + 1} sessions and results...")
    
    print(f"✅ Mock data creation completed!")
    print(f"   Sessions created: {sessions_created}")
    print(f"   Results created: {results_created}")
    print(f"   Ready for ML prediction testing")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_mock_data())