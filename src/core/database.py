from supabase import create_client, Client
from upstash_redis import Redis
from qdrant_client import QdrantClient
from src.utils.config import settings
from loguru import logger

class DatabaseManager:
    def __init__(self):
        try:
            self.supabase: Client = create_client(settings.NEXT_PUBLIC_SUPABASE_URL, settings.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY)
            logger.info("Supabase Client Initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase: {e}")
            self.supabase = None
        try:
            self.redis = Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN)
            logger.info("Upstash Redis Client Initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Upstash: {e}")
            self.redis = None
        try:
            self.qdrant = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
            logger.info("Qdrant Client Initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {e}")
            self.qdrant = None

    def get_supabase(self): return self.supabase
    def get_redis(self): return self.redis
    def get_qdrant(self): return self.qdrant

db_manager = DatabaseManager()
