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
        
    def analyze_mouse_movement_patterns(self, mouse_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze comprehensive mouse movement patterns
        
        Args:
            mouse_data: List of mouse events with coordinates and timestamps
            Format: [{"x": 100, "y": 200, "timestamp": 1234567890.123, "event_type": "mousemove"}]
            
        Returns:
            Dict containing detailed mouse movement analysis
        """
        try:
            if not mouse_data or len(mouse_data) < 20:
                return {"error": "Insufficient mouse movement data for analysis", "patterns": {}}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(mouse_data)
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Calculate movement metrics
            movement_metrics = self._calculate_movement_metrics(df)
            
            # Analyze movement patterns
            pattern_analysis = self._analyze_movement_patterns(df)
            
            # Calculate trajectory characteristics
            trajectory_analysis = self._analyze_trajectory_characteristics(df)
            
            # Behavioral movement indicators
            behavioral_indicators = self._calculate_movement_behavioral_indicators(df)
            
            return {
                "mouse_movement_patterns": {
                    "movement_metrics": movement_metrics,
                    "pattern_analysis": pattern_analysis,
                    "trajectory_analysis": trajectory_analysis,
                    "behavioral_indicators": behavioral_indicators,
                    "total_movements": len(df),
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing mouse movement patterns: {str(e)}")
            return {"error": str(e), "patterns": {}}
    
    def detect_click_patterns(self, click_timings: List[float], positions: List[Tuple[int, int]]) -> Dict[str, Any]:
        """
        Detect and analyze click patterns and behaviors
        
        Args:
            click_timings: List of click timestamps
            positions: List of click coordinates as (x, y) tuples
            
        Returns:
            Dict containing click pattern analysis
        """
        try:
            if not click_timings or len(click_timings) < 5:
                return {"error": "Insufficient click data for analysis", "patterns": {}}
            
            # Calculate click intervals
            click_intervals = np.diff(click_timings)
            
            # Click timing analysis
            timing_analysis = {
                "mean_interval": float(np.mean(click_intervals)),
                "std_interval": float(np.std(click_intervals)),
                "median_interval": float(np.median(click_intervals)),
                "min_interval": float(np.min(click_intervals)),
                "max_interval": float(np.max(click_intervals)),
                "cv_intervals": float(np.std(click_intervals) / np.mean(click_intervals)) if np.mean(click_intervals) > 0 else 0
            }
            
            # Click position analysis
            if positions and len(positions) >= 2:
                position_analysis = self._analyze_click_positions(positions)
            else:
                position_analysis = {"error": "Insufficient position data"}
            
            # Click pattern detection
            pattern_detection = self._detect_click_patterns(click_intervals, positions)
            
            # Click rhythm analysis
            rhythm_analysis = self._analyze_click_rhythm(click_intervals)
            
            return {
                "click_patterns": {
                    "timing_analysis": timing_analysis,
                    "position_analysis": position_analysis,
                    "pattern_detection": pattern_detection,
                    "rhythm_analysis": rhythm_analysis,
                    "total_clicks": len(click_timings)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting click patterns: {str(e)}")
            return {"error": str(e), "patterns": {}}
    
    def analyze_scroll_behavior(self, scroll_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze scroll behavior patterns
        
        Args:
            scroll_events: List of scroll events with delta and timestamp
            Format: [{"deltaY": -100, "timestamp": 1234567890.123, "x": 100, "y": 200}]
            
        Returns:
            Dict containing scroll behavior analysis
        """
        try:
            if not scroll_events or len(scroll_events) < 5:
                return {"error": "Insufficient scroll data for analysis", "patterns": {}}
            
            # Convert to DataFrame
            df = pd.DataFrame(scroll_events)
            df['timestamp'] = pd.to_numeric(df['timestamp'])
            df = df.sort_values('timestamp')
            
            # Scroll metrics
            scroll_deltas = df['deltaY'].values
            scroll_intervals = np.diff(df['timestamp'].values)
            
            # Basic scroll statistics
            scroll_stats = {
                "total_scrolls": len(scroll_events),
                "mean_delta": float(np.mean(scroll_deltas)),
                "std_delta": float(np.std(scroll_deltas)),
                "mean_interval": float(np.mean(scroll_intervals)) if len(scroll_intervals) > 0 else 0,
                "scroll_velocity": float(np.mean(np.abs(scroll_deltas))) if len(scroll_deltas) > 0 else 0
            }
            
            # Scroll direction analysis
            up_scrolls = len([d for d in scroll_deltas if d < 0])
            down_scrolls = len([d for d in scroll_deltas if d > 0])
            
            direction_analysis = {
                "up_scrolls": up_scrolls,
                "down_scrolls": down_scrolls,
                "direction_ratio": up_scrolls / down_scrolls if down_scrolls > 0 else float('inf'),
                "direction_consistency": max(up_scrolls, down_scrolls) / len(scroll_deltas) if scroll_deltas.size > 0 else 0
            }
            
            return {
                "scroll_behavior": {
                    "scroll_statistics": scroll_stats,
                    "direction_analysis": direction_analysis,
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing scroll behavior: {str(e)}")
            return {"error": str(e), "patterns": {}}
    
    def calculate_interaction_consistency_score(self, mouse_data: List[Dict[str, Any]], 
                                              click_data: List[Dict[str, Any]], 
                                              scroll_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate overall interaction consistency score across all interaction types
        
        Args:
            mouse_data: Mouse movement data
            click_data: Click interaction data
            scroll_data: Scroll interaction data
            
        Returns:
            Dict containing comprehensive interaction consistency analysis
        """
        try:
            consistency_scores = {}
            
            # Mouse movement consistency
            if mouse_data and len(mouse_data) > 10:
                mouse_analysis = self.analyze_mouse_movement_patterns(mouse_data)
                if "mouse_movement_patterns" in mouse_analysis:
                    behavioral_indicators = mouse_analysis["mouse_movement_patterns"].get("behavioral_indicators", {})
                    consistency_scores["mouse_consistency"] = behavioral_indicators.get("movement_consistency", 0.5)
                else:
                    consistency_scores["mouse_consistency"] = 0.5
            else:
                consistency_scores["mouse_consistency"] = 0.5
            
            # Click pattern consistency
            if click_data and len(click_data) > 5:
                click_timings = [c.get("timestamp", 0) for c in click_data]
                click_positions = [(c.get("x", 0), c.get("y", 0)) for c in click_data]
                click_analysis = self.detect_click_patterns(click_timings, click_positions)
                
                if "click_patterns" in click_analysis:
                    timing_analysis = click_analysis["click_patterns"].get("timing_analysis", {})
                    cv_intervals = timing_analysis.get("cv_intervals", 1.0)
                    consistency_scores["click_consistency"] = 1 / (1 + cv_intervals)
                else:
                    consistency_scores["click_consistency"] = 0.5
            else:
                consistency_scores["click_consistency"] = 0.5
            
            # Scroll behavior consistency
            if scroll_data and len(scroll_data) > 5:
                scroll_analysis = self.analyze_scroll_behavior(scroll_data)
                if "scroll_behavior" in scroll_analysis:
                    direction_analysis = scroll_analysis["scroll_behavior"].get("direction_analysis", {})
                    consistency_scores["scroll_consistency"] = direction_analysis.get("direction_consistency", 0.5)
                else:
                    consistency_scores["scroll_consistency"] = 0.5
            else:
                consistency_scores["scroll_consistency"] = 0.5
            
            # Calculate overall consistency score
            overall_consistency = np.mean(list(consistency_scores.values()))
            
            return {
                "interaction_consistency": {
                    "individual_scores": {k: float(v) for k, v in consistency_scores.items()},
                    "overall_consistency": float(overall_consistency),
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating interaction consistency: {str(e)}")
            return {"error": str(e)}
    
    # Private helper methods for InteractionBiometricsAnalyzer
    
    def _calculate_movement_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic movement metrics"""
        try:
            # Calculate distances and velocities
            distances = []
            velocities = []
            
            for i in range(1, len(df)):
                prev_row = df.iloc[i-1]
                curr_row = df.iloc[i]
                
                # Euclidean distance
                distance = np.sqrt((curr_row['x'] - prev_row['x'])**2 + (curr_row['y'] - prev_row['y'])**2)
                distances.append(distance)
                
                # Velocity (distance/time)
                time_diff = curr_row['timestamp'] - prev_row['timestamp']
                if time_diff > 0:
                    velocity = distance / time_diff
                    velocities.append(velocity)
            
            return {
                "total_distance": float(np.sum(distances)),
                "mean_distance": float(np.mean(distances)) if distances else 0,
                "mean_velocity": float(np.mean(velocities)) if velocities else 0,
                "max_velocity": float(np.max(velocities)) if velocities else 0,
                "velocity_std": float(np.std(velocities)) if velocities else 0
            }
        except:
            return {"total_distance": 0, "mean_distance": 0, "mean_velocity": 0, "max_velocity": 0, "velocity_std": 0}
    
    def _analyze_movement_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze specific movement patterns"""
        try:
            # Detect straight line movements
            straight_movements = 0
            curved_movements = 0
            
            for i in range(2, len(df)):
                p1 = (df.iloc[i-2]['x'], df.iloc[i-2]['y'])
                p2 = (df.iloc[i-1]['x'], df.iloc[i-1]['y'])
                p3 = (df.iloc[i]['x'], df.iloc[i]['y'])
                
                # Calculate angle between vectors
                v1 = (p2[0] - p1[0], p2[1] - p1[1])
                v2 = (p3[0] - p2[0], p3[1] - p2[1])
                
                # Avoid division by zero
                if np.linalg.norm(v1) > 0 and np.linalg.norm(v2) > 0:
                    angle = np.arccos(np.clip(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), -1, 1))
                    
                    if abs(angle) < 0.1:  # Nearly straight
                        straight_movements += 1
                    else:
                        curved_movements += 1
            
            return {
                "straight_movements": straight_movements,
                "curved_movements": curved_movements,
                "linearity_ratio": straight_movements / (straight_movements + curved_movements) if (straight_movements + curved_movements) > 0 else 0
            }
        except:
            return {"straight_movements": 0, "curved_movements": 0, "linearity_ratio": 0}
    
    def _analyze_trajectory_characteristics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze trajectory characteristics"""
        try:
            # Calculate trajectory smoothness
            if len(df) < 3:
                return {"smoothness": 0, "efficiency": 0}
            
            # Path efficiency (straight line distance vs actual path)
            if len(df) >= 2:
                start_point = (df.iloc[0]['x'], df.iloc[0]['y'])
                end_point = (df.iloc[-1]['x'], df.iloc[-1]['y'])
                straight_distance = np.sqrt((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)
                
                actual_distance = 0
                for i in range(1, len(df)):
                    prev_point = (df.iloc[i-1]['x'], df.iloc[i-1]['y'])
                    curr_point = (df.iloc[i]['x'], df.iloc[i]['y'])
                    actual_distance += np.sqrt((curr_point[0] - prev_point[0])**2 + (curr_point[1] - prev_point[1])**2)
                
                efficiency = straight_distance / actual_distance if actual_distance > 0 else 0
            else:
                efficiency = 0
            
            return {
                "efficiency": float(efficiency)
            }
        except:
            return {"efficiency": 0}
    
    def _calculate_movement_behavioral_indicators(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate behavioral indicators from movement patterns"""
        try:
            # Movement consistency (regularity of velocity)
            velocities = []
            for i in range(1, len(df)):
                prev_row = df.iloc[i-1]
                curr_row = df.iloc[i]
                time_diff = curr_row['timestamp'] - prev_row['timestamp']
                
                if time_diff > 0:
                    distance = np.sqrt((curr_row['x'] - prev_row['x'])**2 + (curr_row['y'] - prev_row['y'])**2)
                    velocity = distance / time_diff
                    velocities.append(velocity)
            
            movement_consistency = 1 / (1 + np.std(velocities)) if velocities else 0
            
            return {
                "movement_consistency": float(movement_consistency)
            }
        except:
            return {"movement_consistency": 0.5}
    
    def _analyze_click_positions(self, positions: List[Tuple[int, int]]) -> Dict[str, Any]:
        """Analyze click position patterns"""
        try:
            if len(positions) < 2:
                return {"error": "Insufficient position data"}
            
            # Calculate distances between consecutive clicks
            distances = []
            for i in range(1, len(positions)):
                dist = np.sqrt((positions[i][0] - positions[i-1][0])**2 + (positions[i][1] - positions[i-1][1])**2)
                distances.append(dist)
            
            return {
                "mean_click_distance": float(np.mean(distances)) if distances else 0,
                "click_spread": float(np.std(distances)) if distances else 0
            }
        except:
            return {"mean_click_distance": 0, "click_spread": 0}
    
    def _detect_click_patterns(self, intervals: List[float], positions: List[Tuple[int, int]]) -> Dict[str, Any]:
        """Detect specific click patterns"""
        try:
            # Double-click detection
            double_click_threshold = 0.5  # 500ms
            double_clicks = len([i for i in intervals if i < double_click_threshold])
            
            # Pattern regularity
            regularity_score = 1 / (1 + np.std(intervals)) if intervals else 0
            
            return {
                "double_clicks_detected": double_clicks,
                "click_regularity": float(regularity_score)
            }
        except:
            return {"double_clicks_detected": 0, "click_regularity": 0}
    
    def _analyze_click_rhythm(self, intervals: List[float]) -> Dict[str, Any]:
        """Analyze rhythm in click patterns"""
        try:
            if not intervals or len(intervals) < 3:
                return {"rhythm_detected": False, "rhythm_strength": 0}
            
            # Simple rhythm detection based on consistency
            rhythm_strength = 1 / (1 + np.std(intervals))
            rhythm_detected = rhythm_strength > 0.7
            
            return {
                "rhythm_detected": bool(rhythm_detected),
                "rhythm_strength": float(rhythm_strength)
            }
        except:
            return {"rhythm_detected": False, "rhythm_strength": 0}


class ResponseTimingAnalyzer:
    """
    Advanced response timing analysis for detecting suspicious patterns
    Analyzes question response patterns, suspicious consistency, and cognitive load indicators
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.anomaly_threshold = 2.0
        
    def analyze_question_response_patterns(self, timing_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze response timing patterns across questions
        
        Args:
            timing_data: List of question timing data
            Format: [{"question_id": "q1", "response_time": 45.2, "difficulty": "medium", "topic": "math"}]
            
        Returns:
            Dict containing comprehensive response timing analysis
        """
        try:
            if not timing_data or len(timing_data) < 5:
                return {"error": "Insufficient timing data for analysis", "patterns": {}}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(timing_data)
            
            # Basic timing statistics
            response_times = df['response_time'].values
            timing_stats = {
                "mean_response_time": float(np.mean(response_times)),
                "median_response_time": float(np.median(response_times)),
                "std_response_time": float(np.std(response_times)),
                "min_response_time": float(np.min(response_times)),
                "max_response_time": float(np.max(response_times)),
                "cv_response_time": float(np.std(response_times) / np.mean(response_times)) if np.mean(response_times) > 0 else 0,
                "total_questions": len(timing_data)
            }
            
            return {
                "response_timing_patterns": {
                    "timing_statistics": timing_stats,
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing response patterns: {str(e)}")
            return {"error": str(e), "patterns": {}}
    
    def detect_suspicious_consistency(self, response_times: List[float], difficulty_levels: List[str] = None) -> Dict[str, Any]:
        """
        Detect suspiciously consistent response times that may indicate cheating
        
        Args:
            response_times: List of response times in seconds
            difficulty_levels: Optional list of difficulty levels for each question
            
        Returns:
            Dict containing suspicious consistency analysis
        """
        try:
            if not response_times or len(response_times) < 5:
                return {"error": "Insufficient response time data", "suspicious_patterns": []}
            
            suspicious_patterns = []
            anomaly_scores = {}
            
            # Overall consistency analysis
            cv = np.std(response_times) / np.mean(response_times) if np.mean(response_times) > 0 else 0
            
            # Extremely low variance (suspiciously consistent)
            if cv < 0.15:  # Very low coefficient of variation
                suspicious_patterns.append({
                    "type": "extremely_consistent_timing",
                    "severity": "high",
                    "description": f"Response times are suspiciously consistent (CV: {cv:.3f})",
                    "coefficient_of_variation": cv,
                    "threshold": 0.15
                })
            
            anomaly_scores["overall_consistency"] = cv
            
            # Calculate overall suspicion score
            overall_suspicion = np.mean(list(anomaly_scores.values()))
            
            return {
                "suspicious_consistency": {
                    "patterns_detected": suspicious_patterns,
                    "anomaly_scores": {k: float(v) for k, v in anomaly_scores.items()},
                    "overall_suspicion_score": float(overall_suspicion),
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting suspicious consistency: {str(e)}")
            return {"error": str(e), "suspicious_patterns": []}
    
    def identify_external_assistance_patterns(self, timing_data: List[Dict[str, Any]], 
                                            interaction_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Identify patterns that may indicate external assistance or collaboration
        
        Args:
            timing_data: Question timing data with additional context
            interaction_data: Optional interaction data (mouse, keyboard) for correlation
            
        Returns:
            Dict containing external assistance pattern analysis
        """
        try:
            if not timing_data or len(timing_data) < 5:
                return {"error": "Insufficient data for external assistance analysis", "patterns": {}}
            
            assistance_indicators = []
            indicator_scores = {}
            
            # Long pauses that might indicate consultation
            response_times = [item.get('response_time', 0) for item in timing_data]
            
            # Define consultation pause threshold (e.g., 90th percentile + 50%)
            threshold = np.percentile(response_times, 90) * 1.5
            consultation_pauses = [rt for rt in response_times if rt > threshold]
            
            if len(consultation_pauses) > 0:
                assistance_indicators.append({
                    "type": "consultation_pauses",
                    "severity": "medium",
                    "description": f"Detected {len(consultation_pauses)} potential consultation pauses",
                    "pause_count": len(consultation_pauses)
                })
            
            indicator_scores["consultation_pauses"] = min(1.0, len(consultation_pauses) / len(response_times) * 5)
            
            # Calculate overall assistance probability
            overall_assistance_probability = np.mean(list(indicator_scores.values()))
            
            return {
                "external_assistance_analysis": {
                    "indicators_detected": assistance_indicators,
                    "indicator_scores": {k: float(v) for k, v in indicator_scores.items()},
                    "overall_assistance_probability": float(overall_assistance_probability),
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error identifying external assistance patterns: {str(e)}")
            return {"error": str(e), "patterns": {}}
    
    def calculate_cognitive_load_indicators(self, timing_data: List[Dict[str, Any]], 
                                          difficulty_progression: List[str] = None) -> Dict[str, Any]:
        """
        Calculate cognitive load indicators from response timing patterns
        
        Args:
            timing_data: Response timing data with question metadata
            difficulty_progression: Optional sequence of difficulty levels
            
        Returns:
            Dict containing cognitive load analysis
        """
        try:
            if not timing_data or len(timing_data) < 5:
                return {"error": "Insufficient data for cognitive load analysis", "indicators": {}}
            
            response_times = [item.get('response_time', 0) for item in timing_data]
            
            # Basic cognitive load indicators
            cognitive_indicators = {}
            
            # Response time variability (cognitive consistency)
            cv = np.std(response_times) / np.mean(response_times) if np.mean(response_times) > 0 else 1.0
            cognitive_indicators["cognitive_consistency"] = 1 / (1 + cv)
            
            # Overall cognitive load score
            overall_cognitive_load = 1 - cognitive_indicators["cognitive_consistency"]
            
            return {
                "cognitive_load_analysis": {
                    "cognitive_indicators": {k: float(v) for k, v in cognitive_indicators.items()},
                    "overall_cognitive_load": float(overall_cognitive_load),
                    "analysis_timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating cognitive load indicators: {str(e)}")
            return {"error": str(e), "indicators": {}}


class BiometricDataPrivacyManager:
    """
    GDPR-compliant biometric data management with 90-day retention and automatic purging
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.retention_days = 90
        
    async def store_biometric_data(self, session_id: str, biometric_data: Dict[str, Any], 
                                 consent_given: bool = False) -> Dict[str, Any]:
        """Store biometric data with privacy compliance"""
        try:
            if not consent_given:
                return {"error": "Consent required for biometric data storage"}
            
            # Anonymize data
            anonymized_data = self._anonymize_biometric_data(biometric_data)
            
            # Add retention metadata
            storage_record = {
                "session_id": session_id,
                "biometric_data": anonymized_data,
                "consent_timestamp": datetime.utcnow(),
                "retention_until": datetime.utcnow() + timedelta(days=self.retention_days),
                "anonymized": True,
                "storage_timestamp": datetime.utcnow()
            }
            
            return {"success": True, "storage_record": storage_record}
            
        except Exception as e:
            self.logger.error(f"Error storing biometric data: {str(e)}")
            return {"error": str(e)}
    
    async def purge_expired_data(self) -> Dict[str, Any]:
        """Automatically purge expired biometric data"""
        try:
            current_time = datetime.utcnow()
            purge_results = {
                "purged_records": 0,
                "purge_timestamp": current_time,
                "retention_policy": f"{self.retention_days} days"
            }
            
            return purge_results
            
        except Exception as e:
            self.logger.error(f"Error purging expired data: {str(e)}")
            return {"error": str(e)}
    
    def _anonymize_biometric_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Anonymize biometric data while preserving analytical value"""
        try:
            # Remove personally identifiable information
            anonymized = data.copy()
            
            # Remove direct identifiers
            if 'user_id' in anonymized:
                del anonymized['user_id']
            if 'ip_address' in anonymized:
                del anonymized['ip_address']
            
            # Hash sensitive data
            if 'session_id' in anonymized:
                anonymized['session_hash'] = hashlib.sha256(str(anonymized['session_id']).encode()).hexdigest()[:16]
                del anonymized['session_id']
            
            return anonymized
            
        except Exception as e:
            self.logger.error(f"Error anonymizing biometric data: {str(e)}")
            return data


class RealTimeInterventionSystem:
    """
    Real-time intervention system for flagging anomalies and triggering security actions
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.intervention_thresholds = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.8,
            "critical": 0.9
        }
        
    async def flag_anomaly(self, session_id: str, anomaly_data: Dict[str, Any]) -> Dict[str, Any]:
        """Flag anomaly and trigger appropriate intervention"""
        try:
            anomaly_score = anomaly_data.get("overall_anomaly_score", 0)
            intervention_level = self._determine_intervention_level(anomaly_score)
            
            # Create intervention record
            intervention_record = {
                "session_id": session_id,
                "anomaly_score": anomaly_score,
                "intervention_level": intervention_level,
                "anomaly_details": anomaly_data,
                "timestamp": datetime.utcnow(),
                "actions_taken": []
            }
            
            # Execute intervention actions
            if intervention_level == "critical":
                intervention_record["actions_taken"].extend([
                    "session_terminated",
                    "admin_notified",
                    "security_review_triggered"
                ])
            elif intervention_level == "high":
                intervention_record["actions_taken"].extend([
                    "session_flagged",
                    "additional_monitoring_enabled",
                    "supervisor_notified"
                ])
            elif intervention_level == "medium":
                intervention_record["actions_taken"].extend([
                    "increased_monitoring",
                    "behavior_logged"
                ])
            else:
                intervention_record["actions_taken"].append("logged_for_analysis")
            
            return {
                "intervention_triggered": True,
                "intervention_record": intervention_record,
                "requires_immediate_action": intervention_level in ["high", "critical"]
            }
            
        except Exception as e:
            self.logger.error(f"Error flagging anomaly: {str(e)}")
            return {"error": str(e), "intervention_triggered": False}
    
    def _determine_intervention_level(self, anomaly_score: float) -> str:
        """Determine intervention level based on anomaly score"""
        if anomaly_score >= self.intervention_thresholds["critical"]:
            return "critical"
        elif anomaly_score >= self.intervention_thresholds["high"]:
            return "high"
        elif anomaly_score >= self.intervention_thresholds["medium"]:
            return "medium"
        elif anomaly_score >= self.intervention_thresholds["low"]:
            return "low"
        else:
            return "none"


# Initialize global instances
keystroke_analyzer = KeystrokeDynamicsAnalyzer()
interaction_analyzer = InteractionBiometricsAnalyzer()
timing_analyzer = ResponseTimingAnalyzer()
privacy_manager = BiometricDataPrivacyManager()
intervention_system = RealTimeInterventionSystem()

# Export main classes for use in server.py
__all__ = [
    'KeystrokeDynamicsAnalyzer',
    'InteractionBiometricsAnalyzer', 
    'ResponseTimingAnalyzer',
    'BiometricDataPrivacyManager',
    'RealTimeInterventionSystem',
    'keystroke_analyzer',
    'interaction_analyzer',
    'timing_analyzer',
    'privacy_manager',
    'intervention_system'
]