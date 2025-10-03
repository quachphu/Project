# 🌊 Progressive Flood Monitoring System with Confidence Scoring

## 🎯 System Overview

A **100-point confidence scoring system** where each monitoring phase contributes points until we reach high confidence in flood risk assessment.

---

## 📊 Confidence Scoring Breakdown (0-100 Points)

| Phase | Points | Trigger Condition | Timeline |
|-------|--------|-------------------|----------|
| **Weather Alert** | 0-25 | Always first | T-2:00:00 |
| **River Gauges** | 0-20 | Weather ≥20/25 | T-1:00:00 |
| **Satellite Imagery** | 0-10 | River ≥15/20 | T-0:50:00 |
| **Drone LiDAR** | 0-10 | Satellite ≥7/10 | T-0:30:00 |
| **Social Media** | 0-10 | Any critical status | T-0:10:00 |

**Total**: 100 points = 100% confidence

---

## 🚀 How It Works

### **Phase 1: Weather Alert (25 Points)**

**Input:**
- Alert ID
- Severity level (1-5)
- Precipitation (mm)
- Probability (%)
- Location + ZIP code

**Scoring Logic:**
```
Severity component: severity_level × 3 (max 15 points)
Precipitation component: precipitation_mm / 20 (max 5 points)
Probability component: probability_percent / 20 (max 5 points)

Total: Up to 25 points
```

**Decision:**
- If score **≥ 20/25**: Escalate to Phase 2 (River Gauges)
- If score < 20/25: Monitor only, no escalation

**AI Agent Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌧️ WEATHER ALERT ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Severity Component: 9/15 points
Precipitation Component: 4.8/5 points
Probability Component: 3.8/5 points

**WEATHER ALERT SCORE: 22/25 points**

📈 CUMULATIVE CONFIDENCE SCORE: 22/100

🚨 ESCALATION DECISION:
✅ Score ≥ 20/25 - ESCALATING TO RIVER GAUGE MONITORING
⚠️ Deploying river gauge sensors near ZIP code 11375
```

---

### **Phase 2: River Gauges (20 Points)**

**Triggered by:** Weather score ≥ 20/25

**Process:**
1. **Search rivers** near ZIP code
2. **Retrieve data** from 2 rivers × 3 sensors each = 6 total sensors
3. **Send to AI** for analysis

**River Data Structure:**
```
River 1: Flushing Creek (1.2 miles away)
  ├─ Sensor 1 (Upper): 3.8m, rising, normal
  ├─ Sensor 2 (Middle): 4.2m, rising, warning
  └─ Sensor 3 (Lower): 3.5m, steady, normal

River 2: Alley Creek (2.5 miles away)
  ├─ Sensor 4 (Upper): 5.1m, rising, warning
  ├─ Sensor 5 (Middle): 5.8m, rising, critical
  └─ Sensor 6 (Lower): 4.9m, rising, warning
```

**Scoring Logic:**
```
For each sensor:
- Critical status: +5 points
- Warning status: +3 points
- Normal status: +0 points
- Rising trend: +1 additional point

Max 20 points (capped)
```

**Example Calculation:**
```
Sensor 1: Normal (0) + Rising (+1) = 1 point
Sensor 2: Warning (+3) + Rising (+1) = 4 points
Sensor 3: Normal (0) + Steady (0) = 0 points
Sensor 4: Warning (+3) + Rising (+1) = 4 points
Sensor 5: Critical (+5) + Rising (+1) = 6 points
Sensor 6: Warning (+3) + Rising (+1) = 4 points

Total: 19/20 points (capped at 20)
```

**AI Agent Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌊 RIVER GAUGE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sensor Status Summary:
- 🔴 Critical: 1 sensors
- 🟡 Warning: 4 sensors
- 🟢 Normal: 1 sensors
- ↗️ Rising Trend: 5 sensors

**RIVER GAUGE SCORE: 19/20 points**

📈 CUMULATIVE CONFIDENCE SCORE: 41/100

Breakdown:
- Weather Alert: 22/25
- River Gauges: 19/20
- Satellite: 0/10 (pending)
- Drone: 0/10 (pending)
- Social Media: 0/10 (pending)

🚨 **HIGH RISK DETECTED**
```

---

## 🖥️ Streamlit UI Display

### **Timeline View:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Monitoring Timeline

┌─────────────────────────────────────────────┐
│ 🕐 T-2:00:00 - 🌧️ Weather Alert Received  │
│ Status: ✅ received                          │
│ [📋 View Alert Details]                     │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 🕐 T-2:00:00 - 🤖 AI Analysis - Phase 1    │
│ Status: ✅ completed                         │
│ [📋 View AI Response] ← Shows 22/25 points │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 🕐 T-1:00:00 - 🔍 Searching Rivers         │
│ Status: in_progress                          │
│ Message: "Searching rivers near ZIP 11375" │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 🕐 T-1:00:00 - 🌊 River Gauge Data         │
│ Status: ✅ completed                         │
│ Rivers: 2 | Sensors: 6 | Critical: 1       │
│ [📋 View Sensor Data] ← Shows 6 sensors    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ 🕐 T-1:00:00 - 🤖 AI Analysis - Phase 2    │
│ Status: ✅ completed                         │
│ [📋 View AI Response] ← Shows 19/20 points │
│                      Total: 41/100          │
└─────────────────────────────────────────────┘
```

---

## 🎮 How to Use

### **1. Start Backend:**
```bash
cd flood-monitoring-demo
python app/backend.py
```

### **2. Start Frontend:**
```bash
streamlit run app/frontend.py
```

### **3. Trigger Scenario:**
1. Open http://localhost:8501
2. Click **"🌧️ Scenario 1: Moderate Flood"**
3. Wait ~10-20 seconds (AI processing)
4. See **multiple events** appear in timeline
5. Expand each to see details

---

## 🔍 What You'll See

### **Event 1: Weather Alert**
- Raw weather data
- Severity: 3/5
- Precipitation: 95mm
- ZIP: 11375

### **Event 2: AI Phase 1 Analysis**
- Weather scoring breakdown
- Confidence score: **22/25**
- Decision: ✅ Escalate to river gauges

### **Event 3: Searching Rivers**
- "Searching for rivers near ZIP 11375..."

### **Event 4: River Gauge Data**
- **2 Rivers** found
- **6 Sensors** total
- Visual display of each sensor:
  - 🟢 Sensor 1: 3.8m, ↗️ rising
  - 🟡 Sensor 2: 4.2m, ↗️ rising (warning)
  - 🟡 Sensor 4: 5.1m, ↗️ rising (warning)
  - 🔴 Sensor 5: 5.8m, ↗️ rising (CRITICAL)

### **Event 5: AI Phase 2 Analysis**
- River gauge scoring breakdown
- Confidence score: **19/20**
- **Cumulative**: **41/100**
- Risk level: **HIGH RISK DETECTED**

---

## 📁 File Structure

```
flood-monitoring-demo/
├── app/
│   ├── backend.py              # Progressive workflow coordinator
│   ├── flood_coordinator.py    # Phase 1 & 2 logic
│   ├── agent_client.py         # AI agent invocation
│   └── frontend.py             # Streamlit UI
├── mock_data/
│   ├── weather_alert.py        # Weather data with ZIP
│   └── river_gauge_data.py     # 2 rivers × 3 sensors

my-awesome-agent/
└── app/
    ├── agents/
    │   └── flood_orchestrator.py  # AI agent with scoring
    └── tools/
        └── flood_scoring_tools.py  # score_weather_alert()
                                     # score_river_gauges()
```

---

## 🤖 AI Agent Tools

### **Tool 1: `score_weather_alert`**
```python
def score_weather_alert(
    alert_id: str,
    severity_level: int,
    precipitation_mm: float,
    probability_percent: int,
    location_region: str,
    zipcode: str
) -> str:
    # Returns formatted analysis with 0-25 point score
```

### **Tool 2: `score_river_gauges`**
```python
def score_river_gauges(
    sensor_1_status: str,  # normal/warning/critical
    sensor_1_trend: str,   # steady/rising/falling
    sensor_2_status: str,
    sensor_2_trend: str,
    # ... repeat for sensors 3-6
) -> str:
    # Returns formatted analysis with 0-20 point score
```

---

## 🎯 Decision Logic

```
IF weather_score ≥ 20/25:
    ✅ Escalate to Phase 2 (River Gauges)
    
    IF river_score ≥ 15/20:
        🚨 HIGH RISK - Prepare evacuation
        
        IF total_score ≥ 60/100:
            🔴 CRITICAL - Activate all emergency protocols
```

---

## ✅ Current Status

- [x] Weather alert with ZIP code
- [x] AI scoring (0-25 points)
- [x] Escalation decision
- [x] River search by ZIP
- [x] 2 rivers × 3 sensors = 6 total
- [x] AI river gauge scoring (0-20 points)
- [x] Progressive UI display
- [x] Cumulative confidence tracking

---

## 🔜 Coming Next (Phases 3-5)

- **Phase 3**: Satellite imagery (0-10 points)
- **Phase 4**: Drone LiDAR (0-10 points)
- **Phase 5**: Social media (0-10 points)

Same pattern: 
1. AI scores previous phase
2. If threshold met, trigger next phase
3. Collect data
4. Send to AI
5. Add points to cumulative score

---

## 🏆 Demo Script

**"Watch this 2-phase progressive monitoring system:"**

1. *Click Scenario 1*
2. "Weather alert comes in - AI scores it 22 out of 25 points"
3. "System decides: score is high enough, escalate to river monitoring"
4. "Searches for rivers near the ZIP code - finds 2 rivers, 6 sensors"
5. "AI analyzes all 6 sensors - 1 critical, 4 warning, 1 normal"
6. "Scores 19 out of 20 points for river gauges"
7. **"Total confidence: 41 out of 100 points - HIGH RISK DETECTED"**

---

**🎉 Your progressive monitoring system is ready to demo!**

