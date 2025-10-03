# Dynamic Scenario-Based Orchestration Guide

## Overview

The flood monitoring system now supports **dynamic scenario selection** at the orchestration phase. When the confidence score reaches 93+, the system **pauses** and prompts the user to select an emergency response scenario, allowing demonstration of different inter-agent communication patterns.

---

## Workflow

### Phase 1-5: Automated Scoring (0-100 points)

The system automatically progresses through phases 1-5, calculating a cumulative confidence score:

1. **Phase 1: Weather Alert** (0-25 points)
2. **Phase 2: River Gauges** (0-25 points)
3. **Phase 3: ML Similarity** (0-20 points)
4. **Phase 4: Social Media** (0-15 points)
5. **Phase 5: Drone Vision** (0-15 points)

**Total Maximum Score:** 100 points

### Phase 6: Orchestration Trigger (Score >= 60)

When the cumulative score reaches **60 or above**, the system:

1. ✅ **STOPS automatic progression**
2. 📊 **Displays**: `orchestration_pending` event
3. 🚨 **Shows**: Two scenario selection buttons in the UI sidebar
4. ⏸️ **Waits**: For user to click a scenario button

---

## Scenario Selection UI

### Location
The scenario buttons appear in the **left sidebar** (score panel) when orchestration is pending.

### Buttons

#### 🏥 **Scenario 1: Hospital Crisis**
*Caption: Hospital overwhelmed → Police crowd control*

#### 🚤 **Scenario 2: Rescue Coordination**
*Caption: Rescue needs routes → Transport + Police coordination*

---

## Scenario Details

### 🏥 Scenario 1: Hospital Overwhelmed

**Initial Conditions:**
- Hospital ICU beds: 2-5 (critically low)
- `force_critical_icu = True`

**Inter-Agent Communication Flow:**

```
1. DecisionMaker → HospitalEMSAgent
   └─ Activates with disaster context

2. HospitalEMSAgent.execute()
   └─ Detects: icu_beds < 10
   └─ Sends message: "hospital_crowd_control" → PoliceAgent
   
3. PoliceAgent.receive_message("hospital_crowd_control")
   └─ Dispatches 15 additional units for crowd control
   └─ Sets station: "Hospital Emergency - Zone A"
   
4. HospitalEMSAgent captures response
   └─ Logs: "Requested police crowd control at hospital"
```

**Key Metrics:**
- Police Cars: 35 total (20 base + 15 crowd control)
- Hospital: 20 ICU beds prepared
- Ambulances: 8 dispatched
- Communication: 1 cross-agent request (Hospital → Police)

---

### 🚤 Scenario 2: Rescue Route Coordination

**Initial Conditions:**
- SOS count: 45 (high evacuation demand)
- `force_evacuation = True`

**Inter-Agent Communication Flow:**

```
1. DecisionMaker → RescueAgent
   └─ Activates with disaster context
   └─ Provides: transport_agent, police_agent references

2. RescueAgent.execute()
   └─ Detects: High SOS count + transport_agent available
   └─ Sends message: "request_pickup_locations" → TransportAgent
   
3. TransportAgent.receive_message("request_pickup_locations")
   └─ Responds with pickup_points: ["Zone A Shelter", "Zone B Center", "Main Square"]
   
4. RescueAgent receives pickup points
   └─ FOR EACH pickup_point:
       └─ Sends message: "clear_evacuation_route" → PoliceAgent
       
5. PoliceAgent.receive_message("clear_evacuation_route")
   └─ FOR EACH route:
       └─ Deploys 8 units to clear route
       └─ Total: 24 units (3 routes × 8 units)

6. RescueAgent captures all responses
   └─ Logs: "Coordinated with Transport for pickup locations"
   └─ Logs: "Requested police to clear 3 evacuation routes"
```

**Key Metrics:**
- Rescue Vehicles: 12 deployed
- Police Cars: 44 total (20 base + 24 route clearing)
- Transport Buses: 15 on evacuation routes
- Communication: 4 cross-agent requests (Rescue → Transport + 3× Rescue → Police)

---

## Backend API

### Endpoint: `POST /api/orchestration/trigger`

**Request:**
```json
{
  "scenario": 1  // or 2
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Orchestration triggered with Scenario 1",
  "scenario": 1,
  "agents_activated": [
    "CommunicationAlertAgent",
    "PoliceAgent",
    "HospitalEMSAgent",
    "RescueAgent",
    "UtilityAgent",
    "TransportationEvacAgent",
    "ReliefShelterAgent"
  ]
}
```

---

## Event Types

### 1. `orchestration_pending`
Triggered when score >= 60, before user selects scenario.

**Data:**
```json
{
  "message": "⚠️ HIGH CONFIDENCE DETECTED (93/65) - SELECT EMERGENCY SCENARIO",
  "confidence_score": 93,
  "threshold": 60,
  "alert_data": { /* original weather alert */ }
}
```

### 2. `orchestration_triggered`
Triggered after user clicks a scenario button.

**Data:**
```json
{
  "message": "⚠️ SCENARIO 1 SELECTED - Activating Emergency Response Coordination",
  "confidence_score": 93,
  "threshold": 60,
  "scenario": 1
}
```

### 3. `orchestration_summary`
Summary of all agent activations.

**Data:**
```json
{
  "summary": {
    "alerts_sent": 50000,
    "police_cars": 35,
    "ambulances": 8,
    "buses": 15,
    "rescue_vehicles": 12,
    "icu_beds": 20,
    "shelter_supplies": 5000
  },
  "agents_activated": [...],
  "scenario": 1
}
```

### 4. `agent_response`
Individual agent response (one per agent).

**Data:**
```json
{
  "agent_name": "PoliceAgent",
  "response": {
    "cars_dispatched": 35,
    "station": "Hospital Emergency - Zone A",
    /* ... other fields ... */
  },
  "scenario": 1
}
```

---

## Code Architecture

### Backend (`backend.py`)

**Lines 391-412:** Check for score >= 60 and create `orchestration_pending` event instead of auto-triggering.

**Lines 460-550:** New endpoint `POST /api/orchestration/trigger` that:
1. Finds the pending event
2. Extracts stored alert_data
3. Calls `process_orchestration_phase(alert_dict, score, scenario=X)`
4. Creates orchestration events

### Coordinator (`flood_coordinator.py`)

**Function:** `process_orchestration_phase(alert_data, total_score, scenario=1)`
- Passes `scenario` parameter to `DecisionMakerAgent.simulate()`

### Decision Maker (`my-awesome-agent/app/agents/decision_maker_adk.py`)

**Function:** `simulate(disaster_type, location, scenario=1)`
- Varies SOS count based on scenario
- Passes agent references to sub-agents for cross-communication
- Sets `force_critical_icu` or `force_evacuation` flags

### Sub-Agents (`my-awesome-agent/app/agents/agents_adk.py`)

**PoliceAgent:**
- Receives: `hospital_crowd_control` (Scenario 1)
- Receives: `clear_evacuation_route` (Scenario 2)

**HospitalEMSAgent:**
- Sends: `hospital_crowd_control` if ICU < 10

**RescueAgent:**
- Sends: `request_pickup_locations` to Transport
- Sends: `clear_evacuation_route` to Police (for each route)

**TransportAgent:**
- Receives: `request_pickup_locations`
- Responds with: `pickup_points` list

### Frontend (`frontend.py`)

**Lines 512-557:** Scenario selection buttons
- Checks for `orchestration_pending` and `orchestration_triggered` events
- Shows buttons only when pending and not yet triggered
- POSTs to `/api/orchestration/trigger` with selected scenario

**Lines 814-825:** Log display for pending/triggered events

**Lines 1033-1047:** Expandable sections for orchestration events

---

## Testing the System

### Step 1: Trigger a Flood Scenario
Click **Scenario 1** or **Scenario 2** button at the top to start the flood monitoring workflow.

### Step 2: Watch Phases 1-5
The system automatically progresses through weather, river, ML, social media, and drone analysis.

### Step 3: Wait for Score >= 60
When the cumulative score reaches 60+:
- ⏸️ System pauses
- 🚨 "CRITICAL THRESHOLD REACHED" message appears
- 📍 Scenario buttons appear in left sidebar

### Step 4: Select Emergency Scenario
Click either:
- 🏥 **Scenario 1: Hospital Crisis**
- 🚤 **Scenario 2: Rescue Coordination**

### Step 5: View Orchestration Results
- See which agents were activated
- View inter-agent communications in agent logs
- Check summary metrics

---

## Key Differences Between Scenarios

| Aspect | Scenario 1 | Scenario 2 |
|--------|-----------|-----------|
| **Focus** | Hospital overcrowding | Rescue route optimization |
| **SOS Count** | 15 (moderate) | 45 (high) |
| **ICU Beds** | 2-5 (critical) | 15-25 (normal) |
| **Police Cars** | 35 (20 + 15 crowd) | 44 (20 + 24 route) |
| **Cross-Agent Calls** | 1 (Hospital → Police) | 4 (Rescue → Transport + 3× Rescue → Police) |
| **Primary Agent** | HospitalEMSAgent | RescueAgent |
| **Secondary Agents** | PoliceAgent | TransportAgent, PoliceAgent |

---

## Demo Script

### For Hackathon/Demo:

1. **Introduction:**
   > "Our system uses AI to monitor flood risks in real-time. Let me show you how it adapts to different emergency scenarios."

2. **Start Monitoring:**
   > "I'll trigger Scenario 1 to simulate a moderate flood risk..."

3. **Explain Phases:**
   > "Watch as our AI agents analyze weather, river gauges, historical patterns, social media, and drone footage..."

4. **Highlight Score:**
   > "The confidence score is building... 25... 50... 75... reaching critical at 93!"

5. **Show Pause:**
   > "Notice the system PAUSED. At 93, it's asking me to choose an emergency response scenario. This shows how our multi-agent system can adapt dynamically."

6. **Explain Scenarios:**
   > "Scenario 1 simulates a hospital overwhelm crisis where agents coordinate crowd control. Scenario 2 shows rescue teams coordinating with police to clear evacuation routes. Let's pick Scenario 1..."

7. **Show Results:**
   > "Look at the orchestration—7 agents activated instantly. The Hospital agent detected low ICU capacity and automatically requested police support for crowd control. This is true inter-agent intelligence."

8. **Repeat for Scenario 2:**
   > "Now let's see Scenario 2... Notice how the Rescue agent coordinates with Transport to get pickup locations, then asks Police to clear multiple routes. Three separate cross-agent communications happening autonomously."

---

## Future Enhancements

### Potential Scenario 3: Shelter Overflow
- Relief Shelter requests medical support from Hospital
- Hospital dispatches ambulances to shelter
- Shelter expands capacity with medical support

### Dynamic Scenario Parameters
- Allow UI to adjust thresholds (ICU beds, SOS count)
- Custom scenario creation
- Real-time scenario switching

### Enhanced Visualizations
- Agent communication graph
- Timeline of inter-agent messages
- Resource allocation charts

---

## Troubleshooting

### Scenario Buttons Don't Appear
- **Check:** Score >= 60?
- **Check:** `orchestration_pending` event in logs?
- **Check:** Backend logs for errors

### Orchestration Fails
- **Check:** Backend logs for `DecisionMakerAgent` errors
- **Check:** API rate limits (Gemini 2.0 Flash)
- **Check:** Agent references passed correctly

### Wrong Scenario Behavior
- **Check:** Scenario parameter in backend logs
- **Check:** Agent `_internal_logs` for communication attempts
- **Check:** Pydantic field assignments in agents

---

## Success Criteria

✅ System pauses at score >= 60  
✅ Scenario buttons appear in UI  
✅ Scenario 1 triggers Hospital → Police communication  
✅ Scenario 2 triggers Rescue → Transport + Police communications  
✅ All 7 agents activate successfully  
✅ Summary metrics display correctly  
✅ Agent responses logged with scenario-specific data  

---

**Last Updated:** October 3, 2025  
**System Status:** ✅ PRODUCTION READY

