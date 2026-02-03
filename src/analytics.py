import json
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
import statistics

class AnalyticsTracker:
    """Tracks and analyzes agent interactions for insights."""
    
    def __init__(self):
        self.interactions: List[Dict] = []
        self.user_stats: Dict[str, Dict] = defaultdict(lambda: {
            "total_queries": 0,
            "total_response_time": 0,
            "queries": []
        })
    
    def log_interaction(self, user_id: str, query: str, response: str, 
                       response_time: float, timestamp: Optional[datetime] = None):
        """Log a single interaction."""
        if timestamp is None:
            timestamp = datetime.now()
        
        interaction = {
            "user_id": user_id,
            "query": query,
            "response": response,
            "response_time": response_time,
            "timestamp": timestamp.isoformat(),
            "query_length": len(query),
            "response_length": len(response)
        }
        
        self.interactions.append(interaction)
        
        # Update user stats
        self.user_stats[user_id]["total_queries"] += 1
        self.user_stats[user_id]["total_response_time"] += response_time
        self.user_stats[user_id]["queries"].append(query)
    
    def get_summary_stats(self) -> Dict:
        """Get overall analytics summary."""
        if not self.interactions:
            return {
                "total_interactions": 0,
                "unique_users": 0,
                "avg_response_time": 0,
                "avg_query_length": 0,
                "avg_response_length": 0
            }
        
        response_times = [i["response_time"] for i in self.interactions]
        query_lengths = [i["query_length"] for i in self.interactions]
        response_lengths = [i["response_length"] for i in self.interactions]
        
        return {
            "total_interactions": len(self.interactions),
            "unique_users": len(self.user_stats),
            "avg_response_time": round(statistics.mean(response_times), 3),
            "min_response_time": round(min(response_times), 3),
            "max_response_time": round(max(response_times), 3),
            "avg_query_length": round(statistics.mean(query_lengths), 1),
            "avg_response_length": round(statistics.mean(response_lengths), 1)
        }
    
    def get_user_stats(self, user_id: str) -> Dict:
        """Get stats for a specific user."""
        if user_id not in self.user_stats:
            return {"error": "User not found"}
        
        stats = self.user_stats[user_id]
        return {
            "user_id": user_id,
            "total_queries": stats["total_queries"],
            "avg_response_time": round(
                stats["total_response_time"] / stats["total_queries"], 3
            ) if stats["total_queries"] > 0 else 0,
            "recent_queries": stats["queries"][-5:]  # Last 5 queries
        }
    
    def get_recent_interactions(self, limit: int = 10) -> List[Dict]:
        """Get most recent interactions."""
        return self.interactions[-limit:]
    
    def get_top_users(self, limit: int = 5) -> List[Dict]:
        """Get most active users."""
        sorted_users = sorted(
            self.user_stats.items(),
            key=lambda x: x[1]["total_queries"],
            reverse=True
        )[:limit]
        
        return [
            {
                "user_id": user_id,
                "total_queries": stats["total_queries"]
            }
            for user_id, stats in sorted_users
        ]

# Global analytics instance
analytics = AnalyticsTracker()
