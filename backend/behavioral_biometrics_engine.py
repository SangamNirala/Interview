"""
🔐 MODULE 1: BEHAVIORAL BIOMETRIC ANALYSIS ENGINE
Enterprise-Grade Security System for Adaptive Testing Platform

This module implements comprehensive behavioral biometric analysis including:
- Keystroke Dynamics Analysis 
- Mouse Movement & Interaction Analysis
- Response Timing Behavioral Analysis
- Real-time Anomaly Detection & Intervention
- GDPR-Compliant Data Management

Dependencies: numpy, scipy, pandas, sklearn (built-in Python libraries only)
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics.pairwise import cosine_similarity
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import uuid
import hashlib
import statistics
from collections import defaultdict
import asyncio

class KeystrokeDynamicsAnalyzer:
    """
    Advanced keystroke dynamics analysis for behavioral fingerprinting
    Analyzes typing patterns, rhythm metrics, and detects anomalies
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.baseline_profiles = {}  # Store baseline patterns per user
        self.anomaly_threshold = 2.5  # Standard deviations for anomaly detection
        
    def analyze_typing_patterns(self, keystroke_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze comprehensive typing patterns from keystroke events
        
        Args:
            keystroke_data: List of keystroke events with timestamps and key info
            Format: [{"key": "a", "timestamp": 1234567890.123, "event_type": "keydown/keyup", "duration": 0.1}]
        
        Returns:
            Dict containing detailed typing pattern analysis
        """
        try:
            if not keystroke_data or len(keystroke_data) < 10:
                return {"error": "Insufficient keystroke data for analysis", "patterns": {}}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(keystroke_data)
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Calculate dwell times (key press duration)
            dwell_times = []
            flight_times = []  # Time between keystrokes
            
            # Group by key press/release pairs
            keydown_events = df[df['event_type'] == 'keydown'].copy()
            keyup_events = df[df['event_type'] == 'keyup'].copy()
            
            # Calculate dwell times
            for _, keydown in keydown_events.iterrows():
                keyup_match = keyup_events[
                    (keyup_events['key'] == keydown['key']) & 
                    (keyup_events['timestamp'] > keydown['timestamp'])
                ].head(1)
                
                if not keyup_match.empty:
                    dwell_time = keyup_match.iloc[0]['timestamp'] - keydown['timestamp']
                    dwell_times.append(dwell_time)
            
            # Calculate flight times (time between consecutive keystrokes)
            sorted_keydowns = keydown_events.sort_values('timestamp')
            timestamps = sorted_keydowns['timestamp'].values
            flight_times = np.diff(timestamps)
            
            # Analyze typing rhythm and patterns
            rhythm_analysis = self.calculate_rhythm_metrics(dwell_times, flight_times)
            
            # Character frequency analysis
            char_frequency = df['key'].value_counts().to_dict()
            
            # Typing speed analysis
            total_time = df['timestamp'].max() - df['timestamp'].min()
            typing_speed = len(keydown_events) / (total_time / 60) if total_time > 0 else 0  # WPM approximation
            
            # Pattern consistency analysis
            consistency_metrics = self._analyze_consistency(dwell_times, flight_times)
            
            # Advanced behavioral metrics
            behavioral_metrics = self._calculate_behavioral_metrics(df, dwell_times, flight_times)
            
            return {
                "typing_patterns": {
                    "rhythm_analysis": rhythm_analysis,
                    "character_frequency": char_frequency,
                    "typing_speed_wpm": round(typing_speed, 2),
                    "consistency_metrics": consistency_metrics,
                    "behavioral_metrics": behavioral_metrics,
                    "total_keystrokes": len(keydown_events),
                    "analysis_duration": total_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing typing patterns: {str(e)}")
            return {"error": str(e), "patterns": {}}
    
    def calculate_rhythm_metrics(self, dwell_times: List[float], flight_times: List[float]) -> Dict[str, Any]:
        """
        Calculate comprehensive rhythm metrics from keystroke timing data
        
        Args:
            dwell_times: List of key press durations
            flight_times: List of time intervals between consecutive keystrokes
            
        Returns:
            Dict containing rhythm analysis metrics
        """
        try:
            if not dwell_times or not flight_times:
                return {"error": "Insufficient timing data"}
            
            # Dwell time statistics
            dwell_stats = {
                "mean": np.mean(dwell_times),
                "std": np.std(dwell_times),
                "median": np.median(dwell_times),
                "min": np.min(dwell_times),
                "max": np.max(dwell_times),
                "q25": np.percentile(dwell_times, 25),
                "q75": np.percentile(dwell_times, 75),
                "cv": np.std(dwell_times) / np.mean(dwell_times) if np.mean(dwell_times) > 0 else 0
            }
            
            # Flight time statistics
            flight_stats = {
                "mean": np.mean(flight_times),
                "std": np.std(flight_times),
                "median": np.median(flight_times),
                "min": np.min(flight_times),
                "max": np.max(flight_times),
                "q25": np.percentile(flight_times, 25),
                "q75": np.percentile(flight_times, 75),
                "cv": np.std(flight_times) / np.mean(flight_times) if np.mean(flight_times) > 0 else 0
            }
            
            # Rhythm regularity metrics
            rhythm_regularity = {
                "dwell_consistency": 1 / (1 + dwell_stats["cv"]),  # Higher = more consistent
                "flight_consistency": 1 / (1 + flight_stats["cv"]),
                "overall_rhythm_score": (dwell_stats["cv"] + flight_stats["cv"]) / 2
            }
            
            # Advanced rhythm patterns
            rhythm_patterns = self._detect_rhythm_patterns(dwell_times, flight_times)
            
            return {
                "dwell_time_stats": {k: float(v) for k, v in dwell_stats.items()},
                "flight_time_stats": {k: float(v) for k, v in flight_stats.items()},
                "rhythm_regularity": {k: float(v) for k, v in rhythm_regularity.items()},
                "rhythm_patterns": rhythm_patterns
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating rhythm metrics: {str(e)}")
            return {"error": str(e)}
    
    def detect_typing_anomalies(self, baseline_pattern: Dict[str, Any], current_pattern: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect typing anomalies by comparing current patterns against baseline
        
        Args:
            baseline_pattern: Previously established typing pattern
            current_pattern: Current typing pattern to analyze
            
        Returns:
            Dict containing anomaly detection results
        """
        try:
            if not baseline_pattern or not current_pattern:
                return {"error": "Missing baseline or current pattern data", "anomalies": []}
            
            anomalies = []
            anomaly_scores = {}
            overall_anomaly_score = 0.0
            
            # Compare typing speed
            baseline_speed = baseline_pattern.get("typing_patterns", {}).get("typing_speed_wpm", 0)
            current_speed = current_pattern.get("typing_patterns", {}).get("typing_speed_wpm", 0)
            
            if baseline_speed > 0:
                speed_deviation = abs(current_speed - baseline_speed) / baseline_speed
                if speed_deviation > 0.3:  # 30% deviation threshold
                    anomalies.append({
                        "type": "typing_speed_anomaly",
                        "severity": "high" if speed_deviation > 0.5 else "medium",
                        "description": f"Typing speed deviation: {speed_deviation:.2%}",
                        "baseline_value": baseline_speed,
                        "current_value": current_speed
                    })
                anomaly_scores["typing_speed"] = speed_deviation
            
            # Compare rhythm consistency
            baseline_rhythm = baseline_pattern.get("typing_patterns", {}).get("rhythm_analysis", {})
            current_rhythm = current_pattern.get("typing_patterns", {}).get("rhythm_analysis", {})
            
            rhythm_anomaly_score = self._compare_rhythm_patterns(baseline_rhythm, current_rhythm)
            if rhythm_anomaly_score > self.anomaly_threshold:
                anomalies.append({
                    "type": "rhythm_pattern_anomaly",
                    "severity": "high" if rhythm_anomaly_score > 4.0 else "medium",
                    "description": f"Rhythm pattern deviation score: {rhythm_anomaly_score:.2f}",
                    "anomaly_score": rhythm_anomaly_score
                })
            anomaly_scores["rhythm_pattern"] = rhythm_anomaly_score
            
            # Compare behavioral metrics
            behavioral_anomaly_score = self._compare_behavioral_metrics(baseline_pattern, current_pattern)
            if behavioral_anomaly_score > self.anomaly_threshold:
                anomalies.append({
                    "type": "behavioral_pattern_anomaly",
                    "severity": "high" if behavioral_anomaly_score > 4.0 else "medium",
                    "description": f"Behavioral pattern deviation score: {behavioral_anomaly_score:.2f}",
                    "anomaly_score": behavioral_anomaly_score
                })
            anomaly_scores["behavioral_pattern"] = behavioral_anomaly_score
            
            # Calculate overall anomaly score
            overall_anomaly_score = np.mean(list(anomaly_scores.values()))
            
            # Determine intervention level
            intervention_level = "none"
            if overall_anomaly_score > 4.0:
                intervention_level = "immediate"
            elif overall_anomaly_score > 3.0:
                intervention_level = "high"
            elif overall_anomaly_score > 2.0:
                intervention_level = "medium"
            elif overall_anomaly_score > 1.0:
                intervention_level = "low"
            
            return {
                "anomalies_detected": anomalies,
                "anomaly_scores": anomaly_scores,
                "overall_anomaly_score": float(overall_anomaly_score),
                "intervention_level": intervention_level,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "requires_intervention": len(anomalies) > 0
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting typing anomalies: {str(e)}")
            return {"error": str(e), "anomalies": []}
    
    def generate_biometric_signature(self, keystroke_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate unique biometric signature from keystroke history
        
        Args:
            keystroke_history: Historical keystroke data for signature generation
            
        Returns:
            Dict containing biometric signature and metadata
        """
        try:
            if not keystroke_history or len(keystroke_history) < 50:
                return {"error": "Insufficient keystroke history for signature generation"}
            
            # Aggregate all keystroke patterns
            all_patterns = []
            for session_data in keystroke_history:
                if "typing_patterns" in session_data:
                    all_patterns.append(session_data["typing_patterns"])
            
            if not all_patterns:
                return {"error": "No valid typing patterns found in history"}
            
            # Extract signature features
            signature_features = self._extract_signature_features(all_patterns)
            
            # Create behavioral fingerprint
            fingerprint = self._create_behavioral_fingerprint(signature_features)
            
            # Calculate signature confidence and stability
            confidence_score = self._calculate_signature_confidence(all_patterns)
            
            # Generate unique signature hash
            signature_hash = self._generate_signature_hash(signature_features)
            
            return {
                "biometric_signature": {
                    "signature_hash": signature_hash,
                    "signature_features": signature_features,
                    "behavioral_fingerprint": fingerprint,
                    "confidence_score": float(confidence_score),
                    "generated_from_sessions": len(keystroke_history),
                    "generation_timestamp": datetime.utcnow().isoformat(),
                    "signature_version": "1.0"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error generating biometric signature: {str(e)}")
            return {"error": str(e)}
    
    # Private helper methods
    
    def _analyze_consistency(self, dwell_times: List[float], flight_times: List[float]) -> Dict[str, float]:
        """Analyze typing consistency patterns"""
        try:
            # Calculate coefficient of variation for consistency
            dwell_cv = np.std(dwell_times) / np.mean(dwell_times) if np.mean(dwell_times) > 0 else 0
            flight_cv = np.std(flight_times) / np.mean(flight_times) if np.mean(flight_times) > 0 else 0
            
            # Consistency score (lower CV = higher consistency)
            consistency_score = 1 / (1 + (dwell_cv + flight_cv) / 2)
            
            return {
                "dwell_consistency": float(1 / (1 + dwell_cv)),
                "flight_consistency": float(1 / (1 + flight_cv)),
                "overall_consistency": float(consistency_score)
            }
        except:
            return {"dwell_consistency": 0.5, "flight_consistency": 0.5, "overall_consistency": 0.5}
    
    def _calculate_behavioral_metrics(self, df: pd.DataFrame, dwell_times: List[float], flight_times: List[float]) -> Dict[str, Any]:
        """Calculate advanced behavioral metrics"""
        try:
            # Typing rhythm analysis
            if len(flight_times) > 10:
                rhythm_fft = np.fft.fft(flight_times[:min(len(flight_times), 100)])
                dominant_frequency = np.argmax(np.abs(rhythm_fft[1:len(rhythm_fft)//2])) + 1
            else:
                dominant_frequency = 0
            
            # Keystroke pressure patterns (simulated from timing variations)
            pressure_simulation = np.std(dwell_times) * 100  # Simulated pressure variance
            
            # Error patterns (backspace usage, corrections)
            backspace_count = df[df['key'] == 'Backspace'].shape[0]
            total_keystrokes = df.shape[0]
            error_rate = backspace_count / total_keystrokes if total_keystrokes > 0 else 0
            
            # Pause patterns (long intervals between keystrokes)
            pause_threshold = np.percentile(flight_times, 90) if flight_times else 1.0
            pause_count = len([ft for ft in flight_times if ft > pause_threshold])
            
            return {
                "dominant_rhythm_frequency": float(dominant_frequency),
                "simulated_pressure_variance": float(pressure_simulation),
                "error_rate": float(error_rate),
                "pause_frequency": float(pause_count / len(flight_times) if flight_times else 0),
                "backspace_usage": int(backspace_count)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _detect_rhythm_patterns(self, dwell_times: List[float], flight_times: List[float]) -> Dict[str, Any]:
        """Detect specific rhythm patterns in typing"""
        try:
            # Burst typing detection (periods of rapid typing)
            if flight_times:
                short_intervals = [ft for ft in flight_times if ft < np.percentile(flight_times, 25)]
                burst_pattern_detected = len(short_intervals) > len(flight_times) * 0.3
            else:
                burst_pattern_detected = False
            
            # Hesitation pattern detection (frequent long pauses)
            if flight_times:
                long_intervals = [ft for ft in flight_times if ft > np.percentile(flight_times, 75)]
                hesitation_pattern_detected = len(long_intervals) > len(flight_times) * 0.2
            else:
                hesitation_pattern_detected = False
            
            # Rhythmic typing detection (consistent intervals)
            rhythm_consistency = 1 / (1 + np.std(flight_times)) if flight_times else 0
            rhythmic_typing_detected = rhythm_consistency > 0.7
            
            return {
                "burst_pattern_detected": burst_pattern_detected,
                "hesitation_pattern_detected": hesitation_pattern_detected,
                "rhythmic_typing_detected": rhythmic_typing_detected,
                "rhythm_consistency_score": float(rhythm_consistency)
            }
        except:
            return {"burst_pattern_detected": False, "hesitation_pattern_detected": False, "rhythmic_typing_detected": False}
    
    def _compare_rhythm_patterns(self, baseline: Dict[str, Any], current: Dict[str, Any]) -> float:
        """Compare rhythm patterns and return anomaly score"""
        try:
            if not baseline or not current:
                return 0.0
            
            # Compare dwell time statistics
            baseline_dwell = baseline.get("dwell_time_stats", {})
            current_dwell = current.get("dwell_time_stats", {})
            
            dwell_score = 0.0
            for key in ["mean", "std", "cv"]:
                if key in baseline_dwell and key in current_dwell:
                    if baseline_dwell[key] > 0:
                        deviation = abs(current_dwell[key] - baseline_dwell[key]) / baseline_dwell[key]
                        dwell_score += deviation
            
            # Compare flight time statistics
            baseline_flight = baseline.get("flight_time_stats", {})
            current_flight = current.get("flight_time_stats", {})
            
            flight_score = 0.0
            for key in ["mean", "std", "cv"]:
                if key in baseline_flight and key in current_flight:
                    if baseline_flight[key] > 0:
                        deviation = abs(current_flight[key] - baseline_flight[key]) / baseline_flight[key]
                        flight_score += deviation
            
            return (dwell_score + flight_score) / 2
        except:
            return 0.0
    
    def _compare_behavioral_metrics(self, baseline: Dict[str, Any], current: Dict[str, Any]) -> float:
        """Compare behavioral metrics and return anomaly score"""
        try:
            baseline_behavioral = baseline.get("typing_patterns", {}).get("behavioral_metrics", {})
            current_behavioral = current.get("typing_patterns", {}).get("behavioral_metrics", {})
            
            if not baseline_behavioral or not current_behavioral:
                return 0.0
            
            score = 0.0
            count = 0
            
            for key in ["dominant_rhythm_frequency", "simulated_pressure_variance", "error_rate", "pause_frequency"]:
                if key in baseline_behavioral and key in current_behavioral:
                    baseline_val = baseline_behavioral[key]
                    current_val = current_behavioral[key]
                    
                    if baseline_val > 0:
                        deviation = abs(current_val - baseline_val) / baseline_val
                        score += deviation
                        count += 1
            
            return score / count if count > 0 else 0.0
        except:
            return 0.0
    
    def _extract_signature_features(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract signature features from multiple typing patterns"""
        try:
            # Aggregate rhythm statistics
            all_dwell_means = []
            all_flight_means = []
            all_consistency_scores = []
            all_typing_speeds = []
            
            for pattern in patterns:
                rhythm = pattern.get("rhythm_analysis", {})
                if "dwell_time_stats" in rhythm:
                    all_dwell_means.append(rhythm["dwell_time_stats"].get("mean", 0))
                if "flight_time_stats" in rhythm:
                    all_flight_means.append(rhythm["flight_time_stats"].get("mean", 0))
                
                consistency = pattern.get("consistency_metrics", {})
                all_consistency_scores.append(consistency.get("overall_consistency", 0))
                
                all_typing_speeds.append(pattern.get("typing_speed_wpm", 0))
            
            # Calculate signature features
            return {
                "average_dwell_time": float(np.mean(all_dwell_means)) if all_dwell_means else 0.0,
                "dwell_time_stability": float(1 / (1 + np.std(all_dwell_means))) if all_dwell_means else 0.0,
                "average_flight_time": float(np.mean(all_flight_means)) if all_flight_means else 0.0,
                "flight_time_stability": float(1 / (1 + np.std(all_flight_means))) if all_flight_means else 0.0,
                "consistency_signature": float(np.mean(all_consistency_scores)) if all_consistency_scores else 0.0,
                "typing_speed_signature": float(np.mean(all_typing_speeds)) if all_typing_speeds else 0.0,
                "speed_stability": float(1 / (1 + np.std(all_typing_speeds))) if all_typing_speeds else 0.0
            }
        except:
            return {}
    
    def _create_behavioral_fingerprint(self, features: Dict[str, Any]) -> str:
        """Create behavioral fingerprint from signature features"""
        try:
            # Create feature vector
            feature_vector = [
                features.get("average_dwell_time", 0),
                features.get("dwell_time_stability", 0),
                features.get("average_flight_time", 0),
                features.get("flight_time_stability", 0),
                features.get("consistency_signature", 0),
                features.get("typing_speed_signature", 0),
                features.get("speed_stability", 0)
            ]
            
            # Normalize and quantize features
            normalized_features = [(f - min(feature_vector)) / (max(feature_vector) - min(feature_vector) + 1e-10) for f in feature_vector]
            quantized_features = [int(f * 1000) for f in normalized_features]
            
            # Create fingerprint string
            fingerprint = ''.join([f"{f:03d}" for f in quantized_features])
            return fingerprint
        except:
            return "000000000000000000000"
    
    def _calculate_signature_confidence(self, patterns: List[Dict[str, Any]]) -> float:
        """Calculate confidence score for the generated signature"""
        try:
            if len(patterns) < 3:
                return 0.3  # Low confidence with few samples
            
            # Calculate variability across sessions
            typing_speeds = [p.get("typing_speed_wpm", 0) for p in patterns]
            consistency_scores = [p.get("consistency_metrics", {}).get("overall_consistency", 0) for p in patterns]
            
            speed_cv = np.std(typing_speeds) / np.mean(typing_speeds) if np.mean(typing_speeds) > 0 else 1.0
            consistency_cv = np.std(consistency_scores) / np.mean(consistency_scores) if np.mean(consistency_scores) > 0 else 1.0
            
            # Lower variability = higher confidence
            variability_score = (speed_cv + consistency_cv) / 2
            confidence = 1 / (1 + variability_score)
            
            # Boost confidence with more samples
            sample_boost = min(1.0, len(patterns) / 10)
            
            return min(1.0, confidence * sample_boost)
        except:
            return 0.5
    
    def _generate_signature_hash(self, features: Dict[str, Any]) -> str:
        """Generate unique hash for the signature"""
        try:
            feature_string = json.dumps(features, sort_keys=True)
            return hashlib.sha256(feature_string.encode()).hexdigest()[:16]
        except:
            return str(uuid.uuid4())[:16]


class InteractionBiometricsAnalyzer:
    """
    Advanced mouse movement and interaction pattern analysis
    Analyzes mouse movements, click patterns, scroll behavior, and interaction consistency
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.anomaly_threshold = 2.0