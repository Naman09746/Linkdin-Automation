import sys, os, ollama
from loguru import logger
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.config import settings
from src.core.llm_router import llm_router
from src.core.database import db_manager

def check_ollama():
    try:
        res = ollama.list()
        if any(m.model.startswith('nomic-embed-text') for m in res.models):
            logger.success("Ollama: nomic-embed-text found"); return True
        return False
    except Exception as e: logger.error(f"Ollama failed: {e}"); return False

def check_llms():
    try:
        res = llm_router.complete("Ping", "Reply with 'Pong'")
        if "Pong" in res: logger.success("LLM Router: Operational"); return True
        return False
    except Exception as e: logger.error(f"LLM failed: {e}"); return False

def check_supabase():
    try:
        sb = db_manager.get_supabase()
        if not sb: return False
        buckets = sb.storage.list_buckets()
        if any(b.name == settings.SUPABASE_STORAGE_BUCKET for b in buckets):
            logger.success(f"Supabase Storage: Bucket '{settings.SUPABASE_STORAGE_BUCKET}' found")
        return True
    except Exception as e: logger.error(f"Supabase failed: {e}"); return False

def main():
    results = {"Ollama": check_ollama(), "LLMs": check_llms(), "Supabase": check_supabase()}
    if all(results.values()): logger.success("🚀 All Systems Operational!")
    else: sys.exit(1)

if __name__ == "__main__": main()
