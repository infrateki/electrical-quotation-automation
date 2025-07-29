from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()


class AgentStatus(BaseModel):
    """Model for agent status."""
    name: str
    type: str
    status: str
    last_active: datetime
    tasks_completed: int
    current_task: Optional[str] = None


class AgentExecuteRequest(BaseModel):
    """Model for agent execution request."""
    agent_name: str
    input_data: Dict[str, Any]


# Mock agent registry
AGENT_REGISTRY = {
    "HeaderAgent": {
        "type": "simple",
        "status": "ready",
        "tasks_completed": 0,
        "last_active": datetime.utcnow()
    },
    "FooterAgent": {
        "type": "simple",
        "status": "not_implemented",
        "tasks_completed": 0,
        "last_active": None
    },
    "CompanyInfoAgent": {
        "type": "simple",
        "status": "not_implemented",
        "tasks_completed": 0,
        "last_active": None
    },
    "ProjectInfoAgent": {
        "type": "workflow",
        "status": "not_implemented",
        "tasks_completed": 0,
        "last_active": None
    },
    "LineItemsAgent": {
        "type": "advanced",
        "status": "not_implemented",
        "tasks_completed": 0,
        "last_active": None
    }
}


@router.get("/", response_model=List[AgentStatus])
async def list_agents() -> List[AgentStatus]:
    """List all available agents and their status."""
    agents = []
    for name, info in AGENT_REGISTRY.items():
        agents.append(AgentStatus(
            name=name,
            type=info["type"],
            status=info["status"],
            last_active=info["last_active"] or datetime.utcnow(),
            tasks_completed=info["tasks_completed"],
            current_task=info.get("current_task")
        ))
    return agents


@router.get("/{agent_name}", response_model=AgentStatus)
async def get_agent_status(agent_name: str) -> AgentStatus:
    """Get status of a specific agent."""
    if agent_name not in AGENT_REGISTRY:
        raise HTTPException(
            status_code=404,
            detail=f"Agent {agent_name} not found"
        )
    
    info = AGENT_REGISTRY[agent_name]
    return AgentStatus(
        name=agent_name,
        type=info["type"],
        status=info["status"],
        last_active=info["last_active"] or datetime.utcnow(),
        tasks_completed=info["tasks_completed"],
        current_task=info.get("current_task")
    )


@router.post("/execute")
async def execute_agent(request: AgentExecuteRequest):
    """Execute a specific agent with input data."""
    if request.agent_name not in AGENT_REGISTRY:
        raise HTTPException(
            status_code=404,
            detail=f"Agent {request.agent_name} not found"
        )
    
    agent_info = AGENT_REGISTRY[request.agent_name]
    
    if agent_info["status"] != "ready":
        raise HTTPException(
            status_code=400,
            detail=f"Agent {request.agent_name} is not ready. Status: {agent_info['status']}"
        )
    
    # TODO: Actually execute the agent
    # For now, return mock response
    
    # Update agent info
    agent_info["tasks_completed"] += 1
    agent_info["last_active"] = datetime.utcnow()
    
    return {
        "agent": request.agent_name,
        "status": "completed",
        "execution_time": 0.5,
        "result": {
            "message": f"Agent {request.agent_name} executed successfully",
            "output": {}
        }
    }


@router.get("/types")
async def get_agent_types():
    """Get information about agent types."""
    return {
        "types": {
            "simple": {
                "description": "Template-based agents for basic tasks",
                "examples": ["HeaderAgent", "FooterAgent", "CompanyInfoAgent"]
            },
            "workflow": {
                "description": "Logic-based agents with moderate intelligence",
                "examples": ["ProjectInfoAgent", "ContactsAgent", "ApprovalAgent"]
            },
            "advanced": {
                "description": "AI-powered agents for complex analysis",
                "examples": ["LineItemsAgent", "PricingAgent", "ExecutiveSummaryAgent"]
            },
            "orchestrator": {
                "description": "Supervisor agent that coordinates all other agents",
                "examples": ["QuotationOrchestrator"]
            }
        }
    }