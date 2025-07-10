# .axiom/index.yml
# Central index for AI-optimized codebase understanding
# This file enables rapid context gathering and token-efficient file discovery

version: "1.0"
generated_at: "{{TIMESTAMP}}"
project_root: "."

# Project-level AI context
project_context:
  name: "{{PROJECT_NAME}}"
  goal: "{{PROJECT_GOAL}}"
  ai_optimization_level: "high"  # high, medium, low
  token_budget_per_session: 100000  # Estimated tokens for full codebase understanding

# File organization for AI consumption
file_categories:
  core_modules:
    description: "Essential files that define project architecture"
    files: []
    estimated_tokens: 0
  
  feature_modules:
    description: "Feature-specific implementation files"
    files: []
    estimated_tokens: 0
  
  config_files:
    description: "Configuration and setup files"
    files: []
    estimated_tokens: 0
  
  test_files:
    description: "Test and validation files"
    files: []
    estimated_tokens: 0

# AI-optimized dependency graph
dependency_clusters:
  # Groups of related files that should be read together
  # Format: cluster_name: [file1, file2, file3]
  
# Quick reference for AI
ai_shortcuts:
  entry_points: []         # Main application entry points
  critical_interfaces: []  # Key APIs and interfaces
  data_models: []         # Core data structures
  external_apis: []       # Third-party integrations

# Meta information tracking
meta_files:
  total_count: 0
  last_updated: "{{TIMESTAMP}}"
  sync_status: "clean"  # clean, dirty, syncing