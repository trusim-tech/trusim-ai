"""TruSim AI Agent entry point.

Delegates to src.main which starts the FastAPI server on port 8090
and the WebSocket server on port 8091.
"""

import asyncio

from src.main import main

if __name__ == "__main__":
    asyncio.run(main())
