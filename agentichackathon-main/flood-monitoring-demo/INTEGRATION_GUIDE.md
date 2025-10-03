# 🤖 AI Agent Integration Guide

## Overview

Your Streamlit flood monitoring app now sends weather alerts to an **AI Orchestrator Agent** powered by **Gemini 2.0 Flash**. You can see the agent's analysis in both:
- **Dev Playground** (for testing iterations)
- **Streamlit UI** (for final demo)

---

## 🎯 How It Works

```
Streamlit UI (Click Scenario 1)
    ↓
Generate Weather Alert JSON
    ↓
POST to Backend (/api/alerts/weather)
    ↓
Backend invokes AI Orchestrator Agent
    ↓
AI Agent processes alert using tools:
  - process_weather_alert()
  - analyze_flood_risk()
    ↓
Agent returns analysis
    ↓
Display in Streamlit UI + See in Playground
```

---

## 🚀 Quick Start

### Step 1: Test the Agent (Optional but Recommended)

```bash
cd flood-monitoring-demo
python test_agent_integration.py
```

This verifies the AI agent is working before you start the full system.

### Step 2: Start Backend (with AI Agent)

```bash
python app/backend.py
```

You'll see:
```
🚀 Starting Flood Monitoring Backend...
📍 Backend URL: http://localhost:8000
```

### Step 3: Start Frontend

```bash
streamlit run app/frontend.py
```

Browser opens to: http://localhost:8501

### Step 4: Test the Flow

1. Click **"🌧️ Scenario 1: Moderate Flood"** button
2. Wait 5-10 seconds for AI agent to process
3. See **two events** appear in timeline:
   - Weather Alert (the JSON you sent)
   - **AI Agent Response** (the analysis)
4. Click **"📋 View Details"** on the AI Agent Response
5. See the agent's full analysis with risk assessment

---

## 🎮 Using the Dev Playground

The dev playground lets you test the AI agent **independently** from the Streamlit app.

### Start the Playground

```bash
cd /Users/parichaypothepalli/Downloads/agent-starter-pack/my-awesome-agent
make playground
```

Opens at: http://localhost:8501 (different from flood monitoring UI)

### Test in Playground

In the chat, type:

```
I have a weather alert. Analyze it:
{
  "alert_id": "WX-FLOOD-TEST",
  "severity": {"level": 3},
  "precipitation": {"expected_amount_mm": 95, "probability_percent": 75},
  "location": {"region": "Northern Valley"},
  "message": "Heavy rainfall expected"
}
```

The agent will:
1. Process the alert
2. Analyze flood risk
3. Provide recommendations

**This is the SAME agent that runs when you click Scenario 1 in Streamlit!**

---

## 🔄 Iteration Workflow for Hackathon

### For Agent Logic Changes:

1. **Edit agent files** in `my-awesome-agent/app/`:
   - `agents/flood_orchestrator.py` - Change agent instructions
   - `tools/flood_monitoring_tools.py` - Change tool logic

2. **Test in Playground**:
   ```bash
   cd my-awesome-agent
   make playground
   ```
   - Try different inputs
   - See agent responses immediately
   - Iterate on prompts/tools

3. **Test in Streamlit** (once satisfied):
   - Keep backend running (it auto-imports agent)
   - Click Scenario 1 in Streamlit
   - See full integration

### For UI Changes:

1. **Edit** `flood-monitoring-demo/app/frontend.py`
2. **Save** - Streamlit auto-reloads
3. **Test** - Click buttons, see updates

---

## 📊 What the AI Agent Does

### Tool 1: `process_weather_alert()`
- Receives weather JSON
- Assesses severity (1-5 scale)
- Determines risk level (LOW/MODERATE/HIGH/CRITICAL)
- Decides if additional monitoring needed
- Returns formatted assessment

### Tool 2: `analyze_flood_risk()`
- Analyzes overall flood risk
- Calculates risk score
- Provides recommendations
- Includes confidence level

### Agent Behavior:
The agent is instructed to:
1. Immediately process incoming alerts
2. Use both tools for complete analysis
3. Provide structured, clear output
4. Make actionable recommendations
5. Trigger additional monitoring if severity ≥ 3/5

---

## 🎬 Demo Flow

### For Your Hackathon Presentation:

**Option A: Show Streamlit Only** (Simplest)
1. Open Streamlit UI
2. Click "Scenario 1"
3. Show weather alert appears
4. Show AI agent response appears
5. Expand and read AI analysis
6. "This is AI-powered real-time analysis"

**Option B: Show Both** (More Impressive)
1. Have **two browser windows** open:
   - Left: Dev Playground (my-awesome-agent)
   - Right: Streamlit (flood-monitoring-demo)
2. In playground, paste a weather alert JSON
3. Show agent's analysis
4. "Now let's see this integrated"
5. Switch to Streamlit, click Scenario 1
6. Show same agent responding to button click
7. "Same AI, integrated into monitoring system"

---

## 🛠️ Files Created

### In `my-awesome-agent/app/`:
- `agents/flood_orchestrator.py` - The AI agent
- `tools/flood_monitoring_tools.py` - Agent's tools

### In `flood-monitoring-demo/app/`:
- `agent_client.py` - Connects to AI agent
- Updated `backend.py` - Invokes agent
- Updated `frontend.py` - Displays agent responses

---

## 🐛 Troubleshooting

### "Agent not available" in UI

**Check 1:** Is the path correct?
```bash
ls /Users/parichaypothepalli/Downloads/agent-starter-pack/my-awesome-agent/app/agents/flood_orchestrator.py
```

**Check 2:** Are dependencies installed?
```bash
cd my-awesome-agent
make install
```

**Check 3:** Check backend logs
Look for:
```
✅ Agent available
```
or
```
⚠️ Agent not found. Running in mock mode.
```

### Agent takes too long (timeout)

Increase timeout in `frontend.py`:
```python
timeout=60  # Increase from 30
```

### Want to see detailed agent logs

Run backend in terminal and watch for:
```
🤖 Invoking AI Orchestrator Agent...
✅ Agent responded successfully
```

---

## 💡 Tips for Hackathon

### Make Agent More Impressive:

1. **Add more decision logic** in `flood_monitoring_tools.py`:
   - "If severity ≥ 4, immediately evacuate"
   - "If precipitation > 100mm, activate emergency protocol"

2. **Improve agent instructions** in `flood_orchestrator.py`:
   - "Compare with historical flood data"
   - "Consider population density in risk scoring"

3. **Add visualization** in Streamlit:
   - Extract risk score from agent response
   - Show as progress bar or gauge

### Demo Script:

**"Watch this: I click this button..."** [Click Scenario 1]

**"The system generates a weather alert and sends it to our AI orchestrator..."** [Point to weather alert card]

**"Within seconds, the AI analyzes the data using multiple tools and provides recommendations..."** [Point to AI response card]

**"Expand this to see the full analysis..."** [Click View Details]

**"The AI determined this is MODERATE risk, severity 3 out of 5, and recommends deploying river gauges and satellite monitoring. This analysis would take a human analyst 15-30 minutes. Our AI does it instantly."**

---

## 🎯 Next Steps to Build On

After the weather alert + AI analysis works, you can add:

### Step 2: River Gauge Monitoring
- Add tool: `trigger_river_gauges()`
- If AI says "deploy sensors", automatically trigger
- Show sensor data in UI

### Step 3: Satellite Imagery
- Add tool: `analyze_satellite_images()`
- Mock 9 images with flood scores
- Display in grid

### Step 4: Social Media Monitoring
- Add tool: `monitor_social_media()`
- Show word cloud of keywords

Each step adds to the timeline, showing progressive monitoring!

---

## ✅ Current Status

✅ AI Agent created and configured  
✅ Backend integrated with agent  
✅ Frontend displays agent responses  
✅ Can test in dev playground  
✅ Can test end-to-end in Streamlit  
✅ Ready for hackathon demo  

---

**🎉 You now have a working AI-powered flood monitoring system!**

Test it, iterate on the agent's logic in the playground, and prepare your demo!

