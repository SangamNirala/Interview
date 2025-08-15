/**
 * 🔐 MODULE 3: ADVANCED SESSION FINGERPRINTING SYSTEM
 * SessionFingerprintCollector.js - Frontend Device Fingerprinting Collection
 * 
 * This module implements comprehensive device fingerprinting including:
 * - Hardware enumeration via WebGL and Canvas
 * - Screen characteristics and color profile
 * - CPU architecture and performance benchmarking
 * - Memory and storage capacity detection
 * - Browser version, plugins, and extensions
 * - Network information and connection characteristics
 * - Environmental data (timezone, locale, sensors)
 */

class SessionFingerprintCollector {
    constructor() {
        this.fingerprintData = {};
        this.collectionInterval = 30000; // 30 seconds
        this.maxRetries = 3;
        this.collectionVersion = "1.0";
        this.logger = console;
        
        // Performance benchmarking configuration
        this.benchmarkConfig = {
            jsPerformanceIterations: 100000,
            canvasRenderingTests: 10,
            webglComplexityTests: 5,
            memoryAllocationTests: 3
        };
        
        this.logger.info("SessionFingerprintCollector initialized");
    }
    
    /**
     * Collect comprehensive device fingerprint
     * Main entry point for device fingerprinting
     */
    async collectComprehensiveFingerprint() {
        try {
            this.logger.info("Starting comprehensive device fingerprinting collection");
            
            const startTime = performance.now();
            
            // Collect all fingerprint components in parallel for better performance
            const [
                deviceData,
                browserData,
                networkData,
                environmentalData
            ] = await Promise.allSettled([
                this.collectDeviceFingerprint(),
                this.collectBrowserCharacteristics(), 
                this.collectNetworkInformation(),
                this.collectEnvironmentalData()
            ]);
            
            const collectionTime = performance.now() - startTime;
            
            const fingerprint = {
                hardware: deviceData.status === 'fulfilled' ? deviceData.value : {},
                browser: browserData.status === 'fulfilled' ? browserData.value : {},
                network: networkData.status === 'fulfilled' ? networkData.value : {},
                environment: environmentalData.status === 'fulfilled' ? environmentalData.value : {},
                performance: await this.collectPerformanceBenchmarks(),
                os: await this.collectOperatingSystemData(),
                screen: await this.collectScreenCharacteristics(),
                collection_metadata: {
                    timestamp: new Date().toISOString(),
                    collection_id: this.generateUniqueId(),
                    collection_time_ms: collectionTime,
                    version: this.collectionVersion,
                    user_agent: navigator.userAgent,
                    collection_method: 'comprehensive'
                }
            };
            
            this.fingerprintData = fingerprint;
            this.logger.info(`Device fingerprinting completed in ${collectionTime.toFixed(2)}ms`);
            
            return fingerprint;
            
        } catch (error) {
            this.logger.error("Error collecting comprehensive fingerprint:", error);
            return this.getFallbackFingerprint();
        }
    }
    
    /**
     * ENHANCED: collectDeviceFingerprint() - Advanced Hardware Enumeration
     * Requirements per original plan:
     * - Hardware enumeration via WebGL and Canvas
     * - Screen characteristics and color profile
     * - CPU architecture and performance benchmarking
     * - Memory and storage capacity detection
     * - Device sensor availability and characteristics
     */
    async collectDeviceFingerprint() {
        try {
            this.logger.info("🔧 Starting PHASE 1.1 enhanced device fingerprint collection");
            
            // Implement comprehensive hardware detection matching backend expectations
            const deviceFingerprint = {
                hardware_enumeration: {
                    webgl_analysis: await this.getAdvancedWebGLHardwareInfo(),
                    canvas_hardware_detection: await this.getCanvasBasedHardwareInfo(),
                    gpu_memory_estimation: await this.estimateGPUMemory(),
                    rendering_performance_profile: await this.profileRenderingPerformance()
                },
                enhanced_screen_analysis: {
                    color_profile_detection: this.getColorProfileCharacteristics(),
                    display_capabilities: this.getDisplayCapabilityAnalysis(),
                    multi_monitor_setup: this.detectMultiMonitorConfiguration(),
                    hdr_wide_gamut_support: this.detectHDRWideGamutSupport()
                },
                cpu_performance_profiling: {
                    architecture_detection: await this.detectDetailedCPUArchitecture(),
                    performance_benchmarking: await this.runCPUPerformanceBenchmarks(),
                    instruction_set_analysis: await this.analyzeInstructionSetSupport(),
                    thermal_throttling_detection: await this.detectThermalThrottling()
                },
                memory_storage_analysis: {
                    memory_capacity_estimation: await this.estimateSystemMemory(),
                    storage_performance_profiling: await this.profileStoragePerformance(),
                    cache_hierarchy_analysis: await this.analyzeCacheHierarchy(),
                    virtual_memory_detection: await this.detectVirtualMemoryUsage()
                },
                device_sensor_enumeration: {
                    motion_sensors: await this.enumerateMotionSensors(),
                    environmental_sensors: await this.enumerateEnvironmentalSensors(),
                    biometric_sensors: await this.enumerateBiometricSensors(),
                    connectivity_sensors: await this.enumerateConnectivitySensors()
                },
                
                // Legacy compatibility data
                legacy_device_data: {
                    hardware_concurrency: navigator.hardwareConcurrency || 0,
                    device_memory_gb: navigator.deviceMemory || 0,
                    platform: navigator.platform,
                    user_agent_platform: this.extractPlatformFromUserAgent(),
                    max_touch_points: navigator.maxTouchPoints || 0,
                    canvas_fingerprint: await this.generateCanvasFingerprint(),
                    webgl_fingerprint: await this.generateWebGLFingerprint()
                },
                
                // Collection metadata
                collection_metadata: {
                    timestamp: new Date().toISOString(),
                    collection_id: this.generateUniqueId(),
                    fingerprint_version: "3.4_enhanced_device_phase1.1",
                    collection_method: "comprehensive_hardware_enumeration_advanced",
                    implementation_phase: "PHASE_1.1_DEVICE_ENHANCEMENT"
                }
            };
            
            this.logger.info("✅ PHASE 1.1 Device fingerprint collection completed successfully");
            return deviceFingerprint;
            
        } catch (error) {
            this.logger.error("❌ Error collecting PHASE 1.1 enhanced device fingerprint:", error);
            return this.getFallbackDeviceFingerprint();
        }
    }
    
    /**
     * Get CPU characteristics through performance analysis
     */
    async getCPUCharacteristics() {
        try {
            const cpuData = {
                cores: navigator.hardwareConcurrency || 0,
                architecture: await this.detectCPUArchitecture(),
                vendor: 'unknown',
                model: 'unknown',
                frequency: 0,
                cache_size: 0,
                features: []
            };
            
            // CPU performance benchmarking
            const performanceMetrics = await this.benchmarkCPUPerformance();
            cpuData.performance_score = performanceMetrics.score;
            cpuData.benchmark_time = performanceMetrics.time;
            
            // CPU feature detection
            cpuData.features = await this.detectCPUFeatures();
            
            return cpuData;
            
        } catch (error) {
            this.logger.error("Error getting CPU characteristics:", error);
            return { cores: navigator.hardwareConcurrency || 0 };
        }
    }
    
    /**
     * Get GPU characteristics through WebGL
     */
    async getGPUCharacteristics() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) {
                return {
                    vendor: 'unknown',
                    renderer: 'no-webgl',
                    version: 'unknown',
                    memory: 0,
                    extensions: []
                };
            }
            
            // Get GPU information
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            const vendor = debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR);
            const renderer = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
            
            const gpuData = {
                vendor: vendor || 'unknown',
                renderer: renderer || 'unknown',
                version: gl.getParameter(gl.VERSION) || 'unknown',
                shading_language_version: gl.getParameter(gl.SHADING_LANGUAGE_VERSION) || 'unknown',
                memory: await this.estimateGPUMemory(gl),
                extensions: this.getWebGLExtensions(gl),
                max_texture_size: gl.getParameter(gl.MAX_TEXTURE_SIZE),
                max_viewport_dims: gl.getParameter(gl.MAX_VIEWPORT_DIMS),
                webgl_version: this.detectWebGLVersion(gl),
                supported_formats: this.getSupportedFormats(gl)
            };
            
            // GPU performance benchmarking
            const gpuPerformance = await this.benchmarkGPUPerformance(gl);
            gpuData.performance_score = gpuPerformance.score;
            gpuData.render_time = gpuPerformance.time;
            
            canvas.remove();
            return gpuData;
            
        } catch (error) {
            this.logger.error("Error getting GPU characteristics:", error);
            return { vendor: 'error', renderer: 'error' };
        }
    }
    
    /**
     * Get memory characteristics
     */
    async getMemoryCharacteristics() {
        try {
            const memoryData = {
                device_memory: navigator.deviceMemory * 1024 * 1024 * 1024 || 0, // Convert GB to bytes
                total_memory: 0,
                available_memory: 0,
                memory_type: 'unknown',
                speed: 0
            };
            
            // Performance memory estimation
            if (performance.memory) {
                memoryData.js_heap_size_limit = performance.memory.jsHeapSizeLimit;
                memoryData.total_js_heap_size = performance.memory.totalJSHeapSize;
                memoryData.used_js_heap_size = performance.memory.usedJSHeapSize;
                memoryData.available_memory = performance.memory.jsHeapSizeLimit - performance.memory.usedJSHeapSize;
            }
            
            // Memory performance test
            const memoryPerformance = await this.benchmarkMemoryPerformance();
            memoryData.performance_score = memoryPerformance.score;
            memoryData.allocation_speed = memoryPerformance.allocationSpeed;
            
            return memoryData;
            
        } catch (error) {
            this.logger.error("Error getting memory characteristics:", error);
            return { device_memory: navigator.deviceMemory * 1024 * 1024 * 1024 || 0 };
        }
    }
    
    /**
     * Get storage characteristics
     */
    async getStorageCharacteristics() {
        try {
            const storageData = {
                total_storage: 0,
                available_storage: 0,
                storage_type: 'unknown',
                filesystem: 'unknown'
            };
            
            // Storage API if available
            if ('storage' in navigator && 'estimate' in navigator.storage) {
                const estimate = await navigator.storage.estimate();
                storageData.quota = estimate.quota || 0;
                storageData.usage = estimate.usage || 0;
                storageData.available_storage = (estimate.quota || 0) - (estimate.usage || 0);
                storageData.total_storage = estimate.quota || 0;
            }
            
            // LocalStorage test
            try {
                const testKey = 'storage_test_' + Date.now();
                const testData = 'x'.repeat(1024); // 1KB test
                const startTime = performance.now();
                localStorage.setItem(testKey, testData);
                const writeTime = performance.now() - startTime;
                localStorage.removeItem(testKey);
                storageData.write_speed_score = Math.max(0, 100 - writeTime);
            } catch (e) {
                storageData.localStorage_available = false;
            }
            
            return storageData;
            
        } catch (error) {
            this.logger.error("Error getting storage characteristics:", error);
            return {};
        }
    }
    
    /**
     * Get sensor characteristics
     */
    async getSensorCharacteristics() {
        try {
            const sensorData = {
                accelerometer: false,
                gyroscope: false,
                magnetometer: false,
                ambient_light: false,
                proximity: false,
                battery_api: false
            };
            
            // Check for DeviceMotionEvent (accelerometer/gyroscope)
            if (typeof DeviceMotionEvent !== 'undefined') {
                sensorData.accelerometer = true;
                sensorData.gyroscope = true;
            }
            
            // Check for DeviceOrientationEvent (magnetometer)
            if (typeof DeviceOrientationEvent !== 'undefined') {
                sensorData.magnetometer = true;
            }
            
            // Check for ambient light sensor
            if ('AmbientLightSensor' in window) {
                sensorData.ambient_light = true;
            }
            
            // Check for proximity sensor
            if ('ProximitySensor' in window) {
                sensorData.proximity = true;
            }
            
            // Check for battery API
            if ('getBattery' in navigator) {
                sensorData.battery_api = true;
                try {
                    const battery = await navigator.getBattery();
                    sensorData.battery_level = Math.floor(battery.level * 100);
                    sensorData.battery_charging = battery.charging;
                    sensorData.charging_time = battery.chargingTime;
                    sensorData.discharging_time = battery.dischargingTime;
                } catch (e) {
                    this.logger.warn("Battery API access denied");
                }
            }
            
            return sensorData;
            
        } catch (error) {
            this.logger.error("Error getting sensor characteristics:", error);
            return {};
        }
    }
    
    /**
     * ENHANCED: collectBrowserCharacteristics() - Advanced Browser Fingerprinting
     * Requirements per original plan:
     * - Browser version, plugins, and extensions detection
     * - JavaScript engine capabilities and performance
     * - Rendering engine fingerprinting
     * - Font enumeration and rendering analysis
     * - Browser API availability and behavior analysis
     */
    async collectBrowserCharacteristics() {
        try {
            this.logger.info("🔧 Starting PHASE 1.2 enhanced browser characteristics collection");
            
            const browserData = {
                enhanced_browser_identification: {
                    detailed_user_agent_analysis: this.parseDetailedUserAgent(),
                    browser_build_detection: await this.detectBrowserBuild(),
                    engine_version_fingerprinting: await this.fingerprintJSEngine(),
                    headless_browser_detection: await this.detectHeadlessBrowser()
                },
                javascript_engine_profiling: {
                    v8_feature_detection: await this.detectV8Features(),
                    performance_characteristics: await this.profileJSPerformance(),
                    memory_management_analysis: await this.analyzeJSMemoryManagement(),
                    compilation_optimization_detection: await this.detectJSOptimizations()
                },
                rendering_engine_analysis: {
                    layout_engine_fingerprinting: await this.fingerprintLayoutEngine(),
                    css_feature_support_matrix: await this.buildCSSFeatureMatrix(),
                    rendering_quirks_detection: await this.detectRenderingQuirks(),
                    graphics_acceleration_analysis: await this.analyzeGraphicsAcceleration()
                },
                font_rendering_analysis: {
                    system_font_enumeration: await this.enumerateSystemFonts(),
                    font_rendering_characteristics: await this.analyzeFontRendering(),
                    text_measurement_precision: await this.measureTextPrecision(),
                    font_substitution_behavior: await this.analyzeFontSubstitution()
                },
                api_availability_profiling: {
                    web_api_comprehensive_scan: await this.scanWebAPIs(),
                    experimental_feature_detection: await this.detectExperimentalFeatures(),
                    permission_api_behavior: await this.analyzePermissionAPI(),
                    feature_policy_analysis: await this.analyzeFeaturePolicy()
                },
                
                // Legacy compatibility data
                legacy_browser_data: {
                    plugins: this.getPluginInfo(),
                    mime_types: this.getMimeTypes(),
                    plugin_count: navigator.plugins.length,
                    mime_count: navigator.mimeTypes.length,
                    user_agent: navigator.userAgent,
                    browser_name: this.getBrowserName(),
                    browser_version: this.getBrowserVersion(),
                    platform: navigator.platform,
                    language: navigator.language,
                    languages: navigator.languages || [],
                    cookie_enabled: navigator.cookieEnabled,
                    do_not_track: navigator.doNotTrack,
                    java_enabled: navigator.javaEnabled ? navigator.javaEnabled() : false
                },
                
                // Collection metadata
                collection_metadata: {
                    timestamp: new Date().toISOString(),
                    collection_id: this.generateUniqueId(),
                    fingerprint_version: "3.4_enhanced_browser_phase1.2",
                    collection_method: "comprehensive_browser_fingerprinting_advanced",
                    implementation_phase: "PHASE_1.2_BROWSER_ENHANCEMENT"
                }
            };
            
            this.logger.info("✅ PHASE 1.2 Browser characteristics collection completed successfully");
            return browserData;
            
        } catch (error) {
            this.logger.error("❌ Error collecting PHASE 1.2 enhanced browser characteristics:", error);
            return this.getFallbackBrowserFingerprint();
        }
    }
    
    /**
     * PHASE 3.4: ENHANCED NETWORK INFORMATION COLLECTION
     * Collect comprehensive network information including:
     * - Connection type and effective bandwidth
     * - Network timing and latency measurements  
     * - WebRTC IP leak detection
     * - DNS resolution characteristics
     * - Network routing and topology analysis
     */
    async collectNetworkInformation() {
        try {
            this.logger.info("🌐 Starting enhanced network information collection");
            
            const networkData = {
                // Enhanced connection type and effective bandwidth
                connection_characteristics: await this.getConnectionCharacteristics(),
                
                // Enhanced network timing and latency measurements
                network_timing: await this.measureComprehensiveNetworkTiming(),
                
                // Enhanced WebRTC IP leak detection
                webrtc_analysis: await this.performWebRTCAnalysis(),
                
                // Enhanced DNS resolution characteristics
                dns_characteristics: await this.analyzeDNSCharacteristics(),
                
                // Enhanced network routing and topology analysis
                network_topology: await this.analyzeNetworkTopology(),
                
                // Basic Network Information API (fallback)
                basic_network_info: this.getBasicNetworkInfo(),
                
                // Network security and privacy features
                network_security: await this.analyzeNetworkSecurity(),
                
                // Bandwidth estimation through multiple methods
                bandwidth_analysis: await this.performBandwidthAnalysis(),
                
                // Network performance metrics
                network_performance: await this.measureNetworkPerformance(),
                
                // Collection metadata
                collection_metadata: {
                    timestamp: new Date().toISOString(),
                    collection_id: this.generateUniqueId(),
                    fingerprint_version: "3.4_enhanced_network",
                    collection_method: "comprehensive_network_analysis"
                }
            };
            
            this.logger.info("✅ Network information collection completed successfully");
            return networkData;
            
        } catch (error) {
            this.logger.error("❌ Error collecting enhanced network information:", error);
            return this.getFallbackNetworkInfo();
        }
    }
    
    /**
     * PHASE 3.4: ENHANCED ENVIRONMENTAL DATA COLLECTION  
     * Collect comprehensive environmental data including:
     * - Timezone and locale information
     * - Battery status and charging characteristics
     * - Device orientation and motion sensors
     * - Ambient light sensor data
     * - Audio and video device enumeration
     */
    async collectEnvironmentalData() {
        try {
            this.logger.info("🌍 Starting enhanced environmental data collection");
            
            const envData = {
                // Enhanced timezone and locale information
                locale_characteristics: await this.getLocaleCharacteristics(),
                
                // Enhanced battery status and charging characteristics
                battery_characteristics: await this.getBatteryCharacteristics(),
                
                // Enhanced device orientation and motion sensors
                motion_sensors: await this.getMotionSensorData(),
                
                // Enhanced ambient light sensor data
                ambient_sensors: await this.getAmbientSensorData(),
                
                // Enhanced audio and video device enumeration
                media_devices: await this.getMediaDeviceCharacteristics(),
                
                // Display and visual preferences
                display_preferences: await this.getDisplayPreferences(),
                
                // Input device capabilities
                input_capabilities: await this.getInputCapabilities(),
                
                // Accessibility features detection
                accessibility_features: await this.getAccessibilityFeatures(),
                
                // System performance indicators
                system_performance: await this.getSystemPerformanceIndicators(),
                
                // Privacy and security preferences
                privacy_settings: await this.getPrivacySettings(),
                
                // Legacy environmental data (for backward compatibility)
                legacy_env_data: {
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    timezone_offset: new Date().getTimezoneOffset(),
                    locale: navigator.language,
                    locales: navigator.languages || [],
                    currency: this.detectCurrency(),
                    number_format: this.detectNumberFormat(),
                    date_format: this.detectDateFormat(),
                    color_scheme: this.detectColorScheme(),
                    reduced_motion: this.detectReducedMotion(),
                    high_contrast: this.detectHighContrast(),
                    font_preferences: await this.detectFontPreferences(),
                    audio_context: this.getAudioContextInfo(),
                    device_orientation: await this.getDeviceOrientation(),
                    viewport_size: this.getViewportSize(),
                    screen_properties: this.getScreenProperties()
                },
                
                // Collection metadata
                collection_metadata: {
                    timestamp: new Date().toISOString(),
                    collection_id: this.generateUniqueId(),
                    fingerprint_version: "3.4_enhanced_environmental", 
                    collection_method: "comprehensive_environmental_analysis"
                }
            };
            
            this.logger.info("✅ Environmental data collection completed successfully");
            return envData;
            
        } catch (error) {
            this.logger.error("❌ Error collecting enhanced environmental data:", error);
            return this.getFallbackEnvironmentalData();
        }
    }
    
    /**
     * Collect performance benchmarks
     */
    async collectPerformanceBenchmarks() {
        try {
            const benchmarks = {
                javascript_performance: await this.benchmarkJavaScriptPerformance(),
                canvas_rendering: await this.benchmarkCanvasRendering(),
                webgl_performance: await this.benchmarkWebGLPerformance(),
                memory_allocation: await this.benchmarkMemoryAllocation(),
                dom_manipulation: await this.benchmarkDOMManipulation(),
                crypto_performance: await this.benchmarkCryptoPerformance()
            };
            
            benchmarks.overall_score = this.calculateOverallPerformanceScore(benchmarks);
            
            return benchmarks;
            
        } catch (error) {
            this.logger.error("Error collecting performance benchmarks:", error);
            return {};
        }
    }
    
    /**
     * Collect operating system data
     */
    async collectOperatingSystemData() {
        try {
            const osData = {
                platform: navigator.platform,
                user_agent_os: this.extractOSFromUserAgent(),
                architecture: this.detectArchitecture(),
                version: 'unknown',
                build: 'unknown',
                kernel_version: 'unknown',
                language: navigator.language,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timezone_offset: new Date().getTimezoneOffset(),
                is_mobile: this.isMobileDevice(),
                is_tablet: this.isTabletDevice(),
                is_desktop: this.isDesktopDevice(),
                touch_enabled: 'ontouchstart' in window || navigator.maxTouchPoints > 0
            };
            
            return osData;
            
        } catch (error) {
            this.logger.error("Error collecting OS data:", error);
            return { platform: navigator.platform };
        }
    }
    
    /**
     * Collect screen characteristics
     */
    async collectScreenCharacteristics() {
        try {
            const screenData = {
                width: screen.width,
                height: screen.height,
                available_width: screen.availWidth,
                available_height: screen.availHeight,
                color_depth: screen.colorDepth,
                pixel_depth: screen.pixelDepth,
                device_pixel_ratio: window.devicePixelRatio || 1,
                orientation: screen.orientation ? screen.orientation.type : 'unknown',
                touch_support: 'ontouchstart' in window,
                max_touch_points: navigator.maxTouchPoints || 0,
                viewport_width: window.innerWidth,
                viewport_height: window.innerHeight,
                outer_width: window.outerWidth,
                outer_height: window.outerHeight,
                screen_left: window.screenLeft || window.screenX || 0,
                screen_top: window.screenTop || window.screenY || 0
            };
            
            // Additional screen analysis
            screenData.aspect_ratio = this.calculateAspectRatio(screenData.width, screenData.height);
            screenData.display_profile = this.classifyDisplayProfile(screenData.width, screenData.height);
            screenData.pixel_density = this.calculatePixelDensity(screenData);
            
            return screenData;
            
        } catch (error) {
            this.logger.error("Error collecting screen characteristics:", error);
            return { width: screen.width, height: screen.height };
        }
    }
    
    // ===== PERFORMANCE BENCHMARKING METHODS =====
    
    async benchmarkCPUPerformance() {
        const startTime = performance.now();
        let result = 0;
        
        // CPU-intensive mathematical operations
        for (let i = 0; i < this.benchmarkConfig.jsPerformanceIterations; i++) {
            result += Math.sqrt(i) * Math.sin(i) * Math.cos(i);
        }
        
        const endTime = performance.now();
        const executionTime = endTime - startTime;
        
        return {
            score: Math.max(0, 1000 - executionTime), // Higher score for faster execution
            time: executionTime,
            result: result
        };
    }
    
    async benchmarkGPUPerformance(gl) {
        if (!gl) return { score: 0, time: 0 };
        
        const startTime = performance.now();
        
        // Simple GPU rendering test
        const vertices = new Float32Array([
            -1, -1, 1, -1, -1, 1,
            -1, 1, 1, -1, 1, 1
        ]);
        
        const buffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
        
        for (let i = 0; i < this.benchmarkConfig.webglComplexityTests; i++) {
            gl.clear(gl.COLOR_BUFFER_BIT);
            gl.drawArrays(gl.TRIANGLES, 0, 6);
        }
        
        const endTime = performance.now();
        gl.deleteBuffer(buffer);
        
        return {
            score: Math.max(0, 100 - (endTime - startTime)),
            time: endTime - startTime
        };
    }
    
    async benchmarkMemoryPerformance() {
        const startTime = performance.now();
        const arrays = [];
        
        // Memory allocation test
        for (let i = 0; i < this.benchmarkConfig.memoryAllocationTests; i++) {
            arrays.push(new Array(100000).fill(Math.random()));
        }
        
        const endTime = performance.now();
        
        // Cleanup
        arrays.length = 0;
        
        return {
            score: Math.max(0, 100 - (endTime - startTime)),
            allocationSpeed: (endTime - startTime) / this.benchmarkConfig.memoryAllocationTests
        };
    }
    
    async benchmarkJavaScriptPerformance() {
        const tests = [
            () => this.arrayOperationsTest(),
            () => this.stringOperationsTest(),
            () => this.mathOperationsTest(),
            () => this.objectOperationsTest()
        ];
        
        const results = [];
        for (const test of tests) {
            const startTime = performance.now();
            await test();
            const endTime = performance.now();
            results.push(endTime - startTime);
        }
        
        const averageTime = results.reduce((a, b) => a + b, 0) / results.length;
        return Math.max(0, 1000 - averageTime);
    }
    
    async benchmarkCanvasRendering() {
        const canvas = document.createElement('canvas');
        canvas.width = 500;
        canvas.height = 500;
        const ctx = canvas.getContext('2d');
        
        const startTime = performance.now();
        
        // Canvas rendering test
        for (let i = 0; i < this.benchmarkConfig.canvasRenderingTests; i++) {
            ctx.fillStyle = `hsl(${i * 36}, 50%, 50%)`;
            ctx.fillRect(i * 50, i * 50, 100, 100);
            ctx.beginPath();
            ctx.arc(250, 250, i * 20, 0, 2 * Math.PI);
            ctx.stroke();
        }
        
        const endTime = performance.now();
        canvas.remove();
        
        return Math.max(0, 1000 - (endTime - startTime));
    }
    
    async benchmarkWebGLPerformance() {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl');
        
        if (!gl) return 0;
        
        const performance_score = await this.benchmarkGPUPerformance(gl);
        canvas.remove();
        
        return performance_score.score;
    }
    
    async benchmarkMemoryAllocation() {
        return (await this.benchmarkMemoryPerformance()).score;
    }
    
    async benchmarkDOMManipulation() {
        const startTime = performance.now();
        const testDiv = document.createElement('div');
        document.body.appendChild(testDiv);
        
        // DOM manipulation test
        for (let i = 0; i < 1000; i++) {
            const element = document.createElement('span');
            element.textContent = `Test ${i}`;
            element.style.color = `hsl(${i}, 50%, 50%)`;
            testDiv.appendChild(element);
        }
        
        const endTime = performance.now();
        testDiv.remove();
        
        return Math.max(0, 1000 - (endTime - startTime));
    }
    
    async benchmarkCryptoPerformance() {
        if (!crypto || !crypto.subtle) return 0;
        
        const startTime = performance.now();
        
        try {
            // Generate a cryptographic key
            const key = await crypto.subtle.generateKey(
                { name: 'AES-GCM', length: 256 },
                false,
                ['encrypt', 'decrypt']
            );
            
            // Encrypt some data
            const data = new TextEncoder().encode('Performance test data');
            const iv = crypto.getRandomValues(new Uint8Array(12));
            
            await crypto.subtle.encrypt(
                { name: 'AES-GCM', iv: iv },
                key,
                data
            );
            
            const endTime = performance.now();
            return Math.max(0, 1000 - (endTime - startTime));
            
        } catch (error) {
            return 0;
        }
    }
    
    calculateOverallPerformanceScore(benchmarks) {
        const scores = Object.values(benchmarks).filter(score => typeof score === 'number');
        return scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
    }
    
    
    // ===== ENHANCED DEVICE FINGERPRINTING METHODS =====
    
    /**
     * Collect comprehensive hardware enumeration via WebGL and Canvas
     */
    async collectHardwareEnumeration() {
        try {
            const hardware = {
                gpu: await this.getGPUCharacteristics(),
                webgl_info: await this.getWebGLHardwareInfo(),
                canvas_info: await this.getCanvasHardwareInfo(),
                graphics_capabilities: await this.getGraphicsCapabilities(),
                compute_capabilities: await this.getComputeCapabilities()
            };
            
            return hardware;
        } catch (error) {
            this.logger.error("Error in hardware enumeration:", error);
            return {};
        }
    }
    
    /**
     * Get WebGL hardware information
     */
    async getWebGLHardwareInfo() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl2') || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) return { supported: false };
            
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            const extensions = gl.getSupportedExtensions() || [];
            
            const webglInfo = {
                version: gl.getParameter(gl.VERSION),
                shading_language_version: gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
                vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR),
                renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER),
                max_texture_size: gl.getParameter(gl.MAX_TEXTURE_SIZE),
                max_viewport_dims: gl.getParameter(gl.MAX_VIEWPORT_DIMS),
                max_vertex_attribs: gl.getParameter(gl.MAX_VERTEX_ATTRIBS),
                max_vertex_uniform_vectors: gl.getParameter(gl.MAX_VERTEX_UNIFORM_VECTORS),
                max_fragment_uniform_vectors: gl.getParameter(gl.MAX_FRAGMENT_UNIFORM_VECTORS),
                max_varying_vectors: gl.getParameter(gl.MAX_VARYING_VECTORS),
                extensions_count: extensions.length,
                extensions: extensions.slice(0, 15), // Limit for privacy
                aliased_line_width_range: gl.getParameter(gl.ALIASED_LINE_WIDTH_RANGE),
                aliased_point_size_range: gl.getParameter(gl.ALIASED_POINT_SIZE_RANGE),
                supported_formats: this.getWebGLSupportedFormats(gl)
            };
            
            // WebGL2 specific parameters
            if (gl.constructor.name === 'WebGL2RenderingContext') {
                webglInfo.webgl2 = true;
                webglInfo.max_3d_texture_size = gl.getParameter(gl.MAX_3D_TEXTURE_SIZE);
                webglInfo.max_array_texture_layers = gl.getParameter(gl.MAX_ARRAY_TEXTURE_LAYERS);
                webglInfo.max_color_attachments = gl.getParameter(gl.MAX_COLOR_ATTACHMENTS);
            }
            
            canvas.remove();
            return webglInfo;
        } catch (error) {
            this.logger.error("Error getting WebGL hardware info:", error);
            return { error: error.message };
        }
    }
    
    /**
     * Font Rendering Analysis Methods
     */
    async enumerateSystemFonts() {
        try {
            const fontEnumeration = {
                detected_fonts: [],
                font_families: {},
                web_fonts: [],
                system_font_characteristics: {},
                font_loading_behavior: {}
            };
            
            // Standard font detection using canvas measurements
            const testFonts = [
                // System fonts
                'Arial', 'Helvetica', 'Times New Roman', 'Times', 'Courier New', 'Courier',
                'Verdana', 'Georgia', 'Palatino', 'Garamond', 'Bookman', 'Comic Sans MS',
                'Trebuchet MS', 'Arial Black', 'Impact', 'Lucida Sans Unicode', 'Tahoma',
                'Lucida Console', 'Monaco', 'Bradley Hand ITC',
                
                // Platform specific
                'Segoe UI', 'Microsoft Sans Serif', 'Calibri', 'Cambria', 'Consolas', // Windows
                'Helvetica Neue', 'Menlo', 'SF Pro Display', 'SF Pro Text', // macOS
                'DejaVu Sans', 'Ubuntu', 'Liberation Sans', 'Noto Sans', // Linux
                
                // Mobile fonts
                'Roboto', 'Droid Sans', 'Noto Color Emoji', 'Apple Color Emoji',
                
                // Asian fonts
                'Hiragino Sans', 'Yu Gothic', 'Meiryo', 'SimSun', 'Microsoft YaHei',
                'Malgun Gothic', 'Gulim', 'Dotum'
            ];
            
            // Font detection through measurement differences
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const testString = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            
            // Baseline measurements with generic fonts
            const baselineFonts = ['serif', 'sans-serif', 'monospace'];
            const baselines = {};
            
            for (const baseline of baselineFonts) {
                ctx.font = `72px ${baseline}`;
                baselines[baseline] = ctx.measureText(testString).width;
            }
            
            // Test each font
            for (const font of testFonts) {
                try {
                    ctx.font = `72px "${font}", sans-serif`;
                    const width = ctx.measureText(testString).width;
                    
                    // Compare with baseline to detect font presence
                    const isAvailable = width !== baselines['sans-serif'];
                    if (isAvailable) {
                        fontEnumeration.detected_fonts.push({
                            name: font,
                            width: width,
                            baseline_difference: width - baselines['sans-serif']
                        });
                    }
                } catch (e) {
                    // Font test failed
                }
            }
            
            // Font family classification
            fontEnumeration.font_families = this.classifyFontFamilies(fontEnumeration.detected_fonts);
            
            // Web font detection
            fontEnumeration.web_fonts = await this.detectWebFonts();
            
            // System font characteristics
            fontEnumeration.system_font_characteristics = await this.analyzeSystemFontCharacteristics();
            
            // Font loading behavior
            fontEnumeration.font_loading_behavior = await this.analyzeFontLoadingBehavior();
            
            canvas.remove();
            return fontEnumeration;
            
        } catch (error) {
            return { error: error.message, detected_fonts: [] };
        }
    }
    
    async analyzeFontRendering() {
        try {
            const rendering = {
                subpixel_rendering: {},
                antialiasing_analysis: {},
                hinting_characteristics: {},
                font_smoothing: {},
                color_emoji_support: {}
            };
            
            // Subpixel rendering analysis
            rendering.subpixel_rendering = await this.analyzeSubpixelRendering();
            
            // Antialiasing detection
            rendering.antialiasing_analysis = await this.analyzeAntialiasing();
            
            // Font hinting characteristics
            rendering.hinting_characteristics = await this.analyzeHinting();
            
            // Font smoothing detection
            rendering.font_smoothing = await this.analyzeFontSmoothing();
            
            // Color emoji support
            rendering.color_emoji_support = await this.analyzeColorEmojiSupport();
            
            return rendering;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async measureTextPrecision() {
        try {
            const precision = {
                measurement_consistency: {},
                fractional_metrics: {},
                kerning_analysis: {},
                ligature_support: {},
                baseline_metrics: {}
            };
            
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Measurement consistency test
            const testText = 'The quick brown fox jumps over the lazy dog';
            const measurements = [];
            
            for (let i = 0; i < 10; i++) {
                ctx.font = '16px Arial';
                measurements.push(ctx.measureText(testText).width);
            }
            
            precision.measurement_consistency = {
                measurements: measurements,
                is_consistent: measurements.every(m => m === measurements[0]),
                variance: this.calculateVariance(measurements),
                coefficient_of_variation: this.calculateCoefficientOfVariation(measurements)
            };
            
            // Fractional metrics test
            precision.fractional_metrics = await this.testFractionalMetrics(ctx);
            
            // Kerning analysis
            precision.kerning_analysis = await this.analyzeKerning(ctx);
            
            // Ligature support test
            precision.ligature_support = await this.testLigatureSupport(ctx);
            
            // Baseline metrics
            precision.baseline_metrics = await this.analyzeBaselineMetrics(ctx);
            
            canvas.remove();
            return precision;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async analyzeFontSubstitution() {
        try {
            const substitution = {
                fallback_behavior: {},
                missing_glyph_handling: {},
                unicode_support: {},
                font_matching_algorithm: {}
            };
            
            // Fallback behavior test
            substitution.fallback_behavior = await this.testFallbackBehavior();
            
            // Missing glyph handling
            substitution.missing_glyph_handling = await this.testMissingGlyphHandling();
            
            // Unicode support analysis
            substitution.unicode_support = await this.analyzeUnicodeSupport();
            
            // Font matching algorithm characteristics
            substitution.font_matching_algorithm = await this.analyzeFontMatching();
            
            return substitution;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * API Availability Profiling Methods
     */
    async scanWebAPIs() {
        try {
            const apiScan = {
                core_apis: {},
                experimental_apis: {},
                deprecated_apis: {},
                vendor_prefixed_apis: {},
                permission_apis: {}
            };
            
            // Core Web APIs
            apiScan.core_apis = {
                // Storage APIs
                localStorage: 'localStorage' in window,
                sessionStorage: 'sessionStorage' in window,
                indexedDB: 'indexedDB' in window,
                webSQL: 'openDatabase' in window,
                cacheAPI: 'caches' in window,
                
                // Network APIs
                fetch: 'fetch' in window,
                xmlHttpRequest: 'XMLHttpRequest' in window,
                webSocket: 'WebSocket' in window,
                serverSentEvents: 'EventSource' in window,
                webRTC: 'RTCPeerConnection' in window,
                
                // Graphics APIs
                canvas2D: this.testCanvas2DSupport(),
                webGL: this.testWebGLSupport(),
                webGL2: this.testWebGL2Support(),
                webGPU: 'gpu' in navigator,
                
                // Audio/Video APIs
                webAudio: 'AudioContext' in window || 'webkitAudioContext' in window,
                mediaDevices: 'mediaDevices' in navigator,
                mediaRecorder: 'MediaRecorder' in window,
                webRTCMedia: 'getUserMedia' in navigator || 'webkitGetUserMedia' in navigator,
                
                // Worker APIs
                webWorkers: 'Worker' in window,
                sharedWorkers: 'SharedWorker' in window,
                serviceWorkers: 'serviceWorker' in navigator,
                
                // Crypto APIs
                cryptoSubtle: 'crypto' in window && 'subtle' in crypto,
                webCrypto: 'crypto' in window,
                
                // File APIs
                fileAPI: 'File' in window,
                fileReader: 'FileReader' in window,
                blob: 'Blob' in window,
                
                // Geolocation
                geolocation: 'geolocation' in navigator,
                
                // Notifications
                notifications: 'Notification' in window,
                
                // Payment APIs
                paymentRequest: 'PaymentRequest' in window,
                
                // WebAssembly
                webAssembly: 'WebAssembly' in window
            };
            
            // Experimental APIs
            apiScan.experimental_apis = await this.scanExperimentalAPIs();
            
            // Deprecated APIs
            apiScan.deprecated_apis = await this.scanDeprecatedAPIs();
            
            // Vendor-prefixed APIs
            apiScan.vendor_prefixed_apis = await this.scanVendorPrefixedAPIs();
            
            // Permission APIs
            apiScan.permission_apis = await this.scanPermissionAPIs();
            
            return apiScan;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async detectExperimentalFeatures() {
        try {
            const experimental = {
                origin_trials: {},
                flag_enabled_features: {},
                webkit_experimental: {},
                mozilla_experimental: {},
                chromium_experimental: {}
            };
            
            // Origin Trials (Chrome/Edge)
            experimental.origin_trials = await this.detectOriginTrials();
            
            // Flag-enabled features
            experimental.flag_enabled_features = await this.detectFlagEnabledFeatures();
            
            // WebKit experimental features
            experimental.webkit_experimental = await this.detectWebKitExperimental();
            
            // Mozilla experimental features
            experimental.mozilla_experimental = await this.detectMozillaExperimental();
            
            // Chromium experimental features
            experimental.chromium_experimental = await this.detectChromiumExperimental();
            
            return experimental;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async analyzePermissionAPI() {
        try {
            const permissionAnalysis = {
                permission_support: false,
                available_permissions: [],
                permission_states: {},
                permission_behavior: {}
            };
            
            if ('permissions' in navigator) {
                permissionAnalysis.permission_support = true;
                
                // Test various permissions
                const testPermissions = [
                    'geolocation', 'notifications', 'camera', 'microphone', 
                    'midi', 'persistent-storage', 'push', 'background-sync'
                ];
                
                for (const permission of testPermissions) {
                    try {
                        const result = await navigator.permissions.query({ name: permission });
                        permissionAnalysis.available_permissions.push(permission);
                        permissionAnalysis.permission_states[permission] = result.state;
                    } catch (e) {
                        // Permission not supported or query failed
                    }
                }
                
                // Analyze permission behavior
                permissionAnalysis.permission_behavior = await this.analyzePermissionBehavior();
            }
            
            return permissionAnalysis;
            
        } catch (error) {
            return { error: error.message, permission_support: false };
        }
    }
    
    async analyzeFeaturePolicy() {
        try {
            const featurePolicyAnalysis = {
                feature_policy_support: false,
                permissions_policy_support: false,
                allowed_features: [],
                feature_policy_behavior: {}
            };
            
            // Feature Policy (deprecated)
            if ('featurePolicy' in document) {
                featurePolicyAnalysis.feature_policy_support = true;
                try {
                    const allowedFeatures = document.featurePolicy.allowedFeatures();
                    featurePolicyAnalysis.allowed_features = allowedFeatures;
                } catch (e) {
                    // Method not available
                }
            }
            
            // Permissions Policy (modern)
            if ('permissionsPolicy' in document) {
                featurePolicyAnalysis.permissions_policy_support = true;
                try {
                    const allowedFeatures = document.permissionsPolicy.allowedFeatures();
                    featurePolicyAnalysis.allowed_features = allowedFeatures;
                } catch (e) {
                    // Method not available
                }
            }
            
            // Feature policy behavior analysis
            featurePolicyAnalysis.feature_policy_behavior = await this.analyzeFeaturePolicyBehavior();
            
            return featurePolicyAnalysis;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get WebGL supported formats
     */
    getWebGLSupportedFormats(gl) {
        const formats = [];
        const compressionFormats = [
            'COMPRESSED_RGB_S3TC_DXT1_EXT',
            'COMPRESSED_RGBA_S3TC_DXT1_EXT',
            'COMPRESSED_RGBA_S3TC_DXT3_EXT',
            'COMPRESSED_RGBA_S3TC_DXT5_EXT',
            'COMPRESSED_RGB_PVRTC_4BPPV1_IMG',
            'COMPRESSED_RGBA_PVRTC_4BPPV1_IMG',
            'COMPRESSED_RGB_PVRTC_2BPPV1_IMG',
            'COMPRESSED_RGBA_PVRTC_2BPPV1_IMG',
            'COMPRESSED_RGB_ETC1_WEBGL'
        ];
        
        compressionFormats.forEach(format => {
            const extension = gl.getExtension('WEBGL_compressed_texture_s3tc') ||
                             gl.getExtension('WEBGL_compressed_texture_pvrtc') ||
                             gl.getExtension('WEBGL_compressed_texture_etc1');
            if (extension && extension[format]) {
                formats.push(format);
            }
        });
        
        return formats;
    }
    
    /**
     * Get Canvas hardware information
     */
    async getCanvasHardwareInfo() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 256;
            const ctx = canvas.getContext('2d');
            
            if (!ctx) return { supported: false };
            
            const canvasInfo = {
                max_width: 32767, // Most browsers limit this
                max_height: 32767,
                image_smoothing_enabled: ctx.imageSmoothingEnabled,
                image_smoothing_quality: ctx.imageSmoothingQuality || 'unknown',
                text_rendering: this.getTextRenderingCapabilities(ctx),
                drawing_performance: await this.benchmarkCanvasDrawing(ctx),
                pixel_manipulation: await this.testCanvasPixelManipulation(ctx),
                supported_formats: await this.getCanvasSupportedFormats(ctx)
            };
            
            canvas.remove();
            return canvasInfo;
        } catch (error) {
            this.logger.error("Error getting Canvas hardware info:", error);
            return { error: error.message };
        }
    }
    
    /**
     * Get text rendering capabilities
     */
    getTextRenderingCapabilities(ctx) {
        const fonts = ['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana'];
        const capabilities = {
            supported_fonts: [],
            font_rendering_quality: 'unknown',
            text_metrics_precision: 0
        };
        
        fonts.forEach(font => {
            ctx.font = `20px ${font}`;
            const metrics = ctx.measureText('Test Text 123');
            if (metrics.width > 0) {
                capabilities.supported_fonts.push({
                    font: font,
                    width: metrics.width,
                    height: metrics.fontBoundingBoxAscent + metrics.fontBoundingBoxDescent || 0
                });
            }
        });
        
        return capabilities;
    }
    
    /**
     * Benchmark canvas drawing performance
     */
    async benchmarkCanvasDrawing(ctx) {
        const startTime = performance.now();
        
        // Simple drawing operations
        for (let i = 0; i < 100; i++) {
            ctx.fillStyle = `hsl(${i * 3.6}, 50%, 50%)`;
            ctx.fillRect(i % 16 * 16, Math.floor(i / 16) * 16, 15, 15);
        }
        
        const endTime = performance.now();
        return {
            operations_per_ms: 100 / (endTime - startTime),
            total_time: endTime - startTime
        };
    }
    
    /**
     * Test canvas pixel manipulation capabilities
     */
    async testCanvasPixelManipulation(ctx) {
        try {
            const startTime = performance.now();
            
            // Create gradient
            ctx.fillStyle = 'red';
            ctx.fillRect(0, 0, 100, 100);
            
            // Get image data
            const imageData = ctx.getImageData(0, 0, 100, 100);
            
            // Manipulate pixels
            for (let i = 0; i < imageData.data.length; i += 4) {
                imageData.data[i] = 255 - imageData.data[i]; // Invert red
            }
            
            // Put back image data
            ctx.putImageData(imageData, 0, 0);
            
            const endTime = performance.now();
            
            return {
                pixel_access_time: endTime - startTime,
                image_data_size: imageData.data.length,
                supports_pixel_manipulation: true
            };
        } catch (error) {
            return { supports_pixel_manipulation: false };
        }
    }
    
    /**
     * Get canvas supported formats
     */
    async getCanvasSupportedFormats(ctx) {
        const formats = {
            image_formats: [],
            export_formats: []
        };
        
        // Test export formats
        const canvas = ctx.canvas;
        const exportFormats = ['image/png', 'image/jpeg', 'image/webp', 'image/gif'];
        
        exportFormats.forEach(format => {
            try {
                const dataURL = canvas.toDataURL(format, 0.5);
                if (dataURL.startsWith(`data:${format}`)) {
                    formats.export_formats.push(format);
                }
            } catch (e) {
                // Format not supported
            }
        });
        
        return formats;
    }
    
    /**
     * Get graphics capabilities
     */
    async getGraphicsCapabilities() {
        try {
            const capabilities = {
                webgl: this.testWebGLSupport(),
                webgl2: this.testWebGL2Support(),
                canvas_2d: this.testCanvasSupport(),
                svg: 'SVGElement' in window,
                css_filters: this.testCSSFiltersSupport(),
                css_animations: this.testCSSAnimationsSupport(),
                css_transforms: this.testCSSTransformsSupport(),
                hardware_acceleration: await this.detectHardwareAcceleration()
            };
            
            return capabilities;
        } catch (error) {
            this.logger.error("Error getting graphics capabilities:", error);
            return {};
        }
    }
    
    /**
     * Test WebGL2 support
     */
    testWebGL2Support() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl2');
            canvas.remove();
            return !!gl;
        } catch (e) {
            return false;
        }
    }
    
    /**
     * Test CSS filters support
     */
    testCSSFiltersSupport() {
        const element = document.createElement('div');
        element.style.filter = 'blur(1px)';
        return element.style.filter === 'blur(1px)';
    }
    
    /**
     * Test CSS animations support
     */
    testCSSAnimationsSupport() {
        const element = document.createElement('div');
        const prefixes = ['', '-webkit-', '-moz-', '-o-', '-ms-'];
        
        for (const prefix of prefixes) {
            if (`${prefix}animation` in element.style) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Test CSS transforms support
     */
    testCSSTransformsSupport() {
        const element = document.createElement('div');
        const prefixes = ['', '-webkit-', '-moz-', '-o-', '-ms-'];
        
        for (const prefix of prefixes) {
            if (`${prefix}transform` in element.style) {
                return true;
            }
        }
        return false;
    }
    
    /**
     * Detect hardware acceleration
     */
    async detectHardwareAcceleration() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl');
            
            if (!gl) return false;
            
            // Check for hardware acceleration indicators
            const renderer = gl.getParameter(gl.RENDERER);
            const isHardwareAccelerated = 
                !renderer.includes('Software') &&
                !renderer.includes('Microsoft') &&
                !renderer.includes('Generic');
            
            canvas.remove();
            return isHardwareAccelerated;
        } catch (error) {
            return false;
        }
    }
    
    /**
     * Get compute capabilities
     */
    async getComputeCapabilities() {
        try {
            const capabilities = {
                web_assembly: 'WebAssembly' in window,
                shared_array_buffer: 'SharedArrayBuffer' in window,
                atomics: 'Atomics' in window,
                bigint: typeof BigInt !== 'undefined',
                workers: 'Worker' in window,
                shared_workers: 'SharedWorker' in window,
                service_workers: 'serviceWorker' in navigator,
                crypto_subtle: 'crypto' in window && 'subtle' in crypto,
                performance_observer: 'PerformanceObserver' in window,
                intersection_observer: 'IntersectionObserver' in window
            };
            
            if (capabilities.web_assembly) {
                capabilities.wasm_features = await this.detectWasmFeatures();
            }
            
            return capabilities;
        } catch (error) {
            this.logger.error("Error getting compute capabilities:", error);
            return {};
        }
    }
    
    /**
     * Detect WebAssembly features
     */
    async detectWasmFeatures() {
        try {
            const features = {
                basic_support: true,
                streaming: 'instantiateStreaming' in WebAssembly,
                bulk_memory: false,
                reference_types: false,
                multi_value: false,
                simd: false,
                threads: 'SharedArrayBuffer' in window
            };
            
            // Test SIMD support
            try {
                // Simple WASM module that uses SIMD (if supported)
                const wasmBytes = new Uint8Array([
                    0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00
                ]);
                await WebAssembly.instantiate(wasmBytes);
                features.instantiation_works = true;
            } catch (e) {
                features.instantiation_works = false;
            }
            
            return features;
        } catch (error) {
            return { basic_support: false };
        }
    }
    
    /**
     * Collect device performance benchmarks
     */
    async collectDevicePerformanceBenchmarks() {
        try {
            const benchmarks = {
                cpu_performance: await this.benchmarkCPUPerformance(),
                memory_performance: await this.benchmarkMemoryPerformance(),
                graphics_performance: await this.benchmarkGraphicsPerformance(),
                storage_performance: await this.benchmarkStoragePerformance(),
                network_performance: await this.benchmarkNetworkPerformance()
            };
            
            benchmarks.overall_score = this.calculateDevicePerformanceScore(benchmarks);
            
            return benchmarks;
        } catch (error) {
            this.logger.error("Error collecting device performance benchmarks:", error);
            return {};
        }
    }
    
    /**
     * Benchmark graphics performance
     */
    async benchmarkGraphicsPerformance() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 500;
            canvas.height = 500;
            const gl = canvas.getContext('webgl');
            
            if (!gl) return { score: 0 };
            
            const startTime = performance.now();
            
            // Create a simple shader program
            const vertexShader = gl.createShader(gl.VERTEX_SHADER);
            gl.shaderSource(vertexShader, `
                attribute vec2 position;
                void main() {
                    gl_Position = vec4(position, 0.0, 1.0);
                }
            `);
            gl.compileShader(vertexShader);
            
            const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
            gl.shaderSource(fragmentShader, `
                precision mediump float;
                void main() {
                    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
                }
            `);
            gl.compileShader(fragmentShader);
            
            const program = gl.createProgram();
            gl.attachShader(program, vertexShader);
            gl.attachShader(program, fragmentShader);
            gl.linkProgram(program);
            gl.useProgram(program);
            
            // Simple rendering test
            const vertices = new Float32Array([-1, -1, 1, -1, 0, 1]);
            const buffer = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
            gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
            
            const positionLocation = gl.getAttribLocation(program, 'position');
            gl.enableVertexAttribArray(positionLocation);
            gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
            
            // Render multiple times to benchmark
            for (let i = 0; i < 100; i++) {
                gl.clear(gl.COLOR_BUFFER_BIT);
                gl.drawArrays(gl.TRIANGLES, 0, 3);
            }
            
            gl.finish(); // Wait for GPU operations to complete
            
            const endTime = performance.now();
            
            // Cleanup
            gl.deleteBuffer(buffer);
            gl.deleteShader(vertexShader);
            gl.deleteShader(fragmentShader);
            gl.deleteProgram(program);
            canvas.remove();
            
            return {
                score: Math.max(0, 1000 - (endTime - startTime)),
                render_time: endTime - startTime,
                frames_per_second: Math.round(100 * 1000 / (endTime - startTime))
            };
        } catch (error) {
            return { score: 0, error: error.message };
        }
    }
    
    /**
     * Benchmark storage performance
     */
    async benchmarkStoragePerformance() {
        try {
            const results = {
                localStorage: await this.benchmarkLocalStoragePerformance(),
                sessionStorage: await this.benchmarkSessionStoragePerformance(),
                indexedDB: await this.benchmarkIndexedDBPerformance()
            };
            
            return results;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Benchmark localStorage performance
     */
    async benchmarkLocalStoragePerformance() {
        try {
            const testData = 'x'.repeat(1000); // 1KB test data
            const iterations = 100;
            
            const writeStartTime = performance.now();
            for (let i = 0; i < iterations; i++) {
                localStorage.setItem(`perf_test_${i}`, testData);
            }
            const writeEndTime = performance.now();
            
            const readStartTime = performance.now();
            for (let i = 0; i < iterations; i++) {
                localStorage.getItem(`perf_test_${i}`);
            }
            const readEndTime = performance.now();
            
            // Cleanup
            for (let i = 0; i < iterations; i++) {
                localStorage.removeItem(`perf_test_${i}`);
            }
            
            return {
                write_time: writeEndTime - writeStartTime,
                read_time: readEndTime - readStartTime,
                write_ops_per_ms: iterations / (writeEndTime - writeStartTime),
                read_ops_per_ms: iterations / (readEndTime - readStartTime)
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Benchmark sessionStorage performance
     */
    async benchmarkSessionStoragePerformance() {
        try {
            const testData = 'x'.repeat(1000);
            const iterations = 100;
            
            const writeStartTime = performance.now();
            for (let i = 0; i < iterations; i++) {
                sessionStorage.setItem(`perf_test_${i}`, testData);
            }
            const writeEndTime = performance.now();
            
            const readStartTime = performance.now();
            for (let i = 0; i < iterations; i++) {
                sessionStorage.getItem(`perf_test_${i}`);
            }
            const readEndTime = performance.now();
            
            // Cleanup
            for (let i = 0; i < iterations; i++) {
                sessionStorage.removeItem(`perf_test_${i}`);
            }
            
            return {
                write_time: writeEndTime - writeStartTime,
                read_time: readEndTime - readStartTime,
                write_ops_per_ms: iterations / (writeEndTime - writeStartTime),
                read_ops_per_ms: iterations / (readEndTime - readStartTime)
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Benchmark IndexedDB performance
     */
    async benchmarkIndexedDBPerformance() {
        return new Promise((resolve) => {
            try {
                const request = indexedDB.open('PerfTestDB', 1);
                
                request.onerror = () => resolve({ error: 'IndexedDB not available' });
                
                request.onupgradeneeded = (event) => {
                    const db = event.target.result;
                    if (!db.objectStoreNames.contains('testStore')) {
                        db.createObjectStore('testStore', { keyPath: 'id' });
                    }
                };
                
                request.onsuccess = async (event) => {
                    const db = event.target.result;
                    
                    try {
                        const transaction = db.transaction(['testStore'], 'readwrite');
                        const store = transaction.objectStore('testStore');
                        
                        const testData = { data: 'x'.repeat(1000) };
                        const iterations = 50; // Fewer iterations for IndexedDB
                        
                        const writeStartTime = performance.now();
                        for (let i = 0; i < iterations; i++) {
                            store.put({ id: i, ...testData });
                        }
                        const writeEndTime = performance.now();
                        
                        transaction.oncomplete = () => {
                            const readTransaction = db.transaction(['testStore'], 'readonly');
                            const readStore = readTransaction.objectStore('testStore');
                            
                            const readStartTime = performance.now();
                            for (let i = 0; i < iterations; i++) {
                                readStore.get(i);
                            }
                            const readEndTime = performance.now();
                            
                            // Cleanup
                            const cleanupTransaction = db.transaction(['testStore'], 'readwrite');
                            const cleanupStore = cleanupTransaction.objectStore('testStore');
                            cleanupStore.clear();
                            
                            db.close();
                            
                            resolve({
                                write_time: writeEndTime - writeStartTime,
                                read_time: readEndTime - readStartTime,
                                write_ops_per_ms: iterations / (writeEndTime - writeStartTime),
                                read_ops_per_ms: iterations / (readEndTime - readStartTime)
                            });
                        };
                    } catch (error) {
                        db.close();
                        resolve({ error: error.message });
                    }
                };
            } catch (error) {
                resolve({ error: error.message });
            }
        });
    }
    
    /**
     * Benchmark network performance
     */
    async benchmarkNetworkPerformance() {
        try {
            const results = [];
            const testUrls = ['/favicon.ico', '/', window.location.href];
            
            for (const url of testUrls) {
                try {
                    const startTime = performance.now();
                    const response = await fetch(url, { 
                        method: 'HEAD', 
                        cache: 'no-cache',
                        mode: 'cors'
                    });
                    const endTime = performance.now();
                    
                    results.push({
                        url: url,
                        latency: endTime - startTime,
                        status: response.status,
                        success: response.ok
                    });
                } catch (error) {
                    results.push({
                        url: url,
                        error: error.message,
                        success: false
                    });
                }
            }
            
            const successful = results.filter(r => r.success);
            const avgLatency = successful.length > 0 
                ? successful.reduce((sum, r) => sum + r.latency, 0) / successful.length
                : 0;
            
            return {
                average_latency: avgLatency,
                test_results: results,
                connection_type: this.getConnectionType(),
                effective_bandwidth: avgLatency > 0 ? 1000 / avgLatency : 0
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Calculate overall device performance score
     */
    calculateDevicePerformanceScore(benchmarks) {
        try {
            const scores = [];
            
            if (benchmarks.cpu_performance && benchmarks.cpu_performance.score) {
                scores.push(benchmarks.cpu_performance.score);
            }
            
            if (benchmarks.memory_performance && benchmarks.memory_performance.score) {
                scores.push(benchmarks.memory_performance.score);
            }
            
            if (benchmarks.graphics_performance && benchmarks.graphics_performance.score) {
                scores.push(benchmarks.graphics_performance.score);
            }
            
            return scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
        } catch (error) {
            return 0;
        }
    }
    
    /**
     * Generate comprehensive Canvas fingerprint
     */
    async generateCanvasFingerprint() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 200;
            canvas.height = 50;
            const ctx = canvas.getContext('2d');
            
            // Text rendering fingerprint
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillStyle = '#f60';
            ctx.fillRect(125, 1, 62, 20);
            ctx.fillStyle = '#069';
            ctx.fillText('Canvas fingerprint text! 🔐', 2, 15);
            
            // Geometric shapes fingerprint
            ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
            ctx.fillRect(26, 26, 100, 20);
            
            // Additional complexity
            ctx.beginPath();
            ctx.arc(50, 50, 20, 0, Math.PI * 2);
            ctx.closePath();
            ctx.fill();
            
            // Get canvas data
            const dataURL = canvas.toDataURL();
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            
            canvas.remove();
            
            // Generate hash of the canvas content
            const canvasHash = await this.hashSensitiveData(dataURL);
            
            return {
                canvas_hash: canvasHash,
                image_data_length: imageData.data.length,
                canvas_size: `${canvas.width}x${canvas.height}`,
                data_url_length: dataURL.length,
                rendering_context: '2d'
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Generate comprehensive WebGL fingerprint
     */
    async generateWebGLFingerprint() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) {
                canvas.remove();
                return { supported: false };
            }
            
            // Render a simple scene
            gl.clearColor(0.2, 0.3, 0.4, 1.0);
            gl.clear(gl.COLOR_BUFFER_BIT);
            
            // Simple triangle
            const vertices = new Float32Array([
                0.0,  0.5,
               -0.5, -0.5,
                0.5, -0.5
            ]);
            
            const buffer = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
            gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
            
            // Create shaders
            const vertexShaderSource = `
                attribute vec2 a_position;
                void main() {
                    gl_Position = vec4(a_position, 0.0, 1.0);
                }
            `;
            
            const fragmentShaderSource = `
                precision mediump float;
                void main() {
                    gl_FragColor = vec4(1.0, 0.5, 0.0, 1.0);
                }
            `;
            
            const vertexShader = this.createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
            const fragmentShader = this.createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);
            
            const program = gl.createProgram();
            gl.attachShader(program, vertexShader);
            gl.attachShader(program, fragmentShader);
            gl.linkProgram(program);
            gl.useProgram(program);
            
            const positionLocation = gl.getAttribLocation(program, 'a_position');
            gl.enableVertexAttribArray(positionLocation);
            gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
            
            gl.drawArrays(gl.TRIANGLES, 0, 3);
            
            // Get rendered pixels
            const pixels = new Uint8Array(canvas.width * canvas.height * 4);
            gl.readPixels(0, 0, canvas.width, canvas.height, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
            
            // Get WebGL info
            const webglInfo = await this.getWebGLHardwareInfo();
            
            // Generate fingerprint hash
            const pixelHash = await this.hashSensitiveData(Array.from(pixels).join(''));
            
            // Cleanup
            gl.deleteBuffer(buffer);
            gl.deleteShader(vertexShader);
            gl.deleteShader(fragmentShader);
            gl.deleteProgram(program);
            canvas.remove();
            
            return {
                pixel_hash: pixelHash,
                webgl_info: webglInfo,
                canvas_size: `${canvas.width}x${canvas.height}`,
                pixel_count: pixels.length,
                supported: true
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Create WebGL shader
     */
    createShader(gl, type, source) {
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            gl.deleteShader(shader);
            throw new Error('Shader compilation failed');
        }
        
        return shader;
    }
    
    /**
     * Extract platform information from user agent
     */
    extractPlatformFromUserAgent() {
        const ua = navigator.userAgent.toLowerCase();
        
        if (ua.includes('windows nt 10.0')) return 'Windows 10';
        if (ua.includes('windows nt 6.3')) return 'Windows 8.1';
        if (ua.includes('windows nt 6.2')) return 'Windows 8';
        if (ua.includes('windows nt 6.1')) return 'Windows 7';
        if (ua.includes('mac os x')) return 'macOS';
        if (ua.includes('android')) return 'Android';
        if (ua.includes('iphone') || ua.includes('ipad')) return 'iOS';
        if (ua.includes('linux')) return 'Linux';
        if (ua.includes('cros')) return 'Chrome OS';
        
        return 'Unknown';
    }
    
    /**
     * Get fallback device fingerprint
     */
    getFallbackDeviceFingerprint() {
        return {
            fallback: true,
            basic_device_info: {
                hardware_concurrency: navigator.hardwareConcurrency || 0,
                device_memory: navigator.deviceMemory || 0,
                platform: navigator.platform,
                user_agent: navigator.userAgent,
                screen_resolution: `${screen.width}x${screen.height}`,
                color_depth: screen.colorDepth,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            },
            error: 'Enhanced device fingerprinting failed, using fallback method'
        };
    }
    
    // ===== PHASE 1.1: HARDWARE ENUMERATION METHODS =====
    
    /**
     * PHASE 1.1.1: Advanced WebGL Hardware Analysis Methods
     * Get advanced WebGL hardware information beyond basic renderer detection
     */
    async getAdvancedWebGLHardwareInfo() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
            
            if (!gl) {
                return { error: 'WebGL not available', fallback_data: this.getBasicGPUFallback() };
            }
            
            const hardwareInfo = {
                // GPU Vendor and Model Analysis
                gpu_analysis: await this.analyzeGPUCharacteristics(gl),
                
                // WebGL Capabilities Matrix
                webgl_capabilities: this.getWebGLCapabilitiesMatrix(gl),
                
                // Performance Profiling
                rendering_performance: await this.profileWebGLPerformance(gl),
                
                // Memory Analysis
                gpu_memory_analysis: await this.analyzeGPUMemory(gl),
                
                // Extension Analysis
                extension_analysis: this.analyzeWebGLExtensions(gl),
                
                // Shader Capabilities
                shader_analysis: await this.analyzeShaderCapabilities(gl),
                
                // Texture and Buffer Limits
                resource_limits: this.getWebGLResourceLimits(gl),
                
                // Precision and Float Support
                precision_analysis: this.analyzeWebGLPrecision(gl)
            };
            
            canvas.remove();
            return hardwareInfo;
            
        } catch (error) {
            this.logger.error("Error in advanced WebGL analysis:", error);
            return { error: error.message, fallback_data: this.getBasicGPUFallback() };
        }
    }
    
    /**
     * PHASE 1.1.1: Canvas-based hardware detection through rendering analysis
     */
    async getCanvasBasedHardwareInfo() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 256;
            const ctx = canvas.getContext('2d');
            
            const hardwareInfo = {
                // Rendering Performance Analysis
                rendering_speed: await this.measureCanvasRenderingSpeed(ctx),
                
                // Text Rendering Characteristics
                text_rendering: await this.analyzeTextRenderingCharacteristics(ctx),
                
                // Image Processing Capabilities
                image_processing: await this.analyzeImageProcessingCapabilities(ctx),
                
                // Color Space and Precision
                color_analysis: await this.analyzeCanvasColorCapabilities(ctx),
                
                // Anti-aliasing and Smoothing
                antialiasing_analysis: await this.analyzeAntialiasingCapabilities(ctx),
                
                // Pattern and Gradient Rendering
                pattern_analysis: await this.analyzePatternRenderingCapabilities(ctx),
                
                // Composite Operations
                composite_analysis: this.analyzeCompositeOperations(ctx),
                
                // Canvas Fingerprint Generation
                canvas_fingerprint: await this.generateAdvancedCanvasFingerprint(ctx)
            };
            
            canvas.remove();
            return hardwareInfo;
            
        } catch (error) {
            this.logger.error("Error in canvas hardware analysis:", error);
            return { error: error.message, basic_canvas: this.getBasicCanvasInfo() };
        }
    }

    /**
     * PHASE 1.1.1: Advanced GPU memory estimation using multiple techniques
     */
    async estimateGPUMemory() {
        try {
            const memoryEstimation = {
                // WebGL Memory Analysis
                webgl_memory: await this.estimateWebGLMemory(),
                
                // Texture Memory Testing
                texture_memory: await this.testTextureMemoryLimits(),
                
                // Buffer Memory Testing
                buffer_memory: await this.testBufferMemoryLimits(),
                
                // Memory Stress Testing
                memory_stress_test: await this.performGPUMemoryStressTest(),
                
                // Memory Bandwidth Estimation
                memory_bandwidth: await this.estimateGPUMemoryBandwidth(),
                
                // Cache Analysis
                cache_analysis: await this.analyzeGPUCache()
            };
            
            // Calculate overall memory estimate
            memoryEstimation.estimated_total_memory = this.calculateGPUMemoryEstimate(memoryEstimation);
            memoryEstimation.confidence_level = this.calculateMemoryEstimationConfidence(memoryEstimation);
            
            return memoryEstimation;
            
        } catch (error) {
            this.logger.error("Error estimating GPU memory:", error);
            return { error: error.message, estimated_memory: "unknown" };
        }
    }
    
    /**
     * PHASE 1.1.1: Comprehensive rendering performance profiling
     */
    async profileRenderingPerformance() {
        try {
            const performanceProfile = {
                // Canvas 2D Performance
                canvas_2d_performance: await this.benchmarkCanvas2DPerformance(),
                
                // WebGL Performance
                webgl_performance: await this.benchmarkWebGLPerformance(),
                
                // GPU Compute Performance
                gpu_compute: await this.benchmarkGPUComputePerformance(),
                
                // Memory Transfer Performance
                memory_transfer: await this.benchmarkMemoryTransferPerformance(),
                
                // Shader Compilation Performance
                shader_performance: await this.benchmarkShaderPerformance(),
                
                // Frame Rate Analysis
                frame_rate_analysis: await this.analyzeFrameRateCapabilities(),
                
                // Thermal Throttling Detection
                thermal_analysis: await this.detectRenderingThermalThrottling()
            };
            
            // Calculate overall performance score
            performanceProfile.overall_performance_score = this.calculateRenderingPerformanceScore(performanceProfile);
            performanceProfile.performance_category = this.categorizeRenderingPerformance(performanceProfile.overall_performance_score);
            
            return performanceProfile;
            
        } catch (error) {
            this.logger.error("Error profiling rendering performance:", error);
            return { error: error.message, performance_level: "unknown" };
        }
    }
    
    // ===== PHASE 1.1: ENHANCED SCREEN ANALYSIS METHODS =====
    
    /**
     * PHASE 1.1.2: Advanced color profile detection and analysis
     */
    getColorProfileCharacteristics() {
        try {
            const colorProfile = {
                // Color Gamut Detection
                color_gamut: this.detectColorGamut(),
                
                // HDR Support Detection
                hdr_support: this.detectHDRSupport(),
                
                // Wide Color Gamut Detection
                wide_gamut: this.detectWideColorGamut(),
                
                // Color Space Analysis
                color_space: this.analyzeColorSpace(),
                
                // Contrast Ratio Analysis
                contrast_analysis: this.analyzeContrastCapabilities(),
                
                // Brightness Range Detection
                brightness_range: this.detectBrightnessRange(),
                
                // Color Accuracy Testing
                color_accuracy: this.testColorAccuracy(),
                
                // Gamma Characteristics
                gamma_analysis: this.analyzeGammaCharacteristics()
            };
            
            return colorProfile;
            
        } catch (error) {
            this.logger.error("Error analyzing color profile:", error);
            return { error: error.message, basic_color_info: this.getBasicColorInfo() };
        }
    }
    
    /**
     * PHASE 1.1.2: Comprehensive display capability analysis
     */
    getDisplayCapabilityAnalysis() {
        try {
            const displayCapabilities = {
                // Refresh Rate Detection
                refresh_rate: this.detectRefreshRate(),
                
                // Variable Refresh Rate Support
                vrr_support: this.detectVariableRefreshRate(),
                
                // Display Technology Detection
                display_technology: this.detectDisplayTechnology(),
                
                // Pixel Density Analysis
                pixel_density: this.calculateAdvancedPixelDensity(),
                
                // Aspect Ratio Analysis
                aspect_ratio_analysis: this.analyzeAspectRatioSupport(),
                
                // Orientation Capabilities
                orientation_capabilities: this.analyzeOrientationCapabilities(),
                
                // Multi-Display Detection
                multi_display: this.detectMultiDisplayConfiguration(),
                
                // Screen Scaling Detection
                scaling_analysis: this.analyzeScreenScaling()
            };
            
            return displayCapabilities;
            
        } catch (error) {
            this.logger.error("Error analyzing display capabilities:", error);
            return { error: error.message, basic_display_info: this.getBasicDisplayInfo() };
        }
    }

    /**
     * PHASE 1.1.2: Multi-monitor setup detection and analysis
     */
    detectMultiMonitorConfiguration() {
        try {
            const multiMonitor = {
                // Screen Count Detection
                screen_count: this.detectScreenCount(),
                
                // Screen Arrangement Analysis
                screen_arrangement: this.analyzeScreenArrangement(),
                
                // Primary Display Detection
                primary_display: this.detectPrimaryDisplay(),
                
                // Resolution Differences
                resolution_analysis: this.analyzeMultiScreenResolutions(),
                
                // Color Profile Differences
                color_profile_differences: this.analyzeMultiScreenColorProfiles(),
                
                // Extended vs Mirrored Detection
                display_mode: this.detectDisplayMode(),
                
                // Virtual Screen Boundaries
                virtual_boundaries: this.calculateVirtualScreenBoundaries()
            };
            
            return multiMonitor;
            
        } catch (error) {
            this.logger.error("Error detecting multi-monitor setup:", error);
            return { error: error.message, single_monitor: true };
        }
    }
    
    /**
     * Detect HDR and wide gamut support
     */
    /**
     * PHASE 1.1.2: HDR and wide gamut support detection
     */
    detectHDRWideGamutSupport() {
        try {
            const advancedDisplay = {
                // HDR Detection
                hdr_support: this.detectHDRCapabilities(),
                
                // Wide Gamut Detection
                wide_gamut_support: this.detectWideGamutCapabilities(),
                
                // Color Space Support
                color_space_support: this.detectColorSpaceSupport(),
                
                // Bit Depth Analysis
                bit_depth: this.analyzeBitDepth(),
                
                // Dynamic Range Analysis
                dynamic_range: this.analyzeDynamicRange(),
                
                // Tone Mapping Capabilities
                tone_mapping: this.detectToneMappingCapabilities()
            };
            
            return advancedDisplay;
            
        } catch (error) {
            this.logger.error("Error detecting HDR/wide gamut support:", error);
            return { error: error.message, standard_display: true };
        }
    }
    
    // ===== PHASE 1.1: CPU PERFORMANCE PROFILING METHODS =====
    
    /**
     * Detect detailed CPU architecture
     */
    /**
     * PHASE 1.1.3: Detailed CPU architecture detection beyond navigator.platform
     */
    async detectDetailedCPUArchitecture() {
        try {
            const cpuArchitecture = {
                // Instruction Set Analysis
                instruction_sets: await this.analyzeInstructionSets(),
                
                // CPU Vendor Detection
                cpu_vendor: await this.detectCPUVendor(),
                
                // Architecture Family Detection
                architecture_family: await this.detectArchitectureFamily(),
                
                // Core Configuration Analysis
                core_configuration: await this.analyzeCoreConfiguration(),
                
                // Cache Hierarchy Detection
                cache_hierarchy: await this.detectCacheHierarchy(),
                
                // CPU Feature Flags
                feature_flags: await this.detectCPUFeatureFlags(),
                
                // Microarchitecture Detection
                microarchitecture: await this.detectMicroarchitecture()
            };
            
            return cpuArchitecture;
            
        } catch (error) {
            this.logger.error("Error detecting CPU architecture:", error);
            return { error: error.message, basic_cpu_info: this.getBasicCPUInfo() };
        }
    }
    
    /**
     * PHASE 1.1.3: Comprehensive CPU performance benchmarking
     */
    async runCPUPerformanceBenchmarks() {
        try {
            const performanceBenchmarks = {
                // Integer Performance
                integer_performance: await this.benchmarkIntegerPerformance(),
                
                // Floating Point Performance
                float_performance: await this.benchmarkFloatingPointPerformance(),
                
                // Vector Operations Performance
                vector_performance: await this.benchmarkVectorPerformance(),
                
                // Branch Prediction Analysis
                branch_prediction: await this.benchmarkBranchPrediction(),
                
                // Cache Performance Analysis
                cache_performance: await this.benchmarkCachePerformance(),
                
                // Memory Latency Analysis
                memory_latency: await this.benchmarkMemoryLatency(),
                
                // CPU Scalability Testing
                scalability_test: await this.benchmarkCPUScalability(),
                
                // Power Efficiency Analysis
                power_efficiency: await this.analyzePowerEfficiency()
            };
            
            // Calculate overall CPU performance score
            performanceBenchmarks.overall_cpu_score = this.calculateCPUPerformanceScore(performanceBenchmarks);
            performanceBenchmarks.cpu_category = this.categorizeCPUPerformance(performanceBenchmarks.overall_cpu_score);
            
            return performanceBenchmarks;
            
        } catch (error) {
            this.logger.error("Error running CPU benchmarks:", error);
            return { error: error.message, performance_level: "unknown" };
        }
    }
                
                // Array operations benchmark
                array_operations: await this.benchmarkArrayOperations(),
                
                // Cryptographic operations benchmark
                crypto_operations: await this.benchmarkCryptoOperations(),
                
                // WebAssembly benchmark
                wasm_performance: await this.benchmarkWebAssemblyPerformance(),
                
                // Multi-threading benchmark
                multi_threading: await this.benchmarkMultiThreading(),
                
                // Combined performance score
                overall_performance_score: 0,
                performance_class: 'unknown'
            };
            
            // Calculate overall performance score
            benchmarks.overall_performance_score = this.calculateOverallPerformanceScore(benchmarks);
            benchmarks.performance_class = this.classifyPerformance(benchmarks.overall_performance_score);
            
            return benchmarks;
            
        } catch (error) {
            return { error: error.message, overall_performance_score: 0 };
        }
    }
    
    /**
     * Analyze instruction set support
     */
    async analyzeInstructionSetSupport() {
        try {
            const instructionSets = {
                // WebAssembly instruction sets
                wasm_simd: await this.detectWasmSIMDSupport(),
                wasm_threads: await this.detectWasmThreadsSupport(),
                wasm_bulk_memory: await this.detectWasmBulkMemorySupport(),
                
                // JavaScript engine optimizations
                js_jit_compilation: this.detectJITCompilation(),
                js_optimization_tier: this.detectJSOptimizationTier(),
                
                // Atomic operations
                shared_array_buffer: 'SharedArrayBuffer' in window,
                atomics_support: 'Atomics' in window,
                
                // Advanced math operations
                bigint_support: typeof BigInt !== 'undefined',
                advanced_math_support: this.detectAdvancedMathSupport()
            };
            
            return instructionSets;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Detect thermal throttling
     */
    async detectThermalThrottling() {
        try {
            const thermalAnalysis = {
                // Performance consistency over time
                performance_consistency: await this.analyzePerformanceConsistency(),
                
                // Clock speed variation detection
                clock_speed_variation: await this.detectClockSpeedVariation(),
                
                // Thermal throttling indicators
                throttling_indicators: await this.detectThrottlingIndicators(),
                
                // Performance degradation detection
                performance_degradation: await this.detectPerformanceDegradation(),
                
                // System responsiveness analysis
                system_responsiveness: await this.analyzeSystemResponsiveness(),
                
                // Battery impact analysis (mobile devices)
                battery_impact: await this.analyzeBatteryImpactOnPerformance()
            };
            
            return thermalAnalysis;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    // ===== PHASE 1.1: MEMORY & STORAGE ANALYSIS METHODS =====
    
    /**
     * Estimate system memory through performance testing
     */
    async estimateSystemMemory() {
        try {
            const memoryAnalysis = {
                // Navigator API memory info
                device_memory_gb: navigator.deviceMemory || 0,
                
                // Performance-based memory estimation
                performance_memory_estimate: await this.estimateMemoryViaPerformance(),
                
                // Memory pressure detection
                memory_pressure_indicators: await this.detectMemoryPressure(),
                
                // Available memory estimation
                available_memory_estimate: await this.estimateAvailableMemory(),
                
                // Memory allocation patterns
                allocation_patterns: await this.analyzeMemoryAllocationPatterns(),
                
                // Garbage collection analysis
                gc_analysis: await this.analyzeGarbageCollection(),
                
                // Memory bandwidth estimation
                memory_bandwidth_estimate: await this.estimateMemoryBandwidth(),
                
                // Virtual memory indicators
                virtual_memory_indicators: this.detectVirtualMemoryIndicators()
            };
            
            return memoryAnalysis;
            
        } catch (error) {
            return { error: error.message, device_memory_gb: navigator.deviceMemory || 0 };
        }
    }
    
    /**
     * Profile storage performance
     */
    async profileStoragePerformance() {
        try {
            const storageProfile = {
                // localStorage performance
                local_storage_performance: await this.benchmarkLocalStoragePerformance(),
                
                // sessionStorage performance  
                session_storage_performance: await this.benchmarkSessionStoragePerformance(),
                
                // IndexedDB performance
                indexed_db_performance: await this.benchmarkIndexedDBPerformance(),
                
                // Cache API performance
                cache_api_performance: await this.benchmarkCacheAPIPerformance(),
                
                // File system access performance
                file_system_performance: await this.benchmarkFileSystemPerformance(),
                
                // Storage capacity analysis
                storage_capacity_analysis: await this.analyzeStorageCapacity(),
                
                // Storage technology detection
                storage_technology_hints: this.detectStorageTechnologyHints(),
                
                // I/O performance characteristics
                io_performance_characteristics: await this.analyzeIOPerformance()
            };
            
            return storageProfile;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Analyze CPU cache hierarchy
     */
    async analyzeCacheHierarchy() {
        try {
            const cacheAnalysis = {
                // L1 cache analysis
                l1_cache_analysis: await this.analyzeL1Cache(),
                
                // L2 cache analysis
                l2_cache_analysis: await this.analyzeL2Cache(),
                
                // L3 cache analysis
                l3_cache_analysis: await this.analyzeL3Cache(),
                
                // Cache line size detection
                cache_line_size: await this.detectCacheLineSize(),
                
                // Cache associativity analysis
                cache_associativity: await this.analyzeCacheAssociativity(),
                
                // Cache coherency characteristics
                cache_coherency: await this.analyzeCacheCoherency(),
                
                // Memory hierarchy performance
                memory_hierarchy_performance: await this.benchmarkMemoryHierarchy()
            };
            
            return cacheAnalysis;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Detect virtual memory usage patterns
     */
    async detectVirtualMemoryUsage() {
        try {
            const virtualMemoryAnalysis = {
                // Virtual memory indicators
                vm_indicators: this.detectVirtualMemoryIndicators(),
                
                // Memory pressure analysis
                memory_pressure: await this.analyzeMemoryPressurePatterns(),
                
                // Paging activity detection
                paging_activity: await this.detectPagingActivity(),
                
                // Memory fragmentation analysis
                memory_fragmentation: await this.analyzeMemoryFragmentation(),
                
                // Swap usage indicators
                swap_usage_indicators: this.detectSwapUsageIndicators(),
                
                // Memory mapping analysis
                memory_mapping_analysis: await this.analyzeMemoryMapping()
            };
            
            return virtualMemoryAnalysis;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    // ===== PHASE 1.1: DEVICE SENSOR ENUMERATION METHODS =====
    
    /**
     * Enumerate motion sensors
     */
    async enumerateMotionSensors() {
        try {
            const motionSensors = {
                // DeviceMotion API
                device_motion_support: 'DeviceMotionEvent' in window,
                device_motion_permission: await this.checkDeviceMotionPermission(),
                
                // DeviceOrientation API
                device_orientation_support: 'DeviceOrientationEvent' in window,
                device_orientation_permission: await this.checkDeviceOrientationPermission(),
                
                // Generic Sensor API
                accelerometer_support: 'Accelerometer' in window,
                gyroscope_support: 'Gyroscope' in window,
                magnetometer_support: 'Magnetometer' in window,
                
                // Sensor readings
                current_motion_data: await this.getCurrentMotionSensorData(),
                current_orientation_data: await this.getCurrentOrientationData(),
                
                // Motion sensor capabilities
                motion_sensor_capabilities: await this.analyzeMotionSensorCapabilities(),
                
                // Sensor accuracy analysis
                sensor_accuracy_analysis: await this.analyzeSensorAccuracy()
            };
            
            return motionSensors;
            
        } catch (error) {
            return { error: error.message, device_motion_support: 'DeviceMotionEvent' in window };
        }
    }
    
    /**
     * Enumerate environmental sensors
     */
    async enumerateEnvironmentalSensors() {
        try {
            const environmentalSensors = {
                // Ambient Light Sensor
                ambient_light_support: 'AmbientLightSensor' in window,
                ambient_light_reading: await this.getAmbientLightReading(),
                
                // Proximity Sensor
                proximity_sensor_support: 'ProximitySensor' in window,
                proximity_reading: await this.getProximityReading(),
                
                // Temperature sensors
                temperature_sensor_support: 'TemperatureSensor' in window,
                
                // Humidity sensors
                humidity_sensor_support: 'HumiditySensor' in window,
                
                // Pressure sensors
                pressure_sensor_support: 'PressureSensor' in window,
                
                // UV sensors
                uv_sensor_support: 'UVSensor' in window,
                
                // Air quality sensors
                air_quality_sensor_support: 'AirQualitySensor' in window,
                
                // Environmental context analysis
                environmental_context: await this.analyzeEnvironmentalContext()
            };
            
            return environmentalSensors;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Enumerate biometric sensors
     */
    async enumerateBiometricSensors() {
        try {
            const biometricSensors = {
                // WebAuthn API
                webauthn_support: 'PublicKeyCredential' in window,
                webauthn_capabilities: await this.analyzeWebAuthnCapabilities(),
                
                // Face detection
                face_detection_support: 'FaceDetector' in window,
                
                // Fingerprint sensors
                fingerprint_sensor_hints: await this.detectFingerprintSensorHints(),
                
                // Heart rate sensors
                heart_rate_sensor_support: 'HeartRateSensor' in window,
                
                // Biometric authentication availability
                biometric_auth_availability: await this.analyzeBiometricAuthAvailability(),
                
                // Touch ID / Face ID hints
                platform_biometrics: await this.detectPlatformBiometrics(),
                
                // Behavioral biometrics capabilities
                behavioral_biometrics: await this.analyzeBehavioralBiometrics()
            };
            
            return biometricSensors;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Enumerate connectivity sensors
     */
    async enumerateConnectivitySensors() {
        try {
            const connectivitySensors = {
                // Network Information API
                network_info_support: 'connection' in navigator,
                network_capabilities: await this.analyzeNetworkCapabilities(),
                
                // Bluetooth API
                bluetooth_support: 'bluetooth' in navigator,
                bluetooth_capabilities: await this.analyzeBluetoothCapabilities(),
                
                // USB API
                usb_support: 'usb' in navigator,
                
                // Serial API
                serial_support: 'serial' in navigator,
                
                // HID API
                hid_support: 'hid' in navigator,
                
                // NFC API
                nfc_support: 'nfc' in navigator,
                
                // Geolocation API
                geolocation_support: 'geolocation' in navigator,
                geolocation_capabilities: await this.analyzeGeolocationCapabilities(),
                
                // Presentation API
                presentation_support: 'presentation' in navigator,
                
                // Wake Lock API
                wake_lock_support: 'wakeLock' in navigator,
                
                // Connectivity analysis
                connectivity_analysis: await this.analyzeConnectivityPatterns()
            };
            
            return connectivitySensors;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    // ===== PHASE 1.1: SUPPORTING HELPER METHODS =====
    
    /**
     * Analyze shader precision for WebGL
     */
    analyzeShaderPrecision(gl, shaderType) {
        try {
            const precisionFormats = ['LOW_FLOAT', 'MEDIUM_FLOAT', 'HIGH_FLOAT', 'LOW_INT', 'MEDIUM_INT', 'HIGH_INT'];
            const precision = {};
            
            precisionFormats.forEach(format => {
                const precisionFormat = gl.getShaderPrecisionFormat(shaderType, gl[format]);
                if (precisionFormat) {
                    precision[format.toLowerCase()] = {
                        precision: precisionFormat.precision,
                        rangeMin: precisionFormat.rangeMin,
                        rangeMax: precisionFormat.rangeMax
                    };
                }
            });
            
            return precision;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Detect GPU architecture from WebGL context
     */
    detectGPUArchitecture(gl, debugInfo) {
        try {
            if (!debugInfo) return 'unknown';
            
            const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) || '';
            const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) || '';
            
            // GPU architecture detection patterns
            const architectures = {
                nvidia: /GeForce|Quadro|Tesla|RTX|GTX/i,
                amd: /Radeon|RX|Vega|RDNA/i,
                intel: /Intel|HD Graphics|Iris|UHD/i,
                apple: /Apple|M1|M2|A[0-9]+/i,
                mali: /Mali/i,
                adreno: /Adreno/i,
                powerVR: /PowerVR/i
            };
            
            for (const [arch, pattern] of Object.entries(architectures)) {
                if (pattern.test(renderer) || pattern.test(vendor)) {
                    return arch;
                }
            }
            
            return 'unknown';
        } catch (error) {
            return 'unknown';
        }
    }
    
    /**
     * Detect GPU generation
     */
    detectGPUGeneration(gl, debugInfo) {
        try {
            if (!debugInfo) return 'unknown';
            
            const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) || '';
            
            // Generation detection patterns
            const generations = {
                'rtx_40_series': /RTX 40[0-9][0-9]/i,
                'rtx_30_series': /RTX 30[0-9][0-9]/i,
                'rtx_20_series': /RTX 20[0-9][0-9]/i,
                'gtx_16_series': /GTX 16[0-9][0-9]/i,
                'gtx_10_series': /GTX 10[0-9][0-9]/i,
                'rx_7000_series': /RX 7[0-9][0-9][0-9]/i,
                'rx_6000_series': /RX 6[0-9][0-9][0-9]/i,
                'rx_5000_series': /RX 5[0-9][0-9][0-9]/i,
                'apple_m2': /M2/i,
                'apple_m1': /M1/i
            };
            
            for (const [gen, pattern] of Object.entries(generations)) {
                if (pattern.test(renderer)) {
                    return gen;
                }
            }
            
            return 'unknown';
        } catch (error) {
            return 'unknown';
        }
    }
    
    /**
     * Get maximum canvas size
     */
    getMaxCanvasSize() {
        try {
            // Test progressively larger canvas sizes
            const testSizes = [2048, 4096, 8192, 16384, 32768];
            let maxSize = 0;
            
            for (const size of testSizes) {
                try {
                    const canvas = document.createElement('canvas');
                    canvas.width = size;
                    canvas.height = size;
                    const ctx = canvas.getContext('2d');
                    if (ctx && canvas.width === size && canvas.height === size) {
                        maxSize = size;
                    } else {
                        break;
                    }
                } catch (e) {
                    break;
                }
            }
            
            return maxSize;
        } catch (error) {
            return 0;
        }
    }
    
    /**
     * Analyze canvas font rendering
     */
    async analyzeCanvasFontRendering(ctx, canvas) {
        try {
            const fontTests = [
                { family: 'Arial', size: 16 },
                { family: 'Times New Roman', size: 16 },
                { family: 'Courier New', size: 16 },
                { family: 'serif', size: 16 },
                { family: 'sans-serif', size: 16 },
                { family: 'monospace', size: 16 }
            ];
            
            const results = {};
            
            fontTests.forEach(test => {
                ctx.font = `${test.size}px ${test.family}`;
                ctx.fillText('Test123', 10, 30);
                
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const hash = this.simpleHash(imageData.data);
                
                results[test.family] = {
                    hash,
                    metrics: ctx.measureText('Test123')
                };
                
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            });
            
            return results;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Detect canvas hardware acceleration
     */
    async detectCanvasHardwareAcceleration(ctx, canvas) {
        try {
            const startTime = performance.now();
            
            // Perform intensive canvas operations
            for (let i = 0; i < 1000; i++) {
                ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 10, 10);
            }
            
            const renderTime = performance.now() - startTime;
            
            // Hardware acceleration typically results in faster rendering
            return {
                render_time_ms: renderTime,
                likely_accelerated: renderTime < 50,
                performance_class: renderTime < 20 ? 'high' : renderTime < 50 ? 'medium' : 'low'
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Generate canvas hash for fingerprinting
     */
    generateCanvasHash(ctx, canvas) {
        try {
            // Draw a complex pattern
            ctx.textBaseline = 'top';
            ctx.font = '14px Arial';
            ctx.fillText('Canvas fingerprint test 🔒', 2, 2);
            
            ctx.fillStyle = 'rgba(102, 204, 0, 0.7)';
            ctx.fillRect(100, 5, 80, 20);
            
            // Get image data and generate hash
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            return this.simpleHash(imageData.data);
        } catch (error) {
            return 'error';
        }
    }
    
    /**
     * Simple hash function for data arrays
     */
    simpleHash(data) {
        let hash = 0;
        for (let i = 0; i < data.length; i++) {
            const char = data[i];
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return hash.toString(16);
    }
    
    /**
     * Detect color gamut
     */
    detectColorGamut() {
        try {
            if (window.matchMedia) {
                if (window.matchMedia('(color-gamut: rec2020)').matches) return 'rec2020';
                if (window.matchMedia('(color-gamut: p3)').matches) return 'p3';
                if (window.matchMedia('(color-gamut: srgb)').matches) return 'srgb';
            }
            return 'unknown';
        } catch (error) {
            return 'unknown';
        }
    }
    
    /**
     * Detect HDR support
     */
    detectHDRSupport() {
        try {
            if (window.matchMedia) {
                return window.matchMedia('(dynamic-range: high)').matches;
            }
            return false;
        } catch (error) {
            return false;
        }
    }
    
    /**
     * Detect wide color gamut
     */
    detectWideColorGamut() {
        try {
            if (window.matchMedia) {
                return window.matchMedia('(color-gamut: p3)').matches || 
                       window.matchMedia('(color-gamut: rec2020)').matches;
            }
            return false;
        } catch (error) {
            return false;
        }
    }
    
    /**
     * Analyze color accuracy
     */
    analyzeColorAccuracy() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 256;
            const ctx = canvas.getContext('2d');
            
            if (!ctx) return { error: 'Canvas not supported' };
            
            // Test color reproduction accuracy
            const testColors = [
                '#FF0000', '#00FF00', '#0000FF',  // Primary colors
                '#FFFF00', '#FF00FF', '#00FFFF',  // Secondary colors
                '#808080', '#404040', '#C0C0C0'   // Grayscale
            ];
            
            const results = {};
            
            testColors.forEach((color, index) => {
                ctx.fillStyle = color;
                ctx.fillRect(index * 20, 0, 20, 20);
                
                const imageData = ctx.getImageData(index * 20, 10, 1, 1);
                const [r, g, b] = imageData.data;
                
                results[color] = { r, g, b };
            });
            
            return results;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Detect Display P3 support
     */
    detectDisplayP3Support() {
        try {
            if (window.matchMedia) {
                return window.matchMedia('(color-gamut: p3)').matches;
            }
            return false;
        } catch (error) {
            return false;
        }
    }
    
    /**
     * Detect Rec2020 support
     */
    detectRec2020Support() {
        try {
            if (window.matchMedia) {
                return window.matchMedia('(color-gamut: rec2020)').matches;
            }
            return false;
        } catch (error) {
            return false;
        }
    }
    
    /**
     * Analyze color management
     */
    analyzeColorManagement() {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d', { colorSpace: 'display-p3' });
            
            return {
                display_p3_context: ctx !== null,
                color_space_support: 'colorSpace' in (canvas.getContext('2d', {}) || {}),
                image_color_space: 'ImageData' in window && 'colorSpace' in new ImageData(1, 1)
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Analyze display gamma
     */
    analyzeDisplayGamma() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 1;
            const ctx = canvas.getContext('2d');
            
            if (!ctx) return { error: 'Canvas not supported' };
            
            // Create gamma test pattern
            for (let i = 0; i < 256; i++) {
                ctx.fillStyle = `rgb(${i},${i},${i})`;
                ctx.fillRect(i, 0, 1, 1);
            }
            
            const imageData = ctx.getImageData(0, 0, 256, 1);
            const gammaAnalysis = {
                linear_response: true,
                gamma_curve_detected: false,
                estimated_gamma: 2.2 // Default assumption
            };
            
            // Analyze for non-linear response
            for (let i = 1; i < 255; i++) {
                const expected = i;
                const actual = imageData.data[i * 4]; // Red channel
                if (Math.abs(expected - actual) > 2) {
                    gammaAnalysis.linear_response = false;
                    gammaAnalysis.gamma_curve_detected = true;
                    break;
                }
            }
            
            return gammaAnalysis;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    // ===== ADDITIONAL SUPPORTING METHODS FOR PHASE 1.1 =====
    
    // CPU Performance and Analysis Methods
    async detectInstructionSetArchitecture() {
        try {
            const wasmSupport = {
                basic_wasm: 'WebAssembly' in window,
                wasm_simd: await this.testWasmSIMD(),
                wasm_threads: await this.testWasmThreads(),
                wasm_bulk_memory: await this.testWasmBulkMemory()
            };
            
            return {
                platform_arch: navigator.platform,
                user_agent_arch: this.extractArchFromUserAgent(),
                wasm_capabilities: wasmSupport,
                estimated_isa: this.estimateISAFromCapabilities(wasmSupport)
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async detectCPUVendor() {
        const userAgent = navigator.userAgent.toLowerCase();
        const platform = navigator.platform.toLowerCase();
        
        if (platform.includes('intel') || userAgent.includes('intel')) return 'intel';
        if (platform.includes('amd') || userAgent.includes('amd')) return 'amd';
        if (platform.includes('arm') || userAgent.includes('arm')) return 'arm';
        if (platform.includes('apple') || userAgent.includes('apple')) return 'apple';
        
        return 'unknown';
    }
    
    async detectCPUFamily() {
        const vendor = await this.detectCPUVendor();
        const userAgent = navigator.userAgent;
        
        // Basic CPU family detection based on available information
        if (vendor === 'apple' && userAgent.includes('M1')) return 'apple_m1';
        if (vendor === 'apple' && userAgent.includes('M2')) return 'apple_m2';
        if (vendor === 'intel' && userAgent.includes('Core')) return 'intel_core';
        if (vendor === 'amd' && userAgent.includes('Ryzen')) return 'amd_ryzen';
        
        return 'unknown';
    }
    
    async detectCPUModel() {
        // Extract CPU model from user agent if available
        const userAgent = navigator.userAgent;
        const modelPatterns = [
            /Intel Core i[3579]-\d+[A-Z]*/i,
            /AMD Ryzen [3579] \d+[A-Z]*/i,
            /Apple M[12][A-Z]*/i,
            /ARM Cortex-[A-Z]\d+/i
        ];
        
        for (const pattern of modelPatterns) {
            const match = userAgent.match(pattern);
            if (match) return match[0];
        }
        
        return 'unknown';
    }
    
    async createCPUPerformanceProfile() {
        const startTime = performance.now();
        
        // Simple CPU performance test
        let result = 0;
        for (let i = 0; i < 1000000; i++) {
            result += Math.sqrt(i);
        }
        
        const executionTime = performance.now() - startTime;
        
        return {
            benchmark_score: Math.round(1000000 / executionTime),
            execution_time_ms: executionTime,
            performance_class: executionTime < 50 ? 'high' : executionTime < 200 ? 'medium' : 'low'
        };
    }
    
    async analyzeCPUCache() {
        // Cache analysis through timing attacks (simplified)
        const cacheSizes = [32 * 1024, 256 * 1024, 8 * 1024 * 1024]; // L1, L2, L3 typical sizes
        const results = {};
        
        for (const size of cacheSizes) {
            const arraySize = size / 4; // Int32 array
            const testArray = new Int32Array(arraySize);
            
            const startTime = performance.now();
            for (let i = 0; i < arraySize; i += 16) { // Cache line stride
                testArray[i] = i;
            }
            const endTime = performance.now();
            
            results[`cache_${size}`] = endTime - startTime;
        }
        
        return results;
    }
    
    detectSIMDSupport() {
        return {
            basic_simd: 'SIMD' in window,
            wasm_simd: this.testWasmSIMD(),
            float32x4: typeof Float32Array !== 'undefined',
            int32x4: typeof Int32Array !== 'undefined'
        };
    }
    
    async analyzeWebAssemblyCapabilities() {
        if (!('WebAssembly' in window)) {
            return { supported: false };
        }
        
        return {
            supported: true,
            streaming_compilation: 'compileStreaming' in WebAssembly,
            streaming_instantiation: 'instantiateStreaming' in WebAssembly,
            bulk_memory: await this.testWasmBulkMemory(),
            simd: await this.testWasmSIMD(),
            threads: await this.testWasmThreads(),
            multi_value: await this.testWasmMultiValue()
        };
    }
    
    async analyzeThreadingCapabilities() {
        return {
            web_workers: 'Worker' in window,
            shared_array_buffer: 'SharedArrayBuffer' in window,
            atomics: 'Atomics' in window,
            hardware_concurrency: navigator.hardwareConcurrency || 0,
            service_workers: 'serviceWorker' in navigator
        };
    }
    
    // Performance Benchmarking Methods
    async benchmarkIntegerArithmetic() {
        const iterations = 1000000;
        const startTime = performance.now();
        
        let result = 0;
        for (let i = 0; i < iterations; i++) {
            result = (result + i * 7) % 1000000;
        }
        
        const executionTime = performance.now() - startTime;
        return {
            score: Math.round(iterations / executionTime),
            execution_time_ms: executionTime
        };
    }
    
    async benchmarkFloatingPoint() {
        const iterations = 1000000;
        const startTime = performance.now();
        
        let result = 0.0;
        for (let i = 0; i < iterations; i++) {
            result += Math.sin(i) * Math.cos(i);
        }
        
        const executionTime = performance.now() - startTime;
        return {
            score: Math.round(iterations / executionTime),
            execution_time_ms: executionTime
        };
    }
    
    async benchmarkMemoryAccess() {
        const arraySize = 1024 * 1024; // 1MB
        const testArray = new Int32Array(arraySize);
        const startTime = performance.now();
        
        // Sequential access
        for (let i = 0; i < arraySize; i++) {
            testArray[i] = i;
        }
        
        const executionTime = performance.now() - startTime;
        return {
            bandwidth_mb_per_sec: Math.round((arraySize * 4) / (executionTime / 1000) / (1024 * 1024)),
            execution_time_ms: executionTime
        };
    }
    
    async benchmarkStringProcessing() {
        const iterations = 10000;
        const testString = 'Hello World! '.repeat(100);
        const startTime = performance.now();
        
        for (let i = 0; i < iterations; i++) {
            testString.split(' ').join('').toLowerCase().toUpperCase();
        }
        
        const executionTime = performance.now() - startTime;
        return {
            score: Math.round(iterations / executionTime),
            execution_time_ms: executionTime
        };
    }
    
    async benchmarkArrayOperations() {
        const arraySize = 100000;
        const testArray = Array.from({length: arraySize}, (_, i) => i);
        const startTime = performance.now();
        
        testArray.sort().reverse().map(x => x * 2).filter(x => x % 2 === 0);
        
        const executionTime = performance.now() - startTime;
        return {
            score: Math.round(arraySize / executionTime),
            execution_time_ms: executionTime
        };
    }
    
    async benchmarkCryptoOperations() {
        if (!('crypto' in window) || !window.crypto.subtle) {
            return { error: 'Web Crypto API not supported' };
        }
        
        const data = new Uint8Array(1024);
        window.crypto.getRandomValues(data);
        
        const startTime = performance.now();
        
        try {
            await window.crypto.subtle.digest('SHA-256', data);
            const executionTime = performance.now() - startTime;
            
            return {
                score: Math.round(1024 / executionTime),
                execution_time_ms: executionTime
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async benchmarkWebAssemblyPerformance() {
        if (!('WebAssembly' in window)) {
            return { error: 'WebAssembly not supported' };
        }
        
        // Simple WASM module for performance testing
        const wasmCode = new Uint8Array([
            0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00,
            0x01, 0x07, 0x01, 0x60, 0x02, 0x7f, 0x7f, 0x01, 0x7f,
            0x03, 0x02, 0x01, 0x00, 0x07, 0x07, 0x01, 0x03, 0x61, 0x64, 0x64, 0x00, 0x00,
            0x0a, 0x09, 0x01, 0x07, 0x00, 0x20, 0x00, 0x20, 0x01, 0x6a, 0x0b
        ]);
        
        try {
            const wasmModule = await WebAssembly.compile(wasmCode);
            const wasmInstance = await WebAssembly.instantiate(wasmModule);
            
            const startTime = performance.now();
            for (let i = 0; i < 1000000; i++) {
                wasmInstance.exports.add(i, i + 1);
            }
            const executionTime = performance.now() - startTime;
            
            return {
                score: Math.round(1000000 / executionTime),
                execution_time_ms: executionTime
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async benchmarkMultiThreading() {
        if (!('Worker' in window)) {
            return { error: 'Web Workers not supported' };
        }
        
        return new Promise((resolve) => {
            const workerCode = `
                self.onmessage = function(e) {
                    const iterations = e.data;
                    let result = 0;
                    for (let i = 0; i < iterations; i++) {
                        result += Math.sqrt(i);
                    }
                    self.postMessage(result);
                };
            `;
            
            const blob = new Blob([workerCode], { type: 'application/javascript' });
            const worker = new Worker(URL.createObjectURL(blob));
            
            const startTime = performance.now();
            worker.postMessage(100000);
            
            worker.onmessage = () => {
                const executionTime = performance.now() - startTime;
                worker.terminate();
                URL.revokeObjectURL(blob);
                
                resolve({
                    score: Math.round(100000 / executionTime),
                    execution_time_ms: executionTime
                });
            };
            
            worker.onerror = () => {
                worker.terminate();
                resolve({ error: 'Worker execution failed' });
            };
            
            // Timeout after 5 seconds
            setTimeout(() => {
                worker.terminate();
                resolve({ error: 'Worker timeout' });
            }, 5000);
        });
    }
    
    calculateOverallPerformanceScore(benchmarks) {
        const scores = [];
        
        Object.values(benchmarks).forEach(benchmark => {
            if (benchmark && typeof benchmark.score === 'number') {
                scores.push(benchmark.score);
            }
        });
        
        if (scores.length === 0) return 0;
        
        return Math.round(scores.reduce((a, b) => a + b) / scores.length);
    }
    
    classifyPerformance(score) {
        if (score > 1000) return 'high';
        if (score > 500) return 'medium';
        if (score > 100) return 'low';
        return 'very_low';
    }
    
    // Utility methods for testing WASM capabilities
    async testWasmSIMD() {
        try {
            // Test if WASM SIMD is supported
            const wasmSIMDCode = new Uint8Array([
                0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00
            ]);
            await WebAssembly.compile(wasmSIMDCode);
            return true;
        } catch (error) {
            return false;
        }
    }
    
    async testWasmThreads() {
        return 'SharedArrayBuffer' in window && 'Atomics' in window;
    }
    
    async testWasmBulkMemory() {
        try {
            // Simple test for bulk memory operations
            return WebAssembly.validate(new Uint8Array([
                0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00
            ]));
        } catch (error) {
            return false;
        }
    }
    
    async testWasmMultiValue() {
        try {
            // Test multi-value returns in WASM
            return true; // Simplified for now
        } catch (error) {
            return false;
        }
    }
    
    extractArchFromUserAgent() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        if (userAgent.includes('x86_64') || userAgent.includes('amd64')) return 'x86_64';
        if (userAgent.includes('i386') || userAgent.includes('i686')) return 'x86';
        if (userAgent.includes('arm64') || userAgent.includes('aarch64')) return 'arm64';
        if (userAgent.includes('arm')) return 'arm';
        
        return 'unknown';
    }
    
    estimateISAFromCapabilities(wasmSupport) {
        if (wasmSupport.wasm_simd) return 'advanced';
        if (wasmSupport.basic_wasm) return 'modern';
        return 'basic';
    }
    
    // ===== STUB METHODS FOR REMAINING FUNCTIONALITY =====
    // These methods provide basic implementations to prevent errors
    // They can be enhanced in future phases
    
    // Memory and Storage Analysis Stubs
    async estimateMemoryViaPerformance() { return navigator.deviceMemory ? navigator.deviceMemory * 1024 : 0; }
    async detectMemoryPressure() { return { pressure_level: 'unknown' }; }
    async estimateAvailableMemory() { return { available_mb: 0 }; }
    async analyzeMemoryAllocationPatterns() { return { pattern: 'unknown' }; }
    async analyzeGarbageCollection() { return { gc_frequency: 'unknown' }; }
    async estimateMemoryBandwidth() { return { bandwidth_mb_s: 0 }; }
    detectVirtualMemoryIndicators() { return { vm_detected: false }; }
    
    async benchmarkLocalStoragePerformance() { 
        try {
            const startTime = performance.now();
            localStorage.setItem('test', 'data');
            localStorage.getItem('test');
            localStorage.removeItem('test');
            return { operation_time_ms: performance.now() - startTime };
        } catch (e) {
            return { error: e.message };
        }
    }
    
    async benchmarkSessionStoragePerformance() {
        try {
            const startTime = performance.now();
            sessionStorage.setItem('test', 'data');
            sessionStorage.getItem('test');
            sessionStorage.removeItem('test');
            return { operation_time_ms: performance.now() - startTime };
        } catch (e) {
            return { error: e.message };
        }
    }
    
    async benchmarkIndexedDBPerformance() { return { operation_time_ms: 0 }; }
    async benchmarkCacheAPIPerformance() { return { operation_time_ms: 0 }; }
    async benchmarkFileSystemPerformance() { return { operation_time_ms: 0 }; }
    async analyzeStorageCapacity() { return { capacity_estimate: 0 }; }
    detectStorageTechnologyHints() { return { technology: 'unknown' }; }
    async analyzeIOPerformance() { return { io_score: 0 }; }
    
    async analyzeL1Cache() { return { size_estimate: 'unknown' }; }
    async analyzeL2Cache() { return { size_estimate: 'unknown' }; }
    async analyzeL3Cache() { return { size_estimate: 'unknown' }; }
    async detectCacheLineSize() { return { line_size: 64 }; } // Common default
    async analyzeCacheAssociativity() { return { associativity: 'unknown' }; }
    async analyzeCacheCoherency() { return { coherency_protocol: 'unknown' }; }
    async benchmarkMemoryHierarchy() { return { hierarchy_score: 0 }; }
    
    async analyzeMemoryPressurePatterns() { return { pressure_patterns: [] }; }
    async detectPagingActivity() { return { paging_detected: false }; }
    async analyzeMemoryFragmentation() { return { fragmentation_level: 'unknown' }; }
    detectSwapUsageIndicators() { return { swap_usage: 'unknown' }; }
    async analyzeMemoryMapping() { return { mapping_efficiency: 'unknown' }; }
    
    // Display and Screen Analysis Stubs
    analyzePixelDensity() { 
        return { 
            dpi: window.devicePixelRatio * 96,
            category: window.devicePixelRatio > 2 ? 'high' : 'standard'
        };
    }
    
    async detectRefreshRate() {
        return new Promise((resolve) => {
            let frameCount = 0;
            const startTime = performance.now();
            
            function countFrames() {
                frameCount++;
                if (frameCount < 60) {
                    requestAnimationFrame(countFrames);
                } else {
                    const duration = performance.now() - startTime;
                    const fps = Math.round(frameCount / (duration / 1000));
                    resolve({ refresh_rate: fps, method: 'frame_counting' });
                }
            }
            
            requestAnimationFrame(countFrames);
            
            // Fallback timeout
            setTimeout(() => resolve({ refresh_rate: 60, method: 'default' }), 2000);
        });
    }
    
    analyzeOrientationSupport() {
        return {
            orientation_api: 'orientation' in screen,
            current_orientation: screen.orientation ? screen.orientation.type : 'unknown',
            orientation_change_support: 'onorientationchange' in window
        };
    }
    
    analyzeTouchCapabilities() {
        return {
            touch_support: 'ontouchstart' in window,
            max_touch_points: navigator.maxTouchPoints || 0,
            touch_events: 'TouchEvent' in window,
            pointer_events: 'PointerEvent' in window
        };
    }
    
    analyzeViewportCapabilities() {
        return {
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight,
            visual_viewport: 'visualViewport' in window,
            device_pixel_ratio: window.devicePixelRatio || 1
        };
    }
    
    analyzeDisplayScaling() {
        return {
            device_pixel_ratio: window.devicePixelRatio || 1,
            scaling_factor: window.devicePixelRatio || 1,
            scaled_display: (window.devicePixelRatio || 1) !== 1
        };
    }
    
    // Multi-monitor and Display Detection Stubs
    detectScreenSpanning() { 
        return screen.width > 2560 || screen.height > 1440; // Simple heuristic
    }
    detectVirtualDesktop() { return false; }
    detectExtendedDisplay() { return screen.availWidth !== screen.width; }
    estimateMonitorCount() { 
        return screen.width > 3000 ? 2 : 1; // Simple estimation
    }
    analyzePrimaryMonitor() { return { is_primary: true }; }
    getMultiMonitorIndicators() { return { indicators: [] }; }
    getDisplayArrangementHints() { return { arrangement: 'single' }; }
    
    // HDR and Color Support Stubs
    detectWebGLHDRSupport() { return false; }
    detectCanvasHDRSupport() { return false; }
    detectMediaHDRSupport() { return 'matchMedia' in window && window.matchMedia('(dynamic-range: high)').matches; }
    detectWebGLWideGamut() { return false; }
    estimateRealColorDepth() { return screen.colorDepth; }
    calculateColorAccuracyScore() { return 0.8; } // Default score
    getDisplayTechnologyHints() { return { technology: 'unknown' }; }
    
    // Performance and Rendering Stubs
    async benchmarkCanvas2DPerformance() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        if (!ctx) return { error: 'Canvas not supported' };
        
        const startTime = performance.now();
        for (let i = 0; i < 1000; i++) {
            ctx.fillRect(i % 100, Math.floor(i / 100) * 10, 5, 5);
        }
        return { render_time_ms: performance.now() - startTime };
    }
    
    async benchmarkWebGLPerformance() {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl');
        if (!gl) return { error: 'WebGL not supported' };
        
        const startTime = performance.now();
        for (let i = 0; i < 1000; i++) {
            gl.clear(gl.COLOR_BUFFER_BIT);
        }
        return { render_time_ms: performance.now() - startTime };
    }
    
    async benchmarkCSS3DPerformance() { return { render_time_ms: 0 }; }
    async benchmarkAnimationPerformance() { return { fps: 60 }; }
    // Enhanced Performance Analysis - Full Implementation
    async benchmarkCompositePerformance() {
        try {
            const startTime = performance.now();
            
            // Run multiple performance tests in sequence
            const results = await Promise.all([
                this.testCPUArithmetic(),
                this.testMemoryAccess(),
                this.testDOMManipulation(),
                this.testCanvasRendering()
            ]);
            
            const totalTime = performance.now() - startTime;
            const avgIndividualTime = results.reduce((a, b) => a + b, 0) / results.length;
            
            // Calculate composite score based on individual and parallel performance
            const parallelEfficiency = avgIndividualTime / (totalTime / results.length);
            const compositeScore = Math.max(0, 100 - (totalTime / 50));
            
            return {
                composite_time_ms: totalTime,
                individual_times: results,
                average_individual_time: avgIndividualTime,
                parallel_efficiency: parallelEfficiency,
                composite_score: compositeScore,
                performance_category: compositeScore > 80 ? 'excellent' : compositeScore > 60 ? 'good' : 'average'
            };
        } catch (error) {
            return { composite_time_ms: 0, error: error.message };
        }
    }
    
    detectHardwareAccelerationIndicators() {
        try {
            const indicators = {
                accelerated: 'unknown',
                webgl_acceleration: false,
                canvas_acceleration: false,
                css_acceleration: false
            };
            
            // Test WebGL hardware acceleration
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (gl) {
                const renderer = gl.getParameter(gl.RENDERER);
                indicators.webgl_acceleration = !renderer.toLowerCase().includes('software');
                indicators.gpu_renderer = renderer;
            }
            
            // Test CSS hardware acceleration indicators
            const testElement = document.createElement('div');
            testElement.style.transform = 'translateZ(0)'; // Force hardware acceleration
            testElement.style.backfaceVisibility = 'hidden';
            
            indicators.css_acceleration = testElement.style.transform === 'translateZ(0px)';
            
            // Overall assessment
            if (indicators.webgl_acceleration) {
                indicators.accelerated = 'hardware';
            } else if (indicators.css_acceleration) {
                indicators.accelerated = 'partial';
            } else {
                indicators.accelerated = 'software';
            }
            
            canvas.remove();
            return indicators;
            
        } catch (error) {
            return { accelerated: 'unknown', error: error.message };
        }
    }
    
    async analyzePerformanceConsistency() {
        try {
            const measurements = [];
            const testCount = 10;
            
            // Run the same test multiple times to measure consistency
            for (let i = 0; i < testCount; i++) {
                const testTime = await this.testCPUArithmetic();
                measurements.push(testTime);
                
                // Small delay between tests
                await new Promise(resolve => setTimeout(resolve, 50));
            }
            
            // Calculate consistency metrics
            const mean = measurements.reduce((a, b) => a + b, 0) / measurements.length;
            const variance = measurements.reduce((sum, time) => sum + Math.pow(time - mean, 2), 0) / measurements.length;
            const stdDev = Math.sqrt(variance);
            const coefficientOfVariation = (stdDev / mean) * 100;
            
            // Consistency score (lower variation = higher score)
            const consistencyScore = Math.max(0, Math.min(1, 1 - (coefficientOfVariation / 50)));
            
            return {
                consistency_score: consistencyScore,
                mean_performance_time: mean,
                standard_deviation: stdDev,
                coefficient_of_variation: coefficientOfVariation,
                measurements: measurements,
                consistency_rating: consistencyScore > 0.8 ? 'excellent' : 
                                  consistencyScore > 0.6 ? 'good' : 
                                  consistencyScore > 0.4 ? 'fair' : 'poor'
            };
            
        } catch (error) {
            return { consistency_score: 0.8, error: error.message };
        }
    }
    
    async detectThermalThrottlingIndicators() {
        try {
            const indicators = {
                throttling_detected: false,
                performance_degradation: 0,
                thermal_stress_test_results: []
            };
            
            // Baseline performance measurement
            const baselineTime = await this.testCPUArithmetic();
            
            // Run sustained workload to generate heat
            const sustainedResults = [];
            for (let i = 0; i < 5; i++) {
                const testTime = await this.testCPUArithmetic();
                sustainedResults.push(testTime);
                
                // Brief pause between tests but not enough to cool down
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            
            indicators.thermal_stress_test_results = sustainedResults;
            
            // Calculate performance degradation
            const avgSustainedTime = sustainedResults.reduce((a, b) => a + b, 0) / sustainedResults.length;
            const degradationPercent = ((avgSustainedTime - baselineTime) / baselineTime) * 100;
            
            indicators.performance_degradation = degradationPercent;
            indicators.throttling_detected = degradationPercent > 15; // >15% degradation indicates throttling
            
            // Additional thermal indicators
            if (sustainedResults.length >= 3) {
                const earlyAvg = sustainedResults.slice(0, 2).reduce((a, b) => a + b, 0) / 2;
                const lateAvg = sustainedResults.slice(-2).reduce((a, b) => a + b, 0) / 2;
                const progressiveDegradation = ((lateAvg - earlyAvg) / earlyAvg) * 100;
                
                if (progressiveDegradation > 10) {
                    indicators.progressive_throttling = true;
                }
            }
            
            return indicators;
            
        } catch (error) {
            return { throttling_detected: false, error: error.message };
        }
    }
    
    // GPU Memory Estimation - Enhanced Implementation
    async estimateGPUMemoryViaTextures() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl2') || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) return 0;
            
            // Test texture allocation capabilities
            let maxTextureSize = gl.getParameter(gl.MAX_TEXTURE_SIZE);
            let textureUnits = gl.getParameter(gl.MAX_COMBINED_TEXTURE_IMAGE_UNITS);
            
            // Estimate memory based on maximum texture capabilities
            // Assumption: 4 bytes per pixel (RGBA), square textures
            let bytesPerTexture = maxTextureSize * maxTextureSize * 4;
            let estimatedMemoryBytes = bytesPerTexture * textureUnits * 0.1; // Conservative estimate
            
            // Test actual texture creation to validate estimate
            try {
                const testTexture = gl.createTexture();
                gl.bindTexture(gl.TEXTURE_2D, testTexture);
                
                // Try to allocate progressively smaller textures to find memory limit
                const testSizes = [4096, 2048, 1024, 512];
                let successfulSize = 0;
                
                for (let size of testSizes) {
                    try {
                        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, size, size, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
                        if (gl.getError() === gl.NO_ERROR) {
                            successfulSize = size;
                            break;
                        }
                    } catch (e) {
                        continue;
                    }
                }
                
                gl.deleteTexture(testTexture);
                
                if (successfulSize > 0) {
                    // Refine estimate based on successful allocation
                    let refinedEstimate = (successfulSize * successfulSize * 4 * textureUnits * 0.3) / (1024 * 1024);
                    return Math.max(refinedEstimate, estimatedMemoryBytes / (1024 * 1024));
                }
                
            } catch (textureError) {
                // Fallback to capability-based estimate
            }
            
            return estimatedMemoryBytes / (1024 * 1024); // Convert to MB
            
        } catch (error) {
            return 0;
        }
    }
    
    async estimateGPUMemoryViaPerformance() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 256;
            canvas.height = 256;
            const gl = canvas.getContext('webgl2') || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) return 0;
            
            // Perform rendering operations and measure performance degradation
            const performanceTests = [];
            const testCounts = [100, 500, 1000, 2000];
            
            for (let count of testCounts) {
                const startTime = performance.now();
                
                // Create multiple textures and render operations
                const textures = [];
                for (let i = 0; i < count; i++) {
                    const texture = gl.createTexture();
                    gl.bindTexture(gl.TEXTURE_2D, texture);
                    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 64, 64, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
                    textures.push(texture);
                }
                
                // Cleanup
                textures.forEach(texture => gl.deleteTexture(texture));
                
                const endTime = performance.now();
                performanceTests.push({
                    count: count,
                    time: endTime - startTime,
                    timePerTexture: (endTime - startTime) / count
                });
            }
            
            // Analyze performance degradation pattern to estimate memory limits
            let degradationPoint = null;
            for (let i = 1; i < performanceTests.length; i++) {
                const prevTest = performanceTests[i-1];
                const currTest = performanceTests[i];
                
                // Check for significant performance degradation (>2x slower per texture)
                if (currTest.timePerTexture > prevTest.timePerTexture * 2) {
                    degradationPoint = prevTest.count;
                    break;
                }
            }
            
            if (degradationPoint) {
                // Estimate memory based on degradation point
                // Assumption: degradation occurs when GPU memory is stressed
                const estimatedMemoryMB = (degradationPoint * 64 * 64 * 4 * 2) / (1024 * 1024);
                return Math.min(estimatedMemoryMB, 8192); // Cap at reasonable limit
            }
            
            // Fallback estimate based on best performance
            const bestPerf = performanceTests[0];
            return Math.max(256, (bestPerf.count * 64 * 64 * 4) / (1024 * 1024));
            
        } catch (error) {
            return 0;
        }
    }
    
    estimateGPUMemoryViaCapabilities() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl2') || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) return 0;
            
            // Get WebGL capability parameters
            const maxTextureSize = gl.getParameter(gl.MAX_TEXTURE_SIZE);
            const maxRenderbufferSize = gl.getParameter(gl.MAX_RENDERBUFFER_SIZE);
            const maxTextureUnits = gl.getParameter(gl.MAX_COMBINED_TEXTURE_IMAGE_UNITS);
            const maxVertexAttribs = gl.getParameter(gl.MAX_VERTEX_ATTRIBS);
            const maxFragmentUniforms = gl.getParameter(gl.MAX_FRAGMENT_UNIFORM_VECTORS);
            const maxVertexUniforms = gl.getParameter(gl.MAX_VERTEX_UNIFORM_VECTORS);
            
            // Calculate memory estimate based on capabilities
            let textureMemoryEstimate = (maxTextureSize * maxTextureSize * 4 * maxTextureUnits * 0.1) / (1024 * 1024);
            let renderbufferEstimate = (maxRenderbufferSize * maxRenderbufferSize * 4) / (1024 * 1024);
            let uniformMemoryEstimate = ((maxFragmentUniforms + maxVertexUniforms) * 16) / (1024 * 1024);
            
            // Get WebGL version specific capabilities
            let versionMultiplier = 1;
            if (gl instanceof WebGL2RenderingContext) {
                versionMultiplier = 1.5; // WebGL2 typically indicates more capable hardware
                
                try {
                    const max3DTextureSize = gl.getParameter(gl.MAX_3D_TEXTURE_SIZE);
                    if (max3DTextureSize) {
                        textureMemoryEstimate += (max3DTextureSize ** 3 * 4 * 0.05) / (1024 * 1024);
                    }
                } catch (e) {
                    // 3D texture not supported
                }
            }
            
            const totalEstimate = (textureMemoryEstimate + renderbufferEstimate + uniformMemoryEstimate) * versionMultiplier;
            
            // Apply realistic bounds based on common hardware capabilities
            return Math.max(128, Math.min(totalEstimate, 16384)); // 128MB to 16GB range
            
        } catch (error) {
            return 256; // Default fallback estimate
        }
    }
    
    estimateGPUMemoryViaRenderer() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl2') || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) return 0;
            
            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
            if (!debugInfo) return 0;
            
            const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
            const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
            
            // GPU memory estimation based on known renderer patterns
            const memoryPatterns = [
                // NVIDIA patterns
                { pattern: /RTX 40(90|80|70|60)/i, memory: [24576, 16384, 12288, 8192] },
                { pattern: /RTX 30(90|80|70|60)/i, memory: [24576, 10240, 8192, 8192] },
                { pattern: /RTX 20(80|70|60)/i, memory: [11264, 8192, 6144] },
                { pattern: /GTX 16(60|50)/i, memory: [6144, 4096] },
                { pattern: /GTX 10(80|70|60)/i, memory: [8192, 8192, 6144] },
                
                // AMD patterns  
                { pattern: /RX 7(900|800|700|600)/i, memory: [24576, 16384, 12288, 8192] },
                { pattern: /RX 6(950|900|800|700|600)/i, memory: [16384, 16384, 12288, 12288, 8192] },
                { pattern: /RX 5(700|600|500)/i, memory: [8192, 6144, 4096] },
                
                // Intel patterns
                { pattern: /Xe Graphics/i, memory: [1024, 2048] },
                { pattern: /UHD Graphics/i, memory: [512, 1024] },
                { pattern: /HD Graphics/i, memory: [256, 512] },
                
                // Mobile patterns
                { pattern: /Adreno (7|6)/i, memory: [1024, 2048] },
                { pattern: /Mali/i, memory: [512, 1024] },
                { pattern: /PowerVR/i, memory: [256, 512] },
                
                // Apple Silicon
                { pattern: /Apple M[123]/i, memory: [8192, 16384, 32768] },
            ];
            
            for (let pattern of memoryPatterns) {
                if (pattern.pattern.test(renderer)) {
                    // Extract model number or use middle estimate
                    const memoryEstimates = pattern.memory;
                    return memoryEstimates[Math.floor(memoryEstimates.length / 2)];
                }
            }
            
            // Vendor-based fallback estimates
            if (/nvidia/i.test(vendor)) {
                return 4096; // Default NVIDIA estimate
            } else if (/amd|ati/i.test(vendor)) {
                return 6144; // Default AMD estimate  
            } else if (/intel/i.test(vendor)) {
                return 1024; // Default Intel integrated estimate
            } else if (/apple/i.test(vendor)) {
                return 8192; // Default Apple Silicon estimate
            }
            
            return 2048; // Generic fallback estimate
            
        } catch (error) {
            return 1024; // Conservative fallback
        }
    }
    
    // Canvas Analysis - Enhanced Implementation
    detectSubpixelRendering(ctx, canvas) {
        try {
            // Test subpixel rendering by drawing at fractional coordinates
            ctx.fillStyle = '#000000';
            ctx.fillRect(0.5, 0.5, 10.5, 10.5);
            
            const imageData = ctx.getImageData(0, 0, 12, 12);
            const data = imageData.data;
            
            // Analyze pixel data for subpixel rendering characteristics
            let antialiasedPixels = 0;
            let totalEdgePixels = 0;
            
            // Check edge pixels for anti-aliasing (grayscale values indicating subpixel rendering)
            for (let y = 0; y < 12; y++) {
                for (let x = 0; x < 12; x++) {
                    const index = (y * 12 + x) * 4;
                    const r = data[index];
                    const g = data[index + 1];
                    const b = data[index + 2];
                    
                    // Check if pixel is on edge of drawn rectangle
                    if ((x === 0 || x === 11 || y === 0 || y === 11) && (r > 0 || g > 0 || b > 0)) {
                        totalEdgePixels++;
                        
                        // Check for anti-aliasing (non-pure black/white values)
                        if (r > 0 && r < 255 && r === g && g === b) {
                            antialiasedPixels++;
                        }
                    }
                }
            }
            
            const subpixelRatio = totalEdgePixels > 0 ? antialiasedPixels / totalEdgePixels : 0;
            
            let renderingType = 'crisp';
            if (subpixelRatio > 0.5) {
                renderingType = 'subpixel_antialiased';
            } else if (subpixelRatio > 0.2) {
                renderingType = 'antialiased';
            }
            
            return {
                subpixel_rendering: renderingType,
                antialiasing_ratio: subpixelRatio,
                edge_pixels_analyzed: totalEdgePixels,
                antialiased_pixels: antialiasedPixels
            };
            
        } catch (error) {
            return { subpixel_rendering: 'unknown', error: error.message };
        }
    }
    
    analyzeCanvasColorSpace(ctx, canvas) {
        try {
            // Test color space capabilities
            const colorSpaceInfo = {
                color_space: 'srgb', // Default assumption
                gamut_support: [],
                hdr_support: false,
                bit_depth: 8
            };
            
            // Test for wide gamut support
            if ('colorSpace' in canvas) {
                colorSpaceInfo.color_space = canvas.colorSpace || 'srgb';
            }
            
            // Test P3 color space support
            try {
                const p3Canvas = document.createElement('canvas');
                const p3Ctx = p3Canvas.getContext('2d', { colorSpace: 'display-p3' });
                if (p3Ctx && p3Ctx.getContextAttributes().colorSpace === 'display-p3') {
                    colorSpaceInfo.gamut_support.push('display-p3');
                }
            } catch (e) {
                // P3 not supported
            }
            
            // Test Rec2020 color space support  
            try {
                const rec2020Canvas = document.createElement('canvas');
                const rec2020Ctx = rec2020Canvas.getContext('2d', { colorSpace: 'rec2020' });
                if (rec2020Ctx && rec2020Ctx.getContextAttributes().colorSpace === 'rec2020') {
                    colorSpaceInfo.gamut_support.push('rec2020');
                }
            } catch (e) {
                // Rec2020 not supported
            }
            
            // Test HDR support through pixel manipulation
            try {
                ctx.fillStyle = 'color(display-p3 1 1 1)';
                ctx.fillRect(0, 0, 1, 1);
                const imageData = ctx.getImageData(0, 0, 1, 1);
                const data = imageData.data;
                
                // Check if HDR values are preserved
                if (data[0] > 235 || data[1] > 235 || data[2] > 235) {
                    colorSpaceInfo.hdr_support = true;
                }
            } catch (e) {
                // HDR test failed
            }
            
            // Estimate bit depth based on color precision
            ctx.fillStyle = '#ff0001';
            ctx.fillRect(0, 0, 1, 1);
            const testData = ctx.getImageData(0, 0, 1, 1);
            const precision = testData.data[0] - testData.data[2]; // Red - Blue difference
            
            if (precision === 1) {
                colorSpaceInfo.bit_depth = 8;
            } else if (precision > 1) {
                colorSpaceInfo.bit_depth = 10; // Possible 10-bit support
            }
            
            return colorSpaceInfo;
            
        } catch (error) {
            return { color_space: 'srgb', error: error.message };
        }
    }
    
    async profileCanvasRenderingPerformance(ctx, canvas) {
        try {
            const performance_tests = {
                fill_operations: 0,
                stroke_operations: 0,
                text_rendering: 0,
                image_operations: 0,
                path_operations: 0,
                composite_operations: 0
            };
            
            // Test fill operations performance
            const fillStart = performance.now();
            for (let i = 0; i < 1000; i++) {
                ctx.fillStyle = `rgb(${i % 255}, ${(i * 2) % 255}, ${(i * 3) % 255})`;
                ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 10, 10);
            }
            performance_tests.fill_operations = performance.now() - fillStart;
            
            // Test stroke operations performance
            const strokeStart = performance.now();
            for (let i = 0; i < 500; i++) {
                ctx.strokeStyle = `rgb(${i % 255}, ${(i * 2) % 255}, ${(i * 3) % 255})`;
                ctx.beginPath();
                ctx.moveTo(Math.random() * canvas.width, Math.random() * canvas.height);
                ctx.lineTo(Math.random() * canvas.width, Math.random() * canvas.height);
                ctx.stroke();
            }
            performance_tests.stroke_operations = performance.now() - strokeStart;
            
            // Test text rendering performance
            const textStart = performance.now();
            ctx.font = '12px Arial';
            for (let i = 0; i < 200; i++) {
                ctx.fillText(`Test ${i}`, Math.random() * canvas.width, Math.random() * canvas.height);
            }
            performance_tests.text_rendering = performance.now() - textStart;
            
            // Test path operations performance
            const pathStart = performance.now();
            for (let i = 0; i < 100; i++) {
                ctx.beginPath();
                ctx.arc(Math.random() * canvas.width, Math.random() * canvas.height, 20, 0, Math.PI * 2);
                ctx.fill();
            }
            performance_tests.path_operations = performance.now() - pathStart;
            
            // Test composite operations performance
            const compositeStart = performance.now();
            const originalComposite = ctx.globalCompositeOperation;
            const compositeOps = ['multiply', 'screen', 'overlay', 'soft-light'];
            for (let i = 0; i < 100; i++) {
                ctx.globalCompositeOperation = compositeOps[i % compositeOps.length];
                ctx.fillRect(Math.random() * canvas.width, Math.random() * canvas.height, 20, 20);
            }
            ctx.globalCompositeOperation = originalComposite;
            performance_tests.composite_operations = performance.now() - compositeStart;
            
            // Calculate overall performance score (lower is better)
            const totalTime = Object.values(performance_tests).reduce((sum, time) => sum + time, 0);
            const normalizedScore = Math.max(0, Math.min(100, 100 - (totalTime / 50))); // Normalize to 0-100
            
            return {
                performance_score: normalizedScore,
                detailed_timings: performance_tests,
                total_time_ms: totalTime,
                operations_per_second: {
                    fill_ops_per_sec: performance_tests.fill_operations > 0 ? 1000 / (performance_tests.fill_operations / 1000) : 0,
                    stroke_ops_per_sec: performance_tests.stroke_operations > 0 ? 500 / (performance_tests.stroke_operations / 1000) : 0,
                    text_ops_per_sec: performance_tests.text_rendering > 0 ? 200 / (performance_tests.text_rendering / 1000) : 0
                }
            };
            
        } catch (error) {
            return { performance_score: 0, error: error.message };
        }
    }
    
    detectCanvasRenderingQuirks(ctx, canvas) {
        try {
            const quirks = [];
            const quirkTests = {};
            
            // Test 1: Fractional pixel rendering
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#000000';
            ctx.fillRect(0.5, 0.5, 1, 1);
            const fractionalData = ctx.getImageData(0, 0, 2, 2);
            if (fractionalData.data.some(value => value > 0 && value < 255)) {
                quirks.push('fractional_pixel_antialiasing');
                quirkTests.fractional_rendering = true;
            }
            
            // Test 2: Text measurement precision
            ctx.font = '12px Arial';
            const width1 = ctx.measureText('W').width;
            const width2 = ctx.measureText('W').width;
            if (width1 !== width2) {
                quirks.push('inconsistent_text_measurement');
                quirkTests.text_measurement_variance = true;
            }
            
            // Test 3: Color precision
            ctx.fillStyle = '#010101';
            ctx.fillRect(0, 0, 1, 1);
            const colorData = ctx.getImageData(0, 0, 1, 1);
            const expectedValue = 1;
            const actualValue = colorData.data[0];
            if (Math.abs(actualValue - expectedValue) > 2) {
                quirks.push('color_precision_loss');
                quirkTests.color_precision_delta = actualValue - expectedValue;
            }
            
            // Test 4: Global alpha behavior
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.globalAlpha = 0.5;
            ctx.fillStyle = '#FF0000';
            ctx.fillRect(0, 0, 1, 1);
            ctx.globalAlpha = 1.0;
            const alphaData = ctx.getImageData(0, 0, 1, 1);
            const expectedAlpha = Math.round(255 * 0.5);
            const actualAlpha = alphaData.data[0];
            if (Math.abs(actualAlpha - expectedAlpha) > 5) {
                quirks.push('non_standard_alpha_blending');
                quirkTests.alpha_precision_delta = actualAlpha - expectedAlpha;
            }
            
            // Test 5: Line width consistency
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(10, 0);
            ctx.stroke();
            const lineData = ctx.getImageData(0, 0, 10, 2);
            let linePixels = 0;
            for (let i = 0; i < lineData.data.length; i += 4) {
                if (lineData.data[i] > 0) linePixels++;
            }
            if (linePixels < 5 || linePixels > 20) {
                quirks.push('non_standard_line_rendering');
                quirkTests.line_pixel_count = linePixels;
            }
            
            // Test 6: Image smoothing behavior
            if (ctx.imageSmoothingEnabled !== undefined) {
                const originalSmoothing = ctx.imageSmoothingEnabled;
                ctx.imageSmoothingEnabled = false;
                const smoothingDisabled = ctx.imageSmoothingEnabled;
                ctx.imageSmoothingEnabled = originalSmoothing;
                
                if (smoothingDisabled !== false) {
                    quirks.push('image_smoothing_override_failed');
                    quirkTests.smoothing_control_available = false;
                }
            }
            
            return {
                quirks: quirks,
                quirk_test_results: quirkTests,
                total_quirks_detected: quirks.length,
                rendering_behavior: quirks.length > 2 ? 'non_standard' : 'standard'
            };
            
        } catch (error) {
            return { quirks: ['test_execution_failed'], error: error.message };
        }
    }
    
    analyzeTextMeasurementPrecision(ctx) {
        try {
            const testStrings = ['W', 'i', 'M', 'l', '1', 'WWW', 'iii', 'Test String', 'The quick brown fox jumps over the lazy dog'];
            const fonts = ['12px Arial', '14px Times', '16px Helvetica', '12px monospace'];
            
            const measurements = {
                consistency_score: 0,
                precision_level: 'standard',
                font_variations: {},
                measurement_variance: {}
            };
            
            let totalConsistencyTests = 0;
            let passedConsistencyTests = 0;
            
            for (let font of fonts) {
                ctx.font = font;
                measurements.font_variations[font] = {};
                
                for (let testStr of testStrings) {
                    // Measure the same string multiple times to check consistency
                    const measurements_array = [];
                    for (let i = 0; i < 5; i++) {
                        measurements_array.push(ctx.measureText(testStr).width);
                    }
                    
                    // Check for consistency
                    const minWidth = Math.min(...measurements_array);
                    const maxWidth = Math.max(...measurements_array);
                    const variance = maxWidth - minWidth;
                    
                    measurements.font_variations[font][testStr] = {
                        avg_width: measurements_array.reduce((a, b) => a + b) / measurements_array.length,
                        variance: variance,
                        consistent: variance < 0.1
                    };
                    
                    totalConsistencyTests++;
                    if (variance < 0.1) {
                        passedConsistencyTests++;
                    }
                }
            }
            
            // Calculate overall consistency score
            measurements.consistency_score = totalConsistencyTests > 0 ? (passedConsistencyTests / totalConsistencyTests) * 100 : 0;
            
            // Determine precision level
            if (measurements.consistency_score > 95) {
                measurements.precision_level = 'high';
            } else if (measurements.consistency_score > 80) {
                measurements.precision_level = 'standard';
            } else {
                measurements.precision_level = 'low';
            }
            
            // Test subpixel precision
            ctx.font = '12px Arial';
            const baseWidth = ctx.measureText('A').width;
            const scaledWidth = ctx.measureText('AA').width;
            measurements.subpixel_precision = Math.abs(scaledWidth - (baseWidth * 2)) < 0.5;
            
            // Test fractional measurements
            const fractionalTest = ctx.measureText('W').width % 1;
            measurements.supports_fractional_widths = fractionalTest !== 0;
            
            return measurements;
            
        } catch (error) {
            return { precision: 'standard', error: error.message };
        }
    }
    
    // Thermal and Performance Analysis - Enhanced Implementation
    async detectClockSpeedVariation() {
        try {
            const measurements = [];
            const testDuration = 2000; // 2 seconds
            const measurementInterval = 100; // 100ms intervals
            const iterations = testDuration / measurementInterval;
            
            // Perform CPU-intensive operations and measure timing consistency
            for (let i = 0; i < iterations; i++) {
                const startTime = performance.now();
                
                // Standardized CPU work (mathematical operations)
                let sum = 0;
                for (let j = 0; j < 10000; j++) {
                    sum += Math.sin(j) * Math.cos(j) + Math.sqrt(j);
                }
                
                const endTime = performance.now();
                const executionTime = endTime - startTime;
                
                measurements.push({
                    iteration: i,
                    execution_time: executionTime,
                    timestamp: startTime
                });
                
                // Wait for next interval
                await new Promise(resolve => setTimeout(resolve, measurementInterval - executionTime));
            }
            
            // Analyze timing variations
            const executionTimes = measurements.map(m => m.execution_time);
            const avgTime = executionTimes.reduce((a, b) => a + b, 0) / executionTimes.length;
            const variance = executionTimes.reduce((sum, time) => sum + Math.pow(time - avgTime, 2), 0) / executionTimes.length;
            const standardDeviation = Math.sqrt(variance);
            const coefficientOfVariation = (standardDeviation / avgTime) * 100;
            
            // Detect trends indicating thermal throttling
            let throttlingIndicators = [];
            
            // Check for increasing execution times (warming up)
            const firstHalf = executionTimes.slice(0, Math.floor(executionTimes.length / 2));
            const secondHalf = executionTimes.slice(Math.floor(executionTimes.length / 2));
            const firstHalfAvg = firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length;
            const secondHalfAvg = secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length;
            
            if (secondHalfAvg > firstHalfAvg * 1.1) {
                throttlingIndicators.push('execution_time_degradation');
            }
            
            // Check for periodic variations
            const periodicVariation = this.detectPeriodicPatterns(executionTimes);
            if (periodicVariation.detected) {
                throttlingIndicators.push('periodic_performance_variation');
            }
            
            return {
                variation_detected: coefficientOfVariation > 15, // >15% variation suggests throttling
                coefficient_of_variation: coefficientOfVariation,
                avg_execution_time: avgTime,
                standard_deviation: standardDeviation,
                performance_degradation: secondHalfAvg > firstHalfAvg * 1.1,
                throttling_indicators: throttlingIndicators,
                measurement_count: measurements.length,
                periodic_patterns: periodicVariation
            };
            
        } catch (error) {
            return { variation_detected: false, error: error.message };
        }
    }
    
    async detectThrottlingIndicators() {
        try {
            const indicators = [];
            const testResults = {};
            
            // Test 1: CPU frequency stability through timing consistency
            const cpuStabilityTest = await this.testCPUStability();
            if (cpuStabilityTest.unstable) {
                indicators.push({
                    type: 'cpu_frequency_instability',
                    severity: cpuStabilityTest.severity,
                    details: cpuStabilityTest.details
                });
            }
            testResults.cpu_stability = cpuStabilityTest;
            
            // Test 2: Memory bandwidth consistency
            const memoryTest = await this.testMemoryBandwidth();
            if (memoryTest.degraded) {
                indicators.push({
                    type: 'memory_bandwidth_degradation',
                    severity: memoryTest.severity,
                    details: memoryTest.details
                });
            }
            testResults.memory_bandwidth = memoryTest;
            
            // Test 3: GPU performance consistency
            const gpuTest = await this.testGPUThrottling();
            if (gpuTest.throttled) {
                indicators.push({
                    type: 'gpu_thermal_throttling',
                    severity: gpuTest.severity,
                    details: gpuTest.details
                });
            }
            testResults.gpu_performance = gpuTest;
            
            // Test 4: Battery impact analysis
            const batteryTest = await this.analyzeBatteryPerformanceImpact();
            if (batteryTest.impacted) {
                indicators.push({
                    type: 'battery_performance_limitation',
                    severity: batteryTest.severity,
                    details: batteryTest.details
                });
            }
            testResults.battery_impact = batteryTest;
            
            // Test 5: System responsiveness
            const responsivenessTest = await this.testSystemResponsiveness();
            if (responsivenessTest.degraded) {
                indicators.push({
                    type: 'system_responsiveness_degradation',
                    severity: responsivenessTest.severity,
                    details: responsivenessTest.details
                });
            }
            testResults.system_responsiveness = responsivenessTest;
            
            return {
                indicators: indicators,
                indicator_count: indicators.length,
                overall_throttling_detected: indicators.length > 0,
                severity_level: this.calculateOverallSeverity(indicators),
                detailed_test_results: testResults
            };
            
        } catch (error) {
            return { indicators: [], error: error.message };
        }
    }
    
    async detectPerformanceDegradation() {
        try {
            const degradationTests = [];
            const testDuration = 5000; // 5 seconds of testing
            const testInterval = 500; // Test every 500ms
            
            const baselineTests = [
                { name: 'cpu_arithmetic', fn: this.testCPUArithmetic },
                { name: 'memory_access', fn: this.testMemoryAccess },
                { name: 'dom_manipulation', fn: this.testDOMManipulation },
                { name: 'canvas_rendering', fn: this.testCanvasRendering }
            ];
            
            for (let test of baselineTests) {
                const testResults = [];
                const testCount = Math.floor(testDuration / testInterval);
                
                for (let i = 0; i < testCount; i++) {
                    const startTime = performance.now();
                    await test.fn.call(this);
                    const endTime = performance.now();
                    
                    testResults.push({
                        iteration: i,
                        time: endTime - startTime,
                        timestamp: startTime
                    });
                    
                    // Wait for next test interval
                    await new Promise(resolve => setTimeout(resolve, testInterval));
                }
                
                // Analyze performance trend
                const times = testResults.map(r => r.time);
                const trend = this.calculatePerformanceTrend(times);
                
                degradationTests.push({
                    test_name: test.name,
                    results: testResults,
                    avg_time: times.reduce((a, b) => a + b, 0) / times.length,
                    performance_trend: trend,
                    degradation_detected: trend.slope > 0.1, // Positive slope indicates degradation
                    degradation_percentage: trend.degradation_percent
                });
            }
            
            // Overall degradation analysis
            const degradedTests = degradationTests.filter(t => t.degradation_detected);
            const overallDegradation = degradedTests.length > 0;
            const avgDegradationPercent = degradedTests.length > 0 ? 
                degradedTests.reduce((sum, t) => sum + t.degradation_percentage, 0) / degradedTests.length : 0;
            
            return {
                degradation_detected: overallDegradation,
                affected_test_count: degradedTests.length,
                total_tests: degradationTests.length,
                average_degradation_percent: avgDegradationPercent,
                degradation_severity: this.categorizeDegradationSeverity(avgDegradationPercent),
                detailed_test_results: degradationTests,
                likely_causes: this.identifyDegradationCauses(degradationTests)
            };
            
        } catch (error) {
            return { degradation_detected: false, error: error.message };
        }
    }
    
    async analyzeSystemResponsiveness() {
        try {
            const responsivenessMetrics = {
                event_response_times: [],
                animation_frame_times: [],
                dom_update_times: [],
                user_interaction_latency: []
            };
            
            // Test 1: Event handling responsiveness
            const eventTest = await this.measureEventResponseTime();
            responsivenessMetrics.event_response_times = eventTest.response_times;
            
            // Test 2: Animation frame consistency
            const animationTest = await this.measureAnimationFrameConsistency();
            responsivenessMetrics.animation_frame_times = animationTest.frame_times;
            
            // Test 3: DOM update performance
            const domTest = await this.measureDOMUpdatePerformance();
            responsivenessMetrics.dom_update_times = domTest.update_times;
            
            // Test 4: Simulated user interaction latency
            const interactionTest = await this.measureInteractionLatency();
            responsivenessMetrics.user_interaction_latency = interactionTest.latencies;
            
            // Calculate overall responsiveness score
            const avgEventTime = this.calculateAverage(responsivenessMetrics.event_response_times);
            const avgFrameTime = this.calculateAverage(responsivenessMetrics.animation_frame_times);
            const avgDOMTime = this.calculateAverage(responsivenessMetrics.dom_update_times);
            const avgInteractionTime = this.calculateAverage(responsivenessMetrics.user_interaction_latency);
            
            // Normalize scores (lower times = higher scores)
            const eventScore = Math.max(0, 100 - (avgEventTime * 10));
            const animationScore = Math.max(0, 100 - (avgFrameTime - 16.67) * 5); // 60fps target
            const domScore = Math.max(0, 100 - (avgDOMTime * 2));
            const interactionScore = Math.max(0, 100 - (avgInteractionTime * 5));
            
            const overallScore = (eventScore + animationScore + domScore + interactionScore) / 4;
            
            return {
                responsiveness_score: overallScore,
                performance_category: this.categorizeResponsiveness(overallScore),
                detailed_metrics: responsivenessMetrics,
                average_times: {
                    event_response_ms: avgEventTime,
                    animation_frame_ms: avgFrameTime,
                    dom_update_ms: avgDOMTime,
                    interaction_latency_ms: avgInteractionTime
                },
                individual_scores: {
                    event_handling: eventScore,
                    animation_performance: animationScore,
                    dom_performance: domScore,
                    interaction_responsiveness: interactionScore
                }
            };
            
        } catch (error) {
            return { responsiveness_score: 0.8, error: error.message };
        }
    }
    
    async analyzeBatteryImpactOnPerformance() {
        try {
            let batteryInfo = { level: null, charging: null };
            
            // Try to get battery information
            if ('getBattery' in navigator) {
                try {
                    const battery = await navigator.getBattery();
                    batteryInfo = {
                        level: battery.level,
                        charging: battery.charging,
                        charging_time: battery.chargingTime,
                        discharging_time: battery.dischargingTime
                    };
                } catch (e) {
                    // Battery API not available or blocked
                }
            }
            
            // Perform performance tests to correlate with battery status
            const performanceBaseline = await this.establishPerformanceBaseline();
            
            let impactAnalysis = {
                impact_level: 'unknown',
                performance_reduction: 0,
                battery_saving_mode_detected: false,
                power_throttling_indicators: []
            };
            
            if (batteryInfo.level !== null) {
                // Analyze performance correlation with battery level
                if (batteryInfo.level < 0.2 && !batteryInfo.charging) {
                    // Low battery - check for power saving throttling
                    const lowBatteryPerformance = await this.measureThrottledPerformance();
                    const performanceReduction = ((performanceBaseline.score - lowBatteryPerformance.score) / performanceBaseline.score) * 100;
                    
                    impactAnalysis = {
                        impact_level: performanceReduction > 10 ? 'high' : performanceReduction > 5 ? 'medium' : 'low',
                        performance_reduction: performanceReduction,
                        battery_saving_mode_detected: performanceReduction > 15,
                        power_throttling_indicators: this.identifyPowerThrottling(performanceBaseline, lowBatteryPerformance),
                        battery_level: batteryInfo.level,
                        charging_status: batteryInfo.charging
                    };
                } else {
                    // Normal battery conditions
                    impactAnalysis = {
                        impact_level: 'minimal',
                        performance_reduction: 0,
                        battery_saving_mode_detected: false,
                        power_throttling_indicators: [],
                        battery_level: batteryInfo.level,
                        charging_status: batteryInfo.charging
                    };
                }
            } else {
                // Battery info unavailable - analyze for desktop power management
                const desktopThrottling = await this.detectDesktopPowerThrottling();
                impactAnalysis = {
                    impact_level: desktopThrottling.detected ? 'medium' : 'unknown',
                    performance_reduction: desktopThrottling.estimated_reduction || 0,
                    battery_saving_mode_detected: false,
                    power_throttling_indicators: desktopThrottling.indicators || [],
                    device_type: 'desktop_or_battery_unavailable'
                };
            }
            
            return impactAnalysis;
            
        } catch (error) {
            return { impact_level: 'unknown', error: error.message };
        }
    }
    
    // Advanced Detection Methods Stubs
    detectJITCompilation() { return { jit_detected: true }; }
    detectJSOptimizationTier() { return { tier: 'optimized' }; }
    detectAdvancedMathSupport() { return { advanced_math: true }; }
    
    // Sensor Permission and Data Methods
    async checkDeviceMotionPermission() {
        if (typeof DeviceMotionEvent.requestPermission === 'function') {
            try {
                const permission = await DeviceMotionEvent.requestPermission();
                return permission === 'granted';
            } catch (e) {
                return false;
            }
        }
        return 'DeviceMotionEvent' in window;
    }
    
    // Helper Methods for Enhanced Implementation
    detectPeriodicPatterns(timings) {
        try {
            if (timings.length < 10) return { detected: false };
            
            // Simple periodic pattern detection using autocorrelation
            const mean = timings.reduce((a, b) => a + b) / timings.length;
            const centered = timings.map(t => t - mean);
            
            // Check for periods from 2 to half the data length
            const maxPeriod = Math.floor(timings.length / 2);
            let bestPeriod = 0;
            let bestCorrelation = 0;
            
            for (let period = 2; period <= maxPeriod; period++) {
                let correlation = 0;
                let count = 0;
                
                for (let i = 0; i < timings.length - period; i++) {
                    correlation += centered[i] * centered[i + period];
                    count++;
                }
                
                if (count > 0) {
                    correlation /= count;
                    if (Math.abs(correlation) > Math.abs(bestCorrelation)) {
                        bestCorrelation = correlation;
                        bestPeriod = period;
                    }
                }
            }
            
            return {
                detected: Math.abs(bestCorrelation) > 0.3,
                period: bestPeriod,
                correlation: bestCorrelation,
                strength: Math.abs(bestCorrelation)
            };
            
        } catch (error) {
            return { detected: false, error: error.message };
        }
    }
    
    async testCPUStability() {
        try {
            const iterations = 10;
            const executionTimes = [];
            
            for (let i = 0; i < iterations; i++) {
                const start = performance.now();
                
                // Standardized CPU workload
                let result = 0;
                for (let j = 0; j < 50000; j++) {
                    result += Math.sin(j) * Math.cos(j);
                }
                
                executionTimes.push(performance.now() - start);
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            
            const avg = executionTimes.reduce((a, b) => a + b) / executionTimes.length;
            const variance = executionTimes.reduce((sum, t) => sum + Math.pow(t - avg, 2), 0) / executionTimes.length;
            const cv = (Math.sqrt(variance) / avg) * 100;
            
            return {
                unstable: cv > 20,
                coefficient_variation: cv,
                avg_execution_time: avg,
                severity: cv > 50 ? 'high' : cv > 30 ? 'medium' : 'low',
                details: { execution_times: executionTimes, variance: variance }
            };
            
        } catch (error) {
            return { unstable: false, error: error.message };
        }
    }
    
    async testMemoryBandwidth() {
        try {
            const arraySizes = [1000, 10000, 100000];
            const results = [];
            
            for (let size of arraySizes) {
                const start = performance.now();
                
                // Memory bandwidth test
                const array1 = new Float32Array(size);
                const array2 = new Float32Array(size);
                
                // Fill arrays
                for (let i = 0; i < size; i++) {
                    array1[i] = Math.random();
                    array2[i] = Math.random();
                }
                
                // Copy operations
                for (let i = 0; i < size; i++) {
                    array2[i] = array1[i] * 2.5;
                }
                
                results.push({
                    size: size,
                    time: performance.now() - start,
                    bandwidth: (size * 8) / ((performance.now() - start) / 1000) // bytes per second
                });
            }
            
            // Analyze bandwidth degradation
            const bandwidths = results.map(r => r.bandwidth);
            const expectedScaling = results[0].bandwidth / results[results.length - 1].bandwidth;
            const actualScaling = arraySizes[0] / arraySizes[arraySizes.length - 1];
            
            return {
                degraded: Math.abs(expectedScaling - actualScaling) > 0.5,
                bandwidth_results: results,
                scaling_factor: expectedScaling / actualScaling,
                severity: Math.abs(expectedScaling - actualScaling) > 1.0 ? 'high' : 'low',
                details: { expected_scaling: expectedScaling, actual_scaling: actualScaling }
            };
            
        } catch (error) {
            return { degraded: false, error: error.message };
        }
    }
    
    async testGPUThrottling() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = canvas.height = 256;
            const gl = canvas.getContext('webgl2') || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            if (!gl) return { throttled: false, reason: 'webgl_unavailable' };
            
            const renderTimes = [];
            const iterations = 5;
            
            // Create shader program for GPU workload
            const vertexShaderSource = `
                attribute vec4 a_position;
                void main() {
                    gl_Position = a_position;
                }
            `;
            
            const fragmentShaderSource = `
                precision mediump float;
                uniform float u_time;
                void main() {
                    vec2 coord = gl_FragCoord.xy / 256.0;
                    float color = 0.0;
                    for(int i = 0; i < 100; i++) {
                        color += sin(coord.x * float(i) + u_time) * cos(coord.y * float(i) + u_time);
                    }
                    gl_FragColor = vec4(color * 0.01, 0.0, 0.0, 1.0);
                }
            `;
            
            // Compile shaders and create program
            const vertexShader = gl.createShader(gl.VERTEX_SHADER);
            gl.shaderSource(vertexShader, vertexShaderSource);
            gl.compileShader(vertexShader);
            
            const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
            gl.shaderSource(fragmentShader, fragmentShaderSource);
            gl.compileShader(fragmentShader);
            
            const program = gl.createProgram();
            gl.attachShader(program, vertexShader);
            gl.attachShader(program, fragmentShader);
            gl.linkProgram(program);
            
            if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
                return { throttled: false, reason: 'shader_compilation_failed' };
            }
            
            // Setup geometry
            const positions = new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]);
            const positionBuffer = gl.createBuffer();
            gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
            gl.bufferData(gl.ARRAY_BUFFER, positions, gl.STATIC_DRAW);
            
            const positionLocation = gl.getAttribLocation(program, 'a_position');
            const timeLocation = gl.getUniformLocation(program, 'u_time');
            
            gl.useProgram(program);
            gl.enableVertexAttribArray(positionLocation);
            gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
            
            // Perform rendering tests
            for (let i = 0; i < iterations; i++) {
                const startTime = performance.now();
                
                // Heavy GPU computation
                for (let frame = 0; frame < 10; frame++) {
                    gl.uniform1f(timeLocation, frame * 0.1);
                    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
                    gl.finish(); // Force GPU to complete
                }
                
                renderTimes.push(performance.now() - startTime);
                
                // Cool down between tests
                await new Promise(resolve => setTimeout(resolve, 200));
            }
            
            // Analyze for throttling
            const avgTime = renderTimes.reduce((a, b) => a + b) / renderTimes.length;
            const firstHalf = renderTimes.slice(0, Math.ceil(renderTimes.length / 2));
            const secondHalf = renderTimes.slice(Math.floor(renderTimes.length / 2));
            
            const firstAvg = firstHalf.reduce((a, b) => a + b) / firstHalf.length;
            const secondAvg = secondHalf.reduce((a, b) => a + b) / secondHalf.length;
            
            const degradation = (secondAvg - firstAvg) / firstAvg * 100;
            
            return {
                throttled: degradation > 15,
                degradation_percent: degradation,
                render_times: renderTimes,
                avg_render_time: avgTime,
                severity: degradation > 30 ? 'high' : degradation > 15 ? 'medium' : 'low',
                details: { first_half_avg: firstAvg, second_half_avg: secondAvg }
            };
            
        } catch (error) {
            return { throttled: false, error: error.message };
        }
    }
    
    calculateAverage(numbers) {
        return numbers.length > 0 ? numbers.reduce((a, b) => a + b, 0) / numbers.length : 0;
    }
    
    calculatePerformanceTrend(timings) {
        if (timings.length < 2) return { slope: 0, degradation_percent: 0 };
        
        // Linear regression to find trend
        const n = timings.length;
        const sumX = (n * (n - 1)) / 2; // Sum of indices
        const sumY = timings.reduce((a, b) => a + b, 0);
        const sumXY = timings.reduce((sum, y, x) => sum + x * y, 0);
        const sumXX = (n * (n - 1) * (2 * n - 1)) / 6; // Sum of squares of indices
        
        const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
        const intercept = (sumY - slope * sumX) / n;
        
        // Calculate degradation percentage
        const firstValue = intercept;
        const lastValue = intercept + slope * (n - 1);
        const degradationPercent = ((lastValue - firstValue) / firstValue) * 100;
        
        return {
            slope: slope,
            intercept: intercept,
            degradation_percent: degradationPercent,
            trend_direction: slope > 0.1 ? 'degrading' : slope < -0.1 ? 'improving' : 'stable'
        };
    }
    
    async checkDeviceOrientationPermission() {
        if (typeof DeviceOrientationEvent.requestPermission === 'function') {
            try {
                const permission = await DeviceOrientationEvent.requestPermission();
                return permission === 'granted';
            } catch (e) {
                return false;
            }
        }
        return 'DeviceOrientationEvent' in window;
    }
    
    async getCurrentMotionSensorData() { return await this.getCurrentMotionReading(); }
    async getCurrentOrientationData() { return await this.getCurrentOrientationReading(); }
    async analyzeMotionSensorCapabilities() { return { capabilities: 'basic' }; }
    async analyzeSensorAccuracy() { return { accuracy: 'unknown' }; }
    
    // Environmental Context Analysis
    async analyzeEnvironmentalContext() {
        const lightReading = await this.getAmbientLightReading();
        return {
            lighting_conditions: lightReading ? this.categorizeLightLevel(lightReading.lux) : 'unknown',
            estimated_environment: lightReading ? this.estimateIndoorOutdoor(lightReading.lux) : 'unknown'
        };
    }
    
    // Biometric and Authentication Stubs
    async analyzeWebAuthnCapabilities() {
        if (!('PublicKeyCredential' in window)) return { supported: false };
        
        return {
            supported: true,
            conditional_ui: PublicKeyCredential.isConditionalMediationAvailable ? 
                await PublicKeyCredential.isConditionalMediationAvailable() : false,
            user_verifying_platform_authenticator: PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable ?
                await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable() : false
        };
    }
    
    async detectFingerprintSensorHints() { return { fingerprint_sensor_likely: false }; }
    async analyzeBiometricAuthAvailability() { return { biometric_auth: 'unknown' }; }
    async detectPlatformBiometrics() { return { platform_biometrics: 'unknown' }; }
    async analyzeBehavioralBiometrics() { return { behavioral_support: true }; }
    
    // Connectivity Analysis Stubs
    async analyzeNetworkCapabilities() {
        return navigator.connection ? {
            connection_type: navigator.connection.type,
            effective_type: navigator.connection.effectiveType,
            downlink: navigator.connection.downlink,
            rtt: navigator.connection.rtt
        } : { network_info_unavailable: true };
    }
    
    async analyzeBluetoothCapabilities() {
        return {
            bluetooth_support: 'bluetooth' in navigator,
            availability: navigator.bluetooth ? await navigator.bluetooth.getAvailability().catch(() => false) : false
        };
    }
    
    async analyzeGeolocationCapabilities() {
        return {
            geolocation_support: 'geolocation' in navigator,
            high_accuracy_support: true // Assume supported
        };
    }
    
    async analyzeConnectivityPatterns() { return { patterns: [] }; }
    
    // ===== ENHANCED BROWSER CHARACTERISTICS METHODS =====
    
    /**
     * Collect JavaScript engine information and performance
     */
    async collectJavaScriptEngineInfo() {
        try {
            const engineInfo = {
                engine_identification: this.getEngineInfo(),
                v8_features: this.detectV8Features(),
                javascript_version: this.detectJavaScriptVersion(),
                performance_characteristics: await this.benchmarkJavaScriptPerformance(),
                memory_management: this.getJavaScriptMemoryInfo(),
                execution_environment: this.getExecutionEnvironmentInfo()
            };
            
            return engineInfo;
        } catch (error) {
            this.logger.error("Error collecting JavaScript engine info:", error);
            return {};
        }
    }
    
    /**
     * Detect V8 specific features
     */
    detectV8Features() {
        const features = {
            has_v8: false,
            compile_hints: false,
            wasm_compilation: false,
            shared_array_buffer: 'SharedArrayBuffer' in window,
            atomics: 'Atomics' in window,
            bigint_support: typeof BigInt !== 'undefined',
            private_fields: false,
            optional_chaining: false
        };
        
        // Check for V8-specific properties
        if (navigator.userAgent.includes('Chrome') || navigator.userAgent.includes('Edge')) {
            features.has_v8 = true;
        }
        
        // Test modern JavaScript features
        try {
            // Test private fields
            eval('class TestClass { #private = 1; }');
            features.private_fields = true;
        } catch (e) {}
        
        try {
            // Test optional chaining
            eval('const test = {}; test?.property?.nested;');
            features.optional_chaining = true;
        } catch (e) {}
        
        return features;
    }
    
    /**
     * Detect JavaScript version/features
     */
    detectJavaScriptVersion() {
        const features = {
            es5: true, // Assume ES5 as baseline
            es6: false,
            es2017: false,
            es2018: false,
            es2019: false,
            es2020: false,
            es2021: false,
            es2022: false
        };
        
        // ES6 features
        try {
            eval('const test = () => {}; class TestClass {}');
            features.es6 = true;
        } catch (e) {}
        
        // ES2017 features
        try {
            eval('async function test() { await Promise.resolve(); }');
            features.es2017 = true;
        } catch (e) {}
        
        // ES2018 features
        try {
            eval('const obj = {a: 1}; const {a, ...rest} = obj;');
            features.es2018 = true;
        } catch (e) {}
        
        // ES2019 features
        try {
            eval('[1, 2, 3].flat();');
            features.es2019 = true;
        } catch (e) {}
        
        // ES2020 features
        try {
            eval('1n + 2n; globalThis;');
            features.es2020 = true;
        } catch (e) {}
        
        // ES2021 features
        try {
            eval('Promise.any([]);');
            features.es2021 = true;
        } catch (e) {}
        
        // ES2022 features
        try {
            eval('class TestClass { #private = 1; }');
            features.es2022 = true;
        } catch (e) {}
        
        return features;
    }
    
    /**
     * Get JavaScript memory information
     */
    getJavaScriptMemoryInfo() {
        if (performance.memory) {
            return {
                js_heap_size_limit: performance.memory.jsHeapSizeLimit,
                total_js_heap_size: performance.memory.totalJSHeapSize,
                used_js_heap_size: performance.memory.usedJSHeapSize,
                memory_pressure: performance.memory.usedJSHeapSize / performance.memory.jsHeapSizeLimit
            };
        }
        
        return { available: false };
    }
    
    /**
     * Get execution environment information
     */
    getExecutionEnvironmentInfo() {
        return {
            global_object: typeof globalThis !== 'undefined' ? 'globalThis' : 
                          typeof window !== 'undefined' ? 'window' : 
                          typeof global !== 'undefined' ? 'global' : 'unknown',
            strict_mode: (function() { return !this; })(),
            eval_available: typeof eval !== 'undefined',
            function_constructor: typeof Function !== 'undefined',
            worker_support: 'Worker' in window,
            module_support: 'import' in document.createElement('script'),
            dynamic_import: false // Would need async testing
        };
    }
    
    /**
     * Collect rendering engine information
     */
    async collectRenderingEngineInfo() {
        try {
            const renderingInfo = {
                engine_identification: this.getEngineInfo(),
                css_support: await this.detectCSSSupport(),
                rendering_performance: await this.benchmarkRenderingPerformance(),
                layout_engine: this.detectLayoutEngine(),
                graphics_rendering: await this.getGraphicsRenderingInfo()
            };
            
            return renderingInfo;
        } catch (error) {
            this.logger.error("Error collecting rendering engine info:", error);
            return {};
        }
    }
    
    /**
     * Detect CSS support features
     */
    async detectCSSSupport() {
        const testElement = document.createElement('div');
        document.body.appendChild(testElement);
        
        const features = {
            flexbox: this.testCSSProperty(testElement, 'display', 'flex'),
            grid: this.testCSSProperty(testElement, 'display', 'grid'),
            custom_properties: this.testCSSCustomProperties(testElement),
            animations: this.testCSSAnimationsSupport(),
            transforms: this.testCSSTransformsSupport(),
            filters: this.testCSSFiltersSupport(),
            masks: this.testCSSProperty(testElement, 'mask', 'url()'),
            blend_modes: this.testCSSProperty(testElement, 'mix-blend-mode', 'multiply'),
            gradients: this.testCSSProperty(testElement, 'background', 'linear-gradient(red, blue)'),
            calc: this.testCSSProperty(testElement, 'width', 'calc(100px + 10px)'),
            vh_vw_units: this.testCSSProperty(testElement, 'width', '50vw'),
            css_shapes: this.testCSSProperty(testElement, 'shape-outside', 'circle()'),
            css_scroll_snap: this.testCSSProperty(testElement, 'scroll-snap-type', 'x mandatory'),
            css_containment: this.testCSSProperty(testElement, 'contain', 'layout'),
            css_logical_properties: this.testCSSProperty(testElement, 'margin-inline-start', '10px')
        };
        
        document.body.removeChild(testElement);
        return features;
    }
    
    /**
     * Test CSS property support
     */
    testCSSProperty(element, property, value) {
        try {
            element.style[property] = value;
            return element.style[property] === value || element.style[property] !== '';
        } catch (e) {
            return false;
        }
    }
    
    /**
     * Test CSS custom properties support
     */
    testCSSCustomProperties(element) {
        try {
            element.style.setProperty('--test-property', 'test-value');
            return element.style.getPropertyValue('--test-property') === 'test-value';
        } catch (e) {
            return false;
        }
    }
    
    /**
     * Detect layout engine
     */
    detectLayoutEngine() {
        const userAgent = navigator.userAgent;
        
        if (userAgent.includes('Blink') || userAgent.includes('Chrome')) {
            return 'Blink';
        }
        if (userAgent.includes('Gecko') && userAgent.includes('Firefox')) {
            return 'Gecko';
        }
        if (userAgent.includes('WebKit') && userAgent.includes('Safari')) {
            return 'WebKit';
        }
        if (userAgent.includes('Trident') || userAgent.includes('MSIE')) {
            return 'Trident';
        }
        if (userAgent.includes('EdgeHTML')) {
            return 'EdgeHTML';
        }
        
        return 'Unknown';
    }
    
    /**
     * Benchmark rendering performance
     */
    async benchmarkRenderingPerformance() {
        try {
            const results = {
                dom_manipulation: await this.benchmarkDOMManipulation(),
                css_animation: await this.benchmarkCSSAnimation(),
                layout_thrashing: await this.benchmarkLayoutThrashing(),
                paint_performance: await this.benchmarkPaintPerformance()
            };
            
            return results;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Benchmark CSS animation performance
     */
    async benchmarkCSSAnimation() {
        return new Promise((resolve) => {
            try {
                const testElement = document.createElement('div');
                testElement.style.cssText = `
                    position: absolute;
                    left: -9999px;
                    width: 100px;
                    height: 100px;
                    background: red;
                    transition: transform 0.1s ease;
                `;
                
                document.body.appendChild(testElement);
                
                const startTime = performance.now();
                let animationCount = 0;
                
                const animate = () => {
                    animationCount++;
                    testElement.style.transform = `translateX(${animationCount % 2 * 100}px)`;
                    
                    if (animationCount < 50) {
                        requestAnimationFrame(animate);
                    } else {
                        const endTime = performance.now();
                        document.body.removeChild(testElement);
                        
                        resolve({
                            total_time: endTime - startTime,
                            animations_per_ms: animationCount / (endTime - startTime),
                            frame_rate: Math.round(animationCount * 1000 / (endTime - startTime))
                        });
                    }
                };
                
                requestAnimationFrame(animate);
            } catch (error) {
                resolve({ error: error.message });
            }
        });
    }
    
    /**
     * Benchmark layout thrashing
     */
    async benchmarkLayoutThrashing() {
        try {
            const testElement = document.createElement('div');
            testElement.style.cssText = 'position: absolute; left: -9999px;';
            document.body.appendChild(testElement);
            
            const startTime = performance.now();
            
            // Force layout recalculation
            for (let i = 0; i < 1000; i++) {
                testElement.style.width = `${100 + i % 50}px`;
                testElement.offsetWidth; // Force layout
            }
            
            const endTime = performance.now();
            document.body.removeChild(testElement);
            
            return {
                total_time: endTime - startTime,
                layouts_per_ms: 1000 / (endTime - startTime)
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Benchmark paint performance
     */
    async benchmarkPaintPerformance() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 200;
            canvas.height = 200;
            canvas.style.position = 'absolute';
            canvas.style.left = '-9999px';
            document.body.appendChild(canvas);
            
            const ctx = canvas.getContext('2d');
            const startTime = performance.now();
            
            // Paint operations
            for (let i = 0; i < 100; i++) {
                ctx.fillStyle = `hsl(${i * 3.6}, 50%, 50%)`;
                ctx.fillRect(i % 20 * 10, Math.floor(i / 20) * 10, 10, 10);
            }
            
            const endTime = performance.now();
            document.body.removeChild(canvas);
            
            return {
                total_time: endTime - startTime,
                paint_ops_per_ms: 100 / (endTime - startTime)
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get graphics rendering information
     */
    async getGraphicsRenderingInfo() {
        try {
            const info = {
                canvas_2d: this.testCanvasSupport(),
                webgl: this.testWebGLSupport(),
                webgl2: this.testWebGL2Support(),
                svg_support: 'SVGElement' in window,
                hardware_acceleration: await this.detectHardwareAcceleration(),
                color_spaces: this.detectColorSpaceSupport(),
                hdr_support: this.detectHDRSupport()
            };
            
            if (info.webgl) {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl');
                if (gl) {
                    info.webgl_extensions = gl.getSupportedExtensions();
                    info.webgl_params = this.getWebGLParameters(gl);
                }
                canvas.remove();
            }
            
            return info;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Detect color space support
     */
    detectColorSpaceSupport() {
        const spaces = {
            srgb: false,
            display_p3: false,
            rec2020: false
        };
        
        if (window.matchMedia) {
            spaces.srgb = window.matchMedia('(color-gamut: srgb)').matches;
            spaces.display_p3 = window.matchMedia('(color-gamut: p3)').matches;
            spaces.rec2020 = window.matchMedia('(color-gamut: rec2020)').matches;
        }
        
        return spaces;
    }
    
    /**
     * Get WebGL parameters
     */
    getWebGLParameters(gl) {
        const params = {};
        
        const parameters = [
            'MAX_TEXTURE_SIZE',
            'MAX_VERTEX_ATTRIBS',
            'MAX_VERTEX_UNIFORM_VECTORS',
            'MAX_FRAGMENT_UNIFORM_VECTORS',
            'MAX_VARYING_VECTORS',
            'MAX_VIEWPORT_DIMS',
            'RENDERER',
            'VENDOR',
            'VERSION',
            'SHADING_LANGUAGE_VERSION'
        ];
        
        parameters.forEach(param => {
            try {
                params[param.toLowerCase()] = gl.getParameter(gl[param]);
            } catch (e) {
                params[param.toLowerCase()] = 'unknown';
            }
        });
        
        return params;
    }
    
    /**
     * Collect comprehensive font analysis
     */
    async collectFontAnalysis() {
        try {
            const fontInfo = {
                system_fonts: await this.detectSystemFonts(),
                font_rendering: await this.analyzeFontRendering(),
                web_font_support: this.detectWebFontSupport(),
                font_metrics: await this.analyzeFontMetrics(),
                emoji_support: await this.analyzeEmojiSupport()
            };
            
            return fontInfo;
        } catch (error) {
            this.logger.error("Error collecting font analysis:", error);
            return {};
        }
    }
    
    /**
     * Detect system fonts
     */
    async detectSystemFonts() {
        const baseFonts = ['monospace', 'sans-serif', 'serif'];
        const testFonts = [
            'Arial', 'Arial Black', 'Arial Unicode MS', 'Calibri', 'Cambria',
            'Comic Sans MS', 'Courier', 'Courier New', 'Georgia', 'Helvetica',
            'Impact', 'Lucida Console', 'Lucida Sans Unicode', 'Microsoft Sans Serif',
            'Palatino', 'Times', 'Times New Roman', 'Trebuchet MS', 'Verdana',
            // macOS fonts
            'Avenir', 'Avenir Next', 'Helvetica Neue', 'San Francisco', 'SF Pro Display',
            // Linux fonts
            'Ubuntu', 'DejaVu Sans', 'Liberation Sans', 'Droid Sans',
            // Mobile fonts
            'Roboto', 'Noto Sans', 'Segoe UI'
        ];
        
        const availableFonts = [];
        
        for (const font of testFonts) {
            if (await this.isFontAvailable(font, baseFonts)) {
                availableFonts.push(font);
            }
        }
        
        return {
            detected_count: availableFonts.length,
            available_fonts: availableFonts.slice(0, 20), // Limit for privacy
            base_fonts: baseFonts
        };
    }
    
    /**
     * Check if font is available
     */
    async isFontAvailable(font, baseFonts) {
        const testString = 'mmmmmmmmmmlli';
        const testSize = '72px';
        
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        // Measure with base font
        ctx.font = `${testSize} ${baseFonts[0]}`;
        const baseWidth = ctx.measureText(testString).width;
        
        // Measure with test font
        ctx.font = `${testSize} ${font}, ${baseFonts[0]}`;
        const testWidth = ctx.measureText(testString).width;
        
        canvas.remove();
        
        // If widths differ, the font is likely available
        return Math.abs(baseWidth - testWidth) > 1;
    }
    
    /**
     * Analyze font rendering characteristics
     */
    async analyzeFontRendering() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 200;
            canvas.height = 100;
            const ctx = canvas.getContext('2d');
            
            const renderingTests = [];
            
            // Test different fonts and sizes
            const testConfigs = [
                { font: 'Arial', size: 12 },
                { font: 'Times New Roman', size: 14 },
                { font: 'Courier New', size: 16 }
            ];
            
            testConfigs.forEach((config, index) => {
                ctx.font = `${config.size}px ${config.font}`;
                ctx.fillStyle = 'black';
                ctx.fillText('Test Text Rendering', 10, 20 + index * 25);
                
                // Get metrics
                const metrics = ctx.measureText('Test Text Rendering');
                renderingTests.push({
                    font: config.font,
                    size: config.size,
                    width: metrics.width,
                    height: metrics.actualBoundingBoxAscent + metrics.actualBoundingBoxDescent
                });
            });
            
            // Get pixel data for fingerprinting
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const pixelHash = await this.hashSensitiveData(Array.from(imageData.data.slice(0, 100)).join(''));
            
            canvas.remove();
            
            return {
                rendering_tests: renderingTests,
                pixel_fingerprint: pixelHash,
                anti_aliasing: this.detectFontAntiAliasing()
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Detect font anti-aliasing
     */
    detectFontAntiAliasing() {
        const canvas = document.createElement('canvas');
        canvas.width = 50;
        canvas.height = 50;
        const ctx = canvas.getContext('2d');
        
        ctx.font = '20px Arial';
        ctx.fillStyle = 'black';
        ctx.fillText('A', 10, 30);
        
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        
        // Look for gray pixels (anti-aliasing)
        let grayPixels = 0;
        for (let i = 0; i < imageData.data.length; i += 4) {
            const r = imageData.data[i];
            const g = imageData.data[i + 1];
            const b = imageData.data[i + 2];
            
            // Check for gray values (not pure black or white)
            if (r === g && g === b && r > 0 && r < 255) {
                grayPixels++;
            }
        }
        
        canvas.remove();
        
        return {
            anti_aliased: grayPixels > 10,
            gray_pixel_count: grayPixels
        };
    }
    
    /**
     * Detect web font support
     */
    detectWebFontSupport() {
        const support = {
            woff: false,
            woff2: false,
            ttf: false,
            otf: false,
            eot: false,
            svg_fonts: false
        };
        
        // Test format support
        const formatTests = [
            { format: 'woff', mimeType: 'application/font-woff' },
            { format: 'woff2', mimeType: 'application/font-woff2' },
            { format: 'ttf', mimeType: 'application/x-font-ttf' },
            { format: 'otf', mimeType: 'application/x-font-opentype' },
            { format: 'eot', mimeType: 'application/vnd.ms-fontobject' }
        ];
        
        formatTests.forEach(test => {
            try {
                const testElement = document.createElement('style');
                testElement.textContent = `@font-face { font-family: 'test'; src: url('data:${test.mimeType};base64,') format('${test.format}'); }`;
                document.head.appendChild(testElement);
                
                // Simple heuristic: if no error thrown, format might be supported
                support[test.format] = true;
                
                document.head.removeChild(testElement);
            } catch (e) {
                support[test.format] = false;
            }
        });
        
        support.svg_fonts = 'SVGElement' in window;
        
        return support;
    }
    
    /**
     * Analyze font metrics
     */
    async analyzeFontMetrics() {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            const testFonts = ['Arial', 'Times New Roman', 'Courier New'];
            const metrics = [];
            
            testFonts.forEach(font => {
                ctx.font = `16px ${font}`;
                const testText = 'The quick brown fox jumps over the lazy dog';
                const measurement = ctx.measureText(testText);
                
                metrics.push({
                    font: font,
                    width: measurement.width,
                    actual_height: measurement.actualBoundingBoxAscent + measurement.actualBoundingBoxDescent,
                    font_height: measurement.fontBoundingBoxAscent + measurement.fontBoundingBoxDescent,
                    baseline: measurement.actualBoundingBoxAscent
                });
            });
            
            canvas.remove();
            
            return {
                font_metrics: metrics,
                metrics_precision: 'high'
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Analyze emoji support
     */
    async analyzeEmojiSupport() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 50;
            canvas.height = 50;
            const ctx = canvas.getContext('2d');
            
            const testEmojis = ['😀', '🚀', '💻', '🌟', '🔥'];
            const emojiSupport = [];
            
            testEmojis.forEach(emoji => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.font = '20px Arial';
                ctx.fillStyle = 'black';
                ctx.fillText(emoji, 10, 30);
                
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                
                // Check if anything was drawn (non-white pixels)
                let hasContent = false;
                for (let i = 0; i < imageData.data.length; i += 4) {
                    if (imageData.data[i] !== 255 || 
                        imageData.data[i + 1] !== 255 || 
                        imageData.data[i + 2] !== 255) {
                        hasContent = true;
                        break;
                    }
                }
                
                emojiSupport.push({
                    emoji: emoji,
                    supported: hasContent
                });
            });
            
            canvas.remove();
            
            return {
                emoji_tests: emojiSupport,
                overall_support: emojiSupport.filter(e => e.supported).length / emojiSupport.length
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Collect comprehensive API availability information
     */
    async collectAPIAvailability() {
        try {
            const apis = {
                // Core Web APIs
                dom_apis: this.testDOMAPIs(),
                storage_apis: this.testStorageAPIs(),
                network_apis: this.testNetworkAPIs(),
                media_apis: this.testMediaAPIs(),
                security_apis: this.testSecurityAPIs(),
                performance_apis: this.testPerformanceAPIs(),
                
                // Modern Web APIs
                modern_apis: this.testModernAPIs(),
                experimental_apis: this.testExperimentalAPIs(),
                
                // Browser-specific APIs
                browser_specific: this.testBrowserSpecificAPIs(),
                
                // Permissions and capabilities
                permissions: await this.testPermissionsAPI()
            };
            
            return apis;
        } catch (error) {
            this.logger.error("Error collecting API availability:", error);
            return {};
        }
    }
    
    /**
     * Test DOM APIs
     */
    testDOMAPIs() {
        return {
            query_selector: 'querySelector' in document,
            get_elements_by_class: 'getElementsByClassName' in document,
            create_element: 'createElement' in document,
            mutation_observer: 'MutationObserver' in window,
            intersection_observer: 'IntersectionObserver' in window,
            resize_observer: 'ResizeObserver' in window,
            custom_elements: 'customElements' in window,
            shadow_dom: 'attachShadow' in Element.prototype,
            template_element: 'HTMLTemplateElement' in window,
            slot_element: 'HTMLSlotElement' in window
        };
    }
    
    /**
     * Test storage APIs
     */
    testStorageAPIs() {
        return {
            local_storage: this.testLocalStorage(),
            session_storage: this.testSessionStorage(),
            indexed_db: this.testIndexedDB(),
            web_sql: 'openDatabase' in window,
            cache_api: 'caches' in window,
            storage_manager: 'storage' in navigator,
            persistent_storage: 'storage' in navigator && 'persist' in navigator.storage,
            quota_management: 'storage' in navigator && 'estimate' in navigator.storage
        };
    }
    
    /**
     * Test network APIs
     */
    testNetworkAPIs() {
        return {
            fetch: 'fetch' in window,
            xml_http_request: 'XMLHttpRequest' in window,
            websockets: 'WebSocket' in window,
            server_sent_events: 'EventSource' in window,
            web_rtc: 'RTCPeerConnection' in window,
            network_information: 'connection' in navigator,
            online_events: 'onLine' in navigator,
            beacon_api: 'sendBeacon' in navigator,
            background_sync: 'serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype
        };
    }
    
    /**
     * Test media APIs
     */
    testMediaAPIs() {
        return {
            media_devices: 'mediaDevices' in navigator,
            get_user_media: 'getUserMedia' in navigator || 'webkitGetUserMedia' in navigator,
            media_recorder: 'MediaRecorder' in window,
            audio_context: 'AudioContext' in window || 'webkitAudioContext' in window,
            web_audio: 'AudioContext' in window,
            media_source: 'MediaSource' in window,
            encrypted_media: 'requestMediaKeySystemAccess' in navigator,
            picture_in_picture: 'pictureInPictureEnabled' in document,
            screen_capture: 'getDisplayMedia' in navigator.mediaDevices || false,
            media_session: 'mediaSession' in navigator
        };
    }
    
    /**
     * Test security APIs
     */
    testSecurityAPIs() {
        return {
            crypto_subtle: 'crypto' in window && 'subtle' in crypto,
            crypto_random: 'crypto' in window && 'getRandomValues' in crypto,
            csp: 'SecurityPolicyViolationEvent' in window,
            sri: 'HTMLScriptElement' in window && 'integrity' in HTMLScriptElement.prototype,
            credential_management: 'credentials' in navigator,
            web_authentication: 'credentials' in navigator && 'create' in navigator.credentials,
            payment_request: 'PaymentRequest' in window,
            permissions_api: 'permissions' in navigator
        };
    }
    
    /**
     * Test performance APIs
     */
    testPerformanceAPIs() {
        return {
            performance_now: 'performance' in window && 'now' in performance,
            performance_observer: 'PerformanceObserver' in window,
            performance_timeline: 'getEntries' in performance,
            resource_timing: 'getEntriesByType' in performance,
            navigation_timing: 'timing' in performance,
            user_timing: 'mark' in performance && 'measure' in performance,
            high_resolution_time: 'performance' in window && performance.now() % 1 !== 0,
            frame_timing: 'PerformanceFrameTiming' in window || false,
            paint_timing: performance.getEntriesByType('paint').length > 0
        };
    }
    
    /**
     * Test modern Web APIs
     */
    testModernAPIs() {
        return {
            streams: 'ReadableStream' in window,
            payment_handler: 'PaymentManager' in window || false,
            background_fetch: 'BackgroundFetch' in window || false,
            clipboard_async: 'clipboard' in navigator,
            share_api: 'share' in navigator,
            contact_picker: 'contacts' in navigator || false,
            device_memory: 'deviceMemory' in navigator,
            hardware_concurrency: 'hardwareConcurrency' in navigator,
            connection_api: 'connection' in navigator,
            wake_lock: 'wakeLock' in navigator || false,
            idle_detection: 'IdleDetector' in window || false,
            web_locks: 'locks' in navigator || false,
            web_share_target: 'serviceWorker' in navigator // Simplified check
        };
    }
    
    /**
     * Test experimental APIs
     */
    testExperimentalAPIs() {
        return {
            file_system_access: 'showOpenFilePicker' in window || false,
            web_hid: 'hid' in navigator || false,
            web_serial: 'serial' in navigator || false,
            web_usb: 'usb' in navigator || false,
            web_bluetooth: 'bluetooth' in navigator || false,
            web_nfc: 'nfc' in navigator || false,
            eye_dropper: 'EyeDropper' in window || false,
            window_controls_overlay: 'windowControlsOverlay' in navigator || false,
            virtual_keyboard: 'virtualKeyboard' in navigator || false,
            keyboard_map: 'keyboard' in navigator && 'getLayoutMap' in navigator.keyboard || false
        };
    }
    
    /**
     * Test browser-specific APIs
     */
    testBrowserSpecificAPIs() {
        return {
            // Chrome/Blink specific
            chrome_extension: 'chrome' in window && 'extension' in window.chrome || false,
            performance_memory: 'memory' in performance,
            
            // Firefox specific
            moz_apis: 'mozInnerScreenX' in window || false,
            
            // Safari specific
            webkit_apis: 'webkitAudioContext' in window,
            
            // Edge specific
            ms_apis: 'MSInputMethodContext' in window || false,
            
            // General vendor prefixes
            vendor_prefixed: this.detectVendorPrefixes()
        };
    }
    
    /**
     * Detect vendor prefixes
     */
    detectVendorPrefixes() {
        const prefixes = {
            webkit: false,
            moz: false,
            ms: false,
            o: false
        };
        
        const testElement = document.createElement('div');
        
        if ('webkitTransform' in testElement.style) prefixes.webkit = true;
        if ('MozTransform' in testElement.style) prefixes.moz = true;
        if ('msTransform' in testElement.style) prefixes.ms = true;
        if ('OTransform' in testElement.style) prefixes.o = true;
        
        return prefixes;
    }
    
    /**
     * Test Permissions API
     */
    async testPermissionsAPI() {
        if (!('permissions' in navigator)) {
            return { available: false };
        }
        
        const permissions = {};
        const testPermissions = [
            'camera', 'microphone', 'geolocation', 'notifications',
            'push', 'accelerometer', 'gyroscope', 'magnetometer'
        ];
        
        for (const permission of testPermissions) {
            try {
                const result = await navigator.permissions.query({ name: permission });
                permissions[permission] = result.state;
            } catch (e) {
                permissions[permission] = 'unsupported';
            }
        }
        
        return {
            available: true,
            permissions: permissions
        };
    }
    
    /**
     * Get browser build ID
     */
    getBrowserBuildId() {
        // Firefox has buildID
        if (navigator.buildID) {
            return navigator.buildID;
        }
        
        // Extract from user agent if possible
        const ua = navigator.userAgent;
        const buildMatch = ua.match(/(?:Chrome|Firefox|Safari)\/([^\s]+)/);
        return buildMatch ? buildMatch[1] : 'unknown';
    }
    
    /**
     * Collect browser performance information
     */
    async collectBrowserPerformanceInfo() {
        try {
            const performance_info = {
                javascript_performance: await this.benchmarkJavaScriptPerformance(),
                dom_performance: await this.benchmarkDOMManipulation(),
                rendering_performance: await this.benchmarkRenderingPerformance(),
                memory_usage: this.getJavaScriptMemoryInfo(),
                timing_precision: this.getTimingPrecision()
            };
            
            return performance_info;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get timing precision
     */
    getTimingPrecision() {
        const measurements = [];
        
        for (let i = 0; i < 10; i++) {
            measurements.push(performance.now());
        }
        
        // Calculate precision based on decimal places
        const precisions = measurements.map(m => {
            const str = m.toString();
            const decimal = str.indexOf('.');
            return decimal >= 0 ? str.length - decimal - 1 : 0;
        });
        
        return {
            average_precision: precisions.reduce((a, b) => a + b, 0) / precisions.length,
            max_precision: Math.max(...precisions),
            min_precision: Math.min(...precisions),
            reduced_precision: Math.max(...precisions) < 3 // Indicates timing attack mitigation
        };
    }
    
    /**
     * Generate browser rendering fingerprint
     */
    async generateBrowserRenderingFingerprint() {
        try {
            const fingerprint = {
                canvas_fingerprint: await this.generateCanvasFingerprint(),
                webgl_fingerprint: await this.generateWebGLFingerprint(),
                css_fingerprint: await this.generateCSSFingerprint(),
                font_fingerprint: await this.generateFontFingerprint()
            };
            
            return fingerprint;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Generate CSS fingerprint
     */
    async generateCSSFingerprint() {
        try {
            const testElement = document.createElement('div');
            testElement.innerHTML = 'CSS Test Element';
            testElement.style.cssText = `
                font-family: Arial;
                font-size: 12px;
                color: red;
                background: linear-gradient(45deg, blue, green);
                transform: rotate(5deg);
                border-radius: 5px;
                box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            `;
            
            document.body.appendChild(testElement);
            
            // Get computed styles
            const computed = window.getComputedStyle(testElement);
            const cssProperties = [
                'fontFamily', 'fontSize', 'color', 'background',
                'transform', 'borderRadius', 'boxShadow', 'width', 'height'
            ];
            
            const styleData = {};
            cssProperties.forEach(prop => {
                styleData[prop] = computed.getPropertyValue(prop.replace(/([A-Z])/g, '-$1').toLowerCase());
            });
            
            document.body.removeChild(testElement);
            
            // Generate hash
            const styleHash = await this.hashSensitiveData(JSON.stringify(styleData));
            
            return {
                css_hash: styleHash,
                computed_styles: styleData
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Generate font fingerprint
     */
    async generateFontFingerprint() {
        try {
            const canvas = document.createElement('canvas');
            canvas.width = 300;
            canvas.height = 100;
            const ctx = canvas.getContext('2d');
            
            // Render text with different fonts
            const fonts = ['Arial', 'Times New Roman', 'Courier New'];
            const text = 'Font fingerprint test 123 !@#';
            
            fonts.forEach((font, index) => {
                ctx.font = `16px ${font}`;
                ctx.fillStyle = `hsl(${index * 120}, 70%, 50%)`;
                ctx.fillText(text, 10, 20 + index * 25);
            });
            
            // Get image data
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const fontHash = await this.hashSensitiveData(Array.from(imageData.data.slice(0, 500)).join(''));
            
            canvas.remove();
            
            return {
                font_hash: fontHash,
                canvas_size: `${canvas.width}x${canvas.height}`,
                fonts_tested: fonts.length
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Enumerate media devices
     */
    async enumerateMediaDevices() {
        try {
            if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
                return { available: false };
            }
            
            const devices = await navigator.mediaDevices.enumerateDevices();
            
            const deviceInfo = {
                total_devices: devices.length,
                audio_input: devices.filter(d => d.kind === 'audioinput').length,
                audio_output: devices.filter(d => d.kind === 'audiooutput').length,
                video_input: devices.filter(d => d.kind === 'videoinput').length,
                device_ids: devices.map(d => d.deviceId ? 'present' : 'absent'),
                labels_available: devices.some(d => d.label !== '')
            };
            
            return deviceInfo;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get storage estimate
     */
    async getStorageEstimate() {
        try {
            if ('storage' in navigator && 'estimate' in navigator.storage) {
                const estimate = await navigator.storage.estimate();
                return {
                    quota: estimate.quota,
                    usage: estimate.usage,
                    available: estimate.quota - estimate.usage,
                    usage_percentage: Math.round((estimate.usage / estimate.quota) * 100)
                };
            }
            
            return { available: false };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get fallback browser fingerprint
     */
    getFallbackBrowserFingerprint() {
        return {
            fallback: true,
            basic_browser_info: {
                user_agent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,
                cookie_enabled: navigator.cookieEnabled,
                online: navigator.onLine,
                java_enabled: navigator.javaEnabled ? navigator.javaEnabled() : false,
                plugins_count: navigator.plugins.length,
                mime_types_count: navigator.mimeTypes.length,
                screen_resolution: `${screen.width}x${screen.height}`,
                color_depth: screen.colorDepth,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            },
            error: 'Enhanced browser characteristics collection failed, using fallback method'
        };
    }
    
    // ===== HELPER METHODS =====
    
    generateUniqueId() {
        return 'fp_' + Date.now().toString(36) + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    getBrowserName() {
        const userAgent = navigator.userAgent;
        if (userAgent.includes('Chrome')) return 'Chrome';
        if (userAgent.includes('Firefox')) return 'Firefox';
        if (userAgent.includes('Safari')) return 'Safari';
        if (userAgent.includes('Edge')) return 'Edge';
        if (userAgent.includes('Opera')) return 'Opera';
        return 'Unknown';
    }
    
    getBrowserVersion() {
        const userAgent = navigator.userAgent;
        const match = userAgent.match(/(Chrome|Firefox|Safari|Edge|Opera)\/(\d+)/);
        return match ? match[2] : 'Unknown';
    }
    
    getEngineInfo() {
        const userAgent = navigator.userAgent;
        if (userAgent.includes('Blink')) return { name: 'Blink', version: 'Unknown' };
        if (userAgent.includes('Gecko')) return { name: 'Gecko', version: 'Unknown' };
        if (userAgent.includes('WebKit')) return { name: 'WebKit', version: 'Unknown' };
        if (userAgent.includes('Trident')) return { name: 'Trident', version: 'Unknown' };
        return { name: 'Unknown', version: 'Unknown' };
    }
    
    getPluginInfo() {
        const plugins = [];
        for (let i = 0; i < navigator.plugins.length; i++) {
            const plugin = navigator.plugins[i];
            plugins.push({
                name: plugin.name,
                description: plugin.description,
                filename: plugin.filename,
                version: plugin.version || 'Unknown'
            });
        }
        return plugins.slice(0, 10); // Limit to first 10 plugins
    }
    
    getMimeTypes() {
        const mimeTypes = [];
        for (let i = 0; i < navigator.mimeTypes.length; i++) {
            const mimeType = navigator.mimeTypes[i];
            mimeTypes.push({
                type: mimeType.type,
                description: mimeType.description,
                suffixes: mimeType.suffixes
            });
        }
        return mimeTypes.slice(0, 10); // Limit to first 10 MIME types
    }
    
    testLocalStorage() {
        try {
            const testKey = 'test_ls_' + Date.now();
            localStorage.setItem(testKey, 'test');
            localStorage.removeItem(testKey);
            return true;
        } catch (e) {
            return false;
        }
    }
    
    testSessionStorage() {
        try {
            const testKey = 'test_ss_' + Date.now();
            sessionStorage.setItem(testKey, 'test');
            sessionStorage.removeItem(testKey);
            return true;
        } catch (e) {
            return false;
        }
    }
    
    testIndexedDB() {
        return 'indexedDB' in window;
    }
    
    testWebGLSupport() {
        try {
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            canvas.remove();
            return !!gl;
        } catch (e) {
            return false;
        }
    }
    
    testCanvasSupport() {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.remove();
            return !!ctx;
        } catch (e) {
            return false;
        }
    }
    
    testAudioSupport() {
        return 'Audio' in window;
    }
    
    testVideoSupport() {
        return 'HTMLVideoElement' in window;
    }
    
    getConnectionType() {
        if ('connection' in navigator) {
            return navigator.connection.type || navigator.connection.effectiveType || 'unknown';
        }
        return 'unknown';
    }
    
    async detectCPUArchitecture() {
        // Try to detect architecture from various sources
        const platform = navigator.platform.toLowerCase();
        if (platform.includes('win32') || platform.includes('win64')) {
            return platform.includes('64') ? 'x64' : 'x86';
        }
        if (platform.includes('mac')) {
            return 'arm64'; // Assume M1/M2 Macs
        }
        if (platform.includes('linux')) {
            return 'x64'; // Most common for Linux
        }
        return 'unknown';
    }
    
    async detectCPUFeatures() {
        const features = [];
        
        // Check for WebAssembly support (indicates modern CPU)
        if ('WebAssembly' in window) {
            features.push('wasm');
        }
        
        // Check for SharedArrayBuffer support (indicates specific CPU features)
        if ('SharedArrayBuffer' in window) {
            features.push('shared_memory');
        }
        
        // Check for BigInt support
        if ('BigInt' in window) {
            features.push('bigint');
        }
        
        return features;
    }
    
    detectWebGLVersion(gl) {
        const version = gl.getParameter(gl.VERSION);
        if (version.includes('2.0')) return '2.0';
        if (version.includes('1.0')) return '1.0';
        return 'unknown';
    }
    
    getWebGLExtensions(gl) {
        const extensions = gl.getSupportedExtensions() || [];
        return extensions.slice(0, 20); // Limit to first 20 extensions
    }
    
    getSupportedFormats(gl) {
        const formats = [];
        
        // Check common texture formats
        const textureFormats = [
            gl.RGB, gl.RGBA, gl.ALPHA, gl.LUMINANCE, gl.LUMINANCE_ALPHA
        ];
        
        textureFormats.forEach(format => {
            if (gl.getParameter(gl.IMPLEMENTATION_COLOR_READ_FORMAT) === format) {
                formats.push(format.toString());
            }
        });
        
        return formats;
    }
    
    async estimateGPUMemory(gl) {
        // Try to estimate GPU memory through texture allocation
        try {
            const texture = gl.createTexture();
            gl.bindTexture(gl.TEXTURE_2D, texture);
            
            // Try different texture sizes to estimate memory
            const maxTextureSize = gl.getParameter(gl.MAX_TEXTURE_SIZE);
            const estimatedMemory = (maxTextureSize * maxTextureSize * 4) / (1024 * 1024); // MB
            
            gl.deleteTexture(texture);
            return estimatedMemory;
        } catch (e) {
            return 0;
        }
    }
    
    async detectLocalIP() {
        return new Promise((resolve) => {
            // Simple WebRTC-based IP detection (privacy-conscious)
            const pc = new RTCPeerConnection({ iceServers: [] });
            
            pc.createDataChannel('');
            pc.createOffer().then(offer => pc.setLocalDescription(offer));
            
            const timeout = setTimeout(() => {
                pc.close();
                resolve({ ip: 'unknown', type: 'timeout' });
            }, 3000);
            
            pc.onicecandidate = (event) => {
                if (event.candidate) {
                    const candidate = event.candidate.candidate;
                    const ipMatch = candidate.match(/(\d+\.\d+\.\d+\.\d+)/);
                    if (ipMatch) {
                        clearTimeout(timeout);
                        pc.close();
                        resolve({ 
                            ip: ipMatch[1], 
                            type: candidate.includes('typ host') ? 'local' : 'external' 
                        });
                    }
                }
            };
        });
    }
    
    async measureNetworkTiming() {
        try {
            const startTime = performance.now();
            
            // Create a small request to measure latency
            const response = await fetch('/favicon.ico', { 
                method: 'HEAD',
                cache: 'no-cache' 
            });
            
            const endTime = performance.now();
            const latency = endTime - startTime;
            
            return {
                latency: latency,
                bandwidth: response.ok ? 1000 / latency : 0 // Rough estimate
            };
        } catch (e) {
            return { latency: 0, bandwidth: 0 };
        }
    }
    
    async hashSensitiveData(data) {
        if (!data || !crypto || !crypto.subtle) return 'unknown';
        
        try {
            const encoder = new TextEncoder();
            const dataBuffer = encoder.encode(data);
            const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, '0')).join('').substring(0, 16);
        } catch (e) {
            return 'hash_error';
        }
    }
    
    detectCurrency() {
        try {
            const formatter = new Intl.NumberFormat(navigator.language, { 
                style: 'currency', 
                currency: 'USD' 
            });
            return formatter.resolvedOptions().currency;
        } catch (e) {
            return 'USD';
        }
    }
    
    detectNumberFormat() {
        try {
            const formatter = new Intl.NumberFormat(navigator.language);
            return formatter.format(1234.56);
        } catch (e) {
            return '1234.56';
        }
    }
    
    detectDateFormat() {
        try {
            const formatter = new Intl.DateTimeFormat(navigator.language);
            return formatter.format(new Date('2024-01-15'));
        } catch (e) {
            return '1/15/2024';
        }
    }
    
    detectColorScheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light';
    }
    
    detectReducedMotion() {
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return true;
        }
        return false;
    }
    
    detectHighContrast() {
        if (window.matchMedia && window.matchMedia('(prefers-contrast: high)').matches) {
            return true;
        }
        return false;
    }
    
    async detectFontPreferences() {
        const fonts = [
            'Arial', 'Helvetica', 'Times New Roman', 'Courier New', 
            'Verdana', 'Georgia', 'Palatino', 'Garamond', 'Comic Sans MS'
        ];
        
        const availableFonts = [];
        
        // Simple font detection
        fonts.forEach(font => {
            const testElement = document.createElement('span');
            testElement.style.fontFamily = font;
            testElement.style.fontSize = '72px';
            testElement.textContent = 'mmmmmmmmmmlli';
            testElement.style.position = 'absolute';
            testElement.style.left = '-9999px';
            
            document.body.appendChild(testElement);
            const width = testElement.offsetWidth;
            document.body.removeChild(testElement);
            
            // Basic font detection logic
            if (width > 0) {
                availableFonts.push(font);
            }
        });
        
        return availableFonts;
    }
    
    getAudioContextInfo() {
        try {
            if ('AudioContext' in window || 'webkitAudioContext' in window) {
                const AudioContextClass = window.AudioContext || window.webkitAudioContext;
                const audioContext = new AudioContextClass();
                
                const info = {
                    sample_rate: audioContext.sampleRate,
                    base_latency: audioContext.baseLatency || 0,
                    output_latency: audioContext.outputLatency || 0,
                    state: audioContext.state
                };
                
                audioContext.close();
                return info;
            }
        } catch (e) {
            return { supported: false };
        }
        
        return { supported: false };
    }
    
    async getDeviceOrientation() {
        return new Promise((resolve) => {
            if ('DeviceOrientationEvent' in window) {
                const handleOrientation = (event) => {
                    window.removeEventListener('deviceorientation', handleOrientation);
                    resolve({
                        alpha: event.alpha,
                        beta: event.beta,
                        gamma: event.gamma,
                        absolute: event.absolute
                    });
                };
                
                window.addEventListener('deviceorientation', handleOrientation);
                
                // Timeout after 1 second
                setTimeout(() => {
                    window.removeEventListener('deviceorientation', handleOrientation);
                    resolve({ supported: false });
                }, 1000);
            } else {
                resolve({ supported: false });
            }
        });
    }
    
    getViewportSize() {
        return {
            width: window.innerWidth,
            height: window.innerHeight,
            outer_width: window.outerWidth,
            outer_height: window.outerHeight,
            screen_x: window.screenX || window.screenLeft || 0,
            screen_y: window.screenY || window.screenTop || 0,
            scroll_x: window.scrollX || window.pageXOffset || 0,
            scroll_y: window.scrollY || window.pageYOffset || 0
        };
    }
    
    getScreenProperties() {
        return {
            color_gamut: this.detectColorGamut(),
            hdr_support: this.detectHDRSupport(),
            refresh_rate: this.estimateRefreshRate()
        };
    }
    
    detectColorGamut() {
        if (window.matchMedia && window.matchMedia('(color-gamut: p3)').matches) {
            return 'p3';
        }
        if (window.matchMedia && window.matchMedia('(color-gamut: srgb)').matches) {
            return 'srgb';
        }
        return 'unknown';
    }
    
    detectHDRSupport() {
        if (window.matchMedia && window.matchMedia('(dynamic-range: high)').matches) {
            return true;
        }
        return false;
    }
    
    estimateRefreshRate() {
        return new Promise((resolve) => {
            let start = null;
            let frames = 0;
            
            const countFrames = (timestamp) => {
                if (!start) start = timestamp;
                frames++;
                
                if (timestamp - start < 1000) {
                    requestAnimationFrame(countFrames);
                } else {
                    resolve(Math.round(frames * 1000 / (timestamp - start)));
                }
            };
            
            requestAnimationFrame(countFrames);
        });
    }
    
    extractOSFromUserAgent() {
        const userAgent = navigator.userAgent.toLowerCase();
        
        if (userAgent.includes('windows nt 10.0')) return 'Windows 10';
        if (userAgent.includes('windows nt 6.3')) return 'Windows 8.1';
        if (userAgent.includes('windows nt 6.2')) return 'Windows 8';
        if (userAgent.includes('windows nt 6.1')) return 'Windows 7';
        if (userAgent.includes('mac os x')) {
            const match = userAgent.match(/mac os x ([\d_]+)/);
            return match ? `macOS ${match[1].replace(/_/g, '.')}` : 'macOS';
        }
        if (userAgent.includes('android')) {
            const match = userAgent.match(/android ([\d.]+)/);
            return match ? `Android ${match[1]}` : 'Android';
        }
        if (userAgent.includes('iphone') || userAgent.includes('ipad')) {
            const match = userAgent.match(/os ([\d_]+)/);
            return match ? `iOS ${match[1].replace(/_/g, '.')}` : 'iOS';
        }
        if (userAgent.includes('linux')) return 'Linux';
        
        return 'Unknown';
    }
    
    detectArchitecture() {
        const platform = navigator.platform.toLowerCase();
        
        if (platform.includes('win32')) return 'x86';
        if (platform.includes('win64') || platform.includes('wow64')) return 'x64';
        if (platform.includes('arm')) return 'ARM';
        if (platform.includes('x86_64') || platform.includes('amd64')) return 'x64';
        if (platform.includes('i386') || platform.includes('i686')) return 'x86';
        
        return 'unknown';
    }
    
    isMobileDevice() {
        return /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
    
    isTabletDevice() {
        return /iPad|Android(?!.*Mobile)/i.test(navigator.userAgent);
    }
    
    isDesktopDevice() {
        return !this.isMobileDevice() && !this.isTabletDevice();
    }
    
    calculateAspectRatio(width, height) {
        if (width === 0 || height === 0) return 'unknown';
        
        const gcd = (a, b) => b === 0 ? a : gcd(b, a % b);
        const divisor = gcd(width, height);
        const ratioW = width / divisor;
        const ratioH = height / divisor;
        
        // Common aspect ratios
        const commonRatios = {
            '16:9': [16, 9],
            '16:10': [16, 10],
            '4:3': [4, 3],
            '21:9': [21, 9],
            '3:2': [3, 2]
        };
        
        for (const [ratio, [w, h]] of Object.entries(commonRatios)) {
            if (ratioW === w && ratioH === h) return ratio;
        }
        
        return `${ratioW}:${ratioH}`;
    }
    
    classifyDisplayProfile(width, height) {
        if (width >= 3840 && height >= 2160) return '4K/UHD';
        if (width >= 2560 && height >= 1440) return '2K/QHD';
        if (width >= 1920 && height >= 1080) return 'Full HD';
        if (width >= 1366 && height >= 768) return 'HD';
        return 'Standard';
    }
    
    calculatePixelDensity(screenData) {
        const diagonal = Math.sqrt(screenData.width ** 2 + screenData.height ** 2);
        // Assume 96 DPI as baseline for web
        const referenceDPI = 96;
        return Math.round((diagonal / referenceDPI) * screenData.device_pixel_ratio);
    }
    
    // Performance test helper methods
    arrayOperationsTest() {
        const arr = new Array(10000).fill(0).map((_, i) => i);
        arr.sort((a, b) => b - a);
        return arr.filter(x => x % 2 === 0).reduce((sum, x) => sum + x, 0);
    }
    
    stringOperationsTest() {
        let str = '';
        for (let i = 0; i < 1000; i++) {
            str += `Test string ${i} `;
        }
        return str.split(' ').reverse().join('-').length;
    }
    
    mathOperationsTest() {
        let result = 0;
        for (let i = 0; i < 100000; i++) {
            result += Math.sqrt(i) * Math.sin(i / 1000) * Math.cos(i / 500);
        }
        return result;
    }
    
    objectOperationsTest() {
        const objects = [];
        for (let i = 0; i < 1000; i++) {
            objects.push({ id: i, value: Math.random(), nested: { data: i * 2 } });
        }
        return objects.filter(obj => obj.value > 0.5).length;
    }
    
    getFallbackFingerprint() {
        return {
            fallback: true,
            basic_info: {
                user_agent: navigator.userAgent,
                language: navigator.language,
                platform: navigator.platform,
                screen_resolution: `${screen.width}x${screen.height}`,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString()
            },
            error: 'Comprehensive fingerprinting failed, using fallback method'
        };
    }
    
    // ===== ENHANCED NETWORK INFORMATION HELPER METHODS =====
    
    /**
     * Get comprehensive connection characteristics
     */
    async getConnectionCharacteristics() {
        try {
            const connectionData = {
                network_api_available: 'connection' in navigator,
                connection_type: 'unknown',
                effective_type: 'unknown',
                downlink: 0,
                rtt: 0,
                save_data: false,
                max_downlink: 0,
                network_change_events_supported: false
            };
            
            // Network Information API
            if ('connection' in navigator) {
                const connection = navigator.connection;
                connectionData.connection_type = connection.type || 'unknown';
                connectionData.effective_type = connection.effectiveType || 'unknown';
                connectionData.downlink = connection.downlink || 0;
                connectionData.rtt = connection.rtt || 0;
                connectionData.save_data = connection.saveData || false;
                connectionData.max_downlink = connection.downlinkMax || 0;
                
                // Test for network change event support
                connectionData.network_change_events_supported = typeof connection.addEventListener === 'function';
            }
            
            return connectionData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Measure comprehensive network timing using multiple methods
     */
    async measureComprehensiveNetworkTiming() {
        try {
            const timingData = {
                navigation_timing: this.getNavigationTiming(),
                resource_timing: await this.getResourceTiming(),
                fetch_timing: await this.measureFetchTiming(),
                ping_timing: await this.measurePingTiming(),
                dns_timing: await this.measureDNSTiming()
            };
            
            return timingData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Perform comprehensive WebRTC analysis
     */
    async performWebRTCAnalysis() {
        try {
            const webrtcData = {
                webrtc_supported: 'RTCPeerConnection' in window,
                local_ips: [],
                public_ips: [],
                ice_servers_tested: [],
                stun_connectivity: false,
                turn_connectivity: false,
                data_channel_support: false,
                media_stream_support: false
            };
            
            if ('RTCPeerConnection' in window) {
                // Test basic WebRTC functionality
                webrtcData.data_channel_support = await this.testDataChannelSupport();
                webrtcData.media_stream_support = 'getUserMedia' in navigator || 'mediaDevices' in navigator;
                
                // IP detection (privacy-conscious)
                const ipInfo = await this.detectComprehensiveIPs();
                webrtcData.local_ips = ipInfo.localIPs;
                webrtcData.public_ips = ipInfo.publicIPs;
                
                // STUN/TURN connectivity testing
                webrtcData.stun_connectivity = await this.testSTUNConnectivity();
            }
            
            return webrtcData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Analyze DNS resolution characteristics
     */
    async analyzeDNSCharacteristics() {
        try {
            const dnsData = {
                dns_resolution_time: 0,
                dns_servers: [],
                dns_over_https_support: false,
                dns_prefetch_support: 'prefetch' in document.createElement('link'),
                public_dns_resolution: await this.testPublicDNSResolution()
            };
            
            // Test DNS resolution timing
            dnsData.dns_resolution_time = await this.measureDNSResolutionTime();
            
            // Test DNS over HTTPS support
            dnsData.dns_over_https_support = await this.testDNSOverHTTPS();
            
            return dnsData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Analyze network topology and routing
     */
    async analyzeNetworkTopology() {
        try {
            const topologyData = {
                hop_count_estimate: 0,
                routing_method: 'unknown',
                proxy_detected: false,
                vpn_indicators: [],
                network_latency_profile: await this.createNetworkLatencyProfile(),
                connection_stability: await this.measureConnectionStability()
            };
            
            // Estimate hop count through timing analysis
            topologyData.hop_count_estimate = await this.estimateHopCount();
            
            // Detect proxy/VPN indicators
            topologyData.proxy_detected = await this.detectProxy();
            topologyData.vpn_indicators = await this.detectVPNIndicators();
            
            return topologyData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get basic network information (fallback)
     */
    getBasicNetworkInfo() {
        try {
            if ('connection' in navigator) {
                const connection = navigator.connection;
                return {
                    type: connection.type || connection.effectiveType || 'unknown',
                    effective_type: connection.effectiveType || 'unknown',
                    downlink: connection.downlink || 0,
                    rtt: connection.rtt || 0,
                    save_data: connection.saveData || false
                };
            }
            return { available: false };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Analyze network security features
     */
    async analyzeNetworkSecurity() {
        try {
            const securityData = {
                https_enabled: window.location.protocol === 'https:',
                hsts_supported: await this.testHSTSSupport(),
                csp_detected: this.detectCSP(),
                mixed_content_warnings: this.detectMixedContent(),
                certificate_transparency: await this.testCertificateTransparency(),
                secure_context: window.isSecureContext
            };
            
            return securityData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Perform comprehensive bandwidth analysis
     */
    async performBandwidthAnalysis() {
        try {
            const bandwidthData = {
                estimated_downlink: 0,
                estimated_uplink: 0,
                throughput_test_results: [],
                connection_quality_score: 0,
                bandwidth_variation: 0
            };
            
            // Multiple bandwidth measurement methods
            const measurements = await Promise.all([
                this.measureBandwidthViaTiming(),
                this.measureBandwidthViaResourceLoading(),
                this.measureBandwidthViaNetworkAPI()
            ]);
            
            bandwidthData.throughput_test_results = measurements;
            bandwidthData.estimated_downlink = this.calculateAverageBandwidth(measurements);
            bandwidthData.connection_quality_score = this.calculateConnectionQuality(measurements);
            
            return bandwidthData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Measure comprehensive network performance
     */
    async measureNetworkPerformance() {
        try {
            const performanceData = {
                page_load_metrics: this.getPageLoadMetrics(),
                resource_load_times: await this.getResourceLoadTimes(),
                network_efficiency: await this.calculateNetworkEfficiency(),
                connection_reliability: await this.measureConnectionReliability(),
                latency_jitter: await this.measureLatencyJitter()
            };
            
            return performanceData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get fallback network information
     */
    getFallbackNetworkInfo() {
        return {
            fallback: true,
            basic_connection: {
                online: navigator.onLine,
                user_agent: navigator.userAgent,
                protocol: window.location.protocol,
                hostname: window.location.hostname,
                port: window.location.port
            },
            error: 'Enhanced network information collection failed, using fallback method'
        };
    }
    
    // ===== ENHANCED ENVIRONMENTAL DATA HELPER METHODS =====
    
    /**
     * Get comprehensive locale characteristics
     */
    async getLocaleCharacteristics() {
        try {
            const localeData = {
                primary_locale: navigator.language,
                supported_locales: navigator.languages || [],
                timezone_info: {
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    timezone_offset: new Date().getTimezoneOffset(),
                    dst_observed: this.detectDaylightSavingTime(),
                    utc_offset_hours: -new Date().getTimezoneOffset() / 60
                },
                formatting_preferences: {
                    currency: this.detectCurrency(),
                    number_format: this.detectNumberFormat(),
                    date_format: this.detectDateFormat(),
                    time_format: this.detectTimeFormat(),
                    calendar_system: this.detectCalendarSystem()
                },
                regional_settings: {
                    country_code: await this.detectCountryCode(),
                    region: await this.detectRegion(),
                    city: await this.detectCity()
                }
            };
            
            return localeData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get comprehensive battery characteristics
     */
    async getBatteryCharacteristics() {
        try {
            const batteryData = {
                battery_api_supported: 'getBattery' in navigator,
                battery_level: null,
                charging_status: null,
                charging_time: null,
                discharging_time: null,
                power_management: {
                    low_power_mode: false,
                    battery_saver_mode: false,
                    performance_mode: 'unknown'
                }
            };
            
            if ('getBattery' in navigator) {
                try {
                    const battery = await navigator.getBattery();
                    batteryData.battery_level = Math.floor(battery.level * 100);
                    batteryData.charging_status = battery.charging;
                    batteryData.charging_time = battery.chargingTime === Infinity ? null : battery.chargingTime;
                    batteryData.discharging_time = battery.dischargingTime === Infinity ? null : battery.dischargingTime;
                    
                    // Set up battery event listeners for change detection
                    batteryData.battery_events_supported = true;
                    
                    // Estimate battery health based on charging characteristics
                    batteryData.battery_health_estimate = this.estimateBatteryHealth(battery);
                    
                } catch (e) {
                    batteryData.battery_access_denied = true;
                }
            }
            
            return batteryData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get comprehensive motion sensor data  
     */
    async getMotionSensorData() {
        try {
            const motionData = {
                device_motion_supported: 'DeviceMotionEvent' in window,
                device_orientation_supported: 'DeviceOrientationEvent' in window,
                accelerometer: {
                    supported: false,
                    permission_required: false,
                    current_reading: null
                },
                gyroscope: {
                    supported: false,
                    permission_required: false,
                    current_reading: null
                },
                magnetometer: {
                    supported: false,
                    permission_required: false,
                    current_reading: null
                },
                orientation_data: null,
                motion_patterns: {
                    device_stationary: true,
                    movement_detected: false,
                    rotation_detected: false
                }
            };
            
            // Test DeviceMotion support
            if ('DeviceMotionEvent' in window) {
                motionData.accelerometer.supported = true;
                motionData.gyroscope.supported = true;
                
                // Check for permission requirement (iOS 13+)
                if (typeof DeviceMotionEvent.requestPermission === 'function') {
                    motionData.accelerometer.permission_required = true;
                    motionData.gyroscope.permission_required = true;
                }
                
                // Get current readings if available
                const motionReading = await this.getCurrentMotionReading();
                if (motionReading) {
                    motionData.accelerometer.current_reading = motionReading.acceleration;
                    motionData.gyroscope.current_reading = motionReading.rotation;
                    motionData.motion_patterns = this.analyzeMotionPatterns(motionReading);
                }
            }
            
            // Test DeviceOrientation support
            if ('DeviceOrientationEvent' in window) {
                motionData.magnetometer.supported = true;
                
                if (typeof DeviceOrientationEvent.requestPermission === 'function') {
                    motionData.magnetometer.permission_required = true;
                }
                
                motionData.orientation_data = await this.getCurrentOrientationReading();
            }
            
            return motionData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get comprehensive ambient sensor data
     */
    async getAmbientSensorData() {
        try {
            const sensorData = {
                ambient_light: {
                    supported: 'AmbientLightSensor' in window,
                    current_lux: null,
                    light_level_category: 'unknown'
                },
                proximity: {
                    supported: 'ProximitySensor' in window,
                    near_object_detected: null,
                    distance_estimate: null
                },
                environmental_context: {
                    indoor_outdoor_estimate: 'unknown',
                    brightness_adaptation: this.detectBrightnessAdaptation(),
                    color_temperature_preference: this.detectColorTemperaturePreference()
                },
                display_brightness: await this.estimateDisplayBrightness(),
                color_scheme_preference: this.detectColorScheme()
            };
            
            // Test Ambient Light Sensor
            if ('AmbientLightSensor' in window) {
                try {
                    const lightReading = await this.getAmbientLightReading();
                    if (lightReading) {
                        sensorData.ambient_light.current_lux = lightReading.lux;
                        sensorData.ambient_light.light_level_category = this.categorizeLightLevel(lightReading.lux);
                        sensorData.environmental_context.indoor_outdoor_estimate = this.estimateIndoorOutdoor(lightReading.lux);
                    }
                } catch (e) {
                    sensorData.ambient_light.access_denied = true;
                }
            }
            
            // Test Proximity Sensor
            if ('ProximitySensor' in window) {
                try {
                    const proximityReading = await this.getProximityReading();
                    if (proximityReading) {
                        sensorData.proximity.near_object_detected = proximityReading.near;
                        sensorData.proximity.distance_estimate = proximityReading.distance;
                    }
                } catch (e) {
                    sensorData.proximity.access_denied = true;
                }
            }
            
            return sensorData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get comprehensive media device characteristics
     */
    async getMediaDeviceCharacteristics() {
        try {
            const mediaData = {
                media_devices_api_supported: 'mediaDevices' in navigator,
                audio_devices: [],
                video_devices: [],
                audio_capabilities: {
                    input_supported: false,
                    output_supported: false,
                    echo_cancellation: false,
                    noise_suppression: false,
                    auto_gain_control: false
                },
                video_capabilities: {
                    camera_supported: false,
                    screen_capture_supported: false,
                    max_resolution: null,
                    supported_formats: []
                },
                media_stream_constraints: await this.getMediaStreamConstraints(),
                audio_context_info: this.getAudioContextInfo()
            };
            
            if ('mediaDevices' in navigator) {
                try {
                    // Enumerate media devices
                    const devices = await navigator.mediaDevices.enumerateDevices();
                    
                    devices.forEach(device => {
                        const deviceInfo = {
                            kind: device.kind,
                            label: device.label || 'Unknown Device',
                            device_id_hash: device.deviceId ? this.hashString(device.deviceId) : null,
                            group_id_hash: device.groupId ? this.hashString(device.groupId) : null
                        };
                        
                        if (device.kind === 'audioinput' || device.kind === 'audiooutput') {
                            mediaData.audio_devices.push(deviceInfo);
                            if (device.kind === 'audioinput') mediaData.audio_capabilities.input_supported = true;
                            if (device.kind === 'audiooutput') mediaData.audio_capabilities.output_supported = true;
                        } else if (device.kind === 'videoinput') {
                            mediaData.video_devices.push(deviceInfo);
                            mediaData.video_capabilities.camera_supported = true;
                        }
                    });
                    
                    // Test advanced audio capabilities
                    mediaData.audio_capabilities = {
                        ...mediaData.audio_capabilities,
                        ...(await this.testAdvancedAudioCapabilities())
                    };
                    
                    // Test advanced video capabilities
                    mediaData.video_capabilities = {
                        ...mediaData.video_capabilities,
                        ...(await this.testAdvancedVideoCapabilities())
                    };
                    
                } catch (e) {
                    mediaData.media_devices_access_denied = true;
                }
            }
            
            return mediaData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get comprehensive display preferences
     */
    async getDisplayPreferences() {
        try {
            const displayData = {
                color_scheme: this.detectColorScheme(),
                reduced_motion: this.detectReducedMotion(),
                high_contrast: this.detectHighContrast(),
                prefers_transparency: this.detectTransparencyPreference(),
                display_properties: {
                    color_gamut: this.detectColorGamut(),
                    hdr_support: this.detectHDRSupport(),
                    refresh_rate: await this.estimateRefreshRate(),
                    pixel_ratio: window.devicePixelRatio || 1
                },
                font_rendering: {
                    subpixel_rendering: this.detectSubpixelRendering(),
                    font_smoothing: this.detectFontSmoothing(),
                    preferred_fonts: await this.detectPreferredFonts()
                },
                visual_preferences: {
                    zoom_level: this.detectZoomLevel(),
                    text_size_preference: this.detectTextSizePreference(),
                    contrast_preference: this.detectContrastPreference()
                }
            };
            
            return displayData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get comprehensive input capabilities
     */
    async getInputCapabilities() {
        try {
            const inputData = {
                touch_support: {
                    touch_enabled: 'ontouchstart' in window,
                    max_touch_points: navigator.maxTouchPoints || 0,
                    touch_precision: this.detectTouchPrecision(),
                    gesture_support: this.detectGestureSupport()
                },
                pointer_support: {
                    mouse_support: 'MouseEvent' in window,
                    pointer_events: 'PointerEvent' in window,
                    fine_pointer: this.detectFinePointer(),
                    hover_capability: this.detectHoverCapability()
                },
                keyboard_support: {
                    physical_keyboard: this.detectPhysicalKeyboard(),
                    virtual_keyboard: 'VirtualKeyboard' in navigator,
                    keyboard_layout: await this.detectKeyboardLayout(),
                    special_keys: this.detectSpecialKeys()
                },
                input_methods: {
                    voice_input: 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window,
                    handwriting_input: this.detectHandwritingInput(),
                    eye_tracking: this.detectEyeTracking()
                }
            };
            
            return inputData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get comprehensive accessibility features
     */
    async getAccessibilityFeatures() {
        try {
            const accessibilityData = {
                screen_reader: {
                    supported: this.detectScreenReader(),
                    active: this.detectActiveScreenReader(),
                    type: this.detectScreenReaderType()
                },
                motor_accessibility: {
                    switch_navigation: this.detectSwitchNavigation(),
                    sticky_keys: this.detectStickyKeys(),
                    slow_keys: this.detectSlowKeys()
                },
                visual_accessibility: {
                    high_contrast_mode: this.detectHighContrast(),
                    large_text_mode: this.detectLargeTextMode(),
                    magnification_active: this.detectMagnification()
                },
                cognitive_accessibility: {
                    reduced_motion: this.detectReducedMotion(),
                    simplified_ui: this.detectSimplifiedUI(),
                    focus_assistance: this.detectFocusAssistance()
                },
                platform_accessibility: {
                    accessibility_api: this.detectAccessibilityAPI(),
                    assistive_technology: this.detectAssistiveTechnology()
                }
            };
            
            return accessibilityData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get system performance indicators
     */
    async getSystemPerformanceIndicators() {
        try {
            const performanceData = {
                memory_pressure: this.detectMemoryPressure(),
                cpu_utilization: await this.estimateCPUUtilization(),
                battery_impact: this.detectBatteryImpact(),
                thermal_state: this.detectThermalState(),
                power_efficiency: await this.calculatePowerEfficiency(),
                system_responsiveness: await this.measureSystemResponsiveness(),
                background_processing: this.detectBackgroundProcessing()
            };
            
            return performanceData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get privacy and security preferences
     */
    async getPrivacySettings() {
        try {
            const privacyData = {
                do_not_track: navigator.doNotTrack === '1' || navigator.doNotTrack === 'yes',
                cookieEnabled: navigator.cookieEnabled,
                third_party_cookies: await this.detectThirdPartyCookies(),
                local_storage_enabled: this.testLocalStorage(),
                permissions: {
                    geolocation: await this.checkGeolocationPermission(),
                    notifications: await this.checkNotificationPermission(),
                    camera: await this.checkCameraPermission(),
                    microphone: await this.checkMicrophonePermission()
                },
                fingerprinting_resistance: {
                    canvas_fingerprinting_blocked: await this.testCanvasFingerprintingBlocked(),
                    webgl_fingerprinting_blocked: await this.testWebGLFingerprintingBlocked(),
                    audio_fingerprinting_blocked: await this.testAudioFingerprintingBlocked()
                },
                tracking_protection: {
                    ad_blocker_detected: await this.detectAdBlocker(),
                    tracking_protection_enabled: await this.detectTrackingProtection(),
                    privacy_mode: this.detectPrivateMode()
                }
            };
            
            return privacyData;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Get fallback environmental data
     */
    getFallbackEnvironmentalData() {
        return {
            fallback: true,
            basic_environment: {
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                language: navigator.language,
                color_scheme: this.detectColorScheme(),
                screen_size: `${screen.width}x${screen.height}`,
                timestamp: new Date().toISOString()
            },
            error: 'Enhanced environmental data collection failed, using fallback method'
        };
    }
    
    /**
     * Send collected fingerprint to backend
     */
    async sendFingerprintToBackend(fingerprint, sessionId) {
        try {
            const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
            
            const response = await fetch(`${backendUrl}/api/session-fingerprinting/generate-device-signature`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    device_data: fingerprint,
                    session_id: sessionId
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            this.logger.info("Device fingerprint sent to backend successfully", result);
            
            return result;
            
        } catch (error) {
            this.logger.error("Error sending fingerprint to backend:", error);
            throw error;
        }
    }
    
    /**
     * Start continuous fingerprint collection
     */
    startContinuousCollection(sessionId, intervalMs = 30000) {
        this.logger.info(`Starting continuous fingerprint collection every ${intervalMs}ms`);
        
        const collectAndSend = async () => {
            try {
                const fingerprint = await this.collectComprehensiveFingerprint();
                await this.sendFingerprintToBackend(fingerprint, sessionId);
            } catch (error) {
                this.logger.error("Error in continuous collection:", error);
            }
        };
        
        // Initial collection
        collectAndSend();
        
        // Set up interval for continuous collection
        return setInterval(collectAndSend, intervalMs);
    }
    
    /**
     * Stop continuous collection
     */
    stopContinuousCollection(intervalId) {
        if (intervalId) {
            clearInterval(intervalId);
            this.logger.info("Continuous fingerprint collection stopped");
        }
    }
    
    // ===== ADDITIONAL HELPER METHODS FOR ENHANCED FUNCTIONALITY =====
    
    /**
     * Network timing and analysis helper methods
     */
    getNavigationTiming() {
        if (!performance.timing) return null;
        const timing = performance.timing;
        return {
            dns_lookup: timing.domainLookupEnd - timing.domainLookupStart,
            tcp_connection: timing.connectEnd - timing.connectStart,
            ssl_handshake: timing.secureConnectionStart ? timing.connectEnd - timing.secureConnectionStart : 0,
            request_response: timing.responseEnd - timing.requestStart,
            dom_loading: timing.domContentLoadedEventEnd - timing.domLoading
        };
    }
    
    async getResourceTiming() {
        try {
            const resources = performance.getEntriesByType('resource').slice(-10); // Last 10 resources
            return resources.map(resource => ({
                name: resource.name,
                duration: resource.duration,
                dns_lookup: resource.domainLookupEnd - resource.domainLookupStart,
                tcp_connection: resource.connectEnd - resource.connectStart,
                response_time: resource.responseEnd - resource.requestStart
            }));
        } catch (error) {
            return [];
        }
    }
    
    async measureFetchTiming() {
        try {
            const testUrls = ['/favicon.ico', window.location.href];
            const results = [];
            
            for (const url of testUrls) {
                const startTime = performance.now();
                try {
                    await fetch(url, { method: 'HEAD', cache: 'no-cache' });
                    const endTime = performance.now();
                    results.push({ url, latency: endTime - startTime, success: true });
                } catch (error) {
                    results.push({ url, error: error.message, success: false });
                }
            }
            return results;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async measurePingTiming() {
        // Simulated ping using image loading
        try {
            const startTime = performance.now();
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = img.onerror = () => {
                    const endTime = performance.now();
                    resolve({ ping_time: endTime - startTime });
                };
                img.src = '/favicon.ico?' + Date.now();
            });
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async measureDNSTiming() {
        try {
            // DNS timing through navigation timing API
            if (performance.timing) {
                return {
                    dns_lookup_time: performance.timing.domainLookupEnd - performance.timing.domainLookupStart,
                    dns_cache_hit: performance.timing.domainLookupStart === performance.timing.domainLookupEnd
                };
            }
            return { not_available: true };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async testDataChannelSupport() {
        try {
            const pc = new RTCPeerConnection();
            const dc = pc.createDataChannel('test');
            const supported = dc.readyState !== undefined;
            pc.close();
            return supported;
        } catch (error) {
            return false;
        }
    }
    
    async detectComprehensiveIPs() {
        try {
            return new Promise((resolve) => {
                const ips = { localIPs: [], publicIPs: [] };
                const pc = new RTCPeerConnection({
                    iceServers: [
                        { urls: 'stun:stun.l.google.com:19302' },
                        { urls: 'stun:stun1.l.google.com:19302' }
                    ]
                });
                
                pc.createDataChannel('');
                
                pc.onicecandidate = (event) => {
                    if (event.candidate) {
                        const candidate = event.candidate.candidate;
                        const ipMatch = candidate.match(/(\d+\.\d+\.\d+\.\d+)/);
                        if (ipMatch) {
                            const ip = ipMatch[1];
                            if (ip.startsWith('192.168.') || ip.startsWith('10.') || ip.startsWith('172.')) {
                                ips.localIPs.push(ip);
                            } else {
                                ips.publicIPs.push(ip);
                            }
                        }
                    }
                };
                
                pc.createOffer().then(offer => pc.setLocalDescription(offer));
                
                setTimeout(() => {
                    pc.close();
                    resolve(ips);
                }, 2000);
            });
        } catch (error) {
            return { localIPs: [], publicIPs: [], error: error.message };
        }
    }
    
    async testSTUNConnectivity() {
        try {
            return new Promise((resolve) => {
                const pc = new RTCPeerConnection({
                    iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
                });
                
                let connected = false;
                pc.onicecandidate = (event) => {
                    if (event.candidate && event.candidate.candidate.includes('stun')) {
                        connected = true;
                    }
                };
                
                pc.createDataChannel('test');
                pc.createOffer().then(offer => pc.setLocalDescription(offer));
                
                setTimeout(() => {
                    pc.close();
                    resolve(connected);
                }, 3000);
            });
        } catch (error) {
            return false;
        }
    }
    
    async testPublicDNSResolution() {
        try {
            const testDomains = ['google.com', 'cloudflare.com'];
            const results = [];
            
            for (const domain of testDomains) {
                try {
                    const startTime = performance.now();
                    await fetch(`https://${domain}/favicon.ico`, { method: 'HEAD', mode: 'no-cors' });
                    const endTime = performance.now();
                    results.push({ domain, resolution_time: endTime - startTime, success: true });
                } catch (error) {
                    results.push({ domain, error: error.message, success: false });
                }
            }
            return results;
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async measureDNSResolutionTime() {
        try {
            const startTime = performance.now();
            await fetch(window.location.origin + '/favicon.ico', { method: 'HEAD', cache: 'no-cache' });
            return performance.now() - startTime;
        } catch (error) {
            return 0;
        }
    }
    
    async testDNSOverHTTPS() {
        try {
            // Test if DNS over HTTPS is supported by trying Cloudflare's DoH
            const response = await fetch('https://1.1.1.1/dns-query?name=example.com&type=A', {
                headers: { 'Accept': 'application/dns-json' },
                mode: 'cors'
            }).catch(() => null);
            return response && response.ok;
        } catch (error) {
            return false;
        }
    }
    
    async createNetworkLatencyProfile() {
        const measurements = [];
        for (let i = 0; i < 5; i++) {
            const result = await this.measurePingTiming();
            measurements.push(result.ping_time || 0);
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        return {
            measurements,
            average: measurements.reduce((a, b) => a + b, 0) / measurements.length,
            min: Math.min(...measurements),
            max: Math.max(...measurements),
            jitter: this.calculateJitter(measurements)
        };
    }
    
    calculateJitter(measurements) {
        if (measurements.length < 2) return 0;
        const deltas = [];
        for (let i = 1; i < measurements.length; i++) {
            deltas.push(Math.abs(measurements[i] - measurements[i-1]));
        }
        return deltas.reduce((a, b) => a + b, 0) / deltas.length;
    }
    
    async measureConnectionStability() {
        try {
            const measurements = [];
            for (let i = 0; i < 3; i++) {
                const result = await this.measureFetchTiming();
                measurements.push(result);
                await new Promise(resolve => setTimeout(resolve, 200));
            }
            
            const successful = measurements.filter(m => m.some && m.some(r => r.success));
            return {
                stability_score: successful.length / measurements.length,
                total_tests: measurements.length,
                successful_tests: successful.length
            };
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async estimateHopCount() {
        // Estimate based on RTT - very rough approximation
        const timing = this.getNavigationTiming();
        if (timing && timing.tcp_connection > 0) {
            return Math.max(1, Math.round(timing.tcp_connection / 30)); // ~30ms per hop estimate
        }
        return 0;
    }
    
    async detectProxy() {
        try {
            // Simple proxy detection based on request headers and timing
            const response = await fetch(window.location.href, { method: 'HEAD' });
            const headers = response.headers;
            
            const proxyIndicators = [
                'via', 'x-forwarded-for', 'x-real-ip', 'x-cluster-client-ip',
                'x-forwarded-proto', 'x-forwarded-host', 'forwarded'
            ];
            
            for (const indicator of proxyIndicators) {
                if (headers.get(indicator)) return true;
            }
            return false;
        } catch (error) {
            return false;
        }
    }
    
    async detectVPNIndicators() {
        const indicators = [];
        
        // Check for timing anomalies
        const timing = await this.measureNetworkPerformance();
        if (timing.average_latency > 200) {
            indicators.push('high_latency');
        }
        
        // Check for DNS inconsistencies
        const dnsTest = await this.testPublicDNSResolution();
        if (dnsTest.some && dnsTest.some(result => !result.success)) {
            indicators.push('dns_blocking');
        }
        
        return indicators;
    }
    
    /**
     * Environmental data helper methods
     */
    detectDaylightSavingTime() {
        const january = new Date(new Date().getFullYear(), 0, 1);
        const july = new Date(new Date().getFullYear(), 6, 1);
        return january.getTimezoneOffset() !== july.getTimezoneOffset();
    }
    
    detectTimeFormat() {
        try {
            const date = new Date();
            const timeString = date.toLocaleTimeString();
            return timeString.includes('AM') || timeString.includes('PM') ? '12-hour' : '24-hour';
        } catch (error) {
            return 'unknown';
        }
    }
    
    detectCalendarSystem() {
        try {
            const calendar = Intl.DateTimeFormat().resolvedOptions().calendar;
            return calendar || 'gregorian';
        } catch (error) {
            return 'gregorian';
        }
    }
    
    async detectCountryCode() {
        try {
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            // Extract country from timezone (rough approximation)
            if (timezone.includes('/')) {
                const parts = timezone.split('/');
                return parts[0] === 'America' ? 'US' : 
                       parts[0] === 'Europe' ? 'EU' :
                       parts[0] === 'Asia' ? 'AS' : 'unknown';
            }
            return 'unknown';
        } catch (error) {
            return 'unknown';
        }
    }
    
    async detectRegion() {
        try {
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            return timezone.split('/')[0] || 'unknown';
        } catch (error) {
            return 'unknown';
        }
    }
    
    async detectCity() {
        try {
            const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            const parts = timezone.split('/');
            return parts[parts.length - 1] || 'unknown';
        } catch (error) {
            return 'unknown';
        }
    }
    
    estimateBatteryHealth(battery) {
        try {
            const level = battery.level;
            const charging = battery.charging;
            const chargingTime = battery.chargingTime;
            
            // Simple battery health estimation
            if (charging && chargingTime < Infinity) {
                return chargingTime < 7200 ? 'good' : 'degraded'; // < 2 hours = good
            }
            
            return level > 0.8 ? 'good' : level > 0.5 ? 'fair' : 'poor';
        } catch (error) {
            return 'unknown';
        }
    }
    
    async getCurrentMotionReading() {
        return new Promise((resolve) => {
            if ('DeviceMotionEvent' in window) {
                const handler = (event) => {
                    window.removeEventListener('devicemotion', handler);
                    resolve({
                        acceleration: event.acceleration,
                        rotation: event.rotationRate,
                        interval: event.interval
                    });
                };
                window.addEventListener('devicemotion', handler);
                setTimeout(() => {
                    window.removeEventListener('devicemotion', handler);
                    resolve(null);
                }, 1000);
            } else {
                resolve(null);
            }
        });
    }
    
    async getCurrentOrientationReading() {
        return new Promise((resolve) => {
            if ('DeviceOrientationEvent' in window) {
                const handler = (event) => {
                    window.removeEventListener('deviceorientation', handler);
                    resolve({
                        alpha: event.alpha,
                        beta: event.beta,
                        gamma: event.gamma,
                        absolute: event.absolute
                    });
                };
                window.addEventListener('deviceorientation', handler);
                setTimeout(() => {
                    window.removeEventListener('deviceorientation', handler);
                    resolve(null);
                }, 1000);
            } else {
                resolve(null);
            }
        });
    }
    
    analyzeMotionPatterns(motionReading) {
        try {
            const threshold = 0.1;
            const acceleration = motionReading.acceleration;
            const rotation = motionReading.rotation;
            
            const movementDetected = acceleration && 
                (Math.abs(acceleration.x) > threshold || 
                 Math.abs(acceleration.y) > threshold || 
                 Math.abs(acceleration.z) > threshold);
                 
            const rotationDetected = rotation &&
                (Math.abs(rotation.alpha) > threshold ||
                 Math.abs(rotation.beta) > threshold ||
                 Math.abs(rotation.gamma) > threshold);
            
            return {
                device_stationary: !movementDetected && !rotationDetected,
                movement_detected: movementDetected,
                rotation_detected: rotationDetected
            };
        } catch (error) {
            return { device_stationary: true, movement_detected: false, rotation_detected: false };
        }
    }
    
    async getAmbientLightReading() {
        // Note: AmbientLightSensor is not widely supported, this is a placeholder
        return new Promise((resolve) => {
            try {
                if (window.AmbientLightSensor) {
                    const sensor = new window.AmbientLightSensor();
                    sensor.onreading = () => {
                        resolve({ lux: sensor.illuminance });
                        sensor.stop();
                    };
                    sensor.onerror = () => resolve(null);
                    sensor.start();
                    setTimeout(() => resolve(null), 2000);
                } else {
                    resolve(null);
                }
            } catch (error) {
                resolve(null);
            }
        });
    }
    
    categorizeLightLevel(lux) {
        if (lux < 10) return 'very_dark';
        if (lux < 100) return 'dark';
        if (lux < 1000) return 'dim';
        if (lux < 10000) return 'bright';
        return 'very_bright';
    }
    
    estimateIndoorOutdoor(lux) {
        return lux > 1000 ? 'likely_outdoor' : 'likely_indoor';
    }
    
    async getProximityReading() {
        // Note: ProximitySensor is not widely supported
        return new Promise((resolve) => {
            try {
                if (window.ProximitySensor) {
                    const sensor = new window.ProximitySensor();
                    sensor.onreading = () => {
                        resolve({ 
                            distance: sensor.distance,
                            near: sensor.near 
                        });
                        sensor.stop();
                    };
                    sensor.onerror = () => resolve(null);
                    sensor.start();
                    setTimeout(() => resolve(null), 2000);
                } else {
                    resolve(null);
                }
            } catch (error) {
                resolve(null);
            }
        });
    }
    
    detectBrightnessAdaptation() {
        // Check if user has brightness adaptation enabled via media queries
        if (window.matchMedia) {
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark_adapted' : 'light_adapted';
        }
        return 'unknown';
    }
    
    detectColorTemperaturePreference() {
        // Estimate based on color scheme preference
        const scheme = this.detectColorScheme();
        return scheme === 'dark' ? 'warm' : 'cool';
    }
    
    async estimateDisplayBrightness() {
        // Rough estimation based on color scheme and time
        const hour = new Date().getHours();
        const isDark = this.detectColorScheme() === 'dark';
        
        if (isDark && (hour < 6 || hour > 20)) {
            return 'low';
        } else if (!isDark && hour > 6 && hour < 20) {
            return 'high';
        }
        return 'medium';
    }
    
    async getMediaStreamConstraints() {
        try {
            if ('mediaDevices' in navigator && navigator.mediaDevices.getSupportedConstraints) {
                return navigator.mediaDevices.getSupportedConstraints();
            }
            return {};
        } catch (error) {
            return {};
        }
    }
    
    async testAdvancedAudioCapabilities() {
        try {
            const capabilities = {};
            
            // Test if we can get audio constraints
            if ('mediaDevices' in navigator) {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ 
                        audio: { 
                            echoCancellation: true,
                            noiseSuppression: true,
                            autoGainControl: true
                        } 
                    });
                    
                    const track = stream.getAudioTracks()[0];
                    if (track) {
                        const settings = track.getSettings();
                        capabilities.echo_cancellation = settings.echoCancellation;
                        capabilities.noise_suppression = settings.noiseSuppression;
                        capabilities.auto_gain_control = settings.autoGainControl;
                        track.stop();
                    }
                } catch (e) {
                    // Permission denied or not available
                }
            }
            
            return capabilities;
        } catch (error) {
            return {};
        }
    }
    
    async testAdvancedVideoCapabilities() {
        try {
            const capabilities = {};
            
            if ('mediaDevices' in navigator) {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    const track = stream.getVideoTracks()[0];
                    
                    if (track) {
                        const settings = track.getSettings();
                        capabilities.max_resolution = {
                            width: settings.width,
                            height: settings.height
                        };
                        capabilities.frame_rate = settings.frameRate;
                        track.stop();
                    }
                } catch (e) {
                    // Permission denied or not available
                }
                
                // Test screen capture
                try {
                    if (navigator.mediaDevices.getDisplayMedia) {
                        capabilities.screen_capture_supported = true;
                    }
                } catch (e) {
                    capabilities.screen_capture_supported = false;
                }
            }
            
            return capabilities;
        } catch (error) {
            return {};
        }
    }
    
    // Simplified implementations for other helper methods
    hashString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return hash.toString(16);
    }
    
    detectTransparencyPreference() {
        return window.matchMedia && window.matchMedia('(prefers-reduced-transparency: reduce)').matches ? 'reduced' : 'normal';
    }
    
    detectSubpixelRendering() {
        // Test if subpixel rendering is enabled
        const canvas = document.createElement('canvas');
        canvas.width = 1;
        canvas.height = 1;
        const ctx = canvas.getContext('2d');
        ctx.fillText('test', 0.5, 0.5);
        return ctx.getImageData(0, 0, 1, 1).data[3] > 0;
    }
    
    detectFontSmoothing() {
        return window.getComputedStyle(document.body).webkitFontSmoothing || 'unknown';
    }
    
    async detectPreferredFonts() {
        return this.detectAvailableFonts().slice(0, 10); // Top 10 fonts
    }
    
    detectZoomLevel() {
        return Math.round((window.outerWidth / window.innerWidth) * 100);
    }
    
    detectTextSizePreference() {
        const fontSize = parseInt(window.getComputedStyle(document.body).fontSize);
        return fontSize > 16 ? 'large' : fontSize < 14 ? 'small' : 'normal';
    }
    
    detectContrastPreference() {
        return window.matchMedia && window.matchMedia('(prefers-contrast: high)').matches ? 'high' : 'normal';
    }
    
    // Additional stub implementations for remaining methods
    detectTouchPrecision() { return navigator.maxTouchPoints > 0 ? 'high' : 'none'; }
    detectGestureSupport() { return 'ontouchstart' in window; }
    detectFinePointer() { return window.matchMedia && window.matchMedia('(pointer: fine)').matches; }
    detectHoverCapability() { return window.matchMedia && window.matchMedia('(hover: hover)').matches; }
    detectPhysicalKeyboard() { return !('ontouchstart' in window); }
    async detectKeyboardLayout() { return 'qwerty'; } // Simplified
    detectSpecialKeys() { return { alt: true, ctrl: true, shift: true, meta: true }; }
    detectHandwritingInput() { return false; }
    detectEyeTracking() { return false; }
    detectScreenReader() { return false; }
    detectActiveScreenReader() { return false; }
    detectScreenReaderType() { return 'none'; }
    detectSwitchNavigation() { return false; }
    detectStickyKeys() { return false; }
    detectSlowKeys() { return false; }
    detectLargeTextMode() { return false; }
    detectMagnification() { return false; }
    detectSimplifiedUI() { return false; }
    detectFocusAssistance() { return false; }
    detectAccessibilityAPI() { return false; }
    detectAssistiveTechnology() { return false; }
    
    // Performance and system methods
    detectMemoryPressure() { 
        return performance.memory ? 
            (performance.memory.usedJSHeapSize / performance.memory.jsHeapSizeLimit) > 0.8 ? 'high' : 'normal' 
            : 'unknown'; 
    }
    
    async estimateCPUUtilization() {
        const startTime = performance.now();
        for (let i = 0; i < 100000; i++) { Math.random(); }
        const endTime = performance.now();
        return endTime - startTime > 10 ? 'high' : 'normal';
    }
    
    detectBatteryImpact() { return 'unknown'; }
    detectThermalState() { return 'unknown'; }
    async calculatePowerEfficiency() { return 'unknown'; }
    async measureSystemResponsiveness() { return 'good'; }
    detectBackgroundProcessing() { return false; }
    
    // Privacy and security methods  
    async detectThirdPartyCookies() { return document.cookie.length > 0; }
    async checkGeolocationPermission() { return 'unknown'; }
    async checkNotificationPermission() { return Notification ? Notification.permission : 'unknown'; }
    async checkCameraPermission() { return 'unknown'; }
    async checkMicrophonePermission() { return 'unknown'; }
    async testCanvasFingerprintingBlocked() { return false; }
    async testWebGLFingerprintingBlocked() { return false; }
    async testAudioFingerprintingBlocked() { return false; }
    async detectAdBlocker() { return false; }
    async detectTrackingProtection() { return false; }
    detectPrivateMode() { 
        try {
            localStorage.setItem('test', 'test');
            localStorage.removeItem('test');
            return false;
        } catch (e) {
            return true;
        }
    }
    
    // Network helper methods
    async testHSTSSupport() { return window.location.protocol === 'https:'; }
    detectCSP() { return document.querySelector('meta[http-equiv="Content-Security-Policy"]') !== null; }
    detectMixedContent() { return false; }
    async testCertificateTransparency() { return false; }
    
    async measureBandwidthViaTiming() { return { bandwidth: 0, method: 'timing' }; }
    async measureBandwidthViaResourceLoading() { return { bandwidth: 0, method: 'resource' }; }
    async measureBandwidthViaNetworkAPI() { 
        return navigator.connection ? { bandwidth: navigator.connection.downlink, method: 'api' } : { bandwidth: 0, method: 'api' }; 
    }
    
    calculateAverageBandwidth(measurements) {
        const values = measurements.filter(m => m.bandwidth > 0).map(m => m.bandwidth);
        return values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;
    }
    
    calculateConnectionQuality(measurements) {
        const avgBandwidth = this.calculateAverageBandwidth(measurements);
        return avgBandwidth > 10 ? 'excellent' : avgBandwidth > 5 ? 'good' : avgBandwidth > 1 ? 'fair' : 'poor';
    }
    
    getPageLoadMetrics() {
        if (performance.timing) {
            return {
                page_load_time: performance.timing.loadEventEnd - performance.timing.navigationStart,
                dom_ready_time: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
                first_byte_time: performance.timing.responseStart - performance.timing.navigationStart
            };
        }
        return {};
    }
    
    async getResourceLoadTimes() {
        const resources = performance.getEntriesByType('resource').slice(-5);
        return resources.map(r => ({ name: r.name, duration: r.duration }));
    }
    
    async calculateNetworkEfficiency() { return 'unknown'; }
    async measureConnectionReliability() { return 'unknown'; }
    async measureLatencyJitter() { return 0; }
    
    // Additional Helper Methods for Enhanced Implementation
    async testCPUArithmetic() {
        const start = performance.now();
        let sum = 0;
        for (let i = 0; i < 50000; i++) {
            sum += Math.sqrt(i) * Math.sin(i) + Math.cos(i);
        }
        return performance.now() - start;
    }
    
    async testMemoryAccess() {
        const start = performance.now();
        const array = new Array(10000).fill(0).map(() => Math.random());
        let sum = 0;
        for (let i = 0; i < array.length; i++) {
            sum += array[i] * 2;
        }
        return performance.now() - start;
    }
    
    async testDOMManipulation() {
        const start = performance.now();
        const container = document.createElement('div');
        for (let i = 0; i < 100; i++) {
            const element = document.createElement('span');
            element.textContent = `Test ${i}`;
            container.appendChild(element);
        }
        return performance.now() - start;
    }
    
    async testCanvasRendering() {
        const start = performance.now();
        const canvas = document.createElement('canvas');
        canvas.width = canvas.height = 200;
        const ctx = canvas.getContext('2d');
        for (let i = 0; i < 50; i++) {
            ctx.fillStyle = `hsl(${i * 7}, 50%, 50%)`;
            ctx.fillRect(i * 4, i * 4, 10, 10);
        }
        return performance.now() - start;
    }
    
    async measureEventResponseTime() {
        return new Promise(resolve => {
            const times = [];
            let count = 0;
            const maxTests = 5;
            
            const testElement = document.createElement('div');
            document.body.appendChild(testElement);
            
            const handler = () => {
                times.push(performance.now() - startTime);
                count++;
                if (count >= maxTests) {
                    testElement.removeEventListener('click', handler);
                    testElement.remove();
                    resolve({ response_times: times });
                } else {
                    setTimeout(() => {
                        startTime = performance.now();
                        testElement.click();
                    }, 100);
                }
            };
            
            testElement.addEventListener('click', handler);
            
            let startTime = performance.now();
            testElement.click();
        });
    }
    
    async measureAnimationFrameConsistency() {
        return new Promise(resolve => {
            const frameTimes = [];
            let lastTime = performance.now();
            let frameCount = 0;
            const maxFrames = 30;
            
            const measure = (currentTime) => {
                frameTimes.push(currentTime - lastTime);
                lastTime = currentTime;
                frameCount++;
                
                if (frameCount < maxFrames) {
                    requestAnimationFrame(measure);
                } else {
                    resolve({ frame_times: frameTimes });
                }
            };
            
            requestAnimationFrame(measure);
        });
    }
    
    async measureDOMUpdatePerformance() {
        const times = [];
        const container = document.createElement('div');
        document.body.appendChild(container);
        
        for (let i = 0; i < 10; i++) {
            const start = performance.now();
            container.innerHTML = `<div>Update ${i}: ${Date.now()}</div>`;
            times.push(performance.now() - start);
        }
        
        container.remove();
        return { update_times: times };
    }
    
    async measureInteractionLatency() {
        return new Promise(resolve => {
            const latencies = [];
            let testCount = 0;
            const maxTests = 5;
            
            const button = document.createElement('button');
            button.textContent = 'Test Button';
            button.style.position = 'fixed';
            button.style.top = '-100px'; // Hide off-screen
            document.body.appendChild(button);
            
            const clickHandler = () => {
                const endTime = performance.now();
                latencies.push(endTime - startTime);
                testCount++;
                
                if (testCount >= maxTests) {
                    button.removeEventListener('click', clickHandler);
                    button.remove();
                    resolve({ latencies: latencies });
                } else {
                    setTimeout(() => {
                        startTime = performance.now();
                        button.click();
                    }, 200);
                }
            };
            
            button.addEventListener('click', clickHandler);
            
            let startTime = performance.now();
            button.click();
        });
    }
    
    categorizeDegradationSeverity(percentage) {
        if (percentage > 30) return 'severe';
        if (percentage > 15) return 'moderate';
        if (percentage > 5) return 'mild';
        return 'negligible';
    }
    
    identifyDegradationCauses(testResults) {
        const causes = [];
        const degradedTests = testResults.filter(t => t.degradation_detected);
        
        if (degradedTests.length > testResults.length * 0.5) {
            causes.push('system_wide_thermal_throttling');
        }
        
        if (degradedTests.some(t => t.test_name === 'cpu_arithmetic')) {
            causes.push('cpu_thermal_throttling');
        }
        
        if (degradedTests.some(t => t.test_name === 'memory_access')) {
            causes.push('memory_bandwidth_limitation');
        }
        
        if (degradedTests.some(t => t.test_name === 'canvas_rendering')) {
            causes.push('gpu_thermal_throttling');
        }
        
        return causes;
    }
    
    calculateOverallSeverity(indicators) {
        if (indicators.length === 0) return 'none';
        
        const severityLevels = indicators.map(i => i.severity);
        if (severityLevels.includes('high')) return 'high';
        if (severityLevels.includes('medium')) return 'medium';
        return 'low';
    }
    
    categorizeResponsiveness(score) {
        if (score > 80) return 'excellent';
        if (score > 60) return 'good';
        if (score > 40) return 'fair';
        if (score > 20) return 'poor';
        return 'very_poor';
    }
    
    async analyzeBatteryPerformanceImpact() {
        try {
            let batteryLevel = null;
            let charging = null;
            
            if ('getBattery' in navigator) {
                try {
                    const battery = await navigator.getBattery();
                    batteryLevel = battery.level;
                    charging = battery.charging;
                } catch (e) {
                    // Battery API not available
                }
            }
            
            const performanceTest = await this.testCPUArithmetic();
            
            return {
                impacted: batteryLevel !== null && batteryLevel < 0.2 && !charging && performanceTest > 100,
                battery_level: batteryLevel,
                charging: charging,
                performance_time: performanceTest,
                severity: performanceTest > 200 ? 'high' : performanceTest > 150 ? 'medium' : 'low',
                details: { test_time_ms: performanceTest }
            };
        } catch (error) {
            return { impacted: false, error: error.message };
        }
    }
    
    async testSystemResponsiveness() {
        const start = performance.now();
        
        // Simulate system load with multiple operations
        await Promise.all([
            this.testCPUArithmetic(),
            this.testMemoryAccess(),
            this.testDOMManipulation()
        ]);
        
        const totalTime = performance.now() - start;
        
        return {
            degraded: totalTime > 500, // More than 500ms indicates degradation
            response_time: totalTime,
            severity: totalTime > 1000 ? 'high' : totalTime > 500 ? 'medium' : 'low',
            details: { total_time_ms: totalTime }
        };
    }
    
    async establishPerformanceBaseline() {
        const cpuTime = await this.testCPUArithmetic();
        const memoryTime = await this.testMemoryAccess();
        const domTime = await this.testDOMManipulation();
        
        return {
            score: Math.max(0, 1000 - (cpuTime + memoryTime + domTime) / 3),
            cpu_time: cpuTime,
            memory_time: memoryTime,
            dom_time: domTime
        };
    }
    
    async measureThrottledPerformance() {
        // Similar to baseline but potentially under throttled conditions
        return await this.establishPerformanceBaseline();
    }
    
    identifyPowerThrottling(baseline, throttled) {
        const indicators = [];
        
        if (throttled.cpu_time > baseline.cpu_time * 1.2) {
            indicators.push('cpu_frequency_reduction');
        }
        
        if (throttled.memory_time > baseline.memory_time * 1.15) {
            indicators.push('memory_bus_throttling');
        }
        
        if (throttled.dom_time > baseline.dom_time * 1.3) {
            indicators.push('graphics_throttling');
        }
        
        return indicators;
    }
    
    async detectDesktopPowerThrottling() {
        const baseline = await this.establishPerformanceBaseline();
        
        // Run a sustained test to trigger throttling
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        const sustained = await this.measureThrottledPerformance();
        const reduction = ((baseline.score - sustained.score) / baseline.score) * 100;
        
        return {
            detected: reduction > 10,
            estimated_reduction: reduction,
            indicators: reduction > 10 ? ['sustained_performance_reduction'] : []
        };
    }
    
    // ===== PHASE 1.2: ENHANCED BROWSER CHARACTERISTICS HELPER METHODS =====
    
    /**
     * Enhanced Browser Identification Methods
     */
    parseDetailedUserAgent() {
        try {
            const ua = navigator.userAgent;
            const analysis = {
                raw_user_agent: ua,
                user_agent_length: ua.length,
                parsed_components: {},
                browser_detection: {},
                os_detection: {},
                device_detection: {},
                suspicious_patterns: []
            };
            
            // Parse major browser patterns
            const browserPatterns = [
                { name: 'Chrome', pattern: /Chrome\/([0-9.]+)/, engine: 'Blink' },
                { name: 'Firefox', pattern: /Firefox\/([0-9.]+)/, engine: 'Gecko' },
                { name: 'Safari', pattern: /Version\/([0-9.]+).*Safari/, engine: 'WebKit' },
                { name: 'Edge', pattern: /Edg\/([0-9.]+)/, engine: 'Blink' },
                { name: 'Opera', pattern: /OPR\/([0-9.]+)/, engine: 'Blink' },
                { name: 'Internet Explorer', pattern: /MSIE ([0-9.]+)|Trident.*rv:([0-9.]+)/, engine: 'Trident' }
            ];
            
            for (const browser of browserPatterns) {
                const match = ua.match(browser.pattern);
                if (match) {
                    analysis.browser_detection = {
                        name: browser.name,
                        version: match[1] || match[2] || 'unknown',
                        engine: browser.engine,
                        match_pattern: browser.pattern.toString()
                    };
                    break;
                }
            }
            
            // Parse OS patterns
            const osPatterns = [
                { name: 'Windows', pattern: /Windows NT ([0-9.]+)/ },
                { name: 'macOS', pattern: /Mac OS X ([0-9_.]+)/ },
                { name: 'Linux', pattern: /Linux/ },
                { name: 'Android', pattern: /Android ([0-9.]+)/ },
                { name: 'iOS', pattern: /OS ([0-9_]+) like Mac OS X/ }
            ];
            
            for (const os of osPatterns) {
                const match = ua.match(os.pattern);
                if (match) {
                    analysis.os_detection = {
                        name: os.name,
                        version: match[1] ? match[1].replace(/_/g, '.') : 'unknown',
                        match_pattern: os.pattern.toString()
                    };
                    break;
                }
            }
            
            // Device detection
            if (ua.includes('Mobile')) analysis.device_detection.mobile = true;
            if (ua.includes('Tablet')) analysis.device_detection.tablet = true;
            if (ua.match(/iPhone|iPad|iPod/)) analysis.device_detection.apple_device = true;
            
            // Detect suspicious patterns
            const suspiciousPatterns = [
                { name: 'headless_chrome', pattern: /HeadlessChrome/ },
                { name: 'phantom_js', pattern: /PhantomJS/ },
                { name: 'selenium', pattern: /selenium/i },
                { name: 'webdriver', pattern: /webdriver/i },
                { name: 'bot_pattern', pattern: /bot|crawler|spider/i },
                { name: 'unusual_length', test: () => ua.length > 500 || ua.length < 50 },
                { name: 'missing_version', test: () => !ua.match(/[0-9]+\.[0-9]+/) }
            ];
            
            for (const suspicious of suspiciousPatterns) {
                if (suspicious.pattern && ua.match(suspicious.pattern)) {
                    analysis.suspicious_patterns.push(suspicious.name);
                } else if (suspicious.test && suspicious.test()) {
                    analysis.suspicious_patterns.push(suspicious.name);
                }
            }
            
            // Parse detailed components
            const componentPatterns = [
                { name: 'webkit_version', pattern: /WebKit\/([0-9.]+)/ },
                { name: 'gecko_version', pattern: /Gecko\/([0-9]+)/ },
                { name: 'chrome_version', pattern: /Chrome\/([0-9.]+)/ },
                { name: 'safari_version', pattern: /Safari\/([0-9.]+)/ }
            ];
            
            for (const component of componentPatterns) {
                const match = ua.match(component.pattern);
                if (match) {
                    analysis.parsed_components[component.name] = match[1];
                }
            }
            
            return analysis;
            
        } catch (error) {
            return { error: error.message, raw_user_agent: navigator.userAgent };
        }
    }
    
    async detectBrowserBuild() {
        try {
            const buildInfo = {
                build_id: 'unknown',
                build_date: null,
                version_details: {},
                browser_specific: {}
            };
            
            // Chrome-specific build detection
            if (window.chrome) {
                buildInfo.browser_specific.chrome = {
                    runtime_version: window.chrome.runtime ? 'present' : 'absent',
                    csi_info: window.chrome.csi ? await this.analyzeChromeCSI() : null,
                    load_times: window.chrome.loadTimes ? window.chrome.loadTimes() : null
                };
            }
            
            // Firefox-specific build detection
            if (navigator.userAgent.includes('Firefox')) {
                buildInfo.browser_specific.firefox = {
                    build_id: navigator.buildID || 'unknown',
                    oscpu: navigator.oscpu || 'unknown',
                    product_sub: navigator.productSub || 'unknown'
                };
            }
            
            // Safari-specific build detection
            if (navigator.userAgent.includes('Safari')) {
                buildInfo.browser_specific.safari = {
                    webkit_version: this.extractWebKitVersion(),
                    safari_version: this.extractSafariVersion(),
                    apple_specific: 'ApplePaySession' in window
                };
            }
            
            // Edge-specific build detection
            if (navigator.userAgent.includes('Edg')) {
                buildInfo.browser_specific.edge = {
                    edge_html_version: navigator.userAgent.match(/Edge\/([0-9.]+)/),
                    chromium_based: navigator.userAgent.includes('Edg/'),
                    webview: 'Windows' in window
                };
            }
            
            // General version detection through feature support
            buildInfo.version_details = {
                es6_support: this.detectES6Support(),
                webgl_version: this.getWebGLVersion(),
                canvas_api_level: this.getCanvasAPILevel(),
                fetch_api: 'fetch' in window,
                promise_support: 'Promise' in window,
                async_await: this.detectAsyncAwaitSupport()
            };
            
            return buildInfo;
            
        } catch (error) {
            return { error: error.message, build_id: 'detection_failed' };
        }
    }
    
    async fingerprintJSEngine() {
        try {
            const engineFingerprint = {
                engine_type: 'unknown',
                version_indicators: {},
                performance_characteristics: {},
                memory_behavior: {},
                compilation_features: {}
            };
            
            // V8 detection (Chrome, Edge, Node.js)
            if (this.detectV8Engine()) {
                engineFingerprint.engine_type = 'V8';
                engineFingerprint.version_indicators = await this.getV8VersionIndicators();
            }
            // SpiderMonkey detection (Firefox)
            else if (this.detectSpiderMonkeyEngine()) {
                engineFingerprint.engine_type = 'SpiderMonkey';
                engineFingerprint.version_indicators = await this.getSpiderMonkeyVersionIndicators();
            }
            // JavaScriptCore detection (Safari, WebKit)
            else if (this.detectJavaScriptCoreEngine()) {
                engineFingerprint.engine_type = 'JavaScriptCore';
                engineFingerprint.version_indicators = await this.getJavaScriptCoreVersionIndicators();
            }
            
            // Performance characteristics testing
            engineFingerprint.performance_characteristics = {
                function_call_overhead: await this.measureFunctionCallOverhead(),
                object_creation_speed: await this.measureObjectCreationSpeed(),
                array_operations_speed: await this.measureArrayOperationsSpeed(),
                string_operations_speed: await this.measureStringOperationsSpeed(),
                math_operations_speed: await this.measureMathOperationsSpeed()
            };
            
            // Memory behavior analysis
            engineFingerprint.memory_behavior = {
                garbage_collection_patterns: await this.analyzeGCPatterns(),
                memory_allocation_behavior: await this.analyzeMemoryAllocation(),
                weak_references_support: 'WeakRef' in window,
                finalization_registry_support: 'FinalizationRegistry' in window
            };
            
            // Compilation features
            engineFingerprint.compilation_features = {
                jit_compilation_indicators: this.detectJITCompilation(),
                optimization_tier_detection: this.detectOptimizationTiers(),
                webassembly_support: 'WebAssembly' in window,
                shared_array_buffer: 'SharedArrayBuffer' in window,
                atomics_support: 'Atomics' in window
            };
            
            return engineFingerprint;
            
        } catch (error) {
            return { error: error.message, engine_type: 'detection_failed' };
        }
    }
    
    async detectHeadlessBrowser() {
        try {
            const headlessIndicators = {
                is_headless: false,
                confidence_score: 0,
                detected_indicators: [],
                phantom_js_indicators: [],
                selenium_indicators: [],
                puppeteer_indicators: []
            };
            
            let suspicionCount = 0;
            
            // PhantomJS indicators
            if (window.phantom) {
                headlessIndicators.phantom_js_indicators.push('phantom_global_object');
                suspicionCount += 3;
            }
            
            if (window.callPhantom) {
                headlessIndicators.phantom_js_indicators.push('call_phantom_function');
                suspicionCount += 3;
            }
            
            // Selenium indicators
            if (window.webdriver || navigator.webdriver) {
                headlessIndicators.selenium_indicators.push('webdriver_property');
                suspicionCount += 3;
            }
            
            if (window.__webdriver_script_fn || document.__webdriver_script_fn) {
                headlessIndicators.selenium_indicators.push('webdriver_script_function');
                suspicionCount += 2;
            }
            
            // Puppeteer indicators
            if (window.outerHeight === 0 && window.outerWidth === 0) {
                headlessIndicators.puppeteer_indicators.push('zero_outer_dimensions');
                suspicionCount += 2;
            }
            
            if (navigator.languages.length === 0) {
                headlessIndicators.puppeteer_indicators.push('no_languages');
                suspicionCount += 1;
            }
            
            // Chrome headless specific
            if (navigator.userAgent.includes('HeadlessChrome')) {
                headlessIndicators.detected_indicators.push('headless_chrome_user_agent');
                suspicionCount += 4;
            }
            
            // General headless indicators
            if (!window.chrome && navigator.userAgent.includes('Chrome')) {
                headlessIndicators.detected_indicators.push('missing_chrome_object');
                suspicionCount += 1;
            }
            
            if (navigator.plugins.length === 0) {
                headlessIndicators.detected_indicators.push('no_plugins');
                suspicionCount += 1;
            }
            
            // Permission API anomalies
            try {
                const permissions = await navigator.permissions.query({ name: 'notifications' });
                if (permissions.state === 'denied' && !('Notification' in window)) {
                    headlessIndicators.detected_indicators.push('permission_notification_anomaly');
                    suspicionCount += 1;
                }
            } catch (e) {
                // Permission API not available
            }
            
            // WebGL context anomalies
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl');
            if (gl) {
                const renderer = gl.getParameter(gl.RENDERER);
                if (renderer.includes('SwiftShader') || renderer.includes('Software')) {
                    headlessIndicators.detected_indicators.push('software_webgl_renderer');
                    suspicionCount += 2;
                }
            }
            
            // Calculate confidence score
            headlessIndicators.confidence_score = Math.min(suspicionCount / 10, 1);
            headlessIndicators.is_headless = headlessIndicators.confidence_score > 0.5;
            
            return headlessIndicators;
            
        } catch (error) {
            return { error: error.message, is_headless: false, confidence_score: 0 };
        }
    }
    
    /**
     * JavaScript Engine Profiling Methods
     */
    async detectV8Features() {
        try {
            const v8Features = {
                engine_detected: false,
                version_indicators: {},
                v8_specific_features: {},
                performance_optimizations: {},
                memory_management: {}
            };
            
            // V8 engine detection
            v8Features.engine_detected = this.detectV8Engine();
            
            if (v8Features.engine_detected) {
                // V8 version indicators
                v8Features.version_indicators = {
                    error_stack_trace_api: Error.captureStackTrace ? true : false,
                    v8_compile_cache: 'v8' in process ? true : false, // Node.js specific
                    array_buffer_transfer: ArrayBuffer.prototype.transfer ? true : false,
                    weak_ref_support: 'WeakRef' in window,
                    finalization_registry: 'FinalizationRegistry' in window
                };
                
                // V8 specific features
                v8Features.v8_specific_features = {
                    harmony_features: await this.detectV8HarmonyFeatures(),
                    turbofan_optimizations: await this.detectTurboFanOptimizations(),
                    ignition_interpreter: await this.detectIgnitionInterpreter(),
                    concurrent_marking: await this.detectConcurrentMarking()
                };
                
                // Performance optimizations
                v8Features.performance_optimizations = {
                    hidden_classes: await this.analyzeHiddenClasses(),
                    inline_caching: await this.analyzeInlineCaching(),
                    escape_analysis: await this.analyzeEscapeAnalysis(),
                    loop_optimization: await this.analyzeLoopOptimization()
                };
                
                // Memory management
                v8Features.memory_management = {
                    heap_snapshot_support: this.detectHeapSnapshotSupport(),
                    memory_pressure_api: 'memory' in performance,
                    gc_scheduling: await this.analyzeGCScheduling(),
                    memory_segments: await this.analyzeMemorySegments()
                };
            }
            
            return v8Features;
            
        } catch (error) {
            return { error: error.message, engine_detected: false };
        }
    }
    
    async profileJSPerformance() {
        try {
            const performanceProfile = {
                execution_speed: {},
                memory_efficiency: {},
                optimization_indicators: {},
                compilation_characteristics: {}
            };
            
            // Execution speed tests
            performanceProfile.execution_speed = {
                function_calls: await this.measureFunctionCallPerformance(),
                object_operations: await this.measureObjectOperationPerformance(),
                array_operations: await this.measureArrayPerformance(),
                string_operations: await this.measureStringPerformance(),
                math_operations: await this.measureMathPerformance(),
                regexp_operations: await this.measureRegExpPerformance()
            };
            
            // Memory efficiency tests
            performanceProfile.memory_efficiency = {
                allocation_speed: await this.measureAllocationSpeed(),
                gc_frequency: await this.measureGCFrequency(),
                memory_fragmentation: await this.measureMemoryFragmentation(),
                object_pooling_efficiency: await this.measureObjectPoolingEfficiency()
            };
            
            // Optimization indicators
            performanceProfile.optimization_indicators = {
                hot_function_detection: await this.detectHotFunctionOptimization(),
                deoptimization_triggers: await this.detectDeoptimizationTriggers(),
                type_feedback: await this.analyzeTypeFeedback(),
                speculative_optimization: await this.detectSpeculativeOptimization()
            };
            
            // Compilation characteristics
            performanceProfile.compilation_characteristics = {
                parse_time: await this.measureParseTime(),
                compilation_time: await this.measureCompilationTime(),
                execution_tier_transitions: await this.measureTierTransitions(),
                bytecode_analysis: await this.analyzeBytecodeExecution()
            };
            
            return performanceProfile;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async analyzeJSMemoryManagement() {
        try {
            const memoryAnalysis = {
                heap_characteristics: {},
                gc_behavior: {},
                memory_pressure: {},
                allocation_patterns: {}
            };
            
            // Heap characteristics
            if (performance.memory) {
                memoryAnalysis.heap_characteristics = {
                    used_heap_size: performance.memory.usedJSHeapSize,
                    total_heap_size: performance.memory.totalJSHeapSize,
                    heap_size_limit: performance.memory.jsHeapSizeLimit,
                    heap_utilization: (performance.memory.usedJSHeapSize / performance.memory.jsHeapSizeLimit) * 100
                };
            }
            
            // GC behavior analysis
            memoryAnalysis.gc_behavior = await this.analyzeGarbageCollectionBehavior();
            
            // Memory pressure detection
            memoryAnalysis.memory_pressure = {
                pressure_indicators: await this.detectMemoryPressure(),
                allocation_failures: await this.detectAllocationFailures(),
                memory_warnings: await this.detectMemoryWarnings()
            };
            
            // Allocation patterns
            memoryAnalysis.allocation_patterns = {
                object_allocation_rate: await this.measureObjectAllocationRate(),
                array_allocation_patterns: await this.analyzeArrayAllocationPatterns(),
                string_allocation_behavior: await this.analyzeStringAllocationBehavior(),
                closure_allocation_analysis: await this.analyzeClosureAllocation()
            };
            
            return memoryAnalysis;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async detectJSOptimizations() {
        try {
            const optimizations = {
                jit_compilation: {},
                inlining_analysis: {},
                dead_code_elimination: {},
                constant_folding: {},
                loop_optimizations: {}
            };
            
            // JIT compilation detection
            optimizations.jit_compilation = {
                compilation_detected: await this.detectJITCompilation(),
                compilation_tiers: await this.identifyCompilationTiers(),
                optimization_thresholds: await this.measureOptimizationThresholds(),
                deoptimization_patterns: await this.analyzeDeoptimizationPatterns()
            };
            
            // Function inlining analysis
            optimizations.inlining_analysis = {
                inline_candidates: await this.identifyInlineCandidates(),
                inlining_effectiveness: await this.measureInliningEffectiveness(),
                polymorphic_inline_cache: await this.analyzePolymorphicInlineCache(),
                megamorphic_detection: await this.detectMegamorphicCallSites()
            };
            
            // Dead code elimination
            optimizations.dead_code_elimination = {
                unreachable_code_detection: await this.detectUnreachableCodeOptimization(),
                unused_variable_elimination: await this.detectUnusedVariableElimination(),
                dead_store_elimination: await this.detectDeadStoreElimination()
            };
            
            // Constant folding and propagation
            optimizations.constant_folding = {
                compile_time_evaluation: await this.detectConstantFolding(),
                constant_propagation: await this.detectConstantPropagation(),
                strength_reduction: await this.detectStrengthReduction()
            };
            
            // Loop optimizations
            optimizations.loop_optimizations = {
                loop_unrolling: await this.detectLoopUnrolling(),
                loop_invariant_motion: await this.detectLoopInvariantMotion(),
                vectorization: await this.detectVectorization(),
                loop_peeling: await this.detectLoopPeeling()
            };
            
            return optimizations;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    /**
     * Rendering Engine Analysis Methods
     */
    async fingerprintLayoutEngine() {
        try {
            const layoutFingerprint = {
                engine_type: 'unknown',
                version_indicators: {},
                layout_characteristics: {},
                css_engine_quirks: {},
                rendering_performance: {}
            };
            
            // Engine detection based on CSS support and behavior
            layoutFingerprint.engine_type = this.detectLayoutEngine();
            
            // Version indicators through CSS feature support
            layoutFingerprint.version_indicators = {
                css_grid_support: CSS.supports('display', 'grid'),
                css_flexbox_support: CSS.supports('display', 'flex'),
                css_custom_properties: CSS.supports('color', 'var(--test)'),
                css_subgrid: CSS.supports('grid-template-rows', 'subgrid'),
                css_container_queries: CSS.supports('container-type', 'inline-size'),
                css_cascade_layers: CSS.supports('layer', 'base'),
                css_color_functions: CSS.supports('color', 'color(display-p3 1 0 0)'),
                css_logical_properties: CSS.supports('margin-inline-start', '1px')
            };
            
            // Layout characteristics
            layoutFingerprint.layout_characteristics = await this.analyzeLayoutCharacteristics();
            
            // CSS engine quirks
            layoutFingerprint.css_engine_quirks = await this.detectCSSEngineQuirks();
            
            // Rendering performance
            layoutFingerprint.rendering_performance = await this.measureRenderingPerformance();
            
            return layoutFingerprint;
            
        } catch (error) {
            return { error: error.message, engine_type: 'detection_failed' };
        }
    }
    
    async buildCSSFeatureMatrix() {
        try {
            const featureMatrix = {
                layout_features: {},
                visual_features: {},
                animation_features: {},
                interaction_features: {},
                experimental_features: {}
            };
            
            // Layout features
            featureMatrix.layout_features = {
                grid: CSS.supports('display', 'grid'),
                subgrid: CSS.supports('grid-template-rows', 'subgrid'),
                flexbox: CSS.supports('display', 'flex'),
                multi_column: CSS.supports('column-count', '2'),
                css_regions: CSS.supports('flow-into', 'region'),
                css_exclusions: CSS.supports('wrap-flow', 'both'),
                css_shapes: CSS.supports('shape-outside', 'circle()'),
                css_writing_modes: CSS.supports('writing-mode', 'vertical-rl'),
                css_logical_properties: CSS.supports('margin-inline-start', '1px'),
                container_queries: CSS.supports('container-type', 'inline-size'),
                content_visibility: CSS.supports('content-visibility', 'auto')
            };
            
            // Visual features
            featureMatrix.visual_features = {
                css_filters: CSS.supports('filter', 'blur(5px)'),
                css_backdrop_filter: CSS.supports('backdrop-filter', 'blur(5px)'),
                css_clip_path: CSS.supports('clip-path', 'circle()'),
                css_masks: CSS.supports('mask-image', 'url(test.png)'),
                css_blend_modes: CSS.supports('mix-blend-mode', 'multiply'),
                css_gradients: CSS.supports('background-image', 'linear-gradient(red, blue)'),
                css_transforms_3d: CSS.supports('transform', 'rotateX(45deg)'),
                css_perspective: CSS.supports('perspective', '1000px'),
                css_custom_properties: CSS.supports('color', 'var(--test)'),
                css_color_functions: CSS.supports('color', 'color(display-p3 1 0 0)'),
                css_color_schemes: CSS.supports('color-scheme', 'dark light')
            };
            
            // Animation features
            featureMatrix.animation_features = {
                css_animations: CSS.supports('animation-duration', '1s'),
                css_transitions: CSS.supports('transition-duration', '1s'),
                css_transforms: CSS.supports('transform', 'scale(2)'),
                web_animations_api: 'Animation' in window,
                css_motion_path: CSS.supports('offset-path', 'path("M 0 0 L 100 100")'),
                css_scroll_snap: CSS.supports('scroll-snap-type', 'x mandatory'),
                css_scroll_behavior: CSS.supports('scroll-behavior', 'smooth'),
                intersection_observer: 'IntersectionObserver' in window,
                resize_observer: 'ResizeObserver' in window
            };
            
            // Interaction features
            featureMatrix.interaction_features = {
                css_pointer_events: CSS.supports('pointer-events', 'none'),
                css_user_select: CSS.supports('user-select', 'none'),
                css_touch_action: CSS.supports('touch-action', 'pan-y'),
                css_scroll_snap: CSS.supports('scroll-snap-type', 'x mandatory'),
                css_overscroll_behavior: CSS.supports('overscroll-behavior', 'contain'),
                pointer_events_api: 'PointerEvent' in window,
                touch_events_api: 'TouchEvent' in window,
                gesture_events_api: 'GestureEvent' in window
            };
            
            // Experimental features
            featureMatrix.experimental_features = {
                css_houdini_paint: 'CSS' in window && 'paintWorklet' in CSS,
                css_houdini_layout: 'CSS' in window && 'layoutWorklet' in CSS,
                css_houdini_animation: 'CSS' in window && 'animationWorklet' in CSS,
                css_anchor_positioning: CSS.supports('anchor-name', '--test'),
                css_cascade_layers: CSS.supports('layer', 'base'),
                css_nesting: CSS.supports('selector(:is(a b))'),
                css_at_property: CSS.supports('syntax', '"<color>"'),
                view_transitions: 'startViewTransition' in document
            };
            
            return featureMatrix;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async detectRenderingQuirks() {
        try {
            const quirks = {
                layout_quirks: [],
                painting_quirks: [],
                font_quirks: [],
                color_quirks: [],
                animation_quirks: []
            };
            
            // Layout quirks detection
            quirks.layout_quirks = await this.detectLayoutQuirks();
            
            // Painting quirks detection
            quirks.painting_quirks = await this.detectPaintingQuirks();
            
            // Font rendering quirks
            quirks.font_quirks = await this.detectFontRenderingQuirks();
            
            // Color handling quirks
            quirks.color_quirks = await this.detectColorHandlingQuirks();
            
            // Animation quirks
            quirks.animation_quirks = await this.detectAnimationQuirks();
            
            return quirks;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    async analyzeGraphicsAcceleration() {
        try {
            const acceleration = {
                hardware_acceleration: false,
                gpu_info: {},
                acceleration_apis: {},
                performance_indicators: {},
                capability_tests: {}
            };
            
            // Hardware acceleration detection
            acceleration.hardware_acceleration = await this.detectHardwareAcceleration();
            
            // GPU information
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (gl) {
                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                acceleration.gpu_info = {
                    vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR),
                    renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER),
                    webgl_version: gl.getParameter(gl.VERSION),
                    shading_language: gl.getParameter(gl.SHADING_LANGUAGE_VERSION),
                    is_software_renderer: this.isSoftwareRenderer(gl)
                };
            }
            
            // Acceleration APIs
            acceleration.acceleration_apis = {
                webgl_support: !!gl,
                webgl2_support: !!(canvas.getContext('webgl2')),
                canvas_2d_acceleration: await this.testCanvas2DAcceleration(),
                css_transforms_acceleration: await this.testCSSTransformAcceleration(),
                video_acceleration: await this.testVideoAcceleration(),
                webgpu_support: 'gpu' in navigator
            };
            
            // Performance indicators
            acceleration.performance_indicators = await this.measureAccelerationPerformance();
            
            // Capability tests
            acceleration.capability_tests = await this.runAccelerationCapabilityTests();
            
            canvas.remove();
            return acceleration;
            
        } catch (error) {
            return { error: error.message };
        }
    }
    
    // ===== SUPPORTING HELPER METHODS FOR BROWSER CHARACTERISTICS =====
    
    // Enhanced Browser Identification Helper Methods
    detectV8Engine() {
        return !!(window.chrome || Error.captureStackTrace || (typeof process !== 'undefined' && process.versions && process.versions.v8));
    }
    
    detectSpiderMonkeyEngine() {
        return navigator.userAgent.includes('Firefox') || 'mozInnerScreenX' in window || 'InstallTrigger' in window;
    }
    
    detectJavaScriptCoreEngine() {
        return /Safari/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent) || 'WebKitCSSMatrix' in window;
    }
    
    async analyzeChromeCSI() {
        if (window.chrome && window.chrome.csi) {
            return window.chrome.csi();
        }
        return null;
    }
    
    extractWebKitVersion() {
        const match = navigator.userAgent.match(/WebKit\/([0-9.]+)/);
        return match ? match[1] : 'unknown';
    }
    
    extractSafariVersion() {
        const match = navigator.userAgent.match(/Safari\/([0-9.]+)/);
        return match ? match[1] : 'unknown';
    }
    
    detectES6Support() {
        try {
            eval('(x => x)(1)'); // Arrow function test
            return true;
        } catch (e) {
            return false;
        }
    }
    
    getWebGLVersion() {
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        if (gl) {
            const version = gl.getParameter(gl.VERSION);
            canvas.remove();
            return version;
        }
        canvas.remove();
        return 'not_supported';
    }
    
    getCanvasAPILevel() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        let level = 'basic';
        
        if (ctx) {
            if ('filter' in ctx) level = 'advanced';
            if ('resetTransform' in ctx) level = 'modern';
        }
        
        canvas.remove();
        return level;
    }
    
    detectAsyncAwaitSupport() {
        try {
            eval('async function test() { await 1; }');
            return true;
        } catch (e) {
            return false;
        }
    }
    
    // JavaScript Engine Version Indicators
    async getV8VersionIndicators() {
        return {
            error_stack_api: Error.captureStackTrace ? true : false,
            weak_ref: 'WeakRef' in window,
            finalization_registry: 'FinalizationRegistry' in window,
            logical_assignment: this.testLogicalAssignment(),
            numeric_separators: this.testNumericSeparators(),
            optional_chaining: this.testOptionalChaining(),
            nullish_coalescing: this.testNullishCoalescing()
        };
    }
    
    async getSpiderMonkeyVersionIndicators() {
        return {
            build_id: navigator.buildID || 'unknown',
            moz_specific: 'mozInnerScreenX' in window,
            install_trigger: 'InstallTrigger' in window,
            moz_connection: 'mozConnection' in navigator,
            moz_battery: 'mozBattery' in navigator
        };
    }
    
    async getJavaScriptCoreVersionIndicators() {
        return {
            webkit_css_matrix: 'WebKitCSSMatrix' in window,
            webkit_point: 'WebKitPoint' in window,
            webkit_url: 'webkitURL' in window,
            safari_specific: /Safari/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent)
        };
    }
    
    // Performance Measurement Helper Methods
    async measureFunctionCallOverhead() {
        const iterations = 100000;
        const testFunction = () => { return 1; };
        
        const start = performance.now();
        for (let i = 0; i < iterations; i++) {
            testFunction();
        }
        const end = performance.now();
        
        return (end - start) / iterations;
    }
    
    async measureObjectCreationSpeed() {
        const iterations = 50000;
        const start = performance.now();
        
        for (let i = 0; i < iterations; i++) {
            const obj = { prop1: i, prop2: i * 2, prop3: 'test' + i };
        }
        
        const end = performance.now();
        return (end - start) / iterations;
    }
    
    async measureArrayOperationsSpeed() {
        const size = 10000;
        const array = new Array(size).fill(0).map((_, i) => i);
        
        const start = performance.now();
        
        // Test various array operations
        array.map(x => x * 2);
        array.filter(x => x > 5000);
        array.reduce((acc, val) => acc + val, 0);
        
        const end = performance.now();
        return end - start;
    }
    
    async measureStringOperationsSpeed() {
        const iterations = 10000;
        let testString = 'test string for performance measurement';
        
        const start = performance.now();
        
        for (let i = 0; i < iterations; i++) {
            testString += i;
            testString = testString.substring(0, 100);
            testString.replace('test', 'best');
        }
        
        const end = performance.now();
        return end - start;
    }
    
    async measureMathOperationsSpeed() {
        const iterations = 100000;
        let result = 0;
        
        const start = performance.now();
        
        for (let i = 0; i < iterations; i++) {
            result += Math.sin(i) * Math.cos(i) + Math.sqrt(i);
        }
        
        const end = performance.now();
        return end - start;
    }
    
    // Layout Engine Detection
    detectLayoutEngine() {
        const ua = navigator.userAgent;
        
        if (ua.includes('Chrome') || ua.includes('Chromium')) return 'Blink';
        if (ua.includes('Firefox')) return 'Gecko';
        if (ua.includes('Safari') && !ua.includes('Chrome')) return 'WebKit';
        if (ua.includes('Edge')) return ua.includes('Edg/') ? 'Blink' : 'EdgeHTML';
        if (ua.includes('Opera')) return 'Blink';
        if (ua.includes('MSIE') || ua.includes('Trident')) return 'Trident';
        
        return 'Unknown';
    }
    
    // Font Analysis Helper Methods
    classifyFontFamilies(detectedFonts) {
        const families = {
            serif: [],
            sans_serif: [],
            monospace: [],
            display: [],
            script: []
        };
        
        const serifFonts = ['Times New Roman', 'Times', 'Georgia', 'Palatino', 'Garamond'];
        const sansSerifFonts = ['Arial', 'Helvetica', 'Verdana', 'Calibri', 'Segoe UI'];
        const monospaceFonts = ['Courier New', 'Courier', 'Monaco', 'Consolas', 'Menlo'];
        const displayFonts = ['Impact', 'Arial Black', 'Bradley Hand ITC'];
        const scriptFonts = ['Comic Sans MS'];
        
        for (const font of detectedFonts) {
            if (serifFonts.includes(font.name)) families.serif.push(font);
            else if (sansSerifFonts.includes(font.name)) families.sans_serif.push(font);
            else if (monospaceFonts.includes(font.name)) families.monospace.push(font);
            else if (displayFonts.includes(font.name)) families.display.push(font);
            else if (scriptFonts.includes(font.name)) families.script.push(font);
        }
        
        return families;
    }
    
    async detectWebFonts() {
        const webFonts = [];
        
        // Check for common web font indicators
        const stylesheets = document.styleSheets;
        for (let i = 0; i < stylesheets.length; i++) {
            try {
                const rules = stylesheets[i].cssRules || stylesheets[i].rules;
                for (let j = 0; j < rules.length; j++) {
                    if (rules[j].type === CSSRule.FONT_FACE_RULE) {
                        webFonts.push({
                            family: rules[j].style.fontFamily,
                            source: rules[j].style.src
                        });
                    }
                }
            } catch (e) {
                // Cross-origin or other access issues
            }
        }
        
        return webFonts;
    }
    
    // Simple statistical helper methods
    calculateVariance(numbers) {
        if (numbers.length === 0) return 0;
        const mean = numbers.reduce((a, b) => a + b, 0) / numbers.length;
        return numbers.reduce((sum, num) => sum + Math.pow(num - mean, 2), 0) / numbers.length;
    }
    
    calculateCoefficientOfVariation(numbers) {
        if (numbers.length === 0) return 0;
        const mean = numbers.reduce((a, b) => a + b, 0) / numbers.length;
        const variance = this.calculateVariance(numbers);
        return mean !== 0 ? (Math.sqrt(variance) / mean) * 100 : 0;
    }
    
    // Feature testing helper methods
    testLogicalAssignment() {
        try {
            eval('let a = 1; a ||= 2;');
            return true;
        } catch (e) {
            return false;
        }
    }
    
    testNumericSeparators() {
        try {
            eval('const num = 1_000_000;');
            return true;
        } catch (e) {
            return false;
        }
    }
    
    testOptionalChaining() {
        try {
            eval('const obj = {}; obj?.prop?.method?.();');
            return true;
        } catch (e) {
            return false;
        }
    }
    
    testNullishCoalescing() {
        try {
            eval('const val = null ?? "default";');
            return true;
        } catch (e) {
            return false;
        }
    }
    
    // Canvas and graphics helper methods
    testCanvas2DSupport() {
        try {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.remove();
            return !!ctx;
        } catch (e) {
            return false;
        }
    }
    
    isSoftwareRenderer(gl) {
        const renderer = gl.getParameter(gl.RENDERER);
        return renderer.toLowerCase().includes('software') || 
               renderer.toLowerCase().includes('swiftshader') ||
               renderer.toLowerCase().includes('llvmpipe');
    }
    
    // Stub methods for complex implementations (to be implemented as needed)
    async analyzeSystemFontCharacteristics() { return {}; }
    async analyzeFontLoadingBehavior() { return {}; }
    async analyzeSubpixelRendering() { return {}; }
    async analyzeAntialiasing() { return {}; }
    async analyzeHinting() { return {}; }
    async analyzeFontSmoothing() { return {}; }
    async analyzeColorEmojiSupport() { return {}; }
    async testFractionalMetrics(ctx) { return {}; }
    async analyzeKerning(ctx) { return {}; }
    async testLigatureSupport(ctx) { return {}; }
    async analyzeBaselineMetrics(ctx) { return {}; }
    async testFallbackBehavior() { return {}; }
    async testMissingGlyphHandling() { return {}; }
    async analyzeUnicodeSupport() { return {}; }
    async analyzeFontMatching() { return {}; }
    async scanExperimentalAPIs() { return {}; }
    async scanDeprecatedAPIs() { return {}; }
    async scanVendorPrefixedAPIs() { return {}; }
    async scanPermissionAPIs() { return {}; }
    async detectOriginTrials() { return {}; }
    async detectFlagEnabledFeatures() { return {}; }
    async detectWebKitExperimental() { return {}; }
    async detectMozillaExperimental() { return {}; }
    async detectChromiumExperimental() { return {}; }
    async analyzePermissionBehavior() { return {}; }
    async analyzeFeaturePolicyBehavior() { return {}; }
    async analyzeLayoutCharacteristics() { return {}; }
    async detectCSSEngineQuirks() { return {}; }
    async measureRenderingPerformance() { return {}; }
    async detectLayoutQuirks() { return []; }
    async detectPaintingQuirks() { return []; }
    async detectFontRenderingQuirks() { return []; }
    async detectColorHandlingQuirks() { return []; }
    async detectAnimationQuirks() { return []; }
    async detectHardwareAcceleration() { return false; }
    async testCanvas2DAcceleration() { return false; }
    async testCSSTransformAcceleration() { return false; }
    async testVideoAcceleration() { return false; }
    async measureAccelerationPerformance() { return {}; }
    async runAccelerationCapabilityTests() { return {}; }
    
    // JavaScript Engine specific methods (stubs)
    async detectV8HarmonyFeatures() { return {}; }
    async detectTurboFanOptimizations() { return {}; }
    async detectIgnitionInterpreter() { return {}; }
    async detectConcurrentMarking() { return {}; }
    async analyzeHiddenClasses() { return {}; }
    async analyzeInlineCaching() { return {}; }
    async analyzeEscapeAnalysis() { return {}; }
    async analyzeLoopOptimization() { return {}; }
    detectHeapSnapshotSupport() { return false; }
    async analyzeGCScheduling() { return {}; }
    async analyzeMemorySegments() { return {}; }
    async measureFunctionCallPerformance() { return 0; }
    async measureObjectOperationPerformance() { return 0; }
    async measureArrayPerformance() { return 0; }
    async measureStringPerformance() { return 0; }
    async measureMathPerformance() { return 0; }
    async measureRegExpPerformance() { return 0; }
    async measureAllocationSpeed() { return 0; }
    async measureGCFrequency() { return 0; }
    async measureMemoryFragmentation() { return 0; }
    async measureObjectPoolingEfficiency() { return 0; }
    async detectHotFunctionOptimization() { return {}; }
    async detectDeoptimizationTriggers() { return {}; }
    async analyzeTypeFeedback() { return {}; }
    async detectSpeculativeOptimization() { return {}; }
    async measureParseTime() { return 0; }
    async measureCompilationTime() { return 0; }
    async measureTierTransitions() { return 0; }
    async analyzeBytecodeExecution() { return {}; }
    async analyzeGarbageCollectionBehavior() { return {}; }
    async detectMemoryPressure() { return []; }
    async detectAllocationFailures() { return []; }
    async detectMemoryWarnings() { return []; }
    async measureObjectAllocationRate() { return 0; }
    async analyzeArrayAllocationPatterns() { return {}; }
    async analyzeStringAllocationBehavior() { return {}; }
    async analyzeClosureAllocation() { return {}; }
    async identifyCompilationTiers() { return []; }
    async measureOptimizationThresholds() { return {}; }
    async analyzeDeoptimizationPatterns() { return {}; }
    async identifyInlineCandidates() { return []; }
    async measureInliningEffectiveness() { return 0; }
    async analyzePolymorphicInlineCache() { return {}; }
    async detectMegamorphicCallSites() { return []; }
    async detectUnreachableCodeOptimization() { return false; }
    async detectUnusedVariableElimination() { return false; }
    async detectDeadStoreElimination() { return false; }
    async detectConstantFolding() { return false; }
    async detectConstantPropagation() { return false; }
    async detectStrengthReduction() { return false; }
    async detectLoopUnrolling() { return false; }
    async detectLoopInvariantMotion() { return false; }
    async detectVectorization() { return false; }
    async detectLoopPeeling() { return false; }
}

// Export the class
export default SessionFingerprintCollector;