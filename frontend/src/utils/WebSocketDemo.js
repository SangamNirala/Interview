/**
 * 🔐 WEBSOCKET REAL-TIME MONITORING DEMO
 * WebSocketDemo.js - Demo implementation showing WebSocket integration usage
 * 
 * This demo shows how to use the FingerprintingWebSocketClient for real-time monitoring
 * with the SessionFingerprintCollector for comprehensive device fingerprinting.
 */

// Demo class showing WebSocket integration usage
class WebSocketFingerprintingDemo {
    constructor(sessionId) {
        this.sessionId = sessionId || `demo_session_${Date.now()}`;
        this.wsClient = null;
        this.fingerprintCollector = null;
        this.isMonitoring = false;
    }

    /**
     * Initialize the demo with WebSocket client and fingerprint collector
     */
    async initialize() {
        try {
            // Initialize WebSocket client
            this.wsClient = new FingerprintingWebSocketClient(this.sessionId, {
                debug: true,
                heartbeatInterval: 30000,
                maxReconnectAttempts: 5
            });

            // Initialize fingerprint collector if available
            if (typeof SessionFingerprintCollector !== 'undefined') {
                this.fingerprintCollector = new SessionFingerprintCollector();
                console.log('✅ SessionFingerprintCollector initialized');
            } else {
                console.warn('⚠️  SessionFingerprintCollector not available - using basic fingerprinting');
            }

            // Register event handlers
            this.registerEventHandlers();

            console.log('✅ WebSocket fingerprinting demo initialized');
            return true;

        } catch (error) {
            console.error('❌ Failed to initialize demo:', error);
            return false;
        }
    }

    /**
     * Start real-time monitoring demo
     */
    async startMonitoring() {
        try {
            if (this.isMonitoring) {
                console.log('⚠️  Monitoring already active');
                return;
            }

            console.log('🚀 Starting real-time monitoring demo...');

            // Connect to WebSocket
            await this.wsClient.connect();

            // Start real-time fingerprinting monitoring
            await this.wsClient.startRealTimeMonitoring();

            // Subscribe to violation alerts
            await this.wsClient.subscribeToViolationAlerts((alertData) => {
                this.handleViolationAlert(alertData);
            });

            // Start device metrics streaming
            await this.wsClient.streamDeviceMetrics((metricsData) => {
                this.handleDeviceMetrics(metricsData);
            });

            // Start session integrity monitoring
            await this.wsClient.monitorSessionIntegrity((integrityData) => {
                this.handleSessionIntegrity(integrityData);
            });

            this.isMonitoring = true;
            console.log('✅ Real-time monitoring started successfully');

            // Start periodic fingerprint collection
            this.startPeriodicFingerprinting();

        } catch (error) {
            console.error('❌ Failed to start monitoring:', error);
        }
    }

    /**
     * Stop real-time monitoring
     */
    stopMonitoring() {
        try {
            if (!this.isMonitoring) {
                console.log('⚠️  Monitoring not active');
                return;
            }

            console.log('🛑 Stopping real-time monitoring...');

            // Disconnect WebSocket
            if (this.wsClient) {
                this.wsClient.disconnect();
            }

            // Stop periodic fingerprinting
            if (this.periodicTimer) {
                clearInterval(this.periodicTimer);
                this.periodicTimer = null;
            }

            this.isMonitoring = false;
            console.log('✅ Real-time monitoring stopped');

        } catch (error) {
            console.error('❌ Error stopping monitoring:', error);
        }
    }

    /**
     * Register event handlers for WebSocket events
     */
    registerEventHandlers() {
        if (!this.wsClient) return;

        // Connection events
        this.wsClient.registerEventHandler('connected', (data) => {
            console.log('🔌 Connected to WebSocket server:', data);
            this.displayStatus('Connected', 'success');
        });

        this.wsClient.registerEventHandler('disconnected', (data) => {
            console.log('🔌 Disconnected from WebSocket server:', data);
            this.displayStatus('Disconnected', 'warning');
        });

        // Fingerprint update events
        this.wsClient.registerEventHandler('fingerprint_update', (data) => {
            console.log('👤 Fingerprint update processed:', data);
            this.displayFingerprintUpdate(data);
        });

        // Subscription confirmation
        this.wsClient.registerEventHandler('subscription_confirmed', (data) => {
            console.log('✅ Subscription confirmed:', data.subscription);
            this.displaySubscriptionStatus(data.subscription, true);
        });

        // Error events
        this.wsClient.registerEventHandler('error', (data) => {
            console.error('❌ WebSocket error:', data);
            this.displayError(data.error);
        });

        // Server error events
        this.wsClient.registerEventHandler('server_error', (data) => {
            console.error('🚨 Server error:', data);
            this.displayError(`Server error: ${data.error}`);
        });
    }

    /**
     * Handle violation alerts
     */
    handleViolationAlert(alertData) {
        console.warn('🚨 SECURITY VIOLATION DETECTED:', alertData);

        // Create visual alert
        this.displayViolationAlert(alertData);

        // Log detailed information
        const logData = {
            type: alertData.violation_type,
            severity: alertData.severity,
            description: alertData.description,
            riskScore: alertData.risk_score,
            timestamp: alertData.detected_at,
            recommendation: alertData.recommendation
        };

        console.table(logData);
    }

    /**
     * Handle device metrics updates
     */
    handleDeviceMetrics(metricsData) {
        console.log('📊 Device metrics update:', metricsData);

        // Update metrics display
        this.displayDeviceMetrics(metricsData);

        // Check for anomalies
        if (metricsData.trends && metricsData.trends.anomaly_count > 0) {
            console.warn(`⚠️  ${metricsData.trends.anomaly_count} anomalies detected`);
        }
    }

    /**
     * Handle session integrity updates
     */
    handleSessionIntegrity(integrityData) {
        console.log('🔒 Session integrity update:', integrityData);

        // Update integrity display
        this.displaySessionIntegrity(integrityData);

        // Alert on low integrity
        if (integrityData.integrity_score < 0.7) {
            console.warn('⚠️  Session integrity compromised:', integrityData.status);
        }
    }

    /**
     * Start periodic fingerprint collection
     */
    startPeriodicFingerprinting() {
        if (this.periodicTimer) {
            clearInterval(this.periodicTimer);
        }

        this.periodicTimer = setInterval(async () => {
            try {
                if (this.fingerprintCollector) {
                    // Collect comprehensive fingerprint
                    const fingerprint = await this.fingerprintCollector.collectComprehensiveFingerprint();
                    await this.wsClient.sendFingerprintData(fingerprint);

                    console.log('📋 Comprehensive fingerprint sent:', {
                        timestamp: new Date().toISOString(),
                        dataSize: JSON.stringify(fingerprint).length
                    });
                } else {
                    // Send basic fingerprint
                    const basicFingerprint = this.collectBasicFingerprint();
                    await this.wsClient.sendFingerprintData(basicFingerprint);

                    console.log('📋 Basic fingerprint sent:', {
                        timestamp: new Date().toISOString(),
                        dataSize: JSON.stringify(basicFingerprint).length
                    });
                }
            } catch (error) {
                console.error('❌ Error sending periodic fingerprint:', error);
            }
        }, 60000); // Every minute
    }

    /**
     * Collect basic fingerprint data when SessionFingerprintCollector is not available
     */
    collectBasicFingerprint() {
        return {
            // Basic browser information
            userAgent: navigator.userAgent,
            language: navigator.language,
            languages: navigator.languages || [],
            platform: navigator.platform,
            
            // Screen information
            screenWidth: screen.width,
            screenHeight: screen.height,
            screenColorDepth: screen.colorDepth,
            screenPixelDepth: screen.pixelDepth,
            
            // Timezone and locale
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            timezoneOffset: new Date().getTimezoneOffset(),
            
            // Browser capabilities
            cookieEnabled: navigator.cookieEnabled,
            doNotTrack: navigator.doNotTrack,
            onLine: navigator.onLine,
            
            // Plugin information
            pluginsCount: navigator.plugins.length,
            mimeTypesCount: navigator.mimeTypes.length,
            
            // Additional data
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId,
            deviceId: this.wsClient ? this.wsClient.deviceId : null
        };
    }

    // UI Display Methods (these would be implemented based on your UI framework)

    displayStatus(status, type) {
        console.log(`📊 Status Update: ${status} (${type})`);
        // Implement UI status display here
    }

    displayFingerprintUpdate(data) {
        console.log('📋 Fingerprint Update Display:', data);
        // Implement fingerprint update display here
    }

    displaySubscriptionStatus(subscription, active) {
        console.log(`🔔 Subscription ${subscription}: ${active ? 'Active' : 'Inactive'}`);
        // Implement subscription status display here
    }

    displayError(error) {
        console.error('🚨 Error Display:', error);
        // Implement error display here
    }

    displayViolationAlert(alertData) {
        console.warn('🚨 Violation Alert Display:', alertData);
        // Implement violation alert display here
        
        // Example: Show browser notification
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Security Violation Detected', {
                body: alertData.description,
                icon: '/favicon.ico'
            });
        }
    }

    displayDeviceMetrics(metricsData) {
        console.log('📊 Device Metrics Display:', metricsData);
        // Implement device metrics display here
    }

    displaySessionIntegrity(integrityData) {
        console.log('🔒 Session Integrity Display:', integrityData);
        // Implement session integrity display here
    }

    /**
     * Get current monitoring status
     */
    getStatus() {
        return {
            isMonitoring: this.isMonitoring,
            sessionId: this.sessionId,
            wsClient: this.wsClient ? this.wsClient.getConnectionStatus() : null,
            fingerprintCollector: !!this.fingerprintCollector
        };
    }

    /**
     * Get monitoring statistics
     */
    getStatistics() {
        const stats = {
            sessionId: this.sessionId,
            isMonitoring: this.isMonitoring,
            fingerprintCollectorAvailable: !!this.fingerprintCollector
        };

        if (this.wsClient) {
            stats.webSocket = this.wsClient.getStatistics();
        }

        return stats;
    }
}

// Usage Example
/*

// Initialize demo
const demo = new WebSocketFingerprintingDemo('test_session_123');

// Start monitoring
demo.initialize().then(async (success) => {
    if (success) {
        await demo.startMonitoring();
        console.log('Demo started successfully!');
    } else {
        console.error('Failed to initialize demo');
    }
});

// Stop monitoring after 5 minutes (demo purposes)
setTimeout(() => {
    demo.stopMonitoring();
    console.log('Demo completed');
}, 300000);

*/

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WebSocketFingerprintingDemo;
} else if (typeof window !== 'undefined') {
    window.WebSocketFingerprintingDemo = WebSocketFingerprintingDemo;
}