# 🌊 System Overview - AI Flood Monitoring & Emergency Response

## 🎯 One-Sentence Summary

**An AI-powered disaster monitoring system that progressively assesses flood risk through 5 phases (0-100 score), requires human approval for medium-risk scenarios (60-89), then orchestrates 7 specialized AI agents with autonomous inter-agent communication for emergency response.**

---

## 🔄 Complete System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)                    │
│                     http://localhost:8501                        │
│                                                                  │
│  [Scenario 1] [Scenario 2] [Scenario 3]  ← User clicks          │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │         MONITORING LOG (Real-time Events)          │         │
│  │  • Phase 1: Weather Alert (AI Analysis)            │         │
│  │  • Phase 2: River Gauge (Sensor Data)              │         │
│  │  • Phase 3: ML Similarity (Pattern Match)          │         │
│  │  • Phase 4: Social Media (Sentiment Analysis)      │         │
│  │  • Phase 5: Drone Vision (Image AI)                │         │
│  │  • Score: 80/100 ⚠️ APPROVAL REQUIRED              │         │
│  │  • [✅ APPROVE] [❌ REJECT]                          │         │
│  │  • Phase 6: Orchestration (7 agents activated)     │         │
│  │  • 🏥→🚔 Hospital requests police support           │         │
│  │  • 🚤→🚌 Rescue coordinates with transport          │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ┌──────────────────────┐                                       │
│  │  SCORE: 80/100       │                                       │
│  │  Phase 1: ✅ (18 pts)│                                       │
│  │  Phase 2: ✅ (20 pts)│                                       │
│  │  Phase 3: ✅ (18 pts)│                                       │
│  │  Phase 4: ✅ (12 pts)│                                       │
│  │  Phase 5: ✅ (12 pts)│                                       │
│  │  ⚠️ HUMAN APPROVAL   │                                       │
│  └──────────────────────┘                                       │
└─────────────────────────────────────────────────────────────────┘
                              ▼
                    POST /api/alerts/weather
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BACKEND SERVER (FastAPI)                       │
│                    http://localhost:8000                         │
│                                                                  │
│  📥 RECEIVE WEATHER ALERT                                        │
│      └─> WeatherAlert object (Pydantic)                         │
│                                                                  │
│  🔄 PHASE 1-5 EXECUTION LOOP                                     │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │  PHASE 1: AI Weather Analysis                      │         │
│  │  ├─> Call: weather_alert.get_alert()               │         │
│  │  ├─> AI processes NWS data                         │         │
│  │  └─> Score: 0-25 points                            │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │  PHASE 2: River Gauge Monitoring (if score >= 15)  │         │
│  │  ├─> Call: river_gauge_data.get_gauge_data()       │         │
│  │  ├─> Analyze water levels, flow rates              │         │
│  │  └─> Score: 0-25 points (cumulative: 0-50)         │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │  PHASE 3: ML Similarity (if score >= 25)           │         │
│  │  ├─> Call: ml_similarity.analyze()                 │         │
│  │  ├─> Compare to 1000+ historical floods            │         │
│  │  └─> Score: 0-20 points (cumulative: 0-70)         │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │  PHASE 4: Social Media (if score >= 35)            │         │
│  │  ├─> Call: x_posts.get_posts()                     │         │
│  │  ├─> Sentiment analysis of citizen reports         │         │
│  │  └─> Score: 0-15 points (cumulative: 0-85)         │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │  PHASE 5: Drone Vision AI (if score >= 45)         │         │
│  │  ├─> Load: drone_images/scenario_X/                │         │
│  │  ├─> AI image analysis (Gemini Vision)             │         │
│  │  └─> Score: 0-15 points (cumulative: 0-100)        │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  🎯 DECISION POINT                                               │
│  ├─> Score < 60:  ❌ No orchestration                           │
│  ├─> Score 60-89: ⚠️ Create approval_required event             │
│  └─> Score 90+:   ✅ Create orchestration_pending event         │
│                                                                  │
│  👤 HUMAN APPROVAL (for 60-89)                                   │
│  ├─> POST /api/orchestration/approve                            │
│  └─> Convert to orchestration_approved event                    │
│                                                                  │
│  🚀 SCENARIO SELECTION                                           │
│  ├─> POST /api/orchestration/trigger?scenario=1                 │
│  └─> Call: process_orchestration_phase()                        │
└─────────────────────────────────────────────────────────────────┘
                              ▼
                flood_coordinator.py
                              ▼
                   agent_client.py
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              AGENT SYSTEM (Google ADK + Gemini 2.0)              │
│                  my-awesome-agent/app/agents/                    │
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │            DECISION MAKER AGENT                     │         │
│  │          (Master Orchestrator)                      │         │
│  │                                                     │         │
│  │  def simulate(disaster_type, location, scenario):  │         │
│  │    ├─> Determine sos_count based on scenario       │         │
│  │    ├─> Activate 7 specialized agents               │         │
│  │    ├─> Enable inter-agent communication            │         │
│  │    └─> Collect and return results                  │         │
│  └────────────────────────────────────────────────────┘         │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │           7 SPECIALIZED AGENTS                    │           │
│  └──────────────────────────────────────────────────┘           │
│                                                                  │
│  1️⃣ CommunicationAlertAgent                                     │
│     └─> Mass notifications, emergency broadcasts                │
│                                                                  │
│  2️⃣ PoliceAgent                                                 │
│     ├─> Traffic control, crowd management                       │
│     └─> Receives: hospital_crowd_control, clear_evacuation_route│
│                                                                  │
│  3️⃣ HospitalEMSAgent                                            │
│     ├─> Medical response, ambulances, ICU beds                  │
│     ├─> Sends: hospital_crowd_control → Police                  │
│     └─> Receives: request_medical_support from Relief           │
│                                                                  │
│  4️⃣ RescueAgent                                                 │
│     ├─> Water rescue, evacuation operations                     │
│     ├─> Sends: request_pickup_locations → Transport             │
│     └─> Sends: clear_evacuation_route → Police (×3)             │
│                                                                  │
│  5️⃣ UtilityAgent                                                │
│     └─> Infrastructure shutdown, power/gas safety               │
│                                                                  │
│  6️⃣ TransportationEvacAgent                                     │
│     ├─> Bus evacuation routes, mass transit                     │
│     └─> Receives: request_pickup_locations from Rescue          │
│                                                                  │
│  7️⃣ ReliefShelterAgent                                          │
│     ├─> Shelter setup, supplies distribution                    │
│     └─> Sends: request_medical_support → Hospital               │
│                                                                  │
│  🔗 INTER-AGENT COMMUNICATION FLOW                               │
│                                                                  │
│  Scenario 1 (Hospital Crisis):                                  │
│    HospitalEMS ──(crowd_control)──> Police                      │
│                                                                  │
│  Scenario 2 (Rescue Coordination):                              │
│    Rescue ──(request_pickup)──> Transport                       │
│    Transport ──(response)──> Rescue                             │
│    Rescue ──(clear_route×3)──> Police                           │
│    Relief ──(request_medical)──> Hospital                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▼
                  Results with internal_logs
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND PROCESSES RESULTS                     │
│                                                                  │
│  📝 Create Events:                                               │
│     ├─> orchestration_triggered                                 │
│     ├─> orchestration_summary                                   │
│     └─> agent_response (×7, one per agent)                      │
│                                                                  │
│  💾 Store in events_store[]                                      │
│                                                                  │
│  📡 Frontend polls: GET /api/events                              │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND DISPLAYS RESULTS                     │
│                                                                  │
│  🎨 Color-coded monitoring log:                                  │
│     🔴 Red: CRITICAL, URGENT messages                            │
│     🟢 Green: SUCCESS, completed actions                         │
│     🟡 Yellow: WARNINGS, coordination                            │
│     🔵 Blue: INFO, progress updates                              │
│                                                                  │
│  🔗 Inter-Agent Communication Section:                           │
│     "🏥 HospitalEMS → 🚔 Police: hospital_crowd_control"         │
│     "✅ Police response: {status: deployed, units: 5}"           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Score Thresholds Decision Tree

```
Weather Alert Received
         │
         ▼
    PHASE 1: Weather Analysis (0-25)
         │
         ▼
  Score >= 15? ──NO──> Stop (Score < 15)
         │ YES
         ▼
    PHASE 2: River Gauge (0-25)
         │
         ▼
  Score >= 25? ──NO──> Stop (Score 15-24)
         │ YES
         ▼
    PHASE 3: ML Similarity (0-20)
         │
         ▼
  Score >= 35? ──NO──> Stop (Score 25-34)
         │ YES
         ▼
    PHASE 4: Social Media (0-15)
         │
         ▼
  Score >= 45? ──NO──> Stop (Score 35-44)
         │ YES
         ▼
    PHASE 5: Drone Vision (0-15)
         │
         ▼
    FINAL SCORE (0-100)
         │
         ├─> < 60: ❌ No Action (Continue Monitoring)
         │
         ├─> 60-89: ⚠️ HUMAN APPROVAL REQUIRED
         │           │
         │           ├─> User clicks ✅ APPROVE
         │           │   └─> SELECT SCENARIO
         │           │
         │           └─> User clicks ❌ REJECT
         │               └─> Stop (Monitoring continues)
         │
         └─> 90-100: ✅ AUTO-APPROVED
                     └─> SELECT SCENARIO (direct)
```

---

## 🎭 Scenario Comparison

### **Scenario 1: High Risk - Hospital Crisis**

```
INPUT DATA:
├─> Severity: 4/5
├─> Precipitation: 120mm
└─> Probability: 90%

PHASES:
├─> Phase 1: 23/25 ✅
├─> Phase 2: 24/25 ✅
├─> Phase 3: 18/20 ✅
├─> Phase 4: 14/15 ✅
└─> Phase 5: 14/15 ✅

TOTAL SCORE: ~93/100 → 🚨 AUTO-APPROVED

ORCHESTRATION FOCUS:
├─> Hospital: LOW ICU beds (2-5)
├─> sos_count: 15
└─> Inter-Agent Communication:
    └─> Hospital ──(crowd_control)──> Police
        └─> Police deploys 3-6 units

AGENTS ACTIVATED:
✅ All 7 agents
```

### **Scenario 2: Medium Risk - Rescue Coordination**

```
INPUT DATA:
├─> Severity: 3/5
├─> Precipitation: 95mm
└─> Probability: 75%

PHASES:
├─> Phase 1: 18/25 ✅
├─> Phase 2: 20/25 ✅
├─> Phase 3: 18/20 ✅
├─> Phase 4: 12/15 ✅
└─> Phase 5: 12/15 ✅

TOTAL SCORE: ~80/100 → ⚠️ HUMAN APPROVAL REQUIRED

USER ACTION:
├─> System pauses
├─> Shows: "⚠️ ELEVATED CONFIDENCE (80/100)"
├─> User clicks ✅ APPROVE
└─> Scenario selection appears

ORCHESTRATION FOCUS:
├─> Rescue: HIGH evacuation demand
├─> sos_count: 45
└─> Inter-Agent Communication:
    ├─> Rescue ──(request_pickup)──> Transport
    ├─> Transport ──(3 locations)──> Rescue
    ├─> Rescue ──(clear_route)──> Police (×3)
    └─> Relief ──(medical_support)──> Hospital

AGENTS ACTIVATED:
✅ All 7 agents
```

### **Scenario 3: Low Risk - No Orchestration**

```
INPUT DATA:
├─> Severity: 1/5
├─> Precipitation: 25mm
└─> Probability: 30%

PHASES:
├─> Phase 1: 8/25 ✅
└─> Phase 2: 7/25 ✅

TOTAL SCORE: ~25/100 → ❌ BELOW THRESHOLD

RESULT:
├─> Phase 3 doesn't trigger (< 25)
├─> System stops at Phase 2
└─> "Continue monitoring" message

AGENTS ACTIVATED:
❌ None (score < 60)
```

---

## 🔗 Inter-Agent Communication Examples

### **Example 1: Hospital → Police (Scenario 1)**

```python
# In HospitalEMSAgent
if self.icu_beds < 10:
    self._log("⚠️ CRITICAL: Only 2 ICU beds available!")
    self._log("⚠️ Requesting police support...")
    
    response = self.send_message(
        police_agent,
        "hospital_crowd_control",
        {"reason": "ICU overwhelmed", "beds": 2}
    )
    
    self._log(f"✅ Police responded: {response['status']}")

# In PoliceAgent
def receive_message(self, action, payload):
    if action == "hospital_crowd_control":
        self._log("🚨 URGENT: Hospital crowd control requested")
        units = random.randint(3, 6)
        self._log(f"🚔 Dispatching {units} additional units")
        return {"status": "deployed", "units": units}
```

**Frontend Display:**

```
🏥 HospitalEMS Agent Activated
  └─ 🔗 ⚠️ CRITICAL: Only 2 ICU beds available!
  └─ 🔗 Requesting police support...
  └─ 🔗 Sending 'hospital_crowd_control' to PoliceAgent
  └─ 🔗 ✅ Police responded: deployed

🚔 Police Agent Activated
  └─ 🔗 ⚠️ 🚨 URGENT: Hospital crowd control requested
  └─ 🔗 ⚠️ 🚔 Dispatching 5 additional units for crowd control
```

---

### **Example 2: Rescue → Transport → Police (Scenario 2)**

```python
# Step 1: Rescue requests pickup locations
response = self.send_message(
    transport_agent,
    "request_pickup_locations",
    {"evacuation_zone": "flood_area"}
)
pickup_points = response.get("pickup_points", [])

# Step 2: Transport responds
def receive_message(self, action, payload):
    if action == "request_pickup_locations":
        points = ["Main St & 5th", "Park Plaza", "City Hall"]
        return {"pickup_points": points}

# Step 3: Rescue requests route clearance for each point
for point in pickup_points:
    self.send_message(
        police_agent,
        "clear_evacuation_route",
        {"location": point}
    )
```

**Frontend Display:**

```
🚤 Rescue Agent Activated
  └─ 🔗 Requesting pickup locations from TransportAgent
  └─ 🔗 ✅ Received 3 pickup locations
  └─ 🔗 Requesting route clearance for Main St & 5th
  └─ 🔗 Requesting route clearance for Park Plaza
  └─ 🔗 Requesting route clearance for City Hall

🚌 Transportation Agent Activated
  └─ 🔗 ⚠️ Pickup location request from RescueAgent
  └─ 🔗 ✅ Providing 3 evacuation pickup points

🚔 Police Agent Activated
  └─ 🔗 ⚠️ 🚨 Route clearance for Main St & 5th
  └─ 🔗 ⚠️ 🚨 Route clearance for Park Plaza
  └─ 🔗 ⚠️ 🚨 Route clearance for City Hall
```

---

## 🎨 Frontend Color Coding

| Color | Emoji | Message Type | Example |
|-------|-------|--------------|---------|
| 🔴 Red | ⚠️, 🚨 | CRITICAL, URGENT | "⚠️ CRITICAL: Only 2 ICU beds!" |
| 🟢 Green | ✅ | SUCCESS, Completed | "✅ Police responded: deployed" |
| 🟡 Yellow | ⚠️ | WARNING, Coordination | "⚠️ Requesting police support" |
| 🔵 Blue | 📊, 🔗 | INFO, Progress | "🔗 Sending message to Police" |

---

## 📈 Key Metrics

| Metric | Value | Description |
|--------|-------|-------------|
| **Max Score** | 100 | Total cumulative risk score |
| **Phases** | 5 | Progressive monitoring phases |
| **Agents** | 7 | Specialized response agents |
| **Scenarios** | 2 | Dynamic orchestration scenarios |
| **Inter-Agent Messages** | 1-6 | Cross-agent communications per scenario |
| **Response Time** | ~15s | Phase 1-5 completion time |
| **Orchestration Time** | ~20s | Agent simulation time |

---

## 🚀 Technology Stack Summary

```
┌─────────────────────────────────────────┐
│           FRONTEND LAYER                │
│  • Streamlit (Python)                   │
│  • Real-time monitoring UI              │
│  • Color-coded event display            │
└─────────────────────────────────────────┘
                  ▲ HTTP
┌─────────────────────────────────────────┐
│           BACKEND LAYER                 │
│  • FastAPI (Python)                     │
│  • RESTful API endpoints                │
│  • Event storage & coordination         │
└─────────────────────────────────────────┘
                  ▲ Python Import
┌─────────────────────────────────────────┐
│           AGENT LAYER                   │
│  • Google ADK Framework                 │
│  • Gemini 2.0 Flash Experimental        │
│  • Pydantic V2 data models              │
│  • Inter-agent message passing          │
└─────────────────────────────────────────┘
                  ▲ API Calls
┌─────────────────────────────────────────┐
│           AI MODEL                      │
│  • Gemini 2.0 Flash (via Vertex AI)     │
│  • Multi-modal (text + images)          │
│  • Natural language understanding       │
└─────────────────────────────────────────┘
```

---

## 🎯 Use Cases

### **1. Emergency Response Training**
- Train emergency coordinators on multi-agency response
- Simulate different disaster scenarios
- Practice human-in-the-loop decision making

### **2. AI Agent Research**
- Study inter-agent communication patterns
- Test hierarchical orchestration models
- Evaluate human-AI collaboration

### **3. Disaster Preparedness**
- Model flood risk assessment workflows
- Test sensor integration strategies
- Validate multi-phase escalation logic

### **4. Hackathon Demos**
- Showcase Google ADK capabilities
- Demonstrate Gemini 2.0 multi-modal AI
- Highlight practical AI applications

---

**Last Updated:** October 3, 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready

