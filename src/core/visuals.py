import io
import requests
from typing import Optional
from loguru import logger
from playwright.async_api import async_playwright
import asyncio
from PIL import Image, ImageDraw
from src.utils.config import settings
from src.core.database import db_manager

class VisualManager:
    def __init__(self):
        self.db = db_manager.get_supabase()

    def add_macos_frame(self, image_bytes: bytes) -> bytes:
        try:
            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size
            
            bar_height = 40
            new_img = Image.new('RGB', (width, height + bar_height), color='#1e1e1e') # Dark mode title bar
            
            # Draw the circles
            draw = ImageDraw.Draw(new_img)
            radius = 6
            y_offset = (bar_height // 2) - radius
            draw.ellipse((20, y_offset, 20 + radius*2, y_offset + radius*2), fill='#FF5F56') # Red
            draw.ellipse((40, y_offset, 40 + radius*2, y_offset + radius*2), fill='#FFBD2E') # Yellow
            draw.ellipse((60, y_offset, 60 + radius*2, y_offset + radius*2), fill='#27C93F') # Green
            
            # Paste original image
            new_img.paste(img, (0, bar_height))
            
            # Convert back to bytes
            out_io = io.BytesIO()
            new_img.save(out_io, format='PNG')
            return out_io.getvalue()
        except Exception as e:
            logger.error(f"Failed to add macOS frame: {e}")
            return image_bytes

    async def get_genuine_visual(self, url: str) -> Optional[bytes]:
        """
        Attempts to get the official og:image graph/thumbnail.
        If not found, takes a genuine screenshot of the webpage as if opened on a laptop.
        """
        logger.info(f"Extracting genuine visual from: {url}")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                # Simulate a MacBook Pro viewport
                context = await browser.new_context(viewport={'width': 1440, 'height': 900})
                page = await context.new_page()
                
                # Navigate to the URL
                await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                
                # 1. Try to find the official og:image (often the comparison graphs in AI papers)
                og_image_url = None
                if "github.com" not in url:
                    og_image_url = await page.evaluate('document.querySelector("meta[property=\'og:image\']")?.content')
                
                if og_image_url:
                    logger.info(f"Found official og:image: {og_image_url}")
                    if not og_image_url.startswith('http'):
                        pass
                    else:
                        # Use requests for downloading the image (can wrap in to_thread if blocking is an issue, but usually fast enough)
                        img_res = await asyncio.to_thread(requests.get, og_image_url, timeout=10)
                        if img_res.status_code == 200:
                            await browser.close()
                            return img_res.content
                
                # 2. Fallback: Take a genuine screenshot of the page
                logger.info("No official og:image found. Taking genuine MacBook screenshot.")
                await page.wait_for_timeout(3000)
                
                screenshot_bytes = await page.screenshot(full_page=False, type="png")
                await browser.close()
                
                # Wrap it in a beautiful macOS frame
                framed_bytes = self.add_macos_frame(screenshot_bytes)
                return framed_bytes

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

    async def process_drafts(self, limit: int = 3):
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
            
            image_bytes = await self.get_genuine_visual(signal_url)
            
            if image_bytes:
                filename = f"{draft_id}.png"
                visual_url = self.upload_asset(image_bytes, filename)
                if visual_url:
                    self.db.table("drafts").update({"visual_url": visual_url}).eq("id", draft_id).execute()
                    logger.success(f"Updated draft {draft_id} with genuine visual URL.")

if __name__ == "__main__":
    asyncio.run(VisualManager().process_drafts())
