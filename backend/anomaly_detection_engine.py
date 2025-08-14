"""
📈 MODULE 2: STATISTICAL ANOMALY DETECTION SYSTEM
ML-Powered Pattern Recognition Engine for Advanced Anti-Cheating

This module implements comprehensive statistical anomaly detection including:
- ML-powered baseline model training from historical data
- Real-time response pattern anomaly detection
- Performance inconsistency analysis
- Probabilistic anomaly scoring with confidence intervals

Dependencies: numpy, scipy, pandas, sklearn (built-in Python libraries)
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import uuid
import statistics
from collections import defaultdict
import asyncio
import joblib
import os

class AnomalyDetectionEngine:
    """
    Advanced ML-powered anomaly detection engine for identifying cheating patterns
    Combines multiple statistical and machine learning approaches for robust detection
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Model storage
        self.baseline_models = {}
        self.scalers = {}
        self.anomaly_detectors = {}
        
        # Configuration parameters
        self.anomaly_threshold = 0.7  # Anomaly probability threshold
        self.contamination_rate = 0.1  # Expected anomaly rate for training
        self.confidence_level = 0.95  # Statistical confidence level
        
        # Feature importance tracking
        self.feature_weights = {
            'response_time_consistency': 0.25,
            'accuracy_pattern': 0.20,
            'difficulty_progression': 0.15,
            'timing_regularity': 0.15,
            'answer_change_frequency': 0.10,
            'cognitive_load_indicators': 0.10,
            'behavioral_consistency': 0.05
        }
        
        # Model paths for persistence
        self.model_dir = "/app/backend/models"
        self._ensure_model_directory()
        
    def _ensure_model_directory(self):
        """Ensure model directory exists"""
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
    
    def train_baseline_models(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train baseline ML models from historical legitimate user data
        
        Args:
            historical_data: List of historical session data from legitimate users
            Format: [{"session_id": "...", "responses": [...], "timings": [...], "scores": [...]}]
        
        Returns:
            Training results with model performance metrics
        """
        try:
            self.logger.info(f"Starting baseline model training with {len(historical_data)} sessions")
            
            # Extract comprehensive features from historical data
            features_df = self._extract_comprehensive_features(historical_data)
            
            if features_df.empty:
                raise ValueError("No valid features could be extracted from historical data")
            
            # Split features into training components
            X = features_df.drop(['session_id', 'is_legitimate'], axis=1, errors='ignore')
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            self.scalers['baseline'] = scaler
            
            # Train multiple anomaly detection models
            training_results = {}
            
            # 1. Isolation Forest for outlier detection
            isolation_forest = IsolationForest(
                contamination=self.contamination_rate,
                random_state=42,
                n_estimators=100
            )
            isolation_forest.fit(X_scaled)
            self.anomaly_detectors['isolation_forest'] = isolation_forest
            
            # 2. DBSCAN for density-based clustering
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            dbscan_labels = dbscan.fit_predict(X_scaled)
            self.anomaly_detectors['dbscan'] = dbscan
            
            # 3. Statistical baseline models for each feature
            baseline_stats = {}
            for column in X.columns:
                values = X[column].dropna()
                if len(values) > 0:
                    baseline_stats[column] = {
                        'mean': float(values.mean()),
                        'std': float(values.std()),
                        'median': float(values.median()),
                        'q25': float(values.quantile(0.25)),
                        'q75': float(values.quantile(0.75)),
                        'min': float(values.min()),
                        'max': float(values.max())
                    }
            
            self.baseline_models['statistical'] = baseline_stats
            
            # 4. PCA for dimensionality reduction and reconstruction error
            pca = PCA(n_components=min(10, X_scaled.shape[1]))
            pca.fit(X_scaled)
            self.baseline_models['pca'] = pca
            
            # Calculate training metrics
            isolation_scores = isolation_forest.decision_function(X_scaled)
            dbscan_outliers = (dbscan_labels == -1).sum()
            
            training_results = {
                'success': True,
                'training_date': datetime.utcnow().isoformat(),
                'num_training_samples': len(historical_data),
                'num_features': X.shape[1],
                'feature_names': list(X.columns),
                'isolation_forest_score_range': {
                    'min': float(isolation_scores.min()),
                    'max': float(isolation_scores.max()),
                    'mean': float(isolation_scores.mean())
                },
                'dbscan_clusters': len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0),
                'dbscan_outliers': int(dbscan_outliers),
                'pca_explained_variance': float(pca.explained_variance_ratio_.sum()),
                'statistical_baselines': baseline_stats
            }
            
            # Save models to disk
            self._save_models()
            
            self.logger.info(f"Baseline model training completed successfully")
            return training_results
            
        except Exception as e:
            self.logger.error(f"Error in baseline model training: {str(e)}")
            raise Exception(f"Baseline model training failed: {str(e)}")
    
    def detect_response_pattern_anomalies(self, current_session: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect anomalies in current session response patterns using trained models
        
        Args:
            current_session: Current test session data
            Format: {"session_id": "...", "responses": [...], "timings": [...]}
        
        Returns:
            Detailed anomaly analysis results
        """
        try:
            session_id = current_session.get('session_id', 'unknown')
            self.logger.info(f"Analyzing response pattern anomalies for session: {session_id}")
            
            # Extract features from current session
            features = self._extract_session_features(current_session)
            
            if not features:
                return {
                    'success': False,
                    'error': 'Could not extract features from session data'
                }
            
            # Convert to DataFrame for consistent processing
            features_df = pd.DataFrame([features])
            X = features_df.drop(['session_id'], axis=1, errors='ignore')
            
            # Scale features using trained scaler
            if 'baseline' not in self.scalers:
                raise ValueError("No trained scaler available. Please train baseline models first.")
            
            X_scaled = self.scalers['baseline'].transform(X)
            
            # Detect anomalies using multiple approaches
            anomaly_results = {}
            
            # 1. Isolation Forest anomaly detection
            if 'isolation_forest' in self.anomaly_detectors:
                isolation_score = self.anomaly_detectors['isolation_forest'].decision_function(X_scaled)[0]
                isolation_anomaly = self.anomaly_detectors['isolation_forest'].predict(X_scaled)[0] == -1
                
                anomaly_results['isolation_forest'] = {
                    'anomaly_detected': bool(isolation_anomaly),
                    'anomaly_score': float(isolation_score),
                    'confidence': abs(float(isolation_score))
                }
            
            # 2. Statistical anomaly detection
            if 'statistical' in self.baseline_models:
                statistical_anomalies = self._detect_statistical_anomalies(features, self.baseline_models['statistical'])
                anomaly_results['statistical'] = statistical_anomalies
            
            # 3. PCA reconstruction error
            if 'pca' in self.baseline_models:
                pca_score = self._calculate_pca_anomaly_score(X_scaled[0], self.baseline_models['pca'])
                anomaly_results['pca_reconstruction'] = {
                    'reconstruction_error': float(pca_score),
                    'anomaly_detected': pca_score > 2.0,  # Threshold for reconstruction error
                    'confidence': min(float(pca_score / 2.0), 1.0)
                }
            
            # 4. Response pattern specific anomalies
            pattern_anomalies = self._analyze_response_patterns(current_session)
            anomaly_results['response_patterns'] = pattern_anomalies
            
            # Calculate overall anomaly assessment
            overall_assessment = self._calculate_overall_anomaly_assessment(anomaly_results)
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'individual_analyses': anomaly_results,
                'overall_assessment': overall_assessment,
                'feature_analysis': self._analyze_feature_contributions(features, X.columns.tolist()),
                'recommendation': self._generate_anomaly_recommendation(overall_assessment)
            }
            
        except Exception as e:
            self.logger.error(f"Error in response pattern anomaly detection: {str(e)}")
            return {
                'success': False,
                'session_id': current_session.get('session_id', 'unknown'),
                'error': str(e)
            }
    
    def analyze_performance_inconsistencies(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance inconsistencies that may indicate cheating
        
        Args:
            session_data: Complete session data with responses and timings
        
        Returns:
            Detailed performance inconsistency analysis
        """
        try:
            session_id = session_data.get('session_id', 'unknown')
            responses = session_data.get('responses', [])
            timings = session_data.get('timings', [])
            
            self.logger.info(f"Analyzing performance inconsistencies for session: {session_id}")
            
            if not responses:
                return {
                    'success': False,
                    'error': 'Insufficient data for performance analysis'
                }
            
            inconsistencies = {}
            
            # 1. Response time inconsistency analysis - Handle both data formats
            response_times = []
            if timings:
                # Format 1: Separate timings array
                response_times = [t.get('response_time', 0) for t in timings if 'response_time' in t]
            else:
                # Format 2: Response times embedded in responses (test data format)
                response_times = [r.get('response_time', 0) for r in responses if 'response_time' in r]
                
            if response_times:
                time_analysis = self._analyze_response_time_consistency(response_times)
                inconsistencies['response_time'] = time_analysis
            
            # 2. Accuracy vs difficulty inconsistency
            accuracy_analysis = self._analyze_accuracy_difficulty_consistency(responses)
            inconsistencies['accuracy_difficulty'] = accuracy_analysis
            
            # 3. Learning curve analysis
            learning_curve = self._analyze_learning_curve_anomalies(responses, timings)
            inconsistencies['learning_curve'] = learning_curve
            
            # 4. Cognitive load indicators
            cognitive_load = self._analyze_cognitive_load_inconsistencies(responses, timings)
            inconsistencies['cognitive_load'] = cognitive_load
            
            # 5. Answer change pattern analysis
            answer_changes = self._analyze_answer_change_patterns(responses)
            inconsistencies['answer_changes'] = answer_changes
            
            # Calculate composite inconsistency score
            composite_score = self._calculate_composite_inconsistency_score(inconsistencies)
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'inconsistency_analyses': inconsistencies,
                'composite_inconsistency_score': composite_score,
                'risk_level': self._determine_risk_level(composite_score),
                'detailed_findings': self._generate_detailed_findings(inconsistencies),
                'recommendations': self._generate_inconsistency_recommendations(composite_score)
            }
            
        except Exception as e:
            self.logger.error(f"Error in performance inconsistency analysis: {str(e)}")
            return {
                'success': False,
                'session_id': session_data.get('session_id', 'unknown'),
                'error': str(e)
            }
    
    def calculate_anomaly_probability_scores(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive anomaly probability scores with confidence intervals
        
        Args:
            session_data: Complete session data for probability calculation
        
        Returns:
            Detailed probability scores and confidence metrics
        """
        try:
            session_id = session_data.get('session_id', 'unknown')
            self.logger.info(f"Calculating anomaly probabilities for session: {session_id}")
            
            # Get anomaly detection results
            anomaly_results = self.detect_response_pattern_anomalies(session_data)
            inconsistency_results = self.analyze_performance_inconsistencies(session_data)
            
            if not anomaly_results.get('success') or not inconsistency_results.get('success'):
                return {
                    'success': False,
                    'error': 'Could not complete prerequisite analyses'
                }
            
            # Extract probability components
            probability_components = {}
            
            # 1. ML model probabilities
            if 'individual_analyses' in anomaly_results:
                ml_analyses = anomaly_results['individual_analyses']
                
                if 'isolation_forest' in ml_analyses:
                    iso_score = ml_analyses['isolation_forest'].get('confidence', 0)
                    probability_components['isolation_forest_prob'] = self._convert_to_probability(iso_score)
                
                if 'statistical' in ml_analyses:
                    stat_anomalies = ml_analyses['statistical'].get('total_anomalies', 0)
                    total_features = ml_analyses['statistical'].get('total_features', 1)
                    probability_components['statistical_prob'] = stat_anomalies / max(total_features, 1)
                
                if 'pca_reconstruction' in ml_analyses:
                    pca_error = ml_analyses['pca_reconstruction'].get('reconstruction_error', 0)
                    probability_components['pca_prob'] = min(pca_error / 5.0, 1.0)  # Normalize to probability
            
            # 2. Performance inconsistency probabilities
            if 'composite_inconsistency_score' in inconsistency_results:
                inconsistency_score = inconsistency_results['composite_inconsistency_score']
                probability_components['inconsistency_prob'] = inconsistency_score / 100.0  # Convert to probability
            
            # 3. Behavioral pattern probabilities
            behavioral_prob = self._calculate_behavioral_anomaly_probability(session_data)
            probability_components['behavioral_prob'] = behavioral_prob
            
            # Calculate weighted composite probability
            weighted_probability = self._calculate_weighted_probability(probability_components)
            
            # Calculate confidence intervals
            confidence_intervals = self._calculate_confidence_intervals(probability_components, weighted_probability)
            
            # Risk classification
            risk_classification = self._classify_risk_level(weighted_probability)
            
            # Generate detailed probability breakdown
            probability_breakdown = self._generate_probability_breakdown(probability_components)
            
            return {
                'success': True,
                'session_id': session_id,
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'composite_anomaly_probability': float(weighted_probability),
                'confidence_intervals': confidence_intervals,
                'risk_classification': risk_classification,
                'probability_components': probability_components,
                'probability_breakdown': probability_breakdown,
                'statistical_significance': self._calculate_statistical_significance(weighted_probability),
                'recommendation_actions': self._generate_probability_based_recommendations(weighted_probability, risk_classification)
            }
            
        except Exception as e:
            self.logger.error(f"Error in anomaly probability calculation: {str(e)}")
            return {
                'success': False,
                'session_id': session_data.get('session_id', 'unknown'),
                'error': str(e)
            }
    
    # ===== HELPER METHODS =====
    
    def _extract_comprehensive_features(self, historical_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Extract comprehensive features from historical data for training"""
        features_list = []
        
        for session in historical_data:
            try:
                session_features = self._extract_session_features(session)
                if session_features:
                    session_features['is_legitimate'] = True  # Historical data assumed legitimate
                    features_list.append(session_features)
            except Exception as e:
                self.logger.warning(f"Could not extract features from session {session.get('session_id', 'unknown')}: {e}")
                continue
        
        return pd.DataFrame(features_list)
    
    def _extract_session_features(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract comprehensive features from a single session"""
        try:
            session_id = session_data.get('session_id', str(uuid.uuid4()))
            responses = session_data.get('responses', [])
            timings = session_data.get('timings', [])
            
            if not responses:
                return {}
            
            features = {'session_id': session_id}
            
            # Response time features - Handle both data formats
            response_times = []
            if timings:
                # Format 1: Separate timings array
                response_times = [t.get('response_time', 0) for t in timings if 'response_time' in t]
            else:
                # Format 2: Response times embedded in responses (test data format)
                response_times = [r.get('response_time', 0) for r in responses if 'response_time' in r]
            if response_times:
                features.update({
                    'avg_response_time': statistics.mean(response_times),
                    'std_response_time': statistics.stdev(response_times) if len(response_times) > 1 else 0,
                    'median_response_time': statistics.median(response_times),
                    'response_time_cv': statistics.stdev(response_times) / statistics.mean(response_times) if statistics.mean(response_times) > 0 and len(response_times) > 1 else 0
                })
            
            # Accuracy features
            correct_responses = [r for r in responses if r.get('is_correct', False)]
            features.update({
                'accuracy_rate': len(correct_responses) / len(responses) if responses else 0,
                'total_responses': len(responses),
                'correct_responses': len(correct_responses)
            })
            
            # Difficulty progression features
            if 'difficulty' in responses[0] if responses else {}:
                difficulties = [r.get('difficulty', 1) for r in responses]
                accuracies = [1 if r.get('is_correct', False) else 0 for r in responses]
                
                # Calculate difficulty-accuracy correlation
                if len(difficulties) > 1 and len(set(difficulties)) > 1:
                    correlation = np.corrcoef(difficulties, accuracies)[0, 1] if not np.isnan(np.corrcoef(difficulties, accuracies)[0, 1]) else 0
                    features['difficulty_accuracy_correlation'] = correlation
                else:
                    features['difficulty_accuracy_correlation'] = 0
            
            # Timing regularity features
            if len(response_times) > 2:
                # Calculate timing consistency using autocorrelation
                time_diffs = np.diff(response_times)
                if len(time_diffs) > 1:
                    features['timing_regularity'] = 1 - (np.std(time_diffs) / (np.mean(time_diffs) + 1e-6))
                else:
                    features['timing_regularity'] = 1.0
            else:
                features['timing_regularity'] = 1.0
            
            # Answer change frequency
            answer_changes = 0
            for response in responses:
                if 'answer_history' in response and len(response['answer_history']) > 1:
                    answer_changes += len(response['answer_history']) - 1
            
            features['answer_change_frequency'] = answer_changes / len(responses) if responses else 0
            
            # Cognitive load indicators
            features.update(self._calculate_cognitive_load_features(responses, timings))
            
            return features
            
        except Exception as e:
            self.logger.error(f"Error extracting session features: {str(e)}")
            return {}
    
    def _calculate_cognitive_load_features(self, responses: List[Dict], timings: List[Dict]) -> Dict[str, float]:
        """Calculate cognitive load indicators from response patterns"""
        features = {}
        
        try:
            # Response time variability as cognitive load indicator - Handle both data formats
            response_times = []
            if timings:
                # Format 1: Separate timings array
                response_times = [t.get('response_time', 0) for t in timings if 'response_time' in t]
            else:
                # Format 2: Response times embedded in responses (test data format)
                response_times = [r.get('response_time', 0) for r in responses if 'response_time' in r]
            
            if len(response_times) > 2:
                # Calculate variability patterns
                time_changes = np.diff(response_times)
                features['response_time_variability'] = np.std(time_changes) if len(time_changes) > 0 else 0
                
                # Sudden speed changes (potential indicator of external help)
                speed_changes = []
                for i in range(1, len(response_times)):
                    if response_times[i-1] > 0:
                        speed_ratio = response_times[i] / response_times[i-1]
                        speed_changes.append(abs(speed_ratio - 1))
                
                features['speed_change_magnitude'] = np.mean(speed_changes) if speed_changes else 0
            else:
                features['response_time_variability'] = 0
                features['speed_change_magnitude'] = 0
            
            # Question complexity vs response time consistency
            if responses and 'difficulty' in responses[0]:
                complexities = [r.get('difficulty', 1) for r in responses]
                
                if len(response_times) == len(complexities) and len(complexities) > 1:
                    complexity_time_corr = np.corrcoef(complexities, response_times)[0, 1]
                    features['complexity_time_correlation'] = complexity_time_corr if not np.isnan(complexity_time_corr) else 0
                else:
                    features['complexity_time_correlation'] = 0
            else:
                features['complexity_time_correlation'] = 0
            
        except Exception as e:
            self.logger.warning(f"Error calculating cognitive load features: {str(e)}")
            features = {
                'response_time_variability': 0,
                'speed_change_magnitude': 0,
                'complexity_time_correlation': 0
            }
        
        return features
    
    def _detect_statistical_anomalies(self, features: Dict[str, Any], baseline_stats: Dict[str, Dict]) -> Dict[str, Any]:
        """Detect statistical anomalies by comparing features to baseline statistics"""
        anomalies = {}
        total_features = 0
        anomalous_features = 0
        
        for feature_name, value in features.items():
            if feature_name in baseline_stats and isinstance(value, (int, float)):
                baseline = baseline_stats[feature_name]
                total_features += 1
                
                # Z-score based anomaly detection
                if baseline['std'] > 0:
                    z_score = abs((value - baseline['mean']) / baseline['std'])
                    is_anomalous = z_score > 2.0  # 2 standard deviations
                    
                    if is_anomalous:
                        anomalous_features += 1
                    
                    anomalies[feature_name] = {
                        'value': float(value),
                        'baseline_mean': baseline['mean'],
                        'z_score': float(z_score),
                        'is_anomalous': is_anomalous,
                        'percentile': self._calculate_percentile(value, baseline)
                    }
        
        return {
            'feature_anomalies': anomalies,
            'total_features': total_features,
            'total_anomalies': anomalous_features,
            'anomaly_rate': anomalous_features / max(total_features, 1)
        }
    
    def _calculate_percentile(self, value: float, baseline: Dict) -> float:
        """Calculate percentile of value within baseline distribution"""
        try:
            # Approximate percentile using quartiles
            if value <= baseline['q25']:
                return 25.0 * (value - baseline['min']) / max(baseline['q25'] - baseline['min'], 1e-6)
            elif value <= baseline['median']:
                return 25.0 + 25.0 * (value - baseline['q25']) / max(baseline['median'] - baseline['q25'], 1e-6)
            elif value <= baseline['q75']:
                return 50.0 + 25.0 * (value - baseline['median']) / max(baseline['q75'] - baseline['median'], 1e-6)
            else:
                return 75.0 + 25.0 * min((value - baseline['q75']) / max(baseline['max'] - baseline['q75'], 1e-6), 1.0)
        except:
            return 50.0  # Default to median percentile
    
    def _calculate_pca_anomaly_score(self, sample: np.ndarray, pca_model) -> float:
        """Calculate PCA reconstruction error as anomaly score"""
        try:
            # Transform and reconstruct
            transformed = pca_model.transform([sample])
            reconstructed = pca_model.inverse_transform(transformed)
            
            # Calculate reconstruction error
            error = np.sum((sample - reconstructed[0]) ** 2)
            return float(error)
        except:
            return 0.0
    
    def _analyze_response_patterns(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze specific response patterns for anomalies"""
        responses = session_data.get('responses', [])
        patterns = {}
        
        try:
            # Pattern 1: Suspicious consistency in wrong answers
            wrong_responses = [r for r in responses if not r.get('is_correct', False)]
            if len(wrong_responses) > 5:
                wrong_times = [r.get('response_time', 0) for r in wrong_responses if 'response_time' in r]
                if wrong_times:
                    wrong_time_consistency = 1 - (statistics.stdev(wrong_times) / max(statistics.mean(wrong_times), 1e-6))
                    patterns['wrong_answer_consistency'] = {
                        'consistency_score': float(wrong_time_consistency),
                        'is_suspicious': wrong_time_consistency > 0.8,
                        'confidence': min(wrong_time_consistency, 1.0)
                    }
            
            # Pattern 2: Unusual accuracy on difficult questions
            if responses and 'difficulty' in responses[0]:
                difficult_questions = [r for r in responses if r.get('difficulty', 1) >= 4]
                if difficult_questions:
                    difficult_accuracy = sum(1 for r in difficult_questions if r.get('is_correct', False)) / len(difficult_questions)
                    overall_accuracy = sum(1 for r in responses if r.get('is_correct', False)) / len(responses)
                    
                    patterns['difficult_question_performance'] = {
                        'difficult_accuracy': float(difficult_accuracy),
                        'overall_accuracy': float(overall_accuracy),
                        'performance_ratio': float(difficult_accuracy / max(overall_accuracy, 0.01)),
                        'is_suspicious': difficult_accuracy > overall_accuracy * 1.5,
                        'confidence': abs(difficult_accuracy - overall_accuracy)
                    }
            
            # Pattern 3: Response time clustering
            if len(responses) > 10:
                response_times = [r.get('response_time', 0) for r in responses if 'response_time' in r]
                if response_times:
                    # Simple clustering analysis
                    time_clusters = self._simple_time_clustering(response_times)
                    patterns['response_time_clustering'] = time_clusters
                    
        except Exception as e:
            self.logger.warning(f"Error in response pattern analysis: {str(e)}")
        
        return patterns
    
    def _simple_time_clustering(self, response_times: List[float]) -> Dict[str, Any]:
        """Simple clustering analysis of response times"""
        try:
            # Divide into fast, medium, slow categories
            sorted_times = sorted(response_times)
            q33 = sorted_times[len(sorted_times)//3]
            q66 = sorted_times[2*len(sorted_times)//3]
            
            fast_times = [t for t in response_times if t <= q33]
            medium_times = [t for t in response_times if q33 < t <= q66]
            slow_times = [t for t in response_times if t > q66]
            
            # Calculate clustering score (higher = more clustered)
            total_variance = statistics.variance(response_times) if len(response_times) > 1 else 0
            within_cluster_variance = 0
            
            for cluster in [fast_times, medium_times, slow_times]:
                if len(cluster) > 1:
                    within_cluster_variance += statistics.variance(cluster) * len(cluster)
            
            within_cluster_variance /= len(response_times)
            clustering_score = 1 - (within_cluster_variance / max(total_variance, 1e-6))
            
            return {
                'clustering_score': float(clustering_score),
                'is_highly_clustered': clustering_score > 0.7,  # Threshold for suspicion
                'cluster_distribution': {
                    'fast': len(fast_times),
                    'medium': len(medium_times),
                    'slow': len(slow_times)
                },
                'confidence': float(clustering_score)
            }
            
        except Exception as e:
            return {
                'clustering_score': 0.0,
                'is_highly_clustered': False,
                'cluster_distribution': {'fast': 0, 'medium': 0, 'slow': 0},
                'confidence': 0.0
            }
    
    # Additional helper methods for performance inconsistency analysis
    def _analyze_response_time_consistency(self, response_times: List[float]) -> Dict[str, Any]:
        """Analyze response time consistency patterns"""
        if len(response_times) < 3:
            return {'consistency_score': 1.0, 'is_suspicious': False}
        
        try:
            # Calculate coefficient of variation
            mean_time = statistics.mean(response_times)
            std_time = statistics.stdev(response_times)
            cv = std_time / max(mean_time, 1e-6)
            
            # Normal variation for legitimate users is typically 0.3-0.8
            # Very low variation (< 0.2) might indicate automated responses
            # Very high variation (> 1.2) might indicate inconsistent assistance
            
            consistency_score = 1 - min(cv, 2.0) / 2.0
            is_suspicious = cv < 0.2 or cv > 1.2
            
            return {
                'consistency_score': float(consistency_score),
                'coefficient_of_variation': float(cv),
                'is_suspicious': is_suspicious,
                'suspicion_reason': 'too_consistent' if cv < 0.2 else 'too_variable' if cv > 1.2 else 'normal'
            }
        except:
            return {'consistency_score': 0.5, 'is_suspicious': False}
    
    def _analyze_accuracy_difficulty_consistency(self, responses: List[Dict]) -> Dict[str, Any]:
        """Analyze consistency between accuracy and question difficulty"""
        if not responses or 'difficulty' not in responses[0]:
            return {'consistency_score': 0.5, 'is_suspicious': False}
        
        try:
            # Group by difficulty level
            difficulty_groups = defaultdict(list)
            for response in responses:
                difficulty = response.get('difficulty', 1)
                is_correct = response.get('is_correct', False)
                difficulty_groups[difficulty].append(is_correct)
            
            # Calculate accuracy for each difficulty level
            difficulty_accuracies = {}
            for difficulty, results in difficulty_groups.items():
                accuracy = sum(results) / len(results)
                difficulty_accuracies[difficulty] = accuracy
            
            # Check if accuracy decreases with difficulty
            sorted_difficulties = sorted(difficulty_accuracies.keys())
            if len(sorted_difficulties) > 1:
                accuracies = [difficulty_accuracies[d] for d in sorted_difficulties]
                
                # Calculate trend (should be negative for legitimate users)
                correlation = np.corrcoef(sorted_difficulties, accuracies)[0, 1] if not np.isnan(np.corrcoef(sorted_difficulties, accuracies)[0, 1]) else 0
                
                # Positive correlation (accuracy increases with difficulty) is suspicious
                is_suspicious = correlation > 0.3
                consistency_score = max(0, 1 - abs(correlation + 0.5))  # Expected correlation is around -0.5
                
                return {
                    'consistency_score': float(consistency_score),
                    'difficulty_accuracy_correlation': float(correlation),
                    'is_suspicious': is_suspicious,
                    'difficulty_accuracies': difficulty_accuracies
                }
            
        except Exception as e:
            self.logger.warning(f"Error in accuracy-difficulty analysis: {str(e)}")
        
        return {'consistency_score': 0.5, 'is_suspicious': False}
    
    def _analyze_learning_curve_anomalies(self, responses: List[Dict], timings: List[Dict]) -> Dict[str, Any]:
        """Analyze learning curve for anomalous patterns"""
        if len(responses) < 10:
            return {'learning_score': 0.5, 'is_suspicious': False}
        
        try:
            # Split responses into quarters to analyze progression
            quarter_size = len(responses) // 4
            quarters = []
            
            for i in range(4):
                start_idx = i * quarter_size
                end_idx = (i + 1) * quarter_size if i < 3 else len(responses)
                quarter_responses = responses[start_idx:end_idx]
                quarter_timings = timings[start_idx:end_idx] if len(timings) >= end_idx else []
                
                # Calculate quarter metrics
                accuracy = sum(1 for r in quarter_responses if r.get('is_correct', False)) / len(quarter_responses)
                avg_time = statistics.mean([t.get('response_time', 0) for t in quarter_timings if 'response_time' in t]) if quarter_timings else 0
                
                quarters.append({
                    'accuracy': accuracy,
                    'avg_response_time': avg_time
                })
            
            # Analyze trends
            accuracies = [q['accuracy'] for q in quarters]
            times = [q['avg_response_time'] for q in quarters]
            
            # Normal learning: accuracy should increase or stabilize, time should decrease or stabilize
            accuracy_trend = (accuracies[-1] - accuracies[0]) / max(accuracies[0], 0.01)
            time_trend = (times[0] - times[-1]) / max(times[0], 1) if times[0] > 0 else 0
            
            # Suspicious patterns: sudden improvement, no learning, performance degradation
            is_suspicious = (accuracy_trend > 0.5) or (accuracy_trend < -0.3) or (abs(time_trend) < 0.1 and accuracy_trend > 0.3)
            
            learning_score = max(0, min(1, 0.5 + accuracy_trend - abs(time_trend - 0.2)))
            
            return {
                'learning_score': float(learning_score),
                'accuracy_trend': float(accuracy_trend),
                'time_trend': float(time_trend),
                'is_suspicious': is_suspicious,
                'quarter_analysis': quarters
            }
            
        except Exception as e:
            self.logger.warning(f"Error in learning curve analysis: {str(e)}")
            return {'learning_score': 0.5, 'is_suspicious': False}
    
    def _analyze_cognitive_load_inconsistencies(self, responses: List[Dict], timings: List[Dict]) -> Dict[str, Any]:
        """Analyze cognitive load patterns for inconsistencies"""
        try:
            response_times = [t.get('response_time', 0) for t in timings if 'response_time' in t]
            
            if len(response_times) < 5:
                return {'cognitive_load_score': 0.5, 'is_suspicious': False}
            
            # Analyze response time patterns relative to question characteristics
            load_indicators = []
            
            for i, (response, timing) in enumerate(zip(responses, timings)):
                difficulty = response.get('difficulty', 1)
                response_time = timing.get('response_time', 0)
                is_correct = response.get('is_correct', False)
                
                # Expected cognitive load based on difficulty
                expected_time = difficulty * 30  # Rough baseline: 30 seconds per difficulty point
                time_ratio = response_time / max(expected_time, 1)
                
                # Cognitive load indicator: combination of time, difficulty, and accuracy
                if is_correct:
                    load_indicator = max(0, 1 - abs(time_ratio - 1))  # Correct answers should take appropriate time
                else:
                    load_indicator = max(0, time_ratio - 0.5)  # Wrong answers with very short time are suspicious
                
                load_indicators.append(load_indicator)
            
            # Calculate consistency of cognitive load
            avg_load = statistics.mean(load_indicators)
            load_variance = statistics.variance(load_indicators) if len(load_indicators) > 1 else 0
            
            # High variance in cognitive load might indicate inconsistent assistance
            consistency_score = max(0, 1 - load_variance)
            is_suspicious = load_variance > 0.3 or avg_load < 0.3
            
            return {
                'cognitive_load_score': float(consistency_score),
                'average_load_indicator': float(avg_load),
                'load_variance': float(load_variance),
                'is_suspicious': is_suspicious,
                'load_indicators': [float(li) for li in load_indicators[:10]]  # First 10 for brevity
            }
            
        except Exception as e:
            self.logger.warning(f"Error in cognitive load analysis: {str(e)}")
            return {'cognitive_load_score': 0.5, 'is_suspicious': False}
    
    def _analyze_answer_change_patterns(self, responses: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in answer changes"""
        try:
            total_changes = 0
            change_patterns = []
            
            for response in responses:
                answer_history = response.get('answer_history', [])
                if len(answer_history) > 1:
                    changes = len(answer_history) - 1
                    total_changes += changes
                    
                    # Analyze change pattern
                    final_correct = response.get('is_correct', False)
                    change_patterns.append({
                        'changes': changes,
                        'final_correct': final_correct,
                        'improved': final_correct  # Simplified: assume first answer was wrong if changed
                    })
            
            if not change_patterns:
                return {'change_score': 1.0, 'is_suspicious': False}
            
            # Calculate metrics
            change_rate = total_changes / len(responses)
            improvement_rate = sum(1 for cp in change_patterns if cp['improved']) / len(change_patterns)
            
            # Suspicious patterns: too many changes, too high improvement rate
            is_suspicious = change_rate > 0.5 or improvement_rate > 0.8
            
            change_score = max(0, 1 - change_rate) * max(0, 1 - abs(improvement_rate - 0.3))
            
            return {
                'change_score': float(change_score),
                'change_rate': float(change_rate),
                'improvement_rate': float(improvement_rate),
                'total_changes': total_changes,
                'is_suspicious': is_suspicious
            }
            
        except Exception as e:
            self.logger.warning(f"Error in answer change analysis: {str(e)}")
            return {'change_score': 1.0, 'is_suspicious': False}
    
    # Composite scoring and recommendation methods
    def _calculate_composite_inconsistency_score(self, inconsistencies: Dict[str, Any]) -> float:
        """Calculate composite inconsistency score from all analyses"""
        try:
            scores = []
            weights = {
                'response_time': 0.25,
                'accuracy_difficulty': 0.20,
                'learning_curve': 0.20,
                'cognitive_load': 0.20,
                'answer_changes': 0.15
            }
            
            for category, weight in weights.items():
                if category in inconsistencies:
                    analysis = inconsistencies[category]
                    
                    # Extract suspicion score
                    if 'consistency_score' in analysis:
                        score = 1 - analysis['consistency_score']  # Convert consistency to inconsistency
                    elif 'learning_score' in analysis:
                        score = 1 - analysis['learning_score']
                    elif 'cognitive_load_score' in analysis:
                        score = 1 - analysis['cognitive_load_score']
                    elif 'change_score' in analysis:
                        score = 1 - analysis['change_score']
                    else:
                        score = 0.5  # Default neutral score
                    
                    # Apply suspicion boost
                    if analysis.get('is_suspicious', False):
                        score = min(1.0, score * 1.5)
                    
                    scores.append(score * weight)
            
            composite_score = sum(scores) * 100  # Convert to 0-100 scale
            return min(100.0, composite_score)
            
        except Exception as e:
            self.logger.warning(f"Error calculating composite inconsistency score: {str(e)}")
            return 50.0  # Default neutral score
    
    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level based on composite score"""
        if score >= 80:
            return 'CRITICAL'
        elif score >= 60:
            return 'HIGH'
        elif score >= 40:
            return 'MEDIUM'
        elif score >= 20:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    def _calculate_overall_anomaly_assessment(self, anomaly_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall anomaly assessment from individual analyses"""
        try:
            total_score = 0
            max_score = 0
            confidence_scores = []
            
            # Weight different analysis types
            weights = {
                'isolation_forest': 0.3,
                'statistical': 0.25,
                'pca_reconstruction': 0.2,
                'response_patterns': 0.25
            }
            
            for analysis_type, weight in weights.items():
                if analysis_type in anomaly_results:
                    analysis = anomaly_results[analysis_type]
                    
                    if analysis_type == 'statistical':
                        score = analysis.get('anomaly_rate', 0) * weight
                        confidence = analysis.get('anomaly_rate', 0)
                    else:
                        confidence = analysis.get('confidence', 0)
                        if analysis.get('anomaly_detected', False):
                            score = confidence * weight
                        else:
                            score = (1 - confidence) * weight * -1  # Negative score for normal behavior
                    
                    total_score += score
                    max_score += weight
                    confidence_scores.append(confidence)
            
            # Normalize score
            normalized_score = (total_score / max_score) if max_score > 0 else 0
            overall_confidence = statistics.mean(confidence_scores) if confidence_scores else 0
            
            return {
                'overall_anomaly_score': float(normalized_score),
                'confidence': float(overall_confidence),
                'risk_level': self._determine_risk_level(normalized_score * 100),
                'anomaly_detected': normalized_score > 0.3
            }
            
        except Exception as e:
            self.logger.warning(f"Error calculating overall anomaly assessment: {str(e)}")
            return {
                'overall_anomaly_score': 0.5,
                'confidence': 0.0,
                'risk_level': 'MEDIUM',
                'anomaly_detected': False
            }
    
    def _save_models(self):
        """Save trained models to disk"""
        try:
            # Save scalers
            for name, scaler in self.scalers.items():
                joblib.dump(scaler, os.path.join(self.model_dir, f"{name}_scaler.pkl"))
            
            # Save anomaly detectors
            for name, detector in self.anomaly_detectors.items():
                joblib.dump(detector, os.path.join(self.model_dir, f"{name}_detector.pkl"))
            
            # Save baseline models
            with open(os.path.join(self.model_dir, "baseline_models.json"), 'w') as f:
                json.dump(self.baseline_models, f, default=str)
                
            self.logger.info("Models saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving models: {str(e)}")
    
    def _convert_to_probability(self, score: float) -> float:
        """Convert various scores to probability scale [0, 1]"""
        return max(0.0, min(1.0, abs(score)))
    
    def _calculate_weighted_probability(self, components: Dict[str, float]) -> float:
        """Calculate weighted composite probability from components"""
        if not components:
            return 0.5
        
        weights = {
            'isolation_forest_prob': 0.25,
            'statistical_prob': 0.25,
            'pca_prob': 0.20,
            'inconsistency_prob': 0.20,
            'behavioral_prob': 0.10
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for component, prob in components.items():
            weight = weights.get(component, 0.1)
            weighted_sum += prob * weight
            total_weight += weight
        
        return weighted_sum / max(total_weight, 1e-6)
    
    def _calculate_confidence_intervals(self, components: Dict[str, float], composite_prob: float) -> Dict[str, float]:
        """Calculate confidence intervals for probability estimates"""
        try:
            # Simple confidence interval based on component variance
            component_values = list(components.values())
            
            if len(component_values) > 1:
                component_std = statistics.stdev(component_values)
                margin_of_error = 1.96 * component_std / np.sqrt(len(component_values))  # 95% CI
            else:
                margin_of_error = 0.1  # Default margin
            
            lower_bound = max(0.0, composite_prob - margin_of_error)
            upper_bound = min(1.0, composite_prob + margin_of_error)
            
            return {
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
                'margin_of_error': float(margin_of_error),
                'confidence_level': 0.95
            }
            
        except:
            return {
                'lower_bound': max(0.0, composite_prob - 0.1),
                'upper_bound': min(1.0, composite_prob + 0.1),
                'margin_of_error': 0.1,
                'confidence_level': 0.95
            }
    
    def _classify_risk_level(self, probability: float) -> Dict[str, Any]:
        """Classify risk level based on anomaly probability"""
        if probability >= 0.8:
            level = 'CRITICAL'
            description = 'Extremely high probability of anomalous behavior'
            recommended_action = 'Immediate intervention required'
        elif probability >= 0.6:
            level = 'HIGH'
            description = 'High probability of anomalous behavior'
            recommended_action = 'Manual review and possible intervention'
        elif probability >= 0.4:
            level = 'MEDIUM'
            description = 'Moderate probability of anomalous behavior'
            recommended_action = 'Enhanced monitoring recommended'
        elif probability >= 0.2:
            level = 'LOW'
            description = 'Low probability of anomalous behavior'
            recommended_action = 'Continue normal monitoring'
        else:
            level = 'MINIMAL'
            description = 'Very low probability of anomalous behavior'
            recommended_action = 'Normal operation'
        
        return {
            'level': level,
            'description': description,
            'recommended_action': recommended_action,
            'numeric_score': float(probability * 100)
        }
    
    def _calculate_behavioral_anomaly_probability(self, session_data: Dict[str, Any]) -> float:
        """Calculate behavioral anomaly probability from session data"""
        try:
            # Simple behavioral scoring based on available data
            responses = session_data.get('responses', [])
            timings = session_data.get('timings', [])
            
            if not responses or not timings:
                return 0.5
            
            # Calculate basic behavioral indicators
            response_times = [t.get('response_time', 0) for t in timings if 'response_time' in t]
            
            if not response_times:
                return 0.5
            
            # Extreme consistency or inconsistency in timing
            cv = statistics.stdev(response_times) / max(statistics.mean(response_times), 1e-6)
            timing_anomaly = 1.0 if cv < 0.1 or cv > 2.0 else max(0, abs(cv - 0.5) / 0.5)
            
            # Accuracy patterns
            accuracy = sum(1 for r in responses if r.get('is_correct', False)) / len(responses)
            accuracy_anomaly = 1.0 if accuracy > 0.95 or accuracy < 0.1 else 0.0
            
            # Combine indicators
            behavioral_prob = (timing_anomaly * 0.6 + accuracy_anomaly * 0.4)
            return min(1.0, behavioral_prob)
            
        except:
            return 0.5
    
    def _generate_probability_breakdown(self, components: Dict[str, float]) -> Dict[str, Any]:
        """Generate detailed probability breakdown"""
        breakdown = {}
        
        for component, probability in components.items():
            if 'isolation_forest' in component:
                breakdown[component] = {
                    'probability': float(probability),
                    'description': 'ML-based outlier detection probability',
                    'interpretation': 'High values indicate deviation from normal patterns'
                }
            elif 'statistical' in component:
                breakdown[component] = {
                    'probability': float(probability),
                    'description': 'Statistical anomaly detection probability',
                    'interpretation': 'Based on Z-score analysis of feature distributions'
                }
            elif 'pca' in component:
                breakdown[component] = {
                    'probability': float(probability),
                    'description': 'PCA reconstruction error probability',
                    'interpretation': 'High reconstruction error indicates unusual feature combinations'
                }
            elif 'inconsistency' in component:
                breakdown[component] = {
                    'probability': float(probability),
                    'description': 'Performance inconsistency probability',
                    'interpretation': 'Based on response patterns and timing analysis'
                }
            elif 'behavioral' in component:
                breakdown[component] = {
                    'probability': float(probability),
                    'description': 'Behavioral pattern anomaly probability',
                    'interpretation': 'Based on interaction and response behavior analysis'
                }
        
        return breakdown
    
    def _calculate_statistical_significance(self, probability: float) -> Dict[str, Any]:
        """Calculate statistical significance of anomaly probability"""
        try:
            # Simple significance testing
            # Null hypothesis: behavior is normal (p = 0.5)
            # Alternative hypothesis: behavior is anomalous (p != 0.5)
            
            z_score = abs(probability - 0.5) / 0.1  # Assuming std error of 0.1
            p_value = 2 * (1 - stats.norm.cdf(z_score))  # Two-tailed test
            
            is_significant = p_value < 0.05
            significance_level = 'significant' if is_significant else 'not_significant'
            
            return {
                'z_score': float(z_score),
                'p_value': float(p_value),
                'is_significant': is_significant,
                'significance_level': significance_level,
                'confidence_level': 0.95
            }
            
        except:
            return {
                'z_score': 0.0,
                'p_value': 1.0,
                'is_significant': False,
                'significance_level': 'not_significant',
                'confidence_level': 0.95
            }
    
    def _generate_anomaly_recommendation(self, overall_assessment: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on anomaly assessment"""
        recommendations = []
        
        risk_level = overall_assessment.get('risk_level', 'MEDIUM')
        anomaly_score = overall_assessment.get('overall_anomaly_score', 0.5)
        
        if risk_level == 'CRITICAL':
            recommendations.extend([
                "Immediate manual review required",
                "Consider terminating session if still active",
                "Flag candidate for comprehensive investigation",
                "Review all historical sessions for this candidate"
            ])
        elif risk_level == 'HIGH':
            recommendations.extend([
                "Schedule manual review within 24 hours",
                "Implement enhanced monitoring for future sessions",
                "Consider additional verification measures",
                "Document findings for pattern analysis"
            ])
        elif risk_level == 'MEDIUM':
            recommendations.extend([
                "Enhanced automated monitoring recommended",
                "Review session data for specific anomaly patterns",
                "Consider baseline adjustment if false positive"
            ])
        else:
            recommendations.extend([
                "Continue standard monitoring",
                "Session appears within normal parameters"
            ])
        
        return recommendations
    
    def _generate_detailed_findings(self, inconsistencies: Dict[str, Any]) -> List[str]:
        """Generate detailed findings from inconsistency analysis"""
        findings = []
        
        for category, analysis in inconsistencies.items():
            if analysis.get('is_suspicious', False):
                if category == 'response_time':
                    reason = analysis.get('suspicion_reason', 'unknown')
                    if reason == 'too_consistent':
                        findings.append("Response times show unusual consistency, possible automation")
                    elif reason == 'too_variable':
                        findings.append("Response times show excessive variability, possible external assistance")
                elif category == 'accuracy_difficulty':
                    findings.append("Accuracy improves with question difficulty, contrary to expected pattern")
                elif category == 'learning_curve':
                    findings.append("Learning progression shows anomalous patterns")
                elif category == 'cognitive_load':
                    findings.append("Cognitive load indicators suggest inconsistent mental effort")
                elif category == 'answer_changes':
                    findings.append("Answer change patterns suggest possible external guidance")
        
        return findings
    
    def _generate_inconsistency_recommendations(self, composite_score: float) -> List[str]:
        """Generate recommendations based on inconsistency score"""
        recommendations = []
        
        if composite_score >= 80:
            recommendations.extend([
                "Critical inconsistencies detected - immediate investigation required",
                "Consider invalidating test results pending review",
                "Implement additional security measures for future assessments"
            ])
        elif composite_score >= 60:
            recommendations.extend([
                "Significant inconsistencies detected - manual review recommended",
                "Enhanced monitoring for future sessions",
                "Consider additional verification questions"
            ])
        elif composite_score >= 40:
            recommendations.extend([
                "Moderate inconsistencies detected - automated flagging for review",
                "Monitor for patterns in future sessions"
            ])
        else:
            recommendations.append("Performance patterns within expected ranges")
        
        return recommendations
    
    def _generate_probability_based_recommendations(self, probability: float, risk_classification: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on probability scores"""
        recommendations = []
        
        level = risk_classification.get('level', 'MEDIUM')
        
        if level == 'CRITICAL':
            recommendations.extend([
                "Immediate intervention required (probability > 80%)",
                "Terminate active session if ongoing",
                "Initiate comprehensive security investigation",
                "Review candidate history and flag account",
                "Consider legal implications and evidence preservation"
            ])
        elif level == 'HIGH':
            recommendations.extend([
                "High-priority manual review required (probability 60-80%)",
                "Implement real-time monitoring if session active",
                "Schedule expert review within 2 hours",
                "Consider additional authentication measures"
            ])
        elif level == 'MEDIUM':
            recommendations.extend([
                "Enhanced monitoring recommended (probability 40-60%)",
                "Automated flagging for routine review",
                "Consider pattern analysis with historical data"
            ])
        elif level == 'LOW':
            recommendations.extend([
                "Low-priority review (probability 20-40%)",
                "Continue standard monitoring protocols"
            ])
        else:
            recommendations.append("Normal operation - no special action required")
        
        return recommendations
    
    def _analyze_feature_contributions(self, features: Dict[str, Any], feature_names: List[str]) -> Dict[str, Any]:
        """Analyze which features contribute most to anomaly detection"""
        contributions = {}
        
        try:
            for feature_name in feature_names:
                if feature_name in features:
                    value = features[feature_name]
                    weight = self.feature_weights.get(feature_name, 0.1)
                    
                    # Calculate normalized contribution
                    if isinstance(value, (int, float)):
                        # Simple normalization based on expected ranges
                        if 'time' in feature_name.lower():
                            normalized_value = min(value / 300, 2.0)  # Normalize by 5 minutes
                        elif 'accuracy' in feature_name.lower():
                            normalized_value = value  # Already 0-1
                        elif 'score' in feature_name.lower():
                            normalized_value = value  # Assume already normalized
                        else:
                            normalized_value = min(abs(value), 2.0)  # Generic normalization
                        
                        contribution = normalized_value * weight
                        contributions[feature_name] = {
                            'value': float(value),
                            'normalized_value': float(normalized_value),
                            'weight': float(weight),
                            'contribution': float(contribution)
                        }
            
            # Sort by contribution
            sorted_contributions = sorted(
                contributions.items(),
                key=lambda x: x[1]['contribution'],
                reverse=True
            )
            
            return {
                'feature_contributions': dict(sorted_contributions[:10]),  # Top 10
                'total_weighted_score': sum(c['contribution'] for c in contributions.values())
            }
            
        except Exception as e:
            self.logger.warning(f"Error analyzing feature contributions: {str(e)}")
            return {'feature_contributions': {}, 'total_weighted_score': 0.0}


# Initialize global instance
anomaly_detection_engine = AnomalyDetectionEngine()