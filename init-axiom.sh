#!/bin/bash
#
# init-axiom.sh: One-click script to initialize the Axiom Protocol for your project.
#

# --- Configuration ---
MANIFEST_TEMPLATE="./templates/axiom/MANIFEST.yml.tpl"
MANIFEST_OUTPUT="./.axiom-manifest.yml"
GITIGNORE_ENTRY="
# Axiom Protocol Files
.axiom-manifest.yml
*.contract.yml
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

# 3. Update .gitignore if it exists
if [ -f ".gitignore" ]; then
    if ! grep -q ".axiom-manifest.yml" ".gitignore"; then
        echo -e "$GITIGNORE_ENTRY" >> .gitignore
        print_info "Added Axiom Protocol files to .gitignore."
    fi
fi

print_success "Axiom Protocol initialized successfully!"
print_info "Next steps:"
echo "1. Customize the TODOs in your new '.axiom-manifest.yml' file."
echo "2. Start creating '.contract.yml' files for your critical code modules."
echo "3. Use the structured commit format to explain your changes."

exit 0
