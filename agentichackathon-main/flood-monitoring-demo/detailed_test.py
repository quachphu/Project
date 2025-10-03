#!/usr/bin/env python
"""Detailed test script to debug Scenario 1 execution."""

import requests
import json
import time
import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
from mock_data.weather_alert import generate_weather_alert

BACKEND_URL = "http://localhost:8000"

def print_section(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_json(data, indent=2):
    """Pretty print JSON data."""
    print(json.dumps(data, indent=indent))

def main():
    print_section("🧪 DETAILED SCENARIO 1 TEST")
    
    # Step 1: Clear events
    print("\n[STEP 1] Clearing old events...")
    try:
        resp = requests.delete(f"{BACKEND_URL}/api/events", timeout=5)
        print(f"✅ Events cleared: {resp.status_code}")
    except Exception as e:
        print(f"❌ Error clearing events: {e}")
        return
    
    # Step 2: Generate weather alert
    print_section("STEP 2: GENERATE WEATHER ALERT")
    alert = generate_weather_alert("moderate_flood")
    
    print("\n📋 Alert Data:")
    print(f"  Alert ID: {alert['alert_id']}")
    print(f"  Severity: {alert['severity']['level']}/5")
    print(f"  Precipitation: {alert['precipitation']['expected_amount_mm']}mm")
    print(f"  Probability: {alert['precipitation']['probability_percent']}%")
    print(f"  Location: {alert['location']['region']}")
    print(f"  ZIP Code: {alert['location'].get('zipcode', 'MISSING!')}")
    
    print("\n📄 Full Alert JSON:")
    print_json(alert)
    
    # Step 3: Send to backend
    print_section("STEP 3: SEND TO BACKEND")
    print(f"\nPOST {BACKEND_URL}/api/alerts/weather")
    print("Waiting for response (timeout: 60s)...\n")
    
    start_time = time.time()
    try:
        resp = requests.post(
            f"{BACKEND_URL}/api/alerts/weather",
            json=alert,
            timeout=60
        )
        elapsed = time.time() - start_time
        
        print(f"✅ Response received in {elapsed:.1f}s")
        print(f"   Status Code: {resp.status_code}")
        print(f"   Response: {resp.json()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 4: Wait for processing
    print("\n⏳ Waiting 3 seconds for backend processing...")
    time.sleep(3)
    
    # Step 5: Fetch events
    print_section("STEP 4: FETCH EVENTS FROM BACKEND")
    try:
        resp = requests.get(f"{BACKEND_URL}/api/events", timeout=5)
        events = resp.json()
        
        print(f"\n📊 Total Events: {len(events)}")
        
        if not events:
            print("\n❌ NO EVENTS FOUND!")
            print("   This means the backend didn't create any events.")
            return
        
        # Step 6: Analyze each event
        print_section("STEP 5: ANALYZE EVENTS")
        
        for idx, event in enumerate(events, 1):
            print(f"\n{'─' * 80}")
            print(f"EVENT #{idx}: {event.get('event_type', 'UNKNOWN')}")
            print(f"{'─' * 80}")
            
            event_type = event.get('event_type', '')
            event_data = event.get('data', {})
            timestamp = event.get('timestamp', 'N/A')
            
            print(f"Timestamp: {timestamp}")
            print(f"Event Type: {event_type}")
            
            # Weather Alert
            if event_type == 'weather_alert':
                print("\n📡 WEATHER ALERT EVENT:")
                alert_data = event_data
                print(f"  Alert ID: {alert_data.get('alert_id', 'N/A')}")
                print(f"  Severity: {alert_data.get('severity', {}).get('level', 'N/A')}/5")
                print(f"  Precipitation: {alert_data.get('precipitation', {}).get('expected_amount_mm', 'N/A')}mm")
                print(f"  ZIP Code: {alert_data.get('location', {}).get('zipcode', 'MISSING!')}")
            
            # AI Phase 1
            elif event_type == 'ai_phase1_weather':
                print("\n🤖 AI PHASE 1 - WEATHER ANALYSIS:")
                agent_response = event_data.get('agent_response', 'NO RESPONSE')
                
                # Extract score
                import re
                match = re.search(r'(\d+)/25', agent_response)
                if match:
                    score = match.group(1)
                    print(f"  ⭐ SCORE: {score}/25")
                else:
                    print("  ⚠️ NO SCORE FOUND IN RESPONSE")
                
                # Check for escalation
                escalation_keywords = ['escalat', 'threshold', 'recommend', 'phase 2']
                found_keywords = [kw for kw in escalation_keywords if kw.lower() in agent_response.lower()]
                
                if found_keywords:
                    print(f"  ✅ ESCALATION DETECTED (keywords: {found_keywords})")
                else:
                    print("  ❌ NO ESCALATION DETECTED")
                
                print("\n  📄 Full AI Response:")
                print("  " + "─" * 76)
                for line in agent_response.split('\n'):
                    print(f"  {line}")
                print("  " + "─" * 76)
            
            # Searching Rivers
            elif event_type == 'searching_rivers':
                print("\n🔍 SEARCHING RIVERS EVENT:")
                zipcode = event_data.get('zipcode', 'N/A')
                print(f"  ZIP Code: {zipcode}")
            
            # River Gauge Data
            elif event_type == 'river_gauge_data':
                print("\n🌊 RIVER GAUGE DATA EVENT:")
                rivers = event_data.get('rivers', [])
                print(f"  Rivers Found: {len(rivers)}")
                
                for river in rivers:
                    river_name = river.get('river_name', 'Unknown')
                    sensors = river.get('sensors', [])
                    print(f"\n  📍 {river_name} ({len(sensors)} sensors):")
                    
                    for sensor in sensors:
                        status = sensor.get('status', 'unknown')
                        trend = sensor.get('trend', 'unknown')
                        level = sensor.get('water_level_m', 0)
                        print(f"     • {sensor.get('sensor_name', 'N/A')}: {status.upper()} | {trend} | {level}m")
            
            # AI Phase 2
            elif event_type == 'ai_phase2_rivers':
                print("\n🤖 AI PHASE 2 - RIVER GAUGE ANALYSIS:")
                agent_response = event_data.get('agent_response', 'NO RESPONSE')
                
                # Extract scores
                import re
                match = re.search(r'(\d+)/20', agent_response)
                if match:
                    score = match.group(1)
                    print(f"  ⭐ RIVER SCORE: {score}/20")
                
                match_cumulative = re.search(r'(\d+)/100', agent_response)
                if match_cumulative:
                    cumulative = match_cumulative.group(1)
                    print(f"  ⭐ CUMULATIVE: {cumulative}/100")
                
                print("\n  📄 Full AI Response:")
                print("  " + "─" * 76)
                for line in agent_response.split('\n'):
                    print(f"  {line}")
                print("  " + "─" * 76)
        
        # Summary
        print_section("📊 SUMMARY")
        
        event_types = [e.get('event_type', 'unknown') for e in events]
        print(f"\nEvent Types Generated:")
        for et in event_types:
            print(f"  ✓ {et}")
        
        # Extract final scores
        phase1_score = None
        phase2_score = None
        cumulative_score = None
        
        import re
        for event in events:
            if event.get('event_type') == 'ai_phase1_weather':
                response = event.get('data', {}).get('agent_response', '')
                match = re.search(r'(\d+)/25', response)
                if match:
                    phase1_score = int(match.group(1))
            
            elif event.get('event_type') == 'ai_phase2_rivers':
                response = event.get('data', {}).get('agent_response', '')
                match = re.search(r'(\d+)/20', response)
                if match:
                    phase2_score = int(match.group(1))
                match = re.search(r'(\d+)/100', response)
                if match:
                    cumulative_score = int(match.group(1))
        
        print(f"\n🎯 FINAL SCORES:")
        print(f"  Phase 1 (Weather): {phase1_score if phase1_score else 'NOT FOUND'}/25")
        print(f"  Phase 2 (Rivers):  {phase2_score if phase2_score else 'NOT FOUND'}/20")
        print(f"  Cumulative Total:  {cumulative_score if cumulative_score else 'NOT FOUND'}/100")
        
        # Validation
        print(f"\n✅ VALIDATION:")
        if 'weather_alert' in event_types:
            print("  ✓ Weather alert received")
        else:
            print("  ✗ Weather alert MISSING")
        
        if 'ai_phase1_weather' in event_types:
            print("  ✓ AI Phase 1 completed")
            if phase1_score and phase1_score >= 20:
                print(f"  ✓ Score ({phase1_score}/25) should trigger escalation")
            else:
                print(f"  ✗ Score ({phase1_score}/25) below escalation threshold")
        else:
            print("  ✗ AI Phase 1 MISSING")
        
        if 'searching_rivers' in event_types:
            print("  ✓ River search initiated")
        else:
            print("  ✗ River search MISSING (Phase 2 not triggered)")
        
        if 'river_gauge_data' in event_types:
            print("  ✓ River gauge data retrieved")
        else:
            print("  ✗ River gauge data MISSING")
        
        if 'ai_phase2_rivers' in event_types:
            print("  ✓ AI Phase 2 completed")
        else:
            print("  ✗ AI Phase 2 MISSING")
        
        expected_events = 5
        if len(events) == expected_events:
            print(f"\n🎉 SUCCESS! All {expected_events} events generated correctly!")
        else:
            print(f"\n⚠️ WARNING: Expected {expected_events} events, got {len(events)}")
        
    except Exception as e:
        print(f"\n❌ Error fetching events: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    print("\n" + "=" * 80)
    print("  TEST COMPLETE")
    print("=" * 80 + "\n")

