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

"""Hospital resource management tools."""


def check_hospital_beds(location: str, radius_miles: int = 2) -> dict:
    """Check hospital bed availability within a specified radius.
    
    Args:
        location: The location to search around
        radius_miles: Search radius in miles (default: 2)
        
    Returns:
        Dictionary with hospital capacity information
    """
    # Mock data that scales with radius
    mock_data = {
        2: {
            "radius_miles": 2,
            "hospitals_found": 3,
            "total_beds_available": 35,
            "burn_unit_beds": 5,
            "trauma_beds": 12,
            "icu_beds": 8,
            "ambulances_available": 8,
            "recommendation": "Insufficient burn unit capacity - consider expanding search radius"
        },
        4: {
            "radius_miles": 4,
            "hospitals_found": 8,
            "total_beds_available": 100,
            "burn_unit_beds": 23,
            "trauma_beds": 35,
            "icu_beds": 18,
            "ambulances_available": 18,
            "recommendation": "Adequate capacity found at 4-mile radius"
        },
        8: {
            "radius_miles": 8,
            "hospitals_found": 15,
            "total_beds_available": 200,
            "burn_unit_beds": 45,
            "trauma_beds": 70,
            "icu_beds": 35,
            "ambulances_available": 32,
            "recommendation": "Excellent capacity available"
        }
    }
    
    # Return data for the requested radius, or closest match
    if radius_miles in mock_data:
        result = mock_data[radius_miles]
    elif radius_miles <= 2:
        result = mock_data[2]
    elif radius_miles <= 4:
        result = mock_data[4]
    else:
        result = mock_data[8]
    
    result["location"] = location
    return result


def check_burn_unit_capacity(location: str, required_beds: int = 20) -> dict:
    """Check specific burn unit capacity and needs.
    
    Args:
        location: The location to check
        required_beds: Number of burn beds estimated to be needed
        
    Returns:
        Dictionary with burn unit analysis
    """
    current_capacity = check_hospital_beds(location, radius_miles=2)
    
    return {
        "location": location,
        "required_burn_beds": required_beds,
        "available_burn_beds_2mi": current_capacity["burn_unit_beds"],
        "sufficient": current_capacity["burn_unit_beds"] >= required_beds,
        "deficit": max(0, required_beds - current_capacity["burn_unit_beds"]),
        "recommendation": "Expand search radius to 4 miles" if current_capacity["burn_unit_beds"] < required_beds else "Sufficient capacity within 2 miles"
    }


def expand_search_radius(current_radius: int) -> int:
    """Calculate expanded search radius.
    
    Args:
        current_radius: Current search radius in miles
        
    Returns:
        New expanded radius (doubles the current radius)
    """
    return current_radius * 2


def get_ambulance_availability(location: str, radius_miles: int = 2) -> dict:
    """Get ambulance availability within radius.
    
    Args:
        location: Location to search
        radius_miles: Search radius in miles
        
    Returns:
        Ambulance availability information
    """
    hospital_data = check_hospital_beds(location, radius_miles)
    
    return {
        "location": location,
        "radius_miles": radius_miles,
        "ambulances_available": hospital_data["ambulances_available"],
        "response_time_avg_minutes": 8 if radius_miles <= 2 else 12 if radius_miles <= 4 else 18
    }

