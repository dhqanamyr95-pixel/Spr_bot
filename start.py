from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import WELCOME_TEXT
from database import add_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # ثبت کاربر در دیتابیس
    await add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "👀 دریافت ویدیو",
                callback_data="get_video"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=reply_markup
    )
