import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from datetime import datetime

from agents.orchestrator.supervisor import QuotationOrchestrator
from shared.models.quotation import create_initial_state


class TestQuotationOrchestrator:
    """Unit tests for QuotationOrchestrator."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create QuotationOrchestrator instance for testing."""
        return QuotationOrchestrator()
    
    @pytest.fixture
    def initial_state(self):
        """Create initial quotation state for testing."""
        state = create_initial_state()
        state["quotation_id"] = "TEST-001"
        state["client_info"]["name"] = "Test Client"
        state["client_info"]["email"] = "test@example.com"
        state["project_info"]["name"] = "Test Project"
        state["metadata"]["created_by"] = "Test User"
        return state
    
    def test_orchestrator_initialization(self, orchestrator):
        """Test orchestrator initializes with all required agents."""
        assert orchestrator.header_agent is not None
        assert orchestrator.footer_agent is not None
        assert orchestrator.company_info_agent is not None
        assert orchestrator.workflow is not None
    
    @pytest.mark.asyncio
    async def test_supervisor_node(self, orchestrator, initial_state):
        """Test supervisor node initializes workflow correctly."""
        result = await orchestrator._supervisor(initial_state)
        
        assert result["quotation_id"] == "TEST-001"
        assert result["metadata"]["updated_at"] is not None
    
    @pytest.mark.asyncio
    async def test_run_header_agent_success(self, orchestrator, initial_state):
        """Test successful header agent execution."""
        # Mock header agent response
        mock_response = {
            "quote_number": "QT-20250128-0001",
            "quote_date": "2025-01-28T12:00:00",
            "valid_until": "2025-02-27T12:00:00"
        }
        
        with patch.object(orchestrator.header_agent, 'process', 
                         new=AsyncMock(return_value=mock_response)):
            result = await orchestrator._run_header_agent(initial_state)
            
            assert result["header"] == mock_response
            assert result["quote_number"] == "QT-20250128-0001"
            assert len(result["agent_execution_log"]) == 1
            assert result["agent_execution_log"][0]["agent"] == "HeaderAgent"
            assert result["agent_execution_log"][0]["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_run_header_agent_failure(self, orchestrator, initial_state):
        """Test header agent execution with error."""
        error_msg = "Header generation failed"
        
        with patch.object(orchestrator.header_agent, 'process',
                         side_effect=Exception(error_msg)):
            result = await orchestrator._run_header_agent(initial_state)
            
            assert len(result["errors"]) == 1
            assert result["errors"][0]["agent"] == "HeaderAgent"
            assert error_msg in result["errors"][0]["error"]
            assert len(result["agent_execution_log"]) == 1
            assert result["agent_execution_log"][0]["status"] == "failed"
    
    @pytest.mark.asyncio
    async def test_run_company_info_agent_success(self, orchestrator, initial_state):
        """Test successful company info agent execution."""
        mock_response = {
            "company_section": {
                "name": "ProQuote Electrical Ltd",
                "contact": {
                    "address": "123 Electric Ave",
                    "phone": "+1234567890",
                    "email": "info@proquote.com",
                    "website": "www.proquote.com"
                },
                "legal": {
                    "registration_number": "REG123",
                    "tax_id": "TAX456"
                },
                "logo_url": "https://example.com/logo.png"
            }
        }
        
        with patch.object(orchestrator.company_info_agent, 'process',
                         new=AsyncMock(return_value=mock_response)):
            result = await orchestrator._run_company_info_agent(initial_state)
            
            assert result["company_info"]["name"] == "ProQuote Electrical Ltd"
            assert result["company_info"]["email"] == "info@proquote.com"
            assert result["company_info"]["logo_url"] == "https://example.com/logo.png"
            assert len(result["agent_execution_log"]) == 1
            assert result["agent_execution_log"][0]["agent"] == "CompanyInfoAgent"
    
    @pytest.mark.asyncio
    async def test_run_company_info_agent_with_overrides(self, orchestrator, initial_state):
        """Test company info agent with custom overrides."""
        initial_state["custom_fields"]["company_overrides"] = {
            "company_name": "Custom Company",
            "phone": "+9876543210"
        }
        
        mock_response = {"company_section": {"name": "Custom Company", "contact": {}}}
        
        with patch.object(orchestrator.company_info_agent, 'process',
                         new=AsyncMock(return_value=mock_response)) as mock_process:
            await orchestrator._run_company_info_agent(initial_state)
            
            # Verify overrides were passed to the agent
            mock_process.assert_called_once()
            call_args = mock_process.call_args[0][0]
            assert call_args["company_name"] == "Custom Company"
            assert call_args["phone"] == "+9876543210"
    
    @pytest.mark.asyncio
    async def test_run_footer_agent_success(self, orchestrator, initial_state):
        """Test successful footer agent execution."""
        mock_response = {
            "terms_and_conditions": "Standard terms apply",
            "disclaimers": ["Disclaimer 1", "Disclaimer 2"],
            "signature_blocks": [{
                "title": "Authorized Signatory",
                "name": "",
                "date": ""
            }]
        }
        
        with patch.object(orchestrator.footer_agent, 'process',
                         new=AsyncMock(return_value=mock_response)):
            result = await orchestrator._run_footer_agent(initial_state)
            
            assert result["footer"] == mock_response
            assert result["terms_and_conditions"] == "Standard terms apply"
            assert len(result["agent_execution_log"]) == 1
            assert result["agent_execution_log"][0]["agent"] == "FooterAgent"
    
    @pytest.mark.asyncio
    async def test_run_footer_agent_with_custom_terms(self, orchestrator, initial_state):
        """Test footer agent with custom terms."""
        initial_state["custom_fields"]["custom_terms"] = "Custom payment terms"
        
        with patch.object(orchestrator.footer_agent, 'process',
                         new=AsyncMock()) as mock_process:
            await orchestrator._run_footer_agent(initial_state)
            
            # Verify custom terms were passed
            mock_process.assert_called_once()
            call_args = mock_process.call_args[0][0]
            assert call_args["custom_terms"] == "Custom payment terms"
    
    def test_route_next_agent(self, orchestrator, initial_state):
        """Test routing logic for next agent selection."""
        # No header - should route to header
        assert orchestrator._route_next_agent(initial_state) == "header"
        
        # Has header but no company info - should route to company
        initial_state["header"] = {"some": "data"}
        initial_state["company_info"]["name"] = None
        assert orchestrator._route_next_agent(initial_state) == "company"
        
        # Has header and company but no footer - should route to footer
        initial_state["company_info"]["name"] = "Test Company"
        assert orchestrator._route_next_agent(initial_state) == "footer"
        
        # Has everything - should complete
        initial_state["footer"] = {"some": "data"}
        assert orchestrator._route_next_agent(initial_state) == "complete"
    
    def test_get_timestamp_ms(self, orchestrator):
        """Test timestamp generation."""
        timestamp1 = orchestrator._get_timestamp_ms()
        timestamp2 = orchestrator._get_timestamp_ms()
        
        assert isinstance(timestamp1, int)
        assert timestamp2 >= timestamp1
    
    @pytest.mark.asyncio
    async def test_generate_quotation_success(self, orchestrator, initial_state):
        """Test successful quotation generation flow."""
        # Mock the workflow execution
        mock_final_state = initial_state.copy()
        mock_final_state["header"] = {"quote_number": "QT-123"}
        mock_final_state["company_info"]["name"] = "Test Company"
        mock_final_state["footer"] = {"terms": "Standard"}
        
        with patch.object(orchestrator.workflow, 'ainvoke',
                         new=AsyncMock(return_value=mock_final_state)):
            result = await orchestrator.generate_quotation(initial_state)
            
            assert result["metadata"]["status"] == "generated"
            assert result["metadata"]["updated_at"] is not None
            assert result["quotation_id"] == "TEST-001"
    
    @pytest.mark.asyncio
    async def test_generate_quotation_failure(self, orchestrator, initial_state):
        """Test quotation generation with workflow failure."""
        error_msg = "Workflow execution failed"
        
        with patch.object(orchestrator.workflow, 'ainvoke',
                         side_effect=Exception(error_msg)):
            result = await orchestrator.generate_quotation(initial_state)
            
            assert result["metadata"]["status"] == "failed"
            assert len(result["errors"]) == 1
            assert result["errors"][0]["agent"] == "Orchestrator"
            assert result["errors"][0]["fatal"] is True
            assert error_msg in result["errors"][0]["error"]
    
    def test_workflow_structure(self, orchestrator):
        """Test workflow graph structure."""
        # Verify workflow is compiled
        assert orchestrator.workflow is not None
        
        # The workflow should have nodes for each agent
        # Note: Direct inspection of LangGraph internals may vary by version
        # This is a basic check that workflow exists and is callable
        assert hasattr(orchestrator.workflow, 'ainvoke')