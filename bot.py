from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from database import init_db

from handlers.start import start

from handlers.callbacks import (
    get_video_callback,
    check_membership_callback,
)

from handlers.admin import (
    admin_panel,
    admin_menu_callback,
)

from handlers.admin_sites import (
    sites_list,
    site_add_start,
    site_add_message,
    site_remove_start,
    site_delete,
)


# ==========================================
# شروع ربات
# ==========================================

async def post_init(application: Application):

    await init_db()

    print("✅ Database initialized")


# ==========================================
# اجرای ربات
# ==========================================

def main():

    if not BOT_TOKEN:

        raise ValueError(
            "❌ BOT_TOKEN تنظیم نشده است."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # ======================================
    # دستورات
    # ======================================

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "admin",
            admin_panel
        )
    )

    # ======================================
    # دریافت ویدیو
    # ======================================

    application.add_handler(
        CallbackQueryHandler(
            get_video_callback,
            pattern="^get_video$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            check_membership_callback,
            pattern="^check_membership$"
        )
    )

    # ======================================
    # پنل مدیریت اصلی
    # ======================================

    application.add_handler(
        CallbackQueryHandler(
            admin_menu_callback,
            pattern="^admin_"
        )
    )

    # ======================================
    # مدیریت سایت‌ها
    # ======================================

    application.add_handler(
        CallbackQueryHandler(
            site_add_start,
            pattern="^site_add$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            sites_list,
            pattern="^site_list$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            site_remove_start,
            pattern="^site_remove$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            site_delete,
            pattern="^site_delete_"
        )
    )

    # ======================================
    # دریافت پیام هنگام افزودن سایت
    # ======================================

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            site_add_message
        )
    )

    # ======================================
    # اجرای Polling
    # ======================================

    print(
        "🤖 SPR Video Bot is running..."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# ==========================================
# اجرای اصلی
# ==========================================

if __name__ == "__main__":

    main()
