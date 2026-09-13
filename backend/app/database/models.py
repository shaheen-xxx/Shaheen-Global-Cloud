"""Database models"""

from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base
import enum
import uuid


class ServerStatus(str, enum.Enum):
    """Server status enumeration"""
    PENDING = "PENDING"
    PROVISIONING = "PROVISIONING"
    BOOTSTRAPPING = "BOOTSTRAPPING"
    READY = "READY"
    FAILED = "FAILED"
    DESTROYING = "DESTROYING"
    DESTROYED = "DESTROYED"


class JobStatus(str, enum.Enum):
    """Job status enumeration"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    servers = relationship("Server", back_populates="owner")
    jobs = relationship("ProvisioningJob", back_populates="user")


class Server(Base):
    """Server model"""
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    provider = Column(String)  # "hetzner", "aws", "digitalocean", "mock"
    region = Column(String)
    size = Column(String)
    image = Column(String)
    status = Column(Enum(ServerStatus), default=ServerStatus.PENDING)
    ipv4 = Column(String, nullable=True)
    ipv6 = Column(String, nullable=True)
    provider_server_id = Column(String, nullable=True)  # Provider's resource ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="servers")
    job = relationship("ProvisioningJob", back_populates="server", uselist=False)


class ProvisioningJob(Base):
    """Provisioning job model"""
    __tablename__ = "provisioning_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    server_id = Column(Integer, ForeignKey("servers.id"))
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    job_type = Column(String)  # "create", "destroy", "update"
    configuration = Column(Text)  # JSON serialized config
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="jobs")
    server = relationship("Server", back_populates="job")
    logs = relationship("JobLog", back_populates="job", cascade="all, delete-orphan")


class JobLog(Base):
    """Job execution logs"""
    __tablename__ = "job_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("provisioning_jobs.id"))
    level = Column(String)  # DEBUG, INFO, WARNING, ERROR
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    job = relationship("ProvisioningJob", back_populates="logs")
