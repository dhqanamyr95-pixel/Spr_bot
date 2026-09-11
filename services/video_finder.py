from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse


# ==========================================
# اطلاعات ویدیو
# ==========================================

@dataclass
class VideoInfo:

    title: str
    url: str
    duration: int
    thumbnail: Optional[str] = None


# حداکثر زمان ویدیو: ۴ دقیقه
MAX_DURATION = 4 * 60


# ==========================================
# بررسی URL
# ==========================================

def is_valid_url(url: str) -> bool:

    try:

        parsed = urlparse(url)

        return (
            parsed.scheme in (
                "http",
                "https"
            )
            and bool(parsed.netloc)
        )

    except Exception:

        return False


# ==========================================
# بررسی مدت ویدیو
# ==========================================

def is_allowed_duration(
    duration: int
) -> bool:

    return (
        0 < duration <= MAX_DURATION
    )


# ==========================================
# پیدا کردن ویدیو
# ==========================================

async def find_video(
    source_url: str
) -> Optional[VideoInfo]:

    # بررسی آدرس سایت
    if not is_valid_url(source_url):

        return None

    # --------------------------------------
    # این قسمت بعداً به سرویس/روش مجاز
    # هر سایت متصل می‌شود.
    # --------------------------------------

    return None
