# 🦜🔊 Customer Support Voice Agent

## 🚀 Introduction

**Customer Support Voice Agent** is a state-of-the-art AI-powered assistant that transforms your documentation into an interactive, voice-accessible knowledge base. Users can query any documentation and receive instant, contextually accurate responses, delivered both as clear text and high-quality synthesized speech.

With seamless integration of leading AI, vector search, and web technologies, this tool is ideal for developer support, product documentation, onboarding, and any scenario where accessible answers are paramount.

---

## 🎯 Features

- **Automated Documentation Crawling:** Easily ingest any public documentation URL. The system crawls, extracts, and processes your docs.
- **Semantic Search (Vector Database):** Retrieves the most relevant information using Qdrant and fast, robust embeddings.
- **Conversational AI Responses:** Utilizes OpenAI GPT-4o for accurate, natural, and context-rich answers.
- **Text-to-Speech Synthesis:** Transforms answers into natural-sounding speech using OpenAI's advanced voice models.
- **Modern Streamlit UI:** Clean, interactive interface for configuration and Q&A.
- **Audio Download & Source Attribution:** Listen to responses or download MP3s. View referenced documentation links for transparency.

---

## 🏗️ Architecture Overview

```mermaid
flowchart TD
    User[User: asks question] -->|Web UI| Streamlit[Streamlit App]
    Streamlit -->|Crawl| Firecrawl[Firecrawl: Crawl Docs]
    Firecrawl -->|Docs| Embeddings[fastembed: Create Embeddings]
    Embeddings -->|Vectors| Qdrant[Qdrant: Vector DB]
    Streamlit -->|User Query| Embeddings
    Embeddings -->|Query Vector| Qdrant
    Qdrant -->|Relevant Docs| OpenAIQA[Processor Agent (OpenAI GPT-4o)]
    OpenAIQA -->|Answer| OpenAITTS[TTS Agent (OpenAI TTS)]
    OpenAITTS -->|Audio| Streamlit
    Streamlit -->|Text, Audio, Sources| User
```

---

## ⚡ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/yourusername/customer-support-voice-agent.git
cd customer-support-voice-agent
pip install -r requirements.txt
```

### 2. Obtain API Keys

- [OpenAI API Key](https://platform.openai.com/)
- [Qdrant API Key & URL](https://qdrant.tech/)
- [Firecrawl API Key](https://firecrawl.dev/)

### 3. Configure Environment Variables

You can enter keys in the Streamlit sidebar, or create a `.env` file:

```
QDRANT_URL=https://your-qdrant-instance.com
QDRANT_API_KEY=your_qdrant_key
FIRECRAWL_API_KEY=your_firecrawl_key
OPENAI_API_KEY=your_openai_key
```

### 4. Launch the Application

```bash
streamlit run app.py
```

If using Google Colab or a remote environment, run:

```bash
npx localtunnel --port 8501
```
to generate a public access link.

---

## 🕹️ Usage Guide

1. **Configure:** Input your API keys, Qdrant settings, the documentation URL, and select a preferred voice in the sidebar.
2. **Initialize:** Click "Initialize System" to crawl the docs and set up the knowledge base.
3. **Ask Questions:** Enter any documentation-related question in the main panel.
4. **Receive Answers:**
   - **Text:** Displayed directly on the page.
   - **Audio:** Listen instantly or download as MP3.
   - **Sources:** All referenced URLs are transparently displayed.

---

## 🛠️ Technology Stack

- **Python & Streamlit:** For web interface and orchestration.
- **OpenAI GPT-4o & TTS:** For language understanding and voice synthesis.
- **Qdrant:** High-performance vector search engine.
- **fastembed:** Efficient text embedding.
- **Firecrawl:** Automated documentation crawling.
- **localtunnel:** Public sharing of your Streamlit app.

---

## 🌟 Benefits

- **Enhanced Support:** Deliver instant, context-aware support for APIs, SaaS, developer tools, or internal docs.
- **Accessibility:** Make documentation usable for visually impaired users or those who prefer audio.
- **Transparency:** Each answer is sourced and cited for trust and verification.
- **Customizable:** Easily adapt for any documentation, voice, or AI model.

---

## 🔍 Example Use Cases

- **API Support Chatbot:** Users ask, “How do I authenticate?” and receive spoken/text answers sourced from your API docs.
- **Product Training Assistant:** Onboard new users with interactive, voice-driven answers.
- **Internal Knowledge Base:** Empower teams to query and hear company playbooks or policies.

---

## 📂 Project Structure

```
.
├── app.py         # Main Streamlit application
├── Customer_support_voice_agent.ipynb  # Jupyter/Colab version
├── requirements.txt
├── README.md
└── .env.example   # Environment variable template
```

---

## 🧠 Advanced Customization

- **Add More Voices:** Update the selectable list in the sidebar.
- **Index Additional Docs:** Modify the crawl limit or add more URLs.
- **Switch AI Models:** Edit agent setup to leverage new OpenAI models.
- **Deployment:** Deploy on Heroku, HuggingFace Spaces, or your preferred cloud platform.

---

## 💡 Tips & Best Practices

- For private documentation, consider running Firecrawl locally or uploading files directly.
- Monitor usage of OpenAI and Qdrant for quotas and billing.
- For extensive documentation, increase the crawl/page limit in `crawl_documentation`.

---

## 🤝 Acknowledgements

- [OpenAI](https://openai.com/)
- [Qdrant](https://qdrant.tech/)
- [Firecrawl](https://firecrawl.dev/)
- [Streamlit](https://streamlit.io/)

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

[Rashedul Albab](https://github.com/rashedulalbab253) | [LinkedIn](https://www.linkedin.com/in/rashedul-albab-91a50b2ab/)

---

> **Empower your documentation with voice! Fork, star, and deploy your own Customer Support Voice Agent today.**
