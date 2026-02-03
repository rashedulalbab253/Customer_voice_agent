import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from groq import Groq
from mem0 import Memory

from src.config import settings
from src.utils import logger

class CustomerSupportAgent:
    """Core logic for the AI Customer Support Agent with memory (using Groq)."""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or fallback to settings
        key = api_key or settings.GROQ_API_KEY
        if not key:
            raise ValueError("Groq API Key is required.")
        
        self.client = Groq(api_key=key)
        self.app_id = settings.APP_ID
        
        # Initialize Memory (Mem0) with Qdrant
        config = {
            "vector_store": {
                "provider": settings.MEMORY_PROVIDER,
                "config": {
                    "host": settings.QDRANT_HOST,
                    "port": settings.QDRANT_PORT,
                }
            },
            "llm": {
                "provider": "groq",
                "config": {
                    "api_key": key,
                    "model": settings.GROQ_MODEL
                }
            }
        }
        
        try:
            self.memory = Memory.from_config(config)
            logger.info("Memory initialized successfully with Qdrant and Groq.")
        except Exception as e:
            logger.error(f"Failed to initialize memory: {e}")
            raise

    def handle_query(self, query: str, user_id: str) -> str:
        """Handles a customer query by retrieving memory context and generating a response."""
        try:
            logger.info(f"Handling query for user {user_id}: {query[:50]}...")
            
            # Search for relevant memories
            relevant_memories = self.memory.search(query=query, user_id=user_id)
            
            # Build context from relevant memories
            context = "Relevant past information:\n"
            if relevant_memories and "results" in relevant_memories:
                for memory in relevant_memories["results"]:
                    if "memory" in memory:
                        context += f"- {memory['memory']}\n"

            # Generate response via Groq
            messages = [
                {"role": "system", "content": "You are a professional customer support AI agent for TechGadgets.com. Use the provided context to give personalized help."},
                {"role": "user", "content": f"{context}\nCustomer Query: {query}"}
            ]
            
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages
            )
            
            answer = response.choices[0].message.content
            
            # Store interaction in memory
            self.memory.add(query, user_id=user_id, metadata={"app_id": self.app_id, "role": "user"})
            self.memory.add(answer, user_id=user_id, metadata={"app_id": self.app_id, "role": "assistant"})
            
            return answer
            
        except Exception as e:
            logger.error(f"Error in handle_query: {e}")
            return "I'm sorry, I'm having trouble processing your request. Please try again later."

    def get_user_memories(self, user_id: str) -> List[str]:
        """Retrieves all memories associated with a user."""
        try:
            memories = self.memory.get_all(user_id=user_id)
            if memories and "results" in memories:
                return [m['memory'] for m in memories["results"] if 'memory' in m]
            return []
        except Exception as e:
            logger.error(f"Failed to fetch memories for {user_id}: {e}")
            return []

    def generate_synthetic_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Generates a realistic customer profile and seeds the memory."""
        try:
            logger.info(f"Generating synthetic profile for user {user_id}")
            today = datetime.now()
            order_date = (today - timedelta(days=10)).strftime("%B %d, %Y")
            expected_delivery = (today + timedelta(days=2)).strftime("%B %d, %Y")

            prompt = f"""Generate a detailed JSON customer profile for ID {user_id}. Include:
            - Basic Info (Name, Email)
            - Recent high-end electronics order (Placed: {order_date}, Delivery: {expected_delivery})
            - 2 past orders and 2 previous support interactions.
            Return ONLY valid JSON."""

            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[{"role": "system", "content": "You are a data generation tool. Return ONLY the JSON object."},
                          {"role": "user", "content": prompt}]
            )

            # Clean the response in case Groq adds markdown formatting
            content = response.choices[0].message.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            customer_data = json.loads(content)

            # Seed memory with this data
            for key, value in customer_data.items():
                content_val = json.dumps(value) if isinstance(value, (list, dict)) else f"{key}: {value}"
                self.memory.add(content_val, user_id=user_id, metadata={"app_id": self.app_id, "role": "system"})

            return customer_data
        except Exception as e:
            logger.error(f"Profile generation failed: {e}")
            return None
