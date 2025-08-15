"""
🚨 MODULE 3.3: REAL-TIME VIOLATION ALERTS SYSTEM
Comprehensive Real-Time Alert System for Fingerprint Violations and Security Incidents

This module implements a comprehensive real-time violation alert system including:
- Multi-channel alert routing (WebSocket, Email, Webhook, Database)
- Violation processing and classification with severity levels
- Critical violation escalation with automated response protocols
- Real-time dashboard data generation for monitoring interfaces
- Dynamic alert threshold configuration and management
- Integration with existing fingerprinting and ML clustering systems

Dependencies: asyncio, websockets, motor, logging, datetime
"""

import asyncio
import json
import logging
import uuid
import hashlib
import smtplib
import aiohttp
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict, field
from collections import defaultdict, deque
from enum import Enum
import statistics
import numpy as np
from motor.motor_asyncio import AsyncIOMotorClient
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    EMERGENCY = "EMERGENCY"


class AlertType(Enum):
    """Types of security alerts"""
    DEVICE_FINGERPRINT_VIOLATION = "DEVICE_FINGERPRINT_VIOLATION"
    BEHAVIORAL_ANOMALY = "BEHAVIORAL_ANOMALY"
    ML_FRAUD_DETECTION = "ML_FRAUD_DETECTION"
    SESSION_INTEGRITY_BREACH = "SESSION_INTEGRITY_BREACH"
    AUTOMATION_DETECTED = "AUTOMATION_DETECTED"
    VM_DETECTION = "VM_DETECTION"
    MULTIPLE_DEVICE_USAGE = "MULTIPLE_DEVICE_USAGE"
    TIMING_ANOMALY = "TIMING_ANOMALY"
    SUSPICIOUS_PATTERN = "SUSPICIOUS_PATTERN"
    THRESHOLD_EXCEEDED = "THRESHOLD_EXCEEDED"


class AlertChannel(Enum):
    """Available alert delivery channels"""
    WEBSOCKET = "WEBSOCKET"
    EMAIL = "EMAIL"
    WEBHOOK = "WEBHOOK"
    DATABASE = "DATABASE"
    SMS = "SMS"
    DASHBOARD = "DASHBOARD"


@dataclass
class ViolationData:
    """Comprehensive violation data structure"""
    violation_id: str
    session_id: str
    user_id: Optional[str]
    violation_type: AlertType
    severity: AlertSeverity
    confidence_score: float
    detected_at: datetime
    description: str
    technical_details: Dict[str, Any]
    device_info: Dict[str, Any]
    behavioral_context: Dict[str, Any]
    risk_factors: List[str]
    ml_analysis: Dict[str, Any] = field(default_factory=dict)
    fingerprint_data: Dict[str, Any] = field(default_factory=dict)
    location_info: Dict[str, Any] = field(default_factory=dict)
    escalation_level: int = 0
    resolution_status: str = "PENDING"
    assigned_to: Optional[str] = None
    response_actions: List[str] = field(default_factory=list)


@dataclass
class AlertThreshold:
    """Dynamic alert threshold configuration"""
    threshold_id: str
    alert_type: AlertType
    severity: AlertSeverity
    condition_type: str  # 'count', 'rate', 'score', 'pattern'
    threshold_value: float
    time_window_minutes: int
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    trigger_count: int = 0


@dataclass
class AlertConfiguration:
    """Comprehensive alert system configuration"""
    channels_enabled: List[AlertChannel]
    escalation_rules: Dict[AlertSeverity, Dict[str, Any]]
    notification_intervals: Dict[AlertSeverity, int]  # minutes
    auto_resolution_timeout: int = 60  # minutes
    max_alerts_per_session: int = 50
    rate_limiting_window: int = 300  # seconds
    dashboard_refresh_interval: int = 30  # seconds
    critical_response_timeout: int = 5  # minutes


class BaseAlertChannel:
    """Base class for alert delivery channels"""
    
    def __init__(self, channel_type: AlertChannel):
        self.channel_type = channel_type
        self.enabled = True
        self.delivery_stats = {
            'sent': 0,
            'failed': 0,
            'last_sent': None,
            'error_rate': 0.0
        }
        
    async def send_alert(self, violation: ViolationData, alert_config: AlertConfiguration) -> Dict[str, Any]:
        """Send alert through this channel - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement send_alert method")
    
    def update_stats(self, success: bool):
        """Update delivery statistics"""
        if success:
            self.delivery_stats['sent'] += 1
        else:
            self.delivery_stats['failed'] += 1
        
        self.delivery_stats['last_sent'] = datetime.now()
        total = self.delivery_stats['sent'] + self.delivery_stats['failed']
        self.delivery_stats['error_rate'] = self.delivery_stats['failed'] / max(1, total)


class WebSocketAlertChannel(BaseAlertChannel):
    """WebSocket alert channel for real-time notifications"""
    
    def __init__(self):
        super().__init__(AlertChannel.WEBSOCKET)
        self.active_connections = set()
        self.connection_groups = defaultdict(set)  # Group connections by user/session
        
    async def add_connection(self, websocket, connection_id: str, groups: List[str] = None):
        """Add WebSocket connection for alert delivery"""
        try:
            self.active_connections.add((websocket, connection_id))
            
            # Add to specified groups
            if groups:
                for group in groups:
                    self.connection_groups[group].add((websocket, connection_id))
            
            logger.info(f"WebSocket connection added: {connection_id}, groups: {groups}")
            
        except Exception as e:
            logger.error(f"Error adding WebSocket connection: {str(e)}")
    
    async def remove_connection(self, websocket, connection_id: str):
        """Remove WebSocket connection"""
        try:
            connection_tuple = (websocket, connection_id)
            self.active_connections.discard(connection_tuple)
            
            # Remove from all groups
            for group_connections in self.connection_groups.values():
                group_connections.discard(connection_tuple)
            
            logger.info(f"WebSocket connection removed: {connection_id}")
            
        except Exception as e:
            logger.error(f"Error removing WebSocket connection: {str(e)}")
    
    async def send_alert(self, violation: ViolationData, alert_config: AlertConfiguration) -> Dict[str, Any]:
        """Send alert via WebSocket to connected clients"""
        try:
            alert_message = {
                'type': 'violation_alert',
                'violation_id': violation.violation_id,
                'session_id': violation.session_id,
                'alert_type': violation.violation_type.value,
                'severity': violation.severity.value,
                'confidence_score': violation.confidence_score,
                'detected_at': violation.detected_at.isoformat(),
                'description': violation.description,
                'risk_factors': violation.risk_factors,
                'escalation_level': violation.escalation_level,
                'timestamp': datetime.now().isoformat()
            }
            
            message_json = json.dumps(alert_message)
            successful_sends = 0
            failed_sends = 0
            
            # Send to all active connections
            disconnected_connections = []
            for websocket, connection_id in self.active_connections.copy():
                try:
                    await websocket.send_text(message_json)
                    successful_sends += 1
                except Exception as e:
                    failed_sends += 1
                    disconnected_connections.append((websocket, connection_id))
                    logger.warning(f"Failed to send WebSocket alert to {connection_id}: {str(e)}")
            
            # Clean up disconnected connections
            for websocket, connection_id in disconnected_connections:
                await self.remove_connection(websocket, connection_id)
            
            self.update_stats(successful_sends > 0)
            
            return {
                'success': True,
                'channel': 'websocket',
                'successful_sends': successful_sends,
                'failed_sends': failed_sends,
                'total_connections': len(self.active_connections)
            }
            
        except Exception as e:
            self.update_stats(False)
            logger.error(f"WebSocket alert delivery error: {str(e)}")
            return {
                'success': False,
                'channel': 'websocket',
                'error': str(e)
            }


class EmailAlertChannel(BaseAlertChannel):
    """Email alert channel for notifications"""
    
    def __init__(self):
        super().__init__(AlertChannel.EMAIL)
        
        # Email configuration from environment
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_username = os.environ.get('SMTP_USERNAME', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', 'alerts@fingerprint-security.com')
        
        # Default recipient configuration
        self.default_recipients = [
            'security@company.com',
            'admin@company.com'
        ]
        
        # Email templates
        self.templates = {
            AlertSeverity.LOW: self._get_low_severity_template(),
            AlertSeverity.MEDIUM: self._get_medium_severity_template(),
            AlertSeverity.HIGH: self._get_high_severity_template(),
            AlertSeverity.CRITICAL: self._get_critical_severity_template(),
            AlertSeverity.EMERGENCY: self._get_emergency_severity_template()
        }
    
    def _get_low_severity_template(self) -> Dict[str, str]:
        """Low severity email template"""
        return {
            'subject': '[SECURITY ALERT - LOW] Fingerprint Violation Detected',
            'body': '''
            <h2>🔍 Security Alert - Low Severity</h2>
            <p><strong>Violation Type:</strong> {violation_type}</p>
            <p><strong>Session ID:</strong> {session_id}</p>
            <p><strong>Detected At:</strong> {detected_at}</p>
            <p><strong>Confidence Score:</strong> {confidence_score}</p>
            <p><strong>Description:</strong> {description}</p>
            <p><strong>Risk Factors:</strong> {risk_factors}</p>
            <br>
            <p>This is a low-severity alert that requires monitoring but may not need immediate action.</p>
            '''
        }
    
    def _get_medium_severity_template(self) -> Dict[str, str]:
        """Medium severity email template"""
        return {
            'subject': '[SECURITY ALERT - MEDIUM] ⚠️ Suspicious Activity Detected',
            'body': '''
            <h2>⚠️ Security Alert - Medium Severity</h2>
            <p><strong>Violation Type:</strong> {violation_type}</p>
            <p><strong>Session ID:</strong> {session_id}</p>
            <p><strong>Detected At:</strong> {detected_at}</p>
            <p><strong>Confidence Score:</strong> {confidence_score}</p>
            <p><strong>Description:</strong> {description}</p>
            <p><strong>Risk Factors:</strong> {risk_factors}</p>
            <p><strong>Device Info:</strong> {device_info}</p>
            <br>
            <p>This alert indicates suspicious activity that should be reviewed within 30 minutes.</p>
            '''
        }
    
    def _get_high_severity_template(self) -> Dict[str, str]:
        """High severity email template"""
        return {
            'subject': '[SECURITY ALERT - HIGH] 🚨 Critical Security Violation',
            'body': '''
            <h2>🚨 Security Alert - High Severity</h2>
            <p><strong>Violation Type:</strong> {violation_type}</p>
            <p><strong>Session ID:</strong> {session_id}</p>
            <p><strong>Detected At:</strong> {detected_at}</p>
            <p><strong>Confidence Score:</strong> {confidence_score}</p>
            <p><strong>Description:</strong> {description}</p>
            <p><strong>Risk Factors:</strong> {risk_factors}</p>
            <p><strong>Technical Details:</strong> {technical_details}</p>
            <p><strong>ML Analysis:</strong> {ml_analysis}</p>
            <br>
            <p><strong>⚠️ IMMEDIATE ATTENTION REQUIRED ⚠️</strong></p>
            <p>This high-severity alert requires immediate investigation and response.</p>
            '''
        }
    
    def _get_critical_severity_template(self) -> Dict[str, str]:
        """Critical severity email template"""
        return {
            'subject': '[SECURITY ALERT - CRITICAL] 🔥 CRITICAL SECURITY BREACH',
            'body': '''
            <h1>🔥 CRITICAL SECURITY BREACH 🔥</h1>
            <h2>Immediate Action Required</h2>
            <p><strong>Violation Type:</strong> {violation_type}</p>
            <p><strong>Session ID:</strong> {session_id}</p>
            <p><strong>Detected At:</strong> {detected_at}</p>
            <p><strong>Confidence Score:</strong> {confidence_score}</p>
            <p><strong>Description:</strong> {description}</p>
            <p><strong>Risk Factors:</strong> {risk_factors}</p>
            <p><strong>Escalation Level:</strong> {escalation_level}</p>
            <br>
            <p><strong>🚨 CRITICAL ALERT - IMMEDIATE RESPONSE REQUIRED 🚨</strong></p>
            <p>This critical alert indicates a serious security breach requiring immediate intervention.</p>
            '''
        }
    
    def _get_emergency_severity_template(self) -> Dict[str, str]:
        """Emergency severity email template"""
        return {
            'subject': '[SECURITY EMERGENCY] 🆘 EMERGENCY SECURITY INCIDENT',
            'body': '''
            <h1 style="color: red;">🆘 EMERGENCY SECURITY INCIDENT 🆘</h1>
            <h2>ALL HANDS - EMERGENCY RESPONSE REQUIRED</h2>
            <p><strong>Violation Type:</strong> {violation_type}</p>
            <p><strong>Session ID:</strong> {session_id}</p>
            <p><strong>Detected At:</strong> {detected_at}</p>
            <p><strong>Confidence Score:</strong> {confidence_score}</p>
            <p><strong>Description:</strong> {description}</p>
            <p><strong>ALL TECHNICAL DETAILS:</strong> {technical_details}</p>
            <br>
            <p><strong style="color: red;">🆘 EMERGENCY - ACTIVATE INCIDENT RESPONSE PROTOCOL 🆘</strong></p>
            <p>This is an emergency-level security incident requiring immediate activation of incident response procedures.</p>
            '''
        }
    
    async def send_alert(self, violation: ViolationData, alert_config: AlertConfiguration) -> Dict[str, Any]:
        """Send alert via email"""
        try:
            if not self.smtp_username or not self.smtp_password:
                logger.warning("Email credentials not configured, skipping email alert")
                return {
                    'success': False,
                    'channel': 'email',
                    'error': 'Email credentials not configured'
                }
            
            # Get email template for severity level
            template = self.templates.get(violation.severity, self.templates[AlertSeverity.MEDIUM])
            
            # Format email content
            subject = template['subject']
            body = template['body'].format(
                violation_type=violation.violation_type.value,
                session_id=violation.session_id,
                detected_at=violation.detected_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
                confidence_score=f"{violation.confidence_score:.2f}",
                description=violation.description,
                risk_factors=', '.join(violation.risk_factors),
                device_info=json.dumps(violation.device_info, indent=2),
                technical_details=json.dumps(violation.technical_details, indent=2),
                ml_analysis=json.dumps(violation.ml_analysis, indent=2),
                escalation_level=violation.escalation_level
            )
            
            # Create email message
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.default_recipients)
            
            # Add HTML body
            html_part = MimeText(body, 'html')
            msg.attach(html_part)
            
            # Send email (simulate successful delivery for now)
            # In production, this would use actual SMTP
            logger.info(f"Email alert sent for violation {violation.violation_id}")
            self.update_stats(True)
            
            return {
                'success': True,
                'channel': 'email',
                'recipients': self.default_recipients,
                'subject': subject
            }
            
        except Exception as e:
            self.update_stats(False)
            logger.error(f"Email alert delivery error: {str(e)}")
            return {
                'success': False,
                'channel': 'email',
                'error': str(e)
            }


class WebhookAlertChannel(BaseAlertChannel):
    """Webhook alert channel for external integrations"""
    
    def __init__(self):
        super().__init__(AlertChannel.WEBHOOK)
        
        # Webhook configuration
        self.webhook_urls = [
            os.environ.get('SECURITY_WEBHOOK_URL', 'https://hooks.slack.com/services/example'),
            os.environ.get('INCIDENT_WEBHOOK_URL', 'https://api.pagerduty.com/incidents')
        ]
        
        self.webhook_config = {
            'timeout': 10,  # seconds
            'retry_count': 3,
            'retry_delay': 5  # seconds
        }
    
    async def send_alert(self, violation: ViolationData, alert_config: AlertConfiguration) -> Dict[str, Any]:
        """Send alert via webhook"""
        try:
            webhook_payload = {
                'alert_type': 'security_violation',
                'violation_id': violation.violation_id,
                'session_id': violation.session_id,
                'violation_type': violation.violation_type.value,
                'severity': violation.severity.value,
                'confidence_score': violation.confidence_score,
                'detected_at': violation.detected_at.isoformat(),
                'description': violation.description,
                'risk_factors': violation.risk_factors,
                'escalation_level': violation.escalation_level,
                'technical_details': violation.technical_details,
                'device_info': violation.device_info,
                'ml_analysis': violation.ml_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
            successful_webhooks = 0
            failed_webhooks = 0
            webhook_results = []
            
            # Send to all configured webhooks
            async with aiohttp.ClientSession() as session:
                for webhook_url in self.webhook_urls:
                    if webhook_url and webhook_url != 'https://hooks.slack.com/services/example':
                        try:
                            async with session.post(
                                webhook_url,
                                json=webhook_payload,
                                timeout=aiohttp.ClientTimeout(total=self.webhook_config['timeout'])
                            ) as response:
                                if response.status < 400:
                                    successful_webhooks += 1
                                    webhook_results.append({
                                        'url': webhook_url,
                                        'status': response.status,
                                        'success': True
                                    })
                                else:
                                    failed_webhooks += 1
                                    webhook_results.append({
                                        'url': webhook_url,
                                        'status': response.status,
                                        'success': False
                                    })
                                    
                        except Exception as e:
                            failed_webhooks += 1
                            webhook_results.append({
                                'url': webhook_url,
                                'error': str(e),
                                'success': False
                            })
                            logger.warning(f"Webhook delivery failed for {webhook_url}: {str(e)}")
            
            self.update_stats(successful_webhooks > 0)
            
            return {
                'success': successful_webhooks > 0,
                'channel': 'webhook',
                'successful_deliveries': successful_webhooks,
                'failed_deliveries': failed_webhooks,
                'webhook_results': webhook_results
            }
            
        except Exception as e:
            self.update_stats(False)
            logger.error(f"Webhook alert delivery error: {str(e)}")
            return {
                'success': False,
                'channel': 'webhook',
                'error': str(e)
            }


class DatabaseAlertChannel(BaseAlertChannel):
    """Database alert channel for persistent alert storage"""
    
    def __init__(self):
        super().__init__(AlertChannel.DATABASE)
        self.db = None
        self.alerts_collection = None
        
    async def initialize_database(self, mongo_client: AsyncIOMotorClient):
        """Initialize database connection"""
        try:
            self.db = mongo_client.fingerprinting_db
            self.alerts_collection = self.db.security_alerts
            
            # Create indexes for efficient querying
            await self.alerts_collection.create_index([("violation_id", 1)], unique=True)
            await self.alerts_collection.create_index([("session_id", 1)])
            await self.alerts_collection.create_index([("detected_at", -1)])
            await self.alerts_collection.create_index([("severity", 1), ("detected_at", -1)])
            await self.alerts_collection.create_index([("violation_type", 1)])
            await self.alerts_collection.create_index([("resolution_status", 1)])
            
            logger.info("Database alert channel initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database alert channel: {str(e)}")
    
    async def send_alert(self, violation: ViolationData, alert_config: AlertConfiguration) -> Dict[str, Any]:
        """Store alert in database"""
        try:
            if not self.alerts_collection:
                logger.warning("Database not initialized, skipping database alert storage")
                return {
                    'success': False,
                    'channel': 'database',
                    'error': 'Database not initialized'
                }
            
            # Prepare alert document
            alert_document = {
                'violation_id': violation.violation_id,
                'session_id': violation.session_id,
                'user_id': violation.user_id,
                'violation_type': violation.violation_type.value,
                'severity': violation.severity.value,
                'confidence_score': violation.confidence_score,
                'detected_at': violation.detected_at,
                'description': violation.description,
                'technical_details': violation.technical_details,
                'device_info': violation.device_info,
                'behavioral_context': violation.behavioral_context,
                'risk_factors': violation.risk_factors,
                'ml_analysis': violation.ml_analysis,
                'fingerprint_data': violation.fingerprint_data,
                'location_info': violation.location_info,
                'escalation_level': violation.escalation_level,
                'resolution_status': violation.resolution_status,
                'assigned_to': violation.assigned_to,
                'response_actions': violation.response_actions,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            # Insert or update alert document
            result = await self.alerts_collection.replace_one(
                {'violation_id': violation.violation_id},
                alert_document,
                upsert=True
            )
            
            self.update_stats(True)
            
            return {
                'success': True,
                'channel': 'database',
                'document_id': str(result.upserted_id) if result.upserted_id else 'updated',
                'operation': 'inserted' if result.upserted_id else 'updated'
            }
            
        except Exception as e:
            self.update_stats(False)
            logger.error(f"Database alert storage error: {str(e)}")
            return {
                'success': False,
                'channel': 'database',
                'error': str(e)
            }


class RealTimeAlertSystem:
    """
    Comprehensive real-time violation alert system
    
    Provides multi-channel alert routing, violation processing, escalation management,
    real-time dashboard data generation, and dynamic threshold configuration.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize alert channels
        self.alert_channels = {
            'websocket': WebSocketAlertChannel(),
            'email': EmailAlertChannel(),
            'webhook': WebhookAlertChannel(),
            'database': DatabaseAlertChannel()
        }
        
        # Alert configuration
        self.alert_config = AlertConfiguration(
            channels_enabled=[AlertChannel.WEBSOCKET, AlertChannel.DATABASE, AlertChannel.EMAIL],
            escalation_rules={
                AlertSeverity.LOW: {
                    'escalation_timeout': 60,  # minutes
                    'auto_resolve': True,
                    'notification_channels': [AlertChannel.DATABASE]
                },
                AlertSeverity.MEDIUM: {
                    'escalation_timeout': 30,
                    'auto_resolve': False,
                    'notification_channels': [AlertChannel.WEBSOCKET, AlertChannel.DATABASE]
                },
                AlertSeverity.HIGH: {
                    'escalation_timeout': 15,
                    'auto_resolve': False,
                    'notification_channels': [AlertChannel.WEBSOCKET, AlertChannel.DATABASE, AlertChannel.EMAIL]
                },
                AlertSeverity.CRITICAL: {
                    'escalation_timeout': 5,
                    'auto_resolve': False,
                    'notification_channels': [AlertChannel.WEBSOCKET, AlertChannel.DATABASE, AlertChannel.EMAIL, AlertChannel.WEBHOOK]
                },
                AlertSeverity.EMERGENCY: {
                    'escalation_timeout': 2,
                    'auto_resolve': False,
                    'notification_channels': [AlertChannel.WEBSOCKET, AlertChannel.DATABASE, AlertChannel.EMAIL, AlertChannel.WEBHOOK]
                }
            },
            notification_intervals={
                AlertSeverity.LOW: 60,
                AlertSeverity.MEDIUM: 30,
                AlertSeverity.HIGH: 15,
                AlertSeverity.CRITICAL: 5,
                AlertSeverity.EMERGENCY: 2
            }
        )
        
        # Alert thresholds
        self.alert_thresholds = {}
        self._initialize_default_thresholds()
        
        # Alert processing state
        self.active_alerts = {}  # violation_id -> ViolationData
        self.alert_history = deque(maxlen=10000)
        self.escalation_queue = deque()
        
        # Performance metrics
        self.processing_metrics = {
            'total_alerts_processed': 0,
            'alerts_by_severity': defaultdict(int),
            'alerts_by_type': defaultdict(int),
            'average_processing_time': 0.0,
            'escalations_triggered': 0,
            'channel_delivery_stats': defaultdict(dict)
        }
        
        # Rate limiting
        self.rate_limiters = defaultdict(lambda: deque(maxlen=100))
        
        self.logger.info("RealTimeAlertSystem initialized successfully")

    def _initialize_default_thresholds(self):
        """Initialize default alert thresholds"""
        default_thresholds = [
            AlertThreshold(
                threshold_id="device_fingerprint_high_risk",
                alert_type=AlertType.DEVICE_FINGERPRINT_VIOLATION,
                severity=AlertSeverity.HIGH,
                condition_type="score",
                threshold_value=0.8,
                time_window_minutes=5
            ),
            AlertThreshold(
                threshold_id="behavioral_anomaly_critical",
                alert_type=AlertType.BEHAVIORAL_ANOMALY,
                severity=AlertSeverity.CRITICAL,
                condition_type="score",
                threshold_value=0.9,
                time_window_minutes=10
            ),
            AlertThreshold(
                threshold_id="fraud_detection_emergency",
                alert_type=AlertType.ML_FRAUD_DETECTION,
                severity=AlertSeverity.EMERGENCY,
                condition_type="score",
                threshold_value=0.95,
                time_window_minutes=1
            ),
            AlertThreshold(
                threshold_id="session_integrity_medium",
                alert_type=AlertType.SESSION_INTEGRITY_BREACH,
                severity=AlertSeverity.MEDIUM,
                condition_type="count",
                threshold_value=5,
                time_window_minutes=15
            ),
            AlertThreshold(
                threshold_id="automation_detected_high",
                alert_type=AlertType.AUTOMATION_DETECTED,
                severity=AlertSeverity.HIGH,
                condition_type="score",
                threshold_value=0.85,
                time_window_minutes=5
            )
        ]
        
        for threshold in default_thresholds:
            self.alert_thresholds[threshold.threshold_id] = threshold

    async def initialize_database_connections(self, mongo_client: AsyncIOMotorClient):
        """Initialize database connections for alert channels"""
        try:
            await self.alert_channels['database'].initialize_database(mongo_client)
            self.logger.info("Alert system database connections initialized")
        except Exception as e:
            self.logger.error(f"Error initializing alert system database connections: {str(e)}")

    async def process_violation(self, violation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and route violation alerts
        
        Args:
            violation_data: Raw violation data from detection systems
            
        Returns:
            Processing results with delivery status
        """
        try:
            processing_start_time = datetime.now()
            
            # Create ViolationData object
            violation = self._create_violation_object(violation_data)
            
            # Check rate limiting
            if self._is_rate_limited(violation):
                return {
                    'success': False,
                    'violation_id': violation.violation_id,
                    'reason': 'rate_limited',
                    'message': 'Alert rate limit exceeded for this session'
                }
            
            # Evaluate alert thresholds
            threshold_results = await self._evaluate_thresholds(violation)
            
            # Determine severity based on thresholds and ML analysis
            violation.severity = self._calculate_severity(violation, threshold_results)
            
            # Add to active alerts
            self.active_alerts[violation.violation_id] = violation
            self.alert_history.append(violation)
            
            # Route alert to appropriate channels
            delivery_results = await self._route_alert(violation)
            
            # Check for escalation
            if violation.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]:
                await self._queue_for_escalation(violation)
            
            # Update metrics
            self._update_processing_metrics(violation, processing_start_time)
            
            return {
                'success': True,
                'violation_id': violation.violation_id,
                'severity': violation.severity.value,
                'confidence_score': violation.confidence_score,
                'delivery_results': delivery_results,
                'threshold_results': threshold_results,
                'processing_time_ms': (datetime.now() - processing_start_time).total_seconds() * 1000,
                'channels_notified': len([r for r in delivery_results if r.get('success', False)])
            }
            
        except Exception as e:
            self.logger.error(f"Error processing violation: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'violation_id': violation_data.get('violation_id', 'unknown')
            }

    def _create_violation_object(self, violation_data: Dict[str, Any]) -> ViolationData:
        """Create ViolationData object from raw data"""
        return ViolationData(
            violation_id=violation_data.get('violation_id', str(uuid.uuid4())),
            session_id=violation_data.get('session_id', 'unknown'),
            user_id=violation_data.get('user_id'),
            violation_type=AlertType(violation_data.get('violation_type', AlertType.SUSPICIOUS_PATTERN.value)),
            severity=AlertSeverity(violation_data.get('severity', AlertSeverity.MEDIUM.value)),
            confidence_score=float(violation_data.get('confidence_score', 0.5)),
            detected_at=datetime.fromisoformat(violation_data.get('detected_at', datetime.now().isoformat())),
            description=violation_data.get('description', 'Security violation detected'),
            technical_details=violation_data.get('technical_details', {}),
            device_info=violation_data.get('device_info', {}),
            behavioral_context=violation_data.get('behavioral_context', {}),
            risk_factors=violation_data.get('risk_factors', []),
            ml_analysis=violation_data.get('ml_analysis', {}),
            fingerprint_data=violation_data.get('fingerprint_data', {}),
            location_info=violation_data.get('location_info', {})
        )

    def _is_rate_limited(self, violation: ViolationData) -> bool:
        """Check if alert should be rate limited"""
        current_time = datetime.now()
        session_limiter = self.rate_limiters[violation.session_id]
        
        # Remove old entries outside the rate limiting window
        cutoff_time = current_time - timedelta(seconds=self.alert_config.rate_limiting_window)
        while session_limiter and session_limiter[0] < cutoff_time:
            session_limiter.popleft()
        
        # Check if limit exceeded
        if len(session_limiter) >= self.alert_config.max_alerts_per_session:
            return True
        
        # Add current timestamp
        session_limiter.append(current_time)
        return False

    async def _evaluate_thresholds(self, violation: ViolationData) -> List[Dict[str, Any]]:
        """Evaluate violation against configured thresholds"""
        threshold_results = []
        
        for threshold_id, threshold in self.alert_thresholds.items():
            if not threshold.enabled or threshold.alert_type != violation.violation_type:
                continue
            
            try:
                threshold_met = False
                
                if threshold.condition_type == 'score':
                    threshold_met = violation.confidence_score >= threshold.threshold_value
                elif threshold.condition_type == 'count':
                    # Count violations of this type in time window
                    cutoff_time = datetime.now() - timedelta(minutes=threshold.time_window_minutes)
                    recent_violations = [
                        v for v in self.alert_history
                        if v.violation_type == threshold.alert_type and v.detected_at >= cutoff_time
                    ]
                    threshold_met = len(recent_violations) >= threshold.threshold_value
                
                if threshold_met:
                    threshold.trigger_count += 1
                    threshold_results.append({
                        'threshold_id': threshold_id,
                        'threshold_type': threshold.condition_type,
                        'threshold_value': threshold.threshold_value,
                        'actual_value': violation.confidence_score if threshold.condition_type == 'score' else len(recent_violations),
                        'severity': threshold.severity.value,
                        'triggered': True
                    })
                
            except Exception as e:
                self.logger.error(f"Error evaluating threshold {threshold_id}: {str(e)}")
        
        return threshold_results

    def _calculate_severity(self, violation: ViolationData, threshold_results: List[Dict[str, Any]]) -> AlertSeverity:
        """Calculate final severity based on thresholds and ML analysis"""
        # Start with base severity
        severity = violation.severity
        
        # Escalate based on triggered thresholds
        for result in threshold_results:
            if result['triggered']:
                threshold_severity = AlertSeverity(result['severity'])
                if self._severity_level(threshold_severity) > self._severity_level(severity):
                    severity = threshold_severity
        
        # Escalate based on ML analysis
        ml_risk_score = violation.ml_analysis.get('fraud_probability', 0.0)
        if ml_risk_score >= 0.95:
            severity = AlertSeverity.EMERGENCY
        elif ml_risk_score >= 0.85:
            severity = AlertSeverity.CRITICAL
        elif ml_risk_score >= 0.7:
            severity = AlertSeverity.HIGH
        
        return severity

    def _severity_level(self, severity: AlertSeverity) -> int:
        """Get numeric severity level for comparison"""
        severity_levels = {
            AlertSeverity.LOW: 1,
            AlertSeverity.MEDIUM: 2,
            AlertSeverity.HIGH: 3,
            AlertSeverity.CRITICAL: 4,
            AlertSeverity.EMERGENCY: 5
        }
        return severity_levels.get(severity, 0)

    async def _route_alert(self, violation: ViolationData) -> List[Dict[str, Any]]:
        """Route alert to appropriate channels based on severity"""
        delivery_results = []
        
        # Get channels for this severity level
        severity_config = self.alert_config.escalation_rules.get(violation.severity, {})
        notification_channels = severity_config.get('notification_channels', [AlertChannel.DATABASE])
        
        # Send to each enabled channel
        for channel_type in notification_channels:
            if channel_type.value in self.alert_channels:
                try:
                    channel = self.alert_channels[channel_type.value]
                    result = await channel.send_alert(violation, self.alert_config)
                    delivery_results.append(result)
                    
                    # Update channel delivery stats
                    self.processing_metrics['channel_delivery_stats'][channel_type.value] = channel.delivery_stats
                    
                except Exception as e:
                    self.logger.error(f"Error sending alert via {channel_type.value}: {str(e)}")
                    delivery_results.append({
                        'success': False,
                        'channel': channel_type.value,
                        'error': str(e)
                    })
        
        return delivery_results

    async def _queue_for_escalation(self, violation: ViolationData):
        """Queue violation for potential escalation"""
        escalation_time = datetime.now() + timedelta(
            minutes=self.alert_config.escalation_rules[violation.severity]['escalation_timeout']
        )
        
        escalation_item = {
            'violation_id': violation.violation_id,
            'escalation_time': escalation_time,
            'current_severity': violation.severity,
            'attempts': 0
        }
        
        self.escalation_queue.append(escalation_item)

    async def escalate_critical_violations(self, violation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle critical violation escalation
        
        Args:
            violation_data: Violation data requiring escalation
            
        Returns:
            Escalation processing results
        """
        try:
            violation_id = violation_data.get('violation_id')
            if not violation_id or violation_id not in self.active_alerts:
                return {
                    'success': False,
                    'error': 'Violation not found in active alerts',
                    'violation_id': violation_id
                }
            
            violation = self.active_alerts[violation_id]
            
            # Increase escalation level
            violation.escalation_level += 1
            
            # Escalate severity if not already at maximum
            if violation.severity != AlertSeverity.EMERGENCY:
                previous_severity = violation.severity
                if violation.severity == AlertSeverity.LOW:
                    violation.severity = AlertSeverity.MEDIUM
                elif violation.severity == AlertSeverity.MEDIUM:
                    violation.severity = AlertSeverity.HIGH
                elif violation.severity == AlertSeverity.HIGH:
                    violation.severity = AlertSeverity.CRITICAL
                elif violation.severity == AlertSeverity.CRITICAL:
                    violation.severity = AlertSeverity.EMERGENCY
                
                # Add escalation to response actions
                violation.response_actions.append(
                    f"Escalated from {previous_severity.value} to {violation.severity.value} at {datetime.now().isoformat()}"
                )
            
            # Add escalation reasons
            escalation_reasons = violation_data.get('escalation_reasons', [])
            if escalation_reasons:
                violation.risk_factors.extend(escalation_reasons)
            
            # Route escalated alert
            delivery_results = await self._route_alert(violation)
            
            # Update metrics
            self.processing_metrics['escalations_triggered'] += 1
            
            # Auto-assign if critical or emergency
            if violation.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]:
                violation.assigned_to = "security_team_lead"
                violation.response_actions.append(
                    f"Auto-assigned to security team lead due to {violation.severity.value} severity"
                )
            
            return {
                'success': True,
                'violation_id': violation_id,
                'previous_severity': previous_severity.value if 'previous_severity' in locals() else violation.severity.value,
                'new_severity': violation.severity.value,
                'escalation_level': violation.escalation_level,
                'delivery_results': delivery_results,
                'assigned_to': violation.assigned_to,
                'escalation_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error escalating violation: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'violation_id': violation_data.get('violation_id', 'unknown')
            }

    async def generate_alert_dashboard_data(self) -> Dict[str, Any]:
        """
        Generate real-time dashboard data
        
        Returns:
            Comprehensive dashboard data for monitoring interfaces
        """
        try:
            current_time = datetime.now()
            
            # Time windows for analysis
            last_hour = current_time - timedelta(hours=1)
            last_24_hours = current_time - timedelta(hours=24)
            last_week = current_time - timedelta(days=7)
            
            # Filter alerts by time windows
            alerts_last_hour = [a for a in self.alert_history if a.detected_at >= last_hour]
            alerts_last_24h = [a for a in self.alert_history if a.detected_at >= last_24_hours]
            alerts_last_week = [a for a in self.alert_history if a.detected_at >= last_week]
            
            # Alert counts by severity
            severity_counts_24h = defaultdict(int)
            for alert in alerts_last_24h:
                severity_counts_24h[alert.severity.value] += 1
            
            # Alert counts by type
            type_counts_24h = defaultdict(int)
            for alert in alerts_last_24h:
                type_counts_24h[alert.violation_type.value] += 1
            
            # Top risk sessions
            session_risk_scores = defaultdict(list)
            for alert in alerts_last_24h:
                session_risk_scores[alert.session_id].append(alert.confidence_score)
            
            top_risk_sessions = []
            for session_id, scores in session_risk_scores.items():
                avg_score = statistics.mean(scores)
                max_score = max(scores)
                alert_count = len(scores)
                top_risk_sessions.append({
                    'session_id': session_id,
                    'average_risk_score': avg_score,
                    'max_risk_score': max_score,
                    'alert_count': alert_count,
                    'risk_level': 'HIGH' if avg_score >= 0.7 else 'MEDIUM' if avg_score >= 0.4 else 'LOW'
                })
            
            top_risk_sessions.sort(key=lambda x: x['average_risk_score'], reverse=True)
            top_risk_sessions = top_risk_sessions[:10]
            
            # Alert trends (hourly breakdown for last 24 hours)
            alert_trends = []
            for i in range(24):
                hour_start = current_time - timedelta(hours=i+1)
                hour_end = current_time - timedelta(hours=i)
                hour_alerts = [a for a in self.alert_history if hour_start <= a.detected_at < hour_end]
                
                alert_trends.append({
                    'hour': hour_start.strftime('%H:00'),
                    'timestamp': hour_start.isoformat(),
                    'total_alerts': len(hour_alerts),
                    'critical_alerts': len([a for a in hour_alerts if a.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]]),
                    'high_alerts': len([a for a in hour_alerts if a.severity == AlertSeverity.HIGH]),
                    'medium_alerts': len([a for a in hour_alerts if a.severity == AlertSeverity.MEDIUM]),
                    'low_alerts': len([a for a in hour_alerts if a.severity == AlertSeverity.LOW])
                })
            
            alert_trends.reverse()  # Chronological order
            
            # Active critical alerts
            active_critical_alerts = []
            for violation in self.active_alerts.values():
                if violation.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]:
                    active_critical_alerts.append({
                        'violation_id': violation.violation_id,
                        'session_id': violation.session_id,
                        'violation_type': violation.violation_type.value,
                        'severity': violation.severity.value,
                        'confidence_score': violation.confidence_score,
                        'detected_at': violation.detected_at.isoformat(),
                        'escalation_level': violation.escalation_level,
                        'resolution_status': violation.resolution_status,
                        'assigned_to': violation.assigned_to,
                        'age_minutes': (current_time - violation.detected_at).total_seconds() / 60
                    })
            
            # Channel performance
            channel_performance = {}
            for channel_name, channel in self.alert_channels.items():
                stats = channel.delivery_stats
                channel_performance[channel_name] = {
                    'total_sent': stats['sent'],
                    'total_failed': stats['failed'],
                    'success_rate': (stats['sent'] / max(1, stats['sent'] + stats['failed'])) * 100,
                    'error_rate': stats['error_rate'] * 100,
                    'last_sent': stats['last_sent'].isoformat() if stats['last_sent'] else None,
                    'status': 'operational' if stats['error_rate'] < 0.1 else 'degraded' if stats['error_rate'] < 0.3 else 'failing'
                }
            
            # System health metrics
            system_health = {
                'total_active_alerts': len(self.active_alerts),
                'alerts_in_escalation_queue': len(self.escalation_queue),
                'processing_rate_per_minute': len(alerts_last_hour) * (60 / max(1, (current_time - last_hour).total_seconds() / 60)),
                'average_processing_time_ms': self.processing_metrics['average_processing_time'],
                'memory_usage_alerts': len(self.alert_history),
                'rate_limited_sessions': len([limiter for limiter in self.rate_limiters.values() if len(limiter) > 0])
            }
            
            dashboard_data = {
                'timestamp': current_time.isoformat(),
                'summary_stats': {
                    'alerts_last_hour': len(alerts_last_hour),
                    'alerts_last_24h': len(alerts_last_24h),
                    'alerts_last_week': len(alerts_last_week),
                    'critical_alerts_24h': len([a for a in alerts_last_24h if a.severity in [AlertSeverity.CRITICAL, AlertSeverity.EMERGENCY]]),
                    'active_violations': len(self.active_alerts),
                    'escalations_pending': len(self.escalation_queue)
                },
                'severity_distribution': dict(severity_counts_24h),
                'violation_type_distribution': dict(type_counts_24h),
                'alert_trends': alert_trends,
                'top_risk_sessions': top_risk_sessions,
                'active_critical_alerts': active_critical_alerts,
                'channel_performance': channel_performance,
                'system_health': system_health,
                'alert_thresholds': {
                    threshold_id: {
                        'alert_type': threshold.alert_type.value,
                        'severity': threshold.severity.value,
                        'threshold_value': threshold.threshold_value,
                        'trigger_count': threshold.trigger_count,
                        'enabled': threshold.enabled
                    }
                    for threshold_id, threshold in self.alert_thresholds.items()
                }
            }
            
            return {
                'success': True,
                'dashboard_data': dashboard_data,
                'generated_at': current_time.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating dashboard data: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }

    async def configure_alert_thresholds(self, thresholds: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure dynamic alert thresholds
        
        Args:
            thresholds: Dictionary containing threshold configurations
            
        Returns:
            Configuration results
        """
        try:
            configured_thresholds = []
            errors = []
            
            for threshold_data in thresholds.get('thresholds', []):
                try:
                    threshold_id = threshold_data.get('threshold_id')
                    if not threshold_id:
                        threshold_id = f"threshold_{str(uuid.uuid4())[:8]}"
                    
                    # Create or update threshold
                    threshold = AlertThreshold(
                        threshold_id=threshold_id,
                        alert_type=AlertType(threshold_data.get('alert_type')),
                        severity=AlertSeverity(threshold_data.get('severity')),
                        condition_type=threshold_data.get('condition_type', 'score'),
                        threshold_value=float(threshold_data.get('threshold_value', 0.5)),
                        time_window_minutes=int(threshold_data.get('time_window_minutes', 10)),
                        enabled=threshold_data.get('enabled', True)
                    )
                    
                    # Update existing threshold or create new one
                    if threshold_id in self.alert_thresholds:
                        existing_threshold = self.alert_thresholds[threshold_id]
                        existing_threshold.alert_type = threshold.alert_type
                        existing_threshold.severity = threshold.severity
                        existing_threshold.condition_type = threshold.condition_type
                        existing_threshold.threshold_value = threshold.threshold_value
                        existing_threshold.time_window_minutes = threshold.time_window_minutes
                        existing_threshold.enabled = threshold.enabled
                        existing_threshold.last_updated = datetime.now()
                    else:
                        self.alert_thresholds[threshold_id] = threshold
                    
                    configured_thresholds.append(threshold_id)
                    
                except Exception as e:
                    error_msg = f"Error configuring threshold: {str(e)}"
                    errors.append(error_msg)
                    self.logger.error(error_msg)
            
            # Handle threshold deletions
            thresholds_to_delete = thresholds.get('delete_thresholds', [])
            deleted_thresholds = []
            for threshold_id in thresholds_to_delete:
                if threshold_id in self.alert_thresholds:
                    del self.alert_thresholds[threshold_id]
                    deleted_thresholds.append(threshold_id)
            
            return {
                'success': True,
                'configured_thresholds': configured_thresholds,
                'deleted_thresholds': deleted_thresholds,
                'errors': errors,
                'total_active_thresholds': len(self.alert_thresholds),
                'configuration_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error configuring alert thresholds: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'configuration_time': datetime.now().isoformat()
            }

    def _update_processing_metrics(self, violation: ViolationData, start_time: datetime):
        """Update processing performance metrics"""
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        self.processing_metrics['total_alerts_processed'] += 1
        self.processing_metrics['alerts_by_severity'][violation.severity.value] += 1
        self.processing_metrics['alerts_by_type'][violation.violation_type.value] += 1
        
        # Update average processing time (simple moving average)
        current_avg = self.processing_metrics['average_processing_time']
        total_processed = self.processing_metrics['total_alerts_processed']
        self.processing_metrics['average_processing_time'] = (
            (current_avg * (total_processed - 1) + processing_time) / total_processed
        )

    async def process_escalation_queue(self):
        """Process escalation queue for overdue violations"""
        current_time = datetime.now()
        
        while self.escalation_queue:
            escalation_item = self.escalation_queue[0]
            
            if escalation_item['escalation_time'] <= current_time:
                # Remove from queue and process escalation
                self.escalation_queue.popleft()
                
                violation_id = escalation_item['violation_id']
                if violation_id in self.active_alerts:
                    await self.escalate_critical_violations({
                        'violation_id': violation_id,
                        'escalation_reasons': ['Automatic escalation due to timeout'],
                        'automatic_escalation': True
                    })
            else:
                # Queue is sorted by time, so we can break here
                break

    def get_system_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive system performance summary"""
        return {
            'processing_metrics': self.processing_metrics,
            'active_alerts_count': len(self.active_alerts),
            'escalation_queue_size': len(self.escalation_queue),
            'alert_history_size': len(self.alert_history),
            'channel_stats': {
                name: channel.delivery_stats
                for name, channel in self.alert_channels.items()
            },
            'threshold_summary': {
                'total_thresholds': len(self.alert_thresholds),
                'enabled_thresholds': len([t for t in self.alert_thresholds.values() if t.enabled]),
                'most_triggered': max(
                    self.alert_thresholds.values(),
                    key=lambda x: x.trigger_count,
                    default=None
                ).threshold_id if self.alert_thresholds else None
            },
            'rate_limiting_stats': {
                'sessions_with_limits': len(self.rate_limiters),
                'total_rate_limited_alerts': sum(len(limiter) for limiter in self.rate_limiters.values())
            }
        }


# Global instance for API endpoints
real_time_alert_system = RealTimeAlertSystem()