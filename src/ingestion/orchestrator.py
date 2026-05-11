import asyncio
from loguru import logger
from src.ingestion.api_collectors import HNCollector, ArXivCollector, RedditCollector
from src.ingestion.scrapers import GitHubScraper

class SignalManager:
    def __init__(self):
        self.hn = HNCollector()
        self.arxiv = ArXivCollector()
        self.reddit = RedditCollector()
        self.github = GitHubScraper()
    async def run_sync(self):
        logger.info("🚀 Starting Global Signal Ingestion...")
        try:
            self.hn.fetch(limit=5)
            self.arxiv.fetch(limit=3)
            self.reddit.fetch(limit=3)
        except Exception as e: logger.error(f"API Collectors failed: {e}")
        try: await self.github.fetch(limit=5)
        except Exception as e: logger.error(f"GitHub Scraper failed: {e}")
        logger.info("✅ Ingestion Cycle Complete.")

if __name__ == "__main__":
    asyncio.run(SignalManager().run_sync())
