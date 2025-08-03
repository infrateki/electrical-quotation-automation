"""
Quotation State Models for Multi-Agent System

This module defines the data models and state management structures
used throughout the quotation automation system. These models ensure
type safety and consistent data flow between agents.

Author: ProQuote Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any, TypedDict
from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, field_validator, ConfigDict
import uuid


# ===================================================================
# ENUMS AND CONSTANTS
# ===================================================================

class QuotationStatus(str, Enum):
    """Status of a quotation throughout its lifecycle"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    SENT = "sent"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class AgentStatus(str, Enum):
    """Status of individual agent execution"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class LineItemCategory(str, Enum):
    """Categories for line items"""
    ESSENTIAL_SYSTEMS = "essential_systems"
    NORMAL_POWER = "normal_power"
    SPECIALIZED_EQUIPMENT = "specialized_equipment"
    BACKUP_POWER = "backup_power"
    LIGHTING = "lighting"
    CABLE_TRAY = "cable_tray"
    CONDUIT = "conduit"
    LABOR = "labor"
    PERMITS = "permits"
    OTHER = "other"


class BuildingType(str, Enum):
    """Types of buildings for electrical requirements"""
    HOSPITAL = "hospital"
    CLINIC = "clinic"
    DATA_CENTER = "data_center"
    OFFICE = "office"
    INDUSTRIAL = "industrial"
    RESIDENTIAL = "residential"
    MIXED_USE = "mixed_use"


class ComplianceStandard(str, Enum):
    """Electrical compliance standards"""
    NEC_517 = "NEC_517"  # Healthcare facilities
    NEC_645 = "NEC_645"  # Data centers
    NEC_700 = "NEC_700"  # Emergency systems
    NEC_701 = "NEC_701"  # Legally required standby
    NEC_702 = "NEC_702"  # Optional standby
    NFPA_99 = "NFPA_99"  # Healthcare facilities
    NFPA_70 = "NFPA_70"  # National Electrical Code
    LOCAL = "local"      # Local building codes


# ===================================================================
# BASE MODELS
# ===================================================================

class Address(BaseModel):
    """Address model for companies and project locations"""
    street_1: str
    street_2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    
    model_config = ConfigDict(from_attributes=True)


class Contact(BaseModel):
    """Contact person information"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str
    last_name: str
    title: str
    email: str
    phone: str
    mobile: Optional[str] = None
    is_primary: bool = False
    
    model_config = ConfigDict(from_attributes=True)
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Company(BaseModel):
    """Company information model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    legal_name: Optional[str] = None
    address: Address
    phone: str
    website: Optional[str] = None
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    contacts: List[Contact] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)
    
    def get_primary_contact(self) -> Optional[Contact]:
        """Get primary contact or first contact if no primary"""
        for contact in self.contacts:
            if contact.is_primary:
                return contact
        return self.contacts[0] if self.contacts else None


# ===================================================================
# PROJECT MODELS
# ===================================================================

class ProjectSpecifications(BaseModel):
    """Detailed project specifications"""
    total_square_feet: int
    building_type: BuildingType
    number_of_floors: int
    special_areas: Dict[str, int] = Field(default_factory=dict)  # e.g., {"operating_rooms": 4}
    compliance_requirements: List[ComplianceStandard]
    electrical_load_estimate_kw: Optional[float] = None
    required_backup_power_kw: Optional[float] = None
    special_requirements: List[str] = Field(default_factory=list)
    
    model_config = ConfigDict(from_attributes=True)


class ProjectInfo(BaseModel):
    """Project information extracted by Project Info Agent"""
    project_name: str
    project_number: Optional[str] = None
    location: Address
    specifications: ProjectSpecifications
    start_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    bid_date: Optional[datetime] = None
    project_manager: Optional[str] = None
    architect: Optional[str] = None
    general_contractor: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


# ===================================================================
# LINE ITEM MODELS
# ===================================================================

class LineItem(BaseModel):
    """Individual line item in quotation"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_number: str
    category: LineItemCategory
    description: str
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    quantity: float
    unit: str
    unit_price: Decimal
    extended_price: Optional[Decimal] = None
    lead_time_days: Optional[int] = None
    compliance_codes: List[str] = Field(default_factory=list)
    notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('extended_price', mode='before')
    def calculate_extended_price(cls, v, values):
        if v is None and 'quantity' in values and 'unit_price' in values:
            return Decimal(str(values['quantity'])) * values['unit_price']
        return v


class LineItemGroup(BaseModel):
    """Group of related line items"""
    category: LineItemCategory
    title: str
    items: List[LineItem]
    subtotal: Optional[Decimal] = None
    notes: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    @field_validator('subtotal', mode='before')
    def calculate_subtotal(cls, v, values):
        if v is None and 'items' in values:
            return sum(item.extended_price or 0 for item in values['items'])
        return v


# ===================================================================
# PRICING MODELS
# ===================================================================

class PricingSummary(BaseModel):
    """Pricing summary with breakdown"""
    material_subtotal: Decimal
    labor_subtotal: Decimal
    equipment_subtotal: Decimal
    permits_subtotal: Decimal
    
    subtotal: Optional[Decimal] = None
    volume_discount_percentage: Decimal = Decimal("0")
    volume_discount_amount: Optional[Decimal] = None
    
    net_price: Optional[Decimal] = None
    markup_percentage: Decimal
    markup_amount: Optional[Decimal] = None
    
    freight_cost: Decimal
    tax_rate: Decimal = Decimal("0.0825")  # Default 8.25%
    tax_amount: Optional[Decimal] = None
    
    grand_total: Optional[Decimal] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    def calculate_totals(self):
        """Calculate all derived totals"""
        # Calculate subtotal
        self.subtotal = (
            self.material_subtotal + 
            self.labor_subtotal + 
            self.equipment_subtotal + 
            self.permits_subtotal
        )
        
        # Calculate discount
        self.volume_discount_amount = self.subtotal * (self.volume_discount_percentage / 100)
        
        # Calculate net price
        self.net_price = self.subtotal - self.volume_discount_amount
        
        # Calculate markup
        self.markup_amount = self.net_price * (self.markup_percentage / 100)
        
        # Calculate tax
        taxable_amount = self.net_price + self.markup_amount
        self.tax_amount = taxable_amount * self.tax_rate
        
        # Calculate grand total
        self.grand_total = taxable_amount + self.tax_amount + self.freight_cost


# ===================================================================
# EXECUTIVE SUMMARY MODEL
# ===================================================================

class ExecutiveSummary(BaseModel):
    """Executive summary for quotation"""
    project_understanding: str
    scope_of_work: List[str]
    key_deliverables: List[str]
    total_project_value: Decimal
    estimated_timeline_days: int
    compliance_standards: List[ComplianceStandard]
    value_propositions: List[str]
    assumptions: List[str]
    exclusions: List[str]
    
    model_config = ConfigDict(from_attributes=True)


# ===================================================================
# AGENT EXECUTION MODELS
# ===================================================================

class AgentResult(BaseModel):
    """Result from individual agent execution"""
    agent_name: str
    status: AgentStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    execution_time_seconds: Optional[float] = None
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = None
    retry_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)
    
    def mark_completed(self, data: Optional[Dict[str, Any]] = None):
        """Mark agent execution as completed"""
        self.status = AgentStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.execution_time_seconds = (self.completed_at - self.started_at).total_seconds()
        if data:
            self.data = data
    
    def mark_failed(self, error_message: str, error_details: Optional[Dict] = None):
        """Mark agent execution as failed"""
        self.status = AgentStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.execution_time_seconds = (self.completed_at - self.started_at).total_seconds()
        self.error_message = error_message
        self.error_details = error_details or {}


# ===================================================================
# MAIN QUOTATION STATE
# ===================================================================

class QuotationState(BaseModel):
    """
    Main state object that flows through the multi-agent system.
    This is the core data structure that LangGraph uses for state management.
    """
    # Metadata
    quote_id: str = Field(default_factory=lambda: f"Q-{uuid.uuid4().hex[:8].upper()}")
    quote_number: Optional[str] = None  # Generated by Header Agent
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: QuotationStatus = QuotationStatus.DRAFT
    
    # Input data
    project_input: Dict[str, Any] = Field(default_factory=dict)
    user_context: Dict[str, str] = Field(default_factory=dict)
    
    # Company Information (populated by Company Info Agent)
    from_company: Optional[Company] = None
    to_company: Optional[Company] = None
    
    # Project Details (populated by Project Info Agent)
    project_info: Optional[ProjectInfo] = None
    
    # Line Items (populated by Line Items Agent and sub-agents)
    line_item_groups: List[LineItemGroup] = Field(default_factory=list)
    
    # Pricing (populated by Pricing Summary Agent)
    pricing_summary: Optional[PricingSummary] = None
    
    # Executive Summary (populated by Executive Summary Agent)
    executive_summary: Optional[ExecutiveSummary] = None
    
    # Contacts (populated by Contacts Agent)
    project_contacts: Dict[str, Contact] = Field(default_factory=dict)
    
    # Terms and Approvals (populated by Approval Agent)
    terms_and_conditions: List[str] = Field(default_factory=list)
    payment_terms: str = "Net 30"
    quote_validity_days: int = 30
    approval_signature_blocks: List[Dict[str, str]] = Field(default_factory=list)
    
    # Agent Tracking
    agent_results: Dict[str, AgentResult] = Field(default_factory=dict)
    
    # Error Tracking
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Processing Metadata
    processing_time_seconds: Optional[float] = None
    llm_tokens_used: int = 0
    
    model_config = ConfigDict(from_attributes=True)
    
    def add_agent_result(self, result: AgentResult):
        """Add agent execution result"""
        self.agent_results[result.agent_name] = result
        self.updated_at = datetime.utcnow()
    
    def add_error(self, error: Dict[str, Any]):
        """Add error to state"""
        self.errors.append({
            **error,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.updated_at = datetime.utcnow()
    
    def add_warning(self, warning: Dict[str, Any]):
        """Add warning to state"""
        self.warnings.append({
            **warning,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.updated_at = datetime.utcnow()
    
    def get_total_line_items(self) -> int:
        """Get total number of line items"""
        return sum(len(group.items) for group in self.line_item_groups)
    
    def get_total_value(self) -> Optional[Decimal]:
        """Get total quotation value"""
        return self.pricing_summary.grand_total if self.pricing_summary else None
    
    def is_complete(self) -> bool:
        """Check if quotation is complete"""
        required_fields = [
            self.from_company,
            self.to_company,
            self.project_info,
            self.line_item_groups,
            self.pricing_summary,
            self.executive_summary
        ]
        return all(field is not None for field in required_fields) and len(self.line_item_groups) > 0
    
    def to_summary_dict(self) -> Dict[str, Any]:
        """Get summary representation for logging/display"""
        return {
            "quote_id": self.quote_id,
            "quote_number": self.quote_number,
            "status": self.status.value,
            "project_name": self.project_info.project_name if self.project_info else None,
            "client": self.to_company.name if self.to_company else None,
            "total_value": str(self.get_total_value()) if self.get_total_value() else None,
            "total_line_items": self.get_total_line_items(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "is_complete": self.is_complete(),
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings)
        }


# ===================================================================
# LANGGRAPH STATE TYPE
# ===================================================================

class QuotationStateDict(TypedDict):
    """
    TypedDict version of QuotationState for LangGraph compatibility.
    This ensures proper type hints in the state graph.
    """
    # Core identifiers
    quote_id: str
    quote_number: Optional[str]
    status: str
    
    # Timestamps
    created_at: str
    updated_at: str
    
    # Input data
    project_input: Dict[str, Any]
    user_context: Dict[str, str]
    
    # Company data
    from_company: Optional[Dict[str, Any]]
    to_company: Optional[Dict[str, Any]]
    
    # Project data
    project_info: Optional[Dict[str, Any]]
    
    # Line items
    line_item_groups: List[Dict[str, Any]]
    
    # Pricing
    pricing_summary: Optional[Dict[str, Any]]
    
    # Executive summary
    executive_summary: Optional[Dict[str, Any]]
    
    # Contacts
    project_contacts: Dict[str, Dict[str, Any]]
    
    # Terms
    terms_and_conditions: List[str]
    payment_terms: str
    quote_validity_days: int
    approval_signature_blocks: List[Dict[str, str]]
    
    # Tracking
    agent_results: Dict[str, Dict[str, Any]]
    errors: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    
    # Metadata
    processing_time_seconds: Optional[float]
    llm_tokens_used: int


# ===================================================================
# UTILITY FUNCTIONS
# ===================================================================

def create_initial_state(project_input: Dict[str, Any], user_context: Optional[Dict[str, str]] = None) -> QuotationState:
    """
    Create initial quotation state from project input.
    
    Args:
        project_input: Raw project input data
        user_context: Optional user context (user_id, company_id, etc.)
    
    Returns:
        Initialized QuotationState
    """
    return QuotationState(
        project_input=project_input,
        user_context=user_context or {},
        status=QuotationStatus.DRAFT
    )


def state_to_dict(state: QuotationState) -> Dict[str, Any]:
    """Convert QuotationState to dictionary for LangGraph"""
    return state.model_dump(mode='json')


def dict_to_state(state_dict: Dict[str, Any]) -> QuotationState:
    """Convert dictionary to QuotationState"""
    return QuotationState(**state_dict)
