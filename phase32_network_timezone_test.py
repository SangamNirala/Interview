#!/usr/bin/env python3
"""
🎯 PHASE 3.2: ADVANCED BROWSER & ENVIRONMENT ANALYSIS TESTING - REMAINING 2 METHODS
Comprehensive testing of Network Characteristics Analysis and Timezone Consistency Analysis endpoints

Test Coverage:
1. Network Characteristics Analysis (POST /api/session-fingerprinting/monitor-network-characteristics)
2. Timezone Consistency Analysis (POST /api/session-fingerprinting/track-timezone-consistency)

Testing Scenarios:
- Normal residential IPs vs VPN/Proxy detection
- Various network configurations and ISP information
- Normal timezone consistency vs timezone mismatches
- System vs browser timezone validation
- Edge cases with malformed data
"""

import requests
import json
import uuid
from datetime import datetime
import time

# Configuration
BACKEND_URL = "https://security-keystroke.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class Phase32NetworkTimezoneTester:
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
                data = response.json()
                if data.get('success'):
                    self.log_result("Admin Authentication", True, f"Successfully authenticated (Status: {response.status_code})")
                    return True
                else:
                    self.log_result("Admin Authentication", False, f"Authentication failed: {data}")
                    return False
            else:
                self.log_result("Admin Authentication", False, f"Authentication failed (Status: {response.status_code}): {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Admin Authentication", False, f"Authentication error: {str(e)}")
            return False

    def test_network_characteristics_normal_residential(self):
        """Test network characteristics analysis with normal residential IP"""
        try:
            # Normal residential network data
            network_data = {
                "ip_address": "192.168.1.100",
                "public_ip": "203.0.113.45",
                "isp_info": {
                    "name": "Comcast Cable Communications",
                    "organization": "Comcast",
                    "country": "United States",
                    "region": "California",
                    "city": "San Francisco",
                    "timezone": "America/Los_Angeles",
                    "connection_type": "cable"
                },
                "geolocation": {
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "accuracy": 50,
                    "country": "US",
                    "region": "CA",
                    "city": "San Francisco"
                },
                "network_performance": {
                    "download_speed": 150.5,
                    "upload_speed": 25.3,
                    "latency": 15,
                    "jitter": 2.1,
                    "packet_loss": 0.1
                },
                "routing_info": {
                    "hop_count": 12,
                    "route_consistency": True,
                    "autonomous_system": "AS7922",
                    "bgp_prefix": "203.0.113.0/24"
                },
                "connection_metadata": {
                    "connection_type": "ethernet",
                    "effective_type": "4g",
                    "downlink": 10,
                    "rtt": 50
                }
            }
            
            payload = {
                "session_id": self.session_id + "_normal_network",
                "network_data": network_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/monitor-network-characteristics",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('network_analysis', {})
                    self.log_result(
                        "Network Analysis - Normal Residential IP", 
                        True, 
                        f"Normal residential network analysis completed. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Network Analysis - Normal Residential IP", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Network Analysis - Normal Residential IP", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Network Analysis - Normal Residential IP", False, f"Exception: {str(e)}")
            return False

    def test_network_characteristics_vpn_proxy_detection(self):
        """Test network characteristics analysis with VPN/Proxy detection"""
        try:
            # VPN/Proxy network data with suspicious characteristics
            network_data = {
                "ip_address": "10.0.0.1",
                "public_ip": "185.220.101.45",  # Known Tor exit node range
                "isp_info": {
                    "name": "DigitalOcean LLC",
                    "organization": "DigitalOcean",
                    "country": "Netherlands",
                    "region": "North Holland",
                    "city": "Amsterdam",
                    "timezone": "Europe/Amsterdam",
                    "connection_type": "datacenter"
                },
                "geolocation": {
                    "latitude": 52.3676,
                    "longitude": 4.9041,
                    "accuracy": 1000,  # Low accuracy indicates VPN
                    "country": "NL",
                    "region": "NH",
                    "city": "Amsterdam"
                },
                "network_performance": {
                    "download_speed": 500.0,  # Very high speed (datacenter)
                    "upload_speed": 500.0,
                    "latency": 150,  # High latency for location
                    "jitter": 15.5,
                    "packet_loss": 0.0
                },
                "routing_info": {
                    "hop_count": 8,  # Fewer hops than expected
                    "route_consistency": False,
                    "autonomous_system": "AS14061",  # DigitalOcean AS
                    "bgp_prefix": "185.220.101.0/24"
                },
                "connection_metadata": {
                    "connection_type": "ethernet",
                    "effective_type": "4g",
                    "downlink": 10,
                    "rtt": 150
                },
                "proxy_indicators": {
                    "tor_exit_node": True,
                    "known_vpn_provider": True,
                    "datacenter_ip": True,
                    "proxy_headers": ["X-Forwarded-For", "X-Real-IP"]
                }
            }
            
            payload = {
                "session_id": self.session_id + "_vpn_proxy_session",
                "network_data": network_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/monitor-network-characteristics",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('network_analysis', {})
                    self.log_result(
                        "Network Analysis - VPN/Proxy Detection", 
                        True, 
                        f"VPN/Proxy network analysis completed. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Network Analysis - VPN/Proxy Detection", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Network Analysis - VPN/Proxy Detection", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Network Analysis - VPN/Proxy Detection", False, f"Exception: {str(e)}")
            return False

    def test_network_characteristics_datacenter_ip(self):
        """Test network characteristics analysis with datacenter IP"""
        try:
            # Datacenter IP network data
            network_data = {
                "ip_address": "172.16.0.1",
                "public_ip": "104.248.123.45",  # DigitalOcean IP range
                "isp_info": {
                    "name": "DigitalOcean LLC",
                    "organization": "DigitalOcean",
                    "country": "United States",
                    "region": "New York",
                    "city": "New York",
                    "timezone": "America/New_York",
                    "connection_type": "datacenter"
                },
                "geolocation": {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "accuracy": 10,
                    "country": "US",
                    "region": "NY",
                    "city": "New York"
                },
                "network_performance": {
                    "download_speed": 1000.0,  # Very high datacenter speed
                    "upload_speed": 1000.0,
                    "latency": 5,  # Very low latency
                    "jitter": 0.5,
                    "packet_loss": 0.0
                },
                "routing_info": {
                    "hop_count": 6,
                    "route_consistency": True,
                    "autonomous_system": "AS14061",
                    "bgp_prefix": "104.248.0.0/16"
                },
                "connection_metadata": {
                    "connection_type": "ethernet",
                    "effective_type": "4g",
                    "downlink": 10,
                    "rtt": 5
                },
                "datacenter_indicators": {
                    "is_datacenter": True,
                    "cloud_provider": "DigitalOcean",
                    "server_grade_connection": True
                }
            }
            
            payload = {
                "session_id": self.session_id + "_datacenter_session",
                "network_data": network_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/monitor-network-characteristics",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('network_analysis', {})
                    self.log_result(
                        "Network Analysis - Datacenter IP", 
                        True, 
                        f"Datacenter IP analysis completed. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Network Analysis - Datacenter IP", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Network Analysis - Datacenter IP", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Network Analysis - Datacenter IP", False, f"Exception: {str(e)}")
            return False

    def test_timezone_consistency_normal(self):
        """Test timezone consistency analysis with normal consistent timezone data"""
        try:
            # Normal consistent timezone data
            timezone_data = {
                "system_timezone": "America/New_York",
                "browser_timezone": "America/New_York",
                "timezone_offset": -300,  # EST offset in minutes
                "dst_active": False,
                "geolocation_timezone": "America/New_York",
                "ip_timezone": "America/New_York",
                "system_time": "2024-01-15T14:30:00-05:00",
                "browser_time": "2024-01-15T14:30:00-05:00",
                "server_time": "2024-01-15T19:30:00Z",
                "time_sync_accuracy": {
                    "ntp_synchronized": True,
                    "time_drift": 0.05,  # seconds
                    "last_sync": "2024-01-15T14:25:00-05:00"
                },
                "geolocation_data": {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "accuracy": 50,
                    "country": "US",
                    "region": "NY",
                    "city": "New York"
                },
                "user_behavior": {
                    "active_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17],
                    "typical_timezone": "America/New_York",
                    "session_start_time": "2024-01-15T14:30:00-05:00"
                }
            }
            
            payload = {
                "session_id": self.session_id + "_normal_timezone",
                "timezone_data": timezone_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-timezone-consistency",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('timezone_analysis', {})
                    self.log_result(
                        "Timezone Analysis - Normal Consistency", 
                        True, 
                        f"Normal timezone consistency analysis completed. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Timezone Analysis - Normal Consistency", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Timezone Analysis - Normal Consistency", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Timezone Analysis - Normal Consistency", False, f"Exception: {str(e)}")
            return False

    def test_timezone_consistency_mismatch(self):
        """Test timezone consistency analysis with timezone mismatches"""
        try:
            # Timezone data with mismatches (potential manipulation)
            timezone_data = {
                "system_timezone": "America/Los_Angeles",  # West Coast
                "browser_timezone": "America/New_York",   # East Coast - mismatch!
                "timezone_offset": -480,  # PST offset but browser says EST
                "dst_active": False,
                "geolocation_timezone": "Europe/London",  # Different continent - major mismatch!
                "ip_timezone": "Asia/Tokyo",              # Another continent - major mismatch!
                "system_time": "2024-01-15T11:30:00-08:00",  # PST
                "browser_time": "2024-01-15T14:30:00-05:00", # EST - 3 hour difference
                "server_time": "2024-01-15T19:30:00Z",
                "time_sync_accuracy": {
                    "ntp_synchronized": False,  # Not synchronized
                    "time_drift": 15.5,  # Large drift
                    "last_sync": "2024-01-10T10:00:00-08:00"  # Old sync
                },
                "geolocation_data": {
                    "latitude": 51.5074,   # London coordinates
                    "longitude": -0.1278,
                    "accuracy": 1000,      # Low accuracy
                    "country": "GB",
                    "region": "England",
                    "city": "London"
                },
                "user_behavior": {
                    "active_hours": [2, 3, 4, 5, 6, 7, 8, 9, 10],  # Unusual hours for claimed timezone
                    "typical_timezone": "America/Los_Angeles",
                    "session_start_time": "2024-01-15T11:30:00-08:00"
                },
                "manipulation_indicators": {
                    "timezone_spoofing": True,
                    "geolocation_spoofing": True,
                    "time_manipulation": True,
                    "vpn_usage": True
                }
            }
            
            payload = {
                "session_id": self.session_id + "_timezone_mismatch",
                "timezone_data": timezone_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-timezone-consistency",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('timezone_analysis', {})
                    self.log_result(
                        "Timezone Analysis - Timezone Mismatches", 
                        True, 
                        f"Timezone mismatch analysis completed. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Timezone Analysis - Timezone Mismatches", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Timezone Analysis - Timezone Mismatches", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Timezone Analysis - Timezone Mismatches", False, f"Exception: {str(e)}")
            return False

    def test_timezone_consistency_dst_handling(self):
        """Test timezone consistency analysis with DST handling"""
        try:
            # Timezone data during DST transition
            timezone_data = {
                "system_timezone": "America/New_York",
                "browser_timezone": "America/New_York",
                "timezone_offset": -240,  # EDT offset (DST active)
                "dst_active": True,
                "geolocation_timezone": "America/New_York",
                "ip_timezone": "America/New_York",
                "system_time": "2024-07-15T15:30:00-04:00",  # EDT
                "browser_time": "2024-07-15T15:30:00-04:00",
                "server_time": "2024-07-15T19:30:00Z",
                "time_sync_accuracy": {
                    "ntp_synchronized": True,
                    "time_drift": 0.1,
                    "last_sync": "2024-07-15T15:25:00-04:00"
                },
                "geolocation_data": {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "accuracy": 25,
                    "country": "US",
                    "region": "NY",
                    "city": "New York"
                },
                "user_behavior": {
                    "active_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17],
                    "typical_timezone": "America/New_York",
                    "session_start_time": "2024-07-15T15:30:00-04:00"
                },
                "dst_info": {
                    "dst_start": "2024-03-10T02:00:00-05:00",
                    "dst_end": "2024-11-03T02:00:00-04:00",
                    "dst_offset": 60,  # 1 hour
                    "dst_transition_handling": "automatic"
                }
            }
            
            payload = {
                "session_id": self.session_id + "_dst_timezone",
                "timezone_data": timezone_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-timezone-consistency",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('timezone_analysis', {})
                    self.log_result(
                        "Timezone Analysis - DST Handling", 
                        True, 
                        f"DST timezone analysis completed. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Timezone Analysis - DST Handling", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Timezone Analysis - DST Handling", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Timezone Analysis - DST Handling", False, f"Exception: {str(e)}")
            return False

    def test_network_characteristics_edge_cases(self):
        """Test network characteristics analysis with malformed/edge case data"""
        try:
            # Malformed network data
            network_data = {
                "ip_address": "invalid_ip",
                "public_ip": None,
                "isp_info": {},
                "geolocation": {
                    "latitude": "invalid_lat",
                    "longitude": None
                },
                "network_performance": {
                    "download_speed": -1,  # Invalid negative speed
                    "latency": "high"      # String instead of number
                },
                "routing_info": None
            }
            
            payload = {
                "session_id": self.session_id + "_edge_case_network",
                "network_data": network_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/monitor-network-characteristics",
                json=payload
            )
            
            # Should handle gracefully (either 200 with error handling or 400 with validation error)
            if response.status_code in [200, 400, 422]:
                self.log_result(
                    "Network Analysis - Edge Cases", 
                    True, 
                    f"Edge case handling working correctly (Status: {response.status_code})"
                )
                return True
            else:
                self.log_result("Network Analysis - Edge Cases", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Network Analysis - Edge Cases", False, f"Exception: {str(e)}")
            return False

    def test_timezone_consistency_edge_cases(self):
        """Test timezone consistency analysis with malformed/edge case data"""
        try:
            # Malformed timezone data
            timezone_data = {
                "system_timezone": "Invalid/Timezone",
                "browser_timezone": None,
                "timezone_offset": "not_a_number",
                "dst_active": "maybe",  # Invalid boolean
                "geolocation_timezone": 12345,  # Number instead of string
                "system_time": "not_a_date",
                "browser_time": None,
                "geolocation_data": "invalid_object"
            }
            
            payload = {
                "session_id": self.session_id + "_edge_case_timezone",
                "timezone_data": timezone_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/track-timezone-consistency",
                json=payload
            )
            
            # Should handle gracefully (either 200 with error handling or 400 with validation error)
            if response.status_code in [200, 400, 422]:
                self.log_result(
                    "Timezone Analysis - Edge Cases", 
                    True, 
                    f"Edge case handling working correctly (Status: {response.status_code})"
                )
                return True
            else:
                self.log_result("Timezone Analysis - Edge Cases", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Timezone Analysis - Edge Cases", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all network and timezone analysis tests"""
        print("🎯 PHASE 3.2: ADVANCED BROWSER & ENVIRONMENT ANALYSIS - REMAINING 2 METHODS TESTING")
        print("=" * 90)
        print("Testing Network Characteristics Analysis and Timezone Consistency Analysis endpoints")
        print("=" * 90)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return 0, 0
        
        # Run all tests
        tests = [
            self.test_network_characteristics_normal_residential,
            self.test_network_characteristics_vpn_proxy_detection,
            self.test_network_characteristics_datacenter_ip,
            self.test_timezone_consistency_normal,
            self.test_timezone_consistency_mismatch,
            self.test_timezone_consistency_dst_handling,
            self.test_network_characteristics_edge_cases,
            self.test_timezone_consistency_edge_cases
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        # Print summary
        print("\n" + "=" * 90)
        print("🎯 PHASE 3.2 REMAINING 2 METHODS TESTING SUMMARY")
        print("=" * 90)
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
    tester = Phase32NetworkTimezoneTester()
    passed, total = tester.run_all_tests()
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! Phase 3.2 remaining 2 methods functionality is working perfectly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the results above.")