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
        """Find positional clustering in answers (placeholder implementation)"""
        return {'available': True, 'clustering_strength': 0.2}
    
    def _calculate_performance_progression(self, bin_performance: Dict) -> Dict[str, Any]:
        """Calculate performance progression metrics (placeholder implementation)"""
        return {'trend': 'normal', 'anomaly_detected': False}
    
    # Additional placeholder methods for timing, collaboration analysis, etc.
    def _extract_timing_data(self, session_data):
        """Extract timing data from session"""
        return {'timestamps': [], 'session_start': None, 'session_end': None, 'total_duration_minutes': 0}
    
    def _analyze_timezone_consistency(self, timing_data, session_data):
        """Analyze timezone consistency"""
        return {'consistent': True, 'anomaly_score': 0.2}
    
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
    
    # Additional helper methods for remaining implementations
    def _analyze_difficulty_progression_patterns(self, difficulty_data):
        """Analyze difficulty progression patterns"""
        return {'progression_anomaly': False, 'pattern_strength': 0.2}
    
    def _detect_difficulty_outliers(self, difficulty_data):
        """Detect statistical outliers in difficulty performance"""
        return {'outliers_detected': 0, 'outlier_details': []}
    
    def _analyze_topic_difficulty_patterns(self, difficulty_data):
        """Analyze topic-specific difficulty patterns"""
        return {'topic_anomalies': {}, 'suspicious_topics': []}


# Initialize global instance
statistical_anomaly_analyzer = StatisticalAnomalyAnalyzer()