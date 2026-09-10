from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import MAIN_CHANNEL_ID
from database import get_channels


async def get_video_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    channels = await get_channels()

    # اگر کانالی برای عضویت اجباری وجود نداشت
    if not channels:
        await query.message.reply_text(
            "🎬 ویدیو آماده است.\n\n"
            "در مرحله بعد ارسال ویدیو را اضافه می‌کنیم."
        )
        return

    keyboard = []

    # ساخت دکمه برای هر کانال
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

    # دکمه بررسی عضویت
    keyboard.append([
        InlineKeyboardButton(
            "✅ بررسی عضویت",
            callback_data="check_membership"
        )
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(
        "🔐 برای دریافت ویدیو ابتدا در کانال‌های زیر عضو شو:\n\n"
        "بعد از عضویت روی «✅ بررسی عضویت» بزن.",
        reply_markup=reply_markup
    )


async def check_membership_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    await query.answer()

    await query.message.edit_text(
        "🔍 در حال بررسی عضویت شما...\n\n"
        "سیستم بررسی عضویت را در فایل بعدی کامل می‌کنیم."
    )
