import logging
from datetime import datetime, timedelta, timezone
from typing import Tuple, Dict, Any
from backend.models.database import get_db
from backend.utils.config import settings

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        self.rpm_limit = settings.RATE_LIMIT_RPM
        self.daily_limit = settings.RATE_LIMIT_DAILY

    def check_rate_limit(self, identifier: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Verifies if requests from the identifier (e.g. session or IP) are within rate limits.
        Returns: (is_limited, reason_code, details)
        """
        db = get_db()
        try:
            # We don't need to manually DELETE old records because TTL index handles it every hour!
            now = datetime.now(timezone.utc)
            one_min_ago = now - timedelta(minutes=1)
            one_day_ago = now - timedelta(days=1)

            # 1. Check RPM (Requests Per Minute)
            rpm_count = db.rate_limits.count_documents({
                "identifier": identifier, 
                "timestamp": {"$gt": one_min_ago}
            })

            # 2. Check Daily limit
            daily_count = db.rate_limits.count_documents({
                "identifier": identifier,
                "timestamp": {"$gt": one_day_ago}
            })

            if rpm_count >= self.rpm_limit:
                cursor_oldest = db.rate_limits.find({
                    "identifier": identifier,
                    "timestamp": {"$gt": one_min_ago}
                }).sort("timestamp", 1).limit(1)
                
                retry_after_sec = 60
                oldest_docs = list(cursor_oldest)
                if oldest_docs:
                    oldest_time = oldest_docs[0]["timestamp"]
                    if oldest_time.tzinfo is None:
                        oldest_time = oldest_time.replace(tzinfo=timezone.utc)
                    elapsed = (now - oldest_time).total_seconds()
                    retry_after_sec = max(1, int(60 - elapsed))
                
                return True, "RPM_LIMITED", {"retry_after_sec": retry_after_sec, "rpm_limit": self.rpm_limit, "daily_limit": self.daily_limit}

            if daily_count >= self.daily_limit:
                cursor_oldest_day = db.rate_limits.find({
                    "identifier": identifier,
                    "timestamp": {"$gt": one_day_ago}
                }).sort("timestamp", 1).limit(1)
                
                retry_after_hours = 24
                oldest_docs_day = list(cursor_oldest_day)
                if oldest_docs_day:
                    oldest_time_day = oldest_docs_day[0]["timestamp"]
                    if oldest_time_day.tzinfo is None:
                        oldest_time_day = oldest_time_day.replace(tzinfo=timezone.utc)
                    elapsed = (now - oldest_time_day).total_seconds()
                    retry_after_hours = max(1, int((86400 - elapsed) / 3600))

                return True, "DAILY_LIMITED", {"retry_after_hours": retry_after_hours, "rpm_limit": self.rpm_limit, "daily_limit": self.daily_limit}

            return False, "", {"rpm_count": rpm_count, "daily_count": daily_count}
        except Exception as e:
            logger.error(f"Error checking rate limits: {str(e)}")
            # Fallback to allowing if rate limits fail, to prevent system denial of service
            return False, "", {}

    def record_request(self, identifier: str):
        """Logs a request event into the database to update the rate limits count."""
        db = get_db()
        try:
            db.rate_limits.insert_one({
                "identifier": identifier, 
                "timestamp": datetime.now(timezone.utc)
            })
        except Exception as e:
            logger.error(f"Error recording request to rate limits: {str(e)}")

    def get_remaining_limits(self, identifier: str) -> Dict[str, int]:
        """Returns details on current usage and remaining requests."""
        db = get_db()
        try:
            now = datetime.now(timezone.utc)
            one_min_ago = now - timedelta(minutes=1)
            one_day_ago = now - timedelta(days=1)
            
            rpm_count = db.rate_limits.count_documents({
                "identifier": identifier, 
                "timestamp": {"$gt": one_min_ago}
            })
            daily_count = db.rate_limits.count_documents({
                "identifier": identifier,
                "timestamp": {"$gt": one_day_ago}
            })

            return {
                "rpm_limit": self.rpm_limit,
                "rpm_remaining": max(0, self.rpm_limit - rpm_count),
                "daily_limit": self.daily_limit,
                "daily_remaining": max(0, self.daily_limit - daily_count)
            }
        except Exception as e:
            logger.error(f"Error checking remaining limits: {str(e)}")
            return {
                "rpm_limit": self.rpm_limit,
                "rpm_remaining": self.rpm_limit,
                "daily_limit": self.daily_limit,
                "daily_remaining": self.daily_limit
            }

rate_limiter = RateLimiter()
