# LinkedIn AI Branding Agent

## What This Is
A full 14-agent LinkedIn branding system designed to run entirely on free-tier tools and APIs. It automates the research, trend detection, POV generation, writing, humanizing, fact-checking, and visual generation process for high-quality LinkedIn content.

## Goal
Build a robust, personal LinkedIn automation pipeline that costs $0/month while saving 4-6 hours of research and writing time weekly.

## Core Value
Authentic content generation at scale through a "human-in-the-loop" system that leverages high-speed free LLM providers (Groq, Gemini) and local tools (Ollama, Crawl4AI).

## Requirements

### Validated
(None yet — ship to validate)

### Active
- [ ] Multi-source research pipeline (HN, Reddit, arXiv, GitHub, etc.)
- [ ] Trend detection and relevance ranking agents
- [ ] POV-driven content generation
- [ ] Quality assurance stack (Humanizer, Cringe Detector, Fact Verifier)
- [ ] Automated visual generation (Code/Diagrams/Terminal visuals)
- [ ] Long-term memory and style extraction (Qdrant + Ollama)
- [ ] Multi-provider LLM router (Groq, Gemini, Cerebras)

### Out of Scope
- [ ] Automated direct posting to LinkedIn (requires manual approval/Buffer)
- [ ] Paid LLM features (GPT-4o/Claude 3.5 Sonnet paid versions)
- [ ] Multi-user SaaS features (Phase 4 only)

## Key Decisions
| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Free-Tier Stack | Zero cost requirement | Qdrant Cloud, Supabase, Render, Vercel, Groq |
| Local Scraper | Bypass paid scraping limits | Crawl4AI + Playwright (External sites only) |
| Local Embeddings | Unlimited vector generation | Ollama (nomic-embed-text) |
| Human-in-the-loop | LinkedIn API Compliance | Mandatory manual approval before posting |

## Compliance & Safety
To ensure zero violations of LinkedIn's Terms of Use:
1. **Mandatory Manual Review:** No 100% automated posting. The system generates drafts; the user clicks "Post".
2. **Official API Only:** No scraping or crawling of LinkedIn.com itself.
3. **No Commercial Use:** No selling of API data or using it for advertising/spam.
4. **Data Privacy:** Delete user-related content immediately upon request.

## Evolution
This document evolves at phase transitions and milestone boundaries.
*Last updated: 2026-05-11 after initialization*
