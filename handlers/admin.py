from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


async def admin_panel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user

    if not is_admin(user.id):
        await update.message.reply_text(
            "❌ شما اجازه دسترسی به پنل مدیریت را ندارید."
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "🌐 مدیریت سایت‌ها",
                callback_data="admin_sites"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 مدیریت کانال‌ها",
                callback_data="admin_channels"
            )
        ],
        [
            InlineKeyboardButton(
                "🎬 مدیریت ویدیوها",
                callback_data="admin_videos"
            )
        ],
        [
            InlineKeyboardButton(
                "📊 آمار ربات",
                callback_data="admin_stats"
            )
        ],
    ]

    await update.message.reply_text(
        "⚙️ پنل مدیریت SPR\n\n"
        "یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def admin_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    user = update.effective_user

    if not is_admin(user.id):
        await query.answer(
            "❌ دسترسی ندارید.",
            show_alert=True
        )
        return

    if query.data == "admin_sites":
        await query.edit_message_text(
            "🌐 مدیریت سایت‌ها\n\n"
            "در مرحله بعد گزینه‌های افزودن و حذف سایت را اضافه می‌کنیم."
        )

    elif query.data == "admin_channels":
        await query.edit_message_text(
            "📢 مدیریت کانال‌ها\n\n"
            "در مرحله بعد افزودن و حذف کانال را اضافه می‌کنیم."
        )

    elif query.data == "admin_videos":
        await query.edit_message_text(
            "🎬 مدیریت ویدیوها\n\n"
            "مدیریت ویدیوها در مرحله بعد اضافه می‌شود."
        )

    elif query.data == "admin_stats":
        await query.edit_message_text(
            "📊 آمار ربات\n\n"
            "سیستم آمار در مرحله بعد متصل می‌شود."
        )
