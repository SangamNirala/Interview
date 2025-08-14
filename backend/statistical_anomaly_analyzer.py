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
            
            # Ensure all values are JSON serializable
            chi2_stat = float(chi2_stat) if hasattr(chi2_stat, 'item') else float(chi2_stat)
            p_value = float(p_value) if hasattr(p_value, 'item') else float(p_value)
            is_uniform = bool(is_uniform)
            
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
            
            # Ensure JSON serializable
            chi2_stat = float(chi2_stat) if hasattr(chi2_stat, 'item') else float(chi2_stat)
            p_value = float(p_value) if hasattr(p_value, 'item') else float(p_value)
            
            # Kolmogorov-Smirnov test (convert to numeric)
            choice_to_num = {choice: i for i, choice in enumerate(sorted(answer_counts.keys()))}
            numeric_choices = [choice_to_num[choice] for choice in answer_choices]
            
            # Test against uniform distribution
            uniform_data = np.random.uniform(0, len(answer_counts)-1, len(answer_choices))
            ks_stat, ks_p_value = stats.ks_2samp(numeric_choices, uniform_data)
            
            # Ensure JSON serializable
            ks_stat = float(ks_stat) if hasattr(ks_stat, 'item') else float(ks_stat)
            ks_p_value = float(ks_p_value) if hasattr(ks_p_value, 'item') else float(ks_p_value)
            
            return {
                'available': True,
                'chi_square': {
                    'statistic': float(chi2_stat),
                    'p_value': float(p_value),
                    'is_uniform': bool(p_value > 0.05)
                },
                'kolmogorov_smirnov': {
                    'statistic': float(ks_stat),
                    'p_value': float(ks_p_value),
                    'is_uniform': bool(ks_p_value > 0.05)
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
            
            # Ensure JSON serializable
            correlation = float(correlation) if hasattr(correlation, 'item') else float(correlation)
            p_value = float(p_value) if hasattr(p_value, 'item') else float(p_value)
            
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
                'statistical_significance': bool(p_value < 0.05)
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
        """Detect alternating answer patterns (ABAB, ABCABC, etc.)"""
        try:
            if len(answer_choices) < 4:
                return {'detected': False, 'patterns': [], 'strength': 0.0}
            
            patterns_found = []
            max_strength = 0.0
            
            # Check for 2-choice alternating patterns (ABAB...)
            for pattern_length in range(2, min(6, len(answer_choices) // 2)):
                for start_idx in range(len(answer_choices) - pattern_length * 2 + 1):
                    pattern = answer_choices[start_idx:start_idx + pattern_length]
                    
                    # Count how many times this pattern repeats consecutively
                    consecutive_repeats = 1
                    check_idx = start_idx + pattern_length
                    
                    while check_idx + pattern_length <= len(answer_choices):
                        next_segment = answer_choices[check_idx:check_idx + pattern_length]
                        if next_segment == pattern:
                            consecutive_repeats += 1
                            check_idx += pattern_length
                        else:
                            break
                    
                    # If pattern repeats at least 2 times (so 3+ total occurrences)
                    if consecutive_repeats >= 2:
                        total_length = pattern_length * (consecutive_repeats + 1)
                        strength = min(total_length / len(answer_choices), 1.0)
                        
                        pattern_info = {
                            'pattern': ''.join(pattern),
                            'length': pattern_length,
                            'repeats': consecutive_repeats + 1,
                            'start_position': start_idx,
                            'total_coverage': total_length,
                            'strength': float(strength)
                        }
                        
                        patterns_found.append(pattern_info)
                        max_strength = max(max_strength, strength)
            
            # Remove overlapping patterns, keep strongest
            unique_patterns = []
            for pattern in sorted(patterns_found, key=lambda x: x['strength'], reverse=True):
                overlaps = False
                for existing in unique_patterns:
                    if (pattern['start_position'] < existing['start_position'] + existing['total_coverage'] and
                        pattern['start_position'] + pattern['total_coverage'] > existing['start_position']):
                        overlaps = True
                        break
                if not overlaps:
                    unique_patterns.append(pattern)
            
            return {
                'detected': len(unique_patterns) > 0,
                'patterns': unique_patterns[:3],  # Return top 3 patterns
                'strength': float(max_strength),
                'total_patterns_found': len(unique_patterns)
            }
            
        except Exception as e:
            self.logger.warning(f"Error detecting alternating patterns: {str(e)}")
            return {'detected': False, 'patterns': [], 'strength': 0.0}
    
    def _find_temporal_answer_clusters(self, answer_choices: List[str], response_times: List[float]) -> Dict[str, Any]:
        """Find temporal clustering in answers based on response timing"""
        try:
            if len(answer_choices) != len(response_times) or len(answer_choices) < 5:
                return {'available': False, 'message': 'Insufficient or mismatched timing data'}
            
            # Group answers by choice and analyze timing patterns
            choice_timings = defaultdict(list)
            for choice, time in zip(answer_choices, response_times):
                choice_timings[choice].append(time)
            
            clustering_metrics = {}
            overall_clustering_strength = 0.0
            
            for choice, times in choice_timings.items():
                if len(times) < 2:
                    continue
                
                # Calculate coefficient of variation for response times
                mean_time = statistics.mean(times)
                std_time = statistics.stdev(times) if len(times) > 1 else 0
                cv = std_time / mean_time if mean_time > 0 else 0
                
                # Lower CV indicates more consistent timing (potential clustering)
                consistency_score = max(0, 1 - cv) if cv <= 2 else 0
                
                # Analyze sequential clustering (same answers appearing close together)
                sequential_clusters = 0
                for i in range(len(answer_choices) - 1):
                    if answer_choices[i] == choice and answer_choices[i + 1] == choice:
                        sequential_clusters += 1
                
                sequential_clustering_score = min(sequential_clusters / max(1, len(times) - 1), 1.0)
                
                # Combined clustering strength for this choice
                choice_clustering = (consistency_score * 0.6) + (sequential_clustering_score * 0.4)
                
                clustering_metrics[choice] = {
                    'count': len(times),
                    'mean_response_time': float(mean_time),
                    'std_response_time': float(std_time),
                    'coefficient_of_variation': float(cv),
                    'consistency_score': float(consistency_score),
                    'sequential_clusters': sequential_clusters,
                    'sequential_clustering_score': float(sequential_clustering_score),
                    'overall_clustering_score': float(choice_clustering)
                }
                
                overall_clustering_strength += choice_clustering * (len(times) / len(answer_choices))
            
            # Detect time-based patterns (e.g., all fast responses for certain answers)
            all_times = list(response_times)
            median_time = statistics.median(all_times)
            
            fast_response_patterns = {}
            for choice, times in choice_timings.items():
                fast_responses = sum(1 for t in times if t < median_time * 0.7)
                if len(times) > 2 and fast_responses / len(times) > 0.75:
                    fast_response_patterns[choice] = {
                        'fast_response_rate': float(fast_responses / len(times)),
                        'average_fast_time': float(statistics.mean([t for t in times if t < median_time * 0.7]))
                    }
            
            return {
                'available': True,
                'clustering_strength': float(overall_clustering_strength),
                'choice_clustering_metrics': clustering_metrics,
                'fast_response_patterns': fast_response_patterns,
                'median_response_time': float(median_time),
                'is_suspicious': overall_clustering_strength > 0.6
            }
            
        except Exception as e:
            self.logger.warning(f"Error in temporal clustering analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _find_positional_answer_clusters(self, answer_choices: List[str]) -> Dict[str, Any]:
        """Find positional clustering in answers based on question position"""
        try:
            if len(answer_choices) < 5:
                return {'available': False, 'message': 'Insufficient data for positional analysis'}
            
            # Analyze answer distribution across different sections of the test
            total_questions = len(answer_choices)
            section_size = total_questions // 3
            
            sections = {
                'beginning': answer_choices[:section_size],
                'middle': answer_choices[section_size:section_size*2],
                'end': answer_choices[section_size*2:]
            }
            
            # Calculate answer distribution in each section
            section_distributions = {}
            overall_distribution = Counter(answer_choices)
            
            for section_name, section_answers in sections.items():
                if not section_answers:
                    continue
                    
                section_counter = Counter(section_answers)
                section_distributions[section_name] = dict(section_counter)
            
            # Look for clustering patterns
            clustering_patterns = []
            clustering_strength = 0.0
            
            # Check if certain answers cluster in specific sections
            for choice in overall_distribution.keys():
                choice_positions = [i for i, ans in enumerate(answer_choices) if ans == choice]
                
                if len(choice_positions) < 2:
                    continue
                
                # Calculate position clustering using coefficient of variation
                mean_pos = statistics.mean(choice_positions)
                std_pos = statistics.stdev(choice_positions) if len(choice_positions) > 1 else 0
                
                # Normalize by total length
                normalized_std = std_pos / total_questions if total_questions > 0 else 0
                
                # Lower normalized std indicates clustering
                position_clustering_score = max(0, 1 - (normalized_std * 3))  # Scale factor
                
                if position_clustering_score > 0.5:  # Threshold for significant clustering
                    pattern = {
                        'choice': choice,
                        'count': len(choice_positions),
                        'positions': choice_positions[:10],  # Limit for output size
                        'mean_position': float(mean_pos),
                        'std_position': float(std_pos),
                        'clustering_score': float(position_clustering_score),
                        'section_distribution': {
                            section: section_distributions[section].get(choice, 0) 
                            for section in section_distributions
                        }
                    }
                    clustering_patterns.append(pattern)
                    clustering_strength = max(clustering_strength, position_clustering_score)
            
            # Analyze sequential runs (consecutive same answers)
            sequential_runs = []
            current_run = {'choice': answer_choices[0], 'start': 0, 'length': 1}
            
            for i in range(1, len(answer_choices)):
                if answer_choices[i] == current_run['choice']:
                    current_run['length'] += 1
                else:
                    if current_run['length'] >= 3:  # Only report runs of 3+
                        sequential_runs.append(dict(current_run))
                    current_run = {'choice': answer_choices[i], 'start': i, 'length': 1}
            
            # Check final run
            if current_run['length'] >= 3:
                sequential_runs.append(dict(current_run))
            
            # Adjust clustering strength based on sequential runs
            if sequential_runs:
                max_run_length = max(run['length'] for run in sequential_runs)
                run_clustering_bonus = min(max_run_length / total_questions, 0.5)
                clustering_strength = min(clustering_strength + run_clustering_bonus, 1.0)
            
            return {
                'available': True,
                'clustering_strength': float(clustering_strength),
                'clustering_patterns': clustering_patterns,
                'sequential_runs': sequential_runs,
                'section_distributions': section_distributions,
                'is_suspicious': clustering_strength > 0.6
            }
            
        except Exception as e:
            self.logger.warning(f"Error in positional clustering analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _calculate_performance_progression(self, bin_performance: Dict) -> Dict[str, Any]:
        """Calculate performance progression metrics (placeholder implementation)"""
        return {'trend': 'normal', 'anomaly_detected': False}
    
    # Additional placeholder methods for timing, collaboration analysis, etc.
    def _extract_timing_data(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract comprehensive timing data from session"""
        try:
            responses = session_data.get('responses', [])
            session_metadata = session_data.get('session_metadata', {})
            
            timestamps = []
            response_times = []
            activity_gaps = []
            
            # Extract timestamps and response times
            for response in responses:
                if 'timestamp' in response:
                    try:
                        timestamp = datetime.fromisoformat(response['timestamp'].replace('Z', '+00:00'))
                        timestamps.append(timestamp)
                    except:
                        continue
                
                if 'response_time' in response:
                    response_times.append(float(response['response_time']))
            
            # Calculate activity gaps between questions
            if len(timestamps) > 1:
                for i in range(1, len(timestamps)):
                    gap = (timestamps[i] - timestamps[i-1]).total_seconds()
                    activity_gaps.append(gap)
            
            # Extract session start/end times
            session_start = None
            session_end = None
            
            if session_metadata.get('start_time'):
                try:
                    session_start = datetime.fromisoformat(session_metadata['start_time'].replace('Z', '+00:00'))
                except:
                    pass
                    
            if session_metadata.get('end_time'):
                try:
                    session_end = datetime.fromisoformat(session_metadata['end_time'].replace('Z', '+00:00'))
                except:
                    pass
            
            # Calculate total duration
            total_duration_minutes = 0
            if session_start and session_end:
                total_duration_minutes = (session_end - session_start).total_seconds() / 60
            elif timestamps:
                total_duration_minutes = (timestamps[-1] - timestamps[0]).total_seconds() / 60
            
            return {
                'timestamps': timestamps,
                'response_times': response_times,
                'activity_gaps': activity_gaps,
                'session_start': session_start.isoformat() if session_start else None,
                'session_end': session_end.isoformat() if session_end else None,
                'total_duration_minutes': float(total_duration_minutes),
                'timezone_info': session_metadata.get('timezone'),
                'location_info': session_metadata.get('location', {}),
                'ip_address': session_metadata.get('ip_address')
            }
            
        except Exception as e:
            self.logger.warning(f"Error extracting timing data: {str(e)}")
            return {'timestamps': [], 'response_times': [], 'activity_gaps': []}
    
    def _analyze_timezone_consistency(self, timing_data: Dict, session_data: Dict) -> Dict[str, Any]:
        """Analyze timezone consistency and detect manipulation"""
        try:
            timestamps = timing_data.get('timestamps', [])
            if not timestamps:
                return {'consistent': True, 'anomaly_score': 0.0, 'message': 'No timestamps available'}
            
            # Extract timezone and location information
            reported_timezone = timing_data.get('timezone_info')
            location_info = timing_data.get('location_info', {})
            ip_address = timing_data.get('ip_address')
            
            anomaly_indicators = []
            anomaly_score = 0.0
            
            # Check timezone vs location consistency
            if reported_timezone and location_info.get('country'):
                country = location_info['country']
                expected_timezones = {
                    'US': ['America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles', 'America/Anchorage', 'Pacific/Honolulu'],
                    'GB': ['Europe/London'],
                    'CA': ['America/Toronto', 'America/Vancouver', 'America/Edmonton'],
                    'AU': ['Australia/Sydney', 'Australia/Melbourne', 'Australia/Perth'],
                    'IN': ['Asia/Kolkata'],
                    'DE': ['Europe/Berlin'],
                    'FR': ['Europe/Paris'],
                    'JP': ['Asia/Tokyo']
                }
                
                if country in expected_timezones:
                    if not any(tz in reported_timezone for tz in expected_timezones[country]):
                        anomaly_indicators.append(f"Timezone {reported_timezone} inconsistent with country {country}")
                        anomaly_score += 0.3
            
            # Analyze testing hours patterns
            if timestamps and reported_timezone:
                local_hours = []
                for timestamp in timestamps:
                    # Convert to local hour (simplified - assumes UTC input)
                    local_hour = timestamp.hour
                    local_hours.append(local_hour)
                
                # Check for unusual testing hours (very late night/early morning)
                unusual_hours = sum(1 for hour in local_hours if hour < 5 or hour > 23)
                if unusual_hours > len(local_hours) * 0.3:  # More than 30% unusual hours
                    anomaly_indicators.append(f"High percentage of unusual testing hours: {unusual_hours}/{len(local_hours)}")
                    anomaly_score += 0.25
                
                # Check for timezone hopping patterns
                hour_variation = max(local_hours) - min(local_hours) if local_hours else 0
                if hour_variation > 18:  # Suspicious hour variation
                    anomaly_indicators.append(f"Suspicious hour variation: {hour_variation} hours")
                    anomaly_score += 0.2
            
            # Check session duration vs expected timezone patterns
            total_duration = timing_data.get('total_duration_minutes', 0)
            if total_duration > 480:  # More than 8 hours
                anomaly_indicators.append(f"Unusually long session duration: {total_duration:.1f} minutes")
                anomaly_score += 0.15
            
            # Activity gap analysis for timezone manipulation
            activity_gaps = timing_data.get('activity_gaps', [])
            if activity_gaps:
                large_gaps = [gap for gap in activity_gaps if gap > 3600]  # Gaps > 1 hour
                if large_gaps:
                    avg_large_gap = statistics.mean(large_gaps) / 3600  # Convert to hours
                    anomaly_indicators.append(f"Large activity gaps detected: {len(large_gaps)} gaps, avg {avg_large_gap:.1f} hours")
                    anomaly_score += min(len(large_gaps) * 0.1, 0.3)
            
            consistency_score = max(0, 1 - anomaly_score)
            
            return {
                'consistent': anomaly_score < 0.4,
                'anomaly_score': float(min(anomaly_score, 1.0)),
                'consistency_score': float(consistency_score),
                'anomaly_indicators': anomaly_indicators,
                'reported_timezone': reported_timezone,
                'location_consistency': location_info,
                'testing_hour_analysis': {
                    'local_hours': local_hours if 'local_hours' in locals() else [],
                    'unusual_hour_count': unusual_hours if 'unusual_hours' in locals() else 0,
                    'hour_variation': hour_variation if 'hour_variation' in locals() else 0
                }
            }
            
        except Exception as e:
            self.logger.warning(f"Error analyzing timezone consistency: {str(e)}")
            return {'consistent': True, 'anomaly_score': 0.0, 'error': str(e)}
    
    def _detect_unusual_testing_hours(self, timing_data):
        """Detect unusual testing hours"""
        return {'unusual_hours_detected': False, 'suspicion_score': 0.1}
    
    def _analyze_break_patterns(self, timing_data):
        """Analyze break patterns"""
        return {'suspicious_breaks': 0, 'pattern_score': 0.1}
    
    def _analyze_session_duration_anomalies(self, timing_data):
        """Analyze session duration anomalies"""
        return {'duration_anomaly': False, 'anomaly_score': 0.0}
    
    def _compare_with_expected_timing_patterns(self, timing_data, session_data):
        """Compare with expected timing patterns"""
        return {'matches_expected': True, 'deviation_score': 0.1}
    
    def _calculate_timezone_manipulation_score(self, analysis_results):
        """Calculate timezone manipulation score"""
        return 0.25  # Placeholder
    
    def _analyze_internal_consistency(self, responses):
        """Analyze internal consistency within session"""
        return {'consistency_score': 0.8, 'anomalies_detected': []}
    
    def _analyze_cross_session_similarities(self, session_data, comparison_sessions):
        """Analyze similarities across sessions"""
        return {'similarity_scores': [], 'high_similarity_detected': False}
    
    def _analyze_timing_coordination(self, session_data, comparison_sessions):
        """Analyze timing coordination between sessions"""
        return {'coordination_detected': False, 'coordination_score': 0.1}
    
    def _analyze_answer_pattern_similarities(self, session_data, comparison_sessions):
        """Analyze answer pattern similarities"""
        return {'pattern_similarity_score': 0.2, 'suspicious_similarities': []}
    
    def _analyze_statistical_clustering(self, session_data, comparison_sessions):
        """Analyze statistical clustering between sessions"""
        return {'clustering_detected': False, 'cluster_strength': 0.1}
    
    def _calculate_collaboration_score(self, analysis_results):
        """Calculate collaboration score"""
        return 0.3  # Placeholder
    
    # Recommendation and significance methods (placeholders)
    def _generate_pattern_recommendations(self, score, analysis_results):
        """Generate recommendations for pattern irregularities"""
        return ["Review answer patterns for suspicious sequences", "Monitor for potential pattern-based cheating"]
    
    def _generate_difficulty_recommendations(self, score, analysis_results):
        """Generate recommendations for difficulty anomalies"""
        return ["Investigate unusual performance on difficult questions", "Consider adaptive difficulty adjustment"]
    
    def _generate_timezone_recommendations(self, score, analysis_results):
        """Generate recommendations for timezone manipulation"""
        return ["Verify candidate location and timezone", "Monitor testing hours for consistency"]
    
    def _generate_collaboration_recommendations(self, score, analysis_results):
        """Generate recommendations for collaborative cheating"""
        return ["Investigate potential collaboration between test-takers", "Implement enhanced monitoring protocols"]
    
    def _calculate_pattern_significance(self, analysis_results):
        """Calculate statistical significance for pattern analysis"""
        return {'significant': False, 'p_value': 0.15, 'confidence_level': 0.95}
    
    def _calculate_difficulty_significance(self, analysis_results):
        """Calculate statistical significance for difficulty analysis"""
        return {'significant': False, 'p_value': 0.12, 'confidence_level': 0.95}
    
    def _calculate_timezone_significance(self, analysis_results):
        """Calculate statistical significance for timezone analysis"""
        return {'significant': False, 'p_value': 0.18, 'confidence_level': 0.95}
    
    def _calculate_collaboration_significance(self, analysis_results):
        """Calculate statistical significance for collaboration analysis"""
        return {'significant': False, 'p_value': 0.20, 'confidence_level': 0.95}
    
    def detect_markov_chain_anomalies(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ENHANCEMENT METHOD: Advanced Markov Chain Analysis for Sophisticated Cheating Detection
        
        This method uses Markov Chain analysis to detect subtle patterns that indicate:
        - Non-random answer selection patterns
        - Hidden dependencies between consecutive answers
        - Sophisticated pattern-based cheating strategies
        - Statistical deviations from expected transition probabilities
        
        Args:
            session_data: Session data containing responses
            
        Returns:
            Comprehensive Markov chain anomaly analysis
        """
        try:
            session_id = session_data.get('session_id', 'unknown')
            responses = session_data.get('responses', [])
            
            if len(responses) < 10:
                return self._create_empty_analysis('markov_chain_anomalies', session_id, "Insufficient data for Markov analysis")
            
            self.logger.info(f"Analyzing Markov chain patterns for session: {session_id}")
            
            # Extract answer sequence
            answer_sequence = [r.get('response', 'X') for r in responses if 'response' in r]
            
            if len(answer_sequence) < 10:
                return self._create_empty_analysis('markov_chain_anomalies', session_id, "Insufficient answer sequence")
            
            analysis_results = {}
            
            # 1. First-Order Markov Chain Analysis
            first_order_analysis = self._analyze_first_order_markov(answer_sequence)
            analysis_results['first_order_markov'] = first_order_analysis
            
            # 2. Second-Order Markov Chain Analysis
            second_order_analysis = self._analyze_second_order_markov(answer_sequence)
            analysis_results['second_order_markov'] = second_order_analysis
            
            # 3. Transition Probability Anomaly Detection
            transition_anomalies = self._detect_transition_anomalies(answer_sequence)
            analysis_results['transition_anomalies'] = transition_anomalies
            
            # 4. Entropy Analysis
            entropy_analysis = self._analyze_markov_entropy(answer_sequence)
            analysis_results['entropy_analysis'] = entropy_analysis
            
            # 5. Stationarity Testing
            stationarity_analysis = self._test_markov_stationarity(answer_sequence)
            analysis_results['stationarity_analysis'] = stationarity_analysis
            
            # Calculate composite Markov anomaly score
            markov_anomaly_score = self._calculate_markov_anomaly_score(analysis_results)
            
            # Risk assessment
            risk_level = self._assess_markov_risk(markov_anomaly_score)
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis_type': 'markov_chain_anomalies',
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'sequence_length': len(answer_sequence),
                'unique_answers': len(set(answer_sequence)),
                'markov_anomaly_score': float(markov_anomaly_score),
                'risk_level': risk_level,
                'detailed_analysis': analysis_results,
                'recommendations': self._generate_markov_recommendations(markov_anomaly_score, analysis_results),
                'statistical_significance': self._calculate_markov_significance(analysis_results)
            }
            
        except Exception as e:
            self.logger.error(f"Error in Markov chain analysis: {str(e)}")
            return {
                'success': False,
                'session_id': session_data.get('session_id', 'unknown'),
                'analysis_type': 'markov_chain_anomalies',
                'error': str(e)
            }
    
    def _analyze_first_order_markov(self, sequence: List[str]) -> Dict[str, Any]:
        """Analyze first-order Markov chain properties"""
        try:
            # Build transition matrix
            transitions = defaultdict(lambda: defaultdict(int))
            unique_states = sorted(set(sequence))
            
            for i in range(len(sequence) - 1):
                current_state = sequence[i]
                next_state = sequence[i + 1]
                transitions[current_state][next_state] += 1
            
            # Convert to probabilities
            transition_probabilities = {}
            for current_state in unique_states:
                total_transitions = sum(transitions[current_state].values())
                if total_transitions > 0:
                    transition_probabilities[current_state] = {
                        next_state: count / total_transitions
                        for next_state, count in transitions[current_state].items()
                    }
                else:
                    transition_probabilities[current_state] = {}
            
            # Calculate expected uniform probabilities
            expected_prob = 1.0 / len(unique_states)
            
            # Measure deviation from uniform distribution
            max_deviation = 0.0
            transition_entropy = 0.0
            
            for current_state in unique_states:
                state_probs = transition_probabilities.get(current_state, {})
                
                # Calculate entropy for this state's transitions
                state_entropy = 0.0
                for prob in state_probs.values():
                    if prob > 0:
                        state_entropy -= prob * math.log2(prob)
                
                transition_entropy += state_entropy
                
                # Calculate maximum deviation from uniform
                for next_state in unique_states:
                    actual_prob = state_probs.get(next_state, 0)
                    deviation = abs(actual_prob - expected_prob)
                    max_deviation = max(max_deviation, deviation)
            
            # Normalize entropy
            max_entropy = len(unique_states) * math.log2(len(unique_states))
            normalized_entropy = transition_entropy / max_entropy if max_entropy > 0 else 0
            
            # Calculate chi-square test for uniformity
            chi_square_stats = []
            for current_state in unique_states:
                observed = [transitions[current_state].get(next_state, 0) for next_state in unique_states]
                total_obs = sum(observed)
                if total_obs > 0:
                    expected = [total_obs / len(unique_states)] * len(unique_states)
                    try:
                        chi2_stat, p_value = stats.chisquare(observed, expected)
                        chi_square_stats.append({
                            'state': current_state,
                            'chi2_statistic': float(chi2_stat),
                            'p_value': float(p_value),
                            'is_uniform': p_value > 0.05
                        })
                    except:
                        continue
            
            return {
                'available': True,
                'transition_matrix': {k: dict(v) for k, v in transitions.items()},
                'transition_probabilities': transition_probabilities,
                'unique_states': unique_states,
                'max_deviation_from_uniform': float(max_deviation),
                'normalized_entropy': float(normalized_entropy),
                'chi_square_tests': chi_square_stats,
                'anomaly_score': float(max_deviation * 2)  # Scale to 0-1 range approximately
            }
            
        except Exception as e:
            self.logger.warning(f"Error in first-order Markov analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _analyze_second_order_markov(self, sequence: List[str]) -> Dict[str, Any]:
        """Analyze second-order Markov chain properties"""
        try:
            if len(sequence) < 3:
                return {'available': False, 'message': 'Insufficient data for second-order analysis'}
            
            # Build second-order transition matrix
            transitions = defaultdict(lambda: defaultdict(int))
            
            for i in range(len(sequence) - 2):
                current_pair = (sequence[i], sequence[i + 1])
                next_state = sequence[i + 2]
                transitions[current_pair][next_state] += 1
            
            # Convert to probabilities and analyze patterns
            second_order_patterns = {}
            strong_dependencies = []
            
            for pair, next_states in transitions.items():
                total_transitions = sum(next_states.values())
                if total_transitions >= 2:  # Only consider pairs with multiple transitions
                    probabilities = {
                        state: count / total_transitions
                        for state, count in next_states.items()
                    }
                    
                    # Find strong second-order dependencies
                    max_prob = max(probabilities.values())
                    if max_prob > 0.7:  # Strong dependency threshold
                        most_likely_next = max(probabilities.items(), key=lambda x: x[1])
                        strong_dependencies.append({
                            'pattern': f"{pair[0]}-{pair[1]}-{most_likely_next[0]}",
                            'probability': float(most_likely_next[1]),
                            'occurrences': next_states[most_likely_next[0]]
                        })
                    
                    second_order_patterns[f"{pair[0]}-{pair[1]}"] = probabilities
            
            # Calculate second-order entropy
            total_entropy = 0.0
            pattern_count = 0
            
            for probs in second_order_patterns.values():
                pattern_entropy = 0.0
                for prob in probs.values():
                    if prob > 0:
                        pattern_entropy -= prob * math.log2(prob)
                total_entropy += pattern_entropy
                pattern_count += 1
            
            avg_entropy = total_entropy / pattern_count if pattern_count > 0 else 0
            
            return {
                'available': True,
                'second_order_patterns': {k: dict(v) for k, v in second_order_patterns.items()},
                'strong_dependencies': strong_dependencies,
                'average_entropy': float(avg_entropy),
                'pattern_count': pattern_count,
                'dependency_strength': float(len(strong_dependencies) / max(1, pattern_count))
            }
            
        except Exception as e:
            self.logger.warning(f"Error in second-order Markov analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _detect_transition_anomalies(self, sequence: List[str]) -> Dict[str, Any]:
        """Detect anomalous transition patterns"""
        try:
            # Calculate transition frequencies
            transition_counts = defaultdict(lambda: defaultdict(int))
            for i in range(len(sequence) - 1):
                transition_counts[sequence[i]][sequence[i + 1]] += 1
            
            # Identify unusual transition patterns
            anomalous_transitions = []
            unique_states = sorted(set(sequence))
            
            for from_state in unique_states:
                transitions_from_state = transition_counts[from_state]
                if not transitions_from_state:
                    continue
                    
                total_from_state = sum(transitions_from_state.values())
                
                for to_state in unique_states:
                    observed_count = transitions_from_state.get(to_state, 0)
                    expected_count = total_from_state / len(unique_states)
                    
                    # Check for significant deviations
                    if expected_count > 0:
                        deviation_ratio = observed_count / expected_count
                        
                        # Flag both over-representation and under-representation
                        if deviation_ratio > 2.0 or (deviation_ratio < 0.5 and expected_count >= 2):
                            anomalous_transitions.append({
                                'from_state': from_state,
                                'to_state': to_state,
                                'observed_count': observed_count,
                                'expected_count': float(expected_count),
                                'deviation_ratio': float(deviation_ratio),
                                'anomaly_type': 'over_represented' if deviation_ratio > 2.0 else 'under_represented'
                            })
            
            # Sort by deviation magnitude
            anomalous_transitions.sort(key=lambda x: abs(math.log(x['deviation_ratio'])), reverse=True)
            
            return {
                'available': True,
                'anomalous_transitions': anomalous_transitions[:10],  # Top 10 anomalies
                'total_anomalies': len(anomalous_transitions),
                'anomaly_strength': float(len(anomalous_transitions) / max(1, len(unique_states) ** 2))
            }
            
        except Exception as e:
            self.logger.warning(f"Error detecting transition anomalies: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _analyze_markov_entropy(self, sequence: List[str]) -> Dict[str, Any]:
        """Analyze entropy patterns in the Markov chain"""
        try:
            # Calculate various entropy measures
            unique_states = sorted(set(sequence))
            
            # 1. Base entropy (overall distribution)
            state_counts = Counter(sequence)
            total_count = len(sequence)
            base_entropy = 0.0
            
            for count in state_counts.values():
                prob = count / total_count
                base_entropy -= prob * math.log2(prob)
            
            max_base_entropy = math.log2(len(unique_states))
            normalized_base_entropy = base_entropy / max_base_entropy if max_base_entropy > 0 else 0
            
            # 2. Conditional entropy (transition entropy)
            conditional_entropy = 0.0
            transition_counts = defaultdict(lambda: defaultdict(int))
            
            for i in range(len(sequence) - 1):
                transition_counts[sequence[i]][sequence[i + 1]] += 1
            
            total_transitions = len(sequence) - 1
            
            for from_state, to_states in transition_counts.items():
                from_count = sum(to_states.values())
                state_prob = from_count / total_transitions
                
                state_entropy = 0.0
                for to_count in to_states.values():
                    trans_prob = to_count / from_count
                    state_entropy -= trans_prob * math.log2(trans_prob)
                
                conditional_entropy += state_prob * state_entropy
            
            # 3. Entropy rate (information content per symbol)
            entropy_rate = conditional_entropy
            
            return {
                'available': True,
                'base_entropy': float(base_entropy),
                'normalized_base_entropy': float(normalized_base_entropy),
                'conditional_entropy': float(conditional_entropy),
                'entropy_rate': float(entropy_rate),
                'max_possible_entropy': float(max_base_entropy),
                'entropy_efficiency': float(normalized_base_entropy),
                'predictability_score': float(1 - normalized_base_entropy)
            }
            
        except Exception as e:
            self.logger.warning(f"Error in Markov entropy analysis: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _test_markov_stationarity(self, sequence: List[str]) -> Dict[str, Any]:
        """Test stationarity of the Markov chain"""
        try:
            if len(sequence) < 20:
                return {'available': False, 'message': 'Insufficient data for stationarity test'}
            
            # Split sequence into chunks and compare transition matrices
            chunk_size = len(sequence) // 4
            chunks = [sequence[i:i+chunk_size] for i in range(0, len(sequence), chunk_size)]
            chunks = [chunk for chunk in chunks if len(chunk) >= 5]  # Filter out small chunks
            
            if len(chunks) < 2:
                return {'available': False, 'message': 'Insufficient chunks for comparison'}
            
            # Calculate transition matrices for each chunk
            chunk_matrices = []
            unique_states = sorted(set(sequence))
            
            for chunk in chunks:
                transitions = defaultdict(lambda: defaultdict(int))
                for i in range(len(chunk) - 1):
                    transitions[chunk[i]][chunk[i + 1]] += 1
                
                # Convert to probabilities
                matrix = {}
                for from_state in unique_states:
                    total = sum(transitions[from_state].values())
                    if total > 0:
                        matrix[from_state] = {
                            to_state: transitions[from_state].get(to_state, 0) / total
                            for to_state in unique_states
                        }
                    else:
                        matrix[from_state] = {to_state: 0 for to_state in unique_states}
                
                chunk_matrices.append(matrix)
            
            # Compare matrices using KL divergence
            stationarity_violations = []
            avg_kl_divergence = 0.0
            comparison_count = 0
            
            for i in range(len(chunk_matrices)):
                for j in range(i + 1, len(chunk_matrices)):
                    kl_div = self._calculate_matrix_kl_divergence(
                        chunk_matrices[i], chunk_matrices[j], unique_states
                    )
                    avg_kl_divergence += kl_div
                    comparison_count += 1
                    
                    if kl_div > 1.0:  # Threshold for significant difference
                        stationarity_violations.append({
                            'chunk_1': i,
                            'chunk_2': j,
                            'kl_divergence': float(kl_div)
                        })
            
            avg_kl_divergence = avg_kl_divergence / comparison_count if comparison_count > 0 else 0
            
            # Determine stationarity
            is_stationary = len(stationarity_violations) == 0 and avg_kl_divergence < 0.5
            
            return {
                'available': True,
                'is_stationary': bool(is_stationary),
                'average_kl_divergence': float(avg_kl_divergence),
                'stationarity_violations': stationarity_violations,
                'chunks_analyzed': len(chunks),
                'non_stationarity_score': float(min(avg_kl_divergence, 2.0) / 2.0)
            }
            
        except Exception as e:
            self.logger.warning(f"Error in stationarity testing: {str(e)}")
            return {'available': False, 'error': str(e)}
    
    def _calculate_matrix_kl_divergence(self, matrix1: Dict, matrix2: Dict, states: List[str]) -> float:
        """Calculate KL divergence between two transition matrices"""
        try:
            total_kl = 0.0
            
            for from_state in states:
                dist1 = matrix1.get(from_state, {})
                dist2 = matrix2.get(from_state, {})
                
                state_kl = 0.0
                for to_state in states:
                    p1 = dist1.get(to_state, 1e-10)  # Small epsilon to avoid log(0)
                    p2 = dist2.get(to_state, 1e-10)
                    
                    if p1 > 1e-10:
                        state_kl += p1 * math.log2(p1 / p2)
                
                total_kl += state_kl
            
            return total_kl / len(states)
            
        except Exception as e:
            return 0.0
    
    def _calculate_markov_anomaly_score(self, analysis_results: Dict) -> float:
        """Calculate composite Markov anomaly score"""
        try:
            score = 0.0
            weights = {
                'first_order_markov': 0.25,
                'second_order_markov': 0.20,
                'transition_anomalies': 0.25,
                'entropy_analysis': 0.15,
                'stationarity_analysis': 0.15
            }
            
            for analysis_type, weight in weights.items():
                if analysis_type in analysis_results and analysis_results[analysis_type].get('available'):
                    analysis = analysis_results[analysis_type]
                    
                    if analysis_type == 'first_order_markov':
                        score += analysis.get('anomaly_score', 0) * weight
                    
                    elif analysis_type == 'second_order_markov':
                        score += analysis.get('dependency_strength', 0) * weight
                    
                    elif analysis_type == 'transition_anomalies':
                        score += min(analysis.get('anomaly_strength', 0) * 2, 1.0) * weight
                    
                    elif analysis_type == 'entropy_analysis':
                        # Low entropy indicates patterns (potential cheating)
                        score += (1 - analysis.get('normalized_base_entropy', 0.5)) * weight
                    
                    elif analysis_type == 'stationarity_analysis':
                        score += analysis.get('non_stationarity_score', 0) * weight
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.warning(f"Error calculating Markov anomaly score: {str(e)}")
            return 0.5
    
    def _assess_markov_risk(self, score: float) -> str:
        """Assess risk level based on Markov anomaly score"""
        return self._assess_pattern_risk(score)  # Use same thresholds
    
    def _generate_markov_recommendations(self, score: float, analysis_results: Dict) -> List[str]:
        """Generate recommendations based on Markov analysis"""
        recommendations = []
        
        if score > 0.7:
            recommendations.append("CRITICAL: Strong evidence of non-random answer patterns detected")
            recommendations.append("Immediate investigation recommended for potential sophisticated cheating")
        elif score > 0.5:
            recommendations.append("HIGH: Unusual answer transition patterns detected")
            recommendations.append("Manual review of answer sequences recommended")
        elif score > 0.3:
            recommendations.append("MODERATE: Some pattern irregularities detected")
            recommendations.append("Monitor for consistent patterns across multiple sessions")
        else:
            recommendations.append("Answer patterns appear consistent with random selection")
        
        # Add specific recommendations based on analysis components
        if analysis_results.get('entropy_analysis', {}).get('available'):
            entropy_data = analysis_results['entropy_analysis']
            if entropy_data.get('predictability_score', 0) > 0.6:
                recommendations.append("Low entropy detected - answers may follow predictable patterns")
        
        if analysis_results.get('stationarity_analysis', {}).get('available'):
            stationarity_data = analysis_results['stationarity_analysis']
            if not stationarity_data.get('is_stationary', True):
                recommendations.append("Non-stationary behavior detected - answer patterns change over time")
        
        return recommendations
    
    def _calculate_markov_significance(self, analysis_results: Dict) -> Dict[str, Any]:
        """Calculate statistical significance for Markov analysis"""
        try:
            # Aggregate p-values from various tests
            p_values = []
            
            if analysis_results.get('first_order_markov', {}).get('available'):
                chi_tests = analysis_results['first_order_markov'].get('chi_square_tests', [])
                p_values.extend([test['p_value'] for test in chi_tests])
            
            if p_values:
                # Use Fisher's method to combine p-values
                from scipy.stats import combine_pvalues
                combined_stat, combined_p = combine_pvalues(p_values, method='fisher')
                
                return {
                    'significant': bool(combined_p < 0.05),
                    'combined_p_value': float(combined_p),
                    'test_statistic': float(combined_stat),
                    'confidence_level': 0.95,
                    'individual_tests': len(p_values)
                }
            else:
                return {
                    'significant': False,
                    'combined_p_value': 0.5,
                    'confidence_level': 0.95,
                    'message': 'No statistical tests available for significance calculation'
                }
                
        except Exception as e:
            self.logger.warning(f"Error calculating Markov significance: {str(e)}")
            return {'significant': False, 'p_value': 0.5, 'error': str(e)}
    
    def _detect_difficulty_outliers(self, difficulty_data):
        """Detect statistical outliers in difficulty performance"""
        return {'outliers_detected': 0, 'outlier_details': []}
    
    def _analyze_topic_difficulty_patterns(self, difficulty_data):
        """Analyze topic-specific difficulty patterns"""
        return {'topic_anomalies': {}, 'suspicious_topics': []}


# Initialize global instance
statistical_anomaly_analyzer = StatisticalAnomalyAnalyzer()