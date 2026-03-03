import asyncio
import logging

import uvicorn

from src.api.server import app
from src.api.ws import start_ws_server
from src.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    """Start both FastAPI and WebSocket servers concurrently."""
    logger.info(
        "Starting TruSim AI | FastAPI port=%d | WS port=%d | model=%s",
        settings.fastapi_port,
        settings.ws_port,
        settings.gemini_model,
    )

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=settings.fastapi_port,
        log_level="info",
    )
    server = uvicorn.Server(config)

    await asyncio.gather(
        server.serve(),
        start_ws_server(settings.ws_port),
    )


if __name__ == "__main__":
    asyncio.run(main())
