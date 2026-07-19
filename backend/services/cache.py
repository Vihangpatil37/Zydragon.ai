import hashlib
import uuid
import logging
from datetime import datetime, timezone
from typing import Optional
from backend.models.database import get_db

logger = logging.getLogger(__name__)

class CacheService:
    @staticmethod
    def _get_hash(query: str) -> str:
        # Normalize: strip leading/trailing whitespace and convert to lowercase for exact match
        normalized = query.strip().lower()
        return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    def get_cached_response(self, query: str, model: str) -> Optional[str]:
        db = get_db()
        query_hash = self._get_hash(query)
        try:
            doc = db.cached_responses.find_one({"query_hash": query_hash, "model_used": model})
            if doc:
                logger.info(f"Cache hit for query hash {query_hash} using model {model}")
                return doc["response"]
            return None
        except Exception as e:
            logger.error(f"Error reading cache: {str(e)}")
            return None

    def cache_response(self, query: str, response: str, model: str):
        db = get_db()
        query_hash = self._get_hash(query)
        cache_id = str(uuid.uuid4())
        try:
            now = datetime.now(timezone.utc)
            db.cached_responses.update_one(
                {"query_hash": query_hash, "model_used": model},
                {"$set": {
                    "id": cache_id, 
                    "response": response, 
                    "created_at": now
                }},
                upsert=True
            )
            logger.info(f"Cached response for query hash {query_hash} using model {model}")
        except Exception as e:
            logger.error(f"Error writing to cache: {str(e)}")

cache_service = CacheService()
