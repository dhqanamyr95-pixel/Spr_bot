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
from handlers.admin_channels import (
    channels_menu,
    channels_list,
    channel_add_start,
    channel_add_message,
    channel_remove_start,
    channel_delete,
)

from handlers.admin_videos import (
    videos_menu,
    video_add_start,
    video_add_message,
    video_publish,
    video_cancel,
)


async def post_init(application: Application):
    await init_db()
    print("✅ Database initialized")


async def admin_text_message(update: Update, context):
    if context.user_data.get("adding_site"):
        await site_add_message(update, context)
        return

    if context.user_data.get("adding_channel"):
        await channel_add_message(update, context)
        return


async def admin_video_message(update: Update, context):
    if context.user_data.get("adding_video"):
        await video_add_message(update, context)


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
    # Commands
    # =========================

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("admin", admin_panel)
    )

    # =========================
    # User callbacks
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
    # Admin menu
    # =========================

    application.add_handler(
        CallbackQueryHandler(
            admin_menu_callback,
            pattern="^admin_"
        )
    )

    # =========================
    # Site management
    # =========================

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

    # =========================
    # Channel management
    # =========================

    application.add_handler(
        CallbackQueryHandler(
            channels_menu,
            pattern="^admin_channels$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            channels_list,
            pattern="^channel_list$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            channel_add_start,
            pattern="^channel_add$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            channel_remove_start,
            pattern="^channel_remove$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            channel_delete,
            pattern="^channel_delete_"
        )
    )

    # =========================
    # Video management
    # =========================

    application.add_handler(
        CallbackQueryHandler(
            videos_menu,
            pattern="^admin_videos$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            video_add_start,
            pattern="^video_add$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            video_publish,
            pattern="^video_publish$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            video_cancel,
            pattern="^video_cancel$"
        )
    )

    # =========================
    # Admin text
    # =========================

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            admin_text_message
        )
    )

    # =========================
    # Admin video
    # =========================

    application.add_handler(
        MessageHandler(
            filters.VIDEO,
            admin_video_message
        )
    )

    # =========================
    # Start
    # =========================

    print("🤖 SPR Video Bot is running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
