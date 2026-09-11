from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# ==========================================
# پنل مدیریت
# ==========================================

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
        "از منوی زیر یک گزینه را انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# مدیریت منوی ادمین
# ==========================================

async def admin_menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    user = update.effective_user

    if not is_admin(user.id):
        await query.answer(
            "❌ دسترسی ندارید.",
            show_alert=True
        )
        return

    await query.answer()

    # مدیریت سایت‌ها
    if query.data == "admin_sites":

        from handlers.admin_sites import sites_menu

        await sites_menu(
            update,
            context
        )

        return

    # مدیریت کانال‌ها
    if query.data == "admin_channels":

        from handlers.admin_channels import channels_menu

        await channels_menu(
            update,
            context
        )

        return

    # مدیریت ویدیوها
    if query.data == "admin_videos":

        await query.edit_message_text(
            "🎬 مدیریت ویدیوها\n\n"
            "این بخش را در مرحله بعد تکمیل می‌کنیم."
        )

        return

    # آمار ربات
    if query.data == "admin_stats":

        await query.edit_message_text(
            "📊 آمار ربات\n\n"
            "این بخش را در مرحله بعد تکمیل می‌کنیم."
        )

        return

    # بازگشت به پنل
    if query.data == "admin_back":

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

        await query.edit_message_text(
            "⚙️ پنل مدیریت SPR\n\n"
            "از منوی زیر یک گزینه را انتخاب کن:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
