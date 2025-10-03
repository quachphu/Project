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

"""Police resource management tools."""


def calculate_evacuation_radius(fire_location: str, wind_speed_mph: int, wind_direction: str) -> dict:
    """Calculate recommended evacuation radius based on fire conditions.
    
    Args:
        fire_location: Location of the fire
        wind_speed_mph: Wind speed in miles per hour
        wind_direction: Wind direction (e.g., 'southwest')
        
    Returns:
        Evacuation radius recommendation
    """
    # Base radius calculation (simplified model)
    if wind_speed_mph > 25:
        radius = 3
        priority_direction = wind_direction
    elif wind_speed_mph > 15:
        radius = 2
        priority_direction = wind_direction
    else:
        radius = 1
        priority_direction = "all directions"
    
    return {
        "fire_location": fire_location,
        "recommended_radius_miles": radius,
        "priority_direction": priority_direction,
        "wind_speed_mph": wind_speed_mph,
        "reasoning": f"High winds ({wind_speed_mph} mph) require {radius}-mile evacuation zone"
    }


def get_police_units_available(location: str) -> dict:
    """Get available police units for the location.
    
    Args:
        location: Location to check police availability
        
    Returns:
        Police unit availability information
    """
    return {
        "location": location,
        "patrol_units_available": 15,
        "patrol_units_on_duty": 20,
        "patrol_units_required_for_evacuation": 22,
        "traffic_control_units": 5,
        "k9_units": 2,
        "swat_available": True,
        "mutual_aid_needed": True,
        "mutual_aid_units_required": 7,
        "recommendation": "Request mutual aid from neighboring counties"
    }


def identify_road_closures(evacuation_zone: str, radius_miles: int) -> dict:
    """Identify roads that need to be closed for evacuation.
    
    Args:
        evacuation_zone: Center of evacuation zone
        radius_miles: Radius of evacuation zone
        
    Returns:
        Road closure information
    """
    # Mock major roads that would need closure
    roads_to_close = []
    
    if radius_miles >= 1:
        roads_to_close.extend(["Main Street", "Oak Avenue"])
    if radius_miles >= 2:
        roads_to_close.extend(["Highway 101 North", "Industrial Parkway"])
    if radius_miles >= 3:
        roads_to_close.extend(["Highway 101 South", "Riverside Drive", "County Road 45"])
    
    return {
        "evacuation_zone": evacuation_zone,
        "radius_miles": radius_miles,
        "roads_to_close": roads_to_close,
        "number_of_roads": len(roads_to_close),
        "detour_routes": ["Interstate 95 (alternate north-south)", "Route 27 (alternate east-west)"],
        "estimated_closure_duration_hours": 6
    }


def estimate_evacuation_time(population: int, available_units: int) -> dict:
    """Estimate time needed to complete evacuation.
    
    Args:
        population: Number of people to evacuate
        available_units: Number of police units available
        
    Returns:
        Evacuation time estimate
    """
    # Simplified model: assume each unit can help evacuate ~500 people per hour
    people_per_unit_per_hour = 500
    
    if available_units > 0:
        hours_needed = population / (available_units * people_per_unit_per_hour)
    else:
        hours_needed = 12  # fallback estimate
    
    return {
        "population_to_evacuate": population,
        "police_units_available": available_units,
        "estimated_time_hours": round(hours_needed, 1),
        "estimated_time_display": f"{int(hours_needed)} hours {int((hours_needed % 1) * 60)} minutes",
        "bottlenecks": ["Limited evacuation routes", "Rush hour traffic"] if hours_needed > 3 else [],
        "recommendation": "Coordinate with fire department for traffic control" if hours_needed > 2 else "Standard evacuation procedures sufficient"
    }


def request_mutual_aid(location: str, units_needed: int) -> dict:
    """Request mutual aid from neighboring jurisdictions.
    
    Args:
        location: Location requesting mutual aid
        units_needed: Number of additional units needed
        
    Returns:
        Mutual aid request information
    """
    return {
        "requesting_location": location,
        "units_requested": units_needed,
        "neighboring_agencies": ["Nassau County Police", "Suffolk County Police", "NYPD"],
        "estimated_response_time_minutes": 45,
        "estimated_cost": units_needed * 5000,  # $5k per unit
        "requires_approval": True,
        "approval_authority": "Emergency Operations Center",
        "status": "pending_approval"
    }

