from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

from config import MAX_VIDEO_DURATION


@dataclass
class VideoInfo:
    title: str
    url: str
    duration: int
    thumbnail: Optional[str] = None


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )

    except Exception:
        return False


def is_allowed_duration(duration: int) -> bool:
    return (
        0 < duration <= MAX_VIDEO_DURATION
    )


async def find_video(source_url: str) -> Optional[VideoInfo]:
    """
    هسته جستجوی ویدیو.

    فعلاً فقط URL معتبر را بررسی می‌کند.
    استخراج واقعی باید برای سایت موردنظر
    با روش مجاز همان سایت پیاده‌سازی شود.
    """

    if not is_valid_url(source_url):
        return None

    # در اینجا Provider مربوط به سایت قرار می‌گیرد.
    # فعلاً استخراج عمومی انجام نمی‌دهیم.

    return None
