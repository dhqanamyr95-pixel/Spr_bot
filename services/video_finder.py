from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse


@dataclass
class VideoInfo:
    title: str
    url: str
    duration: int
    thumbnail: Optional[str] = None


MAX_DURATION = 4 * 60


def is_valid_url(url: str) -> bool:
    """بررسی ساده معتبر بودن لینک."""
    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def is_allowed_duration(duration: int) -> bool:
    """بررسی می‌کند ویدیو کمتر از ۴ دقیقه باشد."""
    return 0 < duration <= MAX_DURATION


async def find_video(source_url: str) -> Optional[VideoInfo]:
    """
    محل اتصال جست‌وجوی منبع ویدیو.

    در نسخه فعلی فقط لینک را بررسی می‌کنیم.
    بعداً منبع مجاز/رسمی را به این قسمت متصل می‌کنیم.
    """

    if not is_valid_url(source_url):
        return None

    # فعلاً نتیجه‌ای برنمی‌گردانیم.
    # منطق دریافت اطلاعات ویدیو در مرحله بعد اضافه می‌شود.
    return None
