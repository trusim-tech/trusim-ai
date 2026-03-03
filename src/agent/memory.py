from typing import Dict, List

MAX_MESSAGES_PER_SESSION = 50


class SessionMemory:
    """Simple in-memory session store with sliding window."""

    def __init__(self) -> None:
        self._sessions: Dict[str, List[dict]] = {}

    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add a message to the session history."""
        if session_id not in self._sessions:
            self._sessions[session_id] = []

        self._sessions[session_id].append({"role": role, "content": content})

        # Sliding window: keep only the last MAX_MESSAGES_PER_SESSION messages
        if len(self._sessions[session_id]) > MAX_MESSAGES_PER_SESSION:
            self._sessions[session_id] = self._sessions[session_id][
                -MAX_MESSAGES_PER_SESSION:
            ]

    def get_history(self, session_id: str) -> List[dict]:
        """Get the full conversation history for a session."""
        return self._sessions.get(session_id, [])

    def clear_session(self, session_id: str) -> None:
        """Clear all messages for a session."""
        if session_id in self._sessions:
            del self._sessions[session_id]

    def has_session(self, session_id: str) -> bool:
        """Check if a session exists."""
        return session_id in self._sessions

    def list_sessions(self) -> List[str]:
        """List all active session IDs."""
        return list(self._sessions.keys())


# Global session memory instance
memory = SessionMemory()
