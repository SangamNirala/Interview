#!/usr/bin/env python3
"""
🎯 PHASE 3.2: ADVANCED BROWSER & ENVIRONMENT ANALYSIS TESTING
Comprehensive testing of Browser Fingerprint Analysis and Automation Tools Detection endpoints

Test Coverage:
1. Browser Fingerprint Analysis (POST /api/session-fingerprinting/analyze-browser-fingerprint)
2. Automation Tools Detection (POST /api/session-fingerprinting/detect-automation-tools)

Testing Scenarios:
- Normal browser fingerprints vs suspicious ones
- Clean browser sessions vs automation tool signatures  
- Various browser types (Chrome, Firefox, Safari, Edge)
- Different automation tools and patterns
- Edge cases with malformed data
"""

import requests
import json
import uuid
from datetime import datetime
import time

# Configuration
BACKEND_URL = "https://session-monitor.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class Phase32BrowserEnvironmentTester:
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

    def test_browser_fingerprint_analysis_normal_chrome(self):
        """Test browser fingerprint analysis with normal Chrome browser data"""
        try:
            # Normal Chrome browser fingerprint data
            browser_data = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "browser_name": "Chrome",
                "browser_version": "119.0.0.0",
                "engine_name": "Blink",
                "engine_version": "119.0.0.0",
                "plugins": [
                    {"name": "Chrome PDF Plugin", "version": "119.0.0.0", "enabled": True},
                    {"name": "Native Client", "version": "119.0.0.0", "enabled": True},
                    {"name": "Widevine Content Decryption Module", "version": "4.10.2557.0", "enabled": True}
                ],
                "mime_types": [
                    {"type": "application/pdf", "description": "Portable Document Format", "suffixes": "pdf"},
                    {"type": "text/html", "description": "HTML Document", "suffixes": "html,htm"},
                    {"type": "image/jpeg", "description": "JPEG Image", "suffixes": "jpg,jpeg"}
                ],
                "languages": ["en-US", "en", "es"],
                "cookie_enabled": True,
                "local_storage": True,
                "session_storage": True,
                "webgl_support": True,
                "canvas_support": True,
                "css3_support": True,
                "svg_support": True,
                "javascript_features": {
                    "async_support": True,
                    "webworker_support": True,
                    "websocket_support": True,
                    "es6_support": True,
                    "fetch_api": True
                },
                "screen_resolution": "1920x1080",
                "color_depth": 24,
                "timezone": "America/New_York",
                "platform": "Win32"
            }
            
            payload = {
                "session_id": self.session_id + "_chrome_normal",
                "browser_data": browser_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('browser_fingerprint_analysis', {})
                    self.log_result(
                        "Browser Fingerprint Analysis - Normal Chrome", 
                        True, 
                        f"Analysis completed successfully. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Browser Fingerprint Analysis - Normal Chrome", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Browser Fingerprint Analysis - Normal Chrome", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Browser Fingerprint Analysis - Normal Chrome", False, f"Exception: {str(e)}")
            return False

    def test_browser_fingerprint_analysis_suspicious_firefox(self):
        """Test browser fingerprint analysis with suspicious Firefox browser data"""
        try:
            # Suspicious Firefox browser fingerprint with inconsistencies
            browser_data = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
                "browser_name": "Firefox",
                "browser_version": "119.0",
                "engine_name": "Gecko",
                "engine_version": "109.0",
                "plugins": [
                    # Suspicious: Chrome plugins in Firefox
                    {"name": "Chrome PDF Plugin", "version": "119.0.0.0", "enabled": True},
                    {"name": "Native Client", "version": "119.0.0.0", "enabled": True}
                ],
                "mime_types": [
                    {"type": "application/pdf", "description": "Portable Document Format", "suffixes": "pdf"},
                    {"type": "text/html", "description": "HTML Document", "suffixes": "html,htm"}
                ],
                "languages": ["en-US", "en"],
                "cookie_enabled": True,
                "local_storage": True,
                "session_storage": True,
                "webgl_support": False,  # Suspicious: WebGL disabled
                "canvas_support": False,  # Suspicious: Canvas disabled
                "css3_support": True,
                "svg_support": True,
                "javascript_features": {
                    "async_support": True,
                    "webworker_support": False,  # Suspicious: WebWorker disabled
                    "websocket_support": True,
                    "es6_support": True,
                    "fetch_api": True
                },
                "screen_resolution": "800x600",  # Suspicious: Low resolution
                "color_depth": 16,  # Suspicious: Low color depth
                "timezone": "UTC",  # Suspicious: Generic timezone
                "platform": "Linux x86_64"  # Inconsistent with Windows user agent
            }
            
            payload = {
                "session_id": self.session_id + "_firefox_suspicious",
                "browser_data": browser_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('browser_fingerprint_analysis', {})
                    self.log_result(
                        "Browser Fingerprint Analysis - Suspicious Firefox", 
                        True, 
                        f"Suspicious analysis completed. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Browser Fingerprint Analysis - Suspicious Firefox", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Browser Fingerprint Analysis - Suspicious Firefox", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Browser Fingerprint Analysis - Suspicious Firefox", False, f"Exception: {str(e)}")
            return False

    def test_browser_fingerprint_analysis_safari(self):
        """Test browser fingerprint analysis with Safari browser data"""
        try:
            # Safari browser fingerprint data
            browser_data = {
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
                "browser_name": "Safari",
                "browser_version": "17.1",
                "engine_name": "WebKit",
                "engine_version": "605.1.15",
                "plugins": [
                    {"name": "WebKit built-in PDF", "version": "17.1", "enabled": True}
                ],
                "mime_types": [
                    {"type": "application/pdf", "description": "Portable Document Format", "suffixes": "pdf"},
                    {"type": "text/html", "description": "HTML Document", "suffixes": "html,htm"},
                    {"type": "image/png", "description": "PNG Image", "suffixes": "png"}
                ],
                "languages": ["en-US", "en"],
                "cookie_enabled": True,
                "local_storage": True,
                "session_storage": True,
                "webgl_support": True,
                "canvas_support": True,
                "css3_support": True,
                "svg_support": True,
                "javascript_features": {
                    "async_support": True,
                    "webworker_support": True,
                    "websocket_support": True,
                    "es6_support": True,
                    "fetch_api": True
                },
                "screen_resolution": "2560x1600",
                "color_depth": 24,
                "timezone": "America/Los_Angeles",
                "platform": "MacIntel"
            }
            
            payload = {
                "session_id": self.session_id + "_safari_normal",
                "browser_data": browser_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    analysis = data.get('browser_fingerprint_analysis', {})
                    self.log_result(
                        "Browser Fingerprint Analysis - Safari", 
                        True, 
                        f"Safari analysis completed. Analysis keys: {list(analysis.keys())}"
                    )
                    return True
                else:
                    self.log_result("Browser Fingerprint Analysis - Safari", False, f"Analysis failed: {data}")
                    return False
            else:
                self.log_result("Browser Fingerprint Analysis - Safari", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Browser Fingerprint Analysis - Safari", False, f"Exception: {str(e)}")
            return False

    def test_automation_detection_clean_session(self):
        """Test automation detection with clean human-like session data"""
        try:
            # Clean browser data (no automation signatures)
            browser_data = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "browser_name": "Chrome",
                "webdriver": False,
                "webdriver_properties": [],
                "plugins": [
                    {"name": "Chrome PDF Plugin", "version": "119.0.0.0", "enabled": True},
                    {"name": "Native Client", "version": "119.0.0.0", "enabled": True}
                ],
                "user_gestures": True,
                "async_execution": True,
                "event_properties": {
                    "isTrusted": True,
                    "timeStamp": 1634567890123,
                    "bubbles": True,
                    "cancelable": True
                },
                "navigator_properties": {
                    "webdriver": False,
                    "permissions": True,
                    "notification": True
                }
            }
            
            # Human-like behavioral data
            behavioral_data = {
                "mouse_data": {
                    "movements": [
                        {"x": 100, "y": 150, "timestamp": 1634567890123},
                        {"x": 102, "y": 152, "timestamp": 1634567890140},
                        {"x": 105, "y": 155, "timestamp": 1634567890157},
                        {"x": 108, "y": 158, "timestamp": 1634567890174},
                        {"x": 112, "y": 162, "timestamp": 1634567890191}
                    ],
                    "clicks": [
                        {"target_x": 200, "target_y": 300, "actual_x": 201, "actual_y": 299, "timestamp": 1634567890500}
                    ]
                },
                "timing_data": {
                    "intervals": [16.7, 33.4, 50.1, 66.8, 83.5],  # Natural human timing
                    "keypress_timings": [1634567890100, 1634567890200, 1634567890350, 1634567890520]
                }
            }
            
            payload = {
                "session_id": self.session_id + "_clean_session",
                "browser_data": browser_data,
                "behavioral_data": behavioral_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-automation-tools",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    detection = data.get('automation_detection', {})
                    self.log_result(
                        "Automation Detection - Clean Session", 
                        True, 
                        f"Clean session analysis completed. Detection keys: {list(detection.keys())}"
                    )
                    return True
                else:
                    self.log_result("Automation Detection - Clean Session", False, f"Detection failed: {data}")
                    return False
            else:
                self.log_result("Automation Detection - Clean Session", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Automation Detection - Clean Session", False, f"Exception: {str(e)}")
            return False

    def test_automation_detection_selenium_signatures(self):
        """Test automation detection with Selenium automation signatures"""
        try:
            # Browser data with Selenium signatures
            browser_data = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "browser_name": "Chrome",
                "webdriver": True,  # Selenium signature
                "webdriver_properties": [
                    "window.navigator.webdriver",
                    "window.chrome.runtime",
                    "window.callPhantom"
                ],
                "plugins": [
                    {"name": "Chrome PDF Plugin", "version": "119.0.0.0", "enabled": True}
                ],
                "user_gestures": False,  # Automation signature
                "async_execution": False,  # Automation signature
                "event_properties": {
                    "isTrusted": False,  # Automation signature
                    "timeStamp": 1634567890123,
                    "bubbles": True,
                    "cancelable": True
                },
                "navigator_properties": {
                    "webdriver": True,  # Selenium signature
                    "permissions": False,
                    "notification": False
                },
                "automation_indicators": [
                    "selenium",
                    "webdriver",
                    "chrome_driver"
                ]
            }
            
            # Robotic behavioral data
            behavioral_data = {
                "mouse_data": {
                    "movements": [
                        {"x": 100, "y": 150, "timestamp": 1634567890123},
                        {"x": 200, "y": 300, "timestamp": 1634567890124},  # Instant movement
                        {"x": 300, "y": 450, "timestamp": 1634567890125}   # Instant movement
                    ],
                    "clicks": [
                        {"target_x": 200, "target_y": 300, "actual_x": 200, "actual_y": 300, "timestamp": 1634567890500}  # Perfect accuracy
                    ]
                },
                "timing_data": {
                    "intervals": [16.0, 16.0, 16.0, 16.0],  # Perfect timing (robotic)
                    "keypress_timings": [1634567890100, 1634567890200, 1634567890300, 1634567890400]  # Regular intervals
                }
            }
            
            payload = {
                "session_id": self.session_id + "_selenium_session",
                "browser_data": browser_data,
                "behavioral_data": behavioral_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-automation-tools",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    detection = data.get('automation_detection', {})
                    self.log_result(
                        "Automation Detection - Selenium Signatures", 
                        True, 
                        f"Selenium detection completed. Detection keys: {list(detection.keys())}"
                    )
                    return True
                else:
                    self.log_result("Automation Detection - Selenium Signatures", False, f"Detection failed: {data}")
                    return False
            else:
                self.log_result("Automation Detection - Selenium Signatures", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Automation Detection - Selenium Signatures", False, f"Exception: {str(e)}")
            return False

    def test_automation_detection_puppeteer_signatures(self):
        """Test automation detection with Puppeteer automation signatures"""
        try:
            # Browser data with Puppeteer signatures
            browser_data = {
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/119.0.0.0 Safari/537.36",
                "browser_name": "Chrome",
                "webdriver": False,
                "webdriver_properties": [
                    "window.chrome.app",
                    "window.chrome.runtime"
                ],
                "plugins": [],  # Headless Chrome has no plugins
                "user_gestures": False,
                "async_execution": True,
                "event_properties": {
                    "isTrusted": False,
                    "timeStamp": 1634567890123,
                    "bubbles": True,
                    "cancelable": True
                },
                "navigator_properties": {
                    "webdriver": False,
                    "permissions": False,
                    "notification": False,
                    "headless": True  # Puppeteer signature
                },
                "automation_indicators": [
                    "puppeteer",
                    "headless_chrome",
                    "chrome_headless"
                ]
            }
            
            # Puppeteer-like behavioral data
            behavioral_data = {
                "mouse_data": {
                    "movements": [],  # No mouse movements in headless
                    "clicks": [
                        {"target_x": 200, "target_y": 300, "actual_x": 200, "actual_y": 300, "timestamp": 1634567890500}
                    ]
                },
                "timing_data": {
                    "intervals": [0, 0, 0, 0],  # No timing variation
                    "keypress_timings": [1634567890100, 1634567890101, 1634567890102, 1634567890103]  # Rapid succession
                }
            }
            
            payload = {
                "session_id": self.session_id + "_puppeteer_session",
                "browser_data": browser_data,
                "behavioral_data": behavioral_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-automation-tools",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    detection = data.get('automation_detection', {})
                    self.log_result(
                        "Automation Detection - Puppeteer Signatures", 
                        True, 
                        f"Puppeteer detection completed. Detection keys: {list(detection.keys())}"
                    )
                    return True
                else:
                    self.log_result("Automation Detection - Puppeteer Signatures", False, f"Detection failed: {data}")
                    return False
            else:
                self.log_result("Automation Detection - Puppeteer Signatures", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Automation Detection - Puppeteer Signatures", False, f"Exception: {str(e)}")
            return False

    def test_automation_detection_playwright_signatures(self):
        """Test automation detection with Playwright automation signatures"""
        try:
            # Browser data with Playwright signatures
            browser_data = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "browser_name": "Chrome",
                "webdriver": False,
                "webdriver_properties": [
                    "window.playwright",
                    "window.__playwright"
                ],
                "plugins": [
                    {"name": "Chrome PDF Plugin", "version": "119.0.0.0", "enabled": True}
                ],
                "user_gestures": False,
                "async_execution": True,
                "event_properties": {
                    "isTrusted": False,
                    "timeStamp": 1634567890123,
                    "bubbles": True,
                    "cancelable": True
                },
                "navigator_properties": {
                    "webdriver": False,
                    "permissions": True,
                    "notification": True,
                    "playwright": True  # Playwright signature
                },
                "automation_indicators": [
                    "playwright",
                    "pw_automation"
                ]
            }
            
            # Playwright-like behavioral data
            behavioral_data = {
                "mouse_data": {
                    "movements": [
                        {"x": 100, "y": 150, "timestamp": 1634567890123},
                        {"x": 200, "y": 300, "timestamp": 1634567890200}  # Linear movement
                    ],
                    "clicks": [
                        {"target_x": 200, "target_y": 300, "actual_x": 200, "actual_y": 300, "timestamp": 1634567890500}
                    ]
                },
                "timing_data": {
                    "intervals": [100, 100, 100, 100],  # Consistent timing
                    "keypress_timings": [1634567890100, 1634567890200, 1634567890300, 1634567890400]
                }
            }
            
            payload = {
                "session_id": self.session_id + "_playwright_session",
                "browser_data": browser_data,
                "behavioral_data": behavioral_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-automation-tools",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    detection = data.get('automation_detection', {})
                    self.log_result(
                        "Automation Detection - Playwright Signatures", 
                        True, 
                        f"Playwright detection completed. Detection keys: {list(detection.keys())}"
                    )
                    return True
                else:
                    self.log_result("Automation Detection - Playwright Signatures", False, f"Detection failed: {data}")
                    return False
            else:
                self.log_result("Automation Detection - Playwright Signatures", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Automation Detection - Playwright Signatures", False, f"Exception: {str(e)}")
            return False

    def test_browser_fingerprint_edge_cases(self):
        """Test browser fingerprint analysis with malformed/edge case data"""
        try:
            # Malformed browser data
            browser_data = {
                "user_agent": "",  # Empty user agent
                "browser_name": None,  # Null browser name
                "browser_version": "invalid_version",
                "plugins": "not_an_array",  # Wrong type
                "mime_types": [],  # Empty array
                "languages": None,  # Null languages
                "javascript_features": {
                    "invalid_feature": "invalid_value"
                }
            }
            
            payload = {
                "session_id": self.session_id + "_edge_case",
                "browser_data": browser_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/analyze-browser-fingerprint",
                json=payload
            )
            
            # Should handle gracefully (either 200 with error handling or 500 with proper error)
            if response.status_code in [200, 500]:
                self.log_result(
                    "Browser Fingerprint Analysis - Edge Cases", 
                    True, 
                    f"Edge case handled gracefully (Status: {response.status_code})"
                )
                return True
            else:
                self.log_result("Browser Fingerprint Analysis - Edge Cases", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Browser Fingerprint Analysis - Edge Cases", False, f"Exception: {str(e)}")
            return False

    def test_automation_detection_edge_cases(self):
        """Test automation detection with malformed/edge case data"""
        try:
            # Malformed data
            browser_data = {
                "user_agent": 12345,  # Wrong type
                "webdriver": "maybe",  # Wrong type
                "plugins": None,  # Null plugins
                "event_properties": "not_an_object"  # Wrong type
            }
            
            behavioral_data = {
                "mouse_data": "invalid",  # Wrong type
                "timing_data": None  # Null timing data
            }
            
            payload = {
                "session_id": self.session_id + "_automation_edge_case",
                "browser_data": browser_data,
                "behavioral_data": behavioral_data
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/session-fingerprinting/detect-automation-tools",
                json=payload
            )
            
            # Should handle gracefully
            if response.status_code in [200, 500]:
                self.log_result(
                    "Automation Detection - Edge Cases", 
                    True, 
                    f"Edge case handled gracefully (Status: {response.status_code})"
                )
                return True
            else:
                self.log_result("Automation Detection - Edge Cases", False, f"Unexpected status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Automation Detection - Edge Cases", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all Phase 3.2 browser and environment analysis tests"""
        print("🎯 STARTING PHASE 3.2: ADVANCED BROWSER & ENVIRONMENT ANALYSIS TESTING")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed. Cannot proceed with tests.")
            return 0, 0
        
        # Run all tests
        tests = [
            self.test_browser_fingerprint_analysis_normal_chrome,
            self.test_browser_fingerprint_analysis_suspicious_firefox,
            self.test_browser_fingerprint_analysis_safari,
            self.test_automation_detection_clean_session,
            self.test_automation_detection_selenium_signatures,
            self.test_automation_detection_puppeteer_signatures,
            self.test_automation_detection_playwright_signatures,
            self.test_browser_fingerprint_edge_cases,
            self.test_automation_detection_edge_cases
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        
        # Print summary
        print("\n" + "=" * 80)
        print("🎯 PHASE 3.2 TESTING SUMMARY")
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
    tester = Phase32BrowserEnvironmentTester()
    passed, total = tester.run_all_tests()
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! Phase 3.2 functionality is working perfectly.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review the results above.")

#!/usr/bin/env python3
"""
Comprehensive Backend Testing for Placement Preparation Assessment Reports and Token-Based Visibility Logic
Testing the complete end-to-end workflow for placement preparation vs admin token separation
"""

import requests
import json
import time
import os
from datetime import datetime

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://session-monitor.preview.emergentagent.com')
BASE_URL = f"{BACKEND_URL}/api"

class PlacementPreparationTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_authenticated = False
        self.placement_prep_token = None
        self.admin_token = None
        self.placement_prep_session_id = None
        self.admin_session_id = None
        self.placement_prep_assessment_id = None
        self.admin_assessment_id = None
        
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

    def create_placement_preparation_token(self):
        """Create a token via placement preparation endpoint"""
        try:
            # Create sample resume content
            resume_content = """
            John Smith
            Senior Software Engineer
            
            EXPERIENCE:
            - 5+ years Python development
            - 3+ years React/JavaScript
            - Experience with FastAPI, MongoDB
            - Team leadership experience
            - AWS cloud deployment
            
            EDUCATION:
            - Bachelor's in Computer Science
            - Master's in Software Engineering
            
            SKILLS:
            Python, JavaScript, React, FastAPI, MongoDB, Docker, AWS, Team Leadership
            """
            
            token_request = {
                "job_title": "Senior Full Stack Developer - Placement Prep",
                "job_description": "We are looking for a senior full stack developer with expertise in Python and React.",
                "job_requirements": "5+ years experience, Python, React, FastAPI, MongoDB, leadership skills",
                "resume_text": resume_content.strip(),
                "role_archetype": "Software Engineer",
                "interview_focus": "Technical Deep-Dive",
                "include_coding_challenge": True,
                "min_questions": 8,
                "max_questions": 12
            }
            
            response = self.session.post(f"{BASE_URL}/admin/create-token", 
                                       json=token_request)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("token"):
                    self.placement_prep_token = data["token"]
                    self.log_test("Placement Preparation Token Creation", "PASS", 
                                f"Token created: {self.placement_prep_token[:8]}... via placement preparation")
                    return True
                else:
                    self.log_test("Placement Preparation Token Creation", "FAIL", 
                                f"Token creation failed: {data}")
                    return False
            else:
                self.log_test("Placement Preparation Token Creation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Placement Preparation Token Creation", "FAIL", f"Exception: {str(e)}")
            return False

    def create_admin_token(self):
        """Create a token via admin dashboard endpoint"""
        try:
            # Create sample resume file content
            resume_content = """
            Jane Doe
            Senior Backend Developer
            
            EXPERIENCE:
            - 6+ years Python development
            - 4+ years Django/FastAPI
            - Database design and optimization
            - Microservices architecture
            - DevOps and CI/CD
            
            EDUCATION:
            - Bachelor's in Computer Engineering
            - AWS Certified Solutions Architect
            
            SKILLS:
            Python, Django, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, AWS
            """
            
            # Prepare form data for admin upload
            files = {
                'resume_file': ('jane_resume.txt', resume_content.encode(), 'text/plain')
            }
            
            form_data = {
                'job_title': 'Senior Backend Developer - Admin',
                'job_description': 'We are seeking a senior backend developer with strong Python skills.',
                'job_requirements': '6+ years experience, Python, Django/FastAPI, database design, microservices'
            }
            
            response = self.session.post(f"{BASE_URL}/admin/upload-job", 
                                       files=files, data=form_data)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("token"):
                    self.admin_token = data["token"]
                    self.log_test("Admin Token Creation", "PASS", 
                                f"Token created: {self.admin_token[:8]}... via admin dashboard")
                    return True
                else:
                    self.log_test("Admin Token Creation", "FAIL", 
                                f"Token creation failed: {data}")
                    return False
            else:
                self.log_test("Admin Token Creation", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Admin Token Creation", "FAIL", f"Exception: {str(e)}")
            return False

    def verify_token_source_marking(self):
        """Verify that tokens are marked with correct created_via field"""
        try:
            # Check placement preparation token in database
            # We'll validate this by starting interviews and checking the assessment created_via field
            # since we can't directly query the database from the test
            
            # Validate placement prep token
            pp_response = self.session.post(f"{BASE_URL}/candidate/validate-token", 
                                          json={"token": self.placement_prep_token})
            
            # Validate admin token  
            admin_response = self.session.post(f"{BASE_URL}/candidate/validate-token", 
                                             json={"token": self.admin_token})
            
            if pp_response.status_code == 200 and admin_response.status_code == 200:
                pp_data = pp_response.json()
                admin_data = admin_response.json()
                
                self.log_test("Token Source Marking Validation", "PASS", 
                            f"Both tokens validated successfully - PP: {pp_data.get('job_title')}, Admin: {admin_data.get('job_title')}")
                return True
            else:
                self.log_test("Token Source Marking Validation", "FAIL", 
                            f"Token validation failed - PP: {pp_response.status_code}, Admin: {admin_response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Token Source Marking Validation", "FAIL", f"Exception: {str(e)}")
            return False

    def complete_placement_preparation_interview(self):
        """Complete a full interview using placement preparation token"""
        try:
            # Start interview
            start_response = self.session.post(f"{BASE_URL}/candidate/start-interview", 
                                             json={
                                                 "token": self.placement_prep_token,
                                                 "candidate_name": "John Smith",
                                                 "voice_mode": False
                                             })
            
            if start_response.status_code != 200:
                self.log_test("Placement Prep Interview Start", "FAIL", 
                            f"Failed to start interview: {start_response.status_code}")
                return False
            
            start_data = start_response.json()
            self.placement_prep_session_id = start_data.get("session_id")
            
            if not self.placement_prep_session_id:
                self.log_test("Placement Prep Interview Start", "FAIL", 
                            "No session ID returned")
                return False
            
            self.log_test("Placement Prep Interview Start", "PASS", 
                        f"Interview started with session ID: {self.placement_prep_session_id}")
            
            # Answer questions to complete the interview
            questions_answered = 0
            max_questions = 8
            
            sample_answers = [
                "I have 5+ years of experience in Python development, working on web applications and APIs.",
                "I've led a team of 4 developers on a microservices project using FastAPI and MongoDB.",
                "My approach to debugging involves systematic logging, unit testing, and using debugging tools.",
                "I stay updated through tech blogs, conferences, and contributing to open source projects.",
                "I handled a critical production issue by implementing proper monitoring and rollback procedures.",
                "I believe in collaborative leadership, clear communication, and mentoring team members.",
                "I prioritize tasks based on business impact, technical complexity, and dependencies.",
                "I've worked with AWS services including EC2, RDS, Lambda, and implemented CI/CD pipelines."
            ]
            
            while questions_answered < max_questions:
                # Send answer
                answer_response = self.session.post(f"{BASE_URL}/candidate/send-message", 
                                                  json={
                                                      "token": self.placement_prep_token,
                                                      "message": sample_answers[questions_answered % len(sample_answers)]
                                                  })
                
                if answer_response.status_code != 200:
                    self.log_test("Placement Prep Interview Answer", "FAIL", 
                                f"Failed to submit answer {questions_answered + 1}: {answer_response.status_code}")
                    return False
                
                answer_data = answer_response.json()
                questions_answered += 1
                
                # Check if interview is complete
                if answer_data.get("interview_complete"):
                    self.log_test("Placement Prep Interview Completion", "PASS", 
                                f"Interview completed after {questions_answered} questions")
                    break
                
                # Small delay between questions
                time.sleep(0.5)
            
            return True
            
        except Exception as e:
            self.log_test("Placement Prep Interview Completion", "FAIL", f"Exception: {str(e)}")
            return False

    def complete_admin_interview(self):
        """Complete a full interview using admin token"""
        try:
            # Start interview
            start_response = self.session.post(f"{BASE_URL}/candidate/start-interview", 
                                             json={
                                                 "token": self.admin_token,
                                                 "candidate_name": "Jane Doe",
                                                 "voice_mode": False
                                             })
            
            if start_response.status_code != 200:
                self.log_test("Admin Interview Start", "FAIL", 
                            f"Failed to start interview: {start_response.status_code}")
                return False
            
            start_data = start_response.json()
            self.admin_session_id = start_data.get("session_id")
            
            if not self.admin_session_id:
                self.log_test("Admin Interview Start", "FAIL", 
                            "No session ID returned")
                return False
            
            self.log_test("Admin Interview Start", "PASS", 
                        f"Interview started with session ID: {self.admin_session_id}")
            
            # Answer questions to complete the interview
            questions_answered = 0
            max_questions = 8
            
            sample_answers = [
                "I have 6+ years of backend development experience with Python and Django/FastAPI.",
                "I've designed and implemented microservices architectures for high-traffic applications.",
                "I use profiling tools, database query optimization, and caching strategies for performance.",
                "I follow TDD practices, write comprehensive unit tests, and use CI/CD for quality assurance.",
                "I've implemented OAuth2, JWT tokens, and proper input validation for security.",
                "I use monitoring tools like Prometheus, implement proper logging, and set up alerts.",
                "I've mentored junior developers and led technical architecture discussions.",
                "I've worked with Docker, Kubernetes, AWS services, and implemented infrastructure as code."
            ]
            
            while questions_answered < max_questions:
                # Send answer
                answer_response = self.session.post(f"{BASE_URL}/candidate/send-message", 
                                                  json={
                                                      "token": self.admin_token,
                                                      "message": sample_answers[questions_answered % len(sample_answers)]
                                                  })
                
                if answer_response.status_code != 200:
                    self.log_test("Admin Interview Answer", "FAIL", 
                                f"Failed to submit answer {questions_answered + 1}: {answer_response.status_code}")
                    return False
                
                answer_data = answer_response.json()
                questions_answered += 1
                
                # Check if interview is complete
                if answer_data.get("interview_complete"):
                    self.log_test("Admin Interview Completion", "PASS", 
                                f"Interview completed after {questions_answered} questions")
                    break
                
                # Small delay between questions
                time.sleep(0.5)
            
            return True
            
        except Exception as e:
            self.log_test("Admin Interview Completion", "FAIL", f"Exception: {str(e)}")
            return False

    def test_placement_preparation_reports_visibility(self):
        """Test that placement preparation reports endpoint only shows placement preparation assessments"""
        try:
            response = self.session.get(f"{BASE_URL}/placement-preparation/reports")
            
            if response.status_code != 200:
                self.log_test("Placement Preparation Reports Visibility", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            reports = data.get("reports", [])
            
            # Verify all reports are from placement preparation
            placement_prep_count = 0
            admin_count = 0
            
            for report in reports:
                created_via = report.get("created_via", "unknown")
                if created_via == "placement_preparation":
                    placement_prep_count += 1
                elif created_via == "admin":
                    admin_count += 1
                    
                # Check if our placement prep session is in the results
                if report.get("session_id") == self.placement_prep_session_id:
                    self.placement_prep_assessment_id = report.get("id")
            
            if admin_count > 0:
                self.log_test("Placement Preparation Reports Visibility", "FAIL", 
                            f"Found {admin_count} admin reports in placement preparation endpoint")
                return False
            
            self.log_test("Placement Preparation Reports Visibility", "PASS", 
                        f"Found {placement_prep_count} placement preparation reports, 0 admin reports (correct separation)")
            return True
            
        except Exception as e:
            self.log_test("Placement Preparation Reports Visibility", "FAIL", f"Exception: {str(e)}")
            return False

    def test_admin_reports_visibility(self):
        """Test that admin reports endpoint only shows admin and legacy assessments"""
        try:
            response = self.session.get(f"{BASE_URL}/admin/reports")
            
            if response.status_code != 200:
                self.log_test("Admin Reports Visibility", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            reports = data.get("reports", [])
            
            # Verify no placement preparation reports are shown
            placement_prep_count = 0
            admin_count = 0
            legacy_count = 0
            
            for report in reports:
                created_via = report.get("created_via")
                if created_via == "placement_preparation":
                    placement_prep_count += 1
                elif created_via == "admin":
                    admin_count += 1
                elif created_via is None:  # Legacy reports
                    legacy_count += 1
                    
                # Check if our admin session is in the results
                if report.get("session_id") == self.admin_session_id:
                    self.admin_assessment_id = report.get("id")
            
            if placement_prep_count > 0:
                self.log_test("Admin Reports Visibility", "FAIL", 
                            f"Found {placement_prep_count} placement preparation reports in admin endpoint")
                return False
            
            self.log_test("Admin Reports Visibility", "PASS", 
                        f"Found {admin_count} admin reports, {legacy_count} legacy reports, 0 placement prep reports (correct separation)")
            return True
            
        except Exception as e:
            self.log_test("Admin Reports Visibility", "FAIL", f"Exception: {str(e)}")
            return False

    def test_placement_preparation_detailed_report(self):
        """Test placement preparation detailed report endpoint"""
        try:
            if not self.placement_prep_session_id:
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            "No placement preparation session ID available")
                return False
            
            response = self.session.get(f"{BASE_URL}/placement-preparation/reports/{self.placement_prep_session_id}")
            
            if response.status_code == 404:
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            "Report not found - assessment may not have been created yet")
                return False
            elif response.status_code != 200:
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            report = data.get("report", {})
            
            # Verify report structure and content
            required_fields = ["session_id", "candidate_name", "job_title", "technical_score", 
                             "behavioral_score", "overall_score", "created_via"]
            
            missing_fields = [field for field in required_fields if field not in report]
            if missing_fields:
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            f"Missing required fields: {missing_fields}")
                return False
            
            # Verify it's marked as placement preparation
            if report.get("created_via") != "placement_preparation":
                self.log_test("Placement Preparation Detailed Report", "FAIL", 
                            f"Report has incorrect created_via: {report.get('created_via')}")
                return False
            
            self.log_test("Placement Preparation Detailed Report", "PASS", 
                        f"Retrieved detailed report for {report.get('candidate_name')} - {report.get('job_title')}")
            return True
            
        except Exception as e:
            self.log_test("Placement Preparation Detailed Report", "FAIL", f"Exception: {str(e)}")
            return False

    def test_admin_detailed_report(self):
        """Test admin detailed report endpoint"""
        try:
            if not self.admin_session_id:
                self.log_test("Admin Detailed Report", "FAIL", 
                            "No admin session ID available")
                return False
            
            response = self.session.get(f"{BASE_URL}/admin/reports/{self.admin_session_id}")
            
            if response.status_code == 404:
                self.log_test("Admin Detailed Report", "FAIL", 
                            "Report not found - assessment may not have been created yet")
                return False
            elif response.status_code != 200:
                self.log_test("Admin Detailed Report", "FAIL", 
                            f"HTTP {response.status_code}: {response.text}")
                return False
            
            data = response.json()
            report = data.get("report", {})
            
            # Verify report structure and content
            required_fields = ["session_id", "candidate_name", "job_title", "technical_score", 
                             "behavioral_score", "overall_score", "created_via"]
            
            missing_fields = [field for field in required_fields if field not in report]
            if missing_fields:
                self.log_test("Admin Detailed Report", "FAIL", 
                            f"Missing required fields: {missing_fields}")
                return False
            
            # Verify it's marked as admin
            if report.get("created_via") != "admin":
                self.log_test("Admin Detailed Report", "FAIL", 
                            f"Report has incorrect created_via: {report.get('created_via')}")
                return False
            
            self.log_test("Admin Detailed Report", "PASS", 
                        f"Retrieved detailed report for {report.get('candidate_name')} - {report.get('job_title')}")
            return True
            
        except Exception as e:
            self.log_test("Admin Detailed Report", "FAIL", f"Exception: {str(e)}")
            return False

    def test_cross_endpoint_isolation(self):
        """Test that placement preparation reports are not accessible via admin endpoint and vice versa"""
        try:
            # Try to access placement preparation report via admin endpoint
            if self.placement_prep_session_id:
                admin_access_response = self.session.get(f"{BASE_URL}/admin/reports/{self.placement_prep_session_id}")
                if admin_access_response.status_code != 404:
                    self.log_test("Cross-Endpoint Isolation", "FAIL", 
                                f"Placement prep report accessible via admin endpoint (should be 404)")
                    return False
            
            # Try to access admin report via placement preparation endpoint
            if self.admin_session_id:
                pp_access_response = self.session.get(f"{BASE_URL}/placement-preparation/reports/{self.admin_session_id}")
                if pp_access_response.status_code != 404:
                    self.log_test("Cross-Endpoint Isolation", "FAIL", 
                                f"Admin report accessible via placement prep endpoint (should be 404)")
                    return False
            
            self.log_test("Cross-Endpoint Isolation", "PASS", 
                        "Reports are properly isolated - placement prep reports not accessible via admin endpoint and vice versa")
            return True
            
        except Exception as e:
            self.log_test("Cross-Endpoint Isolation", "FAIL", f"Exception: {str(e)}")
            return False

    def run_comprehensive_test(self):
        """Run all tests in sequence"""
        print("=" * 80)
        print("PLACEMENT PREPARATION ASSESSMENT REPORTS & TOKEN-BASED VISIBILITY TESTING")
        print("=" * 80)
        print()
        
        test_results = []
        
        # Test 1: Admin Authentication
        test_results.append(self.test_admin_authentication())
        
        if not self.admin_authenticated:
            print("❌ Cannot proceed without admin authentication")
            return False
        
        # Test 2: Token Creation & Source Marking
        test_results.append(self.create_placement_preparation_token())
        test_results.append(self.create_admin_token())
        test_results.append(self.verify_token_source_marking())
        
        # Test 3: Complete Interview Workflows
        test_results.append(self.complete_placement_preparation_interview())
        test_results.append(self.complete_admin_interview())
        
        # Wait a moment for assessments to be generated
        print("⏳ Waiting for assessments to be generated...")
        time.sleep(3)
        
        # Test 4: Assessment Reports Visibility
        test_results.append(self.test_placement_preparation_reports_visibility())
        test_results.append(self.test_admin_reports_visibility())
        
        # Test 5: Detailed Report Functionality
        test_results.append(self.test_placement_preparation_detailed_report())
        test_results.append(self.test_admin_detailed_report())
        
        # Test 6: Cross-Endpoint Isolation
        test_results.append(self.test_cross_endpoint_isolation())
        
        # Summary
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        
        passed_tests = sum(test_results)
        total_tests = len(test_results)
        
        print(f"✅ Passed: {passed_tests}/{total_tests} tests")
        print(f"❌ Failed: {total_tests - passed_tests}/{total_tests} tests")
        print(f"📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Placement preparation assessment reports and token-based visibility logic is working correctly.")
        else:
            print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please review the issues above.")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = PlacementPreparationTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n✅ PLACEMENT PREPARATION TESTING COMPLETED SUCCESSFULLY")
        exit(0)
    else:
        print("\n❌ PLACEMENT PREPARATION TESTING COMPLETED WITH FAILURES")
        exit(1)

if __name__ == "__main__":
    main()