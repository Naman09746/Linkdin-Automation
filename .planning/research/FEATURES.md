# Features Research

## Core Agent System (14 Agents)

### Phase 1: The Pipeline (Weeks 1-6)
1.  **Research Agent:** Multi-source signal collector (HN, Reddit, ArXiv, GitHub).
2.  **Trend Detection Agent:** Extracts emerging topics and groups signals.
3.  **Relevance Ranker:** Filters trends against user interest profile.
4.  **POV Generation Agent:** Injects user's "unique perspective" into the topic.
5.  **Writing Agent:** Drafts the post based on POV and signal data.
6.  **Humanizer Agent:** Refines tone to sound less "AI-like".

### Phase 2: Memory & Quality (Weeks 7-12)
7.  **Memory Management Agent:** RAG system for remembering past posts and styles.
8.  **Fact Verifier Agent:** Cross-references claims using Tavily.
9.  **Cringe Detector:** Scans for common "AIisms" and corporate fluff.

### Phase 3: Visuals & Automation (Weeks 13-20)
10. **Visual Selection Agent:** Decides if a post needs a diagram, code block, or image.
11. **Visual Generator Agent:** Orchestrates Playwright to create the visual.
12. **Scheduling Agent:** Manages Upstash/Redis queue for post timing.
13. **Analytics Agent:** (Optional/OAuth) Tracks post performance.
14. **Orchestrator Agent:** LangGraph controller for the entire workflow.

## Table Stakes (Must-Haves)
- **High-quality drafts:** If it sounds like ChatGPT, it fails.
- **Fact Accuracy:** Verified claims to maintain credibility.
- **Zero Cost:** System must run without credit card charges.
- **Human-in-the-Loop:** User must approve/edit before posting.

## Differentiators (Competitive Advantage)
- **POV Injection:** Unlike generic tools, this learns *your* opinions.
- **Local Scraping:** Bypasses limits of cloud-based scrapers.
- **Multi-Source Signals:** Not just "trending on X", but deep tech signals from ArXiv/GitHub.

## Anti-Features (What NOT to Build)
- **Full Automation (No Review):** Risk of hallucination or shadow banning.
- **Paid Image Gen:** No DALL-E 3 or Midjourney (use HTML visuals instead).
- **Generic Botting:** No auto-commenting or follow/unfollow (spam risk).
