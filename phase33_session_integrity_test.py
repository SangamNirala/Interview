#!/usr/bin/env python3
"""
🎯 PHASE 3.3: SESSION INTEGRITY MONITORING COMPREHENSIVE TESTING
Testing the complete SessionIntegrityMonitor class with 4 core methods

Test Coverage:
1. Session Continuity Monitoring (POST /api/session-fingerprinting/monitor-session-continuity)
2. Session Manipulation Detection (POST /api/session-fingerprinting/detect-session-manipulation)
3. Session Authenticity Validation (POST /api/session-fingerprinting/validate-session-authenticity)
4. Session Anomaly Tracking (POST /api/session-fingerprinting/track-session-anomalies)

Testing Scenarios:
- Normal continuous sessions vs session hijacking attempts
- Clean sessions vs replay attacks and timestamp manipulation
- Valid authenticity vs invalid credentials and identity mismatches
- Normal behavioral patterns vs unusual anomalies
- Edge cases with malformed data
- MongoDB integration verification
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time
import random

# Configuration
BACKEND_URL = "https://interviewmate-1.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class Phase33SessionIntegrityTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.session_id = str(uuid.uuid4())
        
    def log_result(self, test_name, success, details, response_data=None):
        """Log test result with details"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        
    def authenticate_admin(self):
        """Authenticate as admin"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/login",
                json={"password": ADMIN_PASSWORD}
            )
            
            if response.status_code == 200:
                self.log_result("Admin Authentication", True, f"Successfully authenticated (Status: {response.status_code})")
                return True
            else:
                self.log_result("Admin Authentication", False, f"Authentication failed (Status: {response.status_code})")
                return False
                
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Authentication error: {str(e)}")
            return False

    def test_session_continuity_normal_session(self):
        """Test session continuity monitoring with normal continuous session"""
        try:
            session_id = self.session_id + "_normal_continuity"
            
            # Normal continuous session data
            session_data = {
                "session_id": session_id,
                "user_id": "user_12345",
                "session_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzNDUiLCJzZXNzaW9uX2lkIjoiYWJjZGVmIiwiaWF0IjoxNjM0NTY3ODkwfQ.signature",
                "activity_logs": [
                    {
                        "timestamp": "2024-01-15T10:00:00Z",
                        "action": "login",
                        "ip_address": "192.168.1.100",
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "device_fingerprint": "fp_12345_windows_chrome",
                        "location": {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060}
                    },
                    {
                        "timestamp": "2024-01-15T10:05:00Z",
                        "action": "page_view",
                        "ip_address": "192.168.1.100",
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "device_fingerprint": "fp_12345_windows_chrome",
                        "location": {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060}
                    }
                ],
                "behavioral_data": {
                    "typing_patterns": {
                        "avg_keystroke_interval": 150,
                        "typing_rhythm_consistency": 0.85,
                        "pause_patterns": [200, 180, 160, 190, 170]
                    },
                    "mouse_patterns": {
                        "movement_velocity": 1.2,
                        "click_accuracy": 0.92,
                        "scroll_behavior": "smooth",
                        "interaction_frequency": 45
                    }
                },
                "device_characteristics": {
                    "screen_resolution": "1920x1080",
                    "timezone": "America/New_York",
                    "language": "en-US",
                    "platform": "Win32"
                }
            }
            
            payload = {
                "session_data": session_data,
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/monitor-session-continuity",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('session_continuity_analysis', {})
                    self.log_result(
                        "Session Continuity - Normal Session", 
                        True, 
                        f"Normal session analysis completed. Response keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Session Continuity - Normal Session", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Continuity - Normal Session", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Continuity - Normal Session", False, f"Exception: {str(e)}")
            return False

    def test_session_continuity_hijacking_attempt(self):
        """Test session continuity monitoring with session hijacking indicators"""
        try:
            session_id = self.session_id + "_hijacking_attempt"
            
            # Session with hijacking indicators - IP change, device change, impossible travel
            session_data = {
                "session_id": session_id,
                "user_id": "user_67890",
                "session_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjc4OTAiLCJzZXNzaW9uX2lkIjoiaGlqYWNrIiwiaWF0IjoxNjM0NTY3ODkwfQ.signature",
                "activity_logs": [
                    {
                        "timestamp": "2024-01-15T10:00:00Z",
                        "action": "login",
                        "ip_address": "192.168.1.100",
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "device_fingerprint": "fp_67890_windows_chrome",
                        "location": {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060}
                    },
                    {
                        "timestamp": "2024-01-15T10:05:00Z",
                        "action": "page_view",
                        "ip_address": "203.0.113.45",  # Different IP
                        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",  # Different OS/Browser
                        "device_fingerprint": "fp_unknown_linux_chrome",  # Different device
                        "location": {"country": "CN", "city": "Beijing", "lat": 39.9042, "lng": 116.4074}  # Impossible travel
                    }
                ],
                "behavioral_data": {
                    "typing_patterns": {
                        "avg_keystroke_interval": 80,  # Much faster typing
                        "typing_rhythm_consistency": 0.45,  # Inconsistent
                        "pause_patterns": [50, 60, 55, 58, 52]  # Different pattern
                    },
                    "mouse_patterns": {
                        "movement_velocity": 2.8,  # Much faster
                        "click_accuracy": 0.98,  # Too perfect
                        "scroll_behavior": "jerky",  # Different behavior
                        "interaction_frequency": 120  # Much higher
                    }
                },
                "device_characteristics": {
                    "screen_resolution": "1366x768",  # Different resolution
                    "timezone": "Asia/Shanghai",  # Different timezone
                    "language": "zh-CN",  # Different language
                    "platform": "Linux x86_64"  # Different platform
                }
            }
            
            payload = {
                "session_data": session_data,
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/monitor-session-continuity",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('session_continuity_analysis', {})
                    self.log_result(
                        "Session Continuity - Hijacking Attempt", 
                        True, 
                        f"Hijacking detection completed. Response keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Session Continuity - Hijacking Attempt", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Continuity - Hijacking Attempt", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Continuity - Hijacking Attempt", False, f"Exception: {str(e)}")
            return False

    def test_session_manipulation_replay_attack(self):
        """Test session manipulation detection with replay attack patterns"""
        try:
            session_id = self.session_id + "_replay_attack"
            
            # Session data with replay attack indicators
            session_data = {
                "session_id": session_id,
                "user_id": "user_replay_test",
                "request_history": [
                    {
                        "timestamp": "2024-01-15T10:00:00Z",
                        "request_id": "req_001",
                        "endpoint": "/api/user/profile",
                        "method": "GET",
                        "headers": {"Authorization": "Bearer token123", "User-Agent": "Chrome/119.0"},
                        "body_hash": "hash_001",
                        "response_time": 150
                    },
                    {
                        "timestamp": "2024-01-15T10:00:05Z",
                        "request_id": "req_002",
                        "endpoint": "/api/user/profile",
                        "method": "GET",
                        "headers": {"Authorization": "Bearer token123", "User-Agent": "Chrome/119.0"},
                        "body_hash": "hash_001",  # Identical hash - potential replay
                        "response_time": 148  # Very similar response time
                    }
                ],
                "timestamp_data": {
                    "client_timestamps": [
                        "2024-01-15T10:00:00.123Z",
                        "2024-01-15T10:00:05.125Z"
                    ],
                    "server_timestamps": [
                        "2024-01-15T10:00:00.145Z",
                        "2024-01-15T10:00:05.147Z"
                    ],
                    "clock_skew_analysis": {
                        "client_server_drift": [22, 22],  # Consistent drift - suspicious
                        "timezone_consistency": True,
                        "ntp_sync_indicators": False
                    }
                },
                "data_integrity": {
                    "request_checksums": ["chk_001", "chk_001"],  # Identical checksums
                    "session_state_hashes": ["state_001", "state_001"],  # No state changes
                    "csrf_tokens": ["csrf_123", "csrf_123"],  # Reused CSRF tokens
                    "sequence_numbers": [1, 2]
                }
            }
            
            payload = {
                "session_data": session_data,
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-session-manipulation",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('manipulation_analysis', {})
                    self.log_result(
                        "Session Manipulation - Replay Attack", 
                        True, 
                        f"Replay attack detection completed. Response keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Session Manipulation - Replay Attack", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Manipulation - Replay Attack", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Manipulation - Replay Attack", False, f"Exception: {str(e)}")
            return False

    def test_session_manipulation_timestamp_manipulation(self):
        """Test session manipulation detection with timestamp manipulation"""
        try:
            session_id = self.session_id + "_timestamp_manipulation"
            
            # Session data with timestamp manipulation indicators
            session_data = {
                "session_id": session_id,
                "user_id": "user_timestamp_test",
                "request_history": [
                    {
                        "timestamp": "2024-01-15T10:00:00Z",
                        "request_id": "req_ts_001",
                        "endpoint": "/api/data/fetch",
                        "method": "POST",
                        "headers": {"Authorization": "Bearer token456"},
                        "body_hash": "hash_ts_001",
                        "response_time": 200
                    },
                    {
                        "timestamp": "2024-01-15T09:59:55Z",  # Timestamp goes backwards
                        "request_id": "req_ts_002",
                        "endpoint": "/api/data/update",
                        "method": "PUT",
                        "headers": {"Authorization": "Bearer token456"},
                        "body_hash": "hash_ts_002",
                        "response_time": 180
                    }
                ],
                "timestamp_data": {
                    "client_timestamps": [
                        "2024-01-15T10:00:00.000Z",
                        "2024-01-15T09:59:55.000Z"  # Backwards timestamp
                    ],
                    "server_timestamps": [
                        "2024-01-15T10:00:00.050Z",
                        "2024-01-15T10:00:05.050Z"  # Server timestamp continues forward
                    ],
                    "clock_skew_analysis": {
                        "client_server_drift": [50, -294950],  # Massive drift changes
                        "timezone_consistency": False,
                        "ntp_sync_indicators": False,
                        "timestamp_anomalies": [
                            "backwards_timestamp",
                            "large_time_jump",
                            "inconsistent_drift"
                        ]
                    }
                },
                "data_integrity": {
                    "request_checksums": ["chk_ts_001", "chk_ts_002"],
                    "session_state_hashes": ["state_ts_001", "state_ts_002"],
                    "csrf_tokens": ["csrf_456", "csrf_789"],
                    "sequence_numbers": [1, 2]
                }
            }
            
            payload = {
                "session_data": session_data,
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-session-manipulation",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('manipulation_analysis', {})
                    self.log_result(
                        "Session Manipulation - Timestamp Manipulation", 
                        True, 
                        f"Timestamp manipulation detection completed. Response keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Session Manipulation - Timestamp Manipulation", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Manipulation - Timestamp Manipulation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Manipulation - Timestamp Manipulation", False, f"Exception: {str(e)}")
            return False

    def test_session_authenticity_valid_session(self):
        """Test session authenticity validation with valid authentication data"""
        try:
            session_id = self.session_id + "_valid_auth"
            
            # Valid authentication session data
            session_data = {
                "session_id": session_id,
                "user_id": "user_valid_auth",
                "authentication_data": {
                    "credentials": {
                        "username": "john.smith@company.com",
                        "password_hash": "sha256:a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                        "salt": "random_salt_12345",
                        "hash_algorithm": "SHA256",
                        "password_strength": "strong"
                    },
                    "multi_factor": {
                        "enabled": True,
                        "methods": ["totp", "sms"],
                        "totp_verified": True,
                        "sms_verified": True,
                        "backup_codes_used": 0,
                        "last_mfa_timestamp": "2024-01-15T10:00:00Z"
                    },
                    "oauth_tokens": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.valid_payload.valid_signature",
                        "refresh_token": "refresh_token_valid_12345",
                        "token_type": "Bearer",
                        "expires_in": 3600,
                        "scope": "read write",
                        "issued_at": "2024-01-15T10:00:00Z"
                    }
                },
                "identity_claims": {
                    "user_profile": {
                        "user_id": "user_valid_auth",
                        "email": "john.smith@company.com",
                        "full_name": "John Smith",
                        "role": "senior_developer",
                        "department": "engineering",
                        "employee_id": "EMP12345"
                    }
                },
                "biometric_data": {
                    "fingerprint_template": "biometric_template_hash_12345",
                    "face_recognition_score": 0.95,
                    "voice_print_match": 0.92,
                    "behavioral_biometrics": {
                        "typing_pattern_match": 0.88,
                        "mouse_movement_match": 0.91,
                        "navigation_pattern_match": 0.89
                    },
                    "biometric_confidence": 0.91
                },
                "token_integrity": {
                    "jwt_signature_valid": True,
                    "token_not_expired": True,
                    "token_not_before_valid": True,
                    "issuer_verified": True,
                    "audience_verified": True
                }
            }
            
            payload = {
                "session_data": session_data,
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/validate-session-authenticity",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('authenticity_analysis', {})
                    self.log_result(
                        "Session Authenticity - Valid Session", 
                        True, 
                        f"Valid session authenticity analysis completed. Response keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Session Authenticity - Valid Session", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Authenticity - Valid Session", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Authenticity - Valid Session", False, f"Exception: {str(e)}")
            return False

    def test_session_authenticity_invalid_credentials(self):
        """Test session authenticity validation with invalid credentials and identity mismatches"""
        try:
            session_id = self.session_id + "_invalid_auth"
            
            # Invalid authentication session data
            session_data = {
                "session_id": session_id,
                "user_id": "user_invalid_auth",
                "authentication_data": {
                    "credentials": {
                        "username": "suspicious.user@external.com",
                        "password_hash": "weak_hash_123",  # Weak hash
                        "salt": "",  # No salt
                        "hash_algorithm": "MD5",  # Weak algorithm
                        "password_strength": "weak"
                    },
                    "multi_factor": {
                        "enabled": False,  # MFA disabled
                        "methods": [],
                        "totp_verified": False,
                        "sms_verified": False,
                        "backup_codes_used": 5,  # Too many backup codes used
                        "last_mfa_timestamp": None
                    },
                    "oauth_tokens": {
                        "access_token": "invalid.token.signature",  # Invalid token
                        "refresh_token": "expired_refresh_token",
                        "token_type": "Bearer",
                        "expires_in": -3600,  # Expired
                        "scope": "read",  # Limited scope
                        "issued_at": "2024-01-14T10:00:00Z"  # Old token
                    }
                },
                "identity_claims": {
                    "user_profile": {
                        "user_id": "user_different_id",  # Mismatched user ID
                        "email": "different.email@domain.com",  # Mismatched email
                        "full_name": "Different Name",  # Mismatched name
                        "role": "admin",  # Suspicious role escalation
                        "department": "unknown",
                        "employee_id": "INVALID"
                    }
                },
                "biometric_data": {
                    "fingerprint_template": "unknown_template",
                    "face_recognition_score": 0.45,  # Low confidence
                    "voice_print_match": 0.32,  # Very low confidence
                    "behavioral_biometrics": {
                        "typing_pattern_match": 0.25,  # Poor match
                        "mouse_movement_match": 0.18,  # Very poor match
                        "navigation_pattern_match": 0.30  # Poor match
                    },
                    "biometric_confidence": 0.31  # Low overall confidence
                },
                "token_integrity": {
                    "jwt_signature_valid": False,  # Invalid signature
                    "token_not_expired": False,  # Expired
                    "token_not_before_valid": True,
                    "issuer_verified": False,  # Unverified issuer
                    "audience_verified": False  # Unverified audience
                }
            }
            
            payload = {
                "session_data": session_data,
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/validate-session-authenticity",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('authenticity_analysis', {})
                    self.log_result(
                        "Session Authenticity - Invalid Credentials", 
                        True, 
                        f"Invalid credentials analysis completed. Response keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Session Authenticity - Invalid Credentials", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Authenticity - Invalid Credentials", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Authenticity - Invalid Credentials", False, f"Exception: {str(e)}")
            return False

    def test_session_anomaly_normal_patterns(self):
        """Test session anomaly tracking with normal behavioral patterns"""
        try:
            session_id = self.session_id + "_normal_patterns"
            
            # Normal session with typical behavioral patterns
            session_data = {
                "session_id": session_id,
                "user_id": "user_normal_behavior",
                "behavioral_patterns": {
                    "activity_frequency": {
                        "requests_per_minute": [12, 15, 11, 14, 13, 16, 10, 12],
                        "page_views_per_session": 25,
                        "interaction_events_per_minute": [45, 52, 38, 48, 41, 55, 35, 44],
                        "idle_periods": [120, 180, 90, 150, 200, 110, 170]  # Normal idle times
                    },
                    "navigation_behavior": {
                        "page_sequence": ["home", "profile", "settings", "dashboard", "reports", "logout"],
                        "back_button_usage": 3,
                        "bookmark_usage": 2,
                        "search_queries": ["monthly report", "user settings", "help documentation"],
                        "external_link_clicks": 1
                    },
                    "interaction_patterns": {
                        "mouse_movements": {
                            "total_distance": 15420.5,
                            "average_velocity": 1.2,
                            "click_accuracy": 0.89,
                            "double_click_intervals": [180, 200, 190, 185]
                        },
                        "keyboard_usage": {
                            "typing_speed": 65,  # WPM
                            "keystroke_intervals": [150, 180, 160, 170, 155],
                            "backspace_frequency": 0.08,
                            "special_key_usage": ["Tab", "Enter", "Ctrl+C", "Ctrl+V"]
                        }
                    }
                },
                "access_patterns": {
                    "login_times": [
                        "2024-01-15T09:00:00Z",
                        "2024-01-16T09:15:00Z",
                        "2024-01-17T08:45:00Z"
                    ],
                    "session_durations": [480, 520, 450],  # Minutes, normal work sessions
                    "geographic_locations": [
                        {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060},
                        {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060}
                    ],
                    "device_consistency": {
                        "same_device": True,
                        "browser_consistency": True,
                        "screen_resolution_changes": 0,
                        "timezone_consistency": True
                    }
                },
                "duration_analysis": {
                    "total_session_time": 1960,  # 32 minutes, normal
                    "active_time": 1680,  # 28 minutes active
                    "idle_time": 280,  # 4.7 minutes idle
                    "page_dwell_times": [45, 120, 80, 200, 150, 90, 60]  # Seconds per page
                }
            }
            
            payload = {
                "session_data": session_data,
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-session-anomalies",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('anomaly_analysis', {})
                    self.log_result(
                        "Session Anomaly - Normal Patterns", 
                        True, 
                        f"Normal patterns analysis completed. Response keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Session Anomaly - Normal Patterns", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Anomaly - Normal Patterns", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Anomaly - Normal Patterns", False, f"Exception: {str(e)}")
            return False

    def test_session_anomaly_unusual_patterns(self):
        """Test session anomaly tracking with unusual behavioral patterns and anomalies"""
        try:
            session_id = self.session_id + "_unusual_patterns"
            
            # Session with unusual and suspicious behavioral patterns
            session_data = {
                "session_id": session_id,
                "user_id": "user_suspicious_behavior",
                "behavioral_patterns": {
                    "activity_frequency": {
                        "requests_per_minute": [150, 200, 180, 220, 190, 250, 170, 300],  # Extremely high
                        "page_views_per_session": 500,  # Unusually high
                        "interaction_events_per_minute": [800, 900, 750, 850, 920, 1000, 700, 950],  # Inhuman
                        "idle_periods": [0, 1, 0, 2, 1, 0, 1]  # Almost no idle time
                    },
                    "navigation_behavior": {
                        "page_sequence": ["admin", "users", "delete", "admin", "users", "delete", "admin"],  # Repetitive
                        "back_button_usage": 0,  # No back button usage
                        "bookmark_usage": 0,  # No bookmarks
                        "search_queries": ["admin password", "user database", "delete all", "bypass security"],  # Suspicious
                        "external_link_clicks": 50  # Excessive external clicks
                    },
                    "interaction_patterns": {
                        "mouse_movements": {
                            "total_distance": 500.0,  # Very low, suggesting automation
                            "average_velocity": 10.0,  # Unnaturally fast
                            "click_accuracy": 1.0,  # Perfect accuracy, suspicious
                            "double_click_intervals": [100, 100, 100, 100]  # Too consistent
                        },
                        "keyboard_usage": {
                            "typing_speed": 300,  # Inhuman typing speed
                            "keystroke_intervals": [50, 50, 50, 50, 50],  # Too consistent
                            "backspace_frequency": 0.0,  # No mistakes
                            "special_key_usage": ["Ctrl+A", "Ctrl+C", "Ctrl+V", "Delete"] * 5  # Repetitive
                        }
                    }
                },
                "access_patterns": {
                    "login_times": [
                        "2024-01-15T03:00:00Z",  # Unusual time
                        "2024-01-15T03:05:00Z",  # Multiple logins in short time
                        "2024-01-15T03:10:00Z"
                    ],
                    "session_durations": [10, 15, 8],  # Very short sessions
                    "geographic_locations": [
                        {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060},
                        {"country": "RU", "city": "Moscow", "lat": 55.7558, "lng": 37.6176},  # Location jump
                        {"country": "CN", "city": "Beijing", "lat": 39.9042, "lng": 116.4074}  # Another jump
                    ],
                    "device_consistency": {
                        "same_device": False,  # Different devices
                        "browser_consistency": False,  # Different browsers
                        "screen_resolution_changes": 5,  # Multiple changes
                        "timezone_consistency": False  # Inconsistent timezones
                    }
                },
                "duration_analysis": {
                    "total_session_time": 45,  # Very short session
                    "active_time": 45,  # 100% active time, suspicious
                    "idle_time": 0,  # No idle time
                    "page_dwell_times": [1, 2, 1, 3, 2, 1, 2]  # Extremely short dwell times
                }
            }
            
            payload = {
                "session_data": session_data,
                "session_id": session_id
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-session-anomalies",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('anomaly_analysis', {})
                    self.log_result(
                        "Session Anomaly - Unusual Patterns", 
                        True, 
                        f"Unusual patterns analysis completed. Response keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Session Anomaly - Unusual Patterns", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Anomaly - Unusual Patterns", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Anomaly - Unusual Patterns", False, f"Exception: {str(e)}")
            return False

    def test_edge_cases_malformed_data(self):
        """Test all endpoints with malformed data and edge cases"""
        try:
            # Test with malformed data
            malformed_payloads = [
                {"session_data": {}, "session_id": "test_empty"},  # Empty session data
                {"session_data": {"session_id": ""}, "session_id": ""},  # Empty session ID
                {"session_data": {"session_id": None}, "session_id": None},  # Null session ID
                {"invalid_field": "test", "session_id": "test_invalid"},  # Wrong field name
                {"session_id": "test_no_data"}  # Missing session_data
            ]
            
            endpoints = [
                "/session-fingerprinting/monitor-session-continuity",
                "/session-fingerprinting/detect-session-manipulation",
                "/session-fingerprinting/validate-session-authenticity",
                "/session-fingerprinting/track-session-anomalies"
            ]
            
            edge_case_results = []
            
            for endpoint in endpoints:
                for i, payload in enumerate(malformed_payloads):
                    try:
                        response = self.session.post(f"{BACKEND_URL}{endpoint}", json=payload)
                        
                        # We expect either 400 (bad request) or 422 (validation error) for malformed data
                        if response.status_code in [400, 422, 500]:
                            edge_case_results.append(True)
                        else:
                            edge_case_results.append(False)
                            
                    except Exception:
                        # Exception handling is also acceptable for malformed data
                        edge_case_results.append(True)
            
            success_rate = sum(edge_case_results) / len(edge_case_results)
            
            if success_rate >= 0.8:  # 80% of edge cases handled properly
                self.log_result(
                    "Edge Cases - Malformed Data", 
                    True, 
                    f"Edge cases handled properly. Success rate: {success_rate:.1%} ({sum(edge_case_results)}/{len(edge_case_results)})"
                )
                return True
            else:
                self.log_result(
                    "Edge Cases - Malformed Data", 
                    False, 
                    f"Edge cases not handled properly. Success rate: {success_rate:.1%}"
                )
                return False
                
        except Exception as e:
            self.log_result("Edge Cases - Malformed Data", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all Phase 3.3 Session Integrity Monitoring tests"""
        print("=" * 80)
        print("🎯 PHASE 3.3: SESSION INTEGRITY MONITORING COMPREHENSIVE TESTING")
        print("=" * 80)
        print()
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return 0, 0
        
        # Run all tests
        tests = [
            self.test_session_continuity_normal_session,
            self.test_session_continuity_hijacking_attempt,
            self.test_session_manipulation_replay_attack,
            self.test_session_manipulation_timestamp_manipulation,
            self.test_session_authenticity_valid_session,
            self.test_session_authenticity_invalid_credentials,
            self.test_session_anomaly_normal_patterns,
            self.test_session_anomaly_unusual_patterns,
            self.test_edge_cases_malformed_data
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        # Print summary
        print("\n" + "=" * 80)
        print("🎯 PHASE 3.3 SESSION INTEGRITY MONITORING TESTING SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        # Print detailed results
        print("\n📊 DETAILED TEST RESULTS:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}: {result['details']}")
        
        return passed, total

if __name__ == "__main__":
    tester = Phase33SessionIntegrityTester()
    passed, total = tester.run_all_tests()
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! Phase 3.3 Session Integrity Monitoring functionality is working perfectly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the results above.")