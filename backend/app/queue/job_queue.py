"""Job queue implementation using Redis"""

import json
import redis
from typing import Dict, Any, Optional
from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class JobQueue:
    """Redis-based job queue"""

    def __init__(self, redis_url: str = settings.redis_url):
        self.redis_client = redis.from_url(redis_url)
        self.queue_key = "provisioning:queue"
        self.job_key_prefix = "job:"

    def enqueue(self, job_id: str, job_data: Dict[str, Any]) -> bool:
        """Enqueue a provisioning job"""
        try:
            # Store job data
            self.redis_client.set(
                f"{self.job_key_prefix}{job_id}",
                json.dumps(job_data),
                ex=86400,  # 24 hour expiry
            )
            # Add to queue
            self.redis_client.rpush(self.queue_key, job_id)
            logger.info("job_enqueued", job_id=job_id)
            return True
        except Exception as e:
            logger.error("job_enqueue_failed", job_id=job_id, error=str(e))
            return False

    def dequeue(self) -> Optional[str]:
        """Dequeue a job from the queue"""
        try:
            job_id = self.redis_client.lpop(self.queue_key)
            return job_id.decode() if job_id else None
        except Exception as e:
            logger.error("job_dequeue_failed", error=str(e))
            return None

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job data"""
        try:
            data = self.redis_client.get(f"{self.job_key_prefix}{job_id}")
            return json.loads(data) if data else None
        except Exception as e:
            logger.error("job_get_failed", job_id=job_id, error=str(e))
            return None

    def set_job_status(self, job_id: str, status: str) -> bool:
        """Update job status"""
        try:
            job_data = self.get_job(job_id)
            if job_data:
                job_data["status"] = status
                self.redis_client.set(
                    f"{self.job_key_prefix}{job_id}",
                    json.dumps(job_data),
                    ex=86400,
                )
                logger.info("job_status_updated", job_id=job_id, status=status)
                return True
            return False
        except Exception as e:
            logger.error("job_status_update_failed", job_id=job_id, error=str(e))
            return False

    def queue_length(self) -> int:
        """Get queue length"""
        return self.redis_client.llen(self.queue_key)


# Global job queue instance
job_queue = JobQueue()
