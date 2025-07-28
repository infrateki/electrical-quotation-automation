# Debug Agent: $ARGUMENTS

Comprehensive debugging for agent issues:

1. **Enable Debug Mode**
   ```bash
   export AGENT_DEBUG=true
   export LOG_LEVEL=DEBUG
   ```

2. **Trace Execution Flow**
   - Add entry/exit logging
   - Log all state changes
   - Track message passing
   - Monitor resource usage

3. **Inspect State**
   ```python
   # Pretty print current state
   print(json.dumps(state, indent=2))
   
   # Check state consistency
   validate_state_integrity(state)
   
   # Trace state mutations
   log_state_changes(before, after)
   ```

4. **Debug Common Issues**
   - **Stuck agents**: Check for deadlocks
   - **Wrong output**: Validate transformations
   - **Performance**: Profile hot paths
   - **Errors**: Analyze stack traces
   - **Communication**: Trace messages

5. **Interactive Debugging**
   ```python
   import pdb
   pdb.set_trace()  # Breakpoint
   
   # Or use ipdb for better experience
   import ipdb
   ipdb.set_trace()
   ```

6. **Generate Debug Report**
   - Execution timeline
   - State snapshots
   - Error analysis
   - Performance metrics
   - Recommendations

Output debug logs to `logs/debug/agent_name/`