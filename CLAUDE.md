# CLAUDE Agent Instructions

## Behavior Guidelines
- Refer to 'comms.md' for goal and action log.
- Read 'comms.md' before actions.
- Log your actions in the Action Log section.
- Coordinate by reviewing logs.
- Keep logs concise.

## Process
- Each agent logs the small step they are executing and specifies the very next step needed.
- The next agent picks up that next step, logs execution, and specifies the subsequent step.
- Repeat until the <goal> is fully implemented.

## Action Logging Protocol
- Agents are designated as Agent 1, Agent 2, or Agent 3.
- Start each log entry with "Agent X:" where X is your assigned number.
- Describe the small step you executed.
- Specify the very next step required.
- Indicate the agent responsible for the next step (e.g., "Next: Agent Y!").
- Review previous logs to ensure continuity and awareness of others' actions.