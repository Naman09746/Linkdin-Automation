import requests
import arxiv
import praw
import time
import os
import re
from typing import List, Dict, Any
from loguru import logger
from src.utils.config import settings
from src.core.llm_router import llm_router
from src.core.database import db_manager
from src.models.signal import Signal

class BaseCollector:
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.db = db_manager.get_supabase()

    def score_signal(self, title: str, summary: str) -> float:
        try:
            prompt = f"Title: {title}\nSummary: {summary}\n\nRate the relevance of this news for a LinkedIn audience of tech professionals. Return ONLY a single number (1.0-10.0)."
            response = llm_router.complete(prompt, system_prompt="You are a trend analyst. Return a single float.")
            match = re.search(r"(\d+\.?\d*)", response)
            return float(match.group(1)) if match else 5.0
        except Exception: return 5.0

    def save_signal(self, signal_data: Dict[str, Any]):
        if not self.db: return
        try:
            if signal_data.get('url'):
                existing = self.db.table("signals").select("id").eq("url", signal_data['url']).execute()
                if existing.data: return
            self.db.table("signals").insert(signal_data).execute()
            logger.success(f"Saved signal from {self.source_name}: {signal_data.get('title')}")
        except Exception as e: logger.error(f"Failed to save signal: {e}")

class HNCollector(BaseCollector):
    def __init__(self): super().__init__("hacker_news")
    def fetch(self, limit: int = 10):
        url = f"https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage={limit}"
        res = requests.get(url)
        if res.status_code == 200:
            for story in res.json().get("hits", []):
                title = story.get("title")
                url = story.get("url") or f"https://news.ycombinator.com/item?id={story.get('objectID')}"
                score = self.score_signal(title, story.get("story_text", "")[:500])
                self.save_signal(Signal(source=self.source_name, url=url, title=title, content=story.get("story_text"), importance_score=score, raw_json=story).model_dump(exclude={'id', 'created_at'}))

class ArXivCollector(BaseCollector):
    def __init__(self):
        super().__init__("arxiv")
        self.client = arxiv.Client()
    def fetch(self, query: str = "Artificial Intelligence", limit: int = 5):
        search = arxiv.Search(query=query, max_results=limit, sort_by=arxiv.SortCriterion.SubmittedDate)
        for result in self.client.results(search):
            score = self.score_signal(result.title, result.summary[:500])
            self.save_signal(Signal(source=self.source_name, url=result.entry_id, title=result.title, content=result.summary, importance_score=score, raw_json={"authors": [a.name for a in result.authors]}).model_dump(exclude={'id', 'created_at'}))

class RedditCollector(BaseCollector):
    def __init__(self):
        super().__init__("reddit")
        try:
            self.reddit = praw.Reddit(client_id=settings.REDDIT_CLIENT_ID, client_secret=settings.REDDIT_CLIENT_SECRET, user_agent="linkedin_agent_v1")
        except Exception: self.reddit = None
    def fetch(self, subreddit_name: str = "MachineLearning", limit: int = 5):
        if not self.reddit: return
        subreddit = self.reddit.subreddit(subreddit_name)
        for sub in subreddit.hot(limit=limit):
            if sub.stickied: continue
            score = self.score_signal(sub.title, sub.selftext[:500])
            self.save_signal(Signal(source=self.source_name, url=f"https://reddit.com{sub.permalink}", title=sub.title, content=sub.selftext, importance_score=score, raw_json={"subreddit": subreddit_name}).model_dump(exclude={'id', 'created_at'}))
