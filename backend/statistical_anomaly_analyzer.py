#!/usr/bin/env python3
"""
Statistical Anomaly Analyzer - Advanced Statistical Analysis for Cheating Detection

This module implements sophisticated statistical methods to detect various types of
academic dishonesty and anomalous behavior patterns in test-taking scenarios.

Author: AI Assistant
Created: 2025
"""

import logging
import statistics
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict, Counter
import uuid
import math
from scipy import stats
from scipy.stats import chi2_contingency, kstest, anderson
import warnings
warnings.filterwarnings('ignore')

class StatisticalAnomalyAnalyzer:
    """
    Advanced Statistical Analysis for detecting sophisticated cheating patterns
    
    This class implements four key detection methods:
    1. Answer Pattern Irregularities - Detects suspicious response sequences
    2. Difficulty Progression Anomalies - Identifies unusual performance on hard vs easy questions  
    3. Time Zone Manipulation - Detects suspicious timing patterns
    4. Collaborative Cheating Patterns - Identifies coordination between test-takers
    """
    
    def __init__(self):
        """Initialize the Statistical Anomaly Analyzer"""
        self.logger = logging.getLogger(__name__)
        self.analysis_cache = {}
        
        # Statistical thresholds for anomaly detection
        self.thresholds = {
            'pattern_irregularity': 0.75,  # Threshold for suspicious answer patterns
            'difficulty_anomaly': 0.65,    # Threshold for difficulty progression issues
            'timezone_manipulation': 0.70,  # Threshold for suspicious timing
            'collaboration_score': 0.60     # Threshold for collaborative cheating
        }
        
        # Expected answer distribution parameters
        self.expected_patterns = {
            'uniform_distribution_threshold': 0.05,  # Chi-square p-value threshold
            'sequence_length_threshold': 5,          # Maximum suspicious sequence length
            'difficulty_correlation_threshold': -0.3  # Expected difficulty-accuracy correlation
        }
        
        self.logger.info("StatisticalAnomalyAnalyzer initialized successfully")
    
    def detect_answer_pattern_irregularities(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect suspicious answer patterns that may indicate cheating
        
        Analyzes:
        - Answer sequence patterns (ABACABAD, etc.)
        - Response clustering and uniformity
        - Statistical distribution of choices
        - Unusual answer changing patterns
        - Sequential dependencies between answers
        
        Args:
            session_data: Session data containing responses and metadata
            
        Returns:
            Comprehensive analysis of answer pattern irregularities
        """
        try:
            session_id = session_data.get('session_id', 'unknown')
            responses = session_data.get('responses', [])
            
            if not responses:
                return self._create_empty_analysis('answer_patterns', session_id, "No response data available")
            
            self.logger.info(f"Analyzing answer patterns for session: {session_id}")
            
            # Extract answer choices
            answer_choices = []
            answer_changes = []
            response_times = []
            
            for response in responses:
                if 'response' in response:
                    answer_choices.append(response['response'])
                if 'previous_response' in response and response.get('previous_response') != response.get('response'):
                    answer_changes.append({
                        'question_id': response.get('question_id'),
                        'from': response.get('previous_response'),
                        'to': response.get('response'),
                        'change_time': response.get('change_timestamp')
                    })
                if 'response_time' in response:
                    response_times.append(response['response_time'])
            
            analysis_results = {}
            
            # 1. Answer Distribution Analysis
            distribution_analysis = self._analyze_answer_distribution(answer_choices)
            analysis_results['distribution_analysis'] = distribution_analysis
            
            # 2. Sequential Pattern Analysis
            sequence_analysis = self._analyze_answer_sequences(answer_choices)
            analysis_results['sequence_analysis'] = sequence_analysis
            
            # 3. Answer Clustering Analysis
            clustering_analysis = self._analyze_answer_clustering(answer_choices, response_times)
            analysis_results['clustering_analysis'] = clustering_analysis
            
            # 4. Answer Change Pattern Analysis
            change_analysis = self._analyze_answer_changes(answer_changes, responses)
            analysis_results['change_analysis'] = change_analysis
            
            # 5. Statistical Uniformity Tests
            uniformity_analysis = self._test_answer_uniformity(answer_choices)
            analysis_results['uniformity_analysis'] = uniformity_analysis
            
            # Calculate composite irregularity score
            irregularity_score = self._calculate_pattern_irregularity_score(analysis_results)
            
            # Risk assessment
            risk_level = self._assess_pattern_risk(irregularity_score)
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis_type': 'answer_pattern_irregularities',
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'total_responses': len(responses),
                'total_answer_changes': len(answer_changes),
                'irregularity_score': float(irregularity_score),
                'risk_level': risk_level,
                'detailed_analysis': analysis_results,
                'recommendations': self._generate_pattern_recommendations(irregularity_score, analysis_results),
                'statistical_significance': self._calculate_pattern_significance(analysis_results)
            }
            
        except Exception as e:
            self.logger.error(f"Error in answer pattern analysis: {str(e)}")
            return {
                'success': False,
                'session_id': session_data.get('session_id', 'unknown'),
                'analysis_type': 'answer_pattern_irregularities',
                'error': str(e)
            }
    
    def analyze_difficulty_progression_anomalies(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance patterns across difficulty levels to detect anomalies
        
        Detects:
        - Inverted difficulty curves (better on hard questions)
        - Suspicious difficulty jumps
        - Inconsistent performance relative to question complexity
        - Statistical outliers in difficulty-accuracy correlation
        
        Args:
            session_data: Session data with difficulty ratings and performance
            
        Returns:
            Comprehensive difficulty progression anomaly analysis
        """
        try:
            session_id = session_data.get('session_id', 'unknown')
            responses = session_data.get('responses', [])
            
            if not responses:
                return self._create_empty_analysis('difficulty_progression', session_id, "No response data available")
            
            self.logger.info(f"Analyzing difficulty progression for session: {session_id}")
            
            # Extract difficulty and accuracy data
            difficulty_data = []
            for response in responses:
                if 'difficulty' in response and 'is_correct' in response:
                    difficulty_data.append({
                        'question_id': response.get('question_id'),
                        'difficulty': float(response['difficulty']),
                        'is_correct': bool(response['is_correct']),
                        'response_time': response.get('response_time', 0),
                        'topic': response.get('topic', 'unknown')
                    })
            
            if len(difficulty_data) < 3:
                return self._create_empty_analysis('difficulty_progression', session_id, "Insufficient difficulty data")
            
            analysis_results = {}
            
            # 1. Difficulty-Accuracy Correlation Analysis
            correlation_analysis = self._analyze_difficulty_accuracy_correlation(difficulty_data)
            analysis_results['correlation_analysis'] = correlation_analysis
            
            # 2. Performance by Difficulty Bins
            binned_analysis = self._analyze_performance_by_difficulty_bins(difficulty_data)
            analysis_results['binned_analysis'] = binned_analysis
            
            # 3. Difficulty Progression Patterns
            progression_analysis = self._analyze_difficulty_progression_patterns(difficulty_data)
            analysis_results['progression_analysis'] = progression_analysis
            
            # 4. Statistical Outlier Detection
            outlier_analysis = self._detect_difficulty_outliers(difficulty_data)
            analysis_results['outlier_analysis'] = outlier_analysis
            
            # 5. Topic-Specific Difficulty Analysis
            topic_analysis = self._analyze_topic_difficulty_patterns(difficulty_data)
            analysis_results['topic_analysis'] = topic_analysis
            
            # Calculate composite anomaly score
            anomaly_score = self._calculate_difficulty_anomaly_score(analysis_results)
            
            # Risk assessment
            risk_level = self._assess_difficulty_risk(anomaly_score)
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis_type': 'difficulty_progression_anomalies',
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'total_questions_analyzed': len(difficulty_data),
                'difficulty_range': {
                    'min': min(d['difficulty'] for d in difficulty_data),
                    'max': max(d['difficulty'] for d in difficulty_data),
                    'mean': statistics.mean(d['difficulty'] for d in difficulty_data)
                },
                'anomaly_score': float(anomaly_score),
                'risk_level': risk_level,
                'detailed_analysis': analysis_results,
                'recommendations': self._generate_difficulty_recommendations(anomaly_score, analysis_results),
                'statistical_significance': self._calculate_difficulty_significance(analysis_results)
            }
            
        except Exception as e:
            self.logger.error(f"Error in difficulty progression analysis: {str(e)}")
            return {
                'success': False,
                'session_id': session_data.get('session_id', 'unknown'),
                'analysis_type': 'difficulty_progression_anomalies',
                'error': str(e)
            }
    
    def identify_time_zone_manipulation(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify suspicious timing patterns that may indicate time zone manipulation
        
        Detects:
        - Tests taken at unusual hours for the candidate's location
        - Patterns suggesting timezone gaming for extended time
        - Suspicious breaks and resume patterns
        - Coordination with other time zones
        
        Args:
            session_data: Session data with timestamps and location information
            
        Returns:
            Comprehensive time zone manipulation analysis
        """
        try:
            session_id = session_data.get('session_id', 'unknown')
            responses = session_data.get('responses', [])
            
            self.logger.info(f"Analyzing timing patterns for session: {session_id}")
            
            # Extract timing data
            timing_data = self._extract_timing_data(session_data)
            
            if not timing_data['timestamps']:
                return self._create_empty_analysis('timezone_manipulation', session_id, "No timing data available")
            
            analysis_results = {}
            
            # 1. Time Zone Consistency Analysis
            timezone_analysis = self._analyze_timezone_consistency(timing_data, session_data)
            analysis_results['timezone_analysis'] = timezone_analysis
            
            # 2. Unusual Hour Detection
            unusual_hours_analysis = self._detect_unusual_testing_hours(timing_data)
            analysis_results['unusual_hours_analysis'] = unusual_hours_analysis
            
            # 3. Break Pattern Analysis
            break_pattern_analysis = self._analyze_break_patterns(timing_data)
            analysis_results['break_pattern_analysis'] = break_pattern_analysis
            
            # 4. Session Duration Anomalies
            duration_analysis = self._analyze_session_duration_anomalies(timing_data)
            analysis_results['duration_analysis'] = duration_analysis
            
            # 5. Cross-Reference with Expected Patterns
            expected_pattern_analysis = self._compare_with_expected_timing_patterns(timing_data, session_data)
            analysis_results['expected_pattern_analysis'] = expected_pattern_analysis
            
            # Calculate composite manipulation score
            manipulation_score = self._calculate_timezone_manipulation_score(analysis_results)
            
            # Risk assessment
            risk_level = self._assess_timezone_risk(manipulation_score)
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis_type': 'timezone_manipulation',
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'session_start_time': timing_data.get('session_start'),
                'session_end_time': timing_data.get('session_end'),
                'total_duration_minutes': timing_data.get('total_duration_minutes', 0),
                'manipulation_score': float(manipulation_score),
                'risk_level': risk_level,
                'detailed_analysis': analysis_results,
                'recommendations': self._generate_timezone_recommendations(manipulation_score, analysis_results),
                'statistical_significance': self._calculate_timezone_significance(analysis_results)
            }
            
        except Exception as e:
            self.logger.error(f"Error in timezone manipulation analysis: {str(e)}")
            return {
                'success': False,
                'session_id': session_data.get('session_id', 'unknown'),
                'analysis_type': 'timezone_manipulation',
                'error': str(e)
            }
    
    def detect_collaborative_cheating_patterns(self, session_data: Dict[str, Any], comparison_sessions: List[Dict] = None) -> Dict[str, Any]:
        """
        Detect patterns suggesting collaborative cheating between multiple test-takers
        
        Detects:
        - Similar answer patterns across sessions
        - Coordinated timing patterns
        - Unusual similarity in response sequences
        - Statistical evidence of information sharing
        
        Args:
            session_data: Primary session to analyze
            comparison_sessions: Other sessions to compare against (optional)
            
        Returns:
            Comprehensive collaborative cheating pattern analysis
        """
        try:
            session_id = session_data.get('session_id', 'unknown')
            responses = session_data.get('responses', [])
            
            if not responses:
                return self._create_empty_analysis('collaborative_cheating', session_id, "No response data available")
            
            self.logger.info(f"Analyzing collaborative patterns for session: {session_id}")
            
            analysis_results = {}
            
            # 1. Internal Consistency Analysis (within session)
            internal_analysis = self._analyze_internal_consistency(responses)
            analysis_results['internal_analysis'] = internal_analysis
            
            # 2. Cross-Session Comparison (if comparison data available)
            if comparison_sessions:
                cross_session_analysis = self._analyze_cross_session_similarities(session_data, comparison_sessions)
                analysis_results['cross_session_analysis'] = cross_session_analysis
            else:
                analysis_results['cross_session_analysis'] = {
                    'available': False,
                    'message': 'No comparison sessions provided'
                }
            
            # 3. Timing Coordination Analysis
            timing_coordination_analysis = self._analyze_timing_coordination(session_data, comparison_sessions)
            analysis_results['timing_coordination_analysis'] = timing_coordination_analysis
            
            # 4. Answer Pattern Similarity Analysis
            pattern_similarity_analysis = self._analyze_answer_pattern_similarities(session_data, comparison_sessions)
            analysis_results['pattern_similarity_analysis'] = pattern_similarity_analysis
            
            # 5. Statistical Clustering Analysis
            clustering_analysis = self._analyze_statistical_clustering(session_data, comparison_sessions)
            analysis_results['clustering_analysis'] = clustering_analysis
            
            # Calculate composite collaboration score
            collaboration_score = self._calculate_collaboration_score(analysis_results)
            
            # Risk assessment
            risk_level = self._assess_collaboration_risk(collaboration_score)
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis_type': 'collaborative_cheating_patterns',
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'total_responses': len(responses),
                'comparison_sessions_count': len(comparison_sessions) if comparison_sessions else 0,
                'collaboration_score': float(collaboration_score),
                'risk_level': risk_level,
                'detailed_analysis': analysis_results,
                'recommendations': self._generate_collaboration_recommendations(collaboration_score, analysis_results),
                'statistical_significance': self._calculate_collaboration_significance(analysis_results)
            }
            
        except Exception as e:
            self.logger.error(f"Error in collaborative cheating analysis: {str(e)}")
            return {
                'success': False,
                'session_id': session_data.get('session_id', 'unknown'),
                'analysis_type': 'collaborative_cheating_patterns',
                'error': str(e)
            }
    
    # ===== HELPER METHODS FOR ANSWER PATTERN ANALYSIS =====
    
    def _analyze_answer_distribution(self, answer_choices: List[str]) -> Dict[str, Any]:
        """Analyze the distribution of answer choices"""
        try:
            if not answer_choices:
                return {'available': False, 'message': 'No answer choices available'}
            
            # Count answer frequencies
            answer_counts = Counter(answer_choices)
            total_answers = len(answer_choices)
            
            # Calculate expected frequency (uniform distribution)
            unique_choices = len(answer_counts)
            expected_frequency = total_answers / unique_choices if unique_choices > 0 else 0
            
            # Chi-square test for uniformity
            observed_frequencies = list(answer_counts.values())
            expected_frequencies = [expected_frequency] * unique_choices
            
            if unique_choices > 1 and total_answers > 5:
                chi2_stat, p_value = stats.chisquare(observed_frequencies, expected_frequencies)
                is_uniform = bool(p_value > self.expected_patterns['uniform_distribution_threshold'])
            else:
                chi2_stat, p_value, is_uniform = 0, 1, True
            
            # Calculate distribution bias
            distribution_bias = max(answer_counts.values()) / total_answers if total_answers > 0 else 0
            
            return {
                'available': True,
                'answer_counts': dict(answer_counts),
                'total_answers': total_answers,
                'unique_choices': unique_choices,
                'distribution_bias': float(distribution_bias),
                'chi2_statistic': float(chi2_stat),
                'p_value': float(p_value),
                'is_uniform': bool(is_uniform),
                'uniformity_score': float(1 - distribution_bias) if distribution_bias <= 1 else 0.0
            }
            
        except Exception as e:
            self.logger.warning(f"Error in answer distribution analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _analyze_answer_sequences(self, answer_choices: List[str]) -> Dict[str, Any]:
        """Analyze sequential patterns in answers"""
        try:
            if len(answer_choices) < 3:
                return {'available': False, 'message': 'Insufficient answers for sequence analysis'}
            
            # Look for repeating sequences
            sequence_patterns = {}
            max_sequence_length = min(self.expected_patterns['sequence_length_threshold'], len(answer_choices) // 2)
            
            for seq_len in range(2, max_sequence_length + 1):
                for i in range(len(answer_choices) - seq_len + 1):
                    sequence = ''.join(answer_choices[i:i+seq_len])
                    sequence_patterns[sequence] = sequence_patterns.get(sequence, 0) + 1
            
            # Find most common sequences
            repeated_sequences = {seq: count for seq, count in sequence_patterns.items() if count > 1}
            
            # Calculate sequence regularity
            total_possible_sequences = sum(len(answer_choices) - seq_len + 1 for seq_len in range(2, max_sequence_length + 1))
            sequence_regularity = len(repeated_sequences) / total_possible_sequences if total_possible_sequences > 0 else 0
            
            # Look for alternating patterns (ABAB, ABCABC, etc.)
            alternating_patterns = self._detect_alternating_patterns(answer_choices)
            
            return {
                'available': True,
                'repeated_sequences': repeated_sequences,
                'sequence_regularity': float(sequence_regularity),
                'alternating_patterns': alternating_patterns,
                'total_sequences_analyzed': total_possible_sequences,
                'suspicion_score': float(min(sequence_regularity * 2, 1.0))
            }
            
        except Exception as e:
            self.logger.warning(f"Error in sequence analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _analyze_answer_clustering(self, answer_choices: List[str], response_times: List[float]) -> Dict[str, Any]:
        """Analyze clustering patterns in answers and timing"""
        try:
            if len(answer_choices) < 5:
                return {'available': False, 'message': 'Insufficient data for clustering analysis'}
            
            # Temporal clustering analysis
            if len(response_times) == len(answer_choices):
                # Analyze if similar answers cluster in time
                temporal_clusters = self._find_temporal_answer_clusters(answer_choices, response_times)
            else:
                temporal_clusters = {'available': False, 'message': 'Mismatched timing data'}
            
            # Positional clustering analysis
            positional_clusters = self._find_positional_answer_clusters(answer_choices)
            
            # Calculate overall clustering score
            clustering_score = 0
            if temporal_clusters.get('available'):
                clustering_score += temporal_clusters.get('clustering_strength', 0) * 0.6
            if positional_clusters.get('available'):
                clustering_score += positional_clusters.get('clustering_strength', 0) * 0.4
            
            return {
                'available': True,
                'temporal_clusters': temporal_clusters,
                'positional_clusters': positional_clusters,
                'overall_clustering_score': float(clustering_score),
                'is_suspicious': clustering_score > 0.7
            }
            
        except Exception as e:
            self.logger.warning(f"Error in clustering analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _analyze_answer_changes(self, answer_changes: List[Dict], responses: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in answer changes"""
        try:
            if not answer_changes:
                return {
                    'available': True,
                    'total_changes': 0,
                    'change_rate': 0.0,
                    'change_patterns': {},
                    'suspicion_score': 0.0
                }
            
            total_responses = len(responses)
            change_rate = len(answer_changes) / total_responses if total_responses > 0 else 0
            
            # Analyze change patterns
            change_patterns = {
                'most_common_from': Counter(change['from'] for change in answer_changes).most_common(3),
                'most_common_to': Counter(change['to'] for change in answer_changes).most_common(3),
                'change_types': Counter(f"{change['from']}->{change['to']}" for change in answer_changes)
            }
            
            # Calculate suspicion score based on change patterns
            # High suspicion if many changes or specific patterns
            suspicion_score = min(change_rate * 2, 1.0)  # Cap at 1.0
            
            # Additional suspicion for unusual patterns (e.g., many changes to same answer)
            if change_patterns['most_common_to']:
                most_common_to_count = change_patterns['most_common_to'][0][1]
                if most_common_to_count > len(answer_changes) * 0.5:
                    suspicion_score = min(suspicion_score + 0.3, 1.0)
            
            return {
                'available': True,
                'total_changes': len(answer_changes),
                'change_rate': float(change_rate),
                'change_patterns': {
                    'most_common_from': [(choice, count) for choice, count in change_patterns['most_common_from']],
                    'most_common_to': [(choice, count) for choice, count in change_patterns['most_common_to']],
                    'change_types': dict(change_patterns['change_types'])
                },
                'suspicion_score': float(suspicion_score)
            }
            
        except Exception as e:
            self.logger.warning(f"Error in answer change analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _test_answer_uniformity(self, answer_choices: List[str]) -> Dict[str, Any]:
        """Test statistical uniformity of answer distribution"""
        try:
            if len(answer_choices) < 5:
                return {'available': False, 'message': 'Insufficient data for uniformity testing'}
            
            # Chi-square goodness of fit test
            answer_counts = Counter(answer_choices)
            observed = list(answer_counts.values())
            expected_freq = len(answer_choices) / len(answer_counts)
            expected = [expected_freq] * len(answer_counts)
            
            chi2_stat, p_value = stats.chisquare(observed, expected)
            
            # Kolmogorov-Smirnov test (convert to numeric)
            choice_to_num = {choice: i for i, choice in enumerate(sorted(answer_counts.keys()))}
            numeric_choices = [choice_to_num[choice] for choice in answer_choices]
            
            # Test against uniform distribution
            uniform_data = np.random.uniform(0, len(answer_counts)-1, len(answer_choices))
            ks_stat, ks_p_value = stats.ks_2samp(numeric_choices, uniform_data)
            
            return {
                'available': True,
                'chi_square': {
                    'statistic': float(chi2_stat),
                    'p_value': float(p_value),
                    'is_uniform': p_value > 0.05
                },
                'kolmogorov_smirnov': {
                    'statistic': float(ks_stat),
                    'p_value': float(ks_p_value),
                    'is_uniform': ks_p_value > 0.05
                },
                'overall_uniformity_score': float((p_value + ks_p_value) / 2)
            }
            
        except Exception as e:
            self.logger.warning(f"Error in uniformity testing: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    # ===== HELPER METHODS FOR DIFFICULTY ANALYSIS =====
    
    def _analyze_difficulty_accuracy_correlation(self, difficulty_data: List[Dict]) -> Dict[str, Any]:
        """Analyze correlation between difficulty and accuracy"""
        try:
            difficulties = [d['difficulty'] for d in difficulty_data]
            accuracies = [1 if d['is_correct'] else 0 for d in difficulty_data]
            
            if len(set(difficulties)) < 2:
                return {'available': False, 'message': 'Insufficient difficulty variation'}
            
            # Calculate Pearson correlation
            correlation, p_value = stats.pearsonr(difficulties, accuracies)
            
            # Expected correlation should be negative (harder questions, lower accuracy)
            expected_correlation = self.expected_patterns['difficulty_correlation_threshold']
            correlation_anomaly = bool(correlation > expected_correlation)
            
            # Calculate strength of anomaly
            anomaly_strength = max(0, correlation - expected_correlation) if correlation_anomaly else 0
            
            return {
                'available': True,
                'correlation_coefficient': float(correlation),
                'p_value': float(p_value),
                'expected_correlation': expected_correlation,
                'is_anomalous': bool(correlation_anomaly),
                'anomaly_strength': float(anomaly_strength),
                'statistical_significance': p_value < 0.05
            }
            
        except Exception as e:
            self.logger.warning(f"Error in difficulty-accuracy correlation: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _analyze_performance_by_difficulty_bins(self, difficulty_data: List[Dict]) -> Dict[str, Any]:
        """Analyze performance across difficulty bins"""
        try:
            # Create difficulty bins
            difficulties = [d['difficulty'] for d in difficulty_data]
            min_diff, max_diff = min(difficulties), max(difficulties)
            
            if max_diff == min_diff:
                return {'available': False, 'message': 'No difficulty variation'}
            
            # Create 3 bins: Easy, Medium, Hard
            bin_size = (max_diff - min_diff) / 3
            bins = {
                'easy': (min_diff, min_diff + bin_size),
                'medium': (min_diff + bin_size, min_diff + 2*bin_size),
                'hard': (min_diff + 2*bin_size, max_diff)
            }
            
            # Categorize questions and calculate performance
            bin_performance = {}
            for bin_name, (bin_min, bin_max) in bins.items():
                bin_questions = [
                    d for d in difficulty_data 
                    if bin_min <= d['difficulty'] <= bin_max
                ]
                
                if bin_questions:
                    accuracy = sum(1 for q in bin_questions if q['is_correct']) / len(bin_questions)
                    avg_time = statistics.mean(q['response_time'] for q in bin_questions if q['response_time'] > 0)
                    
                    bin_performance[bin_name] = {
                        'question_count': len(bin_questions),
                        'accuracy': float(accuracy),
                        'average_time': float(avg_time) if avg_time else 0,
                        'difficulty_range': (float(bin_min), float(bin_max))
                    }
            
            # Check for inverted performance (better on hard questions)
            anomaly_detected = False
            if 'easy' in bin_performance and 'hard' in bin_performance:
                easy_acc = bin_performance['easy']['accuracy']
                hard_acc = bin_performance['hard']['accuracy']
                anomaly_detected = hard_acc > easy_acc + 0.1  # 10% threshold
            
            return {
                'available': True,
                'bin_performance': bin_performance,
                'inverted_performance_detected': bool(anomaly_detected),
                'performance_progression': self._calculate_performance_progression(bin_performance)
            }
            
        except Exception as e:
            self.logger.warning(f"Error in difficulty bin analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    # ===== COMPOSITE SCORING METHODS =====
    
    def _calculate_pattern_irregularity_score(self, analysis_results: Dict) -> float:
        """Calculate composite irregularity score from pattern analysis"""
        try:
            score = 0.0
            weights = {
                'distribution_analysis': 0.25,
                'sequence_analysis': 0.25,
                'clustering_analysis': 0.20,
                'change_analysis': 0.15,
                'uniformity_analysis': 0.15
            }
            
            for analysis_type, weight in weights.items():
                if analysis_type in analysis_results and analysis_results[analysis_type].get('available'):
                    analysis = analysis_results[analysis_type]
                    
                    if analysis_type == 'distribution_analysis':
                        # High bias indicates irregularity
                        score += (1 - analysis.get('uniformity_score', 0.5)) * weight
                    
                    elif analysis_type == 'sequence_analysis':
                        score += analysis.get('suspicion_score', 0) * weight
                    
                    elif analysis_type == 'clustering_analysis':
                        score += analysis.get('overall_clustering_score', 0) * weight
                    
                    elif analysis_type == 'change_analysis':
                        score += analysis.get('suspicion_score', 0) * weight
                    
                    elif analysis_type == 'uniformity_analysis':
                        # Low uniformity score indicates irregularity
                        score += (1 - analysis.get('overall_uniformity_score', 0.5)) * weight
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.warning(f"Error calculating pattern irregularity score: {str(e)}")
            return 0.5
    
    def _calculate_difficulty_anomaly_score(self, analysis_results: Dict) -> float:
        """Calculate composite difficulty anomaly score"""
        try:
            score = 0.0
            weights = {
                'correlation_analysis': 0.35,
                'binned_analysis': 0.25,
                'progression_analysis': 0.20,
                'outlier_analysis': 0.20
            }
            
            for analysis_type, weight in weights.items():
                if analysis_type in analysis_results and analysis_results[analysis_type].get('available'):
                    analysis = analysis_results[analysis_type]
                    
                    if analysis_type == 'correlation_analysis':
                        if analysis.get('is_anomalous'):
                            score += analysis.get('anomaly_strength', 0) * weight
                    
                    elif analysis_type == 'binned_analysis':
                        if analysis.get('inverted_performance_detected'):
                            score += 0.8 * weight
                    
                    # Add other analysis types as needed
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.warning(f"Error calculating difficulty anomaly score: {str(e)}")
            return 0.5
    
    # ===== UTILITY METHODS =====
    
    def _create_empty_analysis(self, analysis_type: str, session_id: str, message: str) -> Dict[str, Any]:
        """Create empty analysis result for cases with insufficient data"""
        return {
            'success': True,
            'session_id': session_id,
            'analysis_type': analysis_type,
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'message': message,
            'score': 0.0,
            'risk_level': 'MINIMAL',
            'detailed_analysis': {},
            'recommendations': ['Insufficient data for comprehensive analysis'],
            'statistical_significance': {'available': False}
        }
    
    def _assess_pattern_risk(self, score: float) -> str:
        """Assess risk level based on pattern irregularity score"""
        if score >= 0.8:
            return 'CRITICAL'
        elif score >= 0.65:
            return 'HIGH'
        elif score >= 0.45:
            return 'MEDIUM'
        elif score >= 0.25:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def _assess_difficulty_risk(self, score: float) -> str:
        """Assess risk level based on difficulty anomaly score"""
        return self._assess_pattern_risk(score)  # Same thresholds for now
    
    def _assess_timezone_risk(self, score: float) -> str:
        """Assess risk level based on timezone manipulation score"""
        return self._assess_pattern_risk(score)  # Same thresholds for now
    
    def _assess_collaboration_risk(self, score: float) -> str:
        """Assess risk level based on collaboration score"""
        return self._assess_pattern_risk(score)  # Same thresholds for now
    
    # ===== PLACEHOLDER METHODS (TO BE IMPLEMENTED) =====
    
    def _detect_alternating_patterns(self, answer_choices: List[str]) -> Dict[str, Any]:
        """Detect alternating answer patterns (placeholder implementation)"""
        # Simplified implementation for now
        return {'detected': False, 'patterns': [], 'strength': 0.0}
    
    def _find_temporal_answer_clusters(self, answer_choices: List[str], response_times: List[float]) -> Dict[str, Any]:
        """Find temporal clustering in answers (placeholder implementation)"""
        return {'available': True, 'clustering_strength': 0.3}
    
    def _find_positional_answer_clusters(self, answer_choices: List[str]) -> Dict[str, Any]:
        """Find positional clustering in answers (placeholder implementation)"""
        return {'available': True, 'clustering_strength': 0.2}
    
    def _calculate_performance_progression(self, bin_performance: Dict) -> Dict[str, Any]:
        """Calculate performance progression metrics (placeholder implementation)"""
        return {'trend': 'normal', 'anomaly_detected': False}
    
    # ===== TIMING ANALYSIS HELPER METHODS =====
    
    def _extract_timing_data(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract comprehensive timing data from session"""
        try:
            responses = session_data.get('responses', [])
            session_start = session_data.get('session_start_timestamp')
            session_end = session_data.get('session_end_timestamp')
            
            # Extract timestamps from responses
            timestamps = []
            response_intervals = []
            
            for i, response in enumerate(responses):
                if 'timestamp' in response:
                    timestamp = response['timestamp']
                    if isinstance(timestamp, str):
                        try:
                            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        except:
                            timestamp = datetime.utcnow()
                    timestamps.append(timestamp)
                    
                    # Calculate intervals between responses
                    if i > 0 and len(timestamps) > 1:
                        interval = (timestamps[-1] - timestamps[-2]).total_seconds()
                        response_intervals.append(interval)
            
            # Calculate session duration
            total_duration_minutes = 0
            if session_start and session_end:
                if isinstance(session_start, str):
                    session_start = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                if isinstance(session_end, str):
                    session_end = datetime.fromisoformat(session_end.replace('Z', '+00:00'))
                total_duration_minutes = (session_end - session_start).total_seconds() / 60
            elif timestamps:
                total_duration_minutes = (timestamps[-1] - timestamps[0]).total_seconds() / 60
            
            return {
                'timestamps': timestamps,
                'session_start': session_start,
                'session_end': session_end,
                'total_duration_minutes': total_duration_minutes,
                'response_intervals': response_intervals,
                'average_interval': statistics.mean(response_intervals) if response_intervals else 0,
                'total_responses': len(responses)
            }
            
        except Exception as e:
            self.logger.warning(f"Error extracting timing data: {str(e)}")
            return {'timestamps': [], 'session_start': None, 'session_end': None, 'total_duration_minutes': 0}
    
    def _analyze_timezone_consistency(self, timing_data: Dict, session_data: Dict) -> Dict[str, Any]:
        """Analyze timezone consistency and detect suspicious patterns"""
        try:
            timestamps = timing_data.get('timestamps', [])
            if not timestamps:
                return {'consistent': True, 'anomaly_score': 0.0, 'available': False}
            
            # Extract hours from timestamps
            hours = [ts.hour for ts in timestamps if ts]
            if not hours:
                return {'consistent': True, 'anomaly_score': 0.0, 'available': False}
            
            # Analyze hour distribution
            hour_distribution = Counter(hours)
            most_common_hours = hour_distribution.most_common(5)
            
            # Check for unusual patterns
            suspicious_patterns = []
            anomaly_score = 0.0
            
            # Pattern 1: Testing during typical sleep hours (2 AM - 5 AM)
            sleep_hours = [2, 3, 4, 5]
            sleep_hour_count = sum(hour_distribution[hour] for hour in sleep_hours)
            if sleep_hour_count > len(timestamps) * 0.3:  # More than 30% during sleep hours
                suspicious_patterns.append("High activity during typical sleep hours")
                anomaly_score += 0.4
            
            # Pattern 2: Extreme time clustering (all responses within 2-hour window)
            if len(set(hours)) <= 2 and len(timestamps) > 10:
                suspicious_patterns.append("Extremely concentrated timing pattern")
                anomaly_score += 0.3
            
            # Pattern 3: Inconsistent with declared timezone
            declared_timezone = session_data.get('timezone', 'UTC')
            expected_active_hours = self._get_expected_active_hours(declared_timezone)
            actual_active_hours = set(hours)
            overlap = len(actual_active_hours.intersection(expected_active_hours))
            expected_overlap = len(expected_active_hours)
            
            if expected_overlap > 0 and overlap / expected_overlap < 0.3:
                suspicious_patterns.append("Low overlap with expected active hours for timezone")
                anomaly_score += 0.5
            
            return {
                'available': True,
                'consistent': anomaly_score < 0.3,
                'anomaly_score': float(min(anomaly_score, 1.0)),
                'hour_distribution': dict(hour_distribution),
                'most_common_hours': most_common_hours,
                'suspicious_patterns': suspicious_patterns,
                'sleep_hour_activity_ratio': sleep_hour_count / len(timestamps) if timestamps else 0
            }
            
        except Exception as e:
            self.logger.warning(f"Error in timezone consistency analysis: {str(e)}")
            return {'consistent': True, 'anomaly_score': 0.2, 'available': False, 'error': str(e)}
    
    def _detect_unusual_testing_hours(self, timing_data: Dict) -> Dict[str, Any]:
        """Detect unusual testing hours that may indicate timezone manipulation"""
        try:
            timestamps = timing_data.get('timestamps', [])
            if not timestamps:
                return {'unusual_hours_detected': False, 'suspicion_score': 0.0, 'available': False}
            
            # Extract unique hours and calculate statistics
            hours = [ts.hour for ts in timestamps if ts]
            unique_hours = set(hours)
            hour_counts = Counter(hours)
            
            unusual_patterns = []
            suspicion_score = 0.0
            
            # Check for extremely late/early hours (11 PM - 5 AM)
            unusual_hours = {23, 0, 1, 2, 3, 4, 5}
            unusual_hour_activity = sum(hour_counts[hour] for hour in unusual_hours if hour in hour_counts)
            unusual_ratio = unusual_hour_activity / len(timestamps) if timestamps else 0
            
            if unusual_ratio > 0.4:  # More than 40% activity during unusual hours
                unusual_patterns.append(f"High activity during unusual hours ({unusual_ratio:.1%})")
                suspicion_score += unusual_ratio * 0.6
            
            # Check for midnight sessions (activity around midnight)
            midnight_hours = {22, 23, 0, 1, 2}
            midnight_activity = sum(hour_counts[hour] for hour in midnight_hours if hour in hour_counts)
            midnight_ratio = midnight_activity / len(timestamps) if timestamps else 0
            
            if midnight_ratio > 0.5:
                unusual_patterns.append("Significant midnight period activity")
                suspicion_score += 0.3
            
            # Check for consistent off-hours pattern
            if len(unique_hours) >= 3 and all(hour in unusual_hours for hour in unique_hours):
                unusual_patterns.append("Exclusively unusual hours pattern")
                suspicion_score += 0.5
            
            return {
                'available': True,
                'unusual_hours_detected': len(unusual_patterns) > 0,
                'suspicion_score': float(min(suspicion_score, 1.0)),
                'unusual_hour_ratio': unusual_ratio,
                'midnight_activity_ratio': midnight_ratio,
                'unusual_patterns': unusual_patterns,
                'hour_distribution': dict(hour_counts)
            }
            
        except Exception as e:
            self.logger.warning(f"Error detecting unusual testing hours: {str(e)}")
            return {'unusual_hours_detected': False, 'suspicion_score': 0.1, 'available': False, 'error': str(e)}
    
    def _analyze_break_patterns(self, timing_data: Dict) -> Dict[str, Any]:
        """Analyze break patterns for suspicious behavior"""
        try:
            response_intervals = timing_data.get('response_intervals', [])
            if len(response_intervals) < 3:
                return {'suspicious_breaks': 0, 'pattern_score': 0.0, 'available': False}
            
            # Identify potential breaks (intervals > 5 minutes = 300 seconds)
            break_threshold = 300  # 5 minutes
            long_breaks = [interval for interval in response_intervals if interval > break_threshold]
            very_long_breaks = [interval for interval in response_intervals if interval > 1800]  # 30 minutes
            
            suspicious_patterns = []
            pattern_score = 0.0
            
            # Pattern 1: Too many long breaks
            if len(long_breaks) > len(response_intervals) * 0.2:  # More than 20% are breaks
                suspicious_patterns.append("Excessive break frequency")
                pattern_score += 0.3
            
            # Pattern 2: Very long breaks (might indicate external assistance)
            if very_long_breaks:
                suspicious_patterns.append(f"Very long breaks detected ({len(very_long_breaks)} breaks > 30 min)")
                pattern_score += len(very_long_breaks) * 0.2
            
            # Pattern 3: Consistent break timing (might indicate coordination)
            if len(long_breaks) >= 3:
                break_intervals = []
                last_break_pos = -1
                for i, interval in enumerate(response_intervals):
                    if interval > break_threshold:
                        if last_break_pos >= 0:
                            break_intervals.append(i - last_break_pos)
                        last_break_pos = i
                
                if break_intervals and len(set(break_intervals)) <= 2:  # Very regular pattern
                    suspicious_patterns.append("Suspiciously regular break timing")
                    pattern_score += 0.4
            
            # Calculate break statistics
            avg_break_duration = statistics.mean(long_breaks) if long_breaks else 0
            total_break_time = sum(long_breaks)
            total_session_time = sum(response_intervals)
            break_time_ratio = total_break_time / total_session_time if total_session_time > 0 else 0
            
            return {
                'available': True,
                'suspicious_breaks': len(suspicious_patterns),
                'pattern_score': float(min(pattern_score, 1.0)),
                'total_breaks': len(long_breaks),
                'very_long_breaks': len(very_long_breaks),
                'average_break_duration': avg_break_duration,
                'break_time_ratio': break_time_ratio,
                'suspicious_patterns': suspicious_patterns
            }
            
        except Exception as e:
            self.logger.warning(f"Error analyzing break patterns: {str(e)}")
            return {'suspicious_breaks': 0, 'pattern_score': 0.1, 'available': False, 'error': str(e)}
    
    def _analyze_session_duration_anomalies(self, timing_data: Dict) -> Dict[str, Any]:
        """Analyze session duration for anomalies"""
        try:
            total_duration = timing_data.get('total_duration_minutes', 0)
            total_responses = timing_data.get('total_responses', 0)
            
            if total_duration <= 0 or total_responses <= 0:
                return {'duration_anomaly': False, 'anomaly_score': 0.0, 'available': False}
            
            # Calculate metrics
            avg_time_per_response = total_duration / total_responses
            response_intervals = timing_data.get('response_intervals', [])
            
            anomalies = []
            anomaly_score = 0.0
            
            # Anomaly 1: Extremely fast completion (< 30 seconds per question)
            if avg_time_per_response < 0.5:  # Less than 30 seconds per response
                anomalies.append("Extremely fast completion time")
                anomaly_score += 0.6
            
            # Anomaly 2: Extremely slow completion (> 10 minutes per question)
            elif avg_time_per_response > 10:
                anomalies.append("Extremely slow completion time")
                anomaly_score += 0.4
            
            # Anomaly 3: Inconsistent pacing
            if response_intervals:
                interval_std = statistics.stdev(response_intervals) if len(response_intervals) > 1 else 0
                interval_mean = statistics.mean(response_intervals)
                cv = interval_std / interval_mean if interval_mean > 0 else 0  # Coefficient of variation
                
                if cv > 2.0:  # High variability in response times
                    anomalies.append("Highly inconsistent response timing")
                    anomaly_score += 0.3
            
            return {
                'available': True,
                'duration_anomaly': len(anomalies) > 0,
                'anomaly_score': float(min(anomaly_score, 1.0)),
                'total_duration_minutes': total_duration,
                'avg_time_per_response': avg_time_per_response,
                'anomalies_detected': anomalies,
                'pacing_consistency': 1 - (cv / 3) if 'cv' in locals() else 0.5
            }
            
        except Exception as e:
            self.logger.warning(f"Error analyzing session duration: {str(e)}")
            return {'duration_anomaly': False, 'anomaly_score': 0.0, 'available': False, 'error': str(e)}
    
    def _compare_with_expected_timing_patterns(self, timing_data: Dict, session_data: Dict) -> Dict[str, Any]:
        """Compare actual timing with expected patterns"""
        try:
            total_duration = timing_data.get('total_duration_minutes', 0)
            total_responses = timing_data.get('total_responses', 0)
            
            if total_responses <= 0:
                return {'matches_expected': True, 'deviation_score': 0.0, 'available': False}
            
            # Get expected timing based on question types/difficulty
            expected_time_per_response = self._calculate_expected_response_time(session_data)
            expected_total_duration = expected_time_per_response * total_responses
            
            # Calculate deviations
            duration_ratio = total_duration / expected_total_duration if expected_total_duration > 0 else 1
            deviation_score = abs(1 - duration_ratio)
            
            # Classification
            deviations = []
            if duration_ratio < 0.5:
                deviations.append("Completion significantly faster than expected")
            elif duration_ratio > 2.0:
                deviations.append("Completion significantly slower than expected")
            
            matches_expected = deviation_score < 0.5  # Within 50% of expected
            
            return {
                'available': True,
                'matches_expected': matches_expected,
                'deviation_score': float(min(deviation_score, 1.0)),
                'actual_duration': total_duration,
                'expected_duration': expected_total_duration,
                'duration_ratio': duration_ratio,
                'deviations': deviations
            }
            
        except Exception as e:
            self.logger.warning(f"Error comparing timing patterns: {str(e)}")
            return {'matches_expected': True, 'deviation_score': 0.1, 'available': False, 'error': str(e)}
    
    def _calculate_timezone_manipulation_score(self, analysis_results: Dict) -> float:
        """Calculate comprehensive timezone manipulation score"""
        try:
            score = 0.0
            weights = {
                'timezone_analysis': 0.3,
                'unusual_hours_analysis': 0.25,
                'break_pattern_analysis': 0.2,
                'duration_analysis': 0.15,
                'expected_pattern_analysis': 0.1
            }
            
            for analysis_type, weight in weights.items():
                if analysis_type in analysis_results and analysis_results[analysis_type].get('available'):
                    analysis = analysis_results[analysis_type]
                    
                    if analysis_type == 'timezone_analysis':
                        score += analysis.get('anomaly_score', 0) * weight
                    elif analysis_type == 'unusual_hours_analysis':
                        score += analysis.get('suspicion_score', 0) * weight
                    elif analysis_type == 'break_pattern_analysis':
                        score += analysis.get('pattern_score', 0) * weight
                    elif analysis_type == 'duration_analysis':
                        score += analysis.get('anomaly_score', 0) * weight
                    elif analysis_type == 'expected_pattern_analysis':
                        score += analysis.get('deviation_score', 0) * weight
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.warning(f"Error calculating timezone manipulation score: {str(e)}")
            return 0.25
    
    # ===== COLLABORATION ANALYSIS HELPER METHODS =====
    
    def _analyze_internal_consistency(self, responses: List[Dict]) -> Dict[str, Any]:
        """Analyze internal consistency within session"""
        try:
            if len(responses) < 5:
                return {'consistency_score': 0.8, 'anomalies_detected': [], 'available': False}
            
            # Extract response patterns
            correct_answers = [r for r in responses if r.get('is_correct', False)]
            incorrect_answers = [r for r in responses if not r.get('is_correct', True)]
            response_times = [r.get('response_time', 0) for r in responses if r.get('response_time', 0) > 0]
            
            anomalies = []
            consistency_metrics = {}
            
            # 1. Accuracy consistency across difficulty levels
            if correct_answers and incorrect_answers:
                easy_questions = [r for r in responses if r.get('difficulty', 0.5) < 0.4]
                hard_questions = [r for r in responses if r.get('difficulty', 0.5) > 0.7]
                
                if easy_questions and hard_questions:
                    easy_accuracy = sum(1 for q in easy_questions if q.get('is_correct', False)) / len(easy_questions)
                    hard_accuracy = sum(1 for q in hard_questions if q.get('is_correct', False)) / len(hard_questions)
                    
                    # Anomaly: Better performance on hard questions
                    if hard_accuracy > easy_accuracy + 0.2:
                        anomalies.append("Better performance on difficult questions than easy ones")
                    
                    consistency_metrics['difficulty_consistency'] = abs(easy_accuracy - hard_accuracy)
            
            # 2. Response time consistency
            if len(response_times) >= 5:
                avg_time = statistics.mean(response_times)
                time_std = statistics.stdev(response_times)
                cv_time = time_std / avg_time if avg_time > 0 else 0
                
                # Very consistent timing might indicate automation
                if cv_time < 0.15:  # Very low variability
                    anomalies.append("Unusually consistent response timing")
                elif cv_time > 3.0:  # Very high variability
                    anomalies.append("Extremely inconsistent response timing")
                
                consistency_metrics['timing_variability'] = cv_time
            
            # 3. Answer choice distribution consistency
            answer_choices = [r.get('response', '') for r in responses if r.get('response')]
            if len(answer_choices) >= 10:
                choice_distribution = Counter(answer_choices)
                most_common_ratio = choice_distribution.most_common(1)[0][1] / len(answer_choices)
                
                # Extreme bias toward one choice
                if most_common_ratio > 0.6:
                    anomalies.append("Extreme bias toward specific answer choice")
                
                consistency_metrics['choice_distribution_bias'] = most_common_ratio
            
            # Calculate overall consistency score
            consistency_score = 1.0
            if anomalies:
                consistency_score -= len(anomalies) * 0.2
            consistency_score = max(0.0, min(1.0, consistency_score))
            
            return {
                'available': True,
                'consistency_score': float(consistency_score),
                'anomalies_detected': anomalies,
                'consistency_metrics': consistency_metrics,
                'total_responses': len(responses)
            }
            
        except Exception as e:
            self.logger.warning(f"Error in internal consistency analysis: {str(e)}")
            return {'consistency_score': 0.8, 'anomalies_detected': [], 'available': False, 'error': str(e)}
    
    def _analyze_cross_session_similarities(self, session_data: Dict, comparison_sessions: Optional[List[Dict]]) -> Dict[str, Any]:
        """Analyze similarities across sessions"""
        try:
            if not comparison_sessions:
                return {'similarity_scores': [], 'high_similarity_detected': False, 'available': False}
            
            current_responses = session_data.get('responses', [])
            if not current_responses:
                return {'similarity_scores': [], 'high_similarity_detected': False, 'available': False}
            
            similarity_scores = []
            high_similarity_pairs = []
            
            for comp_session in comparison_sessions:
                comp_responses = comp_session.get('responses', [])
                if not comp_responses:
                    continue
                
                # Calculate similarity metrics
                similarity_metrics = self._calculate_session_similarity(current_responses, comp_responses)
                
                if similarity_metrics['overall_similarity'] > 0.8:  # High similarity threshold
                    high_similarity_pairs.append({
                        'session_id': comp_session.get('session_id', 'unknown'),
                        'similarity_score': similarity_metrics['overall_similarity'],
                        'similar_aspects': similarity_metrics['similar_aspects']
                    })
                
                similarity_scores.append({
                    'session_id': comp_session.get('session_id', 'unknown'),
                    'similarity_metrics': similarity_metrics
                })
            
            return {
                'available': True,
                'similarity_scores': similarity_scores,
                'high_similarity_detected': len(high_similarity_pairs) > 0,
                'high_similarity_pairs': high_similarity_pairs,
                'total_comparisons': len(comparison_sessions)
            }
            
        except Exception as e:
            self.logger.warning(f"Error in cross-session similarity analysis: {str(e)}")
            return {'similarity_scores': [], 'high_similarity_detected': False, 'available': False, 'error': str(e)}
    
    def _analyze_timing_coordination(self, session_data: Dict, comparison_sessions: Optional[List[Dict]]) -> Dict[str, Any]:
        """Analyze timing coordination between sessions"""
        try:
            if not comparison_sessions:
                return {'coordination_detected': False, 'coordination_score': 0.0, 'available': False}
            
            current_timing = self._extract_timing_data(session_data)
            if not current_timing.get('timestamps'):
                return {'coordination_detected': False, 'coordination_score': 0.0, 'available': False}
            
            coordination_evidence = []
            coordination_scores = []
            
            for comp_session in comparison_sessions:
                comp_timing = self._extract_timing_data(comp_session)
                if not comp_timing.get('timestamps'):
                    continue
                
                # Check for simultaneous or coordinated timing patterns
                coordination_metrics = self._calculate_timing_coordination(current_timing, comp_timing)
                coordination_scores.append(coordination_metrics['coordination_score'])
                
                if coordination_metrics['coordination_score'] > 0.7:
                    coordination_evidence.append({
                        'session_id': comp_session.get('session_id', 'unknown'),
                        'coordination_type': coordination_metrics['coordination_type'],
                        'score': coordination_metrics['coordination_score']
                    })
            
            overall_coordination_score = max(coordination_scores) if coordination_scores else 0.0
            
            return {
                'available': True,
                'coordination_detected': len(coordination_evidence) > 0,
                'coordination_score': float(overall_coordination_score),
                'coordination_evidence': coordination_evidence,
                'coordination_scores': coordination_scores
            }
            
        except Exception as e:
            self.logger.warning(f"Error in timing coordination analysis: {str(e)}")
            return {'coordination_detected': False, 'coordination_score': 0.1, 'available': False, 'error': str(e)}
    
    def _analyze_answer_pattern_similarities(self, session_data: Dict, comparison_sessions: Optional[List[Dict]]) -> Dict[str, Any]:
        """Analyze answer pattern similarities"""
        try:
            if not comparison_sessions:
                return {'pattern_similarity_score': 0.0, 'suspicious_similarities': [], 'available': False}
            
            current_responses = session_data.get('responses', [])
            current_patterns = self._extract_answer_patterns(current_responses)
            
            if not current_patterns:
                return {'pattern_similarity_score': 0.0, 'suspicious_similarities': [], 'available': False}
            
            suspicious_similarities = []
            similarity_scores = []
            
            for comp_session in comparison_sessions:
                comp_responses = comp_session.get('responses', [])
                comp_patterns = self._extract_answer_patterns(comp_responses)
                
                if comp_patterns:
                    pattern_similarity = self._calculate_pattern_similarity(current_patterns, comp_patterns)
                    similarity_scores.append(pattern_similarity)
                    
                    if pattern_similarity > 0.75:  # High pattern similarity
                        suspicious_similarities.append({
                            'session_id': comp_session.get('session_id', 'unknown'),
                            'similarity_score': pattern_similarity,
                            'similar_patterns': self._identify_similar_patterns(current_patterns, comp_patterns)
                        })
            
            overall_similarity_score = max(similarity_scores) if similarity_scores else 0.0
            
            return {
                'available': True,
                'pattern_similarity_score': float(overall_similarity_score),
                'suspicious_similarities': suspicious_similarities,
                'similarity_scores': similarity_scores
            }
            
        except Exception as e:
            self.logger.warning(f"Error in answer pattern similarity analysis: {str(e)}")
            return {'pattern_similarity_score': 0.2, 'suspicious_similarities': [], 'available': False, 'error': str(e)}
    
    def _analyze_statistical_clustering(self, session_data: Dict, comparison_sessions: Optional[List[Dict]]) -> Dict[str, Any]:
        """Analyze statistical clustering between sessions"""
        try:
            if not comparison_sessions or len(comparison_sessions) < 2:
                return {'clustering_detected': False, 'cluster_strength': 0.0, 'available': False}
            
            # Extract feature vectors from all sessions
            all_sessions = [session_data] + comparison_sessions
            feature_vectors = []
            session_ids = []
            
            for session in all_sessions:
                features = self._extract_session_features(session)
                if features:
                    feature_vectors.append(features)
                    session_ids.append(session.get('session_id', 'unknown'))
            
            if len(feature_vectors) < 3:
                return {'clustering_detected': False, 'cluster_strength': 0.0, 'available': False}
            
            # Perform clustering analysis
            cluster_results = self._perform_clustering_analysis(feature_vectors, session_ids)
            
            return {
                'available': True,
                'clustering_detected': cluster_results['clustering_detected'],
                'cluster_strength': cluster_results['cluster_strength'],
                'cluster_assignments': cluster_results['cluster_assignments'],
                'suspicious_clusters': cluster_results['suspicious_clusters']
            }
            
        except Exception as e:
            self.logger.warning(f"Error in statistical clustering analysis: {str(e)}")
            return {'clustering_detected': False, 'cluster_strength': 0.1, 'available': False, 'error': str(e)}
    
    def _calculate_collaboration_score(self, analysis_results: Dict) -> float:
        """Calculate comprehensive collaboration score"""
        try:
            score = 0.0
            weights = {
                'internal_analysis': 0.2,
                'cross_session_analysis': 0.3,
                'timing_coordination_analysis': 0.25,
                'pattern_similarity_analysis': 0.15,
                'clustering_analysis': 0.1
            }
            
            for analysis_type, weight in weights.items():
                if analysis_type in analysis_results and analysis_results[analysis_type].get('available'):
                    analysis = analysis_results[analysis_type]
                    
                    if analysis_type == 'internal_analysis':
                        # Lower consistency might indicate collaboration
                        consistency = analysis.get('consistency_score', 0.8)
                        score += (1 - consistency) * weight
                    
                    elif analysis_type == 'cross_session_analysis':
                        if analysis.get('high_similarity_detected'):
                            score += 0.8 * weight
                    
                    elif analysis_type == 'timing_coordination_analysis':
                        score += analysis.get('coordination_score', 0) * weight
                    
                    elif analysis_type == 'pattern_similarity_analysis':
                        score += analysis.get('pattern_similarity_score', 0) * weight
                    
                    elif analysis_type == 'clustering_analysis':
                        if analysis.get('clustering_detected'):
                            score += analysis.get('cluster_strength', 0) * weight
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.warning(f"Error calculating collaboration score: {str(e)}")
            return 0.3
    
    # ===== UTILITY HELPER METHODS =====
    
    def _get_expected_active_hours(self, timezone: str) -> set:
        """Get expected active hours for a timezone"""
        # Simplified implementation - assumes 8 AM to 10 PM are active hours
        # In a real implementation, this would consider timezone offsets
        active_hours = set(range(8, 23))  # 8 AM to 10 PM
        return active_hours
    
    def _calculate_expected_response_time(self, session_data: Dict) -> float:
        """Calculate expected response time based on question difficulty"""
        responses = session_data.get('responses', [])
        if not responses:
            return 2.0  # Default 2 minutes per question
        
        # Simple calculation based on difficulty
        total_expected_time = 0
        for response in responses:
            difficulty = response.get('difficulty', 0.5)
            # Base time: 1-3 minutes based on difficulty
            expected_time = 1.0 + (difficulty * 2.0)
            total_expected_time += expected_time
        
        return total_expected_time / len(responses) if responses else 2.0
    
    def _calculate_session_similarity(self, responses1: List[Dict], responses2: List[Dict]) -> Dict[str, Any]:
        """Calculate similarity between two sessions"""
        try:
            if not responses1 or not responses2:
                return {'overall_similarity': 0.0, 'similar_aspects': []}
            
            similar_aspects = []
            similarity_scores = []
            
            # 1. Answer choice similarity
            answers1 = [r.get('response', '') for r in responses1]
            answers2 = [r.get('response', '') for r in responses2]
            
            # Find common questions (by question_id)
            common_questions = []
            for r1 in responses1:
                for r2 in responses2:
                    if r1.get('question_id') == r2.get('question_id'):
                        common_questions.append((r1, r2))
            
            if common_questions:
                matching_answers = sum(1 for r1, r2 in common_questions if r1.get('response') == r2.get('response'))
                answer_similarity = matching_answers / len(common_questions)
                similarity_scores.append(answer_similarity)
                
                if answer_similarity > 0.8:
                    similar_aspects.append("High answer choice similarity")
            
            # 2. Performance pattern similarity
            accuracy1 = sum(1 for r in responses1 if r.get('is_correct', False)) / len(responses1)
            accuracy2 = sum(1 for r in responses2 if r.get('is_correct', False)) / len(responses2)
            accuracy_similarity = 1 - abs(accuracy1 - accuracy2)
            similarity_scores.append(accuracy_similarity)
            
            if accuracy_similarity > 0.9:
                similar_aspects.append("Very similar performance levels")
            
            # 3. Timing pattern similarity
            times1 = [r.get('response_time', 0) for r in responses1 if r.get('response_time', 0) > 0]
            times2 = [r.get('response_time', 0) for r in responses2 if r.get('response_time', 0) > 0]
            
            if times1 and times2:
                avg_time1 = statistics.mean(times1)
                avg_time2 = statistics.mean(times2)
                timing_similarity = 1 - abs(avg_time1 - avg_time2) / max(avg_time1, avg_time2)
                similarity_scores.append(timing_similarity)
                
                if timing_similarity > 0.85:
                    similar_aspects.append("Similar response timing patterns")
            
            overall_similarity = statistics.mean(similarity_scores) if similarity_scores else 0.0
            
            return {
                'overall_similarity': float(overall_similarity),
                'similar_aspects': similar_aspects,
                'answer_similarity': similarity_scores[0] if len(similarity_scores) > 0 else 0.0,
                'performance_similarity': similarity_scores[1] if len(similarity_scores) > 1 else 0.0,
                'timing_similarity': similarity_scores[2] if len(similarity_scores) > 2 else 0.0
            }
            
        except Exception as e:
            self.logger.warning(f"Error calculating session similarity: {str(e)}")
            return {'overall_similarity': 0.0, 'similar_aspects': []}
    
    def _calculate_timing_coordination(self, timing1: Dict, timing2: Dict) -> Dict[str, Any]:
        """Calculate timing coordination between sessions"""
        try:
            timestamps1 = timing1.get('timestamps', [])
            timestamps2 = timing2.get('timestamps', [])
            
            if not timestamps1 or not timestamps2:
                return {'coordination_score': 0.0, 'coordination_type': 'none'}
            
            # Check for simultaneous activity (within 5-minute windows)
            coordination_score = 0.0
            coordination_type = 'none'
            
            simultaneous_count = 0
            for ts1 in timestamps1:
                for ts2 in timestamps2:
                    time_diff = abs((ts1 - ts2).total_seconds())
                    if time_diff < 300:  # Within 5 minutes
                        simultaneous_count += 1
            
            if simultaneous_count > 0:
                coordination_score = min(simultaneous_count / min(len(timestamps1), len(timestamps2)), 1.0)
                
                if coordination_score > 0.7:
                    coordination_type = 'highly_coordinated'
                elif coordination_score > 0.4:
                    coordination_type = 'moderately_coordinated'
                else:
                    coordination_type = 'loosely_coordinated'
            
            return {
                'coordination_score': float(coordination_score),
                'coordination_type': coordination_type,
                'simultaneous_activities': simultaneous_count
            }
            
        except Exception as e:
            self.logger.warning(f"Error calculating timing coordination: {str(e)}")
            return {'coordination_score': 0.0, 'coordination_type': 'none'}
    
    def _extract_answer_patterns(self, responses: List[Dict]) -> Dict[str, Any]:
        """Extract answer patterns from responses"""
        try:
            if not responses:
                return {}
            
            answers = [r.get('response', '') for r in responses]
            
            patterns = {
                'sequence': ''.join(answers),
                'distribution': dict(Counter(answers)),
                'length': len(answers),
                'unique_answers': len(set(answers)),
                'most_common': Counter(answers).most_common(3),
                'alternating_detected': self._detect_alternating_patterns(answers)
            }
            
            return patterns
            
        except Exception as e:
            self.logger.warning(f"Error extracting answer patterns: {str(e)}")
            return {}
    
    def _calculate_pattern_similarity(self, patterns1: Dict, patterns2: Dict) -> float:
        """Calculate similarity between answer patterns"""
        try:
            if not patterns1 or not patterns2:
                return 0.0
            
            similarity_scores = []
            
            # Sequence similarity (if same length)
            seq1 = patterns1.get('sequence', '')
            seq2 = patterns2.get('sequence', '')
            
            if len(seq1) == len(seq2) and seq1 and seq2:
                matching_chars = sum(1 for c1, c2 in zip(seq1, seq2) if c1 == c2)
                sequence_similarity = matching_chars / len(seq1)
                similarity_scores.append(sequence_similarity)
            
            # Distribution similarity
            dist1 = patterns1.get('distribution', {})
            dist2 = patterns2.get('distribution', {})
            
            if dist1 and dist2:
                all_choices = set(dist1.keys()) | set(dist2.keys())
                if all_choices:
                    # Calculate cosine similarity of distributions
                    vec1 = [dist1.get(choice, 0) for choice in all_choices]
                    vec2 = [dist2.get(choice, 0) for choice in all_choices]
                    
                    dot_product = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
                    magnitude1 = math.sqrt(sum(v1 * v1 for v1 in vec1))
                    magnitude2 = math.sqrt(sum(v2 * v2 for v2 in vec2))
                    
                    if magnitude1 > 0 and magnitude2 > 0:
                        cosine_similarity = dot_product / (magnitude1 * magnitude2)
                        similarity_scores.append(cosine_similarity)
            
            return statistics.mean(similarity_scores) if similarity_scores else 0.0
            
        except Exception as e:
            self.logger.warning(f"Error calculating pattern similarity: {str(e)}")
            return 0.0
    
    def _identify_similar_patterns(self, patterns1: Dict, patterns2: Dict) -> List[str]:
        """Identify specific similar patterns between sessions"""
        similar_patterns = []
        
        try:
            # Check sequence similarity
            seq1 = patterns1.get('sequence', '')
            seq2 = patterns2.get('sequence', '')
            
            if seq1 == seq2:
                similar_patterns.append("Identical answer sequences")
            elif len(seq1) == len(seq2) and seq1 and seq2:
                matching_ratio = sum(1 for c1, c2 in zip(seq1, seq2) if c1 == c2) / len(seq1)
                if matching_ratio > 0.8:
                    similar_patterns.append(f"Very similar answer sequences ({matching_ratio:.1%} match)")
            
            # Check distribution similarity
            dist1 = patterns1.get('distribution', {})
            dist2 = patterns2.get('distribution', {})
            
            if dist1 and dist2:
                # Check if most common answers are the same
                most_common1 = patterns1.get('most_common', [])
                most_common2 = patterns2.get('most_common', [])
                
                if most_common1 and most_common2:
                    if most_common1[0][0] == most_common2[0][0]:
                        similar_patterns.append("Same most frequent answer choice")
            
        except Exception as e:
            self.logger.warning(f"Error identifying similar patterns: {str(e)}")
        
        return similar_patterns
    
    def _extract_session_features(self, session_data: Dict) -> Optional[List[float]]:
        """Extract numerical features from session for clustering"""
        try:
            responses = session_data.get('responses', [])
            if not responses:
                return None
            
            features = []
            
            # Accuracy
            accuracy = sum(1 for r in responses if r.get('is_correct', False)) / len(responses)
            features.append(accuracy)
            
            # Average response time
            times = [r.get('response_time', 0) for r in responses if r.get('response_time', 0) > 0]
            avg_time = statistics.mean(times) if times else 0
            features.append(avg_time)
            
            # Response time variability
            time_std = statistics.stdev(times) if len(times) > 1 else 0
            features.append(time_std)
            
            # Answer distribution entropy
            answers = [r.get('response', '') for r in responses]
            answer_counts = Counter(answers)
            total = len(answers)
            entropy = -sum((count/total) * math.log2(count/total) for count in answer_counts.values() if count > 0)
            features.append(entropy)
            
            # Average difficulty
            difficulties = [r.get('difficulty', 0.5) for r in responses]
            avg_difficulty = statistics.mean(difficulties)
            features.append(avg_difficulty)
            
            return features
            
        except Exception as e:
            self.logger.warning(f"Error extracting session features: {str(e)}")
            return None
    
    def _perform_clustering_analysis(self, feature_vectors: List[List[float]], session_ids: List[str]) -> Dict[str, Any]:
        """Perform clustering analysis on feature vectors"""
        try:
            if len(feature_vectors) < 3:
                return {'clustering_detected': False, 'cluster_strength': 0.0, 'cluster_assignments': {}, 'suspicious_clusters': []}
            
            # Simple distance-based clustering
            # Calculate pairwise distances
            distances = []
            pairs = []
            
            for i in range(len(feature_vectors)):
                for j in range(i + 1, len(feature_vectors)):
                    # Euclidean distance
                    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(feature_vectors[i], feature_vectors[j])))
                    distances.append(distance)
                    pairs.append((i, j))
            
            if not distances:
                return {'clustering_detected': False, 'cluster_strength': 0.0, 'cluster_assignments': {}, 'suspicious_clusters': []}
            
            # Find close pairs (distance < threshold)
            avg_distance = statistics.mean(distances)
            threshold = avg_distance * 0.5  # Pairs closer than half the average distance
            
            close_pairs = []
            for distance, (i, j) in zip(distances, pairs):
                if distance < threshold:
                    close_pairs.append({
                        'session1': session_ids[i],
                        'session2': session_ids[j],
                        'distance': distance
                    })
            
            clustering_detected = len(close_pairs) > 0
            cluster_strength = min(len(close_pairs) / len(pairs), 1.0) if pairs else 0.0
            
            # Identify suspicious clusters (multiple sessions very close to each other)
            suspicious_clusters = []
            if len(close_pairs) >= 2:
                suspicious_clusters = close_pairs  # For simplicity, all close pairs are suspicious
            
            return {
                'clustering_detected': clustering_detected,
                'cluster_strength': float(cluster_strength),
                'cluster_assignments': {sid: i for i, sid in enumerate(session_ids)},
                'suspicious_clusters': suspicious_clusters
            }
            
        except Exception as e:
            self.logger.warning(f"Error in clustering analysis: {str(e)}")
            return {'clustering_detected': False, 'cluster_strength': 0.0, 'cluster_assignments': {}, 'suspicious_clusters': []}


# Initialize global instance
statistical_anomaly_analyzer = StatisticalAnomalyAnalyzer()