# Pitfalls Research

## Common Mistakes & Prevention

### 1. LinkedIn Shadow Banning & Policy Violations
- **Risk:** Automated posting or "too much" activity can flag your account.
- **Prevention:** 
  - **MANDATORY:** Never use 100% automated posting. The system MUST generate a draft that you approve and post manually via the dashboard.
  - **MANDATORY:** Do not scrape or crawl LinkedIn.com. Use the official LinkedIn API for all profile and post interactions.
  - Never post more than 1-2 times per day.

### 2. "AI-Vibe" Content
- **Risk:** Groq/Llama/GPT output often has tell-tale signs (emojis, "delve", specific structures).
- **Prevention:**
  - Build a strict Cringe Detector (regex + LLM check).
  - Use a "Humanizer" agent with a negative-prompting strategy (e.g., "Do not use emojis", "Write for a 10th grader").
  - Extract and inject the user's *real* past writing style from Supabase.

### 3. Rate Limit Walls
- **Risk:** Running a full 14-agent pipeline for every signal will exhaust Tavily/Groq limits.
- **Prevention:**
  - Filter signals early with cheap Python logic.
  - Group signals into "Trends" before running deep analysis.
  - Use Upstash to queue tasks so they don't hit RPM (Requests Per Minute) limits.

### 4. Supabase Project Pausing
- **Risk:** Free projects pause after 1 week of inactivity.
- **Prevention:**
  - Use a simple health-check ping (e.g., from cron-job.org or a local script).
  - Use the tool regularly (at least once a week).

### 5. Memory Drift
- **Risk:** Over time, the vector DB gets cluttered with irrelevant "styles".
- **Prevention:**
  - Implement a periodic "Memory Refresh" (as seen in Section 7 of the plan).
  - Only store *approved* posts in the style memory, not drafts.

## Critical Warnings
- **LinkedIn API:** Approval takes time. Start the application TODAY.
- **Groq/Gemini:** Free tier usage is for "non-commercial" development. Be careful if scaling beyond personal branding.
