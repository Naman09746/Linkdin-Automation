# 🤖 LinkedIn AI Agent: Full System Overview

This document provides a comprehensive overview of the **LinkedIn AI Personal Branding Agent**. It serves as a guide for AI assistants to understand the architecture, logic, and refined persona of this project without needing to explore every directory.

---

## 🎯 Project Objective
Automate the professional branding of a **21-year-old AI/ML BTech student** (Year: 2026). The agent scours the latest tech news, drafts authentic "building in public" content, captures genuine visuals, and publishes them to LinkedIn.

---

## 👤 The Persona: "Authentic Tech Student"
The agent is tuned to a specific demographic:
- **Profile:** 4th-year CSE Student specializing in AI/ML.
- **Tone:** Enthusiastic, analytical, genuine, and peer-to-peer.
- **Rules:** 
    - NO corporate jargon (avoid "synergy", "delve", "game-changer").
    - Short paragraphs (1-2 lines).
    - Focuses on the *latest* updates and personal learning insights.
    - Uses technical terms correctly but avoids sounding like a "consultant."

---

## 🏗️ Technical Architecture

### 1. Signal Ingestion (`src/ingestion/`)
- **Sources:** Hacker News, ArXiv (AI Research), GitHub Trending.
- **Strict Recency:** Uses a 24-hour timestamp filter. It only "sees" news from the last day.
- **Scoring:** Every signal is scored (1-10) by an LLM. Only scores **7+** are drafted.

### 2. Drafting Engine (`src/core/drafter.py`)
- **Variants:** Generates 3 versions for every high-score signal:
    - **PAS:** Problem-Agitate-Solution.
    - **HVCTA:** Hook-Value-CTA (Call to Action).
    - **SLA:** Story-Lesson-Application (The "Personal" vibe).
- **Style:** Strictly follows the student persona described above.

### 3. Visuals Engine (`src/core/visuals.py`)
- **Genuine Visuals:** Bypasses "fake" AI generation. 
- **Playwright Scraper:** Opens a headless browser to the signal's URL.
- **MacOS Frame:** Captures a screenshot and uses `Pillow` to wrap it in a sleek **MacOS Dark Mode browser frame** (with the red/yellow/green buttons).
- **Smart Logic:** If the URL is GitHub, it *forces* a screenshot of the repo instead of using the generic thumbnail.

### 4. Publishing & Database (`src/core/publisher.py`)
- **Database:** Supabase (Postgres) stores signals and drafts.
- **Storage:** Supabase Buckets store the generated PNG screenshots.
- **API:** Uses LinkedIn v2023 API with a 3-step media handshake (Register -> Upload -> Post).

---

## 🔄 The Workflow Loop

| Step | Command | Action |
| :--- | :--- | :--- |
| **1. Generate** | `python src/main.py` | Finds news, drafts 3 variants, and takes screenshots. |
| **2. Review** | `python scripts/approve.py` | Interactive CLI to pick your favorite draft. |
| **3. Publish** | `python src/core/publisher.py` | Sends the approved draft + macOS screenshot to LinkedIn. |

---

## 📊 Database Schema Summary
- **Signals Table:** `id, source, url, title, content, importance_score, status ('new', 'drafted')`.
- **Drafts Table:** `id, signal_id, post_type, content, visual_url, status ('pending', 'approved', 'posted')`.

---

## ✨ Key Refinements Made
- **Pivot to Authenticity:** Moved away from Hugging Face AI images to Playwright-based genuine screenshots because AI images looked "too fake."
- **Event Loop Management:** The system is fully asynchronous to allow Playwright and the main agent loop to co-exist without conflicts.
- **Zero-Jargon Enforcement:** The LLM is strictly penalized for using common AI-generated filler words.

---
*This agent is built for high-velocity, authentic branding.*
