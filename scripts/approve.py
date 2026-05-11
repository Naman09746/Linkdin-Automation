import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core.database import db_manager
from loguru import logger

def list_pending_drafts():
    db = db_manager.get_supabase()
    if not db: return
    
    res = db.table("drafts").select("id, post_type, content").eq("status", "pending").limit(10).execute()
    
    if not res.data:
        print("No pending drafts found.")
        return
    
    print("\n--- Pending Drafts ---")
    for i, d in enumerate(res.data):
        print(f"\n[{i}] ID: {d['id']}")
        print(f"Style: {d['post_type']}")
        print(f"Content: {d['content'][:150]}...")
    
    return res.data

def approve_draft(draft_id: str):
    db = db_manager.get_supabase()
    db.table("drafts").update({"status": "approved"}).eq("id", draft_id).execute()
    logger.success(f"Draft {draft_id} marked as APPROVED.")

if __name__ == "__main__":
    drafts = list_pending_drafts()
    if drafts:
        choice = input("\nEnter the index number to APPROVE (or 'q' to quit): ")
        if choice.isdigit() and int(choice) < len(drafts):
            approve_draft(drafts[int(choice)]['id'])
        else:
            print("Exiting.")
