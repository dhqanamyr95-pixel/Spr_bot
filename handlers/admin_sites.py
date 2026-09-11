from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import ADMIN_ID
from database import (
    add_source,
    get_sources,
    remove_source,
)


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# ==========================================
# نمایش مدیریت سایت‌ها
# ==========================================

async def sites_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        await query.answer(
            "❌ شما اجازه دسترسی ندارید.",
            show_alert=True
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "➕ افزودن سایت",
                callback_data="site_add"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 لیست سایت‌ها",
                callback_data="site_list"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 حذف سایت",
                callback_data="site_remove"
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
        "🌐 مدیریت سایت‌ها\n\n"
        "از منوی زیر یک گزینه را انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# لیست سایت‌ها
# ==========================================

async def sites_list(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    sources = await get_sources()

    if not sources:
        text = (
            "📋 لیست سایت‌ها\n\n"
            "❌ هنوز هیچ سایتی اضافه نشده است."
        )
    else:
        text = "📋 لیست سایت‌های ثبت‌شده:\n\n"

        for source in sources:
            source_id = source[0]
            name = source[1]
            url = source[2]

            text += (
                f"🆔 {source_id}\n"
                f"🌐 {name}\n"
                f"🔗 {url}\n\n"
            )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 برگشت",
                callback_data="admin_sites"
            )
        ]
    ]

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# شروع افزودن سایت
# ==========================================

async def site_add_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    context.user_data["adding_site"] = True
    context.user_data["adding_site_step"] = "name"

    await query.edit_message_text(
        "➕ افزودن سایت\n\n"
        "مرحله ۱ از ۲\n\n"
        "نام سایت را ارسال کن.\n\n"
        "مثال:\n"
        "Aparat"
    )


# ==========================================
# دریافت اطلاعات سایت
# ==========================================

async def site_add_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not is_admin(user.id):
        return

    if not context.user_data.get("adding_site"):
        return

    text = update.message.text.strip()

    step = context.user_data.get(
        "adding_site_step"
    )

    # -----------------------------
    # دریافت نام سایت
    # -----------------------------

    if step == "name":

        context.user_data["site_name"] = text
        context.user_data["adding_site_step"] = "url"

        await update.message.reply_text(
            "✅ نام سایت دریافت شد.\n\n"
            "مرحله ۲ از ۲\n\n"
            "حالا آدرس سایت را ارسال کن.\n\n"
            "مثال:\n"
            "https://example.com"
        )

        return

    # -----------------------------
    # دریافت آدرس سایت
    # -----------------------------

    if step == "url":

        site_name = context.user_data.get(
            "site_name"
        )

        site_url = text

        if not (
            site_url.startswith("http://")
            or site_url.startswith("https://")
        ):
            await update.message.reply_text(
                "❌ آدرس سایت معتبر نیست.\n\n"
                "آدرس باید با http:// یا https:// شروع شود."
            )
            return

        try:

            source_id = await add_source(
                name=site_name,
                url=site_url
            )

            context.user_data.pop(
                "adding_site",
                None
            )

            context.user_data.pop(
                "adding_site_step",
                None
            )

            context.user_data.pop(
                "site_name",
                None
            )

            await update.message.reply_text(
                "✅ سایت با موفقیت اضافه شد!\n\n"
                f"🌐 نام: {site_name}\n"
                f"🔗 آدرس: {site_url}\n"
                f"🆔 شناسه: {source_id}"
            )

        except Exception as error:

            print(
                f"Add site error: {error}"
            )

            await update.message.reply_text(
                "❌ هنگام ذخیره سایت مشکلی پیش آمد."
            )


# ==========================================
# شروع حذف سایت
# ==========================================

async def site_remove_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    sources = await get_sources()

    if not sources:

        await query.edit_message_text(
            "🗑 حذف سایت\n\n"
            "❌ هیچ سایتی برای حذف وجود ندارد.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 برگشت",
                        callback_data="admin_sites"
                    )
                ]
            ])
        )

        return

    keyboard = []

    for source in sources:

        source_id = source[0]
        name = source[1]

        keyboard.append([
            InlineKeyboardButton(
                f"🗑 {name}",
                callback_data=f"site_delete_{source_id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "🔙 برگشت",
            callback_data="admin_sites"
        )
    ])

    await query.edit_message_text(
        "🗑 حذف سایت\n\n"
        "سایتی که می‌خواهی حذف شود را انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================================
# حذف سایت
# ==========================================

async def site_delete(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    if not is_admin(update.effective_user.id):
        return

    try:

        source_id = int(
            query.data.replace(
                "site_delete_",
                ""
            )
        )

        await remove_source(source_id)

        await query.edit_message_text(
            "✅ سایت با موفقیت حذف شد.",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🌐 مدیریت سایت‌ها",
                        callback_data="admin_sites"
                    )
                ]
            ])
        )

    except Exception as error:

        print(
            f"Delete site error: {error}"
        )

        await query.edit_message_text(
            "❌ هنگام حذف سایت مشکلی پیش آمد."
  )
