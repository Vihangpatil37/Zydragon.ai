import pymongo
import logging
from backend.utils.config import settings

import os

_client = None

def get_db():
    global _client
    if _client is None:
        _client = pymongo.MongoClient(settings.MONGODB_URL)
    # Use configurable database name, default to "zydrakon"
    db_name = os.getenv("MONGO_DB_NAME", "zydrakon")
    return _client[db_name]

def init_db():
    db = get_db()
    try:
        ttl_seconds = 1800
        
        # Safely drop old TTL indexes if their expiration time is different
        ttl_configs = [
            ("sessions", "created_at"),
            ("messages", "timestamp"),
            ("cached_responses", "created_at"),
            ("rate_limits", "timestamp")
        ]
        for col_name, field_name in ttl_configs:
            try:
                info = db[col_name].index_information()
                idx_name = f"{field_name}_1"
                if idx_name in info:
                    if info[idx_name].get("expireAfterSeconds") != ttl_seconds:
                        db[col_name].drop_index(idx_name)
                        logging.info(f"Dropped old TTL index {idx_name} on {col_name}")
            except Exception as e:
                logging.warning(f"Failed to check/drop TTL index for {col_name}: {str(e)}")

        # Setup TTL Indexes for automatic deletion every 30 minutes (1800 seconds)
        db.sessions.create_index("created_at", expireAfterSeconds=ttl_seconds)
        db.messages.create_index("timestamp", expireAfterSeconds=ttl_seconds)
        db.cached_responses.create_index("created_at", expireAfterSeconds=ttl_seconds)
        db.rate_limits.create_index("timestamp", expireAfterSeconds=ttl_seconds)
        
        # Normal Indexes for querying
        db.messages.create_index("session_id")
        db.cached_responses.create_index(
            [("query_hash", pymongo.ASCENDING), ("model_used", pymongo.ASCENDING)],
            unique=True
        )
        db.rate_limits.create_index([("identifier", pymongo.ASCENDING), ("timestamp", pymongo.ASCENDING)])
        
        logging.info("MongoDB database initialized with TTL indexes.")
    except Exception as e:
        logging.error(f"Error initializing MongoDB: {str(e)}")
