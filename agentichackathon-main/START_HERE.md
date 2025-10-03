# 🚀 START HERE - Quick Guide

Welcome! This is your **one-stop guide** to get the AI Flood Monitoring System running in 5 minutes.

---

## ✅ What You Have

A complete **AI-powered disaster response system** with:
- ✨ **Progressive risk assessment** (5 phases, 0-100 score)
- 🤖 **7 intelligent AI agents** (using Google ADK + Gemini 2.0)
- 👤 **Human-in-the-loop approval** (for medium-risk scenarios)
- 🔗 **Inter-agent communication** (agents coordinate autonomously)
- 🎨 **Beautiful real-time UI** (color-coded monitoring log)

---

## 📚 Documentation Quick Links

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **README.md** | Complete system guide | Read this first |
| **SYSTEM_OVERVIEW.md** | Visual architecture & data flow | Understand how it works |
| **PROJECT_STRUCTURE.md** | File organization & key locations | Find and modify code |
| **QUICK_START.md** | 5-minute quickstart | Get running fast |

---

## 🎯 5-Minute Quickstart

### **Step 1: Set up Google Cloud credentials** (30 seconds)

```bash
export GOOGLE_API_KEY="your-api-key-here"
# OR
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

**Don't have credentials?** Follow [this guide](https://cloud.google.com/docs/authentication/getting-started)

---

### **Step 2: Start the system** (1 command!)

The startup script automatically handles venv, dependencies, and services!

```bash
cd /Users/parichaypothepalli/Downloads/agent-starter-pack
./start_demo.sh
```

**What the script does automatically:**
- ✅ Creates virtual environment (if doesn't exist)
- ✅ Installs all dependencies from requirements.txt
- ✅ Installs Google ADK packages
- ✅ Clears Python cache
- ✅ Starts backend on http://localhost:8000
- ✅ Starts frontend on http://localhost:8501

---

### **Step 3: Open the UI** (10 seconds)

Go to: **http://localhost:8501**

**💡 IMPORTANT TIP:** Streamlit caches aggressively. At each step, **press Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows/Linux)** to hard refresh your browser and see the latest updates!

---

### **Step 4: Run a simulation** (2 minutes)

1. **Click "Scenario 1"** at the top
2. **Watch the magic:**
   - ✅ Phase 1: Weather analysis
   - ✅ Phase 2: River gauge data
   - ✅ Phase 3: ML similarity
   - ✅ Phase 4: Social media
   - ✅ Phase 5: Drone vision AI
   - 🎯 Score reaches **~93/100**
   - 🚨 System auto-approves (90+)
   - 🎭 Scenario selection appears

3. **Click "🏥 Scenario 1: Hospital Crisis"**
4. **Watch the agents coordinate:**
   - 🏥 Hospital detects low ICU beds
   - 🏥→🚔 Hospital requests police support
   - ✅ Police deploys crowd control units
   - 📊 All 7 agents activate

5. **Scroll through the monitoring log** - see color-coded inter-agent communications!

---

## 🎭 Try Different Flows

### **Flow 1: Auto-Approved (High Risk)**
```
Click "Scenario 1" → Score 93 → Auto-approved → Select scenario → See agents
```

### **Flow 2: Human Approval (Medium Risk)**
```
Click "Scenario 2" → Score 80 → Click "✅ APPROVE" → Select scenario → See agents
```

### **Flow 3: No Orchestration (Low Risk)**
```
Click "Scenario 3" → Score 25 → System stops (below threshold)
```

---

## 🎨 What to Look For

### **In the Sidebar:**
- 📊 **Real-time score** accumulating
- ✅ **Phase checkmarks** as they complete
- ⚠️ **Approval buttons** (for Scenario 2)
- 🚨 **Scenario selection** (after approval)

### **In the Monitoring Log:**
- 🔴 **Red text**: CRITICAL/URGENT messages
- 🟢 **Green text**: SUCCESS messages
- 🟡 **Yellow text**: WARNINGS/coordination
- 🔵 **Blue text**: INFO/progress

### **Inter-Agent Communications:**
- 🔗 **"Sending 'hospital_crowd_control' to PoliceAgent"**
- 🔗 **"✅ Received from PoliceAgent: {status: deployed}"**
- 🔗 **"Requesting route clearance for Main St & 5th"**

---

## 🐛 Troubleshooting

### **"Connection refused" error:**
```bash
# Check if backend is running
curl http://localhost:8000/

# If not, start it:
cd flood-monitoring-demo
source venv/bin/activate
python app/backend.py
```

### **"API rate limit" error:**
```
Wait 1 minute between tests (Gemini API rate limits)
```

### **Frontend not updating:**
```
Hard refresh your browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

### **Nuclear option (restart everything):**
```bash
pkill -f backend.py
pkill -f streamlit
rm -rf flood-monitoring-demo/app/__pycache__
./start_demo.sh
```

---

## 🎥 Demo Script (for presentations)

**30-second pitch:**
> "This is an AI disaster monitoring system that progressively assesses flood risk through 5 phases, requires human approval for medium-risk scenarios, then orchestrates 7 specialized AI agents that communicate autonomously to coordinate emergency response. Built with Google's Gemini 2.0 Flash via the ADK framework."

**2-minute demo:**
1. Click Scenario 1
2. Point out phases 1-5 executing
3. Show score reaching 93
4. Highlight auto-approval
5. Select Hospital Crisis scenario
6. Point to inter-agent communications in log

**5-minute full demo:**
- Run Scenario 1 (high risk, auto-approved)
- Run Scenario 2 (medium risk, human approval)
- Compare Hospital Crisis vs Rescue Coordination scenarios
- Highlight specific inter-agent message chains

---

## 📖 Next Steps

### **For Developers:**
1. Read `PROJECT_STRUCTURE.md` - understand file organization
2. Read `SYSTEM_OVERVIEW.md` - understand architecture
3. Modify score thresholds in `backend.py`
4. Add custom scenarios in `mock_data/weather_alert.py`
5. Create new agents in `my-awesome-agent/app/agents/agents_adk.py`

### **For Presenters:**
1. Read `DEMO_READY.md` - presentation guide
2. Practice the 3 flows (auto/approval/no-trigger)
3. Prepare to explain inter-agent communication
4. Highlight the human-in-the-loop approval

### **For Judges:**
1. Read `HACKATHON_READY.md` - judging criteria
2. Test all 3 scenarios
3. Observe inter-agent communications
4. Evaluate real-world applicability

---

## 🏗️ Project Structure at a Glance

```
agent-starter-pack/
├── README.md                    ← Complete guide
├── SYSTEM_OVERVIEW.md           ← Architecture & flow
├── PROJECT_STRUCTURE.md         ← File organization
├── START_HERE.md                ← This file
├── start_demo.sh                ← One-click startup
│
├── flood-monitoring-demo/       ← Main application
│   ├── app/
│   │   ├── backend.py           ← FastAPI server
│   │   ├── frontend.py          ← Streamlit UI
│   │   └── flood_coordinator.py ← Phase logic
│   ├── mock_data/               ← Simulated data
│   └── requirements.txt
│
└── my-awesome-agent/            ← AI agents
    └── app/agents/
        ├── decision_maker_adk.py  ← Orchestrator
        └── agents_adk.py          ← 7 specialists
```

---

## 🎯 Key Features to Highlight

✅ **Progressive Risk Assessment** - 5 phases with escalating data sources  
✅ **Human-in-the-Loop** - Approval required for 60-89 scores  
✅ **Multi-Agent Orchestration** - 7 specialized AI agents  
✅ **Inter-Agent Communication** - Autonomous cross-agent coordination  
✅ **Real-time Monitoring** - Live event log with color coding  
✅ **Dynamic Scenarios** - Different workflows based on context  
✅ **Google ADK Integration** - Gemini 2.0 Flash powered  
✅ **Multi-modal AI** - Text + image analysis (drone vision)  
✅ **Production Ready** - Clean architecture, error handling, logging  

---

## 📊 System Stats

| Metric | Value |
|--------|-------|
| Total Lines of Code | ~3,500 |
| Number of Agents | 7 + 1 orchestrator |
| Assessment Phases | 5 |
| Mock Data Sources | 4 |
| Orchestration Scenarios | 2 |
| Inter-Agent Messages | 1-6 per scenario |
| Response Time | ~15s (phases) + ~20s (agents) |
| Max Score | 100 points |

---

## 🚀 You're Ready!

Everything is consolidated, documented, and ready to run.

**Your next command:**

```bash
./start_demo.sh
```

Then open **http://localhost:8501** and click **"Scenario 1"**.

Enjoy! 🌊✨

---

**Questions?** Check the logs:
- `tail -f flood-monitoring-demo/backend.log`
- `tail -f flood-monitoring-demo/frontend.log`

**Last Updated:** October 3, 2025

