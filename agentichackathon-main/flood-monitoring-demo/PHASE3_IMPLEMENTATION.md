# Phase 3: ML Similarity Analysis - Implementation Guide

## ✅ What's Been Implemented

### 1. **ML Similarity Analysis Module**
- **File**: `mock_data/ml_similarity.py`
- **Features**:
  - Compares current conditions with 7 historical flood events
  - Calculates similarity using weighted features
  - Returns best match with similarity percentage
  - Generates confidence score (0-10 points)

### 2. **Historical Data**
- **File**: `mock_data/historical_events.csv`
- Contains past flood events with outcomes and damage levels

### 3. **AI Agent Tool**
- **File**: `my-awesome-agent/app/tools/ml_scoring_tool.py`
- New tool: `score_ml_similarity()`
- Scores 0-10 points based on ML analysis

### 4. **Updated Orchestrator**
- **File**: `my-awesome-agent/app/agents/flood_orchestrator.py`
- Added ML similarity tool
- Updated instructions with Phase 3 workflow
- Timeline context: T±30 mins

### 5. **Phase 3 Coordinator**
- **File**: `flood-monitoring-demo/app/flood_coordinator.py`
- New function: `process_ml_similarity_phase()`
- Runs ML analysis and invokes AI agent

## 🚧 What Needs to be Done

### Step 1: Update Backend to Trigger Phase 3
Edit `flood-monitoring-demo/app/backend.py`:

```python
# After Phase 2 completes (around line 180), add:

# Phase 3: ML Similarity Analysis (if cumulative score >= 40)
if orchestrator_status == "phase2_completed":
    # Check cumulative score from Phase 2 response
    import re
    cumulative_match = re.search(r'(\d+)/100', phase2_result.get("agent_response", ""))
    if cumulative_match:
        cumulative_score = int(cumulative_match.group(1))
        
        if cumulative_score >= 40:
            print(f"🔬 Phase 3: Running ML Similarity Analysis...")
            
            # Add progress event
            ml_progress_event = {
                "event_type": "ml_analysis_progress",
                "phase": "T-0:30:00",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "message": "Running ML pattern matching against historical flood events...",
                    "status": "analyzing"
                },
                "status": "in_progress"
            }
            monitoring_events.append(ml_progress_event)
            
            from flood_coordinator import process_ml_similarity_phase
            phase3_result = process_ml_similarity_phase(alert_dict, phase2_result["river_data"])
            
            if phase3_result["status"] == "completed":
                print(f"✅ Phase 3 completed - ML analysis finished")
                
                # Store ML analysis event
                ml_event = {
                    "event_type": "ml_similarity_result",
                    "phase": "T-0:30:00",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "ml_analysis": phase3_result["ml_analysis"],
                        "best_match": phase3_result["ml_analysis"]["best_match"],
                        "similarity_percent": phase3_result["ml_analysis"]["similarity_percent"]
                    },
                    "status": "completed"
                }
                monitoring_events.append(ml_event)
                
                # Store Phase 3 AI response
                phase3_ai_event = {
                    "event_type": "ai_phase3_ml",
                    "phase": "T-0:30:00",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "agent_response": phase3_result["agent_response"],
                        "alert_id": alert.alert_id
                    },
                    "status": "completed"
                }
                monitoring_events.append(phase3_ai_event)
                orchestrator_status = "phase3_completed"
```

### Step 2: Update Frontend with Streaming & Toggles
Edit `flood-monitoring-demo/app/frontend.py`:

**Add these new event handlers in the log rendering section:**

```python
# ML Analysis Progress
elif event_type == 'ml_analysis_progress':
    message = event_data.get('message', '')
    log_html += f'<span class="log-phase">PHASE 3: ML ANALYSIS</span><br>'
    log_html += f'  └─ <span class="log-info">{message}</span><br>'
    log_html += f'  └─ ⏳ Analyzing historical patterns...<br>'

# ML Similarity Result
elif event_type == 'ml_similarity_result':
    ml_data = event_data.get('ml_analysis', {})
    best_match = event_data.get('best_match', {})
    similarity = event_data.get('similarity_percent', 0)
    
    log_html += f'  └─ <span class="log-success">✓ Analysis Complete</span><br>'
    log_html += f'  └─ Best Match: {best_match.get("event_id", "N/A")}<br>'
    log_html += f'  └─ Similarity: <span class="log-warning">{similarity:.1f}%</span><br>'
    log_html += f'  └─ Historical Outcome: {best_match.get("outcome", "N/A").replace("_", " ").title()}<br>'

# AI Phase 3
elif event_type == 'ai_phase3_ml':
    response = event_data.get('agent_response', '')
    log_html += f'<span class="log-phase">🤖 AI ANALYSIS - ML SCORING</span><br>'
    
    # Extract score
    import re
    match = re.search(r'(\d+)/10', response)
    if match:
        score = int(match.group(1))
        score_class = 'log-critical' if score >= 8 else 'log-warning'
        log_html += f'  └─ ML Score: <span class="{score_class}">{score}/10</span><br>'
    
    # Extract cumulative
    match_cumulative = re.search(r'(\d+)/100', response)
    if match_cumulative:
        cumulative = int(match_cumulative.group(1))
        log_html += f'  └─ Cumulative: <span class="log-warning">{cumulative}/100</span><br>'
```

**Update score sidebar to include ML:**

```python
elif event_type == 'ai_phase3_ml':
    data = event.get('data', {})
    if isinstance(data, dict):
        response = data.get('agent_response', '')
        match = re.search(r'(\d+)/10', response)
        if match:
            phase3_score = int(match.group(1))
```

**Add Phase 3 to score breakdown:**

```python
st.markdown(f"""
**Phase Breakdown:**
- Phase 1 (Weather): **{phase1_score}/25**
- Phase 2 (Rivers): **{phase2_score}/20**
- Phase 3 (ML Analysis): **{phase3_score}/10**
- Phase 4 (Satellite): **0/15**
- Phase 5 (Ground): **0/20**
""")
```

### Step 3: Add pandas dependency
```bash
cd flood-monitoring-demo
echo "pandas>=2.0.0" >> requirements.txt
echo "numpy>=1.24.0" >> requirements.txt
pip install pandas numpy
```

### Step 4: Test the System
```bash
# Restart backend
cd flood-monitoring-demo
python app/backend.py

# In another terminal, test
python detailed_test.py
```

## 🎯 Expected Results

After clicking "Scenario 1":

1. **Phase 1**: Weather Alert (24/25)
2. **Phase 2**: River Gauges (20/20)
3. **Phase 3**: ML Analysis
   - Progress message
   - ML finds best match (~87% similarity)
   - AI scores 9-10/10
4. **Total Score**: 53-54/100

## 📊 Scoring Breakdown

- Weather: 24/25
- Rivers: 20/20  
- ML Similarity: 9-10/10
- **Total: 53-54/100** 🟠 ELEVATED RISK

## 🔄 Streaming Effect (Future Enhancement)

To add streaming delays:

```python
# In backend before each phase
import time

# Before Phase 2
time.sleep(2)  # Simulate searching

# Before Phase 3
time.sleep(3)  # Simulate ML processing
```

## ✨ Collapsible Toggles (Future Enhancement)

Use Streamlit expanders:

```python
with st.expander(f"📊 Phase 3: ML Analysis Details"):
    st.json(ml_result)
```

---

**Status**: Ready to implement! Just follow Steps 1-4 above.

