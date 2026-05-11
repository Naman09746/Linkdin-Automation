# 🚀 LinkedIn AI Personal Branding Agent

A fully automated agent that scours the web for tech news, drafts engaging LinkedIn posts, generates cinematic visuals, and publishes them for you.

## 🛠️ System Architecture
1.  **Signal Ingestion:** Scrapes Hacker News, ArXiv, and GitHub Trending.
2.  **AI Routing:** Uses a free multi-LLM router (Groq, Gemini, Cerebras) for high-speed scoring and drafting.
3.  **Drafting Engine:** Generates 3 versions of every post (PAS, HVCTA, SLA styles).
4.  **Visual Engine:** Uses Hugging Face SDXL to generate $0-cost professional images.
5.  **Database & Asset Management:** Powered by Supabase (Postgres + Storage).
6.  **Human-in-the-Loop:** Approval workflow via CLI.
7.  **Publishing:** Automated LinkedIn v2023 API integration.

## 🚀 Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
playwright install
```

### 2. Configuration
Fill in your API keys in `.env` (Groq, Gemini, Supabase, Hugging Face, LinkedIn).

### 3. Run the Automation
```bash
export PYTHONPATH=.
python src/main.py --limit 3
```
*This will fetch news, score them, write 3 drafts per signal, and generate images.*

### 4. Review & Approve
```bash
python scripts/approve.py
```
*Follow the prompt to approve a draft.*

### 5. Publish to LinkedIn
```bash
python src/core/publisher.py
```
*Posts all approved drafts with their generated images.*

## 📁 Project Structure
- `src/main.py`: Main entry point.
- `src/ingestion/`: API and Scraper-based news collectors.
- `src/core/drafter.py`: Content generation logic.
- `src/core/visuals.py`: AI image generation and storage.
- `src/core/publisher.py`: LinkedIn API integration.
- `scripts/approve.py`: Manual review tool.

## ⚖️ License
[PRIVACY.md](PRIVACY.md) | [TERMS.md](TERMS.md)