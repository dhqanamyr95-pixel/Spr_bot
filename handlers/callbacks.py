from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database import (
    get_channels,
    get_video,
    get_user_video_request,
)

from services.membership import check_user_membership
from services.video_sender import send_temporary_video


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
            "🎬 در حال حاضر کانالی برای بررسی عضویت تنظیم نشده است."
        )

        return

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
    # کاربر عضو همه کانال‌ها نیست
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
            "ابتدا عضو کانال‌ها شو و دوباره بررسی کن.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return

    # --------------------------------------
    # عضویت تأیید شد
    # --------------------------------------

    video_id = await get_user_video_request(
        user.id
    )

    # اگر ویدیوی مشخصی برای کاربر ثبت نشده
    if not video_id:

        await query.message.edit_text(
            "⚠️ ویدیوی درخواستی پیدا نشد.\n\n"
            "لطفاً دوباره از لینک دریافت ویدیو وارد شو."
        )

        return

    # --------------------------------------
    # دریافت اطلاعات ویدیو
    # --------------------------------------

    video = await get_video(
        video_id
    )

    if not video:

        await query.message.edit_text(
            "❌ این ویدیو دیگر در دسترس نیست."
        )

        return

    # ساختار video:
    # id
    # source_id
    # source_url
    # file_id
    # title
    # caption
    # duration

    file_id = video[3]
    title = video[4]
    caption = video[5]
    duration = video[6]

    if not file_id:

        await query.message.edit_text(
            "❌ فایل ویدیو هنوز آماده ارسال نیست."
        )

        return

    # --------------------------------------
    # حذف پیام بررسی عضویت
    # --------------------------------------

    try:

        await query.message.delete()

    except Exception as error:

        print(
            f"Message delete error: {error}"
        )

    # --------------------------------------
    # آماده‌سازی کپشن
    # --------------------------------------

    final_caption = ""

    if title:

        final_caption += (
            f"🎬 {title}\n"
        )

    if caption:

        final_caption += (
            f"\n{caption}"
        )

    if duration:

        final_caption += (
            f"\n\n⏱ مدت ویدیو: "
            f"{duration // 60}:{duration % 60:02d}"
        )

    # --------------------------------------
    # ارسال ویدیو
    # --------------------------------------

    await send_temporary_video(
        bot=context.bot,
        chat_id=user.id,
        file_id=file_id,
        caption=final_caption.strip()
    )
