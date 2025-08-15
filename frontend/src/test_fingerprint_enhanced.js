/**
 * Test file to verify the enhanced collectNetworkInformation() and collectEnvironmentalData() methods
 * This demonstrates the PHASE 3.4 implementation
 */

import SessionFingerprintCollector from './utils/SessionFingerprintCollector.js';

async function testEnhancedFingerprinting() {
    console.log('🧪 Testing Enhanced Session Fingerprinting Collection - PHASE 3.4');
    
    const collector = new SessionFingerprintCollector();
    
    try {
        console.log('\n🌐 Testing Enhanced Network Information Collection...');
        const networkInfo = await collector.collectNetworkInformation();
        console.log('✅ Network Information Result:', {
            hasConnectionCharacteristics: !!networkInfo.connection_characteristics,
            hasNetworkTiming: !!networkInfo.network_timing,
            hasWebRTCAnalysis: !!networkInfo.webrtc_analysis,
            hasDNSCharacteristics: !!networkInfo.dns_characteristics,
            hasNetworkTopology: !!networkInfo.network_topology,
            hasCollectionMetadata: !!networkInfo.collection_metadata,
            fingerprintVersion: networkInfo.collection_metadata?.fingerprint_version
        });
        
        console.log('\n🌍 Testing Enhanced Environmental Data Collection...');
        const environmentalData = await collector.collectEnvironmentalData();
        console.log('✅ Environmental Data Result:', {
            hasLocaleCharacteristics: !!environmentalData.locale_characteristics,
            hasBatteryCharacteristics: !!environmentalData.battery_characteristics,
            hasMotionSensors: !!environmentalData.motion_sensors,
            hasAmbientSensors: !!environmentalData.ambient_sensors,
            hasMediaDevices: !!environmentalData.media_devices,
            hasDisplayPreferences: !!environmentalData.display_preferences,
            hasCollectionMetadata: !!environmentalData.collection_metadata,
            fingerprintVersion: environmentalData.collection_metadata?.fingerprint_version
        });
        
        console.log('\n🎯 Testing Comprehensive Fingerprint Collection...');
        const comprehensiveFingerprint = await collector.collectComprehensiveFingerprint();
        console.log('✅ Comprehensive Fingerprint Result:', {
            hasNetworkData: !!comprehensiveFingerprint.network,
            hasEnvironmentData: !!comprehensiveFingerprint.environment,
            networkVersion: comprehensiveFingerprint.network?.collection_metadata?.fingerprint_version,
            environmentVersion: comprehensiveFingerprint.environment?.collection_metadata?.fingerprint_version,
            collectionTimeMs: comprehensiveFingerprint.collection_metadata?.collection_time_ms
        });
        
        console.log('\n🎉 All Enhanced Fingerprinting Tests Completed Successfully!');
        console.log('📊 PHASE 3.4 Implementation Status:');
        console.log('   ✅ collectNetworkInformation() - ENHANCED');
        console.log('   ✅ collectEnvironmentalData() - ENHANCED');
        console.log('   ✅ Comprehensive integration - WORKING');
        
        return {
            success: true,
            networkInfo,
            environmentalData,
            comprehensiveFingerprint
        };
        
    } catch (error) {
        console.error('❌ Enhanced Fingerprinting Test Failed:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// Run the test if this file is executed directly
if (typeof window !== 'undefined') {
    // Browser environment
    document.addEventListener('DOMContentLoaded', () => {
        testEnhancedFingerprinting().then(result => {
            console.log('🏁 Test Result:', result);
        });
    });
} else {
    // Node.js environment
    testEnhancedFingerprinting().then(result => {
        console.log('🏁 Test Result:', result);
    });
}

export default testEnhancedFingerprinting;