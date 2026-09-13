"""API v1 schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ServerStatus(str, Enum):
    """Server status"""
    PENDING = "PENDING"
    PROVISIONING = "PROVISIONING"
    BOOTSTRAPPING = "BOOTSTRAPPING"
    READY = "READY"
    FAILED = "FAILED"
    DESTROYING = "DESTROYING"
    DESTROYED = "DESTROYED"


class JobStatus(str, Enum):
    """Job status"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class CreateServerRequest(BaseModel):
    """Create server request schema"""
    name: str = Field(..., min_length=1, max_length=255)
    provider: str = Field(..., min_length=1, max_length=50)
    region: str = Field(..., min_length=1, max_length=100)
    size: str = Field(..., min_length=1, max_length=100)
    image: str = Field(..., min_length=1, max_length=100)

    class Config:
        example = {
            "name": "ubuntu-01",
            "provider": "mock",
            "region": "fsn1",
            "size": "cx22",
            "image": "ubuntu-24.04"
        }


class ServerResponse(BaseModel):
    """Server response schema"""
    id: int
    name: str
    provider: str
    region: str
    size: str
    image: str
    status: ServerStatus
    ipv4: Optional[str] = None
    ipv6: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobResponse(BaseModel):
    """Job response schema"""
    id: str
    server_id: int
    status: JobStatus
    job_type: str
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProvisioningJobResponse(BaseModel):
    """Provisioning job creation response"""
    job_id: str
    server_id: int
    status: JobStatus


class JobLogResponse(BaseModel):
    """Job log response schema"""
    id: int
    level: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ServerListResponse(BaseModel):
    """Server list response"""
    total: int
    servers: List[ServerResponse]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    environment: str
