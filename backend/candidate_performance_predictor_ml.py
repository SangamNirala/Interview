"""
Candidate Performance Prediction Models
Phase 1.2 Step 2: ML-Powered Performance Prediction System

This module implements sophisticated ML models for predicting candidate performance:
- Random Forest, Gradient Boosting, and Neural Networks
- Real-time predictions during test progression
- Feature engineering from response patterns, timing data, ability progression
- Prediction targets: final score, completion time, topic performance
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, RandomForestClassifier
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, accuracy_score, f1_score
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, List, Tuple, Optional, Any, Union
import logging
import math
import pickle
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepPerformancePredictor(nn.Module):
    """
    Deep Neural Network for performance prediction
    """
    def __init__(self, input_size: int, hidden_sizes: List[int] = [128, 64, 32], output_size: int = 1):
        super(DeepPerformancePredictor, self).__init__()
        
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.extend([
                nn.Linear(prev_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.BatchNorm1d(hidden_size)
            ])
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, output_size))
        
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.network(x)

class CandidatePerformancePredictorML:
    """
    Advanced ML-powered Candidate Performance Prediction System
    
    Features:
    - Random Forest, Gradient Boosting, and Neural Networks
    - Real-time predictions with incremental learning
    - Comprehensive feature engineering from test data
    - Multiple prediction targets with confidence intervals
    """
    
    def __init__(self):
        # Model configurations
        self.models = {
            'random_forest': {
                'regressor': RandomForestRegressor(
                    n_estimators=150,
                    max_depth=12,
                    min_samples_split=5,
                    min_samples_leaf=2,
                    random_state=42
                ),
                'classifier': RandomForestClassifier(
                    n_estimators=150,
                    max_depth=12,
                    min_samples_split=5,
                    min_samples_leaf=2,
                    random_state=42
                )
            },
            'gradient_boosting': {
                'regressor': GradientBoostingRegressor(
                    n_estimators=150,
                    max_depth=8,
                    learning_rate=0.1,
                    subsample=0.8,
                    random_state=42
                ),
                'classifier': None  # Will use regressor for probability estimation
            },
            'neural_network': {
                'regressor': MLPRegressor(
                    hidden_layer_sizes=(128, 64, 32),
                    activation='relu',
                    solver='adam',
                    alpha=0.001,
                    learning_rate='adaptive',
                    max_iter=500,
                    random_state=42
                ),
                'classifier': MLPClassifier(
                    hidden_layer_sizes=(128, 64, 32),
                    activation='relu',
                    solver='adam',
                    alpha=0.001,
                    learning_rate='adaptive',
                    max_iter=500,
                    random_state=42
                )
            }
        }
        
        # Deep learning models
        self.deep_models = {}
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Feature scalers
        self.scalers = {
            'features': StandardScaler(),
            'targets': StandardScaler()
        }
        
        # Model training status
        self.trained_models = {
            'final_score': False,
            'completion_time': False,
            'topic_performance': False
        }
        
        # Feature importance tracking
        self.feature_importance = {}
        
        # Model performance metrics
        self.model_performance = {}
        
        # Real-time learning buffer
        self.incremental_buffer = []
        self.buffer_max_size = 100
        
        # Topic mappings
        self.topic_encoder = LabelEncoder()
        self.topics = ['numerical_reasoning', 'logical_reasoning', 'verbal_comprehension', 'spatial_reasoning']
        
    def extract_features(self, session_data: Dict[str, Any], current_progress: Optional[Dict] = None) -> np.ndarray:
        """
        Extract comprehensive features from session data and current progress
        
        Args:
            session_data: Complete or partial session data
            current_progress: Current test progress for real-time predictions
            
        Returns:
            Feature vector for ML models
        """
        try:
            features = []
            
            # Basic session information
            answers = session_data.get('answers', {})
            timing_data = session_data.get('timing_data', {})
            candidate_theta = session_data.get('adaptive_score', 0.0)
            
            # Use current progress if available (for real-time predictions)
            if current_progress:
                answers.update(current_progress.get('answers', {}))
                timing_data.update(current_progress.get('timing_data', {}))
                candidate_theta = current_progress.get('current_theta', candidate_theta)
            
            # 1. Response Pattern Features
            total_questions = len(answers)
            correct_answers = sum(1 for ans in answers.values() if ans.get('correct', False))
            current_accuracy = correct_answers / max(1, total_questions)
            
            features.extend([
                total_questions,           # Number of questions answered
                correct_answers,           # Number correct
                current_accuracy,          # Current accuracy rate
                candidate_theta,           # Current ability estimate
                candidate_theta ** 2,      # Theta squared
                candidate_theta ** 3,      # Theta cubed
            ])
            
            # 2. Timing Pattern Features
            response_times = []
            for q_id, timing in timing_data.items():
                if isinstance(timing, dict):
                    time_taken = timing.get('time_taken', 60.0)
                else:
                    time_taken = float(timing) if timing else 60.0
                response_times.append(max(1.0, time_taken))
            
            if response_times:
                avg_response_time = np.mean(response_times)
                std_response_time = np.std(response_times)
                min_response_time = np.min(response_times)
                max_response_time = np.max(response_times)
                median_response_time = np.median(response_times)
                
                features.extend([
                    avg_response_time,
                    std_response_time,
                    min_response_time,
                    max_response_time,
                    median_response_time,
                    math.log(avg_response_time + 1),  # Log average time
                ])
            else:
                features.extend([60.0, 30.0, 30.0, 120.0, 60.0, math.log(61.0)])
            
            # 3. Topic-specific Performance Features
            topic_performance = {}
            for topic in self.topics:
                topic_correct = 0
                topic_total = 0
                topic_times = []
                
                for q_id, answer_data in answers.items():
                    # Simulate topic assignment (in real implementation, get from question data)
                    question_topic = self._get_question_topic(q_id)
                    if question_topic == topic:
                        topic_total += 1
                        if answer_data.get('correct', False):
                            topic_correct += 1
                        
                        if q_id in timing_data:
                            timing = timing_data[q_id]
                            if isinstance(timing, dict):
                                topic_times.append(timing.get('time_taken', 60.0))
                            else:
                                topic_times.append(float(timing) if timing else 60.0)
                
                topic_accuracy = topic_correct / max(1, topic_total)
                topic_avg_time = np.mean(topic_times) if topic_times else 60.0
                
                topic_performance[topic] = {
                    'accuracy': topic_accuracy,
                    'count': topic_total,
                    'avg_time': topic_avg_time
                }
                
                features.extend([topic_accuracy, topic_total, topic_avg_time])
            
            # 4. Sequential Pattern Features
            if len(answers) > 1:
                # Streak analysis
                correct_streak = self._calculate_current_streak(answers, True)
                incorrect_streak = self._calculate_current_streak(answers, False)
                
                # Response consistency
                recent_accuracy = self._calculate_recent_accuracy(answers, window=5)
                accuracy_trend = self._calculate_accuracy_trend(answers, window=10)
                
                features.extend([
                    correct_streak,
                    incorrect_streak,
                    recent_accuracy,
                    accuracy_trend
                ])
            else:
                features.extend([0, 0, 0.5, 0.0])
            
            # 5. Difficulty Progression Features
            if total_questions > 0:
                difficulty_adaptation = self._calculate_difficulty_adaptation(answers)
                features.append(difficulty_adaptation)
            else:
                features.append(0.0)
            
            # 6. Time Management Features
            if response_times:
                time_acceleration = self._calculate_time_acceleration(response_times)
                time_consistency = 1.0 / (1.0 + std_response_time / max(1.0, avg_response_time))
                features.extend([time_acceleration, time_consistency])
            else:
                features.extend([0.0, 0.5])
            
            # 7. Statistical Features
            if total_questions >= 3:
                # Rolling statistics
                rolling_accuracy = self._calculate_rolling_statistics(answers, 'accuracy', window=3)
                rolling_time = self._calculate_rolling_statistics(timing_data, 'time', window=3)
                features.extend([rolling_accuracy, rolling_time])
            else:
                features.extend([current_accuracy, avg_response_time if response_times else 60.0])
            
            return np.array(features, dtype=np.float32)
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            # Return default feature vector
            return np.zeros(40, dtype=np.float32)
    
    def _get_question_topic(self, question_id: str) -> str:
        """
        Determine question topic (simplified for demo - in real implementation, query database)
        """
        # Simple hash-based topic assignment for demo
        hash_val = hash(question_id) % 4
        return self.topics[hash_val]
    
    def _calculate_current_streak(self, answers: Dict, target: bool) -> int:
        """Calculate current streak of correct/incorrect answers"""
        if not answers:
            return 0
        
        streak = 0
        # Get answers in reverse order (most recent first)
        answer_items = list(answers.items())
        answer_items.reverse()
        
        for _, answer_data in answer_items:
            is_correct = answer_data.get('correct', False)
            if is_correct == target:
                streak += 1
            else:
                break
        
        return streak
    
    def _calculate_recent_accuracy(self, answers: Dict, window: int = 5) -> float:
        """Calculate accuracy over recent window"""
        if not answers:
            return 0.5
        
        recent_answers = list(answers.values())[-window:]
        correct_count = sum(1 for ans in recent_answers if ans.get('correct', False))
        return correct_count / len(recent_answers)
    
    def _calculate_accuracy_trend(self, answers: Dict, window: int = 10) -> float:
        """Calculate accuracy trend (positive = improving, negative = declining)"""
        if len(answers) < window:
            return 0.0
        
        answer_values = list(answers.values())
        first_half_correct = sum(1 for ans in answer_values[:window//2] if ans.get('correct', False))
        second_half_correct = sum(1 for ans in answer_values[window//2:window] if ans.get('correct', False))
        
        first_half_accuracy = first_half_correct / (window // 2)
        second_half_accuracy = second_half_correct / (window - window // 2)
        
        return second_half_accuracy - first_half_accuracy
    
    def _calculate_difficulty_adaptation(self, answers: Dict) -> float:
        """Calculate how well candidate adapts to difficulty changes"""
        if len(answers) < 3:
            return 0.0
        
        # Simplified: assume difficulty increases with question sequence
        total_score = 0
        answer_items = list(answers.items())
        
        for i, (_, answer_data) in enumerate(answer_items):
            expected_difficulty = i / len(answer_items)  # Normalized position
            actual_correct = 1 if answer_data.get('correct', False) else 0
            adaptation_score = actual_correct * (1 - expected_difficulty)  # Higher score for correct answers on later questions
            total_score += adaptation_score
        
        return total_score / len(answers)
    
    def _calculate_time_acceleration(self, response_times: List[float]) -> float:
        """Calculate if candidate is speeding up or slowing down"""
        if len(response_times) < 3:
            return 0.0
        
        # Calculate trend in response times
        x = np.arange(len(response_times))
        y = np.array(response_times)
        
        # Linear regression slope
        if len(x) > 1:
            slope = np.corrcoef(x, y)[0, 1] if not np.isnan(np.corrcoef(x, y)[0, 1]) else 0.0
            return -slope  # Negative slope means speeding up (positive acceleration)
        
        return 0.0
    
    def _calculate_rolling_statistics(self, data: Dict, stat_type: str, window: int = 3) -> float:
        """Calculate rolling statistics for given data type"""
        if not data or len(data) < window:
            return 0.5 if stat_type == 'accuracy' else 60.0
        
        values = []
        data_items = list(data.items())[-window:]
        
        for _, item in data_items:
            if stat_type == 'accuracy':
                values.append(1 if item.get('correct', False) else 0)
            elif stat_type == 'time':
                if isinstance(item, dict):
                    values.append(item.get('time_taken', 60.0))
                else:
                    values.append(float(item) if item else 60.0)
        
        return np.mean(values) if values else (0.5 if stat_type == 'accuracy' else 60.0)
    
    def train_models(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train all ML models on historical data
        
        Args:
            training_data: List of completed sessions with outcomes
            
        Returns:
            Training results and performance metrics
        """
        try:
            logger.info("Starting ML model training for performance prediction...")
            
            if len(training_data) < 20:
                return {
                    'status': 'insufficient_data',
                    'message': f'Need at least 20 training samples, got {len(training_data)}'
                }
            
            # Prepare training data
            features_list = []
            final_scores = []
            completion_times = []
            topic_performances = []
            
            for session in training_data:
                # Extract features
                features = self.extract_features(session)
                features_list.append(features)
                
                # Extract targets
                result = session.get('result', {})
                final_scores.append(result.get('overall_score', 50.0))
                completion_times.append(session.get('total_time', 3600.0))
                
                # Topic performance (binary: above average or not)
                topic_performance = []
                for topic in self.topics:
                    topic_score = result.get('topic_scores', {}).get(topic, {}).get('percentage', 50.0)
                    topic_performance.append(1 if topic_score >= 60.0 else 0)
                topic_performances.append(topic_performance)
            
            X = np.array(features_list)
            y_scores = np.array(final_scores)
            y_times = np.array(completion_times)
            y_topics = np.array(topic_performances)
            
            # Scale features
            X_scaled = self.scalers['features'].fit_transform(X)
            
            # Train models for different prediction targets
            results = {}
            
            # 1. Final Score Prediction
            score_results = self._train_regression_models(X_scaled, y_scores, 'final_score')
            results['final_score'] = score_results
            
            # 2. Completion Time Prediction
            time_results = self._train_regression_models(X_scaled, y_times, 'completion_time')
            results['completion_time'] = time_results
            
            # 3. Topic Performance Prediction
            topic_results = {}
            for i, topic in enumerate(self.topics):
                topic_target = y_topics[:, i]
                topic_result = self._train_classification_models(X_scaled, topic_target, f'topic_{topic}')
                topic_results[topic] = topic_result
            results['topic_performance'] = topic_results
            
            # Update training status
            self.trained_models = {
                'final_score': True,
                'completion_time': True,
                'topic_performance': True
            }
            
            # Calculate feature importance
            self._calculate_feature_importance(X_scaled, y_scores)
            
            return {
                'status': 'success',
                'training_samples': len(training_data),
                'feature_dimensions': X.shape[1],
                'model_performance': results,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
            return {
                'status': 'error',
                'message': f'Training failed: {str(e)}'
            }
    
    def _train_regression_models(self, X: np.ndarray, y: np.ndarray, target_name: str) -> Dict[str, Any]:
        """Train regression models for continuous targets"""
        results = {}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        for model_name, model_config in self.models.items():
            try:
                model = model_config['regressor']
                
                # Cross-validation
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
                
                # Fit model
                model.fit(X_train, y_train)
                
                # Test predictions
                y_pred = model.predict(X_test)
                
                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = model.score(X_test, y_test)
                
                results[model_name] = {
                    'cv_mse': -np.mean(cv_scores),
                    'cv_std': np.std(cv_scores),
                    'test_mse': mse,
                    'test_mae': mae,
                    'r2_score': r2,
                    'predictions_range': [float(np.min(y_pred)), float(np.max(y_pred))]
                }
                
                logger.info(f"{model_name} {target_name}: R² = {r2:.4f}, MAE = {mae:.2f}")
                
            except Exception as e:
                logger.error(f"Error training {model_name} for {target_name}: {e}")
                results[model_name] = {'error': str(e)}
        
        return results
    
    def _train_classification_models(self, X: np.ndarray, y: np.ndarray, target_name: str) -> Dict[str, Any]:
        """Train classification models for binary targets"""
        results = {}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        for model_name, model_config in self.models.items():
            try:
                if model_name == 'gradient_boosting':
                    # Use regressor for probability estimation
                    model = model_config['regressor']
                    
                    # Cross-validation
                    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
                    
                    # Fit model
                    model.fit(X_train, y_train)
                    
                    # Test predictions
                    y_pred_prob = model.predict(X_test)
                    y_pred = (y_pred_prob > 0.5).astype(int)
                    
                else:
                    model = model_config['classifier']
                    
                    # Cross-validation
                    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
                    
                    # Fit model
                    model.fit(X_train, y_train)
                    
                    # Test predictions
                    y_pred = model.predict(X_test)
                    y_pred_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred
                
                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                f1 = f1_score(y_test, y_pred, average='weighted')
                
                results[model_name] = {
                    'cv_score': np.mean(cv_scores),
                    'cv_std': np.std(cv_scores),
                    'test_accuracy': accuracy,
                    'test_f1': f1,
                    'prediction_distribution': {
                        'positive_rate': float(np.mean(y_pred)),
                        'avg_probability': float(np.mean(y_pred_prob))
                    }
                }
                
                logger.info(f"{model_name} {target_name}: Accuracy = {accuracy:.4f}, F1 = {f1:.4f}")
                
            except Exception as e:
                logger.error(f"Error training {model_name} for {target_name}: {e}")
                results[model_name] = {'error': str(e)}
        
        return results
    
    def _calculate_feature_importance(self, X: np.ndarray, y: np.ndarray):
        """Calculate and store feature importance"""
        try:
            rf_model = self.models['random_forest']['regressor']
            if hasattr(rf_model, 'feature_importances_'):
                importances = rf_model.feature_importances_
                
                feature_names = [
                    'total_questions', 'correct_answers', 'current_accuracy', 'candidate_theta',
                    'theta_squared', 'theta_cubed', 'avg_response_time', 'std_response_time',
                    'min_response_time', 'max_response_time', 'median_response_time', 'log_avg_time'
                ]
                
                # Add topic-specific features
                for topic in self.topics:
                    feature_names.extend([f'{topic}_accuracy', f'{topic}_count', f'{topic}_avg_time'])
                
                # Add remaining features
                feature_names.extend([
                    'correct_streak', 'incorrect_streak', 'recent_accuracy', 'accuracy_trend',
                    'difficulty_adaptation', 'time_acceleration', 'time_consistency',
                    'rolling_accuracy', 'rolling_time'
                ])
                
                # Create feature importance dictionary
                self.feature_importance = dict(zip(
                    feature_names[:len(importances)], 
                    importances.tolist()
                ))
                
        except Exception as e:
            logger.error(f"Error calculating feature importance: {e}")
    
    def predict_final_score(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict final test score based on current progress
        
        Args:
            session_data: Current session data
            
        Returns:
            Score prediction with confidence intervals
        """
        try:
            if not self.trained_models['final_score']:
                return {
                    'error': 'Final score prediction model not trained',
                    'predicted_score': 50.0,
                    'confidence': 0.0
                }
            
            # Extract features
            features = self.extract_features(session_data)
            features_scaled = self.scalers['features'].transform([features])
            
            # Get predictions from all models
            predictions = {}
            for model_name, model_config in self.models.items():
                try:
                    model = model_config['regressor']
                    pred = model.predict(features_scaled)[0]
                    predictions[model_name] = float(pred)
                except Exception as e:
                    logger.warning(f"Error with {model_name} prediction: {e}")
                    predictions[model_name] = 50.0
            
            # Ensemble prediction (weighted average)
            weights = {'random_forest': 0.4, 'gradient_boosting': 0.4, 'neural_network': 0.2}
            ensemble_score = sum(weights.get(model, 0.33) * score for model, score in predictions.items())
            
            # Calculate confidence based on model agreement
            prediction_values = list(predictions.values())
            std_dev = np.std(prediction_values)
            confidence = max(0.0, min(1.0, 1.0 - (std_dev / 25.0)))  # Normalize by expected score range
            
            # Bound prediction to reasonable range
            ensemble_score = max(0.0, min(100.0, ensemble_score))
            
            return {
                'predicted_score': float(ensemble_score),
                'confidence': float(confidence),
                'model_predictions': predictions,
                'prediction_range': [
                    max(0.0, ensemble_score - std_dev),
                    min(100.0, ensemble_score + std_dev)
                ],
                'features_used': len(features),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error predicting final score: {e}")
            return {
                'error': f'Prediction failed: {str(e)}',
                'predicted_score': 50.0,
                'confidence': 0.0
            }
    
    def predict_completion_time(self, current_progress: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict time to completion based on current progress
        
        Args:
            current_progress: Current test progress data
            
        Returns:
            Time prediction with confidence intervals
        """
        try:
            if not self.trained_models['completion_time']:
                return {
                    'error': 'Completion time prediction model not trained',
                    'predicted_minutes': 45.0,
                    'confidence': 0.0
                }
            
            # Extract features
            features = self.extract_features(current_progress, current_progress)
            features_scaled = self.scalers['features'].transform([features])
            
            # Get predictions from all models
            predictions = {}
            for model_name, model_config in self.models.items():
                try:
                    model = model_config['regressor']
                    pred = model.predict(features_scaled)[0]
                    predictions[model_name] = float(pred)
                except Exception as e:
                    logger.warning(f"Error with {model_name} time prediction: {e}")
                    predictions[model_name] = 2700.0  # 45 minutes default
            
            # Ensemble prediction
            weights = {'random_forest': 0.4, 'gradient_boosting': 0.4, 'neural_network': 0.2}
            ensemble_time = sum(weights.get(model, 0.33) * time_val for model, time_val in predictions.items())
            
            # Calculate remaining time based on current progress
            elapsed_time = current_progress.get('elapsed_time', 0.0)
            remaining_time = max(0.0, ensemble_time - elapsed_time)
            
            # Calculate confidence
            prediction_values = list(predictions.values())
            std_dev = np.std(prediction_values)
            confidence = max(0.0, min(1.0, 1.0 - (std_dev / 1800.0)))  # Normalize by 30 minutes
            
            return {
                'predicted_total_minutes': float(ensemble_time / 60.0),
                'predicted_remaining_minutes': float(remaining_time / 60.0),
                'confidence': float(confidence),
                'model_predictions': {k: v/60.0 for k, v in predictions.items()},
                'current_progress': {
                    'elapsed_minutes': float(elapsed_time / 60.0),
                    'questions_completed': len(current_progress.get('answers', {}))
                },
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error predicting completion time: {e}")
            return {
                'error': f'Time prediction failed: {str(e)}',
                'predicted_minutes': 45.0,
                'confidence': 0.0
            }
    
    def predict_topic_performance(self, response_history: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict likelihood of success in specific skill areas
        
        Args:
            response_history: Historical response data
            
        Returns:
            Topic-wise performance predictions
        """
        try:
            if not self.trained_models['topic_performance']:
                return {
                    'error': 'Topic performance prediction models not trained',
                    'topic_predictions': {}
                }
            
            # Extract features
            features = self.extract_features(response_history)
            features_scaled = self.scalers['features'].transform([features])
            
            topic_predictions = {}
            
            for topic in self.topics:
                try:
                    # Get predictions from all models for this topic
                    model_preds = {}
                    
                    for model_name, model_config in self.models.items():
                        if model_name == 'gradient_boosting':
                            # Use regressor for probability
                            model = model_config['regressor']
                            prob = model.predict(features_scaled)[0]
                            prob = max(0.0, min(1.0, prob))
                        else:
                            model = model_config['classifier']
                            if hasattr(model, 'predict_proba'):
                                prob = model.predict_proba(features_scaled)[0][1]
                            else:
                                pred = model.predict(features_scaled)[0]
                                prob = float(pred)
                        
                        model_preds[model_name] = float(prob)
                    
                    # Ensemble probability
                    weights = {'random_forest': 0.4, 'gradient_boosting': 0.4, 'neural_network': 0.2}
                    ensemble_prob = sum(weights.get(model, 0.33) * prob for model, prob in model_preds.items())
                    
                    # Calculate confidence
                    prob_values = list(model_preds.values())
                    std_dev = np.std(prob_values)
                    confidence = max(0.0, min(1.0, 1.0 - (std_dev * 2)))
                    
                    topic_predictions[topic] = {
                        'success_probability': float(ensemble_prob),
                        'confidence': float(confidence),
                        'model_predictions': model_preds,
                        'recommendation': 'strong' if ensemble_prob > 0.7 else 'moderate' if ensemble_prob > 0.4 else 'needs_improvement'
                    }
                    
                except Exception as e:
                    logger.warning(f"Error predicting {topic}: {e}")
                    topic_predictions[topic] = {
                        'success_probability': 0.5,
                        'confidence': 0.0,
                        'error': str(e)
                    }
            
            return {
                'topic_predictions': topic_predictions,
                'overall_strength': max(topic_predictions.values(), key=lambda x: x.get('success_probability', 0))['success_probability'] if topic_predictions else 0.5,
                'features_analyzed': len(features),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error predicting topic performance: {e}")
            return {
                'error': f'Topic prediction failed: {str(e)}',
                'topic_predictions': {}
            }
    
    def get_prediction_confidence(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get confidence metrics for all prediction types
        
        Args:
            session_data: Current session data
            
        Returns:
            Comprehensive confidence analysis
        """
        try:
            # Get individual prediction confidences
            score_pred = self.predict_final_score(session_data)
            time_pred = self.predict_completion_time(session_data)
            topic_pred = self.predict_topic_performance(session_data)
            
            # Extract confidence values
            confidences = {
                'final_score': score_pred.get('confidence', 0.0),
                'completion_time': time_pred.get('confidence', 0.0),
                'topic_performance': np.mean([
                    topic_data.get('confidence', 0.0) 
                    for topic_data in topic_pred.get('topic_predictions', {}).values()
                ]) if topic_pred.get('topic_predictions') else 0.0
            }
            
            # Overall confidence
            overall_confidence = np.mean(list(confidences.values()))
            
            # Data quality assessment
            answers = session_data.get('answers', {})
            timing_data = session_data.get('timing_data', {})
            
            data_quality = {
                'questions_answered': len(answers),
                'timing_data_available': len(timing_data),
                'data_completeness': min(1.0, len(timing_data) / max(1, len(answers))),
                'session_maturity': min(1.0, len(answers) / 20.0)  # Mature after 20 questions
            }
            
            # Confidence factors
            confidence_factors = {
                'model_training_status': all(self.trained_models.values()),
                'data_sufficiency': len(answers) >= 5,
                'timing_availability': len(timing_data) >= 3,
                'feature_completeness': data_quality['data_completeness'] > 0.7
            }
            
            return {
                'individual_confidences': confidences,
                'overall_confidence': float(overall_confidence),
                'confidence_level': 'high' if overall_confidence > 0.7 else 'medium' if overall_confidence > 0.4 else 'low',
                'data_quality': data_quality,
                'confidence_factors': confidence_factors,
                'recommendation': self._generate_confidence_recommendation(overall_confidence, data_quality),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating prediction confidence: {e}")
            return {
                'error': f'Confidence calculation failed: {str(e)}',
                'overall_confidence': 0.0
            }
    
    def _generate_confidence_recommendation(self, confidence: float, data_quality: Dict) -> str:
        """Generate recommendation based on confidence analysis"""
        if confidence > 0.8 and data_quality['data_completeness'] > 0.8:
            return "High confidence predictions - reliable for decision making"
        elif confidence > 0.6 and data_quality['questions_answered'] >= 10:
            return "Moderate confidence predictions - suitable for guidance with caution"
        elif data_quality['questions_answered'] < 5:
            return "Limited data available - predictions may be unreliable until more responses collected"
        else:
            return "Low confidence predictions - collect more data for reliable forecasting"
    
    def update_model_realtime(self, new_session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update models with new data using incremental learning
        
        Args:
            new_session_data: New completed session data
            
        Returns:
            Update status and performance metrics
        """
        try:
            # Add to incremental buffer
            self.incremental_buffer.append(new_session_data)
            
            # Trim buffer if too large
            if len(self.incremental_buffer) > self.buffer_max_size:
                self.incremental_buffer = self.incremental_buffer[-self.buffer_max_size:]
            
            # Trigger retraining if enough new data
            if len(self.incremental_buffer) >= 20:
                logger.info("Triggering incremental model update...")
                
                # Extract features and targets from buffer
                features_list = []
                targets = {'scores': [], 'times': [], 'topics': []}
                
                for session in self.incremental_buffer:
                    features = self.extract_features(session)
                    features_list.append(features)
                    
                    result = session.get('result', {})
                    targets['scores'].append(result.get('overall_score', 50.0))
                    targets['times'].append(session.get('total_time', 3600.0))
                    
                    topic_performance = []
                    for topic in self.topics:
                        topic_score = result.get('topic_scores', {}).get(topic, {}).get('percentage', 50.0)
                        topic_performance.append(1 if topic_score >= 60.0 else 0)
                    targets['topics'].append(topic_performance)
                
                X_new = np.array(features_list)
                X_new_scaled = self.scalers['features'].transform(X_new)
                
                # Update models using partial_fit where available
                update_results = {}
                
                for model_name, model_config in self.models.items():
                    try:
                        # For models that support incremental learning
                        if hasattr(model_config['regressor'], 'partial_fit'):
                            model_config['regressor'].partial_fit(X_new_scaled, targets['scores'])
                            update_results[model_name] = 'incremental_update'
                        else:
                            # For models that don't support partial_fit, retrain periodically
                            update_results[model_name] = 'scheduled_retrain'
                    except Exception as e:
                        logger.warning(f"Error updating {model_name}: {e}")
                        update_results[model_name] = f'error: {str(e)}'
                
                return {
                    'status': 'updated',
                    'buffer_size': len(self.incremental_buffer),
                    'new_samples_processed': len(features_list),
                    'model_updates': update_results,
                    'next_full_retrain': 'after_100_samples',
                    'timestamp': datetime.utcnow().isoformat()
                }
            
            else:
                return {
                    'status': 'buffered',
                    'buffer_size': len(self.incremental_buffer),
                    'samples_until_update': 20 - len(self.incremental_buffer),
                    'timestamp': datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error in real-time model update: {e}")
            return {
                'status': 'error',
                'message': f'Real-time update failed: {str(e)}'
            }