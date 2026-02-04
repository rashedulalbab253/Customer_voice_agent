import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    """Application settings and configuration."""
    APP_NAME: str = "OmniServe AI"
    APP_ID: str = "omniserve-voice-platform"
    
    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
