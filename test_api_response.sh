#!/bin/bash

# Test script to debug API responses from the review endpoint
# Usage: ./test_api_response.sh

echo "🔍 Testing API Response Format"
echo "================================"

# Check if JWT token exists
if [ ! -f "$HOME/.genie/token" ]; then
    echo "❌ No JWT token found at $HOME/.genie/token"
    echo "Please run the Genie GitHooks app to login first."
    exit 1
fi

# Read JWT token
jwt_token=$(cat "$HOME/.genie/token" 2>/dev/null)
if [ -z "$jwt_token" ]; then
    echo "❌ JWT token is empty"
    exit 1
fi

echo "✅ JWT token found"

# Get backend URL from existing hooks (if any)
hooks_dir=$(git config --global --get core.hooksPath 2>/dev/null)
if [ -z "$hooks_dir" ] || [ ! -f "$hooks_dir/pre-commit" ]; then
    echo "❌ No git hooks found. Please install Genie GitHooks first."
    exit 1
fi

# Extract backend URL from pre-commit hook (try multiple patterns)
backend_url=$(grep "api_url=" "$hooks_dir/pre-commit" | head -1 | sed 's/.*api_url="\([^"]*\)".*/\1/')
if [ -z "$backend_url" ]; then
    backend_url=$(grep "BASE_API=" "$hooks_dir/pre-commit" | head -1 | sed 's/.*BASE_API="\([^"]*\)".*/\1/')
fi
if [ -z "$backend_url" ]; then
    echo "❌ Could not extract backend URL from hooks"
    echo "Trying to find api_url or BASE_API patterns..."
    grep -n "api_url\|BASE_API" "$hooks_dir/pre-commit" | head -5
    exit 1
fi

# Remove the endpoint path if it exists (we'll add /review/review)
backend_url=$(echo "$backend_url" | sed 's|/review/review$||')

echo "✅ Backend URL: $backend_url"

# Create a simple test payload
test_payload='{
    "code": "def test_function():\n    print(\"Hello World\")\n    return True",
    "language": "python",
    "project_name": "test-project",
    "branch_name": "test-branch",
    "html": true
}'

echo "📤 Sending test request to: $backend_url/review/review"
echo "Payload: $test_payload"
echo ""

# Make the API call
response=$(curl -s -w "\nHTTP_STATUS:%{http_code}\n" \
    -X POST \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $jwt_token" \
    -d "$test_payload" \
    "$backend_url/review/review")

# Extract HTTP status and response body
http_status=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
response_body=$(echo "$response" | sed '/HTTP_STATUS:/d')

echo "📥 Response received:"
echo "HTTP Status: $http_status"
echo ""
echo "Response Body (first 500 characters):"
echo "======================================"
echo "$response_body" | head -c 500
echo ""
echo "======================================"
echo ""

# Analyze response format
if [[ "$response_body" == *"<html"* ]] || [[ "$response_body" == *"<!DOCTYPE"* ]]; then
    echo "🔍 Analysis: Response appears to be HTML"
    echo "Content type: HTML document"
elif [[ "$response_body" == *"{"* ]] && [[ "$response_body" == *"}"* ]]; then
    echo "🔍 Analysis: Response appears to be JSON"
    echo "Attempting to parse JSON structure..."
    
    # Try to pretty-print JSON
    if command -v python3 > /dev/null 2>&1; then
        echo "$response_body" | python3 -m json.tool 2>/dev/null | head -20
    elif command -v python > /dev/null 2>&1; then
        echo "$response_body" | python -m json.tool 2>/dev/null | head -20
    else
        echo "Python not available for JSON parsing"
    fi
else
    echo "🔍 Analysis: Response format unclear"
    echo "Content type: Unknown"
fi

echo ""
echo "💡 Tips:"
echo "- If response is JSON with HTML inside, check for keys like 'html', 'content', 'response', 'data'"
echo "- If response is plain HTML, it should work directly"
echo "- If response is an error, check the 'detail' field in JSON"
echo ""

# Save response to file for further inspection
response_file="/tmp/genie_api_response_$(date +%s).txt"
echo "$response_body" > "$response_file"
echo "📁 Full response saved to: $response_file" 