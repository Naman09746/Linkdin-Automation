import io
import requests
from typing import Optional
from loguru import logger
from playwright.sync_api import sync_playwright
from src.utils.config import settings
from src.core.database import db_manager

class VisualManager:
    def __init__(self):
        self.db = db_manager.get_supabase()

    def get_genuine_visual(self, url: str) -> Optional[bytes]:
        """
        Attempts to get the official og:image graph/thumbnail.
        If not found, takes a genuine screenshot of the webpage as if opened on a laptop.
        """
        logger.info(f"Extracting genuine visual from: {url}")
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                # Simulate a MacBook Pro viewport
                context = browser.new_context(viewport={'width': 1440, 'height': 900})
                page = context.new_page()
                
                # Navigate to the URL
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                
                # 1. Try to find the official og:image (often the comparison graphs in AI papers)
                og_image_url = page.evaluate('document.querySelector("meta[property=\'og:image\']")?.content')
                
                if og_image_url:
                    logger.info(f"Found official og:image: {og_image_url}")
                    # Download the official image
                    # Sometimes URLs are relative, handle that if necessary, but og:image is usually absolute
                    if not og_image_url.startswith('http'):
                        # Best effort parsing, otherwise fallback to screenshot
                        pass
                    else:
                        img_res = requests.get(og_image_url, timeout=10)
                        if img_res.status_code == 200:
                            browser.close()
                            return img_res.content
                
                # 2. Fallback: Take a genuine screenshot of the page
                logger.info("No official og:image found. Taking genuine MacBook screenshot.")
                # Wait a bit longer for graphs to render
                page.wait_for_timeout(3000)
                
                # Take screenshot of the top of the page (usually where the title/abstract is)
                screenshot_bytes = page.screenshot(full_page=False, type="png")
                browser.close()
                return screenshot_bytes

        except Exception as e:
            logger.error(f"Failed to capture genuine visual: {e}")
            return None

    def upload_asset(self, image_bytes: bytes, filename: str) -> Optional[str]:
        if not self.db: return None
        try:
            bucket = settings.SUPABASE_STORAGE_BUCKET
            path = f"drafts/{filename}"
            
            self.db.storage.from_(bucket).upload(
                path=path,
                file=image_bytes,
                file_options={"content-type": "image/png", "upsert": "true"}
            )
            
            return self.db.storage.from_(bucket).get_public_url(path)
        except Exception as e:
            logger.error(f"Upload failed: {e}")
            return None

    def process_drafts(self, limit: int = 3):
        if not self.db: return
        
        # We need the signal URL to take the screenshot, so we must join with signals
        res = self.db.table("drafts").select("id, status, visual_url, signal_id, signals(url)").is_("visual_url", "null").eq("status", "pending").limit(limit).execute()
        
        for draft in res.data:
            draft_id = draft['id']
            signal_url = draft.get('signals', {}).get('url')
            
            if not signal_url:
                logger.warning(f"Draft {draft_id} has no source URL to screenshot.")
                continue

            logger.info(f"Generating genuine visual for draft: {draft_id}")
            
            image_bytes = self.get_genuine_visual(signal_url)
            
            if image_bytes:
                filename = f"{draft_id}.png"
                visual_url = self.upload_asset(image_bytes, filename)
                if visual_url:
                    self.db.table("drafts").update({"visual_url": visual_url}).eq("id", draft_id).execute()
                    logger.success(f"Updated draft {draft_id} with genuine visual URL.")

if __name__ == "__main__":
    VisualManager().process_drafts()
