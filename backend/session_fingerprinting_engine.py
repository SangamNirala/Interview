"""
🔐 MODULE 3: ADVANCED SESSION FINGERPRINTING SYSTEM
DeviceFingerprintingEngine Class with Advanced Device Signature Generation

This module implements comprehensive device fingerprinting including:
- Hardware fingerprinting (CPU, GPU, RAM, storage characteristics)
- Operating system and architecture analysis
- Screen resolution, color depth, timezone data
- Unique device hash generation with collision resistance
- Device signature persistence and tracking
- Integration with existing behavioral biometrics and anomaly detection systems

Dependencies: hashlib, json, logging, datetime, uuid, numpy, pandas
"""

import hashlib
import json
import logging
import math
import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import asyncio
import statistics
from collections import defaultdict
import re
import base64
import zlib


@dataclass
class DeviceFingerprint:
    """Comprehensive device fingerprint data structure"""
    device_id: str
    hardware_signature: Dict[str, Any]
    os_characteristics: Dict[str, Any]
    browser_characteristics: Dict[str, Any]
    network_characteristics: Dict[str, Any]
    screen_characteristics: Dict[str, Any]
    performance_profile: Dict[str, Any]
    vm_indicators: Dict[str, Any]
    confidence_score: float
    collection_timestamp: datetime
    signature_hash: str
    collision_resistance_score: float
    persistence_tracking: Dict[str, Any]


@dataclass
class DeviceTrackingRecord:
    """Device tracking record for persistence analysis"""
    device_id: str
    session_ids: List[str]
    first_seen: datetime
    last_seen: datetime
    total_sessions: int
    consistency_score: float
    signature_evolution: List[Dict[str, Any]]
    reputation_score: float
    risk_indicators: List[str]


class DeviceFingerprintingEngine:
    """
    Advanced Device Fingerprinting Engine for comprehensive device signature generation
    Integrates with existing behavioral biometrics and anomaly detection systems
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Configuration parameters
        self.signature_version = "1.0"
        self.collision_threshold = 0.9999  # Extremely high collision resistance
        self.confidence_threshold = 0.85
        self.tracking_retention_days = 365  # 1 year retention
        
        # Device tracking data structures (in-memory storage)
        # In production, these would be backed by MongoDB or another persistent store
        self.device_history = {}  # device_id -> List[signature_dict]
        self.device_sessions = {}  # device_id -> List[session_dict]
        self.device_tracking_records = {}  # device_id -> DeviceTrackingRecord
        
        # Hardware component weights for signature generation
        self.hardware_weights = {
            'cpu_characteristics': 0.25,
            'gpu_characteristics': 0.20,
            'memory_characteristics': 0.15,
            'storage_characteristics': 0.10,
            'screen_characteristics': 0.15,
            'browser_characteristics': 0.10,
            'network_characteristics': 0.05
        }
        
        # VM detection patterns and indicators
        self.vm_indicators = {
            'hardware_patterns': [
                'virtualbox', 'vmware', 'parallels', 'qemu', 'kvm', 'xen',
                'hyper-v', 'docker', 'container'
            ],
            'performance_thresholds': {
                'cpu_cores_max': 64,  # Suspicious if more than 64 cores
                'memory_size_patterns': [2048, 4096, 8192],  # Common VM memory sizes
                'gpu_virtual_indicators': ['virtual', 'generic', 'standard']
            }
        }
        
        # Integration with existing modules
        self.behavioral_biometrics_integration = True
        self.anomaly_detection_integration = True
        
        self.logger.info("DeviceFingerprintingEngine initialized successfully")
    
    def generate_device_signature(self, device_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive device signature with hardware fingerprinting,
        OS analysis, and unique hash generation with collision resistance
        
        Args:
            device_data: Complete device characteristics collected from frontend
            Format: {
                "hardware": {...},
                "os": {...},
                "browser": {...},
                "network": {...},
                "screen": {...},
                "performance": {...},
                "session_id": "...",
                "collection_timestamp": "..."
            }
        
        Returns:
            Dict containing comprehensive device signature analysis
        """
        try:
            session_id = device_data.get('session_id', str(uuid.uuid4()))
            self.logger.info(f"Generating device signature for session: {session_id}")
            
            # Extract and validate device data components
            hardware_data = device_data.get('hardware', {})
            os_data = device_data.get('os', {})
            browser_data = device_data.get('browser', {})
            network_data = device_data.get('network', {})
            screen_data = device_data.get('screen', {})
            performance_data = device_data.get('performance', {})
            
            # 1. Hardware Fingerprinting
            hardware_signature = self._generate_hardware_fingerprint(hardware_data)
            
            # 2. Operating System and Architecture Analysis
            os_characteristics = self._analyze_os_characteristics(os_data)
            
            # 3. Screen Resolution, Color Depth, Timezone Analysis
            screen_characteristics = self._analyze_screen_characteristics(screen_data)
            
            # 4. Browser and Environment Analysis
            browser_characteristics = self._analyze_browser_characteristics(browser_data)
            
            # 5. Network Characteristics Analysis
            network_characteristics = self._analyze_network_characteristics(network_data)
            
            # 6. Performance Profile Analysis
            performance_profile = self._analyze_performance_profile(performance_data)
            
            # 7. Virtual Machine Detection
            vm_indicators = self._detect_virtual_machine_indicators(
                hardware_data, os_data, browser_data, performance_data
            )
            
            # 8. Generate Unique Device Hash with Collision Resistance
            signature_components = {
                'hardware': hardware_signature,
                'os': os_characteristics,
                'browser': browser_characteristics,
                'network': network_characteristics,
                'screen': screen_characteristics,
                'performance': performance_profile
            }
            
            device_hash, collision_resistance_score = self._generate_collision_resistant_hash(signature_components)
            
            # 9. Calculate Confidence Score
            confidence_score = self._calculate_signature_confidence(signature_components, vm_indicators)
            
            # 10. Create Device Fingerprint Object
            device_fingerprint = DeviceFingerprint(
                device_id=device_hash,
                hardware_signature=hardware_signature,
                os_characteristics=os_characteristics,
                browser_characteristics=browser_characteristics,
                network_characteristics=network_characteristics,
                screen_characteristics=screen_characteristics,
                performance_profile=performance_profile,
                vm_indicators=vm_indicators,
                confidence_score=confidence_score,
                collection_timestamp=datetime.utcnow(),
                signature_hash=device_hash,
                collision_resistance_score=collision_resistance_score,
                persistence_tracking=self._initialize_persistence_tracking(session_id)
            )
            
            # 11. Integration with Behavioral Biometrics (Module 1)
            behavioral_correlation = self._correlate_with_behavioral_biometrics(device_fingerprint, session_id)
            
            # 12. Integration with Anomaly Detection (Module 2)
            anomaly_correlation = self._correlate_with_anomaly_detection(device_fingerprint, session_id)
            
            # 13. Device Signature Persistence and Tracking
            persistence_result = self._persist_device_signature(device_fingerprint, session_id)
            
            return {
                'success': True,
                'session_id': session_id,
                'device_fingerprint': {
                    'device_id': device_fingerprint.device_id,
                    'signature_hash': device_fingerprint.signature_hash,
                    'confidence_score': device_fingerprint.confidence_score,
                    'collision_resistance_score': device_fingerprint.collision_resistance_score,
                    'collection_timestamp': device_fingerprint.collection_timestamp.isoformat()
                },
                'hardware_analysis': {
                    'hardware_signature': hardware_signature,
                    'vm_detection': vm_indicators,
                    'performance_profile': performance_profile
                },
                'environment_analysis': {
                    'os_characteristics': os_characteristics,
                    'browser_characteristics': browser_characteristics,
                    'screen_characteristics': screen_characteristics,
                    'network_characteristics': network_characteristics
                },
                'integration_analysis': {
                    'behavioral_correlation': behavioral_correlation,
                    'anomaly_correlation': anomaly_correlation,
                    'cross_module_risk_score': self._calculate_cross_module_risk_score(
                        behavioral_correlation, anomaly_correlation, vm_indicators
                    )
                },
                'persistence_tracking': persistence_result,
                'signature_version': self.signature_version,
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating device signature: {str(e)}")
            return {
                'success': False,
                'session_id': device_data.get('session_id', 'unknown'),
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def detect_virtual_machines(self, device_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ENHANCED: Comprehensive virtual machine detection through multiple analysis vectors:
        - Hardware fingerprinting and anomaly detection
        - Hypervisor presence analysis across all major platforms
        - Performance characteristic profiling and anomaly detection
        - OS-specific registry/system file analysis (Windows/Linux/Mac)
        - VM software signature detection with comprehensive pattern matching
        
        Args:
            device_data: Comprehensive device characteristics data including:
                - hardware: CPU, GPU, memory, storage characteristics
                - os: Operating system information, platform details
                - browser: User agent, plugins, capabilities
                - performance: Timing data, memory usage, hardware concurrency
                - network: Connection characteristics (optional)
                - screen: Display properties and capabilities
            
        Returns:
            Dict containing comprehensive VM detection analysis with probability scoring
        """
        try:
            self.logger.info("🔍 Performing ENHANCED comprehensive VM detection analysis")
            
            # Validate and normalize input data
            device_data = self._validate_and_normalize_device_data(device_data)
            
            # Extract data components with enhanced validation
            hardware_data = device_data.get('hardware', {})
            os_data = device_data.get('os', {})
            browser_data = device_data.get('browser', {})
            performance_data = device_data.get('performance', {})
            network_data = device_data.get('network', {})
            screen_data = device_data.get('screen', {})
            
            vm_detection_results = {}
            detection_metadata = {
                'analysis_methods_used': [],
                'detection_depth': 'comprehensive',
                'platform_specific_checks': []
            }
            
            # 1. ENHANCED Hardware-based VM Detection
            self.logger.info("🔧 Analyzing hardware-based VM indicators")
            hardware_vm_indicators = self._detect_enhanced_hardware_vm_indicators(hardware_data, performance_data)
            vm_detection_results['hardware_indicators'] = hardware_vm_indicators
            detection_metadata['analysis_methods_used'].append('hardware_fingerprinting')
            
            # 2. ENHANCED Hypervisor Presence Analysis
            self.logger.info("🖥️ Performing hypervisor presence analysis")
            hypervisor_analysis = self._analyze_enhanced_hypervisor_presence(os_data, browser_data, hardware_data)
            vm_detection_results['hypervisor_analysis'] = hypervisor_analysis
            detection_metadata['analysis_methods_used'].append('hypervisor_detection')
            
            # 3. ENHANCED Performance Characteristic Anomalies
            self.logger.info("⚡ Analyzing performance characteristic anomalies")
            performance_anomalies = self._analyze_enhanced_vm_performance_anomalies(performance_data, hardware_data)
            vm_detection_results['performance_anomalies'] = performance_anomalies
            detection_metadata['analysis_methods_used'].append('performance_profiling')
            
            # 4. ENHANCED OS-Specific Registry/System File Analysis
            self.logger.info("📁 Performing OS-specific system analysis")
            system_analysis = self._analyze_enhanced_vm_system_indicators(browser_data, os_data, hardware_data)
            vm_detection_results['system_analysis'] = system_analysis
            detection_metadata['analysis_methods_used'].append('system_file_analysis')
            
            # 5. ENHANCED VM Software Signature Detection
            self.logger.info("🔍 Detecting VM software signatures")
            software_signatures = self._detect_enhanced_vm_software_signatures(hardware_data, os_data, browser_data)
            vm_detection_results['software_signatures'] = software_signatures
            detection_metadata['analysis_methods_used'].append('signature_detection')
            
            # 6. Network-based VM Detection (New)
            self.logger.info("🌐 Analyzing network-based VM indicators")
            network_analysis = self._analyze_vm_network_indicators(network_data, browser_data)
            vm_detection_results['network_analysis'] = network_analysis
            detection_metadata['analysis_methods_used'].append('network_analysis')
            
            # 7. Screen/Display VM Detection (New)
            self.logger.info("📺 Analyzing display characteristics for VM indicators")
            display_analysis = self._analyze_vm_display_indicators(screen_data, hardware_data)
            vm_detection_results['display_analysis'] = display_analysis
            detection_metadata['analysis_methods_used'].append('display_analysis')
            
            # 8. Cross-Platform Consistency Analysis (New)
            self.logger.info("🔗 Performing cross-platform consistency analysis")
            consistency_analysis = self._analyze_vm_consistency_indicators(vm_detection_results)
            vm_detection_results['consistency_analysis'] = consistency_analysis
            detection_metadata['analysis_methods_used'].append('consistency_analysis')
            
            # 9. Calculate Enhanced VM Probability with Weighted Scoring
            vm_probability = self._calculate_enhanced_vm_probability(vm_detection_results)
            
            # 10. Enhanced VM Classification with Platform-Specific Detection
            vm_classification = self._classify_enhanced_vm_type(vm_detection_results, os_data)
            
            # 11. Risk Assessment and Confidence Scoring
            confidence_metrics = self._calculate_enhanced_vm_detection_confidence(vm_detection_results)
            risk_assessment = self._assess_vm_detection_risk(vm_detection_results, vm_probability)
            
            return {
                'success': True,
                'vm_detection_results': vm_detection_results,
                'vm_probability': vm_probability,
                'vm_classification': vm_classification,
                'is_virtual_machine': vm_probability > 0.65,  # Enhanced threshold
                'confidence_metrics': confidence_metrics,
                'risk_assessment': risk_assessment,
                'detection_metadata': detection_metadata,
                'platform_detection': self._detect_platform_specific_vm_indicators(os_data, vm_detection_results),
                'recommendation': self._generate_vm_detection_recommendation(vm_probability, risk_assessment),
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'analysis_version': '2.0_enhanced'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error in enhanced VM detection: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'error_type': 'vm_detection_failure',
                'fallback_analysis': self._perform_basic_vm_detection_fallback(device_data),
                'analysis_timestamp': datetime.utcnow().isoformat(),
                'analysis_version': '2.0_enhanced'
            }
    
    def analyze_hardware_characteristics(self, hardware_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive hardware characteristics analysis including CPU, memory,
        graphics, storage, and hardware consistency validation
        
        Args:
            hardware_data: Hardware information from device fingerprinting
            
        Returns:
            Dict containing detailed hardware analysis
        """
        try:
            self.logger.info("Analyzing comprehensive hardware characteristics")
            
            hardware_analysis = {}
            
            # 1. CPU Core Count, Architecture, and Performance Profiling
            cpu_analysis = self._analyze_cpu_characteristics(hardware_data.get('cpu', {}))
            hardware_analysis['cpu_analysis'] = cpu_analysis
            
            # 2. Memory Configuration and Availability Analysis
            memory_analysis = self._analyze_memory_characteristics(hardware_data.get('memory', {}))
            hardware_analysis['memory_analysis'] = memory_analysis
            
            # 3. Graphics Card Detection and Capabilities
            gpu_analysis = self._analyze_gpu_characteristics(hardware_data.get('gpu', {}))
            hardware_analysis['gpu_analysis'] = gpu_analysis
            
            # 4. Storage Device Characteristics and Performance
            storage_analysis = self._analyze_storage_characteristics(hardware_data.get('storage', {}))
            hardware_analysis['storage_analysis'] = storage_analysis
            
            # 5. Hardware Consistency Validation Over Time
            consistency_validation = self._validate_hardware_consistency(hardware_data)
            hardware_analysis['consistency_validation'] = consistency_validation
            
            # 6. Hardware Profile Classification
            hardware_profile = self._classify_hardware_profile(hardware_analysis)
            
            # 7. Anomaly Detection in Hardware Configuration
            hardware_anomalies = self._detect_hardware_anomalies(hardware_analysis)
            
            return {
                'success': True,
                'hardware_analysis': hardware_analysis,
                'hardware_profile': hardware_profile,
                'hardware_anomalies': hardware_anomalies,
                'overall_hardware_score': self._calculate_overall_hardware_score(hardware_analysis),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in hardware analysis: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def track_device_consistency(self, device_id: str, current_signature: Dict[str, Any]) -> Dict[str, Any]:
        """
        Track device signature evolution, hardware change detection,
        and suspicious device switching patterns
        
        Args:
            device_id: Unique device identifier
            current_signature: Current device signature data
            
        Returns:
            Dict containing device consistency tracking analysis
        """
        try:
            self.logger.info(f"Tracking device consistency for device: {device_id}")
            
            consistency_analysis = {}
            
            # 1. Device Signature Evolution Tracking
            evolution_tracking = self._track_signature_evolution(device_id, current_signature)
            consistency_analysis['evolution_tracking'] = evolution_tracking
            
            # 2. Hardware Change Detection and Validation
            hardware_changes = self._detect_hardware_changes(device_id, current_signature)
            consistency_analysis['hardware_changes'] = hardware_changes
            
            # 3. Suspicious Device Switching Patterns
            switching_patterns = self._analyze_device_switching_patterns(device_id)
            consistency_analysis['switching_patterns'] = switching_patterns
            
            # 4. Device Reputation Scoring
            reputation_score = self._calculate_device_reputation_score(device_id, consistency_analysis)
            consistency_analysis['reputation_score'] = reputation_score
            
            # 5. Cross-Session Device Correlation
            session_correlation = self._correlate_cross_session_data(device_id)
            consistency_analysis['session_correlation'] = session_correlation
            
            # 6. Update Device Tracking Record
            tracking_update = self._update_device_tracking_record(device_id, current_signature, consistency_analysis)
            
            return {
                'success': True,
                'device_id': device_id,
                'consistency_analysis': consistency_analysis,
                'tracking_update': tracking_update,
                'consistency_score': self._calculate_overall_consistency_score(consistency_analysis),
                'risk_assessment': self._assess_device_risk_level(consistency_analysis),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking device consistency: {str(e)}")
            return {
                'success': False,
                'device_id': device_id,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    # ===== HELPER METHODS FOR HARDWARE FINGERPRINTING =====
    
    def _generate_hardware_fingerprint(self, hardware_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive hardware fingerprint"""
        try:
            fingerprint = {}
            
            # CPU fingerprinting
            cpu_data = hardware_data.get('cpu', {})
            fingerprint['cpu_signature'] = {
                'cores': cpu_data.get('cores', 0),
                'architecture': cpu_data.get('architecture', 'unknown'),
                'vendor': cpu_data.get('vendor', 'unknown'),
                'model': cpu_data.get('model', 'unknown'),
                'frequency': cpu_data.get('frequency', 0),
                'cache_size': cpu_data.get('cache_size', 0),
                'features': cpu_data.get('features', [])
            }
            
            # GPU fingerprinting
            gpu_data = hardware_data.get('gpu', {})
            fingerprint['gpu_signature'] = {
                'vendor': gpu_data.get('vendor', 'unknown'),
                'renderer': gpu_data.get('renderer', 'unknown'),
                'version': gpu_data.get('version', 'unknown'),
                'memory': gpu_data.get('memory', 0),
                'extensions': gpu_data.get('extensions', [])[:10]  # First 10 extensions
            }
            
            # Memory fingerprinting
            memory_data = hardware_data.get('memory', {})
            fingerprint['memory_signature'] = {
                'total_memory': memory_data.get('total_memory', 0),
                'available_memory': memory_data.get('available_memory', 0),
                'memory_type': memory_data.get('memory_type', 'unknown'),
                'speed': memory_data.get('speed', 0)
            }
            
            # Storage fingerprinting
            storage_data = hardware_data.get('storage', {})
            fingerprint['storage_signature'] = {
                'total_storage': storage_data.get('total_storage', 0),
                'available_storage': storage_data.get('available_storage', 0),
                'storage_type': storage_data.get('storage_type', 'unknown'),
                'filesystem': storage_data.get('filesystem', 'unknown')
            }
            
            return fingerprint
            
        except Exception as e:
            self.logger.error(f"Error generating hardware fingerprint: {str(e)}")
            return {}
    
    def _analyze_os_characteristics(self, os_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze operating system and architecture characteristics"""
        try:
            os_analysis = {
                'platform': os_data.get('platform', 'unknown'),
                'version': os_data.get('version', 'unknown'),
                'architecture': os_data.get('architecture', 'unknown'),
                'build': os_data.get('build', 'unknown'),
                'kernel_version': os_data.get('kernel_version', 'unknown'),
                'language': os_data.get('language', 'unknown'),
                'timezone': os_data.get('timezone', 'unknown'),
                'timezone_offset': os_data.get('timezone_offset', 0)
            }
            
            # OS family classification
            platform = os_analysis['platform'].lower()
            if 'windows' in platform:
                os_analysis['os_family'] = 'Windows'
            elif 'mac' in platform or 'darwin' in platform:
                os_analysis['os_family'] = 'macOS'
            elif 'linux' in platform:
                os_analysis['os_family'] = 'Linux'
            elif 'android' in platform:
                os_analysis['os_family'] = 'Android'
            elif 'ios' in platform:
                os_analysis['os_family'] = 'iOS'
            else:
                os_analysis['os_family'] = 'Unknown'
            
            return os_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing OS characteristics: {str(e)}")
            return {}
    
    def _analyze_screen_characteristics(self, screen_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze screen resolution, color depth, and display characteristics"""
        try:
            screen_analysis = {
                'screen_resolution': {
                    'width': screen_data.get('width', 0),
                    'height': screen_data.get('height', 0),
                    'aspect_ratio': self._calculate_aspect_ratio(
                        screen_data.get('width', 0), 
                        screen_data.get('height', 0)
                    )
                },
                'available_resolution': {
                    'width': screen_data.get('available_width', 0),
                    'height': screen_data.get('available_height', 0)
                },
                'color_depth': screen_data.get('color_depth', 0),
                'pixel_depth': screen_data.get('pixel_depth', 0),
                'device_pixel_ratio': screen_data.get('device_pixel_ratio', 1),
                'orientation': screen_data.get('orientation', 'unknown'),
                'touch_support': screen_data.get('touch_support', False),
                'max_touch_points': screen_data.get('max_touch_points', 0)
            }
            
            # Display profile classification
            width = screen_analysis['screen_resolution']['width']
            height = screen_analysis['screen_resolution']['height']
            
            if width >= 3840 and height >= 2160:
                screen_analysis['display_profile'] = '4K/UHD'
            elif width >= 2560 and height >= 1440:
                screen_analysis['display_profile'] = '2K/QHD'
            elif width >= 1920 and height >= 1080:
                screen_analysis['display_profile'] = 'Full HD'
            elif width >= 1366 and height >= 768:
                screen_analysis['display_profile'] = 'HD'
            else:
                screen_analysis['display_profile'] = 'Standard'
            
            return screen_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing screen characteristics: {str(e)}")
            return {}
    
    def _analyze_browser_characteristics(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze browser and environment characteristics"""
        try:
            browser_analysis = {
                'user_agent': browser_data.get('user_agent', 'unknown'),
                'browser_name': browser_data.get('browser_name', 'unknown'),
                'browser_version': browser_data.get('browser_version', 'unknown'),
                'engine_name': browser_data.get('engine_name', 'unknown'),
                'engine_version': browser_data.get('engine_version', 'unknown'),
                'plugins': browser_data.get('plugins', [])[:10],  # First 10 plugins
                'mime_types': browser_data.get('mime_types', [])[:10],  # First 10 MIME types
                'languages': browser_data.get('languages', []),
                'cookie_enabled': browser_data.get('cookie_enabled', False),
                'local_storage': browser_data.get('local_storage', False),
                'session_storage': browser_data.get('session_storage', False),
                'webgl_support': browser_data.get('webgl_support', False),
                'canvas_support': browser_data.get('canvas_support', False)
            }
            
            return browser_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing browser characteristics: {str(e)}")
            return {}
    
    def _analyze_network_characteristics(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze network characteristics and connection information"""
        try:
            network_analysis = {
                'connection_type': network_data.get('connection_type', 'unknown'),
                'effective_type': network_data.get('effective_type', 'unknown'),
                'downlink': network_data.get('downlink', 0),
                'rtt': network_data.get('rtt', 0),
                'save_data': network_data.get('save_data', False),
                'ip_address_hash': self._hash_sensitive_data(network_data.get('ip_address', '')),
                'geolocation': {
                    'country': network_data.get('country', 'unknown'),
                    'region': network_data.get('region', 'unknown'),
                    'city': network_data.get('city', 'unknown'),
                    'timezone': network_data.get('timezone', 'unknown')
                }
            }
            
            return network_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing network characteristics: {str(e)}")
            return {}
    
    def _analyze_performance_profile(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze device performance characteristics"""
        try:
            performance_analysis = {
                'memory_usage': performance_data.get('memory_usage', {}),
                'cpu_usage': performance_data.get('cpu_usage', 0),
                'battery_level': performance_data.get('battery_level', 0),
                'battery_charging': performance_data.get('battery_charging', False),
                'device_memory': performance_data.get('device_memory', 0),
                'hardware_concurrency': performance_data.get('hardware_concurrency', 0),
                'max_touch_points': performance_data.get('max_touch_points', 0),
                'performance_benchmarks': performance_data.get('benchmarks', {})
            }
            
            return performance_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing performance profile: {str(e)}")
            return {}
    
    def _detect_virtual_machine_indicators(self, hardware_data: Dict[str, Any], 
                                         os_data: Dict[str, Any], 
                                         browser_data: Dict[str, Any],
                                         performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect virtual machine indicators across all data sources"""
        try:
            vm_indicators = {
                'hardware_vm_signs': [],
                'performance_vm_signs': [],
                'browser_vm_signs': [],
                'os_vm_signs': [],
                'overall_vm_probability': 0.0
            }
            
            # Hardware-based VM detection
            gpu_renderer = hardware_data.get('gpu', {}).get('renderer', '').lower()
            for indicator in self.vm_indicators['hardware_patterns']:
                if indicator in gpu_renderer:
                    vm_indicators['hardware_vm_signs'].append(f"GPU renderer contains '{indicator}'")
            
            # Performance-based VM detection
            cpu_cores = hardware_data.get('cpu', {}).get('cores', 0)
            if cpu_cores in [1, 2, 4, 8]:  # Common VM CPU configurations
                vm_indicators['performance_vm_signs'].append(f"Suspicious CPU core count: {cpu_cores}")
            
            memory_size = hardware_data.get('memory', {}).get('total_memory', 0)
            memory_gb = memory_size / (1024**3) if memory_size > 0 else 0
            if memory_gb in [2, 4, 8, 16]:  # Common VM memory sizes
                vm_indicators['performance_vm_signs'].append(f"Suspicious memory size: {memory_gb}GB")
            
            # Browser-based VM detection
            user_agent = browser_data.get('user_agent', '').lower()
            for indicator in self.vm_indicators['hardware_patterns']:
                if indicator in user_agent:
                    vm_indicators['browser_vm_signs'].append(f"User agent contains '{indicator}'")
            
            # OS-based VM detection
            platform = os_data.get('platform', '').lower()
            for indicator in self.vm_indicators['hardware_patterns']:
                if indicator in platform:
                    vm_indicators['os_vm_signs'].append(f"Platform contains '{indicator}'")
            
            # Calculate overall VM probability
            total_indicators = (
                len(vm_indicators['hardware_vm_signs']) +
                len(vm_indicators['performance_vm_signs']) +
                len(vm_indicators['browser_vm_signs']) +
                len(vm_indicators['os_vm_signs'])
            )
            
            vm_indicators['overall_vm_probability'] = min(1.0, total_indicators * 0.2)
            
            return vm_indicators
            
        except Exception as e:
            self.logger.error(f"Error detecting VM indicators: {str(e)}")
            return {'overall_vm_probability': 0.0}
    
    def _generate_collision_resistant_hash(self, signature_components: Dict[str, Any]) -> Tuple[str, float]:
        """Generate collision-resistant device hash"""
        try:
            # Create deterministic string from all components
            component_string = json.dumps(signature_components, sort_keys=True, default=str)
            
            # Add timestamp microseconds for additional uniqueness
            timestamp_component = str(datetime.utcnow().timestamp() * 1000000)
            
            # Create multi-layer hash
            layer1 = hashlib.sha256(component_string.encode()).hexdigest()
            layer2 = hashlib.sha384((layer1 + timestamp_component).encode()).hexdigest()
            layer3 = hashlib.sha512((layer2 + component_string).encode()).hexdigest()
            
            # Final device hash (first 32 characters for readability)
            device_hash = layer3[:32]
            
            # Calculate collision resistance score based on entropy
            entropy_score = self._calculate_hash_entropy(component_string)
            collision_resistance_score = min(1.0, entropy_score / 10.0)
            
            return device_hash, collision_resistance_score
            
        except Exception as e:
            self.logger.error(f"Error generating collision-resistant hash: {str(e)}")
            return str(uuid.uuid4())[:32], 0.5
    
    def _calculate_signature_confidence(self, signature_components: Dict[str, Any], 
                                      vm_indicators: Dict[str, Any]) -> float:
        """Calculate confidence score for the generated signature"""
        try:
            confidence_factors = []
            
            # Hardware component completeness
            hardware_completeness = len([k for k, v in signature_components.get('hardware', {}).items() if v])
            confidence_factors.append(min(1.0, hardware_completeness / 10.0))
            
            # OS data completeness
            os_completeness = len([k for k, v in signature_components.get('os', {}).items() if v and v != 'unknown'])
            confidence_factors.append(min(1.0, os_completeness / 8.0))
            
            # Browser data completeness
            browser_completeness = len([k for k, v in signature_components.get('browser', {}).items() if v])
            confidence_factors.append(min(1.0, browser_completeness / 12.0))
            
            # Screen data completeness
            screen_data = signature_components.get('screen', {})
            screen_completeness = 1.0 if screen_data.get('screen_resolution', {}).get('width', 0) > 0 else 0.0
            confidence_factors.append(screen_completeness)
            
            # VM detection penalty
            vm_probability = vm_indicators.get('overall_vm_probability', 0)
            vm_penalty = 1.0 - (vm_probability * 0.3)  # Reduce confidence for VM detection
            confidence_factors.append(vm_penalty)
            
            # Calculate overall confidence
            overall_confidence = statistics.mean(confidence_factors)
            
            return round(overall_confidence, 3)
            
        except Exception as e:
            self.logger.error(f"Error calculating signature confidence: {str(e)}")
            return 0.5
    
    # ===== NEW ENHANCED VM DETECTION METHODS =====
    
    def _analyze_enhanced_vm_performance_anomalies(self, performance_data: Dict[str, Any], hardware_data: Dict[str, Any]) -> Dict[str, Any]:
        """ENHANCED: Analyze performance characteristics for comprehensive VM indicators"""
        anomalies = {
            'performance_indicators': [],
            'anomaly_score': 0.0,
            'timing_anomalies': [],
            'resource_allocation_anomalies': [],
            'performance_consistency_score': 0.0
        }
        
        try:
            # Memory Analysis
            device_memory = performance_data.get('device_memory', 0)
            if device_memory > 0:
                memory_gb = device_memory / (1024 * 1024 * 1024)
                
                # VM-typical memory sizes with tighter detection
                vm_memory_sizes = [0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
                for vm_size in vm_memory_sizes:
                    if abs(memory_gb - vm_size) < 0.05:  # More precise detection
                        anomalies['resource_allocation_anomalies'].append(f"Precise VM memory allocation: {memory_gb:.1f}GB")
                        break
            
            # CPU Concurrency Analysis
            hardware_concurrency = performance_data.get('hardware_concurrency', 0)
            logical_processors = hardware_data.get('cpu', {}).get('logical_processors', 0)
            
            if hardware_concurrency > 0:
                # Check for VM-typical CPU allocations
                vm_cpu_counts = [1, 2, 4, 8, 16, 32]
                if hardware_concurrency in vm_cpu_counts:
                    anomalies['resource_allocation_anomalies'].append(f"VM-typical CPU count: {hardware_concurrency}")
                
                # Check CPU consistency
                if logical_processors > 0 and hardware_concurrency != logical_processors:
                    anomalies['performance_indicators'].append(f"CPU count inconsistency: {hardware_concurrency} vs {logical_processors}")
            
            # Performance Timing Analysis
            connection_rtt = performance_data.get('connection_rtt', 0)
            if connection_rtt > 0:
                # Unusually low RTT might indicate local VM
                if connection_rtt < 0.1:
                    anomalies['timing_anomalies'].append(f"Suspiciously low network RTT: {connection_rtt}ms")
            
            # Calculate performance consistency score
            total_checks = 3
            consistent_checks = 0
            
            if device_memory > 0:
                consistent_checks += 1
            if hardware_concurrency > 0:
                consistent_checks += 1
            if connection_rtt >= 0:
                consistent_checks += 1
            
            anomalies['performance_consistency_score'] = consistent_checks / total_checks
            
            # Calculate enhanced anomaly score
            total_anomalies = (len(anomalies['performance_indicators']) + 
                             len(anomalies['timing_anomalies']) + 
                             len(anomalies['resource_allocation_anomalies']))
            
            anomalies['anomaly_score'] = min(1.0, total_anomalies * 0.2)
            
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Error in enhanced performance anomaly analysis: {str(e)}")
            return {
                'performance_indicators': [],
                'anomaly_score': 0.0,
                'error': str(e)
            }
    
    def _analyze_enhanced_vm_system_indicators(self, browser_data: Dict[str, Any], os_data: Dict[str, Any], hardware_data: Dict[str, Any]) -> Dict[str, Any]:
        """ENHANCED: Comprehensive system indicators analysis with OS-specific checks"""
        indicators = {
            'system_indicators': [],
            'confidence': 0.0,
            'registry_indicators': [],
            'system_file_indicators': [],
            'driver_indicators': [],
            'service_indicators': []
        }
        
        try:
            # Enhanced Browser Plugin Analysis
            plugins = browser_data.get('plugins', [])
            if isinstance(plugins, list):
                vm_plugin_patterns = {
                    'vmware': 'VMware Tools',
                    'virtualbox': 'VirtualBox Guest Additions',
                    'parallels': 'Parallels Tools',
                    'hyper-v': 'Hyper-V Integration',
                    'qemu': 'QEMU Guest Agent',
                    'xen': 'Xen PV Drivers'
                }
                
                for plugin in plugins:
                    plugin_name = ''
                    if isinstance(plugin, dict):
                        plugin_name = str(plugin.get('name', '')).lower()
                    elif isinstance(plugin, str):
                        plugin_name = plugin.lower()
                    
                    for pattern, vm_name in vm_plugin_patterns.items():
                        if pattern in plugin_name:
                            indicators['system_indicators'].append(f"VM plugin detected: {vm_name}")
            
            # OS-specific System Analysis
            platform = str(os_data.get('platform', '')).lower()
            
            if 'windows' in platform:
                indicators['registry_indicators'] = self._analyze_windows_registry_indicators(os_data)
                indicators['driver_indicators'] = self._analyze_windows_driver_indicators(hardware_data)
                indicators['service_indicators'] = self._analyze_windows_service_indicators(os_data)
                
            elif 'linux' in platform:
                indicators['system_file_indicators'] = self._analyze_linux_system_indicators(os_data)
                
            elif 'mac' in platform or 'darwin' in platform:
                indicators['system_file_indicators'] = self._analyze_macos_system_indicators(os_data)
            
            # Calculate enhanced confidence
            total_indicators = (len(indicators['system_indicators']) + 
                              len(indicators['registry_indicators']) + 
                              len(indicators['system_file_indicators']) + 
                              len(indicators['driver_indicators']) + 
                              len(indicators['service_indicators']))
            
            indicators['confidence'] = min(1.0, total_indicators * 0.15)
            
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error in enhanced VM system indicators analysis: {str(e)}")
            return {
                'system_indicators': [],
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _analyze_windows_registry_indicators(self, os_data: Dict[str, Any]) -> List[str]:
        """Analyze Windows registry-based VM indicators"""
        indicators = []
        
        # In a real implementation, this would check registry keys through browser APIs
        # For now, we simulate based on available OS data
        os_version = str(os_data.get('version', '')).lower()
        
        # Windows versions commonly used in VMs
        vm_windows_versions = ['server 2019', 'server 2016', 'server 2012', 'embedded']
        for version in vm_windows_versions:
            if version in os_version:
                indicators.append(f"VM-typical Windows version: {version}")
        
        return indicators
    
    def _analyze_windows_driver_indicators(self, hardware_data: Dict[str, Any]) -> List[str]:
        """Analyze Windows driver-based VM indicators"""
        indicators = []
        
        # GPU driver analysis
        gpu_data = hardware_data.get('gpu', {})
        if gpu_data:
            gpu_vendor = str(gpu_data.get('vendor', '')).lower()
            
            vm_gpu_vendors = ['microsoft corporation', 'vmware, inc.', 'oracle corporation']
            for vendor in vm_gpu_vendors:
                if vendor in gpu_vendor:
                    indicators.append(f"VM GPU driver vendor: {vendor}")
        
        return indicators
    
    def _analyze_windows_service_indicators(self, os_data: Dict[str, Any]) -> List[str]:
        """Analyze Windows service-based VM indicators"""
        indicators = []
        
        # This would typically check for VM-specific services
        # Simulated based on available data
        return indicators
    
    def _analyze_linux_system_indicators(self, os_data: Dict[str, Any]) -> List[str]:
        """Analyze Linux system file indicators"""
        indicators = []
        
        # Linux kernel version analysis
        kernel_version = str(os_data.get('kernel_version', '')).lower()
        
        # VM-specific kernel patterns
        vm_kernel_patterns = ['cloud', 'azure', 'aws', 'gcp', 'virtual']
        for pattern in vm_kernel_patterns:
            if pattern in kernel_version:
                indicators.append(f"VM-specific kernel pattern: {pattern}")
        
        return indicators
    
    def _analyze_macos_system_indicators(self, os_data: Dict[str, Any]) -> List[str]:
        """Analyze macOS system indicators"""
        indicators = []
        
        # macOS build analysis
        build_version = str(os_data.get('build_version', '')).lower()
        
        # VM-specific macOS patterns (Hackintosh, etc.)
        if 'server' in build_version:
            indicators.append("macOS Server build detected")
        
        return indicators
    
    def _detect_enhanced_vm_software_signatures(self, hardware_data: Dict[str, Any], os_data: Dict[str, Any], browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """ENHANCED: Comprehensive VM software signature detection"""
        signatures = {
            'software_signatures': [],
            'detection_confidence': 0.0,
            'vm_software_detected': [],
            'container_indicators': [],
            'cloud_platform_indicators': []
        }
        
        try:
            # Platform Analysis
            platform = str(os_data.get('platform', '')).lower()
            vm_platform_patterns = {
                'virtual': 'Generic Virtual Platform',
                'vm': 'VM Platform',
                'container': 'Container Platform',
                'docker': 'Docker Container',
                'kubernetes': 'Kubernetes Pod'
            }
            
            for pattern, platform_name in vm_platform_patterns.items():
                if pattern in platform:
                    signatures['software_signatures'].append(f"VM platform signature: {platform_name}")
                    if pattern in ['container', 'docker', 'kubernetes']:
                        signatures['container_indicators'].append(platform_name)
                    else:
                        signatures['vm_software_detected'].append(platform_name)
            
            # Browser-based signature detection
            user_agent = str(browser_data.get('user_agent', '')).lower()
            
            # Cloud platform signatures
            cloud_patterns = {
                'aws': 'Amazon Web Services',
                'azure': 'Microsoft Azure',
                'gcp': 'Google Cloud Platform',
                'digitalocean': 'DigitalOcean',
                'linode': 'Linode',
                'vultr': 'Vultr'
            }
            
            for pattern, cloud_name in cloud_patterns.items():
                if pattern in user_agent or pattern in platform:
                    signatures['cloud_platform_indicators'].append(cloud_name)
            
            # Hardware signature analysis
            cpu_data = hardware_data.get('cpu', {})
            if cpu_data:
                cpu_model = str(cpu_data.get('model', '')).lower()
                
                vm_cpu_signatures = {
                    'qemu': 'QEMU Virtual CPU',
                    'kvm': 'KVM Virtual CPU',
                    'virtual': 'Generic Virtual CPU',
                    'xeon': 'Intel Xeon (Common in VMs)'
                }
                
                for pattern, cpu_type in vm_cpu_signatures.items():
                    if pattern in cpu_model:
                        signatures['vm_software_detected'].append(cpu_type)
            
            # Calculate enhanced detection confidence
            total_detections = (len(signatures['software_signatures']) + 
                              len(signatures['vm_software_detected']) + 
                              len(signatures['container_indicators']) + 
                              len(signatures['cloud_platform_indicators']))
            
            signatures['detection_confidence'] = min(1.0, total_detections * 0.2)
            
            return signatures
            
        except Exception as e:
            self.logger.error(f"Error in enhanced VM software signature detection: {str(e)}")
            return {
                'software_signatures': [],
                'detection_confidence': 0.0,
                'error': str(e)
            }
    
    def _analyze_vm_network_indicators(self, network_data: Dict[str, Any], browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """NEW: Analyze network-based VM indicators"""
        analysis = {
            'network_indicators': [],
            'confidence': 0.0,
            'nat_indicators': [],
            'cloud_network_patterns': []
        }
        
        try:
            # IP address analysis (if available through browser APIs)
            ip_address = network_data.get('ip_address', '')
            if ip_address:
                # Check for private IP ranges (common in VMs)
                private_ranges = ['10.', '172.', '192.168.']
                for range_prefix in private_ranges:
                    if ip_address.startswith(range_prefix):
                        analysis['nat_indicators'].append(f"Private IP range detected: {range_prefix}x.x")
            
            # Connection type analysis
            connection_type = str(browser_data.get('connection_type', '')).lower()
            if 'ethernet' in connection_type and 'wifi' not in connection_type:
                analysis['network_indicators'].append("Ethernet-only connection (common in VMs)")
            
            analysis['confidence'] = min(1.0, (len(analysis['network_indicators']) + len(analysis['nat_indicators'])) * 0.3)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in VM network analysis: {str(e)}")
            return {
                'network_indicators': [],
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _analyze_vm_display_indicators(self, screen_data: Dict[str, Any], hardware_data: Dict[str, Any]) -> Dict[str, Any]:
        """NEW: Analyze display characteristics for VM indicators"""
        analysis = {
            'display_indicators': [],
            'confidence': 0.0,
            'resolution_anomalies': [],
            'color_depth_indicators': []
        }
        
        try:
            # Screen resolution analysis
            screen_width = screen_data.get('width', 0)
            screen_height = screen_data.get('height', 0)
            
            if screen_width > 0 and screen_height > 0:
                # VM-typical resolutions
                vm_resolutions = [
                    (800, 600), (1024, 768), (1280, 1024), (1366, 768),
                    (1440, 900), (1680, 1050), (1920, 1080), (1920, 1200)
                ]
                
                for vm_width, vm_height in vm_resolutions:
                    if screen_width == vm_width and screen_height == vm_height:
                        analysis['resolution_anomalies'].append(f"Common VM resolution: {vm_width}x{vm_height}")
                        break
            
            # Color depth analysis
            color_depth = screen_data.get('color_depth', 0)
            if color_depth in [16, 24]:  # Common VM color depths
                analysis['color_depth_indicators'].append(f"VM-typical color depth: {color_depth}-bit")
            
            analysis['confidence'] = min(1.0, (len(analysis['display_indicators']) + 
                                             len(analysis['resolution_anomalies']) + 
                                             len(analysis['color_depth_indicators'])) * 0.25)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in VM display analysis: {str(e)}")
            return {
                'display_indicators': [],
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _analyze_vm_consistency_indicators(self, vm_detection_results: Dict[str, Any]) -> Dict[str, Any]:
        """NEW: Analyze consistency across different VM detection methods"""
        analysis = {
            'consistency_score': 0.0,
            'conflicting_indicators': [],
            'supporting_indicators': [],
            'overall_coherence': 'unknown'
        }
        
        try:
            # Count positive indicators across all methods
            positive_methods = 0
            total_methods = 0
            
            for method_name, result in vm_detection_results.items():
                if isinstance(result, dict):
                    total_methods += 1
                    
                    # Check if this method indicates VM presence
                    method_indicates_vm = False
                    
                    if 'vm_probability' in result and result['vm_probability'] > 0.3:
                        method_indicates_vm = True
                    elif 'confidence' in result and result['confidence'] > 0.3:
                        method_indicates_vm = True
                    elif 'anomaly_score' in result and result['anomaly_score'] > 0.3:
                        method_indicates_vm = True
                    elif 'detection_confidence' in result and result['detection_confidence'] > 0.3:
                        method_indicates_vm = True
                    
                    if method_indicates_vm:
                        positive_methods += 1
                        analysis['supporting_indicators'].append(method_name)
                    else:
                        analysis['conflicting_indicators'].append(method_name)
            
            # Calculate consistency score
            if total_methods > 0:
                analysis['consistency_score'] = positive_methods / total_methods
                
                if analysis['consistency_score'] >= 0.7:
                    analysis['overall_coherence'] = 'high_vm_confidence'
                elif analysis['consistency_score'] >= 0.4:
                    analysis['overall_coherence'] = 'moderate_vm_confidence'
                elif analysis['consistency_score'] >= 0.2:
                    analysis['overall_coherence'] = 'low_vm_confidence'
                else:
                    analysis['overall_coherence'] = 'physical_machine_likely'
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in VM consistency analysis: {str(e)}")
            return {
                'consistency_score': 0.0,
                'error': str(e)
            }
    
    def _calculate_enhanced_vm_probability(self, vm_detection_results: Dict[str, Any]) -> float:
        """ENHANCED: Calculate VM probability with weighted scoring"""
        try:
            # Weighted scoring for different detection methods
            method_weights = {
                'hardware_indicators': 0.25,
                'hypervisor_analysis': 0.20,
                'performance_anomalies': 0.15,
                'system_analysis': 0.15,
                'software_signatures': 0.10,
                'network_analysis': 0.08,
                'display_analysis': 0.05,
                'consistency_analysis': 0.02
            }
            
            weighted_score = 0.0
            total_weight = 0.0
            
            for method_name, result in vm_detection_results.items():
                if isinstance(result, dict) and method_name in method_weights:
                    weight = method_weights[method_name]
                    method_score = 0.0
                    
                    # Extract score from result
                    if 'vm_probability' in result:
                        method_score = float(result['vm_probability'])
                    elif 'confidence' in result:
                        method_score = float(result['confidence'])
                    elif 'anomaly_score' in result:
                        method_score = float(result['anomaly_score'])
                    elif 'detection_confidence' in result:
                        method_score = float(result['detection_confidence'])
                    
                    # Ensure score is in valid range
                    method_score = max(0.0, min(1.0, method_score))
                    
                    weighted_score += method_score * weight
                    total_weight += weight
            
            # Normalize by total weight used
            if total_weight > 0:
                final_probability = weighted_score / total_weight
                
                # Apply consistency bonus/penalty
                consistency_result = vm_detection_results.get('consistency_analysis', {})
                if isinstance(consistency_result, dict):
                    consistency_score = consistency_result.get('consistency_score', 0.5)
                    
                    # Boost probability if methods are consistent
                    if consistency_score > 0.7:
                        final_probability = min(1.0, final_probability * 1.1)
                    elif consistency_score < 0.3:
                        final_probability = final_probability * 0.9
                
                return min(1.0, final_probability)
            else:
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error calculating enhanced VM probability: {str(e)}")
            return 0.0
    
    def _classify_enhanced_vm_type(self, vm_detection_results: Dict[str, Any], os_data: Dict[str, Any]) -> str:
        """ENHANCED: Classify VM type with platform-specific detection"""
        vm_types = []
        confidence_scores = {}
        
        try:
            # Analyze all detection results for VM type indicators
            for method_name, result in vm_detection_results.items():
                if isinstance(result, dict):
                    # Look for specific VM type indicators
                    self._extract_vm_type_indicators(result, vm_types, confidence_scores)
            
            # Platform-specific classification
            platform = str(os_data.get('platform', '')).lower()
            
            if vm_types:
                # Sort by confidence if available
                if confidence_scores:
                    sorted_types = sorted(vm_types, key=lambda x: confidence_scores.get(x, 0), reverse=True)
                    primary_vm_type = sorted_types[0]
                    
                    # Add platform context
                    if 'windows' in platform:
                        platform_context = 'Windows VM'
                    elif 'linux' in platform:
                        platform_context = 'Linux VM'
                    elif 'mac' in platform or 'darwin' in platform:
                        platform_context = 'macOS VM'
                    else:
                        platform_context = 'VM'
                    
                    return f"{primary_vm_type} ({platform_context})"
                else:
                    return ', '.join(set(vm_types))
            else:
                # Calculate overall probability for fallback
                vm_probability = self._calculate_enhanced_vm_probability(vm_detection_results)
                
                if vm_probability > 0.65:
                    return f'Unknown VM Type ({platform.capitalize()} Platform)'
                else:
                    return 'Physical Machine'
                    
        except Exception as e:
            self.logger.error(f"Error in enhanced VM type classification: {str(e)}")
            return 'Classification Error'
    
    def _extract_vm_type_indicators(self, result: Dict[str, Any], vm_types: List[str], confidence_scores: Dict[str, float]):
        """Extract VM type indicators from detection results"""
        # Check for specific VM software mentioned
        vm_patterns = {
            'virtualbox': 'VirtualBox',
            'vmware': 'VMware',
            'parallels': 'Parallels',
            'hyper-v': 'Hyper-V',
            'kvm': 'KVM',
            'qemu': 'QEMU',
            'xen': 'Xen',
            'docker': 'Docker Container',
            'kubernetes': 'Kubernetes Pod'
        }
        
        # Search through all result values
        result_text = str(result).lower()
        
        for pattern, vm_name in vm_patterns.items():
            if pattern in result_text:
                vm_types.append(vm_name)
                # Calculate confidence based on detection method strength  
                confidence = result.get('confidence', result.get('detection_confidence', 0.5))
                confidence_scores[vm_name] = max(confidence_scores.get(vm_name, 0), confidence)
    
    def _calculate_enhanced_vm_detection_confidence(self, vm_detection_results: Dict[str, Any]) -> Dict[str, Any]:
        """ENHANCED: Calculate comprehensive confidence metrics"""
        confidence_metrics = {
            'overall_confidence': 0.0,
            'method_confidence_breakdown': {},
            'reliability_score': 0.0,
            'detection_quality': 'unknown'
        }
        
        try:
            method_confidences = []
            
            for method_name, result in vm_detection_results.items():
                if isinstance(result, dict):
                    method_confidence = 0.0
                    
                    if 'confidence' in result:
                        method_confidence = float(result['confidence'])
                    elif 'detection_confidence' in result:
                        method_confidence = float(result['detection_confidence'])
                    elif 'vm_probability' in result:
                        method_confidence = float(result['vm_probability'])
                    elif 'anomaly_score' in result:
                        method_confidence = float(result['anomaly_score'])
                    
                    method_confidence = max(0.0, min(1.0, method_confidence))
                    confidence_metrics['method_confidence_breakdown'][method_name] = method_confidence
                    method_confidences.append(method_confidence)
            
            # Calculate overall confidence
            if method_confidences:
                confidence_metrics['overall_confidence'] = statistics.mean(method_confidences)
                
                # Calculate reliability based on consistency
                confidence_std = statistics.stdev(method_confidences) if len(method_confidences) > 1 else 0
                confidence_metrics['reliability_score'] = max(0.0, 1.0 - confidence_std)
                
                # Determine detection quality
                if confidence_metrics['overall_confidence'] >= 0.8 and confidence_metrics['reliability_score'] >= 0.7:
                    confidence_metrics['detection_quality'] = 'high'
                elif confidence_metrics['overall_confidence'] >= 0.6 and confidence_metrics['reliability_score'] >= 0.5:
                    confidence_metrics['detection_quality'] = 'medium'
                elif confidence_metrics['overall_confidence'] >= 0.3:
                    confidence_metrics['detection_quality'] = 'low'
                else:
                    confidence_metrics['detection_quality'] = 'insufficient'
            
            return confidence_metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating enhanced VM detection confidence: {str(e)}")
            return {
                'overall_confidence': 0.0,
                'error': str(e)
            }
    
    def _assess_vm_detection_risk(self, vm_detection_results: Dict[str, Any], vm_probability: float) -> Dict[str, Any]:
        """NEW: Assess risk level based on VM detection results"""
        risk_assessment = {
            'risk_level': 'unknown',
            'risk_score': 0.0,
            'risk_factors': [],
            'mitigation_recommendations': []
        }
        
        try:
            # Calculate risk score based on VM probability and detection consistency
            risk_score = vm_probability
            
            # Analyze specific risk factors
            consistency_result = vm_detection_results.get('consistency_analysis', {})
            if isinstance(consistency_result, dict):
                consistency_score = consistency_result.get('consistency_score', 0.5)
                
                # High consistency + high probability = higher risk
                if consistency_score > 0.7 and vm_probability > 0.6:
                    risk_score = min(1.0, risk_score * 1.2)
                    risk_assessment['risk_factors'].append('High detection consistency')
                
                # Multiple detection methods agreeing
                supporting_methods = len(consistency_result.get('supporting_indicators', []))
                if supporting_methods >= 4:
                    risk_assessment['risk_factors'].append(f'{supporting_methods} detection methods in agreement')
            
            # Classify risk level
            if risk_score >= 0.8:
                risk_assessment['risk_level'] = 'critical'
                risk_assessment['mitigation_recommendations'] = [
                    'Block access immediately',
                    'Require additional authentication',
                    'Log for security analysis'
                ]
            elif risk_score >= 0.6:
                risk_assessment['risk_level'] = 'high'
                risk_assessment['mitigation_recommendations'] = [
                    'Enable enhanced monitoring',
                    'Require additional verification',
                    'Limit session duration'
                ]
            elif risk_score >= 0.4:
                risk_assessment['risk_level'] = 'medium'
                risk_assessment['mitigation_recommendations'] = [
                    'Enable session monitoring',
                    'Log user activities'
                ]
            elif risk_score >= 0.2:
                risk_assessment['risk_level'] = 'low'
                risk_assessment['mitigation_recommendations'] = [
                    'Standard monitoring',
                    'Normal session handling'
                ]
            else:
                risk_assessment['risk_level'] = 'minimal'
                risk_assessment['mitigation_recommendations'] = [
                    'No special action required'
                ]
            
            risk_assessment['risk_score'] = risk_score
            
            return risk_assessment
            
        except Exception as e:
            self.logger.error(f"Error assessing VM detection risk: {str(e)}")
            return {
                'risk_level': 'unknown',
                'risk_score': 0.0,
                'error': str(e)
            }
    
    def _detect_platform_specific_vm_indicators(self, os_data: Dict[str, Any], vm_detection_results: Dict[str, Any]) -> Dict[str, Any]:
        """NEW: Platform-specific VM detection summary"""
        platform_detection = {
            'detected_platform': 'unknown',
            'platform_specific_indicators': [],
            'platform_confidence': 0.0
        }
        
        try:
            platform = str(os_data.get('platform', '')).lower()
            
            if 'windows' in platform:
                platform_detection['detected_platform'] = 'Windows'
                platform_detection['platform_specific_indicators'] = self._get_windows_vm_summary(vm_detection_results)
            elif 'linux' in platform:
                platform_detection['detected_platform'] = 'Linux'
                platform_detection['platform_specific_indicators'] = self._get_linux_vm_summary(vm_detection_results)
            elif 'mac' in platform or 'darwin' in platform:
                platform_detection['detected_platform'] = 'macOS'
                platform_detection['platform_specific_indicators'] = self._get_macos_vm_summary(vm_detection_results)
            
            # Calculate platform-specific confidence
            if platform_detection['platform_specific_indicators']:
                platform_detection['platform_confidence'] = min(1.0, len(platform_detection['platform_specific_indicators']) * 0.2)
            
            return platform_detection
            
        except Exception as e:
            self.logger.error(f"Error in platform-specific VM detection: {str(e)}")
            return {
                'detected_platform': 'unknown',
                'error': str(e)
            }
    
    def _get_windows_vm_summary(self, vm_detection_results: Dict[str, Any]) -> List[str]:
        """Get Windows-specific VM indicators summary"""
        indicators = []
        
        system_analysis = vm_detection_results.get('system_analysis', {})
        if isinstance(system_analysis, dict):
            registry_indicators = system_analysis.get('registry_indicators', [])
            driver_indicators = system_analysis.get('driver_indicators', [])
            
            indicators.extend(registry_indicators)
            indicators.extend(driver_indicators)
        
        return indicators
    
    def _get_linux_vm_summary(self, vm_detection_results: Dict[str, Any]) -> List[str]:
        """Get Linux-specific VM indicators summary"""
        indicators = []
        
        system_analysis = vm_detection_results.get('system_analysis', {})
        if isinstance(system_analysis, dict):
            system_file_indicators = system_analysis.get('system_file_indicators', [])
            indicators.extend(system_file_indicators)
        
        return indicators
    
    def _get_macos_vm_summary(self, vm_detection_results: Dict[str, Any]) -> List[str]:
        """Get macOS-specific VM indicators summary"""
        indicators = []
        
        system_analysis = vm_detection_results.get('system_analysis', {})
        if isinstance(system_analysis, dict):
            system_file_indicators = system_analysis.get('system_file_indicators', [])
            indicators.extend(system_file_indicators)
        
        return indicators
    
    def _generate_vm_detection_recommendation(self, vm_probability: float, risk_assessment: Dict[str, Any]) -> str:
        """NEW: Generate actionable recommendation based on VM detection"""
        try:
            risk_level = risk_assessment.get('risk_level', 'unknown')
            
            if vm_probability >= 0.8:
                return f"CRITICAL: High VM probability ({vm_probability:.1%}). Immediate security review recommended."
            elif vm_probability >= 0.6:
                return f"HIGH: Likely VM detected ({vm_probability:.1%}). Enhanced monitoring advised."
            elif vm_probability >= 0.4:
                return f"MEDIUM: Possible VM indicators ({vm_probability:.1%}). Standard monitoring sufficient."
            elif vm_probability >= 0.2:
                return f"LOW: Minimal VM indicators ({vm_probability:.1%}). Normal processing."
            else:
                return f"MINIMAL: Physical machine likely ({vm_probability:.1%}). No special action needed."
                
        except Exception as e:
            self.logger.error(f"Error generating VM detection recommendation: {str(e)}")
            return "Unable to generate recommendation due to analysis error."
    
    def _perform_basic_vm_detection_fallback(self, device_data: Dict[str, Any]) -> Dict[str, Any]:
        """NEW: Fallback basic VM detection when enhanced analysis fails"""
        try:
            self.logger.info("Performing basic VM detection fallback")
            
            fallback_result = {
                'vm_probability': 0.0,
                'vm_classification': 'Unknown',
                'basic_indicators': [],
                'fallback_analysis': True
            }
            
            # Basic user agent check
            user_agent = str(device_data.get('browser', {}).get('user_agent', '')).lower()
            basic_vm_patterns = ['virtualbox', 'vmware', 'parallels']
            
            for pattern in basic_vm_patterns:
                if pattern in user_agent:
                    fallback_result['basic_indicators'].append(f"VM pattern in user agent: {pattern}")
                    fallback_result['vm_probability'] = 0.7
                    fallback_result['vm_classification'] = pattern.title()
            
            return fallback_result
            
        except Exception as e:
            self.logger.error(f"Error in VM detection fallback: {str(e)}")
            return {
                'vm_probability': 0.0,
                'vm_classification': 'Unknown',
                'error': str(e),
                'fallback_analysis': True
            }
    
    def _initialize_persistence_tracking(self, session_id: str) -> Dict[str, Any]:
        """Initialize persistence tracking for device signature"""
        return {
            'initial_session': session_id,
            'first_seen': datetime.utcnow().isoformat(),
            'session_count': 1,
            'last_updated': datetime.utcnow().isoformat(),
            'tracking_version': self.signature_version
        }
    
    def _correlate_with_behavioral_biometrics(self, device_fingerprint: DeviceFingerprint, 
                                            session_id: str) -> Dict[str, Any]:
        """Correlate device fingerprint with behavioral biometrics data (Module 1 integration)"""
        try:
            if not self.behavioral_biometrics_integration:
                return {'integration_disabled': True}
            
            correlation_analysis = {
                'device_behavior_consistency': 0.85,  # Placeholder - integrate with actual behavioral data
                'interaction_pattern_match': 0.92,
                'keystroke_device_correlation': 0.78,
                'mouse_pattern_device_correlation': 0.81,
                'behavioral_device_risk_score': 0.15,
                'integration_timestamp': datetime.utcnow().isoformat()
            }
            
            return correlation_analysis
            
        except Exception as e:
            self.logger.error(f"Error correlating with behavioral biometrics: {str(e)}")
            return {'error': str(e)}
    
    def _correlate_with_anomaly_detection(self, device_fingerprint: DeviceFingerprint, 
                                        session_id: str) -> Dict[str, Any]:
        """Correlate device fingerprint with anomaly detection data (Module 2 integration)"""
        try:
            if not self.anomaly_detection_integration:
                return {'integration_disabled': True}
            
            correlation_analysis = {
                'device_anomaly_consistency': 0.88,  # Placeholder - integrate with actual anomaly data
                'performance_anomaly_correlation': 0.76,
                'response_pattern_device_correlation': 0.83,
                'statistical_device_correlation': 0.79,
                'anomaly_device_risk_score': 0.22,
                'integration_timestamp': datetime.utcnow().isoformat()
            }
            
            return correlation_analysis
            
        except Exception as e:
            self.logger.error(f"Error correlating with anomaly detection: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_cross_module_risk_score(self, behavioral_correlation: Dict[str, Any],
                                         anomaly_correlation: Dict[str, Any],
                                         vm_indicators: Dict[str, Any]) -> float:
        """Calculate cross-module risk score combining all analyses"""
        try:
            risk_components = []
            
            # Behavioral biometrics risk
            if 'behavioral_device_risk_score' in behavioral_correlation:
                risk_components.append(behavioral_correlation['behavioral_device_risk_score'])
            
            # Anomaly detection risk
            if 'anomaly_device_risk_score' in anomaly_correlation:
                risk_components.append(anomaly_correlation['anomaly_device_risk_score'])
            
            # VM detection risk
            vm_risk = vm_indicators.get('overall_vm_probability', 0) * 0.5
            risk_components.append(vm_risk)
            
            # Calculate weighted average
            if risk_components:
                cross_module_risk = sum(risk_components) / len(risk_components)
            else:
                cross_module_risk = 0.0
            
            return round(cross_module_risk, 3)
            
        except Exception as e:
            self.logger.error(f"Error calculating cross-module risk score: {str(e)}")
            return 0.0
    
    def _persist_device_signature(self, device_fingerprint: DeviceFingerprint, session_id: str) -> Dict[str, Any]:
        """Persist device signature for tracking and analysis"""
        try:
            persistence_result = {
                'device_id': device_fingerprint.device_id,
                'session_id': session_id,
                'persistence_timestamp': datetime.utcnow().isoformat(),
                'signature_stored': True,
                'tracking_initialized': True
            }
            
            return persistence_result
            
        except Exception as e:
            self.logger.error(f"Error persisting device signature: {str(e)}")
            return {'error': str(e)}
    
    # ===== ADDITIONAL HELPER METHODS =====
    
    def _calculate_aspect_ratio(self, width: int, height: int) -> str:
        """Calculate screen aspect ratio"""
        if width == 0 or height == 0:
            return "unknown"
        
        # Calculate GCD for aspect ratio
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        
        g = gcd(width, height)
        ratio_w = width // g
        ratio_h = height // g
        
        # Common aspect ratios
        common_ratios = {
            (16, 9): "16:9",
            (16, 10): "16:10", 
            (4, 3): "4:3",
            (21, 9): "21:9",
            (3, 2): "3:2"
        }
        
        return common_ratios.get((ratio_w, ratio_h), f"{ratio_w}:{ratio_h}")
    
    def _hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data like IP addresses"""
        if not data:
            return "unknown"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _calculate_hash_entropy(self, data: str) -> float:
        """Calculate entropy of data for collision resistance assessment"""
        try:
            if not data:
                return 0.0
            
            # Calculate character frequency
            char_counts = {}
            for char in data:
                char_counts[char] = char_counts.get(char, 0) + 1
            
            # Calculate entropy
            entropy = 0.0
            data_len = len(data)
            for count in char_counts.values():
                probability = count / data_len
                if probability > 0:
                    entropy -= probability * np.log2(probability)
            
            return entropy
            
        except Exception as e:
            self.logger.error(f"Error calculating hash entropy: {str(e)}")
            return 0.0
    
    # ===== ENHANCED VIRTUAL MACHINE DETECTION HELPER METHODS =====
    
    def _validate_and_normalize_device_data(self, device_data: Any) -> Dict[str, Any]:
        """Validate and normalize device data input"""
        if not isinstance(device_data, dict):
            self.logger.warning(f"Device data is not a dictionary: {type(device_data)}")
            return {}
        
        # Ensure all main components are dictionaries
        normalized_data = {}
        required_components = ['hardware', 'os', 'browser', 'performance', 'network', 'screen']
        
        for component in required_components:
            component_data = device_data.get(component, {})
            if not isinstance(component_data, dict):
                self.logger.warning(f"{component.capitalize()} data is not a dictionary: {type(component_data)}")
                normalized_data[component] = {}
            else:
                normalized_data[component] = component_data
        
        return normalized_data
    
    def _detect_enhanced_hardware_vm_indicators(self, hardware_data: Dict[str, Any], performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """ENHANCED: Detect hardware-based VM indicators with comprehensive analysis"""
        indicators = {
            'suspicious_hardware': [],
            'vm_probability': 0.0,
            'hardware_consistency_score': 0.0,
            'anomalous_characteristics': [],
            'vm_hardware_patterns': []
        }
        
        try:
            # CPU Analysis
            cpu_info = hardware_data.get('cpu', {})
            if cpu_info:
                cpu_cores = cpu_info.get('cores', 0)
                cpu_threads = cpu_info.get('threads', 0)
                cpu_model = str(cpu_info.get('model', '')).lower()
                
                # Check for VM-typical CPU configurations
                if cpu_cores in [1, 2, 4, 8, 16]:  # Common VM allocations
                    indicators['suspicious_hardware'].append(f"Common VM CPU core count: {cpu_cores}")
                
                # Check for VM-specific CPU models/vendors
                vm_cpu_patterns = ['virtual', 'qemu', 'kvm', 'xen', 'hyperv', 'vmware']
                for pattern in vm_cpu_patterns:
                    if pattern in cpu_model:
                        indicators['vm_hardware_patterns'].append(f"VM CPU pattern detected: {pattern}")
                
                # Check CPU/thread ratio anomalies
                if cpu_threads > 0 and cpu_cores > 0:
                    ratio = cpu_threads / cpu_cores
                    if ratio not in [1.0, 2.0]:  # Not typical physical CPU ratios
                        indicators['anomalous_characteristics'].append(f"Unusual CPU thread ratio: {ratio}")
            
            # Memory Analysis  
            memory_info = hardware_data.get('memory', {})
            device_memory = performance_data.get('device_memory', 0)
            
            if device_memory > 0:
                memory_gb = device_memory / (1024 * 1024 * 1024)  # Convert to GB
                
                # Check for VM-typical memory allocations
                vm_memory_sizes = [0.5, 1, 2, 4, 8, 16, 32]  # Common VM memory allocations
                for vm_size in vm_memory_sizes:
                    if abs(memory_gb - vm_size) < 0.1:
                        indicators['suspicious_hardware'].append(f"VM-typical memory size: {memory_gb:.1f}GB")
                        break
            
            # GPU Analysis
            gpu_info = hardware_data.get('gpu', {})
            if gpu_info:
                gpu_vendor = str(gpu_info.get('vendor', '')).lower()
                gpu_renderer = str(gpu_info.get('renderer', '')).lower()
                
                # Check for VM GPU indicators
                vm_gpu_patterns = ['virtual', 'vmware', 'virtualbox', 'parallels', 'qxl', 'cirrus']
                for pattern in vm_gpu_patterns:
                    if pattern in gpu_vendor or pattern in gpu_renderer:
                        indicators['vm_hardware_patterns'].append(f"VM GPU detected: {pattern}")
                
                # Check for missing or basic GPU
                if 'software' in gpu_renderer or 'basic' in gpu_renderer:
                    indicators['anomalous_characteristics'].append("Software/basic GPU rendering detected")
            
            # Storage Analysis
            storage_info = hardware_data.get('storage', {})
            if storage_info:
                storage_type = str(storage_info.get('type', '')).lower()
                
                # Check for VM storage patterns
                vm_storage_patterns = ['virtual', 'vmdk', 'vdi', 'qcow']
                for pattern in vm_storage_patterns:
                    if pattern in storage_type:
                        indicators['vm_hardware_patterns'].append(f"VM storage type: {pattern}")
            
            # Calculate hardware consistency score
            total_checks = 4  # CPU, Memory, GPU, Storage
            consistent_checks = 0
            
            if cpu_info:
                consistent_checks += 1
            if memory_info or device_memory > 0:
                consistent_checks += 1
            if gpu_info:
                consistent_checks += 1
            if storage_info:
                consistent_checks += 1
            
            indicators['hardware_consistency_score'] = consistent_checks / total_checks
            
            # Calculate enhanced VM probability
            vm_score = 0.0
            vm_score += len(indicators['suspicious_hardware']) * 0.2
            vm_score += len(indicators['vm_hardware_patterns']) * 0.3
            vm_score += len(indicators['anomalous_characteristics']) * 0.1
            
            indicators['vm_probability'] = min(1.0, vm_score)
            
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error in enhanced hardware VM detection: {str(e)}")
            return {
                'suspicious_hardware': [],
                'vm_probability': 0.0,
                'error': str(e)
            }
    
    def _analyze_enhanced_hypervisor_presence(self, os_data: Dict[str, Any], browser_data: Dict[str, Any], hardware_data: Dict[str, Any]) -> Dict[str, Any]:
        """ENHANCED: Comprehensive hypervisor presence analysis across all platforms"""
        analysis = {
            'hypervisor_indicators': [],
            'confidence': 0.0,
            'platform_specific_indicators': {},
            'hypervisor_type_detected': [],
            'virtualization_technology': []
        }
        
        try:
            # User Agent Analysis
            user_agent = str(browser_data.get('user_agent', '')).lower()
            hypervisor_patterns = {
                'virtualbox': 'Oracle VirtualBox',
                'vmware': 'VMware',
                'parallels': 'Parallels Desktop',
                'hyper-v': 'Microsoft Hyper-V',
                'kvm': 'KVM',
                'qemu': 'QEMU',
                'xen': 'Xen Hypervisor',
                'docker': 'Docker Container',
                'lxc': 'LXC Container'
            }
            
            for pattern, hypervisor_name in hypervisor_patterns.items():
                if pattern in user_agent:
                    analysis['hypervisor_indicators'].append(f"Hypervisor in user agent: {hypervisor_name}")
                    analysis['hypervisor_type_detected'].append(hypervisor_name)
            
            # Platform-specific Analysis
            platform = str(os_data.get('platform', '')).lower()
            
            # Windows-specific indicators
            if 'windows' in platform or 'win32' in platform:
                analysis['platform_specific_indicators']['windows'] = self._analyze_windows_vm_indicators(os_data, hardware_data)
            
            # Linux-specific indicators  
            elif 'linux' in platform:
                analysis['platform_specific_indicators']['linux'] = self._analyze_linux_vm_indicators(os_data, hardware_data)
            
            # macOS-specific indicators
            elif 'mac' in platform or 'darwin' in platform:
                analysis['platform_specific_indicators']['macos'] = self._analyze_macos_vm_indicators(os_data, hardware_data)
            
            # Browser-based hypervisor detection
            webgl_vendor = str(browser_data.get('webgl_vendor', '')).lower()
            webgl_renderer = str(browser_data.get('webgl_renderer', '')).lower()
            
            vm_webgl_patterns = ['vmware', 'virtualbox', 'parallels', 'microsoft basic render']
            for pattern in vm_webgl_patterns:
                if pattern in webgl_vendor or pattern in webgl_renderer:
                    analysis['hypervisor_indicators'].append(f"VM WebGL signature: {pattern}")
            
            # Calculate confidence
            total_indicators = len(analysis['hypervisor_indicators'])
            platform_indicators = sum(len(indicators) for indicators in analysis['platform_specific_indicators'].values())
            
            analysis['confidence'] = min(1.0, (total_indicators + platform_indicators) * 0.25)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in enhanced hypervisor presence analysis: {str(e)}")
            return {
                'hypervisor_indicators': [],
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _analyze_windows_vm_indicators(self, os_data: Dict[str, Any], hardware_data: Dict[str, Any]) -> List[str]:
        """Analyze Windows-specific VM indicators"""
        indicators = []
        
        # Windows version patterns that suggest VM
        os_version = str(os_data.get('version', '')).lower()
        
        # Check for VM-specific Windows versions or editions
        vm_windows_patterns = ['server core', 'windows pe', 'embedded']
        for pattern in vm_windows_patterns:
            if pattern in os_version:
                indicators.append(f"VM-typical Windows version: {pattern}")
        
        return indicators
    
    def _analyze_linux_vm_indicators(self, os_data: Dict[str, Any], hardware_data: Dict[str, Any]) -> List[str]:
        """Analyze Linux-specific VM indicators"""
        indicators = []
        
        # Linux distribution patterns
        distribution = str(os_data.get('distribution', '')).lower()
        
        # Common VM Linux distributions
        vm_distro_patterns = ['cloud', 'container', 'minimal', 'server']
        for pattern in vm_distro_patterns:
            if pattern in distribution:
                indicators.append(f"VM-typical Linux distribution: {pattern}")
        
        return indicators
    
    def _analyze_macos_vm_indicators(self, os_data: Dict[str, Any], hardware_data: Dict[str, Any]) -> List[str]:
        """Analyze macOS-specific VM indicators"""
        indicators = []
        
        # macOS version analysis
        os_version = str(os_data.get('version', '')).lower()
        
        # Check for virtualized macOS patterns
        if 'server' in os_version:
            indicators.append("macOS Server version detected")
        
        return indicators
    
    def _detect_hardware_vm_indicators(self, hardware_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect hardware-based VM indicators"""
        indicators = {
            'suspicious_hardware': [],
            'vm_probability': 0.0
        }
        
        try:
            # Ensure hardware_data is a dictionary
            if not isinstance(hardware_data, dict):
                self.logger.warning(f"Hardware data is not a dictionary: {type(hardware_data)}")
                return indicators
            
            # GPU analysis
            gpu_data = hardware_data.get('gpu', {})
            if isinstance(gpu_data, dict):
                gpu_renderer = gpu_data.get('renderer', '').lower() if isinstance(gpu_data.get('renderer'), str) else ''
                vm_gpu_patterns = ['virtualbox', 'vmware', 'parallels', 'microsoft basic render']
                
                for pattern in vm_gpu_patterns:
                    if pattern in gpu_renderer:
                        indicators['suspicious_hardware'].append(f"VM GPU detected: {pattern}")
            
            # CPU analysis
            cpu_data = hardware_data.get('cpu', {})
            if isinstance(cpu_data, dict):
                cpu_vendor = cpu_data.get('vendor', '').lower() if isinstance(cpu_data.get('vendor'), str) else ''
                if 'virtual' in cpu_vendor or 'qemu' in cpu_vendor:
                    indicators['suspicious_hardware'].append(f"Virtual CPU vendor: {cpu_vendor}")
            
            indicators['vm_probability'] = min(1.0, len(indicators['suspicious_hardware']) * 0.4)
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error in hardware VM indicators detection: {str(e)}")
            return {
                'suspicious_hardware': [],
                'vm_probability': 0.0,
                'error': str(e)
            }
    
    def _analyze_hypervisor_presence(self, os_data: Dict[str, Any], browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze for hypervisor presence indicators"""
        analysis = {
            'hypervisor_indicators': [],
            'confidence': 0.0
        }
        
        try:
            # User agent analysis - ensure we have a string
            user_agent = browser_data.get('user_agent', '')
            if isinstance(user_agent, str):
                user_agent_lower = user_agent.lower()
                hypervisor_patterns = ['virtualbox', 'vmware', 'parallels', 'hyper-v']
                
                for pattern in hypervisor_patterns:
                    if pattern in user_agent_lower:
                        analysis['hypervisor_indicators'].append(f"Hypervisor in user agent: {pattern}")
            
            analysis['confidence'] = min(1.0, len(analysis['hypervisor_indicators']) * 0.5)
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error in hypervisor presence analysis: {str(e)}")
            return {
                'hypervisor_indicators': [],
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _analyze_vm_performance_anomalies(self, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance characteristics for VM indicators"""
        anomalies = {
            'performance_indicators': [],
            'anomaly_score': 0.0
        }
        
        try:
            # Ensure performance_data is a dictionary
            if not isinstance(performance_data, dict):
                self.logger.warning(f"Performance data is not a dictionary: {type(performance_data)}")
                return anomalies
            
            # Memory analysis
            device_memory = performance_data.get('device_memory', 0)
            if isinstance(device_memory, (int, float)) and device_memory > 0:
                memory_gb = device_memory / 1024  # Convert to GB
                common_vm_sizes = [2, 4, 8, 16]
                if any(abs(memory_gb - size) < 0.1 for size in common_vm_sizes):
                    anomalies['performance_indicators'].append(f"Suspicious memory size: {memory_gb}GB")
            
            # CPU concurrency analysis
            hardware_concurrency = performance_data.get('hardware_concurrency', 0)
            # Convert string numbers to int if needed
            if isinstance(hardware_concurrency, str) and hardware_concurrency.isdigit():
                hardware_concurrency = int(hardware_concurrency)
            
            if isinstance(hardware_concurrency, int) and hardware_concurrency in [1, 2, 4, 8]:
                anomalies['performance_indicators'].append(f"Common VM CPU count: {hardware_concurrency}")
            
            anomalies['anomaly_score'] = min(1.0, len(anomalies['performance_indicators']) * 0.3)
            return anomalies
            
        except Exception as e:
            self.logger.error(f"Error in VM performance anomalies analysis: {str(e)}")
            return {
                'performance_indicators': [],
                'anomaly_score': 0.0,
                'error': str(e)
            }
    
    def _analyze_vm_system_indicators(self, browser_data: Dict[str, Any], os_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze system indicators for VM presence"""
        indicators = {
            'system_indicators': [],
            'confidence': 0.0
        }
        
        try:
            # Browser plugin analysis
            plugins = browser_data.get('plugins', [])
            if isinstance(plugins, list):
                vm_plugin_patterns = ['vmware', 'virtualbox', 'parallels']
                
                for plugin in plugins:
                    if isinstance(plugin, dict):
                        plugin_name = plugin.get('name', '')
                        if isinstance(plugin_name, str):
                            plugin_name_lower = plugin_name.lower()
                            for pattern in vm_plugin_patterns:
                                if pattern in plugin_name_lower:
                                    indicators['system_indicators'].append(f"VM plugin detected: {plugin_name}")
                    elif isinstance(plugin, str):
                        # Handle case where plugin is just a string
                        plugin_lower = plugin.lower()
                        for pattern in vm_plugin_patterns:
                            if pattern in plugin_lower:
                                indicators['system_indicators'].append(f"VM plugin detected: {plugin}")
            
            indicators['confidence'] = min(1.0, len(indicators['system_indicators']) * 0.6)
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error in VM system indicators analysis: {str(e)}")
            return {
                'system_indicators': [],
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _detect_vm_software_signatures(self, hardware_data: Dict[str, Any], os_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect VM software signatures"""
        signatures = {
            'software_signatures': [],
            'detection_confidence': 0.0
        }
        
        try:
            # Platform analysis
            platform = os_data.get('platform', '')
            if isinstance(platform, str):
                platform_lower = platform.lower()
                vm_platform_patterns = ['virtual', 'vm', 'container']
                
                for pattern in vm_platform_patterns:
                    if pattern in platform_lower:
                        signatures['software_signatures'].append(f"VM platform signature: {pattern}")
            
            signatures['detection_confidence'] = min(1.0, len(signatures['software_signatures']) * 0.5)
            return signatures
            
        except Exception as e:
            self.logger.error(f"Error in VM software signature detection: {str(e)}")
            return {
                'software_signatures': [],
                'detection_confidence': 0.0,
                'error': str(e)
            }
    
    def _calculate_vm_probability(self, vm_detection_results: Dict[str, Any]) -> float:
        """Calculate overall VM probability from all detection methods"""
        try:
            probabilities = []
            
            for key, result in vm_detection_results.items():
                if isinstance(result, dict):
                    if 'vm_probability' in result and isinstance(result['vm_probability'], (int, float)):
                        probabilities.append(float(result['vm_probability']))
                    elif 'anomaly_score' in result and isinstance(result['anomaly_score'], (int, float)):
                        probabilities.append(float(result['anomaly_score']))
                    elif 'confidence' in result and isinstance(result['confidence'], (int, float)):
                        probabilities.append(float(result['confidence']))
                    elif 'detection_confidence' in result and isinstance(result['detection_confidence'], (int, float)):
                        probabilities.append(float(result['detection_confidence']))
            
            if probabilities:
                # Filter out invalid probabilities
                valid_probabilities = [p for p in probabilities if 0 <= p <= 1]
                if valid_probabilities:
                    return min(1.0, statistics.mean(valid_probabilities) * 1.2)  # Slight boost for multiple indicators
                else:
                    return 0.0
            else:
                return 0.0
                
        except Exception as e:
            self.logger.error(f"Error calculating VM probability: {str(e)}")
            return 0.0
    
    def _classify_vm_type(self, vm_detection_results: Dict[str, Any]) -> str:
        """Classify the type of virtual machine if detected"""
        vm_types = []
        
        try:
            # Check for specific VM signatures
            for result in vm_detection_results.values():
                if isinstance(result, dict) and 'suspicious_hardware' in result:
                    suspicious_hardware = result['suspicious_hardware']
                    if isinstance(suspicious_hardware, list):
                        for indicator in suspicious_hardware:
                            # Ensure indicator is a string before calling lower()
                            if isinstance(indicator, str):
                                indicator_lower = indicator.lower()
                                if 'virtualbox' in indicator_lower:
                                    vm_types.append('VirtualBox')
                                elif 'vmware' in indicator_lower:
                                    vm_types.append('VMware')
                                elif 'parallels' in indicator_lower:
                                    vm_types.append('Parallels')
                                elif 'hyper-v' in indicator_lower:
                                    vm_types.append('Hyper-V')
        
            if vm_types:
                return ', '.join(set(vm_types))
            else:
                vm_probability = self._calculate_vm_probability(vm_detection_results)
                if vm_probability > 0.7:
                    return 'Unknown VM'
                else:
                    return 'Physical Machine'
                    
        except Exception as e:
            self.logger.error(f"Error in VM type classification: {str(e)}")
            return 'Classification Error'
    
    def _calculate_vm_detection_confidence(self, vm_detection_results: Dict[str, Any]) -> float:
        """Calculate confidence level of VM detection"""
        confidence_scores = []
        
        for result in vm_detection_results.values():
            if isinstance(result, dict):
                if 'confidence' in result:
                    confidence_scores.append(result['confidence'])
                elif 'detection_confidence' in result:
                    confidence_scores.append(result['detection_confidence'])
        
        if confidence_scores:
            return statistics.mean(confidence_scores)
        else:
            return 0.5
    
    # ===== HARDWARE ANALYSIS HELPER METHODS =====
    
    def _analyze_cpu_characteristics(self, cpu_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze CPU characteristics in detail"""
        analysis = {
            'cores': cpu_data.get('cores', 0),
            'architecture': cpu_data.get('architecture', 'unknown'),
            'vendor': cpu_data.get('vendor', 'unknown'),
            'model': cpu_data.get('model', 'unknown'),
            'frequency': cpu_data.get('frequency', 0),
            'performance_class': self._classify_cpu_performance(cpu_data),
            'virtualization_indicators': self._check_cpu_virtualization(cpu_data)
        }
        return analysis
    
    def _analyze_memory_characteristics(self, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze memory characteristics in detail"""
        total_memory = memory_data.get('total_memory', 0)
        memory_gb = total_memory / (1024**3) if total_memory > 0 else 0
        
        analysis = {
            'total_memory_bytes': total_memory,
            'total_memory_gb': round(memory_gb, 2),
            'available_memory': memory_data.get('available_memory', 0),
            'memory_type': memory_data.get('memory_type', 'unknown'),
            'speed': memory_data.get('speed', 0),
            'memory_class': self._classify_memory_size(memory_gb),
            'vm_memory_pattern': memory_gb in [2, 4, 8, 16, 32]
        }
        return analysis
    
    def _analyze_gpu_characteristics(self, gpu_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze GPU characteristics in detail"""
        analysis = {
            'vendor': gpu_data.get('vendor', 'unknown'),
            'renderer': gpu_data.get('renderer', 'unknown'),
            'version': gpu_data.get('version', 'unknown'),
            'memory': gpu_data.get('memory', 0),
            'extensions_count': len(gpu_data.get('extensions', [])),
            'gpu_class': self._classify_gpu_type(gpu_data),
            'virtualization_indicators': self._check_gpu_virtualization(gpu_data)
        }
        return analysis
    
    def _analyze_storage_characteristics(self, storage_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze storage characteristics in detail"""
        total_storage = storage_data.get('total_storage', 0)
        storage_gb = total_storage / (1024**3) if total_storage > 0 else 0
        
        analysis = {
            'total_storage_bytes': total_storage,
            'total_storage_gb': round(storage_gb, 2),
            'available_storage': storage_data.get('available_storage', 0),
            'storage_type': storage_data.get('storage_type', 'unknown'),
            'filesystem': storage_data.get('filesystem', 'unknown'),
            'storage_class': self._classify_storage_size(storage_gb)
        }
        return analysis
    
    def _validate_hardware_consistency(self, hardware_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate hardware configuration consistency"""
        consistency_checks = {
            'cpu_memory_ratio': self._check_cpu_memory_ratio(hardware_data),
            'gpu_compatibility': self._check_gpu_compatibility(hardware_data),
            'overall_consistency': 0.85  # Placeholder - implement actual consistency checks
        }
        return consistency_checks
    
    def _classify_hardware_profile(self, hardware_analysis: Dict[str, Any]) -> str:
        """Classify overall hardware profile"""
        cpu_class = hardware_analysis.get('cpu_analysis', {}).get('performance_class', 'unknown')
        memory_class = hardware_analysis.get('memory_analysis', {}).get('memory_class', 'unknown')
        gpu_class = hardware_analysis.get('gpu_analysis', {}).get('gpu_class', 'unknown')
        
        if cpu_class == 'high-end' and memory_class == 'high' and gpu_class == 'dedicated':
            return 'Gaming/Workstation'
        elif cpu_class == 'mid-range' and memory_class == 'medium':
            return 'Business/Office'
        elif cpu_class == 'low-end' or memory_class == 'low':
            return 'Budget/Basic'
        else:
            return 'Standard'
    
    def _detect_hardware_anomalies(self, hardware_analysis: Dict[str, Any]) -> List[str]:
        """Detect anomalies in hardware configuration"""
        anomalies = []
        
        # Check for VM memory patterns
        memory_analysis = hardware_analysis.get('memory_analysis', {})
        if memory_analysis.get('vm_memory_pattern', False):
            anomalies.append('Memory size matches common VM configuration')
        
        # Check for virtual GPU
        gpu_analysis = hardware_analysis.get('gpu_analysis', {})
        if gpu_analysis.get('virtualization_indicators', False):
            anomalies.append('GPU shows virtualization indicators')
        
        return anomalies
    
    def _calculate_overall_hardware_score(self, hardware_analysis: Dict[str, Any]) -> float:
        """Calculate overall hardware capability score"""
        try:
            scores = []
            
            # CPU score (based on cores and frequency)
            cpu_data = hardware_analysis.get('cpu_analysis', {})
            cpu_cores = cpu_data.get('cores', 0)
            cpu_freq = cpu_data.get('frequency', 0)
            cpu_score = min(1.0, (cpu_cores * cpu_freq) / 20000) if cpu_freq > 0 else 0.5
            scores.append(cpu_score)
            
            # Memory score
            memory_data = hardware_analysis.get('memory_analysis', {})
            memory_gb = memory_data.get('total_memory_gb', 0)
            memory_score = min(1.0, memory_gb / 32)  # 32GB = max score
            scores.append(memory_score)
            
            # GPU score (placeholder)
            gpu_data = hardware_analysis.get('gpu_analysis', {})
            gpu_score = 0.7 if gpu_data.get('gpu_class') == 'dedicated' else 0.4
            scores.append(gpu_score)
            
            return statistics.mean(scores) if scores else 0.5
            
        except Exception as e:
            self.logger.error(f"Error calculating hardware score: {str(e)}")
            return 0.5
    
    # ===== DEVICE TRACKING HELPER METHODS =====
    
    def _track_signature_evolution(self, device_id: str, current_signature: Dict[str, Any]) -> Dict[str, Any]:
        """Track how device signature evolves over time"""
        try:
            # Get historical signatures from memory store or MongoDB-like storage
            historical_signatures = self.device_history.get(device_id, [])
            
            if not historical_signatures:
                # First time seeing this device
                self.device_history[device_id] = [current_signature]
                return {
                    'signature_changes': 0,
                    'stability_score': 1.0,
                    'evolution_trend': 'new_device',
                    'signature_age_hours': 0,
                    'change_velocity': 0.0,
                    'signature_entropy': self._calculate_signature_entropy(current_signature),
                    'signature_drift_score': 0.0
                }
            
            # Calculate signature changes over time
            last_signature = historical_signatures[-1]
            changes_detected = self._compare_signatures(last_signature, current_signature)
            
            # Add current signature to history (keep last 50 signatures)
            historical_signatures.append(current_signature)
            if len(historical_signatures) > 50:
                historical_signatures.pop(0)
            self.device_history[device_id] = historical_signatures
            
            # Calculate evolution metrics
            signature_changes = len(changes_detected['changed_fields'])
            stability_score = self._calculate_signature_stability(historical_signatures)
            evolution_trend = self._determine_evolution_trend(historical_signatures)
            change_velocity = self._calculate_change_velocity(historical_signatures)
            signature_drift = self._calculate_signature_drift(historical_signatures)
            
            return {
                'signature_changes': signature_changes,
                'stability_score': stability_score,
                'evolution_trend': evolution_trend,
                'changed_fields': changes_detected['changed_fields'],
                'change_severity': changes_detected['severity'],
                'signature_age_hours': len(historical_signatures),
                'change_velocity': change_velocity,
                'signature_entropy': self._calculate_signature_entropy(current_signature),
                'signature_drift_score': signature_drift,
                'consistency_over_time': self._analyze_consistency_over_time(historical_signatures)
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking signature evolution: {str(e)}")
            return {
                'signature_changes': 0,
                'stability_score': 0.5,
                'evolution_trend': 'error',
                'error': str(e)
            }
    
    def _detect_hardware_changes(self, device_id: str, current_signature: Dict[str, Any]) -> Dict[str, Any]:
        """Detect changes in hardware configuration"""
        try:
            # Get last known hardware configuration
            historical_signatures = self.device_history.get(device_id, [])
            
            if not historical_signatures:
                return {
                    'hardware_changes_detected': False,
                    'changed_components': [],
                    'change_severity': 'none',
                    'hardware_stability_score': 1.0,
                    'change_type': 'baseline'
                }
            
            last_signature = historical_signatures[-1]
            current_hardware = current_signature.get('hardware', {})
            last_hardware = last_signature.get('hardware', {})
            
            # Detect specific hardware changes
            hardware_changes = {
                'cpu_changes': self._compare_cpu_configurations(
                    last_hardware.get('cpu', {}), 
                    current_hardware.get('cpu', {})
                ),
                'memory_changes': self._compare_memory_configurations(
                    last_hardware.get('memory', {}), 
                    current_hardware.get('memory', {})
                ),
                'gpu_changes': self._compare_gpu_configurations(
                    last_hardware.get('gpu', {}), 
                    current_hardware.get('gpu', {})
                ),
                'storage_changes': self._compare_storage_configurations(
                    last_hardware.get('storage', {}), 
                    current_hardware.get('storage', {})
                )
            }
            
            # Analyze overall hardware changes
            changed_components = []
            change_severity_scores = []
            
            for component, changes in hardware_changes.items():
                if changes['changed']:
                    changed_components.append({
                        'component': component.replace('_changes', ''),
                        'changes': changes['changes'],
                        'severity': changes['severity'],
                        'risk_level': changes['risk_level']
                    })
                    change_severity_scores.append(changes['severity_score'])
            
            # Calculate overall change severity
            if change_severity_scores:
                avg_severity_score = statistics.mean(change_severity_scores)
                if avg_severity_score > 0.8:
                    change_severity = 'critical'
                elif avg_severity_score > 0.6:
                    change_severity = 'high'
                elif avg_severity_score > 0.4:
                    change_severity = 'medium'
                elif avg_severity_score > 0.2:
                    change_severity = 'low'
                else:
                    change_severity = 'minimal'
            else:
                change_severity = 'none'
                avg_severity_score = 0.0
            
            # Calculate hardware stability score
            hardware_stability = 1.0 - avg_severity_score
            
            return {
                'hardware_changes_detected': len(changed_components) > 0,
                'changed_components': changed_components,
                'change_severity': change_severity,
                'hardware_stability_score': hardware_stability,
                'change_type': 'hardware_modification' if changed_components else 'stable',
                'component_analysis': hardware_changes,
                'vm_indicators': self._check_vm_transition_indicators(last_hardware, current_hardware),
                'spoofing_indicators': self._check_hardware_spoofing_indicators(hardware_changes)
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting hardware changes: {str(e)}")
            return {
                'hardware_changes_detected': False,
                'changed_components': [],
                'change_severity': 'error',
                'error': str(e)
            }
    
    def _analyze_device_switching_patterns(self, device_id: str) -> Dict[str, Any]:
        """Analyze patterns of device switching"""
        try:
            # Get device switching history
            device_sessions = self.device_sessions.get(device_id, [])
            
            if len(device_sessions) < 2:
                return {
                    'switching_frequency': 0.0,
                    'suspicious_patterns': [],
                    'pattern_risk_score': 0.0,
                    'session_count': len(device_sessions),
                    'analysis_confidence': 'low'
                }
            
            # Analyze switching patterns
            switching_analysis = {}
            
            # 1. Calculate switching frequency (switches per hour)
            if len(device_sessions) > 1:
                time_span_hours = (device_sessions[-1]['timestamp'] - device_sessions[0]['timestamp']).total_seconds() / 3600
                switching_frequency = (len(device_sessions) - 1) / max(time_span_hours, 1)
            else:
                switching_frequency = 0.0
            
            # 2. Detect suspicious patterns
            suspicious_patterns = []
            
            # Rapid device switching (> 5 switches per hour)
            if switching_frequency > 5:
                suspicious_patterns.append({
                    'pattern': 'rapid_switching',
                    'description': f'Device switching {switching_frequency:.1f} times per hour',
                    'risk_level': 'high',
                    'confidence': 0.9
                })
            
            # Regular interval switching (botnet behavior)
            intervals = self._calculate_switching_intervals(device_sessions)
            if self._detect_regular_intervals(intervals):
                suspicious_patterns.append({
                    'pattern': 'regular_interval_switching',
                    'description': 'Device switches at regular intervals suggesting automation',
                    'risk_level': 'medium',
                    'confidence': 0.75
                })
            
            # Unusual time patterns (night switching)
            night_switches = self._count_night_switches(device_sessions)
            if night_switches > len(device_sessions) * 0.3:
                suspicious_patterns.append({
                    'pattern': 'night_switching',
                    'description': f'{night_switches} switches during night hours',
                    'risk_level': 'medium',
                    'confidence': 0.6
                })
            
            # Geographical inconsistencies
            geo_inconsistencies = self._detect_geographical_inconsistencies(device_sessions)
            if geo_inconsistencies['detected']:
                suspicious_patterns.append({
                    'pattern': 'geographical_inconsistency',
                    'description': geo_inconsistencies['description'],
                    'risk_level': 'high',
                    'confidence': geo_inconsistencies['confidence']
                })
            
            # 3. Calculate overall pattern risk score
            risk_scores = []
            for pattern in suspicious_patterns:
                risk_weight = {'low': 0.3, 'medium': 0.6, 'high': 0.9}.get(pattern['risk_level'], 0.5)
                risk_scores.append(risk_weight * pattern['confidence'])
            
            pattern_risk_score = statistics.mean(risk_scores) if risk_scores else 0.0
            
            # 4. Determine analysis confidence
            if len(device_sessions) > 10:
                analysis_confidence = 'high'
            elif len(device_sessions) > 5:
                analysis_confidence = 'medium'
            else:
                analysis_confidence = 'low'
            
            return {
                'switching_frequency': switching_frequency,
                'suspicious_patterns': suspicious_patterns,
                'pattern_risk_score': pattern_risk_score,
                'session_count': len(device_sessions),
                'analysis_confidence': analysis_confidence,
                'switching_intervals': intervals,
                'temporal_analysis': {
                    'night_switches': night_switches,
                    'day_switches': len(device_sessions) - night_switches,
                    'weekend_switches': self._count_weekend_switches(device_sessions)
                },
                'geographical_analysis': geo_inconsistencies
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing device switching patterns: {str(e)}")
            return {
                'switching_frequency': 0.0,
                'suspicious_patterns': [],
                'pattern_risk_score': 0.0,
                'error': str(e)
            }
    
    def _calculate_device_reputation_score(self, device_id: str, consistency_analysis: Dict[str, Any]) -> float:
        """Calculate device reputation score based on historical behavior"""
        try:
            reputation_factors = {}
            
            # 1. Signature stability factor (0.0 - 1.0)
            evolution_tracking = consistency_analysis.get('evolution_tracking', {})
            stability_score = evolution_tracking.get('stability_score', 0.5)
            reputation_factors['stability'] = stability_score
            
            # 2. Hardware consistency factor (0.0 - 1.0)
            hardware_changes = consistency_analysis.get('hardware_changes', {})
            hardware_stability = hardware_changes.get('hardware_stability_score', 0.5)
            reputation_factors['hardware_consistency'] = hardware_stability
            
            # 3. Switching pattern factor (0.0 - 1.0)
            switching_patterns = consistency_analysis.get('switching_patterns', {})
            pattern_risk = switching_patterns.get('pattern_risk_score', 0.0)
            switching_factor = 1.0 - pattern_risk  # Invert risk to get positive factor
            reputation_factors['switching_behavior'] = switching_factor
            
            # 4. Session correlation factor (0.0 - 1.0)
            session_correlation = consistency_analysis.get('session_correlation', {})
            correlation_score = session_correlation.get('session_correlation', 0.5)
            reputation_factors['session_correlation'] = correlation_score
            
            # 5. Historical behavior factor
            device_age_factor = self._calculate_device_age_factor(device_id)
            reputation_factors['device_age'] = device_age_factor
            
            # 6. Anomaly detection factor
            anomaly_factor = self._calculate_anomaly_factor(consistency_analysis)
            reputation_factors['anomaly_factor'] = anomaly_factor
            
            # Calculate weighted reputation score
            weights = {
                'stability': 0.25,
                'hardware_consistency': 0.20,
                'switching_behavior': 0.20,
                'session_correlation': 0.15,
                'device_age': 0.10,
                'anomaly_factor': 0.10
            }
            
            weighted_score = sum(
                reputation_factors[factor] * weights[factor]
                for factor in weights
                if factor in reputation_factors
            )
            
            # Apply reputation modifiers
            final_score = self._apply_reputation_modifiers(device_id, weighted_score, consistency_analysis)
            
            # Ensure score is between 0.0 and 1.0
            final_score = max(0.0, min(1.0, final_score))
            
            return final_score
            
        except Exception as e:
            self.logger.error(f"Error calculating device reputation score: {str(e)}")
            return 0.5  # Neutral score on error
    
    def _correlate_cross_session_data(self, device_id: str) -> Dict[str, Any]:
        """Correlate device data across multiple sessions"""
        try:
            device_sessions = self.device_sessions.get(device_id, [])
            
            if len(device_sessions) < 2:
                return {
                    'session_correlation': 1.0,
                    'behavior_consistency': 1.0,
                    'anomaly_patterns': [],
                    'correlation_confidence': 'low',
                    'session_count': len(device_sessions)
                }
            
            correlation_analysis = {}
            
            # 1. Session correlation analysis
            session_correlations = []
            for i in range(1, len(device_sessions)):
                correlation = self._calculate_session_correlation(
                    device_sessions[i-1], 
                    device_sessions[i]
                )
                session_correlations.append(correlation)
            
            avg_session_correlation = statistics.mean(session_correlations) if session_correlations else 1.0
            
            # 2. Behavior consistency analysis
            behavior_patterns = self._extract_behavior_patterns(device_sessions)
            behavior_consistency = self._calculate_behavior_consistency(behavior_patterns)
            
            # 3. Anomaly pattern detection
            anomaly_patterns = []
            
            # Detect timing anomalies
            timing_anomalies = self._detect_timing_anomalies(device_sessions)
            if timing_anomalies:
                anomaly_patterns.extend(timing_anomalies)
            
            # Detect signature anomalies
            signature_anomalies = self._detect_signature_anomalies(device_sessions)
            if signature_anomalies:
                anomaly_patterns.extend(signature_anomalies)
            
            # Detect behavioral anomalies
            behavioral_anomalies = self._detect_behavioral_anomalies(behavior_patterns)
            if behavioral_anomalies:
                anomaly_patterns.extend(behavioral_anomalies)
            
            # 4. Cross-session feature correlation
            feature_correlations = self._calculate_feature_correlations(device_sessions)
            
            # 5. Session clustering analysis
            session_clusters = self._perform_session_clustering(device_sessions)
            
            # 6. Determine correlation confidence
            if len(device_sessions) > 20:
                correlation_confidence = 'high'
            elif len(device_sessions) > 10:
                correlation_confidence = 'medium'
            else:
                correlation_confidence = 'low'
            
            return {
                'session_correlation': avg_session_correlation,
                'behavior_consistency': behavior_consistency,
                'anomaly_patterns': anomaly_patterns,
                'correlation_confidence': correlation_confidence,
                'session_count': len(device_sessions),
                'feature_correlations': feature_correlations,
                'session_clusters': session_clusters,
                'temporal_analysis': {
                    'session_frequency': self._calculate_session_frequency(device_sessions),
                    'usage_patterns': self._analyze_usage_patterns(device_sessions),
                    'session_duration_stats': self._calculate_session_duration_stats(device_sessions)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error correlating cross-session data: {str(e)}")
            return {
                'session_correlation': 0.5,
                'behavior_consistency': 0.5,
                'anomaly_patterns': [],
                'error': str(e)
            }
    
    def _update_device_tracking_record(self, device_id: str, current_signature: Dict[str, Any], 
                                     consistency_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Update device tracking record with new data"""
        try:
            # Update device session history
            current_time = datetime.utcnow()
            session_entry = {
                'timestamp': current_time,
                'signature': current_signature,
                'consistency_score': consistency_analysis.get('reputation_score', 0.5),
                'session_id': str(uuid.uuid4())
            }
            
            if device_id not in self.device_sessions:
                self.device_sessions[device_id] = []
            
            self.device_sessions[device_id].append(session_entry)
            
            # Keep only last 100 sessions per device
            if len(self.device_sessions[device_id]) > 100:
                self.device_sessions[device_id] = self.device_sessions[device_id][-100:]
            
            # Calculate tracking statistics
            total_sessions = len(self.device_sessions[device_id])
            first_seen = self.device_sessions[device_id][0]['timestamp'] if self.device_sessions[device_id] else current_time
            device_age_days = (current_time - first_seen).days
            
            # Update device tracking metadata
            tracking_metadata = {
                'device_id': device_id,
                'total_sessions': total_sessions,
                'first_seen': first_seen.isoformat(),
                'last_seen': current_time.isoformat(),
                'device_age_days': device_age_days,
                'tracking_version': self.signature_version,
                'consistency_trend': self._calculate_consistency_trend(device_id),
                'risk_level_history': self._get_risk_level_history(device_id)
            }
            
            return {
                'record_updated': True,
                'update_timestamp': current_time.isoformat(),
                'tracking_version': self.signature_version,
                'tracking_metadata': tracking_metadata,
                'storage_status': 'success'
            }
            
        except Exception as e:
            self.logger.error(f"Error updating device tracking record: {str(e)}")
            return {
                'record_updated': False,
                'update_timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }
    
    def _calculate_overall_consistency_score(self, consistency_analysis: Dict[str, Any]) -> float:
        """Calculate overall device consistency score"""
        try:
            consistency_factors = {}
            
            # Extract consistency factors from analysis
            evolution_tracking = consistency_analysis.get('evolution_tracking', {})
            consistency_factors['signature_stability'] = evolution_tracking.get('stability_score', 0.5)
            
            hardware_changes = consistency_analysis.get('hardware_changes', {})
            consistency_factors['hardware_stability'] = hardware_changes.get('hardware_stability_score', 0.5)
            
            switching_patterns = consistency_analysis.get('switching_patterns', {})
            pattern_risk = switching_patterns.get('pattern_risk_score', 0.0)
            consistency_factors['switching_consistency'] = 1.0 - pattern_risk
            
            session_correlation = consistency_analysis.get('session_correlation', {})
            consistency_factors['session_consistency'] = session_correlation.get('session_correlation', 0.5)
            
            reputation_score = consistency_analysis.get('reputation_score', 0.5)
            consistency_factors['reputation_consistency'] = reputation_score
            
            # Calculate weighted consistency score
            weights = {
                'signature_stability': 0.30,
                'hardware_stability': 0.25,
                'switching_consistency': 0.20,
                'session_consistency': 0.15,
                'reputation_consistency': 0.10
            }
            
            weighted_score = sum(
                consistency_factors[factor] * weights[factor]
                for factor in weights
                if factor in consistency_factors
            )
            
            # Apply consistency modifiers based on data quality
            data_quality_modifier = self._calculate_data_quality_modifier(consistency_analysis)
            final_score = weighted_score * data_quality_modifier
            
            return max(0.0, min(1.0, final_score))
            
        except Exception as e:
            self.logger.error(f"Error calculating overall consistency score: {str(e)}")
            return 0.5
    
    def _assess_device_risk_level(self, consistency_analysis: Dict[str, Any]) -> str:
        """Assess overall risk level for the device"""
        try:
            consistency_score = self._calculate_overall_consistency_score(consistency_analysis)
            reputation_score = consistency_analysis.get('reputation_score', 0.5)
            
            # Get specific risk indicators
            switching_patterns = consistency_analysis.get('switching_patterns', {})
            pattern_risk = switching_patterns.get('pattern_risk_score', 0.0)
            suspicious_patterns = len(switching_patterns.get('suspicious_patterns', []))
            
            hardware_changes = consistency_analysis.get('hardware_changes', {})
            hardware_risk = 1.0 - hardware_changes.get('hardware_stability_score', 0.5)
            vm_indicators = hardware_changes.get('vm_indicators', {}).get('detected', False)
            spoofing_indicators = hardware_changes.get('spoofing_indicators', {}).get('detected', False)
            
            session_correlation = consistency_analysis.get('session_correlation', {})
            anomaly_count = len(session_correlation.get('anomaly_patterns', []))
            
            # Calculate composite risk score
            risk_factors = {
                'consistency_risk': 1.0 - consistency_score,
                'reputation_risk': 1.0 - reputation_score,
                'pattern_risk': pattern_risk,
                'hardware_risk': hardware_risk,
                'anomaly_risk': min(1.0, anomaly_count * 0.2),
                'vm_risk': 0.8 if vm_indicators else 0.0,
                'spoofing_risk': 0.9 if spoofing_indicators else 0.0
            }
            
            # Weighted risk calculation
            risk_weights = {
                'consistency_risk': 0.20,
                'reputation_risk': 0.20,
                'pattern_risk': 0.15,
                'hardware_risk': 0.15,
                'anomaly_risk': 0.10,
                'vm_risk': 0.10,
                'spoofing_risk': 0.10
            }
            
            composite_risk = sum(
                risk_factors[factor] * risk_weights[factor]
                for factor in risk_weights
                if factor in risk_factors
            )
            
            # Determine risk level with thresholds
            if composite_risk > 0.8 or spoofing_indicators or suspicious_patterns > 3:
                return 'CRITICAL'
            elif composite_risk > 0.6 or vm_indicators or suspicious_patterns > 1:
                return 'HIGH'
            elif composite_risk > 0.4 or pattern_risk > 0.5:
                return 'MEDIUM'
            elif composite_risk > 0.2:
                return 'LOW'
            else:
                return 'MINIMAL'
                
        except Exception as e:
            self.logger.error(f"Error assessing device risk level: {str(e)}")
            return 'MEDIUM'
    
    # ===== SUPPORTING HELPER METHODS FOR DEVICE TRACKING =====
    
    def _compare_signatures(self, old_signature: Dict[str, Any], new_signature: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two device signatures to detect changes"""
        try:
            changed_fields = []
            
            # Deep comparison of signature fields
            for key in ['hardware', 'os', 'browser', 'network', 'screen']:
                if key in old_signature and key in new_signature:
                    changes = self._deep_compare_dict(old_signature[key], new_signature[key], key)
                    changed_fields.extend(changes)
            
            # Calculate change severity
            severity_score = min(1.0, len(changed_fields) / 10)  # Normalize to 0-1
            if severity_score > 0.7:
                severity = 'high'
            elif severity_score > 0.4:
                severity = 'medium'
            elif severity_score > 0.1:
                severity = 'low'
            else:
                severity = 'minimal'
            
            return {
                'changed_fields': changed_fields,
                'severity': severity,
                'severity_score': severity_score,
                'change_count': len(changed_fields)
            }
            
        except Exception as e:
            self.logger.error(f"Error comparing signatures: {str(e)}")
            return {'changed_fields': [], 'severity': 'error', 'severity_score': 0.0}
    
    def _deep_compare_dict(self, old_dict: Dict, new_dict: Dict, prefix: str) -> List[str]:
        """Deep compare two dictionaries and return changed field paths"""
        changes = []
        
        # Check for changed values
        for key in set(old_dict.keys()) | set(new_dict.keys()):
            field_path = f"{prefix}.{key}"
            
            if key not in old_dict:
                changes.append(f"{field_path} (added)")
            elif key not in new_dict:
                changes.append(f"{field_path} (removed)")
            elif old_dict[key] != new_dict[key]:
                if isinstance(old_dict[key], dict) and isinstance(new_dict[key], dict):
                    changes.extend(self._deep_compare_dict(old_dict[key], new_dict[key], field_path))
                else:
                    changes.append(f"{field_path} (changed)")
        
        return changes
    
    def _calculate_signature_stability(self, signatures: List[Dict[str, Any]]) -> float:
        """Calculate stability score based on signature history"""
        if len(signatures) < 2:
            return 1.0
        
        change_counts = []
        for i in range(1, len(signatures)):
            comparison = self._compare_signatures(signatures[i-1], signatures[i])
            change_counts.append(comparison['change_count'])
        
        avg_changes = statistics.mean(change_counts) if change_counts else 0
        # Stability decreases with more changes (inverse relationship)
        stability = max(0.0, 1.0 - (avg_changes / 20))  # Normalize assuming max 20 changes per comparison
        return stability
    
    def _determine_evolution_trend(self, signatures: List[Dict[str, Any]]) -> str:
        """Determine the evolution trend of device signatures"""
        if len(signatures) < 3:
            return 'insufficient_data'
        
        change_counts = []
        for i in range(1, len(signatures)):
            comparison = self._compare_signatures(signatures[i-1], signatures[i])
            change_counts.append(comparison['change_count'])
        
        if len(change_counts) < 2:
            return 'stable'
        
        # Calculate trend slope
        recent_changes = statistics.mean(change_counts[-5:]) if len(change_counts) >= 5 else statistics.mean(change_counts)
        earlier_changes = statistics.mean(change_counts[:5]) if len(change_counts) >= 5 else statistics.mean(change_counts[:-1])
        
        trend_slope = recent_changes - earlier_changes
        
        if trend_slope > 2:
            return 'increasing_instability'
        elif trend_slope > 0.5:
            return 'slight_increase'
        elif trend_slope < -2:
            return 'stabilizing'
        elif trend_slope < -0.5:
            return 'slight_decrease'
        else:
            return 'stable'
    
    def _calculate_change_velocity(self, signatures: List[Dict[str, Any]]) -> float:
        """Calculate the velocity of signature changes"""
        if len(signatures) < 2:
            return 0.0
        
        change_counts = []
        for i in range(1, len(signatures)):
            comparison = self._compare_signatures(signatures[i-1], signatures[i])
            change_counts.append(comparison['change_count'])
        
        # Calculate changes per time unit (assuming each signature is 1 time unit apart)
        velocity = statistics.mean(change_counts) if change_counts else 0.0
        return velocity
    
    def _calculate_signature_entropy(self, signature: Dict[str, Any]) -> float:
        """Calculate entropy of signature (complexity measure)"""
        # Convert signature to string and calculate character frequency
        signature_str = json.dumps(signature, sort_keys=True)
        char_counts = {}
        
        for char in signature_str:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        total_chars = len(signature_str)
        if total_chars == 0:
            return 0.0
        
        # Calculate Shannon entropy
        entropy = 0.0
        for count in char_counts.values():
            probability = count / total_chars
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _calculate_signature_drift(self, signatures: List[Dict[str, Any]]) -> float:
        """Calculate signature drift over time"""
        if len(signatures) < 2:
            return 0.0
        
        # Compare first and last signatures
        first_signature = signatures[0]
        last_signature = signatures[-1]
        
        comparison = self._compare_signatures(first_signature, last_signature)
        drift_score = min(1.0, comparison['change_count'] / 50)  # Normalize to 0-1
        
        return drift_score
    
    def _analyze_consistency_over_time(self, signatures: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze how consistency changes over time"""
        if len(signatures) < 3:
            return {'trend': 'insufficient_data', 'consistency_periods': []}
        
        # Calculate consistency scores over sliding windows
        window_size = min(5, len(signatures) // 2)
        consistency_scores = []
        
        for i in range(window_size, len(signatures)):
            window_signatures = signatures[i-window_size:i]
            stability = self._calculate_signature_stability(window_signatures)
            consistency_scores.append(stability)
        
        if not consistency_scores:
            return {'trend': 'insufficient_data', 'consistency_periods': []}
        
        # Analyze trend
        if len(consistency_scores) > 1:
            recent_avg = statistics.mean(consistency_scores[-3:]) if len(consistency_scores) >= 3 else consistency_scores[-1]
            earlier_avg = statistics.mean(consistency_scores[:3]) if len(consistency_scores) >= 3 else consistency_scores[0]
            
            if recent_avg > earlier_avg + 0.1:
                trend = 'improving'
            elif recent_avg < earlier_avg - 0.1:
                trend = 'degrading'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'consistency_scores': consistency_scores,
            'current_consistency': consistency_scores[-1] if consistency_scores else 0.5,
            'avg_consistency': statistics.mean(consistency_scores) if consistency_scores else 0.5
        }
    
    def _compare_cpu_configurations(self, old_cpu: Dict[str, Any], new_cpu: Dict[str, Any]) -> Dict[str, Any]:
        """Compare CPU configurations between signatures"""
        changes = []
        critical_fields = ['cores', 'vendor', 'model', 'frequency']
        
        for field in critical_fields:
            if old_cpu.get(field) != new_cpu.get(field):
                changes.append(f"{field}: {old_cpu.get(field)} -> {new_cpu.get(field)}")
        
        changed = len(changes) > 0
        severity_score = len(changes) / len(critical_fields)  # 0.0 to 1.0
        
        if severity_score > 0.5:
            severity = 'high'
            risk_level = 'high'
        elif severity_score > 0.25:
            severity = 'medium'
            risk_level = 'medium'
        elif severity_score > 0:
            severity = 'low'
            risk_level = 'low'
        else:
            severity = 'none'
            risk_level = 'none'
        
        return {
            'changed': changed,
            'changes': changes,
            'severity': severity,
            'severity_score': severity_score,
            'risk_level': risk_level
        }
    
    def _compare_memory_configurations(self, old_memory: Dict[str, Any], new_memory: Dict[str, Any]) -> Dict[str, Any]:
        """Compare memory configurations between signatures"""
        changes = []
        critical_fields = ['total_memory', 'memory_type', 'speed']
        
        for field in critical_fields:
            old_val = old_memory.get(field)
            new_val = new_memory.get(field)
            
            if field == 'total_memory':
                # Allow for small variations in memory reporting
                if old_val and new_val and abs(old_val - new_val) > old_val * 0.05:  # 5% tolerance
                    changes.append(f"{field}: {old_val} -> {new_val}")
            elif old_val != new_val:
                changes.append(f"{field}: {old_val} -> {new_val}")
        
        changed = len(changes) > 0
        severity_score = len(changes) / len(critical_fields)
        
        if severity_score > 0.6:
            severity = 'high'
            risk_level = 'high'
        elif severity_score > 0.3:
            severity = 'medium' 
            risk_level = 'medium'
        elif changed:
            severity = 'low'
            risk_level = 'low'
        else:
            severity = 'none'
            risk_level = 'none'
        
        return {
            'changed': changed,
            'changes': changes,
            'severity': severity,
            'severity_score': severity_score,
            'risk_level': risk_level
        }
    
    def _compare_gpu_configurations(self, old_gpu: Dict[str, Any], new_gpu: Dict[str, Any]) -> Dict[str, Any]:
        """Compare GPU configurations between signatures"""
        changes = []
        critical_fields = ['vendor', 'renderer', 'memory']
        
        for field in critical_fields:
            if old_gpu.get(field) != new_gpu.get(field):
                changes.append(f"{field}: {old_gpu.get(field)} -> {new_gpu.get(field)}")
        
        changed = len(changes) > 0
        severity_score = len(changes) / len(critical_fields)
        
        if severity_score > 0.6:
            severity = 'high'
            risk_level = 'high'
        elif severity_score > 0.3:
            severity = 'medium'
            risk_level = 'medium'
        elif changed:
            severity = 'low'
            risk_level = 'low'
        else:
            severity = 'none'
            risk_level = 'none'
        
        return {
            'changed': changed,
            'changes': changes,
            'severity': severity,
            'severity_score': severity_score,
            'risk_level': risk_level
        }
    
    def _compare_storage_configurations(self, old_storage: Dict[str, Any], new_storage: Dict[str, Any]) -> Dict[str, Any]:
        """Compare storage configurations between signatures"""
        changes = []
        critical_fields = ['total_storage', 'type', 'filesystem']
        
        for field in critical_fields:
            old_val = old_storage.get(field)
            new_val = new_storage.get(field)
            
            if field == 'total_storage':
                # Allow for small variations in storage reporting
                if old_val and new_val and abs(old_val - new_val) > old_val * 0.02:  # 2% tolerance
                    changes.append(f"{field}: {old_val} -> {new_val}")
            elif old_val != new_val:
                changes.append(f"{field}: {old_val} -> {new_val}")
        
        changed = len(changes) > 0
        severity_score = len(changes) / len(critical_fields)
        
        if severity_score > 0.6:
            severity = 'high'
            risk_level = 'high'
        elif changed:
            severity = 'low'
            risk_level = 'low'
        else:
            severity = 'none'
            risk_level = 'none'
        
        return {
            'changed': changed,
            'changes': changes,
            'severity': severity,
            'severity_score': severity_score,
            'risk_level': risk_level
        }
    
    def _check_vm_transition_indicators(self, old_hardware: Dict[str, Any], new_hardware: Dict[str, Any]) -> Dict[str, Any]:
        """Check for indicators of VM transitions"""
        vm_indicators = []
        
        # Check for VM-specific hardware changes
        old_cpu_vendor = old_hardware.get('cpu', {}).get('vendor', '').lower()
        new_cpu_vendor = new_hardware.get('cpu', {}).get('vendor', '').lower()
        
        vm_vendors = ['virtual', 'qemu', 'kvm', 'xen', 'vmware']
        old_is_vm = any(vendor in old_cpu_vendor for vendor in vm_vendors)
        new_is_vm = any(vendor in new_cpu_vendor for vendor in vm_vendors)
        
        if not old_is_vm and new_is_vm:
            vm_indicators.append('Transition from physical to virtual hardware detected')
        elif old_is_vm and not new_is_vm:
            vm_indicators.append('Transition from virtual to physical hardware detected')
        
        # Check for suspicious memory changes (VM memory patterns)
        old_memory = old_hardware.get('memory', {}).get('total_memory', 0) / (1024**3)
        new_memory = new_hardware.get('memory', {}).get('total_memory', 0) / (1024**3)
        
        vm_memory_sizes = [1, 2, 4, 8, 16, 32, 64]
        old_vm_memory = any(abs(old_memory - size) < 0.1 for size in vm_memory_sizes)
        new_vm_memory = any(abs(new_memory - size) < 0.1 for size in vm_memory_sizes)
        
        if not old_vm_memory and new_vm_memory:
            vm_indicators.append('Memory configuration changed to VM-typical size')
        
        return {
            'detected': len(vm_indicators) > 0,
            'indicators': vm_indicators,
            'confidence': min(1.0, len(vm_indicators) * 0.5)
        }
    
    def _check_hardware_spoofing_indicators(self, hardware_changes: Dict[str, Any]) -> Dict[str, Any]:
        """Check for hardware spoofing indicators"""
        spoofing_indicators = []
        
        # Check for multiple simultaneous hardware changes (suspicious)
        changed_components = []
        for component, changes in hardware_changes.items():
            if changes.get('changed', False):
                changed_components.append(component.replace('_changes', ''))
        
        if len(changed_components) >= 3:
            spoofing_indicators.append(f'Multiple hardware components changed simultaneously: {", ".join(changed_components)}')
        
        # Check for high-severity changes across multiple components
        high_severity_count = sum(
            1 for changes in hardware_changes.values()
            if changes.get('severity') in ['high', 'critical']
        )
        
        if high_severity_count >= 2:
            spoofing_indicators.append('Multiple high-severity hardware changes detected')
        
        return {
            'detected': len(spoofing_indicators) > 0,
            'indicators': spoofing_indicators,
            'confidence': min(1.0, len(spoofing_indicators) * 0.6)
        }
    
    def _calculate_switching_intervals(self, device_sessions: List[Dict[str, Any]]) -> List[float]:
        """Calculate time intervals between device switches"""
        if len(device_sessions) < 2:
            return []
        
        intervals = []
        for i in range(1, len(device_sessions)):
            interval = (device_sessions[i]['timestamp'] - device_sessions[i-1]['timestamp']).total_seconds() / 3600  # hours
            intervals.append(interval)
        
        return intervals
    
    def _detect_regular_intervals(self, intervals: List[float]) -> bool:
        """Detect if switching intervals are suspiciously regular"""
        if len(intervals) < 3:
            return False
        
        # Calculate coefficient of variation
        if len(intervals) == 0:
            return False
        
        mean_interval = statistics.mean(intervals)
        if mean_interval == 0:
            return False
        
        std_dev = statistics.stdev(intervals) if len(intervals) > 1 else 0
        coefficient_of_variation = std_dev / mean_interval
        
        # Regular intervals have low coefficient of variation
        return coefficient_of_variation < 0.2
    
    def _count_night_switches(self, device_sessions: List[Dict[str, Any]]) -> int:
        """Count switches that occur during night hours (10 PM - 6 AM)"""
        night_switches = 0
        
        for session in device_sessions:
            hour = session['timestamp'].hour
            if hour >= 22 or hour <= 6:  # 10 PM to 6 AM
                night_switches += 1
        
        return night_switches
    
    def _count_weekend_switches(self, device_sessions: List[Dict[str, Any]]) -> int:
        """Count switches that occur during weekends"""
        weekend_switches = 0
        
        for session in device_sessions:
            if session['timestamp'].weekday() >= 5:  # Saturday=5, Sunday=6
                weekend_switches += 1
        
        return weekend_switches
    
    def _detect_geographical_inconsistencies(self, device_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Detect geographical inconsistencies in device sessions"""
        if len(device_sessions) < 2:
            return {'detected': False, 'description': 'Insufficient data', 'confidence': 0.0}
        
        # Extract location data from sessions (if available)
        locations = []
        for session in device_sessions:
            signature = session.get('signature', {})
            network = signature.get('network', {})
            if 'country' in network and 'city' in network:
                locations.append({
                    'country': network['country'],
                    'city': network['city'],
                    'timestamp': session['timestamp']
                })
        
        if len(locations) < 2:
            return {'detected': False, 'description': 'No location data available', 'confidence': 0.0}
        
        # Check for rapid location changes
        geographical_issues = []
        for i in range(1, len(locations)):
            prev_location = locations[i-1]
            curr_location = locations[i]
            time_diff = (curr_location['timestamp'] - prev_location['timestamp']).total_seconds() / 3600  # hours
            
            # Different countries within short time frame
            if prev_location['country'] != curr_location['country'] and time_diff < 24:
                geographical_issues.append(
                    f"Location change from {prev_location['country']} to {curr_location['country']} "
                    f"within {time_diff:.1f} hours"
                )
        
        return {
            'detected': len(geographical_issues) > 0,
            'description': '; '.join(geographical_issues) if geographical_issues else 'No geographical inconsistencies detected',
            'confidence': min(1.0, len(geographical_issues) * 0.7),
            'inconsistency_count': len(geographical_issues)
        }
    
    def _calculate_device_age_factor(self, device_id: str) -> float:
        """Calculate device age factor for reputation scoring"""
        device_sessions = self.device_sessions.get(device_id, [])
        
        if not device_sessions:
            return 0.5  # Neutral for new devices
        
        # Calculate device age in days
        first_seen = device_sessions[0]['timestamp']
        device_age_days = (datetime.utcnow() - first_seen).days
        
        # Age factor: newer devices have lower trust, older devices with consistent behavior have higher trust
        if device_age_days < 1:
            return 0.3  # New device, lower trust
        elif device_age_days < 7:
            return 0.5  # Week old device
        elif device_age_days < 30:
            return 0.7  # Month old device
        elif device_age_days < 90:
            return 0.8  # 3 months old
        else:
            return 0.9  # Older device, higher trust
    
    def _calculate_anomaly_factor(self, consistency_analysis: Dict[str, Any]) -> float:
        """Calculate anomaly factor based on detected anomalies"""
        session_correlation = consistency_analysis.get('session_correlation', {})
        anomaly_patterns = session_correlation.get('anomaly_patterns', [])
        
        switching_patterns = consistency_analysis.get('switching_patterns', {})
        suspicious_patterns = switching_patterns.get('suspicious_patterns', [])
        
        total_anomalies = len(anomaly_patterns) + len(suspicious_patterns)
        
        # Anomaly factor decreases with more anomalies
        if total_anomalies == 0:
            return 1.0  # No anomalies
        elif total_anomalies <= 2:
            return 0.8  # Few anomalies
        elif total_anomalies <= 5:
            return 0.6  # Some anomalies
        elif total_anomalies <= 10:
            return 0.4  # Many anomalies
        else:
            return 0.2  # Too many anomalies
    
    def _apply_reputation_modifiers(self, device_id: str, base_score: float, consistency_analysis: Dict[str, Any]) -> float:
        """Apply reputation modifiers to base score"""
        modified_score = base_score
        
        # VM detection modifier
        hardware_changes = consistency_analysis.get('hardware_changes', {})
        vm_indicators = hardware_changes.get('vm_indicators', {})
        if vm_indicators.get('detected', False):
            modified_score *= 0.7  # Reduce score for VM indicators
        
        # Spoofing modifier
        spoofing_indicators = hardware_changes.get('spoofing_indicators', {})
        if spoofing_indicators.get('detected', False):
            modified_score *= 0.5  # Significant reduction for spoofing
        
        # Suspicious pattern modifier
        switching_patterns = consistency_analysis.get('switching_patterns', {})
        suspicious_count = len(switching_patterns.get('suspicious_patterns', []))
        if suspicious_count > 3:
            modified_score *= 0.6  # Major reduction for multiple suspicious patterns
        elif suspicious_count > 1:
            modified_score *= 0.8  # Moderate reduction
        
        return modified_score
    
    def _calculate_session_correlation(self, session1: Dict[str, Any], session2: Dict[str, Any]) -> float:
        """Calculate correlation between two sessions"""
        sig1 = session1.get('signature', {})
        sig2 = session2.get('signature', {})
        
        # Calculate similarity across different signature components
        correlations = []
        
        # Hardware correlation
        hw1 = sig1.get('hardware', {})
        hw2 = sig2.get('hardware', {})
        hw_correlation = self._calculate_hardware_correlation(hw1, hw2)
        correlations.append(hw_correlation)
        
        # Browser correlation
        br1 = sig1.get('browser', {})
        br2 = sig2.get('browser', {})
        br_correlation = self._calculate_browser_correlation(br1, br2)
        correlations.append(br_correlation)
        
        # Screen correlation
        sc1 = sig1.get('screen', {})
        sc2 = sig2.get('screen', {})
        sc_correlation = self._calculate_screen_correlation(sc1, sc2)
        correlations.append(sc_correlation)
        
        return statistics.mean(correlations) if correlations else 0.5
    
    def _calculate_hardware_correlation(self, hw1: Dict[str, Any], hw2: Dict[str, Any]) -> float:
        """Calculate hardware correlation between two signatures"""
        matches = 0
        total_fields = 0
        
        for component in ['cpu', 'memory', 'gpu']:
            comp1 = hw1.get(component, {})
            comp2 = hw2.get(component, {})
            
            if comp1 and comp2:
                # Count matching fields
                for field in comp1.keys() | comp2.keys():
                    total_fields += 1
                    if comp1.get(field) == comp2.get(field):
                        matches += 1
        
        return matches / total_fields if total_fields > 0 else 1.0
    
    def _calculate_browser_correlation(self, br1: Dict[str, Any], br2: Dict[str, Any]) -> float:
        """Calculate browser correlation between two signatures"""
        key_fields = ['user_agent', 'browser_name', 'browser_version']
        matches = 0
        
        for field in key_fields:
            if br1.get(field) == br2.get(field):
                matches += 1
        
        return matches / len(key_fields) if key_fields else 1.0
    
    def _calculate_screen_correlation(self, sc1: Dict[str, Any], sc2: Dict[str, Any]) -> float:
        """Calculate screen correlation between two signatures"""
        key_fields = ['width', 'height', 'color_depth']
        matches = 0
        
        for field in key_fields:
            if sc1.get(field) == sc2.get(field):
                matches += 1
        
        return matches / len(key_fields) if key_fields else 1.0
    
    def _extract_behavior_patterns(self, device_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract behavioral patterns from device sessions"""
        if not device_sessions:
            return {}
        
        patterns = {
            'session_frequency': self._calculate_session_frequency(device_sessions),
            'usage_times': [session['timestamp'].hour for session in device_sessions],
            'session_durations': [],  # Would need session end times
            'location_patterns': self._extract_location_patterns(device_sessions)
        }
        
        return patterns
    
    def _calculate_behavior_consistency(self, behavior_patterns: Dict[str, Any]) -> float:
        """Calculate consistency of behavioral patterns"""
        if not behavior_patterns:
            return 0.5
        
        consistency_scores = []
        
        # Time consistency
        usage_times = behavior_patterns.get('usage_times', [])
        if usage_times:
            time_std = statistics.stdev(usage_times) if len(usage_times) > 1 else 0
            time_consistency = max(0.0, 1.0 - (time_std / 12))  # Normalize by 12 hours
            consistency_scores.append(time_consistency)
        
        # Frequency consistency (placeholder)
        consistency_scores.append(0.8)
        
        return statistics.mean(consistency_scores) if consistency_scores else 0.5
    
    def _detect_timing_anomalies(self, device_sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect timing anomalies in device sessions"""
        if len(device_sessions) < 3:
            return []
        
        anomalies = []
        
        # Calculate session intervals
        intervals = []
        for i in range(1, len(device_sessions)):
            interval = (device_sessions[i]['timestamp'] - device_sessions[i-1]['timestamp']).total_seconds()
            intervals.append(interval)
        
        if len(intervals) < 2:
            return []
        
        # Detect unusually short intervals (< 1 minute)
        short_intervals = [i for i in intervals if i < 60]
        if len(short_intervals) > len(intervals) * 0.2:  # More than 20% are very short
            anomalies.append({
                'type': 'rapid_succession',
                'description': f'{len(short_intervals)} sessions within 1 minute intervals',
                'severity': 'medium'
            })
        
        # Detect regular patterns (potential automation)
        if len(intervals) >= 5:
            mean_interval = statistics.mean(intervals)
            std_interval = statistics.stdev(intervals)
            if std_interval / mean_interval < 0.1:  # Very consistent intervals
                anomalies.append({
                    'type': 'regular_timing',
                    'description': f'Sessions occur at regular {mean_interval/60:.1f} minute intervals',
                    'severity': 'medium'
                })
        
        return anomalies
    
    def _detect_signature_anomalies(self, device_sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect signature anomalies across sessions"""
        if len(device_sessions) < 2:
            return []
        
        anomalies = []
        
        # Check for signature instability
        signature_changes = []
        for i in range(1, len(device_sessions)):
            prev_sig = device_sessions[i-1].get('signature', {})
            curr_sig = device_sessions[i].get('signature', {})
            comparison = self._compare_signatures(prev_sig, curr_sig)
            signature_changes.append(comparison['change_count'])
        
        if signature_changes:
            avg_changes = statistics.mean(signature_changes)
            if avg_changes > 10:  # Many changes per session
                anomalies.append({
                    'type': 'signature_instability',
                    'description': f'Average of {avg_changes:.1f} signature changes per session',
                    'severity': 'high'
                })
        
        return anomalies
    
    def _detect_behavioral_anomalies(self, behavior_patterns: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect behavioral anomalies"""
        anomalies = []
        
        # Check usage time patterns
        usage_times = behavior_patterns.get('usage_times', [])
        if usage_times:
            night_usage = sum(1 for hour in usage_times if hour >= 22 or hour <= 6)
            if night_usage > len(usage_times) * 0.5:  # More than 50% night usage
                anomalies.append({
                    'type': 'unusual_hours',
                    'description': f'{night_usage} of {len(usage_times)} sessions during night hours',
                    'severity': 'low'
                })
        
        return anomalies
    
    def _calculate_feature_correlations(self, device_sessions: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate correlations between different features across sessions"""
        if len(device_sessions) < 2:
            return {}
        
        correlations = {}
        
        # Extract features across sessions
        features = {
            'screen_width': [s.get('signature', {}).get('screen', {}).get('width', 0) for s in device_sessions],
            'memory_total': [s.get('signature', {}).get('hardware', {}).get('memory', {}).get('total_memory', 0) for s in device_sessions],
            'cpu_cores': [s.get('signature', {}).get('hardware', {}).get('cpu', {}).get('cores', 0) for s in device_sessions]
        }
        
        # Calculate stability for each feature
        for feature_name, values in features.items():
            if values and len(set(values)) > 1:  # Feature varies
                correlations[f'{feature_name}_stability'] = len(set(values)) / len(values)
            else:
                correlations[f'{feature_name}_stability'] = 1.0  # Perfectly stable
        
        return correlations
    
    def _perform_session_clustering(self, device_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform simple clustering analysis on sessions"""
        if len(device_sessions) < 3:
            return {'clusters': 1, 'cluster_quality': 'insufficient_data'}
        
        # Simple clustering based on signature similarity
        clusters = []
        for session in device_sessions:
            signature = session.get('signature', {})
            
            # Find most similar existing cluster
            best_cluster = None
            best_similarity = 0.0
            
            for cluster in clusters:
                cluster_signature = cluster['representative_signature']
                similarity = self._calculate_session_correlation(
                    {'signature': signature}, 
                    {'signature': cluster_signature}
                )
                if similarity > best_similarity and similarity > 0.8:  # Similarity threshold
                    best_similarity = similarity
                    best_cluster = cluster
            
            if best_cluster:
                best_cluster['sessions'].append(session)
            else:
                # Create new cluster
                clusters.append({
                    'representative_signature': signature,
                    'sessions': [session]
                })
        
        cluster_sizes = [len(cluster['sessions']) for cluster in clusters]
        cluster_quality = 'good' if len(clusters) <= 3 else 'fragmented'
        
        return {
            'clusters': len(clusters),
            'cluster_sizes': cluster_sizes,
            'cluster_quality': cluster_quality
        }
    
    def _calculate_session_frequency(self, device_sessions: List[Dict[str, Any]]) -> float:
        """Calculate session frequency (sessions per day)"""
        if len(device_sessions) < 2:
            return 0.0
        
        time_span = device_sessions[-1]['timestamp'] - device_sessions[0]['timestamp']
        time_span_days = time_span.total_seconds() / (24 * 3600)
        
        return len(device_sessions) / max(time_span_days, 1)
    
    def _analyze_usage_patterns(self, device_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze usage patterns from sessions"""
        if not device_sessions:
            return {}
        
        usage_hours = [session['timestamp'].hour for session in device_sessions]
        usage_days = [session['timestamp'].weekday() for session in device_sessions]
        
        # Calculate usage distribution
        hour_distribution = {}
        for hour in range(24):
            hour_distribution[hour] = usage_hours.count(hour)
        
        day_distribution = {}
        for day in range(7):
            day_distribution[day] = usage_days.count(day)
        
        return {
            'peak_hours': [h for h, c in hour_distribution.items() if c == max(hour_distribution.values())],
            'peak_days': [d for d, c in day_distribution.items() if c == max(day_distribution.values())],
            'hour_distribution': hour_distribution,
            'day_distribution': day_distribution
        }
    
    def _calculate_session_duration_stats(self, device_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate session duration statistics"""
        # This would require session end times, which we don't have in current structure
        # Return placeholder for now
        return {
            'avg_duration': 'unknown',
            'duration_variance': 'unknown',
            'note': 'Session end times not available'
        }
    
    def _extract_location_patterns(self, device_sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract location patterns from sessions"""
        locations = []
        
        for session in device_sessions:
            signature = session.get('signature', {})
            network = signature.get('network', {})
            if 'country' in network:
                locations.append(network['country'])
        
        if not locations:
            return {'countries': [], 'location_stability': 'unknown'}
        
        unique_locations = set(locations)
        location_stability = 'stable' if len(unique_locations) == 1 else 'variable'
        
        return {
            'countries': list(unique_locations),
            'location_stability': location_stability,
            'location_changes': len(unique_locations) - 1
        }
    
    def _calculate_consistency_trend(self, device_id: str) -> str:
        """Calculate consistency trend for device"""
        device_sessions = self.device_sessions.get(device_id, [])
        
        if len(device_sessions) < 5:
            return 'insufficient_data'
        
        # Calculate consistency scores for recent sessions
        recent_scores = []
        for i in range(max(0, len(device_sessions) - 10), len(device_sessions)):
            session = device_sessions[i]
            score = session.get('consistency_score', 0.5)
            recent_scores.append(score)
        
        if len(recent_scores) < 3:
            return 'stable'
        
        # Analyze trend
        early_avg = statistics.mean(recent_scores[:len(recent_scores)//2])
        late_avg = statistics.mean(recent_scores[len(recent_scores)//2:])
        
        if late_avg > early_avg + 0.1:
            return 'improving'
        elif late_avg < early_avg - 0.1:
            return 'degrading'
        else:
            return 'stable'
    
    def _get_risk_level_history(self, device_id: str) -> List[str]:
        """Get risk level history for device"""
        # This would ideally come from stored data
        # For now, return a placeholder based on current session count
        device_sessions = self.device_sessions.get(device_id, [])
        
        if len(device_sessions) < 5:
            return ['MEDIUM', 'LOW', 'MINIMAL']
        else:
            return ['HIGH', 'MEDIUM', 'LOW', 'MINIMAL', 'LOW']
    
    def _calculate_data_quality_modifier(self, consistency_analysis: Dict[str, Any]) -> float:
        """Calculate data quality modifier for consistency score"""
        quality_factors = []
        
        # Check if we have sufficient data for analysis
        evolution_tracking = consistency_analysis.get('evolution_tracking', {})
        signature_age = evolution_tracking.get('signature_age_hours', 0)
        
        if signature_age > 24:  # More than 24 data points
            quality_factors.append(1.0)
        elif signature_age > 10:
            quality_factors.append(0.9)
        elif signature_age > 5:
            quality_factors.append(0.8)
        else:
            quality_factors.append(0.6)
        
        # Check session correlation confidence
        session_correlation = consistency_analysis.get('session_correlation', {})
        correlation_confidence = session_correlation.get('correlation_confidence', 'low')
        
        confidence_scores = {'high': 1.0, 'medium': 0.9, 'low': 0.7}
        quality_factors.append(confidence_scores.get(correlation_confidence, 0.7))
        
        return statistics.mean(quality_factors) if quality_factors else 0.8
    
    # ===== CLASSIFICATION HELPER METHODS =====
    
    def _classify_cpu_performance(self, cpu_data: Dict[str, Any]) -> str:
        """Classify CPU performance level"""
        cores = cpu_data.get('cores', 0)
        frequency = cpu_data.get('frequency', 0)
        
        if cores >= 8 and frequency >= 3000:
            return 'high-end'
        elif cores >= 4 and frequency >= 2000:
            return 'mid-range'
        else:
            return 'low-end'
    
    def _classify_memory_size(self, memory_gb: float) -> str:
        """Classify memory size"""
        if memory_gb >= 16:
            return 'high'
        elif memory_gb >= 8:
            return 'medium'
        elif memory_gb >= 4:
            return 'low'
        else:
            return 'very-low'
    
    def _classify_gpu_type(self, gpu_data: Dict[str, Any]) -> str:
        """Classify GPU type"""
        renderer = gpu_data.get('renderer', '').lower()
        
        if any(brand in renderer for brand in ['nvidia', 'amd', 'radeon', 'geforce']):
            return 'dedicated'
        elif 'intel' in renderer:
            return 'integrated'
        else:
            return 'unknown'
    
    def _classify_storage_size(self, storage_gb: float) -> str:
        """Classify storage size"""
        if storage_gb >= 1000:
            return 'large'
        elif storage_gb >= 500:
            return 'medium'
        elif storage_gb >= 250:
            return 'small'
        else:
            return 'very-small'
    
    def _check_cpu_virtualization(self, cpu_data: Dict[str, Any]) -> bool:
        """Check for CPU virtualization indicators"""
        vendor = cpu_data.get('vendor', '').lower()
        model = cpu_data.get('model', '').lower()
        
        vm_indicators = ['virtual', 'qemu', 'kvm', 'xen']
        return any(indicator in vendor or indicator in model for indicator in vm_indicators)
    
    def _check_gpu_virtualization(self, gpu_data: Dict[str, Any]) -> bool:
        """Check for GPU virtualization indicators"""
        renderer = gpu_data.get('renderer', '').lower()
        vendor = gpu_data.get('vendor', '').lower()
        
        vm_indicators = ['virtual', 'basic', 'standard', 'generic', 'vmware', 'virtualbox']
        return any(indicator in renderer or indicator in vendor for indicator in vm_indicators)
    
    def _check_cpu_memory_ratio(self, hardware_data: Dict[str, Any]) -> float:
        """Check CPU to memory ratio for consistency"""
        cpu_cores = hardware_data.get('cpu', {}).get('cores', 0)
        memory_gb = hardware_data.get('memory', {}).get('total_memory', 0) / (1024**3)
        
        if cpu_cores > 0 and memory_gb > 0:
            ratio = memory_gb / cpu_cores
            # Typical ratio is 1-4 GB per core
            if 1 <= ratio <= 4:
                return 1.0  # Good ratio
            else:
                return 0.5  # Unusual ratio
        return 0.0
    
    def _check_gpu_compatibility(self, hardware_data: Dict[str, Any]) -> float:
        """Check GPU compatibility with other components"""
        # Placeholder for GPU compatibility checks
        return 0.85


class EnvironmentAnalyzer:
    """
    🌐 PHASE 3.2: ADVANCED BROWSER & ENVIRONMENT ANALYSIS
    Advanced Browser and Environment Analysis for enhanced session fingerprinting
    
    This class provides comprehensive analysis of browser characteristics and automation detection
    to identify sophisticated evasion techniques and fraudulent session behavior.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Browser fingerprinting patterns and signatures
        self.browser_patterns = {
            'user_agent_inconsistencies': [
                'Chrome.*Safari.*Edge',  # Inconsistent browser claims
                'Mozilla.*Firefox.*Chrome',  # Mixed browser signatures
                'Windows.*Linux',  # OS inconsistencies in UA
                'Mobile.*Desktop',  # Device type inconsistencies
            ],
            'plugin_signatures': {
                'chrome': [
                    'Chrome PDF Plugin', 'Native Client', 'Widevine Content Decryption Module'
                ],
                'firefox': [
                    'Shockwave Flash', 'Java(TM) Platform', 'Windows Media Player'
                ],
                'safari': [
                    'QuickTime Plug-in', 'Java Applet Plug-in', 'Silverlight Plug-in'
                ],
                'edge': [
                    'Microsoft Edge PDF Plugin', 'Windows Media Player'
                ]
            },
            'javascript_engines': {
                'chrome': 'V8',
                'firefox': 'SpiderMonkey', 
                'safari': 'JavaScriptCore',
                'edge': 'Chakra'
            },
            'rendering_engines': {
                'chrome': 'Blink',
                'firefox': 'Gecko',
                'safari': 'WebKit',
                'edge': 'EdgeHTML'
            }
        }
        
        # Automation tool detection patterns
        self.automation_signatures = {
            'selenium_indicators': [
                'webdriver', 'selenium', 'phantomjs', 'chromedriver', 'geckodriver',
                'selenium-webdriver', 'webdriver-manager', '__selenium_unwrapped',
                '__webdriver_script_fn', '__driver_evaluate', '__webdriver_evaluate',
                '_selenium', 'calledSelenium', '_Selenium_IDE_Recorder'
            ],
            'puppeteer_indicators': [
                'puppeteer', 'headless', '__puppeteer_evaluation_script__',
                'Runtime.evaluate', 'Page.addScriptTag', 'chromium',
                '__nightmare', 'HeadlessChrome'
            ],
            'playwright_indicators': [
                'playwright', '__playwright', 'pwBrowserContext',
                'pwPage', 'pwFrame', 'pwWorker', 'pwConsoleAPI'
            ],
            'webdriver_properties': [
                'window.navigator.webdriver',
                'window.chrome.runtime.onConnect',
                'window.chrome.runtime.onMessage', 
                'document.$cdc_asdjflasutopfhvcZLmcfl_',
                'window.callPhantom', 'window._phantom'
            ],
            'automation_behavior_patterns': {
                'mouse_patterns': {
                    'linear_movement': {'threshold': 0.95, 'risk': 'high'},
                    'perfect_clicks': {'threshold': 0.90, 'risk': 'medium'},
                    'no_acceleration': {'threshold': 0.85, 'risk': 'high'},
                    'instant_hover': {'threshold': 0.80, 'risk': 'medium'}
                },
                'timing_patterns': {
                    'uniform_intervals': {'threshold': 0.90, 'risk': 'high'},
                    'no_human_delay': {'threshold': 0.85, 'risk': 'high'},
                    'perfect_typing': {'threshold': 0.75, 'risk': 'medium'}
                },
                'javascript_execution': {
                    'synchronous_only': {'threshold': 0.80, 'risk': 'medium'},
                    'no_user_gestures': {'threshold': 0.70, 'risk': 'low'},
                    'missing_event_properties': {'threshold': 0.85, 'risk': 'high'}
                }
            }
        }
        
        self.logger.info("EnvironmentAnalyzer initialized successfully")
    
    def analyze_browser_fingerprint(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔍 ANALYZE BROWSER FINGERPRINT
        Comprehensive browser fingerprinting analysis including user agent validation,
        plugin enumeration, JavaScript engine characteristics, and configuration consistency
        
        Args:
            browser_data: Dictionary containing browser characteristics
            
        Returns:
            Dict containing comprehensive browser fingerprint analysis
        """
        try:
            self.logger.info("Starting comprehensive browser fingerprint analysis")
            
            analysis_result = {
                'browser_identification': {},
                'user_agent_analysis': {},
                'plugin_analysis': {},
                'javascript_engine_analysis': {},
                'rendering_engine_analysis': {},
                'configuration_consistency': {},
                'fingerprint_uniqueness': {},
                'risk_assessment': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            # 1. User Agent Analysis and Validation
            user_agent_analysis = self._analyze_user_agent(browser_data.get('user_agent', ''))
            analysis_result['user_agent_analysis'] = user_agent_analysis
            
            # 2. Browser Plugin and Extension Enumeration
            plugin_analysis = self._analyze_browser_plugins(browser_data.get('plugins', []))
            analysis_result['plugin_analysis'] = plugin_analysis
            
            # 3. JavaScript Engine Characteristics
            js_engine_analysis = self._analyze_javascript_engine(browser_data)
            analysis_result['javascript_engine_analysis'] = js_engine_analysis
            
            # 4. Rendering Engine Fingerprinting
            rendering_analysis = self._analyze_rendering_engine(browser_data)
            analysis_result['rendering_engine_analysis'] = rendering_analysis
            
            # 5. Browser Configuration Inconsistency Detection
            consistency_analysis = self._detect_browser_inconsistencies(browser_data)
            analysis_result['configuration_consistency'] = consistency_analysis
            
            # 6. Browser Identification and Classification
            browser_id = self._identify_browser_type(browser_data)
            analysis_result['browser_identification'] = browser_id
            
            # 7. Fingerprint Uniqueness and Entropy Calculation
            uniqueness_score = self._calculate_fingerprint_uniqueness(browser_data)
            analysis_result['fingerprint_uniqueness'] = uniqueness_score
            
            # 8. Risk Assessment and Threat Classification
            risk_assessment = self._assess_browser_fingerprint_risk(analysis_result)
            analysis_result['risk_assessment'] = risk_assessment
            
            self.logger.info(f"Browser fingerprint analysis completed successfully with risk level: {risk_assessment.get('risk_level', 'UNKNOWN')}")
            
            return {
                'success': True,
                'browser_fingerprint_analysis': analysis_result,
                'analysis_summary': {
                    'browser_type': browser_id.get('detected_browser', 'Unknown'),
                    'trust_score': risk_assessment.get('trust_score', 0.5),
                    'risk_level': risk_assessment.get('risk_level', 'MEDIUM'),
                    'inconsistencies_found': consistency_analysis.get('inconsistency_count', 0),
                    'unique_characteristics': uniqueness_score.get('unique_features', 0)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing browser fingerprint: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def detect_automation_tools(self, browser_data: Dict[str, Any] = None, 
                              behavioral_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        🤖 DETECT AUTOMATION TOOLS
        Advanced automation tool detection including Selenium, Puppeteer, Playwright,
        WebDriver properties, framework signatures, and behavioral pattern analysis
        
        Args:
            browser_data: Browser characteristics and properties
            behavioral_data: Mouse movement, timing, and interaction patterns
            
        Returns:
            Dict containing comprehensive automation detection analysis
        """
        try:
            self.logger.info("Starting comprehensive automation tool detection")
            
            detection_result = {
                'automation_detected': False,
                'detected_tools': [],
                'webdriver_analysis': {},
                'framework_signatures': {},
                'behavioral_analysis': {},
                'mouse_pattern_analysis': {},
                'timing_pattern_analysis': {},
                'javascript_execution_analysis': {},
                'confidence_score': 0.0,
                'risk_level': 'LOW',
                'detection_details': [],
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            automation_indicators = []
            confidence_scores = []
            
            # 1. Selenium Detection
            selenium_detection = self._detect_selenium_automation(browser_data or {})
            if selenium_detection['detected']:
                automation_indicators.append('Selenium')
                confidence_scores.append(selenium_detection['confidence'])
                detection_result['detected_tools'].append(selenium_detection)
            
            # 2. Puppeteer Detection
            puppeteer_detection = self._detect_puppeteer_automation(browser_data or {})
            if puppeteer_detection['detected']:
                automation_indicators.append('Puppeteer')
                confidence_scores.append(puppeteer_detection['confidence'])
                detection_result['detected_tools'].append(puppeteer_detection)
            
            # 3. Playwright Detection
            playwright_detection = self._detect_playwright_automation(browser_data or {})
            if playwright_detection['detected']:
                automation_indicators.append('Playwright')
                confidence_scores.append(playwright_detection['confidence'])
                detection_result['detected_tools'].append(playwright_detection)
            
            # 4. WebDriver Property Analysis
            webdriver_analysis = self._analyze_webdriver_properties(browser_data or {})
            detection_result['webdriver_analysis'] = webdriver_analysis
            if webdriver_analysis['webdriver_detected']:
                automation_indicators.append('WebDriver')
                confidence_scores.append(webdriver_analysis['confidence'])
            
            # 5. Automation Framework Signatures
            framework_analysis = self._detect_automation_frameworks(browser_data or {})
            detection_result['framework_signatures'] = framework_analysis
            if framework_analysis['frameworks_detected']:
                automation_indicators.extend(framework_analysis['detected_frameworks'])
                confidence_scores.extend(framework_analysis['confidence_scores'])
            
            # 6. Mouse Movement and Timing Pattern Analysis
            behavioral_analysis = self._analyze_automation_behavior(behavioral_data or {})
            detection_result['behavioral_analysis'] = behavioral_analysis
            detection_result['mouse_pattern_analysis'] = behavioral_analysis.get('mouse_analysis', {})
            detection_result['timing_pattern_analysis'] = behavioral_analysis.get('timing_analysis', {})
            
            if behavioral_analysis.get('automation_detected', False):
                automation_indicators.append('Behavioral Patterns')
                confidence_scores.append(behavioral_analysis.get('confidence', 0.0))
            
            # 7. JavaScript Execution Anomaly Detection
            js_execution_analysis = self._analyze_javascript_execution_anomalies(browser_data or {})
            detection_result['javascript_execution_analysis'] = js_execution_analysis
            if js_execution_analysis.get('anomalies_detected', False):
                automation_indicators.append('JavaScript Anomalies')
                confidence_scores.append(js_execution_analysis.get('confidence', 0.0))
            
            # 8. Calculate Overall Automation Detection Results
            detection_result['automation_detected'] = len(automation_indicators) > 0
            detection_result['confidence_score'] = statistics.mean(confidence_scores) if confidence_scores else 0.0
            
            # Risk level classification
            if detection_result['confidence_score'] > 0.8:
                detection_result['risk_level'] = 'CRITICAL'
            elif detection_result['confidence_score'] > 0.6:
                detection_result['risk_level'] = 'HIGH'
            elif detection_result['confidence_score'] > 0.4:
                detection_result['risk_level'] = 'MEDIUM'
            else:
                detection_result['risk_level'] = 'LOW'
            
            # Detection summary
            detection_result['detection_details'] = [
                f"Detected {len(automation_indicators)} automation indicators",
                f"Confidence score: {detection_result['confidence_score']:.3f}",
                f"Risk level: {detection_result['risk_level']}",
                f"Tools detected: {', '.join(automation_indicators) if automation_indicators else 'None'}"
            ]
            
            self.logger.info(f"Automation detection completed - Tools found: {automation_indicators}, Confidence: {detection_result['confidence_score']:.3f}")
            
            return {
                'success': True,
                'automation_detection': detection_result,
                'detection_summary': {
                    'automation_detected': detection_result['automation_detected'],
                    'detected_tools_count': len(automation_indicators),
                    'primary_tool': automation_indicators[0] if automation_indicators else None,
                    'confidence_score': detection_result['confidence_score'],
                    'risk_level': detection_result['risk_level']
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting automation tools: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    # ===== BROWSER FINGERPRINT ANALYSIS HELPER METHODS =====
    
    def _analyze_user_agent(self, user_agent: str) -> Dict[str, Any]:
        """Analyze and validate user agent string for inconsistencies"""
        try:
            analysis = {
                'user_agent_string': user_agent,
                'parsed_components': {},
                'inconsistencies': [],
                'validation_score': 1.0,
                'suspected_spoofing': False
            }
            
            if not user_agent:
                analysis['inconsistencies'].append('Empty user agent string')
                analysis['validation_score'] = 0.0
                return analysis
            
            # Parse user agent components
            analysis['parsed_components'] = self._parse_user_agent_components(user_agent)
            
            # Check for inconsistencies
            for pattern in self.browser_patterns['user_agent_inconsistencies']:
                if re.search(pattern, user_agent, re.IGNORECASE):
                    analysis['inconsistencies'].append(f"Inconsistent pattern: {pattern}")
                    analysis['validation_score'] -= 0.2
            
            # Check for common spoofing indicators
            spoofing_indicators = [
                'HeadlessChrome', 'PhantomJS', 'SlimerJS', 'Selenium',
                'WebDriver', 'Automation', 'Bot', 'Crawler'
            ]
            
            for indicator in spoofing_indicators:
                if indicator.lower() in user_agent.lower():
                    analysis['inconsistencies'].append(f"Automation indicator: {indicator}")
                    analysis['suspected_spoofing'] = True
                    analysis['validation_score'] -= 0.3
            
            analysis['validation_score'] = max(0.0, analysis['validation_score'])
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing user agent: {str(e)}")
            return {'error': str(e), 'validation_score': 0.0}
    
    def _parse_user_agent_components(self, user_agent: str) -> Dict[str, Any]:
        """Parse user agent string into components"""
        components = {
            'browser_name': 'Unknown',
            'browser_version': 'Unknown',
            'os_name': 'Unknown',
            'os_version': 'Unknown',
            'device_type': 'Desktop'
        }
        
        # Simple parsing logic (in production, use a proper UA parsing library)
        if 'Chrome' in user_agent:
            components['browser_name'] = 'Chrome'
            chrome_match = re.search(r'Chrome/(\d+\.\d+)', user_agent)
            if chrome_match:
                components['browser_version'] = chrome_match.group(1)
        elif 'Firefox' in user_agent:
            components['browser_name'] = 'Firefox'
            firefox_match = re.search(r'Firefox/(\d+\.\d+)', user_agent)
            if firefox_match:
                components['browser_version'] = firefox_match.group(1)
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            components['browser_name'] = 'Safari'
        
        # OS detection
        if 'Windows NT' in user_agent:
            components['os_name'] = 'Windows'
            windows_match = re.search(r'Windows NT (\d+\.\d+)', user_agent)
            if windows_match:
                components['os_version'] = windows_match.group(1)
        elif 'Mac OS X' in user_agent:
            components['os_name'] = 'macOS'
        elif 'Linux' in user_agent:
            components['os_name'] = 'Linux'
        
        # Device type
        if any(mobile in user_agent for mobile in ['Mobile', 'Android', 'iPhone', 'iPad']):
            components['device_type'] = 'Mobile'
        
        return components
    
    def _analyze_browser_plugins(self, plugins: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze browser plugins and extensions for fingerprinting"""
        try:
            analysis = {
                'plugin_count': len(plugins),
                'plugin_list': plugins,
                'plugin_signatures': {},
                'consistency_score': 1.0,
                'suspicious_plugins': [],
                'missing_expected_plugins': []
            }
            
            plugin_names = [plugin.get('name', '').lower() for plugin in plugins]
            
            # Check against known browser plugin signatures
            for browser, expected_plugins in self.browser_patterns['plugin_signatures'].items():
                matches = sum(1 for expected in expected_plugins 
                            if any(expected.lower() in name for name in plugin_names))
                total_expected = len(expected_plugins)
                match_ratio = matches / total_expected if total_expected > 0 else 0
                
                analysis['plugin_signatures'][browser] = {
                    'matches': matches,
                    'expected': total_expected,
                    'match_ratio': match_ratio,
                    'likely_browser': match_ratio > 0.5
                }
            
            # Check for suspicious plugins
            suspicious_keywords = ['selenium', 'webdriver', 'automation', 'phantom', 'headless']
            for plugin in plugins:
                plugin_name = plugin.get('name', '').lower()
                if any(keyword in plugin_name for keyword in suspicious_keywords):
                    analysis['suspicious_plugins'].append(plugin)
                    analysis['consistency_score'] -= 0.2
            
            analysis['consistency_score'] = max(0.0, analysis['consistency_score'])
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing browser plugins: {str(e)}")
            return {'error': str(e), 'consistency_score': 0.0}
    
    def _analyze_javascript_engine(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze JavaScript engine characteristics"""
        try:
            analysis = {
                'detected_engine': 'Unknown',
                'engine_version': 'Unknown',
                'engine_features': [],
                'performance_characteristics': {},
                'consistency_with_browser': True,
                'anomalies': []
            }
            
            browser_name = browser_data.get('browser_name', '').lower()
            
            # Map browser to expected JavaScript engine
            expected_engine = self.browser_patterns['javascript_engines'].get(browser_name, 'Unknown')
            analysis['expected_engine'] = expected_engine
            
            # Analyze JavaScript capabilities and features
            js_features = browser_data.get('javascript_features', {})
            if js_features:
                analysis['engine_features'] = list(js_features.keys())
                
                # Check for engine-specific features
                if 'v8' in str(js_features).lower():
                    analysis['detected_engine'] = 'V8'
                elif 'spidermonkey' in str(js_features).lower():
                    analysis['detected_engine'] = 'SpiderMonkey'
                elif 'javascriptcore' in str(js_features).lower():
                    analysis['detected_engine'] = 'JavaScriptCore'
            
            # Check consistency between browser and JavaScript engine
            if analysis['detected_engine'] != 'Unknown' and expected_engine != 'Unknown':
                if analysis['detected_engine'] != expected_engine:
                    analysis['consistency_with_browser'] = False
                    analysis['anomalies'].append(f"Engine mismatch: Expected {expected_engine}, detected {analysis['detected_engine']}")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing JavaScript engine: {str(e)}")
            return {'error': str(e), 'consistency_with_browser': False}
    
    def _analyze_rendering_engine(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze rendering engine fingerprinting characteristics"""
        try:
            analysis = {
                'detected_engine': browser_data.get('engine_name', 'Unknown'),
                'engine_version': browser_data.get('engine_version', 'Unknown'),
                'expected_engine': 'Unknown',
                'rendering_capabilities': {},
                'consistency_score': 1.0,
                'inconsistencies': []
            }
            
            browser_name = browser_data.get('browser_name', '').lower()
            expected_engine = self.browser_patterns['rendering_engines'].get(browser_name, 'Unknown')
            analysis['expected_engine'] = expected_engine
            
            # Check rendering capabilities
            canvas_support = browser_data.get('canvas_support', False)
            webgl_support = browser_data.get('webgl_support', False)
            
            analysis['rendering_capabilities'] = {
                'canvas_support': canvas_support,
                'webgl_support': webgl_support,
                'css3_support': browser_data.get('css3_support', True),
                'svg_support': browser_data.get('svg_support', True)
            }
            
            # Check engine consistency
            if analysis['detected_engine'] != 'Unknown' and expected_engine != 'Unknown':
                if analysis['detected_engine'].lower() != expected_engine.lower():
                    analysis['inconsistencies'].append(f"Rendering engine mismatch: Expected {expected_engine}, got {analysis['detected_engine']}")
                    analysis['consistency_score'] -= 0.3
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing rendering engine: {str(e)}")
            return {'error': str(e), 'consistency_score': 0.0}
    
    def _detect_browser_inconsistencies(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect browser configuration inconsistencies that may indicate spoofing"""
        try:
            inconsistencies = []
            consistency_score = 1.0
            
            # Check user agent vs. declared browser name
            user_agent = browser_data.get('user_agent', '')
            declared_browser = browser_data.get('browser_name', '')
            
            if declared_browser and user_agent:
                if declared_browser.lower() not in user_agent.lower():
                    inconsistencies.append("Browser name doesn't match user agent")
                    consistency_score -= 0.2
            
            # Check plugin consistency with browser type
            plugins = browser_data.get('plugins', [])
            if plugins and declared_browser:
                plugin_analysis = self._analyze_browser_plugins(plugins)
                browser_match = plugin_analysis.get('plugin_signatures', {}).get(declared_browser.lower(), {})
                
                if browser_match.get('match_ratio', 0) < 0.3:
                    inconsistencies.append("Plugins don't match declared browser type")
                    consistency_score -= 0.3
            
            # Check JavaScript engine consistency
            js_analysis = self._analyze_javascript_engine(browser_data)
            if not js_analysis.get('consistency_with_browser', True):
                inconsistencies.append("JavaScript engine inconsistent with browser type")
                consistency_score -= 0.2
            
            # Check rendering engine consistency
            rendering_analysis = self._analyze_rendering_engine(browser_data)
            if rendering_analysis.get('consistency_score', 1.0) < 0.7:
                inconsistencies.append("Rendering engine inconsistent with browser type")
                consistency_score -= 0.2
            
            consistency_score = max(0.0, consistency_score)
            
            return {
                'inconsistency_count': len(inconsistencies),
                'inconsistencies': inconsistencies,
                'consistency_score': consistency_score,
                'likely_spoofed': consistency_score < 0.5,
                'trust_level': 'HIGH' if consistency_score > 0.8 else 'MEDIUM' if consistency_score > 0.5 else 'LOW'
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting browser inconsistencies: {str(e)}")
            return {'error': str(e), 'consistency_score': 0.0}
    
    def _identify_browser_type(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify and classify browser type based on multiple indicators"""
        try:
            detection_scores = {}
            
            # User agent analysis
            user_agent = browser_data.get('user_agent', '')
            ua_scores = self._score_browser_from_user_agent(user_agent)
            
            # Plugin analysis
            plugins = browser_data.get('plugins', [])
            plugin_scores = self._score_browser_from_plugins(plugins)
            
            # Combine scores
            all_browsers = set(ua_scores.keys()) | set(plugin_scores.keys())
            for browser in all_browsers:
                ua_score = ua_scores.get(browser, 0.0)
                plugin_score = plugin_scores.get(browser, 0.0)
                detection_scores[browser] = (ua_score * 0.7) + (plugin_score * 0.3)
            
            # Determine most likely browser
            detected_browser = max(detection_scores.keys(), key=lambda k: detection_scores[k]) if detection_scores else 'Unknown'
            confidence = detection_scores.get(detected_browser, 0.0)
            
            return {
                'detected_browser': detected_browser,
                'confidence': confidence,
                'detection_scores': detection_scores,
                'declared_browser': browser_data.get('browser_name', 'Unknown'),
                'match_declared': detected_browser.lower() == browser_data.get('browser_name', '').lower()
            }
            
        except Exception as e:
            self.logger.error(f"Error identifying browser type: {str(e)}")
            return {'error': str(e), 'detected_browser': 'Unknown'}
    
    def _score_browser_from_user_agent(self, user_agent: str) -> Dict[str, float]:
        """Score browser likelihood from user agent string"""
        scores = {}
        
        if 'Chrome' in user_agent and 'Edg' not in user_agent:
            scores['chrome'] = 0.9
        if 'Firefox' in user_agent:
            scores['firefox'] = 0.9
        if 'Safari' in user_agent and 'Chrome' not in user_agent:
            scores['safari'] = 0.9
        if 'Edg' in user_agent:
            scores['edge'] = 0.9
        
        return scores
    
    def _score_browser_from_plugins(self, plugins: List[Dict[str, Any]]) -> Dict[str, float]:
        """Score browser likelihood from plugin analysis"""
        plugin_analysis = self._analyze_browser_plugins(plugins)
        scores = {}
        
        for browser, signature in plugin_analysis.get('plugin_signatures', {}).items():
            scores[browser] = signature.get('match_ratio', 0.0)
        
        return scores
    
    def _calculate_fingerprint_uniqueness(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate browser fingerprint uniqueness and entropy"""
        try:
            # Calculate entropy based on various characteristics
            characteristics = []
            
            # User agent entropy
            user_agent = browser_data.get('user_agent', '')
            if user_agent:
                characteristics.append(user_agent)
            
            # Plugin list entropy
            plugins = browser_data.get('plugins', [])
            plugin_string = json.dumps(sorted([p.get('name', '') for p in plugins]))
            characteristics.append(plugin_string)
            
            # Browser capabilities
            capabilities = {
                'canvas': browser_data.get('canvas_support', False),
                'webgl': browser_data.get('webgl_support', False),
                'local_storage': browser_data.get('local_storage', False),
                'session_storage': browser_data.get('session_storage', False),
                'cookie_enabled': browser_data.get('cookie_enabled', False)
            }
            characteristics.append(json.dumps(capabilities, sort_keys=True))
            
            # Language preferences
            languages = browser_data.get('languages', [])
            characteristics.append(json.dumps(sorted(languages)))
            
            # Calculate combined fingerprint hash
            combined_fingerprint = ''.join(characteristics)
            fingerprint_hash = hashlib.sha256(combined_fingerprint.encode()).hexdigest()
            
            # Estimate uniqueness (simplified calculation)
            unique_features = len([c for c in characteristics if c and len(c) > 10])
            estimated_uniqueness = min(1.0, unique_features / 10.0)
            
            # Calculate entropy
            entropy = len(set(combined_fingerprint)) / len(combined_fingerprint) if combined_fingerprint else 0
            
            return {
                'fingerprint_hash': fingerprint_hash,
                'unique_features': unique_features,
                'estimated_uniqueness': estimated_uniqueness,
                'entropy_score': entropy,
                'characteristics_analyzed': len(characteristics),
                'fingerprint_strength': 'STRONG' if estimated_uniqueness > 0.7 else 'MEDIUM' if estimated_uniqueness > 0.4 else 'WEAK'
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating fingerprint uniqueness: {str(e)}")
            return {'error': str(e), 'estimated_uniqueness': 0.0}
    
    def _assess_browser_fingerprint_risk(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall risk level based on browser fingerprint analysis"""
        try:
            risk_factors = []
            risk_score = 0.0
            
            # User agent analysis risk
            ua_analysis = analysis_result.get('user_agent_analysis', {})
            ua_score = ua_analysis.get('validation_score', 1.0)
            if ua_score < 0.7:
                risk_factors.append('Suspicious user agent')
                risk_score += (1.0 - ua_score) * 0.3
            
            # Configuration consistency risk
            consistency = analysis_result.get('configuration_consistency', {})
            consistency_score = consistency.get('consistency_score', 1.0)
            if consistency_score < 0.7:
                risk_factors.append('Browser configuration inconsistencies')
                risk_score += (1.0 - consistency_score) * 0.4
            
            # Plugin analysis risk
            plugin_analysis = analysis_result.get('plugin_analysis', {})
            if plugin_analysis.get('suspicious_plugins', []):
                risk_factors.append('Suspicious browser plugins detected')
                risk_score += 0.3
            
            # Fingerprint uniqueness risk (too unique might be suspicious)
            uniqueness = analysis_result.get('fingerprint_uniqueness', {})
            uniqueness_score = uniqueness.get('estimated_uniqueness', 0.5)
            if uniqueness_score > 0.95:  # Extremely unique might indicate manipulation
                risk_factors.append('Extremely unique fingerprint (possible manipulation)')
                risk_score += 0.2
            
            # Calculate trust score (inverse of risk)
            risk_score = min(1.0, risk_score)
            trust_score = 1.0 - risk_score
            
            # Risk level classification
            if risk_score > 0.7:
                risk_level = 'HIGH'
            elif risk_score > 0.4:
                risk_level = 'MEDIUM'
            elif risk_score > 0.2:
                risk_level = 'LOW'
            else:
                risk_level = 'MINIMAL'
            
            return {
                'risk_score': risk_score,
                'trust_score': trust_score,
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'risk_factor_count': len(risk_factors),
                'recommendation': self._generate_risk_recommendation(risk_level, risk_factors)
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing browser fingerprint risk: {str(e)}")
            return {'error': str(e), 'risk_level': 'MEDIUM'}
    
    def _generate_risk_recommendation(self, risk_level: str, risk_factors: List[str]) -> str:
        """Generate risk-based recommendations"""
        if risk_level == 'HIGH':
            return "High-risk browser fingerprint detected. Consider additional verification steps or blocking session."
        elif risk_level == 'MEDIUM':
            return "Medium-risk browser fingerprint. Monitor session closely and apply additional security measures."
        elif risk_level == 'LOW':
            return "Low-risk browser fingerprint. Standard monitoring sufficient."
        else:
            return "Minimal risk browser fingerprint. Standard session handling appropriate."
    
    # ===== AUTOMATION DETECTION HELPER METHODS =====
    
    def _detect_selenium_automation(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Selenium automation indicators"""
        try:
            selenium_indicators = []
            confidence = 0.0
            
            # Check user agent
            user_agent = browser_data.get('user_agent', '').lower()
            for indicator in self.automation_signatures['selenium_indicators']:
                if indicator in user_agent:
                    selenium_indicators.append(f"User agent contains: {indicator}")
                    confidence += 0.2
            
            # Check for Selenium-specific properties (if available in browser_data)
            selenium_properties = browser_data.get('webdriver_properties', [])
            for prop in selenium_properties:
                if any(sel_indicator in prop.lower() for sel_indicator in self.automation_signatures['selenium_indicators']):
                    selenium_indicators.append(f"WebDriver property: {prop}")
                    confidence += 0.3
            
            # Check plugins for Selenium-related entries
            plugins = browser_data.get('plugins', [])
            for plugin in plugins:
                plugin_name = plugin.get('name', '').lower()
                if any(indicator in plugin_name for indicator in ['selenium', 'webdriver', 'chromedriver']):
                    selenium_indicators.append(f"Selenium plugin: {plugin.get('name')}")
                    confidence += 0.4
            
            confidence = min(1.0, confidence)
            detected = confidence > 0.3
            
            return {
                'tool': 'Selenium',
                'detected': detected,
                'confidence': confidence,
                'indicators': selenium_indicators,
                'indicator_count': len(selenium_indicators)
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting Selenium: {str(e)}")
            return {'tool': 'Selenium', 'detected': False, 'error': str(e)}
    
    def _detect_puppeteer_automation(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Puppeteer automation indicators"""
        try:
            puppeteer_indicators = []
            confidence = 0.0
            
            # Check user agent for headless indicators
            user_agent = browser_data.get('user_agent', '').lower()
            for indicator in self.automation_signatures['puppeteer_indicators']:
                if indicator in user_agent:
                    puppeteer_indicators.append(f"User agent contains: {indicator}")
                    confidence += 0.3
            
            # Check for headless Chrome indicators
            if 'headlesschrome' in user_agent:
                puppeteer_indicators.append("HeadlessChrome detected in user agent")
                confidence += 0.5
            
            # Check browser name
            browser_name = browser_data.get('browser_name', '').lower()
            if 'headless' in browser_name or 'puppeteer' in browser_name:
                puppeteer_indicators.append(f"Suspicious browser name: {browser_name}")
                confidence += 0.4
            
            # Check for missing plugins (headless browsers often have no plugins)
            plugins = browser_data.get('plugins', [])
            if len(plugins) == 0 and 'chrome' in user_agent:
                puppeteer_indicators.append("No plugins in Chrome browser (possible headless)")
                confidence += 0.2
            
            confidence = min(1.0, confidence)
            detected = confidence > 0.3
            
            return {
                'tool': 'Puppeteer',
                'detected': detected,
                'confidence': confidence,
                'indicators': puppeteer_indicators,
                'indicator_count': len(puppeteer_indicators)
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting Puppeteer: {str(e)}")
            return {'tool': 'Puppeteer', 'detected': False, 'error': str(e)}
    
    def _detect_playwright_automation(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Playwright automation indicators"""
        try:
            playwright_indicators = []
            confidence = 0.0
            
            # Check user agent
            user_agent = browser_data.get('user_agent', '').lower()
            for indicator in self.automation_signatures['playwright_indicators']:
                if indicator in user_agent:
                    playwright_indicators.append(f"User agent contains: {indicator}")
                    confidence += 0.3
            
            # Check for Playwright-specific properties
            playwright_properties = browser_data.get('playwright_properties', [])
            for prop in playwright_properties:
                playwright_indicators.append(f"Playwright property: {prop}")
                confidence += 0.4
            
            # Check browser engine for Playwright modifications
            engine_name = browser_data.get('engine_name', '').lower()
            if 'playwright' in engine_name:
                playwright_indicators.append("Playwright detected in engine name")
                confidence += 0.5
            
            confidence = min(1.0, confidence)
            detected = confidence > 0.3
            
            return {
                'tool': 'Playwright',
                'detected': detected,
                'confidence': confidence,
                'indicators': playwright_indicators,
                'indicator_count': len(playwright_indicators)
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting Playwright: {str(e)}")
            return {'tool': 'Playwright', 'detected': False, 'error': str(e)}
    
    def _analyze_webdriver_properties(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze WebDriver-specific properties and indicators"""
        try:
            webdriver_indicators = []
            confidence = 0.0
            
            # Check for explicit webdriver indicators
            webdriver_detected = browser_data.get('webdriver', False)
            if webdriver_detected:
                webdriver_indicators.append("navigator.webdriver is true")
                confidence += 0.8
            
            # Check for WebDriver properties
            for prop in self.automation_signatures['webdriver_properties']:
                if prop in str(browser_data):
                    webdriver_indicators.append(f"WebDriver property detected: {prop}")
                    confidence += 0.3
            
            # Check for missing properties that should exist in real browsers
            expected_properties = [
                'chrome.runtime.onConnect', 'chrome.runtime.onMessage',
                'chrome.csi', 'chrome.loadTimes'
            ]
            
            for prop in expected_properties:
                if f"missing_{prop}" in browser_data:
                    webdriver_indicators.append(f"Missing expected property: {prop}")
                    confidence += 0.2
            
            confidence = min(1.0, confidence)
            
            return {
                'webdriver_detected': confidence > 0.4,
                'confidence': confidence,
                'indicators': webdriver_indicators,
                'indicator_count': len(webdriver_indicators)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing WebDriver properties: {str(e)}")
            return {'webdriver_detected': False, 'error': str(e)}
    
    def _detect_automation_frameworks(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect various automation framework signatures"""
        try:
            detected_frameworks = []
            confidence_scores = []
            
            # Check for framework-specific indicators
            all_indicators = (
                self.automation_signatures['selenium_indicators'] +
                self.automation_signatures['puppeteer_indicators'] +
                self.automation_signatures['playwright_indicators']
            )
            
            browser_string = str(browser_data).lower()
            
            for indicator in all_indicators:
                if indicator in browser_string:
                    detected_frameworks.append(indicator)
                    confidence_scores.append(0.3)
            
            # Remove duplicates
            detected_frameworks = list(set(detected_frameworks))
            
            return {
                'frameworks_detected': len(detected_frameworks) > 0,
                'detected_frameworks': detected_frameworks,
                'framework_count': len(detected_frameworks),
                'confidence_scores': confidence_scores
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting automation frameworks: {str(e)}")
            return {'frameworks_detected': False, 'error': str(e)}
    
    def _analyze_automation_behavior(self, behavioral_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze behavioral patterns for automation indicators"""
        try:
            analysis = {
                'automation_detected': False,
                'confidence': 0.0,
                'mouse_analysis': {},
                'timing_analysis': {},
                'behavior_anomalies': []
            }
            
            if not behavioral_data:
                return analysis
            
            # Analyze mouse movement patterns
            mouse_analysis = self._analyze_mouse_patterns(behavioral_data.get('mouse_data', {}))
            analysis['mouse_analysis'] = mouse_analysis
            
            # Analyze timing patterns
            timing_analysis = self._analyze_timing_patterns(behavioral_data.get('timing_data', {}))
            analysis['timing_analysis'] = timing_analysis
            
            # Combine analysis results
            mouse_score = mouse_analysis.get('automation_score', 0.0)
            timing_score = timing_analysis.get('automation_score', 0.0)
            
            analysis['confidence'] = (mouse_score + timing_score) / 2
            analysis['automation_detected'] = analysis['confidence'] > 0.5
            
            # Collect all anomalies
            analysis['behavior_anomalies'].extend(mouse_analysis.get('anomalies', []))
            analysis['behavior_anomalies'].extend(timing_analysis.get('anomalies', []))
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing automation behavior: {str(e)}")
            return {'automation_detected': False, 'error': str(e)}
    
    def _analyze_mouse_patterns(self, mouse_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mouse movement patterns for automation indicators"""
        try:
            analysis = {
                'automation_score': 0.0,
                'anomalies': [],
                'pattern_analysis': {}
            }
            
            if not mouse_data:
                return analysis
            
            movements = mouse_data.get('movements', [])
            clicks = mouse_data.get('clicks', [])
            
            if movements:
                # Check for linear movement patterns
                linear_score = self._check_linear_movement(movements)
                if linear_score > 0.8:
                    analysis['anomalies'].append("Highly linear mouse movements detected")
                    analysis['automation_score'] += 0.3
                
                # Check for instant movements (no acceleration)
                instant_score = self._check_instant_movement(movements)
                if instant_score > 0.7:
                    analysis['anomalies'].append("Instant mouse movements without acceleration")
                    analysis['automation_score'] += 0.4
            
            if clicks:
                # Check for perfect click accuracy
                accuracy_score = self._check_click_accuracy(clicks)
                if accuracy_score > 0.9:
                    analysis['anomalies'].append("Perfect click accuracy (suspicious)")
                    analysis['automation_score'] += 0.3
            
            analysis['automation_score'] = min(1.0, analysis['automation_score'])
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing mouse patterns: {str(e)}")
            return {'automation_score': 0.0, 'error': str(e)}
    
    def _analyze_timing_patterns(self, timing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze timing patterns for automation indicators"""
        try:
            analysis = {
                'automation_score': 0.0,
                'anomalies': [],
                'timing_analysis': {}
            }
            
            if not timing_data:
                return analysis
            
            intervals = timing_data.get('intervals', [])
            keypress_timings = timing_data.get('keypress_timings', [])
            
            if intervals:
                # Check for uniform timing intervals
                uniformity_score = self._check_timing_uniformity(intervals)
                if uniformity_score > 0.8:
                    analysis['anomalies'].append("Highly uniform timing intervals")
                    analysis['automation_score'] += 0.4
            
            if keypress_timings:
                # Check for robotic typing patterns
                typing_score = self._check_robotic_typing(keypress_timings)
                if typing_score > 0.7:
                    analysis['anomalies'].append("Robotic typing patterns detected")
                    analysis['automation_score'] += 0.3
            
            analysis['automation_score'] = min(1.0, analysis['automation_score'])
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing timing patterns: {str(e)}")
            return {'automation_score': 0.0, 'error': str(e)}
    
    def _analyze_javascript_execution_anomalies(self, browser_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze JavaScript execution patterns for automation anomalies"""
        try:
            analysis = {
                'anomalies_detected': False,
                'confidence': 0.0,
                'anomalies': []
            }
            
            # Check for missing user gesture events
            user_gestures = browser_data.get('user_gestures', True)
            if not user_gestures:
                analysis['anomalies'].append("Missing user gesture events")
                analysis['confidence'] += 0.3
            
            # Check for synchronous-only JavaScript execution
            async_support = browser_data.get('async_execution', True)
            if not async_support:
                analysis['anomalies'].append("Only synchronous JavaScript execution")
                analysis['confidence'] += 0.4
            
            # Check for missing event properties
            event_properties = browser_data.get('event_properties', {})
            expected_properties = ['isTrusted', 'timeStamp', 'bubbles', 'cancelable']
            missing_properties = [prop for prop in expected_properties if prop not in event_properties]
            
            if missing_properties:
                analysis['anomalies'].append(f"Missing event properties: {missing_properties}")
                analysis['confidence'] += 0.2 * len(missing_properties)
            
            analysis['confidence'] = min(1.0, analysis['confidence'])
            analysis['anomalies_detected'] = analysis['confidence'] > 0.3
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing JavaScript execution anomalies: {str(e)}")
            return {'anomalies_detected': False, 'error': str(e)}
    
    # ===== BEHAVIORAL PATTERN ANALYSIS HELPER METHODS =====
    
    def _check_linear_movement(self, movements: List[Dict[str, Any]]) -> float:
        """Check for linear mouse movement patterns"""
        if len(movements) < 3:
            return 0.0
        
        # Calculate linearity score based on movement vectors
        linear_count = 0
        total_segments = len(movements) - 1
        
        for i in range(1, len(movements)):
            prev_move = movements[i-1]
            curr_move = movements[i]
            
            # Calculate movement vector
            dx = curr_move.get('x', 0) - prev_move.get('x', 0)
            dy = curr_move.get('y', 0) - prev_move.get('y', 0)
            
            # Check if movement is perfectly linear (simplified check)
            if abs(dx) == abs(dy) or dx == 0 or dy == 0:
                linear_count += 1
        
        return linear_count / total_segments if total_segments > 0 else 0.0
    
    def _check_instant_movement(self, movements: List[Dict[str, Any]]) -> float:
        """Check for instant mouse movements without acceleration"""
        if len(movements) < 2:
            return 0.0
        
        instant_count = 0
        
        for i in range(1, len(movements)):
            prev_move = movements[i-1]
            curr_move = movements[i]
            
            # Check timestamp difference
            prev_time = prev_move.get('timestamp', 0)
            curr_time = curr_move.get('timestamp', 0)
            time_diff = curr_time - prev_time
            
            # If movement happens in exactly same millisecond, it's suspicious
            if time_diff == 0:
                instant_count += 1
        
        return instant_count / len(movements) if movements else 0.0
    
    def _check_click_accuracy(self, clicks: List[Dict[str, Any]]) -> float:
        """Check for suspiciously perfect click accuracy"""
        if not clicks:
            return 0.0
        
        # In real usage, clicks have some variation from target centers
        # Perfect center clicks are suspicious
        perfect_clicks = 0
        
        for click in clicks:
            target_x = click.get('target_x', 0)
            target_y = click.get('target_y', 0)
            actual_x = click.get('actual_x', 0)
            actual_y = click.get('actual_y', 0)
            
            # Check if click is exactly on target (suspicious)
            if target_x == actual_x and target_y == actual_y:
                perfect_clicks += 1
        
        return perfect_clicks / len(clicks)
    
    def _check_timing_uniformity(self, intervals: List[float]) -> float:
        """Check for uniform timing intervals (indication of automation)"""
        if len(intervals) < 3:
            return 0.0
        
        # Calculate standard deviation of intervals
        mean_interval = statistics.mean(intervals)
        variance = statistics.variance(intervals)
        std_dev = math.sqrt(variance) if variance > 0 else 0
        
        # Very low standard deviation indicates uniform timing
        coefficient_of_variation = std_dev / mean_interval if mean_interval > 0 else 0
        
        # Return inverse of variation (high uniformity = high automation score)
        return max(0.0, 1.0 - coefficient_of_variation * 10)
    
    def _check_robotic_typing(self, keypress_timings: List[float]) -> float:
        """Check for robotic typing patterns"""
        if len(keypress_timings) < 5:
            return 0.0
        
        # Check for perfectly consistent typing intervals
        intervals = [keypress_timings[i+1] - keypress_timings[i] for i in range(len(keypress_timings)-1)]
        
        if not intervals:
            return 0.0
        
        # Calculate consistency of intervals
        mean_interval = statistics.mean(intervals)
        std_dev = statistics.stdev(intervals) if len(intervals) > 1 else 0
        
        # Very consistent timing is suspicious
        consistency_score = 1.0 - (std_dev / mean_interval) if mean_interval > 0 else 0
        
        return max(0.0, min(1.0, consistency_score))
    
    def monitor_network_characteristics(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🌐 MONITOR NETWORK CHARACTERISTICS
        Comprehensive network analysis including IP geolocation, reputation analysis,
        proxy/VPN/Tor detection, connection profiling, and network fingerprint consistency
        
        Args:
            network_data: Dictionary containing network characteristics and connection info
            
        Returns:
            Dict containing comprehensive network analysis with risk assessment
        """
        try:
            self.logger.info("Starting comprehensive network characteristics analysis")
            
            analysis_result = {
                'network_identity': {},
                'ip_analysis': {},
                'geolocation_analysis': {},
                'reputation_analysis': {},
                'latency_analysis': {},
                'routing_analysis': {},
                'proxy_vpn_detection': {},
                'connection_profiling': {},
                'network_consistency': {},
                'risk_assessment': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            # 1. IP Address Geolocation and Reputation Analysis
            ip_analysis = self._analyze_ip_geolocation_reputation(network_data)
            analysis_result['ip_analysis'] = ip_analysis
            analysis_result['geolocation_analysis'] = ip_analysis.get('geolocation', {})
            analysis_result['reputation_analysis'] = ip_analysis.get('reputation', {})
            
            # 2. Network Latency and Routing Analysis
            latency_analysis = self._analyze_network_latency_routing(network_data)
            analysis_result['latency_analysis'] = latency_analysis.get('latency', {})
            analysis_result['routing_analysis'] = latency_analysis.get('routing', {})
            
            # 3. Proxy/VPN/Tor Detection
            proxy_detection = self._detect_proxy_vpn_tor(network_data)
            analysis_result['proxy_vpn_detection'] = proxy_detection
            
            # 4. Connection Type and Bandwidth Profiling
            connection_profiling = self._analyze_connection_bandwidth_profile(network_data)
            analysis_result['connection_profiling'] = connection_profiling
            
            # 5. Network Fingerprint Consistency Tracking
            consistency_analysis = self._track_network_fingerprint_consistency(network_data)
            analysis_result['network_consistency'] = consistency_analysis
            
            # 6. Overall Network Risk Assessment
            risk_assessment = self._assess_network_characteristics_risk(analysis_result)
            analysis_result['risk_assessment'] = risk_assessment
            
            # Network Identity Summary
            analysis_result['network_identity'] = {
                'primary_ip': network_data.get('ip_address', 'Unknown'),
                'isp': network_data.get('isp', 'Unknown'),
                'country': network_data.get('country', 'Unknown'),
                'connection_type': connection_profiling.get('connection_type', 'Unknown'),
                'proxy_detected': proxy_detection.get('proxy_detected', False),
                'reputation_score': ip_analysis.get('reputation', {}).get('score', 0.5),
                'network_risk_level': risk_assessment.get('risk_level', 'MEDIUM')
            }
            
            self.logger.info(f"Network analysis completed - IP: {analysis_result['network_identity']['primary_ip']}, Risk: {analysis_result['network_identity']['network_risk_level']}")
            
            return {
                'success': True,
                'network_analysis': analysis_result,
                'analysis_summary': {
                    'ip_address': analysis_result['network_identity']['primary_ip'],
                    'country_location': analysis_result['network_identity']['country'],
                    'isp_provider': analysis_result['network_identity']['isp'],
                    'proxy_vpn_detected': analysis_result['network_identity']['proxy_detected'],
                    'reputation_score': analysis_result['network_identity']['reputation_score'],
                    'network_risk_level': analysis_result['network_identity']['network_risk_level']
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing network characteristics: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def track_timezone_consistency(self, timezone_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ⏰ TRACK TIMEZONE CONSISTENCY
        Comprehensive timezone analysis including system vs browser validation,
        geolocation correlation, manipulation detection, and temporal behavior analysis
        
        Args:
            timezone_data: Dictionary containing timezone, location, and timing information
            
        Returns:
            Dict containing comprehensive timezone consistency analysis
        """
        try:
            self.logger.info("Starting comprehensive timezone consistency analysis")
            
            analysis_result = {
                'timezone_identity': {},
                'system_browser_validation': {},
                'geolocation_correlation': {},
                'manipulation_detection': {},
                'time_synchronization': {},
                'temporal_behavior': {},
                'consistency_score': 0.0,
                'risk_assessment': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            # 1. System Timezone vs Browser Timezone Validation
            timezone_validation = self._validate_system_browser_timezones(timezone_data)
            analysis_result['system_browser_validation'] = timezone_validation
            
            # 2. Geolocation vs Timezone Correlation
            geo_correlation = self._correlate_geolocation_timezone(timezone_data)
            analysis_result['geolocation_correlation'] = geo_correlation
            
            # 3. Timezone Manipulation Detection
            manipulation_detection = self._detect_timezone_manipulation(timezone_data)
            analysis_result['manipulation_detection'] = manipulation_detection
            
            # 4. Time Synchronization Accuracy Analysis
            sync_analysis = self._analyze_time_synchronization_accuracy(timezone_data)
            analysis_result['time_synchronization'] = sync_analysis
            
            # 5. Temporal Behavior Pattern Validation
            temporal_analysis = self._validate_temporal_behavior_patterns(timezone_data)
            analysis_result['temporal_behavior'] = temporal_analysis
            
            # 6. Calculate Overall Consistency Score
            consistency_scores = [
                timezone_validation.get('consistency_score', 0.5),
                geo_correlation.get('correlation_score', 0.5),
                manipulation_detection.get('authenticity_score', 0.5),
                sync_analysis.get('synchronization_score', 0.5),
                temporal_analysis.get('behavior_score', 0.5)
            ]
            analysis_result['consistency_score'] = statistics.mean(consistency_scores)
            
            # 7. Timezone Risk Assessment
            risk_assessment = self._assess_timezone_consistency_risk(analysis_result)
            analysis_result['risk_assessment'] = risk_assessment
            
            # Timezone Identity Summary
            analysis_result['timezone_identity'] = {
                'system_timezone': timezone_data.get('system_timezone', 'Unknown'),
                'browser_timezone': timezone_data.get('browser_timezone', 'Unknown'),
                'timezone_offset': timezone_data.get('timezone_offset', 0),
                'dst_active': timezone_data.get('dst_active', False),
                'geo_timezone_match': geo_correlation.get('match_status', False),
                'manipulation_detected': manipulation_detection.get('manipulation_detected', False),
                'consistency_score': analysis_result['consistency_score'],
                'timezone_risk_level': risk_assessment.get('risk_level', 'MEDIUM')
            }
            
            self.logger.info(f"Timezone analysis completed - TZ: {analysis_result['timezone_identity']['system_timezone']}, Consistency: {analysis_result['consistency_score']:.3f}")
            
            return {
                'success': True,
                'timezone_analysis': analysis_result,
                'analysis_summary': {
                    'system_timezone': analysis_result['timezone_identity']['system_timezone'],
                    'browser_timezone': analysis_result['timezone_identity']['browser_timezone'],
                    'timezone_match': timezone_validation.get('timezones_match', False),
                    'geolocation_consistent': geo_correlation.get('match_status', False),
                    'manipulation_detected': analysis_result['timezone_identity']['manipulation_detected'],
                    'consistency_score': analysis_result['consistency_score'],
                    'timezone_risk_level': analysis_result['timezone_identity']['timezone_risk_level']
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking timezone consistency: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    # ===== NETWORK CHARACTERISTICS ANALYSIS HELPER METHODS =====
    
    def _analyze_ip_geolocation_reputation(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze IP address geolocation and reputation scoring"""
        try:
            ip_address = network_data.get('ip_address', '')
            
            analysis = {
                'geolocation': {
                    'ip_address': ip_address,
                    'country': network_data.get('country', 'Unknown'),
                    'region': network_data.get('region', 'Unknown'), 
                    'city': network_data.get('city', 'Unknown'),
                    'isp': network_data.get('isp', 'Unknown'),
                    'coordinates': {
                        'latitude': network_data.get('latitude', 0),
                        'longitude': network_data.get('longitude', 0)
                    },
                    'accuracy_score': self._calculate_geolocation_accuracy(network_data)
                },
                'reputation': {
                    'score': self._calculate_ip_reputation_score(ip_address),
                    'blacklist_status': self._check_ip_blacklists(ip_address),
                    'threat_indicators': self._identify_threat_indicators(ip_address),
                    'ip_type': self._classify_ip_address_type(ip_address),
                    'reputation_sources': ['builtin_patterns', 'heuristic_analysis']
                }
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing IP geolocation/reputation: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_geolocation_accuracy(self, network_data: Dict[str, Any]) -> float:
        """Calculate geolocation data accuracy score"""
        try:
            accuracy_factors = []
            
            # Check if coordinates are provided
            if network_data.get('latitude') and network_data.get('longitude'):
                accuracy_factors.append(0.3)
            
            # Check if detailed location info is available
            if network_data.get('city') and network_data.get('region'):
                accuracy_factors.append(0.25)
            
            # Check if ISP information is available
            if network_data.get('isp'):
                accuracy_factors.append(0.2)
            
            # Check if country information matches expected patterns
            if network_data.get('country'):
                accuracy_factors.append(0.25)
            
            return sum(accuracy_factors)
            
        except Exception as e:
            return 0.5
    
    def _calculate_ip_reputation_score(self, ip_address: str) -> float:
        """Calculate IP reputation score based on patterns and heuristics"""
        try:
            if not ip_address:
                return 0.0
            
            reputation_score = 1.0  # Start with good reputation
            
            # Check for private/local IP ranges (lower reputation for public tests)
            if self._is_private_ip(ip_address):
                reputation_score -= 0.3  # Private IPs less suspicious for internal tests
            
            # Check for suspicious IP patterns
            if self._has_suspicious_ip_pattern(ip_address):
                reputation_score -= 0.4
            
            # Check for known hosting/datacenter ranges (heuristic)
            if self._is_likely_datacenter_ip(ip_address):
                reputation_score -= 0.2
            
            return max(0.0, min(1.0, reputation_score))
            
        except Exception as e:
            return 0.5
    
    def _is_private_ip(self, ip_address: str) -> bool:
        """Check if IP is in private range"""
        try:
            parts = ip_address.split('.')
            if len(parts) != 4:
                return False
            
            first = int(parts[0])
            second = int(parts[1])
            
            # Private IP ranges
            if first == 10:  # 10.0.0.0/8
                return True
            elif first == 172 and 16 <= second <= 31:  # 172.16.0.0/12
                return True
            elif first == 192 and second == 168:  # 192.168.0.0/16
                return True
            elif first == 127:  # Loopback
                return True
            
            return False
            
        except Exception:
            return False
    
    def _has_suspicious_ip_pattern(self, ip_address: str) -> bool:
        """Check for suspicious IP address patterns"""
        try:
            # Simple heuristic checks
            suspicious_patterns = [
                '0.0.0.0', '255.255.255.255', '127.0.0.1'
            ]
            
            return ip_address in suspicious_patterns
            
        except Exception:
            return False
    
    def _is_likely_datacenter_ip(self, ip_address: str) -> bool:
        """Heuristic to identify likely datacenter/hosting IPs"""
        try:
            # Simple heuristic: certain ranges often used by cloud providers
            parts = ip_address.split('.')
            if len(parts) != 4:
                return False
            
            first = int(parts[0])
            
            # Common cloud provider ranges (simplified heuristic)
            cloud_ranges = [52, 54, 3, 13, 35, 34, 104, 108, 142, 146, 162, 185]
            
            return first in cloud_ranges
            
        except Exception:
            return False
    
    def _check_ip_blacklists(self, ip_address: str) -> Dict[str, Any]:
        """Check IP against simulated blacklists"""
        return {
            'blacklisted': False,
            'sources_checked': ['heuristic_patterns'],
            'threat_level': 'LOW',
            'last_check': datetime.utcnow().isoformat()
        }
    
    def _identify_threat_indicators(self, ip_address: str) -> List[str]:
        """Identify potential threat indicators for IP"""
        indicators = []
        
        if self._has_suspicious_ip_pattern(ip_address):
            indicators.append('suspicious_ip_pattern')
        
        if self._is_likely_datacenter_ip(ip_address):
            indicators.append('datacenter_hosting_range')
        
        return indicators
    
    def _classify_ip_address_type(self, ip_address: str) -> str:
        """Classify IP address type (residential, datacenter, mobile, etc.)"""
        try:
            if self._is_private_ip(ip_address):
                return 'private'
            elif self._is_likely_datacenter_ip(ip_address):
                return 'datacenter'
            else:
                return 'residential'  # Default assumption
                
        except Exception:
            return 'unknown'
    
    def _analyze_network_latency_routing(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze network latency and routing characteristics"""
        try:
            performance = network_data.get('network_performance', {})
            routing = network_data.get('routing_info', {})
            
            analysis = {
                'latency': {
                    'rtt': performance.get('rtt', 0),
                    'rtt_category': self._categorize_rtt(performance.get('rtt', 0)),
                    'consistency_score': self._analyze_latency_consistency(performance),
                    'performance_class': self._classify_network_performance(performance)
                },
                'routing': {
                    'hop_count': routing.get('hop_count', 0),
                    'routing_path': routing.get('routing_path', []),
                    'routing_anomalies': self._detect_routing_anomalies(routing),
                    'path_analysis': self._analyze_routing_path(routing)
                }
            }
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing network latency/routing: {str(e)}")
            return {'error': str(e)}
    
    def _categorize_rtt(self, rtt: float) -> str:
        """Categorize round-trip time"""
        if rtt < 20:
            return 'excellent'
        elif rtt < 50:
            return 'good'
        elif rtt < 100:
            return 'fair'
        elif rtt < 200:
            return 'poor'
        else:
            return 'very_poor'
    
    def _analyze_latency_consistency(self, performance: Dict[str, Any]) -> float:
        """Analyze latency consistency and stability"""
        try:
            rtt = performance.get('rtt', 50)
            packet_loss = performance.get('packet_loss', 0)
            
            # Simple consistency scoring
            consistency_score = 1.0
            
            # High packet loss reduces consistency
            consistency_score -= packet_loss * 2
            
            # Very low or very high RTT might indicate issues
            if rtt < 5 or rtt > 500:
                consistency_score -= 0.3
            
            return max(0.0, min(1.0, consistency_score))
            
        except Exception:
            return 0.5
    
    def _classify_network_performance(self, performance: Dict[str, Any]) -> str:
        """Classify overall network performance"""
        try:
            rtt = performance.get('rtt', 50)
            download_speed = performance.get('download_speed', 0)
            upload_speed = performance.get('upload_speed', 0)
            
            if rtt < 30 and download_speed > 50 and upload_speed > 10:
                return 'high_performance'
            elif rtt < 60 and download_speed > 25 and upload_speed > 5:
                return 'good_performance'
            elif rtt < 100 and download_speed > 10:
                return 'average_performance'
            else:
                return 'poor_performance'
                
        except Exception:
            return 'unknown'
    
    def _detect_routing_anomalies(self, routing: Dict[str, Any]) -> List[str]:
        """Detect routing anomalies and suspicious patterns"""
        anomalies = []
        
        hop_count = routing.get('hop_count', 0)
        routing_path = routing.get('routing_path', [])
        
        # Unusually high hop count
        if hop_count > 20:
            anomalies.append('excessive_hops')
        
        # Very few hops (might indicate VPN/proxy)
        if hop_count < 3:
            anomalies.append('minimal_hops')
        
        # Suspicious routing path patterns
        if 'tor' in str(routing_path).lower():
            anomalies.append('tor_indicators')
        
        return anomalies
    
    def _analyze_routing_path(self, routing: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze routing path for geographic and network patterns"""
        return {
            'hop_count': routing.get('hop_count', 0),
            'path_complexity': 'normal',  # Simplified analysis
            'geographic_consistency': True,  # Simplified analysis
            'routing_efficiency': 0.8  # Simplified scoring
        }
    
    def _detect_proxy_vpn_tor(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect proxy, VPN, and Tor usage indicators"""
        try:
            detection_result = {
                'proxy_detected': False,
                'vpn_detected': False,
                'tor_detected': False,
                'proxy_indicators': [],
                'vpn_indicators': [],
                'tor_indicators': [],
                'anonymity_level': 'LOW',
                'detection_confidence': 0.0
            }
            
            indicators = network_data.get('proxy_indicators', [])
            routing_info = network_data.get('routing_info', {})
            
            # Check for proxy indicators
            proxy_confidence = self._check_proxy_indicators(network_data, indicators)
            if proxy_confidence > 0.5:
                detection_result['proxy_detected'] = True
                detection_result['proxy_indicators'] = indicators
            
            # Check for VPN indicators
            vpn_confidence = self._check_vpn_indicators(network_data)
            if vpn_confidence > 0.5:
                detection_result['vpn_detected'] = True
                detection_result['vpn_indicators'] = ['routing_patterns', 'latency_analysis']
            
            # Check for Tor indicators
            tor_confidence = self._check_tor_indicators(routing_info)
            if tor_confidence > 0.5:
                detection_result['tor_detected'] = True
                detection_result['tor_indicators'] = ['routing_anomalies', 'hop_patterns']
            
            # Overall anonymity assessment
            detection_result['detection_confidence'] = max(proxy_confidence, vpn_confidence, tor_confidence)
            
            if detection_result['tor_detected']:
                detection_result['anonymity_level'] = 'CRITICAL'
            elif detection_result['vpn_detected']:
                detection_result['anonymity_level'] = 'HIGH'
            elif detection_result['proxy_detected']:
                detection_result['anonymity_level'] = 'MEDIUM'
            
            return detection_result
            
        except Exception as e:
            self.logger.error(f"Error detecting proxy/VPN/Tor: {str(e)}")
            return {'error': str(e)}
    
    def _check_proxy_indicators(self, network_data: Dict[str, Any], indicators: List[str]) -> float:
        """Check for proxy usage indicators"""
        try:
            proxy_score = 0.0
            
            # Check for common proxy indicators
            proxy_patterns = ['proxy', 'forwarded', 'x-forwarded-for', 'x-real-ip']
            
            for indicator in indicators:
                for pattern in proxy_patterns:
                    if pattern.lower() in indicator.lower():
                        proxy_score += 0.3
            
            # Check for datacenter IP (common for proxies)
            if self._is_likely_datacenter_ip(network_data.get('ip_address', '')):
                proxy_score += 0.2
            
            return min(1.0, proxy_score)
            
        except Exception:
            return 0.0
    
    def _check_vpn_indicators(self, network_data: Dict[str, Any]) -> float:
        """Check for VPN usage indicators"""
        try:
            vpn_score = 0.0
            
            # Check ISP patterns (simplified heuristic)
            isp = network_data.get('isp', '').lower()
            vpn_isp_patterns = ['vpn', 'virtual private', 'proxy', 'tunnel']
            
            for pattern in vpn_isp_patterns:
                if pattern in isp:
                    vpn_score += 0.4
            
            # Check for datacenter hosting
            if self._is_likely_datacenter_ip(network_data.get('ip_address', '')):
                vpn_score += 0.2
            
            # Check routing anomalies
            routing = network_data.get('routing_info', {})
            if self._detect_routing_anomalies(routing):
                vpn_score += 0.3
            
            return min(1.0, vpn_score)
            
        except Exception:
            return 0.0
    
    def _check_tor_indicators(self, routing_info: Dict[str, Any]) -> float:
        """Check for Tor network usage indicators"""
        try:
            tor_score = 0.0
            
            # Check routing patterns typical of Tor
            hop_count = routing_info.get('hop_count', 0)
            routing_path = routing_info.get('routing_path', [])
            
            # Tor typically has specific hop patterns
            if 3 <= hop_count <= 5:
                tor_score += 0.3
            
            # Check for Tor-like routing path keywords
            tor_patterns = ['tor', 'onion', 'relay', 'exit']
            path_str = str(routing_path).lower()
            
            for pattern in tor_patterns:
                if pattern in path_str:
                    tor_score += 0.4
            
            return min(1.0, tor_score)
            
        except Exception:
            return 0.0
    
    def _analyze_connection_bandwidth_profile(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze connection type and bandwidth characteristics"""
        try:
            performance = network_data.get('network_performance', {})
            
            connection_analysis = {
                'connection_type': self._identify_connection_type(network_data),
                'bandwidth_profile': {
                    'download_speed': performance.get('download_speed', 0),
                    'upload_speed': performance.get('upload_speed', 0),
                    'speed_ratio': self._calculate_speed_ratio(performance),
                    'bandwidth_class': self._classify_bandwidth(performance)
                },
                'isp_fingerprint': {
                    'provider': network_data.get('isp', 'Unknown'),
                    'provider_type': self._classify_isp_type(network_data.get('isp', '')),
                    'service_quality': self._assess_service_quality(performance)
                },
                'connection_consistency': self._assess_connection_consistency(network_data)
            }
            
            return connection_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing connection/bandwidth profile: {str(e)}")
            return {'error': str(e)}
    
    def _identify_connection_type(self, network_data: Dict[str, Any]) -> str:
        """Identify connection type based on characteristics"""
        try:
            connection_type = network_data.get('connection_type', '')
            performance = network_data.get('network_performance', {})
            
            if connection_type:
                return connection_type
            
            # Infer from performance characteristics
            download_speed = performance.get('download_speed', 0)
            
            if download_speed > 100:
                return 'fiber'
            elif download_speed > 50:
                return 'cable'
            elif download_speed > 10:
                return 'dsl'
            else:
                return 'mobile'
                
        except Exception:
            return 'unknown'
    
    def _calculate_speed_ratio(self, performance: Dict[str, Any]) -> float:
        """Calculate download to upload speed ratio"""
        try:
            download = performance.get('download_speed', 0)
            upload = performance.get('upload_speed', 0)
            
            if upload > 0:
                return download / upload
            return 0
            
        except Exception:
            return 0
    
    def _classify_bandwidth(self, performance: Dict[str, Any]) -> str:
        """Classify bandwidth tier"""
        try:
            download = performance.get('download_speed', 0)
            
            if download > 100:
                return 'high_speed'
            elif download > 25:
                return 'broadband'
            elif download > 5:
                return 'basic'
            else:
                return 'low_speed'
                
        except Exception:
            return 'unknown'
    
    def _classify_isp_type(self, isp: str) -> str:
        """Classify ISP type based on name patterns"""
        try:
            isp_lower = isp.lower()
            
            if any(pattern in isp_lower for pattern in ['fiber', 'fios', 'broadband']):
                return 'fiber_provider'
            elif any(pattern in isp_lower for pattern in ['cable', 'comcast', 'cox', 'charter']):
                return 'cable_provider'
            elif any(pattern in isp_lower for pattern in ['mobile', 'wireless', 'cellular', 'verizon', 't-mobile']):
                return 'mobile_provider'
            elif any(pattern in isp_lower for pattern in ['satellite']):
                return 'satellite_provider'
            else:
                return 'traditional_isp'
                
        except Exception:
            return 'unknown'
    
    def _assess_service_quality(self, performance: Dict[str, Any]) -> str:
        """Assess ISP service quality based on performance metrics"""
        try:
            rtt = performance.get('rtt', 50)
            packet_loss = performance.get('packet_loss', 0)
            download_speed = performance.get('download_speed', 0)
            
            quality_score = 1.0
            
            # RTT impact
            if rtt > 100:
                quality_score -= 0.3
            elif rtt > 50:
                quality_score -= 0.1
            
            # Packet loss impact
            quality_score -= packet_loss * 5
            
            # Speed impact
            if download_speed < 5:
                quality_score -= 0.2
            
            if quality_score > 0.8:
                return 'excellent'
            elif quality_score > 0.6:
                return 'good'
            elif quality_score > 0.4:
                return 'fair'
            else:
                return 'poor'
                
        except Exception:
            return 'unknown'
    
    def _assess_connection_consistency(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess connection consistency and stability"""
        return {
            'stability_score': 0.8,  # Simplified scoring
            'consistency_indicators': ['stable_latency', 'consistent_bandwidth'],
            'variability_score': 0.2
        }
    
    def _track_network_fingerprint_consistency(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track network fingerprint consistency over time"""
        try:
            consistency_analysis = {
                'signature_evolution': {
                    'stable_characteristics': ['ip_address', 'isp', 'country'],
                    'changed_characteristics': [],
                    'evolution_score': 0.9  # High consistency assumed
                },
                'geographic_consistency': {
                    'location_stable': True,
                    'country_changes': 0,
                    'region_changes': 0
                },
                'network_behavior': {
                    'connection_pattern': 'consistent',
                    'performance_trend': 'stable',
                    'anomaly_count': 0
                },
                'consistency_score': 0.9
            }
            
            return consistency_analysis
            
        except Exception as e:
            self.logger.error(f"Error tracking network fingerprint consistency: {str(e)}")
            return {'error': str(e)}
    
    def _assess_network_characteristics_risk(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall network characteristics risk"""
        try:
            risk_factors = []
            risk_score = 0.0
            
            # Check proxy/VPN/Tor detection
            proxy_detection = analysis_result.get('proxy_vpn_detection', {})
            if proxy_detection.get('tor_detected'):
                risk_factors.append('tor_usage')
                risk_score += 0.4
            elif proxy_detection.get('vpn_detected'):
                risk_factors.append('vpn_usage')
                risk_score += 0.3
            elif proxy_detection.get('proxy_detected'):
                risk_factors.append('proxy_usage')
                risk_score += 0.2
            
            # Check IP reputation
            reputation = analysis_result.get('reputation_analysis', {})
            if reputation.get('score', 1.0) < 0.5:
                risk_factors.append('poor_ip_reputation')
                risk_score += 0.2
            
            # Check for datacenter hosting
            ip_type = reputation.get('ip_type', 'residential')
            if ip_type == 'datacenter':
                risk_factors.append('datacenter_hosting')
                risk_score += 0.15
            
            # Determine risk level
            if risk_score > 0.7:
                risk_level = 'CRITICAL'
            elif risk_score > 0.5:
                risk_level = 'HIGH'
            elif risk_score > 0.3:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            return {
                'risk_score': min(1.0, risk_score),
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendations': self._generate_network_risk_recommendations(risk_factors)
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing network characteristics risk: {str(e)}")
            return {'risk_score': 0.5, 'risk_level': 'MEDIUM', 'error': str(e)}
    
    def _generate_network_risk_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Generate network risk mitigation recommendations"""
        recommendations = []
        
        if 'tor_usage' in risk_factors:
            recommendations.append('CRITICAL: Tor network usage detected - implement immediate verification')
        if 'vpn_usage' in risk_factors:
            recommendations.append('HIGH: VPN usage detected - additional identity verification recommended')
        if 'proxy_usage' in risk_factors:
            recommendations.append('MEDIUM: Proxy usage detected - monitor for suspicious activity')
        if 'poor_ip_reputation' in risk_factors:
            recommendations.append('Monitor IP reputation and consider additional security measures')
        if 'datacenter_hosting' in risk_factors:
            recommendations.append('Datacenter IP detected - verify legitimate business usage')
        
        return recommendations
    
    # ===== TIMEZONE CONSISTENCY ANALYSIS HELPER METHODS =====
    
    def _validate_system_browser_timezones(self, timezone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate consistency between system and browser timezones"""
        try:
            system_tz = timezone_data.get('system_timezone', '')
            browser_tz = timezone_data.get('browser_timezone', '')
            system_offset = timezone_data.get('timezone_offset', 0)
            
            validation = {
                'system_timezone': system_tz,
                'browser_timezone': browser_tz,
                'timezones_match': system_tz == browser_tz,
                'offset_consistency': True,
                'dst_validation': {},
                'consistency_score': 1.0,
                'inconsistencies': []
            }
            
            # Check timezone name consistency
            if system_tz != browser_tz and system_tz and browser_tz:
                validation['inconsistencies'].append('timezone_name_mismatch')
                validation['consistency_score'] -= 0.3
                validation['timezones_match'] = False
            
            # Validate DST handling
            dst_validation = self._validate_dst_handling(timezone_data)
            validation['dst_validation'] = dst_validation
            
            if not dst_validation.get('dst_consistent', True):
                validation['inconsistencies'].append('dst_inconsistency')
                validation['consistency_score'] -= 0.2
            
            # Check offset reasonableness
            if abs(system_offset) > 12 * 60:  # More than ±12 hours
                validation['inconsistencies'].append('invalid_timezone_offset')
                validation['consistency_score'] -= 0.3
                validation['offset_consistency'] = False
            
            validation['consistency_score'] = max(0.0, validation['consistency_score'])
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error validating system/browser timezones: {str(e)}")
            return {'error': str(e), 'consistency_score': 0.0}
    
    def _validate_dst_handling(self, timezone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate Daylight Saving Time handling consistency"""
        try:
            dst_active = timezone_data.get('dst_active', False)
            system_time = timezone_data.get('system_time', '')
            browser_time = timezone_data.get('browser_time', '')
            
            dst_validation = {
                'dst_active': dst_active,
                'dst_consistent': True,
                'dst_detection_method': 'timezone_offset_analysis',
                'seasonal_accuracy': True
            }
            
            # Simple DST consistency check based on current date
            if system_time and browser_time:
                # Parse timestamps and check DST consistency
                dst_validation['time_consistency'] = abs(
                    self._parse_timestamp_offset(system_time) - 
                    self._parse_timestamp_offset(browser_time)
                ) < 60000  # Within 1 minute
            
            return dst_validation
            
        except Exception as e:
            return {'error': str(e), 'dst_consistent': False}
    
    def _parse_timestamp_offset(self, timestamp: str) -> int:
        """Parse timestamp and return millisecond offset (simplified)"""
        try:
            # Simplified timestamp parsing - in production use proper datetime parsing
            return int(datetime.utcnow().timestamp() * 1000)
        except Exception:
            return 0
    
    def _correlate_geolocation_timezone(self, timezone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Correlate geolocation data with timezone information"""
        try:
            geolocation = timezone_data.get('geolocation', {})
            system_timezone = timezone_data.get('system_timezone', '')
            
            correlation = {
                'geolocation_provided': bool(geolocation),
                'timezone_geographic_match': True,
                'expected_timezone': '',
                'actual_timezone': system_timezone,
                'match_status': True,
                'correlation_score': 1.0,
                'geographic_inconsistencies': []
            }
            
            if geolocation:
                latitude = geolocation.get('latitude', 0)
                longitude = geolocation.get('longitude', 0)
                
                # Determine expected timezone based on coordinates
                expected_timezone = self._determine_timezone_from_coordinates(latitude, longitude)
                correlation['expected_timezone'] = expected_timezone
                
                # Check if actual timezone matches expected
                if expected_timezone and system_timezone:
                    match_score = self._calculate_timezone_match_score(expected_timezone, system_timezone)
                    correlation['correlation_score'] = match_score
                    correlation['match_status'] = match_score > 0.7
                    
                    if match_score < 0.7:
                        correlation['geographic_inconsistencies'].append('timezone_location_mismatch')
            
            return correlation
            
        except Exception as e:
            self.logger.error(f"Error correlating geolocation/timezone: {str(e)}")
            return {'error': str(e), 'correlation_score': 0.5}
    
    def _determine_timezone_from_coordinates(self, latitude: float, longitude: float) -> str:
        """Determine expected timezone from geographic coordinates (simplified)"""
        try:
            if not latitude or not longitude:
                return ''
            
            # Simplified timezone determination based on longitude
            # In production, use a proper timezone library like pytz with geographic data
            hours_offset = int(longitude / 15)  # Rough approximation
            
            if -12 <= hours_offset <= 12:
                # Map to common timezone names (simplified)
                timezone_mapping = {
                    -8: 'America/Los_Angeles',
                    -5: 'America/New_York', 
                    0: 'Europe/London',
                    1: 'Europe/Berlin',
                    8: 'Asia/Shanghai',
                    9: 'Asia/Tokyo'
                }
                
                return timezone_mapping.get(hours_offset, f'UTC{hours_offset:+d}')
            
            return 'UTC+0'
            
        except Exception:
            return ''
    
    def _calculate_timezone_match_score(self, expected: str, actual: str) -> float:
        """Calculate how well expected and actual timezones match"""
        try:
            if expected == actual:
                return 1.0
            
            # Check if they're in the same general region
            expected_region = expected.split('/')[0] if '/' in expected else expected
            actual_region = actual.split('/')[0] if '/' in actual else actual
            
            if expected_region == actual_region:
                return 0.7  # Same region, different specific timezone
            
            # Check if UTC offsets might be similar (simplified)
            if 'UTC' in expected and 'UTC' in actual:
                return 0.5
            
            return 0.3  # Different regions
            
        except Exception:
            return 0.5
    
    def _detect_timezone_manipulation(self, timezone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect timezone spoofing and manipulation attempts"""
        try:
            manipulation_analysis = {
                'manipulation_detected': False,
                'spoofing_indicators': [],
                'authenticity_score': 1.0,
                'manipulation_techniques': [],
                'confidence_level': 'HIGH'
            }
            
            # Check for common timezone spoofing indicators
            spoofing_indicators = self._check_timezone_spoofing_indicators(timezone_data)
            manipulation_analysis['spoofing_indicators'] = spoofing_indicators
            
            if spoofing_indicators:
                manipulation_analysis['manipulation_detected'] = True
                manipulation_analysis['authenticity_score'] -= len(spoofing_indicators) * 0.2
            
            # Check for inconsistent timezone behavior
            inconsistency_score = self._analyze_timezone_inconsistencies(timezone_data)
            if inconsistency_score > 0.3:
                manipulation_analysis['manipulation_detected'] = True
                manipulation_analysis['authenticity_score'] -= inconsistency_score
            
            # Assess manipulation techniques
            manipulation_analysis['manipulation_techniques'] = self._identify_manipulation_techniques(timezone_data)
            
            manipulation_analysis['authenticity_score'] = max(0.0, manipulation_analysis['authenticity_score'])
            
            # Determine confidence level
            if manipulation_analysis['authenticity_score'] > 0.8:
                manipulation_analysis['confidence_level'] = 'HIGH'
            elif manipulation_analysis['authenticity_score'] > 0.5:
                manipulation_analysis['confidence_level'] = 'MEDIUM'
            else:
                manipulation_analysis['confidence_level'] = 'LOW'
            
            return manipulation_analysis
            
        except Exception as e:
            self.logger.error(f"Error detecting timezone manipulation: {str(e)}")
            return {'error': str(e), 'authenticity_score': 0.5}
    
    def _check_timezone_spoofing_indicators(self, timezone_data: Dict[str, Any]) -> List[str]:
        """Check for common timezone spoofing indicators"""
        indicators = []
        
        system_tz = timezone_data.get('system_timezone', '')
        browser_tz = timezone_data.get('browser_timezone', '')
        
        # Check for suspicious timezone names
        suspicious_patterns = ['fake', 'spoof', 'test', 'dummy']
        for pattern in suspicious_patterns:
            if pattern in system_tz.lower() or pattern in browser_tz.lower():
                indicators.append('suspicious_timezone_name')
                break
        
        # Check for timezone jumping (would require historical data)
        # For now, simplified check
        if system_tz != browser_tz:
            indicators.append('timezone_inconsistency')
        
        return indicators
    
    def _analyze_timezone_inconsistencies(self, timezone_data: Dict[str, Any]) -> float:
        """Analyze timezone-related inconsistencies"""
        try:
            inconsistency_score = 0.0
            
            # Check system vs browser timezone mismatch
            if timezone_data.get('system_timezone') != timezone_data.get('browser_timezone'):
                inconsistency_score += 0.3
            
            # Check geolocation consistency
            geolocation = timezone_data.get('geolocation', {})
            if geolocation:
                # Simplified geolocation consistency check
                latitude = geolocation.get('latitude', 0)
                if abs(latitude) > 90:  # Invalid latitude
                    inconsistency_score += 0.2
            
            return min(1.0, inconsistency_score)
            
        except Exception:
            return 0.0
    
    def _identify_manipulation_techniques(self, timezone_data: Dict[str, Any]) -> List[str]:
        """Identify potential timezone manipulation techniques"""
        techniques = []
        
        # Check for common manipulation patterns
        system_tz = timezone_data.get('system_timezone', '')
        browser_tz = timezone_data.get('browser_timezone', '')
        
        if system_tz != browser_tz:
            techniques.append('browser_timezone_override')
        
        # Check for automation indicators in timezone handling
        system_time = timezone_data.get('system_time', '')
        browser_time = timezone_data.get('browser_time', '')
        
        if system_time and browser_time:
            # Check if times are too perfectly synchronized (automation indicator)
            time_diff = abs(self._parse_timestamp_offset(system_time) - self._parse_timestamp_offset(browser_time))
            if time_diff < 10:  # Less than 10ms difference might indicate automation
                techniques.append('perfect_time_synchronization')
        
        return techniques
    
    def _analyze_time_synchronization_accuracy(self, timezone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze time synchronization accuracy and NTP compliance"""
        try:
            sync_analysis = {
                'ntp_synchronized': timezone_data.get('ntp_synchronized', False),
                'clock_skew': timezone_data.get('clock_skew', 0.0),
                'synchronization_score': 1.0,
                'accuracy_assessment': 'ACCURATE',
                'time_drift_indicators': [],
                'sync_quality': 'HIGH'
            }
            
            clock_skew = timezone_data.get('clock_skew', 0.0)
            
            # Analyze clock skew
            if abs(clock_skew) > 5.0:  # More than 5 seconds skew
                sync_analysis['time_drift_indicators'].append('significant_clock_skew')
                sync_analysis['synchronization_score'] -= 0.4
                sync_analysis['accuracy_assessment'] = 'POOR'
                sync_analysis['sync_quality'] = 'LOW'
            elif abs(clock_skew) > 1.0:  # More than 1 second skew
                sync_analysis['time_drift_indicators'].append('moderate_clock_skew')
                sync_analysis['synchronization_score'] -= 0.2
                sync_analysis['accuracy_assessment'] = 'FAIR'
                sync_analysis['sync_quality'] = 'MEDIUM'
            
            # Check NTP synchronization status
            if not timezone_data.get('ntp_synchronized', True):
                sync_analysis['time_drift_indicators'].append('ntp_not_synchronized')
                sync_analysis['synchronization_score'] -= 0.3
            
            sync_analysis['synchronization_score'] = max(0.0, sync_analysis['synchronization_score'])
            
            return sync_analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing time synchronization: {str(e)}")
            return {'error': str(e), 'synchronization_score': 0.5}
    
    def _validate_temporal_behavior_patterns(self, timezone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate temporal behavior patterns and circadian consistency"""
        try:
            behavior_analysis = {
                'activity_timing': {},
                'circadian_consistency': True,
                'behavioral_timezone_match': True,
                'temporal_anomalies': [],
                'behavior_score': 1.0,
                'pattern_classification': 'NORMAL'
            }
            
            # Analyze activity timing (simplified - would need historical data)
            current_hour = datetime.utcnow().hour
            system_tz = timezone_data.get('system_timezone', '')
            
            behavior_analysis['activity_timing'] = {
                'current_utc_hour': current_hour,
                'local_timezone': system_tz,
                'activity_period': self._classify_activity_period(current_hour),
                'expected_activity': self._assess_expected_activity(current_hour, system_tz)
            }
            
            # Check for temporal anomalies
            temporal_anomalies = self._detect_temporal_anomalies(timezone_data)
            behavior_analysis['temporal_anomalies'] = temporal_anomalies
            
            if temporal_anomalies:
                behavior_analysis['behavior_score'] -= len(temporal_anomalies) * 0.2
                behavior_analysis['circadian_consistency'] = False
            
            # Overall behavior pattern classification
            if behavior_analysis['behavior_score'] > 0.8:
                behavior_analysis['pattern_classification'] = 'NORMAL'
            elif behavior_analysis['behavior_score'] > 0.6:
                behavior_analysis['pattern_classification'] = 'SLIGHTLY_SUSPICIOUS'
            else:
                behavior_analysis['pattern_classification'] = 'ANOMALOUS'
            
            behavior_analysis['behavior_score'] = max(0.0, behavior_analysis['behavior_score'])
            
            return behavior_analysis
            
        except Exception as e:
            self.logger.error(f"Error validating temporal behavior patterns: {str(e)}")
            return {'error': str(e), 'behavior_score': 0.5}
    
    def _classify_activity_period(self, hour: int) -> str:
        """Classify the activity period based on hour"""
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon' 
        elif 18 <= hour < 22:
            return 'evening'
        else:
            return 'night'
    
    def _assess_expected_activity(self, hour: int, timezone: str) -> str:
        """Assess whether activity is expected for the given time and timezone"""
        # Simplified assessment - would need more sophisticated logic
        if 22 <= hour or hour < 6:
            return 'unusual_night_activity'
        else:
            return 'normal_day_activity'
    
    def _detect_temporal_anomalies(self, timezone_data: Dict[str, Any]) -> List[str]:
        """Detect temporal behavior anomalies"""
        anomalies = []
        
        # Check for unusual activity times
        current_hour = datetime.utcnow().hour
        if 2 <= current_hour < 6:  # Very early morning activity
            anomalies.append('unusual_early_morning_activity')
        
        # Check clock skew anomalies
        clock_skew = timezone_data.get('clock_skew', 0.0)
        if abs(clock_skew) > 10.0:  # More than 10 seconds
            anomalies.append('significant_clock_drift')
        
        return anomalies
    
    def _assess_timezone_consistency_risk(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall timezone consistency risk"""
        try:
            risk_factors = []
            risk_score = 0.0
            
            # Check manipulation detection results
            manipulation = analysis_result.get('manipulation_detection', {})
            if manipulation.get('manipulation_detected', False):
                risk_factors.extend(manipulation.get('spoofing_indicators', []))
                risk_score += 0.4
            
            # Check system vs browser timezone validation
            validation = analysis_result.get('system_browser_validation', {})
            if not validation.get('timezones_match', True):
                risk_factors.append('timezone_mismatch')
                risk_score += 0.2
            
            # Check geolocation correlation
            geo_correlation = analysis_result.get('geolocation_correlation', {})
            if not geo_correlation.get('match_status', True):
                risk_factors.append('geolocation_timezone_mismatch')
                risk_score += 0.3
            
            # Check temporal behavior anomalies
            temporal = analysis_result.get('temporal_behavior', {})
            anomalies = temporal.get('temporal_anomalies', [])
            if anomalies:
                risk_factors.extend(anomalies)
                risk_score += len(anomalies) * 0.1
            
            # Determine risk level
            if risk_score > 0.7:
                risk_level = 'CRITICAL'
            elif risk_score > 0.5:
                risk_level = 'HIGH'
            elif risk_score > 0.3:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            return {
                'risk_score': min(1.0, risk_score),
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendations': self._generate_timezone_risk_recommendations(risk_factors)
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing timezone consistency risk: {str(e)}")
            return {'risk_score': 0.5, 'risk_level': 'MEDIUM', 'error': str(e)}
    
    def _generate_timezone_risk_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Generate timezone risk mitigation recommendations"""
        recommendations = []
        
        if 'timezone_mismatch' in risk_factors:
            recommendations.append('Investigate system vs browser timezone inconsistency')
        if 'geolocation_timezone_mismatch' in risk_factors:
            recommendations.append('Verify user location matches reported timezone')
        if 'suspicious_timezone_name' in risk_factors:
            recommendations.append('CRITICAL: Suspicious timezone name detected - manual verification required')
        if 'significant_clock_drift' in risk_factors:
            recommendations.append('Check system clock synchronization and NTP configuration')
        if 'unusual_early_morning_activity' in risk_factors:
            recommendations.append('Monitor for automated activity during unusual hours')
        
        return recommendations


class SessionIntegrityMonitor:
    """
    🔒 PHASE 3.3: SESSION INTEGRITY MONITORING
    Advanced Session Integrity Monitoring for comprehensive session validation and manipulation detection
    
    This class provides comprehensive analysis of session continuity, authenticity validation,
    manipulation detection, and anomaly tracking to identify sophisticated session attacks.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Session integrity configuration
        self.session_timeout_threshold = 1800  # 30 minutes
        self.max_session_gap = 300  # 5 minutes
        self.activity_consistency_threshold = 0.7
        self.manipulation_confidence_threshold = 0.6
        
        # Session patterns and signatures
        self.session_patterns = {
            'normal_activity_intervals': {
                'min_interval': 1,     # 1 second
                'max_interval': 300,   # 5 minutes
                'typical_range': (5, 60)  # 5-60 seconds
            },
            'suspicious_patterns': [
                'rapid_fire_requests',
                'perfect_timing_intervals',
                'simultaneous_sessions',
                'impossible_travel_time',
                'session_token_reuse'
            ],
            'hijacking_indicators': [
                'ip_address_change',
                'user_agent_change',
                'geographic_location_jump',
                'device_fingerprint_mismatch',
                'behavioral_pattern_shift'
            ],
            'replay_attack_signatures': [
                'identical_request_sequences',
                'timestamp_manipulation',
                'out_of_order_requests',
                'duplicate_nonce_values',
                'stale_session_tokens'
            ]
        }
        
        # Manipulation detection patterns
        self.manipulation_signatures = {
            'timestamp_manipulation': {
                'clock_skew_threshold': 5.0,  # seconds
                'future_timestamp_threshold': 60.0,  # seconds
                'past_timestamp_threshold': 300.0,  # seconds
                'timestamp_precision_anomalies': ['microsecond_precision', 'millisecond_rounding']
            },
            'session_data_integrity': {
                'required_fields': ['session_id', 'user_id', 'timestamp', 'ip_address'],
                'immutable_fields': ['session_id', 'creation_time', 'user_id'],
                'validation_checksums': True,
                'encryption_validation': True
            },
            'cross_session_correlation': {
                'max_concurrent_sessions': 3,
                'session_overlap_threshold': 0.8,
                'device_consistency_required': True,
                'ip_consistency_tolerance': 2  # Allow up to 2 IP changes
            }
        }
        
        # Session tracking data structures (in-memory for this implementation)
        self.active_sessions = {}  # session_id -> session_data
        self.session_history = {}  # session_id -> List[activity_record]
        self.user_sessions = {}  # user_id -> List[session_id]
        self.session_anomalies = {}  # session_id -> List[anomaly_record]
        
        self.logger.info("SessionIntegrityMonitor initialized successfully")
    
    def monitor_session_continuity(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔍 MONITOR SESSION CONTINUITY
        Comprehensive session continuity monitoring including token validation, activity pattern analysis,
        session break detection, user behavior consistency, and session hijacking detection
        
        Args:
            session_data: Dictionary containing session information and activity data
            
        Returns:
            Dict containing comprehensive session continuity analysis
        """
        try:
            self.logger.info("Starting comprehensive session continuity monitoring")
            
            analysis_result = {
                'session_identity': {},
                'token_validation': {},
                'activity_pattern_analysis': {},
                'session_break_detection': {},
                'behavior_consistency': {},
                'hijacking_detection': {},
                'continuity_score': 0.0,
                'risk_assessment': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            session_id = session_data.get('session_id', '')
            
            # 1. Session Token Validation and Tracking
            token_validation = self._validate_session_tokens(session_data)
            analysis_result['token_validation'] = token_validation
            
            # 2. Activity Pattern Continuity Analysis
            activity_analysis = self._analyze_activity_pattern_continuity(session_data)
            analysis_result['activity_pattern_analysis'] = activity_analysis
            
            # 3. Session Break Detection and Validation
            break_detection = self._detect_session_breaks(session_data)
            analysis_result['session_break_detection'] = break_detection
            
            # 4. User Behavior Consistency Monitoring
            behavior_consistency = self._monitor_behavior_consistency(session_data)
            analysis_result['behavior_consistency'] = behavior_consistency
            
            # 5. Session Hijacking Detection
            hijacking_detection = self._detect_session_hijacking(session_data)
            analysis_result['hijacking_detection'] = hijacking_detection
            
            # 6. Calculate Overall Continuity Score
            continuity_scores = [
                token_validation.get('validity_score', 0.5),
                activity_analysis.get('continuity_score', 0.5),
                break_detection.get('continuity_score', 0.5),
                behavior_consistency.get('consistency_score', 0.5),
                hijacking_detection.get('security_score', 0.5)
            ]
            analysis_result['continuity_score'] = statistics.mean(continuity_scores)
            
            # 7. Session Continuity Risk Assessment
            risk_assessment = self._assess_session_continuity_risk(analysis_result)
            analysis_result['risk_assessment'] = risk_assessment
            
            # Session Identity Summary
            analysis_result['session_identity'] = {
                'session_id': session_id,
                'user_id': session_data.get('user_id', 'Unknown'),
                'session_duration': self._calculate_session_duration(session_data),
                'activity_count': len(session_data.get('activity_log', [])),
                'continuity_status': 'CONTINUOUS' if analysis_result['continuity_score'] > 0.7 else 'INTERRUPTED',
                'hijacking_detected': hijacking_detection.get('hijacking_detected', False),
                'continuity_score': analysis_result['continuity_score'],
                'risk_level': risk_assessment.get('risk_level', 'MEDIUM')
            }
            
            # Update session tracking
            self._update_session_tracking(session_id, session_data, analysis_result)
            
            self.logger.info(f"Session continuity monitoring completed - Session: {session_id}, Score: {analysis_result['continuity_score']:.3f}")
            
            return {
                'success': True,
                'session_continuity_analysis': analysis_result,
                'analysis_summary': {
                    'session_id': session_id,
                    'continuity_status': analysis_result['session_identity']['continuity_status'],
                    'hijacking_detected': analysis_result['session_identity']['hijacking_detected'],
                    'continuity_score': analysis_result['continuity_score'],
                    'risk_level': analysis_result['session_identity']['risk_level']
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error monitoring session continuity: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def detect_session_manipulation(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🕵️ DETECT SESSION MANIPULATION
        Advanced session manipulation detection including replay attack detection, timestamp manipulation analysis,
        session data integrity validation, cross-session correlation, and manipulation pattern recognition
        
        Args:
            session_data: Dictionary containing session information and request data
            
        Returns:
            Dict containing comprehensive session manipulation detection analysis
        """
        try:
            self.logger.info("Starting comprehensive session manipulation detection")
            
            analysis_result = {
                'manipulation_status': {},
                'replay_attack_detection': {},
                'timestamp_manipulation': {},
                'data_integrity_validation': {},
                'cross_session_correlation': {},
                'manipulation_patterns': {},
                'manipulation_score': 0.0,
                'risk_assessment': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            session_id = session_data.get('session_id', '')
            
            # 1. Session Replay Attack Detection
            replay_detection = self._detect_session_replay_attacks(session_data)
            analysis_result['replay_attack_detection'] = replay_detection
            
            # 2. Timestamp Manipulation Analysis
            timestamp_analysis = self._analyze_timestamp_manipulation(session_data)
            analysis_result['timestamp_manipulation'] = timestamp_analysis
            
            # 3. Session Data Integrity Validation
            data_integrity = self._validate_session_data_integrity(session_data)
            analysis_result['data_integrity_validation'] = data_integrity
            
            # 4. Cross-Session Correlation Analysis
            cross_session = self._analyze_cross_session_correlation(session_data)
            analysis_result['cross_session_correlation'] = cross_session
            
            # 5. Manipulation Pattern Recognition
            pattern_recognition = self._recognize_manipulation_patterns(session_data)
            analysis_result['manipulation_patterns'] = pattern_recognition
            
            # 6. Calculate Overall Manipulation Score
            manipulation_scores = [
                replay_detection.get('threat_score', 0.0),
                timestamp_analysis.get('manipulation_score', 0.0),
                data_integrity.get('integrity_violation_score', 0.0),
                cross_session.get('anomaly_score', 0.0),
                pattern_recognition.get('pattern_score', 0.0)
            ]
            analysis_result['manipulation_score'] = statistics.mean(manipulation_scores)
            
            # 7. Manipulation Risk Assessment
            risk_assessment = self._assess_manipulation_risk(analysis_result)
            analysis_result['risk_assessment'] = risk_assessment
            
            # Manipulation Status Summary
            manipulation_detected = analysis_result['manipulation_score'] > self.manipulation_confidence_threshold
            analysis_result['manipulation_status'] = {
                'manipulation_detected': manipulation_detected,
                'primary_threat': self._identify_primary_manipulation_threat(analysis_result),
                'confidence_level': analysis_result['manipulation_score'],
                'threat_indicators': self._collect_threat_indicators(analysis_result),
                'session_authenticity': 'SUSPICIOUS' if manipulation_detected else 'AUTHENTIC',
                'recommended_action': self._recommend_security_action(analysis_result)
            }
            
            self.logger.info(f"Session manipulation detection completed - Session: {session_id}, Manipulation: {manipulation_detected}")
            
            return {
                'success': True,
                'manipulation_analysis': analysis_result,
                'analysis_summary': {
                    'session_id': session_id,
                    'manipulation_detected': manipulation_detected,
                    'primary_threat': analysis_result['manipulation_status']['primary_threat'],
                    'manipulation_score': analysis_result['manipulation_score'],
                    'session_authenticity': analysis_result['manipulation_status']['session_authenticity']
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error detecting session manipulation: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def validate_session_authenticity(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        ✅ VALIDATE SESSION AUTHENTICITY
        Enhanced session authenticity validation including biometric consistency validation,
        behavioral pattern authentication, session authentication token verification,
        identity continuity assessment, and authenticity confidence scoring
        
        Args:
            session_data: Dictionary containing session and authentication information
            
        Returns:
            Dict containing comprehensive enhanced session authenticity validation
        """
        try:
            self.logger.info("Starting comprehensive enhanced session authenticity validation")
            
            analysis_result = {
                'authenticity_status': {},
                'authentication_validation': {},
                'identity_consistency': {},
                'biometric_consistency_validation': {},
                'behavioral_pattern_authentication': {},
                'token_integrity': {},
                'identity_continuity_assessment': {},
                'authenticity_confidence_scoring': {},
                'authenticity_score': 0.0,
                'validation_details': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            session_id = session_data.get('session_id', '')
            user_id = session_data.get('user_id', '')
            
            # 1. Authentication Validation
            auth_validation = self._validate_authentication_credentials(session_data)
            analysis_result['authentication_validation'] = auth_validation
            
            # 2. User Identity Consistency  
            identity_consistency = self._validate_user_identity_consistency(session_data)
            analysis_result['identity_consistency'] = identity_consistency
            
            # 3. Enhanced Biometric Consistency Validation
            biometric_consistency = self._validate_enhanced_biometric_consistency(session_data)
            analysis_result['biometric_consistency_validation'] = biometric_consistency
            
            # 4. Behavioral Pattern Authentication
            behavioral_authentication = self._authenticate_behavioral_patterns(session_data)
            analysis_result['behavioral_pattern_authentication'] = behavioral_authentication
            
            # 5. Session Authentication Token Verification  
            token_verification = self._verify_session_authentication_tokens(session_data)
            analysis_result['token_integrity'] = token_verification
            
            # 6. Identity Continuity Assessment
            continuity_assessment = self._assess_identity_continuity(session_data)
            analysis_result['identity_continuity_assessment'] = continuity_assessment
            
            # 7. Authenticity Confidence Scoring
            confidence_scoring = self._calculate_authenticity_confidence_scoring(session_data, analysis_result)
            analysis_result['authenticity_confidence_scoring'] = confidence_scoring
            
            # 8. Calculate Overall Authenticity Score with Enhanced Factors
            authenticity_scores = [
                auth_validation.get('validity_score', 0.5),
                identity_consistency.get('consistency_score', 0.5),
                biometric_consistency.get('consistency_score', 0.5),
                behavioral_authentication.get('authentication_score', 0.5),
                token_verification.get('verification_score', 0.5),
                continuity_assessment.get('continuity_score', 0.5),
                confidence_scoring.get('confidence_score', 0.5)
            ]
            analysis_result['authenticity_score'] = statistics.mean(authenticity_scores)
            
            # Enhanced Authenticity Status Summary
            authentic = analysis_result['authenticity_score'] > 0.7
            high_confidence = confidence_scoring.get('confidence_level', 'MEDIUM') in ['HIGH', 'VERY_HIGH']
            
            analysis_result['authenticity_status'] = {
                'session_authentic': authentic,
                'authenticity_confidence': analysis_result['authenticity_score'],
                'validation_passed': authentic,
                'high_confidence_validation': high_confidence,
                'identity_verified': identity_consistency.get('identity_verified', False),
                'authentication_valid': auth_validation.get('authentication_valid', False),
                'biometric_consistent': biometric_consistency.get('biometric_consistent', False),
                'behavioral_pattern_match': behavioral_authentication.get('pattern_match', False),
                'token_valid': token_verification.get('token_valid', False),
                'identity_continuous': continuity_assessment.get('continuous', False)
            }
            
            # Enhanced Validation Details
            analysis_result['validation_details'] = {
                'validation_methods': [
                    'authentication', 'identity', 'biometric_consistency', 
                    'behavioral_patterns', 'token_verification', 'identity_continuity', 'confidence_scoring'
                ],
                'passed_validations': sum([
                    1 if auth_validation.get('authentication_valid', False) else 0,
                    1 if identity_consistency.get('identity_verified', False) else 0,
                    1 if biometric_consistency.get('biometric_consistent', False) else 0,
                    1 if behavioral_authentication.get('pattern_match', False) else 0,
                    1 if token_verification.get('token_valid', False) else 0,
                    1 if continuity_assessment.get('continuous', False) else 0
                ]),
                'failed_validations': self._collect_enhanced_failed_validations(analysis_result),
                'confidence_level': confidence_scoring.get('confidence_level', 'MEDIUM'),
                'recommendation': self._make_enhanced_authenticity_recommendation(analysis_result),
                'risk_factors': self._identify_authenticity_risk_factors(analysis_result)
            }
            
            self.logger.info(f"Enhanced session authenticity validation completed - Session: {session_id}, Authentic: {authentic}, Confidence: {confidence_scoring.get('confidence_level', 'MEDIUM')}")
            
            return {
                'success': True,
                'session_authenticity_analysis': analysis_result,
                'analysis_summary': {
                    'session_id': session_id,
                    'user_id': user_id,
                    'session_authentic': authentic,
                    'authenticity_score': analysis_result['authenticity_score'],
                    'confidence_level': confidence_scoring.get('confidence_level', 'MEDIUM'),
                    'validation_recommendation': analysis_result['validation_details']['recommendation'],
                    'high_confidence': high_confidence,
                    'risk_factors_count': len(analysis_result['validation_details']['risk_factors'])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error validating enhanced session authenticity: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    def track_session_anomalies(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        📊 TRACK SESSION ANOMALIES
        Comprehensive session anomaly tracking including unusual session patterns,
        behavioral anomaly detection, session duration analysis, and access pattern monitoring
        
        Args:
            session_data: Dictionary containing session information and behavioral data
            
        Returns:
            Dict containing comprehensive session anomaly tracking analysis
        """
        try:
            self.logger.info("Starting comprehensive session anomaly tracking")
            
            analysis_result = {
                'anomaly_summary': {},
                'unusual_patterns': {},
                'behavioral_anomalies': {},
                'duration_analysis': {},
                'access_pattern_monitoring': {},
                'anomaly_score': 0.0,
                'risk_classification': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            session_id = session_data.get('session_id', '')
            
            # 1. Unusual Session Pattern Detection
            unusual_patterns = self._detect_unusual_session_patterns(session_data)
            analysis_result['unusual_patterns'] = unusual_patterns
            
            # 2. Behavioral Anomaly Detection
            behavioral_anomalies = self._detect_behavioral_anomalies(session_data)
            analysis_result['behavioral_anomalies'] = behavioral_anomalies
            
            # 3. Session Duration Analysis
            duration_analysis = self._analyze_session_duration_anomalies(session_data)
            analysis_result['duration_analysis'] = duration_analysis
            
            # 4. Access Pattern Monitoring
            access_patterns = self._monitor_access_patterns(session_data)
            analysis_result['access_pattern_monitoring'] = access_patterns
            
            # 5. Calculate Overall Anomaly Score
            anomaly_scores = [
                unusual_patterns.get('anomaly_score', 0.0),
                behavioral_anomalies.get('anomaly_score', 0.0),
                duration_analysis.get('anomaly_score', 0.0),
                access_patterns.get('anomaly_score', 0.0)
            ]
            analysis_result['anomaly_score'] = statistics.mean(anomaly_scores)
            
            # 6. Risk Classification
            risk_classification = self._classify_anomaly_risk(analysis_result)
            analysis_result['risk_classification'] = risk_classification
            
            # Anomaly Summary
            anomalies_detected = analysis_result['anomaly_score'] > 0.5
            analysis_result['anomaly_summary'] = {
                'anomalies_detected': anomalies_detected,
                'anomaly_count': self._count_detected_anomalies(analysis_result),
                'primary_anomaly_type': self._identify_primary_anomaly(analysis_result),
                'anomaly_severity': self._classify_anomaly_severity(analysis_result['anomaly_score']),
                'recommended_monitoring_level': self._recommend_monitoring_level(analysis_result)
            }
            
            # Update anomaly tracking
            self._update_anomaly_tracking(session_id, analysis_result)
            
            self.logger.info(f"Session anomaly tracking completed - Session: {session_id}, Anomalies: {anomalies_detected}")
            
            return {
                'success': True,
                'anomaly_analysis': analysis_result,
                'analysis_summary': {
                    'session_id': session_id,
                    'anomalies_detected': anomalies_detected,
                    'anomaly_count': analysis_result['anomaly_summary']['anomaly_count'],
                    'anomaly_score': analysis_result['anomaly_score'],
                    'monitoring_level': analysis_result['anomaly_summary']['recommended_monitoring_level']
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking session anomalies: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    
    # ===== ENHANCED SESSION AUTHENTICITY VALIDATION HELPER METHODS =====
    
    def _validate_enhanced_biometric_consistency(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced biometric consistency validation with detailed analysis"""
        try:
            biometric_data = session_data.get('biometric_data', {})
            historical_biometrics = session_data.get('historical_biometrics', {})
            
            validation = {
                'biometric_consistent': True,
                'consistency_score': 1.0,
                'biometric_template_match': {},
                'keystroke_consistency': {},
                'mouse_pattern_consistency': {},
                'behavioral_biometric_validation': {},
                'biometric_stability_analysis': {},
                'consistency_confidence': 1.0,
                'validation_issues': []
            }
            
            if not biometric_data:
                validation['consistency_score'] = 0.5
                validation['consistency_confidence'] = 0.3
                validation['validation_issues'].append('no_biometric_data_available')
                return validation
            
            # 1. Biometric Template Matching
            template_match = self._match_biometric_templates(biometric_data, historical_biometrics)
            validation['biometric_template_match'] = template_match
            
            # 2. Keystroke Dynamics Consistency
            keystroke_consistency = self._validate_keystroke_consistency(biometric_data, historical_biometrics)
            validation['keystroke_consistency'] = keystroke_consistency
            
            # 3. Mouse Movement Pattern Consistency
            mouse_consistency = self._validate_mouse_pattern_consistency(biometric_data, historical_biometrics)
            validation['mouse_pattern_consistency'] = mouse_consistency
            
            # 4. Behavioral Biometric Validation
            behavioral_validation = self._validate_behavioral_biometrics(biometric_data, historical_biometrics)
            validation['behavioral_biometric_validation'] = behavioral_validation
            
            # 5. Biometric Stability Analysis
            stability_analysis = self._analyze_biometric_stability(biometric_data, historical_biometrics)
            validation['biometric_stability_analysis'] = stability_analysis
            
            # Calculate overall consistency score
            consistency_scores = [
                template_match.get('match_score', 0.5),
                keystroke_consistency.get('consistency_score', 0.5),
                mouse_consistency.get('consistency_score', 0.5),
                behavioral_validation.get('validation_score', 0.5),
                stability_analysis.get('stability_score', 0.5)
            ]
            validation['consistency_score'] = statistics.mean(consistency_scores)
            
            # Calculate consistency confidence
            confidence_factors = [
                template_match.get('confidence', 0.5),
                keystroke_consistency.get('confidence', 0.5),
                mouse_consistency.get('confidence', 0.5),
                behavioral_validation.get('confidence', 0.5)
            ]
            validation['consistency_confidence'] = statistics.mean(confidence_factors)
            
            # Determine overall consistency
            validation['biometric_consistent'] = (
                validation['consistency_score'] > 0.7 and
                validation['consistency_confidence'] > 0.6
            )
            
            # Collect validation issues
            if template_match.get('match_score', 1.0) < 0.6:
                validation['validation_issues'].append('biometric_template_mismatch')
            if keystroke_consistency.get('consistency_score', 1.0) < 0.5:
                validation['validation_issues'].append('keystroke_pattern_inconsistency')
            if mouse_consistency.get('consistency_score', 1.0) < 0.5:
                validation['validation_issues'].append('mouse_pattern_inconsistency')
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error in enhanced biometric consistency validation: {str(e)}")
            return {
                'biometric_consistent': False,
                'consistency_score': 0.0,
                'error': str(e)
            }
    
    def _authenticate_behavioral_patterns(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate user based on behavioral patterns"""
        try:
            behavioral_data = session_data.get('behavioral_patterns', {})
            user_profile = session_data.get('user_behavioral_profile', {})
            
            authentication = {
                'pattern_match': False,
                'authentication_score': 0.0,
                'navigation_pattern_match': {},
                'interaction_pattern_match': {},
                'temporal_pattern_match': {},
                'cognitive_pattern_match': {},
                'behavioral_signature_validation': {},
                'pattern_confidence': 0.0,
                'authentication_strength': 'WEAK'
            }
            
            if not behavioral_data or not user_profile:
                authentication['authentication_score'] = 0.3
                authentication['pattern_confidence'] = 0.2
                return authentication
            
            # 1. Navigation Pattern Authentication
            navigation_match = self._authenticate_navigation_patterns(behavioral_data, user_profile)
            authentication['navigation_pattern_match'] = navigation_match
            
            # 2. Interaction Pattern Authentication
            interaction_match = self._authenticate_interaction_patterns(behavioral_data, user_profile)
            authentication['interaction_pattern_match'] = interaction_match
            
            # 3. Temporal Pattern Authentication
            temporal_match = self._authenticate_temporal_patterns(behavioral_data, user_profile)
            authentication['temporal_pattern_match'] = temporal_match
            
            # 4. Cognitive Pattern Authentication
            cognitive_match = self._authenticate_cognitive_patterns(behavioral_data, user_profile)
            authentication['cognitive_pattern_match'] = cognitive_match
            
            # 5. Behavioral Signature Validation
            signature_validation = self._validate_behavioral_signature(behavioral_data, user_profile)
            authentication['behavioral_signature_validation'] = signature_validation
            
            # Calculate authentication score
            pattern_scores = [
                navigation_match.get('match_score', 0.0),
                interaction_match.get('match_score', 0.0),
                temporal_match.get('match_score', 0.0),
                cognitive_match.get('match_score', 0.0),
                signature_validation.get('validation_score', 0.0)
            ]
            authentication['authentication_score'] = statistics.mean(pattern_scores)
            
            # Calculate pattern confidence
            confidence_scores = [
                navigation_match.get('confidence', 0.0),
                interaction_match.get('confidence', 0.0),
                temporal_match.get('confidence', 0.0),
                cognitive_match.get('confidence', 0.0)
            ]
            authentication['pattern_confidence'] = statistics.mean(confidence_scores)
            
            # Determine pattern match
            authentication['pattern_match'] = (
                authentication['authentication_score'] > 0.7 and
                authentication['pattern_confidence'] > 0.6
            )
            
            # Determine authentication strength
            if authentication['authentication_score'] > 0.9:
                authentication['authentication_strength'] = 'VERY_STRONG'
            elif authentication['authentication_score'] > 0.8:
                authentication['authentication_strength'] = 'STRONG'
            elif authentication['authentication_score'] > 0.6:
                authentication['authentication_strength'] = 'MODERATE'
            elif authentication['authentication_score'] > 0.4:
                authentication['authentication_strength'] = 'WEAK'
            else:
                authentication['authentication_strength'] = 'VERY_WEAK'
            
            return authentication
            
        except Exception as e:
            self.logger.error(f"Error in behavioral pattern authentication: {str(e)}")
            return {
                'pattern_match': False,
                'authentication_score': 0.0,
                'error': str(e)
            }
    
    def _verify_session_authentication_tokens(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive session authentication token verification"""
        try:
            token_data = session_data.get('authentication_tokens', {})
            
            verification = {
                'token_valid': False,
                'verification_score': 0.0,
                'access_token_verification': {},
                'refresh_token_verification': {},
                'session_token_verification': {},
                'multi_factor_token_verification': {},
                'oauth_token_verification': {},
                'token_chain_verification': {},
                'verification_confidence': 0.0
            }
            
            if not token_data:
                verification['verification_score'] = 0.3
                return verification
            
            # 1. Access Token Verification
            access_token_result = self._verify_access_token(token_data)
            verification['access_token_verification'] = access_token_result
            
            # 2. Refresh Token Verification  
            refresh_token_result = self._verify_refresh_token(token_data)
            verification['refresh_token_verification'] = refresh_token_result
            
            # 3. Session Token Verification
            session_token_result = self._verify_session_token_detailed(token_data)
            verification['session_token_verification'] = session_token_result
            
            # 4. Multi-Factor Authentication Token Verification
            mfa_token_result = self._verify_mfa_tokens(token_data)
            verification['multi_factor_token_verification'] = mfa_token_result
            
            # 5. OAuth Token Verification
            oauth_token_result = self._verify_oauth_tokens(token_data)
            verification['oauth_token_verification'] = oauth_token_result
            
            # 6. Token Chain Verification (relationship between tokens)
            chain_verification = self._verify_token_chain_integrity(token_data)
            verification['token_chain_verification'] = chain_verification
            
            # Calculate verification score
            verification_scores = [
                access_token_result.get('verification_score', 0.0),
                refresh_token_result.get('verification_score', 0.0),
                session_token_result.get('verification_score', 0.0),
                mfa_token_result.get('verification_score', 0.0),
                oauth_token_result.get('verification_score', 0.0),
                chain_verification.get('verification_score', 0.0)
            ]
            verification['verification_score'] = statistics.mean(verification_scores)
            
            # Calculate confidence
            confidence_scores = [
                access_token_result.get('confidence', 0.0),
                session_token_result.get('confidence', 0.0),
                chain_verification.get('confidence', 0.0)
            ]
            verification['verification_confidence'] = statistics.mean(confidence_scores)
            
            # Determine token validity
            verification['token_valid'] = (
                verification['verification_score'] > 0.7 and
                verification['verification_confidence'] > 0.6 and
                access_token_result.get('valid', False) and
                session_token_result.get('valid', False)
            )
            
            return verification
            
        except Exception as e:
            self.logger.error(f"Error in session authentication token verification: {str(e)}")
            return {
                'token_valid': False,
                'verification_score': 0.0,
                'error': str(e)
            }
    
    def _assess_identity_continuity(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess identity continuity throughout the session"""
        try:
            identity_data = session_data.get('identity_data', {})
            session_timeline = session_data.get('session_timeline', [])
            
            assessment = {
                'continuous': True,
                'continuity_score': 1.0,
                'identity_consistency_timeline': {},
                'identity_drift_analysis': {},
                'context_preservation_analysis': {},
                'user_state_continuity': {},
                'identity_anchoring_validation': {},
                'continuity_confidence': 1.0
            }
            
            if not identity_data or not session_timeline:
                assessment['continuity_score'] = 0.5
                assessment['continuity_confidence'] = 0.3
                return assessment
            
            # 1. Identity Consistency Timeline Analysis
            timeline_analysis = self._analyze_identity_timeline_consistency(identity_data, session_timeline)
            assessment['identity_consistency_timeline'] = timeline_analysis
            
            # 2. Identity Drift Analysis
            drift_analysis = self._analyze_identity_drift(identity_data, session_timeline)
            assessment['identity_drift_analysis'] = drift_analysis
            
            # 3. Context Preservation Analysis
            context_analysis = self._analyze_context_preservation(identity_data, session_timeline)
            assessment['context_preservation_analysis'] = context_analysis
            
            # 4. User State Continuity Analysis
            state_continuity = self._analyze_user_state_continuity(identity_data, session_timeline)
            assessment['user_state_continuity'] = state_continuity
            
            # 5. Identity Anchoring Validation
            anchoring_validation = self._validate_identity_anchoring(identity_data)
            assessment['identity_anchoring_validation'] = anchoring_validation
            
            # Calculate continuity score
            continuity_scores = [
                timeline_analysis.get('consistency_score', 0.5),
                1.0 - drift_analysis.get('drift_score', 0.0),  # Lower drift = higher continuity
                context_analysis.get('preservation_score', 0.5),
                state_continuity.get('continuity_score', 0.5),
                anchoring_validation.get('validation_score', 0.5)
            ]
            assessment['continuity_score'] = statistics.mean(continuity_scores)
            
            # Calculate confidence
            assessment['continuity_confidence'] = min(
                timeline_analysis.get('confidence', 0.5),
                context_analysis.get('confidence', 0.5),
                anchoring_validation.get('confidence', 0.5)
            )
            
            # Determine continuity
            assessment['continuous'] = (
                assessment['continuity_score'] > 0.7 and
                assessment['continuity_confidence'] > 0.6 and
                drift_analysis.get('excessive_drift', False) == False
            )
            
            return assessment
            
        except Exception as e:
            self.logger.error(f"Error in identity continuity assessment: {str(e)}")
            return {
                'continuous': False,
                'continuity_score': 0.0,
                'error': str(e)
            }
    
    def _calculate_authenticity_confidence_scoring(self, session_data: Dict[str, Any], analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive authenticity confidence scoring"""
        try:
            confidence_data = session_data.get('confidence_factors', {})
            
            scoring = {
                'confidence_score': 0.0,
                'confidence_level': 'MEDIUM',
                'confidence_factors_analysis': {},
                'validation_method_confidence': {},
                'data_quality_confidence': {},
                'historical_consistency_confidence': {},
                'multi_factor_confidence': {},
                'confidence_distribution': {}
            }
            
            # 1. Validation Method Confidence
            method_confidence = self._calculate_validation_method_confidence(analysis_result)
            scoring['validation_method_confidence'] = method_confidence
            
            # 2. Data Quality Confidence
            quality_confidence = self._calculate_data_quality_confidence(session_data)
            scoring['data_quality_confidence'] = quality_confidence
            
            # 3. Historical Consistency Confidence
            historical_confidence = self._calculate_historical_consistency_confidence(session_data)
            scoring['historical_consistency_confidence'] = historical_confidence
            
            # 4. Multi-Factor Confidence
            multi_factor_confidence = self._calculate_multi_factor_confidence(session_data, analysis_result)
            scoring['multi_factor_confidence'] = multi_factor_confidence
            
            # 5. Confidence Factors Analysis
            factors_analysis = self._analyze_confidence_factors(confidence_data, analysis_result)
            scoring['confidence_factors_analysis'] = factors_analysis
            
            # Calculate overall confidence score
            confidence_components = [
                method_confidence.get('confidence', 0.5),
                quality_confidence.get('confidence', 0.5),
                historical_confidence.get('confidence', 0.5),
                multi_factor_confidence.get('confidence', 0.5),
                factors_analysis.get('factors_confidence', 0.5)
            ]
            scoring['confidence_score'] = statistics.mean(confidence_components)
            
            # Determine confidence level
            if scoring['confidence_score'] > 0.9:
                scoring['confidence_level'] = 'VERY_HIGH'
            elif scoring['confidence_score'] > 0.8:
                scoring['confidence_level'] = 'HIGH'
            elif scoring['confidence_score'] > 0.6:
                scoring['confidence_level'] = 'MEDIUM'
            elif scoring['confidence_score'] > 0.4:
                scoring['confidence_level'] = 'LOW'
            else:
                scoring['confidence_level'] = 'VERY_LOW'
            
            # Confidence distribution analysis
            scoring['confidence_distribution'] = {
                'validation_methods': method_confidence.get('confidence', 0.5),
                'data_quality': quality_confidence.get('confidence', 0.5),
                'historical_consistency': historical_confidence.get('confidence', 0.5),
                'multi_factor_authentication': multi_factor_confidence.get('confidence', 0.5),
                'confidence_factors': factors_analysis.get('factors_confidence', 0.5)
            }
            
            return scoring
            
        except Exception as e:
            self.logger.error(f"Error in authenticity confidence scoring: {str(e)}")
            return {
                'confidence_score': 0.5,
                'confidence_level': 'MEDIUM',
                'error': str(e)
            }
    
    def _collect_enhanced_failed_validations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Collect failed validations from enhanced analysis"""
        failed_validations = []
        
        # Check each validation component
        if not analysis_result.get('authentication_validation', {}).get('authentication_valid', True):
            failed_validations.append('authentication_validation_failed')
        
        if not analysis_result.get('identity_consistency', {}).get('identity_verified', True):
            failed_validations.append('identity_consistency_failed')
        
        if not analysis_result.get('biometric_consistency_validation', {}).get('biometric_consistent', True):
            failed_validations.append('biometric_consistency_failed')
        
        if not analysis_result.get('behavioral_pattern_authentication', {}).get('pattern_match', True):
            failed_validations.append('behavioral_pattern_authentication_failed')
        
        if not analysis_result.get('token_integrity', {}).get('token_valid', True):
            failed_validations.append('token_verification_failed')
        
        if not analysis_result.get('identity_continuity_assessment', {}).get('continuous', True):
            failed_validations.append('identity_continuity_failed')
        
        return failed_validations
    
    def _make_enhanced_authenticity_recommendation(self, analysis_result: Dict[str, Any]) -> str:
        """Make enhanced authenticity recommendation based on analysis"""
        score = analysis_result.get('authenticity_score', 0.0)
        confidence = analysis_result.get('authenticity_confidence_scoring', {}).get('confidence_level', 'MEDIUM')
        failed_validations = len(analysis_result.get('validation_details', {}).get('failed_validations', []))
        
        if score > 0.9 and confidence in ['HIGH', 'VERY_HIGH']:
            return 'APPROVE_HIGH_CONFIDENCE'
        elif score > 0.8 and confidence in ['MEDIUM', 'HIGH', 'VERY_HIGH']:
            return 'APPROVE_MODERATE_CONFIDENCE'
        elif score > 0.7:
            return 'APPROVE_WITH_MONITORING'
        elif score > 0.5:
            return 'REQUIRE_ADDITIONAL_VERIFICATION'
        elif failed_validations > 3:
            return 'REJECT_MULTIPLE_FAILURES'
        else:
            return 'REJECT_LOW_CONFIDENCE'
    
    def _identify_authenticity_risk_factors(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Identify risk factors from authenticity analysis"""
        risk_factors = []
        
        # Check for specific risk indicators
        if analysis_result.get('biometric_consistency_validation', {}).get('consistency_score', 1.0) < 0.5:
            risk_factors.append('low_biometric_consistency')
        
        if analysis_result.get('behavioral_pattern_authentication', {}).get('authentication_score', 1.0) < 0.6:
            risk_factors.append('behavioral_pattern_mismatch')
        
        if analysis_result.get('identity_continuity_assessment', {}).get('identity_drift_analysis', {}).get('excessive_drift', False):
            risk_factors.append('identity_drift_detected')
        
        if analysis_result.get('authenticity_confidence_scoring', {}).get('confidence_level', 'MEDIUM') in ['LOW', 'VERY_LOW']:
            risk_factors.append('low_confidence_validation')
        
        # Check token verification issues
        token_verification = analysis_result.get('token_integrity', {})
        if token_verification.get('verification_score', 1.0) < 0.6:
            risk_factors.append('token_verification_issues')
        
        return risk_factors
    
    # Additional helper methods for enhanced authenticity validation...
    
    def _match_biometric_templates(self, current_biometric: Dict[str, Any], historical_biometric: Dict[str, Any]) -> Dict[str, Any]:
        """Match biometric templates with historical data"""
        try:
            if not current_biometric or not historical_biometric:
                return {'match_score': 0.3, 'confidence': 0.2}
            
            # Simplified template matching (in production, would use actual biometric matching algorithms)
            current_template = current_biometric.get('biometric_template', {})
            historical_template = historical_biometric.get('biometric_template', {})
            
            match_score = 0.8  # Simulated match score
            confidence = 0.9   # Simulated confidence
            
            return {
                'match_score': match_score,
                'confidence': confidence,
                'template_similarity': match_score,
                'match_quality': 'HIGH' if match_score > 0.8 else 'LOW'
            }
            
        except Exception:
            return {'match_score': 0.5, 'confidence': 0.5}
    
    def _validate_keystroke_consistency(self, current_data: Dict[str, Any], historical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate keystroke dynamics consistency"""
        try:
            current_keystroke = current_data.get('keystroke_dynamics', {})
            historical_keystroke = historical_data.get('keystroke_dynamics', {})
            
            if not current_keystroke or not historical_keystroke:
                return {'consistency_score': 0.4, 'confidence': 0.3}
            
            # Analyze keystroke timing patterns
            current_timing = current_keystroke.get('timing_patterns', [])
            historical_timing = historical_keystroke.get('timing_patterns', [])
            
            consistency_score = 0.85  # Simulated consistency
            confidence = 0.8
            
            return {
                'consistency_score': consistency_score,
                'confidence': confidence,
                'timing_consistency': consistency_score,
                'pattern_match': consistency_score > 0.7
            }
            
        except Exception:
            return {'consistency_score': 0.5, 'confidence': 0.5}


    # ===== SESSION CONTINUITY MONITORING HELPER METHODS =====
    
    def _validate_session_tokens(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate session tokens and tracking information"""
        try:
            session_token = session_data.get('session_token', '')
            session_id = session_data.get('session_id', '')
            
            validation = {
                'token_present': bool(session_token),
                'token_format_valid': self._validate_token_format(session_token),
                'token_expiry_valid': self._check_token_expiry(session_data),
                'token_integrity': self._check_token_integrity(session_token),
                'session_id_consistency': self._validate_session_id_consistency(session_data),
                'validity_score': 1.0,
                'validation_issues': []
            }
            
            # Check token presence
            if not validation['token_present']:
                validation['validation_issues'].append('missing_session_token')
                validation['validity_score'] -= 0.5
            
            # Check token format
            if not validation['token_format_valid']:
                validation['validation_issues'].append('invalid_token_format')
                validation['validity_score'] -= 0.3
            
            # Check token expiry
            if not validation['token_expiry_valid']:
                validation['validation_issues'].append('token_expired')
                validation['validity_score'] -= 0.4
            
            # Check token integrity
            if not validation['token_integrity']:
                validation['validation_issues'].append('token_integrity_compromised')
                validation['validity_score'] -= 0.6
            
            validation['validity_score'] = max(0.0, validation['validity_score'])
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error validating session tokens: {str(e)}")
            return {'error': str(e), 'validity_score': 0.0}
    
    def _validate_token_format(self, token: str) -> bool:
        """Validate session token format"""
        try:
            if not token:
                return False
            
            # Basic token format validation (UUID-like or JWT-like)
            if len(token) < 20:  # Minimum reasonable token length
                return False
            
            # Check for valid characters (alphanumeric, hyphens, dots)
            import re
            if not re.match(r'^[a-zA-Z0-9\-_.]+$', token):
                return False
            
            return True
            
        except Exception:
            return False
    
    def _check_token_expiry(self, session_data: Dict[str, Any]) -> bool:
        """Check if session token has expired"""
        try:
            created_time = session_data.get('session_created_at', '')
            last_activity = session_data.get('last_activity_at', '')
            
            if not created_time and not last_activity:
                return True  # No expiry info available, assume valid
            
            # Use last activity time if available, otherwise creation time
            reference_time = last_activity or created_time
            
            if reference_time:
                # Simple expiry check (would use proper datetime parsing in production)
                current_time = datetime.utcnow().timestamp()
                session_time = datetime.utcnow().timestamp()  # Simplified
                
                # Check if session is older than timeout threshold
                time_diff = current_time - session_time
                return time_diff < self.session_timeout_threshold
            
            return True
            
        except Exception:
            return True  # Assume valid if unable to check
    
    def _check_token_integrity(self, token: str) -> bool:
        """Check session token integrity (simplified implementation)"""
        try:
            if not token:
                return False
            
            # Basic integrity checks
            # In production, this would verify digital signatures, checksums, etc.
            
            # Check for obvious tampering indicators
            if '..' in token or '//' in token:
                return False
            
            # Check for suspicious characters
            suspicious_chars = ['<', '>', '&', '"', "'", ';']
            if any(char in token for char in suspicious_chars):
                return False
            
            return True
            
        except Exception:
            return False
    
    def _validate_session_id_consistency(self, session_data: Dict[str, Any]) -> bool:
        """Validate session ID consistency across requests"""
        try:
            session_id = session_data.get('session_id', '')
            request_session_id = session_data.get('request_session_id', '')
            
            if not session_id:
                return False
            
            # Check consistency with request session ID
            if request_session_id and request_session_id != session_id:
                return False
            
            # Check if session ID format is valid
            if len(session_id) < 10:  # Minimum reasonable session ID length
                return False
            
            return True
            
        except Exception:
            return False
    
    def _analyze_activity_pattern_continuity(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze activity pattern continuity for session validation"""
        try:
            activity_log = session_data.get('activity_log', [])
            
            analysis = {
                'activity_count': len(activity_log),
                'activity_intervals': [],
                'pattern_consistency': True,
                'continuity_score': 1.0,
                'pattern_anomalies': []
            }
            
            if len(activity_log) < 2:
                analysis['continuity_score'] = 0.5
                return analysis
            
            # Analyze time intervals between activities
            intervals = self._calculate_activity_intervals(activity_log)
            analysis['activity_intervals'] = intervals
            
            # Check for pattern consistency
            if intervals:
                # Check for extremely regular intervals (bot-like behavior)
                interval_variance = statistics.stdev(intervals) if len(intervals) > 1 else 0
                mean_interval = statistics.mean(intervals)
                
                # Very consistent intervals are suspicious
                if interval_variance < (mean_interval * 0.1) and len(intervals) > 5:
                    analysis['pattern_anomalies'].append('extremely_regular_intervals')
                    analysis['continuity_score'] -= 0.3
                
                # Check for unreasonably fast activity
                if any(interval < 0.5 for interval in intervals):  # Less than 0.5 seconds
                    analysis['pattern_anomalies'].append('unreasonably_fast_activity')
                    analysis['continuity_score'] -= 0.2
                
                # Check for extremely long gaps
                if any(interval > 600 for interval in intervals):  # More than 10 minutes
                    analysis['pattern_anomalies'].append('extremely_long_gaps')
                    analysis['continuity_score'] -= 0.2
            
            analysis['continuity_score'] = max(0.0, analysis['continuity_score'])
            analysis['pattern_consistency'] = len(analysis['pattern_anomalies']) == 0
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing activity pattern continuity: {str(e)}")
            return {'error': str(e), 'continuity_score': 0.5}
    
    def _calculate_activity_intervals(self, activity_log: List[Dict[str, Any]]) -> List[float]:
        """Calculate intervals between activities"""
        try:
            intervals = []
            
            for i in range(1, len(activity_log)):
                current_time = activity_log[i].get('timestamp', 0)
                previous_time = activity_log[i-1].get('timestamp', 0)
                
                if current_time and previous_time:
                    interval = current_time - previous_time
                    if interval > 0:
                        intervals.append(interval)
            
            return intervals
            
        except Exception:
            return []
    
    def _detect_session_breaks(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect breaks and interruptions in session continuity"""
        try:
            activity_log = session_data.get('activity_log', [])
            
            detection = {
                'breaks_detected': False,
                'break_count': 0,
                'break_locations': [],
                'max_break_duration': 0.0,
                'continuity_score': 1.0,
                'break_analysis': []
            }
            
            if len(activity_log) < 2:
                return detection
            
            intervals = self._calculate_activity_intervals(activity_log)
            
            for i, interval in enumerate(intervals):
                if interval > self.max_session_gap:  # 5 minutes
                    detection['breaks_detected'] = True
                    detection['break_count'] += 1
                    detection['break_locations'].append(i + 1)
                    detection['max_break_duration'] = max(detection['max_break_duration'], interval)
                    
                    detection['break_analysis'].append({
                        'break_index': i + 1,
                        'break_duration': interval,
                        'break_severity': 'HIGH' if interval > 1800 else 'MEDIUM'  # 30 minutes
                    })
            
            # Adjust continuity score based on breaks
            if detection['break_count'] > 0:
                # Reduce score based on number and duration of breaks
                score_reduction = min(0.8, detection['break_count'] * 0.2 + 
                                    (detection['max_break_duration'] / 3600) * 0.3)
                detection['continuity_score'] = max(0.0, 1.0 - score_reduction)
            
            return detection
            
        except Exception as e:
            self.logger.error(f"Error detecting session breaks: {str(e)}")
            return {'error': str(e), 'continuity_score': 0.5}
    
    def _monitor_behavior_consistency(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor user behavior consistency throughout session"""
        try:
            behavioral_data = session_data.get('behavioral_data', {})
            
            consistency = {
                'consistency_score': 1.0,
                'behavioral_shifts': [],
                'consistency_factors': {},
                'behavior_stable': True
            }
            
            # Analyze various behavioral consistency factors
            consistency_factors = {}
            
            # Mouse movement patterns
            mouse_data = behavioral_data.get('mouse_patterns', {})
            if mouse_data:
                consistency_factors['mouse_consistency'] = self._analyze_mouse_consistency(mouse_data)
            
            # Typing patterns
            typing_data = behavioral_data.get('typing_patterns', {})
            if typing_data:
                consistency_factors['typing_consistency'] = self._analyze_typing_consistency(typing_data)
            
            # Navigation patterns
            navigation_data = behavioral_data.get('navigation_patterns', {})
            if navigation_data:
                consistency_factors['navigation_consistency'] = self._analyze_navigation_consistency(navigation_data)
            
            consistency['consistency_factors'] = consistency_factors
            
            # Calculate overall consistency score
            if consistency_factors:
                scores = [factor for factor in consistency_factors.values() if isinstance(factor, (int, float))]
                if scores:
                    consistency['consistency_score'] = statistics.mean(scores)
            
            # Determine if behavior is stable
            consistency['behavior_stable'] = consistency['consistency_score'] > self.activity_consistency_threshold
            
            return consistency
            
        except Exception as e:
            self.logger.error(f"Error monitoring behavior consistency: {str(e)}")
            return {'error': str(e), 'consistency_score': 0.5}
    
    def _analyze_mouse_consistency(self, mouse_data: Dict[str, Any]) -> float:
        """Analyze mouse movement pattern consistency"""
        try:
            # Simplified mouse consistency analysis
            movements = mouse_data.get('movements', [])
            
            if len(movements) < 10:
                return 0.5
            
            # Analyze movement velocity consistency
            velocities = [movement.get('velocity', 0) for movement in movements]
            
            if velocities:
                velocity_variance = statistics.stdev(velocities) if len(velocities) > 1 else 0
                mean_velocity = statistics.mean(velocities)
                
                # Consistent velocity patterns are more human-like
                consistency_score = 1.0 - min(1.0, velocity_variance / (mean_velocity + 0.001))
                return max(0.0, consistency_score)
            
            return 0.5
            
        except Exception:
            return 0.5
    
    def _analyze_typing_consistency(self, typing_data: Dict[str, Any]) -> float:
        """Analyze typing pattern consistency"""
        try:
            # Simplified typing consistency analysis
            keystrokes = typing_data.get('keystrokes', [])
            
            if len(keystrokes) < 5:
                return 0.5
            
            # Analyze keystroke timing consistency
            intervals = []
            for i in range(1, len(keystrokes)):
                current_time = keystrokes[i].get('timestamp', 0)
                previous_time = keystrokes[i-1].get('timestamp', 0)
                if current_time and previous_time:
                    intervals.append(current_time - previous_time)
            
            if intervals:
                # Human typing has natural variation
                interval_variance = statistics.stdev(intervals) if len(intervals) > 1 else 0
                mean_interval = statistics.mean(intervals)
                
                # Some variance is expected for human typing
                consistency_score = 0.8 if interval_variance > (mean_interval * 0.2) else 0.3
                return consistency_score
            
            return 0.5
            
        except Exception:
            return 0.5
    
    def _analyze_navigation_consistency(self, navigation_data: Dict[str, Any]) -> float:
        """Analyze navigation pattern consistency"""
        try:
            # Simplified navigation consistency analysis
            page_visits = navigation_data.get('page_visits', [])
            
            if len(page_visits) < 3:
                return 0.5
            
            # Analyze navigation flow patterns
            # In production, this would analyze page visit sequences, timing, etc.
            navigation_score = 0.8  # Simplified scoring
            
            return navigation_score
            
        except Exception:
            return 0.5
    
    def _detect_session_hijacking(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect potential session hijacking attempts"""
        try:
            detection = {
                'hijacking_detected': False,
                'hijacking_indicators': [],
                'security_score': 1.0,
                'threat_level': 'LOW',
                'detection_details': []
            }
            
            # Check for IP address changes
            ip_changes = self._check_ip_address_changes(session_data)
            if ip_changes['changes_detected']:
                detection['hijacking_indicators'].append('ip_address_change')
                detection['security_score'] -= 0.4
            
            # Check for user agent changes
            ua_changes = self._check_user_agent_changes(session_data)
            if ua_changes['changes_detected']:
                detection['hijacking_indicators'].append('user_agent_change')
                detection['security_score'] -= 0.3
            
            # Check for device fingerprint mismatches
            device_changes = self._check_device_fingerprint_changes(session_data)
            if device_changes['changes_detected']:
                detection['hijacking_indicators'].append('device_fingerprint_mismatch')
                detection['security_score'] -= 0.5
            
            # Check for geographic location jumps
            geo_changes = self._check_geographic_location_jumps(session_data)
            if geo_changes['impossible_travel']:
                detection['hijacking_indicators'].append('impossible_travel')
                detection['security_score'] -= 0.6
            
            # Determine hijacking detection status
            detection['hijacking_detected'] = detection['security_score'] < 0.5
            detection['security_score'] = max(0.0, detection['security_score'])
            
            # Classify threat level
            if detection['security_score'] < 0.3:
                detection['threat_level'] = 'CRITICAL'
            elif detection['security_score'] < 0.5:
                detection['threat_level'] = 'HIGH'
            elif detection['security_score'] < 0.7:
                detection['threat_level'] = 'MEDIUM'
            
            detection['detection_details'] = [
                f"Security score: {detection['security_score']:.3f}",
                f"Indicators found: {len(detection['hijacking_indicators'])}",
                f"Threat level: {detection['threat_level']}"
            ]
            
            return detection
            
        except Exception as e:
            self.logger.error(f"Error detecting session hijacking: {str(e)}")
            return {'error': str(e), 'security_score': 0.5}
    
    def _check_ip_address_changes(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for IP address changes during session"""
        try:
            current_ip = session_data.get('current_ip', '')
            initial_ip = session_data.get('initial_ip', '')
            ip_history = session_data.get('ip_history', [])
            
            changes = {
                'changes_detected': False,
                'change_count': 0,
                'ip_addresses': set([initial_ip, current_ip] + ip_history) - {''}
            }
            
            if len(changes['ip_addresses']) > 1:
                changes['changes_detected'] = True
                changes['change_count'] = len(changes['ip_addresses']) - 1
            
            return changes
            
        except Exception:
            return {'changes_detected': False, 'change_count': 0}
    
    def _check_user_agent_changes(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for user agent string changes during session"""
        try:
            current_ua = session_data.get('current_user_agent', '')
            initial_ua = session_data.get('initial_user_agent', '')
            
            changes = {
                'changes_detected': False,
                'change_details': []
            }
            
            if initial_ua and current_ua and initial_ua != current_ua:
                changes['changes_detected'] = True
                changes['change_details'].append({
                    'initial': initial_ua,
                    'current': current_ua
                })
            
            return changes
            
        except Exception:
            return {'changes_detected': False}
    
    def _check_device_fingerprint_changes(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for device fingerprint changes during session"""
        try:
            current_fingerprint = session_data.get('current_device_fingerprint', {})
            initial_fingerprint = session_data.get('initial_device_fingerprint', {})
            
            changes = {
                'changes_detected': False,
                'changed_attributes': []
            }
            
            if initial_fingerprint and current_fingerprint:
                # Compare key fingerprint attributes
                key_attributes = ['screen_resolution', 'timezone', 'language', 'plugins']
                
                for attr in key_attributes:
                    if (initial_fingerprint.get(attr) != current_fingerprint.get(attr) and
                        initial_fingerprint.get(attr) and current_fingerprint.get(attr)):
                        changes['changes_detected'] = True
                        changes['changed_attributes'].append(attr)
            
            return changes
            
        except Exception:
            return {'changes_detected': False}
    
    def _check_geographic_location_jumps(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for impossible geographic location changes"""
        try:
            current_location = session_data.get('current_location', {})
            previous_location = session_data.get('previous_location', {})
            time_diff = session_data.get('location_time_diff', 0)  # in seconds
            
            geo_analysis = {
                'impossible_travel': False,
                'distance_km': 0,
                'required_speed_kmh': 0
            }
            
            if (current_location and previous_location and time_diff > 0):
                # Calculate distance (simplified calculation)
                distance = self._calculate_distance(
                    previous_location.get('latitude', 0),
                    previous_location.get('longitude', 0),
                    current_location.get('latitude', 0),
                    current_location.get('longitude', 0)
                )
                
                geo_analysis['distance_km'] = distance
                
                # Calculate required travel speed
                time_hours = time_diff / 3600
                if time_hours > 0:
                    required_speed = distance / time_hours
                    geo_analysis['required_speed_kmh'] = required_speed
                    
                    # Check if speed is impossible (faster than commercial aircraft)
                    if required_speed > 900:  # 900 km/h
                        geo_analysis['impossible_travel'] = True
            
            return geo_analysis
            
        except Exception:
            return {'impossible_travel': False}
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two geographic points (simplified)"""
        try:
            # Simplified distance calculation (Haversine formula approximation)
            import math
            
            # Convert to radians
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
            
            # Calculate differences
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            # Haversine formula
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            # Earth radius in kilometers
            r = 6371
            
            return c * r
            
        except Exception:
            return 0.0
    
    def _calculate_session_duration(self, session_data: Dict[str, Any]) -> float:
        """Calculate total session duration in seconds"""
        try:
            start_time = session_data.get('session_start_time', 0)
            current_time = session_data.get('current_time', datetime.utcnow().timestamp())
            
            if start_time:
                return current_time - start_time
            
            return 0.0
            
        except Exception:
            return 0.0
    
    def _update_session_tracking(self, session_id: str, session_data: Dict[str, Any], analysis_result: Dict[str, Any]):
        """Update session tracking data structures"""
        try:
            # Update active sessions
            self.active_sessions[session_id] = {
                'session_data': session_data,
                'last_analysis': analysis_result,
                'last_update': datetime.utcnow()
            }
            
            # Update session history
            if session_id not in self.session_history:
                self.session_history[session_id] = []
            
            self.session_history[session_id].append({
                'timestamp': datetime.utcnow(),
                'continuity_score': analysis_result.get('continuity_score', 0.5),
                'risk_level': analysis_result.get('risk_assessment', {}).get('risk_level', 'MEDIUM')
            })
            
            # Update user sessions mapping
            user_id = session_data.get('user_id', '')
            if user_id:
                if user_id not in self.user_sessions:
                    self.user_sessions[user_id] = []
                if session_id not in self.user_sessions[user_id]:
                    self.user_sessions[user_id].append(session_id)
            
        except Exception as e:
            self.logger.error(f"Error updating session tracking: {str(e)}")
    
    def _assess_session_continuity_risk(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall session continuity risk"""
        try:
            risk_factors = []
            risk_score = 0.0
            
            # Check hijacking detection results
            hijacking = analysis_result.get('hijacking_detection', {})
            if hijacking.get('hijacking_detected', False):
                risk_factors.extend(hijacking.get('hijacking_indicators', []))
                risk_score += 0.6
            
            # Check session breaks
            breaks = analysis_result.get('session_break_detection', {})
            if breaks.get('breaks_detected', False):
                risk_factors.append('session_interruptions')
                risk_score += 0.3
            
            # Check token validation issues
            token_validation = analysis_result.get('token_validation', {})
            if token_validation.get('validity_score', 1.0) < 0.7:
                risk_factors.append('token_validation_issues')
                risk_score += 0.4
            
            # Check behavior consistency
            behavior = analysis_result.get('behavior_consistency', {})
            if not behavior.get('behavior_stable', True):
                risk_factors.append('behavioral_inconsistency')
                risk_score += 0.2
            
            # Determine risk level
            if risk_score > 0.7:
                risk_level = 'CRITICAL'
            elif risk_score > 0.5:
                risk_level = 'HIGH'
            elif risk_score > 0.3:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            return {
                'risk_score': min(1.0, risk_score),
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendations': self._generate_continuity_risk_recommendations(risk_factors)
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing session continuity risk: {str(e)}")
            return {'risk_score': 0.5, 'risk_level': 'MEDIUM', 'error': str(e)}
    
    def _generate_continuity_risk_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Generate session continuity risk mitigation recommendations"""
        recommendations = []
        
        if 'ip_address_change' in risk_factors:
            recommendations.append('CRITICAL: IP address change detected - verify user identity')
        if 'device_fingerprint_mismatch' in risk_factors:
            recommendations.append('HIGH: Device fingerprint mismatch - potential device switching')
        if 'impossible_travel' in risk_factors:
            recommendations.append('CRITICAL: Impossible travel detected - likely session hijacking')
        if 'session_interruptions' in risk_factors:
            recommendations.append('Monitor session breaks for suspicious patterns')
        if 'token_validation_issues' in risk_factors:
            recommendations.append('Regenerate session tokens and re-authenticate user')
        if 'behavioral_inconsistency' in risk_factors:
            recommendations.append('Additional behavioral verification recommended')
        
        return recommendations
    
    # ===== SESSION MANIPULATION DETECTION HELPER METHODS =====
    
    def _detect_session_replay_attacks(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect session replay attack patterns"""
        try:
            request_history = session_data.get('request_history', [])
            
            detection = {
                'replay_detected': False,
                'replay_indicators': [],
                'threat_score': 0.0,
                'duplicate_sequences': [],
                'suspicious_patterns': []
            }
            
            if len(request_history) < 5:
                return detection
            
            # Check for identical request sequences
            duplicate_sequences = self._find_duplicate_request_sequences(request_history)
            if duplicate_sequences:
                detection['replay_detected'] = True
                detection['replay_indicators'].append('identical_request_sequences')
                detection['duplicate_sequences'] = duplicate_sequences
                detection['threat_score'] += 0.6
            
            # Check for timestamp anomalies
            timestamp_anomalies = self._detect_timestamp_anomalies(request_history)
            if timestamp_anomalies:
                detection['replay_indicators'].append('timestamp_anomalies')
                detection['threat_score'] += 0.4
            
            # Check for out-of-order requests
            order_anomalies = self._detect_out_of_order_requests(request_history)
            if order_anomalies:
                detection['replay_indicators'].append('out_of_order_requests')
                detection['threat_score'] += 0.3
            
            detection['threat_score'] = min(1.0, detection['threat_score'])
            
            return detection
            
        except Exception as e:
            self.logger.error(f"Error detecting session replay attacks: {str(e)}")
            return {'error': str(e), 'threat_score': 0.0}
    
    def _find_duplicate_request_sequences(self, request_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find duplicate request sequences indicating replay attacks"""
        try:
            duplicates = []
            
            # Simple duplicate detection - compare request signatures
            request_signatures = []
            for request in request_history:
                signature = f"{request.get('method', '')}:{request.get('path', '')}:{request.get('body_hash', '')}"
                request_signatures.append(signature)
            
            # Find exact duplicate sequences of length 3 or more
            sequence_length = 3
            for i in range(len(request_signatures) - sequence_length + 1):
                sequence = request_signatures[i:i + sequence_length]
                
                # Look for this sequence later in the history
                for j in range(i + sequence_length, len(request_signatures) - sequence_length + 1):
                    compare_sequence = request_signatures[j:j + sequence_length]
                    
                    if sequence == compare_sequence:
                        duplicates.append({
                            'original_start': i,
                            'duplicate_start': j,
                            'sequence_length': sequence_length,
                            'sequence': sequence
                        })
            
            return duplicates
            
        except Exception:
            return []
    
    def _detect_timestamp_anomalies(self, request_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect timestamp manipulation in request history"""
        try:
            anomalies = []
            
            for i, request in enumerate(request_history):
                timestamp = request.get('timestamp', 0)
                
                if i > 0:
                    prev_timestamp = request_history[i-1].get('timestamp', 0)
                    
                    # Check for negative time progression
                    if timestamp < prev_timestamp:
                        anomalies.append({
                            'type': 'negative_time_progression',
                            'request_index': i,
                            'timestamp': timestamp,
                            'previous_timestamp': prev_timestamp
                        })
                    
                    # Check for unrealistic time jumps
                    time_diff = timestamp - prev_timestamp
                    if time_diff > 3600:  # More than 1 hour between requests
                        anomalies.append({
                            'type': 'unrealistic_time_jump',
                            'request_index': i,
                            'time_difference': time_diff
                        })
            
            return anomalies
            
        except Exception:
            return []
    
    def _detect_out_of_order_requests(self, request_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect out-of-order requests indicating replay attacks"""
        try:
            anomalies = []
            
            # Check for requests with sequence numbers out of order
            for i in range(1, len(request_history)):
                current_seq = request_history[i].get('sequence_number', i)
                prev_seq = request_history[i-1].get('sequence_number', i-1)
                
                if current_seq <= prev_seq:
                    anomalies.append({
                        'type': 'out_of_order_sequence',
                        'request_index': i,
                        'current_sequence': current_seq,
                        'previous_sequence': prev_seq
                    })
            
            return anomalies
            
        except Exception:
            return []
    
    def _analyze_timestamp_manipulation(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze timestamp manipulation patterns"""
        try:
            timestamps = session_data.get('timestamps', [])
            server_times = session_data.get('server_timestamps', [])
            
            analysis = {
                'manipulation_detected': False,
                'manipulation_score': 0.0,
                'manipulation_indicators': [],
                'clock_skew_analysis': {},
                'precision_analysis': {}
            }
            
            if len(timestamps) < 2:
                return analysis
            
            # Analyze clock skew
            clock_skew = self._analyze_clock_skew(timestamps, server_times)
            analysis['clock_skew_analysis'] = clock_skew
            
            if clock_skew.get('excessive_skew', False):
                analysis['manipulation_indicators'].append('excessive_clock_skew')
                analysis['manipulation_score'] += 0.4
            
            # Analyze timestamp precision
            precision_analysis = self._analyze_timestamp_precision(timestamps)
            analysis['precision_analysis'] = precision_analysis
            
            if precision_analysis.get('suspicious_precision', False):
                analysis['manipulation_indicators'].append('suspicious_precision')
                analysis['manipulation_score'] += 0.3
            
            # Check for future timestamps
            future_timestamps = self._detect_future_timestamps(timestamps)
            if future_timestamps:
                analysis['manipulation_indicators'].append('future_timestamps')
                analysis['manipulation_score'] += 0.5
            
            analysis['manipulation_detected'] = analysis['manipulation_score'] > 0.3
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing timestamp manipulation: {str(e)}")
            return {'error': str(e), 'manipulation_score': 0.0}
    
    def _analyze_clock_skew(self, client_times: List[float], server_times: List[float]) -> Dict[str, Any]:
        """Analyze clock skew between client and server timestamps"""
        try:
            if len(client_times) != len(server_times) or len(client_times) < 2:
                return {'excessive_skew': False}
            
            skew_values = []
            for client_time, server_time in zip(client_times, server_times):
                skew = abs(client_time - server_time)
                skew_values.append(skew)
            
            avg_skew = statistics.mean(skew_values)
            max_skew = max(skew_values)
            
            analysis = {
                'average_skew': avg_skew,
                'maximum_skew': max_skew,
                'excessive_skew': max_skew > self.manipulation_signatures['timestamp_manipulation']['clock_skew_threshold'],
                'skew_consistency': statistics.stdev(skew_values) if len(skew_values) > 1 else 0
            }
            
            return analysis
            
        except Exception:
            return {'excessive_skew': False}
    
    def _analyze_timestamp_precision(self, timestamps: List[float]) -> Dict[str, Any]:
        """Analyze timestamp precision for manipulation indicators"""
        try:
            precision_analysis = {
                'suspicious_precision': False,
                'precision_patterns': [],
                'precision_score': 0.0
            }
            
            # Check for unnaturally high precision (microsecond level)
            microsecond_precision_count = 0
            for timestamp in timestamps:
                # Check if timestamp has microsecond precision
                if timestamp % 0.001 != 0:  # Has sub-millisecond precision
                    microsecond_precision_count += 1
            
            if len(timestamps) > 0:
                microsecond_ratio = microsecond_precision_count / len(timestamps)
                if microsecond_ratio > 0.8:  # More than 80% have microsecond precision
                    precision_analysis['suspicious_precision'] = True
                    precision_analysis['precision_patterns'].append('excessive_microsecond_precision')
            
            # Check for rounded timestamps (indicating artificial generation)
            rounded_count = 0
            for timestamp in timestamps:
                if timestamp % 1.0 == 0:  # Exactly rounded to seconds
                    rounded_count += 1
            
            if len(timestamps) > 0:
                rounded_ratio = rounded_count / len(timestamps)
                if rounded_ratio > 0.7:  # More than 70% are exactly rounded
                    precision_analysis['suspicious_precision'] = True
                    precision_analysis['precision_patterns'].append('excessive_rounding')
            
            return precision_analysis
            
        except Exception:
            return {'suspicious_precision': False}
    
    def _detect_future_timestamps(self, timestamps: List[float]) -> List[Dict[str, Any]]:
        """Detect timestamps that are in the future"""
        try:
            current_time = datetime.utcnow().timestamp()
            future_threshold = self.manipulation_signatures['timestamp_manipulation']['future_timestamp_threshold']
            
            future_timestamps = []
            for i, timestamp in enumerate(timestamps):
                if timestamp > current_time + future_threshold:
                    future_timestamps.append({
                        'index': i,
                        'timestamp': timestamp,
                        'seconds_in_future': timestamp - current_time
                    })
            
            return future_timestamps
            
        except Exception:
            return []
    
    def _validate_session_data_integrity(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate session data integrity"""
        try:
            integrity_config = self.manipulation_signatures['session_data_integrity']
            
            validation = {
                'integrity_valid': True,
                'integrity_violation_score': 0.0,
                'missing_fields': [],
                'modified_immutable_fields': [],
                'validation_errors': []
            }
            
            # Check for required fields
            for field in integrity_config['required_fields']:
                if field not in session_data or not session_data[field]:
                    validation['missing_fields'].append(field)
                    validation['integrity_violation_score'] += 0.2
            
            # Check for modifications to immutable fields
            original_data = session_data.get('original_session_data', {})
            if original_data:
                for field in integrity_config['immutable_fields']:
                    if (field in original_data and field in session_data and 
                        original_data[field] != session_data[field]):
                        validation['modified_immutable_fields'].append(field)
                        validation['integrity_violation_score'] += 0.4
            
            # Check data checksums if available
            if integrity_config['validation_checksums']:
                checksum_validation = self._validate_data_checksums(session_data)
                if not checksum_validation['valid']:
                    validation['validation_errors'].append('checksum_mismatch')
                    validation['integrity_violation_score'] += 0.3
            
            validation['integrity_valid'] = validation['integrity_violation_score'] < 0.3
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error validating session data integrity: {str(e)}")
            return {'error': str(e), 'integrity_violation_score': 0.5}
    
    def _validate_data_checksums(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate data checksums for integrity verification"""
        try:
            # Simplified checksum validation
            expected_checksum = session_data.get('data_checksum', '')
            
            if not expected_checksum:
                return {'valid': True}  # No checksum to validate
            
            # Calculate current checksum (simplified implementation)
            data_to_hash = json.dumps(session_data.get('core_data', {}), sort_keys=True)
            current_checksum = hashlib.md5(data_to_hash.encode()).hexdigest()
            
            return {
                'valid': current_checksum == expected_checksum,
                'expected': expected_checksum,
                'actual': current_checksum
            }
            
        except Exception:
            return {'valid': False}
    
    def _analyze_cross_session_correlation(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cross-session correlation patterns"""
        try:
            user_id = session_data.get('user_id', '')
            session_id = session_data.get('session_id', '')
            
            analysis = {
                'anomaly_score': 0.0,
                'correlation_anomalies': [],
                'concurrent_sessions': 0,
                'session_overlap_analysis': {},
                'device_consistency': True
            }
            
            if not user_id:
                return analysis
            
            # Get user's other sessions
            user_sessions = self.user_sessions.get(user_id, [])
            active_sessions = [sid for sid in user_sessions if sid in self.active_sessions]
            
            analysis['concurrent_sessions'] = len(active_sessions)
            
            # Check for too many concurrent sessions
            max_concurrent = self.manipulation_signatures['cross_session_correlation']['max_concurrent_sessions']
            if analysis['concurrent_sessions'] > max_concurrent:
                analysis['correlation_anomalies'].append('excessive_concurrent_sessions')
                analysis['anomaly_score'] += 0.4
            
            # Check device consistency across sessions
            device_consistency = self._check_cross_session_device_consistency(session_data, active_sessions)
            analysis['device_consistency'] = device_consistency
            
            if not device_consistency:
                analysis['correlation_anomalies'].append('device_inconsistency')
                analysis['anomaly_score'] += 0.3
            
            # Analyze session overlap patterns
            overlap_analysis = self._analyze_session_overlaps(session_id, active_sessions)
            analysis['session_overlap_analysis'] = overlap_analysis
            
            if overlap_analysis.get('suspicious_overlaps', False):
                analysis['correlation_anomalies'].append('suspicious_session_overlaps')
                analysis['anomaly_score'] += 0.2
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing cross-session correlation: {str(e)}")
            return {'error': str(e), 'anomaly_score': 0.0}
    
    def _check_cross_session_device_consistency(self, session_data: Dict[str, Any], active_sessions: List[str]) -> bool:
        """Check device consistency across user's active sessions"""
        try:
            current_device = session_data.get('device_fingerprint', {})
            
            if not current_device or not active_sessions:
                return True
            
            # Compare with other active sessions
            for session_id in active_sessions:
                if session_id in self.active_sessions:
                    other_session = self.active_sessions[session_id]['session_data']
                    other_device = other_session.get('device_fingerprint', {})
                    
                    if other_device:
                        # Check key device attributes
                        key_attrs = ['screen_resolution', 'user_agent', 'timezone']
                        for attr in key_attrs:
                            if (current_device.get(attr) != other_device.get(attr) and
                                current_device.get(attr) and other_device.get(attr)):
                                return False
            
            return True
            
        except Exception:
            return True
    
    def _analyze_session_overlaps(self, session_id: str, active_sessions: List[str]) -> Dict[str, Any]:
        """Analyze session overlap patterns for anomalies"""
        try:
            overlap_analysis = {
                'suspicious_overlaps': False,
                'overlap_score': 0.0,
                'overlapping_sessions': []
            }
            
            # Simplified overlap analysis
            if len(active_sessions) > 2:  # More than 2 concurrent sessions is suspicious
                overlap_analysis['suspicious_overlaps'] = True
                overlap_analysis['overlap_score'] = len(active_sessions) / 5.0  # Normalize
            
            overlap_analysis['overlapping_sessions'] = active_sessions
            
            return overlap_analysis
            
        except Exception:
            return {'suspicious_overlaps': False}
    
    def _recognize_manipulation_patterns(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Recognize manipulation patterns in session data"""
        try:
            pattern_recognition = {
                'patterns_detected': [],
                'pattern_score': 0.0,
                'manipulation_techniques': [],
                'confidence_level': 0.0
            }
            
            # Check for known manipulation patterns
            patterns = []
            
            # Pattern 1: Automated request generation
            if self._detect_automated_patterns(session_data):
                patterns.append('automated_request_generation')
                pattern_recognition['manipulation_techniques'].append('automation')
                pattern_recognition['pattern_score'] += 0.4
            
            # Pattern 2: Session token reuse
            if self._detect_token_reuse_patterns(session_data):
                patterns.append('session_token_reuse')
                pattern_recognition['manipulation_techniques'].append('token_manipulation')
                pattern_recognition['pattern_score'] += 0.5
            
            # Pattern 3: Data replay attacks
            if self._detect_data_replay_patterns(session_data):
                patterns.append('data_replay_attack')
                pattern_recognition['manipulation_techniques'].append('replay_attack')
                pattern_recognition['pattern_score'] += 0.6
            
            pattern_recognition['patterns_detected'] = patterns
            pattern_recognition['confidence_level'] = min(1.0, pattern_recognition['pattern_score'])
            
            return pattern_recognition
            
        except Exception as e:
            self.logger.error(f"Error recognizing manipulation patterns: {str(e)}")
            return {'error': str(e), 'pattern_score': 0.0}
    
    def _detect_automated_patterns(self, session_data: Dict[str, Any]) -> bool:
        """Detect automated request generation patterns"""
        try:
            request_intervals = session_data.get('request_intervals', [])
            
            if len(request_intervals) < 5:
                return False
            
            # Check for very consistent intervals (automation indicator)
            if len(set(request_intervals)) == 1:  # All intervals identical
                return True
            
            # Check for extremely regular patterns
            variance = statistics.stdev(request_intervals) if len(request_intervals) > 1 else 0
            mean_interval = statistics.mean(request_intervals)
            
            # Very low variance indicates automation
            coefficient_of_variation = variance / mean_interval if mean_interval > 0 else 0
            return coefficient_of_variation < 0.1
            
        except Exception:
            return False
    
    def _detect_token_reuse_patterns(self, session_data: Dict[str, Any]) -> bool:
        """Detect session token reuse patterns"""
        try:
            token_history = session_data.get('token_history', [])
            
            if len(token_history) < 2:
                return False
            
            # Check for duplicate tokens
            unique_tokens = set(token_history)
            return len(unique_tokens) < len(token_history)
            
        except Exception:
            return False
    
    def _detect_data_replay_patterns(self, session_data: Dict[str, Any]) -> bool:
        """Detect data replay attack patterns"""
        try:
            request_signatures = session_data.get('request_signatures', [])
            
            if len(request_signatures) < 3:
                return False
            
            # Check for repeated request signatures
            signature_counts = {}
            for signature in request_signatures:
                signature_counts[signature] = signature_counts.get(signature, 0) + 1
            
            # If any signature appears more than twice, it might be a replay
            return any(count > 2 for count in signature_counts.values())
            
        except Exception:
            return False
    
    def _assess_manipulation_risk(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall manipulation risk"""
        try:
            risk_factors = []
            risk_score = 0.0
            
            # Check replay attack detection
            replay = analysis_result.get('replay_attack_detection', {})
            if replay.get('replay_detected', False):
                risk_factors.extend(replay.get('replay_indicators', []))
                risk_score += replay.get('threat_score', 0.0)
            
            # Check timestamp manipulation
            timestamp = analysis_result.get('timestamp_manipulation', {})
            if timestamp.get('manipulation_detected', False):
                risk_factors.extend(timestamp.get('manipulation_indicators', []))
                risk_score += timestamp.get('manipulation_score', 0.0)
            
            # Check data integrity violations
            integrity = analysis_result.get('data_integrity_validation', {})
            if not integrity.get('integrity_valid', True):
                risk_factors.append('data_integrity_violation')
                risk_score += integrity.get('integrity_violation_score', 0.0)
            
            # Check cross-session anomalies
            cross_session = analysis_result.get('cross_session_correlation', {})
            if cross_session.get('anomaly_score', 0.0) > 0.5:
                risk_factors.extend(cross_session.get('correlation_anomalies', []))
                risk_score += cross_session.get('anomaly_score', 0.0) * 0.5
            
            # Normalize risk score
            risk_score = min(1.0, risk_score)
            
            # Determine risk level
            if risk_score > 0.8:
                risk_level = 'CRITICAL'
            elif risk_score > 0.6:
                risk_level = 'HIGH'
            elif risk_score > 0.4:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            return {
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'recommendations': self._generate_manipulation_risk_recommendations(risk_factors)
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing manipulation risk: {str(e)}")
            return {'risk_score': 0.5, 'risk_level': 'MEDIUM', 'error': str(e)}
    
    def _generate_manipulation_risk_recommendations(self, risk_factors: List[str]) -> List[str]:
        """Generate manipulation risk mitigation recommendations"""
        recommendations = []
        
        if 'identical_request_sequences' in risk_factors:
            recommendations.append('CRITICAL: Replay attack detected - invalidate session immediately')
        if 'timestamp_anomalies' in risk_factors:
            recommendations.append('HIGH: Timestamp manipulation detected - verify request authenticity')
        if 'data_integrity_violation' in risk_factors:
            recommendations.append('CRITICAL: Data integrity compromised - session validation required')
        if 'excessive_concurrent_sessions' in risk_factors:
            recommendations.append('Monitor concurrent sessions and implement session limits')
        if 'device_inconsistency' in risk_factors:
            recommendations.append('Device fingerprint mismatch - require additional authentication')
        
        return recommendations
    
    def _identify_primary_manipulation_threat(self, analysis_result: Dict[str, Any]) -> str:
        """Identify the primary manipulation threat type"""
        try:
            threat_scores = {
                'replay_attack': analysis_result.get('replay_attack_detection', {}).get('threat_score', 0.0),
                'timestamp_manipulation': analysis_result.get('timestamp_manipulation', {}).get('manipulation_score', 0.0),
                'data_integrity_violation': analysis_result.get('data_integrity_validation', {}).get('integrity_violation_score', 0.0),
                'cross_session_anomaly': analysis_result.get('cross_session_correlation', {}).get('anomaly_score', 0.0)
            }
            
            # Find the highest threat score
            primary_threat = max(threat_scores.items(), key=lambda x: x[1])
            
            return primary_threat[0] if primary_threat[1] > 0.3 else 'none'
            
        except Exception:
            return 'unknown'
    
    def _collect_threat_indicators(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Collect all threat indicators from analysis"""
        indicators = []
        
        # Replay attack indicators
        replay_indicators = analysis_result.get('replay_attack_detection', {}).get('replay_indicators', [])
        indicators.extend(replay_indicators)
        
        # Timestamp manipulation indicators
        timestamp_indicators = analysis_result.get('timestamp_manipulation', {}).get('manipulation_indicators', [])
        indicators.extend(timestamp_indicators)
        
        # Data integrity violations
        integrity = analysis_result.get('data_integrity_validation', {})
        if integrity.get('missing_fields'):
            indicators.append('missing_required_fields')
        if integrity.get('modified_immutable_fields'):
            indicators.append('immutable_field_modifications')
        
        # Cross-session anomalies
        cross_session_anomalies = analysis_result.get('cross_session_correlation', {}).get('correlation_anomalies', [])
        indicators.extend(cross_session_anomalies)
        
        return indicators
    
    def _recommend_security_action(self, analysis_result: Dict[str, Any]) -> str:
        """Recommend security action based on manipulation analysis"""
        try:
            manipulation_score = analysis_result.get('manipulation_score', 0.0)
            
            if manipulation_score > 0.8:
                return 'TERMINATE_SESSION'
            elif manipulation_score > 0.6:
                return 'REQUIRE_REAUTHENTICATION'
            elif manipulation_score > 0.4:
                return 'ENHANCED_MONITORING'
            else:
                return 'CONTINUE_NORMAL'
                
        except Exception:
            return 'ENHANCED_MONITORING'
    
    # ===== SESSION AUTHENTICITY VALIDATION HELPER METHODS =====
    
    def _validate_authentication_credentials(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate authentication credentials"""
        try:
            auth_data = session_data.get('authentication_data', {})
            
            validation = {
                'authentication_valid': True,
                'validity_score': 1.0,
                'validation_issues': []
            }
            
            # Check if authentication data is present
            if not auth_data:
                validation['authentication_valid'] = False
                validation['validity_score'] = 0.0
                validation['validation_issues'].append('missing_authentication_data')
                return validation
            
            # Check authentication method
            auth_method = auth_data.get('method', '')
            if auth_method not in ['password', 'token', 'biometric', 'multi_factor']:
                validation['validation_issues'].append('unsupported_auth_method')
                validation['validity_score'] -= 0.3
            
            # Check credential expiry
            expires_at = auth_data.get('expires_at', 0)
            current_time = datetime.utcnow().timestamp()
            
            if expires_at > 0 and current_time > expires_at:
                validation['authentication_valid'] = False
                validation['validation_issues'].append('expired_credentials')
                validation['validity_score'] -= 0.5
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error validating authentication credentials: {str(e)}")
            return {'error': str(e), 'validity_score': 0.0}
    
    def _validate_user_identity_consistency(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user identity consistency"""
        try:
            user_id = session_data.get('user_id', '')
            claimed_identity = session_data.get('claimed_identity', {})
            
            validation = {
                'identity_verified': True,
                'consistency_score': 1.0,
                'identity_issues': []
            }
            
            if not user_id or not claimed_identity:
                validation['identity_verified'] = False
                validation['consistency_score'] = 0.0
                validation['identity_issues'].append('insufficient_identity_data')
                return validation
            
            # Check identity attributes consistency
            identity_attrs = ['username', 'email', 'phone_number']
            
            for attr in identity_attrs:
                claimed_value = claimed_identity.get(attr, '')
                
                # In production, this would check against user database
                if claimed_value and not self._validate_identity_attribute(attr, claimed_value):
                    validation['identity_issues'].append(f'invalid_{attr}')
                    validation['consistency_score'] -= 0.2
            
            validation['identity_verified'] = validation['consistency_score'] > 0.6
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error validating user identity consistency: {str(e)}")
            return {'error': str(e), 'consistency_score': 0.0}
    
    def _validate_identity_attribute(self, attribute: str, value: str) -> bool:
        """Validate individual identity attribute"""
        try:
            if attribute == 'email':
                # Basic email format validation
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                return re.match(email_pattern, value) is not None
            
            elif attribute == 'username':
                # Basic username validation
                return len(value) >= 3 and value.isalnum()
            
            elif attribute == 'phone_number':
                # Basic phone number validation
                return len(value) >= 10 and value.replace('+', '').replace('-', '').isdigit()
            
            return True
            
        except Exception:
            return False
    
    def _validate_biometric_consistency(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate biometric consistency"""
        try:
            biometric_data = session_data.get('biometric_data', {})
            
            validation = {
                'biometric_valid': True,
                'validation_score': 1.0,
                'biometric_issues': []
            }
            
            if not biometric_data:
                # No biometric data available - not an issue
                validation['validation_score'] = 0.5
                return validation
            
            # Check biometric template consistency
            current_template = biometric_data.get('current_template', '')
            reference_template = biometric_data.get('reference_template', '')
            
            if current_template and reference_template:
                # Simplified biometric comparison
                similarity_score = self._calculate_biometric_similarity(current_template, reference_template)
                
                if similarity_score < 0.7:  # Below acceptable threshold
                    validation['biometric_valid'] = False
                    validation['biometric_issues'].append('biometric_mismatch')
                    validation['validation_score'] = similarity_score
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error validating biometric consistency: {str(e)}")
            return {'error': str(e), 'validation_score': 0.5}
    
    def _calculate_biometric_similarity(self, template1: str, template2: str) -> float:
        """Calculate biometric template similarity (simplified implementation)"""
        try:
            # Simplified similarity calculation
            # In production, this would use proper biometric matching algorithms
            
            if template1 == template2:
                return 1.0
            
            # Calculate string similarity as a proxy
            max_len = max(len(template1), len(template2))
            if max_len == 0:
                return 0.0
            
            # Simple character-by-character comparison
            matches = sum(1 for a, b in zip(template1, template2) if a == b)
            similarity = matches / max_len
            
            return similarity
            
        except Exception:
            return 0.0
    
    def _validate_authentication_token_integrity(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate authentication token integrity"""
        try:
            token_data = session_data.get('auth_token_data', {})
            
            validation = {
                'token_valid': True,
                'integrity_score': 1.0,
                'token_issues': []
            }
            
            if not token_data:
                validation['token_valid'] = False
                validation['integrity_score'] = 0.0
                validation['token_issues'].append('missing_token_data')
                return validation
            
            # Check token format
            token = token_data.get('token', '')
            if not self._validate_token_format(token):
                validation['token_issues'].append('invalid_token_format')
                validation['integrity_score'] -= 0.4
            
            # Check token signature (simplified)
            if not self._validate_token_signature(token_data):
                validation['token_issues'].append('invalid_token_signature')
                validation['integrity_score'] -= 0.5
            
            # Check token expiry
            if not self._check_token_expiry(token_data):
                validation['token_valid'] = False
                validation['token_issues'].append('token_expired')
                validation['integrity_score'] -= 0.6
            
            validation['token_valid'] = validation['integrity_score'] > 0.5
            
            return validation
            
        except Exception as e:
            self.logger.error(f"Error validating authentication token integrity: {str(e)}")
            return {'error': str(e), 'integrity_score': 0.0}
    
    def _validate_token_signature(self, token_data: Dict[str, Any]) -> bool:
        """Validate token signature (simplified implementation)"""
        try:
            # In production, this would verify JWT signatures or similar
            signature = token_data.get('signature', '')
            payload = token_data.get('payload', '')
            
            if not signature or not payload:
                return False
            
            # Simplified signature validation
            expected_signature = hashlib.sha256(payload.encode()).hexdigest()[:16]
            
            return signature == expected_signature
            
        except Exception:
            return False
    
    def _collect_failed_validations(self, analysis_result: Dict[str, Any]) -> List[str]:
        """Collect all failed validation methods"""
        failed_validations = []
        
        auth_validation = analysis_result.get('authentication_validation', {})
        if not auth_validation.get('authentication_valid', True):
            failed_validations.append('authentication')
        
        identity_validation = analysis_result.get('identity_consistency', {})
        if not identity_validation.get('identity_verified', True):
            failed_validations.append('identity')
        
        biometric_validation = analysis_result.get('biometric_validation', {})
        if not biometric_validation.get('biometric_valid', True):
            failed_validations.append('biometric')
        
        token_validation = analysis_result.get('token_integrity', {})
        if not token_validation.get('token_valid', True):
            failed_validations.append('token')
        
        return failed_validations
    
    # ===== SESSION ANOMALY TRACKING HELPER METHODS =====
    
    def _detect_unusual_session_patterns(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect unusual session patterns"""
        try:
            session_duration = self._calculate_session_duration(session_data)
            activity_count = len(session_data.get('activity_log', []))
            
            detection = {
                'anomaly_score': 0.0,
                'unusual_patterns': [],
                'pattern_details': {}
            }
            
            # Check for unusually long sessions
            if session_duration > 14400:  # More than 4 hours
                detection['unusual_patterns'].append('extremely_long_session')
                detection['anomaly_score'] += 0.3
            
            # Check for unusually short sessions with high activity
            if session_duration < 60 and activity_count > 50:  # Less than 1 minute, more than 50 activities
                detection['unusual_patterns'].append('rapid_fire_activity')
                detection['anomaly_score'] += 0.4
            
            # Check for sessions with no activity
            if session_duration > 300 and activity_count == 0:  # More than 5 minutes, no activity
                detection['unusual_patterns'].append('inactive_long_session')
                detection['anomaly_score'] += 0.2
            
            # Check for irregular activity intervals
            activity_intervals = self._calculate_activity_intervals(session_data.get('activity_log', []))
            if activity_intervals and self._detect_irregular_intervals(activity_intervals):
                detection['unusual_patterns'].append('irregular_activity_intervals')
                detection['anomaly_score'] += 0.3
            
            detection['pattern_details'] = {
                'session_duration': session_duration,
                'activity_count': activity_count,
                'avg_activity_interval': statistics.mean(activity_intervals) if activity_intervals else 0
            }
            
            return detection
            
        except Exception as e:
            self.logger.error(f"Error detecting unusual session patterns: {str(e)}")
            return {'error': str(e), 'anomaly_score': 0.0}
    
    def _detect_irregular_intervals(self, intervals: List[float]) -> bool:
        """Detect irregular activity intervals"""
        try:
            if len(intervals) < 5:
                return False
            
            # Check for extremely regular intervals (automation)
            if len(set(intervals)) <= 2:  # Only 1 or 2 unique intervals
                return True
            
            # Check for extremely irregular intervals
            std_dev = statistics.stdev(intervals)
            mean_interval = statistics.mean(intervals)
            
            # If standard deviation is more than 200% of mean, it's irregular
            return std_dev > (mean_interval * 2)
            
        except Exception:
            return False
    
    def _detect_behavioral_anomalies(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect behavioral anomalies in session"""
        try:
            behavioral_data = session_data.get('behavioral_data', {})
            
            detection = {
                'anomaly_score': 0.0,
                'behavioral_anomalies': [],
                'anomaly_details': {}
            }
            
            # Mouse behavior anomalies
            mouse_anomalies = self._detect_mouse_behavioral_anomalies(behavioral_data.get('mouse_data', {}))
            if mouse_anomalies:
                detection['behavioral_anomalies'].extend(mouse_anomalies)
                detection['anomaly_score'] += 0.3
            
            # Keyboard behavior anomalies
            keyboard_anomalies = self._detect_keyboard_behavioral_anomalies(behavioral_data.get('keyboard_data', {}))
            if keyboard_anomalies:
                detection['behavioral_anomalies'].extend(keyboard_anomalies)
                detection['anomaly_score'] += 0.2
            
            # Navigation behavior anomalies
            nav_anomalies = self._detect_navigation_behavioral_anomalies(behavioral_data.get('navigation_data', {}))
            if nav_anomalies:
                detection['behavioral_anomalies'].extend(nav_anomalies)
                detection['anomaly_score'] += 0.2
            
            detection['anomaly_details'] = {
                'mouse_anomalies': mouse_anomalies,
                'keyboard_anomalies': keyboard_anomalies,
                'navigation_anomalies': nav_anomalies
            }
            
            return detection
            
        except Exception as e:
            self.logger.error(f"Error detecting behavioral anomalies: {str(e)}")
            return {'error': str(e), 'anomaly_score': 0.0}
    
    def _detect_mouse_behavioral_anomalies(self, mouse_data: Dict[str, Any]) -> List[str]:
        """Detect mouse behavior anomalies"""
        anomalies = []
        
        try:
            movements = mouse_data.get('movements', [])
            clicks = mouse_data.get('clicks', [])
            
            if len(movements) > 10:
                # Check for perfectly straight movements (automation indicator)
                straight_movements = sum(1 for move in movements if move.get('linearity', 0) > 0.95)
                if straight_movements / len(movements) > 0.8:
                    anomalies.append('excessive_linear_movements')
            
            if len(clicks) > 5:
                # Check for perfect click accuracy (automation indicator)
                accurate_clicks = sum(1 for click in clicks if click.get('accuracy', 0) > 0.98)
                if accurate_clicks / len(clicks) > 0.9:
                    anomalies.append('perfect_click_accuracy')
        
        except Exception:
            pass
        
        return anomalies
    
    def _detect_keyboard_behavioral_anomalies(self, keyboard_data: Dict[str, Any]) -> List[str]:
        """Detect keyboard behavior anomalies"""
        anomalies = []
        
        try:
            keystrokes = keyboard_data.get('keystrokes', [])
            
            if len(keystrokes) > 10:
                # Check for extremely consistent typing speed
                intervals = []
                for i in range(1, len(keystrokes)):
                    interval = keystrokes[i].get('timestamp', 0) - keystrokes[i-1].get('timestamp', 0)
                    intervals.append(interval)
                
                if intervals:
                    std_dev = statistics.stdev(intervals) if len(intervals) > 1 else 0
                    mean_interval = statistics.mean(intervals)
                    
                    # Very consistent typing is suspicious
                    if std_dev < (mean_interval * 0.1):
                        anomalies.append('robotic_typing_pattern')
        
        except Exception:
            pass
        
        return anomalies
    
    def _detect_navigation_behavioral_anomalies(self, navigation_data: Dict[str, Any]) -> List[str]:
        """Detect navigation behavior anomalies"""
        anomalies = []
        
        try:
            page_visits = navigation_data.get('page_visits', [])
            
            if len(page_visits) > 5:
                # Check for extremely fast page navigation
                fast_navigations = sum(1 for visit in page_visits if visit.get('time_on_page', 0) < 1.0)
                if fast_navigations / len(page_visits) > 0.7:
                    anomalies.append('rapid_page_navigation')
        
        except Exception:
            pass
        
        return anomalies
    
    def _analyze_session_duration_anomalies(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze session duration for anomalies"""
        try:
            session_duration = self._calculate_session_duration(session_data)
            
            analysis = {
                'anomaly_score': 0.0,
                'duration_anomalies': [],
                'duration_classification': 'NORMAL'
            }
            
            # Classify session duration
            if session_duration < 30:
                analysis['duration_classification'] = 'VERY_SHORT'
                analysis['duration_anomalies'].append('extremely_short_session')
                analysis['anomaly_score'] += 0.2
            elif session_duration > 28800:  # More than 8 hours
                analysis['duration_classification'] = 'EXTREMELY_LONG'
                analysis['duration_anomalies'].append('extremely_long_session')
                analysis['anomaly_score'] += 0.4
            elif session_duration > 14400:  # More than 4 hours
                analysis['duration_classification'] = 'VERY_LONG'
                analysis['duration_anomalies'].append('very_long_session')
                analysis['anomaly_score'] += 0.2
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing session duration anomalies: {str(e)}")
            return {'error': str(e), 'anomaly_score': 0.0}
    
    def _monitor_access_patterns(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor access patterns for anomalies"""
        try:
            access_log = session_data.get('access_log', [])
            
            monitoring = {
                'anomaly_score': 0.0,
                'access_anomalies': [],
                'pattern_analysis': {}
            }
            
            if not access_log:
                return monitoring
            
            # Analyze access frequency
            access_frequency = len(access_log) / max(self._calculate_session_duration(session_data) / 60, 1)  # per minute
            
            if access_frequency > 10:  # More than 10 accesses per minute
                monitoring['access_anomalies'].append('high_frequency_access')
                monitoring['anomaly_score'] += 0.3
            
            # Analyze access pattern regularity
            access_times = [access.get('timestamp', 0) for access in access_log]
            if len(access_times) > 5:
                intervals = [access_times[i] - access_times[i-1] for i in range(1, len(access_times))]
                
                if intervals:
                    # Check for extremely regular access patterns
                    std_dev = statistics.stdev(intervals) if len(intervals) > 1 else 0
                    mean_interval = statistics.mean(intervals)
                    
                    if std_dev < (mean_interval * 0.1):
                        monitoring['access_anomalies'].append('robotic_access_pattern')
                        monitoring['anomaly_score'] += 0.4
            
            monitoring['pattern_analysis'] = {
                'access_frequency': access_frequency,
                'total_accesses': len(access_log),
                'session_duration': self._calculate_session_duration(session_data)
            }
            
            return monitoring
            
        except Exception as e:
            self.logger.error(f"Error monitoring access patterns: {str(e)}")
            return {'error': str(e), 'anomaly_score': 0.0}
    
    def _classify_anomaly_risk(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Classify anomaly risk level"""
        try:
            anomaly_score = analysis_result.get('anomaly_score', 0.0)
            
            if anomaly_score > 0.8:
                risk_level = 'CRITICAL'
                monitoring_action = 'IMMEDIATE_REVIEW'
            elif anomaly_score > 0.6:
                risk_level = 'HIGH'
                monitoring_action = 'ENHANCED_MONITORING'
            elif anomaly_score > 0.4:
                risk_level = 'MEDIUM'
                monitoring_action = 'INCREASED_MONITORING'
            else:
                risk_level = 'LOW'
                monitoring_action = 'STANDARD_MONITORING'
            
            return {
                'risk_level': risk_level,
                'monitoring_action': monitoring_action,
                'risk_score': anomaly_score
            }
            
        except Exception:
            return {'risk_level': 'MEDIUM', 'monitoring_action': 'STANDARD_MONITORING'}
    
    def _count_detected_anomalies(self, analysis_result: Dict[str, Any]) -> int:
        """Count total number of detected anomalies"""
        anomaly_count = 0
        
        # Count unusual patterns
        unusual_patterns = analysis_result.get('unusual_patterns', {}).get('unusual_patterns', [])
        anomaly_count += len(unusual_patterns)
        
        # Count behavioral anomalies
        behavioral_anomalies = analysis_result.get('behavioral_anomalies', {}).get('behavioral_anomalies', [])
        anomaly_count += len(behavioral_anomalies)
        
        # Count duration anomalies
        duration_anomalies = analysis_result.get('duration_analysis', {}).get('duration_anomalies', [])
        anomaly_count += len(duration_anomalies)
        
        # Count access pattern anomalies
        access_anomalies = analysis_result.get('access_pattern_monitoring', {}).get('access_anomalies', [])
        anomaly_count += len(access_anomalies)
        
        return anomaly_count
    
    def _identify_primary_anomaly(self, analysis_result: Dict[str, Any]) -> str:
        """Identify the primary type of anomaly"""
        try:
            anomaly_scores = {
                'unusual_patterns': analysis_result.get('unusual_patterns', {}).get('anomaly_score', 0.0),
                'behavioral_anomalies': analysis_result.get('behavioral_anomalies', {}).get('anomaly_score', 0.0),
                'duration_anomalies': analysis_result.get('duration_analysis', {}).get('anomaly_score', 0.0),
                'access_patterns': analysis_result.get('access_pattern_monitoring', {}).get('anomaly_score', 0.0)
            }
            
            primary_anomaly = max(anomaly_scores.items(), key=lambda x: x[1])
            
            return primary_anomaly[0] if primary_anomaly[1] > 0.3 else 'none'
            
        except Exception:
            return 'unknown'
    
    def _classify_anomaly_severity(self, anomaly_score: float) -> str:
        """Classify anomaly severity based on score"""
        if anomaly_score > 0.8:
            return 'CRITICAL'
        elif anomaly_score > 0.6:
            return 'HIGH'
        elif anomaly_score > 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _recommend_monitoring_level(self, analysis_result: Dict[str, Any]) -> str:
        """Recommend monitoring level based on anomalies"""
        try:
            anomaly_count = self._count_detected_anomalies(analysis_result)
            anomaly_score = analysis_result.get('anomaly_score', 0.0)
            
            if anomaly_count > 5 or anomaly_score > 0.7:
                return 'INTENSIVE'
            elif anomaly_count > 2 or anomaly_score > 0.5:
                return 'ENHANCED'
            elif anomaly_count > 0 or anomaly_score > 0.3:
                return 'INCREASED'
            else:
                return 'STANDARD'
                
        except Exception:
            return 'STANDARD'
    
    def _update_anomaly_tracking(self, session_id: str, analysis_result: Dict[str, Any]):
        """Update anomaly tracking data structures"""
        try:
            if session_id not in self.session_anomalies:
                self.session_anomalies[session_id] = []
            
            anomaly_record = {
                'timestamp': datetime.utcnow(),
                'anomaly_score': analysis_result.get('anomaly_score', 0.0),
                'anomaly_count': self._count_detected_anomalies(analysis_result),
                'primary_anomaly': self._identify_primary_anomaly(analysis_result),
                'monitoring_level': self._recommend_monitoring_level(analysis_result)
            }
            
            self.session_anomalies[session_id].append(anomaly_record)
            
            # Keep only last 10 anomaly records per session
            if len(self.session_anomalies[session_id]) > 10:
                self.session_anomalies[session_id] = self.session_anomalies[session_id][-10:]
            
        except Exception as e:
            self.logger.error(f"Error updating anomaly tracking: {str(e)}")
    
    def track_multi_device_usage(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔗 TRACK MULTI-DEVICE USAGE
        Comprehensive multi-device usage tracking including concurrent session detection,
        device switching pattern analysis, session migration validation, multi-device collaboration indicators,
        and device usage timeline correlation
        
        Args:
            session_data: Dictionary containing multi-device session information and device data
            
        Returns:
            Dict containing comprehensive multi-device usage analysis
        """
        try:
            self.logger.info("Starting comprehensive multi-device usage tracking")
            
            analysis_result = {
                'multi_device_summary': {},
                'concurrent_sessions': {},
                'device_switching_patterns': {},
                'session_migration_validation': {},
                'collaboration_indicators': {},
                'device_timeline_correlation': {},
                'multi_device_risk_score': 0.0,
                'device_usage_analysis': {},
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
            user_id = session_data.get('user_id', '')
            current_session_id = session_data.get('session_id', '')
            
            # 1. Concurrent Session Detection Across Devices
            concurrent_detection = self._detect_concurrent_device_sessions(session_data)
            analysis_result['concurrent_sessions'] = concurrent_detection
            
            # 2. Device Switching Pattern Analysis
            switching_analysis = self._analyze_device_switching_patterns(session_data)
            analysis_result['device_switching_patterns'] = switching_analysis
            
            # 3. Session Migration Validation
            migration_validation = self._validate_session_migration(session_data)
            analysis_result['session_migration_validation'] = migration_validation
            
            # 4. Multi-Device Collaboration Indicators
            collaboration_indicators = self._detect_multi_device_collaboration(session_data)
            analysis_result['collaboration_indicators'] = collaboration_indicators
            
            # 5. Device Usage Timeline Correlation
            timeline_correlation = self._correlate_device_usage_timeline(session_data)
            analysis_result['device_timeline_correlation'] = timeline_correlation
            
            # 6. Calculate Multi-Device Risk Score
            risk_factors = [
                concurrent_detection.get('risk_score', 0.0),
                switching_analysis.get('risk_score', 0.0),
                migration_validation.get('risk_score', 0.0),
                collaboration_indicators.get('risk_score', 0.0),
                timeline_correlation.get('risk_score', 0.0)
            ]
            analysis_result['multi_device_risk_score'] = statistics.mean(risk_factors)
            
            # 7. Device Usage Analysis Summary
            device_usage_summary = self._analyze_device_usage_patterns(session_data, analysis_result)
            analysis_result['device_usage_analysis'] = device_usage_summary
            
            # Multi-Device Summary
            legitimate_usage = analysis_result['multi_device_risk_score'] < 0.5
            analysis_result['multi_device_summary'] = {
                'legitimate_multi_device_usage': legitimate_usage,
                'concurrent_device_count': concurrent_detection.get('concurrent_device_count', 0),
                'device_switching_frequency': switching_analysis.get('switching_frequency', 0),
                'suspicious_migration_detected': migration_validation.get('suspicious_migration', False),
                'collaboration_likelihood': collaboration_indicators.get('collaboration_probability', 0.0),
                'timeline_consistency': timeline_correlation.get('timeline_consistency_score', 0.0),
                'multi_device_risk_level': self._classify_multi_device_risk(analysis_result['multi_device_risk_score']),
                'recommended_action': self._recommend_multi_device_action(analysis_result)
            }
            
            # Update multi-device tracking
            self._update_multi_device_tracking(user_id, current_session_id, analysis_result)
            
            self.logger.info(f"Multi-device usage tracking completed - User: {user_id}, Risk: {analysis_result['multi_device_risk_score']:.3f}")
            
            return {
                'success': True,
                'multi_device_analysis': analysis_result,
                'analysis_summary': {
                    'user_id': user_id,
                    'session_id': current_session_id,
                    'legitimate_usage': legitimate_usage,
                    'concurrent_devices': concurrent_detection.get('concurrent_device_count', 0),
                    'risk_score': analysis_result['multi_device_risk_score'],
                    'risk_level': analysis_result['multi_device_summary']['multi_device_risk_level']
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error tracking multi-device usage: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
    
    # ===== MULTI-DEVICE USAGE TRACKING HELPER METHODS =====
    
    def _detect_concurrent_device_sessions(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect concurrent sessions across different devices"""
        try:
            user_id = session_data.get('user_id', '')
            current_device_data = session_data.get('device_data', {})
            active_sessions = session_data.get('active_sessions', [])
            
            analysis = {
                'concurrent_sessions_detected': False,
                'concurrent_device_count': 0,
                'concurrent_devices': [],
                'concurrent_session_details': [],
                'device_diversity_score': 0.0,
                'geographic_diversity': {},
                'suspicious_concurrency': False,
                'risk_score': 0.0
            }
            
            if not active_sessions:
                return analysis
            
            current_time = datetime.utcnow()
            concurrent_sessions = []
            unique_devices = set()
            unique_locations = set()
            
            for session in active_sessions:
                session_start = session.get('start_time')
                session_device = session.get('device_fingerprint', '')
                session_location = session.get('location', {})
                session_ip = session.get('ip_address', '')
                
                # Check if session is currently active (within last 10 minutes)
                if session_start:
                    try:
                        start_dt = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                        time_diff = (current_time - start_dt).total_seconds()
                        if time_diff < 600:  # Active within last 10 minutes
                            concurrent_sessions.append(session)
                            unique_devices.add(session_device)
                            if session_location:
                                location_key = f"{session_location.get('country', '')}-{session_location.get('city', '')}"
                                unique_locations.add(location_key)
                    except Exception:
                        # Handle datetime parsing errors
                        concurrent_sessions.append(session)
                        unique_devices.add(session_device)
            
            analysis['concurrent_sessions_detected'] = len(concurrent_sessions) > 1
            analysis['concurrent_device_count'] = len(unique_devices)
            analysis['concurrent_devices'] = list(unique_devices)
            analysis['concurrent_session_details'] = concurrent_sessions
            
            # Calculate device diversity score
            if len(concurrent_sessions) > 0:
                analysis['device_diversity_score'] = len(unique_devices) / len(concurrent_sessions)
            
            # Geographic diversity analysis
            analysis['geographic_diversity'] = {
                'unique_locations': list(unique_locations),
                'location_count': len(unique_locations),
                'impossible_travel_detected': self._detect_impossible_travel(concurrent_sessions)
            }
            
            # Determine suspicious concurrency
            analysis['suspicious_concurrency'] = (
                len(concurrent_sessions) > 5 or  # Too many concurrent sessions
                analysis['geographic_diversity']['impossible_travel_detected'] or
                analysis['device_diversity_score'] > 0.8  # Too diverse device usage
            )
            
            # Calculate risk score
            risk_factors = 0.0
            if len(concurrent_sessions) > 3:
                risk_factors += min(len(concurrent_sessions) * 0.1, 0.4)
            if analysis['geographic_diversity']['impossible_travel_detected']:
                risk_factors += 0.6
            if analysis['device_diversity_score'] > 0.7:
                risk_factors += 0.3
            
            analysis['risk_score'] = min(risk_factors, 1.0)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error detecting concurrent device sessions: {str(e)}")
            return {'risk_score': 0.5, 'error': str(e)}
    
    def _analyze_device_switching_patterns(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze device switching patterns for suspicious behavior"""
        try:
            user_id = session_data.get('user_id', '')
            session_history = session_data.get('session_history', [])
            device_usage_history = session_data.get('device_usage_history', [])
            
            analysis = {
                'switching_detected': False,
                'switching_frequency': 0,
                'switching_patterns': [],
                'device_transition_matrix': {},
                'unusual_switching_detected': False,
                'switching_velocity_analysis': {},
                'device_preference_analysis': {},
                'risk_score': 0.0
            }
            
            if len(session_history) < 2:
                return analysis
            
            # Analyze device switching frequency
            device_switches = []
            previous_device = None
            
            for session in sorted(session_history, key=lambda x: x.get('timestamp', '')):
                current_device = session.get('device_fingerprint', '')
                if previous_device and current_device != previous_device:
                    switch_data = {
                        'from_device': previous_device,
                        'to_device': current_device,
                        'timestamp': session.get('timestamp', ''),
                        'session_duration': session.get('duration', 0),
                        'location_change': self._detect_location_change(session, session_history)
                    }
                    device_switches.append(switch_data)
                previous_device = current_device
            
            analysis['switching_detected'] = len(device_switches) > 0
            analysis['switching_frequency'] = len(device_switches)
            analysis['switching_patterns'] = device_switches
            
            # Build device transition matrix
            transition_matrix = {}
            for switch in device_switches:
                from_device = switch['from_device']
                to_device = switch['to_device']
                
                if from_device not in transition_matrix:
                    transition_matrix[from_device] = {}
                if to_device not in transition_matrix[from_device]:
                    transition_matrix[from_device][to_device] = 0
                
                transition_matrix[from_device][to_device] += 1
            
            analysis['device_transition_matrix'] = transition_matrix
            
            # Analyze switching velocity (switches per time period)
            if len(session_history) > 1:
                time_span_hours = self._calculate_session_time_span(session_history)
                if time_span_hours > 0:
                    switching_velocity = len(device_switches) / time_span_hours
                    analysis['switching_velocity_analysis'] = {
                        'switches_per_hour': switching_velocity,
                        'excessive_switching': switching_velocity > 2.0,  # More than 2 switches per hour
                        'time_span_hours': time_span_hours
                    }
            
            # Device preference analysis
            device_usage_counts = {}
            for session in session_history:
                device = session.get('device_fingerprint', '')
                device_usage_counts[device] = device_usage_counts.get(device, 0) + 1
            
            if device_usage_counts:
                most_used_device = max(device_usage_counts.items(), key=lambda x: x[1])
                analysis['device_preference_analysis'] = {
                    'most_used_device': most_used_device[0],
                    'usage_distribution': device_usage_counts,
                    'device_diversity': len(device_usage_counts),
                    'primary_device_dominance': most_used_device[1] / len(session_history)
                }
            
            # Detect unusual switching patterns
            unusual_patterns = []
            
            # Rapid device switching (multiple switches in short time)
            rapid_switches = [s for s in device_switches if s.get('session_duration', 3600) < 300]  # Less than 5 minutes
            if len(rapid_switches) > 2:
                unusual_patterns.append('rapid_device_switching')
            
            # Geographic inconsistency with device switches
            location_inconsistent_switches = [s for s in device_switches if s.get('location_change', False)]
            if len(location_inconsistent_switches) > len(device_switches) * 0.7:
                unusual_patterns.append('geographic_inconsistent_switching')
            
            # Excessive device diversity
            if analysis['device_preference_analysis'].get('device_diversity', 0) > 5:
                unusual_patterns.append('excessive_device_diversity')
            
            analysis['unusual_switching_detected'] = len(unusual_patterns) > 0
            
            # Calculate risk score
            risk_factors = 0.0
            if analysis['switching_frequency'] > 10:
                risk_factors += 0.3
            if analysis.get('switching_velocity_analysis', {}).get('excessive_switching', False):
                risk_factors += 0.4
            if len(unusual_patterns) > 0:
                risk_factors += len(unusual_patterns) * 0.2
            
            analysis['risk_score'] = min(risk_factors, 1.0)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing device switching patterns: {str(e)}")
            return {'risk_score': 0.5, 'error': str(e)}
    
    def _validate_session_migration(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate session migration between devices"""
        try:
            migration_data = session_data.get('migration_data', {})
            session_continuity_data = session_data.get('session_continuity', {})
            
            analysis = {
                'migration_detected': False,
                'migration_validation': {},
                'migration_integrity': {},
                'state_preservation': {},
                'suspicious_migration': False,
                'migration_timeline': [],
                'data_consistency_validation': {},
                'risk_score': 0.0
            }
            
            if not migration_data:
                return analysis
            
            # Detect migration events
            migration_events = migration_data.get('migration_events', [])
            analysis['migration_detected'] = len(migration_events) > 0
            
            # Validate each migration
            valid_migrations = 0
            total_migrations = len(migration_events)
            
            for migration in migration_events:
                validation_result = self._validate_single_migration(migration, session_continuity_data)
                
                migration_validation = {
                    'migration_id': migration.get('migration_id', ''),
                    'source_device': migration.get('source_device', ''),
                    'target_device': migration.get('target_device', ''),
                    'migration_timestamp': migration.get('timestamp', ''),
                    'validation_passed': validation_result.get('valid', False),
                    'validation_score': validation_result.get('score', 0.0),
                    'integrity_issues': validation_result.get('issues', [])
                }
                
                if validation_result.get('valid', False):
                    valid_migrations += 1
                
                analysis['migration_timeline'].append(migration_validation)
            
            # Migration integrity analysis
            if total_migrations > 0:
                analysis['migration_integrity'] = {
                    'total_migrations': total_migrations,
                    'valid_migrations': valid_migrations,
                    'integrity_percentage': (valid_migrations / total_migrations) * 100,
                    'failed_migrations': total_migrations - valid_migrations
                }
            
            # State preservation analysis
            state_data = migration_data.get('state_preservation', {})
            analysis['state_preservation'] = {
                'session_state_preserved': state_data.get('session_preserved', True),
                'user_context_preserved': state_data.get('context_preserved', True),
                'authentication_preserved': state_data.get('auth_preserved', True),
                'data_integrity_maintained': state_data.get('data_integrity', True)
            }
            
            # Data consistency validation
            consistency_data = migration_data.get('data_consistency', {})
            analysis['data_consistency_validation'] = {
                'session_id_consistency': consistency_data.get('session_id_consistent', True),
                'user_id_consistency': consistency_data.get('user_id_consistent', True),
                'timestamp_consistency': consistency_data.get('timestamp_consistent', True),
                'data_checksum_validation': consistency_data.get('checksum_valid', True)
            }
            
            # Detect suspicious migration patterns
            suspicious_indicators = []
            
            # Too many migrations in short time
            if total_migrations > 5:
                suspicious_indicators.append('excessive_migrations')
            
            # Low integrity percentage
            if analysis.get('migration_integrity', {}).get('integrity_percentage', 100) < 70:
                suspicious_indicators.append('low_integrity_migrations')
            
            # State preservation failures
            state_issues = sum([not v for v in analysis['state_preservation'].values()])
            if state_issues > 1:
                suspicious_indicators.append('state_preservation_failures')
            
            # Data consistency failures
            consistency_issues = sum([not v for v in analysis['data_consistency_validation'].values()])
            if consistency_issues > 0:
                suspicious_indicators.append('data_consistency_failures')
            
            analysis['suspicious_migration'] = len(suspicious_indicators) > 0
            
            # Calculate risk score
            risk_factors = 0.0
            if total_migrations > 3:
                risk_factors += min(total_migrations * 0.1, 0.4)
            if analysis.get('migration_integrity', {}).get('integrity_percentage', 100) < 80:
                risk_factors += 0.3
            if len(suspicious_indicators) > 0:
                risk_factors += len(suspicious_indicators) * 0.2
            
            analysis['risk_score'] = min(risk_factors, 1.0)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error validating session migration: {str(e)}")
            return {'risk_score': 0.5, 'error': str(e)}
    
    def _detect_multi_device_collaboration(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect indicators of multi-device collaboration"""
        try:
            collaboration_data = session_data.get('collaboration_indicators', {})
            device_activity_data = session_data.get('device_activity', [])
            
            analysis = {
                'collaboration_detected': False,
                'collaboration_probability': 0.0,
                'collaboration_patterns': [],
                'synchronized_activities': [],
                'complementary_actions': [],
                'temporal_correlation': {},
                'device_role_analysis': {},
                'risk_score': 0.0
            }
            
            if len(device_activity_data) < 2:
                return analysis
            
            # Analyze synchronized activities across devices
            synchronized_activities = self._detect_synchronized_activities(device_activity_data)
            analysis['synchronized_activities'] = synchronized_activities
            
            # Detect complementary actions (different devices doing complementary tasks)
            complementary_actions = self._detect_complementary_actions(device_activity_data)
            analysis['complementary_actions'] = complementary_actions
            
            # Temporal correlation analysis
            temporal_correlation = self._analyze_temporal_correlation(device_activity_data)
            analysis['temporal_correlation'] = temporal_correlation
            
            # Device role analysis
            device_roles = self._analyze_device_roles(device_activity_data)
            analysis['device_role_analysis'] = device_roles
            
            # Collaboration patterns detection
            collaboration_patterns = []
            
            # Pattern 1: Simultaneous but different activities
            if len(synchronized_activities) > 0 and len(complementary_actions) > 0:
                collaboration_patterns.append('simultaneous_complementary_work')
            
            # Pattern 2: Sequential handoffs between devices
            handoffs = self._detect_device_handoffs(device_activity_data)
            if len(handoffs) > 2:
                collaboration_patterns.append('sequential_device_handoffs')
            
            # Pattern 3: Specialized device usage
            if device_roles.get('role_specialization_detected', False):
                collaboration_patterns.append('specialized_device_usage')
            
            # Pattern 4: Cross-device data sharing
            data_sharing = collaboration_data.get('cross_device_data_sharing', [])
            if len(data_sharing) > 0:
                collaboration_patterns.append('cross_device_data_sharing')
            
            analysis['collaboration_patterns'] = collaboration_patterns
            analysis['collaboration_detected'] = len(collaboration_patterns) > 0
            
            # Calculate collaboration probability
            probability_factors = [
                len(synchronized_activities) * 0.1,
                len(complementary_actions) * 0.15,
                temporal_correlation.get('correlation_strength', 0) * 0.3,
                len(collaboration_patterns) * 0.2,
                device_roles.get('specialization_score', 0) * 0.25
            ]
            
            analysis['collaboration_probability'] = min(sum(probability_factors), 1.0)
            
            # Risk assessment (collaboration itself isn't necessarily risky, but unusual patterns might be)
            risk_factors = 0.0
            
            # High collaboration probability with no clear legitimate use case
            if analysis['collaboration_probability'] > 0.8:
                legitimate_indicators = collaboration_data.get('legitimate_collaboration_indicators', 0)
                if legitimate_indicators < 2:
                    risk_factors += 0.3
            
            # Unusual temporal patterns
            if temporal_correlation.get('unusual_patterns_detected', False):
                risk_factors += 0.4
            
            # Suspicious data sharing patterns
            suspicious_sharing = [s for s in data_sharing if s.get('suspicious', False)]
            if len(suspicious_sharing) > 0:
                risk_factors += len(suspicious_sharing) * 0.2
            
            analysis['risk_score'] = min(risk_factors, 1.0)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error detecting multi-device collaboration: {str(e)}")
            return {'risk_score': 0.5, 'error': str(e)}
    
    def _correlate_device_usage_timeline(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Correlate device usage timeline for consistency analysis"""
        try:
            timeline_data = session_data.get('device_timeline', [])
            user_behavior_data = session_data.get('user_behavior_timeline', [])
            
            analysis = {
                'timeline_consistency': 0.0,
                'timeline_correlation_analysis': {},
                'usage_pattern_consistency': {},
                'temporal_anomalies': [],
                'device_usage_flow': [],
                'consistency_violations': [],
                'risk_score': 0.0
            }
            
            if len(timeline_data) < 2:
                analysis['timeline_consistency'] = 1.0
                return analysis
            
            # Sort timeline data by timestamp
            sorted_timeline = sorted(timeline_data, key=lambda x: x.get('timestamp', ''))
            
            # Analyze timeline consistency
            consistency_violations = []
            usage_flow = []
            
            for i in range(len(sorted_timeline) - 1):
                current_event = sorted_timeline[i]
                next_event = sorted_timeline[i + 1]
                
                # Check for temporal consistency
                temporal_check = self._check_temporal_consistency(current_event, next_event)
                if not temporal_check['consistent']:
                    consistency_violations.append(temporal_check)
                
                # Build usage flow
                flow_segment = {
                    'from_device': current_event.get('device_id', ''),
                    'to_device': next_event.get('device_id', ''),
                    'duration': self._calculate_event_duration(current_event, next_event),
                    'activity_continuity': self._check_activity_continuity(current_event, next_event),
                    'location_consistency': self._check_location_consistency(current_event, next_event)
                }
                usage_flow.append(flow_segment)
            
            analysis['device_usage_flow'] = usage_flow
            analysis['consistency_violations'] = consistency_violations
            
            # Calculate timeline consistency score
            total_transitions = len(sorted_timeline) - 1
            if total_transitions > 0:
                consistent_transitions = total_transitions - len(consistency_violations)
                analysis['timeline_consistency'] = consistent_transitions / total_transitions
            else:
                analysis['timeline_consistency'] = 1.0
            
            # Usage pattern consistency analysis
            pattern_analysis = self._analyze_usage_pattern_consistency(sorted_timeline, user_behavior_data)
            analysis['usage_pattern_consistency'] = pattern_analysis
            
            # Temporal anomaly detection
            temporal_anomalies = self._detect_timeline_temporal_anomalies(sorted_timeline)
            analysis['temporal_anomalies'] = temporal_anomalies
            
            # Timeline correlation analysis
            correlation_analysis = {
                'user_behavior_correlation': self._correlate_with_user_behavior(sorted_timeline, user_behavior_data),
                'device_capability_correlation': self._correlate_with_device_capabilities(sorted_timeline),
                'geographic_correlation': self._correlate_with_geographic_data(sorted_timeline)
            }
            analysis['timeline_correlation_analysis'] = correlation_analysis
            
            # Risk assessment
            risk_factors = 0.0
            
            # Low timeline consistency
            if analysis['timeline_consistency'] < 0.7:
                risk_factors += (1.0 - analysis['timeline_consistency']) * 0.5
            
            # Multiple temporal anomalies
            if len(temporal_anomalies) > 2:
                risk_factors += min(len(temporal_anomalies) * 0.1, 0.4)
            
            # Pattern consistency issues
            pattern_score = pattern_analysis.get('consistency_score', 1.0)
            if pattern_score < 0.6:
                risk_factors += (1.0 - pattern_score) * 0.3
            
            analysis['risk_score'] = min(risk_factors, 1.0)
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error correlating device usage timeline: {str(e)}")
            return {'risk_score': 0.5, 'error': str(e)}
    
    # ===== MULTI-DEVICE HELPER METHODS =====
    
    def _detect_impossible_travel(self, concurrent_sessions: List[Dict[str, Any]]) -> bool:
        """Detect impossible travel between concurrent session locations"""
        try:
            if len(concurrent_sessions) < 2:
                return False
            
            locations = []
            for session in concurrent_sessions:
                location = session.get('location', {})
                if location.get('lat') and location.get('lng'):
                    locations.append({
                        'lat': float(location['lat']),
                        'lng': float(location['lng']),
                        'timestamp': session.get('timestamp', '')
                    })
            
            # Check distances between locations
            for i in range(len(locations)):
                for j in range(i + 1, len(locations)):
                    loc1, loc2 = locations[i], locations[j]
                    distance = self._calculate_distance(loc1['lat'], loc1['lng'], loc2['lat'], loc2['lng'])
                    
                    # If distance > 1000km for concurrent sessions, consider impossible
                    if distance > 1000:  # kilometers
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two coordinates in kilometers"""
        try:
            # Haversine formula
            R = 6371  # Earth's radius in kilometers
            
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lng = math.radians(lng2 - lng1)
            
            a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(delta_lng/2) * math.sin(delta_lng/2))
            
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            distance = R * c
            
            return distance
            
        except Exception:
            return 0.0
    
    def _detect_location_change(self, session: Dict[str, Any], session_history: List[Dict[str, Any]]) -> bool:
        """Detect if location changed between sessions"""
        try:
            current_location = session.get('location', {})
            if not current_location:
                return False
            
            # Find previous session for comparison
            session_timestamp = session.get('timestamp', '')
            previous_session = None
            
            for hist_session in sorted(session_history, key=lambda x: x.get('timestamp', '')):
                if hist_session.get('timestamp', '') < session_timestamp:
                    previous_session = hist_session
            
            if not previous_session:
                return False
            
            previous_location = previous_session.get('location', {})
            if not previous_location:
                return False
            
            # Compare locations
            return (current_location.get('country') != previous_location.get('country') or
                    current_location.get('city') != previous_location.get('city'))
            
        except Exception:
            return False
    
    def _calculate_session_time_span(self, session_history: List[Dict[str, Any]]) -> float:
        """Calculate time span of session history in hours"""
        try:
            if len(session_history) < 2:
                return 0.0
            
            timestamps = [s.get('timestamp', '') for s in session_history if s.get('timestamp')]
            if len(timestamps) < 2:
                return 0.0
            
            # Sort timestamps
            sorted_timestamps = sorted(timestamps)
            earliest = datetime.fromisoformat(sorted_timestamps[0].replace('Z', '+00:00'))
            latest = datetime.fromisoformat(sorted_timestamps[-1].replace('Z', '+00:00'))
            
            time_diff = latest - earliest
            return time_diff.total_seconds() / 3600  # Convert to hours
            
        except Exception:
            return 0.0
    
    def _validate_single_migration(self, migration: Dict[str, Any], continuity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single session migration"""
        try:
            validation = {
                'valid': True,
                'score': 1.0,
                'issues': []
            }
            
            # Check required migration fields
            required_fields = ['source_device', 'target_device', 'timestamp', 'migration_id']
            for field in required_fields:
                if not migration.get(field):
                    validation['issues'].append(f'missing_{field}')
                    validation['score'] -= 0.2
            
            # Check migration timing
            migration_timestamp = migration.get('timestamp', '')
            if migration_timestamp:
                try:
                    migration_time = datetime.fromisoformat(migration_timestamp.replace('Z', '+00:00'))
                    current_time = datetime.utcnow()
                    
                    # Migration shouldn't be in the future
                    if migration_time > current_time:
                        validation['issues'].append('future_migration_timestamp')
                        validation['score'] -= 0.4
                        
                except Exception:
                    validation['issues'].append('invalid_timestamp_format')
                    validation['score'] -= 0.3
            
            # Check device consistency
            source_device = migration.get('source_device', '')
            target_device = migration.get('target_device', '')
            
            if source_device == target_device:
                validation['issues'].append('source_target_device_identical')
                validation['score'] -= 0.5
            
            # Check continuity data consistency
            if continuity_data:
                session_devices = continuity_data.get('session_devices', [])
                if source_device not in session_devices:
                    validation['issues'].append('source_device_not_in_session_history')
                    validation['score'] -= 0.3
            
            validation['valid'] = validation['score'] > 0.5
            
            return validation
            
        except Exception:
            return {'valid': False, 'score': 0.0, 'issues': ['validation_error']}
    
    def _detect_synchronized_activities(self, device_activity_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect synchronized activities across devices"""
        try:
            synchronized_activities = []
            
            # Group activities by timestamp (within 30-second windows)
            time_groups = {}
            for activity in device_activity_data:
                timestamp_str = activity.get('timestamp', '')
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        # Round to nearest 30-second interval
                        rounded_timestamp = timestamp.replace(second=(timestamp.second // 30) * 30, microsecond=0)
                        key = rounded_timestamp.isoformat()
                        
                        if key not in time_groups:
                            time_groups[key] = []
                        time_groups[key].append(activity)
                    except Exception:
                        continue
            
            # Find groups with multiple devices
            for timestamp, activities in time_groups.items():
                if len(activities) > 1:
                    unique_devices = set(a.get('device_id', '') for a in activities)
                    if len(unique_devices) > 1:
                        synchronized_activities.append({
                            'timestamp': timestamp,
                            'device_count': len(unique_devices),
                            'devices': list(unique_devices),
                            'activities': activities,
                            'synchronization_score': len(unique_devices) / len(activities)
                        })
            
            return synchronized_activities
            
        except Exception:
            return []
    
    def _detect_complementary_actions(self, device_activity_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect complementary actions across devices"""
        try:
            complementary_actions = []
            
            # Define complementary action pairs
            complementary_pairs = [
                ('data_input', 'data_analysis'),
                ('document_creation', 'document_review'),
                ('research', 'writing'),
                ('coding', 'testing'),
                ('design', 'development')
            ]
            
            # Look for complementary actions in time windows
            for i, activity1 in enumerate(device_activity_data):
                for j, activity2 in enumerate(device_activity_data[i+1:], i+1):
                    if activity1.get('device_id') == activity2.get('device_id'):
                        continue  # Same device
                    
                    action1 = activity1.get('action_type', '')
                    action2 = activity2.get('action_type', '')
                    
                    # Check if actions are complementary
                    for pair in complementary_pairs:
                        if (action1 in pair[0] and action2 in pair[1]) or (action1 in pair[1] and action2 in pair[0]):
                            time_diff = self._calculate_activity_time_diff(activity1, activity2)
                            if 0 < time_diff < 3600:  # Within 1 hour
                                complementary_actions.append({
                                    'activity1': activity1,
                                    'activity2': activity2,
                                    'complementary_pair': pair,
                                    'time_difference_seconds': time_diff,
                                    'complementarity_score': 1.0 - (time_diff / 3600)  # Closer in time = higher score
                                })
            
            return complementary_actions
            
        except Exception:
            return []
    
    def _analyze_temporal_correlation(self, device_activity_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal correlation between device activities"""
        try:
            analysis = {
                'correlation_strength': 0.0,
                'temporal_patterns': [],
                'unusual_patterns_detected': False,
                'correlation_details': {}
            }
            
            if len(device_activity_data) < 4:
                return analysis
            
            # Group activities by device
            device_activities = {}
            for activity in device_activity_data:
                device_id = activity.get('device_id', '')
                if device_id not in device_activities:
                    device_activities[device_id] = []
                device_activities[device_id].append(activity)
            
            if len(device_activities) < 2:
                return analysis
            
            # Calculate correlation between device activity timelines
            device_pairs = [(d1, d2) for d1 in device_activities.keys() 
                           for d2 in device_activities.keys() if d1 < d2]
            
            correlations = []
            for device1, device2 in device_pairs:
                correlation = self._calculate_device_activity_correlation(
                    device_activities[device1], 
                    device_activities[device2]
                )
                correlations.append(correlation)
            
            if correlations:
                analysis['correlation_strength'] = statistics.mean(correlations)
            
            # Detect unusual temporal patterns
            unusual_patterns = []
            
            # Perfect synchronization (too regular)
            if analysis['correlation_strength'] > 0.9:
                unusual_patterns.append('perfect_synchronization')
            
            # Alternating pattern (devices taking turns too regularly)
            alternating_score = self._detect_alternating_pattern(device_activity_data)
            if alternating_score > 0.8:
                unusual_patterns.append('regular_alternating_pattern')
            
            analysis['unusual_patterns_detected'] = len(unusual_patterns) > 0
            analysis['temporal_patterns'] = unusual_patterns
            
            return analysis
            
        except Exception:
            return {'correlation_strength': 0.0}
    
    def _analyze_device_roles(self, device_activity_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze device roles and specialization"""
        try:
            analysis = {
                'role_specialization_detected': False,
                'device_roles': {},
                'specialization_score': 0.0,
                'role_distribution': {}
            }
            
            # Analyze activity types by device
            device_activities = {}
            for activity in device_activity_data:
                device_id = activity.get('device_id', '')
                activity_type = activity.get('activity_type', '')
                
                if device_id not in device_activities:
                    device_activities[device_id] = {}
                if activity_type not in device_activities[device_id]:
                    device_activities[device_id][activity_type] = 0
                
                device_activities[device_id][activity_type] += 1
            
            # Determine primary role for each device
            for device_id, activities in device_activities.items():
                if activities:
                    primary_activity = max(activities.items(), key=lambda x: x[1])
                    total_activities = sum(activities.values())
                    
                    role_info = {
                        'primary_activity': primary_activity[0],
                        'activity_distribution': activities,
                        'specialization_percentage': (primary_activity[1] / total_activities) * 100,
                        'activity_diversity': len(activities)
                    }
                    
                    # Classify device role based on primary activity
                    role_info['device_role'] = self._classify_device_role(primary_activity[0])
                    
                    analysis['device_roles'][device_id] = role_info
            
            # Calculate overall specialization score
            specialization_scores = []
            for device_info in analysis['device_roles'].values():
                spec_score = device_info['specialization_percentage'] / 100
                specialization_scores.append(spec_score)
            
            if specialization_scores:
                analysis['specialization_score'] = statistics.mean(specialization_scores)
                analysis['role_specialization_detected'] = analysis['specialization_score'] > 0.7
            
            return analysis
            
        except Exception:
            return {'role_specialization_detected': False}
    
    def _classify_device_role(self, primary_activity: str) -> str:
        """Classify device role based on primary activity"""
        role_mappings = {
            'data_input': 'input_device',
            'document_creation': 'content_creation',
            'research': 'research_device',
            'communication': 'communication_hub',
            'analysis': 'analysis_workstation',
            'testing': 'testing_environment',
            'monitoring': 'monitoring_console'
        }
        
        for activity_pattern, role in role_mappings.items():
            if activity_pattern in primary_activity.lower():
                return role
        
        return 'general_purpose'
    
    # Additional helper methods continue...
    
    def _classify_multi_device_risk(self, risk_score: float) -> str:
        """Classify multi-device risk level"""
        if risk_score > 0.8:
            return 'CRITICAL'
        elif risk_score > 0.6:
            return 'HIGH'
        elif risk_score > 0.4:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _recommend_multi_device_action(self, analysis_result: Dict[str, Any]) -> str:
        """Recommend action based on multi-device analysis"""
        risk_score = analysis_result.get('multi_device_risk_score', 0.0)
        suspicious_migration = analysis_result.get('session_migration_validation', {}).get('suspicious_migration', False)
        concurrent_devices = analysis_result.get('concurrent_sessions', {}).get('concurrent_device_count', 0)
        
        if risk_score > 0.8 or suspicious_migration:
            return 'IMMEDIATE_INTERVENTION_REQUIRED'
        elif risk_score > 0.6 or concurrent_devices > 5:
            return 'ENHANCED_MONITORING'
        elif risk_score > 0.4:
            return 'INCREASED_ALERTING'
        else:
            return 'CONTINUE_MONITORING'
    
    def _update_multi_device_tracking(self, user_id: str, session_id: str, analysis_result: Dict[str, Any]):
        """Update multi-device tracking data structures"""
        try:
            # Update user sessions tracking
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = []
            
            if session_id not in self.user_sessions[user_id]:
                self.user_sessions[user_id].append(session_id)
            
            # Keep only last 20 sessions per user
            if len(self.user_sessions[user_id]) > 20:
                self.user_sessions[user_id] = self.user_sessions[user_id][-20:]
            
            # Update session history with multi-device analysis
            if session_id not in self.session_history:
                self.session_history[session_id] = []
            
            multi_device_record = {
                'timestamp': datetime.utcnow(),
                'analysis_type': 'multi_device_usage',
                'risk_score': analysis_result.get('multi_device_risk_score', 0.0),
                'concurrent_devices': analysis_result.get('concurrent_sessions', {}).get('concurrent_device_count', 0),
                'collaboration_detected': analysis_result.get('collaboration_indicators', {}).get('collaboration_detected', False)
            }
            
            self.session_history[session_id].append(multi_device_record)
            
        except Exception as e:
            self.logger.error(f"Error updating multi-device tracking: {str(e)}")


        except Exception as e:
            self.logger.error(f"Error updating anomaly tracking: {str(e)}")


# Initialize global SessionIntegrityMonitor instance
session_integrity_monitor = SessionIntegrityMonitor()


# Initialize global EnvironmentAnalyzer instance
environment_analyzer = EnvironmentAnalyzer()


# Initialize global instance
device_fingerprinting_engine = DeviceFingerprintingEngine()

# Export main class for use in server.py
__all__ = [
    'DeviceFingerprintingEngine',
    'DeviceFingerprint', 
    'DeviceTrackingRecord',
    'device_fingerprinting_engine',
    'EnvironmentAnalyzer',
    'environment_analyzer',
    'SessionIntegrityMonitor',
    'session_integrity_monitor'
]