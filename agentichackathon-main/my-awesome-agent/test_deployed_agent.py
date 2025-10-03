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

"""Test the deployed disaster response agent on Vertex AI."""

import time
from datetime import datetime

import vertexai
from vertexai import Client

# Your deployment details
PROJECT_ID = "gen-lang-client-0532474448"
LOCATION = "us-central1"
AGENT_ENGINE_ID = "projects/872130774020/locations/us-central1/reasoningEngines/8735949736168652800"

def main():
    print("\n" + "="*80)
    print("🚀 TESTING DEPLOYED DISASTER RESPONSE AGENT")
    print("="*80)
    
    print(f"\n📋 Deployment Details:")
    print(f"   Project: {PROJECT_ID}")
    print(f"   Location: {LOCATION}")
    print(f"   Agent ID: {AGENT_ENGINE_ID.split('/')[-1]}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize Vertex AI client
        print("\n🔌 Connecting to Vertex AI...")
        client = Client(
            project=PROJECT_ID,
            location=LOCATION
        )
        
        # Get the deployed agent
        print("📡 Fetching deployed agent...")
        agent_engine = client.agent_engines.get(name=AGENT_ENGINE_ID)
        
        print(f"✅ Connected to agent: {agent_engine.api_resource.display_name}")
        print(f"   Resource Name: {agent_engine.api_resource.name}")
        
        # Test query
        test_query = "Simulate a fire alert for Queens County, NY and coordinate the full response"
        
        print("\n" + "-"*80)
        print("🚨 SENDING TEST QUERY:")
        print(f"   \"{test_query}\"")
        print("-"*80 + "\n")
        
        print("⏳ Waiting for response (this may take 20-30 seconds)...")
        start_time = time.time()
        
        # Query the deployed agent
        response = agent_engine.query(prompt=test_query)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✅ Response received in {duration:.2f} seconds")
        
        print("\n" + "="*80)
        print("📋 AGENT RESPONSE:")
        print("="*80)
        print(response)
        print("="*80)
        
        # Provide links to view observability
        print("\n" + "="*80)
        print("📊 VIEW OBSERVABILITY DATA:")
        print("="*80)
        
        print("\n🔍 Cloud Logging:")
        print(f"   https://console.cloud.google.com/logs/query?project={PROJECT_ID}")
        print("   Query to use:")
        print('   resource.type="aiplatform.googleapis.com/ReasoningEngine"')
        
        print("\n📈 Cloud Trace:")
        print(f"   https://console.cloud.google.com/traces/list?project={PROJECT_ID}")
        
        print("\n🎯 Agent Dashboard:")
        print(f"   https://console.cloud.google.com/vertex-ai/agents/locations/{LOCATION}/agent-engines/{AGENT_ENGINE_ID.split('/')[-1]}?project={PROJECT_ID}")
        
        print("\n💾 Cloud Storage (Logs):")
        print(f"   https://console.cloud.google.com/storage/browser?project={PROJECT_ID}")
        
        print("\n" + "="*80)
        print("✅ TEST COMPLETE!")
        print("="*80)
        
        print("\n💡 Next Steps:")
        print("   1. Check the Cloud Logging link above to see detailed logs")
        print("   2. Check Cloud Trace to see the execution timeline")
        print("   3. View the Agent Dashboard to see resource usage")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("   1. Verify agent is deployed: gcloud ai reasoning-engines list --location=us-central1")
        print("   2. Check your credentials: gcloud auth application-default login")
        print("   3. Verify project access: gcloud config get-value project")
        raise

if __name__ == "__main__":
    main()

