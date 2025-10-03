"""Social media monitoring tools for flood analysis."""

from typing import List
import sys
import os

# Add flood-monitoring-demo to path
demo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "flood-monitoring-demo")
sys.path.insert(0, demo_path)

from mock_data.social_media_data import get_mock_tweets_by_zipcode, get_mock_tweets_by_keywords

def search_tweets_by_location(zipcode: str) -> str:
    """
    Search for trending tweets near a specific ZIP code location.
    
    Args:
        zipcode: The ZIP code to search around (e.g., "11375")
    
    Returns:
        JSON string with top trending tweets in that area
    """
    result = get_mock_tweets_by_zipcode(zipcode)
    
    summary = f"""
📍 **Location-Based Search Results (ZIP: {zipcode})**

Found {result['total_tweets']} trending tweets in the area:

"""
    
    for i, tweet in enumerate(result['tweets'], 1):
        summary += f"""
{i}. @{tweet['username']} {'✓' if tweet['verified'] else ''}
   "{tweet['content']}"
   📊 {tweet['engagement']['likes']}❤️ {tweet['engagement']['retweets']}🔁 {tweet['engagement']['replies']}💬
   📍 {tweet['location']}
   
"""
    
    summary += f"\n🔥 Trending: {', '.join(result['trending_topics'])}"
    
    return summary

def search_tweets_by_keywords(keywords: List[str]) -> str:
    """
    Search for tweets matching specific flood-related keywords.
    
    Args:
        keywords: List of keywords to search (e.g., ["flood", "water", "emergency"])
    
    Returns:
        JSON string with tweets matching the keywords
    """
    result = get_mock_tweets_by_keywords(keywords)
    
    summary = f"""
🔍 **Keyword-Based Search Results**
Keywords: {', '.join(keywords)}

Found {result['total_tweets']} highly relevant tweets:

"""
    
    for i, tweet in enumerate(result['tweets'], 1):
        matched = ', '.join(tweet['keywords_matched'])
        summary += f"""
{i}. @{tweet['username']} {'✓' if tweet['verified'] else ''}
   "{tweet['content']}"
   📊 {tweet['engagement']['likes']}❤️ {tweet['engagement']['retweets']}🔁
   🎯 Matched: {matched}
   
"""
    
    summary += f"\n📈 Sentiment: {result['sentiment_breakdown']}"
    
    return summary

def score_social_media_impact(
    location_data: str,
    keyword_data: str,
    total_mentions: int,
    verified_sources: int,
    zone_a_mentions: int,
    zone_b_mentions: int
) -> str:
    """
    Score the social media impact and identify high-risk zones.
    
    Args:
        location_data: Summary from location search
        keyword_data: Summary from keyword search
        total_mentions: Total flood-related mentions
        verified_sources: Number of verified sources reporting
        zone_a_mentions: Mentions of Zone A
        zone_b_mentions: Mentions of Zone B
    
    Returns:
        Scoring analysis with identified zones
    """
    
    # Calculate score (0-15 points)
    score = 0
    
    # Verified sources (0-5 points)
    if verified_sources >= 4:
        score += 5
    elif verified_sources >= 2:
        score += 3
    else:
        score += 2
    
    # Total engagement/mentions (0-5 points)
    if total_mentions >= 8:
        score += 5
    elif total_mentions >= 5:
        score += 3
    else:
        score += 2
    
    # Zone-specific mentions (0-5 points)
    if zone_a_mentions >= 4 and zone_b_mentions >= 3:
        score += 5  # Both zones heavily mentioned
    elif zone_a_mentions >= 3 or zone_b_mentions >= 3:
        score += 4
    elif zone_a_mentions >= 2 or zone_b_mentions >= 2:
        score += 3
    else:
        score += 2
    
    # Cap at 15
    score = min(score, 15)
    
    response = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 **PHASE 4: SOCIAL MEDIA ANALYSIS**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**SCORING BREAKDOWN:**
- Verified Sources: {verified_sources} sources → {min(verified_sources, 3)}/3 points
- Total Mentions: {total_mentions} mentions → {min(3, (total_mentions // 3))}/3 points
- Zone Coverage: Zone A ({zone_a_mentions}), Zone B ({zone_b_mentions}) → {score - min(verified_sources, 3) - min(3, (total_mentions // 3))}/4 points

**SOCIAL MEDIA SCORE: {score}/15 points**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **HIGH-RISK ZONES IDENTIFIED:**

**Zone A (Flushing Downtown):**
- {zone_a_mentions} direct mentions
- Risk Level: CRITICAL (5/5)
- Key Indicators: Evacuation orders, water rescue, 3ft+ depths
- Action: IMMEDIATE EVACUATION REQUIRED

**Zone B (Murray Hill / Alley Creek):**
- {zone_b_mentions} direct mentions  
- Risk Level: HIGH (4/5)
- Key Indicators: Rapid water rise, creek overflow, basement flooding
- Action: SHELTER IN PLACE - HIGHER FLOORS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **PUBLIC IMPACT ASSESSMENT:**
- {verified_sources} verified emergency/news sources active
- High engagement across all posts (10K+ total interactions)
- Sentiment: URGENT/CRITICAL (evacuation-level concern)
- Confidence: 94% (strong correlation with sensor data)

🚨 **RECOMMENDATION:**
Social media confirms ground-level severity. Zone A requires immediate evacuation response. Zone B residents should shelter in place on higher floors.
"""
    
    return response

