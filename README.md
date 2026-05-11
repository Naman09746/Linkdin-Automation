# 🚀 LinkedIn AI Personal Branding Agent

A fully automated agent that scours the web for tech news, drafts engaging LinkedIn posts, generates cinematic visuals, and publishes them for you.

## 🛠️ System Architecture
1.  **Signal Ingestion:** Scrapes Hacker News, ArXiv, and GitHub Trending (Last 24h).
2.  **AI Routing:** Uses a free multi-LLM router (Groq, Gemini, Cerebras) for high-speed scoring and drafting.
3.  **Drafting Engine:** Generates posts in your specific 21yo AI/ML student persona.
4.  **Visual Engine:** Captures genuine source screenshots wrapped in a **macOS Dark Mode frame**.
5.  **Notifications:** Sends Telegram/Discord alerts when new drafts are ready.
6.  **Web Dashboard:** One-click review & approval via Streamlit.
7.  **Publishing:** Automated LinkedIn v2023 API integration.

## 🚀 Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configuration
Fill in your API keys in `.env` (Groq, Gemini, Supabase, LinkedIn, Telegram/Discord).

### 3. Run the Agent
```bash
export PYTHONPATH=.
python src/main.py --limit 3
```
*This will fetch news, score them, write drafts, capture macOS-framed screenshots, and **send a notification to your phone**.*

### 4. Review via Web Dashboard
```bash
# 1. Start the API
uvicorn src.api.dashboard:app --reload

# 2. Start the Dashboard (in a new terminal)
streamlit run dashboard/app.py
```
*Open http://localhost:8501 to review and approve your posts with one click.*

### 5. Publish to LinkedIn
```bash
python src/core/publisher.py
```
*Posts all approved drafts with their genuine screenshots.*

## 📁 Project Structure
- `src/main.py`: Main entry point.
- `src/ingestion/`: API and Scraper-based news collectors.
- `src/core/drafter.py`: Content generation logic.
- `src/core/visuals.py`: AI image generation and storage.
- `src/core/publisher.py`: LinkedIn API integration.
- `scripts/approve.py`: Manual review tool.

## ⚖️ License
[PRIVACY.md](PRIVACY.md) | [TERMS.md](TERMS.md)