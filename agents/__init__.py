# ProQuote Agent Package

This package contains all the AI agents for the ProQuote electrical quotation automation system.

## Agent Types

### Orchestrator
The main supervisor agent that coordinates all other agents.

### Simple Agents
Template-based agents for basic data extraction and formatting:
- HeaderAgent
- FooterAgent
- CompanyInfoAgent

### Workflow Agents
Logic-based agents with moderate intelligence:
- ProjectInfoAgent
- ContactsAgent
- ApprovalRequirementsAgent

### Advanced Agents
AI-powered agents for complex decision-making:
- LineItemsAgent (with sub-agents)
- PricingSummaryAgent
- ExecutiveSummaryAgent
