#!/bin/bash

# Simple script to run your minimalist portfolio website
echo "🚀 Starting your minimalist portfolio website..."
echo "📍 Website will be available at: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the local server
python3 -m http.server 8000
