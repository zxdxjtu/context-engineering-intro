# AI Assistant Global Rules (CLAUDE.md / GEMINI.md)

This document contains the global rules that you, the AI assistant, must follow for every task in this project.

### 👑 Guiding Principle
Your primary goal is to act as a diligent, context-aware engineer. You must use all available context to make informed decisions.

---

### 🔄 **Phase 1: Context Gathering (Before You Code)**

Before writing or modifying any code, you MUST gather context in the following order:

1.  **Check for Axiom Protocol Files (Highest Priority):**
    - **Does `.axiom-manifest.yml` exist?** If yes, read it first. This is the authoritative source for the project's architecture, commands, and policies. You MUST adhere to it.
    - **Are you modifying or using an existing module?** If yes, look for its corresponding `*.contract.yml` file. You MUST read this contract to understand the module's purpose, inputs, and outputs before using it. The contract is the truth.

2.  **Read High-Level Documentation:**
    - Read `PLANNING.md` or `README.md` to understand the project's broader goals and human-written guidelines. If this information conflicts with the `.axiom-manifest.yml`, the manifest takes precedence.

3.  **Review the Current Task:**
    - Check `TASK.md` or the user's latest prompt to understand the specific requirements of the current task.

---

### 🧱 **Phase 2: Code Implementation**

When writing code, you must adhere to the following rules:

1.  **Axiom Protocol Adherence:**
    - **Creating New Modules:** If you create a new, non-trivial function or file, you MUST also create its corresponding `*.contract.yml` file. Use the template in `templates/axiom/CONTRACT.yml.tpl` as a starting point.
    - **Modifying Existing Modules:** If you change the core logic, inputs, or outputs of a module, you MUST update its `*.contract.yml` file to reflect the changes. The code and its contract must always be in sync.
    - **Respect the Architecture:** You must place new files within the correct `component` directory as defined in `.axiom-manifest.yml`.

2.  **General Code Structure:**
    - **Never create a file longer than 500 lines.** Refactor large files into smaller, single-purpose modules.
    - **Organize code into clearly separated modules**, grouped by feature or responsibility.

3.  **Testing & Reliability:**
    - **Always create unit tests for new features.**
    - Tests should live in a `/tests` folder that mirrors the main application structure.
    - When using the Axiom Protocol, your tests should validate the promises made in the module's `contract.yml`.

---

### ✅ **Phase 3: Committing Your Work**

1.  **Use Structured Commits:** If the Axiom Protocol is active, you are strongly encouraged to use the structured commit format to explain your work.
    ```
    feat(component): Short description

    AI-Reasoning:
    A detailed explanation of why you made this change.

    Tool-Trail:
    - A list of the tools you used to make the change.
    - ...
    ```

2.  **Mark Tasks as Complete:** Update `TASK.md` or inform the user that the task is complete.

---

### 🧠 **Core AI Behavior**
- **Never assume missing context. Ask questions if uncertain.**
- If the Axiom Protocol is enabled, use it as your primary source of truth for understanding the codebase.
- **Never delete or overwrite existing code** unless explicitly instructed to or if it's part of a planned refactoring.
