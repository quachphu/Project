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

"""Fire department resource specialist agent."""

from google.adk.agents import Agent

from app.tools.fire_tools import (
    assess_water_supply,
    calculate_containment_resources,
    check_firefighter_availability,
    get_fire_status,
    get_fire_trucks_available,
    request_fire_mutual_aid,
)


def analyze_fire_resources(location: str, fire_size_acres: int, wind_speed_mph: int) -> str:
    """Analyze fire department resources needed for response.
    
    Args:
        location: Fire location
        fire_size_acres: Estimated fire size in acres
        wind_speed_mph: Current wind speed
        
    Returns:
        Analysis of fire department resource needs
    """
    # Get current fire status
    fire_status = get_fire_status(location)
    
    # Check available resources
    trucks_data = get_fire_trucks_available(location)
    firefighters_data = check_firefighter_availability(location)
    water_data = assess_water_supply(location)
    
    # Calculate required resources
    requirements = calculate_containment_resources(fire_size_acres, wind_speed_mph)
    
    # Determine deficits
    truck_deficit = max(0, requirements["fire_trucks_required"] - trucks_data["total_apparatus"])
    firefighter_deficit = max(0, requirements["firefighters_required"] - firefighters_data["total_available"])
    
    mutual_aid_needed = truck_deficit > 0 or firefighter_deficit > 0
    mutual_aid_data = None
    
    if mutual_aid_needed:
        mutual_aid_data = request_fire_mutual_aid(location, truck_deficit, firefighter_deficit)
    
    result = {
        "action": "fire_resource_analysis",
        "location": location,
        "fire_status": fire_status["current_status"],
        "fire_size_acres": fire_size_acres,
        "containment_percent": fire_status["containment_percent"],
        "structures_threatened": fire_status["structures_threatened"],
        "trucks_available": trucks_data["total_apparatus"],
        "trucks_required": requirements["fire_trucks_required"],
        "truck_deficit": truck_deficit,
        "firefighters_available": firefighters_data["total_available"],
        "firefighters_required": requirements["firefighters_required"],
        "firefighter_deficit": firefighter_deficit,
        "water_supply_adequate": water_data["supply_adequate"],
        "estimated_containment_hours": requirements["estimated_containment_hours"],
        "mutual_aid_needed": mutual_aid_needed,
        "status": "MUTUAL_AID_REQUIRED" if mutual_aid_needed else "SUFFICIENT"
    }
    
    if mutual_aid_data:
        result["mutual_aid_cost"] = mutual_aid_data["estimated_cost"]
        result["mutual_aid_response_time"] = mutual_aid_data["estimated_response_time_minutes"]
        result["mutual_aid"] = mutual_aid_data
    
    return f"""Fire Department Resource Analysis Complete:
- Location: {location}
- Fire Status: {fire_status['current_status']}
- Fire Size: {fire_size_acres} acres
- Structures Threatened: {fire_status['structures_threatened']}
- Trucks Available: {trucks_data['total_apparatus']} (Need: {requirements['fire_trucks_required']})
- Firefighters Available: {firefighters_data['total_available']} (Need: {requirements['firefighters_required']})
- Water Supply: {'ADEQUATE' if water_data['supply_adequate'] else 'INADEQUATE - ' + water_data['recommendation']}
- Estimated Containment: {requirements['estimated_containment_hours']} hours
- Mutual Aid Needed: {'YES - ' + str(truck_deficit) + ' trucks, ' + str(firefighter_deficit) + ' firefighters' if mutual_aid_needed else 'NO'}
- Status: {result['status']}
- Recommendation: {'Request mutual aid from Nassau County and surrounding areas' if mutual_aid_needed else 'Proceed with local resources'}
"""


fire_agent = Agent(
    name="fire_specialist",
    model="gemini-2.5-flash",
    instruction="""You are a fire department resource coordinator specialist for wildfire response.

Your responsibilities:
1. Assess current fire status and behavior
2. Calculate fire trucks and firefighter requirements
3. Evaluate water supply infrastructure
4. Estimate containment timeline
5. Request mutual aid if resources are insufficient

Key considerations:
- Typical ratio: 6 firefighters per fire truck
- High wind speeds dramatically increase resource needs
- Water supply is critical - may need tanker shuttles
- Mutual aid from neighboring departments takes 30-60 minutes to deploy
- Cost: ~$15,000 per truck + $500 per firefighter

Always provide specific resource counts, timelines, and actionable recommendations.""",
    tools=[
        analyze_fire_resources,
        get_fire_trucks_available,
        check_firefighter_availability,
        assess_water_supply,
        calculate_containment_resources,
        get_fire_status,
        request_fire_mutual_aid,
    ],
)

