from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router
from src.config import settings

app = FastAPI(
    title="TruSim AI",
    version="0.1.0",
    description="TruSim AI Agent - Workforce verification powered by Google ADK and Gemini",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Type", "X-Accel-Buffering"],
)

app.include_router(router)
