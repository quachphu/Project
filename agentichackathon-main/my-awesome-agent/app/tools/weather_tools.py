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

"""Mock weather API tools for disaster simulation."""

from datetime import datetime, timedelta


def simulate_fire_weather_alert(location: str) -> dict:
    """Simulate a severe fire weather alert for a given location.
    
    Args:
        location: The location to check for fire alerts (e.g., "Queens County, NY")
        
    Returns:
        A dictionary containing the fire weather alert details
    """
    return {
        "alert_id": "NWS-2025-100145",
        "alert_type": "RED_FLAG_WARNING",
        "disaster_classification": "WILDFIRE",
        "location": {
            "city": location.split(",")[0].strip() if "," in location else location,
            "state": location.split(",")[1].strip() if "," in location else "NY",
            "coordinates": {"lat": 40.7282, "lon": -73.7949}
        },
        "severity": "EXTREME",
        "fire_weather_index": 89,
        "conditions": {
            "temperature_f": 95,
            "humidity_percent": 12,
            "wind_speed_mph": 28,
            "wind_direction": "southwest",
            "wind_gusts_mph": 42
        },
        "fire_behavior": {
            "rapid_spread_expected": True,
            "spot_fire_risk": "HIGH",
            "containment_difficulty": "EXTREME"
        },
        "affected_area": {
            "radius_miles": 5,
            "estimated_population": 45000,
            "structures_at_risk": 3200
        },
        "timestamp": datetime.now().isoformat(),
        "expires": (datetime.now() + timedelta(hours=8)).isoformat(),
        "issued_by": "National Weather Service"
    }


def classify_disaster_type(alert_data: dict) -> str:
    """Classify the type of disaster based on alert data.
    
    Args:
        alert_data: Weather alert data
        
    Returns:
        Disaster classification string
    """
    alert_type = alert_data.get("alert_type", "")
    
    if "RED_FLAG" in alert_type or alert_data.get("disaster_classification") == "WILDFIRE":
        return "WILDFIRE"
    elif "FLOOD" in alert_type:
        return "FLOOD"
    elif "HURRICANE" in alert_type or "TROPICAL" in alert_type:
        return "HURRICANE"
    elif "TORNADO" in alert_type:
        return "TORNADO"
    else:
        return "UNKNOWN"

