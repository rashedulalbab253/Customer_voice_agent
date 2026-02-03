from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os

from src.agent import CustomerSupportAgent
from src.config import settings
from src.utils import logger

app = FastAPI(title="TechGadgets AI Support API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agent
# In a real production environment, you might use a dependency 
# or a singleton pattern.
agent = None

def get_agent(api_key: Optional[str] = None):
    global agent
    if agent is None or api_key:
        try:
            agent = CustomerSupportAgent(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    return agent

class ChatQuery(BaseModel):
    query: str
    user_id: str
    api_key: Optional[str] = None

class ProfileRequest(BaseModel):
    user_id: str
    api_key: Optional[str] = None

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/chat")
async def chat(data: ChatQuery):
    try:
        current_agent = get_agent(data.api_key)
        response = current_agent.handle_query(data.query, user_id=data.user_id)
        return {"response": response}
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-profile")
async def generate_profile(data: ProfileRequest):
    try:
        current_agent = get_agent(data.api_key)
        profile = current_agent.generate_synthetic_profile(data.user_id)
        if profile:
            return profile
        else:
            raise HTTPException(status_code=500, detail="Failed to generate profile")
    except Exception as e:
        logger.error(f"Profile generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/memories/{user_id}")
async def get_memories(user_id: str):
    try:
        current_agent = get_agent()
        memories = current_agent.get_user_memories(user_id)
        return {"memories": memories}
    except Exception as e:
        logger.error(f"Memory retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
