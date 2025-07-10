#!/bin/bash
#
# init-axiom.sh: One-click script to initialize the Axiom Protocol for your project.
#

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST_TEMPLATE="$SCRIPT_DIR/templates/axiom/MANIFEST.yml.tpl"
MANIFEST_OUTPUT="./.axiom-manifest.yml"
CLAUDE_COMMANDS_DIR="$SCRIPT_DIR/.claude/commands"
CLAUDE_MD_TEMPLATE="$SCRIPT_DIR/CLAUDE_MD_FOR_USER.md"
CLAUDE_MD_OUTPUT="./CLAUDE.md"
META_GENERATOR_SCRIPT="$SCRIPT_DIR/scripts/axiom-meta-generator.py"
GITIGNORE_ENTRY="
# Axiom Protocol Files
.axiom-manifest.yml
*.contract.yml
.axiom/
"

# --- Functions ---
function print_success {
    # Green color
    echo -e "\033[0;32m$1\033[0m"
}

function print_info {
    # Blue color
    echo -e "\033[0;34m$1\033[0m"
}

function print_error {
    # Red color
    echo -e "\033[0;31m$1\033[0m"
}


# --- Main Script ---
print_info "Initializing Axiom Protocol for this project..."

# 1. Check if manifest already exists
if [ -f "$MANIFEST_OUTPUT" ]; then
    print_error "Error: .axiom-manifest.yml already exists. Initialization aborted."
    exit 1
fi

# 2. Copy the manifest template
if [ ! -f "$MANIFEST_TEMPLATE" ]; then
    print_error "Error: Manifest template not found at $MANIFEST_TEMPLATE"
    exit 1
fi
cp "$MANIFEST_TEMPLATE" "$MANIFEST_OUTPUT"

# 3. Copy Claude commands if they exist
if [ -d "$CLAUDE_COMMANDS_DIR" ]; then
    mkdir -p ".claude/commands"
    cp -r "$CLAUDE_COMMANDS_DIR"/* ".claude/commands/" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_info "Copied Claude slash commands to .claude/commands/"
    fi
fi

# 4. Copy CLAUDE.md template if it exists
if [ -f "$CLAUDE_MD_TEMPLATE" ]; then
    if [ ! -f "$CLAUDE_MD_OUTPUT" ]; then
        cp "$CLAUDE_MD_TEMPLATE" "$CLAUDE_MD_OUTPUT"
        print_info "Created CLAUDE.md from template."
    fi
fi

# 5. Copy and set up meta generator script
if [ -f "$META_GENERATOR_SCRIPT" ]; then
    mkdir -p "scripts"
    cp "$META_GENERATOR_SCRIPT" "scripts/axiom-meta-generator.py"
    chmod +x "scripts/axiom-meta-generator.py"
    print_info "Copied axiom meta generator script to scripts/"
fi

# 6. Initialize .axiom directory structure
print_info "Creating .axiom directory structure..."
mkdir -p ".axiom/meta"
mkdir -p ".axiom/cache"

# 7. Run initial metadata scan if Python is available
if command -v python3 &> /dev/null && [ -f "scripts/axiom-meta-generator.py" ]; then
    print_info "Running initial metadata scan..."
    python3 scripts/axiom-meta-generator.py --init --scan
    if [ $? -eq 0 ]; then
        print_success "Initial metadata scan completed successfully!"
    else
        print_error "Warning: Initial metadata scan failed. You can run it manually later."
    fi
else
    print_info "Python3 not found or meta generator missing. Skipping initial scan."
    print_info "You can run the scan manually later with: python3 scripts/axiom-meta-generator.py --scan"
fi

# 8. Update .gitignore if it exists
if [ -f ".gitignore" ]; then
    if ! grep -q ".axiom-manifest.yml" ".gitignore"; then
        echo -e "$GITIGNORE_ENTRY" >> .gitignore
        print_info "Added Axiom Protocol files to .gitignore."
    fi
fi

print_success "Axiom Protocol initialized successfully!"
print_info "Directory structure created:"
echo "  .axiom/               # AI-optimized metadata directory"
echo "  .axiom/meta/          # File-specific metadata"
echo "  .axiom/cache/         # AI caching and optimization"
echo "  .axiom/index.yml      # Project-wide AI context"
echo "  scripts/              # Axiom management scripts"
echo ""
print_info "Next steps:"
echo "1. Customize the TODOs in your new '.axiom-manifest.yml' file."
echo "2. Review and customize 'CLAUDE.md' for your project needs."
echo "3. Start creating '.contract.yml' files for your critical code modules."
echo "4. Use /generate-prp-pro to create your first PRP for development."
echo "5. Use the structured commit format to explain your changes."
echo ""
print_info "To update metadata later:"
echo "  python3 scripts/axiom-meta-generator.py --scan"
echo "  python3 scripts/axiom-meta-generator.py --update <file>"

exit 0
