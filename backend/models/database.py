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
        # Setup TTL Indexes for automatic deletion every 1 hour (3600 seconds)
        db.sessions.create_index("created_at", expireAfterSeconds=3600)
        db.messages.create_index("timestamp", expireAfterSeconds=3600)
        db.cached_responses.create_index("created_at", expireAfterSeconds=3600)
        db.rate_limits.create_index("timestamp", expireAfterSeconds=3600)
        
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
