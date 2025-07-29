import pytest
from agents.simple_agents.company_info_agent import CompanyInfoAgent, CompanyInfoState


@pytest.fixture
def company_agent():
    """Fixture to create CompanyInfoAgent instance."""
    return CompanyInfoAgent()


@pytest.fixture
def override_data():
    """Fixture for company info override data."""
    return {
        "company_name": "Custom Electric Co",
        "company_logo_url": "/assets/custom-logo.png",
        "address": "456 Power Street, Energy City, EC 54321",
        "phone": "+1 (555) 987-6543",
        "email": "custom@electric.com",
        "website": "www.customelectric.com",
        "registration_number": "CUSTOM-REG-2025",
        "tax_id": "TAX-987654321"
    }


class TestCompanyInfoAgent:
    """Test suite for CompanyInfoAgent."""
    
    def test_agent_initialization(self, company_agent):
        """Test agent initializes correctly."""
        assert company_agent.name == "CompanyInfoAgent"
        assert isinstance(company_agent.state, CompanyInfoState)
        assert company_agent.state.error is None
        assert company_agent._default_info is not None
        assert company_agent._default_info["company_name"] == "ProQuote Electrical Ltd"
    
    def test_validate_input_always_valid(self, company_agent):
        """Test input validation always returns True."""
        assert company_agent.validate_input({}) is True
        assert company_agent.validate_input({"random": "data"}) is True
        assert company_agent.validate_input({"company_name": "Test"}) is True
    
    @pytest.mark.asyncio
    async def test_process_with_defaults(self, company_agent):
        """Test processing with default company information."""
        result = await company_agent.process({})
        
        assert "error" not in result
        assert "company_section" in result
        assert result["company_section"]["name"] == "ProQuote Electrical Ltd"
        assert result["company_section"]["contact"]["phone"] == "+1 (555) 123-4567"
        assert result["company_section"]["contact"]["email"] == "info@proquote.com"
        assert result["company_section"]["legal"]["registration_number"] == "REG-2024-001"
        assert "display_text" in result
        assert "ProQuote Electrical Ltd" in result["display_text"]
    
    @pytest.mark.asyncio
    async def test_process_with_overrides(self, company_agent, override_data):
        """Test processing with custom company information."""
        result = await company_agent.process(override_data)
        
        assert "error" not in result
        assert result["company_section"]["name"] == "Custom Electric Co"
        assert result["company_section"]["contact"]["phone"] == "+1 (555) 987-6543"
        assert result["company_section"]["contact"]["email"] == "custom@electric.com"
        assert result["company_section"]["legal"]["registration_number"] == "CUSTOM-REG-2025"
        assert result["company_section"]["logo_url"] == "/assets/custom-logo.png"
    
    @pytest.mark.asyncio
    async def test_process_partial_overrides(self, company_agent):
        """Test processing with partial overrides."""
        partial_data = {
            "company_name": "Partial Electric",
            "phone": "+1 (555) 111-2222"
        }
        
        result = await company_agent.process(partial_data)
        
        # Overridden fields
        assert result["company_section"]["name"] == "Partial Electric"
        assert result["company_section"]["contact"]["phone"] == "+1 (555) 111-2222"
        
        # Default fields
        assert result["company_section"]["contact"]["email"] == "info@proquote.com"
        assert result["company_section"]["contact"]["address"] == "123 Electric Avenue, Tech City, TC 12345"
    
    @pytest.mark.asyncio
    async def test_display_text_formatting(self, company_agent):
        """Test display text formatting."""
        result = await company_agent.process({})
        display_text = result["display_text"]
        
        assert "ProQuote Electrical Ltd" in display_text
        assert "Phone: +1 (555) 123-4567" in display_text
        assert "Email: info@proquote.com" in display_text
        assert "Website: www.proquote.com" in display_text
        assert "Reg. No: REG-2024-001" in display_text
        assert "Tax ID: TAX-123456789" in display_text
    
    @pytest.mark.asyncio
    async def test_logo_url_handling(self, company_agent):
        """Test logo URL is only included when provided."""
        # Without logo
        result_no_logo = await company_agent.process({})
        assert "logo_url" not in result_no_logo["company_section"]
        
        # With logo
        result_with_logo = await company_agent.process({"company_logo_url": "/logo.png"})
        assert result_with_logo["company_section"]["logo_url"] == "/logo.png"
    
    def test_state_management(self, company_agent, override_data):
        """Test agent state is properly managed."""
        # Initial state
        assert company_agent.state.company_name is None
        assert company_agent.state.phone is None
        
        # After processing
        import asyncio
        asyncio.run(company_agent.process(override_data))
        
        assert company_agent.state.company_name == "Custom Electric Co"
        assert company_agent.state.phone == "+1 (555) 987-6543"
        assert company_agent.state.email == "custom@electric.com"
        assert company_agent.state.registration_number == "CUSTOM-REG-2025"
    
    @pytest.mark.asyncio
    async def test_response_structure(self, company_agent):
        """Test response has correct structure."""
        result = await company_agent.process({})
        
        # Check main sections exist
        assert "company_section" in result
        assert "display_text" in result
        
        # Check company_section structure
        company_section = result["company_section"]
        assert "name" in company_section
        assert "contact" in company_section
        assert "legal" in company_section
        
        # Check contact structure
        assert "address" in company_section["contact"]
        assert "phone" in company_section["contact"]
        assert "email" in company_section["contact"]
        assert "website" in company_section["contact"]
        
        # Check legal structure
        assert "registration_number" in company_section["legal"]
        assert "tax_id" in company_section["legal"]