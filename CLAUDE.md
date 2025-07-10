# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **Context Engineering Axiom Edition** framework - a template and methodology for AI-native development that combines comprehensive context documentation with structured project architecture. The framework enables sophisticated AI-assisted development through two main workflows:

1. **Classic Workflow**: Manual context engineering with CLAUDE.md and documentation
2. **Axiom Protocol**: Structured, self-describing codebase with contracts and manifests

## Core Development Commands

### Initialization
```bash
# Initialize Axiom Protocol for a new project
./init-axiom.sh
```

### PRP (Product Requirements Prompt) Generation
Use these Claude slash commands for complex feature development:
```bash
# Generate a comprehensive PRP with research phase
/generate-prp

# Generate advanced PRP with additional context
/generate-prp-pro  

# Execute an existing PRP
/execute-prp
```

## Critical Development Workflow: Research → Plan → Implement

**NEVER jump straight to coding!** Always follow this mandatory sequence:

### 1. Research Phase (Mandatory First Step)
Before any implementation, you MUST gather comprehensive context:

- **Check for Axiom Protocol**: If `.axiom-manifest.yml` exists, read it first as the authoritative architecture source
- **Read module contracts**: For any existing module you're modifying, read its `*.contract.yml` file
- **Study existing patterns**: Examine `PRPs/` and `examples/` directories for similar implementations
- **Review documentation**: Read `README.md`, `PLANNING.md`, and any relevant feature documentation

### 2. Planning Phase
For complex features (3+ components or files):
- **Generate a PRP**: Use `/generate-prp` to create comprehensive requirements
- **Define validation criteria**: Establish clear success metrics and testing approach
- **Map dependencies**: Identify required components and their interactions
- **Plan in phases**: Break complex work into validatable increments

### 3. Implementation Phase
- **Follow contracts**: Respect existing `*.contract.yml` definitions
- **Create contracts for new modules**: Use `templates/axiom/CONTRACT.yml.tpl` for non-trivial functions
- **Maintain architectural boundaries**: Place files in correct component directories per manifest
- **Validate iteratively**: Test after each major component, not just at the end

## Axiom Protocol Integration

When the Axiom Protocol is active (`.axiom-manifest.yml` exists):

### Architecture Adherence
- **Respect the manifest**: Follow component structure and dependencies defined in `.axiom-manifest.yml`
- **Update contracts**: When modifying module logic, update corresponding `*.contract.yml` files
- **Use defined commands**: Execute install, run, test, and lint commands as specified in manifest

### Contract-Driven Development
- **Read before modify**: Always read a module's contract before using or changing it
- **Sync code and contracts**: Code changes must be reflected in contract updates
- **Create contracts for new modules**: Any non-trivial function needs a corresponding contract

## File Organization Standards

### Size Limits
- **No file over 500 lines**: Refactor large files into focused, single-purpose modules
- **Module cohesion**: Group related functionality, separate distinct concerns

### Directory Structure
```
.claude/commands/     # Claude slash commands
PRPs/                 # Product Requirements Prompts and examples
templates/axiom/      # Axiom Protocol templates
examples/             # Implementation examples and patterns
```

## Quality and Validation

### Testing Strategy
- **Create unit tests for new features**: Tests should live in `/tests` mirroring main structure
- **Validate contract promises**: Tests should verify the guarantees made in `*.contract.yml` files
- **Use defined test commands**: Run tests using commands specified in `.axiom-manifest.yml`

### Code Quality
- **Follow existing patterns**: Study similar implementations in `examples/` and `PRPs/`
- **Use structured commits**: Include AI reasoning and tool trail in commit messages
- **Validate early and often**: Don't wait until completion to test components

## PRP (Product Requirements Prompt) Usage

### When to Generate PRPs
- Complex features requiring multiple components
- New architectural patterns
- Features with significant user interaction
- Systems requiring extensive validation

### PRP Structure Understanding
PRPs include:
- **Comprehensive context gathering requirements**
- **Detailed implementation blueprints**
- **Progressive complexity approaches**
- **Validation loops and testing strategies**
- **Anti-patterns and gotchas documentation**

## Advanced AI Collaboration

### Multi-Agent Workflows
- **Spawn agents for parallel research**: Use Task tool for independent exploration
- **Delegate complex analysis**: Use agents for large codebase understanding
- **Coordinate implementation**: One agent for tests, another for implementation

### External Tool Integration
- **Use Gemini for large context**: When analyzing entire codebases beyond Claude's context window
- **Leverage web research**: Fetch documentation and examples as needed
- **Tool trail documentation**: Record tools used in commit messages

## Error Recovery and Debugging

### Validation Failures
- **Read error messages carefully**: Don't assume - understand the specific failure
- **Check contracts first**: Verify module interfaces match expectations
- **Validate incrementally**: Test components in isolation before integration
- **Use progressive enhancement**: Start with minimal viable implementation, then enhance

### Context Management
- **Re-read CLAUDE.md periodically**: Especially after 30+ minutes of work
- **Update working memory**: Document progress in PROGRESS.md for long sessions
- **Maintain TODO.md**: Track current tasks, completed work, and next steps

## Framework-Specific Patterns

### Context as King
This framework prioritizes comprehensive context over rapid prototyping:
- **Examples are authoritative**: Learn patterns from `PRPs/` and `examples/`
- **Documentation is executable**: Use PRPs as implementation blueprints
- **Validation drives development**: Success criteria determine implementation approach

### Contract-First Development
When using Axiom Protocol:
- **Contracts define interfaces**: Module behavior is specified in `*.contract.yml`
- **Implementation follows contracts**: Code must fulfill contract promises
- **Changes require contract updates**: Interface modifications need contract synchronization

Remember: This framework enables sophisticated AI-human collaboration through structured context and validation. Always gather comprehensive context before coding, and use the framework's patterns and examples as your guide.