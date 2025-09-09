import uuid
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, BaseMessage
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse

# Assuming 'research_agent_full.py' contains the compiled graph as 'deep_researcher_builder'
from research_agent_full import deep_researcher_builder
from schemas import (
    ResearchRequest, 
    ResearchResponse, 
    CheckpointerThreadRequest, 
    CheckpointerThreadResponse
)

# In-memory checkpointer to store the state of ongoing research conversations
checkpointer = InMemorySaver()

# Compile the main research agent graph with the checkpointer
full_agent = deep_researcher_builder.compile(checkpointer=checkpointer)


app = FastAPI(
    title="Deep Research API EndPoint.",
    version="2.0.0",
    description="A conversational API for multi-step deep research with persistent memory."
)

@app.get("/")
async def home():
    """
    Root endpoint for the API.
    """
    return {"messages": "Welcome to Deep Research ERA."}

@app.get("/health")
async def health():
    """
    Health check endpoint.
    """
    return {"status": "I'm alive."}

@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    """
    Handles a conversational turn for a deep research task.

    - If 'thread_id' is not provided, it starts a new conversation.
    - If 'thread_id' is provided, it continues the existing conversation.
    - The agent will first engage in a Q&A to clarify the research scope.
    - Once scoped, it proceeds with deep research and generates a final report.
    """
    # Use the provided thread_id or create a new one for a new conversation
    thread_id = request.thread_id if request.thread_id else str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Prepare the user's message for the agent
    user_message = HumanMessage(content=request.content)
    input_messages = {"messages": [user_message]}

    try:
        # Asynchronously invoke the agent. LangGraph and the checkpointer will handle
        # loading the previous state for the given thread_id.
        result = await full_agent.ainvoke(input_messages, config=config)

        # Determine if the agent has finished and produced the final report
        is_final_report = "final_report" in result and result.get("final_report")

        # Serialize the agent's response messages for a clean JSON output
        response_messages_serialized = []
        if 'messages' in result:
            for msg in result['messages']:
                if isinstance(msg, BaseMessage):
                    response_messages_serialized.append({"type": msg.type, "content": msg.content})
                elif isinstance(msg, str):
                    response_messages_serialized.append({"type": "ai", "content": msg})

        return ResearchResponse(
            thread_id=thread_id,
            response_messages=response_messages_serialized,
            is_final=bool(is_final_report)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.post("/checkpointer_thread", response_model=CheckpointerThreadResponse)
async def get_checkpointer_thread(request: CheckpointerThreadRequest):
    """
    Retrieves the complete state of a given research thread for debugging or monitoring.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    try:
        # get_state is a high-level method to safely retrieve the last saved state
        state_snapshot = full_agent.get_state(config)
        
        if not state_snapshot:
            raise HTTPException(status_code=404, detail="Thread not found or state is empty.")

        # The state is stored in the 'values' attribute of the snapshot
        return CheckpointerThreadResponse(
            thread_id=request.thread_id,
            state=state_snapshot.values
        )
    except Exception:
        raise HTTPException(status_code=404, detail="Thread not found or error retrieving state.")