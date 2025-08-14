"""
Advanced Item Calibration Engine
Phase 1.2: ML-Powered Question Difficulty Calibration using Historical Data

This module implements sophisticated IRT calibration using:
- 3PL IRT Maximum Likelihood Estimation (MLE)
- Machine Learning algorithms for pattern analysis
- Historical response data analytics
- Advanced parameter estimation for discrimination (a), difficulty (b), and guessing (c)
"""

import numpy as np
import pandas as pd
from scipy import optimize
from scipy.stats import norm
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional, Any
import logging
import math
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedItemCalibrationEngine:
    """
    Advanced Item Calibration Engine using ML-powered 3PL IRT calibration
    
    Features:
    - Maximum Likelihood Estimation for 3PL IRT parameters
    - Random Forest and Gradient Boosting for pattern analysis
    - Historical response data analysis
    - Advanced parameter estimation and validation
    """
    
    def __init__(self):
        # IRT Model parameters
        self.D = 1.7  # Scaling constant for logistic function
        self.convergence_threshold = 1e-6
        self.max_iterations = 100
        self.min_responses_per_item = 10  # Minimum responses needed for calibration
        
        # ML Models for supporting analysis
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.gb_model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        self.scaler = StandardScaler()
        
        # Parameter bounds for optimization
        self.param_bounds = {
            'discrimination': (0.1, 4.0),  # a parameter
            'difficulty': (-4.0, 4.0),     # b parameter  
            'guessing': (0.0, 0.35)        # c parameter
        }
        
        # Historical data cache
        self.historical_data = None
        self.calibration_results = {}
        
    def load_historical_data(self, sessions_data: List[Dict]) -> pd.DataFrame:
        """
        Load and preprocess historical response data from completed sessions
        
        Args:
            sessions_data: List of completed aptitude test sessions
            
        Returns:
            Processed DataFrame with response patterns
        """
        try:
            response_records = []
            
            for session in sessions_data:
                session_id = session.get('session_id', '')
                candidate_theta = session.get('adaptive_score', 0.0)
                answers = session.get('answers', {})
                timing_data = session.get('timing_data', {})
                
                for question_id, answer_info in answers.items():
                    # Extract response data
                    is_correct = answer_info.get('correct', False)
                    response_time = timing_data.get(question_id, {}).get('time_taken', 60.0)
                    
                    response_records.append({
                        'session_id': session_id,
                        'question_id': question_id,
                        'candidate_theta': candidate_theta,
                        'is_correct': int(is_correct),
                        'response_time': response_time,
                        'log_response_time': math.log(max(1.0, response_time)),
                    })
            
            df = pd.DataFrame(response_records)
            
            if len(df) == 0:
                logger.warning("No historical response data found")
                return df
                
            # Add derived features for ML analysis
            df['theta_squared'] = df['candidate_theta'] ** 2
            df['theta_cubed'] = df['candidate_theta'] ** 3
            df['response_time_normalized'] = df.groupby('question_id')['response_time'].transform(
                lambda x: (x - x.mean()) / (x.std() + 1e-6)
            )
            
            # Calculate question-level statistics
            question_stats = df.groupby('question_id').agg({
                'is_correct': ['mean', 'std', 'count'],
                'candidate_theta': ['mean', 'std'],
                'response_time': ['mean', 'std'],
                'log_response_time': ['mean', 'std']
            }).round(4)
            
            question_stats.columns = [
                'success_rate', 'success_std', 'response_count',
                'theta_mean', 'theta_std', 
                'time_mean', 'time_std',
                'log_time_mean', 'log_time_std'
            ]
            
            # Merge question statistics back to main dataframe
            df = df.merge(question_stats, left_on='question_id', right_index=True, how='left')
            
            self.historical_data = df
            logger.info(f"Loaded {len(df)} response records for {df['question_id'].nunique()} questions")
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading historical data: {e}")
            return pd.DataFrame()
    
    def likelihood_3pl(self, params: np.ndarray, theta: np.ndarray, responses: np.ndarray) -> float:
        """
        Calculate negative log-likelihood for 3PL IRT model
        
        Args:
            params: [discrimination, difficulty, guessing] parameters
            theta: Array of ability estimates
            responses: Array of response outcomes (0/1)
            
        Returns:
            Negative log-likelihood value
        """
        try:
            a, b, c = params
            
            # Bound parameters within reasonable ranges
            a = max(0.1, min(4.0, a))
            c = max(0.0, min(0.35, c))
            
            # Calculate probabilities using 3PL model
            exp_term = np.exp(self.D * a * (theta - b))
            prob_correct = c + (1 - c) * (exp_term / (1 + exp_term))
            
            # Bound probabilities to avoid log(0)
            prob_correct = np.clip(prob_correct, 1e-10, 1 - 1e-10)
            
            # Calculate log-likelihood
            log_likelihood = np.sum(
                responses * np.log(prob_correct) + 
                (1 - responses) * np.log(1 - prob_correct)
            )
            
            return -log_likelihood  # Return negative for minimization
            
        except (OverflowError, ValueError, ZeroDivisionError) as e:
            logger.warning(f"Likelihood calculation error: {e}")
            return 1e10  # Large positive value for bad parameters
    
    def calibrate_item_mle(self, question_id: str, question_data: pd.DataFrame) -> Dict[str, float]:
        """
        Calibrate single item using Maximum Likelihood Estimation
        
        Args:
            question_id: Unique question identifier
            question_data: DataFrame with response data for this question
            
        Returns:
            Dictionary with calibrated parameters and fit statistics
        """
        try:
            if len(question_data) < self.min_responses_per_item:
                logger.warning(f"Insufficient data for question {question_id}: {len(question_data)} responses")
                return self._get_default_parameters()
            
            # Extract arrays for optimization
            theta_values = question_data['candidate_theta'].values
            responses = question_data['is_correct'].values
            
            # Initial parameter estimates using simple methods
            success_rate = np.mean(responses)
            theta_mean = np.mean(theta_values)
            theta_std = np.std(theta_values)
            
            # Starting values for optimization
            initial_params = [
                1.0,  # discrimination (a)
                theta_mean - math.log(success_rate / (1 - success_rate + 1e-6)),  # difficulty (b)
                0.1   # guessing (c)
            ]
            
            # Parameter bounds
            bounds = [
                self.param_bounds['discrimination'],
                self.param_bounds['difficulty'],
                self.param_bounds['guessing']
            ]
            
            # Optimize using L-BFGS-B algorithm
            result = optimize.minimize(
                fun=self.likelihood_3pl,
                x0=initial_params,
                args=(theta_values, responses),
                method='L-BFGS-B',
                bounds=bounds,
                options={'maxiter': self.max_iterations}
            )
            
            if result.success:
                a_est, b_est, c_est = result.x
                
                # Calculate additional fit statistics
                final_likelihood = -result.fun
                aic = 2 * 3 - 2 * final_likelihood  # 3 parameters
                bic = 3 * math.log(len(question_data)) - 2 * final_likelihood
                
                # Calculate pseudo R-squared
                null_likelihood = len(question_data) * (
                    success_rate * math.log(success_rate + 1e-10) + 
                    (1 - success_rate) * math.log(1 - success_rate + 1e-10)
                )
                pseudo_r2 = 1 - (final_likelihood / null_likelihood) if null_likelihood != 0 else 0
                
                return {
                    'discrimination': float(a_est),
                    'difficulty': float(b_est),
                    'guessing': float(c_est),
                    'log_likelihood': float(final_likelihood),
                    'aic': float(aic),
                    'bic': float(bic),
                    'pseudo_r2': float(pseudo_r2),
                    'sample_size': len(question_data),
                    'success_rate': float(success_rate),
                    'convergence': True,
                    'calibration_method': 'MLE_3PL'
                }
            else:
                logger.warning(f"MLE optimization failed for question {question_id}: {result.message}")
                return self._get_fallback_parameters(question_data)
                
        except Exception as e:
            logger.error(f"Error calibrating question {question_id}: {e}")
            return self._get_default_parameters()
    
    def _get_default_parameters(self) -> Dict[str, float]:
        """Return default parameters for items that cannot be calibrated"""
        return {
            'discrimination': 1.0,
            'difficulty': 0.0,
            'guessing': 0.0,
            'log_likelihood': -1000.0,
            'aic': 2000.0,
            'bic': 2000.0,
            'pseudo_r2': 0.0,
            'sample_size': 0,
            'success_rate': 0.5,
            'convergence': False,
            'calibration_method': 'DEFAULT'
        }
    
    def _get_fallback_parameters(self, question_data: pd.DataFrame) -> Dict[str, float]:
        """Calculate fallback parameters using simple methods when MLE fails"""
        try:
            success_rate = np.mean(question_data['is_correct'])
            theta_mean = np.mean(question_data['candidate_theta'])
            theta_std = np.std(question_data['candidate_theta'])
            
            # Simple parameter estimation
            if 0.01 < success_rate < 0.99:
                difficulty_b = theta_mean - math.log(success_rate / (1 - success_rate))
            else:
                difficulty_b = theta_mean
                
            discrimination_a = min(3.0, max(0.5, 1.0 / max(0.1, theta_std)))
            guessing_c = max(0.0, min(0.2, (success_rate - 0.5) * 0.4)) if success_rate > 0.5 else 0.0
            
            return {
                'discrimination': float(discrimination_a),
                'difficulty': float(difficulty_b),
                'guessing': float(guessing_c),
                'log_likelihood': -500.0,
                'aic': 1000.0,
                'bic': 1000.0,
                'pseudo_r2': 0.0,
                'sample_size': len(question_data),
                'success_rate': float(success_rate),
                'convergence': False,
                'calibration_method': 'FALLBACK'
            }
        except:
            return self._get_default_parameters()
    
    def prepare_ml_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features for ML analysis of response patterns
        
        Args:
            df: Historical response dataframe
            
        Returns:
            Tuple of (feature_matrix, target_array)
        """
        try:
            # Select features for ML analysis
            feature_columns = [
                'candidate_theta', 'theta_squared', 'theta_cubed',
                'response_time', 'log_response_time', 'response_time_normalized',
                'theta_mean', 'theta_std', 'time_mean', 'time_std'
            ]
            
            # Filter out rows with missing values
            ml_data = df[feature_columns + ['is_correct']].dropna()
            
            if len(ml_data) == 0:
                logger.warning("No valid data for ML feature preparation")
                return np.array([]), np.array([])
            
            X = ml_data[feature_columns].values
            y = ml_data['is_correct'].values
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            return X_scaled, y
            
        except Exception as e:
            logger.error(f"Error preparing ML features: {e}")
            return np.array([]), np.array([])
    
    def train_ml_models(self, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Train Random Forest and Gradient Boosting models for pattern analysis
        
        Args:
            X: Feature matrix
            y: Target array
            
        Returns:
            Dictionary with model performance metrics
        """
        try:
            if len(X) == 0 or len(y) == 0:
                return {'rf_score': 0.0, 'gb_score': 0.0, 'status': 'no_data'}
            
            # Train Random Forest
            rf_scores = cross_val_score(self.rf_model, X, y, cv=5, scoring='roc_auc')
            self.rf_model.fit(X, y)
            
            # Train Gradient Boosting
            gb_scores = cross_val_score(self.gb_model, X, y, cv=5, scoring='roc_auc')
            self.gb_model.fit(X, y)
            
            return {
                'rf_score': float(np.mean(rf_scores)),
                'rf_std': float(np.std(rf_scores)),
                'gb_score': float(np.mean(gb_scores)),
                'gb_std': float(np.std(gb_scores)),
                'status': 'trained'
            }
            
        except Exception as e:
            logger.error(f"Error training ML models: {e}")
            return {'rf_score': 0.0, 'gb_score': 0.0, 'status': 'error'}
    
    def calibrate_difficulty_parameters(self, sessions_data: List[Dict]) -> Dict[str, Any]:
        """
        Main calibration function using advanced ML algorithms
        
        Args:
            sessions_data: List of completed aptitude test sessions
            
        Returns:
            Comprehensive calibration results
        """
        try:
            logger.info("Starting advanced ML-powered calibration...")
            
            # Load and preprocess historical data
            df = self.load_historical_data(sessions_data)
            
            if len(df) == 0:
                return {
                    'status': 'error',
                    'message': 'No historical data available for calibration',
                    'calibrated_items': {}
                }
            
            # Train ML models for pattern analysis
            X, y = self.prepare_ml_features(df)
            ml_performance = self.train_ml_models(X, y)
            
            # Calibrate individual items using MLE
            calibrated_items = {}
            question_groups = df.groupby('question_id')
            
            logger.info(f"Calibrating {len(question_groups)} questions...")
            
            for question_id, question_data in question_groups:
                calibration_result = self.calibrate_item_mle(question_id, question_data)
                calibrated_items[question_id] = calibration_result
            
            # Calculate summary statistics
            successful_calibrations = sum(1 for result in calibrated_items.values() 
                                        if result['convergence'])
            
            total_responses = len(df)
            unique_candidates = df['session_id'].nunique()
            
            # Overall calibration quality metrics
            avg_pseudo_r2 = np.mean([result['pseudo_r2'] for result in calibrated_items.values()])
            avg_sample_size = np.mean([result['sample_size'] for result in calibrated_items.values()])
            
            self.calibration_results = {
                'status': 'success',
                'timestamp': datetime.utcnow().isoformat(),
                'summary': {
                    'total_questions': len(calibrated_items),
                    'successful_calibrations': successful_calibrations,
                    'success_rate': successful_calibrations / len(calibrated_items),
                    'total_responses': total_responses,
                    'unique_candidates': unique_candidates,
                    'avg_pseudo_r2': float(avg_pseudo_r2),
                    'avg_sample_size': float(avg_sample_size)
                },
                'ml_performance': ml_performance,
                'calibrated_items': calibrated_items
            }
            
            logger.info(f"Calibration completed: {successful_calibrations}/{len(calibrated_items)} questions successful")
            
            return self.calibration_results
            
        except Exception as e:
            logger.error(f"Calibration error: {e}")
            return {
                'status': 'error',
                'message': f'Calibration failed: {str(e)}',
                'calibrated_items': {}
            }
    
    def validate_item_quality(self, question_id: str, calibration_result: Dict[str, float]) -> Dict[str, Any]:
        """
        Validate calibrated item quality using statistical measures
        
        Args:
            question_id: Question identifier
            calibration_result: Calibration results for the item
            
        Returns:
            Quality validation metrics
        """
        try:
            # Extract parameters
            discrimination = calibration_result.get('discrimination', 1.0)
            difficulty = calibration_result.get('difficulty', 0.0)
            guessing = calibration_result.get('guessing', 0.0)
            pseudo_r2 = calibration_result.get('pseudo_r2', 0.0)
            sample_size = calibration_result.get('sample_size', 0)
            
            # Quality flags
            quality_flags = []
            
            # Check discrimination parameter
            if discrimination < 0.5:
                quality_flags.append('low_discrimination')
            elif discrimination > 3.0:
                quality_flags.append('high_discrimination')
            
            # Check difficulty parameter
            if abs(difficulty) > 3.0:
                quality_flags.append('extreme_difficulty')
            
            # Check guessing parameter
            if guessing > 0.3:
                quality_flags.append('high_guessing')
            
            # Check model fit
            if pseudo_r2 < 0.1:
                quality_flags.append('poor_fit')
            
            # Check sample size
            if sample_size < self.min_responses_per_item:
                quality_flags.append('insufficient_data')
            
            # Overall quality score (0-100)
            quality_score = max(0, min(100, 
                70 * pseudo_r2 +  # Model fit (70%)
                20 * min(1.0, sample_size / 50) +  # Sample size adequacy (20%)
                10 * (1 - len(quality_flags) / 6)  # Penalty for quality flags (10%)
            ))
            
            return {
                'question_id': question_id,
                'quality_score': float(quality_score),
                'quality_flags': quality_flags,
                'recommendations': self._generate_quality_recommendations(quality_flags),
                'parameters_within_bounds': len(quality_flags) == 0,
                'fit_adequate': pseudo_r2 >= 0.1,
                'sample_adequate': sample_size >= self.min_responses_per_item
            }
            
        except Exception as e:
            logger.error(f"Error validating item quality for {question_id}: {e}")
            return {
                'question_id': question_id,
                'quality_score': 0.0,
                'quality_flags': ['validation_error'],
                'recommendations': ['Unable to validate item quality'],
                'parameters_within_bounds': False,
                'fit_adequate': False,
                'sample_adequate': False
            }
    
    def _generate_quality_recommendations(self, quality_flags: List[str]) -> List[str]:
        """Generate recommendations based on quality flags"""
        recommendations = []
        
        flag_recommendations = {
            'low_discrimination': 'Consider reviewing question clarity and distinctiveness',
            'high_discrimination': 'Question may be too sensitive to ability differences', 
            'extreme_difficulty': 'Question difficulty may be outside target range',
            'high_guessing': 'Consider reducing guessing opportunities in options',
            'poor_fit': 'Question may not fit well with IRT model assumptions',
            'insufficient_data': 'Collect more response data for reliable calibration'
        }
        
        for flag in quality_flags:
            if flag in flag_recommendations:
                recommendations.append(flag_recommendations[flag])
        
        if not recommendations:
            recommendations.append('Item shows good psychometric properties')
            
        return recommendations
    
    def detect_misfitting_items(self, calibration_results: Dict[str, Any], 
                              threshold: float = 0.1) -> List[Dict[str, Any]]:
        """
        Detect items that don't fit well with the IRT model
        
        Args:
            calibration_results: Results from calibrate_difficulty_parameters
            threshold: Pseudo R-squared threshold for misfitting detection
            
        Returns:
            List of misfitting items with details
        """
        try:
            misfitting_items = []
            calibrated_items = calibration_results.get('calibrated_items', {})
            
            for question_id, result in calibrated_items.items():
                pseudo_r2 = result.get('pseudo_r2', 0.0)
                convergence = result.get('convergence', False)
                
                if pseudo_r2 < threshold or not convergence:
                    quality_validation = self.validate_item_quality(question_id, result)
                    
                    misfitting_items.append({
                        'question_id': question_id,
                        'pseudo_r2': pseudo_r2,
                        'convergence': convergence,
                        'quality_score': quality_validation['quality_score'],
                        'quality_flags': quality_validation['quality_flags'],
                        'recommendations': quality_validation['recommendations'],
                        'priority': 'high' if pseudo_r2 < 0.05 else 'medium'
                    })
            
            # Sort by priority and quality score
            misfitting_items.sort(key=lambda x: (x['priority'] == 'high', -x['quality_score']), 
                                reverse=True)
            
            return misfitting_items
            
        except Exception as e:
            logger.error(f"Error detecting misfitting items: {e}")
            return []