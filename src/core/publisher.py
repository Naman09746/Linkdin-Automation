import requests
import os
from loguru import logger
from src.utils.config import settings
from src.core.database import db_manager

class LinkedInPublisher:
    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self):
        self.db = db_manager.get_supabase()
        self.access_token = settings.LINKEDIN_ACCESS_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0"
        }

    def get_member_urn(self) -> str:
        res = requests.get(f"{self.BASE_URL}/me", headers=self.headers)
        if res.status_code == 200:
            return f"urn:li:person:{res.json()['id']}"
        logger.error(f"Failed to get Member URN: {res.text}")
        return ""

    def register_image(self, owner_urn: str) -> Dict[str, str]:
        url = f"{self.BASE_URL}/assets?action=registerUpload"
        payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": owner_urn,
                "serviceRelationships": [{
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent"
                }]
            }
        }
        res = requests.post(url, headers=self.headers, json=payload)
        if res.status_code == 200:
            data = res.json()
            return {
                "upload_url": data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl'],
                "asset": data['value']['asset']
            }
        logger.error(f"Image registration failed: {res.text}")
        return {}

    def upload_image(self, upload_url: str, image_url: str):
        # Fetch image from Supabase URL
        img_res = requests.get(image_url)
        if img_res.status_code == 200:
            # Upload to LinkedIn
            res = requests.put(upload_url, headers=self.headers, data=img_res.content)
            return res.status_code == 201
        return False

    def create_post(self, author_urn: str, text: str, asset_urn: str = None):
        url = f"{self.BASE_URL}/ugcPosts"
        payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE" if not asset_urn else "IMAGE",
                    "media": [] if not asset_urn else [{
                        "status": "READY",
                        "description": "AI Generated Insight",
                        "media": asset_urn
                    }]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        res = requests.post(url, headers=self.headers, json=payload)
        if res.status_code == 201:
            logger.success("Post successfully published to LinkedIn!")
            return True
        logger.error(f"Posting failed: {res.text}")
        return False

    def publish_approved_drafts(self):
        if not self.db: return
        res = self.db.table("drafts").select("*").eq("status", "approved").execute()
        
        if not res.data:
            logger.info("No approved drafts to publish.")
            return

        author_urn = self.get_member_urn()
        if not author_urn: return

        for draft in res.data:
            logger.info(f"Publishing draft: {draft['id']}")
            asset_urn = None
            
            if draft['visual_url']:
                reg = self.register_image(author_urn)
                if reg and self.upload_image(reg['upload_url'], draft['visual_url']):
                    asset_urn = reg['asset']
            
            if self.create_post(author_urn, draft['content'], asset_urn):
                self.db.table("drafts").update({"status": "posted", "posted_at": "now()"}).eq("id", draft['id']).execute()

if __name__ == "__main__":
    LinkedInPublisher().publish_approved_drafts()
