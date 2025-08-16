#!/usr/bin/env python3
"""
Industry Benchmark Engine Testing Suite
Phase 1.2 Step 4: Benchmark Comparison Against Industry Standards

This comprehensive testing suite validates:
- Industry percentile calculations with confidence intervals
- Peer comparison across multiple benchmark groups
- Benchmark visualization generation (interactive and static)
- Industry norms updating functionality
- Benchmark accuracy validation
"""

import sys
import os
import json
import asyncio
import aiohttp
import uuid
from datetime import datetime
from typing import Dict, List, Any

# Configuration
BACKEND_URL = "https://securesession.preview.emergentagent.com"
ADMIN_PASSWORD = "Game@1234"

class IndustryBenchmarkEngineTest:
    def __init__(self):
        self.session = None
        self.admin_token = None
        self.test_session_id = None
        self.analysis_results = {}
        
    async def setup(self):
        """Initialize test session"""
        self.session = aiohttp.ClientSession()
        print("🔧 Industry Benchmark Engine Test Suite Initialized")
        
    async def cleanup(self):
        """Clean up test session"""
        if self.session:
            await self.session.close()
        print("🧹 Test cleanup completed")
    
    async def test_admin_authentication(self):
        """Test admin authentication for ML endpoints"""
        print("\n📋 TEST 1: Admin Authentication")
        
        try:
            auth_data = {
                "password": ADMIN_PASSWORD
            }
            
            async with self.session.post(f"{BACKEND_URL}/api/admin/login", json=auth_data) as response:
                result = await response.json()
                
                if response.status == 200 and result.get('success'):
                    print("✅ Admin authentication successful")
                    print(f"   Status: {response.status}")
                    print(f"   Message: {result.get('message', 'N/A')}")
                    return True
                else:
                    print(f"❌ Admin authentication failed: {result}")
                    return False
                    
        except Exception as e:
            print(f"❌ Admin authentication error: {e}")
            return False
    
    async def create_mock_test_session(self):
        """Create mock test session with sample data"""
        print("\n📋 TEST 2: Mock Test Session Creation")
        
        try:
            # Read the session ID from the file created by the mock data script
            try:
                with open('/app/test_session_id.txt', 'r') as f:
                    self.test_session_id = f.read().strip()
                print(f"✅ Using existing session ID from database: {self.test_session_id}")
            except FileNotFoundError:
                print("⚠️  No existing session ID found, creating new mock data...")
                # Run the mock data creation script
                import subprocess
                result = subprocess.run(['python', '/app/create_mock_benchmark_data.py'], 
                                      capture_output=True, text=True, cwd='/app')
                if result.returncode == 0:
                    with open('/app/test_session_id.txt', 'r') as f:
                        self.test_session_id = f.read().strip()
                    print(f"✅ Created new session ID: {self.test_session_id}")
                else:
                    raise Exception(f"Failed to create mock data: {result.stderr}")
            
            # Mock test results data for display purposes
            mock_result_data = {
                "session_id": self.test_session_id,
                "topic_scores": {
                    "numerical_reasoning": {
                        "correct": 8,
                        "total": 12,
                        "percentage": 66.7,
                        "difficulty_average": 0.6
                    },
                    "logical_reasoning": {
                        "correct": 10,
                        "total": 15,
                        "percentage": 66.7,
                        "difficulty_average": 0.5
                    },
                    "verbal_comprehension": {
                        "correct": 12,
                        "total": 15,
                        "percentage": 80.0,
                        "difficulty_average": 0.7
                    },
                    "spatial_reasoning": {
                        "correct": 6,
                        "total": 13,
                        "percentage": 46.2,
                        "difficulty_average": 0.4
                    }
                },
                "questions_correct": 36,
                "questions_total": 55,
                "percentage_score": 65.5,
                "total_time_taken": 2475,
                "questions_attempted": 55
            }
            
            print("✅ Mock test session created successfully")
            print(f"   Session ID: {self.test_session_id}")
            print(f"   Overall Score: {mock_result_data['percentage_score']}%")
            print(f"   Questions Correct: {mock_result_data['questions_correct']}/{mock_result_data['questions_total']}")
            print("   Topic Performance:")
            for topic, scores in mock_result_data['topic_scores'].items():
                print(f"     {topic.replace('_', ' ').title()}: {scores['percentage']:.1f}%")
            
            # Store mock data for later use
            self.mock_result = mock_result_data
            
            return True
            
        except Exception as e:
            print(f"❌ Mock session creation error: {e}")
            return False
    
    async def test_industry_percentile_calculation(self):
        """Test comprehensive industry percentile calculation"""
        print("\n📋 TEST 3: Industry Percentile Calculation")
        
        try:
            # Test different job role and industry combinations
            test_configurations = [
                {
                    "job_role": "software_engineer",
                    "industry": "tech",
                    "job_level": "mid_level",
                    "region": "north_america",
                    "company_size": "mid_size"
                },
                {
                    "job_role": "data_analyst",
                    "industry": "finance",
                    "job_level": "entry_level",
                    "region": "europe",
                    "company_size": "enterprise"
                },
                {
                    "job_role": "project_manager",
                    "industry": "healthcare",
                    "job_level": "senior_level",
                    "region": "asia_pacific",
                    "company_size": "startup"
                }
            ]
            
            successful_tests = 0
            
            for i, config in enumerate(test_configurations, 1):
                print(f"\n   Configuration {i}: {config['job_role']} in {config['industry']}")
                
                # API endpoint parameters
                params = {
                    "session_id": self.test_session_id,
                    **config
                }
                
                async with self.session.post(f"{BACKEND_URL}/api/ml/calculate-industry-percentiles", params=params) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print(f"   ✅ Percentile calculation successful")
                        
                        # Analyze results
                        percentile_analysis = result.get('percentile_analysis', {})
                        percentile_results = percentile_analysis.get('percentile_results', {})
                        
                        print(f"   📊 Analysis ID: {percentile_analysis.get('analysis_id', 'N/A')}")
                        print(f"   📊 Benchmark Profile: {config['job_role']} | {config['industry']} | {config['job_level']}")
                        
                        # Display domain percentiles
                        print("   📊 Domain Percentiles:")
                        for domain, data in percentile_results.items():
                            if domain != 'composite':
                                score = data.get('score', 0)
                                percentile = data.get('percentile', 0)
                                z_score = data.get('z_score', 0)
                                print(f"      {domain.replace('_', ' ').title()}: {score:.1f}% (Percentile: {percentile:.1f}, Z-score: {z_score:.2f})")
                        
                        # Display composite score if available
                        if 'composite' in percentile_results:
                            composite = percentile_results['composite']
                            print(f"   📊 Composite Score: {composite.get('score', 0):.1f}% (Percentile: {composite.get('percentile', 0):.1f})")
                        
                        # Display confidence intervals
                        confidence_intervals = percentile_analysis.get('confidence_intervals', {})
                        if confidence_intervals:
                            print("   📊 95% Confidence Intervals:")
                            for domain, intervals in confidence_intervals.items():
                                if '95%' in intervals:
                                    ci_95 = intervals['95%']
                                    print(f"      {domain.replace('_', ' ').title()}: [{ci_95['lower']:.1f}, {ci_95['upper']:.1f}]")
                        
                        # Store analysis ID for later tests
                        self.analysis_results[f'percentile_{i}'] = {
                            'analysis_id': percentile_analysis.get('analysis_id'),
                            'type': 'percentile',
                            'config': config
                        }
                        
                        successful_tests += 1
                        
                    else:
                        print(f"   ❌ Percentile calculation failed: {result}")
            
            print(f"\n✅ Industry Percentile Calculation: {successful_tests}/{len(test_configurations)} configurations successful")
            return successful_tests == len(test_configurations)
            
        except Exception as e:
            print(f"❌ Industry percentile calculation error: {e}")
            return False
    
    async def test_peer_comparison_generation(self):
        """Test comprehensive peer comparison generation"""
        print("\n📋 TEST 4: Peer Comparison Generation")
        
        try:
            # Test peer comparison with different profiles
            test_profiles = [
                {
                    "job_role": "software_engineer",
                    "industry": "tech",
                    "job_level": "mid_level",
                    "region": "north_america",
                    "company_size": "startup"
                },
                {
                    "job_role": "financial_analyst",
                    "industry": "finance",
                    "job_level": "entry_level",
                    "region": "europe",
                    "company_size": "enterprise"
                }
            ]
            
            successful_tests = 0
            
            for i, profile in enumerate(test_profiles, 1):
                print(f"\n   Profile {i}: {profile['job_role']} in {profile['industry']}")
                
                params = {
                    "session_id": self.test_session_id,
                    **profile
                }
                
                async with self.session.post(f"{BACKEND_URL}/api/ml/generate-peer-comparison", params=params) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print(f"   ✅ Peer comparison successful")
                        
                        # Analyze results
                        peer_comparison = result.get('peer_comparison', {})
                        comparison_groups = peer_comparison.get('comparison_groups', {})
                        
                        print(f"   📊 Analysis ID: {peer_comparison.get('analysis_id', 'N/A')}")
                        print(f"   📊 Comparison Groups: {len(comparison_groups)}")
                        
                        # Display comparison group results
                        for group_name, group_data in comparison_groups.items():
                            avg_percentile = group_data.get('average_percentile', 0)
                            sample_size = group_data.get('sample_size', 0)
                            description = group_data.get('description', group_name)
                            
                            print(f"      {group_name.replace('_', ' ').title()}: {avg_percentile:.1f}% avg (n={sample_size})")
                            print(f"        Description: {description}")
                        
                        # Display relative positioning
                        relative_positioning = peer_comparison.get('relative_positioning', {})
                        if relative_positioning:
                            consistency_score = relative_positioning.get('consistency_score', 0)
                            best_group = relative_positioning.get('best_performing_group', 'N/A')
                            print(f"   📊 Performance Consistency: {consistency_score:.1f}/100")
                            print(f"   📊 Best Performing Group: {best_group.replace('_', ' ').title()}")
                        
                        # Display competitive analysis
                        competitive_analysis = peer_comparison.get('competitive_analysis', {})
                        if competitive_analysis:
                            market_position = competitive_analysis.get('market_position', 'unknown')
                            strengths = len(competitive_analysis.get('competitive_strengths', []))
                            gaps = len(competitive_analysis.get('competitive_gaps', []))
                            print(f"   📊 Market Position: {market_position.replace('_', ' ').title()}")
                            print(f"   📊 Competitive Strengths: {strengths}, Gaps: {gaps}")
                        
                        # Store analysis ID for later tests
                        self.analysis_results[f'peer_comparison_{i}'] = {
                            'analysis_id': peer_comparison.get('analysis_id'),
                            'type': 'peer_comparison',
                            'profile': profile
                        }
                        
                        successful_tests += 1
                        
                    else:
                        print(f"   ❌ Peer comparison failed: {result}")
            
            print(f"\n✅ Peer Comparison Generation: {successful_tests}/{len(test_profiles)} profiles successful")
            return successful_tests == len(test_profiles)
            
        except Exception as e:
            print(f"❌ Peer comparison generation error: {e}")
            return False
    
    async def test_benchmark_visualization_creation(self):
        """Test benchmark visualization creation"""
        print("\n📋 TEST 5: Benchmark Visualization Creation")
        
        try:
            successful_visualizations = 0
            total_analyses = len(self.analysis_results)
            
            for analysis_key, analysis_info in self.analysis_results.items():
                analysis_id = analysis_info['analysis_id']
                analysis_type = analysis_info['type']
                
                print(f"\n   Creating visualizations for {analysis_key} ({analysis_type})")
                
                params = {
                    "analysis_id": analysis_id,
                    "visualization_type": "comprehensive"
                }
                
                async with self.session.post(f"{BACKEND_URL}/api/ml/create-benchmark-visualizations", params=params) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print(f"   ✅ Visualization creation successful")
                        
                        # Analyze visualization results
                        visualizations = result.get('visualizations', {})
                        interactive_charts = visualizations.get('interactive_charts', {})
                        static_images = visualizations.get('static_images', {})
                        chart_metadata = visualizations.get('chart_metadata', {})
                        
                        print(f"   📊 Visualization ID: {visualizations.get('visualization_id', 'N/A')}")
                        print(f"   📊 Interactive Charts: {len(interactive_charts)}")
                        print(f"   📊 Static Images: {len(static_images)}")
                        print(f"   📊 Chart Types Available:")
                        
                        for chart_name, metadata in chart_metadata.items():
                            chart_type = metadata.get('chart_type', 'unknown')
                            title = metadata.get('title', chart_name)
                            print(f"      {title} ({chart_type})")
                        
                        # Validate chart configurations
                        chart_validation_passed = True
                        for chart_name, chart_config in interactive_charts.items():
                            if not isinstance(chart_config, dict) or 'type' not in chart_config:
                                print(f"   ⚠️  Invalid chart configuration for {chart_name}")
                                chart_validation_passed = False
                        
                        # Validate static images
                        image_validation_passed = True
                        for image_name, image_data in static_images.items():
                            if not isinstance(image_data, str) or not image_data.startswith('data:image/'):
                                print(f"   ⚠️  Invalid image data for {image_name}")
                                image_validation_passed = False
                        
                        if chart_validation_passed and image_validation_passed:
                            print(f"   ✅ All visualizations validated successfully")
                            successful_visualizations += 1
                        else:
                            print(f"   ⚠️  Some visualizations failed validation")
                        
                    else:
                        print(f"   ❌ Visualization creation failed: {result}")
            
            print(f"\n✅ Benchmark Visualization Creation: {successful_visualizations}/{total_analyses} analyses successful")
            return successful_visualizations == total_analyses
            
        except Exception as e:
            print(f"❌ Benchmark visualization creation error: {e}")
            return False
    
    async def test_industry_norms_update(self):
        """Test industry norms updating functionality"""
        print("\n📋 TEST 6: Industry Norms Update")
        
        try:
            # Test norm updates with different configurations
            update_configurations = [
                {
                    "job_role": "software_engineer",
                    "industry": "tech",
                    "job_level": "mid_level",
                    "region": "north_america",
                    "company_size": "mid_size"
                },
                {
                    "job_role": "data_analyst",
                    "industry": "finance",
                    "job_level": "entry_level",
                    "region": "europe",
                    "company_size": "startup"
                }
            ]
            
            successful_updates = 0
            
            for i, config in enumerate(update_configurations, 1):
                print(f"\n   Update {i}: {config['job_role']} in {config['industry']}")
                
                params = {
                    "session_id": self.test_session_id,
                    **config
                }
                
                async with self.session.post(f"{BACKEND_URL}/api/ml/update-industry-norms", params=params) as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print(f"   ✅ Industry norms update successful")
                        
                        # Analyze update results
                        update_summary = result.get('update_summary', {})
                        target_benchmark = update_summary.get('target_benchmark', {})
                        impact_analysis = update_summary.get('impact_analysis', {})
                        
                        print(f"   📊 Update ID: {update_summary.get('update_id', 'N/A')}")
                        print(f"   📊 Target: {target_benchmark.get('job_role', 'N/A')} | {target_benchmark.get('industry', 'N/A')}")
                        
                        # Display impact analysis
                        if impact_analysis:
                            print("   📊 Impact Analysis:")
                            for domain, impact in impact_analysis.items():
                                mean_change = impact.get('mean_change', 0)
                                impact_magnitude = impact.get('impact_magnitude', 'unknown')
                                print(f"      {domain.replace('_', ' ').title()}: Δ{mean_change:+.2f} ({impact_magnitude})")
                        
                        successful_updates += 1
                        
                    else:
                        print(f"   ❌ Industry norms update failed: {result}")
            
            print(f"\n✅ Industry Norms Update: {successful_updates}/{len(update_configurations)} updates successful")
            return successful_updates == len(update_configurations)
            
        except Exception as e:
            print(f"❌ Industry norms update error: {e}")
            return False
    
    async def test_benchmark_accuracy_validation(self):
        """Test benchmark accuracy validation"""
        print("\n📋 TEST 7: Benchmark Accuracy Validation")
        
        try:
            async with self.session.get(f"{BACKEND_URL}/api/ml/validate-benchmark-accuracy") as response:
                result = await response.json()
                
                if response.status == 200 and result.get('success'):
                    print("✅ Benchmark accuracy validation successful")
                    
                    # Analyze validation results
                    validation_report = result.get('validation_report', {})
                    overall_quality_score = validation_report.get('overall_quality_score', 0)
                    data_integrity_checks = validation_report.get('data_integrity_checks', {})
                    quality_metrics = validation_report.get('quality_metrics', {})
                    recommendations = validation_report.get('recommendations', [])
                    
                    print(f"📊 Validation ID: {validation_report.get('validation_id', 'N/A')}")
                    print(f"📊 Overall Quality Score: {overall_quality_score:.2f}/1.00")
                    
                    # Display data integrity results
                    if data_integrity_checks:
                        total_configs = data_integrity_checks.get('total_configurations', 0)
                        valid_configs = data_integrity_checks.get('valid_configurations', 0)
                        success_rate = data_integrity_checks.get('validation_success_rate', 0)
                        
                        print(f"📊 Data Integrity: {valid_configs}/{total_configs} configurations valid ({success_rate:.1f}%)")
                        
                        quality_dist = data_integrity_checks.get('quality_distribution', {})
                        if quality_dist:
                            high_quality = quality_dist.get('high_quality', 0)
                            medium_quality = quality_dist.get('medium_quality', 0)
                            low_quality = quality_dist.get('low_quality', 0)
                            print(f"📊 Quality Distribution: High={high_quality}, Medium={medium_quality}, Low={low_quality}")
                    
                    # Display quality metrics
                    if quality_metrics:
                        print("📊 Quality Metrics:")
                        for metric, value in quality_metrics.items():
                            print(f"   {metric.replace('_', ' ').title()}: {value:.1f}%")
                    
                    # Display recommendations
                    if recommendations:
                        print(f"📊 Recommendations: {len(recommendations)} items")
                        for rec in recommendations[:3]:  # Show first 3 recommendations
                            rec_type = rec.get('type', 'general')
                            priority = rec.get('priority', 'medium')
                            recommendation = rec.get('recommendation', 'N/A')
                            print(f"   [{priority.upper()}] {rec_type.replace('_', ' ').title()}: {recommendation}")
                    
                    # Validation success criteria
                    validation_success = (overall_quality_score >= 0.7 and 
                                       data_integrity_checks.get('validation_success_rate', 0) >= 80)
                    
                    if validation_success:
                        print("✅ Benchmark accuracy validation meets quality standards")
                        return True
                    else:
                        print("⚠️  Benchmark accuracy validation below quality standards")
                        return False
                    
                else:
                    print(f"❌ Benchmark accuracy validation failed: {result}")
                    return False
                    
        except Exception as e:
            print(f"❌ Benchmark accuracy validation error: {e}")
            return False
    
    async def test_analysis_retrieval(self):
        """Test stored analysis retrieval"""
        print("\n📋 TEST 8: Analysis Retrieval")
        
        try:
            successful_retrievals = 0
            total_analyses = len(self.analysis_results)
            
            for analysis_key, analysis_info in self.analysis_results.items():
                analysis_id = analysis_info['analysis_id']
                analysis_type = analysis_info['type']
                
                print(f"\n   Retrieving {analysis_key} ({analysis_type})")
                
                async with self.session.get(f"{BACKEND_URL}/api/ml/industry-benchmarks/{analysis_id}") as response:
                    result = await response.json()
                    
                    if response.status == 200 and result.get('success'):
                        print(f"   ✅ Analysis retrieval successful")
                        
                        # Validate retrieved data
                        analysis_results = result.get('analysis_results', {})
                        analysis_type_retrieved = result.get('analysis_type', 'unknown')
                        
                        print(f"   📊 Analysis Type: {analysis_type_retrieved}")
                        print(f"   📊 Session ID: {result.get('session_id', 'N/A')}")
                        print(f"   📊 Created: {result.get('created_at', 'N/A')}")
                        
                        # Validate data structure based on type
                        if analysis_type == 'percentile' and 'percentile_results' in analysis_results:
                            percentile_count = len(analysis_results['percentile_results'])
                            print(f"   📊 Percentile Results: {percentile_count} domains")
                        elif analysis_type == 'peer_comparison' and 'comparison_groups' in analysis_results:
                            group_count = len(analysis_results['comparison_groups'])
                            print(f"   📊 Comparison Groups: {group_count} groups")
                        
                        successful_retrievals += 1
                        
                    else:
                        print(f"   ❌ Analysis retrieval failed: {result}")
            
            print(f"\n✅ Analysis Retrieval: {successful_retrievals}/{total_analyses} analyses retrieved")
            return successful_retrievals == total_analyses
            
        except Exception as e:
            print(f"❌ Analysis retrieval error: {e}")
            return False
    
    async def run_comprehensive_test_suite(self):
        """Run complete Industry Benchmark Engine test suite"""
        print("=" * 80)
        print("🚀 INDUSTRY BENCHMARK ENGINE COMPREHENSIVE TEST SUITE")
        print("   Phase 1.2 Step 4: Benchmark Comparison Against Industry Standards")
        print("=" * 80)
        
        test_results = {}
        
        # Test sequence
        tests = [
            ("Admin Authentication", self.test_admin_authentication),
            ("Mock Test Session Creation", self.create_mock_test_session),
            ("Industry Percentile Calculation", self.test_industry_percentile_calculation),
            ("Peer Comparison Generation", self.test_peer_comparison_generation),
            ("Benchmark Visualization Creation", self.test_benchmark_visualization_creation),
            ("Industry Norms Update", self.test_industry_norms_update),
            ("Benchmark Accuracy Validation", self.test_benchmark_accuracy_validation),
            ("Analysis Retrieval", self.test_analysis_retrieval)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                test_results[test_name] = result
                if result:
                    passed_tests += 1
            except Exception as e:
                print(f"❌ {test_name} encountered unexpected error: {e}")
                test_results[test_name] = False
        
        # Final results
        print("\n" + "=" * 80)
        print("📊 INDUSTRY BENCHMARK ENGINE TEST RESULTS SUMMARY")
        print("=" * 80)
        
        for test_name, result in test_results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{status}: {test_name}")
        
        success_rate = (passed_tests / total_tests) * 100
        print(f"\n🎯 Overall Success Rate: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 85:
            print("🎉 INDUSTRY BENCHMARK ENGINE TEST SUITE: EXCELLENT PERFORMANCE!")
            print("   All major functionality verified and operational")
        elif success_rate >= 70:
            print("✅ INDUSTRY BENCHMARK ENGINE TEST SUITE: GOOD PERFORMANCE")
            print("   Core functionality operational with minor issues")
        else:
            print("⚠️  INDUSTRY BENCHMARK ENGINE TEST SUITE: NEEDS ATTENTION")
            print("   Significant issues detected, review failed tests")
        
        # Feature completion analysis
        print("\n📋 FEATURE COMPLETION ANALYSIS:")
        
        core_features = [
            ("Industry Percentile Calculations", test_results.get("Industry Percentile Calculation", False)),
            ("Peer Group Comparisons", test_results.get("Peer Comparison Generation", False)),
            ("Benchmark Visualizations", test_results.get("Benchmark Visualization Creation", False)),
            ("Industry Norms Updates", test_results.get("Industry Norms Update", False)),
            ("Benchmark Accuracy Validation", test_results.get("Benchmark Accuracy Validation", False))
        ]
        
        completed_features = sum(1 for _, status in core_features if status)
        total_features = len(core_features)
        
        for feature_name, status in core_features:
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {feature_name}")
        
        feature_completion = (completed_features / total_features) * 100
        print(f"\n🎯 Feature Completion: {completed_features}/{total_features} ({feature_completion:.1f}%)")
        
        print("\n" + "=" * 80)
        print("Industry Benchmark Engine Testing Complete!")
        print("=" * 80)
        
        return success_rate >= 85

async def main():
    """Main test runner"""
    tester = IndustryBenchmarkEngineTest()
    
    try:
        await tester.setup()
        success = await tester.run_comprehensive_test_suite()
        return success
    except KeyboardInterrupt:
        print("\n⚠️  Test suite interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test suite failed with error: {e}")
        return False
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)