/**
 * Usage Example for Phase 3.4: Frontend Fingerprinting Collection
 * Demonstrates how to use the enhanced collectDeviceFingerprint() and collectBrowserCharacteristics() methods
 */

import SessionFingerprintCollector from './utils/SessionFingerprintCollector.js';

/**
 * Example: Comprehensive Device and Browser Fingerprinting
 */
export async function comprehensiveExample() {
    console.log('🚀 Starting Phase 3.4: Enhanced Fingerprinting Example\n');
    
    const collector = new SessionFingerprintCollector();
    
    try {
        // Example 1: Collect Device Fingerprint
        console.log('📱 Collecting Enhanced Device Fingerprint...');
        const deviceFingerprint = await collector.collectDeviceFingerprint();
        
        console.log('✅ Device Hardware Enumeration:');
        if (deviceFingerprint.hardware_enumeration) {
            console.log('  - GPU Vendor:', deviceFingerprint.hardware_enumeration.gpu?.vendor || 'Unknown');
            console.log('  - GPU Renderer:', deviceFingerprint.hardware_enumeration.gpu?.renderer || 'Unknown');
            console.log('  - WebGL Support:', deviceFingerprint.hardware_enumeration.webgl_info?.supported || false);
            console.log('  - Canvas Support:', deviceFingerprint.hardware_enumeration.canvas_info?.supported || false);
        }
        
        console.log('✅ Screen Characteristics & Color Profile:');
        if (deviceFingerprint.screen_characteristics) {
            const screen = deviceFingerprint.screen_characteristics;
            console.log(`  - Resolution: ${screen.width}x${screen.height}`);
            console.log(`  - Color Depth: ${screen.color_depth} bits`);
            console.log(`  - Pixel Ratio: ${screen.device_pixel_ratio}`);
            console.log(`  - Orientation: ${screen.orientation}`);
        }
        
        console.log('✅ CPU Architecture & Performance:');
        if (deviceFingerprint.cpu_architecture) {
            const cpu = deviceFingerprint.cpu_architecture;
            console.log(`  - Cores: ${cpu.cores}`);
            console.log(`  - Architecture: ${cpu.architecture}`);
            console.log(`  - Performance Score: ${cpu.performance_score || 'N/A'}`);
            console.log(`  - Features: ${cpu.features?.join(', ') || 'None detected'}`);
        }
        
        console.log('✅ Memory & Storage Detection:');
        if (deviceFingerprint.memory_storage) {
            const memory = deviceFingerprint.memory_storage.memory;
            const storage = deviceFingerprint.memory_storage.storage;
            
            if (memory) {
                console.log(`  - Device Memory: ${memory.device_memory / (1024**3) || 'Unknown'} GB`);
                console.log(`  - JS Heap Limit: ${memory.js_heap_size_limit ? (memory.js_heap_size_limit / (1024**2)).toFixed(2) + ' MB' : 'Unknown'}`);
            }
            
            if (storage) {
                console.log(`  - Storage Quota: ${storage.quota ? (storage.quota / (1024**3)).toFixed(2) + ' GB' : 'Unknown'}`);
                console.log(`  - Storage Usage: ${storage.usage ? (storage.usage / (1024**2)).toFixed(2) + ' MB' : 'Unknown'}`);
            }
        }
        
        console.log('✅ Device Sensors:');
        if (deviceFingerprint.device_sensors) {
            const sensors = deviceFingerprint.device_sensors;
            console.log(`  - Accelerometer: ${sensors.accelerometer ? '✓' : '✗'}`);
            console.log(`  - Gyroscope: ${sensors.gyroscope ? '✓' : '✗'}`);
            console.log(`  - Battery API: ${sensors.battery_api ? '✓' : '✗'}`);
            console.log(`  - Ambient Light: ${sensors.ambient_light ? '✓' : '✗'}`);
        }
        
        // Example 2: Collect Browser Characteristics
        console.log('\n🌐 Collecting Enhanced Browser Characteristics...');
        const browserCharacteristics = await collector.collectBrowserCharacteristics();
        
        console.log('✅ Browser Version, Plugins & Extensions:');
        if (browserCharacteristics.browser_identification) {
            const browser = browserCharacteristics.browser_identification;
            console.log(`  - Browser: ${browser.browser_name} ${browser.browser_version}`);
            console.log(`  - Platform: ${browser.platform}`);
            console.log(`  - Vendor: ${browser.vendor || 'Unknown'}`);
            console.log(`  - Build ID: ${browser.browser_build_id || 'Unknown'}`);
        }
        
        if (browserCharacteristics.plugins_extensions) {
            const plugins = browserCharacteristics.plugins_extensions;
            console.log(`  - Plugins: ${plugins.plugin_count} detected`);
            console.log(`  - MIME Types: ${plugins.mime_count} supported`);
        }
        
        console.log('✅ JavaScript Engine Capabilities & Performance:');
        if (browserCharacteristics.javascript_engine) {
            const jsEngine = browserCharacteristics.javascript_engine;
            console.log(`  - Engine: ${jsEngine.engine_identification?.name || 'Unknown'}`);
            console.log(`  - V8 Features: ${jsEngine.v8_features?.has_v8 ? '✓' : '✗'}`);
            console.log(`  - ES6 Support: ${jsEngine.javascript_version?.es6 ? '✓' : '✗'}`);
            console.log(`  - BigInt Support: ${jsEngine.javascript_version?.es2020 ? '✓' : '✗'}`);
            
            if (jsEngine.memory_management?.available !== false) {
                const memory = jsEngine.memory_management;
                console.log(`  - Memory Pressure: ${memory.memory_pressure ? (memory.memory_pressure * 100).toFixed(1) + '%' : 'Unknown'}`);
            }
        }
        
        console.log('✅ Rendering Engine Fingerprinting:');
        if (browserCharacteristics.rendering_engine) {
            const rendering = browserCharacteristics.rendering_engine;
            console.log(`  - Layout Engine: ${rendering.layout_engine || 'Unknown'}`);
            console.log(`  - Hardware Acceleration: ${rendering.graphics_rendering?.hardware_acceleration ? '✓' : '✗'}`);
            
            if (rendering.css_support) {
                const css = rendering.css_support;
                console.log(`  - Flexbox: ${css.flexbox ? '✓' : '✗'}`);
                console.log(`  - Grid: ${css.grid ? '✓' : '✗'}`);
                console.log(`  - Custom Properties: ${css.custom_properties ? '✓' : '✗'}`);
            }
        }
        
        console.log('✅ Font Enumeration & Rendering Analysis:');
        if (browserCharacteristics.font_analysis) {
            const fonts = browserCharacteristics.font_analysis;
            
            if (fonts.system_fonts) {
                console.log(`  - System Fonts Detected: ${fonts.system_fonts.detected_count}`);
                console.log(`  - Available Fonts: ${fonts.system_fonts.available_fonts?.slice(0, 5).join(', ') || 'None'}...`);
            }
            
            if (fonts.web_font_support) {
                const webFonts = fonts.web_font_support;
                console.log(`  - WOFF Support: ${webFonts.woff ? '✓' : '✗'}`);
                console.log(`  - WOFF2 Support: ${webFonts.woff2 ? '✓' : '✗'}`);
            }
            
            if (fonts.emoji_support) {
                console.log(`  - Emoji Support: ${(fonts.emoji_support.overall_support * 100).toFixed(1)}%`);
            }
        }
        
        console.log('✅ Browser API Availability & Behavior:');
        if (browserCharacteristics.api_availability) {
            const apis = browserCharacteristics.api_availability;
            
            console.log('  - Core APIs:');
            if (apis.dom_apis) {
                console.log(`    • Custom Elements: ${apis.dom_apis.custom_elements ? '✓' : '✗'}`);
                console.log(`    • Shadow DOM: ${apis.dom_apis.shadow_dom ? '✓' : '✗'}`);
                console.log(`    • Intersection Observer: ${apis.dom_apis.intersection_observer ? '✓' : '✗'}`);
            }
            
            console.log('  - Storage APIs:');
            if (apis.storage_apis) {
                console.log(`    • IndexedDB: ${apis.storage_apis.indexed_db ? '✓' : '✗'}`);
                console.log(`    • Cache API: ${apis.storage_apis.cache_api ? '✓' : '✗'}`);
                console.log(`    • Persistent Storage: ${apis.storage_apis.persistent_storage ? '✓' : '✗'}`);
            }
            
            console.log('  - Media APIs:');
            if (apis.media_apis) {
                console.log(`    • WebRTC: ${apis.media_apis.web_rtc ? '✓' : '✗'}`);
                console.log(`    • Media Recorder: ${apis.media_apis.media_recorder ? '✓' : '✗'}`);
                console.log(`    • Web Audio: ${apis.media_apis.web_audio ? '✓' : '✗'}`);
            }
            
            console.log('  - Modern APIs:');
            if (apis.modern_apis) {
                console.log(`    • Payment Request: ${browserCharacteristics.web_apis?.payment_request ? '✓' : '✗'}`);
                console.log(`    • Web Share: ${apis.modern_apis.share_api ? '✓' : '✗'}`);
                console.log(`    • Wake Lock: ${apis.modern_apis.wake_lock ? '✓' : '✗'}`);
            }
        }
        
        // Example 3: Performance Benchmarking Results
        console.log('\n⚡ Performance Benchmarking Results:');
        if (deviceFingerprint.performance_benchmarks) {
            const perf = deviceFingerprint.performance_benchmarks;
            console.log(`  - CPU Performance: ${perf.cpu_performance?.score?.toFixed(2) || 'N/A'}`);
            console.log(`  - Memory Performance: ${perf.memory_performance?.score?.toFixed(2) || 'N/A'}`);
            console.log(`  - Graphics Performance: ${perf.graphics_performance?.score?.toFixed(2) || 'N/A'}`);
            console.log(`  - Overall Score: ${perf.overall_score?.toFixed(2) || 'N/A'}`);
        }
        
        // Example 4: Fingerprinting Hashes
        console.log('\n🔒 Unique Fingerprinting Hashes:');
        if (deviceFingerprint.canvas_fingerprint) {
            console.log(`  - Canvas Hash: ${deviceFingerprint.canvas_fingerprint.canvas_hash || 'N/A'}`);
        }
        if (deviceFingerprint.webgl_fingerprint) {
            console.log(`  - WebGL Hash: ${deviceFingerprint.webgl_fingerprint.pixel_hash || 'N/A'}`);
        }
        if (browserCharacteristics.rendering_fingerprint) {
            const rendering = browserCharacteristics.rendering_fingerprint;
            console.log(`  - CSS Hash: ${rendering.css_fingerprint?.css_hash || 'N/A'}`);
            console.log(`  - Font Hash: ${rendering.font_fingerprint?.font_hash || 'N/A'}`);
        }
        
        console.log('\n🎯 Fingerprinting Summary:');
        console.log(`  - Device fingerprint data size: ${JSON.stringify(deviceFingerprint).length} characters`);
        console.log(`  - Browser characteristics data size: ${JSON.stringify(browserCharacteristics).length} characters`);
        console.log(`  - Total unique data points: ${Object.keys({...deviceFingerprint, ...browserCharacteristics}).length}`);
        
        console.log('\n✨ Phase 3.4 Enhanced Fingerprinting Example Complete!');
        
        return {
            device_fingerprint: deviceFingerprint,
            browser_characteristics: browserCharacteristics
        };
        
    } catch (error) {
        console.error('❌ Error in fingerprinting example:', error);
        throw error;
    }
}

/**
 * Example: Specific Feature Testing
 */
export async function specificFeatureExample() {
    console.log('🎯 Testing Specific Fingerprinting Features\n');
    
    const collector = new SessionFingerprintCollector();
    
    try {
        // Test Canvas Fingerprinting
        console.log('🎨 Canvas Fingerprinting:');
        const canvasFingerprint = await collector.generateCanvasFingerprint();
        console.log(`  - Canvas Hash: ${canvasFingerprint.canvas_hash}`);
        console.log(`  - Image Data Length: ${canvasFingerprint.image_data_length}`);
        
        // Test WebGL Fingerprinting  
        console.log('\n🔺 WebGL Fingerprinting:');
        const webglFingerprint = await collector.generateWebGLFingerprint();
        if (webglFingerprint.supported) {
            console.log(`  - WebGL Support: ✓`);
            console.log(`  - Pixel Hash: ${webglFingerprint.pixel_hash}`);
            console.log(`  - GPU Vendor: ${webglFingerprint.webgl_info?.vendor || 'Unknown'}`);
        } else {
            console.log('  - WebGL Support: ✗');
        }
        
        // Test CPU Performance
        console.log('\n💻 CPU Performance Benchmarking:');
        const cpuBenchmark = await collector.benchmarkCPUPerformance();
        console.log(`  - Performance Score: ${cpuBenchmark.score.toFixed(2)}`);
        console.log(`  - Execution Time: ${cpuBenchmark.time.toFixed(2)}ms`);
        
        // Test Font Detection
        console.log('\n🔤 Font Detection:');
        const fontAnalysis = await collector.collectFontAnalysis();
        if (fontAnalysis.system_fonts) {
            console.log(`  - Fonts Detected: ${fontAnalysis.system_fonts.detected_count}`);
            console.log(`  - Sample Fonts: ${fontAnalysis.system_fonts.available_fonts?.slice(0, 3).join(', ') || 'None'}`);
        }
        
        console.log('\n✅ Specific Feature Testing Complete!');
        
    } catch (error) {
        console.error('❌ Error in specific feature testing:', error);
        throw error;
    }
}

// Export examples for use
export default {
    comprehensiveExample,
    specificFeatureExample
};

// Auto-setup for browser console testing
if (typeof window !== 'undefined') {
    window.fingerprintingExamples = {
        comprehensive: comprehensiveExample,
        specific: specificFeatureExample
    };
    
    console.log('🔐 Phase 3.4 Fingerprinting Examples Ready!');
    console.log('💡 Available commands:');
    console.log('  - fingerprintingExamples.comprehensive() - Run comprehensive example');
    console.log('  - fingerprintingExamples.specific() - Test specific features');
}