"""
Unit tests for the Customer Support Agent
Run with: pytest tests/test_agent.py -v
"""

import pytest
from src.agent import CustomerSupportAgent
from src.config import settings

class TestCustomerSupportAgent:
    """Test suite for CustomerSupportAgent"""
    
    @pytest.fixture
    def agent(self):
        """Create an agent instance for testing"""
        return CustomerSupportAgent()
    
    def test_agent_initialization(self, agent):
        """Test that agent initializes correctly"""
        assert agent is not None
        assert agent.client is not None
        assert agent.conversations == {}
    
    def test_handle_query_basic(self, agent):
        """Test basic query handling"""
        response = agent.handle_query("Hello", "test_user_1")
        assert isinstance(response, str)
        assert len(response) > 0
        assert "test_user_1" in agent.conversations
    
    def test_conversation_memory(self, agent):
        """Test that conversation history is maintained"""
        agent.handle_query("My name is John", "test_user_2")
        response = agent.handle_query("What's my name?", "test_user_2")
        
        assert "john" in response.lower()
        assert len(agent.conversations["test_user_2"]) >= 4  # 2 queries + 2 responses
    
    def test_multiple_users(self, agent):
        """Test handling multiple users separately"""
        agent.handle_query("I like laptops", "user_a")
        agent.handle_query("I like phones", "user_b")
        
        assert "user_a" in agent.conversations
        assert "user_b" in agent.conversations
        assert len(agent.conversations["user_a"]) >= 2
        assert len(agent.conversations["user_b"]) >= 2
    
    def test_get_user_memories(self, agent):
        """Test retrieving user memories"""
        agent.handle_query("Test query", "test_user_3")
        memories = agent.get_user_memories("test_user_3")
        
        assert isinstance(memories, list)
        assert len(memories) >= 2  # At least query and response
    
    def test_get_memories_nonexistent_user(self, agent):
        """Test getting memories for non-existent user"""
        memories = agent.get_user_memories("nonexistent_user")
        assert memories == []
    
    def test_generate_synthetic_profile(self, agent):
        """Test synthetic profile generation"""
        profile = agent.generate_synthetic_profile("test_user_4")
        
        assert profile is not None
        assert isinstance(profile, dict)
        # Profile should have some basic fields
        assert len(profile) > 0
    
    def test_error_handling_empty_query(self, agent):
        """Test handling of empty queries"""
        response = agent.handle_query("", "test_user_5")
        assert isinstance(response, str)
    
    def test_conversation_context_limit(self, agent):
        """Test that conversation history is limited"""
        # Send 15 messages
        for i in range(15):
            agent.handle_query(f"Message {i}", "test_user_6")
        
        # Should only keep last 10 messages in context (20 total with responses)
        assert len(agent.conversations["test_user_6"]) == 30  # 15 queries + 15 responses


class TestAnalytics:
    """Test suite for Analytics"""
    
    @pytest.fixture
    def analytics_tracker(self):
        """Create a fresh analytics tracker"""
        from src.analytics import AnalyticsTracker
        return AnalyticsTracker()
    
    def test_log_interaction(self, analytics_tracker):
        """Test logging an interaction"""
        analytics_tracker.log_interaction(
            user_id="user1",
            query="test query",
            response="test response",
            response_time=0.5
        )
        
        assert len(analytics_tracker.interactions) == 1
        assert analytics_tracker.user_stats["user1"]["total_queries"] == 1
    
    def test_summary_stats(self, analytics_tracker):
        """Test summary statistics"""
        analytics_tracker.log_interaction("user1", "q1", "r1", 0.5)
        analytics_tracker.log_interaction("user2", "q2", "r2", 0.3)
        
        stats = analytics_tracker.get_summary_stats()
        
        assert stats["total_interactions"] == 2
        assert stats["unique_users"] == 2
        assert stats["avg_response_time"] > 0
    
    def test_user_stats(self, analytics_tracker):
        """Test user-specific statistics"""
        analytics_tracker.log_interaction("user1", "q1", "r1", 0.5)
        analytics_tracker.log_interaction("user1", "q2", "r2", 0.3)
        
        user_stats = analytics_tracker.get_user_stats("user1")
        
        assert user_stats["total_queries"] == 2
        assert user_stats["avg_response_time"] > 0
    
    def test_top_users(self, analytics_tracker):
        """Test top users ranking"""
        analytics_tracker.log_interaction("user1", "q", "r", 0.1)
        analytics_tracker.log_interaction("user2", "q", "r", 0.1)
        analytics_tracker.log_interaction("user2", "q", "r", 0.1)
        analytics_tracker.log_interaction("user3", "q", "r", 0.1)
        analytics_tracker.log_interaction("user3", "q", "r", 0.1)
        analytics_tracker.log_interaction("user3", "q", "r", 0.1)
        
        top_users = analytics_tracker.get_top_users(limit=2)
        
        assert len(top_users) == 2
        assert top_users[0]["user_id"] == "user3"
        assert top_users[0]["total_queries"] == 3
