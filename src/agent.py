import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from groq import Groq

from src.config import settings
from src.utils import logger

class CustomerSupportAgent:
    """Core logic for the AI Customer Support Agent with simple memory (using Groq)."""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or fallback to settings
        key = api_key or settings.GROQ_API_KEY
        if not key:
            raise ValueError("Groq API Key is required.")
        
        self.client = Groq(api_key=key)
        self.app_id = settings.APP_ID
        
        # Simple in-memory storage for conversations
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        logger.info("Agent initialized successfully with Groq.")

    def handle_query(self, query: str, user_id: str) -> str:
        """Handles a customer query by retrieving conversation history and generating a response."""
        try:
            logger.info(f"Handling query for user {user_id}: {query[:50]}...")
            
            # Get or create conversation history for this user
            if user_id not in self.conversations:
                self.conversations[user_id] = []
            
            # Build messages from conversation history
            messages = [
                {"role": "system", "content": """You are an expert customer support AI for TechGadgets.com, a premium online electronics retailer.

Your personality:
- Professional yet warm and friendly
- Patient and empathetic
- Solution-oriented
- Knowledgeable about tech products

Your capabilities:
- Help with order tracking, returns, and product recommendations
- Troubleshoot technical issues
- Answer questions about warranties and shipping
- Remember conversation context to provide personalized help

Guidelines:
- Keep responses concise but complete (2-3 sentences ideal)
- Use a conversational, natural tone
- If you don't have specific information, acknowledge it honestly and offer to help in other ways
- Always end with a helpful follow-up question or offer when appropriate"""}
            ]
            
            # Add conversation history (last 10 messages to keep context manageable)
            for msg in self.conversations[user_id][-10:]:
                messages.append(msg)
            
            # Add current query
            messages.append({"role": "user", "content": query})
            
            # Generate response via Groq
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=messages
            )
            
            answer = response.choices[0].message.content
            
            # Store interaction in conversation history
            self.conversations[user_id].append({"role": "user", "content": query})
            self.conversations[user_id].append({"role": "assistant", "content": answer})
            
            return answer
            
        except Exception as e:
            logger.error(f"Error in handle_query: {e}")
            return "I'm sorry, I'm having trouble processing your request. Please try again later."

    def get_user_memories(self, user_id: str) -> List[str]:
        """Retrieves conversation history for a user."""
        try:
            if user_id in self.conversations:
                return [f"{msg['role']}: {msg['content']}" for msg in self.conversations[user_id]]
            return []
        except Exception as e:
            logger.error(f"Failed to fetch memories for {user_id}: {e}")
            return []

    def generate_synthetic_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Generates a realistic customer profile."""
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
            
            # Store profile in conversation as context
            profile_msg = f"Customer Profile: {json.dumps(customer_data)}"
            if user_id not in self.conversations:
                self.conversations[user_id] = []
            self.conversations[user_id].insert(0, {"role": "system", "content": profile_msg})

            return customer_data
        except Exception as e:
            logger.error(f"Profile generation failed: {e}")
            return None
