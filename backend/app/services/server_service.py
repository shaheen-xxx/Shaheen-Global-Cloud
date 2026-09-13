"""Server service"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.database.models import Server, ServerStatus
from app.core.logging import get_logger

logger = get_logger(__name__)


class ServerService:
    """Service for server operations"""

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        name: str,
        provider: str,
        region: str,
        size: str,
        image: str,
    ) -> Server:
        """Create a new server record"""
        server = Server(
            user_id=user_id,
            name=name,
            provider=provider,
            region=region,
            size=size,
            image=image,
            status=ServerStatus.PENDING,
        )
        db.add(server)
        db.commit()
        db.refresh(server)
        logger.info("server_created", server_id=server.id, user_id=user_id)
        return server

    @staticmethod
    def get_by_id(db: Session, server_id: int) -> Optional[Server]:
        """Get server by ID"""
        return db.query(Server).filter(Server.id == server_id).first()

    @staticmethod
    def list_by_user(db: Session, user_id: int) -> List[Server]:
        """List servers for a user"""
        return db.query(Server).filter(Server.user_id == user_id).order_by(desc(Server.created_at)).all()

    @staticmethod
    def update_status(
        db: Session, server_id: int, status: ServerStatus
    ) -> Optional[Server]:
        """Update server status"""
        server = db.query(Server).filter(Server.id == server_id).first()
        if server:
            server.status = status
            db.commit()
            db.refresh(server)
            logger.info("server_status_updated", server_id=server_id, status=status)
        return server

    @staticmethod
    def update_ip_addresses(
        db: Session, server_id: int, ipv4: str, ipv6: str
    ) -> Optional[Server]:
        """Update server IP addresses"""
        server = db.query(Server).filter(Server.id == server_id).first()
        if server:
            server.ipv4 = ipv4
            server.ipv6 = ipv6
            db.commit()
            db.refresh(server)
            logger.info(
                "server_ips_updated",
                server_id=server_id,
                ipv4=ipv4,
                ipv6=ipv6,
            )
        return server

    @staticmethod
    def set_provider_id(
        db: Session, server_id: int, provider_id: str
    ) -> Optional[Server]:
        """Set provider resource ID"""
        server = db.query(Server).filter(Server.id == server_id).first()
        if server:
            server.provider_server_id = provider_id
            db.commit()
            db.refresh(server)
        return server
