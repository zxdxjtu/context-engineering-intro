# Context Engineering + Axiom Protocol

This repository provides a supercharged framework for AI-native development, combining two powerful methodologies:

1.  **Context Engineering:** A discipline for providing clear, comprehensive instructions and context *to* an AI.
2.  **Axiom Protocol:** A system for making the codebase itself structured and self-describing *for* an AI.

This combination creates a virtuous cycle: you tell the AI what to do, and the AI can deeply understand the codebase to do it correctly, efficiently, and safely.

> **This is the next evolution of AI-native development: Human-readable instructions meet a machine-readable codebase.**

## 🚀 Two Ways to Get Started

### 1. The Classic Way (Manual Context)

If you want to focus only on providing manual context through prompts and documentation, follow the original workflow.

```bash
# 1. Clone this template
git clone https://github.com/your-repo/context-engineering-axiom-edition.git
cd context-engineering-axiom-edition

# 2. Set up your project rules (optional - template provided)
# Edit CLAUDE.md to add your project-specific guidelines

# 3. Add examples (highly recommended)
# Place relevant code examples in the examples/ folder

# 4. Create your initial feature request
# Edit INITIAL.md with your feature requirements
```

### 2. The Axiom Way (Supercharged Context)

To give your AI assistant "x-ray vision" into your codebase, initialize the Axiom Protocol. This will augment your project with a machine-readable map of its architecture and contracts.

```bash
# Follow steps 1-4 above, then:

# 5. Initialize Axiom Protocol
./init-axiom.sh

# This will:
# - Create a `.axiom-manifest.yml` file for you to configure.
# - Add Axiom files to your .gitignore.
# - Guide you on your next steps.
```

## 📚 Table of Contents

- [What is this Framework?](#what-is-this-framework)
- [Template Structure](#template-structure)
- [The Classic Workflow](#the-classic-workflow)
- [The Axiom Workflow](#the-axiom-workflow)
- [Best Practices](#best-practices)

## What is this Framework?

This framework integrates two complementary ideas:

### Context Engineering
- **What it is:** A system for providing comprehensive context to an AI through well-structured prompts, examples, and rules (`CLAUDE.md`, `INITIAL.md`).
- **Analogy:** Writing a detailed screenplay for an actor. You provide the script, the scene directions, and the character motivations.

### Axiom Protocol
- **What it is:** A system for making the codebase itself self-describing via metadata files (`.axiom-manifest.yml`, `*.contract.yml`).
- **Analogy:** Giving your actor a detailed map of the film set, a blueprint of the props, and a biography for every other character. The actor can now navigate the world independently and make intelligent decisions.

When used together, the AI not only knows *what* to do (from your prompt) but also deeply understands *where* and *how* to do it (from the Axiom metadata).

## Template Structure

```
context-engineering-axiom-edition/
├── .claude/                  # Claude Code custom commands
├── PRPs/                     # Product Requirements Prompts
├── examples/                 # Your code examples (critical!)
├── templates/
│   └── axiom/                # Templates for the Axiom Protocol
│       ├── MANIFEST.yml.tpl
│       └── CONTRACT.yml.tpl
├── CLAUDE.md                 # Global rules for AI assistant
├── INITIAL.md                # Template for feature requests
├── init-axiom.sh             # One-click script to set up Axiom
└── README.md                 # This file
```

## The Classic Workflow

Follow the original guide for writing effective `INITIAL.md` files and using the PRP workflow. This is the "human-to-AI" part of the equation.

## The Axiom Workflow

After running `./init-axiom.sh`, you unlock a new level of AI collaboration.

### 1. Configure Your Manifest
Edit the newly created `.axiom-manifest.yml`. Define your project's main components (`architecture`) and the commands to run it (`commands`). This is the AI's map of your project.

### 2. Write Contracts for Critical Code
You don't need to document everything at once. Start by creating `*.contract.yml` files for your most important modules. Use the template from `templates/axiom/CONTRACT.yml.tpl`. This gives the AI deep insight into the most critical parts of your codebase.

### 3. Guide the AI with Both
Now, when you write an `INITIAL.md` file, you can reference the Axiom components:

```markdown
## FEATURE:
Add a new endpoint to the 'auth' component to handle password resets.

## EXAMPLES:
Follow the pattern in `examples/api/endpoint.ts`.

## AXIOM CONTEXT:
- The main component for this work is `auth` as defined in `.axiom-manifest.yml`.
- You will need to interact with the `send_email` module, whose contract is defined in `src/utils/send_email.ts.contract.yml`. Please read its contract first.
```

The AI will now use both your instructions and the structured metadata to perform its task with higher precision.

## Best Practices

1.  **Start with Manual Context:** Get comfortable writing good `INITIAL.md` files first.
2.  **Introduce Axiom Incrementally:** Run `init-axiom.sh` and start by creating contracts for only your most critical modules.
3.  **Let the AI Maintain the Protocol:** As the AI adds new features, instruct it to also create or update the corresponding `.contract.yml` files. The system will start to maintain itself.
4.  **Combine, Don't Replace:** Use both `CLAUDE.md` and `.axiom-manifest.yml`. The first defines general behavior, the second defines specific project architecture.
