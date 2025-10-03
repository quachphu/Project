#!/usr/bin/env python3
"""Test script to verify AI agent integration with flood monitoring system."""

import sys
import os

# Add my-awesome-agent to path
agent_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "my-awesome-agent")
sys.path.insert(0, agent_path)

from app.agent_client import test_agent

if __name__ == "__main__":
    print("="*80)
    print("🧪 Testing AI Agent Integration")
    print("="*80)
    print("")
    
    result = test_agent()
    
    print("")
    print("="*80)
    if result["status"] == "success":
        print("✅ Integration test PASSED")
        print("\nThe AI agent is working correctly!")
        print("\nNext steps:")
        print("1. Start the backend: python app/backend.py")
        print("2. Start the frontend: streamlit run app/frontend.py")
        print("3. Click 'Scenario 1' button to see the agent in action")
    else:
        print("❌ Integration test FAILED")
        print(f"\nError: {result.get('error')}")
    print("="*80)

