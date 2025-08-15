"""
MongoDB Database Performance Optimization Module
Task 2.2: Advanced performance optimization for fingerprinting system

This module provides comprehensive database performance optimization including:
- Compound indexes for complex multi-field queries
- TTL indexes for automatic data expiration and privacy compliance
- Pre-built aggregation pipelines for analytics and reporting
- Optimized MongoDB connection pool configuration
- Built-in query performance monitoring and metrics

Author: AI Assistant
Created: 2025
"""

import asyncio
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, TEXT, GEO2D
from pymongo.errors import OperationFailure, DuplicateKeyError
from dotenv import load_dotenv
import statistics
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QueryPerformanceMetrics:
    """Query performance tracking data structure"""
    query_type: str
    collection: str
    execution_time: float
    documents_examined: int
    documents_returned: int
    index_used: str
    timestamp: datetime
    query_pattern: str
    success: bool
    error_message: str = ""

@dataclass
class IndexPerformanceData:
    """Index performance and usage statistics"""
    index_name: str
    collection: str
    usage_count: int
    avg_query_time: float
    total_examined: int
    total_returned: int
    efficiency_ratio: float
    last_used: datetime
    created_at: datetime

class DatabaseOptimizationManager:
    """
    Comprehensive database performance optimization manager
    
    Provides advanced optimization features including compound indexes,
    TTL setup, aggregation pipelines, connection pooling, and performance monitoring.
    """
    
    def __init__(self):
        """Initialize database optimization manager"""
        load_dotenv()
        self.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.db_name = os.environ.get('DB_NAME', 'test_database')
        self.client = None
        self.db = None
        
        # Performance monitoring
        self.query_metrics = deque(maxlen=10000)  # Keep last 10k queries
        self.index_usage_stats = defaultdict(lambda: defaultdict(int))
        self.slow_query_threshold = 1.0  # 1 second threshold
        
        # Aggregation pipelines cache
        self.cached_pipelines = {}
        self.pipeline_performance = {}
        
        logger.info("DatabaseOptimizationManager initialized")
    
    async def connect(self, optimized_settings: bool = True):
        """
        Establish optimized async connection to MongoDB
        
        Args:
            optimized_settings: Whether to apply connection pool optimizations
        """
        try:
            # Connection pool optimization settings
            if optimized_settings:
                connection_options = {
                    # Connection Pool Settings
                    'maxPoolSize': 100,  # Maximum connections in pool
                    'minPoolSize': 10,   # Minimum connections maintained
                    'maxIdleTimeMS': 30000,  # 30 seconds idle timeout
                    'waitQueueTimeoutMS': 5000,  # 5 seconds wait timeout
                    
                    # Network and Timeout Settings
                    'connectTimeoutMS': 10000,  # 10 seconds connection timeout
                    'serverSelectionTimeoutMS': 10000,  # 10 seconds server selection
                    'socketTimeoutMS': 30000,  # 30 seconds socket timeout
                    
                    # Read/Write Settings
                    'readPreference': 'primaryPreferred',  # Read from primary preferably
                    'w': 1,  # Write concern: acknowledge from primary
                    'readConcernLevel': 'local',  # Local read concern for performance
                    
                    # Compression and Performance
                    'compressors': 'snappy,zlib',  # Enable compression
                    'retryWrites': True,  # Retry failed writes
                    'retryReads': True,   # Retry failed reads
                    
                    # Application Settings
                    'appName': 'FingerprintingSystem_Optimized',
                    'heartbeatFrequencyMS': 10000,  # 10 seconds heartbeat
                }
                
                self.client = AsyncIOMotorClient(self.mongo_url, **connection_options)
                logger.info("Connected to MongoDB with optimized connection pool settings")
            else:
                self.client = AsyncIOMotorClient(self.mongo_url)
                logger.info("Connected to MongoDB with default settings")
            
            self.db = self.client[self.db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info(f"Successfully connected to database: {self.db_name}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            return False
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

async def create_compound_indexes():
    """
    Create advanced compound indexes for complex multi-field queries
    
    Implements optimized compound indexes based on common query patterns
    for all 6 fingerprinting collections.
    
    Returns:
        Dict: Status of compound index creation
    """
    
    optimization_manager = DatabaseOptimizationManager()
    
    if not await optimization_manager.connect():
        return {
            'success': False,
            'error': 'Failed to connect to MongoDB',
            'timestamp': datetime.now().isoformat()
        }
    
    compound_index_config = {
        'device_fingerprints': [
            # Multi-field query optimization
            {
                'keys': [('device_id', ASCENDING), ('created_at', DESCENDING), ('confidence_score', DESCENDING)],
                'name': 'device_timeline_confidence_idx',
                'background': True,
                'description': 'Optimizes device timeline queries with confidence filtering'
            },
            {
                'keys': [('signature_hash', ASCENDING), ('session_id', ASCENDING), ('created_at', DESCENDING)],
                'name': 'signature_session_timeline_idx',
                'background': True,
                'description': 'Optimizes signature-based session queries'
            },
            {
                'keys': [('hardware_signature.cpu_cores', ASCENDING), ('hardware_signature.memory_gb', ASCENDING), ('confidence_score', DESCENDING)],
                'name': 'hardware_specs_confidence_idx',
                'background': True,
                'description': 'Optimizes hardware specification queries with confidence ranking'
            },
            {
                'keys': [('device_id', ASCENDING), ('signature_hash', ASCENDING)],
                'name': 'device_signature_lookup_idx',
                'unique': True,
                'background': True,
                'description': 'Ensures unique device-signature combinations'
            }
        ],
        
        'browser_fingerprints': [
            {
                'keys': [('browser_id', ASCENDING), ('created_at', DESCENDING), ('fingerprint_entropy', DESCENDING)],
                'name': 'browser_timeline_entropy_idx',
                'background': True,
                'description': 'Optimizes browser timeline queries with entropy ranking'
            },
            {
                'keys': [('user_agent_hash', ASCENDING), ('session_id', ASCENDING), ('created_at', DESCENDING)],
                'name': 'ua_session_timeline_idx',
                'background': True,
                'description': 'Optimizes user agent session queries'
            },
            {
                'keys': [('user_agent_analysis.browser_family', ASCENDING), ('user_agent_analysis.version', ASCENDING), ('fingerprint_entropy', DESCENDING)],
                'name': 'browser_version_entropy_idx',
                'background': True,
                'description': 'Optimizes browser version queries with entropy filtering'
            },
            {
                'keys': [('canvas_fingerprint', TEXT), ('webgl_fingerprint', TEXT)],
                'name': 'canvas_webgl_text_search_idx',
                'background': True,
                'description': 'Enables text search across canvas and WebGL fingerprints'
            }
        ],
        
        'session_integrity_profiles': [
            {
                'keys': [('session_id', ASCENDING), ('device_id', ASCENDING), ('created_at', DESCENDING)],
                'name': 'session_device_timeline_idx',
                'background': True,
                'description': 'Optimizes session-device relationship queries'
            },
            {
                'keys': [('integrity_score', DESCENDING), ('risk_level', ASCENDING), ('created_at', DESCENDING)],
                'name': 'integrity_risk_timeline_idx',
                'background': True,
                'description': 'Optimizes integrity and risk assessment queries'
            },
            {
                'keys': [('device_consistency_score', DESCENDING), ('authenticity_confidence', DESCENDING), ('session_id', ASCENDING)],
                'name': 'consistency_authenticity_session_idx',
                'background': True,
                'description': 'Optimizes consistency and authenticity scoring queries'
            },
            {
                'keys': [('risk_level', ASCENDING), ('created_at', DESCENDING)],
                'name': 'risk_chronological_idx',
                'background': True,
                'description': 'Optimizes risk-based chronological queries'
            }
        ],
        
        'fingerprint_violations': [
            {
                'keys': [('session_id', ASCENDING), ('violation_type', ASCENDING), ('severity', DESCENDING), ('detected_at', DESCENDING)],
                'name': 'session_violation_severity_idx',
                'background': True,
                'description': 'Optimizes session violation queries with severity ranking'
            },
            {
                'keys': [('device_id', ASCENDING), ('violation_type', ASCENDING), ('detected_at', DESCENDING)],
                'name': 'device_violation_timeline_idx',
                'background': True,
                'description': 'Optimizes device-specific violation timeline queries'
            },
            {
                'keys': [('severity', DESCENDING), ('detected_at', DESCENDING), ('violation_type', ASCENDING)],
                'name': 'severity_timeline_type_idx',
                'background': True,
                'description': 'Optimizes high-severity violation monitoring'
            },
            {
                'keys': [('created_at', DESCENDING), ('severity', DESCENDING)],
                'name': 'recent_severe_violations_idx',
                'background': True,
                'description': 'Optimizes recent severe violation detection'
            }
        ],
        
        'device_reputation_scores': [
            {
                'keys': [('device_id', ASCENDING), ('reputation_score', DESCENDING), ('last_updated', DESCENDING)],
                'name': 'device_reputation_timeline_idx',
                'background': True,
                'description': 'Optimizes device reputation tracking over time'
            },
            {
                'keys': [('risk_category', ASCENDING), ('reputation_score', DESCENDING), ('last_updated', DESCENDING)],
                'name': 'risk_reputation_ranking_idx',
                'background': True,
                'description': 'Optimizes risk-based reputation rankings'
            },
            {
                'keys': [('reputation_score', DESCENDING), ('trust_level', ASCENDING), ('device_id', ASCENDING)],
                'name': 'reputation_trust_device_idx',
                'background': True,
                'description': 'Optimizes reputation and trust level queries'
            },
            {
                'keys': [('last_updated', DESCENDING), ('reputation_score', DESCENDING)],
                'name': 'recent_reputation_changes_idx',
                'background': True,
                'description': 'Optimizes recent reputation change monitoring'
            }
        ],
        
        'fingerprint_analytics': [
            {
                'keys': [('analytics_type', ASCENDING), ('date_range.start', ASCENDING), ('date_range.end', ASCENDING)],
                'name': 'analytics_date_range_idx',
                'background': True,
                'description': 'Optimizes analytics queries by type and date range'
            },
            {
                'keys': [('device_count', DESCENDING), ('analytics_type', ASCENDING), ('created_at', DESCENDING)],
                'name': 'device_count_analytics_idx',
                'background': True,
                'description': 'Optimizes device count analytics with type filtering'
            },
            {
                'keys': [('created_at', DESCENDING), ('analytics_type', ASCENDING)],
                'name': 'recent_analytics_by_type_idx',
                'background': True,
                'description': 'Optimizes recent analytics retrieval by type'
            },
            {
                'keys': [('summary_metrics.total_sessions', DESCENDING), ('summary_metrics.unique_devices', DESCENDING)],
                'name': 'session_device_metrics_idx',
                'background': True,
                'description': 'Optimizes session and device metrics queries'
            }
        ]
    }
    
    compound_results = {
        'success': True,
        'compound_indexes_created': 0,
        'collections_processed': 0,
        'index_status': {},
        'errors': [],
        'timestamp': datetime.now().isoformat(),
        'database': optimization_manager.db_name
    }
    
    try:
        for collection_name, index_configs in compound_index_config.items():
            collection_result = {
                'compound_indexes_created': 0,
                'indexes_attempted': len(index_configs),
                'errors': []
            }
            
            try:
                collection = optimization_manager.db[collection_name]
                
                for index_config in index_configs:
                    try:
                        keys = index_config['keys']
                        options = {k: v for k, v in index_config.items() if k not in ['keys', 'description']}
                        
                        # Create compound index
                        await collection.create_index(keys, **options)
                        collection_result['compound_indexes_created'] += 1
                        compound_results['compound_indexes_created'] += 1
                        
                        logger.info(f"Created compound index '{index_config['name']}' on {collection_name}: {keys}")
                        
                    except DuplicateKeyError:
                        logger.info(f"Compound index '{index_config['name']}' already exists on {collection_name}")
                        collection_result['compound_indexes_created'] += 1
                        compound_results['compound_indexes_created'] += 1
                    except Exception as e:
                        error_msg = f"Failed to create compound index '{index_config['name']}' on {collection_name}: {str(e)}"
                        logger.error(error_msg)
                        collection_result['errors'].append(error_msg)
                
                compound_results['collections_processed'] += 1
                compound_results['index_status'][collection_name] = collection_result
                
            except Exception as e:
                error_msg = f"Failed to process collection {collection_name}: {str(e)}"
                logger.error(error_msg)
                compound_results['errors'].append(error_msg)
        
        logger.info(f"Compound index creation completed:")
        logger.info(f"  - Collections processed: {compound_results['collections_processed']}")
        logger.info(f"  - Compound indexes created: {compound_results['compound_indexes_created']}")
        
        if compound_results['errors']:
            compound_results['success'] = False
            logger.warning(f"Compound index creation completed with {len(compound_results['errors'])} errors")
            
    except Exception as e:
        error_msg = f"Critical error during compound index creation: {str(e)}"
        logger.error(error_msg)
        compound_results['success'] = False
        compound_results['errors'].append(error_msg)
        
    finally:
        await optimization_manager.close()
    
    return compound_results


async def setup_ttl_indexes():
    """
    Set up TTL (Time To Live) indexes for automatic data expiration
    
    Implements privacy compliance through automatic data cleanup.
    Different retention periods based on data sensitivity and regulatory requirements.
    
    Returns:
        Dict: Status of TTL index creation
    """
    
    optimization_manager = DatabaseOptimizationManager()
    
    if not await optimization_manager.connect():
        return {
            'success': False,
            'error': 'Failed to connect to MongoDB',
            'timestamp': datetime.now().isoformat()
        }
    
    # TTL Configuration based on data sensitivity and compliance requirements
    ttl_index_config = {
        'device_fingerprints': {
            'ttl_seconds': 7776000,  # 90 days (3 months) for device data
            'field': 'created_at',
            'description': 'Auto-expire device fingerprints after 90 days for privacy compliance'
        },
        
        'browser_fingerprints': {
            'ttl_seconds': 7776000,  # 90 days (3 months) for browser data
            'field': 'created_at',
            'description': 'Auto-expire browser fingerprints after 90 days for privacy compliance'
        },
        
        'session_integrity_profiles': {
            'ttl_seconds': 2592000,  # 30 days (1 month) for session data
            'field': 'created_at',
            'description': 'Auto-expire session profiles after 30 days for privacy and performance'
        },
        
        'fingerprint_violations': {
            'ttl_seconds': 15552000,  # 180 days (6 months) for security violations
            'field': 'detected_at',
            'description': 'Auto-expire violation records after 180 days for security audit compliance'
        },
        
        'device_reputation_scores': {
            'ttl_seconds': 31536000,  # 365 days (1 year) for reputation data
            'field': 'last_updated',
            'description': 'Auto-expire reputation scores after 1 year for long-term trust analysis'
        },
        
        'fingerprint_analytics': {
            'ttl_seconds': 7776000,  # 90 days (3 months) for analytics data
            'field': 'created_at',
            'description': 'Auto-expire analytics data after 90 days for performance optimization'
        }
    }
    
    ttl_results = {
        'success': True,
        'ttl_indexes_created': 0,
        'collections_processed': 0,
        'ttl_status': {},
        'errors': [],
        'timestamp': datetime.now().isoformat(),
        'database': optimization_manager.db_name
    }
    
    try:
        for collection_name, ttl_config in ttl_index_config.items():
            collection_result = {
                'ttl_created': False,
                'ttl_seconds': ttl_config['ttl_seconds'],
                'retention_days': ttl_config['ttl_seconds'] / 86400,  # Convert to days
                'field': ttl_config['field'],
                'description': ttl_config['description'],
                'error': None
            }
            
            try:
                collection = optimization_manager.db[collection_name]
                
                # Create TTL index
                await collection.create_index(
                    [(ttl_config['field'], ASCENDING)],
                    expireAfterSeconds=ttl_config['ttl_seconds'],
                    name=f"{collection_name}_ttl_idx",
                    background=True
                )
                
                collection_result['ttl_created'] = True
                ttl_results['ttl_indexes_created'] += 1
                ttl_results['collections_processed'] += 1
                
                retention_days = ttl_config['ttl_seconds'] / 86400
                logger.info(f"Created TTL index on {collection_name}.{ttl_config['field']} "
                           f"with {retention_days:.0f} days retention")
                
            except DuplicateKeyError:
                logger.info(f"TTL index already exists on {collection_name}.{ttl_config['field']}")
                collection_result['ttl_created'] = True
                ttl_results['ttl_indexes_created'] += 1
                ttl_results['collections_processed'] += 1
            except Exception as e:
                error_msg = f"Failed to create TTL index on {collection_name}: {str(e)}"
                logger.error(error_msg)
                collection_result['error'] = error_msg
                ttl_results['errors'].append(error_msg)
            
            ttl_results['ttl_status'][collection_name] = collection_result
        
        logger.info(f"TTL index creation completed:")
        logger.info(f"  - Collections processed: {ttl_results['collections_processed']}")
        logger.info(f"  - TTL indexes created: {ttl_results['ttl_indexes_created']}")
        
        # Log retention summary
        logger.info("Data retention summary:")
        for collection_name, ttl_config in ttl_index_config.items():
            retention_days = ttl_config['ttl_seconds'] / 86400
            logger.info(f"  - {collection_name}: {retention_days:.0f} days retention")
        
        if ttl_results['errors']:
            ttl_results['success'] = False
            logger.warning(f"TTL index creation completed with {len(ttl_results['errors'])} errors")
            
    except Exception as e:
        error_msg = f"Critical error during TTL index creation: {str(e)}"
        logger.error(error_msg)
        ttl_results['success'] = False
        ttl_results['errors'].append(error_msg)
        
    finally:
        await optimization_manager.close()
    
    return ttl_results


async def create_aggregation_pipelines():
    """
    Create pre-built optimized aggregation pipelines for analytics and reporting
    
    Implements common analytics queries as optimized MongoDB aggregation pipelines
    with built-in performance monitoring and caching.
    
    Returns:
        Dict: Available aggregation pipelines and their performance characteristics
    """
    
    optimization_manager = DatabaseOptimizationManager()
    
    if not await optimization_manager.connect():
        return {
            'success': False,
            'error': 'Failed to connect to MongoDB',
            'timestamp': datetime.now().isoformat()
        }
    
    # Pre-built aggregation pipelines for common analytics queries
    aggregation_pipelines = {
        'device_fingerprint_analytics': {
            'description': 'Device fingerprinting analytics with confidence scoring',
            'pipeline': [
                # Match recent records (last 30 days)
                {
                    '$match': {
                        'created_at': {
                            '$gte': datetime.now() - timedelta(days=30)
                        }
                    }
                },
                # Group by device characteristics
                {
                    '$group': {
                        '_id': {
                            'device_id': '$device_id',
                            'hardware_signature': '$hardware_signature'
                        },
                        'avg_confidence': {'$avg': '$confidence_score'},
                        'max_confidence': {'$max': '$confidence_score'},
                        'min_confidence': {'$min': '$confidence_score'},
                        'fingerprint_count': {'$sum': 1},
                        'unique_sessions': {'$addToSet': '$session_id'},
                        'first_seen': {'$min': '$created_at'},
                        'last_seen': {'$max': '$created_at'}
                    }
                },
                # Calculate session count
                {
                    '$addFields': {
                        'session_count': {'$size': '$unique_sessions'},
                        'confidence_variance': {
                            '$subtract': ['$max_confidence', '$min_confidence']
                        }
                    }
                },
                # Sort by confidence and activity
                {
                    '$sort': {
                        'avg_confidence': -1,
                        'fingerprint_count': -1
                    }
                },
                # Limit results for performance
                {'$limit': 1000}
            ],
            'collection': 'device_fingerprints',
            'estimated_time': 'fast',  # < 100ms
            'cache_duration': 300  # 5 minutes cache
        },
        
        'browser_entropy_analysis': {
            'description': 'Browser fingerprint entropy analysis and uniqueness scoring',
            'pipeline': [
                # Match recent browser fingerprints
                {
                    '$match': {
                        'created_at': {
                            '$gte': datetime.now() - timedelta(days=7)
                        }
                    }
                },
                # Group by browser characteristics
                {
                    '$group': {
                        '_id': {
                            'browser_family': '$user_agent_analysis.browser_family',
                            'browser_version': '$user_agent_analysis.version',
                            'os_family': '$user_agent_analysis.os_family'
                        },
                        'avg_entropy': {'$avg': '$fingerprint_entropy'},
                        'max_entropy': {'$max': '$fingerprint_entropy'},
                        'fingerprint_count': {'$sum': 1},
                        'unique_browsers': {'$addToSet': '$browser_id'},
                        'canvas_fingerprints': {'$addToSet': '$canvas_fingerprint'},
                        'webgl_fingerprints': {'$addToSet': '$webgl_fingerprint'}
                    }
                },
                # Calculate uniqueness metrics
                {
                    '$addFields': {
                        'browser_count': {'$size': '$unique_browsers'},
                        'canvas_uniqueness': {'$size': '$canvas_fingerprints'},
                        'webgl_uniqueness': {'$size': '$webgl_fingerprints'},
                        'entropy_category': {
                            '$switch': {
                                'branches': [
                                    {'case': {'$gte': ['$avg_entropy', 0.8]}, 'then': 'high'},
                                    {'case': {'$gte': ['$avg_entropy', 0.5]}, 'then': 'medium'},
                                    {'case': {'$gte': ['$avg_entropy', 0.2]}, 'then': 'low'}
                                ],
                                'default': 'minimal'
                            }
                        }
                    }
                },
                # Sort by entropy and uniqueness
                {
                    '$sort': {
                        'avg_entropy': -1,
                        'canvas_uniqueness': -1
                    }
                },
                {'$limit': 500}
            ],
            'collection': 'browser_fingerprints',
            'estimated_time': 'medium',  # 100-500ms
            'cache_duration': 600  # 10 minutes cache
        },
        
        'session_integrity_monitoring': {
            'description': 'Real-time session integrity and risk assessment',
            'pipeline': [
                # Match active sessions (last 24 hours)
                {
                    '$match': {
                        'created_at': {
                            '$gte': datetime.now() - timedelta(hours=24)
                        }
                    }
                },
                # Group by risk level and device
                {
                    '$group': {
                        '_id': {
                            'risk_level': '$risk_level',
                            'device_id': '$device_id'
                        },
                        'avg_integrity_score': {'$avg': '$integrity_score'},
                        'avg_consistency_score': {'$avg': '$device_consistency_score'},
                        'avg_authenticity': {'$avg': '$authenticity_confidence'},
                        'session_count': {'$sum': 1},
                        'unique_sessions': {'$addToSet': '$session_id'},
                        'latest_activity': {'$max': '$created_at'}
                    }
                },
                # Calculate risk metrics
                {
                    '$addFields': {
                        'active_sessions': {'$size': '$unique_sessions'},
                        'risk_score': {
                            '$multiply': [
                                {'$subtract': [1, '$avg_integrity_score']},
                                {'$subtract': [1, '$avg_authenticity']}
                            ]
                        }
                    }
                },
                # Sort by risk level and activity
                {
                    '$sort': {
                        'risk_score': -1,
                        'latest_activity': -1
                    }
                },
                # Focus on high-risk sessions
                {
                    '$match': {
                        '$or': [
                            {'_id.risk_level': 'high'},
                            {'_id.risk_level': 'critical'},
                            {'risk_score': {'$gte': 0.3}}
                        ]
                    }
                },
                {'$limit': 200}
            ],
            'collection': 'session_integrity_profiles',
            'estimated_time': 'fast',  # < 100ms
            'cache_duration': 60  # 1 minute cache (real-time monitoring)
        },
        
        'violation_trend_analysis': {
            'description': 'Violation trends and pattern analysis over time',
            'pipeline': [
                # Match violations from last 7 days
                {
                    '$match': {
                        'detected_at': {
                            '$gte': datetime.now() - timedelta(days=7)
                        }
                    }
                },
                # Group by violation type and day
                {
                    '$group': {
                        '_id': {
                            'violation_type': '$violation_type',
                            'severity': '$severity',
                            'day': {
                                '$dateToString': {
                                    'format': '%Y-%m-%d',
                                    'date': '$detected_at'
                                }
                            }
                        },
                        'violation_count': {'$sum': 1},
                        'unique_devices': {'$addToSet': '$device_id'},
                        'unique_sessions': {'$addToSet': '$session_id'},
                        'avg_severity_score': {'$avg': '$severity_score'},
                        'first_occurrence': {'$min': '$detected_at'},
                        'last_occurrence': {'$max': '$detected_at'}
                    }
                },
                # Calculate additional metrics
                {
                    '$addFields': {
                        'affected_devices': {'$size': '$unique_devices'},
                        'affected_sessions': {'$size': '$unique_sessions'},
                        'violation_rate': {
                            '$divide': ['$violation_count', '$affected_sessions']
                        }
                    }
                },
                # Sort by severity and count
                {
                    '$sort': {
                        '_id.severity': -1,
                        'violation_count': -1,
                        '_id.day': -1
                    }
                },
                {'$limit': 300}
            ],
            'collection': 'fingerprint_violations',
            'estimated_time': 'medium',  # 100-500ms
            'cache_duration': 900  # 15 minutes cache
        },
        
        'reputation_scoring_analysis': {
            'description': 'Device reputation scoring and trust level analysis',
            'pipeline': [
                # Match recent reputation updates
                {
                    '$match': {
                        'last_updated': {
                            '$gte': datetime.now() - timedelta(days=30)
                        }
                    }
                },
                # Group by risk category and trust level
                {
                    '$group': {
                        '_id': {
                            'risk_category': '$risk_category',
                            'trust_level': '$trust_level'
                        },
                        'avg_reputation': {'$avg': '$reputation_score'},
                        'min_reputation': {'$min': '$reputation_score'},
                        'max_reputation': {'$max': '$reputation_score'},
                        'device_count': {'$sum': 1},
                        'unique_devices': {'$addToSet': '$device_id'},
                        'latest_update': {'$max': '$last_updated'}
                    }
                },
                # Calculate reputation distribution
                {
                    '$addFields': {
                        'reputation_range': {
                            '$subtract': ['$max_reputation', '$min_reputation']
                        },
                        'reputation_category': {
                            '$switch': {
                                'branches': [
                                    {'case': {'$gte': ['$avg_reputation', 0.8]}, 'then': 'excellent'},
                                    {'case': {'$gte': ['$avg_reputation', 0.6]}, 'then': 'good'},
                                    {'case': {'$gte': ['$avg_reputation', 0.4]}, 'then': 'fair'},
                                    {'case': {'$gte': ['$avg_reputation', 0.2]}, 'then': 'poor'}
                                ],
                                'default': 'critical'
                            }
                        }
                    }
                },
                # Sort by reputation and count
                {
                    '$sort': {
                        'avg_reputation': -1,
                        'device_count': -1
                    }
                },
                {'$limit': 100}
            ],
            'collection': 'device_reputation_scores',
            'estimated_time': 'fast',  # < 100ms
            'cache_duration': 1800  # 30 minutes cache
        }
    }
    
    pipeline_results = {
        'success': True,
        'pipelines_created': 0,
        'pipeline_details': {},
        'performance_estimates': {},
        'errors': [],
        'timestamp': datetime.now().isoformat(),
        'database': optimization_manager.db_name
    }
    
    try:
        # Test and validate each aggregation pipeline
        for pipeline_name, pipeline_config in aggregation_pipelines.items():
            pipeline_result = {
                'created': False,
                'validated': False,
                'collection': pipeline_config['collection'],
                'estimated_time': pipeline_config['estimated_time'],
                'cache_duration': pipeline_config['cache_duration'],
                'description': pipeline_config['description'],
                'stage_count': len(pipeline_config['pipeline']),
                'error': None
            }
            
            try:
                # Test pipeline execution (with small limit for validation)
                collection = optimization_manager.db[pipeline_config['collection']]
                
                # Add a small limit to test pipeline
                test_pipeline = pipeline_config['pipeline'].copy()
                test_pipeline.append({'$limit': 5})
                
                start_time = time.time()
                
                # Execute test aggregation
                cursor = collection.aggregate(test_pipeline)
                test_results = await cursor.to_list(length=None)
                
                execution_time = time.time() - start_time
                
                pipeline_result['created'] = True
                pipeline_result['validated'] = True
                pipeline_result['test_results_count'] = len(test_results)
                pipeline_result['test_execution_time'] = round(execution_time * 1000, 2)  # ms
                
                # Store pipeline for caching
                optimization_manager.cached_pipelines[pipeline_name] = pipeline_config
                optimization_manager.pipeline_performance[pipeline_name] = {
                    'avg_execution_time': execution_time,
                    'last_executed': datetime.now(),
                    'execution_count': 1,
                    'cache_hits': 0
                }
                
                pipeline_results['pipelines_created'] += 1
                
                logger.info(f"Created and validated aggregation pipeline '{pipeline_name}' "
                           f"({execution_time*1000:.2f}ms, {len(test_results)} results)")
                
            except Exception as e:
                error_msg = f"Failed to create/validate pipeline '{pipeline_name}': {str(e)}"
                logger.error(error_msg)
                pipeline_result['error'] = error_msg
                pipeline_results['errors'].append(error_msg)
            
            pipeline_results['pipeline_details'][pipeline_name] = pipeline_result
        
        logger.info(f"Aggregation pipeline creation completed:")
        logger.info(f"  - Pipelines created: {pipeline_results['pipelines_created']}")
        logger.info(f"  - Total pipeline stages: {sum(len(p['pipeline']) for p in aggregation_pipelines.values())}")
        
        if pipeline_results['errors']:
            pipeline_results['success'] = False
            logger.warning(f"Pipeline creation completed with {len(pipeline_results['errors'])} errors")
            
    except Exception as e:
        error_msg = f"Critical error during aggregation pipeline creation: {str(e)}"
        logger.error(error_msg)
        pipeline_results['success'] = False
        pipeline_results['errors'].append(error_msg)
        
    finally:
        await optimization_manager.close()
    
    return pipeline_results


async def optimize_connection_pool():
    """
    Optimize MongoDB connection pool settings for maximum performance
    
    Tests and validates optimal connection pool configuration based on
    system resources and expected load patterns.
    
    Returns:
        Dict: Connection pool optimization results and recommendations
    """
    
    optimization_results = {
        'success': True,
        'optimizations_applied': [],
        'connection_tests': {},
        'recommendations': [],
        'performance_metrics': {},
        'errors': [],
        'timestamp': datetime.now().isoformat()
    }
    
    # Test different connection pool configurations
    pool_configurations = [
        {
            'name': 'light_load',
            'description': 'Optimized for light load (< 100 concurrent users)',
            'settings': {
                'maxPoolSize': 25,
                'minPoolSize': 5,
                'maxIdleTimeMS': 60000,  # 1 minute
                'waitQueueTimeoutMS': 3000
            }
        },
        {
            'name': 'medium_load',
            'description': 'Optimized for medium load (100-500 concurrent users)',
            'settings': {
                'maxPoolSize': 50,
                'minPoolSize': 10,
                'maxIdleTimeMS': 45000,  # 45 seconds
                'waitQueueTimeoutMS': 5000
            }
        },
        {
            'name': 'heavy_load',
            'description': 'Optimized for heavy load (500+ concurrent users)',
            'settings': {
                'maxPoolSize': 100,
                'minPoolSize': 20,
                'maxIdleTimeMS': 30000,  # 30 seconds
                'waitQueueTimeoutMS': 10000
            }
        }
    ]
    
    try:
        # Test each configuration
        for config in pool_configurations:
            config_name = config['name']
            config_result = {
                'tested': False,
                'connection_time': 0,
                'query_performance': 0,
                'resource_usage': 'unknown',
                'recommended': False,
                'error': None
            }
            
            try:
                # Create test client with specific configuration
                mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
                db_name = os.environ.get('DB_NAME', 'test_database')
                
                start_time = time.time()
                
                test_client = AsyncIOMotorClient(mongo_url, **config['settings'])
                test_db = test_client[db_name]
                
                # Test connection
                await test_client.admin.command('ping')
                connection_time = time.time() - start_time
                
                # Test query performance
                query_start = time.time()
                await test_db.device_fingerprints.find({}).limit(10).to_list(length=None)
                query_time = time.time() - query_start
                
                # Clean up
                test_client.close()
                
                config_result['tested'] = True
                config_result['connection_time'] = round(connection_time * 1000, 2)  # ms
                config_result['query_performance'] = round(query_time * 1000, 2)  # ms
                config_result['resource_usage'] = 'acceptable'  # Simplified assessment
                
                # Simple recommendation based on performance
                if query_time < 0.05:  # < 50ms
                    config_result['recommended'] = True
                
                logger.info(f"Tested connection pool config '{config_name}': "
                           f"connection={config_result['connection_time']}ms, "
                           f"query={config_result['query_performance']}ms")
                
            except Exception as e:
                error_msg = f"Failed to test connection pool config '{config_name}': {str(e)}"
                logger.error(error_msg)
                config_result['error'] = error_msg
                optimization_results['errors'].append(error_msg)
            
            optimization_results['connection_tests'][config_name] = config_result
        
        # Generate recommendations based on test results
        best_config = None
        best_performance = float('inf')
        
        for config_name, result in optimization_results['connection_tests'].items():
            if result['tested'] and result['query_performance'] > 0:
                total_time = result['connection_time'] + result['query_performance']
                if total_time < best_performance:
                    best_performance = total_time
                    best_config = config_name
        
        if best_config:
            optimization_results['recommendations'].append(
                f"Best performing configuration: {best_config} "
                f"(total time: {best_performance:.2f}ms)"
            )
        
        # Add general optimization recommendations
        optimization_results['recommendations'].extend([
            "Enable connection compression for network efficiency",
            "Use read preference 'primaryPreferred' for load balancing",
            "Enable retryWrites and retryReads for resilience",
            "Set appropriate heartbeat frequency for monitoring",
            "Configure write concern based on consistency requirements"
        ])
        
        optimization_results['optimizations_applied'] = [
            "Tested multiple connection pool configurations",
            "Validated connection and query performance",
            "Generated performance-based recommendations"
        ]
        
        logger.info("Connection pool optimization completed successfully")
        
    except Exception as e:
        error_msg = f"Critical error during connection pool optimization: {str(e)}"
        logger.error(error_msg)
        optimization_results['success'] = False
        optimization_results['errors'].append(error_msg)
    
    return optimization_results


class QueryPerformanceMonitor:
    """
    Built-in query performance monitoring and tracking system
    
    Monitors query execution time, index usage, and provides
    performance insights and optimization recommendations.
    """
    
    def __init__(self, slow_query_threshold: float = 1.0):
        """
        Initialize query performance monitor
        
        Args:
            slow_query_threshold: Threshold in seconds for slow query detection
        """
        self.slow_query_threshold = slow_query_threshold
        self.query_metrics = deque(maxlen=10000)  # Keep last 10k queries
        self.index_usage_stats = defaultdict(lambda: defaultdict(int))
        self.collection_stats = defaultdict(lambda: defaultdict(list))
        
        logger.info(f"QueryPerformanceMonitor initialized with {slow_query_threshold}s slow query threshold")
    
    def record_query(self, metrics: QueryPerformanceMetrics):
        """Record query performance metrics"""
        try:
            self.query_metrics.append(metrics)
            
            # Update index usage statistics
            if metrics.index_used:
                self.index_usage_stats[metrics.collection][metrics.index_used] += 1
            
            # Update collection statistics
            self.collection_stats[metrics.collection]['execution_times'].append(metrics.execution_time)
            self.collection_stats[metrics.collection]['documents_examined'].append(metrics.documents_examined)
            self.collection_stats[metrics.collection]['documents_returned'].append(metrics.documents_returned)
            
            # Log slow queries
            if metrics.execution_time > self.slow_query_threshold:
                logger.warning(f"Slow query detected: {metrics.query_type} on {metrics.collection} "
                              f"took {metrics.execution_time:.3f}s, examined {metrics.documents_examined} docs")
                
        except Exception as e:
            logger.error(f"Failed to record query metrics: {str(e)}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        try:
            if not self.query_metrics:
                return {
                    'total_queries': 0,
                    'message': 'No query metrics available'
                }
            
            # Calculate basic statistics
            execution_times = [m.execution_time for m in self.query_metrics]
            documents_examined = [m.documents_examined for m in self.query_metrics]
            documents_returned = [m.documents_returned for m in self.query_metrics]
            
            # Slow query analysis
            slow_queries = [m for m in self.query_metrics if m.execution_time > self.slow_query_threshold]
            
            # Collection performance breakdown
            collection_performance = {}
            for collection, stats in self.collection_stats.items():
                if stats['execution_times']:
                    collection_performance[collection] = {
                        'avg_execution_time': statistics.mean(stats['execution_times']),
                        'max_execution_time': max(stats['execution_times']),
                        'query_count': len(stats['execution_times']),
                        'avg_documents_examined': statistics.mean(stats['documents_examined']) if stats['documents_examined'] else 0,
                        'avg_documents_returned': statistics.mean(stats['documents_returned']) if stats['documents_returned'] else 0
                    }
            
            # Index usage analysis
            index_usage = {}
            for collection, indexes in self.index_usage_stats.items():
                index_usage[collection] = dict(indexes)
            
            summary = {
                'total_queries': len(self.query_metrics),
                'avg_execution_time': statistics.mean(execution_times),
                'max_execution_time': max(execution_times),
                'min_execution_time': min(execution_times),
                'slow_query_count': len(slow_queries),
                'slow_query_percentage': (len(slow_queries) / len(self.query_metrics)) * 100,
                'avg_documents_examined': statistics.mean(documents_examined) if documents_examined else 0,
                'avg_documents_returned': statistics.mean(documents_returned) if documents_returned else 0,
                'collection_performance': collection_performance,
                'index_usage_stats': index_usage,
                'timestamp': datetime.now().isoformat()
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate performance summary: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_optimization_recommendations(self) -> List[str]:
        """Generate performance optimization recommendations"""
        recommendations = []
        
        try:
            if not self.query_metrics:
                return ["No query data available for recommendations"]
            
            # Analyze slow queries
            slow_queries = [m for m in self.query_metrics if m.execution_time > self.slow_query_threshold]
            if slow_queries:
                slow_percentage = (len(slow_queries) / len(self.query_metrics)) * 100
                recommendations.append(
                    f"Consider optimizing {len(slow_queries)} slow queries ({slow_percentage:.1f}% of total)"
                )
            
            # Analyze index usage
            for collection, indexes in self.index_usage_stats.items():
                if not indexes:
                    recommendations.append(f"Collection '{collection}' may benefit from additional indexes")
                else:
                    # Find most and least used indexes
                    most_used = max(indexes.items(), key=lambda x: x[1])
                    least_used = min(indexes.items(), key=lambda x: x[1])
                    
                    if least_used[1] < 10:  # Less than 10 uses
                        recommendations.append(
                            f"Consider dropping unused index '{least_used[0]}' on '{collection}'"
                        )
            
            # Analyze query efficiency
            for collection, stats in self.collection_stats.items():
                if stats['execution_times'] and stats['documents_examined']:
                    avg_examined = statistics.mean(stats['documents_examined'])
                    avg_returned = statistics.mean(stats['documents_returned'])
                    
                    if avg_examined > 0 and avg_returned > 0:
                        efficiency_ratio = avg_returned / avg_examined
                        if efficiency_ratio < 0.1:  # Less than 10% efficiency
                            recommendations.append(
                                f"Poor query efficiency on '{collection}': "
                                f"examining {avg_examined:.0f} docs to return {avg_returned:.0f} docs"
                            )
            
            if not recommendations:
                recommendations.append("Query performance is within acceptable parameters")
                
        except Exception as e:
            logger.error(f"Failed to generate optimization recommendations: {str(e)}")
            recommendations.append(f"Error generating recommendations: {str(e)}")
        
        return recommendations


# Global performance monitor instance
performance_monitor = QueryPerformanceMonitor()


async def monitor_query_performance(collection_name: str, query_type: str, query_func):
    """
    Decorator/wrapper for monitoring query performance
    
    Args:
        collection_name: Name of the MongoDB collection
        query_type: Type/description of the query
        query_func: The async function to monitor
    
    Returns:
        Query result with performance tracking
    """
    try:
        start_time = time.time()
        
        # Execute the query
        result = await query_func()
        
        execution_time = time.time() - start_time
        
        # Create performance metrics (simplified - in production, these would come from MongoDB explain())
        metrics = QueryPerformanceMetrics(
            query_type=query_type,
            collection=collection_name,
            execution_time=execution_time,
            documents_examined=len(result) if isinstance(result, list) else 1,
            documents_returned=len(result) if isinstance(result, list) else 1,
            index_used="unknown",  # Would be determined from explain() output
            timestamp=datetime.now(),
            query_pattern=query_type,
            success=True
        )
        
        # Record metrics
        performance_monitor.record_query(metrics)
        
        return result
        
    except Exception as e:
        # Record failed query
        execution_time = time.time() - start_time
        metrics = QueryPerformanceMetrics(
            query_type=query_type,
            collection=collection_name,
            execution_time=execution_time,
            documents_examined=0,
            documents_returned=0,
            index_used="unknown",
            timestamp=datetime.now(),
            query_pattern=query_type,
            success=False,
            error_message=str(e)
        )
        
        performance_monitor.record_query(metrics)
        raise


# CLI interface for direct execution
async def main():
    """Main function for command-line execution of database optimization"""
    print("🔧 MongoDB Database Performance Optimization")
    print("=" * 60)
    
    # Create compound indexes
    print("📈 Creating compound indexes...")
    compound_result = await create_compound_indexes()
    
    if compound_result['success']:
        print(f"✅ Compound indexes created: {compound_result['compound_indexes_created']}")
        print(f"Collections processed: {compound_result['collections_processed']}")
    else:
        print("❌ Compound index creation failed!")
        for error in compound_result.get('errors', []):
            print(f"Error: {error}")
    
    print("\n" + "=" * 60)
    
    # Setup TTL indexes
    print("⏰ Setting up TTL indexes...")
    ttl_result = await setup_ttl_indexes()
    
    if ttl_result['success']:
        print(f"✅ TTL indexes created: {ttl_result['ttl_indexes_created']}")
        print("Data retention periods:")
        for collection, status in ttl_result.get('ttl_status', {}).items():
            if status.get('ttl_created'):
                print(f"  {collection}: {status['retention_days']:.0f} days")
    else:
        print("❌ TTL index setup failed!")
        for error in ttl_result.get('errors', []):
            print(f"Error: {error}")
    
    print("\n" + "=" * 60)
    
    # Create aggregation pipelines
    print("🔍 Creating aggregation pipelines...")
    pipeline_result = await create_aggregation_pipelines()
    
    if pipeline_result['success']:
        print(f"✅ Aggregation pipelines created: {pipeline_result['pipelines_created']}")
        for name, details in pipeline_result.get('pipeline_details', {}).items():
            if details.get('validated'):
                print(f"  {name}: {details['test_execution_time']}ms ({details['stage_count']} stages)")
    else:
        print("❌ Aggregation pipeline creation failed!")
        for error in pipeline_result.get('errors', []):
            print(f"Error: {error}")
    
    print("\n" + "=" * 60)
    
    # Optimize connection pool
    print("🔗 Optimizing connection pool...")
    pool_result = await optimize_connection_pool()
    
    if pool_result['success']:
        print("✅ Connection pool optimization completed!")
        for recommendation in pool_result.get('recommendations', []):
            print(f"  - {recommendation}")
    else:
        print("❌ Connection pool optimization failed!")
        for error in pool_result.get('errors', []):
            print(f"Error: {error}")
    
    print("\n" + "=" * 60)
    
    # Performance monitoring summary
    print("📊 Query Performance Monitor Status:")
    summary = performance_monitor.get_performance_summary()
    print(f"✅ Monitor initialized (tracking up to 10,000 queries)")
    print(f"Current queries tracked: {summary.get('total_queries', 0)}")
    
    print("\n🎉 Database optimization process completed!")


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())