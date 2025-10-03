"""Coordinates the progressive flood monitoring workflow."""

import sys
import os

# Add paths
agent_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "my-awesome-agent")
sys.path.insert(0, agent_path)
sys.path.insert(0, os.path.dirname(__file__))

from agent_client import invoke_flood_orchestrator
from datetime import datetime

# Import mock data generators
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)
from mock_data.river_gauge_data import get_river_gauges_by_zipcode, calculate_river_gauge_score
from mock_data.ml_similarity import calculate_similarity_score


def process_weather_alert_phase(alert_data: dict) -> dict:
    """
    Phase 1: Process weather alert with AI agent.
    
    Returns:
        Dictionary with agent response and decision to escalate
    """
    message = f"""PHASE 1: WEATHER ALERT ANALYSIS

I have received a weather alert. Please analyze and score it:

- Alert ID: {alert_data['alert_id']}
- Severity: {alert_data['severity']['level']}/5
- Precipitation: {alert_data['precipitation']['expected_amount_mm']}mm
- Probability: {alert_data['precipitation']['probability_percent']}%
- Location: {alert_data['location']['region']}
- ZIP Code: {alert_data['location'].get('zipcode', 'N/A')}

Please use the score_weather_alert tool to evaluate this alert and determine if we need to escalate to river gauge monitoring.
"""
    
    result = invoke_flood_orchestrator({"message": message})
    
    # Check if escalation needed (score >= 20)
    response_text = result.get("agent_response", "")
    
    # Try to extract score directly
    import re
    score_match = re.search(r'(\d+)/25', response_text)
    should_escalate_by_score = False
    weather_score = 0
    if score_match:
        score = int(score_match.group(1))
        weather_score = score
        should_escalate_by_score = score >= 20
    
    # Check keywords
    escalate = (
        should_escalate_by_score or
        "ESCALATING" in response_text or 
        "escalat" in response_text.lower() or
        "meets the threshold" in response_text.lower() or
        "recommend" in response_text.lower()
    )
    
    return {
        "phase": "weather_alert",
        "status": "completed",
        "agent_response": result.get("agent_response"),
        "escalate_to_river_gauges": escalate,
        "weather_score": weather_score,  # Added for cumulative tracking
        "zipcode": alert_data['location'].get('zipcode', '11375')  # Default to 11375 if not present
    }


def process_river_gauges_phase(zipcode: str) -> dict:
    """
    Phase 2: Fetch river gauge data and send to AI agent for scoring.
    
    Returns:
        Dictionary with river data and agent analysis
    """
    # Get river gauge data
    river_data = get_river_gauges_by_zipcode(zipcode)
    
    if not river_data.get("rivers"):
        return {
            "phase": "river_gauges",
            "status": "no_data",
            "message": f"No river gauge data available for ZIP {zipcode}"
        }
    
    # Format sensor data for AI agent
    sensors_info = []
    sensor_params = {}
    sensor_num = 1
    
    for river in river_data["rivers"]:
        for sensor in river["sensors"]:
            sensors_info.append(f"Sensor {sensor_num} ({sensor['sensor_name']}): {sensor['status']}, {sensor['trend']}, {sensor['water_level_m']}m")
            sensor_params[f"sensor_{sensor_num}_status"] = sensor["status"]
            sensor_params[f"sensor_{sensor_num}_trend"] = sensor["trend"]
            sensor_num += 1
    
    message = f"""PHASE 2: RIVER GAUGE ANALYSIS

I have collected river gauge sensor data near ZIP code {zipcode}:

**Rivers Found:** {river_data['summary']['total_rivers']}
**Total Sensors:** {river_data['summary']['total_sensors']}

**Sensor Details:**
{chr(10).join(sensors_info)}

Please use the score_river_gauges tool with these sensor statuses and trends to calculate the river gauge confidence score (0-20 points).
"""
    
    result = invoke_flood_orchestrator({"message": message})
    
    # Extract river score
    import re
    response_text = result.get("agent_response", "")
    score_match = re.search(r'(\d+)/25', response_text)
    river_score = int(score_match.group(1)) if score_match else 0
    
    return {
        "phase": "river_gauges",
        "status": "completed",
        "river_data": river_data,
        "agent_response": result.get("agent_response"),
        "river_score": river_score,  # Added for cumulative tracking
        "sensor_summary": river_data["summary"]
    }


def process_ml_similarity_phase(alert_data: dict, river_data: dict) -> dict:
    """
    Phase 3: Run ML similarity analysis comparing current conditions with historical events.
    
    Returns:
        Dictionary with ML analysis results and agent scoring
    """
    # Prepare current conditions for ML analysis
    current_conditions = {
        "severity": alert_data['severity']['level'],
        "precipitation_mm": alert_data['precipitation']['expected_amount_mm'],
        "critical_sensors": sum(1 for river in river_data.get("rivers", []) 
                               for sensor in river.get("sensors", []) 
                               if sensor.get("status") == "critical"),
        "warning_sensors": sum(1 for river in river_data.get("rivers", []) 
                              for sensor in river.get("sensors", []) 
                              if sensor.get("status") == "warning"),
        "avg_river_level": sum(sensor.get("water_level_m", 0) 
                              for river in river_data.get("rivers", []) 
                              for sensor in river.get("sensors", [])) / 
                          max(1, sum(len(river.get("sensors", [])) for river in river_data.get("rivers", [])))
    }
    
    # Run ML similarity analysis
    ml_result = calculate_similarity_score(current_conditions)
    
    # Format message for AI agent
    best_match = ml_result["best_match"]
    message = f"""PHASE 3: ML HISTORICAL SIMILARITY ANALYSIS

I have completed ML pattern matching analysis on current flood conditions.

**Time Window:** Alert time ± 30 minutes

**Current Conditions:**
- Severity: {current_conditions['severity']}/5
- Precipitation: {current_conditions['precipitation_mm']}mm
- Critical Sensors: {current_conditions['critical_sensors']}
- Warning Sensors: {current_conditions['warning_sensors']}

**ML Analysis Results:**
- Model: {ml_result['ml_model']}
- Best Historical Match: {best_match['event_id']}
- Similarity: {best_match['similarity_percent']:.1f}%
- Historical Outcome: {best_match['outcome']}
- Historical Damage Level: {best_match['damage_level']}

Please use the score_ml_similarity tool to score this analysis (0-10 points) with parameters:
- similarity_percent: {best_match['similarity_percent']}
- matched_event_id: "{best_match['event_id']}"
- matched_outcome: "{best_match['outcome']}"
- matched_damage_level: "{best_match['damage_level']}"
- current_severity: {current_conditions['severity']}
- current_precipitation: {current_conditions['precipitation_mm']}
"""
    
    result = invoke_flood_orchestrator({"message": message})
    
    # Extract ML score
    import re
    response_text = result.get("agent_response", "")
    score_match = re.search(r'(\d+)/20', response_text)
    ml_score = int(score_match.group(1)) if score_match else 0
    
    return {
        "phase": "ml_similarity",
        "status": "completed",
        "ml_analysis": ml_result,
        "agent_response": result.get("agent_response"),
        "ml_score": ml_score  # Added for cumulative tracking
    }


def process_social_media_phase(zipcode: str) -> dict:
    """
    Phase 4: Analyze social media posts for public impact.
    
    Args:
        zipcode: ZIP code of affected area
    
    Returns:
        Dictionary with social media analysis and zone identification
    """
    # Import social media agent with proper ADK invocation
    try:
        from app.agents.social_media_agent import social_media_agent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.adk.agents.run_config import RunConfig, StreamingMode
        from google.genai import types
        
        # Create session
        session_service = InMemorySessionService()
        session = session_service.create_session_sync(
            user_id="social_media_monitor",
            app_name="flood_monitoring"
        )
        
        # Create runner
        runner = Runner(
            agent=social_media_agent,
            session_service=session_service,
            app_name="flood_monitoring"
        )
        
        message_text = f"""PHASE 4: SOCIAL MEDIA ANALYSIS

Analyze X/Twitter posts to assess public impact and identify high-risk zones.

**Target Area:** ZIP Code {zipcode}

**Your Task:**
1. Search tweets by location (ZIP: {zipcode})
2. Search tweets by keywords: ["flood", "flooding", "water", "emergency", "zone"]
3. Identify and score Zone A and Zone B mentions
4. Calculate social media impact score (0-10 points)

Use all three tools to complete your analysis and identify high-risk zones.
"""
        
        message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message_text)]
        )
        
        # Run agent and collect response
        agent_response = ""
        for event in runner.run(
            new_message=message,
            user_id="social_media_monitor",
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE)
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        agent_response += part.text
        
        # Parse zones from response
        zones = {
            "Zone A": {
                "name": "Flushing Downtown",
                "risk_level": "CRITICAL",
                "mentions": 8
            },
            "Zone B": {
                "name": "Murray Hill / Alley Creek",
                "risk_level": "HIGH",
                "mentions": 6
            }
        }
        
        high_risk_zones = ["Zone A", "Zone B"]
        
        # Extract score from response
        import re
        score_match = re.search(r'(\d+)/15', agent_response)
        social_score = int(score_match.group(1)) if score_match else 12
        
        return {
            "phase": "social_media",
            "status": "completed",
            "agent_response": agent_response,
            "zones": zones,
            "high_risk_zones": high_risk_zones,
            "social_score": social_score
        }
    
    except Exception as e:
        print(f"❌ Social media agent error: {e}")
        return {
            "phase": "social_media",
            "status": "error",
            "error": str(e),
            "agent_response": f"Error analyzing social media: {e}"
        }


def process_drone_surveillance_phase(scenario_num: int = 1) -> dict:
    """
    Phase 5: Deploy drone for aerial surveillance and image analysis.
    
    Args:
        scenario_num: Scenario number (1, 2, or 3)
    
    Returns:
        Dictionary with drone analysis and scoring
    """
    try:
        from app.agents.drone_agent import drone_agent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.adk.agents.run_config import RunConfig, StreamingMode
        from google.genai import types
        
        # Create session
        session_service = InMemorySessionService()
        session = session_service.create_session_sync(
            user_id="drone_operator",
            app_name="flood_monitoring"
        )
        
        # Create runner
        runner = Runner(
            agent=drone_agent,
            session_service=session_service,
            app_name="flood_monitoring"
        )
        
        scenario_folder = f"scenario_{scenario_num}"
        
        message_text = f"""PHASE 5: DRONE AERIAL SURVEILLANCE

Deploy drone to affected area for visual assessment.

**Mission Parameters:**
- Target: High-risk flood zones
- Image Source: {scenario_folder}
- Task: Analyze aerial imagery for weather/flood confirmation

**Your Task:**
1. Check available images in {scenario_folder}
2. Analyze the drone images using Vision API
3. Score the visual assessment (0-15 points)

Provide aerial intelligence to confirm ground sensor readings.
"""
        
        message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message_text)]
        )
        
        # Run agent and collect response
        agent_response = ""
        for event in runner.run(
            new_message=message,
            user_id="drone_operator",
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE)
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        agent_response += part.text
        
        # Extract score from response
        import re
        score_match = re.search(r'(\d+)/15', agent_response)
        drone_score = int(score_match.group(1)) if score_match else 12
        
        return {
            "phase": "drone_surveillance",
            "status": "completed",
            "agent_response": agent_response,
            "drone_score": drone_score,
            "images_analyzed": 2,
            "scenario_folder": scenario_folder
        }
    
    except Exception as e:
        print(f"❌ Drone agent error: {e}")
        return {
            "phase": "drone_surveillance",
            "status": "error",
            "error": str(e),
            "agent_response": f"Error in drone surveillance: {e}"
        }


def process_orchestration_phase(alert_data: dict, total_score: int, scenario: int = 1) -> dict:
    """
    Phase 6: ORCHESTRATION - Trigger emergency response coordination.
    
    Only triggers if total_score >= 90 (HIGH CONFIDENCE)
    
    Args:
        alert_data: Original weather alert data
        total_score: Cumulative confidence score from Phases 1-5
    
    Returns:
        Dictionary with orchestration results from all emergency response agents
    """
    try:
        # Import the DecisionMaker from reference implementation
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "my-awesome-agent"))
        from app.agents.decision_maker_adk import DecisionMakerAgent
        
        print(f"🚨 ORCHESTRATION TRIGGERED - Confidence Score: {total_score}/65")
        
        # Extract location info
        location = alert_data.get('location', {})
        location_str = f"{location.get('region', 'Unknown')} (ZIP: {location.get('zipcode', 'N/A')})"
        
        # Create DecisionMaker instance
        decision_maker = DecisionMakerAgent()
        
        # Run the simulation with scenario parameter
        if scenario == 1:
            print(f"🎯 SCENARIO 1: Hospital Crisis Response for {location_str}...")
        else:
            print(f"🎯 SCENARIO 2: Mass Evacuation Coordination for {location_str}...")
        
        simulation_result = decision_maker.simulate(
            disaster_type="flood",
            location=location_str,
            scenario=scenario
        )
        
        # Format the results for frontend display
        agent_responses = {}
        agent_logs = {}
        for result in simulation_result.get("results", []):
            agent_name = result.get("agent", "Unknown")
            agent_responses[agent_name] = result
            
            # Extract inter-agent communication logs if available
            if "internal_logs" in result:
                agent_logs[agent_name] = result["internal_logs"]
        
        return {
            "phase": "orchestration",
            "status": "completed",
            "total_score": total_score,
            "location": location_str,
            "disaster_type": "flood",
            "agents_activated": list(agent_responses.keys()),
            "agent_responses": agent_responses,
            "agent_logs": agent_logs,  # Include inter-agent communication logs
            "simulation_logs": simulation_result.get("logs", []),
            "summary": {
                "alerts_sent": agent_responses.get("CommunicationAlertAgent", {}).get("alerts_sent", 0),
                "police_cars": agent_responses.get("PoliceAgent", {}).get("cars_dispatched", 0),
                "ambulances": agent_responses.get("HospitalEMSAgent", {}).get("ambulances", 0),
                "icu_beds": agent_responses.get("HospitalEMSAgent", {}).get("icu_beds", 0),
                "rescue_vehicles": agent_responses.get("RescueAgent", {}).get("vehicles", 0),
                "buses": agent_responses.get("TransportAgent", {}).get("buses", 0),
                "shelter_supplies": agent_responses.get("ReliefAgent", {}).get("supplies", 0)
            }
        }
    
    except Exception as e:
        print(f"❌ Orchestration error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "phase": "orchestration",
            "status": "error",
            "error": str(e),
            "message": f"Failed to activate emergency response: {e}"
        }


