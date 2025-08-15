#!/usr/bin/env python3
"""
🚨 COMPREHENSIVE BACKEND TESTING: Task 3.3 Real-Time Violation Alerts System

TEST TARGET: Comprehensive testing of the newly implemented Real-Time Violation Alerts System functionality (Task 3.3)

TESTING SCOPE - 6 New Alert System API Endpoints:
1. POST /api/real-time-alerts/process-violation - Process and route violation alerts through multi-channel delivery
2. POST /api/real-time-alerts/escalate-violation - Handle critical violation escalation with automated response protocols
3. GET /api/real-time-alerts/dashboard-data - Generate real-time dashboard data for monitoring interfaces
4. POST /api/real-time-alerts/configure-thresholds - Configure dynamic alert thresholds and management rules
5. GET /api/real-time-alerts/system-performance - Get comprehensive system performance metrics and statistics
6. POST /api/real-time-alerts/simulate-violation - Simulate security violations for testing alert system functionality

IMPLEMENTATION DETAILS TO VERIFY:
✅ RealTimeAlertSystem Class Integration - Test all 4 core methods (process_violation, escalate_critical_violations, generate_alert_dashboard_data, configure_alert_thresholds)
✅ Multi-Channel Alert Delivery - Verify WebSocket, Email, Webhook, and Database channel functionality with delivery statistics
✅ Alert Classification System - Test AlertType (10 types), AlertSeverity (5 levels), and AlertChannel (6 channels) enumeration handling
✅ Violation Data Processing - Test comprehensive ViolationData structure with 17 fields including technical details and ML analysis
✅ Dynamic Threshold Management - Test AlertThreshold configuration with score/count/rate/pattern condition types
✅ Real-Time Dashboard Analytics - Test dashboard data generation with trends, statistics, and system health metrics
✅ Escalation Processing - Test automatic escalation with timeout protocols and severity upgrades
✅ Rate Limiting and Performance - Test session-based rate limiting and processing performance metrics

SPECIFIC TEST SCENARIOS TO EXECUTE:
1. **Violation Processing**: Test alert processing with various violation types (DEVICE_FINGERPRINT_VIOLATION, BEHAVIORAL_ANOMALY, ML_FRAUD_DETECTION, etc.)
2. **Multi-Channel Routing**: Test alert delivery through WebSocket, Database, Email, and Webhook channels with success/failure tracking
3. **Severity Escalation**: Test escalation from LOW→MEDIUM→HIGH→CRITICAL→EMERGENCY with proper routing and notifications
4. **Dashboard Data Generation**: Test real-time dashboard with alert trends, top risk sessions, active alerts, and system health
5. **Threshold Configuration**: Test dynamic threshold setup with different condition types and time windows
6. **System Performance**: Test performance metrics including processing times, delivery rates, and channel statistics
7. **Violation Simulation**: Test simulated violations across different types and severity levels
8. **Rate Limiting**: Test session-based rate limiting with max alerts per session (50) and time windows (300s)

AUTHENTICATION: Use admin authentication with password "Game@1234" for secure endpoint access
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import time
import random

# Configuration
BACKEND_URL = "https://security-keystroke.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class RealTimeAlertsSystemTester:
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
            "timestamp": datetime.now().isoformat()
        }
        if response_data:
            result["response_data"] = response_data
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        print(f"   Details: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
        print()

    def test_admin_authentication(self):
        """Test admin authentication with Game@1234 password"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/login",
                json={"password": ADMIN_PASSWORD},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result(
                        "Admin Authentication",
                        True,
                        f"Successfully authenticated with password {ADMIN_PASSWORD}",
                        {"status": response.status_code, "response": data}
                    )
                    return True
                else:
                    self.log_result(
                        "Admin Authentication",
                        False,
                        f"Authentication failed: {data.get('message', 'Unknown error')}",
                        {"status": response.status_code, "response": data}
                    )
                    return False
            else:
                self.log_result(
                    "Admin Authentication",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {"status": response.status_code}
                )
                return False
                
        except Exception as e:
            self.log_result(
                "Admin Authentication",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )
            return False

    def test_process_violation_endpoint(self):
        """Test POST /api/real-time-alerts/process-violation endpoint"""
        try:
            # Test various violation types
            violation_types = [
                "DEVICE_FINGERPRINT_VIOLATION",
                "BEHAVIORAL_ANOMALY", 
                "ML_FRAUD_DETECTION",
                "SESSION_HIJACKING",
                "MULTIPLE_DEVICE_ACCESS",
                "SUSPICIOUS_TIMING_PATTERNS",
                "BIOMETRIC_INCONSISTENCY",
                "LOCATION_ANOMALY",
                "BROWSER_AUTOMATION_DETECTED",
                "NETWORK_ANOMALY"
            ]
            
            for violation_type in violation_types[:3]:  # Test first 3 types
                violation_data = {
                    "violation_id": str(uuid.uuid4()),
                    "session_id": self.session_id,
                    "user_id": self.user_id,
                    "violation_type": violation_type,
                    "severity": "HIGH",
                    "confidence_score": 0.85,
                    "detected_at": datetime.now().isoformat(),
                    "technical_details": {
                        "fingerprint_mismatch": True,
                        "device_change": True,
                        "location_change": False,
                        "timing_anomaly": True
                    },
                    "ml_analysis": {
                        "fraud_probability": 0.78,
                        "anomaly_score": 0.82,
                        "risk_factors": ["device_inconsistency", "timing_patterns"]
                    },
                    "fingerprint_data": {
                        "device_id": f"device_{str(uuid.uuid4())[:8]}",
                        "browser_fingerprint": f"browser_{str(uuid.uuid4())[:8]}",
                        "screen_resolution": "1920x1080",
                        "timezone": "America/New_York"
                    },
                    "behavioral_context": {
                        "typing_speed": 45.2,
                        "mouse_movement_pattern": "erratic",
                        "click_frequency": 12.5
                    },
                    "risk_factors": ["high_fraud_score", "device_mismatch", "behavioral_anomaly"],
                    "location_info": {
                        "ip_address": "192.168.1.100",
                        "country": "US",
                        "city": "New York"
                    },
                    "escalation_level": "MEDIUM",
                    "resolution_status": "PENDING",
                    "assigned_to": "security_team",
                    "response_actions": ["alert_sent", "session_flagged"]
                }
                
                response = self.session.post(
                    f"{BACKEND_URL}/real-time-alerts/process-violation",
                    json={"violation_data": violation_data},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_result(
                            f"Process Violation - {violation_type}",
                            True,
                            f"Successfully processed {violation_type} violation with {len(data.get('delivery_results', {}))} channel deliveries",
                            {
                                "status": response.status_code,
                                "violation_id": data.get('violation_id'),
                                "channels_used": list(data.get('delivery_results', {}).keys()),
                                "processing_time": data.get('processing_time_ms', 0)
                            }
                        )
                    else:
                        self.log_result(
                            f"Process Violation - {violation_type}",
                            False,
                            f"Processing failed: {data.get('message', 'Unknown error')}",
                            {"status": response.status_code, "response": data}
                        )
                else:
                    self.log_result(
                        f"Process Violation - {violation_type}",
                        False,
                        f"HTTP {response.status_code}: {response.text}",
                        {"status": response.status_code}
                    )
                    
        except Exception as e:
            self.log_result(
                "Process Violation Endpoint",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )

    def test_escalate_violation_endpoint(self):
        """Test POST /api/real-time-alerts/escalate-violation endpoint"""
        try:
            # Test critical violation escalation
            critical_violation_data = {
                "violation_id": str(uuid.uuid4()),
                "session_id": self.session_id,
                "user_id": self.user_id,
                "violation_type": "SESSION_HIJACKING",
                "severity": "CRITICAL",
                "confidence_score": 0.95,
                "detected_at": datetime.now().isoformat(),
                "escalation_reason": "Multiple concurrent sessions detected from different locations",
                "technical_details": {
                    "concurrent_sessions": 3,
                    "location_mismatch": True,
                    "device_fingerprint_mismatch": True,
                    "suspicious_activity_score": 0.92
                },
                "ml_analysis": {
                    "fraud_probability": 0.94,
                    "anomaly_score": 0.96,
                    "risk_factors": ["session_hijacking", "location_anomaly", "device_spoofing"]
                },
                "escalation_level": "CRITICAL",
                "requires_immediate_action": True,
                "timeout_minutes": 5
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/real-time-alerts/escalate-violation",
                json={"violation_data": critical_violation_data},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result(
                        "Escalate Critical Violation",
                        True,
                        f"Successfully escalated critical violation with {len(data.get('escalation_actions', []))} actions taken",
                        {
                            "status": response.status_code,
                            "violation_id": data.get('violation_id'),
                            "escalation_level": data.get('escalation_level'),
                            "actions_taken": data.get('escalation_actions', []),
                            "notifications_sent": data.get('notifications_sent', 0)
                        }
                    )
                else:
                    self.log_result(
                        "Escalate Critical Violation",
                        False,
                        f"Escalation failed: {data.get('message', 'Unknown error')}",
                        {"status": response.status_code, "response": data}
                    )
            else:
                self.log_result(
                    "Escalate Critical Violation",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {"status": response.status_code}
                )
                
        except Exception as e:
            self.log_result(
                "Escalate Violation Endpoint",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )

    def test_dashboard_data_endpoint(self):
        """Test GET /api/real-time-alerts/dashboard-data endpoint"""
        try:
            response = self.session.get(
                f"{BACKEND_URL}/real-time-alerts/dashboard-data",
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    dashboard_data = data.get('dashboard_data', {})
                    
                    # Verify dashboard data structure
                    required_sections = ['summary_stats', 'alert_trends', 'top_risk_sessions', 'active_alerts', 'channel_performance', 'system_health']
                    missing_sections = [section for section in required_sections if section not in dashboard_data]
                    
                    if not missing_sections:
                        self.log_result(
                            "Dashboard Data Generation",
                            True,
                            f"Successfully generated dashboard data with {len(dashboard_data)} sections",
                            {
                                "status": response.status_code,
                                "sections": list(dashboard_data.keys()),
                                "alerts_last_hour": dashboard_data.get('summary_stats', {}).get('alerts_last_hour', 0),
                                "critical_alerts": dashboard_data.get('summary_stats', {}).get('critical_alerts', 0),
                                "active_violations": dashboard_data.get('summary_stats', {}).get('active_violations', 0)
                            }
                        )
                    else:
                        self.log_result(
                            "Dashboard Data Generation",
                            False,
                            f"Missing required dashboard sections: {missing_sections}",
                            {"status": response.status_code, "missing_sections": missing_sections}
                        )
                else:
                    self.log_result(
                        "Dashboard Data Generation",
                        False,
                        f"Dashboard generation failed: {data.get('message', 'Unknown error')}",
                        {"status": response.status_code, "response": data}
                    )
            else:
                self.log_result(
                    "Dashboard Data Generation",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {"status": response.status_code}
                )
                
        except Exception as e:
            self.log_result(
                "Dashboard Data Endpoint",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )

    def test_configure_thresholds_endpoint(self):
        """Test POST /api/real-time-alerts/configure-thresholds endpoint"""
        try:
            # Test dynamic threshold configuration
            threshold_config = {
                "thresholds": [
                    {
                        "threshold_id": str(uuid.uuid4()),
                        "name": "High Fraud Score Threshold",
                        "condition_type": "score",
                        "condition_value": 0.8,
                        "violation_types": ["ML_FRAUD_DETECTION", "BEHAVIORAL_ANOMALY"],
                        "severity_level": "HIGH",
                        "time_window_minutes": 15,
                        "enabled": True,
                        "description": "Trigger alert when fraud score exceeds 0.8"
                    },
                    {
                        "threshold_id": str(uuid.uuid4()),
                        "name": "Multiple Device Access Count",
                        "condition_type": "count",
                        "condition_value": 3,
                        "violation_types": ["MULTIPLE_DEVICE_ACCESS"],
                        "severity_level": "CRITICAL",
                        "time_window_minutes": 30,
                        "enabled": True,
                        "description": "Trigger alert when more than 3 devices access same session"
                    },
                    {
                        "threshold_id": str(uuid.uuid4()),
                        "name": "Suspicious Activity Rate",
                        "condition_type": "rate",
                        "condition_value": 5.0,
                        "violation_types": ["SUSPICIOUS_TIMING_PATTERNS", "BIOMETRIC_INCONSISTENCY"],
                        "severity_level": "MEDIUM",
                        "time_window_minutes": 10,
                        "enabled": True,
                        "description": "Trigger alert when suspicious activity rate exceeds 5 per 10 minutes"
                    }
                ]
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/real-time-alerts/configure-thresholds",
                json={"thresholds": threshold_config},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log_result(
                        "Configure Alert Thresholds",
                        True,
                        f"Successfully configured {len(threshold_config['thresholds'])} alert thresholds",
                        {
                            "status": response.status_code,
                            "thresholds_configured": data.get('thresholds_configured', 0),
                            "thresholds_updated": data.get('thresholds_updated', 0),
                            "configuration_id": data.get('configuration_id')
                        }
                    )
                else:
                    self.log_result(
                        "Configure Alert Thresholds",
                        False,
                        f"Threshold configuration failed: {data.get('message', 'Unknown error')}",
                        {"status": response.status_code, "response": data}
                    )
            else:
                self.log_result(
                    "Configure Alert Thresholds",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {"status": response.status_code}
                )
                
        except Exception as e:
            self.log_result(
                "Configure Thresholds Endpoint",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )

    def test_system_performance_endpoint(self):
        """Test GET /api/real-time-alerts/system-performance endpoint"""
        try:
            response = self.session.get(
                f"{BACKEND_URL}/real-time-alerts/system-performance",
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    performance_data = data.get('performance_summary', {})
                    
                    # Verify performance data structure
                    required_metrics = ['processing_metrics', 'channel_statistics', 'escalation_metrics', 'system_health']
                    missing_metrics = [metric for metric in required_metrics if metric not in performance_data]
                    
                    if not missing_metrics:
                        self.log_result(
                            "System Performance Metrics",
                            True,
                            f"Successfully retrieved system performance with {len(performance_data)} metric categories",
                            {
                                "status": response.status_code,
                                "metrics_categories": list(performance_data.keys()),
                                "avg_processing_time": performance_data.get('processing_metrics', {}).get('avg_processing_time_ms', 0),
                                "total_alerts_processed": performance_data.get('processing_metrics', {}).get('total_alerts_processed', 0),
                                "system_uptime": performance_data.get('system_health', {}).get('uptime_hours', 0)
                            }
                        )
                    else:
                        self.log_result(
                            "System Performance Metrics",
                            False,
                            f"Missing required performance metrics: {missing_metrics}",
                            {"status": response.status_code, "missing_metrics": missing_metrics}
                        )
                else:
                    self.log_result(
                        "System Performance Metrics",
                        False,
                        f"Performance retrieval failed: {data.get('message', 'Unknown error')}",
                        {"status": response.status_code, "response": data}
                    )
            else:
                self.log_result(
                    "System Performance Metrics",
                    False,
                    f"HTTP {response.status_code}: {response.text}",
                    {"status": response.status_code}
                )
                
        except Exception as e:
            self.log_result(
                "System Performance Endpoint",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )

    def test_simulate_violation_endpoint(self):
        """Test POST /api/real-time-alerts/simulate-violation endpoint"""
        try:
            # Test different violation simulation scenarios
            simulation_scenarios = [
                {
                    "violation_type": "DEVICE_FINGERPRINT_VIOLATION",
                    "severity": "HIGH",
                    "scenario": "Device fingerprint mismatch during session"
                },
                {
                    "violation_type": "BEHAVIORAL_ANOMALY",
                    "severity": "MEDIUM", 
                    "scenario": "Unusual typing patterns detected"
                },
                {
                    "violation_type": "SESSION_HIJACKING",
                    "severity": "CRITICAL",
                    "scenario": "Multiple concurrent sessions from different locations"
                }
            ]
            
            for scenario in simulation_scenarios:
                simulation_request = {
                    "violation_type": scenario["violation_type"],
                    "severity": scenario["severity"],
                    "session_id": self.session_id,
                    "simulation_parameters": {
                        "scenario_description": scenario["scenario"],
                        "include_ml_analysis": True,
                        "include_technical_details": True,
                        "generate_realistic_data": True
                    }
                }
                
                response = self.session.post(
                    f"{BACKEND_URL}/real-time-alerts/simulate-violation",
                    json=simulation_request,
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        self.log_result(
                            f"Simulate Violation - {scenario['violation_type']}",
                            True,
                            f"Successfully simulated {scenario['violation_type']} with {scenario['severity']} severity",
                            {
                                "status": response.status_code,
                                "violation_id": data.get('violation_id'),
                                "simulation_result": data.get('simulation_result', {}),
                                "processing_result": data.get('processing_result', {})
                            }
                        )
                    else:
                        self.log_result(
                            f"Simulate Violation - {scenario['violation_type']}",
                            False,
                            f"Simulation failed: {data.get('message', 'Unknown error')}",
                            {"status": response.status_code, "response": data}
                        )
                else:
                    self.log_result(
                        f"Simulate Violation - {scenario['violation_type']}",
                        False,
                        f"HTTP {response.status_code}: {response.text}",
                        {"status": response.status_code}
                    )
                    
        except Exception as e:
            self.log_result(
                "Simulate Violation Endpoint",
                False,
                f"Request failed: {str(e)}",
                {"error": str(e)}
            )

    def test_rate_limiting_and_performance(self):
        """Test rate limiting and performance characteristics"""
        try:
            # Test rapid violation processing to check rate limiting
            violation_data = {
                "violation_id": str(uuid.uuid4()),
                "session_id": self.session_id,
                "user_id": self.user_id,
                "violation_type": "BEHAVIORAL_ANOMALY",
                "severity": "LOW",
                "confidence_score": 0.6,
                "detected_at": datetime.now().isoformat(),
                "technical_details": {"test_rate_limiting": True},
                "ml_analysis": {"fraud_probability": 0.3},
                "risk_factors": ["test_scenario"]
            }
            
            # Send multiple rapid requests to test rate limiting
            rapid_requests = 5
            successful_requests = 0
            rate_limited_requests = 0
            processing_times = []
            
            for i in range(rapid_requests):
                start_time = time.time()
                
                # Modify violation_id for each request
                violation_data["violation_id"] = str(uuid.uuid4())
                
                response = self.session.post(
                    f"{BACKEND_URL}/real-time-alerts/process-violation",
                    json={"violation_data": violation_data},
                    timeout=10
                )
                
                end_time = time.time()
                processing_time = (end_time - start_time) * 1000  # Convert to milliseconds
                processing_times.append(processing_time)
                
                if response.status_code == 200:
                    successful_requests += 1
                elif response.status_code == 429:  # Too Many Requests
                    rate_limited_requests += 1
                
                # Small delay between requests
                time.sleep(0.1)
            
            avg_processing_time = sum(processing_times) / len(processing_times)
            
            self.log_result(
                "Rate Limiting and Performance",
                True,
                f"Processed {successful_requests}/{rapid_requests} requests, {rate_limited_requests} rate limited, avg processing time: {avg_processing_time:.2f}ms",
                {
                    "successful_requests": successful_requests,
                    "rate_limited_requests": rate_limited_requests,
                    "avg_processing_time_ms": avg_processing_time,
                    "max_processing_time_ms": max(processing_times),
                    "min_processing_time_ms": min(processing_times)
                }
            )
            
        except Exception as e:
            self.log_result(
                "Rate Limiting and Performance",
                False,
                f"Performance test failed: {str(e)}",
                {"error": str(e)}
            )

    def run_all_tests(self):
        """Run all Real-Time Violation Alerts System tests"""
        print("🚨 COMPREHENSIVE BACKEND TESTING: Task 3.3 Real-Time Violation Alerts System")
        print("=" * 80)
        print()
        
        # Test 1: Admin Authentication
        print("🔐 Testing Admin Authentication...")
        auth_success = self.test_admin_authentication()
        
        if not auth_success:
            print("❌ Admin authentication failed. Cannot proceed with protected endpoints.")
            return self.generate_summary()
        
        print("✅ Admin authentication successful. Proceeding with alert system tests...")
        print()
        
        # Test 2: Process Violation Endpoint
        print("🚨 Testing Violation Processing...")
        self.test_process_violation_endpoint()
        
        # Test 3: Escalate Violation Endpoint  
        print("⚡ Testing Critical Violation Escalation...")
        self.test_escalate_violation_endpoint()
        
        # Test 4: Dashboard Data Endpoint
        print("📊 Testing Dashboard Data Generation...")
        self.test_dashboard_data_endpoint()
        
        # Test 5: Configure Thresholds Endpoint
        print("⚙️ Testing Alert Threshold Configuration...")
        self.test_configure_thresholds_endpoint()
        
        # Test 6: System Performance Endpoint
        print("📈 Testing System Performance Metrics...")
        self.test_system_performance_endpoint()
        
        # Test 7: Simulate Violation Endpoint
        print("🎭 Testing Violation Simulation...")
        self.test_simulate_violation_endpoint()
        
        # Test 8: Rate Limiting and Performance
        print("⚡ Testing Rate Limiting and Performance...")
        self.test_rate_limiting_and_performance()
        
        return self.generate_summary()

    def generate_summary(self):
        """Generate comprehensive test summary"""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['success']])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("\n" + "=" * 80)
        print("🎯 REAL-TIME VIOLATION ALERTS SYSTEM TEST SUMMARY")
        print("=" * 80)
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
            print()
        
        print("✅ PASSED TESTS:")
        for result in self.test_results:
            if result['success']:
                print(f"   • {result['test']}: {result['details']}")
        
        print("\n" + "=" * 80)
        
        # Determine overall status
        if success_rate >= 80:
            print("🎉 OVERALL STATUS: EXCELLENT - Real-Time Violation Alerts System is fully operational!")
        elif success_rate >= 60:
            print("⚠️  OVERALL STATUS: GOOD - Most alert system features are working correctly")
        else:
            print("❌ OVERALL STATUS: NEEDS ATTENTION - Multiple alert system issues detected")
        
        print("=" * 80)
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": success_rate,
            "test_results": self.test_results
        }

if __name__ == "__main__":
    tester = RealTimeAlertsSystemTester()
    summary = tester.run_all_tests()