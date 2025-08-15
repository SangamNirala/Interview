/**
 * Test script for Phase 3.4: Frontend Fingerprinting Collection
 * Tests the enhanced collectDeviceFingerprint() and collectBrowserCharacteristics() methods
 */

import SessionFingerprintCollector from './utils/SessionFingerprintCollector.js';

async function testFingerprintCollection() {
    console.log('🧪 Testing Phase 3.4: Frontend Fingerprinting Collection');
    
    try {
        const collector = new SessionFingerprintCollector();
        
        console.log('\n📱 Testing Enhanced Device Fingerprint Collection...');
        const deviceStart = performance.now();
        const deviceFingerprint = await collector.collectDeviceFingerprint();
        const deviceTime = performance.now() - deviceStart;
        
        console.log(`✅ Device fingerprint collected in ${deviceTime.toFixed(2)}ms`);
        console.log('📊 Device fingerprint components:');
        console.log('  - Hardware enumeration:', !!deviceFingerprint.hardware_enumeration);
        console.log('  - Screen characteristics:', !!deviceFingerprint.screen_characteristics);
        console.log('  - CPU architecture:', !!deviceFingerprint.cpu_architecture);
        console.log('  - Memory/Storage:', !!deviceFingerprint.memory_storage);
        console.log('  - Device sensors:', !!deviceFingerprint.device_sensors);
        console.log('  - Performance benchmarks:', !!deviceFingerprint.performance_benchmarks);
        console.log('  - Canvas fingerprint:', !!deviceFingerprint.canvas_fingerprint);
        console.log('  - WebGL fingerprint:', !!deviceFingerprint.webgl_fingerprint);
        
        console.log('\n🌐 Testing Enhanced Browser Characteristics Collection...');
        const browserStart = performance.now();
        const browserCharacteristics = await collector.collectBrowserCharacteristics();
        const browserTime = performance.now() - browserStart;
        
        console.log(`✅ Browser characteristics collected in ${browserTime.toFixed(2)}ms`);
        console.log('📊 Browser characteristics components:');
        console.log('  - Browser identification:', !!browserCharacteristics.browser_identification);
        console.log('  - JavaScript engine:', !!browserCharacteristics.javascript_engine);
        console.log('  - Rendering engine:', !!browserCharacteristics.rendering_engine);
        console.log('  - Font analysis:', !!browserCharacteristics.font_analysis);
        console.log('  - API availability:', !!browserCharacteristics.api_availability);
        console.log('  - Plugins/extensions:', !!browserCharacteristics.plugins_extensions);
        console.log('  - Storage capabilities:', !!browserCharacteristics.storage_capabilities);
        console.log('  - Media/input:', !!browserCharacteristics.media_input);
        console.log('  - Web APIs:', !!browserCharacteristics.web_apis);
        console.log('  - Performance capabilities:', !!browserCharacteristics.performance_capabilities);
        console.log('  - Rendering fingerprint:', !!browserCharacteristics.rendering_fingerprint);
        
        console.log('\n🎯 Testing Comprehensive Fingerprint Collection...');
        const comprehensiveStart = performance.now();
        const comprehensiveFingerprint = await collector.collectComprehensiveFingerprint();
        const comprehensiveTime = performance.now() - comprehensiveStart;
        
        console.log(`✅ Comprehensive fingerprint collected in ${comprehensiveTime.toFixed(2)}ms`);
        console.log('📊 Total data size:', JSON.stringify(comprehensiveFingerprint).length, 'characters');
        
        // Display key fingerprinting results
        console.log('\n🔍 Key Fingerprinting Results:');
        
        if (deviceFingerprint.hardware_enumeration?.gpu) {
            console.log('  GPU:', deviceFingerprint.hardware_enumeration.gpu.vendor, 
                       deviceFingerprint.hardware_enumeration.gpu.renderer);
        }
        
        if (deviceFingerprint.cpu_architecture) {
            console.log('  CPU cores:', deviceFingerprint.cpu_architecture.cores);
            console.log('  CPU architecture:', deviceFingerprint.cpu_architecture.architecture);
        }
        
        if (deviceFingerprint.screen_characteristics) {
            console.log('  Screen:', `${deviceFingerprint.screen_characteristics.width}x${deviceFingerprint.screen_characteristics.height}`);
            console.log('  Color depth:', deviceFingerprint.screen_characteristics.color_depth);
        }
        
        if (browserCharacteristics.browser_identification) {
            console.log('  Browser:', browserCharacteristics.browser_identification.browser_name, 
                       browserCharacteristics.browser_identification.browser_version);
        }
        
        if (browserCharacteristics.javascript_engine) {
            console.log('  JS Engine:', browserCharacteristics.javascript_engine.engine_identification?.name);
        }
        
        if (browserCharacteristics.font_analysis?.system_fonts) {
            console.log('  Fonts detected:', browserCharacteristics.font_analysis.system_fonts.detected_count);
        }
        
        if (browserCharacteristics.web_apis) {
            const apiCount = Object.values(browserCharacteristics.web_apis).filter(Boolean).length;
            console.log('  Web APIs supported:', apiCount);
        }
        
        console.log('\n🎉 Phase 3.4 Frontend Fingerprinting Collection Test Complete!');
        console.log('📈 Performance Summary:');
        console.log(`  - Device fingerprinting: ${deviceTime.toFixed(2)}ms`);
        console.log(`  - Browser characteristics: ${browserTime.toFixed(2)}ms`);
        console.log(`  - Comprehensive collection: ${comprehensiveTime.toFixed(2)}ms`);
        
        return {
            success: true,
            device_fingerprint: deviceFingerprint,
            browser_characteristics: browserCharacteristics,
            comprehensive_fingerprint: comprehensiveFingerprint,
            performance: {
                device_time: deviceTime,
                browser_time: browserTime,
                comprehensive_time: comprehensiveTime
            }
        };
        
    } catch (error) {
        console.error('❌ Error during fingerprint collection testing:', error);
        return {
            success: false,
            error: error.message
        };
    }
}

// Export for use in other modules
export default testFingerprintCollection;

// Auto-run if directly executed
if (typeof window !== 'undefined' && window.location) {
    // Add a global function for browser console testing
    window.testFingerprintCollection = testFingerprintCollection;
    
    console.log('🔐 Phase 3.4: Frontend Fingerprinting Collection Test Ready!');
    console.log('💡 Run "testFingerprintCollection()" in browser console to test the functionality');
}