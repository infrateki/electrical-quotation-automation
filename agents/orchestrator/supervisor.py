from typing import Dict, List, Any, Literal, Annotated
from langgraph.graph import StateGraph, END
import logging

from shared.models.quotation import (
    QuotationState,
    log_agent_execution,
    update_state_timestamp
)
from agents.simple_agents.header_agent import HeaderAgent
from agents.simple_agents.footer_agent import FooterAgent
from agents.simple_agents.company_info_agent import CompanyInfoAgent

# Configure logging
logger = logging.getLogger(__name__)


class QuotationOrchestrator:
    """Main orchestrator that coordinates all agents using LangGraph."""
    
    def __init__(self):
        """Initialize the orchestrator with all available agents."""
        # Initialize simple agents
        self.header_agent = HeaderAgent()
        self.footer_agent = FooterAgent()
        self.company_info_agent = CompanyInfoAgent()
        
        # TODO: Initialize workflow agents
        # self.project_info_agent = ProjectInfoAgent()
        # self.contacts_agent = ContactsAgent()
        
        # TODO: Initialize advanced agents
        # self.line_items_agent = LineItemsAgent()
        # self.pricing_agent = PricingAgent()
        # self.executive_summary_agent = ExecutiveSummaryAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for quotation generation."""
        # Create the graph
        workflow = StateGraph(QuotationState)
        
        # Add nodes for each agent
        workflow.add_node("header", self._run_header_agent)
        workflow.add_node("company_info", self._run_company_info_agent)
        workflow.add_node("footer", self._run_footer_agent)
        workflow.add_node("supervisor", self._supervisor)
        
        # Set the entry point
        workflow.set_entry_point("supervisor")
        
        # Add edges
        workflow.add_edge("supervisor", "header")
        workflow.add_edge("header", "company_info")
        workflow.add_edge("company_info", "footer")
        workflow.add_edge("footer", END)
        
        # TODO: Add more complex routing when additional agents are ready
        # workflow.add_conditional_edges(
        #     "supervisor",
        #     self._route_next_agent,
        #     {
        #         "header": "header",
        #         "company": "company_info",
        #         "project": "project_info",
        #         "line_items": "line_items",
        #         "pricing": "pricing",
        #         "footer": "footer",
        #         "complete": END
        #     }
        # )
        
        return workflow.compile()
    
    async def _run_header_agent(self, state: QuotationState) -> Dict[str, Any]:
        """Execute the header agent."""
        try:
            start_time = self._get_timestamp_ms()
            
            # Prepare input for header agent
            input_data = {
                "company_name": state["company_info"]["name"] or "ProQuote Electrical",
                "prepared_by": state["metadata"]["created_by"],
                "client_name": state["client_info"]["name"],
                "client_contact": state["client_info"]["email"],
                "project_name": state["project_info"]["name"],
                "validity_days": 30  # Default, can be configured
            }
            
            # Run the agent
            result = await self.header_agent.process(input_data)
            
            # Update state
            state["header"] = result
            state["quote_number"] = result.get("quote_number", "")
            
            # Log execution
            execution_time = self._get_timestamp_ms() - start_time
            log_agent_execution(state, "HeaderAgent", "success", execution_time)
            
            logger.info(f"HeaderAgent completed in {execution_time}ms")
            
        except Exception as e:
            logger.error(f"HeaderAgent failed: {str(e)}")
            log_agent_execution(state, "HeaderAgent", "failed", 0, str(e))
            state["errors"].append({"agent": "HeaderAgent", "error": str(e)})
        
        return state
    
    async def _run_company_info_agent(self, state: QuotationState) -> Dict[str, Any]:
        """Execute the company info agent."""
        try:
            start_time = self._get_timestamp_ms()
            
            # Prepare input for company info agent
            input_data = {
                "quotation_id": state["quotation_id"]
            }
            
            # Add any custom company overrides if provided
            if state.get("custom_fields", {}).get("company_overrides"):
                input_data.update(state["custom_fields"]["company_overrides"])
            
            # Run the agent
            result = await self.company_info_agent.process(input_data)
            
            # Update state with company info
            if "company_section" in result:
                company_section = result["company_section"]
                state["company_info"]["name"] = company_section["name"]
                state["company_info"]["address"] = company_section["contact"]["address"]
                state["company_info"]["phone"] = company_section["contact"]["phone"]
                state["company_info"]["email"] = company_section["contact"]["email"]
                state["company_info"]["website"] = company_section["contact"]["website"]
                state["company_info"]["registration_number"] = company_section["legal"]["registration_number"]
                state["company_info"]["tax_id"] = company_section["legal"]["tax_id"]
                
                if "logo_url" in company_section:
                    state["company_info"]["logo_url"] = company_section["logo_url"]
            
            # Log execution
            execution_time = self._get_timestamp_ms() - start_time
            log_agent_execution(state, "CompanyInfoAgent", "success", execution_time)
            
            logger.info(f"CompanyInfoAgent completed in {execution_time}ms")
            
        except Exception as e:
            logger.error(f"CompanyInfoAgent failed: {str(e)}")
            log_agent_execution(state, "CompanyInfoAgent", "failed", 0, str(e))
            state["errors"].append({"agent": "CompanyInfoAgent", "error": str(e)})
        
        return state
    
    async def _run_footer_agent(self, state: QuotationState) -> Dict[str, Any]:
        """Execute the footer agent."""
        try:
            start_time = self._get_timestamp_ms()
            
            # Prepare input for footer agent
            input_data = {
                "quotation_id": state["quotation_id"],
                "validity_days": 30  # Default, can be configured
            }
            
            # Add any custom footer overrides if provided
            if state.get("custom_fields", {}).get("custom_terms"):
                input_data["custom_terms"] = state["custom_fields"]["custom_terms"]
            
            # Run the agent
            result = await self.footer_agent.process(input_data)
            
            # Update state
            state["footer"] = result
            state["terms_and_conditions"] = result.get("terms_and_conditions", "")
            
            # Log execution
            execution_time = self._get_timestamp_ms() - start_time
            log_agent_execution(state, "FooterAgent", "success", execution_time)
            
            logger.info(f"FooterAgent completed in {execution_time}ms")
            
        except Exception as e:
            logger.error(f"FooterAgent failed: {str(e)}")
            log_agent_execution(state, "FooterAgent", "failed", 0, str(e))
            state["errors"].append({"agent": "FooterAgent", "error": str(e)})
        
        return state
    
    async def _supervisor(self, state: QuotationState) -> Dict[str, Any]:
        """Supervisor node that initializes the workflow."""
        logger.info(f"Starting quotation generation for ID: {state['quotation_id']}")
        update_state_timestamp(state)
        return state
    
    def _route_next_agent(self, state: QuotationState) -> str:
        """Determine which agent should run next based on state."""
        # Simple routing logic for now
        # TODO: Implement more sophisticated routing based on state completion
        
        if not state.get("header"):
            return "header"
        elif not state["company_info"]["name"]:
            return "company"
        elif not state.get("footer"):
            return "footer"
        else:
            return "complete"
    
    def _get_timestamp_ms(self) -> int:
        """Get current timestamp in milliseconds."""
        import time
        return int(time.time() * 1000)
    
    async def generate_quotation(self, initial_state: QuotationState) -> QuotationState:
        """Main entry point to generate a quotation.
        
        Args:
            initial_state: Initial quotation state with basic information
            
        Returns:
            Updated quotation state after all agents have run
        """
        try:
            # Run the workflow
            final_state = await self.workflow.ainvoke(initial_state)
            
            # Update status
            final_state["metadata"]["status"] = "generated"
            update_state_timestamp(final_state)
            
            logger.info(f"Quotation generation completed for ID: {final_state['quotation_id']}")
            return final_state
            
        except Exception as e:
            logger.error(f"Quotation generation failed: {str(e)}")
            initial_state["errors"].append({
                "agent": "Orchestrator",
                "error": str(e),
                "fatal": True
            })
            initial_state["metadata"]["status"] = "failed"
            update_state_timestamp(initial_state)
            return initial_state