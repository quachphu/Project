# 📂 Project Structure Reference

## Quick Navigation

```
agent-starter-pack/
├── 🚀 START HERE
│   ├── README.md                    ← Main documentation (START HERE!)
│   ├── start_demo.sh               ← One-click startup script
│   └── PROJECT_STRUCTURE.md        ← This file
│
├── 🌊 MAIN APPLICATION (flood-monitoring-demo/)
│   ├── app/
│   │   ├── backend.py              ← FastAPI server (http://localhost:8000)
│   │   ├── frontend.py             ← Streamlit UI (http://localhost:8501)
│   │   ├── flood_coordinator.py    ← Phase orchestration
│   │   └── agent_client.py         ← Bridge to ADK agents
│   │
│   ├── mock_data/                  ← Simulated sensor data
│   │   ├── weather_alert.py        ← NWS weather alerts
│   │   ├── river_gauge_data.py     ← USGS river sensors
│   │   ├── ml_similarity.py        ← ML pattern matching
│   │   ├── x_posts.py              ← Social media posts
│   │   └── historical_events.csv   ← Historical flood data
│   │
│   ├── drone_images/               ← AI vision analysis images
│   │   ├── scenario_1/             ← High-risk flood imagery
│   │   └── scenario_2/             ← Medium-risk flood imagery
│   │
│   ├── venv/                       ← Python virtual environment
│   ├── requirements.txt            ← Python dependencies
│   ├── backend.log                 ← Backend logs
│   └── frontend.log                ← Frontend logs
│
├── 🤖 AGENT SYSTEM (my-awesome-agent/)
│   ├── app/
│   │   ├── agents/
│   │   │   ├── decision_maker_adk.py      ← Master orchestrator
│   │   │   └── agents_adk.py              ← 7 specialized agents:
│   │   │       ├── CommunicationAlertAgent
│   │   │       ├── PoliceAgent
│   │   │       ├── HospitalEMSAgent
│   │   │       ├── RescueAgent
│   │   │       ├── UtilityAgent
│   │   │       ├── TransportationEvacAgent
│   │   │       └── ReliefShelterAgent
│   │   │
│   │   └── tools/                   ← Agent capabilities (not used in demo)
│   │
│   ├── pyproject.toml              ← ADK project config
│   └── uv.lock                     ← Dependency lock file
│
└── 📚 REFERENCE (reference/)
    └── agentic-adk-hackathon/      ← Original reference implementation
```

---

## 🗂️ File Types & Purposes

### **Core Application Files**

| File | Purpose | When to Edit |
|------|---------|--------------|
| `backend.py` | FastAPI server, phase logic, score thresholds | Change scoring, add phases |
| `frontend.py` | Streamlit UI, monitoring log display | Change UI, add visualizations |
| `flood_coordinator.py` | Coordinates phases 1-6, calls agents | Add new phases |
| `agent_client.py` | Imports ADK agents into flood system | Modify agent interface |

### **Mock Data Files**

| File | Purpose | Scenario Data |
|------|---------|---------------|
| `weather_alert.py` | NWS weather alerts | 3 scenarios (severe, medium, low) |
| `river_gauge_data.py` | USGS river sensors | Water levels, flow rates |
| `ml_similarity.py` | Historical pattern matching | Similar flood events |
| `x_posts.py` | Twitter/X social media | Real-time citizen reports |
| `historical_events.csv` | Past flood database | 1000+ historical events |

### **Agent Files**

| File | Purpose | Agents |
|------|---------|--------|
| `decision_maker_adk.py` | Master orchestrator | DecisionMakerAgent |
| `agents_adk.py` | All 7 specialized agents | Police, Hospital, Rescue, etc. |

### **Documentation Files**

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Complete system guide | Everyone (START HERE) |
| `QUICK_START.md` | 5-minute quickstart | First-time users |
| `ARCHITECTURE.txt` | Technical details | Developers |
| `DEMO_READY.md` | Presentation script | Demo presenters |
| `HACKATHON_READY.md` | Judging guide | Hackathon judges |
| `ORCHESTRATION_INTEGRATION.md` | How agents integrate | Developers |
| `DYNAMIC_SCENARIO_GUIDE.md` | Scenario system | Content creators |

---

## 🔄 Data Flow

```
1. USER CLICKS SCENARIO
   └─> frontend.py (Streamlit UI)
       └─> trigger_scenario() function

2. SEND TO BACKEND
   └─> POST http://localhost:8000/api/alerts/weather
       └─> backend.py: receive_weather_alert()

3. PHASE 1-5 EXECUTION
   ├─> Phase 1: AI Weather Analysis (0-25 pts)
   │   └─> mock_data/weather_alert.py
   │
   ├─> Phase 2: River Gauge Monitoring (0-25 pts)
   │   └─> mock_data/river_gauge_data.py
   │
   ├─> Phase 3: ML Similarity (0-20 pts)
   │   └─> mock_data/ml_similarity.py
   │
   ├─> Phase 4: Social Media Analysis (0-15 pts)
   │   └─> mock_data/x_posts.py
   │
   └─> Phase 5: Drone Vision AI (0-15 pts)
       └─> drone_images/scenario_X/

4. SCORE EVALUATION
   ├─> Score < 60: Stop
   ├─> Score 60-89: Request approval
   └─> Score 90+: Auto-approve

5. ORCHESTRATION (if approved)
   └─> flood_coordinator.py: process_orchestration_phase()
       └─> agent_client.py: invoke_decision_maker()
           └─> my-awesome-agent/app/agents/decision_maker_adk.py
               ├─> Simulate disaster scenario
               ├─> Activate 7 agents
               ├─> Enable inter-agent communication
               └─> Return results

6. DISPLAY RESULTS
   └─> Events stored in backend.py: events_store[]
       └─> Frontend polls: GET /api/events
           └─> frontend.py: Display monitoring log
```

---

## 🎯 Key Integration Points

### **1. Frontend ↔ Backend Communication**

**Location:** `frontend.py` line ~660-680

```python
# Frontend sends scenario trigger
response = requests.post(
    f"{BACKEND_URL}/api/alerts/weather",
    json=payload
)
```

**Backend receives:** `backend.py` line ~167

```python
@app.post("/api/alerts/weather")
async def receive_weather_alert(alert: WeatherAlert):
    # Process phases 1-5
```

---

### **2. Backend → Agent System Integration**

**Location:** `backend.py` line ~427-441

```python
# Trigger orchestration
orchestration_result = process_orchestration_phase(
    alert_dict,
    final_cumulative_score,
    scenario=scenario
)
```

**Agent Coordinator:** `flood_coordinator.py` line ~112-173

```python
def process_orchestration_phase(alert_data, total_score, scenario=1):
    # Import ADK agents
    from app.agent_client import invoke_decision_maker
    
    # Run simulation
    result = invoke_decision_maker(
        disaster_type="flood",
        location=location,
        scenario=scenario
    )
```

**Agent Client:** `agent_client.py`

```python
# Bridge to ADK
sys.path.insert(0, ADK_AGENT_PATH)
from agents.decision_maker_adk import DecisionMakerAgent

def invoke_decision_maker(disaster_type, location, scenario):
    agent = DecisionMakerAgent()
    return agent.simulate(disaster_type, location, scenario)
```

---

### **3. Inter-Agent Communication**

**Location:** `my-awesome-agent/app/agents/agents_adk.py`

**Example: Hospital → Police**

```python
# HospitalEMSAgent (line ~155)
if self.icu_beds < 10:
    self._log(f"⚠️ CRITICAL: Only {self.icu_beds} ICU beds!")
    if police_agent:
        response = self.send_message(
            police_agent,
            "hospital_crowd_control",
            {"reason": "ICU overwhelmed"}
        )

# PoliceAgent (line ~90)
def receive_message(self, action, payload):
    if action == "hospital_crowd_control":
        self._log("🚨 URGENT: Hospital crowd control requested")
        self._log(f"🚔 Dispatching {units} additional units")
        return {"status": "deployed", "units": units}
```

---

## 📊 Score Thresholds & Configuration

### **Where to Find Score Logic**

| Configuration | File | Line(s) | Default |
|---------------|------|---------|---------|
| Phase 3 trigger | `backend.py` | ~205 | 15 points |
| Phase 4 trigger | `backend.py` | ~266 | 25 points |
| Phase 5 trigger | `backend.py` | ~328 | 35 points |
| Approval threshold | `backend.py` | ~400 | 60 points |
| Auto-approve threshold | `backend.py` | ~393 | 90 points |
| Phase 1 max score | `backend.py` | ~192 | 25 points |
| Phase 2 max score | `backend.py` | ~254 | 25 points |
| Phase 3 max score | `backend.py` | ~316 | 20 points |
| Phase 4 max score | `backend.py` | ~379 | 15 points |
| Phase 5 max score | `backend.py` | ~391 | 15 points |

---

## 🧪 Testing Quick Reference

### **Scenario Scoring**

| Scenario | Severity | Precipitation | Expected Score | Orchestration |
|----------|----------|---------------|----------------|---------------|
| Scenario 1 | 4/5 | 120mm | ~93/100 | Auto-approved |
| Scenario 2 | 3/5 | 95mm | ~80/100 | Requires approval |
| Scenario 3 | 1/5 | 25mm | ~25/100 | No orchestration |

### **Test Commands**

```bash
# Start system
./start_demo.sh

# Check backend
curl http://localhost:8000/

# Check events
curl http://localhost:8000/api/events | python3 -m json.tool

# View logs
tail -f flood-monitoring-demo/backend.log
tail -f flood-monitoring-demo/frontend.log

# Stop system
pkill -f backend.py
pkill -f streamlit
```

---

## 🔧 Common Customizations

### **1. Add a New Scenario**

**File:** `flood-monitoring-demo/mock_data/weather_alert.py`

```python
scenarios = {
    "your_new_scenario": {
        "precipitation_probability": 70,
        "expected_precipitation_mm": 85,
        "severity_level": 3,
        "description": "Your custom scenario description"
    }
}
```

### **2. Add a New Agent**

**File:** `my-awesome-agent/app/agents/agents_adk.py`

```python
class YourNewAgent(BaseADKAgent):
    def __init__(self):
        super().__init__(
            name="YourNewAgent",
            description="What your agent does"
        )
    
    def receive_message(self, action, payload):
        # Process incoming messages
        pass
```

**Register in:** `decision_maker_adk.py`

### **3. Adjust UI Display**

**File:** `flood-monitoring-demo/app/frontend.py`

- **Monitoring log:** Line ~185-400
- **Sidebar:** Line ~75-165
- **Color scheme:** Line ~61-73

---

## 📞 Need Help?

**Issue locations:**

- **Backend errors:** Check `backend.log`
- **Frontend errors:** Check `frontend.log`
- **Agent errors:** Check terminal output
- **Connection issues:** Ensure both services running

**Quick fixes:**

```bash
# Nuclear restart
pkill -f backend.py; pkill -f streamlit
rm -rf flood-monitoring-demo/app/__pycache__
./start_demo.sh
```

---

**Last Updated:** October 3, 2025

