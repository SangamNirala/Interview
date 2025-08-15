"""
MongoDB Collections Initialization for Fingerprinting System
Task 2.1: Comprehensive database setup for advanced fingerprinting capabilities

This module provides functionality to initialize all required MongoDB collections
for the fingerprinting system with proper indexes and validation rules.
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import CollectionInvalid, OperationFailure
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseSetupManager:
    """
    Manages comprehensive database initialization for fingerprinting system
    """
    
    def __init__(self):
        """Initialize database connection parameters"""
        load_dotenv()
        self.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        self.db_name = os.environ.get('DB_NAME', 'test_database')
        self.client = None
        self.db = None
    
    async def connect(self):
        """Establish async connection to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(self.mongo_url)
            self.db = self.client[self.db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB at {self.mongo_url}")
            logger.info(f"Using database: {self.db_name}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            return False
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

async def initialize_fingerprinting_collections():
    """
    Initialize all 6 required MongoDB collections for fingerprinting system
    
    Collections created:
    1. device_fingerprints - Hardware and device characteristic data
    2. browser_fingerprints - Browser-specific fingerprinting data  
    3. session_integrity_profiles - Session continuity and authenticity data
    4. fingerprint_violations - Security violations and anomaly records
    5. device_reputation_scores - Device trust and reputation metrics
    6. fingerprint_analytics - Analytics and reporting data
    
    Returns:
        Dict: Status report of collection creation and index setup
    """
    
    setup_manager = DatabaseSetupManager()
    
    # Connect to MongoDB
    if not await setup_manager.connect():
        return {
            'success': False,
            'error': 'Failed to connect to MongoDB',
            'timestamp': datetime.now().isoformat()
        }
    
    collections_config = {
        'device_fingerprints': {
            'indexes': [
                {'keys': [('device_id', 1)], 'unique': True},
                {'keys': [('session_id', 1)]},
                {'keys': [('signature_hash', 1)]},
                {'keys': [('created_at', -1)]},
                {'keys': [('device_id', 1), ('created_at', -1)]}
            ],
            'validation': {
                'required_fields': ['device_id', 'hardware_signature', 'confidence_score']
            }
        },
        
        'browser_fingerprints': {
            'indexes': [
                {'keys': [('browser_id', 1)], 'unique': True},
                {'keys': [('session_id', 1)]},
                {'keys': [('user_agent_hash', 1)]},
                {'keys': [('created_at', -1)]},
                {'keys': [('fingerprint_entropy', -1)]}
            ],
            'validation': {
                'required_fields': ['browser_id', 'user_agent_analysis', 'fingerprint_entropy']
            }
        },
        
        'session_integrity_profiles': {
            'indexes': [
                {'keys': [('session_id', 1)], 'unique': True},
                {'keys': [('device_id', 1)]},
                {'keys': [('integrity_score', -1)]},
                {'keys': [('created_at', -1)]},
                {'keys': [('risk_level', 1)]}
            ],
            'validation': {
                'required_fields': ['session_id', 'device_consistency_score', 'authenticity_confidence']
            }
        },
        
        'fingerprint_violations': {
            'indexes': [
                {'keys': [('session_id', 1)]},
                {'keys': [('device_id', 1)]},
                {'keys': [('violation_type', 1)]},
                {'keys': [('severity', -1)]},
                {'keys': [('created_at', -1)]}
            ],
            'validation': {
                'required_fields': ['session_id', 'violation_type', 'severity', 'detected_at']
            }
        },
        
        'device_reputation_scores': {
            'indexes': [
                {'keys': [('device_id', 1)], 'unique': True},
                {'keys': [('reputation_score', -1)]},
                {'keys': [('risk_category', 1)]},
                {'keys': [('last_updated', -1)]},
                {'keys': [('device_id', 1), ('last_updated', -1)]}
            ],
            'validation': {
                'required_fields': ['device_id', 'reputation_score', 'risk_category']
            }
        },
        
        'fingerprint_analytics': {
            'indexes': [
                {'keys': [('analytics_type', 1)]},
                {'keys': [('date_range', 1)]},
                {'keys': [('created_at', -1)]},
                {'keys': [('device_count', -1)]},
                {'keys': [('analytics_type', 1), ('created_at', -1)]}
            ],
            'validation': {
                'required_fields': ['analytics_type', 'date_range', 'device_count']
            }
        }
    }
    
    setup_results = {
        'success': True,
        'collections_created': 0,
        'indexes_created': 0,
        'collections_status': {},
        'errors': [],
        'timestamp': datetime.now().isoformat(),
        'database': setup_manager.db_name,
        'mongo_url': setup_manager.mongo_url
    }
    
    try:
        # Get existing collections for verification
        existing_collections = await setup_manager.db.list_collection_names()
        logger.info(f"Existing collections: {existing_collections}")
        
        # Process each collection configuration
        for collection_name, config in collections_config.items():
            collection_result = {
                'exists': False,
                'created': False,
                'indexes_created': 0,
                'validation_set': False,
                'errors': []
            }
            
            try:
                # Check if collection exists
                if collection_name in existing_collections:
                    collection_result['exists'] = True
                    logger.info(f"Collection '{collection_name}' already exists")
                else:
                    # Create collection
                    await setup_manager.db.create_collection(collection_name)
                    collection_result['created'] = True
                    setup_results['collections_created'] += 1
                    logger.info(f"Created collection: {collection_name}")
                
                # Get collection reference
                collection = setup_manager.db[collection_name]
                
                # Create indexes
                for index_config in config['indexes']:
                    try:
                        keys = index_config['keys']
                        options = {k: v for k, v in index_config.items() if k != 'keys'}
                        
                        # Create index
                        await collection.create_index(keys, **options)
                        collection_result['indexes_created'] += 1
                        setup_results['indexes_created'] += 1
                        
                        logger.info(f"Created index on {collection_name}: {keys} with options: {options}")
                        
                    except OperationFailure as e:
                        if "already exists" in str(e):
                            logger.info(f"Index already exists on {collection_name}: {keys}")
                            collection_result['indexes_created'] += 1
                            setup_results['indexes_created'] += 1
                        else:
                            error_msg = f"Failed to create index on {collection_name}: {str(e)}"
                            logger.error(error_msg)
                            collection_result['errors'].append(error_msg)
                    except Exception as e:
                        error_msg = f"Unexpected error creating index on {collection_name}: {str(e)}"
                        logger.error(error_msg)
                        collection_result['errors'].append(error_msg)
                
                # Set validation schema (MongoDB schema validation)
                validation_config = config.get('validation', {})
                if validation_config.get('required_fields'):
                    try:
                        # Create JSON Schema validation
                        schema = {
                            "bsonType": "object",
                            "required": validation_config['required_fields'],
                            "properties": {}
                        }
                        
                        # Set validation for the collection
                        await setup_manager.db.command({
                            "collMod": collection_name,
                            "validator": {"$jsonSchema": schema},
                            "validationLevel": "moderate",
                            "validationAction": "warn"
                        })
                        
                        collection_result['validation_set'] = True
                        logger.info(f"Set validation schema for {collection_name}: {validation_config['required_fields']}")
                        
                    except Exception as e:
                        error_msg = f"Failed to set validation for {collection_name}: {str(e)}"
                        logger.warning(error_msg)
                        collection_result['errors'].append(error_msg)
                
                # Store collection status
                setup_results['collections_status'][collection_name] = collection_result
                
            except Exception as e:
                error_msg = f"Failed to setup collection {collection_name}: {str(e)}"
                logger.error(error_msg)
                collection_result['errors'].append(error_msg)
                setup_results['collections_status'][collection_name] = collection_result
                setup_results['errors'].append(error_msg)
        
        # Verify final collection state
        final_collections = await setup_manager.db.list_collection_names()
        setup_results['final_collections'] = final_collections
        
        # Success summary
        logger.info(f"Database initialization completed:")
        logger.info(f"  - Collections processed: {len(collections_config)}")
        logger.info(f"  - Collections created: {setup_results['collections_created']}")
        logger.info(f"  - Indexes created: {setup_results['indexes_created']}")
        logger.info(f"  - Final collections in database: {len(final_collections)}")
        
        # Determine overall success
        if setup_results['errors']:
            setup_results['success'] = False
            logger.warning(f"Setup completed with {len(setup_results['errors'])} errors")
        else:
            logger.info("Database initialization completed successfully!")
            
    except Exception as e:
        error_msg = f"Critical error during database initialization: {str(e)}"
        logger.error(error_msg)
        setup_results['success'] = False
        setup_results['errors'].append(error_msg)
        
    finally:
        # Close connection
        await setup_manager.close()
    
    return setup_results


async def verify_collections_integrity():
    """
    Verify that all fingerprinting collections exist and have proper indexes
    
    Returns:
        Dict: Verification report with collection status and index information
    """
    
    setup_manager = DatabaseSetupManager()
    
    if not await setup_manager.connect():
        return {
            'success': False,
            'error': 'Failed to connect to MongoDB',
            'timestamp': datetime.now().isoformat()
        }
    
    verification_results = {
        'success': True,
        'collections_verified': 0,
        'collections_missing': [],
        'index_status': {},
        'errors': [],
        'timestamp': datetime.now().isoformat(),
        'database': setup_manager.db_name
    }
    
    expected_collections = [
        'device_fingerprints',
        'browser_fingerprints', 
        'session_integrity_profiles',
        'fingerprint_violations',
        'device_reputation_scores',
        'fingerprint_analytics'
    ]
    
    try:
        # Get current collections
        existing_collections = await setup_manager.db.list_collection_names()
        
        # Verify each expected collection
        for collection_name in expected_collections:
            if collection_name in existing_collections:
                verification_results['collections_verified'] += 1
                
                # Check indexes for the collection
                collection = setup_manager.db[collection_name]
                indexes = await collection.list_indexes().to_list(length=None)
                
                verification_results['index_status'][collection_name] = {
                    'index_count': len(indexes),
                    'indexes': [idx['name'] for idx in indexes]
                }
                
                logger.info(f"Verified collection: {collection_name} with {len(indexes)} indexes")
                
            else:
                verification_results['collections_missing'].append(collection_name)
                logger.warning(f"Missing collection: {collection_name}")
        
        # Overall verification status
        if verification_results['collections_missing']:
            verification_results['success'] = False
            logger.error(f"Verification failed - missing collections: {verification_results['collections_missing']}")
        else:
            logger.info(f"All {len(expected_collections)} fingerprinting collections verified successfully")
            
    except Exception as e:
        error_msg = f"Error during collection verification: {str(e)}"
        logger.error(error_msg)
        verification_results['success'] = False
        verification_results['errors'].append(error_msg)
        
    finally:
        await setup_manager.close()
    
    return verification_results


async def get_collections_stats():
    """
    Get statistics for all fingerprinting collections
    
    Returns:
        Dict: Collection statistics including document counts and sizes
    """
    
    setup_manager = DatabaseSetupManager()
    
    if not await setup_manager.connect():
        return {
            'success': False,
            'error': 'Failed to connect to MongoDB',
            'timestamp': datetime.now().isoformat()
        }
    
    stats_results = {
        'success': True,
        'database': setup_manager.db_name,
        'collection_stats': {},
        'total_documents': 0,
        'errors': [],
        'timestamp': datetime.now().isoformat()
    }
    
    fingerprinting_collections = [
        'device_fingerprints',
        'browser_fingerprints', 
        'session_integrity_profiles',
        'fingerprint_violations',
        'device_reputation_scores',
        'fingerprint_analytics'
    ]
    
    try:
        for collection_name in fingerprinting_collections:
            try:
                collection = setup_manager.db[collection_name]
                
                # Get document count
                doc_count = await collection.count_documents({})
                
                # Get collection stats
                try:
                    collection_stats = await setup_manager.db.command("collStats", collection_name)
                    size_info = {
                        'document_count': doc_count,
                        'storage_size': collection_stats.get('storageSize', 0),
                        'index_size': collection_stats.get('totalIndexSize', 0),
                        'average_obj_size': collection_stats.get('avgObjSize', 0)
                    }
                except Exception:
                    # Fallback if collStats not available
                    size_info = {
                        'document_count': doc_count,
                        'storage_size': 'N/A',
                        'index_size': 'N/A', 
                        'average_obj_size': 'N/A'
                    }
                
                stats_results['collection_stats'][collection_name] = size_info
                stats_results['total_documents'] += doc_count
                
                logger.info(f"Stats for {collection_name}: {doc_count} documents")
                
            except Exception as e:
                error_msg = f"Error getting stats for {collection_name}: {str(e)}"
                logger.warning(error_msg)
                stats_results['errors'].append(error_msg)
                stats_results['collection_stats'][collection_name] = {'error': error_msg}
        
        logger.info(f"Total documents across fingerprinting collections: {stats_results['total_documents']}")
        
    except Exception as e:
        error_msg = f"Critical error getting collection stats: {str(e)}"
        logger.error(error_msg)
        stats_results['success'] = False
        stats_results['errors'].append(error_msg)
        
    finally:
        await setup_manager.close()
    
    return stats_results


# CLI interface for direct execution
async def main():
    """Main function for command-line execution"""
    print("🔧 Initializing MongoDB Fingerprinting Collections...")
    print("=" * 60)
    
    # Initialize collections
    result = await initialize_fingerprinting_collections()
    
    if result['success']:
        print("✅ Database initialization completed successfully!")
        print(f"Collections created: {result['collections_created']}")
        print(f"Indexes created: {result['indexes_created']}")
        print(f"Database: {result['database']}")
    else:
        print("❌ Database initialization failed!")
        for error in result['errors']:
            print(f"Error: {error}")
    
    print("\n" + "=" * 60)
    
    # Verify collections
    print("🔍 Verifying collection integrity...")
    verification = await verify_collections_integrity()
    
    if verification['success']:
        print("✅ All collections verified successfully!")
        print(f"Collections verified: {verification['collections_verified']}")
    else:
        print("❌ Collection verification issues found!")
        if verification['collections_missing']:
            print(f"Missing collections: {verification['collections_missing']}")
    
    print("\n" + "=" * 60)
    
    # Get stats
    print("📊 Getting collection statistics...")
    stats = await get_collections_stats()
    
    if stats['success']:
        print("✅ Statistics collected successfully!")
        print(f"Total documents: {stats['total_documents']}")
        print("\nCollection breakdown:")
        for coll_name, coll_stats in stats['collection_stats'].items():
            if 'error' not in coll_stats:
                print(f"  {coll_name}: {coll_stats['document_count']} documents")
    else:
        print("❌ Failed to collect statistics!")
    
    print("\n🎉 Database setup process completed!")


if __name__ == "__main__":
    # Run the main function
    asyncio.run(main())