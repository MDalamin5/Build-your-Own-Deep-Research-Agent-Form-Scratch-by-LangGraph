from pydantic import BaseModel
from typing import List, Optional, Any

class ResearchRequest(BaseModel):
    """
    Defines the schema for an incoming conversational request.
    The 'thread_id' is optional. If not provided, a new research thread is created.
    """
    user_id: str
    thread_id: Optional[str] = None
    content: str

class ResearchResponse(BaseModel):
    """
    Defines the schema for a response from the research agent.
    It returns the current 'thread_id' so the client can continue the conversation.
    'is_final' indicates if the agent has produced the final report.
    """
    thread_id: str
    response_messages: List[dict]
    is_final: bool = False

class CheckpointerThreadRequest(BaseModel):
    """
    Defines the schema for requesting the state of a specific thread.
    """
    thread_id: str

class CheckpointerThreadResponse(BaseModel):
    """
    Defines the schema for the response containing a thread's state.
    """
    thread_id: str
    state: Any