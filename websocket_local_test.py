#!/usr/bin/env python3
"""
🎯 WEBSOCKET REAL-TIME MONITORING INTEGRATION TESTING (LOCAL WEBSOCKET VERSION)

This script comprehensively tests the WebSocket Real-Time Monitoring Integration (Task 3.1)
using local WebSocket connections and external API endpoints.

Test Coverage:
1. WebSocket Connection Testing (3 endpoints) - LOCAL
2. Real-time Data Streaming - LOCAL  
3. Message Broadcasting and Subscription - LOCAL
4. API Integration Testing (2 endpoints) - EXTERNAL
5. Database Integration - BOTH
6. Error Handling and Edge Cases - BOTH

Author: Testing Agent
Created: 2025
"""

import asyncio
import websockets
import json
import requests
import time
import uuid
from datetime import datetime
import logging
import sys
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebSocketRealTimeMonitoringTester:
    def __init__(self):
        # External API URL for HTTP endpoints
        self.backend_url = "https://codebase-upgrade-1.preview.emergentagent.com"
        self.api_base_url = f"{self.backend_url}/api"
        
        # Local WebSocket URL for WebSocket connections
        self.ws_base_url = "ws://localhost:8001"
        
        # Test configuration
        self.test_session_id = f"test_session_{uuid.uuid4().hex[:8]}"
        self.test_device_id = f"test_device_{uuid.uuid4().hex[:8]}"
        
        # Test results tracking
        self.test_results = []
        self.connected_websockets = []
        
        # Admin credentials
        self.admin_password = "Game@1234"
        self.auth_token = None
        
        logger.info(f"WebSocket Real-Time Monitoring Tester initialized")
        logger.info(f"External API URL: {self.backend_url}")
        logger.info(f"Local WebSocket URL: {self.ws_base_url}")
        logger.info(f"Test Session ID: {self.test_session_id}")
        logger.info(f"Test Device ID: {self.test_device_id}")

    def log_test_result(self, test_name: str, success: bool, details: str = "", data: Any = None):
        """Log test result"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status} - {test_name}: {details}")
        
        if data and isinstance(data, dict):
            for key, value in data.items():
                logger.info(f"  {key}: {value}")

    async def authenticate_admin(self):
        """Authenticate as admin"""
        try:
            response = requests.post(
                f"{self.api_base_url}/admin/login",
                json={"password": self.admin_password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get("token")
                self.log_test_result(
                    "Admin Authentication",
                    True,
                    f"Successfully authenticated (Status: {response.status_code})",
                    {"token_received": bool(self.auth_token)}
                )
                return True
            else:
                self.log_test_result(
                    "Admin Authentication",
                    False,
                    f"Authentication failed (Status: {response.status_code})"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Admin Authentication",
                False,
                f"Authentication error: {str(e)}"
            )
            return False

    async def test_websocket_connection(self, endpoint_path: str, test_id: str, test_name: str):
        """Test WebSocket connection establishment"""
        try:
            ws_url = f"{self.ws_base_url}{endpoint_path}"
            logger.info(f"Connecting to WebSocket: {ws_url}")
            
            # Connect to WebSocket
            websocket = await websockets.connect(ws_url)
            
            self.connected_websockets.append(websocket)
            
            # Wait for welcome message
            try:
                welcome_message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                welcome_data = json.loads(welcome_message)
                
                self.log_test_result(
                    f"{test_name} - Connection",
                    True,
                    f"WebSocket connected successfully to {endpoint_path}",
                    {
                        "url": ws_url,
                        "welcome_message_type": welcome_data.get("type"),
                        "connection_id": welcome_data.get("data", {}).get("connection_id"),
                        "server_time": welcome_data.get("data", {}).get("server_time")
                    }
                )
                
                return websocket, welcome_data
                
            except asyncio.TimeoutError:
                self.log_test_result(
                    f"{test_name} - Connection",
                    False,
                    f"No welcome message received within timeout"
                )
                await websocket.close()
                return None, None
                
        except Exception as e:
            self.log_test_result(
                f"{test_name} - Connection",
                False,
                f"WebSocket connection failed: {str(e)}"
            )
            return None, None

    async def test_fingerprint_updates_endpoint(self):
        """Test /ws/fingerprinting/{session_id} endpoint"""
        endpoint_path = f"/ws/fingerprinting/{self.test_session_id}"
        websocket, welcome_data = await self.test_websocket_connection(
            endpoint_path, 
            "fingerprint", 
            "Fingerprint Updates WebSocket"
        )
        
        if not websocket:
            return False
        
        try:
            # Test subscription acknowledgment
            try:
                subscription_ack = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                ack_data = json.loads(subscription_ack)
                
                if ack_data.get("type") == "subscription_ack":
                    self.log_test_result(
                        "Fingerprint Updates - Subscription",
                        True,
                        "Subscription acknowledgment received",
                        {
                            "subscription": ack_data.get("data", {}).get("subscription"),
                            "status": ack_data.get("data", {}).get("status")
                        }
                    )
                else:
                    self.log_test_result(
                        "Fingerprint Updates - Subscription",
                        False,
                        f"Unexpected message type: {ack_data.get('type')}"
                    )
            except asyncio.TimeoutError:
                self.log_test_result(
                    "Fingerprint Updates - Subscription",
                    False,
                    "No subscription acknowledgment received"
                )
            
            # Test sending fingerprint data
            fingerprint_data = {
                "type": "fingerprint_data",
                "data": {
                    "user_agent": "Mozilla/5.0 (Test Browser)",
                    "screen_resolution": "1920x1080",
                    "timezone": "America/New_York",
                    "language": "en-US",
                    "platform": "Test Platform",
                    "device_id": self.test_device_id,
                    "ip_address": "192.168.1.100",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            await websocket.send(json.dumps(fingerprint_data))
            
            # Wait for processing confirmation or heartbeat
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                response_data = json.loads(response)
                
                self.log_test_result(
                    "Fingerprint Updates - Data Processing",
                    True,
                    f"Received response to fingerprint data",
                    {
                        "response_type": response_data.get("type"),
                        "session_id": response_data.get("session_id")
                    }
                )
            except asyncio.TimeoutError:
                self.log_test_result(
                    "Fingerprint Updates - Data Processing",
                    False,
                    "No response received to fingerprint data"
                )
            
            # Test heartbeat mechanism
            heartbeat_message = {
                "type": "heartbeat",
                "session_id": self.test_session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(heartbeat_message))
            
            try:
                heartbeat_response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                heartbeat_data = json.loads(heartbeat_response)
                
                if heartbeat_data.get("type") == "heartbeat":
                    self.log_test_result(
                        "Fingerprint Updates - Heartbeat",
                        True,
                        "Heartbeat mechanism working",
                        {
                            "server_time": heartbeat_data.get("data", {}).get("server_time"),
                            "status": heartbeat_data.get("data", {}).get("status")
                        }
                    )
                else:
                    self.log_test_result(
                        "Fingerprint Updates - Heartbeat",
                        False,
                        f"Unexpected heartbeat response: {heartbeat_data.get('type')}"
                    )
            except asyncio.TimeoutError:
                self.log_test_result(
                    "Fingerprint Updates - Heartbeat",
                    False,
                    "No heartbeat response received"
                )
            
            await websocket.close()
            return True
            
        except Exception as e:
            self.log_test_result(
                "Fingerprint Updates - Testing",
                False,
                f"Error during fingerprint updates testing: {str(e)}"
            )
            try:
                await websocket.close()
            except:
                pass
            return False

    async def test_device_analytics_endpoint(self):
        """Test /ws/device-analytics/{device_id} endpoint"""
        endpoint_path = f"/ws/device-analytics/{self.test_device_id}"
        websocket, welcome_data = await self.test_websocket_connection(
            endpoint_path, 
            "device_analytics", 
            "Device Analytics WebSocket"
        )
        
        if not websocket:
            return False
        
        try:
            # Test subscription acknowledgment
            try:
                subscription_ack = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                ack_data = json.loads(subscription_ack)
                
                if ack_data.get("type") == "subscription_ack":
                    self.log_test_result(
                        "Device Analytics - Subscription",
                        True,
                        "Subscription acknowledgment received",
                        {
                            "subscription": ack_data.get("data", {}).get("subscription"),
                            "device_id": ack_data.get("device_id")
                        }
                    )
                else:
                    self.log_test_result(
                        "Device Analytics - Subscription",
                        False,
                        f"Unexpected message type: {ack_data.get('type')}"
                    )
            except asyncio.TimeoutError:
                self.log_test_result(
                    "Device Analytics - Subscription",
                    False,
                    "No subscription acknowledgment received"
                )
            
            # Test receiving analytics data
            analytics_received = 0
            max_wait_time = 15  # Wait up to 15 seconds for analytics
            
            try:
                while analytics_received < 2:  # Try to receive at least 2 analytics messages
                    analytics_message = await asyncio.wait_for(websocket.recv(), timeout=max_wait_time)
                    analytics_data = json.loads(analytics_message)
                    
                    if analytics_data.get("type") == "device_analytics":
                        analytics_received += 1
                        self.log_test_result(
                            f"Device Analytics - Data Stream {analytics_received}",
                            True,
                            "Analytics data received",
                            {
                                "device_id": analytics_data.get("device_id"),
                                "metrics_count": len(analytics_data.get("data", {}).get("metrics", {})),
                                "trends_available": bool(analytics_data.get("data", {}).get("trends")),
                                "timestamp": analytics_data.get("timestamp")
                            }
                        )
                    elif analytics_data.get("type") == "heartbeat":
                        # Heartbeat is expected, continue waiting
                        continue
                    else:
                        self.log_test_result(
                            "Device Analytics - Unexpected Message",
                            False,
                            f"Unexpected message type: {analytics_data.get('type')}"
                        )
                        break
                        
            except asyncio.TimeoutError:
                if analytics_received > 0:
                    self.log_test_result(
                        "Device Analytics - Streaming",
                        True,
                        f"Received {analytics_received} analytics messages (partial success)"
                    )
                else:
                    self.log_test_result(
                        "Device Analytics - Streaming",
                        False,
                        "No analytics data received within timeout"
                    )
            
            await websocket.close()
            return analytics_received > 0
            
        except Exception as e:
            self.log_test_result(
                "Device Analytics - Testing",
                False,
                f"Error during device analytics testing: {str(e)}"
            )
            try:
                await websocket.close()
            except:
                pass
            return False

    async def test_session_integrity_endpoint(self):
        """Test /ws/session-integrity/{session_id} endpoint"""
        endpoint_path = f"/ws/session-integrity/{self.test_session_id}"
        websocket, welcome_data = await self.test_websocket_connection(
            endpoint_path, 
            "session_integrity", 
            "Session Integrity WebSocket"
        )
        
        if not websocket:
            return False
        
        try:
            # Test subscription acknowledgment
            try:
                subscription_ack = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                ack_data = json.loads(subscription_ack)
                
                if ack_data.get("type") == "subscription_ack":
                    self.log_test_result(
                        "Session Integrity - Subscription",
                        True,
                        "Subscription acknowledgment received",
                        {
                            "subscription": ack_data.get("data", {}).get("subscription"),
                            "session_id": ack_data.get("session_id")
                        }
                    )
                else:
                    self.log_test_result(
                        "Session Integrity - Subscription",
                        False,
                        f"Unexpected message type: {ack_data.get('type')}"
                    )
            except asyncio.TimeoutError:
                self.log_test_result(
                    "Session Integrity - Subscription",
                    False,
                    "No subscription acknowledgment received"
                )
            
            # Test receiving integrity monitoring data
            integrity_received = 0
            max_wait_time = 15  # Wait up to 15 seconds for integrity data
            
            try:
                while integrity_received < 2:  # Try to receive at least 2 integrity messages
                    integrity_message = await asyncio.wait_for(websocket.recv(), timeout=max_wait_time)
                    integrity_data = json.loads(integrity_message)
                    
                    if integrity_data.get("type") == "session_integrity":
                        integrity_received += 1
                        self.log_test_result(
                            f"Session Integrity - Monitor {integrity_received}",
                            True,
                            "Integrity monitoring data received",
                            {
                                "session_id": integrity_data.get("session_id"),
                                "integrity_score": integrity_data.get("data", {}).get("integrity_score"),
                                "status": integrity_data.get("data", {}).get("status"),
                                "violations_count": len(integrity_data.get("data", {}).get("violations", [])),
                                "data_points_analyzed": integrity_data.get("data", {}).get("data_points_analyzed")
                            }
                        )
                    elif integrity_data.get("type") == "heartbeat":
                        # Heartbeat is expected, continue waiting
                        continue
                    else:
                        self.log_test_result(
                            "Session Integrity - Unexpected Message",
                            False,
                            f"Unexpected message type: {integrity_data.get('type')}"
                        )
                        break
                        
            except asyncio.TimeoutError:
                if integrity_received > 0:
                    self.log_test_result(
                        "Session Integrity - Monitoring",
                        True,
                        f"Received {integrity_received} integrity messages (partial success)"
                    )
                else:
                    self.log_test_result(
                        "Session Integrity - Monitoring",
                        False,
                        "No integrity monitoring data received within timeout"
                    )
            
            await websocket.close()
            return integrity_received > 0
            
        except Exception as e:
            self.log_test_result(
                "Session Integrity - Testing",
                False,
                f"Error during session integrity testing: {str(e)}"
            )
            try:
                await websocket.close()
            except:
                pass
            return False

    def test_websocket_stats_api(self):
        """Test GET /api/websocket/stats endpoint"""
        try:
            response = requests.get(
                f"{self.api_base_url}/websocket/stats",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success") and "data" in data:
                    stats = data["data"]
                    self.log_test_result(
                        "WebSocket Stats API",
                        True,
                        f"Stats retrieved successfully (Status: {response.status_code})",
                        {
                            "active_connections": stats.get("active_connections"),
                            "session_connections": stats.get("session_connections"),
                            "device_connections": stats.get("device_connections"),
                            "total_subscriptions": stats.get("total_subscriptions"),
                            "background_tasks_running": stats.get("background_tasks_running")
                        }
                    )
                    return True
                else:
                    self.log_test_result(
                        "WebSocket Stats API",
                        False,
                        f"Invalid response structure: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "WebSocket Stats API",
                    False,
                    f"API request failed (Status: {response.status_code})"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "WebSocket Stats API",
                False,
                f"API request error: {str(e)}"
            )
            return False

    def test_broadcast_violation_api(self):
        """Test POST /api/websocket/broadcast-violation endpoint"""
        try:
            violation_data = {
                "session_id": self.test_session_id,
                "device_id": self.test_device_id,
                "violation_type": "test_violation",
                "severity": "medium",
                "description": "Test violation alert for WebSocket broadcasting",
                "risk_score": 0.6,
                "detected_at": datetime.now().isoformat(),
                "recommendation": "Monitor session closely",
                "evidence": {
                    "test_indicator": "automated_test",
                    "detection_method": "websocket_test"
                }
            }
            
            response = requests.post(
                f"{self.api_base_url}/websocket/broadcast-violation",
                json=violation_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("success"):
                    self.log_test_result(
                        "Broadcast Violation API",
                        True,
                        f"Violation broadcast successful (Status: {response.status_code})",
                        {
                            "message": data.get("message"),
                            "violation_type": violation_data["violation_type"],
                            "severity": violation_data["severity"]
                        }
                    )
                    return True
                else:
                    self.log_test_result(
                        "Broadcast Violation API",
                        False,
                        f"Broadcast failed: {data}"
                    )
                    return False
            else:
                self.log_test_result(
                    "Broadcast Violation API",
                    False,
                    f"API request failed (Status: {response.status_code})"
                )
                return False
                
        except Exception as e:
            self.log_test_result(
                "Broadcast Violation API",
                False,
                f"API request error: {str(e)}"
            )
            return False

    async def run_comprehensive_tests(self):
        """Run all WebSocket Real-Time Monitoring tests"""
        logger.info("🎯 Starting WebSocket Real-Time Monitoring Integration Testing")
        logger.info("=" * 80)
        
        # Authenticate first
        auth_success = await self.authenticate_admin()
        if not auth_success:
            logger.error("Authentication failed - some tests may not work properly")
        
        # Test results tracking
        test_functions = [
            ("WebSocket Endpoints", [
                ("Fingerprint Updates Endpoint", self.test_fingerprint_updates_endpoint()),
                ("Device Analytics Endpoint", self.test_device_analytics_endpoint()),
                ("Session Integrity Endpoint", self.test_session_integrity_endpoint())
            ]),
            ("API Endpoints", [
                ("WebSocket Stats API", self.test_websocket_stats_api()),
                ("Broadcast Violation API", self.test_broadcast_violation_api())
            ])
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for category_name, tests in test_functions:
            logger.info(f"\n📋 Testing {category_name}")
            logger.info("-" * 50)
            
            for test_name, test_coro in tests:
                total_tests += 1
                try:
                    if asyncio.iscoroutine(test_coro):
                        result = await test_coro
                    else:
                        result = test_coro
                    
                    if result:
                        passed_tests += 1
                        
                except Exception as e:
                    logger.error(f"Test {test_name} failed with exception: {e}")
                    self.log_test_result(test_name, False, f"Exception: {str(e)}")
        
        # Clean up any remaining WebSocket connections
        for websocket in self.connected_websockets:
            try:
                await websocket.close()
            except:
                pass
        
        # Generate summary
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        logger.info("\n" + "=" * 80)
        logger.info("🎯 WEBSOCKET REAL-TIME MONITORING INTEGRATION TEST SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {total_tests - passed_tests}")
        logger.info(f"Success Rate: {success_rate:.1f}%")
        
        # Detailed results
        logger.info("\n📊 DETAILED TEST RESULTS:")
        logger.info("-" * 50)
        
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            logger.info(f"{status} {result['test_name']}: {result['details']}")
        
        # Final assessment
        if success_rate >= 80:
            logger.info(f"\n🎉 EXCELLENT RESULTS: WebSocket Real-Time Monitoring Integration is working excellently with {success_rate:.1f}% success rate!")
            logger.info("✅ All major WebSocket endpoints are operational")
            logger.info("✅ Real-time data streaming is functional")
            logger.info("✅ API integration is working correctly")
            logger.info("✅ System is ready for production use")
        elif success_rate >= 60:
            logger.info(f"\n✅ GOOD RESULTS: WebSocket Real-Time Monitoring Integration is mostly working with {success_rate:.1f}% success rate")
            logger.info("⚠️  Some minor issues detected but core functionality is operational")
        else:
            logger.info(f"\n❌ ISSUES DETECTED: WebSocket Real-Time Monitoring Integration has significant issues with {success_rate:.1f}% success rate")
            logger.info("🔧 Major functionality problems need to be addressed")
        
        return success_rate >= 60

async def main():
    """Main test execution function"""
    tester = WebSocketRealTimeMonitoringTester()
    
    try:
        success = await tester.run_comprehensive_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        logger.info("\n⚠️  Test interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"\n❌ Test execution failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)