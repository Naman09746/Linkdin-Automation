# Requirements: LinkedIn AI Branding Agent

**Defined:** 2026-05-11
**Core Value:** Build a robust, personal LinkedIn automation pipeline that costs $0/month while saving 4-6 hours of research and writing time weekly.

## v1 Requirements (Phase 1-3)

### Core Infrastructure
- [ ] **CORE-01**: Multi-provider LLM Router (Groq, Gemini, Cerebras) with fallback logic.
- [ ] **CORE-02**: Local tool integration (Ollama for embeddings, Playwright for scraping/visuals).
- [ ] **CORE-03**: Supabase (Postgres) integration for persistence.
- [ ] **CORE-04**: Upstash (Redis) integration for task queuing.

### Research & Signals
- [ ] **RSRCH-01**: Signal ingestion from HackerNews (Algolia API).
- [ ] **RSRCH-02**: Signal ingestion from Reddit (PRAW).
- [ ] **RSRCH-03**: Signal ingestion from ArXiv (Official API).
- [ ] **RSRCH-04**: Signal ingestion from GitHub Trending (Crawl4AI).
- [ ] **RSRCH-05**: Signal ingestion from official AI blogs (Crawl4AI).
- [ ] **RSRCH-06**: Signal ingestion from Twitter/X (Nitter RSS fallback).

### Content Generation
- [ ] **CONT-01**: Trend Detection agent (groups raw signals into cohesive topics).
- [ ] **CONT-02**: Relevance Ranking agent (scores topics against user profile).
- [ ] **CONT-03**: POV Generation agent (injects user-defined perspective into drafts).
- [ ] **CONT-04**: Writing agent (generates first draft with specific formatting).
- [ ] **CONT-05**: Humanizer agent (strips AI-isms and refines tone).

### Quality & Memory
- [ ] **QUAL-01**: Fact Verifier agent (cross-references claims with Tavily).
- [ ] **QUAL-02**: Cringe Detector (regex + LLM filter for corporate fluff).
- [ ] **QUAL-03**: Style Memory (Qdrant RAG to match user's past writing).

### Visuals
- [ ] **VIS-01**: Automatic selection of visual type (code, diagram, terminal).
- [ ] **VIS-02**: Visual generation via Playwright + HTML/Tailwind templates.
- [ ] **VIS-03**: Cloudflare R2 integration for asset storage.

### Interface
- [ ] **UI-01**: Next.js dashboard to review, edit, and approve drafts.
- [ ] **UI-02**: Feed of raw signals and trends.
- [ ] **UI-03**: User interest profile management.

## v2 Requirements (Phase 4+)
- **SAAS-01**: Multi-user support (RBAC, per-user storage namespaces).
- **SAAS-02**: Stripe integration for billing.
- **SOCL-01**: Automated direct posting to LinkedIn (requires API approval).
- **ANLY-01**: Post performance tracking dashboard.

## Out of Scope
| Feature | Reason |
|---------|--------|
| Paid LLM APIs | Project goal is $0 monthly spend |
| Paid Image Gen | High cost, replaced by HTML visuals |
| Auto-commenting | High risk of account suspension |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CORE-01 | Phase 1 | Pending |
| CORE-02 | Phase 1 | Pending |
| CORE-03 | Phase 1 | Pending |
| CORE-04 | Phase 1 | Pending |
| RSRCH-01 | Phase 1 | Pending |
| RSRCH-02 | Phase 1 | Pending |
| RSRCH-03 | Phase 1 | Pending |
| RSRCH-04 | Phase 1 | Pending |
| RSRCH-05 | Phase 1 | Pending |
| RSRCH-06 | Phase 1 | Pending |
| CONT-01 | Phase 1 | Pending |
| CONT-02 | Phase 1 | Pending |
| CONT-03 | Phase 2 | Pending |
| CONT-04 | Phase 2 | Pending |
| CONT-05 | Phase 2 | Pending |
| QUAL-01 | Phase 2 | Pending |
| QUAL-02 | Phase 2 | Pending |
| QUAL-03 | Phase 2 | Pending |
| VIS-01 | Phase 3 | Pending |
| VIS-02 | Phase 3 | Pending |
| VIS-03 | Phase 3 | Pending |
| UI-01 | Phase 3 | Pending |
| UI-02 | Phase 3 | Pending |
| UI-03 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 24 total
- Mapped to phases: 24
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-11*
*Last updated: 2026-05-11 after initial definition*
