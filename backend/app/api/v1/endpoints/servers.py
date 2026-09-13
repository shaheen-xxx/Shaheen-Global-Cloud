"""Server endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.schemas import (
    CreateServerRequest,
    ServerResponse,
    ServerListResponse,
    ProvisioningJobResponse,
)
from app.database.models import User, ServerStatus, JobStatus
from app.services.server_service import ServerService
from app.services.job_service import JobService
from app.services.provider_service import ProviderService
from app.queue.job_queue import job_queue
from app.dependencies import get_db, get_current_user
from app.core.logging import get_logger
import json

logger = get_logger(__name__)
router = APIRouter(prefix="/servers", tags=["servers"])


@router.post("/", response_model=ProvisioningJobResponse, status_code=202)
async def create_server(
    request: CreateServerRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new server"""
    # Validate provider
    if not ProviderService.is_supported(request.provider):
        raise HTTPException(
            status_code=400,
            detail=f"Provider '{request.provider}' is not supported",
        )

    # Create server record
    server = ServerService.create(
        db=db,
        user_id=user.id,
        name=request.name,
        provider=request.provider,
        region=request.region,
        size=request.size,
        image=request.image,
    )

    # Create provisioning job
    config = {
        "name": request.name,
        "provider": request.provider,
        "region": request.region,
        "size": request.size,
        "image": request.image,
    }

    job = JobService.create(
        db=db,
        user_id=user.id,
        server_id=server.id,
        job_type="create",
        configuration=config,
    )

    # Enqueue job
    job_data = {
        "job_id": job.id,
        "server_id": server.id,
        "user_id": user.id,
        "configuration": config,
        "status": JobStatus.PENDING,
    }
    job_queue.enqueue(job.id, job_data)

    logger.info(
        "server_creation_requested",
        server_id=server.id,
        job_id=job.id,
        user_id=user.id,
    )

    return ProvisioningJobResponse(
        job_id=job.id,
        server_id=server.id,
        status=JobStatus.PENDING,
    )


@router.get("/", response_model=ServerListResponse)
async def list_servers(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List all servers for current user"""
    servers = ServerService.list_by_user(db=db, user_id=user.id)
    return ServerListResponse(
        total=len(servers),
        servers=servers,
    )


@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(
    server_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get server details"""
    server = ServerService.get_by_id(db=db, server_id=server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    if server.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return server


@router.post("/{server_id}/destroy", status_code=202)
async def destroy_server(
    server_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Destroy a server"""
    server = ServerService.get_by_id(db=db, server_id=server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    if server.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Update server status
    ServerService.update_status(db=db, server_id=server_id, status=ServerStatus.DESTROYING)

    # Create destroy job
    config = {
        "server_id": server.provider_server_id or str(server.id),
        "provider": server.provider,
    }

    job = JobService.create(
        db=db,
        user_id=user.id,
        server_id=server_id,
        job_type="destroy",
        configuration=config,
    )

    # Enqueue job
    job_data = {
        "job_id": job.id,
        "server_id": server_id,
        "user_id": user.id,
        "configuration": config,
        "status": JobStatus.PENDING,
    }
    job_queue.enqueue(job.id, job_data)

    logger.info(
        "server_destroy_requested",
        server_id=server_id,
        job_id=job.id,
    )

    return {"job_id": job.id, "status": "destroying"}
