from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import asyncio

from agents.orchestrator.supervisor import QuotationOrchestrator
from shared.models.quotation import create_initial_state

router = APIRouter()

# Initialize orchestrator
orchestrator = QuotationOrchestrator()


# Pydantic models for request/response
class QuotationCreate(BaseModel):
    """Model for creating a new quotation."""
    company_name: str = Field(..., description="Company requesting quotation")
    prepared_by: str = Field(..., description="Person preparing the quotation")
    client_name: Optional[str] = Field(None, description="Client name")
    client_contact: Optional[str] = Field(None, description="Client contact info")
    project_name: Optional[str] = Field(None, description="Project name")
    validity_days: int = Field(30, description="Quotation validity in days")


class QuotationResponse(BaseModel):
    """Model for quotation response."""
    id: str
    quote_number: str
    company_name: str
    prepared_by: str
    status: str
    created_at: datetime
    updated_at: datetime
    client_name: Optional[str] = None
    client_contact: Optional[str] = None
    project_name: Optional[str] = None


class QuotationUpdate(BaseModel):
    """Model for updating quotation."""
    status: Optional[str] = None
    client_name: Optional[str] = None
    client_contact: Optional[str] = None
    project_name: Optional[str] = None


# Temporary in-memory storage (replace with database)
quotations_db = {}


@router.post("/", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation(quotation: QuotationCreate) -> QuotationResponse:
    """Create a new quotation."""
    # Generate ID and quote number
    quotation_id = f"quot_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    quote_number = f"QT-{datetime.utcnow().strftime('%Y%m%d')}-0001"
    
    # Create quotation record
    new_quotation = {
        "id": quotation_id,
        "quote_number": quote_number,
        "company_name": quotation.company_name,
        "prepared_by": quotation.prepared_by,
        "status": "draft",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "client_name": quotation.client_name,
        "client_contact": quotation.client_contact,
        "project_name": quotation.project_name,
        "validity_days": quotation.validity_days
    }
    
    # Store in database
    quotations_db[quotation_id] = new_quotation
    
    return QuotationResponse(**new_quotation)


@router.get("/", response_model=List[QuotationResponse])
async def list_quotations(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None
) -> List[QuotationResponse]:
    """List all quotations with optional filtering."""
    all_quotations = list(quotations_db.values())
    
    # Filter by status if provided
    if status:
        all_quotations = [q for q in all_quotations if q["status"] == status]
    
    # Apply pagination
    return [QuotationResponse(**q) for q in all_quotations[skip:skip + limit]]


@router.get("/{quotation_id}", response_model=QuotationResponse)
async def get_quotation(quotation_id: str) -> QuotationResponse:
    """Get a specific quotation by ID."""
    if quotation_id not in quotations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quotation {quotation_id} not found"
        )
    
    return QuotationResponse(**quotations_db[quotation_id])


@router.patch("/{quotation_id}", response_model=QuotationResponse)
async def update_quotation(
    quotation_id: str,
    update: QuotationUpdate
) -> QuotationResponse:
    """Update a quotation."""
    if quotation_id not in quotations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quotation {quotation_id} not found"
        )
    
    # Update fields
    quotation = quotations_db[quotation_id]
    update_data = update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        quotation[field] = value
    
    quotation["updated_at"] = datetime.utcnow()
    
    return QuotationResponse(**quotation)


@router.delete("/{quotation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quotation(quotation_id: str):
    """Delete a quotation."""
    if quotation_id not in quotations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quotation {quotation_id} not found"
        )
    
    del quotations_db[quotation_id]


@router.post("/{quotation_id}/generate")
async def generate_quotation(
    quotation_id: str,
    background_tasks: BackgroundTasks
):
    """Trigger quotation generation using agents."""
    if quotation_id not in quotations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quotation {quotation_id} not found"
        )
    
    quotation = quotations_db[quotation_id]
    
    # Create initial state for orchestrator
    initial_state = create_initial_state(quotation_id, quotation["prepared_by"])
    
    # Update state with quotation data
    initial_state["client_info"]["name"] = quotation.get("client_name", "")
    initial_state["client_info"]["email"] = quotation.get("client_contact", "")
    initial_state["project_info"]["name"] = quotation.get("project_name", "")
    initial_state["company_info"]["name"] = quotation["company_name"]
    
    # Run orchestrator in background
    background_tasks.add_task(
        run_orchestrator_async,
        quotation_id,
        initial_state
    )
    
    # Update status
    quotation["status"] = "processing"
    quotation["updated_at"] = datetime.utcnow()
    
    return {
        "message": "Quotation generation started",
        "quotation_id": quotation_id,
        "status": "processing"
    }


async def run_orchestrator_async(quotation_id: str, initial_state: Dict[str, Any]):
    """Run orchestrator asynchronously and update quotation status."""
    try:
        # Generate quotation using orchestrator
        final_state = await orchestrator.generate_quotation(initial_state)
        
        # Update quotation in database
        if quotation_id in quotations_db:
            quotation = quotations_db[quotation_id]
            quotation["status"] = final_state["metadata"]["status"]
            quotation["updated_at"] = datetime.utcnow()
            
            # Store generated data
            quotation["generated_data"] = {
                "quote_number": final_state.get("quote_number"),
                "header": final_state.get("header"),
                "company_info": dict(final_state.get("company_info", {})),
                "footer": final_state.get("footer"),
                "terms_and_conditions": final_state.get("terms_and_conditions"),
                "agent_logs": final_state.get("agent_logs", []),
                "errors": final_state.get("errors", [])
            }
            
    except Exception as e:
        # Update status on error
        if quotation_id in quotations_db:
            quotation = quotations_db[quotation_id]
            quotation["status"] = "failed"
            quotation["updated_at"] = datetime.utcnow()
            quotation["error"] = str(e)


@router.get("/{quotation_id}/status")
async def get_generation_status(quotation_id: str):
    """Get the status of quotation generation."""
    if quotation_id not in quotations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quotation {quotation_id} not found"
        )
    
    quotation = quotations_db[quotation_id]
    
    response = {
        "quotation_id": quotation_id,
        "status": quotation["status"],
        "updated_at": quotation["updated_at"]
    }
    
    # Include generated data if available
    if "generated_data" in quotation:
        response["generated_data"] = quotation["generated_data"]
    
    # Include error if failed
    if "error" in quotation:
        response["error"] = quotation["error"]
    
    return response


@router.get("/{quotation_id}/document")
async def get_quotation_document(quotation_id: str):
    """Get the generated quotation document."""
    if quotation_id not in quotations_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quotation {quotation_id} not found"
        )
    
    quotation = quotations_db[quotation_id]
    
    if quotation["status"] != "generated":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Quotation is not ready. Current status: {quotation['status']}"
        )
    
    if "generated_data" not in quotation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Generated data not found"
        )
    
    # Format the quotation document
    generated = quotation["generated_data"]
    
    document = {
        "quotation_id": quotation_id,
        "document": {
            "header": generated.get("header", {}),
            "company_info": generated.get("company_info", {}),
            "client_info": {
                "name": quotation.get("client_name", ""),
                "contact": quotation.get("client_contact", ""),
                "project": quotation.get("project_name", "")
            },
            "line_items": [],  # TODO: Add when LineItemsAgent is ready
            "pricing_summary": {},  # TODO: Add when PricingAgent is ready
            "terms_and_conditions": generated.get("terms_and_conditions", ""),
            "footer": generated.get("footer", {})
        },
        "metadata": {
            "generated_at": quotation["updated_at"],
            "prepared_by": quotation["prepared_by"],
            "quote_number": generated.get("quote_number", "")
        }
    }
    
    return document