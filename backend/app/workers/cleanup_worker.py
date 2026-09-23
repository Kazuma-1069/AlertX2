import asyncio
from app.core.logging import logger

async def cleanup_expired_sessions():
    """Worker for cleaning up old expired telemetry or unverified timers."""
    logger.info("Cleanup worker initialized.")
    while True:
        await asyncio.sleep(3600)
