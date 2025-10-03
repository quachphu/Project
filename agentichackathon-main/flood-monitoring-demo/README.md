# 🌊 Flood Monitoring Simulation System

A step-by-step simulation of a flood monitoring and disaster response system with real-time UI updates.

## 📁 Project Structure

```
flood-monitoring-demo/
├── app/
│   ├── backend.py          # FastAPI backend (port 8000)
│   └── frontend.py         # Streamlit UI (port 8501)
├── mock_data/
│   └── weather_alert.py    # Weather alert data generator
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd flood-monitoring-demo
pip install -r requirements.txt
```

### Step 2: Start the Backend

Open a terminal and run:

```bash
python app/backend.py
```

You should see:
```
🚀 Starting Flood Monitoring Backend...
📍 Backend URL: http://localhost:8000
📖 API Docs: http://localhost:8000/docs
```

### Step 3: Start the Frontend

Open a **new terminal** and run:

```bash
streamlit run app/frontend.py
```

Your browser should automatically open to: `http://localhost:8501`

## 🎮 How to Use

1. **Check Backend Status**: The UI shows a green "✅ Backend Online" indicator when connected
2. **Click "Scenario 1: Moderate Flood"**: This sends a simulated weather alert to the backend
3. **View the Timeline**: The right panel shows the weather alert with all details
4. **Expand Alert Details**: Click "📋 View Alert Details" to see the full JSON payload

## 📊 Current Features (Step 1)

- ✅ Weather Alert Generation (T-2 hours)
- ✅ Send alert to backend orchestrator endpoint
- ✅ Real-time UI updates
- ✅ Event timeline visualization
- ✅ Detailed alert data inspection

## 🔜 Coming Next

Step 2: River Gauge Sensors (T-1 hour)
Step 3: Satellite Imagery Analysis (T-50 mins)
Step 4: Drone LiDAR Surveys (T-30 mins)
Step 5: Social Media Monitoring (T-10 mins)
Step 6: Emergency Response Coordination

## 🛠️ API Endpoints

### Backend (http://localhost:8000)

- `GET /` - Health check
- `POST /api/alerts/weather` - Receive weather alerts
- `GET /api/events` - Get all monitoring events
- `GET /api/events/latest` - Get latest event
- `DELETE /api/events` - Clear all events

Interactive API docs available at: http://localhost:8000/docs

## 📝 Weather Alert JSON Schema

```json
{
  "alert_id": "WX-FLOOD-20251003123456",
  "alert_type": "FLOOD_WATCH",
  "timestamp": "2025-10-03T12:34:56",
  "severity": {
    "level": 3,
    "scale": "1-5 (5 being most severe)",
    "description": "Heavy rainfall expected with moderate flood risk"
  },
  "precipitation": {
    "probability_percent": 75,
    "expected_amount_mm": 95,
    "timeframe_hours": 2
  },
  "location": {
    "region": "Northern Valley",
    "affected_areas": ["River Basin District", "Downtown"]
  }
}
```

## 🧪 Testing

Test the backend directly with curl:

```bash
# Health check
curl http://localhost:8000/

# Get all events
curl http://localhost:8000/api/events

# Clear events
curl -X DELETE http://localhost:8000/api/events
```

## 💡 Tips

- Keep both backend and frontend running in separate terminals
- Use "🔄 Refresh Status" if backend connection is lost
- Click "🗑️ Clear All Events" to reset the simulation
- Check `http://localhost:8000/docs` for interactive API testing

## 🎯 Architecture

```
┌─────────────────┐         POST          ┌──────────────────┐
│   Streamlit UI  │ ───────────────────▶  │  FastAPI Backend │
│   (Frontend)    │      /api/alerts      │   (Orchestrator) │
│   Port 8501     │ ◀───────────────────  │    Port 8000     │
└─────────────────┘        Events         └──────────────────┘
         │                                          │
         │                                          │
         ▼                                          ▼
  User clicks                              Stores events &
  "Scenario 1"                             triggers agents
         │                                    (future step)
         │                                          │
         ▼                                          ▼
  Generates mock                           Returns status &
  weather alert JSON                       event count
```

---

Built with ❤️ for flood monitoring and disaster response simulation

