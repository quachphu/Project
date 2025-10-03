"""ML similarity scoring tool for flood monitoring."""

try:
    from app.utils.shared_state import get_disaster_context, set_disaster_context
except ImportError:
    # Fallback for when shared_state is not available
    _context = {"score_breakdown": {}, "total_confidence_score": 0}
    
    def get_disaster_context():
        return _context
    
    def set_disaster_context(ctx):
        global _context
        _context = ctx


def score_ml_similarity(
    similarity_percent: float,
    matched_event_id: str,
    matched_outcome: str,
    matched_damage_level: str,
    current_severity: int,
    current_precipitation: float
) -> str:
    """
    Score ML-based historical similarity analysis out of 20 points.
    
    This tool analyzes how closely current flood conditions match historical
    flood events using ML pattern matching. Higher similarity to severe past
    events increases confidence score.
    
    Scoring:
    - Similarity >= 85%: 10 points (VERY HIGH confidence)
    - Similarity >= 75%: 9 points (HIGH confidence)
    - Similarity >= 65%: 7 points (MODERATE confidence)
    - Similarity >= 50%: 5 points (LOW confidence)
    - Similarity < 50%: 3 points (VERY LOW confidence)
    
    Args:
        similarity_percent: ML-calculated similarity to best historical match (0-100)
        matched_event_id: ID of the most similar historical event
        matched_outcome: Outcome of the matched event (e.g., "flooding", "severe_flooding")
        matched_damage_level: Damage level from matched event ("none", "low", "moderate", "high")
        current_severity: Current weather severity level (1-5)
        current_precipitation: Current precipitation amount in mm
        
    Returns:
        ML similarity analysis with confidence score out of 10 points
    """
    
    # Calculate score based on similarity (0-20 points)
    if similarity_percent >= 85:
        score = 20
        confidence = "VERY HIGH"
    elif similarity_percent >= 75:
        score = 18
        confidence = "HIGH"
    elif similarity_percent >= 65:
        score = 14
        confidence = "MODERATE"
    elif similarity_percent >= 50:
        score = 10
        confidence = "LOW"
    else:
        score = 6
        confidence = "VERY LOW"
    
    # Update shared context
    context = get_disaster_context()
    prev_score = context.get("total_confidence_score", 0)
    
    # Ensure score_breakdown exists
    if "score_breakdown" not in context:
        context["score_breakdown"] = {}
    
    context["score_breakdown"]["ml_similarity"] = score
    context["total_confidence_score"] = prev_score + score
    context["ml_analysis"] = {
        "similarity_percent": similarity_percent,
        "matched_event": matched_event_id,
        "matched_outcome": matched_outcome,
        "confidence_level": confidence
    }
    set_disaster_context(context)
    
    total_score = context["total_confidence_score"]
    
    # Generate risk assessment
    if matched_damage_level == "high" and similarity_percent >= 80:
        risk_level = "🔴 CRITICAL"
        action = "IMMEDIATE EVACUATION RECOMMENDED"
    elif matched_damage_level in ["high", "moderate"] and similarity_percent >= 70:
        risk_level = "🟠 SEVERE"
        action = "PREPARE FOR EMERGENCY RESPONSE"
    elif similarity_percent >= 60:
        risk_level = "🟡 ELEVATED"
        action = "ENHANCED MONITORING"
    else:
        risk_level = "🟢 STANDARD"
        action = "CONTINUE ROUTINE MONITORING"
    
    response = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 **PHASE 3: ML HISTORICAL SIMILARITY ANALYSIS**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**ML Model:** Flood Event Similarity Analyzer v2.1
**Analysis Type:** Historical Pattern Matching

**Current Conditions:**
- Severity Level: {current_severity}/5
- Precipitation: {current_precipitation}mm

**Best Historical Match:**
- Event ID: {matched_event_id}
- Similarity: {similarity_percent:.1f}%
- Outcome: {matched_outcome.replace('_', ' ').title()}
- Damage Level: {matched_damage_level.upper()}

📊 **ML CONFIDENCE SCORING:**

Similarity Score: {similarity_percent:.1f}%
Confidence Level: {confidence}

**ML SIMILARITY SCORE: {score}/20 points**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 **CUMULATIVE CONFIDENCE SCORE: {total_score}/100**

**Score Breakdown:**
- Weather Alert: {context["score_breakdown"]["weather_alert"]}/25
- River Gauges: {context["score_breakdown"]["river_gauges"]}/20
- ML Similarity: {score}/10 ✨ **NEW**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**RISK ASSESSMENT:** {risk_level}

**RECOMMENDED ACTION:** {action}

{'🚨 **WARNING**: Current conditions match historical event that caused ' + matched_damage_level.upper() + ' damage.' if similarity_percent >= 75 and matched_damage_level in ['high', 'moderate'] else ''}

{'✅ Pattern analysis complete. Recommend proceeding to Phase 4 (Satellite Imagery) if cumulative score >= 50.' if total_score >= 45 else ''}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return response

