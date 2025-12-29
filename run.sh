#!/bin/bash

# Simple script to run your minimalist portfolio website
echo "🚀 Starting your minimalist portfolio website..."
echo "📍 Website will be available at: http://localhost:8089"
echo "🛑 Press Ctrl+C to stop the server"
echo ""
echo "💡 Tip: To rebuild articles from markdown, run: ./scripts/build.sh or python3 scripts/build.py"
echo ""

# Start the local server
python3 -m http.server 8089
