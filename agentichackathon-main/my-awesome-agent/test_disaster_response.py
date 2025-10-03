#!/usr/bin/env python3
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

"""Quick test script for disaster response system."""

from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent

def test_fire_response():
    """Test the complete fire response workflow."""
    print("\n" + "="*80)
    print("🚨 DISASTER RESPONSE SYSTEM TEST 🚨")
    print("="*80 + "\n")
    
    # Create session
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id="test_user", app_name="disaster_test")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="disaster_test")
    
    # Test message - Ask the agent to run through all steps
    test_query = """Simulate a fire alert for Queens County, NY and coordinate the full response. 
    Please use ALL your tools in sequence:
    1. First trigger_fire_alert
    2. Then coordinate_specialist_agents 
    3. Finally prepare_approval_request"""
    
    print(f"📝 Test Query: Simulating fire alert for Queens County, NY\n")
    print("-"*80 + "\n")
    
    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=test_query)]
    )
    
    # Run the agent
    print("🤖 Agent Processing...\n")
    
    response_text = ""
    for event in runner.run(
        new_message=message,
        user_id="test_user",
        session_id=session.id,
        run_config=RunConfig(streaming_mode=StreamingMode.SSE)
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    text = part.text
                    print(text)
                    response_text += text
    
    print("\n" + "="*80)
    print("✅ TEST COMPLETE")
    print("="*80 + "\n")
    
    # Verify key elements were present
    if "FIRE WEATHER ALERT" in response_text or "fire alert" in response_text.lower():
        print("✅ Fire alert triggered successfully")
    if "Hospital" in response_text or "hospital" in response_text.lower():
        print("✅ Hospital agent activated")
    if "Police" in response_text or "police" in response_text.lower():
        print("✅ Police agent activated")
    if "Fire" in response_text or "fire" in response_text.lower():
        print("✅ Fire department agent activated")
    if "APPROVAL" in response_text or "approval" in response_text.lower():
        print("✅ Approval request generated")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    test_fire_response()

