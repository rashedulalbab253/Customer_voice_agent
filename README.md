# 🤖 AI Customer Support Agent (Industry Standard)

A professional-grade customer support assistant built with **Python**, **Streamlit**, and **Mem0** for long-term memory retrieval.

## 🚀 Features
- **Long-term Memory**: Remembers user preferences and past issues using Mem0 and Qdrant.
- **Modular Architecture**: Clean separation between AI logic and UI.
- **Production Ready**: Fully containerized with Docker and Docker Compose.
- **Synthetic Data Generation**: Automatically seed user profiles for testing.
- **Config Management**: Uses Pydantic and `.env` for secure credential handling.

## 🛠️ Tech Stack
- **Framework**: FastAPI
- **AI Model**: Groq (Llama 3)
- **Memory Buffer**: Mem0
- **Vector DB**: Qdrant
- **DevOps**: Docker, Docker Compose

## 📦 Getting Started

### 1. Prerequisite
- Docker & Docker Compose installed.
- Groq API Key (Fast and free/cheap).

### 2. Configuration
Copy the example environment file and fill in your keys:
```bash
cp .env.example .env
```

### 3. Run with Docker (Recommended)
This will set up both the application and the Qdrant database automatically.
```bash
docker-compose up --build
```
Access the app at `http://localhost:8501`.

### 4. Run Locally
If you prefer running without Docker:
1. Start Qdrant locally (on port 6333).
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the app: `streamlit run app.py`

## 📂 Project Structure
- `src/agent.py`: Core AI logic.
- `src/config.py`: Global settings.
- `src/utils.py`: Logging and helpers.
- `app.py`: Streamlit frontend.
- `docker-compose.yml`: Infrastructure orchestration.
```
