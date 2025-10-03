"""ML-based similarity analysis for flood events."""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_similarity_score(current_data: dict) -> dict:
    """
    Simulate ML model that compares current conditions with historical flood events.
    
    Args:
        current_data: Dictionary with current weather and river gauge data
        
    Returns:
        Dictionary with similarity analysis results
    """
    
    # Load historical data
    csv_path = os.path.join(os.path.dirname(__file__), 'historical_events.csv')
    historical_df = pd.read_csv(csv_path)
    
    # Extract current metrics
    current_severity = current_data.get('severity', 0)
    current_precip = current_data.get('precipitation_mm', 0)
    current_critical = current_data.get('critical_sensors', 0)
    current_warning = current_data.get('warning_sensors', 0)
    current_avg_level = current_data.get('avg_river_level', 0)
    
    # Calculate similarity scores with each historical event
    similarities = []
    
    for idx, row in historical_df.iterrows():
        # Feature-based similarity (weighted Euclidean distance)
        severity_diff = abs(current_severity - row['severity']) / 5.0
        precip_diff = abs(current_precip - row['precipitation_mm']) / 200.0
        critical_diff = abs(current_critical - row['critical_sensors']) / 5.0
        warning_diff = abs(current_warning - row['warning_sensors']) / 10.0
        
        # Calculate weighted similarity (0-100%)
        similarity = 100 * (1 - (
            0.3 * severity_diff +
            0.3 * precip_diff +
            0.2 * critical_diff +
            0.2 * warning_diff
        ))
        
        similarities.append({
            'event_id': row['event_id'],
            'date': row['date'],
            'similarity_percent': max(0, min(100, similarity)),
            'outcome': row['outcome'],
            'damage_level': row['damage_level'],
            'precipitation_mm': row['precipitation_mm'],
            'critical_sensors': row['critical_sensors'],
            'warning_sensors': row['warning_sensors']
        })
    
    # Sort by similarity
    similarities.sort(key=lambda x: x['similarity_percent'], reverse=True)
    
    # Get top match
    best_match = similarities[0]
    
    # Calculate confidence score (0-10 points)
    # Higher similarity = higher confidence score
    similarity_pct = best_match['similarity_percent']
    
    if similarity_pct >= 85:
        confidence_score = 10
        confidence_level = "VERY HIGH"
    elif similarity_pct >= 75:
        confidence_score = 9
        confidence_level = "HIGH"
    elif similarity_pct >= 65:
        confidence_score = 7
        confidence_level = "MODERATE"
    elif similarity_pct >= 50:
        confidence_score = 5
        confidence_level = "LOW"
    else:
        confidence_score = 3
        confidence_level = "VERY LOW"
    
    return {
        "ml_model": "Flood Event Similarity Analyzer v2.1",
        "analysis_type": "Historical Pattern Matching",
        "best_match": best_match,
        "top_5_matches": similarities[:5],
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "similarity_percent": similarity_pct,
        "recommendation": _generate_recommendation(best_match, similarity_pct),
        "features_analyzed": {
            "severity_level": current_severity,
            "precipitation_mm": current_precip,
            "critical_sensors": current_critical,
            "warning_sensors": current_warning,
            "avg_river_level_m": current_avg_level
        }
    }

def _generate_recommendation(match: dict, similarity: float) -> str:
    """Generate recommendation based on historical match."""
    outcome = match['outcome']
    damage = match['damage_level']
    
    if similarity >= 85:
        if damage == 'high':
            return f"⚠️ CRITICAL: Current conditions closely match {match['event_id']} which resulted in {outcome} with {damage} damage. Immediate action recommended."
        elif damage == 'moderate':
            return f"⚠️ WARNING: Pattern highly similar to {match['event_id']} which caused {outcome}. Prepare emergency response."
        else:
            return f"ℹ️ Current conditions match {match['event_id']}, which had minimal impact. Continue monitoring."
    elif similarity >= 70:
        return f"⚠️ Conditions similar to past event {match['event_id']}. Enhanced monitoring recommended."
    else:
        return f"ℹ️ Limited similarity to historical events. Standard monitoring protocols apply."

