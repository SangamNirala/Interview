"""
Industry Benchmark Engine
Phase 1.2 Step 4: Benchmark Comparison Against Industry Standards

This module implements comprehensive industry benchmarking capabilities:
- Industry benchmark database with comprehensive mock data
- Percentile ranking system with confidence intervals
- Multi-dimensional comparison (overall, by topic, by difficulty level)
- Norm-referenced scoring against relevant peer groups
- Benchmark visualization generation (interactive and static)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from datetime import datetime, timedelta
import logging
import json
import math
from scipy import stats
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import warnings
import uuid
import base64
import io
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndustryBenchmarkEngine:
    """
    Advanced Industry Benchmarking Engine
    
    Features:
    - Comprehensive industry benchmark database with multi-dimensional criteria
    - Percentile ranking system with statistical confidence intervals
    - Peer comparison against relevant job roles, industries, experience levels
    - Multi-dimensional analysis (overall, topic-wise, difficulty-wise)
    - Interactive and static visualization generation
    - Dynamic benchmark updating and validation
    """
    
    def __init__(self):
        # Initialize comprehensive industry benchmark database
        self.industry_benchmarks = self._initialize_benchmark_database()
        
        # Reasoning domains for benchmarking
        self.reasoning_domains = [
            'numerical_reasoning', 'logical_reasoning', 
            'verbal_comprehension', 'spatial_reasoning'
        ]
        
        # Benchmark dimensions
        self.job_levels = ['entry_level', 'mid_level', 'senior_level']
        self.industries = ['tech', 'finance', 'healthcare', 'education', 'consulting', 'manufacturing']
        self.regions = ['north_america', 'europe', 'asia_pacific']
        self.company_sizes = ['startup', 'mid_size', 'enterprise']
        
        # Statistical parameters
        self.confidence_levels = [0.80, 0.90, 0.95, 0.99]
        
        # Visualization settings
        plt.style.use('default')
        sns.set_palette("husl")
        
    def _initialize_benchmark_database(self) -> Dict[str, Any]:
        """
        Initialize comprehensive industry benchmark database with realistic mock data
        
        Returns:
            Dictionary containing benchmark data across multiple dimensions
        """
        
        # Job role definitions with industry-specific variations
        job_roles = {
            'software_engineer': {
                'title': 'Software Engineer',
                'primary_industries': ['tech', 'finance', 'healthcare'],
                'domain_weights': {
                    'numerical_reasoning': 0.25,
                    'logical_reasoning': 0.35,
                    'verbal_comprehension': 0.20,
                    'spatial_reasoning': 0.20
                }
            },
            'data_analyst': {
                'title': 'Data Analyst',
                'primary_industries': ['tech', 'finance', 'consulting'],
                'domain_weights': {
                    'numerical_reasoning': 0.40,
                    'logical_reasoning': 0.30,
                    'verbal_comprehension': 0.20,
                    'spatial_reasoning': 0.10
                }
            },
            'project_manager': {
                'title': 'Project Manager',
                'primary_industries': ['tech', 'consulting', 'manufacturing'],
                'domain_weights': {
                    'numerical_reasoning': 0.20,
                    'logical_reasoning': 0.30,
                    'verbal_comprehension': 0.35,
                    'spatial_reasoning': 0.15
                }
            },
            'financial_analyst': {
                'title': 'Financial Analyst',
                'primary_industries': ['finance', 'consulting'],
                'domain_weights': {
                    'numerical_reasoning': 0.45,
                    'logical_reasoning': 0.25,
                    'verbal_comprehension': 0.25,
                    'spatial_reasoning': 0.05
                }
            },
            'healthcare_analyst': {
                'title': 'Healthcare Analyst',
                'primary_industries': ['healthcare'],
                'domain_weights': {
                    'numerical_reasoning': 0.35,
                    'logical_reasoning': 0.25,
                    'verbal_comprehension': 0.30,
                    'spatial_reasoning': 0.10
                }
            },
            'education_coordinator': {
                'title': 'Education Coordinator',
                'primary_industries': ['education'],
                'domain_weights': {
                    'numerical_reasoning': 0.15,
                    'logical_reasoning': 0.25,
                    'verbal_comprehension': 0.45,
                    'spatial_reasoning': 0.15
                }
            }
        }
        
        # Industry-specific performance modifiers
        industry_modifiers = {
            'tech': {
                'base_multiplier': 1.10,
                'domain_boosts': {
                    'logical_reasoning': 0.15,
                    'numerical_reasoning': 0.10
                }
            },
            'finance': {
                'base_multiplier': 1.05,
                'domain_boosts': {
                    'numerical_reasoning': 0.20,
                    'logical_reasoning': 0.10
                }
            },
            'healthcare': {
                'base_multiplier': 1.00,
                'domain_boosts': {
                    'verbal_comprehension': 0.15,
                    'logical_reasoning': 0.10
                }
            },
            'education': {
                'base_multiplier': 0.95,
                'domain_boosts': {
                    'verbal_comprehension': 0.20,
                    'spatial_reasoning': 0.10
                }
            },
            'consulting': {
                'base_multiplier': 1.08,
                'domain_boosts': {
                    'logical_reasoning': 0.15,
                    'verbal_comprehension': 0.15
                }
            },
            'manufacturing': {
                'base_multiplier': 0.98,
                'domain_boosts': {
                    'spatial_reasoning': 0.20,
                    'numerical_reasoning': 0.10
                }
            }
        }
        
        # Regional performance variations
        regional_modifiers = {
            'north_america': {'multiplier': 1.05, 'std_adjustment': 0.95},
            'europe': {'multiplier': 1.02, 'std_adjustment': 0.90},
            'asia_pacific': {'multiplier': 1.08, 'std_adjustment': 1.10}
        }
        
        # Company size performance impact
        company_size_modifiers = {
            'startup': {'multiplier': 1.02, 'std_adjustment': 1.15},
            'mid_size': {'multiplier': 1.00, 'std_adjustment': 1.00},
            'enterprise': {'multiplier': 1.06, 'std_adjustment': 0.85}
        }
        
        # Generate comprehensive benchmark database
        benchmark_data = {}
        
        # Base performance levels by job level
        base_performances = {
            'entry_level': {
                'numerical_reasoning': {'mean': 45.0, 'std': 12.0},
                'logical_reasoning': {'mean': 42.0, 'std': 13.0},
                'verbal_comprehension': {'mean': 48.0, 'std': 11.0},
                'spatial_reasoning': {'mean': 40.0, 'std': 14.0}
            },
            'mid_level': {
                'numerical_reasoning': {'mean': 65.0, 'std': 10.0},
                'logical_reasoning': {'mean': 62.0, 'std': 11.0},
                'verbal_comprehension': {'mean': 68.0, 'std': 9.0},
                'spatial_reasoning': {'mean': 58.0, 'std': 12.0}
            },
            'senior_level': {
                'numerical_reasoning': {'mean': 78.0, 'std': 8.0},
                'logical_reasoning': {'mean': 75.0, 'std': 9.0},
                'verbal_comprehension': {'mean': 80.0, 'std': 7.0},
                'spatial_reasoning': {'mean': 70.0, 'std': 10.0}
            }
        }
        
        # Generate benchmark data for all combinations
        for job_role, role_info in job_roles.items():
            benchmark_data[job_role] = {}
            
            for job_level in self.job_levels:
                benchmark_data[job_role][job_level] = {}
                
                for industry in self.industries:
                    benchmark_data[job_role][job_level][industry] = {}
                    
                    for region in self.regions:
                        benchmark_data[job_role][job_level][industry][region] = {}
                        
                        for company_size in self.company_sizes:
                            # Calculate adjusted performance statistics
                            domain_stats = {}
                            
                            for domain in self.reasoning_domains:
                                base_stats = base_performances[job_level][domain]
                                
                                # Apply industry modifier
                                industry_mod = industry_modifiers.get(industry, {'base_multiplier': 1.0, 'domain_boosts': {}})
                                domain_boost = industry_mod['domain_boosts'].get(domain, 0.0)
                                
                                # Apply regional modifier
                                regional_mod = regional_modifiers[region]
                                
                                # Apply company size modifier
                                company_mod = company_size_modifiers[company_size]
                                
                                # Calculate final statistics
                                adjusted_mean = (
                                    base_stats['mean'] * 
                                    industry_mod['base_multiplier'] * 
                                    regional_mod['multiplier'] * 
                                    company_mod['multiplier'] * 
                                    (1 + domain_boost)
                                )
                                
                                adjusted_std = (
                                    base_stats['std'] * 
                                    regional_mod['std_adjustment'] * 
                                    company_mod['std_adjustment']
                                )
                                
                                # Generate sample data points for percentile calculations
                                sample_size = 1000
                                samples = np.random.normal(adjusted_mean, adjusted_std, sample_size)
                                samples = np.clip(samples, 0, 100)  # Ensure scores are within 0-100
                                
                                domain_stats[domain] = {
                                    'mean': float(adjusted_mean),
                                    'std': float(adjusted_std),
                                    'percentiles': {
                                        '10th': float(np.percentile(samples, 10)),
                                        '25th': float(np.percentile(samples, 25)),
                                        '50th': float(np.percentile(samples, 50)),
                                        '75th': float(np.percentile(samples, 75)),
                                        '90th': float(np.percentile(samples, 90)),
                                        '95th': float(np.percentile(samples, 95)),
                                        '99th': float(np.percentile(samples, 99))
                                    },
                                    'sample_size': sample_size,
                                    'samples': samples.tolist()
                                }
                            
                            # Calculate overall composite score
                            composite_samples = []
                            weights = role_info['domain_weights']
                            
                            for i in range(sample_size):
                                composite_score = sum(
                                    domain_stats[domain]['samples'][i] * weights[domain]
                                    for domain in self.reasoning_domains
                                )
                                composite_samples.append(composite_score)
                            
                            composite_samples = np.array(composite_samples)
                            
                            benchmark_data[job_role][job_level][industry][region][company_size] = {
                                'domain_stats': domain_stats,
                                'composite_stats': {
                                    'mean': float(np.mean(composite_samples)),
                                    'std': float(np.std(composite_samples)),
                                    'percentiles': {
                                        '10th': float(np.percentile(composite_samples, 10)),
                                        '25th': float(np.percentile(composite_samples, 25)),
                                        '50th': float(np.percentile(composite_samples, 50)),
                                        '75th': float(np.percentile(composite_samples, 75)),
                                        '90th': float(np.percentile(composite_samples, 90)),
                                        '95th': float(np.percentile(composite_samples, 95)),
                                        '99th': float(np.percentile(composite_samples, 99))
                                    },
                                    'sample_size': sample_size,
                                    'samples': composite_samples.tolist()
                                },
                                'job_role_weights': weights,
                                'last_updated': datetime.utcnow().isoformat(),
                                'metadata': {
                                    'industry_primary': industry in role_info['primary_industries'],
                                    'region': region,
                                    'company_size': company_size,
                                    'sample_generation_method': 'statistical_simulation'
                                }
                            }
        
        return benchmark_data
    
    def calculate_industry_percentiles(
        self, 
        score: Union[float, Dict[str, float]], 
        job_role: str, 
        industry: str,
        job_level: str = 'mid_level',
        region: str = 'north_america',
        company_size: str = 'mid_size'
    ) -> Dict[str, Any]:
        """
        Calculate industry percentiles for given score(s) and demographic profile
        
        Args:
            score: Either composite score (float) or domain scores (dict)
            job_role: Target job role for comparison
            industry: Industry for benchmarking
            job_level: Career level (entry_level, mid_level, senior_level)
            region: Geographic region
            company_size: Company size category
            
        Returns:
            Comprehensive percentile analysis with confidence intervals
        """
        try:
            # Validate inputs
            if job_role not in self.industry_benchmarks:
                raise ValueError(f"Job role '{job_role}' not found in benchmark database")
            
            benchmark_path = self.industry_benchmarks[job_role][job_level][industry][region][company_size]
            
            percentile_analysis = {
                'analysis_id': str(uuid.uuid4()),
                'input_profile': {
                    'job_role': job_role,
                    'industry': industry,
                    'job_level': job_level,
                    'region': region,
                    'company_size': company_size
                },
                'percentile_results': {},
                'confidence_intervals': {},
                'performance_classification': {},
                'peer_comparison_summary': {},
                'benchmark_metadata': benchmark_path['metadata'],
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            if isinstance(score, dict):
                # Domain-wise percentile analysis
                for domain, domain_score in score.items():
                    if domain in self.reasoning_domains:
                        domain_stats = benchmark_path['domain_stats'][domain]
                        samples = np.array(domain_stats['samples'])
                        
                        # Calculate exact percentile
                        percentile = float(stats.percentileofscore(samples, domain_score))
                        
                        # Calculate confidence intervals
                        confidence_intervals = {}
                        for conf_level in self.confidence_levels:
                            n = len(samples)
                            se = math.sqrt(percentile * (100 - percentile) / n)
                            z_score = stats.norm.ppf((1 + conf_level) / 2)
                            margin = z_score * se
                            
                            confidence_intervals[f'{int(conf_level*100)}%'] = {
                                'lower': max(0, percentile - margin),
                                'upper': min(100, percentile + margin)
                            }
                        
                        # Performance classification
                        if percentile >= 90:
                            classification = 'exceptional'
                        elif percentile >= 75:
                            classification = 'above_average'
                        elif percentile >= 25:
                            classification = 'average'
                        elif percentile >= 10:
                            classification = 'below_average'
                        else:
                            classification = 'needs_improvement'
                        
                        percentile_analysis['percentile_results'][domain] = {
                            'score': domain_score,
                            'percentile': percentile,
                            'benchmark_mean': domain_stats['mean'],
                            'benchmark_std': domain_stats['std'],
                            'z_score': (domain_score - domain_stats['mean']) / domain_stats['std'],
                            'standard_deviations_from_mean': abs(domain_score - domain_stats['mean']) / domain_stats['std']
                        }
                        
                        percentile_analysis['confidence_intervals'][domain] = confidence_intervals
                        percentile_analysis['performance_classification'][domain] = classification
                
                # Calculate composite percentile if all domains present
                if len(score) == len(self.reasoning_domains):
                    weights = benchmark_path['job_role_weights']
                    composite_score = sum(score[domain] * weights[domain] for domain in self.reasoning_domains)
                    
                    composite_stats = benchmark_path['composite_stats']
                    composite_samples = np.array(composite_stats['samples'])
                    composite_percentile = float(stats.percentileofscore(composite_samples, composite_score))
                    
                    percentile_analysis['percentile_results']['composite'] = {
                        'score': composite_score,
                        'percentile': composite_percentile,
                        'benchmark_mean': composite_stats['mean'],
                        'benchmark_std': composite_stats['std'],
                        'z_score': (composite_score - composite_stats['mean']) / composite_stats['std']
                    }
            
            else:
                # Single composite score analysis
                composite_stats = benchmark_path['composite_stats']
                composite_samples = np.array(composite_stats['samples'])
                percentile = float(stats.percentileofscore(composite_samples, score))
                
                # Confidence intervals
                confidence_intervals = {}
                for conf_level in self.confidence_levels:
                    n = len(composite_samples)
                    se = math.sqrt(percentile * (100 - percentile) / n)
                    z_score = stats.norm.ppf((1 + conf_level) / 2)
                    margin = z_score * se
                    
                    confidence_intervals[f'{int(conf_level*100)}%'] = {
                        'lower': max(0, percentile - margin),
                        'upper': min(100, percentile + margin)
                    }
                
                percentile_analysis['percentile_results']['composite'] = {
                    'score': score,
                    'percentile': percentile,
                    'benchmark_mean': composite_stats['mean'],
                    'benchmark_std': composite_stats['std'],
                    'z_score': (score - composite_stats['mean']) / composite_stats['std']
                }
                
                percentile_analysis['confidence_intervals']['composite'] = confidence_intervals
            
            # Generate peer comparison summary
            percentile_analysis['peer_comparison_summary'] = self._generate_peer_comparison_summary(
                percentile_analysis['percentile_results']
            )
            
            return percentile_analysis
            
        except Exception as e:
            logger.error(f"Error calculating industry percentiles: {e}")
            raise
    
    def generate_peer_comparison(self, candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive peer comparison across multiple benchmark groups
        
        Args:
            candidate_profile: Dictionary containing candidate data and demographics
            
        Returns:
            Multi-dimensional peer comparison analysis
        """
        try:
            analysis_id = str(uuid.uuid4())
            
            # Extract candidate information
            scores = candidate_profile.get('scores', {})
            job_role = candidate_profile.get('job_role', 'software_engineer')
            target_industry = candidate_profile.get('industry', 'tech')
            job_level = candidate_profile.get('job_level', 'mid_level')
            region = candidate_profile.get('region', 'north_america')
            company_size = candidate_profile.get('company_size', 'mid_size')
            
            peer_comparison = {
                'analysis_id': analysis_id,
                'candidate_profile': candidate_profile,
                'comparison_groups': {},
                'relative_positioning': {},
                'competitive_analysis': {},
                'recommendations': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            # Define comparison groups
            comparison_groups = [
                {
                    'name': 'exact_peers',
                    'description': f'{job_role.replace("_", " ").title()} in {target_industry.title()}',
                    'filters': {
                        'job_role': job_role,
                        'industry': target_industry,
                        'job_level': job_level,
                        'region': region,
                        'company_size': company_size
                    }
                },
                {
                    'name': 'same_role_all_industries',
                    'description': f'{job_role.replace("_", " ").title()} across all industries',
                    'filters': {
                        'job_role': job_role,
                        'job_level': job_level,
                        'region': region,
                        'company_size': company_size
                    }
                },
                {
                    'name': 'same_industry_all_roles',
                    'description': f'All roles in {target_industry.title()}',
                    'filters': {
                        'industry': target_industry,
                        'job_level': job_level,
                        'region': region,
                        'company_size': company_size
                    }
                },
                {
                    'name': 'regional_peers',
                    'description': f'Regional comparison in {region.replace("_", " ").title()}',
                    'filters': {
                        'job_level': job_level,
                        'region': region
                    }
                }
            ]
            
            # Perform comparison for each group
            for group in comparison_groups:
                group_results = []
                
                if group['name'] == 'exact_peers':
                    # Direct percentile calculation for exact peer group
                    percentile_results = self.calculate_industry_percentiles(
                        scores, job_role, target_industry, job_level, region, company_size
                    )
                    group_results.append({
                        'configuration': group['filters'],
                        'percentile_analysis': percentile_results
                    })
                
                elif group['name'] == 'same_role_all_industries':
                    # Compare across all industries for same role
                    for industry in self.industries:
                        if industry in self.industry_benchmarks[job_role][job_level]:
                            percentile_results = self.calculate_industry_percentiles(
                                scores, job_role, industry, job_level, region, company_size
                            )
                            group_results.append({
                                'configuration': {**group['filters'], 'industry': industry},
                                'percentile_analysis': percentile_results
                            })
                
                elif group['name'] == 'same_industry_all_roles':
                    # Compare across all roles in same industry
                    for role in self.industry_benchmarks.keys():
                        if target_industry in self.industry_benchmarks[role][job_level]:
                            percentile_results = self.calculate_industry_percentiles(
                                scores, role, target_industry, job_level, region, company_size
                            )
                            group_results.append({
                                'configuration': {**group['filters'], 'job_role': role},
                                'percentile_analysis': percentile_results
                            })
                
                elif group['name'] == 'regional_peers':
                    # Regional comparison across multiple roles and industries
                    role_count = 0
                    for role in list(self.industry_benchmarks.keys())[:3]:  # Sample 3 roles
                        for industry in list(self.industries)[:3]:  # Sample 3 industries
                            if industry in self.industry_benchmarks[role][job_level]:
                                percentile_results = self.calculate_industry_percentiles(
                                    scores, role, industry, job_level, region, company_size
                                )
                                group_results.append({
                                    'configuration': {**group['filters'], 'job_role': role, 'industry': industry},
                                    'percentile_analysis': percentile_results
                                })
                                role_count += 1
                                if role_count >= 6:  # Limit to 6 comparisons for regional
                                    break
                        if role_count >= 6:
                            break
                
                # Analyze group results
                if group_results:
                    composite_percentiles = []
                    for result in group_results:
                        if 'composite' in result['percentile_analysis']['percentile_results']:
                            composite_percentiles.append(
                                result['percentile_analysis']['percentile_results']['composite']['percentile']
                            )
                    
                    if composite_percentiles:
                        peer_comparison['comparison_groups'][group['name']] = {
                            'description': group['description'],
                            'sample_size': len(group_results),
                            'average_percentile': float(np.mean(composite_percentiles)),
                            'percentile_range': {
                                'min': float(np.min(composite_percentiles)),
                                'max': float(np.max(composite_percentiles))
                            },
                            'percentile_std': float(np.std(composite_percentiles)),
                            'detailed_comparisons': group_results[:5],  # Store top 5 detailed comparisons
                            'performance_consistency': 'high' if np.std(composite_percentiles) < 10 else 'medium' if np.std(composite_percentiles) < 20 else 'low'
                        }
            
            # Generate relative positioning analysis
            peer_comparison['relative_positioning'] = self._analyze_relative_positioning(
                peer_comparison['comparison_groups']
            )
            
            # Generate competitive analysis
            peer_comparison['competitive_analysis'] = self._generate_competitive_analysis(
                scores, peer_comparison['comparison_groups']
            )
            
            # Generate recommendations
            peer_comparison['recommendations'] = self._generate_benchmark_recommendations(
                peer_comparison['comparison_groups'], peer_comparison['competitive_analysis']
            )
            
            return peer_comparison
            
        except Exception as e:
            logger.error(f"Error generating peer comparison: {e}")
            raise
    
    def create_benchmark_visualizations(
        self, 
        analysis_data: Dict[str, Any],
        visualization_type: str = 'comprehensive'
    ) -> Dict[str, Any]:
        """
        Create comprehensive benchmark visualizations (both interactive and static)
        
        Args:
            analysis_data: Analysis results from percentile or peer comparison
            visualization_type: Type of visualization ('percentile', 'peer_comparison', 'comprehensive')
            
        Returns:
            Dictionary containing visualization data and static chart images
        """
        try:
            viz_id = str(uuid.uuid4())
            
            visualizations = {
                'visualization_id': viz_id,
                'analysis_id': analysis_data.get('analysis_id', 'unknown'),
                'visualization_type': visualization_type,
                'interactive_charts': {},
                'static_images': {},
                'chart_metadata': {},
                'created_at': datetime.utcnow().isoformat()
            }
            
            # Create percentile radar chart
            if 'percentile_results' in analysis_data:
                radar_data = self._create_percentile_radar_chart(analysis_data['percentile_results'])
                visualizations['interactive_charts']['percentile_radar'] = radar_data['chart_config']
                visualizations['static_images']['percentile_radar'] = radar_data['static_image']
            
            # Create peer comparison bar chart
            if 'comparison_groups' in analysis_data:
                bar_data = self._create_peer_comparison_bar_chart(analysis_data['comparison_groups'])
                visualizations['interactive_charts']['peer_comparison_bars'] = bar_data['chart_config']
                visualizations['static_images']['peer_comparison_bars'] = bar_data['static_image']
            
            # Create performance distribution chart
            distribution_data = self._create_performance_distribution_chart(analysis_data)
            visualizations['interactive_charts']['performance_distribution'] = distribution_data['chart_config']
            visualizations['static_images']['performance_distribution'] = distribution_data['static_image']
            
            # Create benchmark positioning chart
            positioning_data = self._create_benchmark_positioning_chart(analysis_data)
            visualizations['interactive_charts']['benchmark_positioning'] = positioning_data['chart_config']
            visualizations['static_images']['benchmark_positioning'] = positioning_data['static_image']
            
            # Chart metadata for frontend rendering
            visualizations['chart_metadata'] = {
                'percentile_radar': {
                    'title': 'Domain Performance Percentiles',
                    'description': 'Your performance percentiles across different reasoning domains',
                    'chart_type': 'radar',
                    'recommended_height': 400
                },
                'peer_comparison_bars': {
                    'title': 'Peer Group Comparisons',
                    'description': 'Average percentile performance across different peer groups',
                    'chart_type': 'bar',
                    'recommended_height': 300
                },
                'performance_distribution': {
                    'title': 'Performance Distribution',
                    'description': 'Your position within the performance distribution curve',
                    'chart_type': 'histogram',
                    'recommended_height': 350
                },
                'benchmark_positioning': {
                    'title': 'Industry Position Matrix',
                    'description': 'Your position relative to industry benchmarks',
                    'chart_type': 'scatter',
                    'recommended_height': 400
                }
            }
            
            return visualizations
            
        except Exception as e:
            logger.error(f"Error creating benchmark visualizations: {e}")
            raise
    
    def update_industry_norms(self, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update industry norms with new candidate data
        
        Args:
            new_data: New candidate performance data
            
        Returns:
            Update summary and impact analysis
        """
        try:
            update_id = str(uuid.uuid4())
            
            # Extract demographic information
            job_role = new_data.get('job_role')
            industry = new_data.get('industry')
            job_level = new_data.get('job_level')
            region = new_data.get('region')
            company_size = new_data.get('company_size')
            scores = new_data.get('scores', {})
            
            if not all([job_role, industry, job_level, region, company_size]):
                raise ValueError("Missing required demographic information for benchmark update")
            
            # Locate target benchmark
            if job_role not in self.industry_benchmarks:
                raise ValueError(f"Job role '{job_role}' not found in benchmark database")
            
            benchmark_path = self.industry_benchmarks[job_role][job_level][industry][region][company_size]
            
            update_summary = {
                'update_id': update_id,
                'target_benchmark': {
                    'job_role': job_role,
                    'industry': industry,
                    'job_level': job_level,
                    'region': region,
                    'company_size': company_size
                },
                'before_update': {},
                'after_update': {},
                'impact_analysis': {},
                'update_timestamp': datetime.utcnow().isoformat()
            }
            
            # Store original statistics
            for domain in self.reasoning_domains:
                if domain in scores:
                    original_stats = benchmark_path['domain_stats'][domain]
                    update_summary['before_update'][domain] = {
                        'mean': original_stats['mean'],
                        'std': original_stats['std'],
                        'sample_size': original_stats['sample_size']
                    }
            
            # Update domain statistics
            for domain in self.reasoning_domains:
                if domain in scores:
                    domain_stats = benchmark_path['domain_stats'][domain]
                    new_score = scores[domain]
                    
                    # Update running statistics
                    current_samples = np.array(domain_stats['samples'])
                    updated_samples = np.append(current_samples, new_score)
                    
                    # Limit sample size to prevent infinite growth
                    if len(updated_samples) > 2000:
                        updated_samples = updated_samples[-2000:]
                    
                    # Recalculate statistics
                    new_mean = float(np.mean(updated_samples))
                    new_std = float(np.std(updated_samples))
                    
                    # Update percentiles
                    new_percentiles = {
                        '10th': float(np.percentile(updated_samples, 10)),
                        '25th': float(np.percentile(updated_samples, 25)),
                        '50th': float(np.percentile(updated_samples, 50)),
                        '75th': float(np.percentile(updated_samples, 75)),
                        '90th': float(np.percentile(updated_samples, 90)),
                        '95th': float(np.percentile(updated_samples, 95)),
                        '99th': float(np.percentile(updated_samples, 99))
                    }
                    
                    # Update benchmark data
                    benchmark_path['domain_stats'][domain].update({
                        'mean': new_mean,
                        'std': new_std,
                        'percentiles': new_percentiles,
                        'sample_size': len(updated_samples),
                        'samples': updated_samples.tolist()
                    })
                    
                    # Calculate impact
                    mean_change = new_mean - update_summary['before_update'][domain]['mean']
                    std_change = new_std - update_summary['before_update'][domain]['std']
                    
                    update_summary['after_update'][domain] = {
                        'mean': new_mean,
                        'std': new_std,
                        'sample_size': len(updated_samples)
                    }
                    
                    update_summary['impact_analysis'][domain] = {
                        'mean_change': mean_change,
                        'std_change': std_change,
                        'relative_mean_change_percent': (mean_change / update_summary['before_update'][domain]['mean']) * 100,
                        'impact_magnitude': 'high' if abs(mean_change) > 2 else 'medium' if abs(mean_change) > 0.5 else 'low'
                    }
            
            # Update composite statistics
            if len(scores) == len(self.reasoning_domains):
                weights = benchmark_path['job_role_weights']
                
                # Recalculate composite samples
                composite_samples = []
                sample_size = benchmark_path['domain_stats']['numerical_reasoning']['sample_size']
                
                for i in range(sample_size):
                    composite_score = sum(
                        benchmark_path['domain_stats'][domain]['samples'][i] * weights[domain]
                        for domain in self.reasoning_domains
                    )
                    composite_samples.append(composite_score)
                
                composite_samples = np.array(composite_samples)
                
                # Update composite statistics
                benchmark_path['composite_stats'].update({
                    'mean': float(np.mean(composite_samples)),
                    'std': float(np.std(composite_samples)),
                    'percentiles': {
                        '10th': float(np.percentile(composite_samples, 10)),
                        '25th': float(np.percentile(composite_samples, 25)),
                        '50th': float(np.percentile(composite_samples, 50)),
                        '75th': float(np.percentile(composite_samples, 75)),
                        '90th': float(np.percentile(composite_samples, 90)),
                        '95th': float(np.percentile(composite_samples, 95)),
                        '99th': float(np.percentile(composite_samples, 99))
                    },
                    'sample_size': len(composite_samples),
                    'samples': composite_samples.tolist()
                })
            
            # Update metadata
            benchmark_path['last_updated'] = datetime.utcnow().isoformat()
            
            return update_summary
            
        except Exception as e:
            logger.error(f"Error updating industry norms: {e}")
            raise
    
    def validate_benchmark_accuracy(self) -> Dict[str, Any]:
        """
        Validate benchmark accuracy and data quality
        
        Returns:
            Comprehensive validation report
        """
        try:
            validation_id = str(uuid.uuid4())
            
            validation_report = {
                'validation_id': validation_id,
                'validation_timestamp': datetime.utcnow().isoformat(),
                'overall_quality_score': 0.0,
                'validation_results': {},
                'quality_metrics': {},
                'recommendations': [],
                'data_integrity_checks': {}
            }
            
            total_configurations = 0
            valid_configurations = 0
            quality_scores = []
            
            # Validate each benchmark configuration
            for job_role in self.industry_benchmarks:
                for job_level in self.job_levels:
                    for industry in self.industries:
                        if industry in self.industry_benchmarks[job_role][job_level]:
                            for region in self.regions:
                                for company_size in self.company_sizes:
                                    total_configurations += 1
                                    
                                    config_key = f"{job_role}_{job_level}_{industry}_{region}_{company_size}"
                                    benchmark_data = self.industry_benchmarks[job_role][job_level][industry][region][company_size]
                                    
                                    # Validate configuration
                                    config_validation = self._validate_benchmark_configuration(benchmark_data)
                                    validation_report['validation_results'][config_key] = config_validation
                                    
                                    if config_validation['is_valid']:
                                        valid_configurations += 1
                                        quality_scores.append(config_validation['quality_score'])
            
            # Calculate overall metrics
            validation_report['overall_quality_score'] = float(np.mean(quality_scores)) if quality_scores else 0.0
            validation_report['data_integrity_checks'] = {
                'total_configurations': total_configurations,
                'valid_configurations': valid_configurations,
                'validation_success_rate': (valid_configurations / total_configurations) * 100 if total_configurations > 0 else 0,
                'average_quality_score': validation_report['overall_quality_score'],
                'quality_distribution': {
                    'high_quality': len([s for s in quality_scores if s >= 0.8]),
                    'medium_quality': len([s for s in quality_scores if 0.6 <= s < 0.8]),
                    'low_quality': len([s for s in quality_scores if s < 0.6])
                }
            }
            
            # Generate quality metrics
            validation_report['quality_metrics'] = self._calculate_benchmark_quality_metrics()
            
            # Generate recommendations
            validation_report['recommendations'] = self._generate_validation_recommendations(
                validation_report['data_integrity_checks'],
                validation_report['quality_metrics']
            )
            
            return validation_report
            
        except Exception as e:
            logger.error(f"Error validating benchmark accuracy: {e}")
            raise
    
    def _generate_peer_comparison_summary(self, percentile_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary for peer comparison"""
        summary = {
            'overall_performance': 'average',
            'strongest_domains': [],
            'improvement_areas': [],
            'percentile_summary': {}
        }
        
        if 'composite' in percentile_results:
            composite_percentile = percentile_results['composite']['percentile']
            if composite_percentile >= 75:
                summary['overall_performance'] = 'above_average'
            elif composite_percentile >= 25:
                summary['overall_performance'] = 'average'
            else:
                summary['overall_performance'] = 'below_average'
        
        # Identify strongest and weakest domains
        domain_percentiles = []
        for domain, result in percentile_results.items():
            if domain != 'composite':
                domain_percentiles.append((domain, result['percentile']))
        
        domain_percentiles.sort(key=lambda x: x[1], reverse=True)
        
        if len(domain_percentiles) >= 2:
            summary['strongest_domains'] = [domain for domain, _ in domain_percentiles[:2]]
            summary['improvement_areas'] = [domain for domain, _ in domain_percentiles[-2:]]
        
        return summary
    
    def _analyze_relative_positioning(self, comparison_groups: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze relative positioning across peer groups"""
        positioning = {
            'consistency_score': 0.0,
            'best_performing_group': None,
            'most_competitive_group': None,
            'positioning_summary': {}
        }
        
        group_percentiles = []
        for group_name, group_data in comparison_groups.items():
            avg_percentile = group_data.get('average_percentile', 0)
            group_percentiles.append((group_name, avg_percentile))
            
            positioning['positioning_summary'][group_name] = {
                'average_percentile': avg_percentile,
                'performance_level': 'high' if avg_percentile >= 75 else 'medium' if avg_percentile >= 25 else 'low'
            }
        
        if group_percentiles:
            group_percentiles.sort(key=lambda x: x[1], reverse=True)
            positioning['best_performing_group'] = group_percentiles[0][0]
            
            # Calculate consistency (lower std = higher consistency)
            percentiles = [p for _, p in group_percentiles]
            positioning['consistency_score'] = max(0, 100 - np.std(percentiles) * 5)  # Convert to 0-100 scale
        
        return positioning
    
    def _generate_competitive_analysis(self, scores: Dict[str, float], comparison_groups: Dict[str, Any]) -> Dict[str, Any]:
        """Generate competitive analysis"""
        analysis = {
            'competitive_strengths': [],
            'competitive_gaps': [],
            'market_position': 'unknown',
            'improvement_priority': []
        }
        
        # Analyze based on peer group performance
        for group_name, group_data in comparison_groups.items():
            avg_percentile = group_data.get('average_percentile', 0)
            
            if avg_percentile >= 75:
                analysis['competitive_strengths'].append({
                    'area': group_name,
                    'advantage': f"Strong performance in {group_data.get('description', group_name)}"
                })
            elif avg_percentile < 25:
                analysis['competitive_gaps'].append({
                    'area': group_name,
                    'gap': f"Below average in {group_data.get('description', group_name)}"
                })
        
        # Determine overall market position
        all_percentiles = [group_data.get('average_percentile', 0) for group_data in comparison_groups.values()]
        if all_percentiles:
            avg_percentile = np.mean(all_percentiles)
            if avg_percentile >= 80:
                analysis['market_position'] = 'market_leader'
            elif avg_percentile >= 60:
                analysis['market_position'] = 'strong_performer'
            elif avg_percentile >= 40:
                analysis['market_position'] = 'average_performer'
            else:
                analysis['market_position'] = 'needs_improvement'
        
        return analysis
    
    def _generate_benchmark_recommendations(self, comparison_groups: Dict[str, Any], competitive_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on benchmark analysis"""
        recommendations = []
        
        # Performance-based recommendations
        if competitive_analysis['market_position'] == 'needs_improvement':
            recommendations.append({
                'type': 'performance_improvement',
                'priority': 'high',
                'title': 'Focus on Core Skill Development',
                'description': 'Your performance is below industry averages. Focus on foundational skill building.',
                'action_items': [
                    'Take targeted practice tests in weak areas',
                    'Consider skill development courses',
                    'Seek mentoring or coaching'
                ]
            })
        
        # Competitive gap recommendations
        for gap in competitive_analysis['competitive_gaps']:
            recommendations.append({
                'type': 'competitive_gap',
                'priority': 'medium',
                'title': f'Improve Performance in {gap["area"].replace("_", " ").title()}',
                'description': gap['gap'],
                'action_items': [
                    f'Research best practices in {gap["area"]}',
                    'Network with high performers in this area',
                    'Consider specialized training'
                ]
            })
        
        return recommendations
    
    def _create_percentile_radar_chart(self, percentile_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create radar chart for percentile performance"""
        # Chart.js configuration for interactive chart
        domains = [domain for domain in percentile_results.keys() if domain != 'composite']
        percentiles = [percentile_results[domain]['percentile'] for domain in domains]
        
        chart_config = {
            'type': 'radar',
            'data': {
                'labels': [domain.replace('_', ' ').title() for domain in domains],
                'datasets': [{
                    'label': 'Your Percentile',
                    'data': percentiles,
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'pointBackgroundColor': 'rgba(54, 162, 235, 1)',
                    'pointBorderColor': '#fff',
                    'pointHoverBackgroundColor': '#fff',
                    'pointHoverBorderColor': 'rgba(54, 162, 235, 1)'
                }]
            },
            'options': {
                'scales': {
                    'r': {
                        'beginAtZero': True,
                        'max': 100,
                        'ticks': {
                            'stepSize': 20
                        }
                    }
                },
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Domain Performance Percentiles'
                    }
                }
            }
        }
        
        # Create static matplotlib chart
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        angles = np.linspace(0, 2 * np.pi, len(domains), endpoint=False)
        percentiles_plot = percentiles + [percentiles[0]]  # Close the radar chart
        angles_plot = np.concatenate((angles, [angles[0]]))
        
        ax.plot(angles_plot, percentiles_plot, 'o-', linewidth=2, color='#36a2eb')
        ax.fill(angles_plot, percentiles_plot, alpha=0.25, color='#36a2eb')
        ax.set_xticks(angles)
        ax.set_xticklabels([domain.replace('_', ' ').title() for domain in domains])
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_title('Domain Performance Percentiles', size=16, pad=20)
        ax.grid(True)
        
        # Convert to base64 image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return {
            'chart_config': chart_config,
            'static_image': f'data:image/png;base64,{image_base64}'
        }
    
    def _create_peer_comparison_bar_chart(self, comparison_groups: Dict[str, Any]) -> Dict[str, Any]:
        """Create bar chart for peer group comparisons"""
        group_names = list(comparison_groups.keys())
        percentiles = [comparison_groups[group]['average_percentile'] for group in group_names]
        
        # Chart.js configuration
        chart_config = {
            'type': 'bar',
            'data': {
                'labels': [group.replace('_', ' ').title() for group in group_names],
                'datasets': [{
                    'label': 'Average Percentile',
                    'data': percentiles,
                    'backgroundColor': ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 
                                      'rgba(255, 205, 86, 0.2)', 'rgba(75, 192, 192, 0.2)'],
                    'borderColor': ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)',
                                   'rgba(255, 205, 86, 1)', 'rgba(75, 192, 192, 1)'],
                    'borderWidth': 1
                }]
            },
            'options': {
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'max': 100
                    }
                },
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Peer Group Comparisons'
                    }
                }
            }
        }
        
        # Create static matplotlib chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(group_names)), percentiles, 
                      color=['#ff6384', '#36a2eb', '#ffcd56', '#4bc0c0'])
        
        ax.set_xlabel('Peer Groups')
        ax.set_ylabel('Average Percentile')
        ax.set_title('Peer Group Comparisons')
        ax.set_xticks(range(len(group_names)))
        ax.set_xticklabels([group.replace('_', ' ').title() for group in group_names], rotation=45)
        ax.set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, percentile in zip(bars, percentiles):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{percentile:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        return {
            'chart_config': chart_config,
            'static_image': f'data:image/png;base64,{image_base64}'
        }
    
    def _create_performance_distribution_chart(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create performance distribution visualization"""
        # Simple histogram for demonstration
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Generate sample distribution data
        sample_data = np.random.normal(65, 15, 1000)
        sample_data = np.clip(sample_data, 0, 100)
        
        ax.hist(sample_data, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        
        # Add candidate score line if available
        if 'percentile_results' in analysis_data and 'composite' in analysis_data['percentile_results']:
            candidate_score = analysis_data['percentile_results']['composite']['score']
            ax.axvline(candidate_score, color='red', linestyle='--', linewidth=2, label='Your Score')
            ax.legend()
        
        ax.set_xlabel('Performance Score')
        ax.set_ylabel('Frequency')
        ax.set_title('Performance Distribution')
        ax.grid(True, alpha=0.3)
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        # Chart.js config (simplified histogram)
        chart_config = {
            'type': 'bar',
            'data': {
                'labels': ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'],
                'datasets': [{
                    'label': 'Distribution',
                    'data': [5, 15, 25, 45, 85, 120, 95, 65, 35, 15],  # Sample data
                    'backgroundColor': 'rgba(135, 206, 235, 0.7)',
                    'borderColor': 'rgba(135, 206, 235, 1)',
                    'borderWidth': 1
                }]
            },
            'options': {
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Performance Distribution'
                    }
                }
            }
        }
        
        return {
            'chart_config': chart_config,
            'static_image': f'data:image/png;base64,{image_base64}'
        }
    
    def _create_benchmark_positioning_chart(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create benchmark positioning scatter plot"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Sample positioning data
        industries = ['Tech', 'Finance', 'Healthcare', 'Education', 'Consulting']
        x_values = [75, 65, 60, 55, 70]  # Performance scores
        y_values = [80, 70, 65, 50, 75]  # Market competitiveness
        
        scatter = ax.scatter(x_values, y_values, s=100, alpha=0.7, c=['red', 'blue', 'green', 'orange', 'purple'])
        
        # Add labels
        for i, industry in enumerate(industries):
            ax.annotate(industry, (x_values[i], y_values[i]), xytext=(5, 5), textcoords='offset points')
        
        ax.set_xlabel('Performance Score')
        ax.set_ylabel('Market Competitiveness')
        ax.set_title('Industry Position Matrix')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(40, 90)
        ax.set_ylim(40, 90)
        
        # Add quadrant lines
        ax.axhline(y=65, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=65, color='gray', linestyle='--', alpha=0.5)
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        
        # Chart.js scatter plot config
        chart_config = {
            'type': 'scatter',
            'data': {
                'datasets': [{
                    'label': 'Industry Positions',
                    'data': [{'x': x, 'y': y} for x, y in zip(x_values, y_values)],
                    'backgroundColor': ['rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)', 
                                       'rgba(255, 205, 86, 0.6)', 'rgba(75, 192, 192, 0.6)', 
                                       'rgba(153, 102, 255, 0.6)']
                }]
            },
            'options': {
                'scales': {
                    'x': {
                        'title': {
                            'display': True,
                            'text': 'Performance Score'
                        }
                    },
                    'y': {
                        'title': {
                            'display': True,
                            'text': 'Market Competitiveness'
                        }
                    }
                },
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Industry Position Matrix'
                    }
                }
            }
        }
        
        return {
            'chart_config': chart_config,
            'static_image': f'data:image/png;base64,{image_base64}'
        }
    
    def _validate_benchmark_configuration(self, benchmark_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate individual benchmark configuration"""
        validation = {
            'is_valid': True,
            'quality_score': 1.0,
            'issues': [],
            'warnings': []
        }
        
        # Check required fields
        required_fields = ['domain_stats', 'composite_stats', 'job_role_weights']
        for field in required_fields:
            if field not in benchmark_data:
                validation['is_valid'] = False
                validation['issues'].append(f"Missing required field: {field}")
        
        # Validate domain statistics
        if 'domain_stats' in benchmark_data:
            for domain in self.reasoning_domains:
                if domain not in benchmark_data['domain_stats']:
                    validation['issues'].append(f"Missing domain statistics for: {domain}")
                    validation['is_valid'] = False
                else:
                    domain_stats = benchmark_data['domain_stats'][domain]
                    
                    # Check statistical validity
                    if domain_stats.get('sample_size', 0) < 100:
                        validation['warnings'].append(f"Small sample size for {domain}: {domain_stats.get('sample_size', 0)}")
                        validation['quality_score'] *= 0.9
                    
                    if domain_stats.get('std', 0) <= 0:
                        validation['issues'].append(f"Invalid standard deviation for {domain}")
                        validation['is_valid'] = False
        
        return validation
    
    def _calculate_benchmark_quality_metrics(self) -> Dict[str, Any]:
        """Calculate overall benchmark quality metrics"""
        metrics = {
            'data_completeness': 0.0,
            'statistical_validity': 0.0,
            'sample_size_adequacy': 0.0,
            'distribution_normality': 0.0
        }
        
        total_configs = 0
        valid_configs = 0
        adequate_samples = 0
        
        for job_role in self.industry_benchmarks:
            for job_level in self.job_levels:
                for industry in self.industries:
                    if industry in self.industry_benchmarks[job_role][job_level]:
                        for region in self.regions:
                            for company_size in self.company_sizes:
                                total_configs += 1
                                benchmark_data = self.industry_benchmarks[job_role][job_level][industry][region][company_size]
                                
                                # Check completeness
                                if all(field in benchmark_data for field in ['domain_stats', 'composite_stats']):
                                    valid_configs += 1
                                
                                # Check sample size
                                if benchmark_data.get('composite_stats', {}).get('sample_size', 0) >= 500:
                                    adequate_samples += 1
        
        metrics['data_completeness'] = (valid_configs / total_configs) * 100 if total_configs > 0 else 0
        metrics['sample_size_adequacy'] = (adequate_samples / total_configs) * 100 if total_configs > 0 else 0
        metrics['statistical_validity'] = 85.0  # Simulated - would calculate from actual statistical tests
        metrics['distribution_normality'] = 78.0  # Simulated - would use Shapiro-Wilk or similar tests
        
        return metrics
    
    def _generate_validation_recommendations(self, integrity_checks: Dict[str, Any], quality_metrics: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        if quality_metrics['data_completeness'] < 95:
            recommendations.append({
                'type': 'data_quality',
                'priority': 'high',
                'recommendation': 'Address missing benchmark configurations to improve data completeness'
            })
        
        if quality_metrics['sample_size_adequacy'] < 80:
            recommendations.append({
                'type': 'sample_size',
                'priority': 'medium',
                'recommendation': 'Increase sample sizes for more reliable statistical estimates'
            })
        
        if integrity_checks['validation_success_rate'] < 90:
            recommendations.append({
                'type': 'validation',
                'priority': 'high',
                'recommendation': 'Review and fix benchmark configurations with validation failures'
            })
        
        return recommendations

# Initialize the Industry Benchmark Engine
industry_benchmark_engine = IndustryBenchmarkEngine()