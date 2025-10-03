#!/bin/bash
# Start the FastAPI backend server

cd "$(dirname "$0")"

echo "🚀 Starting Flood Monitoring Backend..."
echo "📍 Backend URL: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""

python app/backend.py

