"""
🔐 MODULE 3.1: WEBSOCKET REAL-TIME MONITORING INTEGRATION
WebSocket Manager - Backend Real-Time Fingerprinting Monitoring

This module implements comprehensive real-time monitoring for device fingerprinting
and session integrity using WebSocket connections for live data streaming.

Key Features:
- Real-time fingerprint updates streaming to connected clients
- Violation alerts broadcasting with immediate notification
- Device analytics streaming with continuous monitoring
- Session integrity monitoring with live validation
- Connection management with automatic reconnection support
- Event-driven architecture with pub/sub patterns

Technical Implementation:
- FastAPI WebSocket integration with connection pooling
- Asynchronous message broadcasting to multiple clients
- JSON-based message protocol with type safety
- Error handling and connection recovery mechanisms
- Memory-efficient event streaming with backpressure control

Author: AI Assistant
Created: 2025
"""

import asyncio
import json
import logging
from typing import Dict, Set, List, Any, Optional, Callable
from datetime import datetime, timedelta
import uuid
from dataclasses import dataclass, asdict
from enum import Enum
import weakref
import threading
from collections import defaultdict, deque

from fastapi import WebSocket, WebSocketDisconnect
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    """WebSocket message types for fingerprinting monitoring"""
    FINGERPRINT_UPDATE = "fingerprint_update"
    VIOLATION_ALERT = "violation_alert"
    DEVICE_ANALYTICS = "device_analytics"
    SESSION_INTEGRITY = "session_integrity"
    CONNECTION_STATUS = "connection_status"
    HEARTBEAT = "heartbeat"
    ERROR = "error"
    SUBSCRIPTION_ACK = "subscription_ack"

@dataclass
class WebSocketMessage:
    """Structured message for WebSocket communication"""
    type: MessageType
    session_id: str
    device_id: Optional[str] = None
    timestamp: str = None
    data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.data is None:
            self.data = {}

@dataclass
class ConnectionInfo:
    """Information about WebSocket connection"""
    websocket: WebSocket
    session_id: str
    device_id: Optional[str] = None
    subscriptions: Set[str] = None
    connected_at: datetime = None
    last_heartbeat: datetime = None
    
    def __post_init__(self):
        if self.subscriptions is None:
            self.subscriptions = set()
        if self.connected_at is None:
            self.connected_at = datetime.now()
        if self.last_heartbeat is None:
            self.last_heartbeat = datetime.now()

class FingerprintingWebSocketManager:
    """Real-time fingerprinting monitoring via WebSocket"""
    
    def __init__(self, mongo_url: str = None):
        # Connection management
        self.active_connections: Dict[str, ConnectionInfo] = {}
        self.session_connections: Dict[str, Set[str]] = defaultdict(set)
        self.device_connections: Dict[str, Set[str]] = defaultdict(set)
        
        # Event broadcasting
        self.event_queues: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.subscribers: Dict[str, Set[str]] = defaultdict(set)
        
        # Configuration
        self.heartbeat_interval = 30  # seconds
        self.max_queue_size = 1000
        self.cleanup_interval = 300  # 5 minutes
        
        # MongoDB connection
        self.mongo_url = mongo_url or os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.mongo_client = None
        self.db = None
        
        # Background tasks
        self._heartbeat_task = None
        self._cleanup_task = None
        self._running = False
        
        logger.info("FingerprintingWebSocketManager initialized")

    async def initialize_database(self):
        """Initialize MongoDB connection"""
        try:
            if not self.mongo_client:
                self.mongo_client = AsyncIOMotorClient(self.mongo_url)
                self.db = self.mongo_client.aptitude_test_db
                logger.info("MongoDB connection established for WebSocket manager")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    async def start_background_tasks(self):
        """Start background maintenance tasks"""
        if not self._running:
            self._running = True
            self._heartbeat_task = asyncio.create_task(self._heartbeat_monitor())
            self._cleanup_task = asyncio.create_task(self._connection_cleanup())
            logger.info("Background tasks started")

    async def stop_background_tasks(self):
        """Stop background maintenance tasks"""
        self._running = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        if self._cleanup_task:
            self._cleanup_task.cancel()
        logger.info("Background tasks stopped")

    async def register_connection(self, websocket: WebSocket, session_id: str, device_id: str = None) -> str:
        """Register a new WebSocket connection"""
        connection_id = str(uuid.uuid4())
        
        connection_info = ConnectionInfo(
            websocket=websocket,
            session_id=session_id,
            device_id=device_id
        )
        
        self.active_connections[connection_id] = connection_info
        self.session_connections[session_id].add(connection_id)
        
        if device_id:
            self.device_connections[device_id].add(connection_id)
        
        # Send connection acknowledgment
        welcome_message = WebSocketMessage(
            type=MessageType.CONNECTION_STATUS,
            session_id=session_id,
            device_id=device_id,
            data={
                "status": "connected",
                "connection_id": connection_id,
                "server_time": datetime.now().isoformat()
            }
        )
        
        await self._send_message(websocket, welcome_message)
        
        logger.info(f"WebSocket connection registered: {connection_id} for session {session_id}")
        return connection_id

    async def unregister_connection(self, connection_id: str):
        """Unregister a WebSocket connection"""
        if connection_id in self.active_connections:
            connection_info = self.active_connections[connection_id]
            session_id = connection_info.session_id
            device_id = connection_info.device_id
            
            # Remove from tracking
            del self.active_connections[connection_id]
            self.session_connections[session_id].discard(connection_id)
            
            if device_id:
                self.device_connections[device_id].discard(connection_id)
            
            # Clean up subscriptions
            for subscription_key in list(self.subscribers.keys()):
                self.subscribers[subscription_key].discard(connection_id)
            
            logger.info(f"WebSocket connection unregistered: {connection_id}")

    async def handle_fingerprint_updates(self, websocket: WebSocket, session_id: str):
        """Handle real-time fingerprint updates"""
        try:
            connection_id = await self.register_connection(websocket, session_id)
            
            # Subscribe to fingerprint updates for this session
            subscription_key = f"fingerprint_updates:{session_id}"
            self.subscribers[subscription_key].add(connection_id)
            
            # Send subscription acknowledgment
            ack_message = WebSocketMessage(
                type=MessageType.SUBSCRIPTION_ACK,
                session_id=session_id,
                data={
                    "subscription": "fingerprint_updates",
                    "status": "active"
                }
            )
            await self._send_message(websocket, ack_message)
            
            # Listen for incoming messages and handle disconnection
            while True:
                try:
                    # Wait for client messages or heartbeat
                    message = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
                    client_data = json.loads(message)
                    
                    # Process client fingerprint data
                    if client_data.get('type') == 'fingerprint_data':
                        await self._process_fingerprint_data(session_id, client_data.get('data', {}))
                    
                    elif client_data.get('type') == 'heartbeat':
                        # Update last heartbeat
                        if connection_id in self.active_connections:
                            self.active_connections[connection_id].last_heartbeat = datetime.now()
                        
                        # Send heartbeat response
                        heartbeat_response = WebSocketMessage(
                            type=MessageType.HEARTBEAT,
                            session_id=session_id,
                            data={"status": "alive", "server_time": datetime.now().isoformat()}
                        )
                        await self._send_message(websocket, heartbeat_response)
                    
                except asyncio.TimeoutError:
                    # Send heartbeat to keep connection alive
                    heartbeat_message = WebSocketMessage(
                        type=MessageType.HEARTBEAT,
                        session_id=session_id,
                        data={"server_time": datetime.now().isoformat()}
                    )
                    await self._send_message(websocket, heartbeat_message)
                
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected for session {session_id}")
        except Exception as e:
            logger.error(f"Error in fingerprint updates handler: {e}")
            error_message = WebSocketMessage(
                type=MessageType.ERROR,
                session_id=session_id,
                data={"error": str(e)}
            )
            try:
                await self._send_message(websocket, error_message)
            except:
                pass
        finally:
            if 'connection_id' in locals():
                await self.unregister_connection(connection_id)

    async def broadcast_violation_alerts(self, violation_data: Dict[str, Any]):
        """Broadcast violations to connected clients"""
        try:
            session_id = violation_data.get('session_id')
            device_id = violation_data.get('device_id')
            
            # Create violation alert message
            alert_message = WebSocketMessage(
                type=MessageType.VIOLATION_ALERT,
                session_id=session_id,
                device_id=device_id,
                data={
                    "violation_type": violation_data.get('violation_type'),
                    "severity": violation_data.get('severity', 'medium'),
                    "description": violation_data.get('description'),
                    "risk_score": violation_data.get('risk_score', 0.0),
                    "detected_at": violation_data.get('detected_at', datetime.now().isoformat()),
                    "recommendation": violation_data.get('recommendation'),
                    "evidence": violation_data.get('evidence', {})
                }
            )
            
            # Determine target connections
            target_connections = set()
            
            # Add session-specific connections
            if session_id:
                target_connections.update(self.session_connections.get(session_id, set()))
            
            # Add device-specific connections
            if device_id:
                target_connections.update(self.device_connections.get(device_id, set()))
            
            # Add subscribers to violation alerts
            violation_subscription_key = "violation_alerts"
            target_connections.update(self.subscribers.get(violation_subscription_key, set()))
            
            # Broadcast to all target connections
            broadcast_tasks = []
            for connection_id in target_connections:
                if connection_id in self.active_connections:
                    connection_info = self.active_connections[connection_id]
                    task = asyncio.create_task(
                        self._send_message(connection_info.websocket, alert_message)
                    )
                    broadcast_tasks.append(task)
            
            # Wait for all broadcasts to complete
            if broadcast_tasks:
                results = await asyncio.gather(*broadcast_tasks, return_exceptions=True)
                successful_broadcasts = sum(1 for result in results if not isinstance(result, Exception))
                
                logger.info(f"Violation alert broadcasted to {successful_broadcasts}/{len(broadcast_tasks)} connections")
                
                # Store violation in database
                await self._store_violation_alert(violation_data)
            
        except Exception as e:
            logger.error(f"Error broadcasting violation alert: {e}")

    async def stream_device_analytics(self, websocket: WebSocket, device_id: str):
        """Stream real-time device analytics"""
        try:
            session_id = f"analytics_{device_id}"
            connection_id = await self.register_connection(websocket, session_id, device_id)
            
            # Subscribe to device analytics
            subscription_key = f"device_analytics:{device_id}"
            self.subscribers[subscription_key].add(connection_id)
            
            # Send subscription acknowledgment
            ack_message = WebSocketMessage(
                type=MessageType.SUBSCRIPTION_ACK,
                session_id=session_id,
                device_id=device_id,
                data={
                    "subscription": "device_analytics",
                    "status": "active"
                }
            )
            await self._send_message(websocket, ack_message)
            
            # Continuously stream analytics data
            analytics_interval = 5  # seconds
            
            while True:
                try:
                    # Generate analytics data
                    analytics_data = await self._generate_device_analytics(device_id)
                    
                    analytics_message = WebSocketMessage(
                        type=MessageType.DEVICE_ANALYTICS,
                        session_id=session_id,
                        device_id=device_id,
                        data=analytics_data
                    )
                    
                    await self._send_message(websocket, analytics_message)
                    
                    # Wait for next analytics cycle
                    await asyncio.sleep(analytics_interval)
                
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    logger.error(f"Error streaming device analytics: {e}")
                    break
        
        except Exception as e:
            logger.error(f"Error in device analytics stream: {e}")
        finally:
            if 'connection_id' in locals():
                await self.unregister_connection(connection_id)

    async def monitor_session_integrity(self, websocket: WebSocket, session_id: str):
        """Monitor session integrity in real-time"""
        try:
            connection_id = await self.register_connection(websocket, session_id)
            
            # Subscribe to session integrity monitoring
            subscription_key = f"session_integrity:{session_id}"
            self.subscribers[subscription_key].add(connection_id)
            
            # Send subscription acknowledgment
            ack_message = WebSocketMessage(
                type=MessageType.SUBSCRIPTION_ACK,
                session_id=session_id,
                data={
                    "subscription": "session_integrity",
                    "status": "active"
                }
            )
            await self._send_message(websocket, ack_message)
            
            # Monitor session integrity
            integrity_check_interval = 10  # seconds
            
            while True:
                try:
                    # Perform integrity checks
                    integrity_data = await self._check_session_integrity(session_id)
                    
                    integrity_message = WebSocketMessage(
                        type=MessageType.SESSION_INTEGRITY,
                        session_id=session_id,
                        data=integrity_data
                    )
                    
                    await self._send_message(websocket, integrity_message)
                    
                    # Check for integrity violations
                    if integrity_data.get('violations'):
                        # Broadcast violation alerts
                        for violation in integrity_data['violations']:
                            violation['session_id'] = session_id
                            await self.broadcast_violation_alerts(violation)
                    
                    # Wait for next integrity check
                    await asyncio.sleep(integrity_check_interval)
                
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    logger.error(f"Error monitoring session integrity: {e}")
                    break
        
        except Exception as e:
            logger.error(f"Error in session integrity monitor: {e}")
        finally:
            if 'connection_id' in locals():
                await self.unregister_connection(connection_id)

    # Helper Methods
    
    async def _send_message(self, websocket: WebSocket, message: WebSocketMessage):
        """Send message to WebSocket client"""
        try:
            message_dict = asdict(message)
            message_dict['type'] = message.type.value
            await websocket.send_text(json.dumps(message_dict))
        except Exception as e:
            logger.error(f"Failed to send WebSocket message: {e}")
            raise

    async def _process_fingerprint_data(self, session_id: str, fingerprint_data: Dict[str, Any]):
        """Process incoming fingerprint data"""
        try:
            # Store fingerprint data
            await self.initialize_database()
            
            fingerprint_document = {
                "session_id": session_id,
                "fingerprint_data": fingerprint_data,
                "timestamp": datetime.now(),
                "processed_at": datetime.now().isoformat()
            }
            
            await self.db.realtime_fingerprint_updates.insert_one(fingerprint_document)
            
            # Broadcast update to subscribers
            update_message = WebSocketMessage(
                type=MessageType.FINGERPRINT_UPDATE,
                session_id=session_id,
                data={
                    "status": "processed",
                    "timestamp": datetime.now().isoformat(),
                    "data_size": len(json.dumps(fingerprint_data))
                }
            )
            
            # Broadcast to session subscribers
            subscription_key = f"fingerprint_updates:{session_id}"
            await self._broadcast_to_subscribers(subscription_key, update_message)
            
            logger.info(f"Processed fingerprint data for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error processing fingerprint data: {e}")

    async def _generate_device_analytics(self, device_id: str) -> Dict[str, Any]:
        """Generate real-time device analytics"""
        try:
            # Fetch recent device data from database
            await self.initialize_database()
            
            # Query recent fingerprint data
            recent_data = await self.db.realtime_fingerprint_updates.find({
                "fingerprint_data.device_id": device_id
            }).sort("timestamp", -1).limit(10).to_list(None)
            
            # Generate analytics
            analytics = {
                "device_id": device_id,
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "total_updates": len(recent_data),
                    "update_frequency": len(recent_data) / 60,  # updates per minute
                    "last_update": recent_data[0]["timestamp"].isoformat() if recent_data else None,
                    "data_consistency": self._calculate_consistency_score(recent_data),
                    "risk_indicators": self._extract_risk_indicators(recent_data)
                },
                "trends": {
                    "update_pattern": "consistent" if len(recent_data) > 5 else "irregular",
                    "device_stability": self._assess_device_stability(recent_data),
                    "anomaly_count": self._count_anomalies(recent_data)
                }
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating device analytics: {e}")
            return {
                "device_id": device_id,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    async def _check_session_integrity(self, session_id: str) -> Dict[str, Any]:
        """Check session integrity and detect violations"""
        try:
            # Fetch session data
            await self.initialize_database()
            
            # Query session data
            session_data = await self.db.realtime_fingerprint_updates.find({
                "session_id": session_id
            }).sort("timestamp", -1).limit(20).to_list(None)
            
            violations = []
            integrity_score = 1.0
            
            if len(session_data) >= 2:
                # Check for device consistency
                device_ids = set()
                ip_addresses = set()
                user_agents = set()
                
                for data in session_data:
                    fingerprint = data.get("fingerprint_data", {})
                    device_ids.add(fingerprint.get("device_id"))
                    ip_addresses.add(fingerprint.get("ip_address"))
                    user_agents.add(fingerprint.get("user_agent"))
                
                # Detect inconsistencies
                if len(device_ids) > 1:
                    violations.append({
                        "type": "device_inconsistency",
                        "severity": "high",
                        "description": f"Multiple device IDs detected: {list(device_ids)}",
                        "detected_at": datetime.now().isoformat()
                    })
                    integrity_score -= 0.3
                
                if len(ip_addresses) > 2:
                    violations.append({
                        "type": "ip_inconsistency", 
                        "severity": "medium",
                        "description": f"Multiple IP addresses detected: {list(ip_addresses)}",
                        "detected_at": datetime.now().isoformat()
                    })
                    integrity_score -= 0.2
                
                if len(user_agents) > 1:
                    violations.append({
                        "type": "user_agent_inconsistency",
                        "severity": "medium", 
                        "description": f"Multiple user agents detected",
                        "detected_at": datetime.now().isoformat()
                    })
                    integrity_score -= 0.1
            
            integrity_result = {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "integrity_score": max(0.0, integrity_score),
                "status": "healthy" if integrity_score > 0.7 else "suspicious" if integrity_score > 0.4 else "compromised",
                "violations": violations,
                "data_points_analyzed": len(session_data)
            }
            
            return integrity_result
            
        except Exception as e:
            logger.error(f"Error checking session integrity: {e}")
            return {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "integrity_score": 0.0,
                "status": "error"
            }

    async def _broadcast_to_subscribers(self, subscription_key: str, message: WebSocketMessage):
        """Broadcast message to all subscribers"""
        subscribers = self.subscribers.get(subscription_key, set())
        
        broadcast_tasks = []
        for connection_id in subscribers:
            if connection_id in self.active_connections:
                connection_info = self.active_connections[connection_id]
                task = asyncio.create_task(
                    self._send_message(connection_info.websocket, message)
                )
                broadcast_tasks.append(task)
        
        if broadcast_tasks:
            await asyncio.gather(*broadcast_tasks, return_exceptions=True)

    async def _store_violation_alert(self, violation_data: Dict[str, Any]):
        """Store violation alert in database"""
        try:
            await self.initialize_database()
            
            violation_document = {
                **violation_data,
                "stored_at": datetime.now(),
                "alert_id": str(uuid.uuid4())
            }
            
            await self.db.websocket_violation_alerts.insert_one(violation_document)
            
        except Exception as e:
            logger.error(f"Error storing violation alert: {e}")

    def _calculate_consistency_score(self, data: List[Dict]) -> float:
        """Calculate data consistency score"""
        if not data:
            return 0.0
        
        # Simple consistency calculation based on data similarity
        consistency_score = 1.0 - (len(set(str(d.get("fingerprint_data", {})) for d in data)) / len(data))
        return round(consistency_score, 3)

    def _extract_risk_indicators(self, data: List[Dict]) -> List[str]:
        """Extract risk indicators from data"""
        indicators = []
        
        if not data:
            return indicators
        
        # Check for suspicious patterns
        recent_data = data[:5]  # Last 5 updates
        
        # Check for rapid changes
        if len(set(str(d.get("fingerprint_data", {})) for d in recent_data)) > 3:
            indicators.append("rapid_fingerprint_changes")
        
        # Check for missing standard fields
        required_fields = ["user_agent", "screen_resolution", "timezone"]
        for field in required_fields:
            if not any(d.get("fingerprint_data", {}).get(field) for d in recent_data):
                indicators.append(f"missing_{field}")
        
        return indicators

    def _assess_device_stability(self, data: List[Dict]) -> str:
        """Assess device stability based on data"""
        if len(data) < 5:
            return "insufficient_data"
        
        # Check for consistency in core device characteristics
        core_fields = ["user_agent", "screen_resolution", "timezone", "language"]
        stable_count = 0
        
        for field in core_fields:
            values = set(d.get("fingerprint_data", {}).get(field) for d in data)
            if len(values) <= 1:  # Consistent values
                stable_count += 1
        
        stability_ratio = stable_count / len(core_fields)
        
        if stability_ratio > 0.8:
            return "stable"
        elif stability_ratio > 0.6:
            return "moderate"
        else:
            return "unstable"

    def _count_anomalies(self, data: List[Dict]) -> int:
        """Count anomalies in the data"""
        anomalies = 0
        
        for d in data:
            fingerprint = d.get("fingerprint_data", {})
            
            # Check for common anomaly indicators
            if not fingerprint.get("user_agent"):
                anomalies += 1
            
            if fingerprint.get("plugins_count", 0) == 0:
                anomalies += 1
            
            if not fingerprint.get("screen_resolution"):
                anomalies += 1
        
        return anomalies

    async def _heartbeat_monitor(self):
        """Background task to monitor connection health"""
        while self._running:
            try:
                current_time = datetime.now()
                stale_connections = []
                
                # Find stale connections
                for connection_id, connection_info in self.active_connections.items():
                    if current_time - connection_info.last_heartbeat > timedelta(seconds=self.heartbeat_interval * 2):
                        stale_connections.append(connection_id)
                
                # Clean up stale connections
                for connection_id in stale_connections:
                    logger.warning(f"Cleaning up stale connection: {connection_id}")
                    await self.unregister_connection(connection_id)
                
                # Send heartbeat to active connections
                heartbeat_tasks = []
                for connection_info in self.active_connections.values():
                    heartbeat_message = WebSocketMessage(
                        type=MessageType.HEARTBEAT,
                        session_id=connection_info.session_id,
                        data={"server_time": datetime.now().isoformat()}
                    )
                    task = asyncio.create_task(
                        self._send_message(connection_info.websocket, heartbeat_message)
                    )
                    heartbeat_tasks.append(task)
                
                if heartbeat_tasks:
                    await asyncio.gather(*heartbeat_tasks, return_exceptions=True)
                
                await asyncio.sleep(self.heartbeat_interval)
                
            except Exception as e:
                logger.error(f"Error in heartbeat monitor: {e}")
                await asyncio.sleep(5)

    async def _connection_cleanup(self):
        """Background task to clean up resources"""
        while self._running:
            try:
                # Clean up empty subscription sets
                empty_subscriptions = [key for key, subscribers in self.subscribers.items() if not subscribers]
                for key in empty_subscriptions:
                    del self.subscribers[key]
                
                # Clean up empty connection sets
                empty_sessions = [session_id for session_id, connections in self.session_connections.items() if not connections]
                for session_id in empty_sessions:
                    del self.session_connections[session_id]
                
                empty_devices = [device_id for device_id, connections in self.device_connections.items() if not connections]
                for device_id in empty_devices:
                    del self.device_connections[device_id]
                
                # Trim event queues
                for queue in self.event_queues.values():
                    while len(queue) > self.max_queue_size:
                        queue.popleft()
                
                logger.debug(f"Connection cleanup completed. Active connections: {len(self.active_connections)}")
                
                await asyncio.sleep(self.cleanup_interval)
                
            except Exception as e:
                logger.error(f"Error in connection cleanup: {e}")
                await asyncio.sleep(30)

    async def get_connection_stats(self) -> Dict[str, Any]:
        """Get current connection statistics"""
        return {
            "active_connections": len(self.active_connections),
            "session_connections": len(self.session_connections),
            "device_connections": len(self.device_connections),
            "total_subscriptions": sum(len(subs) for subs in self.subscribers.values()),
            "uptime": datetime.now().isoformat(),
            "background_tasks_running": self._running
        }

# Global WebSocket manager instance
websocket_manager = FingerprintingWebSocketManager()