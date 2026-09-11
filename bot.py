from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
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


async def post_init(application: Application):
    await init_db()
    print("✅ Database initialized")


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

    # =========================
    # User commands
    # =========================

    application.add_handler(
        CommandHandler("start", start)
    )

    # =========================
    # Admin
    # =========================

    application.add_handler(
        CommandHandler("admin", admin_panel)
    )

    # =========================
    # User buttons
    # =========================

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

    # =========================
    # Admin buttons
    # =========================

    application.add_handler(
        CallbackQueryHandler(
            admin_menu_callback,
            pattern="^admin_"
        )
    )

    print("🤖 SPR Video Bot is running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
