"""FastAPI backend for receiving flood monitoring alerts and data."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import uvicorn
import os
import sys

# Add my-awesome-agent to path for agent client
agent_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "my-awesome-agent")
print(f"🔍 Looking for agent at: {agent_path}")

AGENT_AVAILABLE = False
invoke_flood_orchestrator = None

if os.path.exists(agent_path):
    sys.path.insert(0, agent_path)
    try:
        # Import from the agent client which handles the imports correctly
        import sys
        client_path = os.path.join(os.path.dirname(__file__))
        sys.path.insert(0, client_path)
        from agent_client import invoke_flood_orchestrator
        AGENT_AVAILABLE = True
        print("✅ Agent available and loaded successfully!")
    except Exception as e:
        print(f"⚠️  Failed to load agent: {e}")
        print("Running in mock mode.")
else:
    print(f"⚠️  Agent path not found: {agent_path}")
    print("Running in mock mode.")

app = FastAPI(title="Flood Monitoring Backend")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for monitoring events
monitoring_events: List[Dict] = []


class WeatherAlert(BaseModel):
    """Weather alert data model"""
    alert_id: str
    alert_type: str
    timestamp: str
    valid_until: str
    issued_by: str
    location: Dict
    precipitation: Dict
    severity: Dict
    forecast: Dict
    message: str
    recommendations: List[str]


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Flood Monitoring Backend",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/alerts/weather")
async def receive_weather_alert(alert: WeatherAlert):
    """
    Receive weather alert from monitoring system.
    This is the entry point that triggers the orchestrator.
    """
    try:
        alert_dict = alert.model_dump()
        
        # Store the event
        event = {
            "event_type": "weather_alert",
            "phase": "T-2:00:00",
            "timestamp": datetime.now().isoformat(),
            "data": alert_dict,
            "status": "received"
        }
        monitoring_events.append(event)
        
        print(f"📡 Weather Alert Received: {alert.alert_id}")
        print(f"   Severity: {alert.severity['level']}/5")
        print(f"   Precipitation: {alert.precipitation['expected_amount_mm']}mm")
        
        # Trigger the AI orchestrator agent - Phase 1: Weather Alert
        agent_response = None
        orchestrator_status = "triggered"
        escalate_to_rivers = False
        
        if AGENT_AVAILABLE:
            print(f"🤖 Phase 1: Invoking AI Orchestrator for Weather Alert...")
            
            try:
                from flood_coordinator import process_weather_alert_phase
                phase1_result = process_weather_alert_phase(alert_dict)
                
                if phase1_result["status"] == "completed":
                    agent_response = phase1_result["agent_response"]
                    escalate_to_rivers = phase1_result["escalate_to_river_gauges"]
                    orchestrator_status = "phase1_completed"
                    print(f"✅ Phase 1 completed - Score calculated")
                    
                    # Store Phase 1 response
                    phase1_event = {
                        "event_type": "ai_phase1_weather",
                        "phase": "T-2:00:00",
                        "timestamp": datetime.now().isoformat(),
                        "data": {
                            "agent_response": agent_response,  # Fixed: was "response"
                            "alert_id": alert.alert_id,
                            "escalate": escalate_to_rivers
                        },
                        "status": "completed"
                    }
                    monitoring_events.append(phase1_event)
                    
                    # Phase 2: River Gauges (if escalated)
                    if escalate_to_rivers:
                        print(f"🌊 Phase 2: Escalating to River Gauge Monitoring...")
                        zipcode = alert_dict['location']['zipcode']
                        
                        # Add searching event
                        search_event = {
                            "event_type": "searching_rivers",
                            "phase": "T-1:00:00",
                            "timestamp": datetime.now().isoformat(),
                            "data": {
                                "message": f"Searching for rivers near ZIP code {zipcode}...",
                                "zipcode": zipcode
                            },
                            "status": "in_progress"
                        }
                        monitoring_events.append(search_event)
                        
                        # Add fetching gauges event
                        fetch_event = {
                            "event_type": "fetching_gauges",
                            "phase": "T-1:00:00",
                            "timestamp": datetime.now().isoformat(),
                            "data": {
                                "message": f"Fetching sensor data from identified rivers...",
                                "zipcode": zipcode
                            },
                            "status": "in_progress"
                        }
                        monitoring_events.append(fetch_event)
                        
                        from flood_coordinator import process_river_gauges_phase
                        phase2_result = process_river_gauges_phase(zipcode)
                        
                        if phase2_result["status"] == "completed":
                            print(f"✅ Phase 2 completed - River gauges analyzed")
                            
                            # Store river data event
                            river_data = phase2_result.get("river_data", {})
                            river_event = {
                                "event_type": "river_gauge_data",
                                "phase": "T-1:00:00",
                                "timestamp": datetime.now().isoformat(),
                                "data": {
                                    "rivers": river_data.get("rivers", []),  # Extract rivers array
                                    "summary": phase2_result.get("sensor_summary", {})
                                },
                                "status": "completed"
                            }
                            monitoring_events.append(river_event)
                            
                            # Store Phase 2 AI response
                            phase2_event = {
                                "event_type": "ai_phase2_rivers",
                                "phase": "T-1:00:00",
                                "timestamp": datetime.now().isoformat(),
                                "data": {
                                    "agent_response": phase2_result["agent_response"],  # Fixed: was "response"
                                    "alert_id": alert.alert_id
                                },
                                "status": "completed"
                            }
                            monitoring_events.append(phase2_event)
                            orchestrator_status = "phase2_completed"
                            
                            # Phase 3: ML Similarity Analysis (if cumulative score >= 40)
                            # Calculate cumulative score manually
                            cumulative_score_phase3 = (
                                phase1_result.get("weather_score", 0) +
                                phase2_result.get("river_score", 0)
                            )
                            
                            print(f"📊 Cumulative Score after Phase 2: {cumulative_score_phase3}/50")
                            
                            if cumulative_score_phase3 >= 15:  # Lowered to allow medium scenarios to progress
                                    print(f"🔬 Phase 3: Running ML Similarity Analysis...")
                                    
                                    # Add progress event
                                    import time
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
                                        
                                        # Phase 4: Social Media Analysis (trigger if cumulative >= 44)
                                        # Calculate cumulative score manually
                                        cumulative_score_phase4 = (
                                            phase1_result.get("weather_score", 0) +
                                            phase2_result.get("river_score", 0) +
                                            phase3_result.get("ml_score", 0)
                                        )
                                        
                                        print(f"📊 Cumulative Score after Phase 3: {cumulative_score_phase4}/70")
                                        
                                        if cumulative_score_phase4 >= 25:  # Lowered to allow medium scenarios to progress
                                                print(f"📱 Phase 4: Analyzing Social Media...")
                                                
                                                # Add social media search event
                                                social_search_event = {
                                                    "event_type": "social_media_search",
                                                    "phase": "T-0:15:00",
                                                    "timestamp": datetime.now().isoformat(),
                                                    "data": {
                                                        "message": f"Searching X/Twitter for flood reports near ZIP {zipcode}...",
                                                        "keywords": ["flood", "flooding", "water", "emergency", "zone"]
                                                    },
                                                    "status": "in_progress"
                                                }
                                                monitoring_events.append(social_search_event)
                                                
                                                from flood_coordinator import process_social_media_phase
                                                phase4_result = process_social_media_phase(zipcode)
                                                
                                                if phase4_result["status"] == "completed":
                                                    print(f"✅ Phase 4 completed - Social media analyzed")
                                                    
                                                    # Store affected zones event
                                                    zones_event = {
                                                        "event_type": "affected_zones",
                                                        "phase": "T-0:15:00",
                                                        "timestamp": datetime.now().isoformat(),
                                                        "data": {
                                                            "zones": phase4_result["zones"],
                                                            "high_risk_zones": phase4_result["high_risk_zones"]
                                                        },
                                                        "status": "completed"
                                                    }
                                                    monitoring_events.append(zones_event)
                                                    
                                                    # Store Phase 4 AI response
                                                    phase4_ai_event = {
                                                        "event_type": "ai_phase4_social",
                                                        "phase": "T-0:15:00",
                                                        "timestamp": datetime.now().isoformat(),
                                                        "data": {
                                                            "agent_response": phase4_result["agent_response"],
                                                            "social_score": phase4_result["social_score"],
                                                            "high_risk_zones": phase4_result["high_risk_zones"]
                                                        },
                                                        "status": "completed"
                                                    }
                                                    monitoring_events.append(phase4_ai_event)
                                                    
                                                    orchestrator_status = "phase4_completed"
                                                    
                                                    # Phase 5: Drone Surveillance (trigger if cumulative >= 54)
                                                    # Calculate cumulative score manually since social media agent doesn't track it
                                                    cumulative_score_phase5 = (
                                                        phase1_result.get("weather_score", 0) +
                                                        phase2_result.get("river_score", 0) +
                                                        phase3_result.get("ml_score", 0) +
                                                        phase4_result.get("social_score", 0)
                                                    )
                                                    
                                                    print(f"📊 Cumulative Score: {cumulative_score_phase5}/85 (before drone)")
                                                    
                                                    if cumulative_score_phase5 >= 35:  # Lowered to allow medium scenarios to progress
                                                            print(f"🚁 Phase 5: Deploying Drone for Aerial Surveillance...")
                                                            
                                                            # Add drone deployment event
                                                            drone_deploy_event = {
                                                                "event_type": "drone_deployment",
                                                                "phase": "T-0:10:00",
                                                                "timestamp": datetime.now().isoformat(),
                                                                "data": {
                                                                    "message": "Deploying surveillance drone to affected zones...",
                                                                    "target": "Zone A & Zone B"
                                                                },
                                                                "status": "in_progress"
                                                            }
                                                            monitoring_events.append(drone_deploy_event)
                                                            
                                                            # Add drone streaming event
                                                            drone_streaming_event = {
                                                                "event_type": "drone_streaming",
                                                                "phase": "T-0:10:00",
                                                                "timestamp": datetime.now().isoformat(),
                                                                "data": {
                                                                    "message": "Drone reached target area. Streaming aerial imagery...",
                                                                    "status": "streaming"
                                                                },
                                                                "status": "in_progress"
                                                            }
                                                            monitoring_events.append(drone_streaming_event)
                                                            
                                                            # Determine scenario from alert data
                                                            scenario_num = 1  # Default to scenario 1
                                                            
                                                            from flood_coordinator import process_drone_surveillance_phase
                                                            phase5_result = process_drone_surveillance_phase(scenario_num)
                                                            
                                                            if phase5_result["status"] == "completed":
                                                                print(f"✅ Phase 5 completed - Drone surveillance analyzed")
                                                                
                                                                # Store Phase 5 AI response
                                                                phase5_ai_event = {
                                                                    "event_type": "ai_phase5_drone",
                                                                    "phase": "T-0:10:00",
                                                                    "timestamp": datetime.now().isoformat(),
                                                                    "data": {
                                                                        "agent_response": phase5_result["agent_response"],
                                                                        "drone_score": phase5_result["drone_score"],
                                                                        "images_analyzed": phase5_result["images_analyzed"]
                                                                    },
                                                                    "status": "completed"
                                                                }
                                                                monitoring_events.append(phase5_ai_event)
                                                                
                                                                orchestrator_status = "phase5_completed"
                                                                
                                                                # PHASE 6: ORCHESTRATION - Trigger if cumulative score >= 90
                                                                final_cumulative_score = (
                                                                    phase1_result.get("weather_score", 0) +
                                                                    phase2_result.get("river_score", 0) +
                                                                    phase3_result.get("ml_score", 0) +
                                                                    phase4_result.get("social_score", 0) +
                                                                    phase5_result.get("drone_score", 0)
                                                                )
                                                                
                                                                print(f"📊 FINAL Cumulative Score: {final_cumulative_score}/65")
                                                                
                                                                if final_cumulative_score >= 90:
                                                                    print(f"🚨 CRITICAL THRESHOLD (90+) REACHED - AUTO-TRIGGERING SCENARIO SELECTION")
                                                                    
                                                                    # Score >= 90: Direct scenario selection (auto-approved)
                                                                    pending_orchestration_event = {
                                                                        "event_type": "orchestration_pending",
                                                                        "phase": "ORCHESTRATION",
                                                                        "timestamp": datetime.now().isoformat(),
                                                                        "data": {
                                                                            "message": f"🚨 CRITICAL CONFIDENCE ({final_cumulative_score}/100) - SELECT EMERGENCY SCENARIO",
                                                                            "confidence_score": final_cumulative_score,
                                                                            "threshold": 90,
                                                                            "alert_data": alert_dict,
                                                                            "requires_approval": False
                                                                        },
                                                                        "status": "awaiting_selection"
                                                                    }
                                                                    monitoring_events.append(pending_orchestration_event)
                                                                    orchestrator_status = "orchestration_pending"
                                                                    
                                                                elif final_cumulative_score >= 60:
                                                                    print(f"⚠️ HIGH THRESHOLD (60-89) REACHED - HUMAN APPROVAL REQUIRED")
                                                                    
                                                                    # Score 60-89: Requires human approval first
                                                                    approval_required_event = {
                                                                        "event_type": "orchestration_approval_required",
                                                                        "phase": "ORCHESTRATION",
                                                                        "timestamp": datetime.now().isoformat(),
                                                                        "data": {
                                                                            "message": f"⚠️ ELEVATED CONFIDENCE ({final_cumulative_score}/100) - HUMAN APPROVAL REQUIRED",
                                                                            "confidence_score": final_cumulative_score,
                                                                            "threshold": 60,
                                                                            "alert_data": alert_dict,
                                                                            "requires_approval": True
                                                                        },
                                                                        "status": "awaiting_approval"
                                                                    }
                                                                    monitoring_events.append(approval_required_event)
                                                                    orchestrator_status = "orchestration_approval_required"
                                                                else:
                                                                    print(f"ℹ️ Score {final_cumulative_score}/100 below orchestration threshold (60). No emergency response triggered.")
                
            except Exception as e:
                print(f"❌ Agent error: {e}")
                import traceback
                traceback.print_exc()
                orchestrator_status = "error"
        else:
            print("⚠️  Agent not available - running in mock mode")
        
        return {
            "status": "success",
            "message": "Weather alert received and processing initiated",
            "alert_id": alert.alert_id,
            "orchestrator_status": orchestrator_status,
            "agent_response": agent_response,
            "agent_available": AGENT_AVAILABLE,
            "event_count": len(monitoring_events)
        }
        
    except Exception as e:
        print(f"❌ Error processing alert: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/events")
def get_monitoring_events():
    """Get all monitoring events for display"""
    # Return just the list for easier frontend consumption
    return monitoring_events


@app.delete("/api/events")
def clear_events():
    """Clear all monitoring events (for testing)"""
    global monitoring_events
    monitoring_events = []
    return {"status": "success", "message": "All events cleared"}


@app.get("/api/events/latest")
def get_latest_event():
    """Get the most recent monitoring event"""
    if not monitoring_events:
        return {"status": "no_events"}
    return monitoring_events[-1]


@app.post("/api/orchestration/approve")
async def approve_orchestration():
    """
    Approve orchestration when human approval is required (score 60-89).
    """
    try:
        # Find the approval required event
        approval_event = None
        for event in reversed(monitoring_events):
            if event.get("event_type") == "orchestration_approval_required":
                approval_event = event
                break
        
        if not approval_event:
            raise HTTPException(status_code=400, detail="No approval required event found")
        
        confidence_score = approval_event["data"]["confidence_score"]
        alert_dict = approval_event["data"]["alert_data"]
        
        print(f"✅ HUMAN APPROVAL GRANTED - Converting to scenario selection")
        
        # Convert approval to pending (scenario selection)
        pending_event = {
            "event_type": "orchestration_approved",
            "phase": "ORCHESTRATION",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "message": f"✅ APPROVED - SELECT EMERGENCY SCENARIO",
                "confidence_score": confidence_score,
                "alert_data": alert_dict,
                "approved_by": "human"
            },
            "status": "approved"
        }
        monitoring_events.append(pending_event)
        
        return {
            "status": "success",
            "message": "Orchestration approved - select scenario",
            "confidence_score": confidence_score
        }
        
    except Exception as e:
        print(f"❌ Approval error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/orchestration/trigger")
async def trigger_orchestration(request: dict):
    """
    Trigger orchestration with a selected scenario.
    Expected payload: {"scenario": 1 or 2}
    """
    try:
        scenario = request.get("scenario", 1)
        
        # Find either pending or approved orchestration event
        pending_event = None
        for event in reversed(monitoring_events):
            if event.get("event_type") in ["orchestration_pending", "orchestration_approved"]:
                pending_event = event
                break
        
        if not pending_event:
            raise HTTPException(status_code=400, detail="No pending orchestration found")
        
        # Get stored data
        confidence_score = pending_event["data"]["confidence_score"]
        alert_dict = pending_event["data"]["alert_data"]
        
        print(f"🚨 TRIGGERING ORCHESTRATION - Scenario {scenario}")
        
        # Add orchestration trigger event
        orchestration_trigger_event = {
            "event_type": "orchestration_triggered",
            "phase": "ORCHESTRATION",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "message": f"⚠️ SCENARIO {scenario} SELECTED - Activating Emergency Response Coordination",
                "confidence_score": confidence_score,
                "threshold": 60,
                "scenario": scenario
            },
            "status": "triggered"
        }
        monitoring_events.append(orchestration_trigger_event)
        
        # Process orchestration with selected scenario
        from flood_coordinator import process_orchestration_phase
        orchestration_result = process_orchestration_phase(alert_dict, confidence_score, scenario=scenario)
        
        if orchestration_result["status"] == "completed":
            print(f"✅ ORCHESTRATION COMPLETED - All emergency agents responded")
            
            # Store orchestration summary event
            orchestration_summary_event = {
                "event_type": "orchestration_summary",
                "phase": "ORCHESTRATION",
                "timestamp": datetime.now().isoformat(),
                "data": {
                    "summary": orchestration_result["summary"],
                    "agents_activated": orchestration_result["agents_activated"],
                    "scenario": scenario
                },
                "status": "completed"
            }
            monitoring_events.append(orchestration_summary_event)
            
            # Store detailed responses from each agent
            agent_logs_dict = orchestration_result.get("agent_logs", {})
            for agent_name, agent_data in orchestration_result.get("agent_responses", {}).items():
                agent_event = {
                    "event_type": "agent_response",
                    "phase": "ORCHESTRATION",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "agent_name": agent_name,
                        "response": agent_data,
                        "logs": agent_logs_dict.get(agent_name, []),  # Include inter-agent communication logs
                        "scenario": scenario
                    },
                    "status": "completed"
                }
                monitoring_events.append(agent_event)
            
            return {
                "status": "success",
                "message": f"Orchestration triggered with Scenario {scenario}",
                "scenario": scenario,
                "agents_activated": orchestration_result["agents_activated"]
            }
        else:
            print(f"⚠️ Orchestration encountered issues")
            raise HTTPException(status_code=500, detail="Orchestration failed")
            
    except Exception as e:
        print(f"❌ Orchestration error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("🚀 Starting Flood Monitoring Backend...")
    print("📍 Backend URL: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

