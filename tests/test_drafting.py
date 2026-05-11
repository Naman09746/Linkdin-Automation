import pytest
import asyncio
from src.core.drafter import DraftGenerator
from src.core.database import db_manager

def test_drafting_logic():
    drafter = DraftGenerator()
    
    # Check if there are any high-score signals in the DB
    sb = db_manager.get_supabase()
    res = sb.table("signals").select("*").gt("importance_score", 7).limit(1).execute()
    
    if not res.data:
        print("No high-score signals found in DB. Skipping drafting test.")
        return

    # Process one signal
    print(f"Testing drafting for: {res.data[0]['title']}")
    drafter.process_pending_signals(limit=1)
    
    # Verify a draft was created
    drafts = sb.table("drafts").select("*").eq("signal_id", res.data[0]['id']).execute()
    assert len(drafts.data) > 0
    print(f"Verified: Found {len(drafts.data)} drafts in database.")

if __name__ == "__main__":
    test_drafting_logic()
