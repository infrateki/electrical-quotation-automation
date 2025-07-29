import pytest
from datetime import datetime, timedelta
from agents.workflow_agents.project_info_agent import ProjectInfoAgent, ProjectInfoState


@pytest.fixture
def project_agent():
    """Fixture to create ProjectInfoAgent instance."""
    return ProjectInfoAgent()


@pytest.fixture
def sample_project_data():
    """Fixture for sample project data."""
    return {
        "project_name": "Office Building Electrical Upgrade",
        "project_description": "Complete electrical system upgrade for a 10,000 sq ft office building. Install new 400 amp panel, upgrade to 240V service, add 50 outlets, LED lighting throughout. Work includes 3 conference rooms and server room. Estimated duration 6 weeks.",
        "location": {
            "address": "123 Business Park Drive, Suite 200",
            "city": "Springfield",
            "state": "IL",
            "zip": "62701"
        },
        "start_date": "2025-02-01T00:00:00",
        "permit_required": True
    }


@pytest.fixture
def minimal_project_data():
    """Fixture for minimal project data."""
    return {
        "project_description": "Residential electrical work"
    }


@pytest.fixture
def raw_text_data():
    """Fixture for raw text input."""
    return {
        "raw_text": "Need to install 20 new outlets in warehouse. 15,000 square feet facility requires 480V three phase power. Also need new lighting panels and emergency exit signs. Project should take about 2 months."
    }


class TestProjectInfoAgent:
    """Test suite for ProjectInfoAgent."""
    
    def test_agent_initialization(self, project_agent):
        """Test agent initializes correctly."""
        assert project_agent.name == "ProjectInfoAgent"
        assert isinstance(project_agent.state, ProjectInfoState)
        assert project_agent.state.error is None
        assert len(project_agent.project_types) > 0
        assert len(project_agent.voltage_patterns) > 0
    
    def test_validate_input_valid(self, project_agent, sample_project_data):
        """Test input validation with valid data."""
        assert project_agent.validate_input(sample_project_data) is True
        assert project_agent.validate_input({"project_name": "Test"}) is True
        assert project_agent.validate_input({"raw_text": "Test"}) is True
    
    def test_validate_input_invalid(self, project_agent):
        """Test input validation with invalid data."""
        assert project_agent.validate_input({}) is False
        assert project_agent.validate_input({"other_field": "value"}) is False
    
    @pytest.mark.asyncio
    async def test_process_complete_data(self, project_agent, sample_project_data):
        """Test processing with complete project data."""
        result = await project_agent.process(sample_project_data)
        
        assert "error" not in result
        assert result["project_name"] == "Office Building Electrical Upgrade"
        assert result["project_type"] == "renovation"  # "upgrade" is detected first
        assert result["location"]["address"] == "123 Business Park Drive, Suite 200"
        assert result["technical_details"]["square_footage"] == 10000
        assert result["technical_details"]["voltage_requirements"] == "240V"
        assert result["technical_details"]["permit_required"] is True
        assert len(result["specifications"]) > 0
        assert "400 amp panel" in " ".join(result["specifications"])
    
    @pytest.mark.asyncio
    async def test_process_minimal_data(self, project_agent, minimal_project_data):
        """Test processing with minimal data."""
        result = await project_agent.process(minimal_project_data)
        
        assert "error" not in result
        assert result["project_type"] == "residential"
        assert result["timeline"]["estimated_duration"] == "30 days"  # Default
        assert result["technical_details"]["permit_required"] is False
    
    @pytest.mark.asyncio
    async def test_process_raw_text(self, project_agent, raw_text_data):
        """Test processing raw text input."""
        result = await project_agent.process(raw_text_data)
        
        assert "error" not in result
        assert result["project_type"] == "industrial"  # warehouse
        assert result["technical_details"]["square_footage"] == 15000
        assert result["technical_details"]["voltage_requirements"] == "480V three phase"
        assert result["timeline"]["estimated_duration"] == "60 days"  # 2 months
        assert len(result["specifications"]) > 0
    
    def test_extract_project_type(self, project_agent):
        """Test project type extraction."""
        assert project_agent._extract_project_type("office renovation") == "renovation"
        assert project_agent._extract_project_type("new construction project") == "new_construction"
        assert project_agent._extract_project_type("factory upgrade") == "renovation"  # upgrade keyword
        assert project_agent._extract_project_type("hospital wing") == "institutional"
        assert project_agent._extract_project_type("office building") == "commercial"
        assert project_agent._extract_project_type("unknown work") == "general"
    
    def test_extract_voltage_requirements(self, project_agent):
        """Test voltage extraction."""
        assert project_agent._extract_voltage_requirements("need 120V service") == "120V"
        assert project_agent._extract_voltage_requirements("240/480 panel") == "240/480"
        assert project_agent._extract_voltage_requirements("three phase power") == "three phase"
        assert project_agent._extract_voltage_requirements("no voltage info") is None
    
    def test_extract_square_footage(self, project_agent):
        """Test square footage extraction."""
        assert project_agent._extract_square_footage("5000 sq ft building") == 5000
        assert project_agent._extract_square_footage("12,500 square feet") == 12500
        assert project_agent._extract_square_footage("1500sf space") == 1500
        assert project_agent._extract_square_footage("no size info") is None
    
    def test_parse_duration(self, project_agent):
        """Test duration parsing."""
        assert project_agent._parse_duration("3 weeks") == 21
        assert project_agent._parse_duration("2 months") == 60
        assert project_agent._parse_duration("45 days") == 45
        assert project_agent._parse_duration("1 week") == 7
        assert project_agent._parse_duration("unknown") == 30  # Default
    
    def test_extract_specifications(self, project_agent):
        """Test specification extraction."""
        text = "Install 10 new outlets, upgrade main panel to 200 amp, add lighting in 3 rooms"
        specs = project_agent._extract_specifications(text)
        
        assert len(specs) > 0
        assert any("10 new outlets" in spec for spec in specs)
        assert any("200 amp" in spec for spec in specs)
    
    @pytest.mark.asyncio
    async def test_timeline_calculation(self, project_agent, sample_project_data):
        """Test timeline calculations."""
        result = await project_agent.process(sample_project_data)
        
        timeline = result["timeline"]
        start = datetime.fromisoformat(timeline["start_date"])
        completion = datetime.fromisoformat(timeline["completion_date"])
        
        # 6 weeks = 42 days
        assert (completion - start).days == 42
        assert timeline["estimated_duration"] == "42 days"
    
    @pytest.mark.asyncio
    async def test_permit_detection(self, project_agent):
        """Test permit requirement detection."""
        # Commercial should require permit
        commercial = await project_agent.process({"project_description": "office building work"})
        assert commercial["technical_details"]["permit_required"] is True
        
        # Residential typically doesn't require permit
        residential = await project_agent.process({"project_description": "home outlet installation"})
        assert residential["technical_details"]["permit_required"] is False
        
        # Explicit mention should require permit
        explicit = await project_agent.process({"project_description": "work requiring permit"})
        assert explicit["technical_details"]["permit_required"] is True
    
    @pytest.mark.asyncio
    async def test_project_summary_generation(self, project_agent, sample_project_data):
        """Test project summary generation."""
        result = await project_agent.process(sample_project_data)
        summary = result["project_summary"]
        
        assert "Renovation project" in summary
        assert "10,000 sq ft" in summary
        assert "240V" in summary
        assert "42 days" in summary
        assert "Permit required" in summary
    
    def test_state_management(self, project_agent, sample_project_data):
        """Test agent state is properly managed."""
        # Initial state
        assert project_agent.state.project_name is None
        assert project_agent.state.square_footage is None
        
        # After processing
        import asyncio
        asyncio.run(project_agent.process(sample_project_data))
        
        assert project_agent.state.project_name == "Office Building Electrical Upgrade"
        assert project_agent.state.square_footage == 10000
        assert project_agent.state.voltage_requirements == "240V"
        assert project_agent.state.permit_required is True