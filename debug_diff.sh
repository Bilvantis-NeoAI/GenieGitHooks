#!/bin/bash

echo "🔍 Debugging Git Diff Content..."
echo "================================"

# Check staged files
echo "Staged files:"
git diff --cached --name-only
echo ""

# Check if there are any staged changes
staged_files=$(git diff --cached --name-only)
if [[ -z "$staged_files" ]]; then
    echo "❌ No files are staged for commit!"
    echo "   Run: git add <files> first"
    exit 1
fi

# Get diff content
echo "Getting diff content..."
diff_content=$(git diff --cached)

# Show diff content info
echo "Diff content length: ${#diff_content}"
echo ""
echo "Raw diff content (first 500 chars):"
echo "--- START DIFF ---"
echo "$diff_content" | head -c 500
echo ""
echo "--- END DIFF ---"
echo ""

# Test if diff_content is empty
if [[ -z "$diff_content" ]]; then
    echo "❌ PROBLEM: diff_content is empty!"
    echo "   This means git diff --cached returned nothing"
else
    echo "✅ diff_content has content (${#diff_content} characters)"
fi

# Test the Python payload creation
echo ""
echo "Testing Python payload creation..."
json_file=$(mktemp)
diff_file=$(mktemp)

# Write diff content to temporary file (same as the fixed hook)
echo "$diff_content" > "$diff_file"

python3 - <<EOF > "$json_file"
import json
import sys

# Read the diff content from temporary file
with open('$diff_file', 'r', encoding='utf-8') as f:
    diff_content = f.read()

print(f"Python received: {len(diff_content)} characters")
print(f"First 100 chars: {repr(diff_content[:100])}")

# Create test payload
payload = {
    "code": diff_content,
    "language": "test",
    "project_name": "test-repo", 
    "branch_name": "test-branch",
    "html": True
}

print(f"Payload code field length: {len(payload['code'])}")

# Output the JSON
print(json.dumps(payload, indent=2))
EOF

echo ""
echo "Generated JSON file content (first 300 chars):"
head -c 300 "$json_file"
echo ""

# Clean up
rm -f "$json_file" "$diff_file"

echo ""
echo " Debug complete!" 