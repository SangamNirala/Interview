/**
 * 🔐 BIOMETRIC DATA COLLECTOR - Frontend Component
 * Module 1: Behavioral Biometric Analysis Engine
 * 
 * Silently collect keystroke, mouse, scroll, and timing data for security analysis
 * GDPR-compliant with user consent management
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';

class BiometricDataCollector {
    constructor(sessionId, consentGiven = false) {
        this.sessionId = sessionId;
        this.consentGiven = consentGiven;
        this.isCollecting = false;
        
        // Data storage
        this.keystrokeData = [];
        this.mouseData = [];
        this.scrollData = [];
        this.clickData = [];
        this.timingData = [];
        
        // Configuration
        this.maxDataPoints = 1000; // Limit data collection to prevent memory issues
        this.submitInterval = 30000; // Submit every 30 seconds
        this.submitTimer = null;
        
        // Event listeners
        this.boundKeydownHandler = this.handleKeydown.bind(this);
        this.boundKeyupHandler = this.handleKeyup.bind(this);
        this.boundMousemoveHandler = this.handleMousemove.bind(this);
        this.boundClickHandler = this.handleClick.bind(this);
        this.boundScrollHandler = this.handleScroll.bind(this);
        
        // Throttling for mouse events
        this.lastMouseMove = 0;
        this.mouseMoveThrottle = 100; // 100ms throttle
        
        // Question timing tracking
        this.questionStartTime = null;
        this.currentQuestionId = null;
    }
    
    startCollection() {
        if (!this.consentGiven) {
            console.warn('Biometric data collection requires user consent');
            return false;
        }
        
        if (this.isCollecting) {
            return true;
        }
        
        this.isCollecting = true;
        
        // Add event listeners
        document.addEventListener('keydown', this.boundKeydownHandler, true);
        document.addEventListener('keyup', this.boundKeyupHandler, true);
        document.addEventListener('mousemove', this.boundMousemoveHandler, true);
        document.addEventListener('click', this.boundClickHandler, true);
        document.addEventListener('scroll', this.boundScrollHandler, true);
        
        // Start periodic data submission
        this.submitTimer = setInterval(() => {
            this.submitBiometricData();
        }, this.submitInterval);
        
        console.log('🔐 Biometric data collection started for session:', this.sessionId);
        return true;
    }
    
    stopCollection() {
        if (!this.isCollecting) {
            return;
        }
        
        this.isCollecting = false;
        
        // Remove event listeners
        document.removeEventListener('keydown', this.boundKeydownHandler, true);
        document.removeEventListener('keyup', this.boundKeyupHandler, true);
        document.removeEventListener('mousemove', this.boundMousemoveHandler, true);
        document.removeEventListener('click', this.boundClickHandler, true);
        document.removeEventListener('scroll', this.boundScrollHandler, true);
        
        // Clear timer
        if (this.submitTimer) {
            clearInterval(this.submitTimer);
            this.submitTimer = null;
        }
        
        // Submit any remaining data
        this.submitBiometricData();
        
        console.log('🔐 Biometric data collection stopped for session:', this.sessionId);
    }
    
    updateConsent(consentGiven) {
        this.consentGiven = consentGiven;
        
        if (!consentGiven && this.isCollecting) {
            this.stopCollection();
        }
    }
    
    // Keystroke event handlers
    handleKeydown(event) {
        if (!this.isCollecting) return;
        
        const timestamp = performance.now();
        
        this.keystrokeData.push({
            key: event.key,
            code: event.code,
            timestamp: timestamp,
            event_type: 'keydown',
            shift_key: event.shiftKey,
            ctrl_key: event.ctrlKey,
            alt_key: event.altKey,
            meta_key: event.metaKey
        });
        
        // Limit data points
        if (this.keystrokeData.length > this.maxDataPoints) {
            this.keystrokeData.shift();
        }
    }
    
    handleKeyup(event) {
        if (!this.isCollecting) return;
        
        const timestamp = performance.now();
        
        this.keystrokeData.push({
            key: event.key,
            code: event.code,
            timestamp: timestamp,
            event_type: 'keyup',
            shift_key: event.shiftKey,
            ctrl_key: event.ctrlKey,
            alt_key: event.altKey,
            meta_key: event.metaKey
        });
        
        // Limit data points
        if (this.keystrokeData.length > this.maxDataPoints) {
            this.keystrokeData.shift();
        }
    }
    
    // Mouse event handlers
    handleMousemove(event) {
        if (!this.isCollecting) return;
        
        const now = performance.now();
        
        // Throttle mouse move events
        if (now - this.lastMouseMove < this.mouseMoveThrottle) {
            return;
        }
        
        this.lastMouseMove = now;
        
        this.mouseData.push({
            x: event.clientX,
            y: event.clientY,
            timestamp: now,
            event_type: 'mousemove',
            target: event.target.tagName.toLowerCase(),
            button: event.button
        });
        
        // Limit data points
        if (this.mouseData.length > this.maxDataPoints) {
            this.mouseData.shift();
        }
    }
    
    handleClick(event) {
        if (!this.isCollecting) return;
        
        const timestamp = performance.now();
        
        this.clickData.push({
            x: event.clientX,
            y: event.clientY,
            timestamp: timestamp,
            event_type: 'click',
            button: event.button,
            target: event.target.tagName.toLowerCase(),
            target_id: event.target.id || '',
            target_class: event.target.className || ''
        });
        
        // Also add to mouse data for consistency analysis
        this.mouseData.push({
            x: event.clientX,
            y: event.clientY,
            timestamp: timestamp,
            event_type: 'click',
            target: event.target.tagName.toLowerCase(),
            button: event.button
        });
        
        // Limit data points
        if (this.clickData.length > this.maxDataPoints) {
            this.clickData.shift();
        }
        
        if (this.mouseData.length > this.maxDataPoints) {
            this.mouseData.shift();
        }
    }
    
    // Scroll event handler
    handleScroll(event) {
        if (!this.isCollecting) return;
        
        const timestamp = performance.now();
        
        this.scrollData.push({
            x: window.scrollX || window.pageXOffset,
            y: window.scrollY || window.pageYOffset,
            deltaX: event.deltaX || 0,
            deltaY: event.deltaY || 0,
            timestamp: timestamp,
            event_type: 'scroll',
            target: event.target.tagName.toLowerCase()
        });
        
        // Limit data points
        if (this.scrollData.length > this.maxDataPoints) {
            this.scrollData.shift();
        }
    }
    
    // Question timing methods
    startQuestionTiming(questionId) {
        if (!this.isCollecting) return;
        
        this.questionStartTime = performance.now();
        this.currentQuestionId = questionId;
    }
    
    endQuestionTiming(questionId, correct = null, difficulty = null, topic = null) {
        if (!this.isCollecting || !this.questionStartTime) return;
        
        const endTime = performance.now();
        const responseTime = (endTime - this.questionStartTime) / 1000; // Convert to seconds
        
        this.timingData.push({
            question_id: questionId || this.currentQuestionId,
            response_time: responseTime,
            start_time: this.questionStartTime,
            end_time: endTime,
            correct: correct,
            difficulty: difficulty,
            topic: topic,
            timestamp: endTime
        });
        
        // Reset timing
        this.questionStartTime = null;
        this.currentQuestionId = null;
        
        // Limit data points
        if (this.timingData.length > this.maxDataPoints) {
            this.timingData.shift();
        }
    }
    
    // Data submission
    async submitBiometricData() {
        if (!this.consentGiven || (!this.keystrokeData.length && !this.mouseData.length && !this.scrollData.length && !this.clickData.length && !this.timingData.length)) {
            return;
        }
        
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
            
            const payload = {
                session_id: this.sessionId,
                keystroke_data: [...this.keystrokeData],
                mouse_data: [...this.mouseData],
                scroll_data: [...this.scrollData],
                click_data: [...this.clickData],
                timing_data: [...this.timingData],
                consent_given: this.consentGiven
            };
            
            const response = await fetch(`${backendUrl}/api/security/biometric-data/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('🔐 Biometric data submitted successfully:', result.message);
                
                // Clear submitted data
                this.keystrokeData = [];
                this.mouseData = [];
                this.scrollData = [];
                this.clickData = [];
                this.timingData = [];
                
                return result;
            } else {
                console.error('🔐 Failed to submit biometric data:', response.statusText);
            }
        } catch (error) {
            console.error('🔐 Error submitting biometric data:', error);
        }
    }
    
    // Get current data stats (for debugging)
    getDataStats() {
        return {
            keystroke_events: this.keystrokeData.length,
            mouse_events: this.mouseData.length,
            scroll_events: this.scrollData.length,
            click_events: this.clickData.length,
            timing_events: this.timingData.length,
            is_collecting: this.isCollecting,
            consent_given: this.consentGiven,
            session_id: this.sessionId
        };
    }
}

// React Hook for Biometric Data Collection
export const useBiometricDataCollection = (sessionId, initialConsent = false) => {
    const [collector, setCollector] = useState(null);
    const [isCollecting, setIsCollecting] = useState(false);
    const [consentGiven, setConsentGiven] = useState(initialConsent);
    const [dataStats, setDataStats] = useState({});
    
    // Initialize collector
    useEffect(() => {
        if (sessionId) {
            const newCollector = new BiometricDataCollector(sessionId, initialConsent);
            setCollector(newCollector);
            
            return () => {
                if (newCollector) {
                    newCollector.stopCollection();
                }
            };
        }
    }, [sessionId, initialConsent]);
    
    // Start collection
    const startCollection = useCallback(() => {
        if (collector && consentGiven) {
            const started = collector.startCollection();
            setIsCollecting(started);
            return started;
        }
        return false;
    }, [collector, consentGiven]);
    
    // Stop collection
    const stopCollection = useCallback(() => {
        if (collector) {
            collector.stopCollection();
            setIsCollecting(false);
        }
    }, [collector]);
    
    // Update consent
    const updateConsent = useCallback((consent) => {
        setConsentGiven(consent);
        if (collector) {
            collector.updateConsent(consent);
            if (!consent) {
                setIsCollecting(false);
            }
        }
    }, [collector]);
    
    // Question timing methods
    const startQuestionTiming = useCallback((questionId) => {
        if (collector) {
            collector.startQuestionTiming(questionId);
        }
    }, [collector]);
    
    const endQuestionTiming = useCallback((questionId, correct, difficulty, topic) => {
        if (collector) {
            collector.endQuestionTiming(questionId, correct, difficulty, topic);
        }
    }, [collector]);
    
    // Get data statistics
    const getStats = useCallback(() => {
        if (collector) {
            const stats = collector.getDataStats();
            setDataStats(stats);
            return stats;
        }
        return {};
    }, [collector]);
    
    // Submit data manually
    const submitData = useCallback(async () => {
        if (collector) {
            return await collector.submitBiometricData();
        }
    }, [collector]);
    
    return {
        isCollecting,
        consentGiven,
        startCollection,
        stopCollection,
        updateConsent,
        startQuestionTiming,
        endQuestionTiming,
        getStats,
        submitData,
        dataStats
    };
};

// React Component for GDPR Consent Management
export const BiometricConsentDialog = ({ sessionId, onConsentChange, show = true }) => {
    const [consentGiven, setConsentGiven] = useState(false);
    const [showDialog, setShowDialog] = useState(show);
    
    const handleConsentSubmit = async (consent) => {
        setConsentGiven(consent);
        
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
            
            const response = await fetch(`${backendUrl}/api/security/data-privacy/consent`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    candidate_id: sessionId, // Using session ID as candidate ID for now
                    consent_given: consent,
                    data_types: ['keystroke', 'mouse', 'scroll', 'timing']
                })
            });
            
            if (response.ok) {
                console.log('🔐 Consent recorded successfully');
            }
        } catch (error) {
            console.error('🔐 Error recording consent:', error);
        }
        
        setShowDialog(false);
        onConsentChange(consent);
    };
    
    if (!showDialog) {
        return null;
    }
    
    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-md mx-4 shadow-xl">
                <div className="flex items-center mb-4">
                    <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                        <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                        </svg>
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900">Security & Privacy Notice</h3>
                </div>
                
                <div className="mb-6">
                    <p className="text-gray-700 mb-4">
                        To ensure test integrity and prevent cheating, we collect behavioral data during your assessment including:
                    </p>
                    
                    <ul className="text-sm text-gray-600 mb-4 space-y-1">
                        <li>• Keystroke timing patterns</li>
                        <li>• Mouse movement and click patterns</li>
                        <li>• Scroll behavior</li>
                        <li>• Response timing data</li>
                    </ul>
                    
                    <p className="text-sm text-gray-600">
                        This data is anonymized, encrypted, and automatically deleted after 90 days. 
                        It is used solely for security analysis and fraud prevention.
                    </p>
                </div>
                
                <div className="flex space-x-3">
                    <button
                        onClick={() => handleConsentSubmit(true)}
                        className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors font-medium"
                    >
                        Accept & Continue
                    </button>
                    <button
                        onClick={() => handleConsentSubmit(false)}
                        className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors font-medium"
                    >
                        Decline
                    </button>
                </div>
                
                <p className="text-xs text-gray-500 mt-3 text-center">
                    Declining will disable security monitoring but you can still take the test.
                </p>
            </div>
        </div>
    );
};

// React Component for Admin Biometric Configuration
export const BiometricConfigPanel = ({ sessionId, onConfigChange }) => {
    const [config, setConfig] = useState({
        enable_biometric_tracking: true,
        tracking_sensitivity: 'medium',
        real_time_analysis: true,
        intervention_enabled: true
    });
    
    const [isUpdating, setIsUpdating] = useState(false);
    
    const handleConfigUpdate = async (newConfig) => {
        setIsUpdating(true);
        
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL || '';
            
            const response = await fetch(`${backendUrl}/api/security/biometric-config/update`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    ...newConfig
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                setConfig(newConfig);
                onConfigChange(newConfig);
                console.log('🔐 Biometric configuration updated:', result.message);
            }
        } catch (error) {
            console.error('🔐 Error updating biometric configuration:', error);
        } finally {
            setIsUpdating(false);
        }
    };
    
    return (
        <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
                <svg className="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
                Biometric Security Configuration
            </h3>
            
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Enable Biometric Tracking</label>
                    <button
                        onClick={() => handleConfigUpdate({
                            ...config,
                            enable_biometric_tracking: !config.enable_biometric_tracking
                        })}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            config.enable_biometric_tracking ? 'bg-blue-600' : 'bg-gray-200'
                        }`}
                        disabled={isUpdating}
                    >
                        <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                config.enable_biometric_tracking ? 'translate-x-6' : 'translate-x-1'
                            }`}
                        />
                    </button>
                </div>
                
                <div>
                    <label className="text-sm font-medium text-gray-700 block mb-2">Tracking Sensitivity</label>
                    <select
                        value={config.tracking_sensitivity}
                        onChange={(e) => handleConfigUpdate({
                            ...config,
                            tracking_sensitivity: e.target.value
                        })}
                        className="w-full p-2 border border-gray-300 rounded-md text-sm"
                        disabled={isUpdating}
                    >
                        <option value="low">Low - Basic tracking</option>
                        <option value="medium">Medium - Standard tracking</option>
                        <option value="high">High - Detailed tracking</option>
                    </select>
                </div>
                
                <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Real-time Analysis</label>
                    <button
                        onClick={() => handleConfigUpdate({
                            ...config,
                            real_time_analysis: !config.real_time_analysis
                        })}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            config.real_time_analysis ? 'bg-blue-600' : 'bg-gray-200'
                        }`}
                        disabled={isUpdating}
                    >
                        <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                config.real_time_analysis ? 'translate-x-6' : 'translate-x-1'
                            }`}
                        />
                    </button>
                </div>
                
                <div className="flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-700">Auto Intervention</label>
                    <button
                        onClick={() => handleConfigUpdate({
                            ...config,
                            intervention_enabled: !config.intervention_enabled
                        })}
                        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                            config.intervention_enabled ? 'bg-blue-600' : 'bg-gray-200'
                        }`}
                        disabled={isUpdating}
                    >
                        <span
                            className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                                config.intervention_enabled ? 'translate-x-6' : 'translate-x-1'
                            }`}
                        />
                    </button>
                </div>
            </div>
            
            {isUpdating && (
                <div className="mt-4 text-center">
                    <div className="inline-flex items-center text-sm text-gray-600">
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-600" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Updating configuration...
                    </div>
                </div>
            )}
        </div>
    );
};

export default BiometricDataCollector;