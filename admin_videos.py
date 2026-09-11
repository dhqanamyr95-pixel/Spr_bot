from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID, MAIN_CHANNEL_ID
from database import add_video


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


async def videos_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        await query.answer(
            "❌ دسترسی ندارید.",
            show_alert=True
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "➕ ثبت ویدیو",
                callback_data="video_add"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ]
    ]

    await query.edit_message_text(
        "🎬 مدیریت ویدیوها\n\n"
        "از منوی زیر انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def video_add_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    context.user_data["adding_video"] = True

    await query.edit_message_text(
        "➕ ثبت ویدیو\n\n"
        "حالا ویدیو را همینجا برای ربات ارسال کن."
    )


async def video_add_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user

    if not is_admin(user.id):
        return

    if not context.user_data.get("adding_video"):
        return

    if not update.message.video:
        await update.message.reply_text(
            "❌ لطفاً فقط یک فایل ویدیویی ارسال کن."
        )
        return

    video = update.message.video

    file_id = video.file_id
    duration = video.duration or 0

    if duration > 4 * 60:
        await update.message.reply_text(
            "❌ این ویدیو بیشتر از ۴ دقیقه است."
        )
        return

    context.user_data["video_file_id"] = file_id
    context.user_data["video_duration"] = duration
    context.user_data["adding_video"] = False

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 انتشار در کانال",
                callback_data="video_publish"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ لغو",
                callback_data="video_cancel"
            )
        ]
    ]

    await update.message.reply_text(
        "✅ ویدیو دریافت شد.\n\n"
        f"⏱ مدت: {duration // 60}:{duration % 60:02d}\n\n"
        "آیا می‌خواهی در کانال اصلی منتشر شود؟",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def video_publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    file_id = context.user_data.get("video_file_id")
    duration = context.user_data.get("video_duration", 0)

    if not file_id:
        await query.edit_message_text(
            "❌ ویدیویی برای انتشار وجود ندارد."
        )
        return

    if not MAIN_CHANNEL_ID:
        await query.edit_message_text(
            "❌ MAIN_CHANNEL_ID در فایل .env تنظیم نشده است."
        )
        return

    try:
        video_id = await add_video(
            source_id=None,
            source_url=None,
            file_id=file_id,
            title="ویدیوی SPR",
            caption="",
            duration=duration
        )

        bot_username = (
            context.bot.username
        )

        deep_link = (
            f"https://t.me/{bot_username}"
            f"?start=video_{video_id}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "👀 دریافت ویدیو",
                    url=deep_link
                )
            ]
        ])

        await context.bot.send_message(
            chat_id=MAIN_CHANNEL_ID,
            text=(
                "🎬 ویدیوی جدید SPR\n\n"
                "👀 برای دیدن ویدیو روی دکمه زیر کلیک کنید."
            ),
            reply_markup=keyboard
        )

        context.user_data.pop("video_file_id", None)
        context.user_data.pop("video_duration", None)

        await query.edit_message_text(
            "✅ ویدیو با موفقیت در کانال منتشر شد.\n\n"
            f"🆔 شناسه ویدیو: {video_id}"
        )

    except Exception as error:
        print(f"Video publish error: {error}")

        await query.edit_message_text(
            "❌ هنگام انتشار ویدیو مشکلی پیش آمد."
        )


async def video_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    context.user_data.pop("video_file_id", None)
    context.user_data.pop("video_duration", None)
    context.user_data.pop("adding_video", None)

    await query.edit_message_text(
        "❌ ثبت ویدیو لغو شد."
      )
