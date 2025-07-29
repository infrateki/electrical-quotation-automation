from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from shared.models.base import BaseAgent, AgentState


class CompanyInfoState(AgentState):
    """State model for CompanyInfoAgent."""
    company_name: Optional[str] = None
    company_logo_url: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None


class CompanyInfoAgent(BaseAgent):
    """Agent responsible for managing company information in quotations."""
    
    def __init__(self):
        super().__init__(name="CompanyInfoAgent")
        self._state = CompanyInfoState()
        # Default company info (would come from DB in production)
        self._default_info = {
            "company_name": "ProQuote Electrical Ltd",
            "address": "123 Electric Avenue, Tech City, TC 12345",
            "phone": "+1 (555) 123-4567",
            "email": "info@proquote.com",
            "website": "www.proquote.com",
            "registration_number": "REG-2024-001",
            "tax_id": "TAX-123456789"
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for company info.
        
        Args:
            input_data: Can be empty (uses defaults) or contain company overrides
            
        Returns:
            True (always valid as we have defaults)
        """
        # Company info is always valid since we have defaults
        return True
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to generate company information section.
        
        Args:
            input_data: Optional overrides for company information
            
        Returns:
            Dict containing formatted company information
        """
        # Start with default info
        company_info = self._default_info.copy()
        
        # Override with any provided input
        for field in ["company_name", "company_logo_url", "address", "phone", 
                     "email", "website", "registration_number", "tax_id"]:
            if field in input_data:
                company_info[field] = input_data[field]
        
        # Update state
        self._state.company_name = company_info.get("company_name")
        self._state.company_logo_url = company_info.get("company_logo_url")
        self._state.address = company_info.get("address")
        self._state.phone = company_info.get("phone")
        self._state.email = company_info.get("email")
        self._state.website = company_info.get("website")
        self._state.registration_number = company_info.get("registration_number")
        self._state.tax_id = company_info.get("tax_id")
        
        # Format the response
        response = {
            "company_section": {
                "name": company_info["company_name"],
                "contact": {
                    "address": company_info["address"],
                    "phone": company_info["phone"],
                    "email": company_info["email"],
                    "website": company_info["website"]
                },
                "legal": {
                    "registration_number": company_info["registration_number"],
                    "tax_id": company_info["tax_id"]
                }
            }
        }
        
        # Add logo if provided
        if company_info.get("company_logo_url"):
            response["company_section"]["logo_url"] = company_info["company_logo_url"]
        
        # Add formatted display text
        response["display_text"] = self._format_display_text(company_info)
        
        return response
    
    def _format_display_text(self, company_info: Dict[str, Any]) -> str:
        """Format company info for display in quotation.
        
        Args:
            company_info: Company information dict
            
        Returns:
            Formatted text for display
        """
        lines = [
            company_info["company_name"],
            company_info["address"],
            f"Phone: {company_info['phone']}",
            f"Email: {company_info['email']}",
            f"Website: {company_info['website']}"
        ]
        
        if company_info.get("registration_number"):
            lines.append(f"Reg. No: {company_info['registration_number']}")
        
        if company_info.get("tax_id"):
            lines.append(f"Tax ID: {company_info['tax_id']}")
        
        return "\n".join(lines)