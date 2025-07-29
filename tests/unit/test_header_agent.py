import pytest
from datetime import datetime
from unittest.mock import patch
from agents.simple_agents.header_agent import HeaderAgent, HeaderState


@pytest.fixture
def header_agent():
    """Fixture to create HeaderAgent instance."""
    return HeaderAgent()


@pytest.fixture
def valid_input_data():
    """Fixture for valid input data."""
    return {
        "company_name": "ProQuote Electrical",
        "prepared_by": "John Doe",
        "client_name": "ABC Corporation",
        "client_contact": "jane@abc.com",
        "project_name": "Office Renovation",
        "validity_days": 45
    }


@pytest.fixture
def minimal_input_data():
    """Fixture for minimal valid input data."""
    return {
        "company_name": "ProQuote Electrical",
        "prepared_by": "John Doe"
    }


class TestHeaderAgent:
    """Test suite for HeaderAgent."""
    
    def test_agent_initialization(self, header_agent):
        """Test agent initializes correctly."""
        assert header_agent.name == "HeaderAgent"
        assert isinstance(header_agent.state, HeaderState)
        assert header_agent.state.error is None
    
    def test_validate_input_valid(self, header_agent, valid_input_data):
        """Test input validation with valid data."""
        assert header_agent.validate_input(valid_input_data) is True
    
    def test_validate_input_missing_company(self, header_agent):
        """Test input validation with missing company_name."""
        invalid_data = {"prepared_by": "John Doe"}
        assert header_agent.validate_input(invalid_data) is False
    
    def test_validate_input_missing_preparer(self, header_agent):
        """Test input validation with missing prepared_by."""
        invalid_data = {"company_name": "ProQuote"}
        assert header_agent.validate_input(invalid_data) is False
    
    @pytest.mark.asyncio
    async def test_process_valid_input(self, header_agent, valid_input_data):
        """Test processing with valid input data."""
        with patch('agents.simple_agents.header_agent.datetime') as mock_datetime:
            mock_now = datetime(2025, 1, 15, 10, 0, 0)
            mock_datetime.utcnow.return_value = mock_now
            mock_datetime.strptime.side_effect = datetime.strptime
            
            result = await header_agent.process(valid_input_data)
            
            assert "error" not in result
            assert result["quote_number"] == "QT-20250115-0001"
            assert result["company_name"] == "ProQuote Electrical"
            assert result["prepared_by"] == "John Doe"
            assert result["client_name"] == "ABC Corporation"
            assert result["client_contact"] == "jane@abc.com"
            assert result["project_name"] == "Office Renovation"
            assert result["status"] == "draft"
    
    @pytest.mark.asyncio
    async def test_process_minimal_input(self, header_agent, minimal_input_data):
        """Test processing with minimal required input."""
        result = await header_agent.process(minimal_input_data)
        
        assert "error" not in result
        assert result["company_name"] == "ProQuote Electrical"
        assert result["prepared_by"] == "John Doe"
        assert "client_name" not in result
        assert "client_contact" not in result
        assert "project_name" not in result
    
    @pytest.mark.asyncio
    async def test_process_invalid_input(self, header_agent):
        """Test processing with invalid input."""
        invalid_data = {"some_field": "some_value"}
        result = await header_agent.process(invalid_data)
        
        assert "error" in result
        assert result["error"] == "Missing required fields: company_name or prepared_by"
        assert header_agent.state.error == "Missing required fields: company_name or prepared_by"
    
    @pytest.mark.asyncio
    async def test_quote_number_generation(self, header_agent, minimal_input_data):
        """Test quote number generation format."""
        with patch('agents.simple_agents.header_agent.datetime') as mock_datetime:
            mock_now = datetime(2025, 3, 25, 14, 30, 0)
            mock_datetime.utcnow.return_value = mock_now
            mock_datetime.strptime.side_effect = datetime.strptime
            
            result = await header_agent.process(minimal_input_data)
            
            assert result["quote_number"] == "QT-20250325-0001"
    
    @pytest.mark.asyncio
    async def test_validity_period_default(self, header_agent, minimal_input_data):
        """Test default validity period of 30 days."""
        result = await header_agent.process(minimal_input_data)
        
        quote_date = datetime.fromisoformat(result["quote_date"])
        valid_until = datetime.fromisoformat(result["valid_until"])
        
        # Should be approximately 30 days difference
        # Using approximate check due to potential date calculation differences
        days_diff = (valid_until - quote_date).days
        assert 29 <= days_diff <= 31
    
    @pytest.mark.asyncio
    async def test_validity_period_custom(self, header_agent, valid_input_data):
        """Test custom validity period."""
        result = await header_agent.process(valid_input_data)
        
        quote_date = datetime.fromisoformat(result["quote_date"])
        valid_until = datetime.fromisoformat(result["valid_until"])
        
        # Should be approximately 45 days as specified in input
        days_diff = (valid_until - quote_date).days
        assert 44 <= days_diff <= 46
    
    def test_state_management(self, header_agent, minimal_input_data):
        """Test agent state is properly managed."""
        # Initial state
        assert header_agent.state.company_name is None
        assert header_agent.state.quote_number is None
        
        # After processing
        import asyncio
        asyncio.run(header_agent.process(minimal_input_data))
        
        assert header_agent.state.company_name == "ProQuote Electrical"
        assert header_agent.state.prepared_by == "John Doe"
        assert header_agent.state.quote_number is not None
        assert header_agent.state.quote_date is not None