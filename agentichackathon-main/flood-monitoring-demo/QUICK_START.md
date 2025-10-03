# 🚀 Quick Start Guide - Flood Monitoring Demo

## ✅ System is Running!

Both backend and frontend have been started for you!

### 🌐 Access URLs

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend (FastAPI)**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 🎮 How to Use

### Step 1: Open the Frontend
Open your browser to: **http://localhost:8501**

You should see the "🌊 Flood Monitoring Simulation System" interface.

### Step 2: Check Backend Status
Look for the **"✅ Backend Online"** indicator at the top.

### Step 3: Trigger Scenario 1
1. On the left side, click the **"🌧️ Scenario 1: Moderate Flood"** button
2. Watch the timeline on the right side populate with the weather alert
3. Expand **"📋 View Alert Details"** to see the full JSON payload

### Step 4: Inspect the Data
The alert includes:
- **Severity Level**: 3/5
- **Precipitation**: 95mm expected
- **Probability**: 75%
- **Location**: Northern Valley region
- **Message**: "Expected rain in 2 hours..."

---

## 📊 What Just Happened?

When you clicked "Scenario 1":

1. **Frontend** generated a mock weather alert JSON
2. **Sent** it to `POST http://localhost:8000/api/alerts/weather`
3. **Backend** received it and stored it as an event
4. **Backend** would trigger the orchestrator (coming in next steps)
5. **Frontend** displayed the alert in the timeline

---

## 🔧 Manual Start (if needed)

If you need to restart the services:

### Terminal 1 - Backend:
```bash
cd flood-monitoring-demo
python app/backend.py
```

### Terminal 2 - Frontend:
```bash
cd flood-monitoring-demo
streamlit run app/frontend.py
```

Or use the convenience scripts:
```bash
./start_backend.sh    # Terminal 1
./start_frontend.sh   # Terminal 2
```

---

## 🧪 Test the Backend API

You can test the backend directly:

```bash
# Health check
curl http://localhost:8000/

# Get all events
curl http://localhost:8000/api/events

# Clear events
curl -X DELETE http://localhost:8000/api/events
```

Or visit the interactive API docs: http://localhost:8000/docs

---

## 📋 Current Features (Step 1)

✅ **Weather Alert System**
- Mock weather data generation
- POST to orchestrator endpoint
- Real-time UI updates
- Event timeline display
- Full JSON inspection

---

## 🔜 Next Steps

We'll build on this foundation to add:

- **Step 2**: River Gauge Sensors (T-1 hour)
- **Step 3**: Satellite Imagery Analysis (T-50 mins)  
- **Step 4**: Drone LiDAR Surveys (T-30 mins)
- **Step 5**: Social Media Monitoring (T-10 mins)
- **Step 6**: Emergency Response Coordination

Each step will trigger automatically based on severity scoring!

---

## 🛑 To Stop the Services

Press `Ctrl+C` in each terminal, or find and kill the processes:

```bash
# Find processes
ps aux | grep "python app/backend.py"
ps aux | grep "streamlit run"

# Kill them
pkill -f "python app/backend.py"
pkill -f "streamlit run"
```

---

## 💡 Tips

- Use **"🗑️ Clear All Events"** button to reset the simulation
- Click **"🔄 Refresh Status"** if backend connection drops
- Multiple scenarios can be triggered (more coming soon!)
- Check the terminal output to see backend logs

---

## 📁 Project Structure

```
flood-monitoring-demo/
├── app/
│   ├── backend.py       # FastAPI server (port 8000)
│   └── frontend.py      # Streamlit UI (port 8501)
├── mock_data/
│   └── weather_alert.py # Weather data generator
└── README.md            # Full documentation
```

---

**🎉 You're all set! Click "Scenario 1" and watch the magic happen!**

