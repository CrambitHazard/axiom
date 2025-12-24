#!/bin/bash
# Axiom Installer Script for Linux/macOS
# Adds Axiom to PATH so it can be used system-wide

echo "Axiom Installer"
echo "==============="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AXIOM_PATH="$SCRIPT_DIR"

echo "Installing Axiom from: $AXIOM_PATH"
echo ""

# Detect shell
SHELL_NAME=$(basename "$SHELL")
SHELL_RC=""

case "$SHELL_NAME" in
    bash)
        SHELL_RC="$HOME/.bashrc"
        ;;
    zsh)
        SHELL_RC="$HOME/.zshrc"
        ;;
    fish)
        SHELL_RC="$HOME/.config/fish/config.fish"
        ;;
    *)
        echo "Unsupported shell: $SHELL_NAME"
        echo "Please manually add this line to your shell config:"
        echo "export PATH=\"\$PATH:$AXIOM_PATH\""
        exit 1
        ;;
esac

# Create executable symlink if it doesn't exist
AXIOM_EXEC="$AXIOM_PATH/axiom"
AXIOM_PY="$AXIOM_PATH/axiom.py"

if [ ! -f "$AXIOM_PY" ]; then
    echo "Error: axiom.py not found at $AXIOM_PY"
    exit 1
fi

# Make axiom.py executable
chmod +x "$AXIOM_PY"

# Create symlink named 'axiom' if it doesn't exist
if [ ! -e "$AXIOM_EXEC" ]; then
    ln -s "$AXIOM_PY" "$AXIOM_EXEC"
    echo "✓ Created executable symlink: axiom -> axiom.py"
elif [ ! -L "$AXIOM_EXEC" ]; then
    echo "Warning: $AXIOM_EXEC exists but is not a symlink"
    echo "Skipping symlink creation"
else
    echo "✓ Executable symlink already exists"
fi

# Check if already in PATH
if grep -q "$AXIOM_PATH" "$SHELL_RC" 2>/dev/null; then
    echo "✓ Axiom is already in your PATH!"
    echo ""
    echo "To use it, reload your shell:"
    echo "  source $SHELL_RC"
    echo "Then run: axiom --help"
    exit 0
fi

# Add to shell config
echo "" >> "$SHELL_RC"
echo "# Axiom CLI" >> "$SHELL_RC"
echo "export PATH=\"\$PATH:$AXIOM_PATH\"" >> "$SHELL_RC"

echo "✓ Successfully added Axiom to PATH!"
echo ""
echo "Next steps:"
echo "  1. Reload your shell: source $SHELL_RC"
echo "  2. Navigate to any Git repository"
echo "  3. Run: axiom init"
echo ""
echo "To verify installation, run: axiom --help"

