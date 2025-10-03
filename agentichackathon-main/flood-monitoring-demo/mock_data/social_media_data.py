"""Mock social media data for flood monitoring."""

from datetime import datetime, timedelta
import random

def get_mock_tweets_by_zipcode(zipcode: str) -> dict:
    """Get mock trending tweets near a zipcode."""
    
    # Mock tweets for zipcode area
    tweets = [
        {
            "tweet_id": "1234567890",
            "username": "@FlushingResident",
            "content": "Water levels rising fast on 41st Ave near Flushing Creek! Street flooding already started. Stay safe everyone! #Flooding #Flushing",
            "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "location": "Flushing, Queens (ZIP: 11375)",
            "engagement": {
                "likes": 847,
                "retweets": 312,
                "replies": 89
            },
            "verified": True,
            "sentiment": "urgent"
        },
        {
            "tweet_id": "1234567891",
            "username": "@NYCWeatherWatch",
            "content": "🚨 FLOOD ALERT: Northern Queens seeing rapid water accumulation. Residents in 11375 zone report basements flooding. Avoid low-lying areas!",
            "timestamp": (datetime.now() - timedelta(minutes=22)).isoformat(),
            "location": "Queens, NY (ZIP: 11375)",
            "engagement": {
                "likes": 1523,
                "retweets": 892,
                "replies": 234
            },
            "verified": True,
            "sentiment": "warning"
        },
        {
            "tweet_id": "1234567892",
            "username": "@QueensLocal",
            "content": "Main Street intersection completely flooded. Cars stalled in water. Emergency services on scene. #Queens #FloodEmergency",
            "timestamp": (datetime.now() - timedelta(minutes=8)).isoformat(),
            "location": "Main St, Flushing (ZIP: 11375)",
            "engagement": {
                "likes": 634,
                "retweets": 201,
                "replies": 67
            },
            "verified": False,
            "sentiment": "critical"
        },
        {
            "tweet_id": "1234567893",
            "username": "@EmergencyNYC",
            "content": "FDNY responding to multiple water rescue calls in Zone A (Flushing) and Zone B (Murray Hill). Please stay indoors if you're in these areas.",
            "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
            "location": "Queens, NY",
            "engagement": {
                "likes": 2134,
                "retweets": 1456,
                "replies": 456
            },
            "verified": True,
            "sentiment": "emergency"
        },
        {
            "tweet_id": "1234567894",
            "username": "@LocalNewsQNS",
            "content": "Breaking: Flushing Creek has overflowed its banks. Neighborhoods near Northern Blvd experiencing severe flooding. Evacuation orders expected.",
            "timestamp": (datetime.now() - timedelta(minutes=3)).isoformat(),
            "location": "Flushing, Queens",
            "engagement": {
                "likes": 1876,
                "retweets": 967,
                "replies": 345
            },
            "verified": True,
            "sentiment": "breaking"
        }
    ]
    
    return {
        "zipcode": zipcode,
        "total_tweets": 5,
        "search_type": "location_based",
        "tweets": tweets,
        "trending_topics": ["#Flooding", "#Queens", "#FloodEmergency", "#Flushing"],
        "query_time": datetime.now().isoformat()
    }

def get_mock_tweets_by_keywords(keywords: list) -> dict:
    """Get mock tweets matching flood-related keywords."""
    
    # Mock tweets for keyword search
    tweets = [
        {
            "tweet_id": "1234567895",
            "username": "@FloodAlertNY",
            "content": "⚠️ Zone A (Flushing Downtown): Water 3ft deep on major roads. DO NOT DRIVE. Zone B (Murray Hill): Rapidly rising water near creek.",
            "timestamp": (datetime.now() - timedelta(minutes=12)).isoformat(),
            "location": "Queens, NY",
            "engagement": {
                "likes": 3421,
                "retweets": 2134,
                "replies": 789
            },
            "verified": True,
            "sentiment": "critical",
            "keywords_matched": ["flood", "water", "zone"]
        },
        {
            "tweet_id": "1234567896",
            "username": "@ResidentQNS",
            "content": "My basement just flooded in 5 minutes! Water coming up from drains. This is insane. Never seen it this bad. #flooding #emergency",
            "timestamp": (datetime.now() - timedelta(minutes=18)).isoformat(),
            "location": "Murray Hill, Queens",
            "engagement": {
                "likes": 892,
                "retweets": 456,
                "replies": 123
            },
            "verified": False,
            "sentiment": "panic",
            "keywords_matched": ["flooded", "water", "emergency"]
        },
        {
            "tweet_id": "1234567897",
            "username": "@NYCEmergency",
            "content": "URGENT: Zone A residents - evacuate immediately. Water levels critical. Zone B - shelter in place, move to higher floors. #FloodEvacuation",
            "timestamp": (datetime.now() - timedelta(minutes=6)).isoformat(),
            "location": "NYC Emergency Management",
            "engagement": {
                "likes": 5678,
                "retweets": 4321,
                "replies": 1234
            },
            "verified": True,
            "sentiment": "evacuation",
            "keywords_matched": ["emergency", "water", "flood", "zone"]
        },
        {
            "tweet_id": "1234567898",
            "username": "@WeatherChannel",
            "content": "Northern Queens flood situation deteriorating rapidly. Zone A & B under severe flood warning. 120mm+ rainfall in 2 hours. Life-threatening.",
            "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(),
            "location": "Queens, NY",
            "engagement": {
                "likes": 4523,
                "retweets": 3421,
                "replies": 987
            },
            "verified": True,
            "sentiment": "severe",
            "keywords_matched": ["flood", "water", "zone"]
        },
        {
            "tweet_id": "1234567899",
            "username": "@QueensCommunity",
            "content": "Neighbors helping neighbors in Zone B. If you need help evacuating, call 911. Water rescue teams deployed to Zone A. Stay strong Queens! 💙",
            "timestamp": (datetime.now() - timedelta(minutes=4)).isoformat(),
            "location": "Queens, NY",
            "engagement": {
                "likes": 2345,
                "retweets": 1234,
                "replies": 567
            },
            "verified": False,
            "sentiment": "community",
            "keywords_matched": ["water", "zone"]
        }
    ]
    
    return {
        "keywords": keywords,
        "total_tweets": 5,
        "search_type": "keyword_based",
        "tweets": tweets,
        "sentiment_breakdown": {
            "critical": 2,
            "severe": 1,
            "urgent": 1,
            "community": 1
        },
        "query_time": datetime.now().isoformat()
    }

def analyze_affected_zones(location_tweets: dict, keyword_tweets: dict) -> dict:
    """Analyze tweets to identify high-risk zones."""
    
    # Mock zone analysis
    zones = {
        "Zone A": {
            "name": "Flushing Downtown",
            "coordinates": {"lat": 40.7614, "lon": -73.8303},
            "mentions": 8,
            "risk_level": "CRITICAL",
            "risk_value": 5,
            "top_keywords": ["flooded", "water rescue", "evacuation"],
            "verified_reports": 4,
            "engagement_score": 12456,
            "severity_indicators": [
                "Multiple evacuation orders",
                "Water rescue operations active",
                "3ft+ water depth reported",
                "Major road closures"
            ]
        },
        "Zone B": {
            "name": "Murray Hill / Alley Creek",
            "coordinates": {"lat": 40.7455, "lon": -73.8184},
            "mentions": 6,
            "risk_level": "HIGH",
            "risk_value": 4,
            "top_keywords": ["rising water", "flooding", "shelter"],
            "verified_reports": 3,
            "engagement_score": 8934,
            "severity_indicators": [
                "Rapidly rising water levels",
                "Basement flooding widespread",
                "Creek overflow confirmed",
                "Shelter in place orders"
            ]
        }
    }
    
    return {
        "zones": zones,
        "high_risk_zones": ["Zone A", "Zone B"],
        "total_zones_affected": 2,
        "analysis_confidence": 0.94,
        "recommendation": "Immediate evacuation of Zone A, shelter-in-place for Zone B"
    }

