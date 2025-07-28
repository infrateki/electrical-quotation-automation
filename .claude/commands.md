# 📚 Claude Code Commands Guide - Electrical Quotation Automation

## 🎮 Core Claude Code Commands

### Project Navigation & Understanding
```bash
# Understand the entire codebase structure
claude-code map

# Get context about specific modules
claude-code explain agents/orchestrator/

# Find relationships between components
claude-code trace --from "HeaderAgent" --to "QuotationState"

# Search for specific patterns or implementations
claude-code search "async def process"
```

### Code Generation Commands
```bash
# Generate a new agent with full implementation
claude-code create-agent --name "TaxCalculatorAgent" --type "workflow" --integrates-with "PricingSummaryAgent"

# Generate test cases for an agent
claude-code generate-tests --agent "HeaderAgent" --coverage 90

# Create database models
claude-code create-model --name "ElectricalComponent" --db "neo4j" --relationships "manufacturer,category,specifications"

# Generate API endpoints
claude-code create-endpoint --path "/quotations/{id}/line-items" --method "POST" --agent "LineItemsAgent"
```

### Development Workflow Commands
```bash
# Start development environment
claude-code dev --services "postgres,neo4j,redis"

# Run specific agent in isolation
claude-code run-agent --name "HeaderAgent" --input "test_data.json" --debug

# Watch for changes and auto-reload
claude-code watch --agents --hot-reload

# Generate migration files
claude-code migrate --create "add_compliance_fields"
```

### Testing & Debugging
```bash
# Run comprehensive test suite
claude-code test --all --coverage --parallel

# Debug specific workflow
claude-code debug-workflow --quotation-id "12345" --breakpoint "LineItemsAgent"

# Analyze performance bottlenecks
claude-code profile --agent "LineItemsAgent" --iterations 100

# Validate NEC compliance
claude-code validate-compliance --quotation "output.json" --nec-version "2023"
```

### Multi-Agent Orchestration
```bash
# Visualize agent communication flow
claude-code visualize --workflow "complete-quotation"

# Spawn sub-agents dynamically
claude-code spawn-sub-agents --parent "LineItemsAgent" --count 4 --type "specialized"

# Monitor agent health
claude-code monitor --realtime --metrics "latency,errors,throughput"

# Replay failed workflows
claude-code replay --failed --last-24h
```

## 🚀 Advanced Command Patterns

### Context-Aware Development
```bash
# Let Claude Code understand your current task
claude-code context --task "implement pricing calculation with 15% markup and tax integration"

# Get implementation suggestions based on context
claude-code suggest --for "current-file" --style "best-practices"

# Auto-complete complex implementations
claude-code complete --partial-code "async def calculate_load"
```

### Database Operations
```bash
# Query Neo4j graph for components
claude-code query-graph --cypher "MATCH (c:Component)-[:MANUFACTURED_BY]->(m:Manufacturer) WHERE m.name = 'Siemens' RETURN c"

# Populate test data
claude-code seed-db --dataset "commercial-project" --size "large"

# Backup and restore state
claude-code backup --include "postgres,neo4j" --tag "v1.0"
```

### Integration Commands
```bash
# Connect to external pricing APIs
claude-code integrate --service "pricing-api" --credentials ".env"

# Sync with component catalogs
claude-code sync-catalog --source "manufacturer-api" --target "neo4j"

# Generate OpenAPI documentation
claude-code generate-docs --format "openapi" --version "3.0"
```

## 🎯 Custom Commands (Already in your repo)

### analyze-nec-compliance
Analyzes electrical specifications for NEC 2023 compliance
```bash
claude-code analyze-nec-compliance --file "quotation.json" --report-format "detailed"
```

### debug-agent
Deep debugging for specific agents with state inspection
```bash
claude-code debug-agent --name "LineItemsAgent" --state-snapshot --trace-calls
```

### generate-test-data
Creates realistic test quotations with varied complexity
```bash
claude-code generate-test-data --type "commercial" --components 150 --phases 3
```

### optimize-performance
Identifies and fixes performance bottlenecks
```bash
claude-code optimize-performance --target "sub-30s" --profile "full-quotation"
```

### spawn-sub-agents
Dynamically creates specialized sub-agents for parallel processing
```bash
claude-code spawn-sub-agents --parent "LineItemsAgent" --specializations "motor-control,lighting,hvac,emergency"
```

### validate-quotation
Comprehensive validation of generated quotations
```bash
claude-code validate-quotation --file "output.json" --checks "all"
```

## 💡 Pro Command Combinations

### Complete Development Flow
```bash
# 1. Understand the task
claude-code context --epic "QUOT-123"

# 2. Generate implementation
claude-code create-agent --from-context

# 3. Test immediately  
claude-code test --auto-generated --watch

# 4. Optimize if needed
claude-code optimize-performance --auto-fix
```

### Debugging Production Issues
```bash
# 1. Identify problematic quotation
claude-code logs --error --last-1h | claude-code analyze

# 2. Replay with debugging
claude-code replay --quotation-id "failed-123" --debug --step-through

# 3. Fix and test
claude-code fix --auto --test-before-commit
```

### Rapid Feature Development
```bash
# 1. Describe what you want
claude-code implement "add solar panel calculations to line items agent"

# 2. Review generated code
claude-code diff --preview

# 3. Test with real data
claude-code test --with-fixtures "solar_project.json"

# 4. Deploy with confidence
claude-code deploy --canary 10%
```

## 🔧 Environment Variables for Claude Code

```bash
# Set these in your shell or .env file
export CLAUDE_CODE_PROJECT="electrical-quotation-automation"
export CLAUDE_CODE_CONTEXT="multi-agent-langgraph"
export CLAUDE_CODE_STYLE="async-first,type-safe,tested"
export CLAUDE_CODE_VERBOSITY="detailed"
export CLAUDE_CODE_AUTO_TEST="true"
export CLAUDE_CODE_AI_MODEL="claude-3-sonnet"
```

## 📊 Command Metrics & Monitoring

```bash
# View command usage stats
claude-code stats --my-usage --last-7d

# Monitor resource consumption
claude-code resources --realtime

# Track code quality metrics
claude-code quality --report --trends
```

## 🆘 Troubleshooting Commands

```bash
# General health check
claude-code doctor

# Fix common issues
claude-code fix-common --auto

# Reset development environment
claude-code reset --env --preserve-data

# Get help on any command
claude-code help [command]
claude-code explain-error --last
```

## 🎨 Workflow Optimization Tips

1. **Chain Commands**: Use `&&` to chain related commands
   ```bash
   claude-code create-agent --name "NewAgent" && claude-code test --latest && claude-code commit
   ```

2. **Use Aliases**: Create shortcuts for common workflows
   ```bash
   alias cca="claude-code create-agent"
   alias cct="claude-code test --watch"
   ```

3. **Leverage Context**: Always set context before complex tasks
   ```bash
   claude-code context --load "quotation-optimization"
   ```

4. **Monitor Everything**: Keep monitoring dashboard open
   ```bash
   claude-code monitor --dashboard --port 8080
   ```

5. **Document as You Go**: Auto-generate documentation
   ```bash
   claude-code document --auto --on-save
   ```

Remember: Claude Code learns from your patterns. The more consistently you use these commands, the better it becomes at anticipating your needs!
