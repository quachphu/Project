#!/usr/bin/env python3
"""Quick test to verify AI agent is working."""

import requests
import json

# Test weather alert
alert = {
    "alert_id": "WX-FLOOD-TEST-123",
    "alert_type": "FLOOD_WATCH",
    "timestamp": "2025-10-03T10:00:00",
    "valid_until": "2025-10-03T16:00:00",
    "issued_by": "National Weather Service",
    "location": {
        "region": "Northern Valley",
        "coordinates": {"lat": 42.3601, "lon": -71.0589},
        "affected_areas": ["River Basin District"]
    },
    "precipitation": {
        "probability_percent": 75,
        "expected_amount_mm": 95,
        "timeframe_hours": 2,
        "intensity": "heavy"
    },
    "severity": {
        "level": 3,
        "scale": "1-5 (5 being most severe)",
        "description": "Heavy rainfall expected with moderate flood risk"
    },
    "forecast": {
        "temperature_c": 18,
        "wind_speed_kmh": 25,
        "wind_direction": "northeast",
        "atmospheric_pressure_hpa": 1008
    },
    "message": "Expected rain in 2 hours. Monitor river levels.",
    "recommendations": ["Monitor local river gauge levels"]
}

print("🧪 Testing AI Agent Integration...")
print("=" * 80)

try:
    response = requests.post(
        "http://localhost:8000/api/alerts/weather",
        json=alert,
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Backend Response Status: {result['status']}")
        print(f"📊 Orchestrator Status: {result['orchestrator_status']}")
        print(f"🤖 Agent Available: {result['agent_available']}")
        
        if result.get('agent_response'):
            print("\n" + "=" * 80)
            print("🤖 AI AGENT RESPONSE:")
            print("=" * 80)
            print(result['agent_response'])
            print("=" * 80)
            print("\n✅ SUCCESS! AI Agent is working!")
        else:
            print("\n⚠️  No agent response - agent may not be available")
            print("Check backend logs for errors")
    else:
        print(f"\n❌ Error: HTTP {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure backend is running: python app/backend.py")

print("\n" + "=" * 80)

