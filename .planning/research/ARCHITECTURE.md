# Architecture Research

## System Structure: Local-Cloud Hybrid

### 1. Local Node (The "Worker")
- **Responsibility:** Compute-heavy and limit-sensitive tasks.
- **Components:**
  - **Ollama:** Local inference for embeddings (nomic-embed-text).
  - **Crawl4AI:** Browser-based scraping (Playwright).
  - **Visual Gen:** Playwright rendering of HTML/Tailwind templates.
  - **Mermaid CLI:** Diagram rendering.

### 2. Cloud Backend (The "Brain")
- **Responsibility:** Orchestration, state management, and lightweight API calls.
- **Components:**
  - **FastAPI:** Main API gateway.
  - **LangGraph:** Orchestration of the 14-agent DAG (Directed Acyclic Graph).
  - **Free LLM APIs:** Groq (Writing), Gemini (Fact-checking).

### 3. Persistence Layer (The "Memory")
- **Supabase (Postgres):** Stores user profiles, raw signals, drafts, and logs.
- **Qdrant (Vector):** Stores document embeddings for RAG and style matching.
- **Upstash (Redis):** Task queues and transient state for long-running agents.

## Data Flow
1. **Trigger:** Cron job (or manual) starts the Research Agent.
2. **Ingestion:** Local worker scrapes signals → Sends to Cloud Backend.
3. **Processing:** 
   - Backend routes to Groq for Trend Detection.
   - Relevance Ranker filters against Supabase user profile.
   - POV & Writing agents generate drafts.
4. **Verification:** Gemini Fact Verifier checks claims via Tavily.
5. **Human Review:** Draft sent to Frontend (Vercel/Next.js) for user approval.
6. **Finalization:** Approved post saved → Visuals generated locally → Final assets uploaded to R2.

## Build Order (Dependencies)
1. **LLM Router & Local Tools:** Essential for all following steps.
2. **Research Pipeline:** Need data before we can write.
3. **Database Schema:** Need to store signals/drafts.
4. **Content Generation Agents:** Core value proposition.
5. **Visuals & Memory:** Optimization and polish.
