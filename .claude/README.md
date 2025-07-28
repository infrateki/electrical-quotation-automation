# 🧠 Claude Code Configuration Directory

This directory contains all the essential documentation and commands for Claude Code agents to build and maintain the Electrical Quotation Automation system effectively.

## 📁 Directory Structure

```
.claude/
├── commands/                 # Custom Claude Code commands
│   ├── analyze-nec-compliance.md
│   ├── debug-agent.md
│   ├── generate-test-data.md
│   ├── optimize-performance.md
│   ├── spawn-sub-agents.md
│   └── validate-quotation.md
├── CLAUDE.md                # Main instructions for agent swarm
├── commands.md              # Comprehensive command reference
├── project-context.md       # Domain knowledge & business rules
├── agent-prompting-guide.md # Prompt engineering patterns
├── development-workflow.md  # Step-by-step development process
└── README.md               # This file
```

## 🎯 Purpose of Each File

### 📄 CLAUDE.md
**The Mission Brief** - Start here!
- Project overview and architecture
- Agent hierarchy and responsibilities
- Development standards and patterns
- Key implementation tasks
- Success metrics

### 📄 commands.md
**The Toolbox** - All available commands
- Core Claude Code commands
- Project-specific commands
- Advanced patterns and workflows
- Troubleshooting commands
- Environment setup

### 📄 project-context.md
**The Domain Expert** - Electrical quotation knowledge
- Business domain understanding
- Quotation component breakdowns
- NEC compliance requirements
- Pricing strategies
- Workflow states

### 📄 agent-prompting-guide.md
**The Communication Guide** - How to talk to Claude Code
- Prompt templates for common tasks
- Agent-specific patterns
- Testing prompt patterns
- Performance optimization prompts
- Meta-prompting techniques

### 📄 development-workflow.md
**The Playbook** - Day-to-day development
- Initial setup instructions
- Feature development workflow
- GitHub integration
- Testing strategies
- Deployment procedures

### 📁 commands/
**Custom Tools** - Project-specific commands
Each `.md` file defines a custom command that Claude Code can execute

## 🚀 Getting Started for New Developers

1. **Read in this order:**
   - CLAUDE.md (understand the mission)
   - project-context.md (learn the domain)
   - development-workflow.md (set up environment)
   - commands.md (learn the tools)
   - agent-prompting-guide.md (communicate effectively)

2. **Set up your environment:**
   ```bash
   # Follow the steps in development-workflow.md
   git clone https://github.com/infrateki/electrical-quotation-automation.git
   cd electrical-quotation-automation
   cursor .  # Open in Cursor IDE
   ```

3. **Configure Claude Code:**
   ```bash
   # Set environment variables
   export CLAUDE_CODE_PROJECT="electrical-quotation-automation"
   export CLAUDE_CODE_CONTEXT="multi-agent-langgraph"
   export CLAUDE_CODE_STYLE="async-first,type-safe,tested"
   ```

## 💡 Best Practices

### For Human Developers
1. **Always provide context** - Reference these docs in your prompts
2. **Use specific commands** - Don't reinvent what's already built
3. **Follow the patterns** - Consistency matters for agent learning
4. **Update documentation** - Keep these files current

### For Claude Code Agents
1. **Check project-context.md** - For domain-specific questions
2. **Follow CLAUDE.md standards** - For code quality
3. **Use agent-prompting-guide.md** - For complex implementations
4. **Reference commands.md** - For available tools

## 🔄 Keeping Documentation Updated

When you:
- **Add a new agent** → Update CLAUDE.md with its role
- **Create a new command** → Add to commands/ and update commands.md
- **Learn domain knowledge** → Update project-context.md
- **Discover a pattern** → Add to agent-prompting-guide.md
- **Improve workflow** → Update development-workflow.md

## 🤝 Contributing

### Adding a New Command
1. Create `commands/your-command.md`
2. Follow the existing format:
   ```markdown
   # command-name
   
   Brief description of what the command does.
   
   ## Usage
   ```
   claude-code command-name [options]
   ```
   
   ## Options
   - `--option`: Description
   
   ## Examples
   ```

3. Update `commands.md` with the new command

### Updating Documentation
1. Keep language clear and concise
2. Use examples whenever possible
3. Include both what and why
4. Test any code examples
5. Update the modification date

## 🚨 Important Notes

### For Cursor IDE Integration
- These files are automatically loaded by Claude Code
- They provide context for better code generation
- Updates take effect immediately
- No restart required

### For CI/CD Pipeline
- GitHub Actions read these for automated workflows
- Custom commands are available in CI environment
- Documentation is validated on each commit

## 📊 Documentation Metrics

Track documentation health:
```bash
# Check documentation coverage
claude-code docs --coverage

# Find outdated sections
claude-code docs --check-outdated

# Generate documentation report
claude-code docs --report
```

## 🆘 Help & Support

- **Documentation issues** → Create GitHub issue with `docs` label
- **Command problems** → Check troubleshooting in `commands.md`
- **Workflow questions** → Refer to `development-workflow.md`
- **Domain questions** → Consult `project-context.md`

---

Remember: Well-documented code is a gift to your future self and your team. These files are your blueprint for building an exceptional electrical quotation automation system!

Last Updated: 2025-07-28
