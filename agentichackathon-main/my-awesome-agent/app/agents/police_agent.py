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

"""Police resource specialist agent."""

from google.adk.agents import Agent

from app.tools.police_tools import (
    calculate_evacuation_radius,
    estimate_evacuation_time,
    get_police_units_available,
    identify_road_closures,
    request_mutual_aid,
)


def analyze_police_resources(
    location: str,
    disaster_type: str,
    wind_speed_mph: int,
    wind_direction: str,
    affected_population: int
) -> str:
    """Analyze police resources needed for disaster response.
    
    Args:
        location: Location of disaster
        disaster_type: Type of disaster
        wind_speed_mph: Wind speed
        wind_direction: Wind direction
        affected_population: Estimated affected population
        
    Returns:
        Analysis of police resource needs
    """
    # Calculate evacuation radius
    evac_data = calculate_evacuation_radius(location, wind_speed_mph, wind_direction)
    evac_radius = evac_data["recommended_radius_miles"]
    
    # Get available police units
    units_data = get_police_units_available(location)
    
    # Identify road closures needed
    road_data = identify_road_closures(location, evac_radius)
    
    # Calculate evacuation population (scaled by radius)
    evac_population = min(affected_population, int(affected_population * (evac_radius / 5)))
    
    # Estimate evacuation time
    time_data = estimate_evacuation_time(evac_population, units_data["patrol_units_available"])
    
    # Determine if mutual aid needed
    mutual_aid_needed = units_data["mutual_aid_needed"]
    mutual_aid_data = None
    
    if mutual_aid_needed:
        units_deficit = units_data["mutual_aid_units_required"]
        mutual_aid_data = request_mutual_aid(location, units_deficit)
    
    result = {
        "action": "police_resource_analysis",
        "location": location,
        "disaster_type": disaster_type,
        "evacuation_radius_miles": evac_radius,
        "evacuation_population": evac_population,
        "police_units_available": units_data["patrol_units_available"],
        "police_units_required": units_data["patrol_units_required_for_evacuation"],
        "mutual_aid_needed": mutual_aid_needed,
        "mutual_aid_units": units_data["mutual_aid_units_required"] if mutual_aid_needed else 0,
        "estimated_evacuation_time": time_data["estimated_time_display"],
        "roads_to_close": road_data["roads_to_close"],
        "road_closure_count": road_data["number_of_roads"],
        "status": "MUTUAL_AID_REQUIRED" if mutual_aid_needed else "SUFFICIENT"
    }
    
    if mutual_aid_data:
        result["mutual_aid_cost"] = mutual_aid_data["estimated_cost"]
        result["mutual_aid_response_time"] = mutual_aid_data["estimated_response_time_minutes"]
        result["mutual_aid"] = mutual_aid_data
    
    return f"""Police Resource Analysis Complete:
- Location: {location}
- Evacuation Radius: {evac_radius} miles
- Population to Evacuate: {evac_population:,} people
- Units Available: {units_data['patrol_units_available']} units
- Units Required: {units_data['patrol_units_required_for_evacuation']} units
- Mutual Aid Needed: {'YES - ' + str(units_data['mutual_aid_units_required']) + ' additional units' if mutual_aid_needed else 'NO'}
- Estimated Evacuation Time: {time_data['estimated_time_display']}
- Roads to Close: {', '.join(road_data['roads_to_close'])}
- Status: {result['status']}
- Recommendation: {'Request mutual aid from neighboring counties' if mutual_aid_needed else 'Proceed with local resources'}
"""


police_agent = Agent(
    name="police_specialist",
    model="gemini-2.5-flash",
    instruction="""You are a police resource coordination specialist for emergency disaster response.

Your responsibilities:
1. Calculate appropriate evacuation radius based on fire conditions
2. Assess police unit availability and requirements
3. Identify roads that need closure
4. Estimate evacuation time
5. Request mutual aid if local resources are insufficient

Key considerations:
- High wind speeds require larger evacuation zones
- Each evacuation requires significant police presence for traffic control
- Road closures must be coordinated with fire department
- Mutual aid requests require approval and cost ~$5,000 per unit

Always provide specific numbers, timelines, and clear recommendations.""",
    tools=[
        analyze_police_resources,
        calculate_evacuation_radius,
        get_police_units_available,
        identify_road_closures,
        estimate_evacuation_time,
        request_mutual_aid,
    ],
)

