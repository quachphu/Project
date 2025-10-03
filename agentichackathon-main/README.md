# 🌊 AI-Powered Flood Monitoring & Emergency Response System

A multi-agent AI system using Google ADK (Agent Development Kit) with Gemini 2.0 Flash that provides real-time flood monitoring, risk assessment, and intelligent emergency response coordination.

---

## 📁 Project Structure

```
agent-starter-pack/
├── flood-monitoring-demo/          # Main Application (Streamlit UI + FastAPI Backend)
│   ├── app/
│   │   ├── backend.py              # FastAPI server with 5-phase monitoring
│   │   ├── frontend.py             # Streamlit UI with real-time monitoring
│   │   ├── flood_coordinator.py    # Phase orchestration logic
│   │   └── agent_client.py         # Bridge to agent system
│   ├── mock_data/                  # Simulated sensor & API data
│   │   ├── weather_alert.py
│   │   ├── river_gauge_data.py
│   │   ├── ml_similarity.py
│   │   ├── x_posts.py
│   │   └── historical_events.csv
│   ├── drone_images/               # Drone imagery for AI analysis
│   │   └── scenario_1/             # Different flood scenarios
│   ├── venv/                       # Python virtual environment
│   ├── requirements.txt
│   └── *.md                        # Documentation files
│
├── my-awesome-agent/               # Google ADK Agent System
│   ├── app/
│   │   ├── agents/
│   │   │   ├── decision_maker_adk.py    # Master orchestrator agent
│   │   │   └── agents_adk.py            # 7 specialized response agents
│   │   └── tools/                       # Agent tools & capabilities
│   ├── pyproject.toml
│   ├── uv.lock
│   └── *.md                        # Agent documentation
│
└── reference/                      # Reference implementations
    └── agentic-adk-hackathon/      # Original reference code
```

---

## 🎯 System Overview

### **Part 1: Progressive Risk Assessment (Phases 1-5)**
Real-time AI-driven monitoring that progressively escalates through 5 phases:

1. **Phase 1: Weather Alert Analysis** (0-25 pts) - NWS alert evaluation
2. **Phase 2: River Gauge Monitoring** (0-25 pts) - Real-time sensor data
3. **Phase 3: ML Historical Similarity** (0-20 pts) - Pattern matching
4. **Phase 4: Social Media Analysis** (0-15 pts) - X/Twitter sentiment
5. **Phase 5: Drone Vision AI** (0-15 pts) - Aerial imagery analysis

**Total Score:** 0-100 points

### **Part 2: Human-in-the-Loop Orchestration**

Based on the cumulative confidence score:

| Score | Trigger | Action |
|-------|---------|--------|
| **< 60** | No Action | Continue monitoring |
| **60-89** | ⚠️ **Human Approval Required** | Approve/Reject → Select Scenario |
| **90-100** | 🚨 **Auto-Approved** | Direct Scenario Selection |

### **Part 3: Multi-Agent Emergency Response**

After approval, choose between 2 dynamic scenarios:

#### **🏥 Scenario 1: Hospital Crisis**
- Hospital ICU overwhelmed (2-5 beds)
- **Inter-Agent Communication:**
  - Hospital → Police: Request crowd control
  - Police: Dispatch 3-6 additional units
  - Hospital ↔ Relief Shelter: Medical support coordination

#### **🚤 Scenario 2: Rescue Coordination**
- High evacuation demand (45+ SOS)
- **Inter-Agent Communication:**
  - Rescue → Transport: Request pickup locations
  - Transport → Rescue: Provide 3 evacuation points
  - Rescue → Police (×3): Clear routes for each point
  - Relief → Hospital: Request ambulance support

---

## 🚀 Quick Start

### **Prerequisites**

```bash
# Python 3.8+ (check your version)
python3 --version

# Google Cloud credentials (for Gemini AI)
export GOOGLE_API_KEY="your-api-key-here"
# OR
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### **One-Command Startup (Recommended)**

The startup script automatically handles everything: venv creation, dependency installation, and service startup!

```bash
cd /Users/parichaypothepalli/Downloads/agent-starter-pack
./start_demo.sh
```

**That's it!** The script will:
- ✅ Create virtual environment (if needed)
- ✅ Install all dependencies (if needed)
- ✅ Install Google ADK packages
- ✅ Clear Python cache
- ✅ Start backend (FastAPI)
- ✅ Start frontend (Streamlit)

---

### **Manual Setup (Alternative)**

If you prefer to set up manually:

#### **Step 1: Install Dependencies**

```bash
cd /Users/parichaypothepalli/Downloads/agent-starter-pack/flood-monitoring-demo

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
pip install google-genai google-cloud-aiplatform google-auth vertexai
```

#### **Step 2: Start Services**

**Terminal 1: Backend (FastAPI)**
```bash
cd flood-monitoring-demo
source venv/bin/activate
python app/backend.py
```

**Terminal 2: Frontend (Streamlit)**
```bash
cd flood-monitoring-demo
source venv/bin/activate
streamlit run app/frontend.py
```

---

### **Step 3: Run a Simulation**

1. Open http://localhost:8501 in your browser

**💡 TIP:** Press **Cmd+Shift+R (Mac)** or **Ctrl+Shift+R (Windows)** to hard refresh at each step!

2. Click one of the scenario buttons at the top:
   - **Scenario 1**: High Risk (4/5 severity, 120mm) → ~93 score → Auto-approved
   - **Scenario 2**: Medium Risk (3/5, 95mm) → ~80 score → Requires approval
   - **Scenario 3**: Low Risk (1/5, 25mm) → ~25 score → No orchestration

3. **Watch the progression:**
   - Phases 1-5 execute automatically (~15 seconds)
   - Score accumulates in the sidebar
   - Monitoring log shows real-time events

4. **For Scenario 2 (Score 60-89):**
   - System pauses and shows **⚠️ HUMAN APPROVAL REQUIRED**
   - Click **✅ APPROVE** in the sidebar
   - Scenario selection buttons appear

5. **Select Emergency Response Scenario:**
   - **🏥 Scenario 1**: Hospital Crisis
   - **🚤 Scenario 2**: Rescue Coordination

6. **View Results:**
   - 7 agents activate (Communication, Police, Hospital, Rescue, Utility, Transport, Relief)
   - Inter-agent communications appear in the monitoring log
   - Color-coded messages show cross-agent coordination

---

## 🧪 Testing Different Flows

### **Flow 1: Auto-Approved (Score 90+)**
```
1. Click "Scenario 1" (top)
2. Wait ~15 seconds
3. Score reaches 93/100
4. Sidebar shows: "🚨 SELECT SCENARIO"
5. Choose Scenario 1 or 2
6. See agent coordination
```

### **Flow 2: Human Approval (Score 60-89)**
```
1. Click "Scenario 2" (top)
2. Wait ~15 seconds
3. Score reaches ~80/100
4. Sidebar shows: "⚠️ HUMAN APPROVAL REQUIRED"
5. Click "✅ APPROVE"
6. Sidebar shows: "🚨 SELECT SCENARIO"
7. Choose Scenario 1 or 2
8. See agent coordination
```

### **Flow 3: No Orchestration (Score < 60)**
```
1. Click "Scenario 3" (top)
2. Phases 1-2 execute
3. Score reaches ~25/100
4. System stops (below threshold)
5. No orchestration triggered
```

---

## 📊 Understanding the Monitoring Log

The monitoring log uses color-coded indicators:

- 🔴 **Red (Critical)**: URGENT messages, inter-agent requests
- 🟢 **Green (Success)**: Completed actions, successful responses
- 🟡 **Yellow (Warning)**: Escalations, warnings, coordination messages
- 🔵 **Blue (Info)**: General information, progress updates

### **Inter-Agent Communication Format:**
```
🏥 HospitalEMS Agent Activated
  └─ 🚑 2 ambulances
  └─ 🏥 2 ICU beds
  └─ 🔗 ⚠️ CRITICAL: Only 2 ICU beds available! Requesting police support...
  └─ 🔗 Sending 'hospital_crowd_control' to PoliceAgent
  └─ ✅ Received from PoliceAgent: {'status': 'deployed'...}
  └─ ✅ Police responded: deployed

🚔 Police Agent Activated
  └─ 🚔 13 cars
  └─ ⚠️ 🚨 URGENT: Hospital crowd control requested
  └─ ⚠️ 🚔 Dispatching 5 additional units for crowd control
```

---

## 🏗️ Architecture

### **Technology Stack**

- **Frontend**: Streamlit (Python)
- **Backend**: FastAPI (Python)
- **AI Framework**: Google ADK (Agent Development Kit)
- **AI Model**: Gemini 2.0 Flash Experimental
- **Data Validation**: Pydantic V2
- **Mock Data**: CSV, JSON, Python generators

### **Agent System (Google ADK)**

**Master Agent:**
- `DecisionMakerAgent`: Orchestrates all emergency response agents

**Specialized Agents (7):**
1. `CommunicationAlertAgent`: Mass notifications & alerts
2. `PoliceAgent`: Law enforcement & crowd control
3. `HospitalEMSAgent`: Medical response & ambulances
4. `RescueAgent`: Water rescue & evacuation
5. `UtilityAgent`: Infrastructure shutdown
6. `TransportationEvacAgent`: Bus evacuation routes
7. `ReliefShelterAgent`: Shelter setup & supplies

### **Inter-Agent Communication**

Agents communicate via message passing:

```python
# Agent A sends message to Agent B
response = agent_a.send_message(
    agent_b, 
    "message_type",
    {"payload": "data"}
)

# Agent B receives and processes
def receive_message(self, action, payload):
    if action == "message_type":
        # Process and respond
        return {"status": "success"}
```

---

## 📝 Configuration

### **Adjusting Score Thresholds**

Edit `flood-monitoring-demo/app/backend.py`:

```python
# Phase 3 trigger (Line ~205)
if cumulative_score_phase3 >= 15:  # Lower = easier to trigger

# Phase 4 trigger (Line ~266)
if cumulative_score_phase4 >= 25:

# Phase 5 trigger (Line ~328)
if cumulative_score_phase5 >= 35:

# Orchestration triggers (Line ~393-413)
if final_cumulative_score >= 90:     # Auto-approved
elif final_cumulative_score >= 60:   # Requires approval
```

### **Adding Custom Scenarios**

Edit `flood-monitoring-demo/mock_data/weather_alert.py`:

```python
scenarios = {
    "your_scenario": {
        "precipitation_probability": 85,
        "expected_precipitation_mm": 100,
        "severity_level": 3,
        "description": "Your description"
    }
}
```

---

## 🐛 Troubleshooting

### **Backend won't start:**
```bash
# Check if port 8000 is in use
lsof -i:8000

# Kill existing process
kill -9 <PID>

# Clear Python cache
rm -rf flood-monitoring-demo/app/__pycache__
```

### **Frontend shows "Connection Refused":**
```bash
# Ensure backend is running
curl http://localhost:8000/

# Restart frontend
pkill -f streamlit
streamlit run app/frontend.py
```

### **API Rate Limit (429 Error):**
```
google.genai.errors.ClientError: 429 Too Many Requests
```

**Solution:** Wait 1 minute between tests. The free tier has rate limits.

### **Agents not communicating:**
```bash
# Clear cache and restart
rm -rf my-awesome-agent/app/agents/__pycache__
# Restart backend
```

---

## 📚 Documentation Files

### **Main Documentation:**
- `README.md` (this file) - Complete system guide
- `QUICK_START.md` - 5-minute quickstart
- `ARCHITECTURE.txt` - Technical architecture

### **Implementation Guides:**
- `ORCHESTRATION_INTEGRATION.md` - How orchestration works
- `DYNAMIC_SCENARIO_GUIDE.md` - Scenario system explained
- `PHASE3_IMPLEMENTATION.md` - ML similarity phase details

### **Demo Guides:**
- `DEMO_READY.md` - Demo script for presentations
- `HACKATHON_READY.md` - Hackathon judging guide

---

## 🎥 Demo Script

**For presentations or hackathons:**

1. **Introduction (30 sec)**
   - "AI-powered flood monitoring with multi-agent emergency response"
   - "Uses Google's Gemini 2.0 Flash via ADK framework"

2. **Phase 1-5 Demo (2 min)**
   - Click Scenario 1
   - Show progressive phases in monitoring log
   - Point out score building up
   - Highlight AI analysis at each phase

3. **Approval Flow Demo (1 min)**
   - Click Scenario 2
   - Show human-in-the-loop approval at 80 score
   - Explain the 3-tier system (< 60, 60-89, 90+)

4. **Agent Orchestration Demo (2 min)**
   - Select Scenario 1 (Hospital Crisis)
   - Show agent activation
   - **Highlight inter-agent communications:**
     - Point to "Sending 'hospital_crowd_control' to PoliceAgent"
     - Show Police response
     - Explain autonomous coordination

5. **Alternative Flow (1 min)**
   - Select Scenario 2 (Rescue Coordination)
   - Show Rescue → Transport → Police chain
   - Emphasize 4 cross-agent messages

6. **Conclusion (30 sec)**
   - "True multi-agent intelligence"
   - "Human oversight for critical decisions"
   - "Scalable to real-world disaster response"

---

## 🚀 Future Enhancements

- [ ] Real USGS river gauge API integration
- [ ] Live Twitter/X API for social media
- [ ] Real drone imagery processing
- [ ] WebSocket for real-time updates
- [ ] Historical data dashboard
- [ ] Agent performance metrics
- [ ] Multi-disaster support (earthquake, wildfire)
- [ ] Mobile app integration
- [ ] Voice notifications

---

## 📄 License

This project is for educational and demonstration purposes.

---

## 👥 Credits

Built using:
- Google Agent Development Kit (ADK)
- Gemini 2.0 Flash Experimental
- Streamlit
- FastAPI
- Pydantic

---

## 📞 Support

For issues or questions:
1. Check logs in `backend.log` and `frontend.log`
2. Review troubleshooting section above
3. Clear cache and restart services

---

**Last Updated:** October 3, 2025  
**System Status:** ✅ Production Ready  
**Version:** 1.0.0

