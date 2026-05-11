# Stack Research

## Recommended Stack (2026 Free-Tier)

### Core LLMs
- **Primary:** Groq (Llama 3.3 70B)
  - *Rationale:* Fastest inference (500+ tok/s), high rate limits (14k+ RPD).
  - *Free Limit:* 14,400 requests/day.
- **Secondary:** Gemini 1.5 Flash
  - *Rationale:* Excellent reasoning, massive context window (1M+), best for fact-checking.
  - *Free Limit:* 1,500 requests/day.
- **Backup:** Cerebras Inference (Llama 3.1 70B)
  - *Rationale:* High-speed fallback if Groq is down.

### Databases & Memory
- **Relational:** Supabase (PostgreSQL)
  - *Rationale:* "Free forever" tier, built-in Auth, easy vector support (pgvector) if needed.
  - *Free Limit:* 500MB database, 2 active projects.
- **Vector:** Qdrant Cloud
  - *Rationale:* Dedicated vector engine, high performance, generous free tier.
  - *Free Limit:* 1GB RAM, 4GB disk.
- **Queue/Cache:** Upstash Redis
  - *Rationale:* Serverless Redis, perfect for job queues (LangGraph/Celery).
  - *Free Limit:* 10,000 commands/day.

### Retrieval & Scraping
- **Search:** Tavily API
  - *Rationale:* AI-optimized search, returns clean content.
  - *Free Limit:* 1,000 searches/month.
- **Scraping:** Crawl4AI (Local)
  - *Rationale:* Open-source, no limits, returns markdown, handles JS-heavy sites.
  - *Free Limit:* Unlimited (runs locally).

### Visuals & Storage
- **Visual Gen:** Playwright + HTML Templates
  - *Rationale:* Programmatic screenshots, zero cost, infinite customization.
- **Storage:** Cloudflare R2
  - *Rationale:* S3-compatible, no egress fees, 10GB free.
  - *Free Limit:* 10GB storage.

### Hosting
- **Backend:** Render.com (Free)
  - *Rationale:* Native Python support, 750 free hours/month.
  - *Caveat:* Cold starts (needs health-check ping).
- **Frontend:** Vercel (Free)
  - *Rationale:* Industry standard for Next.js.

## Versions to Use
- **Python:** 3.11+
- **FastAPI:** 0.110+
- **LangGraph:** Latest
- **Next.js:** 14+ (App Router)
- **TailwindCSS:** 3.4+

## Rationale Summary
The chosen stack maximizes performance while ensuring $0 monthly overhead. By splitting heavy tasks (scraping, visual gen) to local execution and using managed cloud services for persistence, we stay within all free tier limits.
