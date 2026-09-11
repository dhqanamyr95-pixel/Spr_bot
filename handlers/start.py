from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import WELCOME_TEXT
from database import (
    add_user,
    set_user_video_request,
)


# ==========================================
# /start
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    # ثبت کاربر
    await add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

    # ======================================
    # دریافت video_id از لینک
    #
    # مثال:
    # /start video_15
    # ======================================

    if context.args:

        argument = context.args[0]

        if argument.startswith("video_"):

            try:

                video_id = int(
                    argument.replace(
                        "video_",
                        "",
                        1
                    )
                )

                await set_user_video_request(
                    user_id=user.id,
                    video_id=video_id
                )

            except ValueError:

                pass

    # ======================================
    # دکمه دریافت ویدیو
    # ======================================

    keyboard = [
        [
            InlineKeyboardButton(
                "👀 دریافت ویدیو",
                callback_data="get_video"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=reply_markup
  )
