"""Provisioning job worker"""

import asyncio
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.base import SessionLocal
from app.database.models import JobStatus, ServerStatus
from app.core.logging import setup_logging, get_logger
from app.queue.job_queue import job_queue
from app.services.job_service import JobService
from app.services.server_service import ServerService
from app.services.provider_service import ProviderService
from app.services.dagger_service import DaggerService

logger = get_logger(__name__)


class ProvisioningWorker:
    """Worker for processing provisioning jobs"""

    def __init__(self, poll_interval: int = 5):
        self.poll_interval = poll_interval
        self.running = False

    async def process_job(self, job_id: str, job_data: dict) -> bool:
        """Process a single provisioning job"""
        db: Session = SessionLocal()
        try:
            logger.info("job_processing_started", job_id=job_id)

            # Update job status to RUNNING
            job = JobService.get_by_id(db, job_id)
            if not job:
                logger.error("job_not_found", job_id=job_id)
                return False

            JobService.update_status(db, job_id, JobStatus.RUNNING)
            server_id = job.server_id

            # Update server status to PROVISIONING
            ServerService.update_status(
                db, server_id, ServerStatus.PROVISIONING
            )

            # Add log entry
            JobService.add_log(
                db, job_id, "INFO", "Job processing started"
            )

            # Get configuration
            config = json.loads(job.configuration)
            provider_name = config.get("provider", "mock")

            logger.info(
                "job_configuration_loaded",
                job_id=job_id,
                provider=provider_name,
            )

            # Get provider
            provider = ProviderService.get_provider(provider_name)
            if not provider:
                error_msg = f"Provider {provider_name} not found"
                logger.error("provider_not_found", provider=provider_name)
                JobService.add_log(db, job_id, "ERROR", error_msg)
                JobService.update_status(db, job_id, JobStatus.FAILED)
                JobService.set_error(db, job_id, error_msg)
                ServerService.update_status(db, server_id, ServerStatus.FAILED)
                return False

            # Run provisioning via Dagger
            dagger_result = await DaggerService.run_provisioning(config)

            if not dagger_result.get("success"):
                error_msg = dagger_result.get("error", "Provisioning failed")
                logger.error(
                    "provisioning_failed",
                    job_id=job_id,
                    error=error_msg,
                )
                JobService.add_log(db, job_id, "ERROR", error_msg)
                JobService.update_status(db, job_id, JobStatus.FAILED)
                JobService.set_error(db, job_id, error_msg)
                ServerService.update_status(db, server_id, ServerStatus.FAILED)
                return False

            # Update server with provisioning results
            ipv4 = dagger_result.get("ipv4")
            ipv6 = dagger_result.get("ipv6")
            provider_id = dagger_result.get("server_id")

            if ipv4:
                ServerService.update_ip_addresses(db, server_id, ipv4, ipv6 or "")
            if provider_id:
                ServerService.set_provider_id(db, server_id, provider_id)

            # Update server status to BOOTSTRAPPING
            ServerService.update_status(
                db, server_id, ServerStatus.BOOTSTRAPPING
            )
            JobService.add_log(
                db, job_id, "INFO", f"Server created with IPv4: {ipv4}"
            )

            # Simulate cloud-init completion (in production, this would poll)
            await asyncio.sleep(2)

            # Update server status to READY
            ServerService.update_status(
                db, server_id, ServerStatus.READY
            )
            JobService.add_log(
                db, job_id, "INFO", "Server is ready"
            )

            # Mark job as completed
            JobService.update_status(db, job_id, JobStatus.COMPLETED)

            logger.info(
                "job_processing_completed",
                job_id=job_id,
                server_id=server_id,
            )
            return True

        except Exception as e:
            logger.error(
                "job_processing_error",
                job_id=job_id,
                error=str(e),
                exc_info=True,
            )
            try:
                JobService.update_status(db, job_id, JobStatus.FAILED)
                JobService.set_error(db, job_id, str(e))
                if job_data and "server_id" in job_data:
                    ServerService.update_status(
                        db,
                        job_data["server_id"],
                        ServerStatus.FAILED,
                    )
            except Exception as inner_e:
                logger.error(
                    "job_error_update_failed",
                    job_id=job_id,
                    error=str(inner_e),
                )
            return False
        finally:
            db.close()

    async def run(self):
        """Run the worker loop"""
        self.running = True
        logger.info("worker_started")

        while self.running:
            try:
                # Try to dequeue a job
                job_id = job_queue.dequeue()

                if job_id:
                    job_data = job_queue.get_job(job_id)
                    if job_data:
                        await self.process_job(job_id, job_data)
                    else:
                        logger.warning(
                            "job_data_not_found",
                            job_id=job_id,
                        )
                else:
                    # Queue is empty, sleep before checking again
                    await asyncio.sleep(self.poll_interval)

            except Exception as e:
                logger.error(
                    "worker_error",
                    error=str(e),
                    exc_info=True,
                )
                await asyncio.sleep(self.poll_interval)

    def stop(self):
        """Stop the worker"""
        self.running = False
        logger.info("worker_stop_requested")


async def main():
    """Main entry point"""
    setup_logging()
    worker = ProvisioningWorker()
    try:
        await worker.run()
    except KeyboardInterrupt:
        logger.info("worker_interrupted")
        worker.stop()


if __name__ == "__main__":
    asyncio.run(main())
