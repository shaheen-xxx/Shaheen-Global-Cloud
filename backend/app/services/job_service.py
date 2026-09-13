"""Job service"""

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime
from app.database.models import ProvisioningJob, JobStatus, JobLog
from app.core.logging import get_logger
import json

logger = get_logger(__name__)


class JobService:
    """Service for provisioning job operations"""

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        server_id: int,
        job_type: str,
        configuration: Dict[str, Any],
    ) -> ProvisioningJob:
        """Create a new provisioning job"""
        job = ProvisioningJob(
            user_id=user_id,
            server_id=server_id,
            job_type=job_type,
            configuration=json.dumps(configuration),
            status=JobStatus.PENDING,
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        logger.info("job_created", job_id=job.id, server_id=server_id)
        return job

    @staticmethod
    def get_by_id(db: Session, job_id: str) -> Optional[ProvisioningJob]:
        """Get job by ID"""
        return db.query(ProvisioningJob).filter(ProvisioningJob.id == job_id).first()

    @staticmethod
    def update_status(
        db: Session, job_id: str, status: JobStatus
    ) -> Optional[ProvisioningJob]:
        """Update job status"""
        job = db.query(ProvisioningJob).filter(ProvisioningJob.id == job_id).first()
        if job:
            job.status = status
            if status == JobStatus.RUNNING and not job.started_at:
                job.started_at = datetime.utcnow()
            if status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                job.finished_at = datetime.utcnow()
            db.commit()
            db.refresh(job)
            logger.info("job_status_updated", job_id=job_id, status=status)
        return job

    @staticmethod
    def set_error(
        db: Session, job_id: str, error_message: str
    ) -> Optional[ProvisioningJob]:
        """Set job error message"""
        job = db.query(ProvisioningJob).filter(ProvisioningJob.id == job_id).first()
        if job:
            job.error_message = error_message
            db.commit()
            db.refresh(job)
            logger.error("job_error_set", job_id=job_id, error=error_message)
        return job

    @staticmethod
    def add_log(db: Session, job_id: str, level: str, message: str) -> JobLog:
        """Add a log entry to a job"""
        log = JobLog(job_id=job_id, level=level, message=message)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_logs(db: Session, job_id: str) -> list:
        """Get all logs for a job"""
        return (
            db.query(JobLog)
            .filter(JobLog.job_id == job_id)
            .order_by(JobLog.timestamp)
            .all()
        )
