# .axiom-manifest.yml
# This file is the single source of truth for your project's architecture and rules.
# It enables an AI assistant to understand your project's structure at a glance.
version: "1.0"

project:
  name: "My-New-Project"
  goal: "A one-sentence description of what this project does."
  stack: ["Python", "FastAPI", "React"] # TODO: Customize your tech stack

commands:
  install: "npm install && pip install -r requirements.txt" # TODO: Customize install command
  run: "npm run dev" # TODO: Customize run command
  test: "npm run test" # TODO: Customize test command
  lint: "npm run lint" # TODO: Customize lint command
  preflight: "npm run lint && npm run test" # TODO: Customize preflight checks

architecture:
  - component: "backend"
    path: "./backend"
    responsibility: "Handles API logic and database interactions."
    contracts:
      - "backend/**/*.contract.yml"
  - component: "frontend"
    path: "./frontend"
    responsibility: "Contains the user interface components."
    contracts:
      - "frontend/**/*.contract.yml"

policies:
  - id: "CONTRACT_REQUIRED"
    level: "warn" # Start with 'warn' to avoid blocking early development
    description: "Every functional module should have a .contract.yml file."
  - id: "LEDGER_OF_INTENT_REQUIRED"
    level: "info" # Start with 'info' as a gentle reminder
    description: "Commit messages should follow the structured format for clarity."
