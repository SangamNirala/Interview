#!/usr/bin/env python3
"""
🎯 MODULE 2: STATISTICAL ANOMALY DETECTION SYSTEM - Step 2.3
Real-time Risk Scoring System for Advanced Anti-Cheating

This module implements comprehensive real-time risk scoring that integrates with:
- Step 2.1: AnomalyDetectionEngine (ML-powered pattern recognition)
- Step 2.2: StatisticalAnomalyAnalyzer (advanced statistical analysis)

Key Features:
- Composite risk score aggregation from multiple anomaly detection engines
- Real-time risk factor updates with sliding window analysis
- Multi-level intervention alerts (LOW, MEDIUM, HIGH, CRITICAL)
- Statistical confidence intervals for risk assessments
- WebSocket support for live dashboard updates

Author: AI Assistant
Created: 2025
"""

import asyncio
import logging
import statistics
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import defaultdict, deque
from dataclasses import dataclass, field
import uuid
import json
import threading
import time
from scipy import stats
from scipy.stats import norm, beta
import warnings
warnings.filterwarnings('ignore')

# WebSocket support (will be implemented in Phase 2)
try:
    import websockets
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    logging.warning("WebSocket support not available - install websockets package for real-time updates")

@dataclass
class RiskFactor:
    """Individual risk factor with metadata"""
    name: str
    value: float
    weight: float
    confidence: float
    source: str  # 'anomaly_engine', 'statistical_analyzer', 'behavioral', etc.
    timestamp: datetime
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass  
class RiskAlert:
    """Risk alert with escalation information"""
    alert_id: str
    session_id: str
    risk_level: str
    risk_score: float
    threshold_exceeded: float
    triggered_at: datetime
    alert_type: str
    message: str
    escalation_level: int = 1
    acknowledged: bool = False
    resolved: bool = False
    context: Dict[str, Any] = field(default_factory=dict)

class RealTimeRiskCalculator:
    """
    Real-time Risk Scoring System that aggregates risk scores from multiple 
    anomaly detection engines and provides comprehensive risk assessment
    
    Integrates with:
    - AnomalyDetectionEngine (Step 2.1)
    - StatisticalAnomalyAnalyzer (Step 2.2)
    - Behavioral biometric analysis (when available)
    """
    
    def __init__(self, anomaly_engine=None, statistical_analyzer=None):
        """Initialize the Real-time Risk Calculator"""
        self.logger = logging.getLogger(__name__)
        
        # Engine integrations
        self.anomaly_engine = anomaly_engine
        self.statistical_analyzer = statistical_analyzer
        
        # Risk scoring configuration
        self.risk_thresholds = {
            'LOW': 0.3,
            'MEDIUM': 0.5, 
            'HIGH': 0.7,
            'CRITICAL': 0.9
        }
        
        # Risk factor weights (configurable)
        self.risk_factor_weights = {
            'statistical_anomalies': 0.25,      # From StatisticalAnomalyAnalyzer
            'ml_predictions': 0.25,             # From AnomalyDetectionEngine
            'behavioral_biometrics': 0.20,      # From behavioral analysis
            'response_patterns': 0.15,          # Response timing/accuracy patterns
            'collaboration_indicators': 0.10,   # Cross-session collaboration
            'timing_irregularities': 0.05       # Timing manipulation indicators
        }
        
        # Real-time data structures
        self.active_sessions = {}  # session_id -> session risk data
        self.risk_factor_history = defaultdict(lambda: deque(maxlen=100))  # Sliding window
        self.active_alerts = {}    # alert_id -> RiskAlert
        self.session_risk_cache = {}  # Performance optimization
        
        # Sliding window configuration
        self.window_size = 50  # Number of recent responses to consider
        self.update_interval = 30  # Update interval in seconds
        self.confidence_levels = [0.80, 0.90, 0.95, 0.99]
        
        # Threading for continuous updates
        self.update_thread = None
        self.stop_updates = threading.Event()
        
        # WebSocket connections (for real-time dashboard)
        self.websocket_connections = set()
        
        self.logger.info("RealTimeRiskCalculator initialized successfully")
    
    async def calculate_composite_risk_score(self, session_id: str, current_response_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Aggregate risk scores from multiple anomaly detection engines
        
        Combines scores from:
        - AnomalyDetectionEngine (ML predictions)
        - StatisticalAnomalyAnalyzer (statistical anomalies)
        - Behavioral biometric scores (if available)
        - Response pattern irregularities
        - Timing and progression anomalies
        
        Args:
            session_id: Session identifier
            current_response_data: Latest response data for real-time calculation
            
        Returns:
            Comprehensive composite risk score with detailed breakdown
        """
        try:
            self.logger.info(f"Calculating composite risk score for session: {session_id}")
            
            # Get current session data
            session_data = await self._get_session_data(session_id)
            if not session_data:
                return {
                    'success': False,
                    'error': 'Session data not found',
                    'session_id': session_id
                }
            
            # Update session data with current response if provided
            if current_response_data:
                session_data = self._update_session_with_current_response(session_data, current_response_data)
            
            # Collect risk factors from all engines
            risk_factors = []
            
            # 1. Get risk factors from AnomalyDetectionEngine (Step 2.1)
            if self.anomaly_engine:
                anomaly_factors = await self._get_anomaly_engine_risk_factors(session_data)
                risk_factors.extend(anomaly_factors)
            
            # 2. Get risk factors from StatisticalAnomalyAnalyzer (Step 2.2)  
            if self.statistical_analyzer:
                statistical_factors = await self._get_statistical_analyzer_risk_factors(session_data)
                risk_factors.extend(statistical_factors)
            
            # 3. Get behavioral biometric risk factors
            behavioral_factors = await self._get_behavioral_risk_factors(session_data)
            risk_factors.extend(behavioral_factors)
            
            # 4. Calculate response pattern risk factors
            response_pattern_factors = await self._calculate_response_pattern_risk_factors(session_data)
            risk_factors.extend(response_pattern_factors)
            
            # 5. Calculate timing irregularity factors
            timing_factors = await self._calculate_timing_risk_factors(session_data)
            risk_factors.extend(timing_factors)
            
            # Calculate weighted composite score
            composite_score = self._calculate_weighted_composite_score(risk_factors)
            
            # Generate risk breakdown
            risk_breakdown = self._generate_risk_breakdown(risk_factors)
            
            # Determine risk level
            risk_level = self._determine_risk_level(composite_score)
            
            # Generate confidence intervals
            confidence_intervals = await self.generate_confidence_intervals(session_id, risk_factors)
            
            # Check if alerts should be triggered
            alerts_triggered = await self._check_alert_thresholds(session_id, composite_score, risk_level)
            
            # Generate recommendations
            recommendations = self._generate_risk_recommendations(composite_score, risk_level, risk_breakdown)
            
            # Update session risk cache
            risk_assessment = {
                'success': True,
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'composite_risk_score': float(composite_score),
                'risk_level': risk_level,
                'risk_breakdown': risk_breakdown,
                'confidence_intervals': confidence_intervals,
                'alerts_triggered': alerts_triggered,
                'recommendations': recommendations,
                'total_risk_factors': len(risk_factors),
                'calculation_metadata': {
                    'engines_used': self._get_engines_used(),
                    'window_size': self.window_size,
                    'update_interval': self.update_interval,
                    'calculation_time_ms': 0  # Will be calculated
                }
            }
            
            # Cache the result
            self.session_risk_cache[session_id] = risk_assessment
            
            # Store in risk factor history for sliding window
            self.risk_factor_history[session_id].append({
                'timestamp': datetime.utcnow(),
                'composite_score': composite_score,
                'risk_factors': [rf.__dict__ if hasattr(rf, '__dict__') else rf for rf in risk_factors]
            })
            
            # Send real-time updates via WebSocket (if available)
            if WEBSOCKET_AVAILABLE:
                await self._broadcast_risk_update(risk_assessment)
            
            self.logger.info(f"Composite risk score calculated: {composite_score:.3f} ({risk_level}) for session {session_id}")
            return risk_assessment
            
        except Exception as e:
            self.logger.error(f"Error calculating composite risk score for session {session_id}: {str(e)}")
            return {
                'success': False,
                'session_id': session_id,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def update_risk_factors_continuously(self, session_id: str, new_response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Real-time updating of risk factors as session progresses
        
        Features:
        - Sliding window analysis for recent activity patterns
        - Dynamic weight adjustment based on session evolution
        - Incremental risk calculation for performance
        - Risk factor history and trend analysis
        
        Args:
            session_id: Session identifier
            new_response_data: New response data to incorporate
            
        Returns:
            Updated risk assessment with trends and incremental changes
        """
        try:
            self.logger.info(f"Updating risk factors continuously for session: {session_id}")
            
            # Get current risk state
            current_risk = self.session_risk_cache.get(session_id, {})
            previous_score = current_risk.get('composite_risk_score', 0.0)
            
            # Calculate new composite risk score with new data
            updated_assessment = await self.calculate_composite_risk_score(session_id, new_response_data)
            
            if not updated_assessment.get('success'):
                return updated_assessment
            
            new_score = updated_assessment['composite_risk_score']
            
            # Calculate trend analysis
            trend_analysis = self._calculate_risk_trend_analysis(session_id, new_score, previous_score)
            
            # Dynamic weight adjustment based on session evolution
            adjusted_weights = self._adjust_weights_dynamically(session_id, new_response_data)
            
            # Sliding window analysis
            sliding_window_analysis = self._analyze_sliding_window(session_id)
            
            # Incremental risk calculation metrics
            incremental_metrics = {
                'score_change': float(new_score - previous_score),
                'score_change_percentage': float((new_score - previous_score) / max(previous_score, 0.01) * 100),
                'trend_direction': 'increasing' if new_score > previous_score else 'decreasing' if new_score < previous_score else 'stable',
                'volatility': self._calculate_score_volatility(session_id),
                'momentum': self._calculate_risk_momentum(session_id)
            }
            
            # Check for significant risk changes
            significant_change = abs(new_score - previous_score) > 0.1
            if significant_change:
                await self._handle_significant_risk_change(session_id, previous_score, new_score, trend_analysis)
            
            # Update response with continuous update metadata
            updated_assessment.update({
                'continuous_update': True,
                'previous_risk_score': float(previous_score),
                'trend_analysis': trend_analysis,
                'adjusted_weights': adjusted_weights,
                'sliding_window_analysis': sliding_window_analysis,
                'incremental_metrics': incremental_metrics,
                'significant_change_detected': significant_change,
                'update_sequence': len(self.risk_factor_history[session_id])
            })
            
            # Real-time dashboard update
            if significant_change and WEBSOCKET_AVAILABLE:
                await self._broadcast_significant_change_alert(session_id, updated_assessment)
            
            self.logger.info(f"Risk factors updated continuously for session {session_id}: {previous_score:.3f} → {new_score:.3f}")
            return updated_assessment
            
        except Exception as e:
            self.logger.error(f"Error updating risk factors continuously for session {session_id}: {str(e)}")
            return {
                'success': False,
                'session_id': session_id,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def trigger_intervention_alerts(self, session_id: str, current_risk_assessment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Define risk thresholds for different intervention levels and generate real-time alerts
        
        Alert Levels:
        - LOW (0.3): Monitoring alert
        - MEDIUM (0.5): Supervisor notification  
        - HIGH (0.7): Immediate manual review required
        - CRITICAL (0.9): Test termination recommended
        
        Features:
        - Multiple alert types with escalation protocols
        - Rate limiting to prevent alert spam
        - Alert acknowledgment and resolution tracking
        - Integration with notification systems
        
        Args:
            session_id: Session identifier
            current_risk_assessment: Current risk assessment (optional)
            
        Returns:
            Alert generation results with escalation information
        """
        try:
            self.logger.info(f"Checking intervention alert thresholds for session: {session_id}")
            
            # Get current risk assessment
            if not current_risk_assessment:
                current_risk_assessment = await self.calculate_composite_risk_score(session_id)
            
            if not current_risk_assessment.get('success'):
                return current_risk_assessment
            
            risk_score = current_risk_assessment['composite_risk_score']
            risk_level = current_risk_assessment['risk_level']
            
            # Check if we need to generate new alerts
            alerts_generated = []
            escalation_actions = []
            
            # Determine alert type based on risk level
            if risk_score >= self.risk_thresholds['CRITICAL']:
                alert = await self._generate_critical_alert(session_id, risk_score, current_risk_assessment)
                alerts_generated.append(alert)
                escalation_actions.extend(['immediate_manual_review', 'consider_test_termination', 'security_team_notification'])
                
            elif risk_score >= self.risk_thresholds['HIGH']:
                alert = await self._generate_high_alert(session_id, risk_score, current_risk_assessment)
                alerts_generated.append(alert)
                escalation_actions.extend(['immediate_manual_review', 'supervisor_notification'])
                
            elif risk_score >= self.risk_thresholds['MEDIUM']:
                alert = await self._generate_medium_alert(session_id, risk_score, current_risk_assessment)
                alerts_generated.append(alert)
                escalation_actions.extend(['supervisor_notification', 'enhanced_monitoring'])
                
            elif risk_score >= self.risk_thresholds['LOW']:
                alert = await self._generate_low_alert(session_id, risk_score, current_risk_assessment)
                alerts_generated.append(alert)
                escalation_actions.extend(['monitoring_alert', 'log_for_review'])
            
            # Rate limiting check
            rate_limited_alerts = self._apply_alert_rate_limiting(session_id, alerts_generated)
            
            # Store alerts in active alerts tracking
            for alert in rate_limited_alerts:
                self.active_alerts[alert.alert_id] = alert
            
            # Integration with notification systems
            notification_results = await self._send_alert_notifications(rate_limited_alerts)
            
            # Generate alert summary
            alert_summary = {
                'success': True,
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'current_risk_score': float(risk_score),
                'current_risk_level': risk_level,
                'alerts_generated': len(rate_limited_alerts),
                'alerts_rate_limited': len(alerts_generated) - len(rate_limited_alerts),
                'escalation_actions': escalation_actions,
                'alert_details': [self._serialize_alert(alert) for alert in rate_limited_alerts],
                'notification_results': notification_results,
                'active_alerts_count': len([a for a in self.active_alerts.values() if a.session_id == session_id and not a.resolved]),
                'escalation_protocols': {
                    'immediate_action_required': risk_score >= self.risk_thresholds['HIGH'],
                    'manual_review_required': risk_score >= self.risk_thresholds['MEDIUM'],
                    'automated_monitoring': risk_score >= self.risk_thresholds['LOW']
                }
            }
            
            # Real-time alert broadcasting
            if rate_limited_alerts and WEBSOCKET_AVAILABLE:
                await self._broadcast_alert_notifications(alert_summary)
            
            self.logger.info(f"Alert check completed for session {session_id}: {len(rate_limited_alerts)} alerts generated at {risk_level} level")
            return alert_summary
            
        except Exception as e:
            self.logger.error(f"Error triggering intervention alerts for session {session_id}: {str(e)}")
            return {
                'success': False,
                'session_id': session_id,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    async def generate_confidence_intervals(self, session_id: str, risk_factors: List[RiskFactor] = None) -> Dict[str, Any]:
        """
        Statistical confidence intervals for risk scores
        
        Features:
        - Multiple confidence levels (80%, 90%, 95%, 99%)
        - Bootstrap and analytical confidence interval methods
        - Uncertainty quantification in risk assessment
        - Confidence-based decision making support
        
        Args:
            session_id: Session identifier
            risk_factors: Risk factors to analyze (optional)
            
        Returns:
            Comprehensive confidence interval analysis
        """
        try:
            self.logger.info(f"Generating confidence intervals for session: {session_id}")
            
            # Get risk factors if not provided
            if not risk_factors:
                current_assessment = await self.calculate_composite_risk_score(session_id)
                if not current_assessment.get('success'):
                    return current_assessment
                # Extract risk factors from assessment (simplified for now)
                risk_factors = []
            
            # Get historical risk scores for the session
            historical_scores = self._get_historical_risk_scores(session_id)
            
            if len(historical_scores) < 5:
                # Insufficient data for statistical confidence intervals
                return {
                    'success': True,
                    'session_id': session_id,
                    'timestamp': datetime.utcnow().isoformat(),
                    'confidence_intervals': {},
                    'message': 'Insufficient historical data for confidence interval calculation',
                    'minimum_samples_needed': 5,
                    'current_samples': len(historical_scores)
                }
            
            confidence_intervals = {}
            
            # Calculate confidence intervals for multiple confidence levels
            for confidence_level in self.confidence_levels:
                alpha = 1 - confidence_level
                
                # Method 1: Bootstrap confidence intervals
                bootstrap_ci = self._calculate_bootstrap_confidence_interval(historical_scores, confidence_level)
                
                # Method 2: Analytical confidence intervals (assuming normal distribution)
                analytical_ci = self._calculate_analytical_confidence_interval(historical_scores, confidence_level)
                
                # Method 3: Bayesian confidence intervals (if sufficient data)
                bayesian_ci = self._calculate_bayesian_confidence_interval(historical_scores, confidence_level)
                
                confidence_intervals[f"{int(confidence_level*100)}%"] = {
                    'confidence_level': float(confidence_level),
                    'alpha': float(alpha),
                    'bootstrap_method': bootstrap_ci,
                    'analytical_method': analytical_ci,
                    'bayesian_method': bayesian_ci,
                    'recommended_method': self._select_best_ci_method(bootstrap_ci, analytical_ci, bayesian_ci),
                    'interpretation': self._interpret_confidence_interval(bootstrap_ci, confidence_level)
                }
            
            # Calculate uncertainty metrics
            uncertainty_metrics = self._calculate_uncertainty_metrics(historical_scores, confidence_intervals)
            
            # Generate confidence-based recommendations
            confidence_based_recommendations = self._generate_confidence_based_recommendations(
                confidence_intervals, uncertainty_metrics
            )
            
            result = {
                'success': True,
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'confidence_intervals': confidence_intervals,
                'uncertainty_metrics': uncertainty_metrics,
                'confidence_based_recommendations': confidence_based_recommendations,
                'statistical_summary': {
                    'sample_size': len(historical_scores),
                    'mean_risk_score': float(statistics.mean(historical_scores)),
                    'std_risk_score': float(statistics.stdev(historical_scores)) if len(historical_scores) > 1 else 0.0,
                    'min_risk_score': float(min(historical_scores)),
                    'max_risk_score': float(max(historical_scores)),
                    'score_volatility': float(statistics.stdev(historical_scores)) if len(historical_scores) > 1 else 0.0
                },
                'methodology': {
                    'bootstrap_samples': 1000,
                    'analytical_assumption': 'normal_distribution',
                    'bayesian_prior': 'beta_distribution',
                    'confidence_levels_calculated': [int(cl*100) for cl in self.confidence_levels]
                }
            }
            
            self.logger.info(f"Confidence intervals generated for session {session_id} with {len(historical_scores)} samples")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating confidence intervals for session {session_id}: {str(e)}")
            return {
                'success': False,
                'session_id': session_id,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    # ===== HELPER METHODS =====
    
    async def _get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive session data for risk calculation"""
        try:
            # This would typically fetch from database
            # For now, return mock data structure
            return {
                'session_id': session_id,
                'responses': [],
                'timings': [],
                'metadata': {},
                'start_time': datetime.utcnow() - timedelta(minutes=30),
                'last_update': datetime.utcnow()
            }
        except Exception as e:
            self.logger.error(f"Error getting session data for {session_id}: {str(e)}")
            return None
    
    def _update_session_with_current_response(self, session_data: Dict[str, Any], current_response: Dict[str, Any]) -> Dict[str, Any]:
        """Update session data with current response"""
        updated_session = session_data.copy()
        if 'responses' not in updated_session:
            updated_session['responses'] = []
        updated_session['responses'].append(current_response)
        updated_session['last_update'] = datetime.utcnow()
        return updated_session
    
    async def _get_anomaly_engine_risk_factors(self, session_data: Dict[str, Any]) -> List[RiskFactor]:
        """Get risk factors from AnomalyDetectionEngine (Step 2.1)"""
        risk_factors = []
        try:
            if self.anomaly_engine:
                # Call anomaly detection methods
                pattern_results = self.anomaly_engine.detect_response_pattern_anomalies(session_data)
                inconsistency_results = self.anomaly_engine.analyze_performance_inconsistencies(session_data)
                probability_results = self.anomaly_engine.calculate_anomaly_probability_scores(session_data)
                
                # Convert results to risk factors
                if pattern_results.get('success'):
                    overall_assessment = pattern_results.get('overall_assessment', {})
                    if 'overall_anomaly_score' in overall_assessment:
                        risk_factors.append(RiskFactor(
                            name='ml_pattern_anomalies',
                            value=float(overall_assessment['overall_anomaly_score']),
                            weight=self.risk_factor_weights['ml_predictions'],
                            confidence=float(overall_assessment.get('confidence_score', 0.8)),
                            source='anomaly_engine',
                            timestamp=datetime.utcnow(),
                            context=pattern_results
                        ))
                
                if probability_results.get('success'):
                    composite_prob = probability_results.get('composite_anomaly_probability', 0.0)
                    risk_factors.append(RiskFactor(
                        name='ml_probability_score',
                        value=float(composite_prob),
                        weight=self.risk_factor_weights['ml_predictions'] * 0.5,
                        confidence=float(probability_results.get('statistical_significance', {}).get('confidence', 0.8)),
                        source='anomaly_engine',
                        timestamp=datetime.utcnow(),
                        context=probability_results
                    ))
                    
        except Exception as e:
            self.logger.warning(f"Error getting anomaly engine risk factors: {str(e)}")
        
        return risk_factors
    
    async def _get_statistical_analyzer_risk_factors(self, session_data: Dict[str, Any]) -> List[RiskFactor]:
        """Get risk factors from StatisticalAnomalyAnalyzer (Step 2.2)"""
        risk_factors = []
        try:
            if self.statistical_analyzer:
                # Call statistical analysis methods
                pattern_analysis = self.statistical_analyzer.detect_answer_pattern_irregularities(session_data)
                difficulty_analysis = self.statistical_analyzer.analyze_difficulty_progression_anomalies(session_data)
                timezone_analysis = self.statistical_analyzer.identify_time_zone_manipulation(session_data)
                collaboration_analysis = self.statistical_analyzer.detect_collaborative_cheating_patterns(session_data)
                
                # Convert results to risk factors
                if pattern_analysis.get('success'):
                    irregularity_score = pattern_analysis.get('irregularity_score', 0.0)
                    risk_factors.append(RiskFactor(
                        name='statistical_pattern_irregularities',
                        value=float(irregularity_score),
                        weight=self.risk_factor_weights['statistical_anomalies'],
                        confidence=0.85,
                        source='statistical_analyzer',
                        timestamp=datetime.utcnow(),
                        context=pattern_analysis
                    ))
                
                if difficulty_analysis.get('success'):
                    anomaly_score = difficulty_analysis.get('anomaly_score', 0.0)
                    risk_factors.append(RiskFactor(
                        name='difficulty_progression_anomalies',
                        value=float(anomaly_score),
                        weight=self.risk_factor_weights['statistical_anomalies'] * 0.6,
                        confidence=0.8,
                        source='statistical_analyzer',
                        timestamp=datetime.utcnow(),
                        context=difficulty_analysis
                    ))
                
                if timezone_analysis.get('success'):
                    manipulation_score = timezone_analysis.get('manipulation_score', 0.0)
                    risk_factors.append(RiskFactor(
                        name='timezone_manipulation',
                        value=float(manipulation_score),
                        weight=self.risk_factor_weights['timing_irregularities'],
                        confidence=0.75,
                        source='statistical_analyzer',
                        timestamp=datetime.utcnow(),
                        context=timezone_analysis
                    ))
                
                if collaboration_analysis.get('success'):
                    collaboration_score = collaboration_analysis.get('collaboration_score', 0.0)
                    risk_factors.append(RiskFactor(
                        name='collaborative_cheating',
                        value=float(collaboration_score),
                        weight=self.risk_factor_weights['collaboration_indicators'],
                        confidence=0.8,
                        source='statistical_analyzer',
                        timestamp=datetime.utcnow(),
                        context=collaboration_analysis
                    ))
                    
        except Exception as e:
            self.logger.warning(f"Error getting statistical analyzer risk factors: {str(e)}")
        
        return risk_factors
    
    async def _get_behavioral_risk_factors(self, session_data: Dict[str, Any]) -> List[RiskFactor]:
        """Get behavioral biometric risk factors"""
        risk_factors = []
        try:
            # Placeholder for behavioral biometric integration
            # This would integrate with behavioral_biometrics_engine if available
            behavioral_score = 0.3  # Mock score
            risk_factors.append(RiskFactor(
                name='behavioral_biometrics',
                value=float(behavioral_score),
                weight=self.risk_factor_weights['behavioral_biometrics'],
                confidence=0.7,
                source='behavioral_analysis',
                timestamp=datetime.utcnow(),
                context={'analysis_type': 'behavioral_biometrics', 'mock_data': True}
            ))
        except Exception as e:
            self.logger.warning(f"Error getting behavioral risk factors: {str(e)}")
        
        return risk_factors
    
    async def _calculate_response_pattern_risk_factors(self, session_data: Dict[str, Any]) -> List[RiskFactor]:
        """Calculate response pattern risk factors"""
        risk_factors = []
        try:
            responses = session_data.get('responses', [])
            if not responses:
                return risk_factors
            
            # Response time consistency analysis
            response_times = [r.get('response_time', 0) for r in responses if r.get('response_time', 0) > 0]
            if len(response_times) > 3:
                time_consistency = self._analyze_response_time_consistency(response_times)
                risk_factors.append(RiskFactor(
                    name='response_time_consistency',
                    value=float(1 - time_consistency),  # Convert consistency to risk
                    weight=self.risk_factor_weights['response_patterns'] * 0.6,
                    confidence=0.8,
                    source='response_pattern_analysis',
                    timestamp=datetime.utcnow(),
                    context={'response_times_analyzed': len(response_times)}
                ))
            
            # Accuracy pattern analysis
            accuracy_scores = [1 if r.get('is_correct', False) else 0 for r in responses]
            if len(accuracy_scores) > 5:
                accuracy_risk = self._analyze_accuracy_pattern_risk(accuracy_scores)
                risk_factors.append(RiskFactor(
                    name='accuracy_pattern_risk',
                    value=float(accuracy_risk),
                    weight=self.risk_factor_weights['response_patterns'] * 0.4,
                    confidence=0.75,
                    source='response_pattern_analysis',
                    timestamp=datetime.utcnow(),
                    context={'accuracy_responses_analyzed': len(accuracy_scores)}
                ))
                
        except Exception as e:
            self.logger.warning(f"Error calculating response pattern risk factors: {str(e)}")
        
        return risk_factors
    
    async def _calculate_timing_risk_factors(self, session_data: Dict[str, Any]) -> List[RiskFactor]:
        """Calculate timing irregularity risk factors"""
        risk_factors = []
        try:
            # Timing irregularity analysis
            timing_risk = 0.2  # Mock calculation
            risk_factors.append(RiskFactor(
                name='timing_irregularities',
                value=float(timing_risk),
                weight=self.risk_factor_weights['timing_irregularities'],
                confidence=0.7,
                source='timing_analysis',
                timestamp=datetime.utcnow(),
                context={'analysis_type': 'timing_irregularities'}
            ))
        except Exception as e:
            self.logger.warning(f"Error calculating timing risk factors: {str(e)}")
        
        return risk_factors
    
    def _calculate_weighted_composite_score(self, risk_factors: List[RiskFactor]) -> float:
        """Calculate weighted composite risk score from risk factors"""
        if not risk_factors:
            return 0.0
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for factor in risk_factors:
            weighted_score = factor.value * factor.weight * factor.confidence
            total_weighted_score += weighted_score
            total_weight += factor.weight * factor.confidence
        
        if total_weight == 0:
            return 0.0
        
        composite_score = total_weighted_score / total_weight
        return min(max(composite_score, 0.0), 1.0)  # Clamp between 0 and 1
    
    def _generate_risk_breakdown(self, risk_factors: List[RiskFactor]) -> Dict[str, Any]:
        """Generate detailed risk breakdown by category"""
        breakdown = {}
        
        # Group risk factors by source
        by_source = defaultdict(list)
        for factor in risk_factors:
            by_source[factor.source].append(factor)
        
        # Calculate breakdown by source
        for source, factors in by_source.items():
            source_score = sum(f.value * f.weight * f.confidence for f in factors)
            source_weight = sum(f.weight * f.confidence for f in factors)
            
            breakdown[source] = {
                'score': float(source_score / source_weight if source_weight > 0 else 0),
                'weight': float(source_weight),
                'factor_count': len(factors),
                'confidence': float(statistics.mean([f.confidence for f in factors]))
            }
        
        return breakdown
    
    def _determine_risk_level(self, composite_score: float) -> str:
        """Determine risk level based on composite score"""
        if composite_score >= self.risk_thresholds['CRITICAL']:
            return 'CRITICAL'
        elif composite_score >= self.risk_thresholds['HIGH']:
            return 'HIGH'
        elif composite_score >= self.risk_thresholds['MEDIUM']:
            return 'MEDIUM'
        elif composite_score >= self.risk_thresholds['LOW']:
            return 'LOW'
        else:
            return 'MINIMAL'
    
    async def _check_alert_thresholds(self, session_id: str, composite_score: float, risk_level: str) -> List[str]:
        """Check if any alert thresholds are exceeded"""
        alerts_triggered = []
        
        for threshold_name, threshold_value in self.risk_thresholds.items():
            if composite_score >= threshold_value:
                alerts_triggered.append(f"{threshold_name}_RISK_THRESHOLD")
        
        return alerts_triggered
    
    def _generate_risk_recommendations(self, composite_score: float, risk_level: str, risk_breakdown: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on risk assessment"""
        recommendations = []
        
        if risk_level == 'CRITICAL':
            recommendations.extend([
                "Immediate manual review required",
                "Consider test termination",
                "Escalate to security team",
                "Review all session data for evidence"
            ])
        elif risk_level == 'HIGH':
            recommendations.extend([
                "Immediate manual review required",
                "Enhanced monitoring of remaining session",
                "Notify supervisor immediately"
            ])
        elif risk_level == 'MEDIUM':
            recommendations.extend([
                "Supervisor notification recommended",
                "Enhanced monitoring enabled",
                "Review session patterns"
            ])
        elif risk_level == 'LOW':
            recommendations.extend([
                "Continue monitoring",
                "Log for post-session review"
            ])
        else:
            recommendations.append("Normal session - continue standard monitoring")
        
        # Add specific recommendations based on risk breakdown
        for source, data in risk_breakdown.items():
            if data['score'] > 0.7:
                if source == 'anomaly_engine':
                    recommendations.append("Review ML anomaly detection patterns")
                elif source == 'statistical_analyzer':
                    recommendations.append("Investigate statistical anomalies in detail")
                elif source == 'behavioral_analysis':
                    recommendations.append("Analyze behavioral biometric patterns")
        
        return recommendations
    
    def _get_engines_used(self) -> List[str]:
        """Get list of engines currently in use"""
        engines = []
        if self.anomaly_engine:
            engines.append('AnomalyDetectionEngine')
        if self.statistical_analyzer:
            engines.append('StatisticalAnomalyAnalyzer')
        engines.append('RealTimeRiskCalculator')
        return engines
    
    def _calculate_risk_trend_analysis(self, session_id: str, new_score: float, previous_score: float) -> Dict[str, Any]:
        """Calculate risk trend analysis"""
        history = list(self.risk_factor_history[session_id])
        
        if len(history) < 2:
            return {
                'trend': 'insufficient_data',
                'slope': 0.0,
                'correlation': 0.0,
                'volatility': 0.0
            }
        
        scores = [h['composite_score'] for h in history]
        timestamps = [i for i in range(len(scores))]
        
        # Calculate trend slope
        if len(scores) > 1:
            slope, intercept, r_value, p_value, std_err = stats.linregress(timestamps, scores)
            trend = 'increasing' if slope > 0.05 else 'decreasing' if slope < -0.05 else 'stable'
        else:
            slope, r_value, trend = 0.0, 0.0, 'stable'
        
        # Calculate volatility
        volatility = float(statistics.stdev(scores)) if len(scores) > 1 else 0.0
        
        return {
            'trend': trend,
            'slope': float(slope),
            'correlation': float(r_value),
            'volatility': volatility,
            'sample_size': len(scores)
        }
    
    def _adjust_weights_dynamically(self, session_id: str, new_response_data: Dict[str, Any]) -> Dict[str, float]:
        """Dynamically adjust risk factor weights based on session evolution"""
        # For now, return current weights
        # In production, this would implement dynamic weight adjustment logic
        return self.risk_factor_weights.copy()
    
    def _analyze_sliding_window(self, session_id: str) -> Dict[str, Any]:
        """Analyze risk patterns in sliding window"""
        history = list(self.risk_factor_history[session_id])
        
        if len(history) < 5:
            return {'available': False, 'message': 'Insufficient data for sliding window analysis'}
        
        # Get recent window
        window_data = history[-self.window_size:]
        scores = [h['composite_score'] for h in window_data]
        
        return {
            'available': True,
            'window_size': len(window_data),
            'mean_score': float(statistics.mean(scores)),
            'std_score': float(statistics.stdev(scores)) if len(scores) > 1 else 0.0,
            'min_score': float(min(scores)),
            'max_score': float(max(scores)),
            'trend': 'increasing' if scores[-1] > scores[0] else 'decreasing' if scores[-1] < scores[0] else 'stable'
        }
    
    def _calculate_score_volatility(self, session_id: str) -> float:
        """Calculate risk score volatility"""
        history = list(self.risk_factor_history[session_id])
        if len(history) < 2:
            return 0.0
        
        scores = [h['composite_score'] for h in history]
        return float(statistics.stdev(scores))
    
    def _calculate_risk_momentum(self, session_id: str) -> float:
        """Calculate risk momentum (rate of change)"""
        history = list(self.risk_factor_history[session_id])
        if len(history) < 3:
            return 0.0
        
        # Calculate momentum as average rate of change over recent periods
        recent_scores = [h['composite_score'] for h in history[-5:]]
        changes = [recent_scores[i] - recent_scores[i-1] for i in range(1, len(recent_scores))]
        
        return float(statistics.mean(changes)) if changes else 0.0
    
    async def _handle_significant_risk_change(self, session_id: str, previous_score: float, new_score: float, trend_analysis: Dict[str, Any]):
        """Handle significant risk changes"""
        self.logger.warning(f"Significant risk change detected for session {session_id}: {previous_score:.3f} → {new_score:.3f}")
        
        # Log the significant change
        # In production, this might trigger additional monitoring or alerts
        pass
    
    # Alert generation methods
    async def _generate_critical_alert(self, session_id: str, risk_score: float, risk_assessment: Dict[str, Any]) -> RiskAlert:
        """Generate critical level alert"""
        return RiskAlert(
            alert_id=str(uuid.uuid4()),
            session_id=session_id,
            risk_level='CRITICAL',
            risk_score=risk_score,
            threshold_exceeded=self.risk_thresholds['CRITICAL'],
            triggered_at=datetime.utcnow(),
            alert_type='CRITICAL_INTERVENTION_REQUIRED',
            message=f"CRITICAL: Risk score {risk_score:.3f} exceeds critical threshold. Immediate action required.",
            escalation_level=4,
            context=risk_assessment
        )
    
    async def _generate_high_alert(self, session_id: str, risk_score: float, risk_assessment: Dict[str, Any]) -> RiskAlert:
        """Generate high level alert"""
        return RiskAlert(
            alert_id=str(uuid.uuid4()),
            session_id=session_id,
            risk_level='HIGH',
            risk_score=risk_score,
            threshold_exceeded=self.risk_thresholds['HIGH'],
            triggered_at=datetime.utcnow(),
            alert_type='HIGH_RISK_MANUAL_REVIEW',
            message=f"HIGH: Risk score {risk_score:.3f} requires immediate manual review.",
            escalation_level=3,
            context=risk_assessment
        )
    
    async def _generate_medium_alert(self, session_id: str, risk_score: float, risk_assessment: Dict[str, Any]) -> RiskAlert:
        """Generate medium level alert"""
        return RiskAlert(
            alert_id=str(uuid.uuid4()),
            session_id=session_id,
            risk_level='MEDIUM',
            risk_score=risk_score,
            threshold_exceeded=self.risk_thresholds['MEDIUM'],
            triggered_at=datetime.utcnow(),
            alert_type='MEDIUM_RISK_SUPERVISOR_NOTIFICATION',
            message=f"MEDIUM: Risk score {risk_score:.3f} requires supervisor notification.",
            escalation_level=2,
            context=risk_assessment
        )
    
    async def _generate_low_alert(self, session_id: str, risk_score: float, risk_assessment: Dict[str, Any]) -> RiskAlert:
        """Generate low level alert"""
        return RiskAlert(
            alert_id=str(uuid.uuid4()),
            session_id=session_id,
            risk_level='LOW',
            risk_score=risk_score,
            threshold_exceeded=self.risk_thresholds['LOW'],
            triggered_at=datetime.utcnow(),
            alert_type='LOW_RISK_MONITORING',
            message=f"LOW: Risk score {risk_score:.3f} flagged for monitoring.",
            escalation_level=1,
            context=risk_assessment
        )
    
    def _apply_alert_rate_limiting(self, session_id: str, alerts: List[RiskAlert]) -> List[RiskAlert]:
        """Apply rate limiting to prevent alert spam"""
        # Simple rate limiting - in production, this would be more sophisticated
        return alerts[:3]  # Limit to 3 alerts per check
    
    async def _send_alert_notifications(self, alerts: List[RiskAlert]) -> Dict[str, Any]:
        """Send alert notifications to various systems"""
        # Placeholder for notification system integration
        return {
            'email_notifications_sent': len(alerts),
            'dashboard_notifications_sent': len(alerts),
            'webhook_notifications_sent': 0,
            'sms_notifications_sent': 0 if len(alerts) == 0 else (1 if alerts[0].risk_level in ['HIGH', 'CRITICAL'] else 0)
        }
    
    def _serialize_alert(self, alert: RiskAlert) -> Dict[str, Any]:
        """Serialize alert for JSON response"""
        return {
            'alert_id': alert.alert_id,
            'session_id': alert.session_id,
            'risk_level': alert.risk_level,
            'risk_score': alert.risk_score,
            'threshold_exceeded': alert.threshold_exceeded,
            'triggered_at': alert.triggered_at.isoformat(),
            'alert_type': alert.alert_type,
            'message': alert.message,
            'escalation_level': alert.escalation_level,
            'acknowledged': alert.acknowledged,
            'resolved': alert.resolved
        }
    
    # Confidence interval calculation methods
    def _get_historical_risk_scores(self, session_id: str) -> List[float]:
        """Get historical risk scores for confidence interval calculation"""
        history = list(self.risk_factor_history[session_id])
        return [h['composite_score'] for h in history]
    
    def _calculate_bootstrap_confidence_interval(self, scores: List[float], confidence_level: float) -> Dict[str, Any]:
        """Calculate bootstrap confidence interval"""
        try:
            n_bootstrap = 1000
            n_samples = len(scores)
            
            bootstrap_means = []
            for _ in range(n_bootstrap):
                bootstrap_sample = np.random.choice(scores, size=n_samples, replace=True)
                bootstrap_means.append(np.mean(bootstrap_sample))
            
            alpha = 1 - confidence_level
            lower_percentile = (alpha / 2) * 100
            upper_percentile = (1 - alpha / 2) * 100
            
            lower_bound = np.percentile(bootstrap_means, lower_percentile)
            upper_bound = np.percentile(bootstrap_means, upper_percentile)
            
            return {
                'method': 'bootstrap',
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
                'confidence_level': float(confidence_level),
                'bootstrap_samples': n_bootstrap,
                'mean_estimate': float(np.mean(bootstrap_means)),
                'available': True
            }
        except Exception as e:
            return {'method': 'bootstrap', 'available': False, 'error': str(e)}
    
    def _calculate_analytical_confidence_interval(self, scores: List[float], confidence_level: float) -> Dict[str, Any]:
        """Calculate analytical confidence interval assuming normal distribution"""
        try:
            n = len(scores)
            mean_score = statistics.mean(scores)
            std_score = statistics.stdev(scores) if n > 1 else 0
            
            # t-distribution for small samples, normal for large samples
            if n < 30:
                from scipy.stats import t
                t_value = t.ppf((1 + confidence_level) / 2, df=n-1)
            else:
                t_value = norm.ppf((1 + confidence_level) / 2)
            
            margin_of_error = t_value * (std_score / np.sqrt(n))
            lower_bound = mean_score - margin_of_error
            upper_bound = mean_score + margin_of_error
            
            return {
                'method': 'analytical',
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
                'confidence_level': float(confidence_level),
                'mean_estimate': float(mean_score),
                'standard_error': float(std_score / np.sqrt(n)),
                'margin_of_error': float(margin_of_error),
                'distribution_used': 't_distribution' if n < 30 else 'normal_distribution',
                'available': True
            }
        except Exception as e:
            return {'method': 'analytical', 'available': False, 'error': str(e)}
    
    def _calculate_bayesian_confidence_interval(self, scores: List[float], confidence_level: float) -> Dict[str, Any]:
        """Calculate Bayesian confidence interval"""
        try:
            # Simple Bayesian approach using Beta distribution for bounded scores [0,1]
            # Convert scores to successes/failures format
            n = len(scores)
            successes = sum(scores)  # Treating scores as success rates
            
            # Beta distribution parameters (using Jeffrey's prior)
            alpha = successes + 0.5
            beta_param = n - successes + 0.5
            
            alpha_level = 1 - confidence_level
            lower_bound = beta.ppf(alpha_level / 2, alpha, beta_param)
            upper_bound = beta.ppf(1 - alpha_level / 2, alpha, beta_param)
            
            return {
                'method': 'bayesian',
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
                'confidence_level': float(confidence_level),
                'posterior_mean': float(alpha / (alpha + beta_param)),
                'alpha_parameter': float(alpha),
                'beta_parameter': float(beta_param),
                'prior_used': 'jeffreys_prior',
                'available': True
            }
        except Exception as e:
            return {'method': 'bayesian', 'available': False, 'error': str(e)}
    
    def _select_best_ci_method(self, bootstrap_ci: Dict, analytical_ci: Dict, bayesian_ci: Dict) -> str:
        """Select the best confidence interval method based on data characteristics"""
        # Simple heuristic - in production, this would be more sophisticated
        if bootstrap_ci.get('available') and analytical_ci.get('available'):
            return 'bootstrap'  # Generally more robust
        elif analytical_ci.get('available'):
            return 'analytical'
        elif bayesian_ci.get('available'):
            return 'bayesian'
        else:
            return 'none_available'
    
    def _interpret_confidence_interval(self, ci_data: Dict, confidence_level: float) -> str:
        """Interpret confidence interval results"""
        if not ci_data.get('available'):
            return "Confidence interval not available"
        
        lower = ci_data['lower_bound']
        upper = ci_data['upper_bound']
        width = upper - lower
        
        interpretation = f"With {confidence_level*100:.0f}% confidence, the true risk score lies between {lower:.3f} and {upper:.3f}."
        
        if width < 0.1:
            interpretation += " The interval is narrow, indicating high precision."
        elif width > 0.3:
            interpretation += " The interval is wide, indicating higher uncertainty."
        
        return interpretation
    
    def _calculate_uncertainty_metrics(self, scores: List[float], confidence_intervals: Dict) -> Dict[str, Any]:
        """Calculate uncertainty metrics from confidence intervals"""
        try:
            # Calculate average interval width across confidence levels
            interval_widths = []
            for level, ci_data in confidence_intervals.items():
                recommended_method = ci_data.get('recommended_method', 'bootstrap')
                if recommended_method in ci_data and ci_data[recommended_method].get('available'):
                    method_data = ci_data[recommended_method]
                    width = method_data['upper_bound'] - method_data['lower_bound']
                    interval_widths.append(width)
            
            return {
                'average_interval_width': float(statistics.mean(interval_widths)) if interval_widths else 0.0,
                'max_interval_width': float(max(interval_widths)) if interval_widths else 0.0,
                'min_interval_width': float(min(interval_widths)) if interval_widths else 0.0,
                'uncertainty_score': float(statistics.mean(interval_widths)) if interval_widths else 0.5,
                'precision_rating': 'high' if (statistics.mean(interval_widths) if interval_widths else 1.0) < 0.1 else 'medium' if (statistics.mean(interval_widths) if interval_widths else 1.0) < 0.3 else 'low'
            }
        except Exception as e:
            return {'error': str(e), 'uncertainty_score': 0.5}
    
    def _generate_confidence_based_recommendations(self, confidence_intervals: Dict, uncertainty_metrics: Dict) -> List[str]:
        """Generate recommendations based on confidence analysis"""
        recommendations = []
        
        uncertainty_score = uncertainty_metrics.get('uncertainty_score', 0.5)
        precision_rating = uncertainty_metrics.get('precision_rating', 'medium')
        
        if precision_rating == 'high':
            recommendations.append("High precision risk assessment - confidence in risk score is strong")
        elif precision_rating == 'medium':
            recommendations.append("Moderate precision - consider additional data points for higher confidence")
        else:
            recommendations.append("Low precision - risk assessment has high uncertainty, use caution in decision making")
        
        if uncertainty_score > 0.4:
            recommendations.append("High uncertainty detected - consider manual review regardless of risk score")
        
        recommendations.append(f"Uncertainty score: {uncertainty_score:.3f} - factor this into risk-based decisions")
        
        return recommendations
    
    # Helper methods for response pattern analysis
    def _analyze_response_time_consistency(self, response_times: List[float]) -> float:
        """Analyze response time consistency (returns consistency score 0-1)"""
        if len(response_times) < 2:
            return 1.0
        
        mean_time = statistics.mean(response_times)
        std_time = statistics.stdev(response_times)
        
        # Coefficient of variation
        cv = std_time / mean_time if mean_time > 0 else 0
        
        # Convert to consistency score (lower CV = higher consistency)
        consistency = max(0, 1 - cv / 2)  # Normalize assuming CV of 2.0 = 0 consistency
        return min(consistency, 1.0)
    
    def _analyze_accuracy_pattern_risk(self, accuracy_scores: List[int]) -> float:
        """Analyze accuracy patterns for risk indicators"""
        if len(accuracy_scores) < 2:
            return 0.0
        
        # Simple analysis - look for suspicious patterns
        accuracy_rate = statistics.mean(accuracy_scores)
        
        # Risk factors:
        # 1. Perfect accuracy (might indicate cheating)
        # 2. Very low accuracy with sudden improvements
        # 3. Alternating patterns
        
        risk = 0.0
        
        if accuracy_rate == 1.0:  # Perfect accuracy
            risk += 0.3
        
        # Check for alternating patterns
        alternations = sum(1 for i in range(1, len(accuracy_scores)) 
                          if accuracy_scores[i] != accuracy_scores[i-1])
        alternation_rate = alternations / (len(accuracy_scores) - 1) if len(accuracy_scores) > 1 else 0
        
        if alternation_rate > 0.8:  # High alternation might be suspicious
            risk += 0.2
        
        return min(risk, 1.0)
    
    # WebSocket broadcasting methods (placeholders)
    async def _broadcast_risk_update(self, risk_assessment: Dict[str, Any]):
        """Broadcast risk update to connected WebSocket clients"""
        if WEBSOCKET_AVAILABLE and self.websocket_connections:
            message = json.dumps({
                'type': 'risk_update',
                'data': risk_assessment
            })
            # In production, this would broadcast to all connected clients
            pass
    
    async def _broadcast_significant_change_alert(self, session_id: str, assessment: Dict[str, Any]):
        """Broadcast significant change alert"""
        if WEBSOCKET_AVAILABLE and self.websocket_connections:
            message = json.dumps({
                'type': 'significant_change_alert',
                'session_id': session_id,
                'data': assessment
            })
            # In production, this would broadcast to all connected clients
            pass
    
    async def _broadcast_alert_notifications(self, alert_summary: Dict[str, Any]):
        """Broadcast alert notifications"""
        if WEBSOCKET_AVAILABLE and self.websocket_connections:
            message = json.dumps({
                'type': 'alert_notification',
                'data': alert_summary
            })
            # In production, this would broadcast to all connected clients
            pass

    # Continuous update management
    def start_continuous_updates(self):
        """Start continuous risk factor updates in background thread"""
        if not self.update_thread or not self.update_thread.is_alive():
            self.stop_updates.clear()
            self.update_thread = threading.Thread(target=self._continuous_update_worker, daemon=True)
            self.update_thread.start()
            self.logger.info("Continuous risk updates started")
    
    def stop_continuous_updates(self):
        """Stop continuous risk factor updates"""
        self.stop_updates.set()
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=5)
        self.logger.info("Continuous risk updates stopped")
    
    def _continuous_update_worker(self):
        """Background worker for continuous risk updates"""
        while not self.stop_updates.is_set():
            try:
                # Update risk factors for all active sessions
                for session_id in list(self.active_sessions.keys()):
                    asyncio.run(self._periodic_risk_update(session_id))
                
                # Wait for next update interval
                self.stop_updates.wait(self.update_interval)
                
            except Exception as e:
                self.logger.error(f"Error in continuous update worker: {str(e)}")
                self.stop_updates.wait(10)  # Wait 10 seconds before retrying
    
    async def _periodic_risk_update(self, session_id: str):
        """Perform periodic risk update for a session"""
        try:
            # Check if session is still active
            if session_id not in self.active_sessions:
                return
            
            # Calculate current risk score
            current_assessment = await self.calculate_composite_risk_score(session_id)
            
            if current_assessment.get('success'):
                # Check for alerts
                await self.trigger_intervention_alerts(session_id, current_assessment)
                
        except Exception as e:
            self.logger.error(f"Error in periodic risk update for session {session_id}: {str(e)}")