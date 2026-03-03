import asyncio
import logging
from typing import Optional

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from src.agent.memory import memory
from src.agent.prompts import SYSTEM_PROMPT
from src.config import settings
from src.tools.shift_tools import get_current_shifts, get_shift_summary, get_worker_shifts
from src.tools.absence_tools import get_absences, get_absence_patterns, get_bradford_scores
from src.tools.worker_tools import get_worker_status, get_team_overview, get_unverified_workers
from src.tools.anomaly_tools import get_anomalies, get_fraud_alerts
from src.tools.report_tools import generate_daily_report, generate_payroll_report
from src.tools.prediction_tools import predict_absences, get_risk_scores
from src.tools.nokia_tools import check_sim_swap, check_device_status, verify_location

logger = logging.getLogger(__name__)

APP_NAME = "trusim"

# All tool functions to register with the agent
ALL_TOOLS = [
    # Shift tools
    get_current_shifts,
    get_shift_summary,
    get_worker_shifts,
    # Absence tools
    get_absences,
    get_absence_patterns,
    get_bradford_scores,
    # Worker tools
    get_worker_status,
    get_team_overview,
    get_unverified_workers,
    # Anomaly tools
    get_anomalies,
    get_fraud_alerts,
    # Report tools
    generate_daily_report,
    generate_payroll_report,
    # Prediction tools
    predict_absences,
    get_risk_scores,
    # Nokia Network as Code tools
    check_sim_swap,
    check_device_status,
    verify_location,
]

# Create the ADK agent
agent = Agent(
    name="trusim_assistant",
    model=settings.gemini_model,
    instruction=SYSTEM_PROMPT,
    tools=ALL_TOOLS,
)

# Session service and runner
session_service = InMemorySessionService()
runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=session_service,
)


async def chat(session_id: str, user_id: str, message: str) -> str:
    """Send a message to the agent and return the response.

    Args:
        session_id: Unique session identifier for conversation continuity.
        user_id: Unique user identifier.
        message: The user's message text.

    Returns:
        The agent's response as a string.
    """
    # Store user message in our memory
    memory.add_message(session_id, "user", message)

    # Get or create the ADK session
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )

    # Build the user content
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)],
    )

    # Run the agent and collect the final response
    response_text = ""
    tool_calls = []

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=user_content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
        # Track tool calls for transparency
        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_calls.append(
                        {
                            "name": part.function_call.name,
                            "args": dict(part.function_call.args) if part.function_call.args else {},
                        }
                    )

    if not response_text:
        response_text = "No he podido procesar tu solicitud. Por favor, intenta de nuevo."

    # Store assistant response in our memory
    memory.add_message(session_id, "assistant", response_text)

    logger.info(
        "Chat completed | session=%s | user=%s | tools_used=%d | response_length=%d",
        session_id,
        user_id,
        len(tool_calls),
        len(response_text),
    )

    return response_text


async def chat_with_tools(session_id: str, user_id: str, message: str) -> dict:
    """Send a message and return both the response and tool call information.

    Args:
        session_id: Unique session identifier.
        user_id: Unique user identifier.
        message: The user's message text.

    Returns:
        Dict with 'response' and 'tool_calls' keys.
    """
    memory.add_message(session_id, "user", message)

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )

    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)],
    )

    response_text = ""
    tool_calls = []

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=user_content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text

        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "function_call") and part.function_call:
                    tool_calls.append(
                        {
                            "name": part.function_call.name,
                            "args": dict(part.function_call.args) if part.function_call.args else {},
                        }
                    )

    if not response_text:
        response_text = "No he podido procesar tu solicitud. Por favor, intenta de nuevo."

    memory.add_message(session_id, "assistant", response_text)

    return {
        "response": response_text,
        "tool_calls": tool_calls,
    }
