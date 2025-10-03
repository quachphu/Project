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

"""Flood monitoring tools with confidence scoring (0-100 points)."""

from app.utils.shared_state import set_disaster_context, get_disaster_context


def score_weather_alert(
    alert_id: str,
    severity_level: int,
    precipitation_mm: float,
    probability_percent: int,
    location_region: str,
    zipcode: str
) -> str:
    """
    Score weather alert out of 25 points for flood risk confidence.
    
    Scoring criteria (AGGRESSIVE WEIGHTING):
    - Severity level (1-5): severity * 4 points (max 20)
    - Precipitation amount: (precip_mm / 50) * 3 points (max 3)
    - Probability: (probability / 50) points (max 2)
    
    Args:
        alert_id: Unique weather alert identifier
        severity_level: Severity rating 1-5 (5 most severe)
        precipitation_mm: Expected precipitation in millimeters
        probability_percent: Probability of precipitation 0-100%
        location_region: Geographic region name
        zipcode: ZIP code of affected area
        
    Returns:
        Weather alert assessment with confidence score out of 25 points
    """
    # Calculate score components (VERY AGGRESSIVE - almost always triggers)
    # Severity: 5 points per level (4/5 = 20 points!)
    severity_score = min(severity_level * 5, 20)
    
    # Precipitation: 3 points max (100mm+ = full points)
    precip_score = min((precipitation_mm / 100) * 3, 3)
    
    # Probability: 2 points (70%+ = full points)
    prob_score = min(probability_percent / 50, 2)
    
    total_score = int(severity_score + precip_score + prob_score)
    
    # Ensure severe scenarios always score >= 20
    if severity_level >= 4 and precipitation_mm >= 100:
        total_score = max(total_score, 22)
    
    # Store in shared context
    alert_data = {
        "alert_id": alert_id,
        "severity": {"level": severity_level},
        "precipitation": {"expected_amount_mm": precipitation_mm, "probability_percent": probability_percent},
        "location": {"region": location_region, "zipcode": zipcode},
        "score": total_score
    }
    
    context = get_disaster_context()
    context["alert_data"] = alert_data
    context["disaster_type"] = "FLOOD"
    context["location"] = location_region
    context["zipcode"] = zipcode
    context["total_confidence_score"] = total_score
    context["score_breakdown"] = {
        "weather_alert": total_score,
        "river_gauges": 0,
        "satellite": 0,
        "drone": 0,
        "social_media": 0
    }
    set_disaster_context(context)
    
    # Determine if escalation needed
    needs_escalation = total_score >= 20
    
    response = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌧️ WEATHER ALERT ANALYSIS (Phase 1: T-2:00:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 **Alert Details:**
- Alert ID: {alert_id}
- Location: {location_region} (ZIP: {zipcode})
- Severity Level: {severity_level}/5
- Expected Precipitation: {precipitation_mm}mm
- Probability: {probability_percent}%

📊 **CONFIDENCE SCORING:**

Severity Component:  {severity_score:.1f}/15 points
Precipitation Component: {precip_score:.1f}/5 points
Probability Component: {prob_score:.1f}/5 points

**WEATHER ALERT SCORE: {total_score}/25 points**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 **CUMULATIVE CONFIDENCE SCORE: {total_score}/100**

{'🚨 **ESCALATION DECISION:**' if needs_escalation else ''}
{'✅ Score ≥ 20/25 - ESCALATING TO RIVER GAUGE MONITORING' if needs_escalation else ''}
{'⚠️ Deploying river gauge sensors near ZIP code ' + zipcode if needs_escalation else ''}

{'' if needs_escalation else '⏸️ Score below escalation threshold (20/25). Monitoring only.'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return response


def score_river_gauges(
    sensor_1_status: str,
    sensor_1_trend: str,
    sensor_2_status: str,
    sensor_2_trend: str,
    sensor_3_status: str,
    sensor_3_trend: str,
    sensor_4_status: str,
    sensor_4_trend: str,
    sensor_5_status: str,
    sensor_5_trend: str,
    sensor_6_status: str,
    sensor_6_trend: str
) -> str:
    """
    Score river gauge sensors out of 25 points for flood risk confidence.
    
    Scoring: Each sensor contributes based on status and trend:
    - Critical status: +6 points
    - Warning status: +4 points
    - Normal status: +0 points
    - Rising trend: +2 additional point
    
    Max 25 points total (capped).
    
    Args:
        sensor_X_status: Status of sensor X (normal/warning/critical)
        sensor_X_trend: Trend of sensor X (steady/rising/falling)
        
    Returns:
        River gauge analysis with confidence score out of 20 points
    """
    sensors = [
        (sensor_1_status, sensor_1_trend),
        (sensor_2_status, sensor_2_trend),
        (sensor_3_status, sensor_3_trend),
        (sensor_4_status, sensor_4_trend),
        (sensor_5_status, sensor_5_trend),
        (sensor_6_status, sensor_6_trend)
    ]
    
    score = 0
    critical_count = 0
    warning_count = 0
    rising_count = 0
    
    for status, trend in sensors:
        # AGGRESSIVE scoring - weight critical/warning heavily
        if status == "critical":
            score += 7  # Increased for 25-point scale
            critical_count += 1
        elif status == "warning":
            score += 5  # Increased for 25-point scale
            warning_count += 1
        
        if trend == "rising":
            score += 2  # Increased from 1 - rising is very concerning
            rising_count += 1
    
    # Cap at 25 points
    score = min(score, 25)
    
    # If we have critical sensors + rising trends, ensure high score
    if critical_count >= 1 and rising_count >= 4:
        score = max(score, 22)  # Guarantee escalation-worthy score
    
    # Update context
    context = get_disaster_context()
    prev_score = context.get("total_confidence_score", 0)
    
    # Ensure score_breakdown exists
    if "score_breakdown" not in context:
        context["score_breakdown"] = {}
    
    context["score_breakdown"]["river_gauges"] = score
    context["total_confidence_score"] = prev_score + score
    set_disaster_context(context)
    
    total_score = context["total_confidence_score"]
    
    response = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌊 RIVER GAUGE ANALYSIS (Phase 2: T-1:00:00)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Sensor Status Summary:**
- 🔴 Critical: {critical_count} sensors
- 🟡 Warning: {warning_count} sensors  
- 🟢 Normal: {6 - critical_count - warning_count} sensors
- ↗️ Rising Trend: {rising_count} sensors

📈 **CONFIDENCE SCORING:**

Status-Based Score: {score - rising_count}/15 points
Trend-Based Score: {rising_count}/5 points

**RIVER GAUGE SCORE: {score}/20 points**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 **CUMULATIVE CONFIDENCE SCORE: {total_score}/100**

Breakdown:
- Weather Alert: {context["score_breakdown"]["weather_alert"]}/25
- River Gauges: {score}/20
- Satellite Imagery: {context["score_breakdown"]["satellite"]}/10 (pending)
- Drone LiDAR: {context["score_breakdown"]["drone"]}/10 (pending)
- Social Media: {context["score_breakdown"]["social_media"]}/10 (pending)

{'🚨 **HIGH RISK DETECTED**' if score >= 15 else '⚠️ **MODERATE RISK**' if score >= 10 else '✅ **MONITORING**'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return response

