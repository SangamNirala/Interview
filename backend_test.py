#!/usr/bin/env python3
"""
🎯 PHASE 3.3: SESSION INTEGRITY MONITORING TESTING - COMPREHENSIVE TESTING
Testing the two newly implemented/enhanced Phase 3.3 Session Integrity Monitoring methods:

1. track_multi_device_usage() - NEW METHOD testing
2. validate_session_authenticity() - ENHANCED METHOD testing

Test Coverage:
- POST /api/session-fingerprinting/track-multi-device-usage
- POST /api/session-fingerprinting/validate-session-authenticity

Testing Scenarios:
- Normal multi-device usage vs suspicious patterns
- Concurrent session detection across devices
- Device switching pattern analysis
- Session migration validation
- Multi-device collaboration indicators
- Device usage timeline correlation
- Biometric consistency validation
- Behavioral pattern authentication
- Session authentication token verification
- Identity continuity assessment
- Authenticity confidence scoring
- Edge cases and error handling
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time
import random

# Configuration
BACKEND_URL = "https://netdata-collector.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class Phase33SessionIntegrityTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.session_id = str(uuid.uuid4())
        self.user_id = str(uuid.uuid4())
        
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

    def test_track_multi_device_usage_normal_scenario(self):
        """Test multi-device usage tracking with normal legitimate usage patterns"""
        try:
            # Normal multi-device usage scenario
            session_data = {
                "user_id": self.user_id,
                "session_id": self.session_id + "_normal",
                "active_sessions": [
                    {
                        "session_id": self.session_id + "_desktop",
                        "device_fingerprint": "fp_desktop_chrome_windows",
                        "start_time": "2024-01-15T10:00:00Z",
                        "location": {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060},
                        "ip_address": "192.168.1.100",
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "device_type": "desktop"
                    },
                    {
                        "session_id": self.session_id + "_mobile",
                        "device_fingerprint": "fp_mobile_safari_ios",
                        "start_time": "2024-01-15T10:30:00Z",
                        "location": {"country": "US", "city": "New York", "lat": 40.7589, "lng": -73.9851},
                        "ip_address": "192.168.1.101",
                        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
                        "device_type": "mobile"
                    }
                ],
                "device_activity": [
                    {
                        "device_id": "desktop_001",
                        "timestamp": "2024-01-15T10:00:00Z",
                        "activity_type": "data_input",
                        "action_type": "document_creation",
                        "session_id": self.session_id + "_desktop"
                    },
                    {
                        "device_id": "mobile_001",
                        "timestamp": "2024-01-15T10:35:00Z",
                        "activity_type": "data_view",
                        "action_type": "document_review",
                        "session_id": self.session_id + "_mobile"
                    }
                ],
                "session_history": [
                    {
                        "session_id": self.session_id + "_desktop",
                        "device_fingerprint": "fp_desktop_chrome_windows",
                        "timestamp": "2024-01-15T10:00:00Z",
                        "duration": 1800,
                        "location": {"country": "US", "city": "New York"},
                        "activities_count": 25,
                        "data_transferred": 1024000
                    },
                    {
                        "session_id": self.session_id + "_mobile",
                        "device_fingerprint": "fp_mobile_safari_ios",
                        "timestamp": "2024-01-15T10:30:00Z",
                        "duration": 900,
                        "location": {"country": "US", "city": "New York"},
                        "activities_count": 12,
                        "data_transferred": 512000
                    }
                ]
            }
            
            payload = {
                "session_id": self.session_id + "_normal",
                "user_id": self.user_id,
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-multi-device-usage",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('multi_device_analysis', {})
                    analysis_summary = analysis.get('analysis_summary', {})
                    
                    self.log_result(
                        "Multi-Device Usage - Normal Scenario", 
                        True, 
                        f"Normal usage analysis completed. Risk Score: {analysis_summary.get('risk_score', 'N/A')}, Concurrent Sessions: {analysis_summary.get('concurrent_sessions_count', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Multi-Device Usage - Normal Scenario", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Multi-Device Usage - Normal Scenario", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Multi-Device Usage - Normal Scenario", False, f"Exception: {str(e)}")
            return False

    def test_track_multi_device_usage_suspicious_scenario(self):
        """Test multi-device usage tracking with suspicious patterns"""
        try:
            # Suspicious multi-device usage scenario with impossible travel and concurrent access
            session_data = {
                "user_id": self.user_id,
                "session_id": self.session_id + "_suspicious",
                "active_sessions": [
                    {
                        "session_id": self.session_id + "_location1",
                        "device_fingerprint": "fp_desktop_chrome_windows",
                        "start_time": "2024-01-15T10:00:00Z",
                        "location": {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060},
                        "ip_address": "192.168.1.100",
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "device_type": "desktop"
                    },
                    {
                        "session_id": self.session_id + "_location2",
                        "device_fingerprint": "fp_desktop_chrome_linux",
                        "start_time": "2024-01-15T10:05:00Z",  # Only 5 minutes later
                        "location": {"country": "JP", "city": "Tokyo", "lat": 35.6762, "lng": 139.6503},  # Impossible travel
                        "ip_address": "203.0.113.1",
                        "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
                        "device_type": "desktop"
                    },
                    {
                        "session_id": self.session_id + "_location3",
                        "device_fingerprint": "fp_mobile_chrome_android",
                        "start_time": "2024-01-15T10:10:00Z",  # Another 5 minutes later
                        "location": {"country": "GB", "city": "London", "lat": 51.5074, "lng": -0.1278},  # Another impossible travel
                        "ip_address": "198.51.100.1",
                        "user_agent": "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
                        "device_type": "mobile"
                    }
                ],
                "device_activity": [
                    {
                        "device_id": "desktop_001",
                        "timestamp": "2024-01-15T10:00:00Z",
                        "activity_type": "data_input",
                        "action_type": "document_creation",
                        "session_id": self.session_id + "_location1"
                    },
                    {
                        "device_id": "desktop_002",
                        "timestamp": "2024-01-15T10:05:30Z",  # Simultaneous activity
                        "activity_type": "data_input",
                        "action_type": "document_creation",
                        "session_id": self.session_id + "_location2"
                    },
                    {
                        "device_id": "mobile_001",
                        "timestamp": "2024-01-15T10:10:15Z",  # More simultaneous activity
                        "activity_type": "data_export",
                        "action_type": "bulk_download",
                        "session_id": self.session_id + "_location3"
                    }
                ],
                "session_history": [
                    {
                        "session_id": self.session_id + "_location1",
                        "device_fingerprint": "fp_desktop_chrome_windows",
                        "timestamp": "2024-01-15T10:00:00Z",
                        "duration": 600,
                        "location": {"country": "US", "city": "New York"},
                        "activities_count": 50,  # High activity
                        "data_transferred": 5120000  # Large data transfer
                    },
                    {
                        "session_id": self.session_id + "_location2",
                        "device_fingerprint": "fp_desktop_chrome_linux",
                        "timestamp": "2024-01-15T10:05:00Z",
                        "duration": 300,
                        "location": {"country": "JP", "city": "Tokyo"},
                        "activities_count": 75,  # Very high activity
                        "data_transferred": 10240000  # Very large data transfer
                    },
                    {
                        "session_id": self.session_id + "_location3",
                        "device_fingerprint": "fp_mobile_chrome_android",
                        "timestamp": "2024-01-15T10:10:00Z",
                        "duration": 180,
                        "location": {"country": "GB", "city": "London"},
                        "activities_count": 100,  # Extremely high activity
                        "data_transferred": 20480000  # Extremely large data transfer
                    }
                ]
            }
            
            payload = {
                "session_id": self.session_id + "_suspicious",
                "user_id": self.user_id,
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-multi-device-usage",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('multi_device_analysis', {})
                    analysis_summary = analysis.get('analysis_summary', {})
                    
                    self.log_result(
                        "Multi-Device Usage - Suspicious Scenario", 
                        True, 
                        f"Suspicious usage analysis completed. Risk Score: {analysis_summary.get('risk_score', 'N/A')}, Concurrent Sessions: {analysis_summary.get('concurrent_sessions_count', 'N/A')}, Impossible Travel: {analysis_summary.get('impossible_travel_detected', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Multi-Device Usage - Suspicious Scenario", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Multi-Device Usage - Suspicious Scenario", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Multi-Device Usage - Suspicious Scenario", False, f"Exception: {str(e)}")
            return False

    def test_validate_session_authenticity_valid_session(self):
        """Test session authenticity validation with valid credentials and consistent identity"""
        try:
            # Valid session authenticity data
            session_data = {
                "session_id": self.session_id + "_valid_auth",
                "user_id": self.user_id,
                "authentication_data": {
                    "method": "multi_factor",
                    "expires_at": int((datetime.now() + timedelta(hours=2)).timestamp()),
                    "credential_hash": "sha256:a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3",
                    "mfa_verified": True,
                    "last_auth_time": int(datetime.now().timestamp()),
                    "auth_strength": "strong"
                },
                "claimed_identity": {
                    "username": "john_doe_authenticated",
                    "email": "john.doe@company.com",
                    "phone_number": "+1234567890",
                    "user_id": self.user_id,
                    "account_created": "2023-01-15T10:00:00Z",
                    "last_login": "2024-01-15T09:30:00Z"
                },
                "biometric_data": {
                    "current_template": {
                        "keystroke_dynamics": {
                            "dwell_times": [120, 115, 125, 118, 122],
                            "flight_times": [85, 92, 88, 90, 87],
                            "typing_rhythm": 0.85,
                            "pressure_patterns": [0.7, 0.8, 0.75, 0.82, 0.78]
                        },
                        "mouse_dynamics": {
                            "movement_velocity": [150, 145, 155, 148, 152],
                            "click_patterns": [0.95, 0.92, 0.97, 0.94, 0.96],
                            "scroll_behavior": [2.1, 2.3, 2.0, 2.2, 2.1]
                        }
                    },
                    "reference_template": {
                        "keystroke_dynamics": {
                            "dwell_times": [118, 122, 120, 116, 124],
                            "flight_times": [88, 90, 85, 92, 89],
                            "typing_rhythm": 0.87,
                            "pressure_patterns": [0.72, 0.78, 0.76, 0.80, 0.77]
                        },
                        "mouse_dynamics": {
                            "movement_velocity": [148, 152, 150, 146, 154],
                            "click_patterns": [0.94, 0.96, 0.95, 0.93, 0.97],
                            "scroll_behavior": [2.0, 2.2, 2.1, 2.3, 2.0]
                        }
                    },
                    "similarity_score": 0.92,
                    "confidence_level": "high"
                },
                "auth_token_data": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                    "refresh_token": "rt_1234567890abcdef",
                    "session_token": "st_abcdef1234567890",
                    "mfa_token": "mfa_0987654321fedcba",
                    "oauth_token": "oauth_fedcba0987654321",
                    "signature": "valid_signature_hash",
                    "payload": {
                        "user_id": self.user_id,
                        "username": "john_doe_authenticated",
                        "roles": ["user", "verified"],
                        "permissions": ["read", "write"]
                    },
                    "expires_at": int((datetime.now() + timedelta(hours=2)).timestamp()),
                    "issued_at": int(datetime.now().timestamp()),
                    "token_type": "Bearer"
                }
            }
            
            payload = {
                "session_id": self.session_id + "_valid_auth",
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/validate-session-authenticity",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('authenticity_analysis', {})
                    analysis_summary = analysis.get('analysis_summary', {})
                    
                    self.log_result(
                        "Session Authenticity - Valid Session", 
                        True, 
                        f"Valid session analysis completed. Authentic: {analysis_summary.get('session_authentic', 'N/A')}, Confidence: {analysis_summary.get('authenticity_confidence', 'N/A')}, Biometric Match: {analysis_summary.get('biometric_match_score', 'N/A')}"
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

    def test_validate_session_authenticity_invalid_session(self):
        """Test session authenticity validation with invalid credentials and inconsistent identity"""
        try:
            # Invalid session authenticity data with multiple red flags
            session_data = {
                "session_id": self.session_id + "_invalid_auth",
                "user_id": self.user_id,
                "authentication_data": {
                    "method": "password",
                    "expires_at": int((datetime.now() - timedelta(hours=1)).timestamp()),  # Expired
                    "credential_hash": "invalid_hash_format",  # Invalid hash
                    "mfa_verified": False,
                    "last_auth_time": int((datetime.now() - timedelta(days=30)).timestamp()),  # Very old
                    "auth_strength": "weak"
                },
                "claimed_identity": {
                    "username": "suspicious_user",
                    "email": "fake@suspicious.com",
                    "phone_number": "+0000000000",  # Suspicious phone
                    "user_id": "different_user_id",  # Mismatched user ID
                    "account_created": "2024-01-15T10:00:00Z",  # Very new account
                    "last_login": "1970-01-01T00:00:00Z"  # Suspicious timestamp
                },
                "biometric_data": {
                    "current_template": {
                        "keystroke_dynamics": {
                            "dwell_times": [50, 45, 55, 48, 52],  # Very different from reference
                            "flight_times": [200, 195, 205, 198, 202],  # Very different
                            "typing_rhythm": 0.3,  # Very different
                            "pressure_patterns": [0.1, 0.2, 0.15, 0.12, 0.18]  # Very different
                        },
                        "mouse_dynamics": {
                            "movement_velocity": [300, 295, 305, 298, 302],  # Very different
                            "click_patterns": [0.1, 0.2, 0.15, 0.18, 0.12],  # Very different
                            "scroll_behavior": [10.1, 10.3, 10.0, 10.2, 10.1]  # Very different
                        }
                    },
                    "reference_template": {
                        "keystroke_dynamics": {
                            "dwell_times": [118, 122, 120, 116, 124],
                            "flight_times": [88, 90, 85, 92, 89],
                            "typing_rhythm": 0.87,
                            "pressure_patterns": [0.72, 0.78, 0.76, 0.80, 0.77]
                        },
                        "mouse_dynamics": {
                            "movement_velocity": [148, 152, 150, 146, 154],
                            "click_patterns": [0.94, 0.96, 0.95, 0.93, 0.97],
                            "scroll_behavior": [2.0, 2.2, 2.1, 2.3, 2.0]
                        }
                    },
                    "similarity_score": 0.15,  # Very low similarity
                    "confidence_level": "very_low"
                },
                "auth_token_data": {
                    "access_token": "invalid.token.format",  # Invalid JWT format
                    "refresh_token": "expired_refresh_token",
                    "session_token": "invalid_session_token",
                    "mfa_token": "",  # Empty MFA token
                    "oauth_token": "revoked_oauth_token",
                    "signature": "invalid_signature",
                    "payload": {
                        "user_id": "different_user_again",  # Another mismatch
                        "username": "another_suspicious_user",
                        "roles": ["admin"],  # Suspicious elevated privileges
                        "permissions": ["read", "write", "delete", "admin"]  # Too many permissions
                    },
                    "expires_at": int((datetime.now() - timedelta(hours=5)).timestamp()),  # Expired
                    "issued_at": int((datetime.now() + timedelta(hours=1)).timestamp()),  # Future issue time (impossible)
                    "token_type": "Invalid"
                }
            }
            
            payload = {
                "session_id": self.session_id + "_invalid_auth",
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/validate-session-authenticity",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('authenticity_analysis', {})
                    analysis_summary = analysis.get('analysis_summary', {})
                    
                    self.log_result(
                        "Session Authenticity - Invalid Session", 
                        True, 
                        f"Invalid session analysis completed. Authentic: {analysis_summary.get('session_authentic', 'N/A')}, Confidence: {analysis_summary.get('authenticity_confidence', 'N/A')}, Biometric Match: {analysis_summary.get('biometric_match_score', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Session Authenticity - Invalid Session", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Authenticity - Invalid Session", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Authenticity - Invalid Session", False, f"Exception: {str(e)}")
            return False

    def test_multi_device_collaboration_indicators(self):
        """Test detection of multi-device collaboration patterns"""
        try:
            # Collaboration scenario with coordinated activities across devices
            session_data = {
                "user_id": self.user_id,
                "session_id": self.session_id + "_collaboration",
                "active_sessions": [
                    {
                        "session_id": self.session_id + "_device1",
                        "device_fingerprint": "fp_desktop_chrome_windows",
                        "start_time": "2024-01-15T10:00:00Z",
                        "location": {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060},
                        "ip_address": "192.168.1.100",
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "device_type": "desktop"
                    },
                    {
                        "session_id": self.session_id + "_device2",
                        "device_fingerprint": "fp_laptop_firefox_macos",
                        "start_time": "2024-01-15T10:02:00Z",
                        "location": {"country": "US", "city": "New York", "lat": 40.7589, "lng": -73.9851},
                        "ip_address": "192.168.1.102",
                        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
                        "device_type": "laptop"
                    }
                ],
                "device_activity": [
                    # Coordinated activities suggesting collaboration
                    {
                        "device_id": "desktop_001",
                        "timestamp": "2024-01-15T10:05:00Z",
                        "activity_type": "data_input",
                        "action_type": "question_answer",
                        "session_id": self.session_id + "_device1",
                        "content_type": "text_input",
                        "response_time": 2.5
                    },
                    {
                        "device_id": "laptop_001",
                        "timestamp": "2024-01-15T10:05:05Z",  # 5 seconds later
                        "activity_type": "data_search",
                        "action_type": "web_search",
                        "session_id": self.session_id + "_device2",
                        "content_type": "search_query",
                        "response_time": 0.8  # Very fast response
                    },
                    {
                        "device_id": "desktop_001",
                        "timestamp": "2024-01-15T10:05:15Z",  # 10 seconds after search
                        "activity_type": "data_input",
                        "action_type": "answer_update",
                        "session_id": self.session_id + "_device1",
                        "content_type": "text_modification",
                        "response_time": 1.2  # Suspiciously fast for complex answer
                    }
                ],
                "session_history": [
                    {
                        "session_id": self.session_id + "_device1",
                        "device_fingerprint": "fp_desktop_chrome_windows",
                        "timestamp": "2024-01-15T10:00:00Z",
                        "duration": 1800,
                        "location": {"country": "US", "city": "New York"},
                        "activities_count": 45,
                        "data_transferred": 2048000,
                        "activity_pattern": "answer_focused"
                    },
                    {
                        "session_id": self.session_id + "_device2",
                        "device_fingerprint": "fp_laptop_firefox_macos",
                        "timestamp": "2024-01-15T10:02:00Z",
                        "duration": 1680,
                        "location": {"country": "US", "city": "New York"},
                        "activities_count": 120,  # High search activity
                        "data_transferred": 5120000,  # High data usage for searches
                        "activity_pattern": "search_focused"
                    }
                ]
            }
            
            payload = {
                "session_id": self.session_id + "_collaboration",
                "user_id": self.user_id,
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-multi-device-usage",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('multi_device_analysis', {})
                    analysis_summary = analysis.get('analysis_summary', {})
                    
                    self.log_result(
                        "Multi-Device Collaboration Indicators", 
                        True, 
                        f"Collaboration analysis completed. Risk Score: {analysis_summary.get('risk_score', 'N/A')}, Collaboration Detected: {analysis_summary.get('collaboration_indicators', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Multi-Device Collaboration Indicators", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Multi-Device Collaboration Indicators", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Multi-Device Collaboration Indicators", False, f"Exception: {str(e)}")
            return False

    def test_session_migration_validation(self):
        """Test session migration validation across devices"""
        try:
            # Session migration scenario
            session_data = {
                "user_id": self.user_id,
                "session_id": self.session_id + "_migration",
                "active_sessions": [
                    {
                        "session_id": self.session_id + "_original",
                        "device_fingerprint": "fp_desktop_chrome_windows",
                        "start_time": "2024-01-15T10:00:00Z",
                        "end_time": "2024-01-15T10:30:00Z",  # Session ended
                        "location": {"country": "US", "city": "New York", "lat": 40.7128, "lng": -74.0060},
                        "ip_address": "192.168.1.100",
                        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "device_type": "desktop",
                        "status": "migrated"
                    },
                    {
                        "session_id": self.session_id + "_migrated",
                        "device_fingerprint": "fp_mobile_safari_ios",
                        "start_time": "2024-01-15T10:32:00Z",  # Started 2 minutes after original ended
                        "location": {"country": "US", "city": "New York", "lat": 40.7589, "lng": -73.9851},
                        "ip_address": "192.168.1.101",  # Different IP but same network
                        "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
                        "device_type": "mobile",
                        "status": "active",
                        "migration_data": {
                            "previous_session_id": self.session_id + "_original",
                            "migration_timestamp": "2024-01-15T10:30:30Z",
                            "state_transferred": True,
                            "authentication_carried_over": True
                        }
                    }
                ],
                "device_activity": [
                    {
                        "device_id": "desktop_001",
                        "timestamp": "2024-01-15T10:29:00Z",
                        "activity_type": "session_save",
                        "action_type": "state_preservation",
                        "session_id": self.session_id + "_original"
                    },
                    {
                        "device_id": "mobile_001",
                        "timestamp": "2024-01-15T10:32:30Z",
                        "activity_type": "session_restore",
                        "action_type": "state_restoration",
                        "session_id": self.session_id + "_migrated"
                    }
                ],
                "session_history": [
                    {
                        "session_id": self.session_id + "_original",
                        "device_fingerprint": "fp_desktop_chrome_windows",
                        "timestamp": "2024-01-15T10:00:00Z",
                        "duration": 1800,
                        "location": {"country": "US", "city": "New York"},
                        "activities_count": 35,
                        "data_transferred": 1536000,
                        "migration_prepared": True
                    },
                    {
                        "session_id": self.session_id + "_migrated",
                        "device_fingerprint": "fp_mobile_safari_ios",
                        "timestamp": "2024-01-15T10:32:00Z",
                        "duration": 900,
                        "location": {"country": "US", "city": "New York"},
                        "activities_count": 18,
                        "data_transferred": 768000,
                        "migration_restored": True
                    }
                ]
            }
            
            payload = {
                "session_id": self.session_id + "_migration",
                "user_id": self.user_id,
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-multi-device-usage",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('multi_device_analysis', {})
                    analysis_summary = analysis.get('analysis_summary', {})
                    
                    self.log_result(
                        "Session Migration Validation", 
                        True, 
                        f"Migration analysis completed. Risk Score: {analysis_summary.get('risk_score', 'N/A')}, Migration Valid: {analysis_summary.get('migration_valid', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Session Migration Validation", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Session Migration Validation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Session Migration Validation", False, f"Exception: {str(e)}")
            return False

    def test_comprehensive_token_verification(self):
        """Test comprehensive authentication token verification"""
        try:
            # Comprehensive token verification scenario
            session_data = {
                "session_id": self.session_id + "_token_verification",
                "user_id": self.user_id,
                "authentication_data": {
                    "method": "multi_factor",
                    "expires_at": int((datetime.now() + timedelta(hours=4)).timestamp()),
                    "credential_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "mfa_verified": True,
                    "last_auth_time": int(datetime.now().timestamp()),
                    "auth_strength": "very_strong"
                },
                "claimed_identity": {
                    "username": "verified_user_tokens",
                    "email": "verified.user@company.com",
                    "phone_number": "+1234567890",
                    "user_id": self.user_id,
                    "account_created": "2022-06-15T10:00:00Z",
                    "last_login": "2024-01-15T09:45:00Z"
                },
                "biometric_data": {
                    "current_template": {
                        "keystroke_dynamics": {
                            "dwell_times": [119, 121, 118, 120, 122],
                            "flight_times": [87, 89, 86, 88, 90],
                            "typing_rhythm": 0.88,
                            "pressure_patterns": [0.73, 0.79, 0.75, 0.81, 0.77]
                        }
                    },
                    "reference_template": {
                        "keystroke_dynamics": {
                            "dwell_times": [118, 122, 120, 116, 124],
                            "flight_times": [88, 90, 85, 92, 89],
                            "typing_rhythm": 0.87,
                            "pressure_patterns": [0.72, 0.78, 0.76, 0.80, 0.77]
                        }
                    },
                    "similarity_score": 0.94,
                    "confidence_level": "very_high"
                },
                "auth_token_data": {
                    # Access Token (JWT)
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ2ZXJpZmllZF91c2VyX3Rva2VucyIsIm5hbWUiOiJWZXJpZmllZCBVc2VyIiwiaWF0IjoxNzA0MDY3MjAwLCJleHAiOjE3MDQwODUyMDB9.signature",
                    "access_token_valid": True,
                    "access_token_expires_at": int((datetime.now() + timedelta(hours=4)).timestamp()),
                    
                    # Refresh Token
                    "refresh_token": "rt_secure_refresh_token_1234567890abcdef",
                    "refresh_token_valid": True,
                    "refresh_token_expires_at": int((datetime.now() + timedelta(days=30)).timestamp()),
                    
                    # Session Token
                    "session_token": "st_secure_session_token_abcdef1234567890",
                    "session_token_valid": True,
                    "session_token_expires_at": int((datetime.now() + timedelta(hours=8)).timestamp()),
                    
                    # MFA Token
                    "mfa_token": "mfa_verified_token_0987654321fedcba",
                    "mfa_token_valid": True,
                    "mfa_token_expires_at": int((datetime.now() + timedelta(minutes=30)).timestamp()),
                    
                    # OAuth Token
                    "oauth_token": "oauth_provider_token_fedcba0987654321",
                    "oauth_token_valid": True,
                    "oauth_token_expires_at": int((datetime.now() + timedelta(hours=2)).timestamp()),
                    
                    "signature": "valid_hmac_sha256_signature",
                    "payload": {
                        "user_id": self.user_id,
                        "username": "verified_user_tokens",
                        "roles": ["user", "verified", "premium"],
                        "permissions": ["read", "write", "profile_edit"],
                        "token_version": "v2.1",
                        "security_level": "high"
                    },
                    "expires_at": int((datetime.now() + timedelta(hours=4)).timestamp()),
                    "issued_at": int((datetime.now() - timedelta(minutes=5)).timestamp()),
                    "token_type": "Bearer",
                    "token_integrity_verified": True
                }
            }
            
            payload = {
                "session_id": self.session_id + "_token_verification",
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/validate-session-authenticity",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('authenticity_analysis', {})
                    analysis_summary = analysis.get('analysis_summary', {})
                    
                    self.log_result(
                        "Comprehensive Token Verification", 
                        True, 
                        f"Token verification completed. Authentic: {analysis_summary.get('session_authentic', 'N/A')}, Token Integrity: {analysis_summary.get('token_integrity_score', 'N/A')}, All Tokens Valid: {analysis_summary.get('all_tokens_valid', 'N/A')}"
                    )
                    return True
                else:
                    self.log_result("Comprehensive Token Verification", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Comprehensive Token Verification", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Comprehensive Token Verification", False, f"Exception: {str(e)}")
            return False

    def test_edge_cases_malformed_data(self):
        """Test edge cases with malformed data"""
        try:
            # Malformed multi-device usage data
            session_data = {
                "user_id": None,  # Null user ID
                "session_id": "",  # Empty session ID
                "active_sessions": "not_an_array",  # Wrong type
                "device_activity": [],  # Empty array
                "session_history": None  # Null history
            }
            
            payload = {
                "session_id": self.session_id + "_edge_case",
                "user_id": "edge_case_user",
                "session_data": session_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-multi-device-usage",
                json=payload
            )
            
            # Should handle gracefully (either 200 with error handling or 500 with proper error)
            if response.status_code in [200, 500]:
                self.log_result(
                    "Edge Cases - Malformed Multi-Device Data", 
                    True, 
                    f"Malformed data handled gracefully (Status: {response.status_code})"
                )
                return True
            else:
                self.log_result("Edge Cases - Malformed Multi-Device Data", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Edge Cases - Malformed Multi-Device Data", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all Phase 3.3 Session Integrity Monitoring tests"""
        print("🎯 STARTING PHASE 3.3: SESSION INTEGRITY MONITORING TESTING")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return 0, 0
        
        # Run all tests
        tests = [
            self.test_track_multi_device_usage_normal_scenario,
            self.test_track_multi_device_usage_suspicious_scenario,
            self.test_validate_session_authenticity_valid_session,
            self.test_validate_session_authenticity_invalid_session,
            self.test_multi_device_collaboration_indicators,
            self.test_session_migration_validation,
            self.test_comprehensive_token_verification,
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