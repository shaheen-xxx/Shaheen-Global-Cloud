"""Job endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.schemas import JobResponse, JobLogResponse
from app.database.models import User
from app.services.job_service import JobService
from app.dependencies import get_db, get_current_user
from typing import List

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get job details"""
    job = JobService.get_by_id(db=db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return job


@router.get("/{job_id}/logs", response_model=List[JobLogResponse])
async def get_job_logs(
    job_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get job logs"""
    job = JobService.get_by_id(db=db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return JobService.get_logs(db=db, job_id=job_id)
