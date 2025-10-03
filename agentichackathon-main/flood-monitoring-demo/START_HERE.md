# 🌊 START HERE - Flood Monitoring + AI Agent System

## 🎯 What You Have

A complete AI-powered flood monitoring system where:
1. **You click a button in Streamlit UI**
2. **System sends weather alert JSON to AI Agent** 
3. **AI Agent (Gemini 2.0 Flash) analyzes the data**
4. **You see the results in BOTH:**
   - Dev Playground (for testing/iteration)
   - Streamlit UI (for demo)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start Backend (with AI Agent)
```bash
cd /Users/parichaypothepalli/Downloads/agent-starter-pack/flood-monitoring-demo
python app/backend.py
```

**Expected output:**
```
🚀 Starting Flood Monitoring Backend...
📍 Backend URL: http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Leave this running!**

---

### Step 2: Start Streamlit UI (New Terminal)
```bash
cd /Users/parichaypothepalli/Downloads/agent-starter-pack/flood-monitoring-demo
streamlit run app/frontend.py
```

**Browser opens to:** http://localhost:8501

**Leave this running!**

---

### Step 3: Test It!

1. **In Streamlit UI**, click **"🌧️ Scenario 1: Moderate Flood"**
2. **Wait 5-10 seconds** (AI is processing)
3. **See TWO events appear:**
   - 🌧️ Weather Alert
   - 🤖 AI Agent Response
4. **Click "📋 View Details" on AI Agent Response**
5. **Read the AI's analysis!**

---

## 🎮 Dev Playground (For Testing Agent)

Want to test the AI agent separately? Open a **third terminal**:

```bash
cd /Users/parichaypothepalli/Downloads/agent-starter-pack/my-awesome-agent
make playground
```

**New browser tab opens to:** http://localhost:8501 (different port or instance)

**In the playground, type:**
```
Analyze this weather alert: {"alert_id": "TEST", "severity": {"level": 3}, "precipitation": {"expected_amount_mm": 95}, "location": {"region": "Valley"}, "message": "Heavy rain expected"}
```

**The agent will:**
- Process the alert
- Analyze flood risk
- Give recommendations

**This is the SAME agent that responds when you click Scenario 1!**

---

## 📁 What's Where

### Your Project Has Two Parts:

#### 1. Flood Monitoring App (`flood-monitoring-demo/`)
```
flood-monitoring-demo/
├── app/
│   ├── frontend.py          # Streamlit UI
│   ├── backend.py            # FastAPI server
│   └── agent_client.py       # Connects to AI agent
├── mock_data/
│   └── weather_alert.py      # Generates weather alerts
└── START_HERE.md             # This file!
```

#### 2. AI Agent (`my-awesome-agent/`)
```
my-awesome-agent/
├── app/
│   ├── agent.py              # Main entry point
│   ├── agents/
│   │   └── flood_orchestrator.py   # 🤖 Your AI agent
│   └── tools/
│       └── flood_monitoring_tools.py  # Agent's tools
```

---

## 🔄 The Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. You Click "Scenario 1" in Streamlit                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Frontend generates weather alert JSON                   │
│     - Severity: 3/5                                          │
│     - Precipitation: 95mm                                    │
│     - Probability: 75%                                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  3. POST to Backend: /api/alerts/weather                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Backend invokes AI Agent (flood_orchestrator_agent)     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  5. AI Agent uses tools:                                     │
│     - process_weather_alert() → Severity assessment         │
│     - analyze_flood_risk() → Risk scoring & recommendations │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  6. Agent responds with analysis (using Gemini 2.0 Flash)   │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  7. Backend returns to Frontend                              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  8. Streamlit displays BOTH:                                 │
│     - Original weather alert                                 │
│     - AI Agent's analysis                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 For Your Hackathon

### Testing Iterations:

**Method 1: Test in Playground (Fast)**
```bash
cd my-awesome-agent
make playground
```
- Paste weather JSON
- See agent response immediately
- Edit agent files, test again
- No need to restart!

**Method 2: Test in Streamlit (Full Integration)**
- Click Scenario 1
- See full flow
- Takes a bit longer

### Making Changes:

**To change AI behavior:**
1. Edit `my-awesome-agent/app/agents/flood_orchestrator.py`
2. Change the `instruction` or add tools
3. Test in playground

**To change decision logic:**
1. Edit `my-awesome-agent/app/tools/flood_monitoring_tools.py`
2. Update thresholds, scoring, recommendations
3. Test in playground

**To change UI:**
1. Edit `flood-monitoring-demo/app/frontend.py`
2. Save (auto-reloads)
3. See changes immediately

---

## 🐛 Troubleshooting

### "Backend Offline" in UI
```bash
# Check if backend is running
curl http://localhost:8000/

# If not, start it:
cd flood-monitoring-demo
python app/backend.py
```

### "Agent not available"
```bash
# Check if agent files exist
ls /Users/parichaypothepalli/Downloads/agent-starter-pack/my-awesome-agent/app/agents/flood_orchestrator.py

# Install dependencies
cd my-awesome-agent
make install
```

### AI Agent takes too long
Edit `flood-monitoring-demo/app/frontend.py`, line 89:
```python
timeout=60  # Increase from 30 seconds
```

### Want to see what's happening
**Watch backend terminal** - it shows:
```
📡 Weather Alert Received: WX-FLOOD-...
🤖 Invoking AI Orchestrator Agent...
✅ Agent responded successfully
```

---

## 📖 Documentation

- **INTEGRATION_GUIDE.md** - Detailed technical guide
- **HACKATHON_READY.md** - Demo script and talking points
- **README.md** - General overview

---

## ✅ Checklist Before Demo

- [ ] Backend running (`python app/backend.py`)
- [ ] Frontend running (`streamlit run app/frontend.py`)
- [ ] Tested Scenario 1 (works!)
- [ ] Cleared old events (🗑️ button)
- [ ] Browser at http://localhost:8501
- [ ] Terminal visible (shows logs)
- [ ] Talking points ready

---

## 🎬 2-Minute Demo Script

**[0:00]** "I built an AI-powered flood monitoring system."

**[0:15]** *Click Scenario 1* "When weather data comes in..."

**[0:30]** *Point to weather alert* "System receives the alert: 95mm rain, 75% probability, severity 3/5"

**[0:45]** *Point to AI response* "Our AI agent, powered by Gemini 2.0, analyzes it instantly..."

**[1:00]** *Click View Details* "It assesses risk, determines next steps..."

**[1:30]** "This would take a human 15-30 minutes. Our AI does it in seconds."

**[1:45]** "Built on production-ready Google Cloud infrastructure, ready to deploy."

**[2:00]** "Questions?"

---

## 🏆 Key Selling Points

1. **Real AI** - Not just displaying data, AI makes decisions
2. **Instant** - 15-30 min analysis done in <10 seconds  
3. **Production-Ready** - Built on Vertex AI, scalable
4. **Modular** - Easy to add more monitoring phases
5. **Tested** - Dev playground for iteration

---

## 🚀 You're Ready!

Everything is set up and working. Just:

1. **Start backend** → `python app/backend.py`
2. **Start frontend** → `streamlit run app/frontend.py`
3. **Click Scenario 1** → See the magic!

**Good luck! 🎉**

---

## 📞 Quick Commands

```bash
# Start everything
cd /Users/parichaypothepalli/Downloads/agent-starter-pack/flood-monitoring-demo
python app/backend.py &
streamlit run app/frontend.py

# Test agent separately
cd /Users/parichaypothepalli/Downloads/agent-starter-pack/my-awesome-agent
make playground

# Kill everything
pkill -f "python app/backend.py"
pkill -f "streamlit run"
```

**Now go win that hackathon!** 🏆

