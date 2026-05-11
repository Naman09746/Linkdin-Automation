import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: str
    GEMINI_API_KEY: Optional[str] = None
    CEREBRAS_API_KEY: Optional[str] = None
    HF_TOKEN: Optional[str] = None
    NEXT_PUBLIC_SUPABASE_URL: str
    NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: str
    DATABASE_URL: str
    SUPABASE_STORAGE_BUCKET: str = "linkedin-assets"
    UPSTASH_REDIS_REST_URL: str
    UPSTASH_REDIS_REST_TOKEN: str
    QDRANT_URL: str
    QDRANT_API_KEY: str
    TAVILY_API_KEY: str
    REDDIT_CLIENT_ID: Optional[str] = None
    REDDIT_CLIENT_SECRET: Optional[str] = None
    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None
    LINKEDIN_ACCESS_TOKEN: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None
    DISCORD_WEBHOOK_URL: Optional[str] = None
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
