import pytest
from datetime import datetime
from agents.simple_agents.footer_agent import FooterAgent, FooterState


@pytest.fixture
def footer_agent():
    """Fixture to create FooterAgent instance."""
    return FooterAgent()


@pytest.fixture
def valid_input_data():
    """Fixture for valid input data."""
    return {
        "quotation_id": "quot_20250128_001",
        "validity_days": 45,
        "custom_terms": "Custom terms with {validity_days} days validity",
        "custom_disclaimer": "Custom disclaimer text"
    }


@pytest.fixture
def minimal_input_data():
    """Fixture for minimal valid input data."""
    return {
        "quotation_id": "quot_20250128_002"
    }


class TestFooterAgent:
    """Test suite for FooterAgent."""
    
    def test_agent_initialization(self, footer_agent):
        """Test agent initializes correctly."""
        assert footer_agent.name == "FooterAgent"
        assert isinstance(footer_agent.state, FooterState)
        assert footer_agent.state.error is None
        assert footer_agent.default_terms is not None
        assert footer_agent.default_disclaimer is not None
        assert footer_agent.default_signature_block is not None
    
    def test_validate_input_valid(self, footer_agent, valid_input_data):
        """Test input validation with valid data."""
        assert footer_agent.validate_input(valid_input_data) is True
    
    def test_validate_input_missing_quotation_id(self, footer_agent):
        """Test input validation with missing quotation_id."""
        invalid_data = {"validity_days": 30}
        assert footer_agent.validate_input(invalid_data) is False
    
    @pytest.mark.asyncio
    async def test_process_valid_input(self, footer_agent, valid_input_data):
        """Test processing with valid input data."""
        result = await footer_agent.process(valid_input_data)
        
        assert "error" not in result
        assert result["quotation_id"] == "quot_20250128_001"
        assert "45 days validity" in result["terms_and_conditions"]
        assert result["disclaimer"] == "Custom disclaimer text"
        assert "signature_block" in result
        assert "footer_sections" in result
        assert result["footer_sections"]["license_info"] == "Licensed Electrical Contractor #EC123456"
        assert "generated_at" in result
        assert "page_template" in result
    
    @pytest.mark.asyncio
    async def test_process_minimal_input(self, footer_agent, minimal_input_data):
        """Test processing with minimal required input."""
        result = await footer_agent.process(minimal_input_data)
        
        assert "error" not in result
        assert result["quotation_id"] == "quot_20250128_002"
        assert "30 days" in result["terms_and_conditions"]  # Default validity
        assert "NEC 2023" in result["terms_and_conditions"]
        assert "This quotation is based on" in result["disclaimer"]
        assert result["signature_block"]["acceptance_text"] is not None
    
    @pytest.mark.asyncio
    async def test_process_invalid_input(self, footer_agent):
        """Test processing with invalid input."""
        invalid_data = {"some_field": "some_value"}
        result = await footer_agent.process(invalid_data)
        
        assert "error" in result
        assert result["error"] == "Missing required field: quotation_id"
        assert footer_agent.state.error == "Missing required field: quotation_id"
    
    @pytest.mark.asyncio
    async def test_custom_signature_block(self, footer_agent):
        """Test custom signature block processing."""
        custom_signature = {
            "acceptance_text": "Custom acceptance text",
            "client_signature": "Custom client line",
            "company_signature": "Custom company line"
        }
        
        input_data = {
            "quotation_id": "quot_test",
            "custom_signature_block": custom_signature
        }
        
        result = await footer_agent.process(input_data)
        
        assert result["signature_block"] == custom_signature
    
    @pytest.mark.asyncio
    async def test_footer_sections(self, footer_agent, minimal_input_data):
        """Test footer sections are properly included."""
        result = await footer_agent.process(minimal_input_data)
        
        footer_sections = result["footer_sections"]
        assert "contact_info" in footer_sections
        assert footer_sections["contact_info"]["phone"] == "(555) 123-4567"
        assert footer_sections["contact_info"]["email"] == "quotes@proquote.com"
        assert "license_info" in footer_sections
        assert "insurance_info" in footer_sections
    
    @pytest.mark.asyncio
    async def test_terms_formatting(self, footer_agent):
        """Test terms template formatting with validity days."""
        input_data = {
            "quotation_id": "quot_test",
            "validity_days": 60
        }
        
        result = await footer_agent.process(input_data)
        
        assert "60 days" in result["terms_and_conditions"]
        assert "Payment terms:" in result["terms_and_conditions"]
        assert "Warranty:" in result["terms_and_conditions"]
    
    def test_state_management(self, footer_agent, valid_input_data):
        """Test agent state is properly managed."""
        # Initial state
        assert footer_agent.state.terms_template is None
        assert footer_agent.state.disclaimer_template is None
        
        # After processing
        import asyncio
        asyncio.run(footer_agent.process(valid_input_data))
        
        assert footer_agent.state.terms_template is not None
        assert footer_agent.state.disclaimer_template is not None
        assert footer_agent.state.signature_block is not None