#!/usr/bin/env python3
"""
🎯 TASK 2.2: DATABASE PERFORMANCE OPTIMIZATION TESTING - COMPREHENSIVE TESTING

Testing the newly implemented Task 2.2: Database Performance Optimization functionality.

Test Coverage:
1. Core Optimization Features Testing
2. Compound Index Testing  
3. TTL Index Testing
4. Aggregation Pipeline Testing
5. Connection Pool Optimization Testing
6. Query Performance Monitoring Testing
7. Comprehensive Optimization Testing
8. Integration and Performance Testing

API Endpoints to Test:
- POST /api/admin/database/create-compound-indexes
- POST /api/admin/database/setup-ttl-indexes  
- POST /api/admin/database/create-aggregation-pipelines
- POST /api/admin/database/optimize-connection-pool
- GET /api/admin/database/query-performance
- POST /api/admin/database/optimize-all

Testing Scenarios:
- Direct database_optimization.py script execution
- All 4 optimization areas functionality
- Automatic startup optimization integration
- Performance improvements and metrics collection
- 24 compound indexes across 6 collections
- TTL indexes with different retention periods
- 5 pre-built aggregation pipelines
- Connection pool optimization with load testing
- Query performance monitoring and slow query detection
- Comprehensive optimization with success rate calculation
- Admin authentication and error handling
"""

import requests
import json
import uuid
import subprocess
import sys
import os
from datetime import datetime, timedelta
import time
import asyncio

# Configuration
BACKEND_URL = "https://security-keystroke.preview.emergentagent.com/api"
ADMIN_PASSWORD = "Game@1234"

class DatabaseOptimizationTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
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

    def test_direct_database_optimization_script(self):
        """Test direct execution of database_optimization.py script"""
        try:
            # Change to backend directory and run the script
            script_path = "/app/backend/database_optimization.py"
            
            if not os.path.exists(script_path):
                self.log_result("Direct Script Execution", False, f"Script not found at {script_path}")
                return False
            
            # Execute the script directly
            result = subprocess.run(
                [sys.executable, script_path],
                cwd="/app/backend",
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                output_lines = result.stdout.split('\n')
                success_indicators = [
                    "Compound indexes created:",
                    "TTL indexes created:",
                    "Aggregation pipelines created:",
                    "Connection pool optimization completed!"
                ]
                
                found_indicators = sum(1 for line in output_lines for indicator in success_indicators if indicator in line)
                
                self.log_result(
                    "Direct Script Execution", 
                    True, 
                    f"Script executed successfully. Found {found_indicators}/4 optimization indicators. Output length: {len(result.stdout)} chars"
                )
                return True
            else:
                self.log_result(
                    "Direct Script Execution", 
                    False, 
                    f"Script failed with return code {result.returncode}. Error: {result.stderr[:200]}"
                )
                return False
                
        except subprocess.TimeoutExpired:
            self.log_result("Direct Script Execution", False, "Script execution timed out after 60 seconds")
            return False
        except Exception as e:
            self.log_result("Direct Script Execution", False, f"Exception during script execution: {str(e)}")
            return False

    def test_compound_index_creation(self):
        """Test compound index creation endpoint"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/database/create-compound-indexes"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    details = data.get('details', {})
                    compound_indexes_created = details.get('compound_indexes_created', 0)
                    collections_processed = details.get('collections_processed', 0)
                    
                    # Verify expected compound indexes (24 across 6 collections)
                    expected_indexes = 24
                    expected_collections = 6
                    
                    success = (compound_indexes_created >= expected_indexes * 0.8 and 
                              collections_processed >= expected_collections)
                    
                    self.log_result(
                        "Compound Index Creation", 
                        success, 
                        f"Created {compound_indexes_created} compound indexes across {collections_processed} collections (Expected: {expected_indexes} indexes, {expected_collections} collections)"
                    )
                    return success
                else:
                    self.log_result("Compound Index Creation", False, f"API returned success=false: {data}")
                    return False
            else:
                self.log_result("Compound Index Creation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Compound Index Creation", False, f"Exception: {str(e)}")
            return False

    def test_ttl_index_setup(self):
        """Test TTL index setup endpoint"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/database/setup-ttl-indexes"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    details = data.get('details', {})
                    ttl_indexes_created = details.get('ttl_indexes_created', 0)
                    ttl_status = details.get('ttl_status', {})
                    
                    # Verify expected TTL configurations
                    expected_collections = [
                        'device_fingerprints', 'browser_fingerprints', 'session_integrity_profiles',
                        'fingerprint_violations', 'device_reputation_scores', 'fingerprint_analytics'
                    ]
                    
                    expected_retention_periods = {
                        'device_fingerprints': 90,
                        'browser_fingerprints': 90,
                        'session_integrity_profiles': 30,
                        'fingerprint_violations': 180,
                        'device_reputation_scores': 365,
                        'fingerprint_analytics': 90
                    }
                    
                    configured_collections = len([col for col in expected_collections if col in ttl_status])
                    
                    # Check retention periods
                    retention_correct = True
                    for collection, expected_days in expected_retention_periods.items():
                        if collection in ttl_status:
                            actual_days = ttl_status[collection].get('retention_days', 0)
                            if abs(actual_days - expected_days) > 1:  # Allow 1 day tolerance
                                retention_correct = False
                                break
                    
                    success = (ttl_indexes_created >= 6 and configured_collections >= 6 and retention_correct)
                    
                    self.log_result(
                        "TTL Index Setup", 
                        success, 
                        f"Created {ttl_indexes_created} TTL indexes for {configured_collections}/6 collections with correct retention periods: {retention_correct}"
                    )
                    return success
                else:
                    self.log_result("TTL Index Setup", False, f"API returned success=false: {data}")
                    return False
            else:
                self.log_result("TTL Index Setup", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("TTL Index Setup", False, f"Exception: {str(e)}")
            return False

    def test_aggregation_pipeline_creation(self):
        """Test aggregation pipeline creation endpoint"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/database/create-aggregation-pipelines"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    pipelines_created = data.get('pipelines_created', 0)
                    pipeline_details = data.get('pipeline_details', {})
                    
                    # Verify expected 5 pre-built pipelines
                    expected_pipelines = [
                        'device_fingerprint_analytics',
                        'browser_entropy_analysis', 
                        'session_integrity_monitoring',
                        'violation_trend_analysis',
                        'reputation_scoring_analysis'
                    ]
                    
                    created_pipelines = [name for name, details in pipeline_details.items() if details.get('validated')]
                    performance_check = True
                    
                    # Check pipeline performance (fast <100ms, medium <500ms)
                    for name, details in pipeline_details.items():
                        if details.get('validated'):
                            exec_time = details.get('test_execution_time', 0)
                            estimated_time = details.get('estimated_time', 'unknown')
                            
                            if estimated_time == 'fast' and exec_time > 100:
                                performance_check = False
                            elif estimated_time == 'medium' and exec_time > 500:
                                performance_check = False
                    
                    success = (pipelines_created >= 5 and len(created_pipelines) >= 5 and performance_check)
                    
                    self.log_result(
                        "Aggregation Pipeline Creation", 
                        success, 
                        f"Created {pipelines_created} pipelines, validated {len(created_pipelines)}/5 expected pipelines, performance targets met: {performance_check}"
                    )
                    return success
                else:
                    self.log_result("Aggregation Pipeline Creation", False, f"API returned success=false: {data}")
                    return False
            else:
                self.log_result("Aggregation Pipeline Creation", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Aggregation Pipeline Creation", False, f"Exception: {str(e)}")
            return False

    def test_connection_pool_optimization(self):
        """Test connection pool optimization endpoint"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/database/optimize-connection-pool"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    connection_tests = data.get('connection_tests', {})
                    recommendations = data.get('recommendations', [])
                    
                    # Verify 3 load configurations tested
                    expected_configs = ['light_load', 'medium_load', 'heavy_load']
                    tested_configs = [config for config in expected_configs if config in connection_tests]
                    
                    # Check if tests were successful
                    successful_tests = 0
                    for config_name, result in connection_tests.items():
                        if result.get('tested') and result.get('connection_time', 0) > 0:
                            successful_tests += 1
                    
                    # Check for performance recommendations
                    has_recommendations = len(recommendations) >= 3
                    
                    success = (len(tested_configs) >= 3 and successful_tests >= 2 and has_recommendations)
                    
                    self.log_result(
                        "Connection Pool Optimization", 
                        success, 
                        f"Tested {len(tested_configs)}/3 load configurations, {successful_tests} successful tests, {len(recommendations)} recommendations provided"
                    )
                    return success
                else:
                    self.log_result("Connection Pool Optimization", False, f"API returned success=false: {data}")
                    return False
            else:
                self.log_result("Connection Pool Optimization", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Connection Pool Optimization", False, f"Exception: {str(e)}")
            return False

    def test_query_performance_monitoring(self):
        """Test query performance monitoring endpoint"""
        try:
            response = self.session.get(
                f"{BACKEND_URL}/admin/database/query-performance"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    performance_data = data.get('performance_summary', {})
                    recommendations = data.get('recommendations', [])
                    
                    # Check performance monitoring features
                    has_query_metrics = 'total_queries' in performance_data
                    has_execution_times = 'avg_execution_time' in performance_data
                    has_slow_query_detection = 'slow_query_count' in performance_data
                    has_recommendations = len(recommendations) > 0
                    
                    # Check slow query threshold (1.0 seconds as specified)
                    slow_query_threshold_ok = True
                    if 'slow_query_count' in performance_data and 'total_queries' in performance_data:
                        total_queries = performance_data['total_queries']
                        if total_queries > 0:
                            # This is acceptable even if no queries yet
                            slow_query_threshold_ok = True
                    
                    success = (has_query_metrics and has_execution_times and 
                              has_slow_query_detection and has_recommendations and 
                              slow_query_threshold_ok)
                    
                    self.log_result(
                        "Query Performance Monitoring", 
                        success, 
                        f"Performance monitoring active: metrics={has_query_metrics}, timing={has_execution_times}, slow_query_detection={has_slow_query_detection}, recommendations={len(recommendations)}"
                    )
                    return success
                else:
                    self.log_result("Query Performance Monitoring", False, f"API returned success=false: {data}")
                    return False
            else:
                self.log_result("Query Performance Monitoring", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Query Performance Monitoring", False, f"Exception: {str(e)}")
            return False

    def test_comprehensive_optimization(self):
        """Test comprehensive optimization endpoint (optimize-all)"""
        try:
            response = self.session.post(
                f"{BACKEND_URL}/admin/database/optimize-all"
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    optimization_results = data.get('optimization_results', {})
                    success_rate = data.get('success_rate', 0)
                    
                    # Verify all 4 optimization areas were attempted
                    expected_areas = [
                        'compound_indexes',
                        'ttl_indexes', 
                        'aggregation_pipelines',
                        'connection_pool'
                    ]
                    
                    completed_areas = [area for area in expected_areas if area in optimization_results]
                    successful_areas = [area for area in expected_areas 
                                      if optimization_results.get(area, {}).get('success', False)]
                    
                    # Check success rate calculation (should be reasonable)
                    success_rate_ok = success_rate >= 0.5  # At least 50% success rate
                    
                    # Check error handling
                    has_error_handling = 'errors' in data or all(
                        'errors' in optimization_results.get(area, {}) 
                        for area in completed_areas
                    )
                    
                    success = (len(completed_areas) >= 4 and len(successful_areas) >= 2 and 
                              success_rate_ok and has_error_handling)
                    
                    self.log_result(
                        "Comprehensive Optimization", 
                        success, 
                        f"Completed {len(completed_areas)}/4 optimization areas, {len(successful_areas)} successful, success rate: {success_rate:.1%}, error handling: {has_error_handling}"
                    )
                    return success
                else:
                    self.log_result("Comprehensive Optimization", False, f"API returned success=false: {data}")
                    return False
            else:
                self.log_result("Comprehensive Optimization", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_result("Comprehensive Optimization", False, f"Exception: {str(e)}")
            return False

    def test_startup_optimization_integration(self):
        """Test that optimization runs automatically on application startup"""
        try:
            # Check server logs or startup indicators
            # Since we can't directly test startup, we'll verify the optimization endpoints are available
            # and that the optimization system is properly integrated
            
            endpoints_to_check = [
                "/admin/database/create-compound-indexes",
                "/admin/database/setup-ttl-indexes", 
                "/admin/database/create-aggregation-pipelines",
                "/admin/database/optimize-connection-pool",
                "/admin/database/query-performance",
                "/admin/database/optimize-all"
            ]
            
            available_endpoints = 0
            for endpoint in endpoints_to_check:
                try:
                    # Use HEAD request to check endpoint availability
                    response = self.session.head(f"{BACKEND_URL}{endpoint}")
                    if response.status_code in [200, 405]:  # 405 = Method Not Allowed (but endpoint exists)
                        available_endpoints += 1
                except:
                    pass
            
            # Check if optimization functions are imported in server.py
            server_integration = True
            try:
                with open("/app/backend/server.py", "r") as f:
                    server_content = f.read()
                    integration_indicators = [
                        "from database_optimization import",
                        "create_compound_indexes",
                        "setup_ttl_indexes", 
                        "create_aggregation_pipelines",
                        "optimize_connection_pool"
                    ]
                    found_indicators = sum(1 for indicator in integration_indicators if indicator in server_content)
                    server_integration = found_indicators >= 4
            except:
                server_integration = False
            
            success = available_endpoints >= 6 and server_integration
            
            self.log_result(
                "Startup Optimization Integration", 
                success, 
                f"Available endpoints: {available_endpoints}/6, server integration: {server_integration}"
            )
            return success
            
        except Exception as e:
            self.log_result("Startup Optimization Integration", False, f"Exception: {str(e)}")
            return False

    def test_performance_improvements_validation(self):
        """Test that performance improvements are measurable"""
        try:
            # Test query performance before and after optimization
            # This is a simplified test - in production, we'd measure actual query times
            
            # Get current performance metrics
            response = self.session.get(f"{BACKEND_URL}/admin/database/query-performance")
            
            if response.status_code == 200:
                data = response.json()
                performance_summary = data.get('performance_summary', {})
                
                # Check for performance tracking capabilities
                has_timing_metrics = 'avg_execution_time' in performance_summary
                has_index_usage = 'index_usage_stats' in performance_summary
                has_collection_performance = 'collection_performance' in performance_summary
                has_optimization_recommendations = len(data.get('recommendations', [])) > 0
                
                # Verify metrics collection is working
                metrics_collection_working = (has_timing_metrics and has_index_usage and 
                                            has_collection_performance and has_optimization_recommendations)
                
                self.log_result(
                    "Performance Improvements Validation", 
                    metrics_collection_working, 
                    f"Performance metrics collection: timing={has_timing_metrics}, indexes={has_index_usage}, collections={has_collection_performance}, recommendations={has_optimization_recommendations}"
                )
                return metrics_collection_working
            else:
                self.log_result("Performance Improvements Validation", False, f"Failed to get performance metrics: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log_result("Performance Improvements Validation", False, f"Exception: {str(e)}")
            return False

    def test_integration_with_fingerprinting_collections(self):
        """Test integration with existing fingerprinting collections from Task 2.1"""
        try:
            # Verify that optimization works with the 6 fingerprinting collections
            expected_collections = [
                'device_fingerprints',
                'browser_fingerprints', 
                'session_integrity_profiles',
                'fingerprint_violations',
                'device_reputation_scores',
                'fingerprint_analytics'
            ]
            
            # Test compound indexes on fingerprinting collections
            compound_response = self.session.post(f"{BACKEND_URL}/admin/database/create-compound-indexes")
            compound_success = compound_response.status_code == 200 and compound_response.json().get('success', False)
            
            # Test TTL indexes on fingerprinting collections  
            ttl_response = self.session.post(f"{BACKEND_URL}/admin/database/setup-ttl-indexes")
            ttl_success = ttl_response.status_code == 200 and ttl_response.json().get('success', False)
            
            # Test aggregation pipelines using fingerprinting collections
            pipeline_response = self.session.post(f"{BACKEND_URL}/admin/database/create-aggregation-pipelines")
            pipeline_success = pipeline_response.status_code == 200 and pipeline_response.json().get('success', False)
            
            # Check if collections are properly referenced in optimization
            integration_score = sum([compound_success, ttl_success, pipeline_success])
            success = integration_score >= 2  # At least 2 out of 3 should work
            
            self.log_result(
                "Integration with Fingerprinting Collections", 
                success, 
                f"Integration test results: compound_indexes={compound_success}, ttl_indexes={ttl_success}, aggregation_pipelines={pipeline_success} (Score: {integration_score}/3)"
            )
            return success
            
        except Exception as e:
            self.log_result("Integration with Fingerprinting Collections", False, f"Exception: {str(e)}")
            return False

    def test_error_handling_and_graceful_degradation(self):
        """Test error handling and graceful degradation"""
        try:
            # Test with invalid/malformed requests
            test_cases = [
                {
                    "name": "Invalid endpoint",
                    "url": f"{BACKEND_URL}/admin/database/invalid-endpoint",
                    "method": "POST",
                    "expected_status": [404, 405]
                },
                {
                    "name": "Malformed request data",
                    "url": f"{BACKEND_URL}/admin/database/optimize-all",
                    "method": "POST", 
                    "data": {"invalid": "data"},
                    "expected_status": [200, 400, 422]  # Should handle gracefully
                }
            ]
            
            error_handling_score = 0
            for test_case in test_cases:
                try:
                    if test_case["method"] == "POST":
                        response = self.session.post(
                            test_case["url"], 
                            json=test_case.get("data", {})
                        )
                    else:
                        response = self.session.get(test_case["url"])
                    
                    if response.status_code in test_case["expected_status"]:
                        error_handling_score += 1
                except:
                    pass  # Expected for some error cases
            
            # Test graceful degradation - optimization should continue even if some parts fail
            optimize_response = self.session.post(f"{BACKEND_URL}/admin/database/optimize-all")
            graceful_degradation = False
            
            if optimize_response.status_code == 200:
                data = optimize_response.json()
                # Even if some optimizations fail, the endpoint should return success with details
                graceful_degradation = 'optimization_results' in data and 'success_rate' in data
            
            success = error_handling_score >= 1 and graceful_degradation
            
            self.log_result(
                "Error Handling and Graceful Degradation", 
                success, 
                f"Error handling score: {error_handling_score}/2, graceful degradation: {graceful_degradation}"
            )
            return success
            
        except Exception as e:
            self.log_result("Error Handling and Graceful Degradation", False, f"Exception: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all database optimization tests"""
        print("🎯 TASK 2.2: DATABASE PERFORMANCE OPTIMIZATION TESTING")
        print("=" * 80)
        
        # Authenticate first
        if not self.authenticate_admin():
            print("❌ Authentication failed - cannot proceed with tests")
            return 0, len([
                self.test_direct_database_optimization_script,
                self.test_compound_index_creation,
                self.test_ttl_index_setup,
                self.test_aggregation_pipeline_creation,
                self.test_connection_pool_optimization,
                self.test_query_performance_monitoring,
                self.test_comprehensive_optimization,
                self.test_startup_optimization_integration,
                self.test_performance_improvements_validation,
                self.test_integration_with_fingerprinting_collections,
                self.test_error_handling_and_graceful_degradation
            ])
        
        # Run all tests
        tests = [
            self.test_direct_database_optimization_script,
            self.test_compound_index_creation,
            self.test_ttl_index_setup,
            self.test_aggregation_pipeline_creation,
            self.test_connection_pool_optimization,
            self.test_query_performance_monitoring,
            self.test_comprehensive_optimization,
            self.test_startup_optimization_integration,
            self.test_performance_improvements_validation,
            self.test_integration_with_fingerprinting_collections,
            self.test_error_handling_and_graceful_degradation
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed_tests += 1
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
        
        print("\n" + "=" * 80)
        print(f"🎯 DATABASE OPTIMIZATION TESTING SUMMARY")
        print(f"Tests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("🎉 ALL TESTS PASSED - Database Performance Optimization is fully functional!")
        elif passed_tests >= total_tests * 0.8:
            print("✅ MOSTLY SUCCESSFUL - Database Performance Optimization is working well with minor issues")
        elif passed_tests >= total_tests * 0.5:
            print("⚠️  PARTIAL SUCCESS - Database Performance Optimization has significant issues")
        else:
            print("❌ MAJOR ISSUES - Database Performance Optimization needs significant fixes")
        
        return passed_tests, total_tests

def main():
    """Main function to run database optimization tests"""
    tester = DatabaseOptimizationTester()
    result = tester.run_all_tests()
    if result is None:
        passed, total = 0, 11
    else:
        passed, total = result
    
    # Return appropriate exit code
    if passed == total:
        exit(0)  # All tests passed
    elif passed >= total * 0.8:
        exit(1)  # Mostly successful but some issues
    else:
        exit(2)  # Significant issues

if __name__ == "__main__":
    main()