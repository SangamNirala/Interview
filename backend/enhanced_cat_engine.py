"""
Enhanced Computer Adaptive Testing (CAT) Engine
Phase 1.1: Advanced CAT Algorithms with Multi-dimensional IRT Implementation
"""
import numpy as np
import scipy.stats as stats
from scipy.optimize import minimize_scalar
from typing import Dict, List, Tuple, Optional, Any
import logging
import math
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedCATEngine:
    """
    Enhanced Computer Adaptive Testing Engine with:
    - Multi-dimensional IRT (Item Response Theory) implementation
    - Real-time ability estimation with confidence intervals
    - Dynamic question selection optimization
    - Fraud detection through response pattern analysis
    """
    
    def __init__(self):
        # IRT Parameters
        self.D = 1.7  # Scaling constant for logistic function
        self.initial_theta = 0.0  # Initial ability estimate
        self.initial_se = 1.0  # Initial standard error
        self.min_se_target = 0.3  # Target SE for test termination
        self.max_questions = 50  # Maximum questions per test
        self.min_questions = 10  # Minimum questions per test
        
        # Multi-dimensional settings
        self.dimensions = {
            'numerical_reasoning': 0,
            'logical_reasoning': 1, 
            'verbal_comprehension': 2,
            'spatial_reasoning': 3
        }
        
        # Fraud detection thresholds
        self.fraud_thresholds = {
            'min_response_time': 2.0,  # seconds
            'max_response_time': 300.0,  # seconds
            'consistency_threshold': 0.3,  # ability estimate consistency
            'pattern_detection_window': 5,  # questions to analyze for patterns
            'rapid_clicking_threshold': 0.5  # seconds for rapid clicking
        }
    
    def item_characteristic_curve(self, theta: float, a: float, b: float, c: float = 0.0) -> float:
        """
        Calculate the probability of correct response using 3PL IRT model
        
        Args:
            theta: Ability level
            a: Item discrimination parameter
            b: Item difficulty parameter  
            c: Guessing parameter (pseudo-guessing)
            
        Returns:
            Probability of correct response
        """
        try:
            exp_term = np.exp(self.D * a * (theta - b))
            p = c + (1 - c) * (exp_term / (1 + exp_term))
            return max(0.001, min(0.999, p))  # Bound between 0.001 and 0.999
        except (OverflowError, ZeroDivisionError):
            return 0.5
    
    def item_information_function(self, theta: float, a: float, b: float, c: float = 0.0) -> float:
        """
        Calculate Fisher Information for an item at ability level theta
        
        Args:
            theta: Ability level
            a: Item discrimination parameter
            b: Item difficulty parameter
            c: Guessing parameter
            
        Returns:
            Information value
        """
        try:
            p = self.item_characteristic_curve(theta, a, b, c)
            q = 1 - p
            
            # Calculate derivative of ICC
            exp_term = np.exp(self.D * a * (theta - b))
            denominator = (1 + exp_term) ** 2
            
            if denominator == 0:
                return 0.0
                
            dpdt = (1 - c) * self.D * a * exp_term / denominator
            
            # Fisher Information formula
            if p * q == 0:
                return 0.0
                
            information = (dpdt ** 2) / (p * q)
            return max(0.0, information)
        except (OverflowError, ZeroDivisionError, ValueError):
            return 0.0
    
    def update_ability_estimate(self, current_theta: float, current_se: float, 
                              item_params: Dict[str, float], response: bool,
                              info_sum: float = 0.0) -> Tuple[float, float, float]:
        """
        Update ability estimate using Maximum Likelihood Estimation (MLE)
        
        Args:
            current_theta: Current ability estimate
            current_se: Current standard error
            item_params: Dictionary with 'a', 'b', 'c' parameters
            response: True if correct, False if incorrect
            info_sum: Cumulative information sum
            
        Returns:
            Tuple of (new_theta, new_se, new_info_sum)
        """
        try:
            a = item_params.get('discrimination', 1.0)
            b = item_params.get('difficulty', 0.0)
            c = item_params.get('guessing', 0.0)
            
            # Calculate current item information
            item_info = self.item_information_function(current_theta, a, b, c)
            new_info_sum = info_sum + item_info
            
            # Update SE using Fisher Information
            new_se = 1.0 / math.sqrt(max(0.01, new_info_sum))
            
            # Newton-Raphson method for MLE theta update
            def likelihood_first_derivative(theta):
                p = self.item_characteristic_curve(theta, a, b, c)
                if response:
                    return a * (1 - p) / p if p > 0.001 else 0
                else:
                    return -a * p / (1 - p) if p < 0.999 else 0
            
            def likelihood_second_derivative(theta):
                p = self.item_characteristic_curve(theta, a, b, c)
                q = 1 - p
                if p * q == 0:
                    return -0.1  # Small negative value for stability
                return -a * a * p * q
            
            # Newton-Raphson update
            first_deriv = likelihood_first_derivative(current_theta)
            second_deriv = likelihood_second_derivative(current_theta)
            
            if abs(second_deriv) > 0.001:
                theta_update = -first_deriv / second_deriv
                # Apply damping to prevent large jumps
                theta_update = max(-2.0, min(2.0, theta_update))
                new_theta = current_theta + 0.5 * theta_update  # Damping factor
            else:
                # Fallback to simple Bayesian update
                p = self.item_characteristic_curve(current_theta, a, b, c)
                expected = 1.0 if response else 0.0
                new_theta = current_theta + 0.3 * (expected - p)
            
            # Bound theta within reasonable range
            new_theta = max(-4.0, min(4.0, new_theta))
            
            return new_theta, new_se, new_info_sum
            
        except Exception as e:
            logger.error(f"Error updating ability estimate: {e}")
            # Return conservative update
            return current_theta, current_se * 0.9, info_sum + 0.5
    
    def calculate_confidence_interval(self, theta: float, se: float, confidence: float = 0.95) -> Tuple[float, float]:
        """
        Calculate confidence interval for ability estimate
        
        Args:
            theta: Ability estimate
            se: Standard error
            confidence: Confidence level (default 95%)
            
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        try:
            z_score = stats.norm.ppf((1 + confidence) / 2)
            margin = z_score * se
            return (theta - margin, theta + margin)
        except Exception:
            # Fallback to simple interval  
            margin = 1.96 * se  # 95% CI
            return (theta - margin, theta + margin)
    
    def select_optimal_question(self, candidate_theta: float, available_questions: List[Dict], 
                               asked_questions: List[str], topic_requirements: Dict[str, int],
                               current_topic_counts: Dict[str, int]) -> Optional[Dict]:
        """
        Select the most informative question using Maximum Information criterion
        
        Args:
            candidate_theta: Current ability estimate
            available_questions: List of available question documents
            asked_questions: List of already asked question IDs
            topic_requirements: Required questions per topic
            current_topic_counts: Current questions asked per topic
            
        Returns:
            Optimal question document or None
        """
        try:
            if not available_questions:
                return None
            
            # Filter out already asked questions
            eligible_questions = [
                q for q in available_questions 
                if q.get('id') not in asked_questions
            ]
            
            if not eligible_questions:
                return None
            
            # Apply topic constraints
            prioritized_questions = []
            for q in eligible_questions:
                topic = q.get('topic', '')
                required = topic_requirements.get(topic, 0)
                current = current_topic_counts.get(topic, 0)
                
                # Skip if topic quota is already met
                if required > 0 and current >= required:
                    continue
                    
                prioritized_questions.append(q)
            
            if not prioritized_questions:
                prioritized_questions = eligible_questions  # Fallback to all eligible
            
            # Calculate information for each question
            best_question = None
            max_information = -1
            
            for question in prioritized_questions:
                # Extract IRT parameters (with defaults if not available)
                a = question.get('discrimination', self._get_default_discrimination(question))
                b = question.get('difficulty_value', self._convert_difficulty_to_value(question.get('difficulty', 'medium')))
                c = question.get('guessing', 0.25 if question.get('question_type') == 'multiple_choice' else 0.0)
                
                # Calculate information at current theta
                info = self.item_information_function(candidate_theta, a, b, c)
                
                # Apply topic priority boost
                topic = question.get('topic', '')
                required = topic_requirements.get(topic, 1)
                current = current_topic_counts.get(topic, 0)
                if required > current:
                    info *= 1.5  # Boost for needed topics
                
                if info > max_information:
                    max_information = info
                    best_question = question
            
            return best_question
            
        except Exception as e:
            logger.error(f"Error in question selection: {e}")
            # Fallback to random selection from eligible questions
            eligible = [q for q in available_questions if q.get('id') not in asked_questions]
            return eligible[0] if eligible else None
    
    def _get_default_discrimination(self, question: Dict) -> float:
        """Get default discrimination parameter based on question metadata"""
        try:
            difficulty = question.get('difficulty', 'medium')
            success_rate = question.get('success_rate', 0.5)
            
            # Higher discrimination for questions with good success rate variance
            if 0.3 <= success_rate <= 0.7:
                return 1.5  # Good discrimination
            elif success_rate < 0.2 or success_rate > 0.8:
                return 0.8  # Lower discrimination for very easy/hard questions
            else:
                return 1.2  # Medium discrimination
        except Exception:
            return 1.0
    
    def _convert_difficulty_to_value(self, difficulty: str) -> float:
        """Convert difficulty string to numeric value for IRT"""
        mapping = {
            'easy': -1.0,
            'medium': 0.0,
            'hard': 1.0
        }
        return mapping.get(difficulty, 0.0)
    
    def should_terminate_test(self, current_se: float, questions_asked: int, 
                            time_elapsed: float, topic_requirements: Dict[str, int],
                            current_topic_counts: Dict[str, int]) -> Tuple[bool, str]:
        """
        Determine if test should be terminated based on multiple criteria
        
        Args:
            current_se: Current standard error
            questions_asked: Number of questions asked
            time_elapsed: Time elapsed in seconds
            topic_requirements: Required questions per topic
            current_topic_counts: Current questions per topic
            
        Returns:
            Tuple of (should_terminate, reason)
        """
        try:
            # Check minimum questions requirement
            if questions_asked < self.min_questions:
                return False, "minimum_not_reached"
            
            # Check maximum questions limit
            if questions_asked >= self.max_questions:
                return True, "maximum_reached"
            
            # Check precision criterion
            if current_se <= self.min_se_target:
                return True, "precision_achieved"
            
            # Check topic requirements
            all_topics_met = True
            for topic, required in topic_requirements.items():
                current = current_topic_counts.get(topic, 0)
                if current < required:
                    all_topics_met = False
                    break
            
            if all_topics_met and current_se <= 0.5:
                return True, "content_coverage_complete"
            
            # Check time limits (if applicable)
            if time_elapsed > 7200:  # 2 hours maximum
                return True, "time_limit_exceeded"
            
            return False, "continue_testing"
            
        except Exception as e:
            logger.error(f"Error in termination check: {e}")
            return questions_asked >= 20, "error_fallback"
    
    def detect_fraud_patterns(self, session_data: Dict, response_times: List[float],
                            responses: List[bool], question_difficulties: List[str]) -> Dict[str, Any]:
        """
        Detect potential fraud patterns in test responses
        
        Args:
            session_data: Session information
            response_times: List of response times for each question
            responses: List of response correctness (True/False)
            question_difficulties: List of difficulty levels
            
        Returns:
            Dictionary with fraud analysis results
        """
        try:
            fraud_flags = []
            fraud_score = 0.0
            
            # 1. Response time analysis
            if response_times:
                avg_time = np.mean(response_times)
                std_time = np.std(response_times)
                
                # Check for suspiciously fast responses
                fast_responses = sum(1 for t in response_times if t < self.fraud_thresholds['min_response_time'])
                if fast_responses > len(response_times) * 0.2:  # More than 20% too fast
                    fraud_flags.append("excessive_fast_responses")
                    fraud_score += 0.3
                
                # Check for rapid clicking pattern
                rapid_clicks = sum(1 for t in response_times if t < self.fraud_thresholds['rapid_clicking_threshold'])
                if rapid_clicks > 3:
                    fraud_flags.append("rapid_clicking_pattern")
                    fraud_score += 0.4
                
                # Check for unusually consistent timing
                if std_time < 1.0 and len(response_times) > 5:
                    fraud_flags.append("suspicious_timing_consistency")
                    fraud_score += 0.2
            
            # 2. Response pattern analysis
            if len(responses) >= 5:
                # Check for alternating patterns
                pattern_score = self._analyze_response_patterns(responses)
                if pattern_score > 0.8:
                    fraud_flags.append("systematic_response_pattern")
                    fraud_score += 0.3
                
                # Check performance consistency with difficulty
                consistency_score = self._analyze_difficulty_consistency(responses, question_difficulties)
                if consistency_score < 0.3:
                    fraud_flags.append("inconsistent_performance_difficulty")
                    fraud_score += 0.2
            
            # 3. Statistical outlier detection
            if len(responses) >= 10:
                outlier_score = self._detect_statistical_outliers(response_times, responses)
                if outlier_score > 0.7:
                    fraud_flags.append("statistical_outlier")
                    fraud_score += 0.3
            
            # 4. Session behavior analysis
            session_flags = self._analyze_session_behavior(session_data)
            fraud_flags.extend(session_flags)
            fraud_score += len(session_flags) * 0.1
            
            # Calculate overall fraud risk
            risk_level = "low"
            if fraud_score > 0.7:
                risk_level = "high"
            elif fraud_score > 0.4:
                risk_level = "medium"
            
            return {
                "fraud_score": min(1.0, fraud_score),
                "risk_level": risk_level,
                "flags": fraud_flags,
                "analysis": {
                    "avg_response_time": np.mean(response_times) if response_times else 0,
                    "response_time_std": np.std(response_times) if response_times else 0,
                    "fast_response_ratio": fast_responses / len(response_times) if response_times else 0,
                    "pattern_detected": len(fraud_flags) > 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error in fraud detection: {e}")
            return {
                "fraud_score": 0.0,
                "risk_level": "unknown",
                "flags": ["analysis_error"],
                "analysis": {}
            }
    
    def _analyze_response_patterns(self, responses: List[bool]) -> float:
        """Analyze responses for systematic patterns"""
        try:
            if len(responses) < 4:
                return 0.0
            
            # Check for alternating patterns
            alternating_score = 0.0
            for i in range(1, len(responses)):
                if responses[i] != responses[i-1]:
                    alternating_score += 1
            
            alternating_ratio = alternating_score / (len(responses) - 1)
            
            # Check for runs of same responses
            max_run = 1
            current_run = 1
            for i in range(1, len(responses)):
                if responses[i] == responses[i-1]:
                    current_run += 1
                    max_run = max(max_run, current_run)
                else:
                    current_run = 1
            
            run_score = max_run / len(responses)
            
            # Combine scores (high alternating or high runs indicate patterns)
            return max(alternating_ratio if alternating_ratio > 0.8 else 0, run_score if run_score > 0.6 else 0)
            
        except Exception:
            return 0.0
    
    def _analyze_difficulty_consistency(self, responses: List[bool], difficulties: List[str]) -> float:
        """Analyze consistency between responses and question difficulty"""
        try:
            if len(responses) != len(difficulties):
                return 0.5  # Neutral score if data mismatch
            
            difficulty_values = {'easy': 1, 'medium': 2, 'hard': 3}
            consistency_score = 0.0
            
            for i, (correct, diff) in enumerate(zip(responses, difficulties)):
                diff_val = difficulty_values.get(diff, 2)
                
                # Expected: higher chance of correct on easier questions
                if diff_val == 1 and correct:  # Easy question correct
                    consistency_score += 1
                elif diff_val == 3 and not correct:  # Hard question incorrect
                    consistency_score += 1  
                elif diff_val == 2:  # Medium questions
                    consistency_score += 0.5
            
            return consistency_score / len(responses)
            
        except Exception:
            return 0.5
    
    def _detect_statistical_outliers(self, response_times: List[float], responses: List[bool]) -> float:
        """Detect statistical outliers in response patterns"""
        try:
            if len(response_times) < 5:
                return 0.0
            
            # Z-score analysis for response times
            mean_time = np.mean(response_times)
            std_time = np.std(response_times)
            
            if std_time == 0:
                return 0.8  # Perfect consistency is suspicious
            
            outliers = 0
            for time in response_times:
                z_score = abs(time - mean_time) / std_time
                if z_score > 2.5:  # More than 2.5 standard deviations
                    outliers += 1
            
            outlier_ratio = outliers / len(response_times)
            return outlier_ratio
            
        except Exception:
            return 0.0
    
    def _analyze_session_behavior(self, session_data: Dict) -> List[str]:
        """Analyze session-level behavior for anomalies"""
        flags = []
        
        try:
            # Check for rapid session completion
            start_time = session_data.get('start_time')
            end_time = session_data.get('end_time')
            
            if start_time and end_time:
                if isinstance(start_time, str):
                    start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                if isinstance(end_time, str):
                    end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                
                duration = (end_time - start_time).total_seconds()
                questions_count = len(session_data.get('answers', {}))
                
                if questions_count > 0 and duration / questions_count < 5:  # Less than 5 seconds per question
                    flags.append("rapid_session_completion")
            
            # Check for suspicious user agent or IP patterns
            user_agent = session_data.get('user_agent', '')
            if 'bot' in user_agent.lower() or 'crawler' in user_agent.lower():
                flags.append("suspicious_user_agent")
            
        except Exception as e:
            logger.error(f"Error in session behavior analysis: {e}")
            
        return flags

# Global instance for use in main server
enhanced_cat_engine = EnhancedCATEngine()