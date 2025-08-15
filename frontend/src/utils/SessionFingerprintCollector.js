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
     * Collect browser characteristics
     */
    async collectBrowserCharacteristics() {
        try {
            const browserData = {
                user_agent: navigator.userAgent,
                browser_name: this.getBrowserName(),
                browser_version: this.getBrowserVersion(),
                engine_name: this.getEngineInfo().name,
                engine_version: this.getEngineInfo().version,
                platform: navigator.platform,
                language: navigator.language,
                languages: navigator.languages || [],
                cookie_enabled: navigator.cookieEnabled,
                do_not_track: navigator.doNotTrack,
                java_enabled: navigator.javaEnabled ? navigator.javaEnabled() : false,
                plugins: this.getPluginInfo(),
                mime_types: this.getMimeTypes(),
                local_storage: this.testLocalStorage(),
                session_storage: this.testSessionStorage(),
                indexed_db: this.testIndexedDB(),
                webgl_support: this.testWebGLSupport(),
                canvas_support: this.testCanvasSupport(),
                audio_support: this.testAudioSupport(),
                video_support: this.testVideoSupport(),
                geolocation_support: 'geolocation' in navigator,
                notification_support: 'Notification' in window,
                service_worker_support: 'serviceWorker' in navigator,
                web_assembly_support: 'WebAssembly' in window,
                touch_support: 'ontouchstart' in window,
                max_touch_points: navigator.maxTouchPoints || 0,
                pointer_enabled: 'PointerEvent' in window,
                pdf_viewer: navigator.pdfViewerEnabled || false
            };
            
            // Additional browser fingerprinting
            browserData.timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            browserData.timezone_offset = new Date().getTimezoneOffset();
            browserData.screen_orientation = screen.orientation ? screen.orientation.type : 'unknown';
            
            return browserData;
            
        } catch (error) {
            this.logger.error("Error collecting browser characteristics:", error);
            return { user_agent: navigator.userAgent };
        }
    }
    
    /**
     * Collect network information
     */
    async collectNetworkInformation() {
        try {
            const networkData = {
                connection_type: 'unknown',
                effective_type: 'unknown',
                downlink: 0,
                rtt: 0,
                save_data: false
            };
            
            // Network Information API
            if ('connection' in navigator) {
                const connection = navigator.connection;
                networkData.connection_type = connection.type || connection.effectiveType || 'unknown';
                networkData.effective_type = connection.effectiveType || 'unknown';
                networkData.downlink = connection.downlink || 0;
                networkData.rtt = connection.rtt || 0;
                networkData.save_data = connection.saveData || false;
            }
            
            // WebRTC IP detection (privacy-conscious)
            try {
                const ipInfo = await this.detectLocalIP();
                networkData.local_ip_hash = await this.hashSensitiveData(ipInfo.ip);
                networkData.ip_type = ipInfo.type;
            } catch (e) {
                this.logger.warn("IP detection failed (privacy settings may block)");
            }
            
            // Network timing measurement
            const networkTiming = await this.measureNetworkTiming();
            networkData.latency_estimate = networkTiming.latency;
            networkData.bandwidth_estimate = networkTiming.bandwidth;
            
            return networkData;
            
        } catch (error) {
            this.logger.error("Error collecting network information:", error);
            return {};
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