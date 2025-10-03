#!/bin/bash
# Start the Streamlit frontend

cd "$(dirname "$0")"

echo "🌊 Starting Flood Monitoring Frontend..."
echo "📍 Frontend URL: http://localhost:8501"
echo ""

streamlit run app/frontend.py

