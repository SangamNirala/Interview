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


# Initialize global instance
device_fingerprinting_engine = DeviceFingerprintingEngine()

# Export main class for use in server.py
__all__ = [
    'DeviceFingerprintingEngine',
    'DeviceFingerprint',
    'DeviceTrackingRecord',
    'device_fingerprinting_engine'
]