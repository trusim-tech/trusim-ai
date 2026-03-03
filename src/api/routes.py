import logging
import uuid
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.agent.memory import memory
from src.agent.workforce_agent import chat, chat_with_tools

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    user_id: Optional[str] = "default_user"
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    tool_calls: list = []


@router.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "trusim-ai", "version": "0.1.0"}


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Send a message to the AI agent and get a response."""
    session_id = request.session_id or str(uuid.uuid4())
    user_id = request.user_id or "default_user"

    try:
        result = await chat_with_tools(
            session_id=session_id,
            user_id=user_id,
            message=request.message,
        )
        return ChatResponse(
            session_id=session_id,
            response=result["response"],
            tool_calls=result["tool_calls"],
        )
    except Exception as e:
        logger.error("Chat error: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}",
        )


@router.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """Send a message and receive a Server-Sent Events stream."""
    session_id = request.session_id or str(uuid.uuid4())
    user_id = request.user_id or "default_user"

    async def event_stream():
        try:
            result = await chat_with_tools(
                session_id=session_id,
                user_id=user_id,
                message=request.message,
            )

            # Send tool calls as events
            for tool_call in result["tool_calls"]:
                import json

                yield f"data: {json.dumps({'type': 'tool_call', 'content': tool_call})}\n\n"

            # Send response in chunks to simulate streaming
            response_text = result["response"]
            chunk_size = 50
            for i in range(0, len(response_text), chunk_size):
                chunk = response_text[i : i + chunk_size]
                import json

                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"

            import json

            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"

        except Exception as e:
            import json

            logger.error("Stream error: %s", str(e), exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get conversation history for a session."""
    history = memory.get_history(session_id)
    if not history and not memory.has_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "session_id": session_id,
        "messages": history,
        "message_count": len(history),
    }


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Clear a session's conversation history."""
    if not memory.has_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    memory.clear_session(session_id)
    return {"status": "ok", "message": f"Session {session_id} cleared"}
