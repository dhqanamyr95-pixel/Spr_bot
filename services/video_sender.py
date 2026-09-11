import asyncio

from telegram import Bot


# ==========================================
# ارسال ویدیو و حذف خودکار
# ==========================================

async def send_temporary_video(
    bot: Bot,
    chat_id: int,
    file_id: str,
    caption: str = ""
):

    # ارسال ویدیو
    video_message = await bot.send_video(
        chat_id=chat_id,
        video=file_id,
        caption=caption
    )

    # پیام هشدار
    warning_message = await bot.send_message(
        chat_id=chat_id,
        text="⏱ این ویدیو تا ۱ دقیقه دیگر حذف خواهد شد."
    )

    # صبر به مدت ۱ دقیقه
    await asyncio.sleep(60)

    # حذف ویدیو
    try:

        await bot.delete_message(
            chat_id=chat_id,
            message_id=video_message.message_id
        )

    except Exception as error:

        print(
            f"Video delete error: {error}"
        )

    # حذف پیام هشدار
    try:

        await bot.delete_message(
            chat_id=chat_id,
            message_id=warning_message.message_id
        )

    except Exception as error:

        print(
            f"Warning delete error: {error}"
        )

    return True
