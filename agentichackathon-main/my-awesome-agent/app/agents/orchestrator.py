# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Disaster response orchestrator agent - coordinates all specialist agents."""

from google.adk.agents import Agent
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agents.fire_agent import fire_agent
from app.agents.hospital_agent import hospital_agent
from app.agents.police_agent import police_agent
from app.tools.approval_tools import (
    format_approval_request,
    request_human_approval,
    simulate_human_approval,
)
from app.tools.weather_tools import classify_disaster_type, simulate_fire_weather_alert
from app.utils.shared_state import (
    get_all_agent_responses,
    reset_shared_state,
    set_disaster_context,
    store_agent_response,
)


def trigger_fire_alert(location: str) -> str:
    """Trigger a fire weather alert for the given location.
    
    Args:
        location: Location to simulate fire alert for
        
    Returns:
        Formatted alert information
    """
    alert_data = simulate_fire_weather_alert(location)
    disaster_type = classify_disaster_type(alert_data)
    
    # Store in shared context
    set_disaster_context({
        "alert_data": alert_data,
        "disaster_type": disaster_type,
        "location": location
    })
    
    return f"""🚨 FIRE WEATHER ALERT RECEIVED 🚨

Alert ID: {alert_data['alert_id']}
Type: {alert_data['alert_type']}
Classification: {disaster_type}
Location: {alert_data['location']['city']}, {alert_data['location']['state']}
Severity: {alert_data['severity']}

Conditions:
- Temperature: {alert_data['conditions']['temperature_f']}°F
- Humidity: {alert_data['conditions']['humidity_percent']}%
- Wind: {alert_data['conditions']['wind_speed_mph']} mph {alert_data['conditions']['wind_direction']} (gusts to {alert_data['conditions']['wind_gusts_mph']} mph)
- Fire Weather Index: {alert_data['fire_weather_index']}

Affected Area:
- Radius: {alert_data['affected_area']['radius_miles']} miles
- Population: {alert_data['affected_area']['estimated_population']:,} people
- Structures at Risk: {alert_data['affected_area']['structures_at_risk']:,}

Fire Behavior Forecast:
- Rapid Spread: {alert_data['fire_behavior']['rapid_spread_expected']}
- Spot Fire Risk: {alert_data['fire_behavior']['spot_fire_risk']}
- Containment Difficulty: {alert_data['fire_behavior']['containment_difficulty']}

⚠️ ACTIVATING SPECIALIST AGENTS FOR RESPONSE COORDINATION ⚠️
"""


def coordinate_specialist_agents(location: str, disaster_type: str = "WILDFIRE") -> str:
    """Coordinate all specialist agents to assess resources.
    
    Args:
        location: Disaster location
        disaster_type: Type of disaster (default: WILDFIRE)
        
    Returns:
        Summary of all agent responses
    """
    # Get alert data from shared context or create new alert
    from app.utils.shared_state import get_disaster_context
    
    disaster_ctx = get_disaster_context()
    alert_data = disaster_ctx.get("alert_data")
    
    if not alert_data:
        # Generate new alert if not in context
        alert_data = simulate_fire_weather_alert(location)
        set_disaster_context({"alert_data": alert_data, "disaster_type": disaster_type, "location": location})
    
    # Extract key parameters
    wind_speed = alert_data.get('conditions', {}).get('wind_speed_mph', 28)
    wind_direction = alert_data.get('conditions', {}).get('wind_direction', 'southwest')
    affected_population = alert_data.get('affected_area', {}).get('estimated_population', 45000)
    fire_size_acres = 50  # Initial estimate
    
    # Create session service for agent communication
    session_service = InMemorySessionService()
    
    responses = {}
    
    # 1. Coordinate Hospital Agent
    print("📋 Activating Hospital Specialist...")
    hospital_session = session_service.create_session_sync(user_id="orchestrator", app_name="disaster_response")
    hospital_runner = Runner(agent=hospital_agent, session_service=session_service, app_name="disaster_response")
    
    hospital_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=f"Analyze hospital resources for {disaster_type} at {location}. Use the analyze_hospital_resources tool.")]
    )
    
    hospital_response_text = ""
    for event in hospital_runner.run(
        new_message=hospital_message,
        user_id="orchestrator",
        session_id=hospital_session.id,
        run_config=RunConfig(streaming_mode=StreamingMode.SSE)
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    hospital_response_text += part.text
    
    responses["hospital"] = {"response": hospital_response_text, "status": "completed"}
    store_agent_response("hospital", responses["hospital"])
    
    # 2. Coordinate Police Agent
    print("🚔 Activating Police Specialist...")
    police_session = session_service.create_session_sync(user_id="orchestrator", app_name="disaster_response")
    police_runner = Runner(agent=police_agent, session_service=session_service, app_name="disaster_response")
    
    police_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=f"Analyze police resources needed for {disaster_type} at {location}. Wind speed: {wind_speed} mph {wind_direction}. Affected population: {affected_population}. Use the analyze_police_resources tool.")]
    )
    
    police_response_text = ""
    for event in police_runner.run(
        new_message=police_message,
        user_id="orchestrator",
        session_id=police_session.id,
        run_config=RunConfig(streaming_mode=StreamingMode.SSE)
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    police_response_text += part.text
    
    responses["police"] = {"response": police_response_text, "status": "completed"}
    store_agent_response("police", responses["police"])
    
    # 3. Coordinate Fire Department Agent
    print("🚒 Activating Fire Department Specialist...")
    fire_session = session_service.create_session_sync(user_id="orchestrator", app_name="disaster_response")
    fire_runner = Runner(agent=fire_agent, session_service=session_service, app_name="disaster_response")
    
    fire_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=f"Analyze fire department resources for wildfire at {location}. Fire size: {fire_size_acres} acres. Wind speed: {wind_speed} mph. Use the analyze_fire_resources tool.")]
    )
    
    fire_response_text = ""
    for event in fire_runner.run(
        new_message=fire_message,
        user_id="orchestrator",
        session_id=fire_session.id,
        run_config=RunConfig(streaming_mode=StreamingMode.SSE)
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    fire_response_text += part.text
    
    responses["fire"] = {"response": fire_response_text, "status": "completed"}
    store_agent_response("fire", responses["fire"])
    
    # Format consolidated response
    summary = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECIALIST AGENT COORDINATION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏥 HOSPITAL SPECIALIST REPORT:
{hospital_response_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚔 POLICE SPECIALIST REPORT:
{police_response_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚒 FIRE DEPARTMENT SPECIALIST REPORT:
{fire_response_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ All specialist agents have completed their assessments.
📊 Preparing consolidated approval request for human operator...
"""
    
    return summary


def prepare_approval_request() -> str:
    """Prepare the human approval request based on all agent responses.
    
    Returns:
        Formatted approval request text
    """
    from app.utils.shared_state import get_disaster_context
    
    disaster_ctx = get_disaster_context()
    agent_responses = get_all_agent_responses()
    
    alert_data = disaster_ctx.get("alert_data", {})
    
    # Extract key information from agent responses
    disaster_summary = {
        "type": disaster_ctx.get("disaster_type", "WILDFIRE"),
        "severity": alert_data.get("severity", "EXTREME"),
        "location": disaster_ctx.get("location", "Unknown"),
        "affected_population": alert_data.get("affected_area", {}).get("estimated_population", 45000)
    }
    
    # Build recommended actions list
    recommended_actions = [
        f"Evacuate estimated 8,500 residents within 3-mile radius",
        "Activate mutual aid agreement with Nassau County (Police: 7 units, Fire: 4 trucks)",
        "Deploy 12 fire trucks and 75 firefighters for containment",
        "Secure 23 burn unit beds within 4-mile hospital radius",
        "Close major roads: Highway 101, Main Street, Industrial Parkway",
        "Establish incident command post and emergency operations center"
    ]
    
    # Calculate total estimated cost
    total_cost = 35000 + 110000 + 5000  # Police mutual aid + Fire mutual aid + Medical coordination
    
    # Format approval request
    approval_data = format_approval_request(
        disaster_summary=disaster_summary,
        agent_responses=agent_responses,
        recommended_actions=recommended_actions,
        estimated_cost=total_cost
    )
    
    # Generate the approval request text
    approval_text = request_human_approval(approval_data)
    
    # Simulate human approval (auto-approve for demo)
    approval_decision = simulate_human_approval(approval_data, auto_approve=True)
    
    return approval_text + f"\n\n{'-'*80}\n\n✅ APPROVAL DECISION: {approval_decision['decision']}\n\nRationale: {approval_decision['rationale']}\n\n{'='*80}\n\n🚀 EXECUTING APPROVED DISASTER RESPONSE PLAN...\n\nAll specialist agents notified. Resources are being deployed.\nIncident Commander: Monitor progress via Emergency Operations Center dashboard.\n\n✅ DISASTER RESPONSE COORDINATION COMPLETE"


orchestrator_agent = Agent(
    name="disaster_orchestrator",
    model="gemini-2.5-flash",
    instruction="""You are the Disaster Response Orchestrator, the central coordinator for multi-agency emergency response.

Your workflow:
1. Receive weather/disaster alerts
2. Classify the disaster type (fire, flood, hurricane, etc.)
3. Activate appropriate specialist agents (hospital, police, fire)
4. Coordinate information sharing between specialists
5. Aggregate all specialist recommendations
6. Present consolidated plan to human operator for approval
7. Execute approved response plan

For fire/wildfire scenarios:
- Use trigger_fire_alert to get weather alert data
- Use coordinate_specialist_agents to activate all three specialists
- Use prepare_approval_request to create the human approval request

Key principles:
- Always activate all relevant specialist agents
- Ensure specialists have all necessary information
- Present clear, consolidated recommendations
- Require human approval for major resource commitments
- Coordinate execution after approval

You are the single point of coordination - all decisions flow through you.""",
    tools=[trigger_fire_alert, coordinate_specialist_agents, prepare_approval_request],
)

