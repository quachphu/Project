"""Mock weather alert data generator for flood monitoring simulation."""

from datetime import datetime, timedelta
from typing import Dict


def generate_weather_alert(scenario: str = "moderate_flood") -> Dict:
    """
    Generate a mock weather API alert for flood scenarios.
    
    Args:
        scenario: Type of scenario - "moderate_flood", "severe_flood", "minor_rain"
    
    Returns:
        Dictionary containing weather alert data
    """
    
    scenarios = {
        "moderate_flood": {
            "precipitation_probability": 85,
            "expected_precipitation_mm": 120,
            "severity_level": 4,
            "description": "Severe rainfall expected with high flood risk"
        },
        "medium_flood": {
            "precipitation_probability": 75,
            "expected_precipitation_mm": 95,
            "severity_level": 3,
            "description": "Moderate rainfall expected with elevated flood risk"
        },
        "severe_flood": {
            "precipitation_probability": 95,
            "expected_precipitation_mm": 150,
            "severity_level": 5,
            "description": "Extreme rainfall expected with severe flood risk"
        },
        "minor_rain": {
            "precipitation_probability": 45,
            "expected_precipitation_mm": 25,
            "severity_level": 1,
            "description": "Light rainfall expected with minimal flood risk"
        }
    }
    
    scenario_data = scenarios.get(scenario, scenarios["moderate_flood"])
    
    weather_alert = {
        "alert_id": f"WX-FLOOD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "alert_type": "FLOOD_WATCH",
        "timestamp": datetime.now().isoformat(),
        "valid_until": (datetime.now() + timedelta(hours=6)).isoformat(),
        "issued_by": "National Weather Service",
        "location": {
            "region": "Northern Valley",
            "zipcode": "11375",  # Queens, NY
            "coordinates": {
                "lat": 42.3601,
                "lon": -71.0589
            },
            "affected_areas": ["River Basin District", "Downtown", "Riverside Neighborhoods"]
        },
        "precipitation": {
            "probability_percent": scenario_data["precipitation_probability"],
            "expected_amount_mm": scenario_data["expected_precipitation_mm"],
            "timeframe_hours": 2,
            "intensity": "heavy" if scenario_data["severity_level"] >= 3 else "moderate"
        },
        "severity": {
            "level": scenario_data["severity_level"],
            "scale": "1-5 (5 being most severe)",
            "description": scenario_data["description"]
        },
        "forecast": {
            "temperature_c": 18,
            "wind_speed_kmh": 25,
            "wind_direction": "northeast",
            "atmospheric_pressure_hpa": 1008
        },
        "message": f"⚠️ Expected rain in 2 hours. {scenario_data['description']}. Monitor river levels and prepare for potential flooding.",
        "recommendations": [
            "Monitor local river gauge levels",
            "Prepare emergency supplies",
            "Stay informed of updates",
            "Avoid low-lying areas if flooding occurs"
        ]
    }
    
    return weather_alert


if __name__ == "__main__":
    # Test the generator
    import json
    alert = generate_weather_alert("moderate_flood")
    print(json.dumps(alert, indent=2))

