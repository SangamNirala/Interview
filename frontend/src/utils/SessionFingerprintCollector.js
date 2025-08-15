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
     * PHASE 3.4: ENHANCED DEVICE FINGERPRINT COLLECTION
     * Collect comprehensive device hardware fingerprint including:
     * - Hardware enumeration via WebGL and Canvas
     * - Screen characteristics and color profile  
     * - CPU architecture and performance benchmarking
     * - Memory and storage capacity detection
     * - Device sensor availability and characteristics
     */
    async collectDeviceFingerprint() {
        try {
            this.logger.info("🔧 Starting enhanced device fingerprint collection");
            
            const deviceFingerprint = {
                // Enhanced hardware enumeration via WebGL and Canvas
                hardware_enumeration: await this.collectHardwareEnumeration(),
                
                // Enhanced screen characteristics and color profile
                screen_characteristics: await this.collectScreenCharacteristics(),
                
                // Enhanced CPU architecture and performance benchmarking  
                cpu_architecture: await this.getCPUCharacteristics(),
                
                // Enhanced memory and storage capacity detection
                memory_storage: {
                    memory: await this.getMemoryCharacteristics(),
                    storage: await this.getStorageCharacteristics()
                },
                
                // Enhanced device sensor availability and characteristics
                device_sensors: await this.getSensorCharacteristics(),
                
                // Additional device identifiers
                device_identifiers: {
                    hardware_concurrency: navigator.hardwareConcurrency || 0,
                    device_memory_gb: navigator.deviceMemory || 0,
                    platform: navigator.platform,
                    user_agent_platform: this.extractPlatformFromUserAgent(),
                    max_touch_points: navigator.maxTouchPoints || 0,
                    connection_type: this.getConnectionType()
                },
                
                // Performance benchmarking results
                performance_benchmarks: await this.collectDevicePerformanceBenchmarks(),
                
                // Canvas fingerprinting
                canvas_fingerprint: await this.generateCanvasFingerprint(),
                
                // WebGL fingerprinting
                webgl_fingerprint: await this.generateWebGLFingerprint(),
                
                // Collection metadata
                collection_metadata: {
                    timestamp: new Date().toISOString(),
                    collection_id: this.generateUniqueId(),
                    fingerprint_version: "3.4_enhanced",
                    collection_method: "comprehensive_hardware_enumeration"
                }
            };
            
            this.logger.info("✅ Device fingerprint collection completed successfully");
            return deviceFingerprint;
            
        } catch (error) {
            this.logger.error("❌ Error collecting enhanced device fingerprint:", error);
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
     * PHASE 3.4: ENHANCED BROWSER CHARACTERISTICS COLLECTION
     * Collect comprehensive browser characteristics including:
     * - Browser version, plugins, and extensions
     * - JavaScript engine capabilities and performance
     * - Rendering engine fingerprinting
     * - Font enumeration and rendering analysis
     * - Browser API availability and behavior
     */
    async collectBrowserCharacteristics() {
        try {
            this.logger.info("🌐 Starting enhanced browser characteristics collection");
            
            const browserData = {
                // Enhanced browser version, plugins, and extensions
                browser_identification: {
                    user_agent: navigator.userAgent,
                    browser_name: this.getBrowserName(),
                    browser_version: this.getBrowserVersion(),
                    browser_build_id: this.getBrowserBuildId(),
                    platform: navigator.platform,
                    oscpu: navigator.oscpu || 'unknown',
                    product: navigator.product,
                    product_sub: navigator.productSub,
                    vendor: navigator.vendor,
                    vendor_sub: navigator.vendorSub || 'unknown'
                },
                
                // Enhanced JavaScript engine capabilities and performance
                javascript_engine: await this.collectJavaScriptEngineInfo(),
                
                // Enhanced rendering engine fingerprinting
                rendering_engine: await this.collectRenderingEngineInfo(),
                
                // Enhanced font enumeration and rendering analysis
                font_analysis: await this.collectFontAnalysis(),
                
                // Enhanced browser API availability and behavior
                api_availability: await this.collectAPIAvailability(),
                
                // Plugin and extension analysis
                plugins_extensions: {
                    plugins: this.getPluginInfo(),
                    mime_types: this.getMimeTypes(),
                    plugin_count: navigator.plugins.length,
                    mime_count: navigator.mimeTypes.length
                },
                
                // Language and localization
                localization: {
                    language: navigator.language,
                    languages: navigator.languages || [],
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                    timezone_offset: new Date().getTimezoneOffset(),
                    number_format: this.detectNumberFormat(),
                    date_format: this.detectDateFormat(),
                    currency: this.detectCurrency()
                },
                
                // Security and privacy settings
                security_privacy: {
                    cookie_enabled: navigator.cookieEnabled,
                    do_not_track: navigator.doNotTrack,
                    java_enabled: navigator.javaEnabled ? navigator.javaEnabled() : false,
                    pdf_viewer_enabled: navigator.pdfViewerEnabled || false,
                    webdriver_present: navigator.webdriver || false
                },
                
                // Storage capabilities
                storage_capabilities: {
                    local_storage: this.testLocalStorage(),
                    session_storage: this.testSessionStorage(),
                    indexed_db: this.testIndexedDB(),
                    web_sql: 'openDatabase' in window,
                    cache_api: 'caches' in window,
                    storage_estimate: await this.getStorageEstimate()
                },
                
                // Media and input capabilities
                media_input: {
                    audio_support: this.testAudioSupport(),
                    video_support: this.testVideoSupport(),
                    media_devices: await this.enumerateMediaDevices(),
                    touch_support: 'ontouchstart' in window,
                    max_touch_points: navigator.maxTouchPoints || 0,
                    pointer_events: 'PointerEvent' in window,
                    mouse_events: 'MouseEvent' in window,
                    keyboard_events: 'KeyboardEvent' in window
                },
                
                // Advanced web APIs
                web_apis: {
                    geolocation: 'geolocation' in navigator,
                    notifications: 'Notification' in window,
                    service_worker: 'serviceWorker' in navigator,
                    web_assembly: 'WebAssembly' in window,
                    webgl_support: this.testWebGLSupport(),
                    webgl2_support: this.testWebGL2Support(),
                    canvas_support: this.testCanvasSupport(),
                    web_rtc: 'RTCPeerConnection' in window,
                    websockets: 'WebSocket' in window,
                    shared_workers: 'SharedWorker' in window,
                    dedicated_workers: 'Worker' in window,
                    crypto_subtle: 'crypto' in window && 'subtle' in crypto,
                    fetch_api: 'fetch' in window,
                    streams_api: 'ReadableStream' in window
                },
                
                // Performance and capabilities testing
                performance_capabilities: await this.collectBrowserPerformanceInfo(),
                
                // Browser fingerprinting via rendering
                rendering_fingerprint: await this.generateBrowserRenderingFingerprint(),
                
                // Collection metadata
                collection_metadata: {
                    timestamp: new Date().toISOString(),
                    collection_id: this.generateUniqueId(),
                    fingerprint_version: "3.4_enhanced",
                    user_agent_hash: await this.hashSensitiveData(navigator.userAgent)
                }
            };
            
            this.logger.info("✅ Browser characteristics collection completed successfully");
            return browserData;
            
        } catch (error) {
            this.logger.error("❌ Error collecting enhanced browser characteristics:", error);
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
     * Collect environmental data
     */
    async collectEnvironmentalData() {
        try {
            const envData = {
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
            };
            
            return envData;
            
        } catch (error) {
            this.logger.error("Error collecting environmental data:", error);
            return { timezone: Intl.DateTimeFormat().resolvedOptions().timeZone };
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
}

// Export the class
export default SessionFingerprintCollector;