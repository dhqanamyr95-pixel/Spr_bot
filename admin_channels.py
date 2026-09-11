from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID
from database import (
    add_channel,
    get_channels,
    remove_channel,
)


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# ==========================================
# منوی مدیریت کانال‌ها
# ==========================================

async def channels_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "➕ افزودن کانال",
                callback_data="channel_add"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 لیست کانال‌ها",
                callback_data="channel_list"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 حذف کانال",
                callback_data="channel_remove"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 بازگشت",
                callback_data="admin_back"
            )
        ],
    ]

    await query.edit_message_text(
        "📢 مدیریت کانال‌های تبلیغاتی\n\n"
        "از منوی زیر یک گزینه را انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# لیست کانال‌ها
# ==========================================

async def channels_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    channels = await get_channels()

    if not channels:

        text = (
            "📋 لیست کانال‌ها\n\n"
            "❌ هنوز هیچ کانالی اضافه نشده است."
        )

    else:

        text = "📋 کانال‌های تبلیغاتی:\n\n"

        for channel in channels:

            channel_id = channel[1]
            title = channel[2]
            invite_link = channel[3]

            text += (
                f"🆔 {channel_id}\n"
                f"📢 {title}\n"
                f"🔗 {invite_link}\n\n"
            )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 برگشت",
                callback_data="admin_channels"
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# شروع افزودن کانال
# ==========================================

async def channel_add_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    context.user_data["adding_channel"] = True
    context.user_data["adding_channel_step"] = "id"

    await query.edit_message_text(
        "➕ افزودن کانال\n\n"
        "مرحله ۱ از ۳\n\n"
        "آیدی کانال را ارسال کن.\n\n"
        "مثال:\n"
        "@my_channel\n\n"
        "یا اگر کانال Private است، شناسه عددی آن را وارد کن."
    )


# ==========================================
# دریافت اطلاعات کانال
# ==========================================

async def channel_add_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_admin(user.id):
        return

    if not context.user_data.get("adding_channel"):
        return

    text = update.message.text.strip()

    step = context.user_data.get(
        "adding_channel_step"
    )

    # --------------------------------------
    # مرحله ۱: آیدی کانال
    # --------------------------------------

    if step == "id":

        context.user_data["channel_id"] = text
        context.user_data["adding_channel_step"] = "title"

        await update.message.reply_text(
            "✅ آیدی کانال دریافت شد.\n\n"
            "مرحله ۲ از ۳\n\n"
            "نام کانال را ارسال کن.\n\n"
            "مثال:\n"
            "کانال تبلیغاتی SPR"
        )

        return

    # --------------------------------------
    # مرحله ۲: نام کانال
    # --------------------------------------

    if step == "title":

        context.user_data["channel_title"] = text
        context.user_data["adding_channel_step"] = "link"

        await update.message.reply_text(
            "✅ نام کانال دریافت شد.\n\n"
            "مرحله ۳ از ۳\n\n"
            "لینک عضویت کانال را ارسال کن.\n\n"
            "مثال:\n"
            "https://t.me/my_channel"
        )

        return

    # --------------------------------------
    # مرحله ۳: لینک
    # --------------------------------------

    if step == "link":

        channel_id = context.user_data.get(
            "channel_id"
        )

        channel_title = context.user_data.get(
            "channel_title"
        )

        invite_link = text

        if not (
            invite_link.startswith(
                "https://t.me/"
            )
            or invite_link.startswith(
                "http://t.me/"
            )
        ):

            await update.message.reply_text(
                "❌ لینک معتبر نیست.\n\n"
                "لینک باید مثل این باشد:\n"
                "https://t.me/example"
            )

            return

        try:

            await add_channel(
                channel_id=channel_id,
                title=channel_title,
                invite_link=invite_link
            )

            context.user_data.pop(
                "adding_channel",
                None
            )

            context.user_data.pop(
                "adding_channel_step",
                None
            )

            context.user_data.pop(
                "channel_id",
                None
            )

            context.user_data.pop(
                "channel_title",
                None
            )

            await update.message.reply_text(
                "✅ کانال با موفقیت اضافه شد!\n\n"
                f"🆔 آیدی: {channel_id}\n"
                f"📢 نام: {channel_title}\n"
                f"🔗 لینک: {invite_link}"
            )

        except Exception as error:

            print(
                f"Add channel error: {error}"
            )

            await update.message.reply_text(
                "❌ هنگام ذخیره کانال مشکلی پیش آمد."
            )


# ==========================================
# شروع حذف کانال
# ==========================================

async def channel_remove_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    channels = await get_channels()

    if not channels:

        await query.edit_message_text(
            "🗑 حذف کانال\n\n"
            "❌ هیچ کانالی برای حذف وجود ندارد.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 برگشت",
                        callback_data="admin_channels"
                    )
                ]
            ])
        )

        return

    keyboard = []

    for channel in channels:

        channel_id = channel[1]
        title = channel[2]

        keyboard.append([
            InlineKeyboardButton(
                f"🗑 {title}",
                callback_data=f"channel_delete_{channel_id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "🔙 برگشت",
            callback_data="admin_channels"
        )
    ])

    await query.edit_message_text(
        "🗑 حذف کانال\n\n"
        "کانالی که می‌خواهی حذف شود را انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# حذف کانال
# ==========================================

async def channel_delete(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    try:

        channel_id = query.data.replace(
            "channel_delete_",
            ""
        )

        await remove_channel(
            channel_id
        )

        await query.edit_message_text(
            "✅ کانال با موفقیت حذف شد.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📢 مدیریت کانال‌ها",
                        callback_data="admin_channels"
                    )
                ]
            ])
        )

    except Exception as error:

        print(
            f"Delete channel error: {error}"
        )

        await query.edit_message_text(
            "❌ هنگام حذف کانال مشکلی پیش آمد."
  )
