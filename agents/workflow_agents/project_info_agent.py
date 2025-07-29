from typing import Any, Dict, Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import re

from shared.models.base import BaseAgent, AgentState


class ProjectInfoState(AgentState):
    """State model for ProjectInfoAgent."""
    project_name: Optional[str] = None
    project_type: Optional[str] = None
    location: Optional[Dict[str, str]] = None
    start_date: Optional[datetime] = None
    estimated_duration_days: Optional[int] = None
    specifications: Optional[List[str]] = None
    square_footage: Optional[int] = None
    voltage_requirements: Optional[str] = None
    permit_required: bool = False


class ProjectInfoAgent(BaseAgent):
    """Workflow agent for extracting and structuring project information."""
    
    def __init__(self):
        super().__init__(name="ProjectInfoAgent")
        self._state = ProjectInfoState()
        
        # Common project types (order matters - check more specific types first)
        self.project_types = [
            ("new_construction", ["new build", "new construction", "ground up", "new development"]),
            ("renovation", ["remodel", "renovation", "upgrade", "retrofit", "modernization"]),
            ("industrial", ["factory", "warehouse", "plant", "industrial", "manufacturing"]),
            ("commercial", ["office", "retail", "store", "shop", "commercial", "business"]),
            ("institutional", ["school", "hospital", "church", "government", "institutional"]),
            ("residential", ["home", "house", "apartment", "condo", "residential"])
        ]
        
        # Voltage patterns (order matters - match more specific patterns first)
        self.voltage_patterns = [
            r"(\d{2,3}[vV]\s*(?:three|3)\s*phase)",  # 480V three phase
            r"(\d{2,3}[vV]\s*(?:single|1)\s*phase)",  # 120V single phase
            r"(\d{2,3})\s*[vV]",  # 120V, 240V
            r"(\d{2,3})/(\d{2,3})",  # 120/240
            r"(\d+)\s*phase",  # 3 phase
            r"single\s*phase",
            r"three\s*phase"
        ]
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data for project info extraction.
        
        Args:
            input_data: Must contain project_description or project_name
            
        Returns:
            True if valid, False otherwise
        """
        return any(field in input_data for field in ["project_description", "project_name", "raw_text"])
    
    def _extract_project_type(self, text: str) -> str:
        """Extract project type from text description."""
        text_lower = text.lower()
        
        for proj_type, keywords in self.project_types:
            for keyword in keywords:
                if keyword in text_lower:
                    return proj_type
        
        return "general"
    
    def _extract_voltage_requirements(self, text: str) -> Optional[str]:
        """Extract voltage requirements from text."""
        for pattern in self.voltage_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        return None
    
    def _extract_square_footage(self, text: str) -> Optional[int]:
        """Extract square footage from text."""
        patterns = [
            r"(\d{1,3}(?:,\d{3})*)\s*(?:sq\.?|square)\s*(?:ft|feet|foot)",  # With comma: 12,500 square feet
            r"(\d{1,6})\s*(?:sq\.?|square)\s*(?:ft|feet|foot)",  # No comma: 5000 sq ft
            r"(\d{1,6})\s*(?:sf|sqft)"  # Abbreviated: 1500sf
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Remove commas before converting to int
                number_str = match.group(1).replace(",", "")
                try:
                    return int(number_str)
                except ValueError:
                    continue
        return None
    
    def _parse_duration(self, duration_text: str) -> int:
        """Parse duration text into days."""
        duration_text = duration_text.lower()
        
        # Look for weeks
        weeks_match = re.search(r"(\d+)\s*weeks?", duration_text)
        if weeks_match:
            return int(weeks_match.group(1)) * 7
        
        # Look for months
        months_match = re.search(r"(\d+)\s*months?", duration_text)
        if months_match:
            return int(months_match.group(1)) * 30
        
        # Look for days
        days_match = re.search(r"(\d+)\s*days?", duration_text)
        if days_match:
            return int(days_match.group(1))
        
        # Default to 30 days if not specified
        return 30
    
    def _extract_specifications(self, text: str) -> List[str]:
        """Extract project specifications from text."""
        specs = []
        
        # Common electrical specifications to look for
        spec_patterns = [
            r"install\s+(\d+)\s+([^,.\n]+)",
            r"upgrade\s+([^,.\n]+)",
            r"replace\s+([^,.\n]+)",
            r"add\s+(\d+)?\s*([^,.\n]+)",
            r"new\s+([^,.\n]+)",
            r"(\d+)\s*amp\s+([^,.\n]+)",
            r"lighting\s+([^,.\n]+)",
            r"panel\s+([^,.\n]+)",
            r"outlet[s]?\s+([^,.\n]+)",
            r"circuit[s]?\s+([^,.\n]+)"
        ]
        
        for pattern in spec_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    spec = " ".join(str(m) for m in match if m).strip()
                else:
                    spec = str(match).strip()
                if spec and len(spec) > 3:  # Avoid very short matches
                    specs.append(spec[:100])  # Limit length
        
        # Remove duplicates while preserving order
        seen = set()
        unique_specs = []
        for spec in specs:
            if spec.lower() not in seen:
                seen.add(spec.lower())
                unique_specs.append(spec)
        
        return unique_specs[:10]  # Limit to 10 specifications
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data to extract project information.
        
        Args:
            input_data: Contains project description, raw text, or structured data
            
        Returns:
            Dict containing extracted project information
        """
        if not self.validate_input(input_data):
            self._state.error = "Missing required fields: project_description, project_name, or raw_text"
            return {"error": self._state.error}
        
        # Get text to analyze
        text = (
            input_data.get("project_description", "") or 
            input_data.get("raw_text", "") or 
            input_data.get("project_name", "")
        )
        
        # Extract project name
        self._state.project_name = (
            input_data.get("project_name") or 
            input_data.get("project_title") or 
            f"Project-{datetime.utcnow().strftime('%Y%m%d')}"
        )
        
        # Extract project type
        self._state.project_type = self._extract_project_type(text)
        
        # Extract location
        location_data = input_data.get("location", {})
        if isinstance(location_data, str):
            self._state.location = {"address": location_data}
        elif isinstance(location_data, dict):
            self._state.location = location_data
        else:
            self._state.location = {"address": "To be determined"}
        
        # Extract dates
        if "start_date" in input_data:
            try:
                self._state.start_date = datetime.fromisoformat(input_data["start_date"])
            except:
                self._state.start_date = datetime.utcnow() + timedelta(days=7)  # Default to 1 week from now
        else:
            self._state.start_date = datetime.utcnow() + timedelta(days=7)
        
        # Extract duration
        duration_text = input_data.get("duration", "") or input_data.get("estimated_duration", "")
        if not duration_text:
            # Try to extract from the main text
            duration_match = re.search(r"(?:take|last|duration|about)\s+(?:about\s+)?(\d+\s*(?:weeks?|months?|days?))", text, re.IGNORECASE)
            if duration_match:
                duration_text = duration_match.group(1)
        
        if duration_text:
            self._state.estimated_duration_days = self._parse_duration(duration_text)
        else:
            self._state.estimated_duration_days = 30  # Default
        
        # Extract technical details
        self._state.square_footage = self._extract_square_footage(text)
        self._state.voltage_requirements = self._extract_voltage_requirements(text)
        
        # Extract specifications
        self._state.specifications = self._extract_specifications(text)
        if not self._state.specifications and "specifications" in input_data:
            self._state.specifications = input_data["specifications"]
        
        # Determine if permit is required
        self._state.permit_required = (
            self._state.project_type in ["commercial", "industrial", "new_construction"] or
            "permit" in text.lower() or
            input_data.get("permit_required", False)
        )
        
        # Build response
        project_info = {
            "project_name": self._state.project_name,
            "project_type": self._state.project_type,
            "location": self._state.location,
            "timeline": {
                "start_date": self._state.start_date.isoformat(),
                "estimated_duration": f"{self._state.estimated_duration_days} days",
                "completion_date": (
                    self._state.start_date + timedelta(days=self._state.estimated_duration_days)
                ).isoformat()
            },
            "technical_details": {
                "square_footage": self._state.square_footage,
                "voltage_requirements": self._state.voltage_requirements,
                "permit_required": self._state.permit_required
            },
            "specifications": self._state.specifications,
            "project_summary": self._generate_summary()
        }
        
        return project_info
    
    def _generate_summary(self) -> str:
        """Generate a project summary from extracted information."""
        parts = []
        
        # Project type and name
        parts.append(f"{self._state.project_type.replace('_', ' ').title()} project: {self._state.project_name}")
        
        # Location
        if self._state.location:
            location_str = self._state.location.get("address", "Location TBD")
            parts.append(f"Location: {location_str}")
        
        # Size
        if self._state.square_footage:
            parts.append(f"Size: {self._state.square_footage:,} sq ft")
        
        # Voltage
        if self._state.voltage_requirements:
            parts.append(f"Voltage: {self._state.voltage_requirements}")
        
        # Timeline
        parts.append(f"Duration: {self._state.estimated_duration_days} days")
        
        # Permit
        if self._state.permit_required:
            parts.append("Permit required")
        
        return " | ".join(parts)