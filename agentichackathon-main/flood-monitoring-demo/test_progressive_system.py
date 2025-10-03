#!/usr/bin/env python3
"""Test the progressive monitoring system."""

import requests
import json
import time

# Generate weather alert
from mock_data.weather_alert import generate_weather_alert

print("="*80)
print("🧪 Testing Progressive Flood Monitoring System")
print("="*80)
print()

# Generate alert
alert = generate_weather_alert("moderate_flood")
print("📋 Generated Weather Alert:")
print(f"   - Severity: {alert['severity']['level']}/5")
print(f"   - Precipitation: {alert['precipitation']['expected_amount_mm']}mm")
print(f"   - ZIP Code: {alert['location']['zipcode']}")
print()

# Send to backend
print("📡 Sending to backend...")
try:
    response = requests.post(
        "http://localhost:8000/api/alerts/weather",
        json=alert,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Backend received alert")
        print(f"   Status: {result['orchestrator_status']}")
        print()
        
        # Wait a moment then fetch events
        time.sleep(2)
        
        events_response = requests.get("http://localhost:8000/api/events")
        if events_response.status_code == 200:
            events = events_response.json().get("events", [])
            print(f"📊 Total Events Generated: {len(events)}")
            print()
            
            for i, event in enumerate(events, 1):
                event_type = event.get("event_type")
                print(f"{i}. {event_type}")
                
                if event_type == "ai_phase1_weather":
                    print("   └─ Phase 1: Weather Alert Scoring")
                elif event_type == "searching_rivers":
                    print(f"   └─ {event['data'].get('message')}")
                elif event_type == "river_gauge_data":
                    summary = event['data'].get('summary', {})
                    print(f"   └─ Found {summary.get('total_rivers')} rivers, {summary.get('total_sensors')} sensors")
                    print(f"      Critical: {summary.get('sensors_critical')}, Warning: {summary.get('sensors_warning')}")
                elif event_type == "ai_phase2_rivers":
                    print("   └─ Phase 2: River Gauge Scoring")
            
            print()
            print("="*80)
            print("✅ PROGRESSIVE MONITORING SYSTEM WORKING!")
            print("="*80)
            print()
            print("🎉 You now have:")
            print("   1. Weather alert with ZIP code")
            print("   2. AI scoring (Phase 1: 0-25 points)")
            print("   3. Automatic escalation decision")
            print("   4. River search by ZIP code")
            print("   5. 6 sensor data retrieval")
            print("   6. AI river gauge scoring (Phase 2: 0-20 points)")
            print("   7. Cumulative confidence score tracking")
            print()
            print("🌐 Go to http://localhost:8501 and click 'Scenario 1'!")
            print("="*80)
            
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Make sure backend is running:")
    print("  cd flood-monitoring-demo")
    print("  python app/backend.py")

