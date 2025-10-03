"""Mock river gauge sensor data generator."""

from datetime import datetime
from typing import Dict, List


# Static sensor data for 2 rivers with 3 sensors each
RIVER_GAUGE_DATA = {
    "11375": {  # Zipcode: Queens, NY
        "rivers": [
            {
                "river_id": "RIVER-001",
                "river_name": "Flushing Creek",
                "distance_miles": 1.2,
                "sensors": [
                    {
                        "sensor_id": "SENSOR-R1-001",
                        "sensor_name": "Flushing Creek Upper",
                        "gauge_id": "USGS-01311500",
                        "water_level_m": 3.8,
                        "flow_rate_cms": 45.2,
                        "trend": "rising",
                        "sensor_health": 99,
                        "last_updated": datetime.now().isoformat(),
                        "threshold_warning_m": 4.5,
                        "threshold_critical_m": 6.0,
                        "status": "normal"
                    },
                    {
                        "sensor_id": "SENSOR-R1-002",
                        "sensor_name": "Flushing Creek Middle",
                        "gauge_id": "USGS-01311501",
                        "water_level_m": 4.2,
                        "flow_rate_cms": 52.8,
                        "trend": "rising",
                        "sensor_health": 98,
                        "last_updated": datetime.now().isoformat(),
                        "threshold_warning_m": 4.5,
                        "threshold_critical_m": 6.0,
                        "status": "warning"
                    },
                    {
                        "sensor_id": "SENSOR-R1-003",
                        "sensor_name": "Flushing Creek Lower",
                        "gauge_id": "USGS-01311502",
                        "water_level_m": 3.5,
                        "flow_rate_cms": 38.6,
                        "trend": "steady",
                        "sensor_health": 97,
                        "last_updated": datetime.now().isoformat(),
                        "threshold_warning_m": 4.5,
                        "threshold_critical_m": 6.0,
                        "status": "normal"
                    }
                ]
            },
            {
                "river_id": "RIVER-002",
                "river_name": "Alley Creek",
                "distance_miles": 2.5,
                "sensors": [
                    {
                        "sensor_id": "SENSOR-R2-001",
                        "sensor_name": "Alley Creek Upper",
                        "gauge_id": "USGS-01311600",
                        "water_level_m": 5.1,
                        "flow_rate_cms": 68.4,
                        "trend": "rising",
                        "sensor_health": 99,
                        "last_updated": datetime.now().isoformat(),
                        "threshold_warning_m": 5.0,
                        "threshold_critical_m": 7.0,
                        "status": "warning"
                    },
                    {
                        "sensor_id": "SENSOR-R2-002",
                        "sensor_name": "Alley Creek Middle",
                        "gauge_id": "USGS-01311601",
                        "water_level_m": 5.8,
                        "flow_rate_cms": 75.2,
                        "trend": "rising",
                        "sensor_health": 96,
                        "last_updated": datetime.now().isoformat(),
                        "threshold_warning_m": 5.0,
                        "threshold_critical_m": 7.0,
                        "status": "critical"
                    },
                    {
                        "sensor_id": "SENSOR-R2-003",
                        "sensor_name": "Alley Creek Lower",
                        "gauge_id": "USGS-01311602",
                        "water_level_m": 4.9,
                        "flow_rate_cms": 62.1,
                        "trend": "rising",
                        "sensor_health": 99,
                        "last_updated": datetime.now().isoformat(),
                        "threshold_warning_m": 5.0,
                        "threshold_critical_m": 7.0,
                        "status": "warning"
                    }
                ]
            }
        ]
    }
}


def get_river_gauges_by_zipcode(zipcode: str) -> Dict:
    """
    Get river gauge data for a specific zipcode.
    
    Args:
        zipcode: ZIP code to search rivers near
        
    Returns:
        Dictionary containing river and sensor data
    """
    data = RIVER_GAUGE_DATA.get(zipcode, {
        "rivers": [],
        "message": f"No river gauge data available for zipcode {zipcode}"
    })
    
    if data.get("rivers"):
        # Add summary statistics
        all_sensors = []
        for river in data["rivers"]:
            all_sensors.extend(river["sensors"])
        
        normal_count = sum(1 for s in all_sensors if s["status"] == "normal")
        warning_count = sum(1 for s in all_sensors if s["status"] == "warning")
        critical_count = sum(1 for s in all_sensors if s["status"] == "critical")
        
        data["summary"] = {
            "total_rivers": len(data["rivers"]),
            "total_sensors": len(all_sensors),
            "sensors_normal": normal_count,
            "sensors_warning": warning_count,
            "sensors_critical": critical_count,
            "zipcode": zipcode
        }
    
    return data


def calculate_river_gauge_score(river_data: Dict) -> int:
    """
    Calculate confidence score (0-20) based on river gauge data.
    
    Scoring criteria:
    - Each sensor in critical status: +5 points
    - Each sensor in warning status: +3 points  
    - Rising trend: +1 point per sensor
    - Max 20 points
    
    Args:
        river_data: River gauge data from get_river_gauges_by_zipcode
        
    Returns:
        Score from 0-20
    """
    score = 0
    
    if not river_data.get("rivers"):
        return 0
    
    for river in river_data["rivers"]:
        for sensor in river["sensors"]:
            # Status-based scoring
            if sensor["status"] == "critical":
                score += 5
            elif sensor["status"] == "warning":
                score += 3
            
            # Trend-based scoring
            if sensor["trend"] == "rising":
                score += 1
    
    # Cap at 20 points
    return min(score, 20)


if __name__ == "__main__":
    # Test the generator
    import json
    
    data = get_river_gauges_by_zipcode("11375")
    print(json.dumps(data, indent=2))
    
    score = calculate_river_gauge_score(data)
    print(f"\nRiver Gauge Score: {score}/20")

