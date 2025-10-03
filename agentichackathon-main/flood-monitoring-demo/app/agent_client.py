"""Client to interact with AI Agent from the flood monitoring system."""

import sys
import os

# Add the my-awesome-agent to the path so we can import it
agent_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "my-awesome-agent")
sys.path.insert(0, agent_path)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai import types
import json

# Import the flood orchestrator agent
from app.agents.flood_orchestrator import flood_orchestrator_agent


def invoke_flood_orchestrator(weather_alert_json: dict) -> dict:
    """
    Invoke the flood orchestrator AI agent with weather alert data.
    
    Args:
        weather_alert_json: Weather alert data dictionary
        
    Returns:
        Dictionary with agent response and metadata
    """
    try:
        # Create session service
        session_service = InMemorySessionService()
        session = session_service.create_session_sync(
            user_id="flood_monitoring_system",
            app_name="flood_monitoring"
        )
        
        # Create runner for the agent
        runner = Runner(
            agent=flood_orchestrator_agent,
            session_service=session_service,
            app_name="flood_monitoring"
        )
        
        # Format the message to the agent with the weather alert JSON
        message_text = f"""I have received a weather alert from our monitoring system. 
Please analyze this alert and provide your assessment.

Weather Alert Data:
{json.dumps(weather_alert_json, indent=2)}

Please use your tools to:
1. Process this weather alert
2. Analyze the flood risk
3. Provide recommendations for next steps
"""
        
        message = types.Content(
            role="user",
            parts=[types.Part.from_text(text=message_text)]
        )
        
        # Run the agent and collect response
        full_response = ""
        for event in runner.run(
            new_message=message,
            user_id="flood_monitoring_system",
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE)
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        full_response += part.text
        
        return {
            "status": "success",
            "agent_response": full_response,
            "alert_id": weather_alert_json.get("alert_id", "unknown"),
            "session_id": session.id
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "alert_id": weather_alert_json.get("alert_id", "unknown")
        }


def test_agent():
    """Test the agent invocation with sample data."""
    sample_alert = {
        "alert_id": "WX-FLOOD-TEST-001",
        "alert_type": "FLOOD_WATCH",
        "timestamp": "2025-10-03T10:00:00",
        "location": {
            "region": "Northern Valley",
            "coordinates": {"lat": 42.3601, "lon": -71.0589}
        },
        "precipitation": {
            "probability_percent": 75,
            "expected_amount_mm": 95,
            "timeframe_hours": 2
        },
        "severity": {
            "level": 3,
            "description": "Heavy rainfall expected with moderate flood risk"
        },
        "message": "Expected rain in 2 hours. Monitor river levels."
    }
    
    print("🧪 Testing agent invocation...")
    result = invoke_flood_orchestrator(sample_alert)
    
    if result["status"] == "success":
        print("\n✅ Agent Response:")
        print(result["agent_response"])
    else:
        print("\n❌ Error:")
        print(result["error"])
    
    return result


if __name__ == "__main__":
    test_agent()

