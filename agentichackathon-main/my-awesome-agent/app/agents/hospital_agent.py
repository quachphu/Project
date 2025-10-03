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

"""Hospital resource specialist agent."""

from google.adk.agents import Agent

from app.tools.hospital_tools import (
    check_burn_unit_capacity,
    check_hospital_beds,
    expand_search_radius,
    get_ambulance_availability,
)


def analyze_hospital_resources(location: str, disaster_type: str) -> str:
    """Analyze hospital resources for disaster response.
    
    Args:
        location: Location of the disaster
        disaster_type: Type of disaster (e.g., 'WILDFIRE')
        
    Returns:
        Analysis of hospital resource availability and recommendations
    """
    # Start with 2-mile radius
    current_radius = 2
    
    # Check burn unit capacity for wildfires
    if disaster_type == "WILDFIRE":
        burn_capacity = check_burn_unit_capacity(location, required_beds=20)
        
        if not burn_capacity["sufficient"]:
            # Expand to 4 miles
            current_radius = expand_search_radius(current_radius)
            expanded_data = check_hospital_beds(location, current_radius)
            
            result = {
                "action": "hospital_resource_analysis",
                "location": location,
                "disaster_type": disaster_type,
                "initial_search_radius_miles": 2,
                "initial_burn_beds": burn_capacity["available_burn_beds_2mi"],
                "required_burn_beds": burn_capacity["required_burn_beds"],
                "expanded_to_radius_miles": current_radius,
                "expanded_burn_beds": expanded_data["burn_unit_beds"],
                "total_beds_available": expanded_data["total_beds_available"],
                "hospitals_in_network": expanded_data["hospitals_found"],
                "ambulances_available": expanded_data["ambulances_available"],
                "status": "ADEQUATE" if expanded_data["burn_unit_beds"] >= 20 else "INSUFFICIENT",
                "recommendation": f"Secure {expanded_data['burn_unit_beds']} burn unit beds across {expanded_data['hospitals_found']} hospitals within {current_radius}-mile radius"
            }
        else:
            initial_data = check_hospital_beds(location, current_radius)
            result = {
                "action": "hospital_resource_analysis",
                "location": location,
                "disaster_type": disaster_type,
                "search_radius_miles": current_radius,
                "burn_beds_available": burn_capacity["available_burn_beds_2mi"],
                "total_beds_available": initial_data["total_beds_available"],
                "hospitals_in_network": initial_data["hospitals_found"],
                "ambulances_available": initial_data["ambulances_available"],
                "status": "ADEQUATE",
                "recommendation": f"Sufficient capacity within {current_radius}-mile radius"
            }
    else:
        # For other disasters, check general capacity
        hospital_data = check_hospital_beds(location, current_radius)
        result = {
            "action": "hospital_resource_analysis",
            "location": location,
            "disaster_type": disaster_type,
            "search_radius_miles": current_radius,
            "total_beds_available": hospital_data["total_beds_available"],
            "trauma_beds": hospital_data["trauma_beds"],
            "icu_beds": hospital_data["icu_beds"],
            "hospitals_in_network": hospital_data["hospitals_found"],
            "ambulances_available": hospital_data["ambulances_available"],
            "status": "ADEQUATE",
            "recommendation": hospital_data["recommendation"]
        }
    
    # Get ambulance availability
    ambulance_data = get_ambulance_availability(location, current_radius)
    result["ambulance_response_time_minutes"] = ambulance_data["response_time_avg_minutes"]
    
    # Format as string for the agent
    return f"""Hospital Resource Analysis Complete:
- Location: {location}
- Disaster Type: {disaster_type}
- Search Radius: {result.get('expanded_to_radius_miles', result.get('search_radius_miles'))} miles
- Burn Unit Beds Available: {result.get('expanded_burn_beds', result.get('burn_beds_available', 'N/A'))}
- Total Beds Available: {result['total_beds_available']}
- Hospitals in Network: {result['hospitals_in_network']}
- Ambulances Available: {result['ambulances_available']}
- Status: {result['status']}
- Recommendation: {result['recommendation']}
"""


hospital_agent = Agent(
    name="hospital_specialist",
    model="gemini-2.5-flash",
    instruction="""You are a hospital resource management specialist for emergency disaster response.

Your responsibilities:
1. Assess hospital bed availability (especially burn units for wildfires)
2. Start with 2-mile search radius and expand to 4 miles if needed
3. Check ambulance availability and response times
4. Provide clear recommendations for medical resource allocation

For wildfire scenarios:
- Prioritize burn unit bed availability
- Aim for at least 20 burn beds to handle severe cases
- Expand search radius if local capacity is insufficient

Always provide specific numbers and actionable recommendations.""",
    tools=[analyze_hospital_resources, check_hospital_beds, check_burn_unit_capacity, get_ambulance_availability],
)

