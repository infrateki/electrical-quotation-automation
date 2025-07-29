from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from shared.models.base import BaseAgent, AgentState


class HeaderState(AgentState):
    """State model for HeaderAgent."""
    company_name: Optional[str] = None
    quote_number: Optional[str] = None
    quote_date: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    prepared_by: Optional[str] = None


class HeaderAgent(BaseAgent):
    """Agent responsible for generating quotation headers."""
    
    def __init__(self):
        super().__init__(name="HeaderAgent")
        self._state = HeaderState()
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for header generation.
        
        Args:
            input_data: Must contain company_name and prepared_by
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = ["company_name", "prepared_by"]
        return all(field in input_data for field in required_fields)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to generate quotation header.
        
        Args:
            input_data: Contains company details and preparer info
            
        Returns:
            Dict containing formatted header information
        """
        if not self.validate_input(input_data):
            self._state.error = "Missing required fields: company_name or prepared_by"
            return {"error": self._state.error}
        
        # Update state with input data
        self._state.company_name = input_data.get("company_name")
        self._state.prepared_by = input_data.get("prepared_by")
        self._state.quote_date = datetime.utcnow()
        
        # Generate quote number (format: QT-YYYYMMDD-XXXX)
        date_str = self._state.quote_date.strftime("%Y%m%d")
        # In production, this would query DB for sequential number
        quote_sequence = "0001"
        self._state.quote_number = f"QT-{date_str}-{quote_sequence}"
        
        # Set validity period (default 30 days)
        validity_days = input_data.get("validity_days", 30)
        self._state.valid_until = self._state.quote_date + timedelta(days=validity_days)
        
        # Build header response
        header_data = {
            "quote_number": self._state.quote_number,
            "company_name": self._state.company_name,
            "quote_date": self._state.quote_date.isoformat(),
            "valid_until": self._state.valid_until.isoformat(),
            "prepared_by": self._state.prepared_by,
            "status": "draft"
        }
        
        # Add optional fields if provided
        if "client_name" in input_data:
            header_data["client_name"] = input_data["client_name"]
        if "client_contact" in input_data:
            header_data["client_contact"] = input_data["client_contact"]
        if "project_name" in input_data:
            header_data["project_name"] = input_data["project_name"]
        
        return header_data