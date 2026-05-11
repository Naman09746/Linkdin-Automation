from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.core.database import db_manager
from loguru import logger

app = FastAPI(title="LinkedIn AI Agent Dashboard API")
db = db_manager.get_supabase()

class DraftUpdate(BaseModel):
    status: str
    rejection_reason: Optional[str] = None

@app.get("/api/drafts/pending")
def get_pending():
    res = db.table("drafts").select("*, signals(title, url)").eq("status", "pending").execute()
    return res.data

@app.post("/api/drafts/{draft_id}/approve")
def approve(draft_id: str):
    try:
        res = db.table("drafts").update({"status": "approved"}).eq("id", draft_id).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/drafts/{draft_id}/reject")
def reject(draft_id: str, update: DraftUpdate):
    try:
        res = db.table("drafts").update({
            "status": "rejected",
            "rejection_reason": update.rejection_reason
        }).eq("id", draft_id).execute()
        return {"status": "success", "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/drafts/history")
def get_history():
    res = db.table("drafts").select("*, signals(title)").neq("status", "pending").order("created_at", desc=True).execute()
    return res.data

@app.get("/api/stats")
def get_stats():
    # Basic aggregation logic (can be optimized with RPC in Supabase)
    pending = db.table("drafts").select("id", count="exact").eq("status", "pending").execute().count
    approved = db.table("drafts").select("id", count="exact").eq("status", "approved").execute().count
    posted = db.table("drafts").select("id", count="exact").eq("status", "posted").execute().count
    rejected = db.table("drafts").select("id", count="exact").eq("status", "rejected").execute().count
    
    return {
        "pending": pending or 0,
        "approved": approved or 0,
        "posted": posted or 0,
        "rejected": rejected or 0
    }
