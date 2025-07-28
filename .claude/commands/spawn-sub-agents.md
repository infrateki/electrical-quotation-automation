# Spawn Sub-Agents for $ARGUMENTS

Create and manage sub-agents for complex parallel tasks:

1. **Analyze Task Complexity**
   - Determine if task needs sub-agents
   - Identify parallelizable components
   - Estimate resource requirements
   - Plan coordination strategy

2. **Design Sub-Agent Architecture**
   ```python
   sub_agents = [
       {
           "name": "sub_agent_1",
           "task": "specific_subtask",
           "input": filtered_data,
           "thinking_mode": "think",
           "timeout": 60
       },
       # ... more sub-agents
   ]
   ```

3. **Spawn Sub-Agents**
   - Create isolated execution contexts
   - Assign specific responsibilities
   - Set resource limits
   - Configure communication channels

4. **Coordinate Execution**
   - Launch agents in parallel
   - Monitor progress
   - Handle inter-agent communication
   - Manage shared state safely

5. **Aggregate Results**
   - Collect outputs from all sub-agents
   - Resolve any conflicts
   - Merge data appropriately
   - Validate combined output

6. **Error Handling**
   - Implement timeout handling
   - Retry failed sub-agents
   - Graceful degradation
   - Report partial results

Use for:
- Line Items Agent (4 sub-agents)
- Large data processing
- Complex calculations
- Multi-source integrations