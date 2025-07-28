# 🚀 Electrical Quotation Automation System - Claude Code Agent Instructions

## 🎯 Project Overview
You are part of an elite swarm of Claude Code agents building a sophisticated electrical quotation automation system - think "Gamma.app for electrical contractors". This system uses multi-agent orchestration with LangGraph to automate complex electrical project quotations.

## 🧠 Your Mission
Transform manual electrical quotation processes into an intelligent, automated system that:
- Understands electrical engineering requirements and NEC compliance
- Generates accurate, professional quotations in seconds
- Learns from historical data to improve pricing accuracy
- Handles complex multi-phase commercial projects

## 🏗️ System Architecture

### Core Technologies
- **Agent Framework**: LangGraph (for complex orchestration)
- **API Layer**: FastAPI with WebSocket support
- **Databases**: 
  - PostgreSQL (primary data)
  - Neo4j Aura (electrical component graph)
  - Redis (caching & sessions)
  - Vector DB (semantic search)
- **AI/ML**: OpenAI GPT-4, Claude API integration
- **Infrastructure**: Docker, GitHub Actions, AWS-ready

### Agent Hierarchy
```
Supervisor Agent (Orchestrator)
├── Simple Agents (Level 1)
│   ├── Header Agent
│   ├── Footer Agent
│   └── Company Info Agent
├── Workflow Agents (Level 2)
│   ├── Project Information Agent
│   ├── Contacts Agent
│   └── Approval Requirements Agent
└── Advanced Agents (Level 3)
    ├── Line Items Agent (with 4 sub-agents)
    ├── Pricing Summary Agent
    └── Executive Summary Agent
```

## 📋 Development Standards

### Code Quality Rules
1. **Type Safety**: Use type hints everywhere - Pydantic models for all data
2. **Async First**: All I/O operations must be async
3. **Error Handling**: Every agent must handle failures gracefully
4. **Testing**: 80% code coverage minimum - use pytest
5. **Documentation**: Docstrings for all functions/classes

### Agent Development Pattern
```python
from typing import Dict, Any
from langgraph.graph import StateGraph
from shared.models.base import BaseAgent
from shared.models.state import QuotationState

class YourAgent(BaseAgent):
    """Agent description and capabilities."""
    
    async def process(self, state: QuotationState) -> Dict[str, Any]:
        """Process state and return updates."""
        try:
            # Your logic here
            return {"field": updated_value}
        except Exception as e:
            return {"errors": [str(e)]}
```

### Database Interaction Patterns
- **PostgreSQL**: Use SQLAlchemy async sessions
- **Neo4j**: Use async driver with connection pooling
- **Redis**: Use aioredis for all operations
- **Transactions**: Always use proper transaction boundaries

## 🛠️ Key Implementation Tasks

### Phase 1: Foundation (Current)
- [ ] Set up complete project structure
- [ ] Implement base agent framework
- [ ] Create shared utilities and models
- [ ] Set up Docker development environment
- [ ] Implement CI/CD pipeline

### Phase 2: Simple Agents
- [ ] Header Agent - Company branding extraction
- [ ] Footer Agent - Terms and conditions
- [ ] Company Info Agent - Client data management
- [ ] Basic API endpoints

### Phase 3: Workflow Agents  
- [ ] Project Information Agent - Parse requirements
- [ ] Contacts Agent - Manage stakeholders
- [ ] Approval Requirements Agent - Compliance checks
- [ ] State management with LangGraph

### Phase 4: Advanced AI Agents
- [ ] Line Items Agent with sub-agents:
  - Essential Systems Sub-Agent
  - Normal Power Sub-Agent
  - Specialized Equipment Sub-Agent
  - Backup Power Sub-Agent
- [ ] Pricing Summary Agent
- [ ] Executive Summary Agent

## 🎮 Command Patterns

### Creating New Agents
```bash
claude-code create-agent --name "AgentName" --type "simple|workflow|advanced" --description "What this agent does"
```

### Testing Agents
```bash
claude-code test-agent --name "AgentName" --fixture "test_data.json"
```

### Debugging Workflows
```bash
claude-code debug-workflow --trace --state-file "debug_state.json"
```

## 💡 Pro Tips for Claude Code Agents

### 1. Context Awareness
- Always check `shared/context/` for domain knowledge
- Reference NEC codes in `docs/compliance/`
- Use historical data from `tests/fixtures/`

### 2. State Management
- Never mutate state directly
- Use immutable updates: `return {**state, "field": new_value}`
- Always validate state transitions

### 3. Performance Optimization
- Cache expensive calculations in Redis
- Use batch operations for database queries
- Implement circuit breakers for external APIs

### 4. Error Recovery
- Every agent must be idempotent
- Implement retry logic with exponential backoff
- Log all errors with full context

### 5. Collaboration Patterns
- Use clear commit messages: `feat(agent-name): description`
- Update tests when modifying agents
- Document any NEC compliance considerations

## 🔍 Key Files to Understand

1. **`shared/models/state.py`** - Core state definition
2. **`shared/models/base.py`** - Base agent class
3. **`agents/orchestrator/supervisor.py`** - Main coordinator
4. **`shared/data_access/neo4j_client.py`** - Graph database queries
5. **`api/main.py`** - FastAPI application entry

## 🚨 Critical Business Rules

1. **NEC Compliance**: All electrical calculations must follow NEC 2023
2. **Pricing Accuracy**: Margin of error must be < 3%
3. **Data Privacy**: Never log sensitive customer data
4. **Audit Trail**: Every quotation must be fully traceable
5. **Performance**: Quotation generation < 30 seconds

## 📊 Success Metrics

- **Accuracy**: 97%+ quotation accuracy
- **Speed**: 95% reduction in quotation time
- **Adoption**: 80% user satisfaction
- **Reliability**: 99.9% uptime

## 🆘 Getting Help

1. Check `docs/troubleshooting.md` first
2. Use `claude-code explain-error --trace` for debugging
3. Reference `tests/` for implementation examples
4. Consult Neo4j graph for component relationships

## 🎯 Remember

You're building a system that will revolutionize how electrical contractors create quotations. Every line of code should focus on:
- **Accuracy** - Lives depend on correct electrical calculations
- **Speed** - Time is money in construction
- **Usability** - Contractors aren't programmers
- **Reliability** - Downtime costs deals

Let's build something extraordinary! 🚀
