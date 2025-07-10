# File meta information for AI-optimized understanding
# Location: .axiom/meta/{{RELATIVE_PATH}}.yml
# Source: {{RELATIVE_PATH}}

version: "1.0"
generated_at: "{{TIMESTAMP}}"
last_updated: "{{TIMESTAMP}}"

# Basic file information
file_info:
  path: "{{RELATIVE_PATH}}"
  type: "{{FILE_TYPE}}"  # module, component, config, test, script, doc
  language: "{{LANGUAGE}}"
  size_bytes: {{FILE_SIZE}}
  estimated_tokens: {{ESTIMATED_TOKENS}}

# AI-optimized summary (token-efficient)
ai_summary:
  purpose: "{{PURPOSE}}"  # One-sentence description
  complexity: "{{COMPLEXITY}}"  # low, medium, high
  importance: "{{IMPORTANCE}}"  # core, feature, util, test
  
  # Key concepts for AI understanding
  key_concepts: []  # [concept1, concept2, concept3]
  
  # Quick reading hints
  reading_priority: "{{PRIORITY}}"  # critical, important, optional
  context_dependencies: []  # Files that should be read first
  
# Code structure (for programming files)
code_structure:
  exports: []          # Public interfaces/exports
  imports: []          # Dependencies
  main_functions: []   # Key functions/methods
  data_structures: []  # Important classes/types
  
# AI-specific optimizations
ai_hints:
  # Sections that can be skipped for quick understanding
  skippable_sections: []
  
  # Key lines that contain essential logic
  critical_lines: []
  
  # Patterns that this file demonstrates
  patterns: []

# Relationships
relationships:
  # Files that import this file
  imported_by: []
  
  # Files that this file depends on
  depends_on: []
  
  # Similar files (for pattern recognition)
  similar_files: []
  
  # Related test files
  test_files: []

# Change tracking for AI context
change_tracking:
  last_significant_change: "{{TIMESTAMP}}"
  change_frequency: "{{FREQUENCY}}"  # high, medium, low
  stability: "{{STABILITY}}"  # stable, evolving, experimental
  
# Contract reference (if exists)
contract_file: "{{CONTRACT_PATH}}"  # Path to .contract.yml if exists