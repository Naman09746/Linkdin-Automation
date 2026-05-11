import pytest
from src.core.visuals import VisualManager
from src.core.database import db_manager

import asyncio

async def test_genuine_visual_pipeline():
    manager = VisualManager()
    sb = db_manager.get_supabase()
    
    # 1. Get a draft that needs a visual
    res = sb.table("drafts").select("id, status, visual_url, signal_id, signals(url)").limit(1).execute()
    if not res.data:
        print("No drafts found to test visuals.")
        return

    draft = res.data[0]
    signal_url = draft.get('signals', {}).get('url')
    
    if not signal_url:
        # Fallback to a known URL for testing
        signal_url = "https://github.com/microsoft/autogen"
        print("Using fallback URL for testing: ", signal_url)

    print(f"Testing visual extraction for: {signal_url}")
    
    # 2. Extract genuine visual
    image_bytes = await manager.get_genuine_visual(signal_url)
    assert image_bytes is not None
    print("Successfully captured screenshot/og_image bytes.")
    
    # 3. Upload
    url = manager.upload_asset(image_bytes, f"test_genuine_{draft['id']}.png")
    assert url is not None
    print(f"Success! Genuine image available at: {url}")

if __name__ == "__main__":
    asyncio.run(test_genuine_visual_pipeline())
