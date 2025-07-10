# AI-Native Development Guidelines

This document provides AI-optimized development instructions for projects using the Axiom Protocol.

## 🤖 AI-First Development Mindset

### Core Principle: AI as Primary Developer
- **AI is the primary coder**, humans provide intent and validation
- **Optimize for AI understanding**, not human reading convenience
- **Minimize token consumption** while maximizing context richness
- **Automate metadata maintenance** to support continuous AI context

### Context Engineering Priority
1. **Always read `.axiom/index.yml` first** - This contains AI-optimized project overview
2. **Check `.axiom/meta/` directory** - Contains file-specific AI context for rapid understanding
3. **Use meta information** - Read file meta before reading actual source code to save tokens
4. **Maintain context consistency** - Update meta files whenever you modify source code

## 🏗️ AI-Optimized Code Architecture

### Extreme Modularity (AI-Native)
- **Maximum 200 lines per file** - Enable rapid AI comprehension
- **Single responsibility principle** - Each file does exactly one thing
- **Minimal dependencies** - Reduce cognitive load for AI analysis
- **Clear interfaces** - Use `.contract.yml` files to define module behavior

### Module Organization Pattern:
```
feature/
├── core.py              # Core logic (< 200 lines)
├── core.contract.yml    # AI-readable interface definition
├── types.py             # Data structures (< 100 lines)
├── utils.py             # Helper functions (< 150 lines)
└── __init__.py          # Public interface (< 50 lines)
```

### Token-Optimized File Structure
- **Front-load important information** - Key logic first, helpers later
- **Use descriptive names** - Reduce need for comments
- **Minimal comments** - Only for complex algorithms or business logic
- **Consistent patterns** - Enable AI pattern recognition across files

## 📊 Axiom Protocol Integration

### Meta Information Maintenance (CRITICAL)
- **After every file modification**, run: `python3 scripts/axiom-meta-generator.py --update <file>`
- **After major changes**, run: `python3 scripts/axiom-meta-generator.py --scan`
- **Check meta sync status** in `.axiom/index.yml` before starting work
- **Never commit** without updating corresponding meta files

### Contract-Driven Development
- **Create `.contract.yml`** for every non-trivial module
- **Define interfaces first** - Establish contracts before implementation
- **Validate against contracts** - Ensure implementation matches promises
- **Update contracts** when interfaces change

### AI-Optimized Dependencies
- **Document all imports** in meta files for AI context
- **Use dependency injection** - Enable easy AI testing and modification
- **Minimize circular dependencies** - Simplify AI dependency analysis
- **Group related dependencies** - Reduce AI context switching

## 🧪 AI-Driven Testing Strategy

### Test Philosophy
- **AI generates comprehensive tests** based on contracts
- **Focus on behavior verification** - Test what, not how
- **Use property-based testing** - Let AI explore edge cases
- **Maintain test meta files** - Help AI understand test coverage

### Test Organization:
```
tests/
├── test_feature_core.py
├── test_feature_core.py.yml    # Meta: test coverage, AI insights
├── test_integration.py
└── conftest.py                 # Shared test utilities
```

## 🔧 AI Development Workflow

### Standard Development Cycle
1. **Read meta context** - `.axiom/index.yml` and relevant meta files
2. **Understand requirements** - PRP or user intent
3. **Design contracts** - Create `.contract.yml` files
4. **Implement incrementally** - Small, testable modules
5. **Update meta files** - Maintain AI context consistency
6. **Validate and test** - Ensure contracts are fulfilled
7. **Sync axiom metadata** - Update project-wide context

### Token Budget Management
- **Track estimated tokens** in `.axiom/index.yml`
- **Prioritize high-impact files** for AI review
- **Use meta summaries** instead of reading full files when possible
- **Batch related changes** to minimize context switching

## 🎯 AI-Specific Code Patterns

### Prefer AI-Friendly Patterns:
```python
# ✅ AI-Friendly: Clear, single purpose
def calculate_user_score(user_data: UserData) -> Score:
    return Score(value=user_data.points * MULTIPLIER)

# ❌ Avoid: Complex, multi-purpose functions
def process_user_and_calculate_stuff(user, options=None, debug=False):
    # Multiple responsibilities, unclear interface
```

### Data Structures:
- **Use dataclasses/pydantic** - Clear structure for AI understanding
- **Explicit typing** - Help AI understand data flow
- **Immutable when possible** - Reduce AI state tracking complexity
- **Small, focused classes** - Enable rapid AI comprehension

### Error Handling:
- **Explicit error types** - Help AI understand failure modes
- **Early returns** - Reduce nesting for AI analysis
- **Structured error responses** - Enable AI error pattern recognition

## 📝 AI Context Documentation

### Meta-First Documentation
- **Rely on meta files** for AI context - Don't duplicate in comments
- **Document intent, not implementation** - Let AI read the code
- **Use structured formats** - YAML/JSON for AI consumption
- **Update meta files atomically** with code changes

### Commit Message Format (AI-Optimized):
```
type(scope): Brief description

AI-Context:
- Meta files updated: [list]
- Token impact: +/- estimated change
- Contracts modified: [list]

Validation:
- Tests: pass/fail
- Meta sync: clean/dirty
```

## 🔄 Continuous AI Context Maintenance

### Daily Maintenance:
- **Morning**: `python3 scripts/axiom-meta-generator.py --scan`
- **After major changes**: Update contracts and meta files
- **Before commits**: Verify meta sync status
- **Weekly**: Review token budget and optimize heavy files

### Context Validation:
- **Meta files exist** for all tracked source files
- **Contracts are current** and match implementation
- **Dependencies are documented** in meta files
- **Token estimates are accurate** in index.yml

## ⚡ AI Performance Optimizations

### Token Efficiency:
- **Use meta summaries** for initial file understanding
- **Read contracts** before source code
- **Batch similar operations** to maintain context
- **Cache AI analysis** in `.axiom/cache/` directory

### AI Assistant Workflow:
1. **Check `.axiom/index.yml`** for project context
2. **Read relevant meta files** for targeted understanding
3. **Use contracts** to understand interfaces
4. **Read minimal source code** only when necessary
5. **Update meta information** after changes
6. **Validate consistency** before completion

## 🚨 Critical AI Guidelines

### Always Required:
- **Update meta files** after every source code change
- **Maintain contract consistency** with implementation
- **Verify token estimates** are reasonable
- **Check meta sync status** before declaring tasks complete
- **Use incremental development** to maintain AI context
- **Validate with tests** before moving to next module

### Never Do:
- **Commit without meta updates** - Breaks AI context continuity
- **Create files > 200 lines** - Exceeds AI comprehension budget
- **Skip contract creation** for complex modules
- **Ignore token budget** warnings in index.yml
- **Modify multiple unrelated files** in single commit

Remember: This is AI-native development. Every decision should optimize for AI understanding, token efficiency, and automated context maintenance.