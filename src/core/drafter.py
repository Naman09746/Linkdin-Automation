from typing import List, Dict, Any, Optional
from loguru import logger
from src.core.llm_router import llm_router
from src.core.database import db_manager
from src.models.signal import Signal

class DraftGenerator:
    STYLES = {
        "PAS": "Problem-Agitate-Solution: Start with a tech pain point, explain why it's frustrating, then show the solution from the signal.",
        "HVCTA": "Hook-Value-CTA: Start with a punchy 1-line hook, give 3 bullet points of value, end with a question for comments.",
        "SLA": "Story-Lesson-Application: Tell a brief personal-sounding story about the tech, give the lesson, and how to apply it."
    }

    SYSTEM_PROMPT = """Act as a Senior Software Engineering LinkedIn Content Strategist. 
Your goal is to build a personal brand that is professional, authentic, and highly engaging.
Rules:
1. Use short, scannable paragraphs (max 3 lines).
2. NO corporate jargon (e.g., 'synergy', 'game-changer').
3. NO links in the body.
4. Hook must be under 140 chars.
5. End with an engagement question.
6. Tone: Technical expert but approachable."""

    def __init__(self):
        self.db = db_manager.get_supabase()

    def generate_variant(self, signal: Signal, style_name: str) -> str:
        style_desc = self.STYLES.get(style_name, "")
        prompt = f"""Draft a LinkedIn post based on this signal:
Title: {signal.title}
Content: {signal.content}

Style to use: {style_desc}
"""
        try:
            return llm_router.complete(prompt, system_prompt=self.SYSTEM_PROMPT)
        except Exception as e:
            logger.error(f"Drafting failed for {style_name}: {e}")
            return ""

    def process_pending_signals(self, limit: int = 5):
        if not self.db: return
        
        # Get signals with high score that haven't been drafted
        res = self.db.table("signals").select("*").gt("importance_score", 7).eq("status", "new").limit(limit).execute()
        
        for item in res.data:
            signal = Signal(**item)
            logger.info(f"Drafting for signal: {signal.title}")
            
            for style in self.STYLES.keys():
                content = self.generate_variant(signal, style)
                if content:
                    self.save_draft(signal.id, content, style)
            
            # Update signal status
            self.db.table("signals").update({"status": "drafted"}).eq("id", str(signal.id)).execute()

    def save_draft(self, signal_id: Any, content: str, style: str):
        try:
            draft_data = {
                "signal_id": str(signal_id),
                "content": content,
                "post_type": style,
                "status": "pending"
            }
            self.db.table("drafts").insert(draft_data).execute()
            logger.success(f"Saved {style} draft to database.")
        except Exception as e:
            logger.error(f"Failed to save draft: {e}")

if __name__ == "__main__":
    drafter = DraftGenerator()
    drafter.process_pending_signals()
