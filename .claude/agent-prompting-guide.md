# 🧠 Agent Prompt Engineering Guide

## 🎯 Core Principles for Claude Code Agents

### 1. Context is King
Always provide rich context about:
- The specific agent's role in the system
- Dependencies and interactions with other agents
- Business rules and constraints
- Expected input/output formats
- Performance requirements

### 2. Think Step-by-Step
Break down complex tasks into clear steps:
```
1. Validate input state
2. Extract required data
3. Apply business logic
4. Perform calculations
5. Format output
6. Update state
7. Handle errors gracefully
```

### 3. Be Explicit About Requirements
- **Type Safety**: "All functions must have type hints"
- **Error Handling**: "Wrap all external calls in try-except"
- **Testing**: "Include pytest fixtures and test cases"
- **Documentation**: "Add docstrings with examples"

## 📝 Prompt Templates for Common Tasks

### Creating a New Agent
```
Create a {agent_type} agent named {AgentName} that:

Purpose: {specific_purpose}

Inputs:
- {input_1}: {type} - {description}
- {input_2}: {type} - {description}

Processing Steps:
1. {step_1}
2. {step_2}
3. {step_3}

Outputs:
- {output_1}: {type} - {description}

Integration Points:
- Receives data from: {upstream_agent}
- Sends data to: {downstream_agent}
- External APIs: {api_list}

Business Rules:
- {rule_1}
- {rule_2}

Performance Requirements:
- Process within {time_limit}
- Handle {volume} concurrent requests

Include comprehensive error handling, logging, and test cases.
```

### Implementing Complex Business Logic
```
Implement the {feature_name} calculation that:

NEC Compliance:
- Follow NEC {section} for {requirement}
- Apply derating factors from Table {table_number}
- Consider exceptions in {section}

Calculation Steps:
1. Base calculation: {formula}
2. Apply factors: {factors_list}
3. Check limits: {min/max values}
4. Round per code: {rounding_rules}

Edge Cases:
- {edge_case_1}: {handling}
- {edge_case_2}: {handling}

Validation:
- Input ranges: {valid_ranges}
- Output verification: {checks}

Generate test cases covering normal, boundary, and error conditions.
```

### Database Integration
```
Create a {database_type} data access function that:

Operation: {CRUD operation}
Entity: {entity_name}
Database: {postgres|neo4j|redis}

Requirements:
- Use async/await pattern
- Implement connection pooling
- Add retry logic with exponential backoff
- Include transaction management
- Log all operations with timing

Query Optimization:
- {optimization_strategy}
- Expected volume: {records}
- Performance target: {milliseconds}

Error Scenarios:
- Connection timeout
- Constraint violations
- Concurrent updates
- Network failures

Return type: {return_type_specification}
```

## 🔧 Specific Agent Patterns

### Simple Agents (Header, Footer, Company Info)
```python
# Prompt pattern for simple template agents
"""
Create a simple agent that extracts and formats {section_name} information.

Input: Raw company data or user preferences
Output: Formatted {section_name} component

Key behaviors:
- Cache results for identical inputs
- Validate all required fields
- Apply company branding rules
- Support multiple output formats (PDF, HTML, JSON)
"""
```

### Workflow Agents (Project Info, Contacts)
```python
# Prompt pattern for workflow orchestration
"""
Create a workflow agent that manages {workflow_name} process.

State Management:
- Track progress through steps
- Handle rollbacks on failure
- Persist intermediate results
- Emit status events

Coordination:
- Wait for dependencies
- Trigger downstream agents
- Handle timeout scenarios
- Implement circuit breakers
"""
```

### Advanced AI Agents (Line Items, Pricing)
```python
# Prompt pattern for AI-powered analysis
"""
Create an advanced AI agent for {analysis_type}.

AI Integration:
- Prepare prompts with context
- Handle token limits
- Implement fallback strategies
- Cache AI responses

Learning Features:
- Track accuracy metrics
- Identify improvement areas
- Suggest optimizations
- Learn from corrections

Quality Assurance:
- Validate AI outputs
- Apply business constraints
- Flag anomalies
- Request human review when uncertain
"""
```

## 🎨 Output Format Guidelines

### Code Structure
```python
# Always follow this structure for agents
class AgentName(BaseAgent):
    """Clear, concise description.
    
    Detailed explanation of purpose and behavior.
    
    Attributes:
        config: Agent configuration
        logger: Structured logger instance
        
    Example:
        >>> agent = AgentName(config)
        >>> result = await agent.process(state)
    """
    
    def __init__(self, config: AgentConfig):
        """Initialize with configuration."""
        super().__init__(config)
        # Agent-specific initialization
    
    async def process(self, state: QuotationState) -> Dict[str, Any]:
        """Process state and return updates.
        
        Args:
            state: Current quotation state
            
        Returns:
            Dictionary of state updates
            
        Raises:
            ValidationError: If input validation fails
            ProcessingError: If processing fails
        """
        # Implementation
```

### Error Messages
```python
# Use descriptive, actionable error messages
raise ValidationError(
    f"Invalid wire size: {wire_size}AWG for {load}A load. "
    f"Minimum required: {min_size}AWG per NEC Table 310.16"
)
```

### Logging Patterns
```python
# Structured logging with context
self.logger.info(
    "Processing line items",
    agent="LineItemsAgent",
    quotation_id=state.quotation_id,
    item_count=len(items),
    total_value=total
)
```

## 🚀 Advanced Techniques

### Dynamic Prompt Construction
```python
def build_prompt(context: Dict[str, Any]) -> str:
    """Build context-aware prompts dynamically."""
    base_prompt = "Analyze the following electrical specifications:"
    
    if context.get('project_type') == 'industrial':
        base_prompt += "\nConsider industrial voltage levels and motor loads."
    
    if context.get('hazardous_location'):
        base_prompt += "\nApply Class I Division 2 requirements."
    
    return base_prompt
```

### Multi-Shot Examples
When asking Claude Code to generate complex logic, provide multiple examples:
```
Example 1 - Residential:
Input: {residential_input}
Output: {residential_output}

Example 2 - Commercial:
Input: {commercial_input}
Output: {commercial_output}

Example 3 - Industrial:
Input: {industrial_input}
Output: {industrial_output}

Now generate for: {actual_input}
```

### Chain-of-Thought Reasoning
For complex calculations, ask for step-by-step reasoning:
```
Calculate the service size needed:
1. List all loads with descriptions
2. Show individual calculations
3. Apply demand factors with references
4. Sum up with safety margin
5. Select next standard size
6. Verify against NEC minimums
```

## 📊 Testing Prompt Patterns

### Unit Test Generation
```
Generate comprehensive unit tests for {function_name} that cover:

Happy Path:
- Normal inputs with expected outputs
- Various valid configurations

Edge Cases:
- Minimum/maximum values
- Empty/null inputs
- Boundary conditions

Error Cases:
- Invalid inputs
- External service failures
- Timeout scenarios

Use pytest with:
- Fixtures for test data
- Parametrize for multiple cases
- Mock external dependencies
- Assert specific exceptions
```

### Integration Test Scenarios
```
Create integration tests that verify:
1. Agent communication flow
2. State persistence across agents
3. Error propagation
4. Transaction rollback
5. Performance under load
```

## 🎯 Performance Optimization Prompts

### Code Optimization
```
Optimize this code for:
- Execution speed (target: <100ms)
- Memory usage (handle 1000 concurrent)
- Database queries (minimize round trips)
- Caching strategy (Redis integration)

Maintain:
- Readability
- Type safety
- Test coverage
- Error handling
```

### Async Patterns
```
Convert to async with:
- Proper concurrency control
- Connection pooling
- Graceful shutdown
- Backpressure handling
- Progress reporting
```

## 💡 Meta-Prompting Tips

### For Claude Code to Self-Improve
```
After implementing, analyze:
1. What patterns could be reused?
2. What abstractions would help?
3. Where might this fail in production?
4. What monitoring would help?
5. How to make this more maintainable?
```

### For Learning Project Patterns
```
Study the existing codebase and identify:
- Naming conventions
- Error handling patterns
- Testing strategies
- Documentation style
- Performance patterns

Apply these consistently in new code.
```

Remember: The best prompts are specific, contextual, and include examples. The more precise your prompt, the better Claude Code's output will be!
