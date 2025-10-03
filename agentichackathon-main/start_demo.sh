#!/bin/bash

# 🌊 AI Flood Monitoring System - Easy Startup Script
# This script automatically sets up and starts both backend and frontend services

echo "🌊 Starting AI Flood Monitoring System..."
echo "========================================"

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f "backend.py" 2>/dev/null
pkill -f "streamlit" 2>/dev/null
sleep 2

# Navigate to project directory
cd "$(dirname "$0")/flood-monitoring-demo"

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating one..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment!"
        echo "Please ensure Python 3.8+ is installed: python3 --version"
        exit 1
    fi
    echo "✅ Virtual environment created!"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Installing dependencies (this may take a minute)..."
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet
    echo "✅ Dependencies installed!"
else
    echo "✅ Dependencies already installed"
fi

# Verify Google ADK is installed
if ! python -c "import google.genai" 2>/dev/null; then
    echo "🔧 Installing Google ADK packages..."
    pip install google-genai google-cloud-aiplatform google-auth vertexai --quiet
    echo "✅ Google ADK installed!"
fi

# Clear cache
echo "🗑️  Clearing Python cache..."
rm -rf app/__pycache__ 2>/dev/null
rm -rf mock_data/__pycache__ 2>/dev/null

# Start backend
echo "🚀 Starting Backend (FastAPI)..."
python app/backend.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
for i in {1..10}; do
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    sleep 1
done

# Start frontend
echo "🚀 Starting Frontend (Streamlit)..."
streamlit run app/frontend.py --server.headless=true > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 5

echo ""
echo "=========================================="
echo "✅ SYSTEM READY!"
echo "=========================================="
echo ""
echo "📊 Backend:  http://localhost:8000"
echo "🖥️  Frontend: http://localhost:8501"
echo ""
echo "📝 Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop:"
echo "   pkill -f backend.py"
echo "   pkill -f streamlit"
echo ""
echo "🎯 Next Steps:"
echo "   1. Open http://localhost:8501 in your browser"
echo "   2. Click 'Scenario 1' or 'Scenario 2' at the top"
echo "   3. Watch the 5-phase monitoring system"
echo "   4. For Scenario 2: Approve when prompted"
echo "   5. Select orchestration scenario"
echo ""

