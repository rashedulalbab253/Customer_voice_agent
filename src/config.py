import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration."""
    APP_NAME: str = "AI Customer Support Agent"
    APP_ID: str = "customer-support-pro"
    
    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama3-8b-8192"
    
    # Qdrant Configuration
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", 6333))
    
    # Memory Configuration
    MEMORY_PROVIDER: str = "qdrant"

    class Config:
        env_file = ".env"

settings = Settings()
