import asyncio

from telegram import Bot


async def send_temporary_video(
    bot: Bot,
    chat_id: int,
    file_id: str,
    caption: str = ""
):
    # ارسال ویدیو
    message = await bot.send_video(
        chat_id=chat_id,
        video=file_id,
        caption=caption
    )

    # پیام اطلاع‌رسانی
    warning_message = await bot.send_message(
        chat_id=chat_id,
        text="⏱ این ویدیو تا ۱ دقیقه دیگر حذف خواهد شد."
    )

    # انتظار ۶۰ ثانیه
    await asyncio.sleep(60)

    # حذف ویدیو
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=message.message_id
        )
    except Exception as error:
        print(f"Video delete error: {error}")

    # حذف پیام اطلاع‌رسانی
    try:
        await bot.delete_message(
            chat_id=chat_id,
            message_id=warning_message.message_id
        )
    except Exception as error:
        print(f"Warning delete error: {error}")

    return True
