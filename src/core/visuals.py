import io
from typing import Optional, Any
from loguru import logger
from huggingface_hub import InferenceClient
from src.utils.config import settings
from src.core.llm_router import llm_router
from src.core.database import db_manager

class VisualManager:
    def __init__(self):
        self.db = db_manager.get_supabase()
        self.client = InferenceClient(
            model="stabilityai/stable-diffusion-xl-base-1.0",
            token=settings.HF_TOKEN
        )

    def generate_image_prompt(self, draft_content: str) -> str:
        system_prompt = "Convert this LinkedIn post into a high-quality DALL-E/Stable Diffusion image prompt. Style: Professional tech aesthetic, minimalist, clean, 8k resolution, cinematic lighting. NO text in image."
        try:
            return llm_router.complete(draft_content, system_prompt=system_prompt)
        except Exception as e:
            logger.error(f"Failed to generate image prompt: {e}")
            return "Professional software engineering aesthetic, minimalist tech background, cinematic lighting, 8k"

    def generate_image(self, prompt: str) -> Optional[bytes]:
        try:
            logger.info("Generating image with HF InferenceClient...")
            image = self.client.text_to_image(prompt)
            
            # Convert PIL Image to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue()
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
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
        res = self.db.table("drafts").select("*").is_("visual_url", "null").eq("status", "pending").limit(limit).execute()
        
        for draft in res.data:
            logger.info(f"Generating visual for draft: {draft['id']}")
            prompt = self.generate_image_prompt(draft['content'])
            image_bytes = self.generate_image(prompt)
            
            if image_bytes:
                filename = f"{draft['id']}.png"
                visual_url = self.upload_asset(image_bytes, filename)
                if visual_url:
                    self.db.table("drafts").update({"visual_url": visual_url}).eq("id", draft['id']).execute()
                    logger.success(f"Updated draft {draft['id']} with visual URL.")

if __name__ == "__main__":
    VisualManager().process_drafts()
