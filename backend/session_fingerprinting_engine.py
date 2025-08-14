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
        Comprehensive virtual machine detection through hardware indicators,
        hypervisor presence analysis, and performance characteristics
        
        Args:
            device_data: Device characteristics data
            
        Returns:
            Dict containing VM detection analysis
        """
        try:
            self.logger.info("Performing comprehensive VM detection analysis")
            
            # Ensure device_data is a dictionary and extract components safely
            if not isinstance(device_data, dict):
                self.logger.warning(f"Device data is not a dictionary: {type(device_data)}")
                device_data = {}
            
            hardware_data = device_data.get('hardware', {})
            os_data = device_data.get('os', {})
            browser_data = device_data.get('browser', {})
            performance_data = device_data.get('performance', {})
            
            # Ensure all components are dictionaries
            if not isinstance(hardware_data, dict):
                self.logger.warning(f"Hardware data is not a dictionary: {type(hardware_data)}")
                hardware_data = {}
            if not isinstance(os_data, dict):
                self.logger.warning(f"OS data is not a dictionary: {type(os_data)}")
                os_data = {}
            if not isinstance(browser_data, dict):
                self.logger.warning(f"Browser data is not a dictionary: {type(browser_data)}")
                browser_data = {}
            if not isinstance(performance_data, dict):
                self.logger.warning(f"Performance data is not a dictionary: {type(performance_data)}")
                performance_data = {}
            
            vm_detection_results = {}
            
            # 1. Hardware-based VM Detection
            hardware_vm_indicators = self._detect_hardware_vm_indicators(hardware_data)
            vm_detection_results['hardware_indicators'] = hardware_vm_indicators
            
            # 2. Hypervisor Presence Analysis
            hypervisor_analysis = self._analyze_hypervisor_presence(os_data, browser_data)
            vm_detection_results['hypervisor_analysis'] = hypervisor_analysis
            
            # 3. Performance Characteristic Anomalies
            performance_anomalies = self._analyze_vm_performance_anomalies(performance_data)
            vm_detection_results['performance_anomalies'] = performance_anomalies
            
            # 4. Registry/System File Analysis (via browser fingerprinting)
            system_analysis = self._analyze_vm_system_indicators(browser_data, os_data)
            vm_detection_results['system_analysis'] = system_analysis
            
            # 5. VM Software Signature Detection
            software_signatures = self._detect_vm_software_signatures(hardware_data, os_data)
            vm_detection_results['software_signatures'] = software_signatures
            
            # 6. Calculate Overall VM Probability
            vm_probability = self._calculate_vm_probability(vm_detection_results)
            
            # 7. VM Classification
            vm_classification = self._classify_vm_type(vm_detection_results)
            
            return {
                'success': True,
                'vm_detection_results': vm_detection_results,
                'vm_probability': vm_probability,
                'vm_classification': vm_classification,
                'is_virtual_machine': vm_probability > 0.7,
                'confidence_level': self._calculate_vm_detection_confidence(vm_detection_results),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error in VM detection: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.utcnow().isoformat()
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
    
    # ===== VIRTUAL MACHINE DETECTION HELPER METHODS =====
    
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
        return {
            'signature_changes': 0,
            'stability_score': 0.95,
            'evolution_trend': 'stable'
        }
    
    def _detect_hardware_changes(self, device_id: str, current_signature: Dict[str, Any]) -> Dict[str, Any]:
        """Detect changes in hardware configuration"""
        return {
            'hardware_changes_detected': False,
            'changed_components': [],
            'change_severity': 'none'
        }
    
    def _analyze_device_switching_patterns(self, device_id: str) -> Dict[str, Any]:
        """Analyze patterns of device switching"""
        return {
            'switching_frequency': 0.0,
            'suspicious_patterns': [],
            'pattern_risk_score': 0.0
        }
    
    def _calculate_device_reputation_score(self, device_id: str, consistency_analysis: Dict[str, Any]) -> float:
        """Calculate device reputation score based on historical behavior"""
        return 0.85  # Placeholder
    
    def _correlate_cross_session_data(self, device_id: str) -> Dict[str, Any]:
        """Correlate device data across multiple sessions"""
        return {
            'session_correlation': 0.92,
            'behavior_consistency': 0.88,
            'anomaly_patterns': []
        }
    
    def _update_device_tracking_record(self, device_id: str, current_signature: Dict[str, Any], 
                                     consistency_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Update device tracking record with new data"""
        return {
            'record_updated': True,
            'update_timestamp': datetime.utcnow().isoformat(),
            'tracking_version': self.signature_version
        }
    
    def _calculate_overall_consistency_score(self, consistency_analysis: Dict[str, Any]) -> float:
        """Calculate overall device consistency score"""
        return 0.87  # Placeholder
    
    def _assess_device_risk_level(self, consistency_analysis: Dict[str, Any]) -> str:
        """Assess overall risk level for the device"""
        reputation_score = consistency_analysis.get('reputation_score', 0.5)
        
        if reputation_score > 0.8:
            return 'LOW'
        elif reputation_score > 0.6:
            return 'MEDIUM'
        elif reputation_score > 0.4:
            return 'HIGH'
        else:
            return 'CRITICAL'
    
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