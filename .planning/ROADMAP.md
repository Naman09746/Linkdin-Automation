# Roadmap: LinkedIn AI Branding Agent

## Overview
This roadmap takes the project from a blank directory to a fully functional 14-agent LinkedIn automation system. We start by building the core LLM router and signal ingestion, then move to sophisticated content generation with POV injection, and finally add quality verification and automated visual generation.

## Phases

- [ ] **Phase 1: Foundation & LLM Router** - Set up the environment, local tools, and multi-provider fallback router.
- [ ] **Phase 2: Signal Ingestion Engine** - Build connectors for HN, Reddit, ArXiv, and GitHub trending.
- [ ] **Phase 3: Trend & Rank Pipeline** - Implement topic grouping and relevance scoring against user interests.
- [ ] **Phase 4: Content Generation Core** - Build POV injection, writing, and humanizer agents.
- [ ] **Phase 5: Quality & Memory Layers** - Add fact-verification, cringe detection, and style-matching memory.
- [ ] **Phase 6: Visual Generation** - Implement automated code/diagram/terminal visual creation using Playwright.
- [ ] **Phase 7: Dashboard & Orchestration** - Build the Next.js review interface and LangGraph orchestrator.

## Phase Details

### Phase 1: Foundation & LLM Router
**Goal**: Establish a stable, zero-cost execution environment.
**Depends on**: Nothing
**Requirements**: CORE-01, CORE-02, CORE-03, CORE-04
**Success Criteria**:
  1. Ollama serves embeddings locally.
  2. LLM Router successfully falls back from Groq to Gemini/Cerebras on rate limits.
  3. Supabase and Upstash connections are verified.
**Plans**: 3 plans

Plans:
- [ ] 01-01: Environment & Local Tool Setup (Ollama, Playwright, Crawl4AI)
- [ ] 01-02: Multi-Provider LLM Router Implementation
- [ ] 01-03: Database Schema & Connection Logic

### Phase 2: Signal Ingestion Engine
**Goal**: Gather raw data from diverse tech sources at $0 cost.
**Depends on**: Phase 1
**Requirements**: RSRCH-01, RSRCH-02, RSRCH-03, RSRCH-04, RSRCH-05, RSRCH-06
**Success Criteria**:
  1. Research agent successfully scrapes HackerNews, Reddit, and ArXiv.
  2. Crawl4AI handles GitHub Trending and official AI blogs.
  3. Raw signals are deduplicated and stored in Supabase.
**Plans**: 2 plans

Plans:
- [ ] 02-01: API-based Signal Collectors (HN, Reddit, ArXiv)
- [ ] 02-02: Scraper-based Signal Collectors (GitHub, Blogs, Twitter RSS)

### Phase 3: Trend & Rank Pipeline
**Goal**: Filter the noise and find what matters to the user.
**Depends on**: Phase 2
**Requirements**: CONT-01, CONT-02
**Success Criteria**:
  1. Trend Detection Agent groups 50+ signals into distinct topics.
  2. Relevance Ranker correctly identifies topics matching the user profile.
**Plans**: 2 plans

Plans:
- [ ] 03-01: Trend Detection & Topic Grouping Logic
- [ ] 03-02: User Profile Scoring & Ranking Agent

### Phase 4: Content Generation Core
**Goal**: Generate high-quality, non-generic LinkedIn drafts.
**Depends on**: Phase 3
**Requirements**: CONT-03, CONT-04, CONT-05
**Success Criteria**:
  1. POV agent injects specific user viewpoints into every topic.
  2. Writing agent produces formatted LinkedIn posts (hooks, body, CTAs).
  3. Humanizer agent successfully removes 90% of common AI-isms.
**Plans**: 3 plans

Plans:
- [ ] 04-01: POV Injection & System Prompting
- [ ] 04-02: Writing Agent & Draft Generation
- [ ] 04-03: Humanizer Agent & Tone Refinement

### Phase 5: Quality & Memory Layers
**Goal**: Ensure accuracy and consistent personal style.
**Depends on**: Phase 4
**Requirements**: QUAL-01, QUAL-02, QUAL-03
**Success Criteria**:
  1. Fact Verifier flags false claims using Tavily search.
  2. Cringe Detector blocks posts with excessive emojis or corporate fluff.
  3. Style Memory retrieves relevant past posts for few-shot prompting.
**Plans**: 2 plans

Plans:
- [ ] 05-01: Quality Agents (Fact Check & Cringe Detect)
- [ ] 05-02: Qdrant Memory & Style Extraction

### Phase 6: Visual Generation
**Goal**: Create stunning visuals for posts without paid tools.
**Depends on**: Phase 5
**Requirements**: VIS-01, VIS-02, VIS-03
**Success Criteria**:
  1. Visual Selection agent chooses appropriate visual types for content.
  2. Playwright renders high-res screenshots of code/diagrams.
  3. Assets are uploaded to Cloudflare R2 and URLs returned.
**Plans**: 2 plans

Plans:
- [ ] 06-01: Visual Selection & HTML/Mermaid Templates
- [ ] 06-02: Playwright Renderer & R2 Storage Service

### Phase 7: Dashboard & Orchestration
**Goal**: Provide a seamless human-in-the-loop review experience.
**Depends on**: Phase 6
**Requirements**: UI-01, UI-02, UI-03
**Success Criteria**:
  1. LangGraph orchestrates the full DAG from signal to draft.
  2. User can edit and approve drafts in the Next.js dashboard.
**Plans**: 3 plans

Plans:
- [ ] 07-01: LangGraph Orchestration & Job Scheduler
- [ ] 07-02: Next.js Frontend Foundation & Signal Feed
- [ ] 07-03: Draft Review & Approval UI

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & LLM Router | 0/3 | Not started | - |
| 2. Signal Ingestion Engine | 0/2 | Not started | - |
| 3. Trend & Rank Pipeline | 0/2 | Not started | - |
| 4. Content Generation Core | 0/3 | Not started | - |
| 5. Quality & Memory Layers | 0/2 | Not started | - |
| 6. Visual Generation | 0/2 | Not started | - |
| 7. Dashboard & Orchestration | 0/3 | Not started | - |

---
*Roadmap defined: 2026-05-11*
*Last updated: 2026-05-11 after initialization*
