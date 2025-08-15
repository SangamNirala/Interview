/**
 * 🔐 MODULE 3.1: WEBSOCKET REAL-TIME MONITORING INTEGRATION
 * WebSocketManager.js - Frontend Real-Time Fingerprinting Monitoring Client
 * 
 * This module implements comprehensive real-time monitoring client for device fingerprinting
 * and session integrity using WebSocket connections for live data streaming.
 * 
 * Key Features:
 * - Real-time fingerprint data streaming to backend
 * - Violation alerts subscription with immediate notifications
 * - Device metrics streaming with continuous monitoring
 * - Session integrity monitoring with live validation
 * - Automatic reconnection with exponential backoff
 * - Event-driven architecture with callback support
 * 
 * Technical Implementation:
 * - Native WebSocket API with JSON message protocol
 * - Promise-based connection management
 * - Event handler registration and management
 * - Automatic heartbeat and connection recovery
 * - Memory-efficient event processing
 * 
 * Author: AI Assistant
 * Created: 2025
 */

class FingerprintingWebSocketClient {
    constructor(sessionId, options = {}) {
        this.sessionId = sessionId;
        this.deviceId = options.deviceId || this.generateDeviceId();
        
        // WebSocket configuration
        this.ws = null;
        this.wsUrl = this.constructWebSocketUrl(options.backendUrl);
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = options.maxReconnectAttempts || 10;
        this.reconnectInterval = options.reconnectInterval || 1000; // Start with 1 second
        this.maxReconnectInterval = options.maxReconnectInterval || 30000; // Max 30 seconds
        
        // Connection state
        this.isConnected = false;
        this.isReconnecting = false;
        this.connectionId = null;
        this.lastMessageTime = null;
        
        // Event handling
        this.eventHandlers = new Map();
        this.subscriptions = new Set();
        
        // Heartbeat configuration
        this.heartbeatInterval = options.heartbeatInterval || 30000; // 30 seconds
        this.heartbeatTimer = null;
        this.lastHeartbeat = null;
        
        // Message queue for offline scenarios
        this.messageQueue = [];
        this.maxQueueSize = options.maxQueueSize || 100;
        
        // Logging
        this.logger = console;
        this.debugMode = options.debug || false;
        
        this.log('info', 'FingerprintingWebSocketClient initialized', {
            sessionId: this.sessionId,
            deviceId: this.deviceId
        });
    }
    
    /**
     * Generate unique device ID for fingerprinting
     */
    generateDeviceId() {
        // Create device ID based on browser characteristics
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        ctx.textBaseline = 'top';
        ctx.font = '14px Arial';
        ctx.fillText('Device fingerprinting', 2, 2);
        
        const canvasFingerprint = canvas.toDataURL().slice(22, 32);
        const screenFingerprint = `${screen.width}x${screen.height}x${screen.colorDepth}`;
        const timezoneFingerprint = Intl.DateTimeFormat().resolvedOptions().timeZone;
        
        const deviceString = `${navigator.userAgent}${canvasFingerprint}${screenFingerprint}${timezoneFingerprint}`;
        
        // Simple hash function
        let hash = 0;
        for (let i = 0; i < deviceString.length; i++) {
            const char = deviceString.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        
        return `device_${Math.abs(hash).toString(36)}`;
    }
    
    /**
     * Construct WebSocket URL based on environment
     */
    constructWebSocketUrl(backendUrl) {
        // Use environment variable or default URL
        let baseUrl = backendUrl;
        
        if (!baseUrl) {
            // Try to get from React environment
            if (typeof process !== 'undefined' && process.env) {
                baseUrl = process.env.REACT_APP_BACKEND_URL;
            } else if (typeof import !== 'undefined' && import.meta && import.meta.env) {
                baseUrl = import.meta.env.REACT_APP_BACKEND_URL;
            }
        }
        
        if (!baseUrl) {
            baseUrl = window.location.origin;
        }
        
        // Convert HTTP(S) to WS(S)
        const wsUrl = baseUrl.replace(/^https?:/, 'wss:').replace(/^http:/, 'ws:');
        return `${wsUrl}/ws/fingerprinting`;
    }
    
    /**
     * Connect to WebSocket server
     */
    async connect() {
        if (this.isConnected || this.isReconnecting) {
            this.log('warn', 'Connection already established or in progress');
            return;
        }
        
        try {
            this.log('info', 'Connecting to WebSocket server', { url: this.wsUrl });
            
            this.ws = new WebSocket(`${this.wsUrl}/${this.sessionId}`);
            
            // Set up event listeners
            this.ws.onopen = (event) => this.handleOpen(event);
            this.ws.onmessage = (event) => this.handleMessage(event);
            this.ws.onclose = (event) => this.handleClose(event);
            this.ws.onerror = (event) => this.handleError(event);
            
            // Wait for connection to be established
            await this.waitForConnection();
            
        } catch (error) {
            this.log('error', 'Failed to establish WebSocket connection', error);
            await this.handleReconnection();
            throw error;
        }
    }
    
    /**
     * Wait for WebSocket connection to be established
     */
    waitForConnection(timeout = 10000) {
        return new Promise((resolve, reject) => {
            const timer = setTimeout(() => {
                reject(new Error('WebSocket connection timeout'));
            }, timeout);
            
            const checkConnection = () => {
                if (this.isConnected) {
                    clearTimeout(timer);
                    resolve();
                } else if (this.ws && this.ws.readyState === WebSocket.CLOSED) {
                    clearTimeout(timer);
                    reject(new Error('WebSocket connection failed'));
                } else {
                    setTimeout(checkConnection, 100);
                }
            };
            
            checkConnection();
        });
    }
    
    /**
     * Disconnect from WebSocket server
     */
    disconnect() {
        this.log('info', 'Disconnecting from WebSocket server');
        
        // Stop heartbeat
        this.stopHeartbeat();
        
        // Close connection
        if (this.ws) {
            this.ws.onclose = null; // Prevent reconnection
            this.ws.close(1000, 'Client disconnect');
            this.ws = null;
        }
        
        this.isConnected = false;
        this.isReconnecting = false;
        this.connectionId = null;
        
        // Clear subscriptions
        this.subscriptions.clear();
        
        // Trigger disconnection event
        this.triggerEvent('disconnected', {
            reason: 'client_disconnect',
            timestamp: new Date().toISOString()
        });
    }
    
    /**
     * Start real-time fingerprinting monitoring
     */
    async startRealTimeMonitoring() {
        try {
            this.log('info', 'Starting real-time fingerprinting monitoring');
            
            // Ensure WebSocket connection
            if (!this.isConnected) {
                await this.connect();
            }
            
            // Subscribe to fingerprint updates
            await this.subscribe('fingerprint_updates');
            
            // Start collecting and streaming fingerprint data
            await this.startFingerprintStreaming();
            
            this.log('info', 'Real-time monitoring started successfully');
            
        } catch (error) {
            this.log('error', 'Failed to start real-time monitoring', error);
            throw error;
        }
    }
    
    /**
     * Subscribe to violation alerts
     */
    async subscribeToViolationAlerts(callback) {
        try {
            this.log('info', 'Subscribing to violation alerts');
            
            // Register callback
            this.registerEventHandler('violation_alert', callback);
            
            // Subscribe to violation alerts on server
            await this.subscribe('violation_alerts');
            
            // Send subscription request
            const subscriptionMessage = {
                type: 'subscribe',
                subscription: 'violation_alerts',
                session_id: this.sessionId,
                timestamp: new Date().toISOString()
            };
            
            await this.sendMessage(subscriptionMessage);
            
            this.log('info', 'Successfully subscribed to violation alerts');
            
        } catch (error) {
            this.log('error', 'Failed to subscribe to violation alerts', error);
            throw error;
        }
    }
    
    /**
     * Stream real-time device metrics
     */
    async streamDeviceMetrics(callback) {
        try {
            this.log('info', 'Starting device metrics streaming');
            
            // Register callback for device analytics
            this.registerEventHandler('device_analytics', callback);
            
            // Subscribe to device analytics
            await this.subscribe('device_analytics');
            
            // Send streaming request
            const streamingMessage = {
                type: 'start_device_streaming',
                device_id: this.deviceId,
                session_id: this.sessionId,
                timestamp: new Date().toISOString()
            };
            
            await this.sendMessage(streamingMessage);
            
            this.log('info', 'Device metrics streaming started');
            
        } catch (error) {
            this.log('error', 'Failed to start device metrics streaming', error);
            throw error;
        }
    }
    
    /**
     * Monitor session integrity
     */
    async monitorSessionIntegrity(callback) {
        try {
            this.log('info', 'Starting session integrity monitoring');
            
            // Register callback for session integrity updates
            this.registerEventHandler('session_integrity', callback);
            
            // Subscribe to session integrity monitoring
            await this.subscribe('session_integrity');
            
            // Send monitoring request
            const monitoringMessage = {
                type: 'start_session_monitoring',
                session_id: this.sessionId,
                timestamp: new Date().toISOString()
            };
            
            await this.sendMessage(monitoringMessage);
            
            this.log('info', 'Session integrity monitoring started');
            
        } catch (error) {
            this.log('error', 'Failed to start session integrity monitoring', error);
            throw error;
        }
    }
    
    /**
     * Send fingerprint data to server
     */
    async sendFingerprintData(fingerprintData) {
        try {
            const message = {
                type: 'fingerprint_data',
                session_id: this.sessionId,
                device_id: this.deviceId,
                data: fingerprintData,
                timestamp: new Date().toISOString()
            };
            
            await this.sendMessage(message);
            
            this.log('debug', 'Fingerprint data sent', {
                dataSize: JSON.stringify(fingerprintData).length
            });
            
        } catch (error) {
            this.log('error', 'Failed to send fingerprint data', error);
            throw error;
        }
    }
    
    /**
     * Register event handler
     */
    registerEventHandler(eventType, callback) {
        if (!this.eventHandlers.has(eventType)) {
            this.eventHandlers.set(eventType, []);
        }
        
        this.eventHandlers.get(eventType).push(callback);
        
        this.log('debug', `Event handler registered for ${eventType}`);
    }
    
    /**
     * Unregister event handler
     */
    unregisterEventHandler(eventType, callback) {
        if (this.eventHandlers.has(eventType)) {
            const handlers = this.eventHandlers.get(eventType);
            const index = handlers.indexOf(callback);
            if (index > -1) {
                handlers.splice(index, 1);
                this.log('debug', `Event handler unregistered for ${eventType}`);
            }
        }
    }
    
    /**
     * Send message to WebSocket server
     */
    async sendMessage(message) {
        if (!this.isConnected || !this.ws || this.ws.readyState !== WebSocket.OPEN) {
            // Queue message if not connected
            if (this.messageQueue.length < this.maxQueueSize) {
                this.messageQueue.push(message);
                this.log('warn', 'Message queued - WebSocket not connected', message);
            } else {
                this.log('error', 'Message queue full - dropping message', message);
            }
            return;
        }
        
        try {
            const messageString = JSON.stringify(message);
            this.ws.send(messageString);
            this.lastMessageTime = new Date();
            
            this.log('debug', 'Message sent', message);
            
        } catch (error) {
            this.log('error', 'Failed to send message', error);
            throw error;
        }
    }
    
    // Event Handlers
    
    handleOpen(event) {
        this.log('info', 'WebSocket connection opened');
        this.isConnected = true;
        this.isReconnecting = false;
        this.reconnectAttempts = 0;
        this.lastHeartbeat = new Date();
        
        // Start heartbeat
        this.startHeartbeat();
        
        // Send queued messages
        this.sendQueuedMessages();
        
        // Trigger connection event
        this.triggerEvent('connected', {
            connectionId: this.connectionId,
            timestamp: new Date().toISOString()
        });
    }
    
    handleMessage(event) {
        try {
            const message = JSON.parse(event.data);
            this.lastMessageTime = new Date();
            
            this.log('debug', 'Message received', message);
            
            // Handle different message types
            switch (message.type) {
                case 'connection_status':
                    this.handleConnectionStatus(message);
                    break;
                    
                case 'subscription_ack':
                    this.handleSubscriptionAck(message);
                    break;
                    
                case 'fingerprint_update':
                    this.triggerEvent('fingerprint_update', message.data);
                    break;
                    
                case 'violation_alert':
                    this.handleViolationAlert(message);
                    break;
                    
                case 'device_analytics':
                    this.triggerEvent('device_analytics', message.data);
                    break;
                    
                case 'session_integrity':
                    this.triggerEvent('session_integrity', message.data);
                    break;
                    
                case 'heartbeat':
                    this.handleHeartbeat(message);
                    break;
                    
                case 'error':
                    this.handleServerError(message);
                    break;
                    
                default:
                    this.log('warn', 'Unknown message type received', message);
            }
            
        } catch (error) {
            this.log('error', 'Failed to parse WebSocket message', error);
        }
    }
    
    handleClose(event) {
        this.log('info', 'WebSocket connection closed', {
            code: event.code,
            reason: event.reason,
            wasClean: event.wasClean
        });
        
        this.isConnected = false;
        this.connectionId = null;
        
        // Stop heartbeat
        this.stopHeartbeat();
        
        // Trigger disconnection event
        this.triggerEvent('disconnected', {
            code: event.code,
            reason: event.reason,
            wasClean: event.wasClean,
            timestamp: new Date().toISOString()
        });
        
        // Attempt reconnection if not intentionally closed
        if (event.code !== 1000 && !this.isReconnecting) {
            this.handleReconnection();
        }
    }
    
    handleError(event) {
        this.log('error', 'WebSocket error', event);
        
        this.triggerEvent('error', {
            error: event.error || 'WebSocket error',
            timestamp: new Date().toISOString()
        });
    }
    
    // Message Type Handlers
    
    handleConnectionStatus(message) {
        if (message.data && message.data.connection_id) {
            this.connectionId = message.data.connection_id;
            this.log('info', 'Connection established', {
                connectionId: this.connectionId
            });
        }
    }
    
    handleSubscriptionAck(message) {
        if (message.data && message.data.subscription) {
            this.subscriptions.add(message.data.subscription);
            this.log('info', `Subscription confirmed: ${message.data.subscription}`);
            
            this.triggerEvent('subscription_confirmed', {
                subscription: message.data.subscription,
                status: message.data.status
            });
        }
    }
    
    handleViolationAlert(message) {
        this.log('warn', 'Violation alert received', message.data);
        
        // Trigger violation alert event
        this.triggerEvent('violation_alert', {
            ...message.data,
            sessionId: message.session_id,
            deviceId: message.device_id
        });
        
        // Show browser notification if permission granted
        this.showNotification('Security Alert', message.data.description);
    }
    
    handleHeartbeat(message) {
        this.lastHeartbeat = new Date();
        this.log('debug', 'Heartbeat received');
        
        // Respond to heartbeat
        const heartbeatResponse = {
            type: 'heartbeat',
            session_id: this.sessionId,
            timestamp: new Date().toISOString()
        };
        
        this.sendMessage(heartbeatResponse);
    }
    
    handleServerError(message) {
        this.log('error', 'Server error received', message.data);
        
        this.triggerEvent('server_error', {
            error: message.data.error,
            sessionId: message.session_id,
            timestamp: message.timestamp
        });
    }
    
    // Helper Methods
    
    async subscribe(subscription) {
        if (!this.subscriptions.has(subscription)) {
            this.subscriptions.add(subscription);
            this.log('info', `Subscribed to ${subscription}`);
        }
    }
    
    triggerEvent(eventType, data) {
        if (this.eventHandlers.has(eventType)) {
            const handlers = this.eventHandlers.get(eventType);
            handlers.forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    this.log('error', `Error in event handler for ${eventType}`, error);
                }
            });
        }
    }
    
    async startFingerprintStreaming() {
        // Import and use SessionFingerprintCollector if available
        if (typeof SessionFingerprintCollector !== 'undefined') {
            try {
                const collector = new SessionFingerprintCollector();
                const fingerprint = await collector.collectComprehensiveFingerprint();
                
                // Send initial fingerprint
                await this.sendFingerprintData(fingerprint);
                
                // Set up periodic fingerprint updates
                setInterval(async () => {
                    try {
                        const updatedFingerprint = await collector.collectBrowserCharacteristics();
                        await this.sendFingerprintData(updatedFingerprint);
                    } catch (error) {
                        this.log('error', 'Failed to collect updated fingerprint', error);
                    }
                }, 60000); // Update every minute
                
            } catch (error) {
                this.log('error', 'Failed to initialize fingerprint streaming', error);
            }
        } else {
            this.log('warn', 'SessionFingerprintCollector not available - basic fingerprint streaming');
            
            // Basic fingerprint data
            const basicFingerprint = {
                userAgent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,
                screenResolution: `${screen.width}x${screen.height}`,
                colorDepth: screen.colorDepth,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            };
            
            await this.sendFingerprintData(basicFingerprint);
        }
    }
    
    startHeartbeat() {
        this.stopHeartbeat(); // Clear any existing heartbeat
        
        this.heartbeatTimer = setInterval(() => {
            if (this.isConnected && this.ws && this.ws.readyState === WebSocket.OPEN) {
                const heartbeatMessage = {
                    type: 'heartbeat',
                    session_id: this.sessionId,
                    timestamp: new Date().toISOString()
                };
                
                this.sendMessage(heartbeatMessage);
            }
        }, this.heartbeatInterval);
        
        this.log('debug', 'Heartbeat started');
    }
    
    stopHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
            this.log('debug', 'Heartbeat stopped');
        }
    }
    
    sendQueuedMessages() {
        if (this.messageQueue.length > 0) {
            this.log('info', `Sending ${this.messageQueue.length} queued messages`);
            
            const messages = [...this.messageQueue];
            this.messageQueue = [];
            
            messages.forEach(message => {
                this.sendMessage(message);
            });
        }
    }
    
    async handleReconnection() {
        if (this.isReconnecting || this.reconnectAttempts >= this.maxReconnectAttempts) {
            this.log('error', 'Max reconnection attempts reached');
            return;
        }
        
        this.isReconnecting = true;
        this.reconnectAttempts++;
        
        // Calculate backoff delay
        const delay = Math.min(
            this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1),
            this.maxReconnectInterval
        );
        
        this.log('info', `Attempting reconnection ${this.reconnectAttempts}/${this.maxReconnectAttempts} in ${delay}ms`);
        
        setTimeout(async () => {
            try {
                await this.connect();
                this.log('info', 'Reconnection successful');
            } catch (error) {
                this.log('error', 'Reconnection failed', error);
                this.isReconnecting = false;
                // Will try again on next connection failure
            }
        }, delay);
    }
    
    showNotification(title, message) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(title, {
                body: message,
                icon: '/favicon.ico'
            });
        }
    }
    
    log(level, message, data = null) {
        if (!this.debugMode && level === 'debug') {
            return;
        }
        
        const logMessage = `[WebSocketClient:${this.sessionId}] ${message}`;
        
        if (data) {
            this.logger[level](logMessage, data);
        } else {
            this.logger[level](logMessage);
        }
    }
    
    // Public API Methods
    
    getConnectionStatus() {
        return {
            isConnected: this.isConnected,
            isReconnecting: this.isReconnecting,
            connectionId: this.connectionId,
            reconnectAttempts: this.reconnectAttempts,
            subscriptions: Array.from(this.subscriptions),
            lastMessageTime: this.lastMessageTime,
            lastHeartbeat: this.lastHeartbeat
        };
    }
    
    getStatistics() {
        return {
            sessionId: this.sessionId,
            deviceId: this.deviceId,
            connectionStatus: this.getConnectionStatus(),
            eventHandlers: Array.from(this.eventHandlers.keys()),
            messageQueueSize: this.messageQueue.length,
            uptime: this.lastHeartbeat ? new Date() - this.lastHeartbeat : 0
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FingerprintingWebSocketClient;
} else if (typeof window !== 'undefined') {
    window.FingerprintingWebSocketClient = FingerprintingWebSocketClient;
}