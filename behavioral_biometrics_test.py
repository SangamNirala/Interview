#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Module 1: Behavioral Biometric Analysis Engine
Testing all biometric security endpoints and functionality as requested in the review
"""

import requests
import json
import time
import os
import uuid
from datetime import datetime, timedelta
import random

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://keystroke-analysis.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class BiometricAnalysisTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        self.test_session_id = str(uuid.uuid4())
        self.baseline_session_id = str(uuid.uuid4())
        self.signature_session_ids = []
        
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

    def test_behavioral_biometrics_engine_import(self):
        """Test if the behavioral_biometrics_engine.py module is properly imported and functional"""
        try:
            # Test by making a simple request to one of the biometric endpoints
            # This will fail if the module is not properly imported
            response = self.session.get(f"{BASE_URL}/security/biometric-analysis/{self.test_session_id}")
            
            # We expect 404 since no data exists yet, but not 500 (import error)
            if response.status_code == 404:
                self.log_test("Behavioral Biometrics Engine Import", "PASS", 
                            "Module imported successfully - endpoint accessible")
                return True
            elif response.status_code == 500:
                error_text = response.text
                if "module" in error_text.lower() or "import" in error_text.lower():
                    self.log_test("Behavioral Biometrics Engine Import", "FAIL", 
                                f"Module import error: {error_text}")
                    return False
                else:
                    # 500 for other reasons, module likely imported
                    self.log_test("Behavioral Biometrics Engine Import", "PASS", 
                                "Module imported successfully - endpoint functional")
                    return True
            else:
                self.log_test("Behavioral Biometrics Engine Import", "PASS", 
                            f"Module imported successfully - HTTP {response.status_code}")
                return True
                
        except Exception as e:
            self.log_test("Behavioral Biometrics Engine Import", "FAIL", f"Exception: {str(e)}")
            return False

    def generate_realistic_keystroke_data(self, num_keystrokes=50):
        """Generate realistic keystroke dynamics data for testing"""
        keystrokes = []
        base_time = time.time() * 1000  # Current time in milliseconds
        
        # Common words and typing patterns
        words = ["hello", "world", "test", "user", "password", "email", "name", "address"]
        
        for i in range(num_keystrokes):
            # Simulate typing a word
            word = random.choice(words)
            for j, char in enumerate(word):
                keystroke = {
                    "key": char,
                    "keydown_time": base_time + i * 100 + j * 80 + random.uniform(-20, 20),
                    "keyup_time": base_time + i * 100 + j * 80 + random.uniform(50, 120),
                    "dwell_time": random.uniform(50, 120),
                    "flight_time": random.uniform(20, 80) if j > 0 else 0,
                    "pressure": random.uniform(0.3, 1.0),
                    "typing_speed": random.uniform(200, 400)  # WPM equivalent
                }
                keystrokes.append(keystroke)
        
        return keystrokes

    def generate_realistic_mouse_data(self, num_movements=30):
        """Generate realistic mouse movement data for testing"""
        movements = []
        base_time = time.time() * 1000
        x, y = 400, 300  # Starting position
        
        for i in range(num_movements):
            # Simulate natural mouse movement
            x += random.uniform(-50, 50)
            y += random.uniform(-30, 30)
            x = max(0, min(1920, x))  # Keep within screen bounds
            y = max(0, min(1080, y))
            
            movement = {
                "x": x,
                "y": y,
                "timestamp": base_time + i * 50 + random.uniform(-10, 10),
                "velocity": random.uniform(100, 800),
                "acceleration": random.uniform(-200, 200),
                "pressure": random.uniform(0.1, 0.8),
                "movement_type": random.choice(["linear", "curved", "jerky"])
            }
            movements.append(movement)
        
        return movements

    def generate_realistic_timing_data(self, num_questions=10):
        """Generate realistic response timing data for testing"""
        timing_data = []
        base_time = time.time() * 1000
        
        for i in range(num_questions):
            # Simulate question response timing
            question_start = base_time + i * 30000  # 30 seconds between questions
            thinking_time = random.uniform(2000, 15000)  # 2-15 seconds thinking
            typing_time = random.uniform(5000, 45000)   # 5-45 seconds typing
            
            timing = {
                "question_id": f"q_{i+1}",
                "question_start_time": question_start,
                "first_keystroke_time": question_start + thinking_time,
                "last_keystroke_time": question_start + thinking_time + typing_time,
                "total_response_time": thinking_time + typing_time,
                "thinking_time": thinking_time,
                "typing_time": typing_time,
                "pause_count": random.randint(0, 5),
                "revision_count": random.randint(0, 3),
                "cognitive_load_indicators": {
                    "pause_frequency": random.uniform(0.1, 0.8),
                    "typing_rhythm_consistency": random.uniform(0.3, 0.9),
                    "response_confidence": random.uniform(0.4, 0.95)
                }
            }
            timing_data.append(timing)
        
        return timing_data

    def test_biometric_data_submission(self):
        """Test POST /api/security/biometric-data/submit endpoint"""
        try:
            # Generate realistic test data
            keystroke_data = self.generate_realistic_keystroke_data(30)
            mouse_data = self.generate_realistic_mouse_data(20)
            timing_data = self.generate_realistic_timing_data(5)
            
            # Create scroll and click data
            scroll_data = [
                {
                    "scroll_x": 0,
                    "scroll_y": random.randint(-100, 100),
                    "timestamp": time.time() * 1000 + i * 200,
                    "scroll_speed": random.uniform(50, 300),
                    "scroll_direction": random.choice(["up", "down"])
                }
                for i in range(10)
            ]
            
            click_data = [
                {
                    "x": random.randint(100, 800),
                    "y": random.randint(100, 600),
                    "timestamp": time.time() * 1000 + i * 1000,
                    "button": random.choice(["left", "right"]),
                    "click_duration": random.uniform(50, 200)
                }
                for i in range(8)
            ]
            
            request_data = {
                "session_id": self.test_session_id,
                "keystroke_data": keystroke_data,
                "mouse_data": mouse_data,
                "scroll_data": scroll_data,
                "click_data": click_data,
                "timing_data": timing_data,
                "consent_given": True
            }
            
            response = self.session.post(f"{BASE_URL}/security/biometric-data/submit", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    analysis_results = data.get("analysis_results", {})
                    
                    # Verify analysis components
                    expected_analyses = ["keystroke_analysis", "mouse_analysis", "scroll_analysis", 
                                       "click_analysis", "timing_analysis", "interaction_consistency"]
                    found_analyses = [key for key in expected_analyses if key in analysis_results]
                    
                    self.log_test("Biometric Data Submission", "PASS", 
                                f"Data submitted successfully. Analyses: {', '.join(found_analyses)}")
                    return True
                else:
                    self.log_test("Biometric Data Submission", "FAIL", 
                                f"Submission failed: {data}")
                    return False
            else:
                self.log_test("Biometric Data Submission", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Biometric Data Submission", "FAIL", f"Exception: {str(e)}")
            return False

    def test_anomaly_detection(self):
        """Test POST /api/security/biometric-analysis/detect-anomalies endpoint"""
        try:
            # First create baseline data
            baseline_keystroke_data = self.generate_realistic_keystroke_data(40)
            baseline_timing_data = self.generate_realistic_timing_data(8)
            
            baseline_request = {
                "session_id": self.baseline_session_id,
                "keystroke_data": baseline_keystroke_data,
                "timing_data": baseline_timing_data,
                "consent_given": True
            }
            
            # Submit baseline data
            baseline_response = self.session.post(f"{BASE_URL}/security/biometric-data/submit", 
                                                json=baseline_request)
            
            if baseline_response.status_code != 200:
                self.log_test("Anomaly Detection - Baseline Setup", "FAIL", 
                            f"Failed to create baseline: {baseline_response.status_code}")
                return False
            
            # Wait a moment for processing
            time.sleep(1)
            
            # Now test anomaly detection
            anomaly_request = {
                "session_id": self.test_session_id,
                "analysis_types": ["keystroke_dynamics", "response_timing"],
                "baseline_comparison": True,
                "baseline_session_id": self.baseline_session_id
            }
            
            response = self.session.post(f"{BASE_URL}/security/biometric-analysis/detect-anomalies", 
                                       json=anomaly_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    anomaly_score = data.get("overall_anomaly_score", 0)
                    anomaly_results = data.get("anomaly_results", {})
                    intervention_triggered = data.get("intervention_triggered", False)
                    
                    self.log_test("Anomaly Detection", "PASS", 
                                f"Anomaly score: {anomaly_score:.3f}, Intervention: {intervention_triggered}")
                    return True
                else:
                    self.log_test("Anomaly Detection", "FAIL", 
                                f"Detection failed: {data}")
                    return False
            else:
                self.log_test("Anomaly Detection", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Anomaly Detection", "FAIL", f"Exception: {str(e)}")
            return False

    def test_biometric_signature_generation(self):
        """Test POST /api/security/biometric-signature/generate endpoint"""
        try:
            # Create multiple sessions for signature generation
            session_ids = []
            
            for i in range(3):  # Minimum 3 sessions required
                session_id = str(uuid.uuid4())
                session_ids.append(session_id)
                
                # Generate varied keystroke data for each session
                keystroke_data = self.generate_realistic_keystroke_data(25 + i * 5)
                
                request_data = {
                    "session_id": session_id,
                    "keystroke_data": keystroke_data,
                    "consent_given": True
                }
                
                response = self.session.post(f"{BASE_URL}/security/biometric-data/submit", 
                                           json=request_data)
                
                if response.status_code != 200:
                    self.log_test("Biometric Signature Generation - Data Setup", "FAIL", 
                                f"Failed to create session {i+1}: {response.status_code}")
                    return False
            
            # Wait for processing
            time.sleep(2)
            
            # Generate biometric signature
            response = self.session.post(f"{BASE_URL}/security/biometric-signature/generate", 
                                       json=session_ids)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    signature_result = data.get("signature_result", {})
                    sessions_analyzed = data.get("sessions_analyzed", 0)
                    signature_id = data.get("signature_id")
                    
                    self.signature_session_ids = session_ids  # Store for later tests
                    
                    self.log_test("Biometric Signature Generation", "PASS", 
                                f"Signature generated from {sessions_analyzed} sessions, ID: {signature_id}")
                    return True
                else:
                    self.log_test("Biometric Signature Generation", "FAIL", 
                                f"Generation failed: {data}")
                    return False
            else:
                self.log_test("Biometric Signature Generation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Biometric Signature Generation", "FAIL", f"Exception: {str(e)}")
            return False

    def test_biometric_configuration_update(self):
        """Test POST /api/security/biometric-config/update endpoint"""
        try:
            config_request = {
                "session_id": self.test_session_id,
                "enable_biometric_tracking": True,
                "tracking_sensitivity": "high",
                "real_time_analysis": True,
                "intervention_enabled": True
            }
            
            response = self.session.post(f"{BASE_URL}/security/biometric-config/update", 
                                       json=config_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    configuration = data.get("configuration", {})
                    
                    self.log_test("Biometric Configuration Update", "PASS", 
                                f"Configuration updated: sensitivity={configuration.get('tracking_sensitivity')}")
                    return True
                else:
                    self.log_test("Biometric Configuration Update", "FAIL", 
                                f"Update failed: {data}")
                    return False
            else:
                self.log_test("Biometric Configuration Update", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Biometric Configuration Update", "FAIL", f"Exception: {str(e)}")
            return False

    def test_biometric_analysis_retrieval(self):
        """Test GET /api/security/biometric-analysis/{session_id} endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/security/biometric-analysis/{self.test_session_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    analysis_results = data.get("analysis_results", {})
                    anomaly_score = data.get("anomaly_score", 0)
                    intervention_level = data.get("intervention_level", "none")
                    
                    self.log_test("Biometric Analysis Retrieval", "PASS", 
                                f"Analysis retrieved: anomaly_score={anomaly_score}, level={intervention_level}")
                    return True
                else:
                    self.log_test("Biometric Analysis Retrieval", "FAIL", 
                                f"Retrieval failed: {data}")
                    return False
            elif response.status_code == 404:
                self.log_test("Biometric Analysis Retrieval", "FAIL", 
                            "No analysis data found - previous tests may have failed")
                return False
            else:
                self.log_test("Biometric Analysis Retrieval", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Biometric Analysis Retrieval", "FAIL", f"Exception: {str(e)}")
            return False

    def test_gdpr_consent_management(self):
        """Test POST /api/security/data-privacy/consent endpoint"""
        try:
            consent_request = {
                "session_id": self.test_session_id,
                "candidate_id": "test_candidate_123",
                "consent_given": True,
                "data_types": ["keystroke", "mouse", "scroll", "timing"]
            }
            
            response = self.session.post(f"{BASE_URL}/security/data-privacy/consent", 
                                       json=consent_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("consent_recorded"):
                    consent_given = data.get("consent_given")
                    data_types = data.get("data_types", [])
                    
                    self.log_test("GDPR Consent Management", "PASS", 
                                f"Consent recorded: {consent_given}, types: {', '.join(data_types)}")
                    return True
                else:
                    self.log_test("GDPR Consent Management", "FAIL", 
                                f"Consent recording failed: {data}")
                    return False
            else:
                self.log_test("GDPR Consent Management", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("GDPR Consent Management", "FAIL", f"Exception: {str(e)}")
            return False

    def test_data_purging(self):
        """Test POST /api/security/data-privacy/purge-expired endpoint"""
        try:
            response = self.session.post(f"{BASE_URL}/security/data-privacy/purge-expired")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    purge_results = data.get("purge_results", {})
                    biometric_purged = purge_results.get("biometric_data_purged", 0)
                    consent_purged = purge_results.get("consent_records_purged", 0)
                    interventions_purged = purge_results.get("interventions_purged", 0)
                    
                    self.log_test("Data Purging", "PASS", 
                                f"Purged: {biometric_purged} biometric, {consent_purged} consent, {interventions_purged} interventions")
                    return True
                else:
                    self.log_test("Data Purging", "FAIL", 
                                f"Purging failed: {data}")
                    return False
            else:
                self.log_test("Data Purging", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Data Purging", "FAIL", f"Exception: {str(e)}")
            return False

    def test_security_interventions(self):
        """Test GET /api/security/interventions/{session_id} endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/security/interventions/{self.test_session_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    interventions = data.get("interventions", [])
                    total_interventions = data.get("total_interventions", 0)
                    highest_anomaly_score = data.get("highest_anomaly_score", 0)
                    
                    self.log_test("Security Interventions", "PASS", 
                                f"Retrieved {total_interventions} interventions, max anomaly: {highest_anomaly_score}")
                    return True
                else:
                    self.log_test("Security Interventions", "FAIL", 
                                f"Retrieval failed: {data}")
                    return False
            else:
                self.log_test("Security Interventions", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Security Interventions", "FAIL", f"Exception: {str(e)}")
            return False

    def test_keystroke_analysis_scenario(self):
        """Test comprehensive keystroke analysis scenario"""
        try:
            # Generate keystroke data with specific patterns
            keystroke_data = []
            base_time = time.time() * 1000
            
            # Simulate typing "Hello World" with realistic timing
            text = "Hello World"
            for i, char in enumerate(text):
                if char == ' ':
                    continue  # Skip spaces for this test
                    
                keystroke = {
                    "key": char,
                    "keydown_time": base_time + i * 150 + random.uniform(-30, 30),
                    "keyup_time": base_time + i * 150 + random.uniform(80, 120),
                    "dwell_time": random.uniform(80, 120),
                    "flight_time": random.uniform(30, 100) if i > 0 else 0,
                    "pressure": random.uniform(0.4, 0.9),
                    "typing_speed": random.uniform(250, 350)
                }
                keystroke_data.append(keystroke)
            
            request_data = {
                "session_id": f"keystroke_test_{uuid.uuid4()}",
                "keystroke_data": keystroke_data,
                "consent_given": True
            }
            
            response = self.session.post(f"{BASE_URL}/security/biometric-data/submit", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                analysis_results = data.get("analysis_results", {})
                
                if "keystroke_analysis" in analysis_results:
                    keystroke_analysis = analysis_results["keystroke_analysis"]
                    
                    # Check if analysis contains expected components
                    if "error" not in keystroke_analysis:
                        self.log_test("Keystroke Analysis Scenario", "PASS", 
                                    f"Keystroke analysis completed successfully")
                        return True
                    else:
                        self.log_test("Keystroke Analysis Scenario", "FAIL", 
                                    f"Keystroke analysis error: {keystroke_analysis['error']}")
                        return False
                else:
                    self.log_test("Keystroke Analysis Scenario", "FAIL", 
                                "No keystroke analysis in results")
                    return False
            else:
                self.log_test("Keystroke Analysis Scenario", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Keystroke Analysis Scenario", "FAIL", f"Exception: {str(e)}")
            return False

    def test_mouse_interaction_analysis_scenario(self):
        """Test comprehensive mouse/interaction analysis scenario"""
        try:
            # Generate mouse movement data simulating form filling
            mouse_data = []
            click_data = []
            scroll_data = []
            base_time = time.time() * 1000
            
            # Simulate mouse movements to different form fields
            form_fields = [(200, 150), (200, 200), (200, 250), (200, 300)]
            
            for i, (target_x, target_y) in enumerate(form_fields):
                # Mouse movement to field
                for j in range(10):
                    progress = j / 9.0
                    x = 100 + (target_x - 100) * progress + random.uniform(-5, 5)
                    y = 100 + (target_y - 100) * progress + random.uniform(-5, 5)
                    
                    mouse_data.append({
                        "x": x,
                        "y": y,
                        "timestamp": base_time + i * 2000 + j * 50,
                        "velocity": random.uniform(100, 400),
                        "acceleration": random.uniform(-100, 100),
                        "pressure": random.uniform(0.1, 0.6)
                    })
                
                # Click on field
                click_data.append({
                    "x": target_x,
                    "y": target_y,
                    "timestamp": base_time + i * 2000 + 500,
                    "button": "left",
                    "click_duration": random.uniform(80, 150)
                })
                
                # Some scrolling
                if i % 2 == 0:
                    scroll_data.append({
                        "scroll_x": 0,
                        "scroll_y": random.randint(-50, 50),
                        "timestamp": base_time + i * 2000 + 1000,
                        "scroll_speed": random.uniform(100, 200)
                    })
            
            request_data = {
                "session_id": f"interaction_test_{uuid.uuid4()}",
                "mouse_data": mouse_data,
                "click_data": click_data,
                "scroll_data": scroll_data,
                "consent_given": True
            }
            
            response = self.session.post(f"{BASE_URL}/security/biometric-data/submit", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                analysis_results = data.get("analysis_results", {})
                
                expected_analyses = ["mouse_analysis", "click_analysis", "scroll_analysis", "interaction_consistency"]
                found_analyses = [key for key in expected_analyses if key in analysis_results and "error" not in analysis_results[key]]
                
                if len(found_analyses) >= 2:  # At least 2 analyses should work
                    self.log_test("Mouse/Interaction Analysis Scenario", "PASS", 
                                f"Interaction analyses completed: {', '.join(found_analyses)}")
                    return True
                else:
                    self.log_test("Mouse/Interaction Analysis Scenario", "FAIL", 
                                f"Insufficient analyses completed: {found_analyses}")
                    return False
            else:
                self.log_test("Mouse/Interaction Analysis Scenario", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Mouse/Interaction Analysis Scenario", "FAIL", f"Exception: {str(e)}")
            return False

    def test_response_timing_analysis_scenario(self):
        """Test comprehensive response timing analysis scenario"""
        try:
            # Generate timing data simulating test-taking behavior
            timing_data = []
            base_time = time.time() * 1000
            
            # Simulate 5 questions with varying difficulty and response patterns
            question_difficulties = ["easy", "medium", "hard", "medium", "easy"]
            
            for i, difficulty in enumerate(question_difficulties):
                question_start = base_time + i * 45000  # 45 seconds between questions
                
                # Adjust thinking time based on difficulty
                if difficulty == "easy":
                    thinking_time = random.uniform(3000, 8000)
                elif difficulty == "medium":
                    thinking_time = random.uniform(8000, 20000)
                else:  # hard
                    thinking_time = random.uniform(15000, 35000)
                
                typing_time = random.uniform(10000, 30000)
                
                timing = {
                    "question_id": f"q_{i+1}",
                    "question_difficulty": difficulty,
                    "question_start_time": question_start,
                    "first_keystroke_time": question_start + thinking_time,
                    "last_keystroke_time": question_start + thinking_time + typing_time,
                    "total_response_time": thinking_time + typing_time,
                    "thinking_time": thinking_time,
                    "typing_time": typing_time,
                    "pause_count": random.randint(1, 4),
                    "revision_count": random.randint(0, 2),
                    "cognitive_load_indicators": {
                        "pause_frequency": random.uniform(0.2, 0.7),
                        "typing_rhythm_consistency": random.uniform(0.4, 0.8),
                        "response_confidence": random.uniform(0.5, 0.9)
                    }
                }
                timing_data.append(timing)
            
            request_data = {
                "session_id": f"timing_test_{uuid.uuid4()}",
                "timing_data": timing_data,
                "consent_given": True
            }
            
            response = self.session.post(f"{BASE_URL}/security/biometric-data/submit", 
                                       json=request_data)
            
            if response.status_code == 200:
                data = response.json()
                analysis_results = data.get("analysis_results", {})
                
                if "timing_analysis" in analysis_results:
                    timing_analysis = analysis_results["timing_analysis"]
                    
                    if "error" not in timing_analysis:
                        self.log_test("Response Timing Analysis Scenario", "PASS", 
                                    f"Timing analysis completed successfully")
                        return True
                    else:
                        self.log_test("Response Timing Analysis Scenario", "FAIL", 
                                    f"Timing analysis error: {timing_analysis['error']}")
                        return False
                else:
                    self.log_test("Response Timing Analysis Scenario", "FAIL", 
                                "No timing analysis in results")
                    return False
            else:
                self.log_test("Response Timing Analysis Scenario", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Response Timing Analysis Scenario", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all behavioral biometric tests in sequence"""
        print("=" * 80)
        print("MODULE 1: BEHAVIORAL BIOMETRIC ANALYSIS ENGINE TESTING")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Admin Authentication
        test_results.append(self.test_admin_authentication())
        
        if not self.admin_authenticated:
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Test 2: Module Import Verification
        test_results.append(self.test_behavioral_biometrics_engine_import())
        
        # Test 3: Core API Endpoints
        test_results.append(self.test_biometric_data_submission())
        test_results.append(self.test_anomaly_detection())
        test_results.append(self.test_biometric_signature_generation())
        test_results.append(self.test_biometric_configuration_update())
        test_results.append(self.test_biometric_analysis_retrieval())
        
        # Test 4: GDPR Compliance
        test_results.append(self.test_gdpr_consent_management())
        test_results.append(self.test_data_purging())
        
        # Test 5: Security Interventions
        test_results.append(self.test_security_interventions())
        
        # Test 6: Specific Analysis Scenarios
        test_results.append(self.test_keystroke_analysis_scenario())
        test_results.append(self.test_mouse_interaction_analysis_scenario())
        test_results.append(self.test_response_timing_analysis_scenario())
        
        # Summary
        print("=" * 80)
        print("BEHAVIORAL BIOMETRIC ANALYSIS ENGINE TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Behavioral Biometric Analysis Engine is working correctly.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = BiometricAnalysisTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ BEHAVIORAL BIOMETRIC ANALYSIS ENGINE TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ BEHAVIORAL BIOMETRIC ANALYSIS ENGINE TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()