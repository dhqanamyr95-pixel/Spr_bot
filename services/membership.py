from telegram.ext import ContextTypes

from database import get_channels


# ==========================================
# بررسی عضویت کاربر در کانال‌ها
# ==========================================

async def check_user_membership(
    user_id: int,
    context: ContextTypes.DEFAULT_TYPE
) -> bool:

    channels = await get_channels()

    # اگر هیچ کانالی تعریف نشده باشد
    if not channels:
        return True

    for channel in channels:

        channel_id = channel[1]

        try:

            member = await context.bot.get_chat_member(
                chat_id=channel_id,
                user_id=user_id
            )

            # وضعیت‌های قابل قبول
            if member.status in (
                "member",
                "administrator",
                "creator"
            ):
                continue

            # کاربر عضو نیست
            return False

        except Exception as error:

            print(
                f"Membership check error "
                f"for {channel_id}: {error}"
            )

            return False

    # عضو همه کانال‌هاست
    return True
