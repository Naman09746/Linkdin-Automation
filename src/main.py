import asyncio
import sys
import argparse
from loguru import logger
from src.ingestion.orchestrator import SignalManager
from src.core.drafter import DraftGenerator
from src.core.visuals import VisualManager

async def run_pipeline(limit: int = 5):
    logger.info("🎬 Starting Full LinkedIn AI Agent Loop...")
    
    # 1. Ingestion
    logger.info("--- Phase 2: Ingesting Signals ---")
    await SignalManager().run_sync()
    
    # 2. Drafting
    logger.info("--- Phase 3: Generating Drafts ---")
    DraftGenerator().process_pending_signals(limit=limit)
    
    # 3. Visuals
    logger.info("--- Phase 4: Generating Visuals ---")
    await VisualManager().process_drafts(limit=limit)
    
    logger.success("🏁 Full Loop Complete. Check your Supabase 'drafts' table for review!")

def main():
    parser = argparse.ArgumentParser(description="LinkedIn AI Agent CLI")
    parser.add_argument("--limit", type=int, default=3, help="Number of signals to process")
    args = parser.parse_args()
    
    asyncio.run(run_pipeline(limit=args.limit))

if __name__ == "__main__":
    main()
