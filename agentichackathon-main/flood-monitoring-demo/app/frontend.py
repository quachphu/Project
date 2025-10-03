"""Streamlit frontend - Clean logging UI for flood monitoring."""

import streamlit as st
import requests
import json
from datetime import datetime
import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mock_data.weather_alert import generate_weather_alert

BACKEND_URL = "http://localhost:8000"

# Page config
st.set_page_config(
    page_title="Flood Monitoring System",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean logging UI
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Dark terminal-like styling */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Compact header */
    h1 {
        font-size: 1.5rem !important;
        margin-bottom: 0.5rem !important;
        color: #58a6ff !important;
    }
    
    /* Small scenario buttons */
    .scenario-btn {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        background: #238636;
        color: white;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
    }
    
    /* Log container */
    .log-container {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 1rem;
        font-family: 'Monaco', 'Menlo', monospace;
        font-size: 0.9rem;
        max-height: 75vh;
        overflow-y: auto;
        margin-top: 1rem;
    }
    
    /* Log entries */
    .log-entry {
        padding: 0.5rem 0;
        border-bottom: 1px solid #21262d;
        color: #c9d1d9;
    }
    
    .log-timestamp {
        color: #8b949e;
        font-size: 0.85rem;
    }
    
    .log-phase {
        color: #58a6ff;
        font-weight: bold;
    }
    
    .log-success {
        color: #3fb950;
    }
    
    .log-warning {
        color: #d29922;
    }
    
    .log-critical {
        color: #f85149;
    }
    
    .log-info {
        color: #79c0ff;
    }
    
    /* Score box */
    .score-box {
        background: #21262d;
        border: 2px solid #58a6ff;
        border-radius: 6px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .score-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #58a6ff;
    }
    
    .score-label {
        color: #8b949e;
        font-size: 0.85rem;
    }
    
    /* Sensor table */
    .sensor-table {
        width: 100%;
        border-collapse: collapse;
        margin: 0.5rem 0;
        font-size: 0.85rem;
    }
    
    .sensor-table th {
        background: #21262d;
        color: #58a6ff;
        padding: 0.5rem;
        text-align: left;
    }
    
    .sensor-table td {
        padding: 0.5rem;
        border-bottom: 1px solid #21262d;
        color: #c9d1d9;
    }
    
    .status-normal { color: #3fb950; }
    .status-warning { color: #d29922; }
    .status-critical { color: #f85149; }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌊 Flood Monitoring System")

# Scenario buttons - small and compact at top
col1, col2, col3, col4, col5 = st.columns([1.2, 1.2, 1.2, 1, 5])

with col1:
    if st.button("Scenario 1", use_container_width=True):
        st.session_state['trigger_scenario'] = 1
        st.rerun()

with col2:
    if st.button("Scenario 2", use_container_width=True):
        st.session_state['trigger_scenario'] = 2
        st.rerun()

with col3:
    if st.button("Scenario 3", use_container_width=True):
        st.session_state['trigger_scenario'] = 3
        st.rerun()

with col4:
    if st.button("Clear", type="secondary"):
        try:
            requests.delete(f"{BACKEND_URL}/api/events")
            st.session_state['events'] = []
            st.rerun()
        except:
            pass

# Show scenario details
st.caption("**Scenario 1:** High Risk (4/5 severity, 120mm → ~93 score) | **Scenario 2:** Medium Risk (3/5, 95mm → ~80 score) | **Scenario 3:** Low Risk (1/5, 25mm)")

st.markdown("---")

# Main layout: Score sidebar + Log output
col_score, col_logs = st.columns([1, 4])

def get_events():
    """Fetch events from backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/api/events", timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Ensure it's a list
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'events' in data:
                return data['events']
            else:
                return []
        return []
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []

def display_single_event_realtime(event, event_num):
    """Display a single event in real-time as it arrives."""
    if not isinstance(event, dict):
        return
    
    event_type = event.get('event_type', '')
    event_data = event.get('data', {})
    timestamp = event.get('timestamp', '')
    
    # Weather Alert
    if event_type == 'weather_alert':
        alert = event_data
        severity = alert.get('severity', {}).get('level', 'N/A')
        precip = alert.get('precipitation', {}).get('expected_amount_mm', 'N/A')
        location = alert.get('location', {}).get('region', 'N/A')
        zipcode = alert.get('location', {}).get('zipcode', 'N/A')
        
        st.markdown(f"#### 🌧️ Weather Alert Received")
        st.write(f"**Severity:** {severity}/5 | **Precipitation:** {precip}mm")
        st.write(f"**Location:** {location} (ZIP: {zipcode})")
        st.caption(f"⏰ {timestamp}")
    
    # AI Phase 1
    elif event_type == 'ai_phase1_weather':
        st.markdown(f"#### 🤖 AI Orchestrator: Analyzing Weather Alert...")
        
        response = event_data.get('agent_response', '')
        
        # Extract score
        import re
        match = re.search(r'(\d+)/25', response)
        if match:
            score = int(match.group(1))
            st.metric("Weather Alert Score", f"{score}/25", 
                     delta="ESCALATION REQUIRED" if score >= 20 else "Monitoring")
        
        # Show AI output in expander
        with st.expander("📄 View AI Analysis", expanded=False):
            st.text(response)
        
        # Show decision
        if 'escalat' in response.lower() or (match and int(match.group(1)) >= 20):
            st.success("✅ **Decision: ESCALATE to Phase 2 - River Gauge Monitoring**")
        
        st.caption(f"⏰ {timestamp}")
    
    # Searching Rivers
    elif event_type == 'searching_rivers':
        zipcode = event_data.get('zipcode', 'N/A')
        st.markdown(f"#### 🔍 Searching for rivers near ZIP {zipcode}...")
        with st.spinner("Querying geographical database..."):
            time.sleep(0.5)  # Visual effect
        st.caption(f"⏰ {timestamp}")
    
    # River Gauge Data
    elif event_type == 'river_gauge_data':
        rivers = event_data.get('rivers', [])
        st.markdown(f"#### 📊 River Gauge Sensors Deployed")
        st.write(f"**Found {len(rivers)} rivers** with active sensors")
        
        with st.expander(f"🌊 View {len(rivers)} Rivers & Sensors", expanded=False):
            for river in rivers:
                st.write(f"**{river.get('river_name')}** - {river.get('distance_miles')} miles away")
                sensors = river.get('sensors', [])
                for sensor in sensors:
                    status_emoji = "🟢" if sensor.get('status') == 'normal' else "🟡" if sensor.get('status') == 'warning' else "🔴"
                    st.write(f"  {status_emoji} {sensor.get('sensor_name')}: {sensor.get('water_level_m')}m, {sensor.get('flow_rate_cms')} m³/s")
        
        st.caption(f"⏰ {timestamp}")
    
    # AI Phase 2
    elif event_type == 'ai_phase2_rivers':
        st.markdown(f"#### 🤖 AI Orchestrator: Analyzing River Gauges...")
        
        response = event_data.get('agent_response', '')
        
        # Extract score
        import re
        match = re.search(r'(\d+)/20', response)
        if match:
            score = int(match.group(1))
            st.metric("River Gauge Score", f"{score}/20", 
                     delta="HIGH RISK" if score >= 15 else "Moderate Risk")
        
        # Show AI output in expander
        with st.expander("📄 View AI Analysis", expanded=False):
            st.text(response)
        
        # Show decision
        cumulative_match = re.search(r'cumulative.*?(\d+)', response.lower())
        if cumulative_match and int(cumulative_match.group(1)) >= 40:
            st.success("✅ **Decision: ESCALATE to Phase 3 - ML Similarity Analysis**")
        
        st.caption(f"⏰ {timestamp}")
    
    # ML Analysis Progress
    elif event_type == 'ml_analysis_progress':
        st.markdown(f"#### 🧠 Running ML Similarity Analysis...")
        with st.spinner("Comparing with historical flood events..."):
            time.sleep(0.5)
        st.caption(f"⏰ {timestamp}")
    
    # ML Results
    elif event_type == 'ml_similarity_result':
        similarity = event_data.get('similarity_percent', 0)
        best_match = event_data.get('best_match', {})
        
        st.markdown(f"#### 🎯 ML Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Similarity Match", f"{similarity:.1f}%")
        with col2:
            st.metric("Historical Event", best_match.get('event_id', 'N/A'))
        with col3:
            outcome = best_match.get('outcome', 'N/A').replace('_', ' ').title()
            st.metric("Outcome", outcome)
        
        st.write(f"**Damage Level:** {best_match.get('damage_level', 'N/A').upper()}")
        
        st.caption(f"⏰ {timestamp}")
    
    # AI Phase 3
    elif event_type == 'ai_phase3_ml':
        st.markdown(f"#### 🤖 AI Orchestrator: Final Risk Assessment...")
        
        response = event_data.get('agent_response', '')
        
        # Extract score
        import re
        match = re.search(r'(\d+)/10', response)
        if match:
            score = int(match.group(1))
            st.metric("ML Similarity Score", f"{score}/10")
        
        # Extract cumulative score
        cumulative_match = re.search(r'(?:total|cumulative).*?(\d+)', response.lower())
        if cumulative_match:
            total = int(cumulative_match.group(1))
            st.metric("🎯 TOTAL CONFIDENCE SCORE", f"{total}/55", 
                     delta=f"{(total/55)*100:.0f}% confidence")
        
        # Show AI output in expander
        with st.expander("📄 View Final AI Assessment", expanded=False):
            st.text(response)
        
        st.caption(f"⏰ {timestamp}")
    
    st.markdown("---")

def trigger_scenario(scenario_num):
    """Trigger a scenario and poll for real-time updates."""
    # Clear old events
    try:
        requests.delete(f"{BACKEND_URL}/api/events", timeout=5)
        st.session_state['events'] = []
    except:
        pass
    
    # Generate alert
    if scenario_num == 1:
        alert = generate_weather_alert("moderate_flood")  # ~93 score
    elif scenario_num == 2:
        alert = generate_weather_alert("medium_flood")    # ~80 score - triggers approval
    else:
        alert = generate_weather_alert("light_rain")
    
    # Start backend processing in background thread
    import threading
    def process_alert():
        try:
            requests.post(
                f"{BACKEND_URL}/api/alerts/weather",
                json=alert,
                timeout=90
            )
        except Exception as e:
            print(f"Backend error: {e}")
    
    thread = threading.Thread(target=process_alert, daemon=True)
    thread.start()
    
    # Poll for new events and auto-rerun to show them
    last_event_count = 0
    max_polls = 60  # 60 seconds max
    
    for poll_iteration in range(max_polls):
        time.sleep(1)  # Poll every second
        events = get_events()
        
        if len(events) > last_event_count:
            # New events! Update session and rerun
            st.session_state['events'] = events
            last_event_count = len(events)
            st.rerun()
        
        # Check if done (10 events = all 3 phases complete with new progress messages)
        if len(events) >= 10 or (not thread.is_alive() and len(events) > 0 and poll_iteration > 10):
            st.session_state['events'] = events
            break
    
    # Final update
    st.session_state['events'] = get_events()

# Check if scenario triggered
if 'trigger_scenario' in st.session_state:
    scenario = st.session_state.pop('trigger_scenario')
    with st.spinner(f'Running Scenario {scenario}...'):
        trigger_scenario(scenario)

# Initialize events
if 'events' not in st.session_state:
    st.session_state['events'] = get_events()

events = st.session_state['events']

# Score sidebar
with col_score:
    st.markdown("### 📊 Confidence Score")
    
    # Extract scores from events
    phase1_score = 0
    phase2_score = 0
    phase3_score = 0
    phase4_score = 0
    phase5_score = 0
    total_score = 0
    
    import re
    
    # Ensure events is a list
    if not isinstance(events, list):
        events = []
    
    for event in events:
        if not isinstance(event, dict):
            continue
            
        event_type = event.get('event_type', '')
        
        if event_type == 'ai_phase1_weather':
            data = event.get('data', {})
            if isinstance(data, dict):
                response = data.get('agent_response', '')
                match = re.search(r'(\d+)/25', response)
                if match:
                    phase1_score = int(match.group(1))
        
        elif event_type == 'ai_phase2_rivers':
            data = event.get('data', {})
            if isinstance(data, dict):
                response = data.get('agent_response', '')
                match = re.search(r'(\d+)/25', response)
                if match:
                    phase2_score = int(match.group(1))
        
        elif event_type == 'ai_phase3_ml':
            data = event.get('data', {})
            if isinstance(data, dict):
                response = data.get('agent_response', '')
                match = re.search(r'(\d+)/20', response)
                if match:
                    phase3_score = int(match.group(1))
        
        elif event_type == 'ai_phase4_social':
            data = event.get('data', {})
            if isinstance(data, dict):
                phase4_score = data.get('social_score', 0)
        
        elif event_type == 'ai_phase5_drone':
            data = event.get('data', {})
            if isinstance(data, dict):
                phase5_score = data.get('drone_score', 0)
    
    total_score = phase1_score + phase2_score + phase3_score + phase4_score + phase5_score
    
    # Display scores
    st.markdown(f"""
    <div class="score-box">
        <div class="score-value">{total_score}/100</div>
        <div class="score-label">TOTAL CONFIDENCE</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    **Phase Breakdown:**
    - Phase 1 (Weather): **{phase1_score}/25**
    - Phase 2 (Rivers): **{phase2_score}/25**
    - Phase 3 (ML Analysis): **{phase3_score}/20**
    - Phase 4 (Social Media): **{phase4_score}/15**
    - Phase 5 (Drone Vision): **{phase5_score}/15**
    """)
    
    if total_score >= 60:
        st.markdown("🔴 **Status:** CRITICAL")
    elif total_score >= 20:
        st.markdown("🟡 **Status:** WARNING")
    elif total_score > 0:
        st.markdown("🟢 **Status:** MONITORING")
    else:
        st.markdown("⚪ **Status:** IDLE")
    
    # Check orchestration state
    approval_required = False
    orchestration_approved = False
    orchestration_pending = False
    orchestration_triggered = False
    
    for event in events:
        if isinstance(event, dict):
            if event.get("event_type") == "orchestration_approval_required":
                approval_required = True
            elif event.get("event_type") == "orchestration_approved":
                orchestration_approved = True
            elif event.get("event_type") == "orchestration_pending":
                orchestration_pending = True
            elif event.get("event_type") == "orchestration_triggered":
                orchestration_triggered = True
    
    # Show approval buttons if approval required (score 60-89)
    if approval_required and not orchestration_approved and not orchestration_triggered:
        st.markdown("---")
        st.markdown("### ⚠️ HUMAN APPROVAL REQUIRED")
        st.warning("Score 60-89: Emergency response requires human authorization")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ APPROVE", use_container_width=True, type="primary"):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/orchestration/approve",
                        timeout=10
                    )
                    if response.status_code == 200:
                        st.success("Approved! Now select scenario...")
                        time.sleep(1)
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            if st.button("❌ REJECT", use_container_width=True):
                st.warning("Orchestration rejected - continuing monitoring")
    
    # Show scenario selection buttons if approved OR pending (90+)
    if (orchestration_pending or orchestration_approved) and not orchestration_triggered:
        st.markdown("---")
        st.markdown("### 🚨 SELECT SCENARIO")
        
        if st.button("🏥 Scenario 1: Hospital Crisis", use_container_width=True, type="primary"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/orchestration/trigger",
                    json={"scenario": 1},
                    timeout=30
                )
                if response.status_code == 200:
                    st.success("Scenario 1 activated!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        
        st.caption("Hospital overwhelmed → Police crowd control")
        
        if st.button("🚤 Scenario 2: Rescue Coordination", use_container_width=True, type="primary"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/orchestration/trigger",
                    json={"scenario": 2},
                    timeout=30
                )
                if response.status_code == 200:
                    st.success("Scenario 2 activated!")
                    time.sleep(1)
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
        
        st.caption("Rescue needs routes → Transport + Police coordination")

# Logs section
with col_logs:
    st.markdown("### 📋 Monitoring Log")
    
    if not events:
        st.info("⏳ No events yet. Click a scenario button to start monitoring.")
    else:
        # Create log-style output
        log_html = '<div class="log-container">'
        
        for idx, event in enumerate(events):
            if not isinstance(event, dict):
                continue
                
            event_type = event.get('event_type', '')
            event_data = event.get('data', {})
            timestamp = event.get('timestamp', datetime.now().isoformat())
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime('%H:%M:%S')
            except:
                time_str = timestamp[:8]
            
            log_html += f'<div class="log-entry">'
            log_html += f'<span class="log-timestamp">[{time_str}]</span> '
            
            # Weather alert
            if event_type == 'weather_alert':
                alert = event_data
                severity = alert.get('severity', {}).get('level', 0)
                precip = alert.get('precipitation', {}).get('expected_amount_mm', 0)
                log_html += f'<span class="log-phase">PHASE 1: WEATHER ALERT</span><br>'
                log_html += f'  └─ Alert ID: {alert.get("alert_id", "N/A")}<br>'
                log_html += f'  └─ Severity: <span class="log-warning">{severity}/5</span> | Precipitation: <span class="log-warning">{precip}mm</span><br>'
                log_html += f'  └─ Location: {alert.get("location", {}).get("region", "N/A")} (ZIP: {alert.get("location", {}).get("zipcode", "N/A")})<br>'
            
            # AI Phase 1
            elif event_type == 'ai_phase1_weather':
                response = event_data.get('agent_response', '')
                log_html += f'<span class="log-phase">🤖 AI ANALYSIS - WEATHER SCORING</span><br>'
                
                # Extract score
                import re
                match = re.search(r'(\d+)/25', response)
                if match:
                    score = int(match.group(1))
                    score_class = 'log-critical' if score >= 20 else 'log-warning'
                    log_html += f'  └─ Weather Score: <span class="{score_class}">{score}/25</span><br>'
                
                # Extract recommendation
                if 'escalat' in response.lower():
                    log_html += f'  └─ <span class="log-warning">⚠️ ESCALATION RECOMMENDED</span><br>'
                
                # Add embedded toggle for AI details
                log_html += '</div>'
                st.markdown(log_html, unsafe_allow_html=True)
                log_html = ''
                with st.expander("🔍 View Detailed AI Analysis", expanded=False):
                    st.code(response, language="markdown")
                continue
            
            # Searching rivers
            elif event_type == 'searching_rivers':
                zipcode = event_data.get('zipcode', 'N/A')
                log_html += f'<span class="log-phase">PHASE 2: RIVER GAUGE DEPLOYMENT</span><br>'
                log_html += f'  └─ <span class="log-info">🔍 Searching rivers near ZIP {zipcode}...</span><br>'
            
            # Fetching gauges
            elif event_type == 'fetching_gauges':
                log_html += f'  └─ <span class="log-info">📡 Fetching sensor data from identified rivers...</span><br>'
            
            # River data
            elif event_type == 'river_gauge_data':
                rivers = event_data.get('rivers', [])
                log_html += f'  └─ <span class="log-success">Found {len(rivers)} rivers</span><br>'
                
                for river in rivers:
                    river_name = river.get('river_name', 'Unknown')
                    sensors = river.get('sensors', [])
                    log_html += f'  └─ 📍 {river_name} ({len(sensors)} sensors)<br>'
                    
                    # Show sensor table
                    log_html += '  └─ <table class="sensor-table">'
                    log_html += '<tr><th>Sensor</th><th>Water Level</th><th>Flow Rate</th><th>Status</th><th>Trend</th></tr>'
                    
                    for sensor in sensors:
                        status = sensor.get('status', 'normal')
                        status_class = f'status-{status}'
                        log_html += f'<tr>'
                        log_html += f'<td>{sensor.get("sensor_name", "N/A")}</td>'
                        log_html += f'<td>{sensor.get("water_level_m", 0)}m</td>'
                        log_html += f'<td>{sensor.get("flow_rate_cms", 0)} m³/s</td>'
                        log_html += f'<td class="{status_class}">{status.upper()}</td>'
                        log_html += f'<td>{sensor.get("trend", "N/A")}</td>'
                        log_html += f'</tr>'
                    
                    log_html += '</table>'
            
            # AI Phase 2
            elif event_type == 'ai_phase2_rivers':
                response = event_data.get('agent_response', '')
                log_html += f'<span class="log-phase">🤖 AI ANALYSIS - RIVER GAUGE SCORING</span><br>'
                
                # Extract score
                import re
                match = re.search(r'(\d+)/25', response)
                if match:
                    score = int(match.group(1))
                    score_class = 'log-critical' if score >= 20 else 'log-warning'
                    log_html += f'  └─ River Score: <span class="{score_class}">{score}/25</span><br>'
                
                # Add embedded toggle for AI details
                log_html += '</div>'
                st.markdown(log_html, unsafe_allow_html=True)
                log_html = ''
                with st.expander("🔍 View Detailed AI Analysis", expanded=False):
                    st.code(response, language="markdown")
                continue
                
                # Extract cumulative
                match = re.search(r'Cumulative.*?(\d+)/100', response)
                if match:
                    cumulative = int(match.group(1))
                    log_html += f'  └─ Cumulative: <span class="log-warning">{cumulative}/100</span><br>'
                
                # Check for next escalation
                if 'Phase 3' in response or 'satellite' in response.lower():
                    log_html += f'  └─ <span class="log-warning">⚠️ ESCALATION TO PHASE 3 RECOMMENDED</span><br>'
                
                log_html += f'  └─ Analysis: {response[:200]}...<br>'
            
            # ML Analysis Progress
            elif event_type == 'ml_analysis_progress':
                message = event_data.get('message', '')
                log_html += f'<span class="log-phase">PHASE 3: ML ANALYSIS</span><br>'
                log_html += f'  └─ <span class="log-info">{message}</span><br>'
                log_html += f'  └─ ⏳ Analyzing patterns (T±30 mins window)...<br>'
            
            # ML Similarity Result
            elif event_type == 'ml_similarity_result':
                ml_data = event_data.get('ml_analysis', {})
                best_match = event_data.get('best_match', {})
                similarity = event_data.get('similarity_percent', 0)
                
                log_html += f'  └─ <span class="log-success">✓ Analysis Complete</span><br>'
                log_html += f'  └─ Best Match: <b>{best_match.get("event_id", "N/A")}</b><br>'
                log_html += f'  └─ Similarity: <span class="log-warning">{similarity:.1f}%</span><br>'
                log_html += f'  └─ Historical Outcome: {best_match.get("outcome", "N/A").replace("_", " ").title()}<br>'
                log_html += f'  └─ Damage Level: <span class="log-critical">{best_match.get("damage_level", "N/A").upper()}</span><br>'
            
            # AI Phase 3
            elif event_type == 'ai_phase3_ml':
                response = event_data.get('agent_response', '')
                log_html += f'<span class="log-phase">🤖 AI ANALYSIS - ML HISTORICAL SCORING</span><br>'
                
                # Extract score
                import re
                match = re.search(r'(\d+)/20', response)
                if match:
                    score = int(match.group(1))
                    score_class = 'log-critical' if score >= 15 else 'log-warning'
                    log_html += f'  └─ ML Score: <span class="{score_class}">{score}/20</span><br>'
                
                # Add embedded toggle for AI details
                log_html += '</div>'
                st.markdown(log_html, unsafe_allow_html=True)
                log_html = ''
                with st.expander("🔍 View Detailed AI Analysis", expanded=False):
                    st.code(response, language="markdown")
                continue
                
                # Extract cumulative
                match_cumulative = re.search(r'(\d+)/100', response)
                if match_cumulative:
                    cumulative = int(match_cumulative.group(1))
                    log_html += f'  └─ Cumulative: <span class="log-warning">{cumulative}/100</span><br>'
                
                log_html += f'  └─ Analysis: {response[:250]}...<br>'
            
            # Social Media Search
            elif event_type == 'social_media_search':
                keywords = event_data.get('keywords', [])
                message = event_data.get('message', '')
                log_html += f'<span class="log-phase">PHASE 4: SOCIAL MEDIA ANALYSIS</span><br>'
                log_html += f'  └─ <span class="log-info">{message}</span><br>'
                log_html += f'  └─ Keywords: {", ".join(keywords)}<br>'
            
            # Affected Zones
            elif event_type == 'affected_zones':
                zones = event_data.get('zones', {})
                high_risk = event_data.get('high_risk_zones', [])
                
                log_html += f'  └─ <span class="log-warning">📍 HIGH-RISK ZONES IDENTIFIED:</span><br>'
                for zone_name, zone_data in zones.items():
                    risk_level = zone_data.get('risk_level', 'N/A')
                    mentions = zone_data.get('mentions', 0)
                    risk_class = 'log-critical' if risk_level == 'CRITICAL' else 'log-warning'
                    log_html += f'  └─ <span class="{risk_class}">{zone_name}</span>: {zone_data.get("name", "N/A")} - {risk_level} ({mentions} mentions)<br>'
                
                if high_risk:
                    log_html += f'  └─ <span class="log-critical">⚠️ EVACUATION ZONES: {", ".join(high_risk)}</span><br>'
            
            # AI Phase 4
            elif event_type == 'ai_phase4_social':
                response = event_data.get('agent_response', '')
                social_score = event_data.get('social_score', 0)
                high_risk_zones = event_data.get('high_risk_zones', [])
                
                log_html += f'<span class="log-phase">🤖 AI ANALYSIS - SOCIAL MEDIA SCORING</span><br>'
                log_html += f'  └─ Social Media Score: <span class="log-warning">{social_score}/15</span><br>'
                
                if high_risk_zones:
                    log_html += f'  └─ Priority Zones: {", ".join(high_risk_zones)}<br>'
                
                # Add embedded toggle for AI details
                log_html += '</div>'
                st.markdown(log_html, unsafe_allow_html=True)
                log_html = ''
                with st.expander("🔍 View Detailed AI Analysis", expanded=False):
                    st.code(response, language="markdown")
                continue
            
            # Drone Deployment
            elif event_type == 'drone_deployment':
                target = event_data.get('target', 'N/A')
                log_html += f'<span class="log-phase">PHASE 5: DRONE AERIAL SURVEILLANCE</span><br>'
                log_html += f'  └─ <span class="log-info">🚁 Deploying surveillance drone...</span><br>'
                log_html += f'  └─ Target: {target}<br>'
            
            # Drone Streaming
            elif event_type == 'drone_streaming':
                log_html += f'  └─ <span class="log-success">✓ Drone reached target area</span><br>'
                log_html += f'  └─ <span class="log-info">📸 Streaming aerial imagery...</span><br>'
            
            # AI Phase 5
            elif event_type == 'ai_phase5_drone':
                response = event_data.get('agent_response', '')
                drone_score = event_data.get('drone_score', 0)
                images_analyzed = event_data.get('images_analyzed', 0)
                
                log_html += f'<span class="log-phase">🤖 AI ANALYSIS - DRONE VISION SCORING</span><br>'
                log_html += f'  └─ Drone Vision Score: <span class="log-warning">{drone_score}/15</span><br>'
                log_html += f'  └─ Images Analyzed: {images_analyzed}<br>'
                
                # Add embedded toggle for AI details
                log_html += '</div>'
                st.markdown(log_html, unsafe_allow_html=True)
                log_html = ''
                with st.expander("🔍 View Detailed AI Analysis", expanded=False):
                    st.code(response, language="markdown")
                continue
            
            # ORCHESTRATION EVENTS
            elif event_type == 'orchestration_approval_required':
                confidence_score = event_data.get('confidence_score', 0)
                log_html += f'<span class="log-warning">⚠️ ELEVATED CONFIDENCE (60-89) - HUMAN APPROVAL REQUIRED</span><br>'
                log_html += f'  └─ Confidence Score: <span class="log-warning">{confidence_score}/100</span><br>'
                log_html += f'  └─ <span class="log-warning">👈 APPROVE/REJECT IN SIDEBAR</span><br>'
            
            elif event_type == 'orchestration_approved':
                confidence_score = event_data.get('confidence_score', 0)
                log_html += f'<span class="log-success">✅ ORCHESTRATION APPROVED BY HUMAN</span><br>'
                log_html += f'  └─ Confidence Score: <span class="log-success">{confidence_score}/100</span><br>'
                log_html += f'  └─ <span class="log-warning">👉 SELECT EMERGENCY SCENARIO FROM SIDEBAR</span><br>'
            
            elif event_type == 'orchestration_pending':
                confidence_score = event_data.get('confidence_score', 0)
                log_html += f'<span class="log-critical">🚨 CRITICAL THRESHOLD (90+) REACHED - AUTO-APPROVED</span><br>'
                log_html += f'  └─ Confidence Score: <span class="log-critical">{confidence_score}/100</span><br>'
                log_html += f'  └─ <span class="log-warning">👉 SELECT EMERGENCY SCENARIO FROM SIDEBAR</span><br>'
            
            elif event_type == 'orchestration_triggered':
                confidence_score = event_data.get('confidence_score', 0)
                scenario = event_data.get('scenario', 1)
                log_html += f'<span class="log-critical">🚨 SCENARIO {scenario} ACTIVATED - EMERGENCY ORCHESTRATION TRIGGERED</span><br>'
                log_html += f'  └─ Confidence Score: <span class="log-critical">{confidence_score}/65</span><br>'
                log_html += f'  └─ <span class="log-critical">⚠️ ACTIVATING ALL EMERGENCY RESPONSE AGENTS</span><br>'
            
            elif event_type == 'orchestration_summary':
                summary = event_data.get('summary', {})
                agents = event_data.get('agents_activated', [])
                log_html += f'<span class="log-success">✅ EMERGENCY COORDINATION COMPLETE</span><br>'
                log_html += f'  └─ <span class="log-success">{len(agents)} agents activated</span><br>'
                log_html += f'  └─ 📡 Alerts Sent: <span class="log-warning">{summary.get("alerts_sent", 0):,}</span><br>'
                log_html += f'  └─ 🚔 Police Cars: <span class="log-warning">{summary.get("police_cars", 0)}</span><br>'
                log_html += f'  └─ 🚑 Ambulances: <span class="log-warning">{summary.get("ambulances", 0)}</span><br>'
                log_html += f'  └─ 🚌 Buses: <span class="log-warning">{summary.get("buses", 0)}</span><br>'
            
            elif event_type == 'agent_response':
                agent_name = event_data.get('agent_name', '').replace('Agent', '')
                response = event_data.get('response', {})
                logs = event_data.get('logs', [])
                
                icon_map = {
                    'CommunicationAlert': '📡',
                    'Police': '🚔',
                    'HospitalEMS': '🏥',
                    'Rescue': '🚤',
                    'Utility': '⚡',
                    'Transport': '🚌',
                    'Relief': '🏠'
                }
                icon = icon_map.get(agent_name, '🔧')
                
                log_html += f'<span class="log-success">{icon} {agent_name} Agent Activated</span><br>'
                
                # Show key metrics
                if isinstance(response, dict):
                    key_metrics = []
                    if 'alerts_sent' in response:
                        key_metrics.append(f"📡 {response['alerts_sent']:,} alerts sent")
                    if 'cars_dispatched' in response:
                        key_metrics.append(f"🚔 {response['cars_dispatched']} cars")
                    if 'ambulances' in response:
                        key_metrics.append(f"🚑 {response['ambulances']} ambulances")
                    if 'icu_beds' in response:
                        key_metrics.append(f"🏥 {response['icu_beds']} ICU beds")
                    if 'vehicles' in response:
                        key_metrics.append(f"🚤 {response['vehicles']} rescue vehicles")
                    if 'buses' in response:
                        key_metrics.append(f"🚌 {response['buses']} buses")
                    if 'supplies' in response:
                        key_metrics.append(f"📦 {response['supplies']} supplies")
                    
                    for metric in key_metrics:
                        log_html += f'  └─ {metric}<br>'
                
                # Show inter-agent communications prominently
                if logs:
                    for log in logs:
                        log_clean = log.replace('[' + agent_name + 'Agent]', '').strip()
                        if 'Sending' in log or 'CRITICAL' in log or 'URGENT' in log:
                            log_html += f'  └─ <span class="log-critical">🔗 {log_clean}</span><br>'
                        elif 'Received' in log or '✅' in log:
                            log_html += f'  └─ <span class="log-success">✅ {log_clean}</span><br>'
                        elif '⚠️' in log or 'HIGH' in log:
                            log_html += f'  └─ <span class="log-warning">⚠️ {log_clean}</span><br>'
                        elif '📡' in log or '📨' in log or '🚨' in log or '🚔' in log:
                            log_html += f'  └─ <span class="log-warning">{log_clean}</span><br>'
                        else:
                            log_html += f'  └─ <span class="log-info">{log_clean}</span><br>'
            
            log_html += '</div>'
        
        log_html += '</div>'
        st.markdown(log_html, unsafe_allow_html=True)
        
        # Skip Decision Flowchart and Detailed Responses - everything is in the monitoring log
        if False and phase1_score > 0 and phase2_score > 0 and phase3_score > 0 and phase4_score > 0 and phase5_score > 0:
            st.markdown("---")
            st.markdown("### 📊 AI Agent Decision Chain")
            
            # Build flowchart as clean markdown
            flowchart = f"""
**🎯 AI Agent Decision Flow**

**🤖 Flood Orchestrator Agent**  
└─ **Phase 1:** Weather Alert Analysis  
   └─ Tool: `score_weather_alert` → **{phase1_score}/25**  
   └─ Decision: {'🔴 ESCALATE' if phase1_score >= 20 else '🟡 Monitor'}

↓

└─ **Phase 2:** River Gauge Analysis  
   └─ Tool: `score_river_gauges` (6 sensors, 2 rivers) → **{phase2_score}/25**  
   └─ Decision: {'🔴 ESCALATE' if phase2_score >= 15 else '🟡 Continue monitoring'}

↓

└─ **Phase 3:** ML Historical Similarity  
   └─ Tool: `score_ml_similarity` (87% match) → **{phase3_score}/20**  
   └─ Decision: {'🔴 ESCALATE' if phase3_score >= 10 else '🟡 Low similarity'}

---

**🤖 Social Media Agent**  
└─ **Phase 4:** X/Twitter Analysis  
   └─ Tools: `search_tweets_by_location`, `search_tweets_by_keywords`, `score_social_media_impact`  
   └─ Result: Zone A & Zone B identified → **{phase4_score}/15**  
   └─ Decision: {'🔴 ESCALATE' if phase4_score >= 10 else '🟡 Low concern'}

---

**🤖 Drone Agent**  
└─ **Phase 5:** Aerial Surveillance  
   └─ Tools: `analyze_drone_images`, `score_drone_analysis`  
   └─ Result: Visual confirmation of severe conditions → **{phase5_score}/15**  
   └─ Decision: {'🔴 CONFIRMED' if phase5_score >= 10 else '🟡 Moderate'}

---

**📈 FINAL DECISION**

{'🔴 **CRITICAL ALERT**' if total_score >= 80 else '🟠 **HIGH RISK**' if total_score >= 60 else '🟡 **MODERATE RISK**'}  
**Total Confidence:** {total_score}/100 ({int(total_score)}%)  
**Recommendation:** {'Immediate emergency response and evacuation' if total_score >= 80 else 'Activate emergency protocols' if total_score >= 60 else 'Continue enhanced monitoring'}
"""
            st.markdown(flowchart)
        
# All monitoring now in main log - removed redundant "Detailed AI Responses" section

# Refresh button
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Refresh Events"):
        st.session_state['events'] = get_events()
        st.rerun()
