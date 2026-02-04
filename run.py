import uvicorn
import os
import sys

# Add the current directory to sys.path to ensure 'src' is found correctly
# even if run from outside the root directory.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting OmniServe AI: Voice Support Platform...")
    print("📍 URL: http://localhost:8000")
    print("Press Ctrl+C to stop the server.")
    
    # Run the FastAPI app using uvicorn
    # We use the string import 'app:app' for the root app.py
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
