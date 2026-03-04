#!/bin/bash

# Read the JSON input from Claude
input=$(cat)

# Extract the command
command=$(echo "$input" | jq -r '.tool_input.command // empty')

# Define dangerous patterns
dangerous_patterns=(
    'rm\s+.*-[rf]'           # rm -rf variants
    'sudo\s+rm'              # sudo rm commands  
    'chmod\s+777'            # Dangerous permissions
    '>\s*/etc/'              # Writing to system directories
    'dd\s+if='               # dd commands
    'mkfs\.'                 # Format commands
    ':(){:|:&};:'            # Fork bombs
)

# Check for dangerous patterns
for pattern in "${dangerous_patterns[@]}"; do
    if echo "$command" | grep -E "$pattern" > /dev/null 2>&1; then
        echo "🚫 BLOCKED: Dangerous command pattern detected: $pattern" >&2
        echo "Command was: $command" >&2
        exit 2  # Exit code 2 blocks the command
    fi
done

# If we get here, command is safe
exit 0
