# 🔄 Development Workflow Guide - Claude Code + GitHub Integration

## 🚀 Quick Start Workflow

### 1. Initial Setup (One-Time)
```bash
# Clone the repository
git clone https://github.com/infrateki/electrical-quotation-automation.git
cd electrical-quotation-automation

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Start Docker services
docker-compose up -d

# Run initial migrations
python scripts/setup_database.py

# Verify setup
python scripts/health_check.py
```

### 2. Daily Development Flow
```bash
# Start your day
git pull origin main
docker-compose up -d
source venv/bin/activate

# Create feature branch
git checkout -b feature/agent-name

# Open in Cursor IDE
cursor .

# Start Claude Code monitoring
claude-code watch --auto-test
```

## 📝 Feature Development Workflow

### Step 1: Plan with Claude Code
In Cursor IDE terminal:
```bash
# Set context for your task
claude-code context --task "Implement HeaderAgent that extracts company branding info"

# Get implementation plan
claude-code plan --detailed
```

### Step 2: Generate Agent Structure
```bash
# Generate agent with tests
claude-code create-agent \
  --name "HeaderAgent" \
  --type "simple" \
  --generates "header_section" \
  --test-cases 5

# This creates:
# - agents/simple_agents/header_agent.py
# - tests/unit/agents/test_header_agent.py
# - tests/fixtures/header_agent_fixtures.json
```

### Step 3: Implement Core Logic
Ask Claude Code in Cursor:
```
Implement the process method for HeaderAgent that:
1. Extracts company name, logo URL, license numbers
2. Validates all required fields are present
3. Formats data according to template requirements
4. Handles missing data gracefully
5. Caches results for repeated calls

Include proper error handling and logging.
```

### Step 4: Test Driven Development
```bash
# Run tests in watch mode
claude-code test --watch agents/simple_agents/header_agent.py

# Run specific test
pytest tests/unit/agents/test_header_agent.py -v

# Check coverage
pytest --cov=agents.simple_agents.header_agent --cov-report=html
```

### Step 5: Integration Testing
```bash
# Test agent in workflow
claude-code test-workflow \
  --agents "HeaderAgent,FooterAgent" \
  --input "tests/fixtures/sample_project.json"

# Debug if needed
claude-code debug-agent \
  --name "HeaderAgent" \
  --breakpoint "process" \
  --state "debug_state.json"
```

### Step 6: Commit and Push
```bash
# Format code
black agents/ tests/
isort agents/ tests/

# Type checking
mypy agents/simple_agents/header_agent.py

# Lint
flake8 agents/simple_agents/header_agent.py

# Commit with conventional commits
git add .
git commit -m "feat(agents): implement HeaderAgent with company branding extraction

- Extract company name, logo, and license numbers
- Add caching for repeated calls
- Include comprehensive error handling
- Add unit tests with 95% coverage"

# Push feature branch
git push origin feature/header-agent
```

## 🔄 GitHub Actions Integration

### Automatic CI/CD Pipeline
When you push, GitHub Actions automatically:

1. **Linting & Formatting** (2 min)
   - Black formatting check
   - isort import ordering
   - flake8 linting
   - mypy type checking

2. **Testing** (5 min)
   - Unit tests with pytest
   - Integration tests
   - Coverage report (must be >80%)

3. **Security Scanning** (3 min)
   - Dependency vulnerability scan
   - Code security analysis
   - License compliance

4. **Build & Deploy** (5 min)
   - Docker image build
   - Deploy to staging (if main branch)
   - Run smoke tests

### Pull Request Workflow
```bash
# Create PR from feature branch
# GitHub automatically:
# 1. Runs all CI checks
# 2. Generates coverage report
# 3. Posts Claude Code analysis comments
# 4. Checks for merge conflicts

# After PR approval and merge:
# 1. Deploys to staging automatically
# 2. Runs full integration test suite
# 3. Notifies team in Slack
```

## 🧪 Testing Strategies

### Unit Testing Pattern
```python
# Ask Claude Code to generate tests like this:
"""
Generate comprehensive unit tests for HeaderAgent including:
1. Happy path with complete data
2. Missing required fields
3. Invalid data formats
4. Empty inputs
5. Cache hit/miss scenarios
6. Concurrent access tests
"""
```

### Integration Testing
```bash
# Test complete workflow
claude-code test-integration \
  --scenario "complete-quotation" \
  --agents "all" \
  --parallel

# Test specific integration
claude-code test-integration \
  --from "ProjectInfoAgent" \
  --to "LineItemsAgent" \
  --fixture "complex_project.json"
```

### Performance Testing
```bash
# Profile agent performance
claude-code profile \
  --agent "LineItemsAgent" \
  --iterations 1000 \
  --concurrent 10 \
  --report "performance.html"

# Load test API endpoints
claude-code load-test \
  --endpoint "/api/quotations" \
  --users 100 \
  --duration "5m"
```

## 🐛 Debugging Workflow

### Local Debugging
```python
# In Cursor, ask Claude Code:
"""
Add comprehensive debugging to LineItemsAgent:
1. Log entry/exit with state snapshots
2. Add breakpoints at key decision points
3. Include performance timing
4. Capture all external API calls
5. Enable debug mode via environment variable
"""
```

### Remote Debugging
```bash
# Connect to staging logs
claude-code logs --env staging --tail --filter "ERROR"

# Replay production issue
claude-code replay \
  --quotation-id "prod-12345" \
  --env staging \
  --debug
```

## 📦 Database Workflow

### Schema Changes
```bash
# Generate migration
claude-code migrate --create "add_tax_fields_to_line_items"

# Review migration
claude-code migrate --review

# Apply migration
claude-code migrate --up

# Rollback if needed
claude-code migrate --down
```

### Data Management
```bash
# Seed development data
claude-code seed --dataset "large-commercial" --count 100

# Backup before major changes
claude-code backup --all --tag "pre-v2.0"

# Sync Neo4j catalog
claude-code sync-catalog --source "supplier-api" --update
```

## 🔐 Security Workflow

### API Key Rotation
```bash
# Rotate API keys
claude-code rotate-keys --service "openai" --env ".env"

# Update in production
claude-code deploy-secret --name "OPENAI_API_KEY" --env "production"
```

### Security Scanning
```bash
# Scan for vulnerabilities
claude-code security-scan --deep

# Check dependencies
pip-audit

# Update vulnerable packages
claude-code fix-vulnerabilities --auto
```

## 📊 Monitoring & Observability

### Local Development
```bash
# Start monitoring dashboard
claude-code monitor --dashboard --port 8080

# Watch specific metrics
claude-code monitor \
  --metrics "agent-latency,error-rate,throughput" \
  --agents "LineItemsAgent,PricingSummaryAgent"
```

### Production Monitoring
```bash
# Check agent health
claude-code health --env production --all-agents

# View metrics
claude-code metrics \
  --env production \
  --period "last-24h" \
  --export "report.pdf"
```

## 🚢 Deployment Workflow

### Staging Deployment
```bash
# Automatic on merge to main
# Manual deployment:
claude-code deploy --env staging --version "git-hash"

# Run smoke tests
claude-code smoke-test --env staging
```

### Production Deployment
```bash
# Create release
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# GitHub Actions automatically:
# 1. Builds production images
# 2. Runs full test suite
# 3. Creates release notes
# 4. Deploys with blue-green strategy

# Verify deployment
claude-code verify --env production --comprehensive
```

## 💡 Best Practices

### 1. Branch Naming
- `feature/agent-name` - New agents
- `fix/issue-description` - Bug fixes
- `refactor/component-name` - Code improvements
- `docs/what-updated` - Documentation

### 2. Commit Messages
```bash
feat(agents): add HeaderAgent with caching
fix(api): handle null values in quotation endpoint
refactor(db): optimize Neo4j queries for performance
docs(claude): update command examples
test(integration): add workflow validation tests
```

### 3. Code Review Checklist
- [ ] Tests pass with >80% coverage
- [ ] Type hints on all functions
- [ ] Docstrings updated
- [ ] No hardcoded values
- [ ] Error handling comprehensive
- [ ] Performance acceptable
- [ ] Security considered

### 4. Documentation Updates
Always update when:
- Adding new agents
- Changing API contracts
- Modifying workflows
- Adding dependencies
- Changing configuration

## 🆘 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Regenerate __init__.py files
claude-code fix-imports --auto

# Verify Python path
python -c "import sys; print(sys.path)"
```

#### 2. Database Connection
```bash
# Check services
docker-compose ps

# Restart specific service
docker-compose restart postgres

# View logs
docker-compose logs -f neo4j
```

#### 3. Test Failures
```bash
# Run with verbose output
pytest -vvs tests/unit/agents/test_header_agent.py

# Debug specific test
pytest --pdb tests/unit/agents/test_header_agent.py::test_missing_fields
```

#### 4. Performance Issues
```bash
# Profile code
claude-code profile --agent "SlowAgent" --visualize

# Check database queries
claude-code analyze-queries --slow --limit 10
```

## 📅 Weekly Maintenance

### Monday - Planning
1. Review metrics from previous week
2. Plan feature development
3. Update project board

### Wednesday - Quality Check
1. Run full test suite
2. Update dependencies
3. Review security alerts

### Friday - Optimization
1. Profile agent performance
2. Optimize slow queries
3. Clean up technical debt

Remember: The key to success is consistent application of these workflows. Let Claude Code handle the heavy lifting while you focus on the business logic!
