import asyncio
import json
import logging
import uuid

import websockets

from src.agent.workforce_agent import chat_with_tools

logger = logging.getLogger(__name__)


async def handle_connection(websocket):
    """Handle a single WebSocket connection."""
    logger.info("New WebSocket connection from %s", websocket.remote_address)

    try:
        async for raw_message in websocket:
            try:
                data = json.loads(raw_message)
                session_id = data.get("session_id", str(uuid.uuid4()))
                user_id = data.get("user_id", "default_user")
                message = data.get("message", "")

                if not message:
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "error",
                                "content": "Message field is required",
                            }
                        )
                    )
                    continue

                logger.info(
                    "WS message | session=%s | user=%s | message_length=%d",
                    session_id,
                    user_id,
                    len(message),
                )

                # Process through the agent
                result = await chat_with_tools(
                    session_id=session_id,
                    user_id=user_id,
                    message=message,
                )

                # Send tool call notifications
                for tool_call in result["tool_calls"]:
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "tool_call",
                                "content": tool_call,
                                "session_id": session_id,
                            }
                        )
                    )

                # Stream the response in chunks
                response_text = result["response"]
                chunk_size = 80
                for i in range(0, len(response_text), chunk_size):
                    chunk = response_text[i : i + chunk_size]
                    await websocket.send(
                        json.dumps(
                            {
                                "type": "chunk",
                                "content": chunk,
                                "session_id": session_id,
                            }
                        )
                    )
                    # Small delay to simulate streaming
                    await asyncio.sleep(0.02)

                # Send done signal
                await websocket.send(
                    json.dumps(
                        {
                            "type": "done",
                            "session_id": session_id,
                            "tool_calls_count": len(result["tool_calls"]),
                        }
                    )
                )

            except json.JSONDecodeError:
                await websocket.send(
                    json.dumps(
                        {
                            "type": "error",
                            "content": "Invalid JSON message",
                        }
                    )
                )
            except Exception as e:
                logger.error("WS processing error: %s", str(e), exc_info=True)
                await websocket.send(
                    json.dumps(
                        {
                            "type": "error",
                            "content": f"Processing error: {str(e)}",
                        }
                    )
                )

    except websockets.exceptions.ConnectionClosed:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error("WebSocket error: %s", str(e), exc_info=True)


async def start_ws_server(port: int):
    """Start the WebSocket server.

    Args:
        port: Port number to listen on.
    """
    logger.info("Starting WebSocket server on port %d", port)
    async with websockets.serve(handle_connection, "0.0.0.0", port):
        logger.info("WebSocket server running on ws://0.0.0.0:%d", port)
        await asyncio.Future()  # Run forever
