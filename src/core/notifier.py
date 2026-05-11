import requests
from loguru import logger
from src.utils.config import settings

class NotificationManager:
    def __init__(self):
        self.telegram_token = settings.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = settings.TELEGRAM_CHAT_ID
        self.discord_webhook = settings.DISCORD_WEBHOOK_URL

    def send_telegram(self, message: str):
        if not self.telegram_token or not self.telegram_chat_id:
            logger.warning("Telegram credentials missing, skipping notification.")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            res = requests.post(url, json=payload, timeout=10)
            return res.status_code == 200
        except Exception as e:
            logger.error(f"Telegram notification failed: {e}")
            return False

    def send_discord(self, message: str):
        if not self.discord_webhook:
            logger.warning("Discord webhook missing, skipping notification.")
            return False
        
        try:
            payload = {"content": message}
            res = requests.post(self.discord_webhook, json=payload, timeout=10)
            return res.status_code == 204 # Discord returns 204 No Content for success
        except Exception as e:
            logger.error(f"Discord notification failed: {e}")
            return False

    def notify_drafts_ready(self, draft_count: int):
        message = f"🚀 *New Drafts Ready for Review!*\n\nGenerated *{draft_count}* new LinkedIn post drafts.\n\n🔗 Open Dashboard: http://localhost:8501"
        
        logger.info("Sending notifications...")
        t_success = self.send_telegram(message)
        d_success = self.send_discord(message)
        
        if t_success or d_success:
            logger.success("Notifications sent successfully!")
        else:
            logger.warning("All notifications failed (check your .env settings).")
