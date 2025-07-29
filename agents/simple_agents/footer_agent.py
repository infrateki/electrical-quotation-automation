from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

from shared.models.base import BaseAgent, AgentState


class FooterState(AgentState):
    """State model for FooterAgent."""
    terms_template: Optional[str] = None
    disclaimer_template: Optional[str] = None
    signature_block: Optional[Dict[str, str]] = None


class FooterAgent(BaseAgent):
    """Agent responsible for generating quotation footers with terms and legal disclaimers."""
    
    def __init__(self):
        super().__init__(name="FooterAgent")
        self._state = FooterState()
        
        # Default templates
        self.default_terms = """
Terms & Conditions:
1. This quotation is valid for {validity_days} days from the date of issue.
2. Prices are subject to change based on material availability.
3. Payment terms: 50% deposit upon acceptance, 50% upon completion.
4. All work will be performed in accordance with NEC 2023 standards.
5. Warranty: 1 year on workmanship, manufacturer's warranty on materials.
"""
        
        self.default_disclaimer = """
Disclaimer:
This quotation is based on the information provided and site conditions observed. 
Any changes to scope, specifications, or unforeseen conditions may result in 
additional charges. Permits and inspection fees are not included unless specified.
"""
        
        self.default_signature_block = {
            "acceptance_text": "By signing below, you accept this quotation and agree to the terms and conditions.",
            "client_signature": "Client Signature: _______________________  Date: ___________",
            "company_signature": "Company Representative: _______________________  Date: ___________"
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for footer generation.
        
        Args:
            input_data: Must contain quotation_id
            
        Returns:
            True if valid, False otherwise
        """
        return "quotation_id" in input_data
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to generate quotation footer.
        
        Args:
            input_data: Contains quotation details and optional custom terms
            
        Returns:
            Dict containing formatted footer information
        """
        if not self.validate_input(input_data):
            self._state.error = "Missing required field: quotation_id"
            return {"error": self._state.error}
        
        # Get validity days for terms
        validity_days = input_data.get("validity_days", 30)
        
        # Use custom templates if provided, otherwise defaults
        terms = input_data.get("custom_terms", self.default_terms)
        disclaimer = input_data.get("custom_disclaimer", self.default_disclaimer)
        signature_block = input_data.get("custom_signature_block", self.default_signature_block)
        
        # Format terms with validity days
        if "{validity_days}" in terms:
            terms = terms.format(validity_days=validity_days)
        
        # Update state
        self._state.terms_template = terms
        self._state.disclaimer_template = disclaimer
        self._state.signature_block = signature_block
        
        # Build footer response
        footer_data = {
            "quotation_id": input_data["quotation_id"],
            "terms_and_conditions": terms,
            "disclaimer": disclaimer,
            "signature_block": signature_block,
            "footer_sections": {
                "contact_info": {
                    "phone": "(555) 123-4567",
                    "email": "quotes@proquote.com",
                    "website": "www.proquote.com"
                },
                "license_info": "Licensed Electrical Contractor #EC123456",
                "insurance_info": "Fully Insured and Bonded"
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
        # Add page numbering template
        footer_data["page_template"] = "Page {page_num} of {total_pages}"
        
        return footer_data