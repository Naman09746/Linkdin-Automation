from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

class Signal(BaseModel):
    id: Optional[uuid.UUID] = None
    source: str
    url: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    raw_json: Optional[Dict[str, Any]] = None
    importance_score: float = 0.0
    status: str = "new"
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
