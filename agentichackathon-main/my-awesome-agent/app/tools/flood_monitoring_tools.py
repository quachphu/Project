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

"""Flood monitoring tools for disaster simulation."""

from typing import Any
from app.utils.shared_state import set_disaster_context, get_disaster_context


def process_weather_alert(
    alert_id: str,
    severity_level: int,
    precipitation_mm: float,
    probability_percent: int,
    location_region: str,
    message: str
) -> str:
    """
    Process incoming weather alert for flood monitoring.
    
    Args:
        alert_id: Unique identifier for the weather alert
        severity_level: Severity rating from 1-5 (5 being most severe)
        precipitation_mm: Expected precipitation amount in millimeters
        probability_percent: Probability of precipitation (0-100%)
        location_region: Geographic region affected by the alert
        message: Weather alert message text
        
    Returns:
        Formatted assessment of the alert with risk analysis
    """
    # Reconstruct the alert_json from parameters
    alert_json = {
        "alert_id": alert_id,
        "severity": {"level": severity_level},
        "precipitation": {"expected_amount_mm": precipitation_mm, "probability_percent": probability_percent},
        "location": {"region": location_region},
        "message": message
    }
    # Store alert in shared context
    set_disaster_context({
        "alert_data": alert_json,
        "disaster_type": "FLOOD",
        "location": alert_json.get("location", {}).get("region", "Unknown")
    })
    
    severity_level = alert_json.get("severity", {}).get("level", 0)
    precipitation_mm = alert_json.get("precipitation", {}).get("expected_amount_mm", 0)
    probability = alert_json.get("precipitation", {}).get("probability_percent", 0)
    message = alert_json.get("message", "")
    
    # Decision logic based on severity
    should_trigger_sensors = severity_level >= 3
    risk_assessment = "HIGH" if severity_level >= 4 else "MODERATE" if severity_level >= 3 else "LOW"
    
    response = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌧️ WEATHER ALERT RECEIVED (T-2:00:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 **Location:** {alert_json.get("location", {}).get("region", "Unknown")}
🆔 **Alert ID:** {alert_json.get("alert_id", "N/A")}
⏰ **Timestamp:** {alert_json.get("timestamp", "N/A")}

**SEVERITY ASSESSMENT:**
- Level: {severity_level}/5
- Risk: {risk_assessment}
- Expected Precipitation: {precipitation_mm}mm
- Probability: {probability}%

**ALERT MESSAGE:**
{message}

**INITIAL ASSESSMENT:**
{'✅ Severity threshold met - Proceeding to next monitoring phase' if should_trigger_sensors else '⚠️ Severity below threshold - Monitoring only'}

{'**NEXT STEPS:**' if should_trigger_sensors else ''}
{'- Deploy river gauge sensors (T-1:00:00)' if should_trigger_sensors else ''}
{'- Activate satellite imagery analysis (T-0:50:00)' if should_trigger_sensors else ''}
{'- Prepare drone deployment if needed (T-0:30:00)' if should_trigger_sensors else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return response


def analyze_flood_risk() -> str:
    """
    Analyze overall flood risk based on the most recent weather alert.
    
    This tool uses the weather alert data that was previously processed
    to calculate an overall risk score and provide recommendations.
        
    Returns:
        Comprehensive risk analysis with recommendations and confidence level
    """
    # Get stored context from previously processed alert
    context = get_disaster_context()
    alert_data = context.get("alert_data", {})
    
    severity = alert_data.get("severity", {}).get("level", 0)
    precipitation = alert_data.get("precipitation", {}).get("expected_amount_mm", 0)
    
    # Simple risk scoring
    risk_score = (severity * 0.6) + ((precipitation / 200) * 5 * 0.4)
    
    if risk_score >= 4:
        risk_level = "CRITICAL"
        recommendation = "IMMEDIATE EVACUATION - Activate all emergency response teams"
    elif risk_score >= 3:
        risk_level = "HIGH"
        recommendation = "PREPARE FOR EVACUATION - Deploy monitoring systems"
    elif risk_score >= 2:
        risk_level = "MODERATE"
        recommendation = "MONITOR CLOSELY - Prepare emergency resources"
    else:
        risk_level = "LOW"
        recommendation = "ROUTINE MONITORING - No immediate action required"
    
    return f"""
🎯 **FLOOD RISK ANALYSIS**

**Overall Risk Score:** {risk_score:.1f}/5
**Risk Level:** {risk_level}

**Factors Considered:**
- Weather severity: {severity}/5
- Expected precipitation: {precipitation}mm
- Historical flood patterns: Normal
- Current river levels: Within normal range (mock data)

**RECOMMENDATION:**
{recommendation}

**Confidence:** 85%
"""

