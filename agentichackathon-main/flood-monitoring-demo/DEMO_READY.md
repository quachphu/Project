# 🌊 Flood Monitoring System - READY FOR DEMO

## ✅ System Status: LIVE

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:8501
- **Status**: Both services running

---

## 🎯 What You Have Now

### **Clean Logging UI**
- Dark terminal-style interface
- Compact scenario buttons at top
- Real-time confidence score sidebar (X/100)
- Large logging area showing all monitoring phases

### **3 Scenarios**
1. **Scenario 1**: High Risk (4/5 severity, 120mm) → **Triggers Phase 2**
2. **Scenario 2**: Extreme (5/5, 150mm) → **Triggers Phase 2**
3. **Scenario 3**: Low Risk (1/5, 25mm) → **No escalation**

### **Progressive Monitoring System**

#### **Phase 1: Weather Alert (0-25 points)**
- AI analyzes severity, precipitation, probability
- **Aggressive scoring**: 4/5 severity = 20+ points
- Score ≥20 → **Automatically escalates to Phase 2**
- Expected score for Scenario 1: **22-24/25**

#### **Phase 2: River Gauge Sensors (0-20 points)**
- Searches rivers near ZIP code
- Deploys 6 sensors across 2 rivers
- Shows real-time sensor data:
  - 1 CRITICAL sensor (rising)
  - 4 WARNING sensors (rising)
  - 1 NORMAL sensor
- AI scores based on status + trend
- Expected score for Scenario 1: **18-20/20**

#### **Total Confidence Score**
- Phase 1 + Phase 2 = **~40-44/100**
- Displayed prominently in sidebar
- Color-coded status indicator

---

## 🚀 How to Demo

### **Step 1: Open the UI**
```
Open browser: http://localhost:8501
```

### **Step 2: Clear Events (if needed)**
Click the "Clear" button to start fresh

### **Step 3: Run Scenario 1**
1. Click **"Scenario 1"** button
2. Wait 15-20 seconds for AI processing
3. Watch the logging area populate in real-time

### **Step 4: What You'll See**

**Timeline Log:**
```
[10:30:45] PHASE 1: WEATHER ALERT
  └─ Alert ID: WX-FLOOD-20251003103045
  └─ Severity: 4/5 | Precipitation: 120mm
  └─ Location: Northern Valley (ZIP: 11375)

[10:30:47] 🤖 AI ANALYSIS - WEATHER SCORING
  └─ Weather Score: 22/25
  └─ ⚠️ ESCALATION RECOMMENDED

[10:30:48] PHASE 2: RIVER GAUGE DEPLOYMENT
  └─ Searching rivers near ZIP 11375...
  └─ Found 2 rivers
  
  └─ 📍 Flushing Creek (3 sensors)
  └─ [Sensor Table showing status, trends, levels]
  
  └─ 📍 Alley Creek (3 sensors)
  └─ [Sensor Table showing status, trends, levels]

[10:31:05] 🤖 AI ANALYSIS - RIVER GAUGE SCORING
  └─ River Score: 19/20
  └─ Cumulative: 41/100
  └─ ⚠️ ESCALATION TO PHASE 3 RECOMMENDED
```

**Sidebar Score:**
```
📊 Confidence Score
    41/100
  TOTAL CONFIDENCE

Phase Breakdown:
- Phase 1 (Weather): 22/25
- Phase 2 (Rivers): 19/20
- Phase 3 (Satellite): 0/15
- Phase 4 (Ground): 0/25
- Phase 5 (Prediction): 0/15

🔴 Status: CRITICAL
```

---

## 🎨 Key Features

### **1. Aggressive AI Scoring**
- Weather alerts with 4/5 severity **always** score ≥20/25
- Critical + rising sensors **always** score high
- Consistent escalation behavior for demo

### **2. Real-time AI Analysis**
- Every phase shows actual AI agent responses
- Scores calculated by LLM using Google ADK
- Natural language explanations from AI

### **3. Clean Logging UI**
- Terminal-style dark interface
- Color-coded status (green/yellow/red)
- Timestamp for each event
- Expandable sensor data tables

### **4. Multi-phase Progression**
- Phase 1 → triggers → Phase 2
- Phase 2 → recommends → Phase 3 (future)
- Cumulative confidence score

---

## 🛠️ Technical Details

### **Architecture**
```
Frontend (Streamlit) → Backend (FastAPI) → AI Agent (Google ADK)
                     ↓
              Mock Data Generators
```

### **AI Agent Tools**
1. `score_weather_alert()` - Analyzes weather data (0-25 pts)
2. `score_river_gauges()` - Analyzes 6 sensors (0-20 pts)

### **Scoring Logic**
```python
# Phase 1: Weather (AGGRESSIVE)
severity_score = severity * 5  # 4/5 = 20 pts
precip_score = (precip / 100) * 3  # 120mm = 3.6 pts
prob_score = probability / 50  # 85% = 1.7 pts
# If severe: guarantee ≥22 points

# Phase 2: Rivers (AGGRESSIVE)
critical = 6 pts each
warning = 4 pts each
rising = 2 pts each
# 1 critical + 4 warning + 5 rising = ~20 pts
```

---

## 📊 Expected Demo Results

### **Scenario 1 (High Risk)**
- ✅ Phase 1: 22-24/25
- ✅ Phase 2: 18-20/20
- ✅ Total: 40-44/100
- ✅ Status: CRITICAL
- ✅ Escalates to Phase 2

### **Scenario 2 (Extreme)**
- ✅ Phase 1: 24-25/25
- ✅ Phase 2: 19-20/20
- ✅ Total: 43-45/100
- ✅ Status: CRITICAL

### **Scenario 3 (Low Risk)**
- ✅ Phase 1: 5-10/25
- ❌ No escalation
- ✅ Total: 5-10/100
- ✅ Status: MONITORING

---

## 🐛 Troubleshooting

### **If Frontend Shows Error**
```bash
cd flood-monitoring-demo
lsof -ti:8501 | xargs kill -9
streamlit run app/frontend.py --server.headless=true &
```

### **If Backend Not Responding**
```bash
cd flood-monitoring-demo
lsof -ti:8000 | xargs kill -9
python app/backend.py &
```

### **If No Events Appear**
1. Click "Clear" button
2. Wait 3 seconds
3. Click "Scenario 1" again
4. Wait 20 seconds

### **Manual Restart**
```bash
# Kill everything
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Start backend
cd flood-monitoring-demo
python app/backend.py &

# Start frontend
streamlit run app/frontend.py &
```

---

## 🎉 You're Ready!

**Open**: http://localhost:8501

**Click**: Scenario 1

**Watch**: AI-powered progressive flood monitoring in action!

---

## 📝 Notes for Hackathon Judges

- **Real AI Integration**: Using Google ADK with Gemini
- **Progressive Escalation**: Automatic threshold-based phase triggers
- **Confidence Scoring**: 100-point cumulative system
- **Mock Data**: Simulated weather + river sensors
- **Clean UI**: Professional logging interface
- **Extensible**: Ready for Phases 3-5 (satellite, ground, prediction)

**This is Phase 1 + Phase 2 of a 5-phase system.**

