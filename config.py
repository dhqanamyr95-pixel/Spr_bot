import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# Telegram Bot
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# آیدی عددی ادمین اصلی ربات
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


# =========================
# Main Channel
# =========================

# آیدی کانالی که پست‌های اصلی در آن منتشر می‌شوند
MAIN_CHANNEL_ID = os.getenv("MAIN_CHANNEL_ID", "")


# =========================
# Video Settings
# =========================

# مدت زمان مجاز ویدیو بر حسب ثانیه
MAX_VIDEO_DURATION = 4 * 60

# مدت زمانی که ویدیو برای کاربر باقی می‌ماند
VIDEO_DELETE_AFTER = 60


# =========================
# Database
# =========================

DATABASE_NAME = "bot.db"


# =========================
# General Settings
# =========================

BOT_NAME = "SPR Video Bot"

WELCOME_TEXT = """
👋 به ربات SPR خوش آمدید.

برای دریافت ویدیو ابتدا عضویت خود را در کانال‌های مشخص‌شده تأیید کنید.
"""

VIDEO_EXPIRE_TEXT = """
⏱ این ویدیو تا ۱ دقیقه دیگر حذف خواهد شد.
"""

REQUIRED_CHANNELS = []
