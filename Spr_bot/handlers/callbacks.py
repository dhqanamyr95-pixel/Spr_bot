from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import get_channels
from services.membership import check_user_membership


# ==========================================
# دکمه دریافت ویدیو
# ==========================================

async def get_video_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    channels = await get_channels()

    if not channels:

        await query.message.edit_text(
            "🎬 هنوز ویدیویی برای دریافت آماده نشده است."
        )

        return

    keyboard = []

    for channel in channels:

        channel_id = channel[1]
        title = channel[2]
        invite_link = channel[3]

        keyboard.append([
            InlineKeyboardButton(
                f"📢 عضویت در {title}",
                url=invite_link
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "✅ بررسی عضویت",
            callback_data="check_membership"
        )
    ])

    await query.message.edit_text(
        "🔐 برای دریافت ویدیو ابتدا در کانال‌های زیر عضو شو:\n\n"
        "بعد از عضویت روی «✅ بررسی عضویت» بزن.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# بررسی عضویت
# ==========================================

async def check_membership_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    user = update.effective_user

    await query.answer()

    is_member = await check_user_membership(
        user_id=user.id,
        context=context
    )

    # --------------------------------------
    # اگر عضو همه کانال‌ها نیست
    # --------------------------------------

    if not is_member:

        channels = await get_channels()

        keyboard = []

        for channel in channels:

            title = channel[2]
            invite_link = channel[3]

            keyboard.append([
                InlineKeyboardButton(
                    f"📢 عضویت در {title}",
                    url=invite_link
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                "🔄 دوباره بررسی کن",
                callback_data="check_membership"
            )
        ])

        await query.message.edit_text(
            "❌ هنوز در همه کانال‌ها عضو نشده‌ای.\n\n"
            "ابتدا در کانال‌های بالا عضو شو و سپس "
            "روی «🔄 دوباره بررسی کن» بزن.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    # --------------------------------------
    # اگر عضو همه کانال‌هاست
    # --------------------------------------

    await query.message.edit_text(
        "✅ عضویت شما تأیید شد!\n\n"
        "🎬 آماده دریافت ویدیو هستیم.\n\n"
        "سیستم ارسال ویدیو را در مرحله بعد وصل می‌کنیم."
    )
